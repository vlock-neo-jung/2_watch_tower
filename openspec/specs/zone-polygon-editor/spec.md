## ADDED Requirements

### Requirement: Polygon 그리기 (Drawing 상태)

사용자가 canvas 위에서 마우스 클릭으로 꼭짓점을 배치하고 polygon을 생성할 수 있어야 한다 (SHALL).

#### Scenario: 꼭짓점 배치
- **WHEN** Drawing 상태에서 canvas를 클릭하면
- **THEN** 해당 위치에 꼭짓점이 추가되고 이전 꼭짓점과 선으로 연결된다

#### Scenario: 마우스 미리보기
- **WHEN** Drawing 상태에서 마우스를 이동하면
- **THEN** 마지막 꼭짓점에서 마우스 위치까지 점선 미리보기가 표시된다

#### Scenario: Polygon 닫기
- **WHEN** Drawing 상태에서 우클릭하면
- **THEN** polygon이 닫히고 반투명 색상으로 채워지며 Editing 상태로 전환된다

#### Scenario: 그리기 취소
- **WHEN** Drawing 상태에서 Esc를 누르면
- **THEN** 현재 그리기가 취소되고 찍은 꼭짓점이 모두 삭제되며 Idle 상태로 복귀한다

### Requirement: Polygon 편집 (Editing 상태)

완성된 polygon의 꼭짓점을 드래그하여 이동하고, polygon 전체를 이동할 수 있어야 한다 (SHALL).

#### Scenario: 꼭짓점 드래그
- **WHEN** Editing 상태에서 꼭짓점 핸들을 드래그하면
- **THEN** 해당 꼭짓점이 마우스 위치로 이동하고 polygon 형태가 실시간 갱신된다

#### Scenario: 전체 이동
- **WHEN** Editing 상태에서 polygon 내부를 드래그하면
- **THEN** polygon 전체가 마우스 이동량만큼 이동한다

### Requirement: 상태 머신

Zone 편집 모드는 Idle, Drawing, Editing 세 가지 상태를 가져야 한다 (SHALL).

#### Scenario: Idle → Drawing 전환
- **WHEN** [+추가] 버튼으로 zone을 추가하고 확인하면
- **THEN** Drawing 상태로 진입한다

#### Scenario: Editing → Idle 전환
- **WHEN** zone 선택을 해제하면 (다른 zone 클릭 또는 빈 영역 클릭)
- **THEN** Idle 상태로 복귀한다

#### Scenario: 기존 zone 재편집
- **WHEN** 우측 패널에서 기존 zone을 클릭하면
- **THEN** 해당 polygon이 Editing 상태로 전환되고 꼭짓점 핸들이 표시된다

### Requirement: 좌표 정규화

polygon 좌표는 저장 시 0-1 정규화 좌표로 변환되어야 한다 (SHALL).

#### Scenario: 저장 시 좌표 변환
- **WHEN** polygon 좌표를 저장할 때
- **THEN** canvas 픽셀 좌표가 canvas 크기로 나누어져 0-1 범위의 정규화 좌표로 변환된다

#### Scenario: 로드 시 좌표 변환
- **WHEN** 저장된 zone 설정을 로드할 때
- **THEN** 0-1 정규화 좌표가 현재 canvas 크기에 맞게 픽셀 좌표로 변환된다
