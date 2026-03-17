# 건설현장 고각도 CCTV 소형 객체 탐지 종합 가이드

YOLO11m이 조감도(bird's eye view) CCTV에서 작업자를 탐지하지 못하는 핵심 원인은 **수십 픽셀 크기의 객체가 640×640 리사이즈 과정에서 수 픽셀로 축소**되고, 탑뷰 실루엣이 학습 데이터의 정면/측면 인체 형상과 근본적으로 다르기 때문이다. 가장 즉각적이고 효과적인 해결책은 **SAHI(Slicing Aided Hyper Inference) + P2 탐지 헤드 추가 + 항공뷰 데이터셋 파인튜닝**의 3단 조합이며, 이 파이프라인만으로 소형 객체 재현율을 **4배 이상** 개선할 수 있다. 아래에서 모델, 상용 API, 파인튜닝, 추론 최적화, 대안적 접근법 5개 카테고리를 구체적인 코드·벤치마크·비용과 함께 상세히 다룬다.

---

## SAHI가 가장 먼저 적용해야 할 단일 최고 솔루션인 이유

**SAHI(Slicing Aided Hyper Inference)**는 재학습 없이 기존 YOLO11m에 즉시 적용할 수 있으며, 소형 객체 탐지에서 가장 높은 비용 대비 효과를 제공한다. 1920×1080 영상을 640×640 타일로 분할하여 각 타일에서 독립적으로 추론한 뒤, NMS로 결과를 병합하는 방식이다. VisDrone 데이터셋에서 **AP 최대 +6.8%**, 슬라이싱 파인튜닝까지 결합 시 **누적 +14.5% AP** 향상이 보고되었으며, FiftyOne 평가에서 소형 인물 재현율이 8%에서 **31%로 4배 증가**했다.

```python
from sahi import AutoDetectionModel
from sahi.predict import get_sliced_prediction

model = AutoDetectionModel.from_pretrained(
    model_type="ultralytics",
    model_path="yolo11m.pt",  # 기존 모델 그대로 사용
    confidence_threshold=0.25,
    device="cuda:0"
)

result = get_sliced_prediction(
    image="construction_frame.jpg",
    detection_model=model,
    slice_height=640, slice_width=640,
    overlap_height_ratio=0.2, overlap_width_ratio=0.2,
    perform_standard_pred=True,        # 전체 이미지 추론도 병행
    postprocess_type="GREEDYNMM",
    postprocess_match_threshold=0.5,
    postprocess_class_agnostic=True,   # 단일 클래스(person)일 때
)
```

1080p에서 640×640 타일 기준 약 **6~7회 추론**(타일 6개 + 전체 1회)이 필요하므로 속도가 약 6배 느려지지만, RTX 3090에서 **3~5 FPS** 수준으로 CCTV 모니터링에는 충분하다. 4K 영상은 약 25~30개 타일이 필요하므로 1080p로 다운스케일 후 SAHI 적용을 권장한다. GitHub 레포: `obss/sahi` (MIT 라이선스, 학술 인용 400+건).

---

## 소형 객체에 특화된 모델 아키텍처 선택지

### P2 탐지 헤드: 가장 효과적인 아키텍처 수정

표준 YOLOv8/v11은 P3/P4/P5(stride 8/16/32) 3개 탐지 헤드를 사용한다. **P2 헤드를 추가**하면 stride 4의 고해상도 피처맵(입력 1280 기준 320×320)에서 탐지하므로 초소형 객체 감지 능력이 극적으로 향상된다. SOD-YOLO 논문(2025, arXiv:2507.12727)에 따르면 YOLOv8m 기준 VisDrone에서 **mAP50 43.6% → 47.6%(+4.0%)**, Soft-NMS 추가 시 **52.6%(+9.0%)**까지 개선되었다. Ultralytics 내장 YAML(`yolov8-p2.yaml`)을 활용하면 된다.

```python
from ultralytics import YOLO
model = YOLO('yolov8m-p2.yaml').load('yolov8m.pt')  # P2 헤드 + COCO 가중치
model.train(data='aerial_person.yaml', imgsz=1280, epochs=300)
```

### Pose-Head 보조 학습 트릭: 추론 비용 제로의 +12% 향상

YOLOv8을 포즈 모델로 학습(바운딩 박스 중심을 키포인트로 사용)한 뒤, 디텍트 모델로 변환하는 기법이다. IoU 기반 손실이 소형 객체에서 극도로 불안정한 문제를 중심점 거리 손실로 우회하며, 소형 객체에서 **mAP50 +12%** 개선이 보고되었다. 추론 시 GFLOPs 증가가 전혀 없다는 것이 핵심 장점이다. (`box=0.01, dfl=0.01`로 학습 후 변환)

### RT-DETR 및 드론 특화 트랜스포머 모델

| 모델 | 기반 | VisDrone mAP50 | 파라미터 | 가용성 |
|------|------|---------------|---------|--------|
| **Drone-DETR** | RT-DETR | **53.9%** | 28.7M | 논문만 (코드 미공개) |
| **UAV-DETR** | RT-DETR | 51.6% | 16.8M | 논문만 |
| **SOD-YOLO** | YOLOv8 | 52.6% | ~79 GFLOPs | 논문만 |
| **TPH-YOLOv5** | YOLOv5 | 39.2% (test) | - | GitHub 공개 + 사전학습 가중치 |
| **RT-DETR** | DETR | ~48% | - | Ultralytics 내장 |

실용성 측면에서 **RT-DETR + SAHI** 조합이 트랜스포머 계열 최선의 선택이다. `YOLO('rtdetr-l.pt')`로 Ultralytics에서 바로 로드 가능하며 SAHI와 호환된다. Drone-DETR(53.9% mAP50)이 최고 성능이지만 코드가 미공개되어 즉시 사용이 어렵다.

### NWD(Normalized Wasserstein Distance) 손실 함수

IoU가 소형 객체에서 위치 편차에 극도로 민감한 문제를 해결하기 위해, 바운딩 박스를 2D 가우시안으로 모델링하고 Wasserstein 거리를 사용한다. AI-TOD 데이터셋에서 **+6.7 AP** 향상이 보고되었다. CIoU 손실에 NWD를 결합하여 학습하면 라벨 할당과 NMS 모두에서 소형 객체 처리가 개선된다 (GitHub: `jwwangchn/NWD`).

---

## 파인튜닝을 위한 데이터셋과 구체적 학습 전략

### 핵심 데이터셋 비교

| 데이터셋 | 이미지 수 | 인물 어노테이션 | 포맷 | 무료 | 핵심 특징 |
|----------|----------|---------------|------|------|----------|
| **VisDrone-DET** | 10,209 | ✅ 보행자+사람 | YOLO 변환 가능 | ✅ | 항공뷰 기본 사전학습용, Ultralytics 내장 |
| **Zenodo Aerial Person** | 3,136 | ✅ 61,708개 | **YOLO/COCO/VOC** | ✅ CC-BY 4.0 | **가장 적합** — UAV 탑뷰 인물 전용 |
| **TinyPerson** | 1,610 | ✅ 72,651개 (2~20px) | COCO | ✅ | 초소형 인물 특화 벤치마크 |
| **Stanford Drone** | 100+ 장면 | ✅ 다중 클래스 | 커스텀 | ✅ | 진정한 오버헤드 뷰 |
| **Okutama-Action** | ~77K 프레임 | ✅ 행동 인식 포함 | BBox | ✅ | 4K UAV, 작업자 활동 인식 |
| **SODA-A** | 2,513 | 혼합 9클래스 | OBB | 학술 전용 | 소형 객체 연구용 |
| **UAVDT** | 80,000 프레임 | ❌ 차량 중심 | BBox | ✅ | 항공 도메인 적응용 |

**Zenodo Aerial Person 데이터셋**(zenodo.org/records/7740081)이 가장 직접적으로 관련된다. UAV 탑뷰에서 촬영된 3,136개 이미지에 61,708개 인물 어노테이션이 YOLO 포맷으로 제공되며, CC-BY 4.0 라이선스로 상업적 사용도 가능하다. Roboflow Universe에서도 `aerial person detection`, `construction site worker` 키워드로 커뮤니티 데이터셋을 검색할 수 있다.

### 권장 3단계 전이학습 파이프라인

**Stage 1**: COCO 사전학습 가중치에서 VisDrone으로 항공 도메인 사전학습

```bash
yolo detect train model=yolov8m-p2.yaml pretrained=yolov8m.pt \
    data=VisDrone.yaml imgsz=1280 epochs=100 batch=8 name=visdrone_pretrain
```

**Stage 2**: VisDrone 가중치에서 자체 건설현장 데이터로 파인튜닝

```bash
yolo detect train model=runs/detect/visdrone_pretrain/weights/best.pt \
    data=construction_person.yaml imgsz=1280 epochs=300 batch=4 \
    lr0=0.001 cos_lr=True mosaic=1.0 close_mosaic=20 copy_paste=0.3 \
    flipud=0.5 degrees=10 scale=0.9 patience=50 name=construction_finetune
```

**Stage 2 대안 — 2단계 학습**: 먼저 백본(레이어 0~9)을 동결(freeze=10)하고 헤드만 50에폭 학습한 뒤, 전체 네트워크를 낮은 학습률(lr0=0.001)로 200에폭 파인튜닝한다. 이 방식이 소량 데이터에서 과적합을 방지하면서 도메인 적응 효과를 극대화한다.

### 소형 객체 최적 하이퍼파라미터

핵심 설정: **imgsz=1280**(640 대비 소형 객체 디테일 4배 보존), **copy_paste=0.3**(소형 인물 인스턴스 증강), **flipud=0.5**(오버헤드 뷰는 회전 불변), **scale=0.9**(공격적 스케일 변형), **close_mosaic=20**(마지막 20에폭 모자이크 비활성화로 정밀 학습). 모자이크 증강(mosaic=1.0)은 소형 객체에 필수적이며, 4개 이미지를 결합하여 다양한 스케일의 객체를 강제로 학습시킨다.

### 리소스 추정

전이학습 기반으로 **최소 500~1,000장의 자체 건설현장 어노테이션 이미지**면 실용적 성능 달성이 가능하다(mAP50 55~70%). 최적 성능을 위해서는 3,000~5,000장을 권장한다. YOLOv8m-P2를 imgsz=1280으로 5,000장 데이터에서 300에폭 학습 시, RTX 3090에서 약 **40~60시간**, A100(80GB)에서 약 **15~20시간** 소요된다. RTX 3090 기준 배치 사이즈는 4~8이다.

---

## 추론 시 성능 극대화를 위한 기법 조합

### 고해상도 입력의 효과와 한계

| imgsz | VRAM (배치1, FP16) | 상대 속도 | 권장 상황 |
|-------|-------------------|----------|----------|
| 640 | 2~3 GB | 1× (기준) | 객체 20px 이상 |
| **1280** | 6~10 GB | 0.25× | **객체 5~30px — 건설현장 권장** |
| 1920 | 14~20 GB | 0.1× | 1280 대비 한계적 이득 |

**imgsz=1280이 최적 균형점**이다. 1920 이상은 메모리 비용 대비 한계적 개선만 제공한다. 핵심 원칙: 학습과 추론에서 동일한 imgsz를 사용해야 한다. 640으로 학습한 모델을 1280으로 추론하면 오히려 성능이 저하될 수 있다.

### TTA(테스트 시간 증강)

`model.predict(source="image.jpg", augment=True)`로 활성화하면, 원본(1×) + 축소(0.83×, 좌우반전) + 축소(0.67×) 3개 스케일에서 추론 후 결과를 병합한다. YOLOv5x COCO 벤치마크에서 소형 객체 재현율이 **+2.9 포인트** 향상되었으나, 속도가 **3.6배 느려진다**. SAHI와 동시 사용 시 슬라이스당 3회 추론으로 계산 비용이 12~18배 증가하므로, 오프라인 배치 처리에서만 권장한다.

### 멀티스케일 추론 + WBF 병합

640, 960, 1280 3개 해상도에서 각각 추론한 뒤 **Weighted Boxes Fusion(WBF)**으로 결과를 병합하는 방식이다. WBF는 NMS와 달리 예측을 폐기하지 않고 가중 평균하여 더 정밀한 바운딩 박스를 생성한다 (GitHub: `ZFTurbo/Weighted-Boxes-Fusion`). 높은 해상도에 더 큰 가중치(예: `weights=[1, 1.5, 2]`)를 부여한다. 단일 모델의 SAHI에서는 NMS가 적합하고, 멀티스케일 앙상블에서는 WBF가 우수하다.

### 실시간 vs 오프라인 파이프라인 권장 구성

**실시간(5~10 FPS, 1080p)**: SAHI(640×640, 20% 오버랩) + YOLOv8m/v11m(TensorRT FP16) → RTX 4090에서 약 10~15 FPS 달성. `pip install sahi` 후 5줄 코드로 구현 가능.

**오프라인/배치 처리(정확도 우선)**: SAHI(512×512, 30% 오버랩) + 멀티스케일 추론(640/960/1280) + WBF 병합 + TTA → mAP 기준선 대비 **+10~15%** 향상 가능. A100 GPU 권장, 약 1~2 FPS.

---

## 상용 API와 건설 특화 솔루션의 현실적 한계

### 클라우드 비전 API 비교

| 항목 | Google Cloud Vision | AWS Rekognition | Azure Vision |
|------|-------------------|-----------------|-------------|
| **5fps 카메라당 월 비용** | ~$29,000 | ~$2,880 (Custom Labels) | ~$2,016 |
| **지연시간** | 0.5~1.5초/이미지 | ~0.5초 | ~0.5~1초 |
| **소형 객체 정확도** | 커스텀 모델 없이 낮음 | Custom Labels로 보통 | Custom Vision으로 보통 |
| **엣지 배포** | 제한적 | 제한적 | Docker 컨테이너 (강점) |
| **PPE 탐지** | 없음 | **내장 기능** | 없음 |

**범용 클라우드 API는 32×32 픽셀 미만의 소형 객체를 안정적으로 탐지하지 못한다.** 커스텀 모델 학습 기능(AutoML, Custom Labels, Custom Vision)을 활용해도 타일링/SAHI 전략이 병행되어야 한다. 비용 측면에서 5fps 실시간 처리 시 카메라당 월 $2,000~$30,000으로, 자체 엣지 GPU 배포 대비 경제성이 크게 떨어진다.

**Roboflow**이 가장 실용적인 대안이다. 네이티브 SAHI 통합, 자체 데이터 어노테이션→학습→배포 파이프라인, 셀프 호스팅 추론 서버(Docker)를 제공하며, Starter 플랜 월 **$249**부터 시작한다. 특히 Roboflow Workflows의 Image Slicer 블록으로 노코드 SAHI 파이프라인을 구축할 수 있다.

### 건설 특화 상용 솔루션

**Smartvid.io(VINNIE)**: 현장 사진/영상에서 안전 위반(하드햇 미착용, 추락 위험 등)을 AI로 탐지한다. 1,080장 이미지를 10분 내 분석하며(인간 전문가 4.5시간 대비), Procore·Autodesk BIM 360과 연동된다. 그러나 **조감도 특화가 아닌** 일반 카메라 높이 기준이다.

**viAct**: 기존 CCTV에 플러그앤플레이로 적용하는 엣지 기반 건설 안전 AI 플랫폼이다. PPE 탐지, 밀폐 공간 모니터링, 환경 모니터링을 지원하며, 사고 **95% 감소**를 주장한다. 엘리베이티드 카메라를 포함한 기존 CCTV 시스템과 호환된다.

**Indus.ai(현재 Procore 통합)**: 현장 주변 카메라로 트럭, 작업자, 장비를 모니터링하며 다중 카메라 각도를 분석한다. Procore 구독에 포함되어 대형 건설사에 적합하다.

**핵심 결론: 어떤 건설 특화 상용 솔루션도 조감도/탑뷰 최적화를 명시적으로 광고하지 않는다.** 대부분 눈높이~중간 높이 카메라 기준이므로, 극단적 고각도 CCTV에서는 자체 모델 학습이 불가피하다.

---

## 하이브리드 및 대안적 접근법

### 배경 차분법 + YOLO 하이브리드

고정 CCTV에서 OpenCV의 MOG2/KNN 배경 차분으로 움직임이 있는 영역(ROI)만 추출한 뒤, 해당 영역을 크롭·업스케일하여 YOLO로 탐지하는 방식이다. Xiong 등(2025, The Visual Computer)은 이 조합이 정밀도 **+2.3%**, 재현율 **+3.5%** 개선을 보고했다. 전체 프레임 대신 ROI만 처리하므로 오히려 **속도가 향상**된다는 장점이 있다. 단, **정지 상태 작업자를 탐지하지 못하는** 근본적 한계가 있으므로, N프레임마다 전체 프레임 YOLO 추론을 병행해야 한다.

### Super-Resolution 전처리

Real-ESRGAN, SwinIR 등으로 ROI를 4배 업스케일한 뒤 YOLO를 적용하면, 소형 객체 AP가 **+5~15%** 개선될 수 있다. Wang 등(PLOS ONE 2025)은 경량 SR + YOLOv8 조합에서 재현율 70.23% → **80.51%**, mAP 77.48% → **83.32%** 향상을 보고했다. 그러나 SR 자체가 이미지당 **200~1,000ms** 소요되므로 전체 프레임에 적용하면 실시간 처리가 불가능하다. **움직임 감지 ROI에만 선택적으로 적용**하는 것이 현실적이다.

### ByteTrack 기반 시간적 보강

Ultralytics에 내장된 ByteTrack(`model.track(source=video, tracker="bytetrack.yaml")`)은 저신뢰도 탐지 결과도 기존 트랙렛과 매칭하여 복구하며, 누락 프레임을 선형/가우시안 보간으로 채운다. 추가 연산 비용이 프레임당 **~4ms**로 거의 무시할 수 있으며, 건설현장 작업자는 느리게 움직이므로 칼만 필터 예측이 매우 정확하다. **실질 탐지율 +5~15%** 향상을 기대할 수 있다. 아래 한 줄로 적용 가능하다:

```python
results = model.track(source="site.mp4", tracker="bytetrack.yaml", conf=0.15, persist=True)
```

### Attention 메커니즘과 FPN 수정

CBAM(Channel + Spatial Attention)을 YOLO 백본에 추가하면 **+2~5% mAP** 향상이 보고되며, 추론 지연은 **5% 미만**으로 최소화된다. BiFPN(양방향 피처 피라미드)은 크로스 스케일 특성 융합을 가중치 기반으로 수행하여 소형 객체에 유리하다. 이들은 모델 YAML 수정 후 재학습이 필요하므로 P2 헤드 추가와 함께 적용하면 시너지가 크다.

### 합성 데이터 생성

학습 데이터가 부족할 때, Unreal Engine이나 Unity Perception 패키지로 건설현장 조감도를 렌더링하여 합성 데이터를 생성할 수 있다. CGI 기반 합성 데이터는 객체 크기·위치·텍스처·조명을 완전히 제어 가능하므로, 소형 객체 탐지에 특화된 데이터셋을 만들 수 있다. 실제 데이터 대비 **+10~20% mAP** 부스트가 보고되었으나, 3D 모델링 파이프라인 구축에 상당한 초기 노력이 필요하다.

---

## 종합 권장 구현 로드맵

아래 로드맵은 구현 난이도가 낮은 것부터 순서대로 나열하며, 각 단계에서 누적 효과를 기대할 수 있다.

**1단계 — 즉시 적용 (재학습 불필요, 1~2일)**

SAHI를 기존 YOLO11m에 적용한다. `pip install sahi` 후 640×640 타일, 20% 오버랩으로 설정하면 소형 작업자 재현율이 즉시 **3~4배** 향상된다. 동시에 ByteTrack 추적을 활성화하여 프레임 간 누락을 보간한다. 이것만으로 "전혀 탐지 못함" 상태에서 "실용적 수준"으로 전환될 가능성이 높다.

**2단계 — 아키텍처 수정 + 항공 데이터 사전학습 (1~2주)**

YOLOv8m-P2(또는 YOLO11m-P2) 모델을 구성하고, VisDrone + Zenodo Aerial Person + TinyPerson을 결합하여 imgsz=1280으로 학습한다. NWD 손실 함수 적용과 Pose-head 보조 학습 트릭을 결합한다. RTX 3090 1대로 약 **40~60시간**이면 완료된다.

**3단계 — 자체 데이터 파인튜닝 (2~4주)**

자체 건설현장 CCTV에서 500~2,000장을 샘플링하여 Roboflow 또는 CVAT로 어노테이션한 뒤, 2단계 모델을 파인튜닝한다. `freeze=10`으로 백본 동결 후 50에폭 헤드 학습, 이어서 전체 네트워크 200에폭 파인튜닝의 2단계 전략을 적용한다.

**4단계 — 고급 최적화 (선택적)**

배경 차분법 ROI + SR 전처리 하이브리드, CBAM/BiFPN 어텐션 추가, 합성 데이터 보강을 필요에 따라 적용한다. TensorRT FP16 내보내기로 최종 배포 속도를 최적화한다.

**비용 효율적 최종 구성**: 엣지 GPU(RTX 4090 ~$2,000 또는 Jetson AGX Orin ~$2,000) + Roboflow Starter($249/월)로 카메라당 SAHI 파이프라인을 자체 호스팅하면, 클라우드 API 대비 **10~100배 저렴**하면서 더 높은 정확도와 낮은 지연시간을 달성할 수 있다. 이 조합이 건설현장 고각도 CCTV 소형 작업자 탐지의 현재 최적해다.