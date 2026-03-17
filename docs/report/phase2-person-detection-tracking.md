# Phase 2 종합 리포트: Person Detection + Tracking 검증

- 작성일: 2026-03-17
- 프로젝트: WatchTower (건설 현장 AI 안전 모니터링)
- 관련 이슈: FWY-47, FWY-48, FWY-52

## 1. 목적

건설 현장 CCTV 영상에서 **사람을 찾고(Detection) 추적(Tracking)** 하는 것이 실제 환경에서 가능한지 검증한다. 이것은 보호구 미착용 감지, 위험구역 침입 감지 등 모든 후속 기능의 기반이다.

## 2. 테스트한 모델

| 모델 | 출처 | 클래스 수 | 특징 |
|------|------|----------|------|
| yolo11m-construction-hazard.pt | yihong1120 | 11 | 건설현장 특화 (Person, Hardhat, Safety Vest 등) |
| yolo11m.pt | Ultralytics (COCO) | 80 | 범용 모델, 다양한 각도/환경 학습 |

## 3. 테스트 데이터

### 3-1. 정량 평가 데이터셋

| 데이터셋 | 이미지 수 | 클래스 | 용도 |
|----------|----------|--------|------|
| Construction-PPE (Ultralytics) | 1,416장 (val 143) | 11 | model.val() 정량 평가 |

**클래스 매핑 이슈**: 데이터셋과 모델의 클래스 인덱스가 불일치하여 라벨 리매핑 수행. 매핑 가능한 4개 클래스(Hardhat, Person, Safety Vest, NO-Hardhat)만 평가에 포함.

### 3-2. 정성 평가 영상

| 영상 | 해상도 | 길이 | 시점 | 특징 |
|------|--------|------|------|------|
| construction_helmets.mp4 | 1280x720 | 8초 | 눈높이/중간 | PoC 영상, 사람 가까이 보임 |
| construction_subway_cctv.mp4 | 1280x720 | 3분 21초 | 높은 조감 | 지하철 건설현장, 위에서 내려다봄 |
| construction_tower_crane_cctv.mp4 | 1280x720 | 3분 20초 | 높은 | 타워크레인 현장 |
| construction_site_cctv.mp4 | 586x480 | 1분 27초 | 중간~높음 | 건설현장 CCTV |

## 4. 테스트 결과

### 4-1. 정량 평가: Person Detection mAP (FWY-47)

Construction-PPE 데이터셋으로 yolo11m-construction-hazard 모델 평가.

| conf 임계값 | mAP@50 | Recall | Precision |
|------------|--------|--------|-----------|
| 0.25 | 77.9% | 76.2% | 76.2% |
| 0.15 | 78.7% | 78.7% | 74.3% |
| 0.10 | 78.7% | 79.5% | 71.4% |

**Go/No-Go 기준**: mAP@50 ≥ 75% (✅ 통과), Recall ≥ 80% (❌ 최대 79.5%)

**판정: 조건부 Go** — Recall이 0.5%p 차이로 경계선. val set 143장의 통계적 오차 범위.

### 4-2. 클래스별 성능 (conf=0.25)

| 클래스 | mAP@50 | Recall | Precision |
|--------|--------|--------|-----------|
| Hardhat | 65.3% | 59.7% | 72.3% |
| NO-Hardhat | 2.8% | 6.7% | 4.8% |
| Person | 77.9% | 76.2% | 76.2% |
| Safety Vest | 78.7% | 67.3% | 90.6% |

**주목**: NO-Hardhat(헬멧 미착용) 감지율이 2.8%로 극히 낮음 → Phase 4(PPE 감지)에서 중요한 리스크.

### 4-3. 정성 평가: 영상별 Detection + Tracking (FWY-48)

ByteTrack(ultralytics 내장) + supervision 시각화.

| 영상 | 시점 | hazard 모델 | COCO 모델 | 판정 |
|------|------|------------|----------|------|
| helmets | 눈높이 | ✅ 3~6명 지속 | - | 정상 |
| subway_cctv | 높은 조감 | ❌ 3회/6,019프레임 | ❌ 4회 | **둘 다 실패** |
| tower_crane | 높은 | ❌ 간헐적 | ❌ 4회 | **둘 다 실패** |
| site_cctv | 중간~높음 | ✅ 1~2명 지속 | ❌ 0회 | **hazard 승** |

### 4-4. COCO pretrained 교체 테스트 (FWY-52)

높은 각도 CCTV에서의 Detection 실패가 모델 문제인지 확인하기 위해 COCO pretrained YOLO(yolo11m.pt) 비교.

**결론: COCO 모델도 동일하게 실패.** 오히려 건설현장 특화 모델(hazard)이 나은 경우도 있음.

## 5. 발견된 이슈

### 이슈 1: 높은 각도 CCTV에서 Person 감지 실패 (Critical)

**현상**: 실제 건설현장 CCTV(높은 곳에서 내려다보는 시점)에서 사람을 거의 감지하지 못함.

**영향**: 보호구 감지, 위험구역 침입 감지 등 모든 후속 기능의 전제 조건 불충족.

**근본 원인**: 모델 선택의 문제가 아니라 **소형 객체 탐지의 한계**.
- YOLO 입력 크기 640x640 대비 사람이 수십 픽셀 수준으로 작음
- 높은 각도에서 사람의 형태가 일반적인 학습 데이터의 실루엣과 다름
- COCO pretrained도 동일하게 실패 → 학습 데이터 문제만이 아님

### 이슈 2: 클래스 인덱스 불일치 (Resolved)

**현상**: Construction-PPE 데이터셋과 모델의 클래스 인덱스가 달라 model.val() 결과가 엉뚱하게 나옴.

**해결**: 라벨 리매핑 스크립트(`scripts/remap_construction_ppe.py`) 작성하여 해결.

### 이슈 3: NO-Hardhat 감지율 극히 낮음 (Warning)

**현상**: 헬멧 미착용(NO-Hardhat) mAP@50 = 2.8%.

**영향**: Phase 4(PPE 감지)에서 "미착용" 감지가 이 모델의 약점일 수 있음. 파인튜닝 시 우선 개선 대상.

## 6. 종합 판단

```
Phase 2 Go/No-Go
═══════════════════════════════════════════

P2-1 정량 평가      → 조건부 Go (Recall 0.5%p 미달)
P2-2 정성 평가      → No-Go (높은 각도 CCTV에서 Detection 실패)
P2-1c COCO 교체     → 효과 없음 (COCO도 동일 실패)

종합 판정: No-Go — 소형 객체 탐지 문제 해결 필요
```

### 동작하는 조건

| 조건 | Person Detection | Tracking |
|------|-----------------|----------|
| 눈높이/중간 각도 + 가까운 거리 | ✅ | ✅ (ByteTrack) |
| 중간 각도 + 건설현장 배경 | ✅ | ✅ |
| 높은 각도(조감) + 먼 거리 | ❌ | 평가 불가 |
| 높은 각도 + 작은 사람 (수십px) | ❌ | 평가 불가 |

## 7. 후속 대응 방안

| 우선순위 | 옵션 | 비용 | 기대 효과 |
|---------|------|------|----------|
| 1 | **SAHI (Slicing Aided Hyper Inference)** | 낮음 | 이미지를 타일로 분할하여 추론, 작은 객체 감지 개선. 즉시 테스트 가능 |
| 2 | **고해상도 입력 (imgsz=1280)** | 낮음 | YOLO 입력 크기를 키워 작은 객체 해상도 확보. 속도 저하 있음 |
| 3 | **높은 각도 데이터로 파인튜닝** | 높음 | 시점 특화 모델 구축. SODA 등 데이터 필요 |
| 4 | **카메라 각도/위치 제한** | 운영 제약 | "중간 각도 이하에서만 동작" 제품 스펙으로 수용 |

**권장**: 1번(SAHI) → 2번(고해상도) 순서로 빠르게 테스트. 이 두 가지는 코드 변경만으로 즉시 확인 가능하며, 효과가 없을 경우 3번(파인튜닝) 또는 4번(운영 제약)으로 전환.

## 8. 관련 산출물

### 스크립트

| 스크립트 | 용도 |
|---------|------|
| `scripts/eval_person_detection.py` | 정량 평가 (model.val()) |
| `scripts/remap_construction_ppe.py` | 데이터셋 클래스 리매핑 |
| `scripts/run_tracking.py` | Detection + Tracking 정성 평가 |
| `scripts/download_video.py` | YouTube 영상 다운로드 유틸 |

### 실험 기록

| 경로 | 내용 |
|------|------|
| `experiments/2026-03-17-person-detection-eval/` | P2-1 정량 평가 결과 (report.md, results.json) |
| `experiments/2026-03-17-detection-tracking-eval/` | P2-2 정성 평가 + COCO 비교 결과 |

### Linear 이슈

| 이슈 | 상태 | 내용 |
|------|------|------|
| FWY-47 | Done | Person Detection 정량 평가 |
| FWY-48 | Done | Detection + Tracking 정성 평가 |
| FWY-51 | Backlog | SODA 독립 검증 (보류) |
| FWY-52 | Done | COCO pretrained 비교 테스트 |
