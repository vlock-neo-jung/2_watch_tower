## ADDED Requirements

### Requirement: 샘플 데이터 디렉토리
프로젝트는 수동 관리 파일(PoC 영상, 테스트 이미지)을 위한 data/samples/ 디렉토리를 가져야 한다 (SHALL).

#### Scenario: 디렉토리 존재 확인
- **WHEN** 프로젝트 루트에서 data/samples/ 를 확인하면
- **THEN** 디렉토리가 존재해야 한다

### Requirement: ultralytics 데이터셋 경로 설정
ultralytics의 datasets_dir이 /home/neo/toy-project/workspace_watch-tower/dataset/ 으로 설정되어야 한다 (SHALL).

#### Scenario: 데이터셋 경로 확인
- **WHEN** ultralytics settings에서 datasets_dir을 확인하면
- **THEN** /home/neo/toy-project/workspace_watch-tower/dataset/ 이어야 한다

### Requirement: .gitignore에 데이터 제외
data/ 디렉토리는 git에서 추적하지 않아야 한다 (SHALL).

#### Scenario: gitignore 확인
- **WHEN** .gitignore를 확인하면
- **THEN** data/ 항목이 포함되어 있어야 한다
