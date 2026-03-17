## MODIFIED Requirements

### Requirement: 실험 디렉토리 구조
실험 결과는 config.EXPERIMENTS_DIR/YYYY-MM-DD-주제/ 형식의 디렉토리에 저장해야 한다 (SHALL).

#### Scenario: 실험 디렉토리 경로
- **WHEN** config.EXPERIMENTS_DIR을 확인하면
- **THEN** DATA_ROOT/experiments/ 이어야 한다

## REMOVED Requirements

### Requirement: 실험 결과 gitignore
**Reason**: 실험 디렉토리가 프로젝트 밖으로 이동하여 gitignore 불필요
**Migration**: experiments/ 관련 gitignore 규칙 제거, experiments/README.md git rm, 내용은 config 모듈 docstring에 보존
