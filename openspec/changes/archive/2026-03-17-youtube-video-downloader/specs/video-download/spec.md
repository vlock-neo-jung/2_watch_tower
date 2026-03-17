## ADDED Requirements

### Requirement: YouTube 영상 다운로드

스크립트는 YouTube URL을 받아 영상을 mp4 포맷으로 samples/에 저장해야 한다.

#### Scenario: 기본 다운로드

- **WHEN** URL과 파일명을 지정하여 스크립트를 실행하면
- **THEN** 해당 영상이 samples/{name}.mp4로 저장된다

#### Scenario: URL이 유효하지 않은 경우

- **WHEN** 잘못된 URL을 입력하면
- **THEN** 에러 메시지를 출력하고 종료한다

### Requirement: 해상도 제한

다운로드 시 영상 해상도를 제한할 수 있어야 한다.

#### Scenario: 해상도 지정

- **WHEN** `--resolution 1080` 옵션을 지정하면
- **THEN** 1080p 이하의 최적 화질로 다운로드한다

#### Scenario: 해상도 미지정

- **WHEN** 해상도 옵션을 생략하면
- **THEN** 기본값 1080p로 다운로드한다

### Requirement: 구간 추출

영상의 특정 구간만 다운로드할 수 있어야 한다.

#### Scenario: 구간 지정

- **WHEN** `--section "1:30-3:00"` 옵션을 지정하면
- **THEN** 해당 구간만 추출하여 저장한다

#### Scenario: 구간 미지정

- **WHEN** 구간 옵션을 생략하면
- **THEN** 영상 전체를 다운로드한다
