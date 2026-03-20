# Watch Tower

건설 현장 실시간 AI 안전 모니터링 시스템.
카메라 영상을 AI로 분석하여 보호구 미착용, 작업자 쓰러짐, 위험구역 침입, 구역 내 인원 수를 자동 감지하고 즉각 알림을 발송한다.

## 문서

전체 목차: [docs/index.md](docs/index.md)

- `concepts/` — 요구사항 정의서, 1차 로드맵
- `research/` — PPE·쓰러짐·위험구역 감지, 엣지 디바이스, 스트리밍, 상용 솔루션 비교
- `references/` — 개발환경, HW 스펙, 평가 지표 해설, **모델·데이터셋 현황 테이블** (`models-and-datasets.md`)
- `report/` — Person Detection 벤치마크 시리즈. 모델 비교 → SAHI → SODA 파인튜닝까지 순차 검증 기록. 각 리포트에 실험 설정, 결과 테이블, 분석, Go/No-Go 판단 포함

새 문서 생성 시 `docs/index.md`에 링크를 추가할 것.

## 데이터 경로

대용량 데이터는 프로젝트 외부에 위치. `src/watch_tower/config.py`에서 관리.
환경변수 `WATCH_TOWER_DATA_ROOT`로 변경 가능 (기본값: `/home/neo/share/watch-tower_data`).

```
DATA_ROOT/
├── models/        # YOLO 가중치 — COCO, construction-hazard, SODA-ft, VisDrone
├── dataset/       # SODA(19K장), Construction-PPE(1.4K장) 등
├── ground_truth/  # 자체 구축 건설현장 GT (26장/96 bbox)
├── samples/       # PoC 영상, 테스트 이미지
├── outputs/       # 추론 결과
└── experiments/   # 학습 로그, 벤치마크 결과
```

상세 모델·데이터셋 목록: [docs/references/models-and-datasets.md](docs/references/models-and-datasets.md)

## Linear

- Team: FWY
- Project: WatchTower (`watchtower-f6ee3203fb62`)

@AGENTS.md
