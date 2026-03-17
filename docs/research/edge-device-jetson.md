# Edge 디바이스: NVIDIA Jetson 가이드

**작성일:** 2026-02-24
**관련 문서:** [시스템 구성도](../system-architecture.md)

---

## 1. Jetson이란

NVIDIA가 만든 **소형 AI 전용 컴퓨터**. 신용카드~손바닥 크기의 보드에 NVIDIA GPU가 내장되어 있어서, 현장에 설치해 AI 추론을 수행하는 Edge 디바이스.

**핵심: GPU가 붙어있는 소형 리눅스 컴퓨터.** 일반 Ubuntu Linux가 돌아가며, SSH 접속, Python 코드 실행 등 일반 리눅스 서버와 동일하게 사용.

---

## 2. 제품 라인업

| 모델 | GPU 성능 | RAM | 전력 | 가격대 | 카메라 처리량 |
|------|---------|-----|------|-------|-------------|
| Orin Nano | 40 TOPS | 8GB | 7-15W | ~$249 | 1-2대 |
| Orin NX | 100 TOPS | 16GB | 10-25W | ~$599 | 2-3대 |
| **AGX Orin** | **275 TOPS** | **32-64GB** | **15-60W** | **~$999-1999** | **5-8대** |

> Watch Tower 시스템에서는 **AGX Orin 32GB × 2대** (각 5카메라 담당)를 채택.

---

## 3. OS 및 실행 환경

### 3.1 운영체제

```
$ uname -a
Linux jetson-agx-orin 5.15.136-tegra #1 SMP Ubuntu 22.04 aarch64 GNU/Linux

$ python3 --version
Python 3.10.12
```

| 항목 | 내용 |
|------|------|
| OS | **Ubuntu 22.04** (ARM64 버전) |
| 패키지 관리 | apt, pip, conda 모두 사용 가능 |
| 컨테이너 | Docker 지원 (NVIDIA Container Runtime) |
| SSH | 일반 리눅스와 동일하게 원격 접속 |
| 파일시스템 | ext4, NVMe SSD 장착 가능 |

### 3.2 JetPack SDK

Jetson 구매 시 NVIDIA가 제공하는 올인원 소프트웨어 패키지. AI 추론에 필요한 모든 것이 사전 설치되어 있음.

| 포함 구성요소 | 역할 | 별도 설치 여부 |
|-------------|------|-------------|
| Ubuntu 22.04 | 운영체제 | 포함 |
| CUDA | GPU 병렬 연산 라이브러리 | 포함 |
| cuDNN | 딥러닝 연산 가속 | 포함 |
| TensorRT | 모델 최적화/양자화 (INT8) | 포함 |
| DeepStream | 멀티스트림 영상 파이프라인 | 포함 |
| NVDEC/NVENC | HW 영상 디코딩/인코딩 | 포함 |
| VPI (Vision Programming Interface) | 영상 전처리 가속 | 포함 |

### 3.3 일반 리눅스 서버와의 차이

| | 일반 리눅스 서버 | Jetson |
|---|---|---|
| CPU 아키텍처 | x86_64 (Intel/AMD) | **ARM64 (ARM Cortex)** |
| GPU | 별도 카드 (PCIe) | **보드에 내장** |
| GPU 드라이버 | 별도 설치 | JetPack에 포함 |
| CUDA/TensorRT | 별도 설치 | JetPack에 포함 |
| pip 패키지 | 그대로 설치 | 대부분 동일. 일부 ARM 빌드 필요 |
| Docker | 동일 | `--runtime=nvidia` 옵션으로 GPU 접근 |
| 크기/전력 | 랙마운트, 수백W | 손바닥 크기, 15-60W |

> **ARM64 주의사항:** 대부분의 Python 패키지(ultralytics, opencv, numpy 등)는 ARM64 빌드를 제공하지만, 일부 C 확장 패키지는 ARM64용 wheel이 없어 소스 빌드가 필요할 수 있음.

---

## 4. 애플리케이션 실행 방법

### 4.1 직접 실행

```bash
# SSH 접속
ssh user@192.168.1.100

# 프로젝트 배포
git clone <repo-url> /opt/watch-tower
cd /opt/watch-tower

# 의존성 설치
pip install -e .

# 애플리케이션 실행
python3 -m watch_tower.edge_node --cameras rtsp://cam01,rtsp://cam02,...
```

### 4.2 Docker 실행

```bash
# NVIDIA Container Runtime으로 GPU 접근
docker run --runtime=nvidia \
  --device /dev/video0 \
  -v /opt/watch-tower/config:/app/config \
  watch-tower-edge:latest
```

### 4.3 시스템 서비스 등록 (부팅 시 자동 실행)

```ini
# /etc/systemd/system/watch-tower.service
[Unit]
Description=Watch Tower Edge Node
After=network.target

[Service]
Type=simple
User=watchtower
ExecStart=/usr/bin/python3 -m watch_tower.edge_node
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
```

```bash
sudo systemctl enable watch-tower.service
sudo systemctl start watch-tower.service
```

---

## 5. Edge 배치 구성 (대안 비교)

Jetson Edge 방식만이 유일한 선택지는 아님. 네트워크 환경에 따라 중앙 GPU 서버 구성도 가능.

### 5.1 구성 대안

```
옵션 A: Jetson Edge 분산            옵션 B: 중앙 GPU 서버
────────────────────               ──────────────────────

현장                                현장
┌──────────────┐                    ┌──────────────┐
│ CAM 01~05    │                    │ CAM 01~10    │
│      │       │                    │      │       │
│ Jetson AGX A │ ← 현장에서 AI 추론  │      │       │ ← AI 추론 없음
│ CAM 06~10    │                    │      │       │
│      │       │                    └──────┼───────┘
│ Jetson AGX B │ ← 현장에서 AI 추론         │
└──────┬───────┘                    RTSP 10채널 전송
       │ 이벤트만                          │ ~40-80 Mbps
       │ ~0.5 Mbps                        │
       ▼                                  ▼
   중앙 서버                       중앙 GPU 서버
   (API/DB만)                      (RTX 4090 등)
                                   AI 추론 + API/DB
```

### 5.2 비교표

| | **A. Jetson Edge (채택안)** | **B. 중앙 GPU 서버** | **C. 클라우드 GPU** |
|---|---|---|---|
| 장비 | Jetson AGX Orin × 2 | GPU 서버 1대 (RTX 4090 등) | AWS/GCP GPU 인스턴스 |
| 초기 비용 | ~$2,000 | ~$3,000-5,000 | 없음 |
| 운영 비용 | 전기만 (저전력) | 전기 + 서버실 | ~$1-3/시간 (종량) |
| 현장↔중앙 대역폭 | **~0.5 Mbps (이벤트만)** | ~40-80 Mbps (영상 전체) | ~40-80 Mbps |
| 네트워크 단절 시 | **현장 독립 동작** | **전체 중단** | **전체 중단** |
| 감지 지연 | ~0.3초 (로컬) | ~0.5-1초 | ~1-3초 |
| 장비 관리 | 현장 방문 필요 | 서버실 1곳 | 관리 최소 |
| 확장 | Edge 노드 추가 | GPU 추가/교체 | 인스턴스 추가 |

### 5.3 선택 기준

```
현장 → 중앙 네트워크가 100Mbps 이상 안정적인가?

  YES → 옵션 B (중앙 GPU 서버)도 가능. 장비 관리가 더 쉬움.
  NO  → 옵션 A (Jetson Edge) 권장. 건설 현장은 보통 여기에 해당.
```

> Watch Tower는 건설 현장의 불안정한 네트워크 환경을 고려하여 **옵션 A (Jetson Edge)** 를 기본 구성으로 채택.

---

## 6. 참고 링크

- [NVIDIA Jetson 공식 페이지](https://www.nvidia.com/en-us/autonomous-machines/embedded-systems/)
- [JetPack SDK 다운로드](https://developer.nvidia.com/embedded/jetpack)
- [Jetson AGX Orin 개발자 킷](https://developer.nvidia.com/embedded/jetson-agx-orin-developer-kit)
- [DeepStream SDK 문서](https://developer.nvidia.com/deepstream-sdk)
- [Jetson 커뮤니티 포럼](https://forums.developer.nvidia.com/c/agx-autonomous-machines/jetson-embedded-systems/)
