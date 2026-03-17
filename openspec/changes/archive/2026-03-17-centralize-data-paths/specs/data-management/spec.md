## MODIFIED Requirements

### Requirement: 샘플 데이터 디렉토리
프로젝트는 수동 관리 파일(PoC 영상, 테스트 이미지)을 DATA_ROOT/samples/ 디렉토리에서 관리해야 한다 (SHALL).

#### Scenario: 디렉토리 존재 확인
- **WHEN** config.SAMPLES_DIR 경로를 확인하면
- **THEN** /home/neo/share/watch-tower_data/samples/ 이어야 한다

### Requirement: ultralytics 데이터셋 경로 설정
ultralytics의 datasets_dir이 config.DATASET_DIR으로 설정되어야 한다 (SHALL).

#### Scenario: 데이터셋 경로 확인
- **WHEN** ultralytics settings에서 datasets_dir을 확인하면
- **THEN** config.DATASET_DIR 값과 일치해야 한다

## REMOVED Requirements

### Requirement: .gitignore에 데이터 제외
**Reason**: 데이터 디렉토리가 프로젝트 밖으로 이동하여 gitignore 불필요
**Migration**: data/ 관련 gitignore 규칙 제거, data/samples/.gitkeep git rm
