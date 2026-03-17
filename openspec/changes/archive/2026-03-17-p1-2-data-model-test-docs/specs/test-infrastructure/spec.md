## ADDED Requirements

### Requirement: pytest 실행 가능
`uv run pytest`로 테스트를 실행할 수 있어야 한다 (SHALL).

#### Scenario: pytest 실행
- **WHEN** `uv run pytest`를 실행하면
- **THEN** 테스트가 수집되고 실행되어야 한다

### Requirement: 패키지 임포트 테스트
watch_tower 패키지 및 핵심 의존성의 임포트를 검증하는 smoke test가 존재해야 한다 (SHALL).

#### Scenario: 임포트 테스트 통과
- **WHEN** `uv run pytest tests/test_smoke.py`를 실행하면
- **THEN** watch_tower, ultralytics, supervision 임포트 테스트가 통과해야 한다
