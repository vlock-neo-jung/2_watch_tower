## ADDED Requirements

### Requirement: Zone 목록 표시

시스템은 현재 로드된 zone 목록을 우측 패널에 표시해야 한다 (SHALL). zone 타입별 색상으로 구분한다 (danger=빨강, warning=노랑, entry=파랑).

#### Scenario: zone 목록 렌더링
- **WHEN** zone 설정이 로드되면
- **THEN** 각 zone의 이름과 타입이 우측 패널에 표시되고 타입별 색상으로 구분된다

#### Scenario: zone 선택
- **WHEN** 패널에서 zone을 클릭하면
- **THEN** 해당 zone이 강조 표시되고 canvas의 polygon이 편집 가능 상태가 된다

### Requirement: Zone 추가

[+추가] 버튼으로 새 zone을 생성할 수 있어야 한다 (SHALL). 이름과 타입(danger/warning/entry)을 입력받는다.

#### Scenario: zone 추가 다이얼로그
- **WHEN** [+추가] 버튼을 클릭하면
- **THEN** 이름과 타입 입력 UI가 표시되고 확인 시 Drawing 상태로 진입한다

### Requirement: Zone 삭제

[-삭제] 버튼으로 선택된 zone을 삭제할 수 있어야 한다 (SHALL).

#### Scenario: zone 삭제
- **WHEN** zone을 선택하고 [-삭제] 버튼을 클릭하면
- **THEN** 해당 zone과 polygon이 제거된다
