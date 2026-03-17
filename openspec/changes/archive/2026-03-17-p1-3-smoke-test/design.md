## Context

FWY-43(프로젝트 초기화), FWY-44(관리 체계)가 완료된 상태. data/samples/에 7개 샘플 파일이 준비되어 있다. 이제 프로젝트 모델로 실제 추론을 실행하여 전체 인프라가 동작하는지 확인한다.

## Goals / Non-Goals

**Goals:**
- download_models.py → 모델 로드 → GPU 추론 → 결과 저장의 end-to-end 흐름 검증
- 건설 현장 영상에서 Person/PPE 감지 결과를 시각적으로 확인

**Non-Goals:**
- detection 모듈 래퍼 구현 (Phase 2에서 필요할 때 생성)
- mAP 등 정량 평가 (Phase 2 P2-1에서 수행)
- Tracking (Phase 2 P2-2에서 수행)

## Decisions

### 1. 단순 스크립트 방식 (방식 A)
- scripts/run_inference.py에서 ultralytics YOLO를 직접 호출
- src/watch_tower/detection/ 래퍼는 만들지 않음
- 이유: Smoke Test는 인프라 검증이 목적. 래퍼는 현 시점에서 YOLO.predict() 감싸기뿐이라 부가가치 없음. Phase 2에서 tracking/zone 로직이 필요해질 때 모듈화

### 2. 입출력 구조
- 입력: data/samples/ 내 영상/이미지 (경로 인자로 지정)
- 출력: outputs/ 디렉토리에 bbox 오버레이 결과 저장
- 콘솔: 감지 객체 수, 클래스별 분포, 추론 속도 요약

## Risks / Trade-offs

- **[모델 다운로드 실패]** → HuggingFace 서버 의존. 네트워크 오류 시 재시도 또는 수동 다운로드.
- **[PoC 대비 결과 차이]** → PoC는 MacBook CPU, 지금은 RTX 3080 Ti GPU. 속도는 빨라지지만 감지 결과는 동일 모델이므로 유사해야 함.
