# 모델 및 데이터셋 현황

**작성일:** 2026-03-20
**경로:** 모든 데이터는 `config.DATA_ROOT` (`/home/neo/share/watch-tower_data/`) 하위에 위치

## 모델

경로: `config.MODELS_DIR` (`DATA_ROOT/models/`)

| 모델 파일 | 크기 | 아키텍처 | 출처 | 클래스 | 용도 |
|-----------|------|----------|------|--------|------|
| `yolo11m.pt` | 39MB | YOLOv11m | [Ultralytics COCO pretrained](https://docs.ultralytics.com/models/yolo11/) (자동 다운로드) | COCO 80클래스 (person 포함) | Person Detection baseline, SODA-ft 학습 base 모델 |
| `yolo11m-construction-hazard.pt` | 39MB | YOLOv11m | [yihong1120/Construction-Hazard-Detection](https://huggingface.co/yihong1120/Construction-Hazard-Detection) (HuggingFace) | Hardhat, Mask, NO-Hardhat, NO-Mask, NO-Safety Vest, Person, Safety Cone, Safety Vest, machinery, utility pole, vehicle (11클래스) | PPE 감지, Person Detection |
| `yolo11m-soda-person.pt` | 116MB | YOLOv11m | COCO pretrained → SODA train set 파인튜닝 (자체 학습) | person (1클래스) | 고각 CCTV Person Detection 특화 |
| `yolov8m-visdrone.pt` | 50MB | YOLOv8m | VisDrone 사전학습 모델 | pedestrian, people 등 (드론 항공뷰) | 드론/항공 시점 객체 탐지 (벤치마크 비교용) |

> **참고:** `yolo11m.pt`는 Ultralytics가 자동 다운로드하여 프로젝트 루트에 위치. 나머지 모델은 `MODELS_DIR`에 위치.

### yolo11m-soda-person.pt 학습 이력

- **FWY-61**: SODA train set으로 COCO 모델 파인튜닝
- **학습 전략**: 2단계 (Stage 1: backbone freeze 50ep → Stage 2: 전체 200ep, early stop 162ep)
- **학습 설정**: imgsz=1280, batch=4, cos_lr, patience=50
- **학습 결과**: mAP50 ~92.3%, mAP50-95 ~52.4% (SODA val set 기준)
- **실험 디렉토리**: `DATA_ROOT/experiments/soda-finetune/stage2/`
- **학습 스크립트**: `scripts/train_soda_person.py`

## 데이터셋

경로: `config.DATASET_DIR` (`DATA_ROOT/dataset/`)

| 데이터셋 | 이미지 수 | 어노테이션 수 | 포맷 | 클래스 | 설명 |
|----------|----------|--------------|------|--------|------|
| `soda/yolo/train` | 17,859장 (13,011장에 Person) | 63,447 Person bbox | YOLO | person (1클래스) | SODA 학술 데이터셋. 도로/거리 고각 감시카메라. 해상도 1920x1080 균일. 파인튜닝 학습에 사용 |
| `soda/yolo/test` | 1,984장 (1,468장에 Person) | 7,399 Person bbox | YOLO | person (1클래스) | SODA test split. 학습에 미사용. 모델 성능 평가용 |
| `soda/VOCdevkit` | (위와 동일) | (위와 동일) | VOC XML | person | SODA 원본 (VOC 포맷). `convert_soda_to_yolo.py`로 YOLO 변환 |
| `construction-ppe` | 1,416장 (train 1,132 / val 143 / test 141) | 다수 (11클래스) | YOLO | helmet, gloves, vest, boots, goggles, none, Person, no_helmet, no_goggle, no_gloves, no_boots | [Ultralytics Construction-PPE](https://docs.ultralytics.com/datasets/detect/construction-ppe/). 건설현장 PPE 착용 감지 |
| `construction-ppe-remapped` | 1,416장 | (위와 동일, 클래스 리매핑) | YOLO | construction-hazard 모델 클래스에 매핑 (Hardhat, Person, Safety Vest 등 11클래스) | `remap_construction_ppe.py`로 변환. hazard 모델 평가용 |
| `construction-ppe-val` | 12장 | 소량 | YOLO | (위와 동일) | PPE 검증용 소규모 샘플 |

### Ground Truth (자체 구축)

경로: `DATA_ROOT/ground_truth/`

| 항목 | 값 |
|------|-----|
| 이미지 수 | 26장 |
| 어노테이션 | 96 Person bbox |
| 포맷 | YOLO (labels/) + metadata.json |
| 출처 | 실제 건설현장 CCTV 영상에서 프레임 추출 (4개 소스) |
| 해상도 | 586x480 ~ 1280x720 (혼합) |
| 용도 | 실제 타겟 도메인 성능 평가. 모델 벤치마크 기본 GT |

영상 소스별 구성:

| 소스 | 프레임 수 | 특징 |
|------|----------|------|
| `construction_helmets` | 4장 | 근거리 헬멧캠 |
| `construction_site_cctv` | 6장 | 건설현장 고정 CCTV |
| `construction_subway_cctv` | 8장 | 지하철 공사현장 CCTV |
| `construction_tower_crane_cctv` | 8장 | 타워크레인 상부 CCTV (고각) |

