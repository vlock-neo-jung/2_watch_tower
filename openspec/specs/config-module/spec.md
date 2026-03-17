## ADDED Requirements

### Requirement: 중앙 경로 설정 모듈
src/watch_tower/config.py가 DATA_ROOT 환경변수 기반으로 모든 데이터 경로를 제공해야 한다 (SHALL).

#### Scenario: 환경변수 설정 시
- **WHEN** WATCH_TOWER_DATA_ROOT=/custom/path 환경변수가 설정되어 있으면
- **THEN** config.DATA_ROOT는 Path("/custom/path")이어야 한다

#### Scenario: 환경변수 미설정 시
- **WHEN** WATCH_TOWER_DATA_ROOT 환경변수가 없으면
- **THEN** config.DATA_ROOT는 Path("/home/neo/share/watch-tower_data")이어야 한다

#### Scenario: 하위 경로 제공
- **WHEN** config 모듈을 임포트하면
- **THEN** SAMPLES_DIR, MODELS_DIR, OUTPUTS_DIR, DATASET_DIR, EXPERIMENTS_DIR가 DATA_ROOT의 하위 경로로 정의되어야 한다
