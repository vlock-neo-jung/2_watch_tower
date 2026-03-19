  학습 실행 방법

  # 한 번에 Stage 1 → Stage 2 순차 실행 (총 40~60시간)
  uv run python scripts/train_soda_person.py --stage all

  # 또는 단계별로
  uv run python scripts/train_soda_person.py --stage 1   # ~8시간
  uv run python scripts/train_soda_person.py --stage 2   # ~40시간

  학습 완료 후

  # 벤치마크 실행 (파인튜닝 모델이 자동으로 포함됨)
  uv run python scripts/benchmark_models.py \
    --gt-images /home/neo/share/watch-tower_data/dataset/soda/yolo/test/images \
    --gt-labels /home/neo/share/watch-tower_data/dataset/soda/yolo/test/labels