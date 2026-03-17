## Context

이전 벤치마크(Grounding DINO 정답, 26장)의 한계를 극복하기 위해 SODA 데이터셋을 도입한다. 건설현장 특화 + 사람 라벨링 + 대량 데이터로 신뢰할 수 있는 정량 비교가 가능해진다.

### SODA 데이터셋 스펙

- 이미지: 19,846장 (train 17,861 / test 1,985)
- 어노테이션: 286,201개 (VOC XML 포맷)
- 해상도: 1920x1080 (86%)
- 15개 클래스: person, helmet, vest, wood, board, rebar, brick, scaffold, hook, fence, cutter, handcart, hopper, ebox, slogan
- 다운로드: https://scut-scet-academic.oss-cn-guangzhou.aliyuncs.com/SODA/2022.2/VOCv1.zip
- 라이센스: 학술 연구용 (BIM-LAB, SCUT)

## Goals / Non-Goals

**Goals:**
- SODA 다운로드 및 VOC → YOLO 변환
- Person 클래스만 추출하여 벤치마크용 데이터셋 구성
- test set (1,985장)으로 hazard/COCO/VisDrone 정량 비교
- 기존 benchmark_models.py 재사용 (경로만 변경)

**Non-Goals:**
- 전체 15개 클래스 변환 (Person만)
- 파인튜닝 (이번 change에서는 벤치마크만)
- train set 활용 (벤치마크는 test set만)

## Decisions

### 1. VOC → YOLO 변환

VOC XML의 `<object><name>person</name><bndbox>` 태그에서 bbox를 추출하여 YOLO 포맷(class x_center y_center w h)으로 변환. Person 클래스만 추출하고 나머지는 무시.

### 2. test set만 사용 (1,985장)

벤치마크 목적이므로 test set만 변환. train set은 향후 파인튜닝 시 별도 변환.

### 3. 기존 benchmark_models.py 확장

기존 스크립트의 GT 경로를 파라미터로 받도록 수정하여 SODA test set에 대해서도 실행 가능하게 한다.

## Risks / Trade-offs

- **다운로드 용량**: VOCv1.zip 크기 불확실 (수 GB 추정). 디스크 확인 필요
- **Person 클래스 수**: test 1,985장 중 Person 어노테이션이 몇 개인지 변환 후 확인
- **val split 없음**: SODA는 train/test만 제공. 벤치마크에는 test만 쓰면 충분
