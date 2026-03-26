# Watch Tower 문서 목차

## roadmap/ — 마일스톤, 로드맵

- [00-setup.md](roadmap/00-setup.md) — 1차 로드맵 (개발환경 → 모델검증 → 통합)

## product/ — 제품 오버뷰, 핵심 도메인 규칙

- [overview.md](product/overview.md) — 프로젝트 개요 및 요구사항 정의서

## references/ — 아키텍처, 인프라, 셋업, API 등 개발자 참고 문서

- [architecture.md](references/architecture.md) — 시스템 아키텍처
- [getting-started.md](references/getting-started.md) — 설치 및 실행 가이드
- [dev-environment.md](references/dev-environment.md) — 개발 환경 설정 및 검증 결과
- [pc-speck.md](references/pc-speck.md) — 개발 머신 하드웨어 스펙
- [detection-metrics.md](references/detection-metrics.md) — Object Detection 평가 수치 가이드
- [models-and-datasets.md](references/models-and-datasets.md) — 모델 및 데이터셋 현황

## research/ — 기술 비교, 라이브러리 평가, 설계 대안 분석

- [ppe-detection.md](research/ppe-detection.md) — PPE 감지 리서치
- [ppe-detection-technical.md](research/ppe-detection-technical.md) — PPE 감지 기술 상세
- [pretrained-models.md](research/pretrained-models.md) — 사전학습 모델 비교
- [fall-detection.md](research/fall-detection.md) — 쓰러짐 감지 리서치
- [danger-zone-intrusion-research.md](research/danger-zone-intrusion-research.md) — 위험구역 침입 감지 리서치
- [edge-device-jetson.md](research/edge-device-jetson.md) — Jetson 엣지 디바이스 조사
- [realtime-pipeline.md](research/realtime-pipeline.md) — 실시간 파이프라인 설계
- [video-streaming-framework.md](research/video-streaming-framework.md) — 영상 스트리밍 프레임워크 비교
- [comparison-recommendation.md](research/comparison-recommendation.md) — 상용 솔루션 비교 및 Build vs Buy
- [research_01.md](research/research_01.md) — 리서치 노트 1
- [research_02.md](research/research_02.md) — 리서치 노트 2

## report/ — 검증 리포트

- [00.phase2-person-detection-tracking.md](report/00.phase2-person-detection-tracking.md) — Phase 2 종합: Person Detection + Tracking 검증 결과
- [01.small-object-detection-improvements.md](report/01.small-object-detection-improvements.md) — 소형 객체 탐지 개선 시도: SAHI, 고해상도, VisDrone 모델
- [02.soda-benchmark-results.md](report/02.soda-benchmark-results.md) — SODA 대규모 벤치마크: 1,984장/7,399명 기준 모델 비교 확정
- [03.sahi-coco-benchmark.md](report/03.sahi-coco-benchmark.md) — SAHI + COCO 조합: Recall 36.7%→57.8% (+21%p)
- [04.soda-finetune-benchmark.md](report/04.soda-finetune-benchmark.md) — SODA 파인튜닝: SODA 도메인 Recall 84.1%, 건설현장 도메인 한계 확인
- [05.visual-model-comparison.md](report/05.visual-model-comparison.md) — 모델별 영상 육안 비교: hazard가 건설현장에서 최선, SODA-ft 부적합 확인
- [06.ppe-detection.md](report/06.ppe-detection.md) — PPE 감지 검증 및 Zone×PPE 결합 로직: NO-Hardhat 탐지 한계 확인, 이중 판정 방식 프로토타입 구현
