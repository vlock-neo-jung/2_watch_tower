## ADDED Requirements

### Requirement: Zone 설정 YAML 로드

시스템은 YAML 파일에서 zone 설정을 로드하여 ZoneConfig 객체를 반환해야 한다 (SHALL).

#### Scenario: 유효한 YAML 파일 로드
- **WHEN** 유효한 zone 설정 YAML 파일 경로가 제공될 때
- **THEN** ZoneConfig 객체가 반환되고 모든 zone 정의가 포함된다

#### Scenario: 파일 미존재 시 에러
- **WHEN** 존재하지 않는 파일 경로가 제공될 때
- **THEN** FileNotFoundError가 발생한다

#### Scenario: 잘못된 YAML 구조 시 에러
- **WHEN** YAML 파일의 구조가 ZoneConfig 스키마와 맞지 않을 때
- **THEN** ValidationError가 발생하고 어떤 필드가 잘못되었는지 메시지에 포함된다

### Requirement: Zone 설정 YAML 저장

시스템은 ZoneConfig 객체를 YAML 파일로 저장할 수 있어야 한다 (SHALL).

#### Scenario: 정상 저장
- **WHEN** ZoneConfig 객체와 출력 파일 경로가 제공될 때
- **THEN** YAML 파일이 생성되고 내용이 다시 로드 시 동일한 ZoneConfig를 반환한다

#### Scenario: 디렉토리 자동 생성
- **WHEN** 출력 경로의 부모 디렉토리가 존재하지 않을 때
- **THEN** 부모 디렉토리가 자동으로 생성된다

### Requirement: 샘플 zone 설정 파일

DATA_ROOT/configs/zones/sample.yaml에 테스트용 샘플 zone 설정 파일을 제공해야 한다 (SHALL).
최소 2개의 zone 정의 (danger 타입 1개, warning 타입 1개)를 포함한다.

#### Scenario: 샘플 파일 로드 가능
- **WHEN** sample.yaml을 load_zone_config()로 로드할 때
- **THEN** ZoneConfig 객체가 정상 반환되고 2개 이상의 zone이 포함된다
