# PPE 감지 모델 개선 기술 리서치

**작성일:** 2026-02-26
**목적:** Watch Tower 시스템의 PPE 감지 정확도 및 커버리지 개선을 위한 기술 조사
**현재 모델:** yolo11m-construction-hazard (YOLO11 Medium, 11클래스, 39MB, 12 FPS on CPU)

---

## 1. 현재 시스템 문제점 요약

| 문제 | 심각도 | 설명 |
|------|--------|------|
| NO-Mask 오탐 | 중 | 마스크 미착용을 잘못 감지 (yolo11m에서 91% 감소했으나 잔존) |
| 장갑 감지 미지원 | 상 | 모델에 장갑 클래스 없음 (요구사항상 필수 감지 항목) |
| 원거리 감지율 하락 | 중 | ~15m 이상에서 Person/PPE 감지율 하락 |
| 가림(Occlusion) 시 미감지 | 중 | 자재/장비에 의해 몸 가려지면 Person 감지 실패 |

---

## 2. 최신 객체 감지 모델 비교

### 2.1 모델별 성능 비교표

| 모델 | mAP (COCO) | 추론 속도 (T4 GPU) | 파라미터 | 크기 | 라이선스 | 비고 |
|------|-----------|-------------------|---------|------|---------|------|
| **YOLO11m** (현재) | ~51% | ~84ms (CPU) | 20M | 39MB | AGPL-3.0 | 현재 사용 중 |
| **YOLOv12n** | 40.6% | 1.64ms | 2.6M | ~6MB | AGPL-3.0 | Attention 메커니즘 도입, 소형 모델 최고속 |
| **YOLOv12m** | ~52% | ~4ms | ~20M | ~40MB | AGPL-3.0 | YOLO11m 대비 유사 정확도, 속도 향상 (GPU) |
| **RF-DETR-B** | 54.7% | 4.52ms | ~33M | ~66MB | Apache 2.0 | Transformer 기반 SOTA, 파인튜닝 최적화 |
| **RT-DETR-L** | 53.0% | ~8.7ms (114 FPS) | ~32M | ~65MB | Apache 2.0 | NMS 불필요, 디코더 레이어로 속도 조절 가능 |
| **YOLO-World-L** | 35.4 AP (LVIS) | ~19ms (52 FPS) | ~48M | ~96MB | GPL-3.0 | 오픈 보캐블러리, 텍스트 프롬프트로 클래스 지정 |
| **YOLOE26-L** | 36.8% (LVIS) | ~6.2ms (161 FPS) | - | - | AGPL-3.0 | YOLO-World 대비 +10 AP, 1.4배 빠름 |
| **Grounding DINO** | ~52% (COCO) | ~30-50ms | ~170M | ~700MB | Apache 2.0 | 오픈 보캐블러리, 텍스트 기반 감지, 느림 |
| **Florence-2** | - | ~1s (GPU) | 230M/770M | ~1-3GB | MIT | VLM 기반, 다목적, 실시간 부적합 |

### 2.2 모델별 상세 평가

#### YOLOv12 (2025)
- **장점:** Efficient Area Attention 도입으로 Transformer의 글로벌 수용장(receptive field) 활용, 기존 YOLO 대비 약간의 정확도 향상
- **단점:** YOLO11 대비 극적 개선은 아님, 파인튜닝 생태계가 아직 YOLO11만큼 성숙하지 않음
- **적용 가능성:** GPU 환경이라면 드롭인 교체 가능. CPU 환경에서는 이점 제한적
- **구현 난이도:** 낮음 (Ultralytics 프레임워크 동일)

#### RF-DETR (2025, ICLR 2026)
- **장점:** COCO SOTA (54.7% mAP), DINOv2 백본 기반, NMS 불필요, 파인튜닝에 최적화 설계, **Apache 2.0 라이선스**
- **단점:** GPU 필수, CPU 추론 느림, 새 프레임워크(Roboflow) 학습 필요
- **적용 가능성:** GPU 배포 환경에서 유력 후보. 커스텀 PPE 데이터셋 파인튜닝 시 높은 정확도 기대
- **구현 난이도:** 중 (프레임워크 전환 필요)

#### RT-DETR (2024, CVPR)
- **장점:** NMS 제거로 후처리 병목 없음, 디코더 레이어 수 조절로 속도/정확도 트레이드오프, **Apache 2.0**
- **단점:** GPU 필수, Transformer 특성상 소형 객체에 약할 수 있음
- **적용 가능성:** 멀티카메라 GPU 서버 환경에서 유리
- **구현 난이도:** 중

#### YOLO-World / YOLOE (오픈 보캐블러리)
- **장점:** 텍스트 프롬프트로 임의 클래스 감지 가능 ("safety gloves", "hardhat" 등), 파인튜닝 없이 즉시 장갑 감지 시도 가능
- **단점:** 고정 클래스 모델 대비 정확도 낮음 (LVIS 35-37% AP), 도메인 특화 성능은 파인튜닝 모델에 미달
- **적용 가능성:** 빠른 프로토타이핑 및 새 PPE 항목 추가 시 유용. 프로덕션에서는 파인튜닝 필요
- **구현 난이도:** 낮음 (Ultralytics 통합)

#### Grounding DINO / Florence-2 (파운데이션 모델)
- **장점:** 강력한 제로샷 성능, 다양한 비전 태스크 지원
- **단점:** 추론 속도 느림 (Florence-2는 ~1초/이미지), 모델 크기 매우 큼, 실시간 불가
- **적용 가능성:** 오프라인 분석, 데이터 라벨링 보조, 앙상블 검증용으로만 적합
- **구현 난이도:** 중~상

---

## 3. 건설현장 PPE 전용 데이터셋

### 3.1 주요 데이터셋

| 데이터셋 | 클래스 | 이미지 수 | 출처 | 특징 |
|---------|--------|----------|------|------|
| **Construction-PPE** (Ultralytics) | 11 (helmet, vest, gloves, boots, goggles + 미착용 쌍) | 1,416 | Ultralytics Docs | 공식 지원, 장갑/부츠/고글 포함, 실제 현장 이미지 |
| **Roboflow Construction Site Safety** | 다수 (hardhat, vest, person 등) | 수천 | Roboflow Universe | 커뮤니티 기여, 다양한 어노테이션 품질 |
| **keremberke/construction-safety** (HF) | 17 (gloves, hardhat, mask, no-hardhat 등) | ~2,600 | HuggingFace | 장갑 포함, YOLO 포맷, 장비 클래스도 포함 |
| **keremberke/protective-equipment** (HF) | 10 (glove, goggles, helmet, mask, shoes + 미착용) | ~2,800 | HuggingFace | PPE 전용, 산업 전반 |
| **SH17** | 17 | ~8,000 | 학술 | 제조업 특화, 높은 어노테이션 품질 |

### 3.2 파인튜닝 vs 사전학습 모델 직접 사용

| 전략 | 장점 | 단점 | 추천 상황 |
|------|------|------|----------|
| **사전학습 모델 직접 사용** (현재) | 즉시 사용, 추가 비용 없음, 유지보수 단순 | 도메인 특화 부족, 장갑 등 미지원 | PoC, 빠른 검증 |
| **기존 모델 파인튜닝** | 도메인 성능 대폭 향상, 적은 데이터로 효과 | GPU 필요, 하이퍼파라미터 튜닝, 과적합 위험 | 프로덕션 (추천) |
| **데이터셋 합치기 + 처음부터 학습** | 최대 커스터마이징 | 대량 데이터/GPU 필요, 긴 학습 시간 | 대규모 서비스 |

**추천:** Construction-PPE 또는 keremberke/construction-safety 데이터셋 기반으로 YOLO11m (또는 RF-DETR)을 **파인튜닝**하는 것이 비용 대비 효과가 가장 높음. 장갑 클래스가 포함된 데이터셋을 활용하면 현재의 "장갑 미지원" 문제 해결 가능.

### 3.3 전이학습 전략

```
1단계: COCO 사전학습 가중치 로드 (일반 객체 감지 능력)
2단계: Construction-PPE 데이터셋으로 파인튜닝 (도메인 특화)
3단계: 자체 현장 데이터 수집 후 추가 파인튜닝 (현장 특화)
```

- Ultralytics 프레임워크에서 `model.train(data="construction-ppe.yaml", epochs=100, imgsz=640)` 한 줄로 실행 가능
- Backbone freeze (처음 10개 레이어) 시 학습 시간 50% 단축, 소량 데이터에서 과적합 방지
- PEFT(Parameter-Efficient Fine-Tuning) 기법으로 GPU 메모리 절약 가능

---

## 4. 소형 객체(장갑) 감지 전략

### 4.1 2단계 파이프라인

```
[1단계] 전체 프레임 → Person 감지 (현재 모델)
         ↓
[2단계] Person 바운딩박스 크롭 → 손/장갑 영역 감지 (전용 모델)
```

- **장점:** 소형 객체가 크롭 후 상대적으로 크게 보임, 기존 시스템과 호환
- **단점:** 추론 시간 2배 (Person 수 × 2단계 추론), 파이프라인 복잡도 증가
- **구현 난이도:** 중 (2단계 모델 학습 + 크롭 로직)
- **예상 소요:** 2~3주

#### MediaPipe 손 감지 활용
- MediaPipe Hand Landmarker로 Palm 감지 → 손 영역 크롭 → 장갑 유무 분류
- 21개 손 키포인트 감지, 손목(wrist) 기준 영역 설정
- **한계:** 장갑 착용 시 키포인트 감지 정확도 하락 가능 (맨손 기준 학습)
- 대안: Person 크롭 내에서 손 영역을 단순 비율(하단 20%)로 추정하는 방식이 더 실용적

### 4.2 SAHI (Slicing Aided Hyper Inference)

```
원본 이미지 (1280x720)
    ↓ 슬라이싱
[640x640 타일] [640x640 타일] [640x640 타일] ...
    ↓ 각 타일에서 개별 감지
    ↓ 결과 병합 (NMS로 중복 제거)
최종 감지 결과
```

- **장점:** 기존 모델 수정 없이 적용 가능, AP 5~15% 향상 보고, 원거리 소형 객체 감지 크게 개선
- **단점:** 추론 시간 타일 수에 비례하여 증가 (3~6배), 메모리 사용량 증가
- **구현 난이도:** 낮음 (`pip install sahi`, 코드 수 줄 추가)
- **예상 소요:** 1~2일

```python
# SAHI 적용 예시
from sahi import AutoDetectionModel
from sahi.predict import get_sliced_prediction

model = AutoDetectionModel.from_pretrained(
    model_type="ultralytics",
    model_path="models/yolo11m-construction-hazard.pt",
    confidence_threshold=0.3,
)

result = get_sliced_prediction(
    image="frame.jpg",
    detection_model=model,
    slice_height=640,
    slice_width=640,
    overlap_height_ratio=0.2,
    overlap_width_ratio=0.2,
)
```

### 4.3 고해상도 입력

- 현재 640px 입력 → 1280px로 확대 시 소형 객체 감지율 향상
- **트레이드오프:** 추론 시간 약 4배 증가 (해상도 제곱에 비례)
- SAHI 대비 효율 낮음 — SAHI가 동일 효과를 더 효율적으로 달성

### 4.4 전략 비교

| 전략 | 장갑 감지 | 원거리 개선 | 속도 영향 | 구현 난이도 | 추천도 |
|------|----------|-----------|----------|-----------|--------|
| 2단계 파이프라인 | 매우 좋음 | 보통 | 2~3배 느림 | 중 | ★★★★ (장갑 전용) |
| SAHI | 좋음 | 매우 좋음 | 3~6배 느림 | 낮음 | ★★★★★ (범용) |
| 고해상도 입력 | 좋음 | 좋음 | 4배 느림 | 낮음 | ★★ |
| 장갑 포함 데이터셋 파인튜닝 | 좋음 | 보통 | 변화 없음 | 중 | ★★★★★ (근본 해결) |

---

## 5. 오탐 억제 기법

### 5.1 클래스별 신뢰도 임계값 조정

현재 전체 클래스 동일 임계값(0.30) 사용 중. 클래스별로 다르게 설정하여 오탐 억제 가능.

```python
# 클래스별 신뢰도 임계값 예시
CLASS_THRESHOLDS = {
    "Person": 0.30,       # 기본 유지
    "Hardhat": 0.35,      # 약간 높임
    "Safety Vest": 0.35,
    "NO-Hardhat": 0.50,   # 위반 클래스는 높은 신뢰도 요구
    "NO-Safety Vest": 0.50,
    "NO-Mask": 0.70,      # 오탐 많은 클래스 — 매우 높게
    "Mask": 0.40,
}
```

- **장점:** 코드 변경 최소, 즉시 적용 가능, NO-Mask 오탐 제거 효과적
- **단점:** 최적 임계값 찾기 위한 실험 필요, 높은 임계값 = 미감지 증가 위험
- **구현 난이도:** 매우 낮음
- **예상 소요:** 반나절

### 5.2 Temporal Smoothing (연속 프레임 기반 판정)

```
프레임 1: NO-Hardhat 감지 → 카운트 1
프레임 2: NO-Hardhat 감지 → 카운트 2
프레임 3: NO-Hardhat 미감지 → 카운트 리셋
프레임 4: NO-Hardhat 감지 → 카운트 1
프레임 5: NO-Hardhat 감지 → 카운트 2
프레임 6: NO-Hardhat 감지 → 카운트 3 → ✅ 이벤트 트리거!
```

- **원리:** 단발성 오탐은 연속 프레임에서 일관되지 않음. N프레임(예: 3~5) 연속 감지 시에만 이벤트 생성
- **장점:** 단발성 오탐 완전 제거, 실질적 위반만 보고, 구현 단순
- **단점:** 감지 지연 증가 (N프레임 × 프레임 간격), 빠르게 지나가는 위반 놓칠 수 있음
- **구현 난이도:** 낮음
- **예상 소요:** 1~2일

### 5.3 구역별 PPE 규칙 엔진

```python
# 구역별 규칙 예시
ZONE_RULES = {
    "crane_area": {"required": ["Hardhat", "Safety Vest"], "ignore": ["Mask"]},
    "welding_area": {"required": ["Hardhat", "Safety Vest", "Mask"], "ignore": []},
    "office_area": {"required": [], "ignore": ["Mask", "Safety Vest"]},
}
```

- **장점:** NO-Mask가 마스크 불필요 구역에서는 자동 무시, 현장별 커스터마이징
- **단점:** 카메라 시야 내 구역 매핑 필요 (좌표 기반), 구역 설정 UI 필요
- **구현 난이도:** 중
- **예상 소요:** 1주

### 5.4 모델 앙상블

```
모델 A (YOLO11m) → 감지 결과 A
모델 B (RF-DETR) → 감지 결과 B
     ↓
교차 검증: 두 모델 모두 위반 감지 시에만 이벤트 생성
```

- **장점:** 오탐을 극적으로 줄임, 서로 다른 아키텍처의 약점 보완
- **단점:** 추론 시간 2배, GPU 메모리 2배, 시스템 복잡도 증가
- **구현 난이도:** 중~상
- **예상 소요:** 2~3주

### 5.5 Soft-NMS

- 기존 NMS의 하드 임계값 대신 겹치는 박스의 신뢰도를 점진적으로 감소
- 가림(Occlusion) 상황에서 겹친 객체 감지율 향상
- Ultralytics에서 기본 지원 (`iou` 파라미터 조정으로 유사 효과)

### 5.6 기법 비교

| 기법 | NO-Mask 오탐 억제 | 전체 오탐 감소 | 속도 영향 | 구현 난이도 | 추천도 |
|------|-----------------|-------------|----------|-----------|--------|
| 클래스별 임계값 | 매우 효과적 | 효과적 | 없음 | 매우 낮음 | ★★★★★ |
| Temporal smoothing | 매우 효과적 | 매우 효과적 | 감지 지연 추가 | 낮음 | ★★★★★ |
| 구역별 규칙 엔진 | 매우 효과적 | 효과적 | 없음 | 중 | ★★★★ |
| 모델 앙상블 | 극히 효과적 | 극히 효과적 | 2배 느림 | 중~상 | ★★★ |
| Soft-NMS | 보통 | 보통 | 미미 | 낮음 | ★★★ |

---

## 6. 라이선스 고려사항

| 모델/프레임워크 | 라이선스 | 상용 사용 |
|---------------|---------|----------|
| Ultralytics YOLO (YOLO11, YOLOv12, YOLOE) | AGPL-3.0 | 상용 시 Enterprise 라이선스 필요 (유료) |
| RF-DETR | Apache 2.0 | 자유 상용 사용 가능 |
| RT-DETR | Apache 2.0 | 자유 상용 사용 가능 |
| YOLO-World | GPL-3.0 | 소스 공개 의무 |
| Grounding DINO | Apache 2.0 | 자유 상용 사용 가능 |
| Florence-2 | MIT | 자유 상용 사용 가능 |

**참고:** 현재 사용 중인 Ultralytics 프레임워크는 AGPL-3.0이므로, 상용화 시 Enterprise 라이선스 구매 또는 Apache 2.0 모델(RF-DETR, RT-DETR)로 전환을 고려해야 함.

---

## 7. 최종 추천안

### 7.1 단기 (1~2주) — 즉시 적용 가능한 개선

| 항목 | 작업 | 예상 효과 | 소요 |
|------|------|----------|------|
| 1 | **클래스별 신뢰도 임계값** 도입 (NO-Mask: 0.70) | NO-Mask 오탐 사실상 제거 | 반나절 |
| 2 | **Temporal smoothing** (3프레임 연속 위반 시 이벤트) | 단발성 오탐 완전 억제 | 1~2일 |
| 3 | **SAHI 적용** (원거리/소형 객체 개선) | 원거리 AP 5~15% 향상 | 1~2일 |
| 4 | **구역별 PPE 규칙 엔진** (마스크 불필요 구역 필터) | 불필요 알림 제거 | 1주 |

### 7.2 중기 (1~2개월) — 모델 파인튜닝 및 장갑 감지

| 항목 | 작업 | 예상 효과 | 소요 |
|------|------|----------|------|
| 5 | **Construction-PPE 데이터셋으로 파인튜닝** (장갑 포함 11클래스) | 장갑 감지 추가, 전체 mAP 향상 | 2~3주 |
| 6 | **2단계 파이프라인** (Person 크롭 → 장갑/소형 PPE 감지) | 장갑 감지 정확도 극대화 | 2~3주 |
| 7 | **자체 현장 데이터 수집 및 추가 파인튜닝** | 현장 특화 성능 최적화 | 지속적 |

### 7.3 장기 (3~6개월) — 아키텍처 고도화

| 항목 | 작업 | 예상 효과 | 소요 |
|------|------|----------|------|
| 8 | **RF-DETR로 모델 전환** (Apache 2.0, SOTA 정확도) | 정확도 향상 + 라이선스 자유 | 1~2개월 |
| 9 | **YOLOE/YOLO-World 통합** (신규 PPE 항목 즉시 추가) | 유연한 클래스 확장 | 2~3주 |
| 10 | **모델 앙상블 파이프라인** (YOLO + DETR 교차 검증) | 오탐률 극소화 | 1개월 |
| 11 | **TensorRT/ONNX 최적화** (엣지 배포용) | 추론 속도 3~5배 향상 | 2~3주 |

### 7.4 우선순위 요약

```
[즉시] 클래스별 임계값 + Temporal smoothing → NO-Mask 오탐 해결
  ↓
[1~2주] SAHI + 구역별 규칙 → 원거리 개선 + 불필요 알림 제거
  ↓
[1~2개월] 파인튜닝 (장갑 포함) → 장갑 감지 추가, 전체 정확도 향상
  ↓
[3~6개월] RF-DETR 전환 + 앙상블 → 프로덕션급 정확도 + 라이선스 확보
```

---

## 8. 참고 자료

- [Ultralytics 모델 비교](https://docs.ultralytics.com/compare/)
- [YOLO11 vs 이전 모델](https://www.ultralytics.com/blog/comparing-ultralytics-yolo11-vs-previous-yolo-models)
- [RF-DETR GitHub](https://github.com/roboflow/rf-detr)
- [RT-DETR 논문](https://arxiv.org/abs/2304.08069)
- [YOLO-World 논문](https://arxiv.org/abs/2401.17270)
- [YOLOE Docs](https://docs.ultralytics.com/models/yoloe/)
- [SAHI GitHub](https://github.com/obss/sahi)
- [Construction-PPE 데이터셋](https://docs.ultralytics.com/datasets/detect/construction-ppe/)
- [HuggingFace construction-safety 데이터셋](https://huggingface.co/datasets/keremberke/construction-safety-object-detection)
- [HuggingFace protective-equipment 데이터셋](https://huggingface.co/datasets/keremberke/protective-equipment-detection)
- [Roboflow 베스트 모델 2025](https://blog.roboflow.com/best-object-detection-models/)
- [Ultralytics 라이선스](https://www.ultralytics.com/license)
