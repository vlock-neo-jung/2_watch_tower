## ADDED Requirements

### Requirement: drawImage 기반 영상 렌더링

시스템은 hidden `<video>` 요소의 프레임을 drawImage()로 canvas에 렌더링해야 한다 (SHALL).

#### Scenario: 영상 로드 후 첫 프레임 표시
- **WHEN** 영상을 선택하면
- **THEN** 첫 프레임이 video-canvas에 표시된다

#### Scenario: canvas 비율 유지
- **WHEN** 영상이 로드되면
- **THEN** canvas의 가로/세로 비율이 영상 원본 비율과 동일하게 설정된다

### Requirement: 재생 제어

시스템은 재생/일시정지, 프레임 단위 이동, 5초 점프, 시간 슬라이더를 제공해야 한다 (SHALL).

#### Scenario: 프레임 단위 이동
- **WHEN** [▶] 버튼 또는 → 키를 누르면
- **THEN** 영상이 1프레임 앞으로 이동하고 canvas가 갱신된다

#### Scenario: 시간 슬라이더 seek
- **WHEN** 슬라이더를 드래그하면
- **THEN** 해당 시점으로 이동하고 canvas가 갱신된다

### Requirement: 재생 속도 조절

시스템은 0.5x, 1x, 2x, 4x 재생 속도를 버튼으로 제공해야 한다 (SHALL).

#### Scenario: 속도 변경
- **WHEN** [2x] 버튼을 클릭하면
- **THEN** video.playbackRate가 2.0으로 설정되고 영상이 2배속으로 재생된다
