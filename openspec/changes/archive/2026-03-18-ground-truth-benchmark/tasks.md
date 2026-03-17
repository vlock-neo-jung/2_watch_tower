## 1. 환경 준비

- [x] 1.1 Grounding DINO 의존성 설치 (transformers via HuggingFace)
- [x] 1.2 ground_truth/images/, ground_truth/labels/ 디렉토리 생성

## 2. 프레임 추출

- [x] 2.1 프레임 추출 스크립트 작성 (`scripts/extract_frames.py`)
- [x] 2.2 4개 영상에서 26장 추출 완료

## 3. 정답 생성

- [x] 3.1 Grounding DINO 정답 생성 스크립트 작성 (`scripts/generate_ground_truth.py`)
- [x] 3.2 26장에서 96명 Person bbox 생성 완료
- [x] 3.3 생성된 정답 수동 검증 — 대부분 정확, 일부 그림자 오탐 (수용 가능)

## 4. 벤치마크

- [x] 4.1 모델별 비교 스크립트 작성 (`scripts/benchmark_models.py`)
- [x] 4.2 hazard, COCO, VisDrone 3개 모델 벤치마크 실행 완료
- [x] 4.3 결과 기록 및 분석 — COCO 최고(Recall 43.8%), VisDrone 오탐 다수, 이전 판단 뒤집힘
