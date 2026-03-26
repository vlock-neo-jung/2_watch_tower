# Watch Tower

건설 현장 실시간 AI 안전 모니터링 시스템.
카메라 영상을 AI로 분석하여 보호구 미착용, 작업자 쓰러짐, 위험구역 침입, 구역 내 인원 수를 자동 감지하고 즉각 알림을 발송한다.

## 문서 (Documentation)

- **전체 목차**: `docs/index.md`
- **목차 갱신 규칙**: 구현을 완료하거나 커밋 전에 수정사항을 문서에 반영할 것. 대상 references

### 1. 프로젝트 뼈대 (docs/)
- `docs/index.md` — 문서 전체 구조 안내 및 진입점. (drafts 등 임시 문서 제외)
- `docs/roadmap/` — 프로젝트 전체 마일스톤 및 주요 로드맵. OpenSpec 작업들의 상위 목표 및 진행 계획을 파악할 때 확인.
- `docs/product/` — 제품 오버뷰, 핵심 요구사항, 주요 비즈니스 규칙. 프로젝트의 '왜(Why)'와 '무엇(What)'을 파악할 때 확인.
- `docs/references/` — 아키텍처, 인프라, 셋업, API, 평가 지표 등 개발자 참고 문서. '어떻게(How)'를 확인.
- `docs/research/` — 기술 비교, 라이브러리 평가, 설계 대안 분석 등 조사 자료.
- `docs/report/` — Person Detection 벤치마크 시리즈. 모델 비교 → SAHI → SODA 파인튜닝까지 순차 검증 기록.

### 2. 설계 및 구현 스펙 (openspec/)
프로젝트의 세부 기능 기획과 개발 작업 내역은 OpenSpec을 통해 관리됩니다.
- `openspec/specs/` — 모듈별 구현 스펙. 프로젝트 현황이나 세부 설계 의도 파악 시 여기를 **가장 먼저** 참조할 것.
- `openspec/changes/` — 현재 진행 중인 기능 단위의 작업 공간 (proposal → design → tasks).
- `openspec/changes/archive/` — 완료된 작업 내역 및 과거 히스토리.

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
