## Why

Phase 3(위험구역 침입 + 인원 탐지)의 모든 기능이 zone 정의/판정/이벤트 로직 위에서 동작한다.
Phase 2 SODA 파인튜닝이 진행 중인 동안 이 기반 모듈을 먼저 구축하면, 이후 PoC 스크립트(Step 4), 어노테이션 도구(Step 3a), 정량 평가(Step 5)가 모두 이 모듈을 재사용할 수 있다.

## What Changes

- Zone 정의를 위한 Pydantic 데이터 모델 추가 (GeoJSON Polygon 포맷, 정규화 좌표)
- Zone 설정 YAML 파일의 로드/저장/검증 기능 추가
- 정규화 좌표 → supervision PolygonZone 변환 메서드 추가
- PolygonZone 판정 로직(anchor point, 경계선 동작)에 대한 단위 테스트 추가
- 샘플 zone 설정 YAML 파일 제공

## Capabilities

### New Capabilities

- `zone-models`: Zone 정의를 위한 Pydantic 데이터 모델 (ZoneDefinition, ZoneConfig, GeoJSONPolygon). 검증 로직 내장.
- `zone-config-io`: Zone 설정 YAML 파일의 로드/저장. DATA_ROOT 경로 패턴 준수.
- `zone-logic-validation`: supervision PolygonZone의 anchor point 판정, 경계선 동작, 좌표 변환을 검증하는 단위 테스트.

### Modified Capabilities

(없음)

## Impact

- 새 모듈: `src/watch_tower/zone/` (models.py, config.py, __init__.py)
- 새 테스트: `tests/test_zone_logic.py`, `tests/test_zone_config.py`
- 새 데이터: `DATA_ROOT/configs/zones/sample.yaml`
- 의존성 추가 없음 (pydantic, pyyaml 모두 ultralytics 경유로 이미 설치됨)
- 기존 코드 수정 없음
