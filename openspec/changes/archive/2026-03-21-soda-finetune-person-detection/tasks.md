## 1. 데이터 준비

- [x] 1.1 SODA train set VOC→YOLO 변환 — 17,859장, Person 13,011장, 63,447 어노테이션
- [x] 1.2 YOLO 학습 yaml 작성 (`dataset/soda/yolo/soda-person.yaml`)

## 2. 파인튜닝 실행

- [x] 2.1 Stage 1: 헤드만 학습 (freeze=10, epochs=50, imgsz=1280, batch=4)
- [x] 2.2 Stage 2: 전체 학습 (Stage 1 가중치, lr0=0.001, epochs=200 → early stop epoch 162)
- [x] 2.3 최종 가중치를 models/yolo11m-soda-person.pt로 복사

## 3. 벤치마크

- [x] 3.1 파인튜닝 모델 단독 벤치마크 (SODA test set) — Recall 84.1%, F1 85.1%
- [x] 3.2 파인튜닝 모델 + SAHI 벤치마크 — SAHI + SODA-ft Recall 90.2%, F1 85.3%
- [x] 3.3 결과 비교 테이블 작성 및 Go/No-Go 판단 — `docs/report/04.soda-finetune-benchmark.md`
