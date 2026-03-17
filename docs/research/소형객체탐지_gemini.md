# **건설 현장 고각 CCTV 환경에서의 소형 객체 탐지 및 클래스 불균형 해결을 위한 심층 기술 분석 보고서**

## **1\. 서론 및 진단 분석: 객체 탐지 한계의 근본 원인 규명**

건설 현장의 폐쇄회로 텔레비전(CCTV) 영상 인프라를 활용하여 작업자의 안전을 모니터링하고 추적(Tracking)하는 시스템은 스마트 건설의 핵심 요소로 자리 잡고 있다. 그러나 실시된 기술 검증(PoC) 결과, 현재 도입된 기반 모델(YOLOv11m-construction-hazard)은 치명적인 두 가지 한계점에 직면해 있다. 첫째, 조감도(Bird's-eye view) 형태의 높은 각도에서 촬영된 영상에서 소형 객체(Small Object)를 거의 탐지하지 못하는 현상이 발생했다. 둘째, 정량 평가 결과 '안전모 미착용(NO-Hardhat)' 클래스의 mAP@50 성능이 2.8%에 불과하여, 모델이 소수 클래스의 특성을 전혀 학습하지 못하는 극심한 클래스 불균형(Class Imbalance) 문제를 드러냈다.

이러한 성능 저하는 단순히 학습 횟수(Epoch)가 부족하거나 범용 모델을 사용했기 때문에 발생하는 지엽적인 문제가 아니다. 이는 합성곱 신경망(Convolutional Neural Network, CNN)의 구조적 한계와 데이터의 공간적 밀도가 충돌하면서 발생하는 수학적이고 구조적인 문제이다.1

### **1.1 고각 CCTV 환경에서의 소형 객체 특징 소실 메커니즘**

현재 테스트된 YOLO 모델은 일반적으로 640x640 픽셀의 해상도로 입력 이미지를 리사이징(Resizing)하여 처리한다. 타워크레인이나 높은 철골 구조물에 설치된 CCTV가 촬영하는 영상의 경우, 사람 한 명의 크기는 원본 영상에서도 수십 픽셀에 불과하다. 이 영상이 640x640 크기로 압축될 경우, 객체의 크기는 10x10 픽셀 이하의 극소형 픽셀 클러스터로 붕괴한다.3

YOLOv11의 특성 추출을 담당하는 백본(Backbone) 네트워크는 이미지를 여러 단계로 압축하며 의미론적(Semantic) 특징을 추출한다. 최종적인 객체 탐지는 일반적으로 Stride 8(P3), Stride 16(P4), Stride 32(P5) 크기의 특징 맵(Feature Map)에서 수행된다. 640x640 입력 기준으로 P5 레이어의 그리드 크기는 20x20이다. 즉, 원본에서 10x10 픽셀이었던 객체는 신경망의 깊은 레이어에 도달하면 소수점 이하의 픽셀 정보를 가지게 되어 주변의 배경(Background clutter) 노이즈와 구별할 수 없는 상태로 소멸된다.2 따라서 COCO 사전 학습 모델 여부와 무관하게, 이 해상도 압축과 특징 맵의 스케일 불일치 문제를 해결하지 않으면 고각 탐지 실패는 필연적으로 발생한다.

### **1.2 소수 클래스(NO-Hardhat)의 극단적 불균형과 그래디언트 소멸**

정량 평가에서 나타난 2.8%의 NO-Hardhat 감지율은 데이터셋 내의 심각한 클래스 불균형이 학습에 미치는 영향을 여실히 보여준다. 건설 현장의 데이터 수집 환경 특성상, 대부분의 작업자는 안전모를 착용하고 있다(다수 클래스). 따라서 'Person'과 'Hardhat' 클래스는 수만 건의 데이터가 수집되지만, 'NO-Hardhat' 클래스는 극소수에 불과하다.6

표준적인 교차 엔트로피(Cross-Entropy) 기반의 손실 함수를 사용할 경우, 모델은 전체 오차(Total Loss)를 줄이는 가장 쉬운 방법으로 '모든 사람은 안전모를 쓰고 있다'고 예측하는 통계적 편향을 학습하게 된다.8 학습 과정에서 소수 클래스가 발생시키는 역전파(Backpropagation) 그래디언트(Gradient)는 다수 클래스와 압도적인 양의 배경(Background) 데이터가 발생시키는 그래디언트에 파묻혀버린다. 결과적으로 모델은 보호구 미착용 상태를 '오류'가 아닌 '통계적 예외'로 취급하게 되며, 이는 안전 모니터링 시스템의 치명적인 결함으로 이어진다.

## **2\. 소형 객체 탐지(SOD) 고도화를 위한 아키텍처 및 알고리즘 혁신**

문제를 근본적으로 해결하기 위해서는 단순히 모델을 교체하는 것을 넘어, 신경망이 객체의 미세한 경계와 픽셀을 인식하는 방식 자체를 재설계해야 한다. 최신 2024-2025년 컴퓨터 비전 연구 동향에 따르면, 소형 객체 탐지(Small Object Detection, SOD) 분야는 고해상도 특징 맵의 활용과 수학적 거리 측정 방식의 전환을 통해 돌파구를 마련하고 있다.5

### **2.1 고해상도 P2 탐지 헤드(P2 Detection Head)의 도입**

기존 YOLOv11 모델의 YAML 설정은 앞서 언급한 바와 같이 P3, P4, P5 레이어를 사용하여 탐지를 수행한다. 소형 객체를 탐지하기 위해서는 이미지의 세부적인 질감과 에지(Edge) 정보가 소실되기 전인 얕은(Shallow) 레이어의 특징을 활용해야 한다. 이를 위해 백본 네트워크의 더 이른 단계에서 특징을 추출하는 P2 레이어(Stride 4)를 탐지 헤드에 추가하는 구조적 수정이 필수적이다.11

| 특징 맵 레이어 | Stride 비율 | 640x640 입력 시 그리드 크기 | 최적 탐지 객체 크기 | 아키텍처 적용 시사점 |
| :---- | :---- | :---- | :---- | :---- |
| P5 (기본) | 32 | 20x20 | 대형 객체 (\>96x96 px) | 깊은 전역적 의미를 파악하나, 소형 객체는 완전히 소멸됨 |
| P4 (기본) | 16 | 40x40 | 중형 객체 (32x32 \~ 96x96) | 의미론적 정보와 공간 해상도의 균형점 |
| P3 (기본) | 8 | 80x80 | 소형 객체 (16x16 \~ 32x32) | 일반적인 소형 객체 탐지의 기준선 |
| **P2 (커스텀)** | **4** | **160x160** | **극소형 객체 (\<16x16 px)** | **고각 CCTV의 극소형 사람 탐지를 위한 핵심 레이어** |

YOLOv11 모델의 구성 파일(yolo11.yaml)을 직접 수정하여 얕은 계층의 고주파 특징(High-frequency feature)을 유지하는 P2 헤드를 추가하면, 극도로 작은 작업자의 경계선 정보가 보존된다.13 이때 연산량 증가를 억제하기 위해, 고각 환경에서는 전혀 등장하지 않는 화면의 절반 크기를 차지하는 대형 객체용 P5 레이어를 네트워크 구조에서 과감히 제거하는 최적화 전략을 병행할 수 있다.15

### **2.2 NWD(Normalized Wasserstein Distance) 손실 함수의 적용**

구조적 변경과 함께 손실 함수(Loss Function)의 전환이 수반되어야 한다. 객체 탐지 모델은 예측한 바운딩 박스(Bounding Box)와 실제 정답 박스 간의 겹치는 영역을 측정하는 IoU(Intersection over Union)를 기반으로 손실을 계산한다. 그러나 10x10 픽셀 크기의 객체에서 단 1픽셀의 위치 오차만 발생해도 IoU 값은 급격하게 하락하여 '0'에 수렴하게 된다.17 이는 신경망에 극단적으로 불안정한 그래디언트를 제공하여 수렴을 방해한다.

이를 해결하기 위해 최근 소형 객체 탐지의 표준으로 자리 잡고 있는 것이 NWD(Normalized Gaussian Wasserstein Distance) 지표이다. NWD는 바운딩 박스를 딱딱한 사각형이 아닌 2D 가우시안 분포(Gaussian distribution)로 모델링한다.18 두 가우시안 분포 간의 유사성을 측정함으로써, 두 박스가 1픽셀도 겹치지 않더라도 거리에 따른 연속적이고 부드러운 손실 값을 계산해 낼 수 있다.19 YOLO의 기본 회귀 손실을 CIoU에서 NWD 기반 손실로 교체함으로써 극소형 객체의 위치 추정 정확도를 획기적으로 끌어올릴 수 있다.16

### **2.3 최신 특화 아키텍처 대안: DMS-YOLO 및 FDM-YOLO**

일반적인 YOLOv11 모델의 수정을 넘어, 2025년 현재 소형 객체 탐지에 특화되어 학계에 발표된 선도적인 파생 아키텍처들을 고려해 볼 수 있다.

* **DMS-YOLO (Dynamic Multi-scale and Channel-scaled YOLO):** 이 모델은 백본의 C3k2 모듈을 DMS-EdgeNet으로 교체하여 에지 특징과 공간 특징을 명시적으로 포착한다. P2 레이어 추가와 NWD 손실 함수가 기본으로 내장되어 있으며, VisDrone과 같은 공중 촬영 데이터셋에서 기존 YOLOv11n 대비 소형 객체 mAP50을 최대 7.0%p 향상시킨 것으로 보고되었다.11  
* **FDM-YOLO:** 이 아키텍처는 주파수 도메인(Frequency domain)에서 피처 추출을 수행하여 복잡한 배경 속의 소형 객체 패턴을 분리한다. 경량화된 구조를 유지하면서도 파라미터 수를 38% 감소시키고, 추론 속도를 유지한 채 탐지 성능을 크게 향상시킨 모델로, 엣지 디바이스(Edge device) 배포에 매우 유리하다.15

## **3\. 추론(Inference) 단계의 물리적 한계 극복 전략**

모델의 아키텍처 개선만으로는 고해상도 영상을 완벽하게 소화할 수 없다. 원본 영상의 픽셀 정보를 신경망 내에서 온전히 유지하기 위해서는 추론 단계에서의 이미지 분할 처리 기법과 컴퓨팅 자원 할당 전략이 정교하게 결합되어야 한다.

### **3.1 SAHI (Slicing Aided Hyper Inference) 도입의 효용성과 한계**

SAHI 알고리즘은 대형 이미지를 모델의 학습 해상도(예: 640x640)에 맞게 강제로 축소하는 대신, 이미지를 겹치는 여러 개의 패치(Tile)로 잘라서 각각 추론한 후 원래의 좌표계로 병합하는 기술이다.3 이 방식을 사용하면 CCTV 영상의 수십 픽셀짜리 작업자가 리사이징 과정에서 뭉개지지 않고 온전한 픽셀 형태를 유지한 채 네트워크에 입력되므로, 탐지 성공률이 극적으로 상승한다. 24에 따르면 차량 탐지 실험에서 SAHI 적용 후 재현율(Recall)이 31.8%에서 86.4%로 상승하는 등 경이로운 성능 개선이 입증되었다.24

그러나 SAHI는 치명적인 연산량의 증가(Trade-off)를 동반한다.25 1280x1280 해상도의 이미지를 640x640 크기로 슬라이싱할 경우, 단 한 장의 원본 이미지를 처리하기 위해 신경망은 여러 번(예: 중첩 영역을 포함하여 최소 4\~6회)의 순전파(Forward pass) 연산을 수행해야 한다.3

| 입력 해상도 및 처리 방식 | 추정 VRAM 소모량 | 전처리 시간 (ms) | 평균 추론 시간 (ms) | 적용 가능성 및 한계 |
| :---- | :---- | :---- | :---- | :---- |
| **640x640 단일 추론** | 약 1,424 MB | \~2.7 ms | \~20 \- 43 ms | 빠르나 소형 객체 탐지 실패 26 |
| **1280x1280 단일 추론** | 약 1,424 MB | \~9.2 ms | \~83 \- 173 ms | 속도 저하, VRAM 효율적이나 해상도 손실 잔존 26 |
| **SAHI (다중 슬라이스 패치)** | 1,600 MB 이상 (배치 처리 시) | 슬라이스 수에 비례 | **150 \- 300 ms 이상** | **속도는 크게 저하되나(4\~6 FPS), 탐지 정확도는 기하급수적으로 상승** 25 |

참고: 위 데이터는 TensorRT를 적용한 환경에서의 근사치이며, 하드웨어 사양에 따라 변동될 수 있다.26

### **3.2 실시간성 확보를 위한 TensorRT 및 엣지 컴퓨팅 최적화**

SAHI의 무거운 연산량을 건설 현장의 실시간 모니터링 시스템에 적용하기 위해서는 하드웨어 최적화가 필수적이다. 파이썬(Python) 기반의 PyTorch 모델을 NVIDIA TensorRT 엔진으로 변환(.engine 포맷)하면, 레이어 융합(Layer fusion)과 INT8 또는 FP16 정밀도 양자화(Quantization)를 통해 추론 속도를 최대 3\~5배가량 가속할 수 있다.27

또한, 여러 개의 SAHI 잘라낸 이미지를 루프(Loop)를 돌며 순차적으로 처리하는 대신, C++ 환경을 구축하여 배치(Batch) 차원으로 한 번에 텐서 코어에 밀어 넣는 방식이 요구된다.30 이러한 병렬 처리를 소화하기 위해서는 NVIDIA Jetson AGX Orin 또는 RTX 4090과 같이 VRAM(최소 12GB 이상 권장) 대역폭이 풍부하고 병렬 연산 코어가 강력한 엣지 디바이스 및 서버 아키텍처가 동반되어야 한다.32

## **4\. 데이터 중심(Data-Centric) 접근: 파인튜닝 데이터셋 및 합성 데이터**

강력한 모델과 효율적인 추론 방식이 준비되었더라도, 모델이 고각에서 바라보는 객체의 패턴을 한 번도 학습하지 못했다면 성능 향상은 기대할 수 없다. COCO 데이터셋은 대부분 정면 눈높이에서 촬영된 사진으로 구성되어 있어 건설 현장 CCTV 데이터의 분포와는 판이하게 다르다.

### **4.1 고각 특화 오픈소스 데이터셋 도입**

모델의 사전 학습(Pre-training)이나 파인튜닝(Fine-tuning) 단계에서 다음과 같은 고각 및 건설 현장 특화 데이터를 반드시 주입하여 데이터 도메인을 일치시켜야 한다.

* **SODA (Site Object Detection dAtaset):** 건설 현장 환경을 위해 특수하게 구축된 약 2만 장 규모의 거대 데이터셋이다. 특히 SODA 데이터셋의 하위 분류인 **SODA-A (Aerial)** 데이터셋은 2,513장의 초고해상도 공중 촬영 이미지와 872,069개의 인스턴스(객체)를 포함하고 있다.35 회전된 바운딩 박스(Oriented bounding box)를 지원하며 작업자, 굴삭기, 안전모 등 건설 현장의 필수 클래스가 위에서 내려다보는 시점으로 정밀하게 라벨링 되어 있어 본 과제의 가장 핵심적인 외부 데이터가 될 수 있다.37  
* **UAVDT (Unmanned Aerial Vehicle Benchmark):** 80,000장에 달하는 드론 촬영 이미지로 구성되어 있다. 소형 객체의 밀집, 카메라 각도의 변화, 객체의 크기 변환 등을 모델이 학습하는 데 최적화되어 있다.39  
* **VisDrone:** 다양한 도심 및 교외 환경에서 드론으로 촬영된 이미지로 구성되며, 복잡한 배경 속에서 수십 픽셀 크기의 사람을 분간해 내는 배경 노이즈 억제 능력을 키우는 데 기여한다.41

또한 Nexdata 등 상용 데이터 제공업체는 아시아인 배경의 실내외 건설 현장 이미지 58,255장과 안전모, 안전 조끼가 마킹된 60만 개 이상의 정밀 바운딩 박스 데이터를 판매하고 있다. 라벨링에 소모되는 시간과 비용을 고려할 때, 상용 데이터를 구매하는 것이 프로젝트의 타임 투 마켓(Time-to-market)을 앞당기는 효과적인 전략이 될 수 있다.42

### **4.2 게임 엔진과 생성 AI를 융합한 합성 데이터(Synthetic Data) 생성**

데이터셋 수집의 가장 큰 장벽인 '보호구 미착용(NO-Hardhat)' 클래스의 절대적 부족 문제는 물리적인 현장 촬영만으로는 단기간에 해결할 수 없다. 이를 타개할 혁신적인 방법은 '안전 임계 합성 데이터(Safety-Critical Synthetic Data)' 파이프라인의 구축이다.43

**Unity Perception을 활용한 디지털 트윈 시뮬레이션:** Unity 3D 게임 엔진과 Perception 패키지를 활용하면 가상의 건설 현장을 시뮬레이션할 수 있다. 이 환경 내에 안전모를 쓰지 않은 가상의 3D 작업자 모델을 배치하고, 카메라의 위치를 15m, 20m, 30m 높이의 다양한 각도로 설정한다.44 엔진의 '도메인 무작위화(Domain Randomization)' 기능을 통해 빛의 방향, 그림자, 질감 등을 무한대로 변형하여 수만 장의 고각 NO-Hardhat 이미지를 버튼 클릭 한 번으로 생성할 수 있다. 이때 모든 픽셀의 라벨링 데이터(바운딩 박스, 분할 마스크)는 엔진에서 100%의 정확도로 자동 추출된다.46

**Stable Diffusion 기반의 현실화(Reality Gap 보정):** 3D 그래픽 엔진이 생성한 데이터는 픽셀의 질감이 현실과 미세하게 달라 모델이 현장에 적용되었을 때 성능 저하(Reality Gap)를 유발할 수 있다. 이를 보완하기 위해 Stable Diffusion과 같은 생성형 AI(Generative AI)의 Image-to-Image 기술을 활용한다. Unity에서 생성된 합성 데이터를 입력으로 넣고 적절한 텍스트 프롬프트를 부여하여 CCTV의 렌즈 왜곡, 현장의 흙먼지 노이즈, 자연광의 반사 등을 덧입힘으로써 물리적으로 촬영된 사진과 구별할 수 없는 최고 품질의 희소 클래스 데이터를 대량으로 양산할 수 있다.48

## **5\. 클래스 불균형(Class Imbalance) 타개를 위한 손실 함수 최적화**

합성 데이터로 NO-Hardhat 클래스의 절대적인 수를 늘리더라도, 여전히 대다수의 정상 작업자와 배경 데이터가 학습을 지배할 가능성이 크다. 따라서 알고리즘 내부적으로 소수 클래스를 보호하는 메커니즘이 강제되어야 한다.

### **5.1 Focal Loss의 도입과 하이퍼파라미터 튜닝**

앞서 진단한 2.8%의 mAP는 다수 클래스에 압도당하는 Cross-Entropy의 약점 때문이다. 이를 교정하기 위해 **Focal Loss**를 적용해야 한다.8 Focal Loss는 모델이 이미 쉽게 맞추고 있는 다수 데이터(예: 명확하게 잘 보이는 안전모)에서 발생하는 손실 값을 0에 가깝게 억눌러 버리고, 모델이 지속적으로 헷갈려 하는 어려운 데이터(예: 배경과 색상이 비슷한 헬멧 미착용 작업자)에 가중치를 부여한다.51

* **알파(![][image1]) 파라미터 조정:** 클래스 간의 데이터 비율을 보정하는 역할을 한다. NO-Hardhat 클래스에 높은 가중치를 주어 해당 객체의 특징이 나타날 때 발생하는 그래디언트의 크기를 의도적으로 증폭시킨다.52  
* **감마(![][image2]) 파라미터 조정:** '쉬운 예제'를 얼마나 강력하게 무시할 것인지를 결정한다. 이 값을 높임으로써 네트워크는 학습의 후반부에서도 끊임없이 소수 클래스의 미세한 패턴을 찾는 데 최적화 자원을 집중하게 된다.50

### **5.2 동적 오버샘플링(Dynamic Oversampling) 및 Copy-Paste 증강**

학습 데이터 파이프라인(Dataloader) 단에서 극단적인 데이터 증강 기법을 함께 적용해야 한다. **동적 클래스 균형 Copy-Paste (Dynamic Class-balanced Copy-Paste, DCC)** 기법은 이미지 내에서 소형 객체나 희소 클래스를 분리한 뒤, 다른 학습 이미지의 빈 공간에 동적으로 합성해 넣는 기술이다.9 이 방식을 사용하면 모델이 배치(Batch)를 불러올 때마다 반드시 NO-Hardhat 클래스를 포함하게 되며, 모델이 해당 클래스의 공간적 맥락(Spatial context)을 잃지 않고 꾸준히 학습하도록 강제할 수 있다.7

## **6\. 전략적 대안: 상용 API 및 SaaS 솔루션(Buy)의 타당성 평가**

모델 아키텍처 개조(P2 레이어, NWD 손실 등), SAHI 파이프라인의 엣지 구축, 합성 데이터 시뮬레이터 개발은 방대한 머신러닝 엔지니어링 리소스(MLOps)와 수억 원 규모의 초기 자본 투자(CapEx)를 요구한다. AI 모델 내재화가 핵심 비즈니스가 아닌 건설 기업의 경우, 수백만 장의 산업 데이터로 이미 파인튜닝이 완료된 상용 SaaS(Software-as-a-Service) 플랫폼을 도입하는 것이 총소유비용(TCO) 측면에서 압도적으로 유리할 수 있다.55

### **6.1 핵심 상용 솔루션 비교 분석**

현재 건설 및 중공업 안전 감지 시장에서 가장 높은 점유율과 성능을 보여주는 상용 플랫폼들을 비교하면 다음과 같다.

| 플랫폼(Vendor) | 핵심 강점 및 특화 영역 | 구현 방식 및 인프라 | 과금 구조 (추정치) | 한계점 및 특이사항 |
| :---- | :---- | :---- | :---- | :---- |
| **viAct** | **건설 현장 특화**, PPE 및 위험 구역, 장비 충돌 방지 56 | 기존 CCTV를 클라우드나 엣지에 연결(플러그 앤 플레이). 30개 이상의 기성 시나리오 모듈 보유 58 | 모듈/카메라당 **월 $100\~$200 내외** 60 | 타 사 시스템과의 API 통합이 다소 제한적임 62 |
| **Intenseye** | 대규모 제조 및 산업 시설의 SIF(중대재해) 실시간 감지 63 | 클라우드, 프라이빗 클라우드, 하이브리드 온프레미스 모두 지원. 50개 이상의 자동 감지 기능 내장 63 | 맞춤형 엔터프라이즈 견적 (통상적으로 대규모 도입 시 유리) 64 | 개별 건설 현장보다는 전사적(Enterprise) 차원의 통합 모니터링에 초점 59 |
| **Spot AI** | 영상 검색(자연어 기반) 및 다중 현장 보안 관리 62 | 하이브리드(Cloud \+ Edge) 환경, 모든 IP 카메라 지원, 무제한 클라우드 백업 62 | 구독형 및 장비 번들 모델 | 건설 환경 특화 모듈보다는 범용 보안/운영 관리에 치중됨 62 |
| **Safesite** | 모바일 기반 현장 점검, 규제 준수 및 사고 문서화 자동화 연계 67 | 앱 기반 점검, 문서화 중심 플랫폼. (영상 분석보다는 절차 준수 초점) 69 | **무료 버전 제공**, 프리미엄 월 $20/인 67 | AI 객체 탐지 엔진(Computer Vision)보다는 워크플로우 관리에 특화됨 66 |
| **Matroid** | 맞춤형 기계 비전(Custom Machine Vision) 디텍터 생성 플랫폼 71 | 노코드(No-code) 인터페이스로 사용자가 직접 관심 객체를 지정하고 AI 학습 수행 71 | 크레딧 기반 종량제 / 커스텀 견적 | 현장별로 특수한 장비나 변칙적인 상황을 직접 학습시켜야 할 때 강력함 71 |

### **6.2 Build vs. Buy : 전략적 TCO(총소유비용) 판단**

**자체 개발(Build) 모델**은 초기 구축 비용이 막대하다. C3k2, C2PSA 블록을 수정하는 아키텍처 설계와 Unity 기반 합성 데이터 파이프라인 구축을 위해서는 연봉 10만\~20만 달러에 달하는 고급 AI 인력과 4만 달러를 호가하는 고성능 GPU(A100 등) 인프라가 필수적이다.73 엣지 디바이스 역시 현장당 2천 달러 이상의 NVIDIA 장비가 필요하다. 그러나 수십 개의 현장, 수천 대의 카메라로 확산될 경우 한계 비용이 급격히 낮아지며 기업의 민감한 보안 데이터를 내부망(On-premise)에서 완벽히 통제할 수 있다는 강력한 이점이 있다.73

반면, **상용 서비스(Buy) 모델**은 당장의 자본 지출(CapEx)을 획기적으로 줄여준다.55 예를 들어 viAct를 도입할 경우 카메라 10대를 운영하는 단일 현장에서 월 1,000\~2,000달러 수준의 운영비(OpEx)만으로, 수백만 장의 건설 데이터를 학습한 대기업 수준의 알고리즘을 즉각적으로 활용할 수 있다.56 이들은 고각에서 발생하는 소형 객체 인식 문제나 보호구 미착용자의 데이터 부족 문제를 이미 자체적인 대규모 데이터 풀로 극복한 상태이다.

따라서 회사의 핵심 역량이 소프트웨어 개발에 있지 않거나 즉각적인 현장 안전 준수(OSHA 등) 입증이 필요한 경우, 2단계 이상의 파인튜닝을 자체적으로 진행하기보다는 **viAct**나 **Intenseye**와 같이 검증된 SaaS 플랫폼을 현장에 우선 배포하는 것이 기술적·재무적 타당성이 가장 높다.56

## **7\. 종합 결론 및 문제 해결을 위한 실행 로드맵**

제시된 정량 및 정성 평가 결과를 종합할 때, 현재 상태의 범용 YOLO 모델을 이용한 고각 CCTV 인물 탐지 및 보호구 미착용 판별은 물리적 한계로 인해 불가능하다(No-Go). 이 한계를 돌파하기 위해서는 해상도 손실, 바운딩 박스의 수학적 불안정성, 클래스 불균형이라는 세 가지 근본 원인을 입체적으로 타격하는 융합적 접근이 요구된다. 이를 실무 환경에 안착시키기 위해 다음과 같은 3단계 실행 로드맵을 제안한다.

* **1단계: 즉각적 추론 최적화 및 타당성 검토 (1\~3주차)**  
  * **과제:** 현재 보유한 모델(YOLOv11m)에 별도의 재학습 없이 SAHI(Slicing Aided Hyper Inference) 파이프라인을 즉시 연결하여 고각 CCTV 영상(Subway/Tower crane)에서의 탐지 성공률 회복 여부를 테스트한다.  
  * **목표:** 해상도 보존이 소형 객체 탐지에 미치는 효과를 확인하고, 시스템의 추론 지연(Latency)이 감내할 수 있는 수준(예: 2\~5 FPS)인지 평가한다. 동시에 TensorRT 엔진 변환을 통해 GPU 리소스 최적화율을 산출한다.  
* **2단계: 데이터셋 대규모 확장 및 손실 함수 튜닝 (4\~8주차)**  
  * **과제:** 공공 데이터셋인 SODA-A와 UAVDT를 확보하여 백그라운드 맥락으로 추가하고, Unity 3D와 Stable Diffusion 파이프라인을 구축하여 고각 45도에서 바라본 '안전모 미착용(NO-Hardhat)' 작업자의 합성 데이터를 최소 1만 장 이상 양산한다.  
  * **목표:** 데이터 풀 내 클래스 균형을 1:1에 가깝게 맞추고, 학습 알고리즘에 Focal Loss를 적용하여 감마(![][image2]) 계수를 점진적으로 높여 소수 클래스에 대한 식별 능력을 강제 주입한다.  
* **3단계: 아키텍처 개조 및 최종 배포 결정 (9\~12주차)**  
  * **과제:** 1, 2단계를 통해 확보된 최적의 데이터셋을 바탕으로, 기존 P5 레이어를 제거하고 P2 초고해상도 레이어를 추가한 커스텀 모델 구조(예: DMS-YOLO 또는 FDM-YOLO의 구조 차용)를 설계한다. 동시에 바운딩 박스 손실 함수를 NWD(Normalized Wasserstein Distance)로 교체하여 재학습을 수행한다.  
  * **목표:** 자체 구축(Build)한 모델의 성능(mAP 및 Recall)이 85% 이상의 상용화 수준에 도달하는지 평가한다. 만약 엔지니어링 리소스 및 TCO의 제약으로 이 목표 도달이 지연될 경우, 즉각적으로 viAct 등 외부 상용 솔루션(Buy) 도입으로 방향을 선회하여 건설 현장의 안전 공백을 차단한다.

결론적으로, 고각 CCTV 환경에서의 추적 및 객체 인식 한계는 기술적으로 명확히 극복 가능한 영역에 진입해 있다. 앞서 서술한 아키텍처의 혁신, SAHI와 엣지 컴퓨팅의 결합, 그리고 합성 데이터를 동반한 데이터 중심(Data-Centric)의 튜닝 기법을 체계적으로 적용하거나, 산업에 특화된 상용 솔루션을 채택함으로써 현존하는 모든 위험 요소를 통제할 수 있는 강건한 안전 모니터링 시스템을 구축할 수 있을 것이다.

#### **참고 자료**

1. \[2503.20516\] Small Object Detection: A Comprehensive Survey on Challenges, Techniques and Real-World Applications \- arXiv.org, 3월 18, 2026에 액세스, [https://arxiv.org/abs/2503.20516](https://arxiv.org/abs/2503.20516)  
2. MS-YOLOv11: A Wavelet-Enhanced Multi-Scale Network for Small Object Detection in Remote Sensing Images \- PMC, 3월 18, 2026에 액세스, [https://pmc.ncbi.nlm.nih.gov/articles/PMC12526788/](https://pmc.ncbi.nlm.nih.gov/articles/PMC12526788/)  
3. How to Accurately Detect Small Objects with YOLO and Sahi \- Pysource, 3월 18, 2026에 액세스, [https://pysource.com/2025/04/23/how-to-accurately-detect-small-objects-with-yolo-and-sahi/](https://pysource.com/2025/04/23/how-to-accurately-detect-small-objects-with-yolo-and-sahi/)  
4. A Comparative Analysis of YOLOv11 Models: Impact of Object Size on Detection Performance \- Diva-Portal.org, 3월 18, 2026에 액세스, [https://www.diva-portal.org/smash/get/diva2:1985752/FULLTEXT01.pdf](https://www.diva-portal.org/smash/get/diva2:1985752/FULLTEXT01.pdf)  
5. Advancements in Small-Object Detection (2023–2025): Approaches, Datasets, Benchmarks, Applications, and Practical Guidance \- MDPI, 3월 18, 2026에 액세스, [https://www.mdpi.com/2076-3417/15/22/11882](https://www.mdpi.com/2076-3417/15/22/11882)  
6. How to Deal with Imbalanced Datasets in Computer Vision \- Picsellia, 3월 18, 2026에 액세스, [https://www.picsellia.com/post/improve-imbalanced-datasets-in-computer-vision](https://www.picsellia.com/post/improve-imbalanced-datasets-in-computer-vision)  
7. How to Handle Unbalanced Classes: 5 Strategies \- Roboflow Blog, 3월 18, 2026에 액세스, [https://blog.roboflow.com/handling-unbalanced-classes/](https://blog.roboflow.com/handling-unbalanced-classes/)  
8. How Focal Loss fixes the Class Imbalance problem in Object Detection | by Yash \- Medium, 3월 18, 2026에 액세스, [https://medium.com/analytics-vidhya/how-focal-loss-fixes-the-class-imbalance-problem-in-object-detection-3d2e1c4da8d7](https://medium.com/analytics-vidhya/how-focal-loss-fixes-the-class-imbalance-problem-in-object-detection-3d2e1c4da8d7)  
9. A Data Augmentation Methodology to Reduce the Class Imbalance in Histopathology Images \- PMC, 3월 18, 2026에 액세스, [https://pmc.ncbi.nlm.nih.gov/articles/PMC11300732/](https://pmc.ncbi.nlm.nih.gov/articles/PMC11300732/)  
10. Small Object Detection: A Comprehensive Survey on Challenges, Techniques and Real-World Applications \- ResearchGate, 3월 18, 2026에 액세스, [https://www.researchgate.net/publication/390213601\_Small\_Object\_Detection\_A\_Comprehensive\_Survey\_on\_Challenges\_Techniques\_and\_Real-World\_Applications](https://www.researchgate.net/publication/390213601_Small_Object_Detection_A_Comprehensive_Survey_on_Challenges_Techniques_and_Real-World_Applications)  
11. DMS-YOLO: Small target detection algorithm based on YOLOv11 \- PMC, 3월 18, 2026에 액세스, [https://pmc.ncbi.nlm.nih.gov/articles/PMC12858059/](https://pmc.ncbi.nlm.nih.gov/articles/PMC12858059/)  
12. Enhanced YOLOv11n for small object detection in UAV imagery: higher accuracy with fewer parameters \- PMC, 3월 18, 2026에 액세스, [https://pmc.ncbi.nlm.nih.gov/articles/PMC12887013/](https://pmc.ncbi.nlm.nih.gov/articles/PMC12887013/)  
13. ultralytics/ultralytics/cfg/models/11/yolo11.yaml at main \- GitHub, 3월 18, 2026에 액세스, [https://github.com/ultralytics/ultralytics/blob/main/ultralytics/cfg/models/11/yolo11.yaml](https://github.com/ultralytics/ultralytics/blob/main/ultralytics/cfg/models/11/yolo11.yaml)  
14. yolo11-p2.yaml · davsolai/yolo11x-p2-coco at main \- Hugging Face, 3월 18, 2026에 액세스, [https://huggingface.co/davsolai/yolo11x-p2-coco/blob/main/yolo11-p2.yaml](https://huggingface.co/davsolai/yolo11x-p2-coco/blob/main/yolo11-p2.yaml)  
15. A lightweight model FDM-YOLO for small target improvement based on YOLOv8 \- arXiv, 3월 18, 2026에 액세스, [https://arxiv.org/abs/2503.04452](https://arxiv.org/abs/2503.04452)  
16. A Lightweight and Effective YOLO Model for Infrared Small Object Detection | International Journal of Pattern Recognition and Artificial Intelligence \- World Scientific Publishing, 3월 18, 2026에 액세스, [https://www.worldscientific.com/doi/10.1142/S0218001425510097](https://www.worldscientific.com/doi/10.1142/S0218001425510097)  
17. YOLO-PDNet: Small Target Recognition Improvement for Remote Sensing Image Based on YOLOv8 \- IEEE Xplore, 3월 18, 2026에 액세스, [https://ieeexplore.ieee.org/document/10650721/](https://ieeexplore.ieee.org/document/10650721/)  
18. \[2110.13389\] A Normalized Gaussian Wasserstein Distance for Tiny Object Detection \- arXiv, 3월 18, 2026에 액세스, [https://arxiv.org/abs/2110.13389](https://arxiv.org/abs/2110.13389)  
19. Wasserstein Loss-Based Deep Object Detection \- CVF Open Access, 3월 18, 2026에 액세스, [https://openaccess.thecvf.com/content\_CVPRW\_2020/papers/w60/Han\_Wasserstein\_Loss-Based\_Deep\_Object\_Detection\_CVPRW\_2020\_paper.pdf](https://openaccess.thecvf.com/content_CVPRW_2020/papers/w60/Han_Wasserstein_Loss-Based_Deep_Object_Detection_CVPRW_2020_paper.pdf)  
20. Fine-YOLO: A Simplified X-ray Prohibited Object Detection Network Based on Feature Aggregation and Normalized Wasserstein Distance \- MDPI, 3월 18, 2026에 액세스, [https://www.mdpi.com/1424-8220/24/11/3588](https://www.mdpi.com/1424-8220/24/11/3588)  
21. DMS-YOLO: Small target detection algorithm based on YOLOv11 | PLOS One, 3월 18, 2026에 액세스, [https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0341991](https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0341991)  
22. FDM-RTDETR: A Multi-Scale Small Target Detection Algorithm \- IEEE Xplore, 3월 18, 2026에 액세스, [https://ieeexplore.ieee.org/iel8/6287639/10820123/11006668.pdf](https://ieeexplore.ieee.org/iel8/6287639/10820123/11006668.pdf)  
23. YOLOv8 Small Object Detection With SAHI In Python | Sliced Inference \- Eran Feit, 3월 18, 2026에 액세스, [https://eranfeit.net/how-to-detect-small-objects-with-yolov8-and-sahi/](https://eranfeit.net/how-to-detect-small-objects-with-yolov8-and-sahi/)  
24. Small Object Detection using YOLO with SAHI Explained \- Labellerr, 3월 18, 2026에 액세스, [https://www.labellerr.com/blog/small-object-detection/](https://www.labellerr.com/blog/small-object-detection/)  
25. High-Precision Marine Radar Object Detection Using Tiled Training and SAHI Enhanced YOLOv11-OBB \- MDPI, 3월 18, 2026에 액세스, [https://www.mdpi.com/1424-8220/26/3/942](https://www.mdpi.com/1424-8220/26/3/942)  
26. Does SAHI with YOLO11 make sense \- Discussion \- Ultralytics, 3월 18, 2026에 액세스, [https://community.ultralytics.com/t/does-sahi-with-yolo11-make-sense/1465](https://community.ultralytics.com/t/does-sahi-with-yolo11-make-sense/1465)  
27. Model Benchmarking with Ultralytics YOLO, 3월 18, 2026에 액세스, [https://docs.ultralytics.com/modes/benchmark/](https://docs.ultralytics.com/modes/benchmark/)  
28. How to Speed Up Deep Learning Inference Using TensorRT | NVIDIA Technical Blog, 3월 18, 2026에 액세스, [https://developer.nvidia.com/blog/speed-up-inference-tensorrt/](https://developer.nvidia.com/blog/speed-up-inference-tensorrt/)  
29. Speeding Up Deep Learning Inference Using TensorRT | NVIDIA Technical Blog, 3월 18, 2026에 액세스, [https://developer.nvidia.com/blog/speeding-up-deep-learning-inference-using-tensorrt/](https://developer.nvidia.com/blog/speeding-up-deep-learning-inference-using-tensorrt/)  
30. guides/sahi-tiled-inference/ · ultralytics · Discussion \#8121 \- GitHub, 3월 18, 2026에 액세스, [https://github.com/orgs/ultralytics/discussions/8121](https://github.com/orgs/ultralytics/discussions/8121)  
31. TensorRT \+ SAHI ? : r/computervision \- Reddit, 3월 18, 2026에 액세스, [https://www.reddit.com/r/computervision/comments/1lchcdx/tensorrt\_sahi/](https://www.reddit.com/r/computervision/comments/1lchcdx/tensorrt_sahi/)  
32. Comparison of YOLOv8 and YOLO11 performance across RTX 4080 and Jetson... | Download Scientific Diagram \- ResearchGate, 3월 18, 2026에 액세스, [https://www.researchgate.net/figure/Comparison-of-YOLOv8-and-YOLO11-performance-across-RTX-4080-and-Jetson-AGX-Orin-The\_fig8\_391579902](https://www.researchgate.net/figure/Comparison-of-YOLOv8-and-YOLO11-performance-across-RTX-4080-and-Jetson-AGX-Orin-The_fig8_391579902)  
33. Yolo Speed Test On Jetson: Orin Nano Super • AGX Orin • AGX Thor \- YouTube, 3월 18, 2026에 액세스, [https://www.youtube.com/watch?v=MnaohuzEuhA](https://www.youtube.com/watch?v=MnaohuzEuhA)  
34. System Hardware Requirements for YOLO in 2025 \- ProX PC, 3월 18, 2026에 액세스, [https://www.proxpc.com/blogs/system-hardware-requirements-for-yolo-in-2025](https://www.proxpc.com/blogs/system-hardware-requirements-for-yolo-in-2025)  
35. SODA: Site Object Detection dAtaset for Deep Learning in Construction \- SciSpace, 3월 18, 2026에 액세스, [https://scispace.com/pdf/soda-site-object-detection-dataset-for-deep-learning-in-269g29rh.pdf](https://scispace.com/pdf/soda-site-object-detection-dataset-for-deep-learning-in-269g29rh.pdf)  
36. danielopisani/SODA-Dataset \- GitHub, 3월 18, 2026에 액세스, [https://github.com/danielopisani/SODA-Dataset](https://github.com/danielopisani/SODA-Dataset)  
37. SODA: Site Object Detection dAtaset for Deep Learning in Construction \- Jia-Rui Lin's Page, 3월 18, 2026에 액세스, [https://linjiarui.net/en/portfolio/2022-02-22-SODA-site-object-detection-dataset-for-deep-learning-in-construction](https://linjiarui.net/en/portfolio/2022-02-22-SODA-site-object-detection-dataset-for-deep-learning-in-construction)  
38. A large-scale Small Object Detection dAtaset | SODA \- GitHub Pages, 3월 18, 2026에 액세스, [https://shaunyuan22.github.io/SODA/](https://shaunyuan22.github.io/SODA/)  
39. UAVDT \- Dataset Ninja, 3월 18, 2026에 액세스, [https://datasetninja.com/uavdt](https://datasetninja.com/uavdt)  
40. The Unmanned Aerial Vehicle Benchmark: Object Detection and Tracking \- CVF Open Access, 3월 18, 2026에 액세스, [https://openaccess.thecvf.com/content\_ECCV\_2018/papers/Dawei\_Du\_The\_Unmanned\_Aerial\_ECCV\_2018\_paper.pdf](https://openaccess.thecvf.com/content_ECCV_2018/papers/Dawei_Du_The_Unmanned_Aerial_ECCV_2018_paper.pdf)  
41. MMOT: The First Challenging Benchmark for Drone-based Multispectral Multi-Object Tracking \- arXiv.org, 3월 18, 2026에 액세스, [https://arxiv.org/html/2510.12565v1](https://arxiv.org/html/2510.12565v1)  
42. Construction Site Object Detection Dataset – 58,255 Images with Safety Helmets and Vests, 3월 18, 2026에 액세스, [https://www.nexdata.ai/datasets/computervision/1220](https://www.nexdata.ai/datasets/computervision/1220)  
43. Safety-Critical Synthetic Data \- Emergent Mind, 3월 18, 2026에 액세스, [https://www.emergentmind.com/topics/safety-critical-synthetic-data](https://www.emergentmind.com/topics/safety-critical-synthetic-data)  
44. Utilizing 360-Degree Images for Synthetic Data Generation in Construction Scenarios \- Firenze University Press, 3월 18, 2026에 액세스, [https://books.fupress.com/chapter/utilizing-360-degree-images-for-synthetic-data-generation-in-construction-scenarios/14457](https://books.fupress.com/chapter/utilizing-360-degree-images-for-synthetic-data-generation-in-construction-scenarios/14457)  
45. Perception Synthetic Data Tutorial \- Unity 6.3 User Manual, 3월 18, 2026에 액세스, [https://docs.unity3d.com/Packages/com.unity.perception@1.0/manual/Tutorial/TUTORIAL.html](https://docs.unity3d.com/Packages/com.unity.perception@1.0/manual/Tutorial/TUTORIAL.html)  
46. Harnessing Synthetic Image Datasets for Enhanced Scene Understanding in Construction Work Zones, 3월 18, 2026에 액세스, [https://workzonesafety.org/publication/harnessing-synthetic-image-datasets-for-enhanced-scene-understanding-in-construction-work-zones/](https://workzonesafety.org/publication/harnessing-synthetic-image-datasets-for-enhanced-scene-understanding-in-construction-work-zones/)  
47. Unity Perception: Beginner Tutorial (for Synthetic Image Data) \- YouTube, 3월 18, 2026에 액세스, [https://www.youtube.com/watch?v=mkVE2Yhe454](https://www.youtube.com/watch?v=mkVE2Yhe454)  
48. Training Dataset Generation through Generative AI for Multi-Modal Safety Monitoring in Construction \- KoreaScience, 3월 18, 2026에 액세스, [https://koreascience.kr/article/CFKO202431947345213.do](https://koreascience.kr/article/CFKO202431947345213.do)  
49. Synthetic Data Generation with Stable Diffusion: A Guide \- Roboflow Blog, 3월 18, 2026에 액세스, [https://blog.roboflow.com/synthetic-data-with-stable-diffusion-a-guide/](https://blog.roboflow.com/synthetic-data-with-stable-diffusion-a-guide/)  
50. How to Fix Imbalanced Classes with Focal Loss | by Natthawat Phongchit | Medium, 3월 18, 2026에 액세스, [https://medium.com/@natthawatphongchit/how-to-fix-imbalanced-classes-with-focal-loss-559de3ef94a3](https://medium.com/@natthawatphongchit/how-to-fix-imbalanced-classes-with-focal-loss-559de3ef94a3)  
51. Class Imbalance in Computer Vision, Explained \- Tutorials \- Datature, 3월 18, 2026에 액세스, [https://datature.io/tutorials/class-imbalance-in-computer-vision-explained](https://datature.io/tutorials/class-imbalance-in-computer-vision-explained)  
52. Class Imbalance · Issue \#20838 \- GitHub, 3월 18, 2026에 액세스, [https://github.com/ultralytics/ultralytics/issues/20838](https://github.com/ultralytics/ultralytics/issues/20838)  
53. Focal Loss in Object Detection: A Comprehensive Guide for 2025 \- Shadecoder \- 100% Invisibile AI Coding Interview Copilot, 3월 18, 2026에 액세스, [https://www.shadecoder.com/topics/focal-loss-in-object-detection-a-comprehensive-guide-for-2025](https://www.shadecoder.com/topics/focal-loss-in-object-detection-a-comprehensive-guide-for-2025)  
54. AD-Det: Boosting Object Detection in UAV Images with Focused Small Objects and Balanced Tail Classes \- MDPI, 3월 18, 2026에 액세스, [https://www.mdpi.com/2072-4292/17/9/1556](https://www.mdpi.com/2072-4292/17/9/1556)  
55. Build vs Buy: AI Vision in 2025 | API4AI \- Medium, 3월 18, 2026에 액세스, [https://medium.com/@API4AI/build-or-buy-how-to-make-the-right-choice-d96f501095ce](https://medium.com/@API4AI/build-or-buy-how-to-make-the-right-choice-d96f501095ce)  
56. viAct: Reviews, Pricing, Features in 2026 \- Software Suggest, 3월 18, 2026에 액세스, [https://www.softwaresuggest.com/viact](https://www.softwaresuggest.com/viact)  
57. viAct Software Reviews, Demo & Pricing \- 2026, 3월 18, 2026에 액세스, [https://www.softwareadvice.com/construction/viact-profile/](https://www.softwareadvice.com/construction/viact-profile/)  
58. viAct \- AI Monitoring That Redefines Workplace Safety, 3월 18, 2026에 액세스, [https://www.viact.ai/](https://www.viact.ai/)  
59. Top Web-Based AI Workplace Safety Software in 2025 \- Slashdot, 3월 18, 2026에 액세스, [https://slashdot.org/software/ai-workplace-safety/saas/](https://slashdot.org/software/ai-workplace-safety/saas/)  
60. viAct: Pricing, Free Demo & Features \- Software Finder, 3월 18, 2026에 액세스, [https://softwarefinder.com/construction/viact](https://softwarefinder.com/construction/viact)  
61. Intenseye vs. viAct.ai Comparison \- SourceForge, 3월 18, 2026에 액세스, [https://sourceforge.net/software/compare/Intenseye-vs-viAct/](https://sourceforge.net/software/compare/Intenseye-vs-viAct/)  
62. AI Video Analytics & Tools for Construction Sites: 2025 Comparison Guide | Spot AI, 3월 18, 2026에 액세스, [https://www.spot.ai/blog/ai-video-analytics-tools-construction-2025-guide](https://www.spot.ai/blog/ai-video-analytics-tools-construction-2025-guide)  
63. Intenseye Reviews 2026: Details, Pricing, & Features \- G2, 3월 18, 2026에 액세스, [https://www.g2.com/products/intenseye/reviews](https://www.g2.com/products/intenseye/reviews)  
64. Intenseye \- Key features, use cases, pricing, alternatives \- Cybernews, 3월 18, 2026에 액세스, [https://cybernews.com/ai-knowledge-base/tools/intenseye/](https://cybernews.com/ai-knowledge-base/tools/intenseye/)  
65. Intenseye: Pricing, Free Demo & Features \- Software Finder, 3월 18, 2026에 액세스, [https://softwarefinder.com/manufacturing-software/intenseye](https://softwarefinder.com/manufacturing-software/intenseye)  
66. Compare Matroid vs. viAct.ai in 2026 \- Slashdot, 3월 18, 2026에 액세스, [https://slashdot.org/software/comparison/Matroid-vs-viAct/](https://slashdot.org/software/comparison/Matroid-vs-viAct/)  
67. Safesite Software Reviews, Demo & Pricing \- 2026, 3월 18, 2026에 액세스, [https://www.softwareadvice.com/audit/safesite-profile/](https://www.softwareadvice.com/audit/safesite-profile/)  
68. Safesite Software Pricing, Alternatives & More 2026 \- Capterra, 3월 18, 2026에 액세스, [https://www.capterra.com/p/165101/Safesite/](https://www.capterra.com/p/165101/Safesite/)  
69. Safesite: Best-in-Class Safety Management System & Safety App, 3월 18, 2026에 액세스, [https://safesitehq.com/](https://safesitehq.com/)  
70. Features \- Safesite, 3월 18, 2026에 액세스, [https://safesitehq.com/features/](https://safesitehq.com/features/)  
71. Best AI Workplace Safety Software for Freelancers of 2026 \- Reviews & Comparison, 3월 18, 2026에 액세스, [https://sourceforge.net/software/ai-workplace-safety/for-freelance/](https://sourceforge.net/software/ai-workplace-safety/for-freelance/)  
72. Best Matroid Alternatives & Competitors \- SourceForge, 3월 18, 2026에 액세스, [https://sourceforge.net/software/product/Matroid/alternatives](https://sourceforge.net/software/product/Matroid/alternatives)  
73. Self-Hosted AI for Construction Firms: Architecture, Costs, and Compliance in 2025, 3월 18, 2026에 액세스, [https://orderstack.xyz/self-hosted-ai-construction-firms-architecture-costs-compliance-2025/](https://orderstack.xyz/self-hosted-ai-construction-firms-architecture-costs-compliance-2025/)

[image1]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAwAAAAZCAYAAAAFbs/PAAAAy0lEQVR4Xu3RvwpBYRjH8QcpJVIGoxIXYOIGlCxWm9UgBndgk52UxWRgMYlkUCYxuBuDP9/jeV+9nTLYDOdXnzr9nvO8p3OOSJB/TRp15PwDfxKY4YAORjiJHuClIM4hcVyxQtSW5IixuV6ILr0zxQN5W5gMcEdR9Mmf/LSQwg07Wzjp4Yktarb0vohX9m3hpC06W7plxZQNtzRpic7KbhnCBUOni6CJs+hCVfT9kvaGEtaYiy5O0EXM9Hts3AWbjOg/8SeLsL8M8i0vKaAlWRE9qlQAAAAASUVORK5CYII=>

[image2]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAsAAAAYCAYAAAAs7gcTAAAApklEQVR4XmNgGAUDASyB2BZdEAj4gZgdxtEH4oNA/B+KlwAxG0wSCDYBsQiIwQnEN4B4GRAnAvFEIH4LxDlQhSZAPAvKZmgD4iIYBwrcgfg0lA0yRBcmAWeggSNArAfEu9AlsIF5DBANgegS2EA9ED8AYmY0cawgH4jL0QVxAVAIGKAL4gL3GFDDGicAhdBFdEFcIJMBEjlEgRYgNkMXxAWICi7qAQB3FRafcdhzmgAAAABJRU5ErkJggg==>