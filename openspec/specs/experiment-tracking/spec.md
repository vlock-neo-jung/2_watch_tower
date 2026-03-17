## ADDED Requirements

### Requirement: 실험 디렉토리 구조
실험 결과는 experiments/YYYY-MM-DD-주제/ 형식의 디렉토리에 저장해야 한다 (SHALL).

#### Scenario: 실험 디렉토리 생성
- **WHEN** 새로운 실험을 기록할 때
- **THEN** experiments/YYYY-MM-DD-주제/ 디렉토리를 생성하고 README.md와 outputs/ 를 포함해야 한다

### Requirement: 실험 기록 형식
각 실험 디렉토리에는 설정, 결과, 분석을 포함한 README.md가 있어야 한다 (SHALL).

#### Scenario: README 구조 확인
- **WHEN** 실험 디렉토리의 README.md를 확인하면
- **THEN** 실험 목적, 설정(모델/데이터/파라미터), 결과 수치, 분석/결론 섹션이 포함되어 있어야 한다

### Requirement: 실험 결과 gitignore
experiments/ 디렉토리는 git에서 추적하지 않아야 한다 (SHALL).

#### Scenario: gitignore 확인
- **WHEN** .gitignore를 확인하면
- **THEN** experiments/ 항목이 포함되어 있어야 한다
