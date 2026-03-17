## ADDED Requirements

### Requirement: Detection + Tracking 결과 영상 생성

스크립트는 건설 현장 영상에 Detection + ByteTrack을 적용하여, bbox + track ID + 궤적이 오버레이된 결과 영상을 생성해야 한다.

#### Scenario: 기본 실행

- **WHEN** 입력 영상 경로를 지정하여 스크립트를 실행하면
- **THEN** `model.track()`으로 Detection + ByteTrack이 실행되고, supervision으로 시각화된 결과 영상이 `outputs/tracking/`에 저장된다

#### Scenario: 결과 영상 시각화 요소

- **WHEN** 결과 영상이 생성되면
- **THEN** 각 프레임에 bbox, track ID, 클래스명, 이동 궤적이 오버레이되어 있다

### Requirement: Tracking 정성 평가 기준

결과 영상을 통해 Tracking 안정성을 정성적으로 평가할 수 있어야 한다.

#### Scenario: ID 유지 확인

- **WHEN** 사람이 직선으로 이동할 때
- **THEN** 동일 track ID가 유지된다

#### Scenario: 가림 후 복귀

- **WHEN** 사람이 1-2초 가려졌다 다시 나타날 때
- **THEN** 동일 track ID로 복귀한다

#### Scenario: 교차 시 ID 스왑

- **WHEN** 두 사람이 교차할 때
- **THEN** ID 스왑이 영상당 1-2회 이하로 발생한다

### Requirement: Detection 실패 케이스 파악

P2-1의 Recall 79.5% 경계선 결과를 보완하여, 어떤 상황에서 사람을 놓치는지 패턴을 파악해야 한다.

#### Scenario: 실패 케이스 기록

- **WHEN** 결과 영상에서 감지되지 않은 사람이 관찰되면
- **THEN** 실패 조건(거리, 가림, 조명, 포즈 등)을 실험 기록에 정리한다
