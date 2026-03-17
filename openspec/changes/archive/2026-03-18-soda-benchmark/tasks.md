## 1. 데이터셋 확보

- [x] 1.1 SODA 데이터셋 확보 — 기존 다운로드분 발견, DATASET_DIR/soda/로 이동
- [x] 1.2 디렉토리 구조 확인 — VOCdevkit/VOC2007/ (19,847 annotations, 19,846 images, test 1,985장)

## 2. VOC → YOLO 변환

- [x] 2.1 VOC→YOLO 변환 스크립트 작성 (`scripts/convert_soda_to_yolo.py`)
- [x] 2.2 test set 변환 — 1,984장, Person 포함 1,468장, Person 어노테이션 7,399개

## 3. 벤치마크

- [x] 3.1 benchmark_models.py에 --gt-images, --gt-labels 파라미터 추가
- [x] 3.2 SODA test set 벤치마크 실행 완료
- [x] 3.3 결과: COCO 최고(Recall 36.7%, F1 50.9%), hazard 유사(35.7%, 50.3%), VisDrone 최악(7.9%). 소규모 벤치마크와 동일 결론 확정.
