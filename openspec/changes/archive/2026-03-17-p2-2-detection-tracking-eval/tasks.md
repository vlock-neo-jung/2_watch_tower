## 1. 추적 스크립트 작성

- [x] 1.1 `scripts/run_tracking.py` 생성 — `model.track()` + ByteTrack 실행
- [x] 1.2 supervision 시각화 연동 (BoxAnnotator, LabelAnnotator, TraceAnnotator)
- [x] 1.3 결과 영상을 `outputs/tracking/`에 저장

## 2. 영상별 실행

- [x] 2.1 construction_helmets.mp4 실행 — Person 3~6명 지속 감지
- [x] 2.2 construction_subway_cctv.mp4 실행 — Person 거의 미감지 (평가 부적합)
- [x] 2.3 construction_tower_crane_cctv.mp4 실행 — Person 0~4명 간헐적 감지

## 3. 정성 평가 및 기록

- [x] 3.1 영상별 Detection 실패 케이스 정리 — 높은 각도(조감 시점)에서 Person 감지 실패 확인
- [x] 3.2 Tracking 안정성 확인 — helmets 영상에서만 가능, 높은 각도 영상은 Detection 미작동으로 평가 불가
- [x] 3.3 Go/No-Go 정성 판단 — No-Go (Detection 근본 문제: 학습 데이터 vs 배포 환경 시점 불일치)
