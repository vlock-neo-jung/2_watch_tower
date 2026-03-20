## ADDED Requirements

### Requirement: Zone 설정 파일 목록

시스템은 DATA_ROOT/configs/zones/ 디렉토리의 YAML 파일 목록을 반환해야 한다 (SHALL).

#### Scenario: 설정 파일 목록 반환
- **WHEN** GET /api/zones/ 요청 시
- **THEN** .yaml 파일명 리스트가 JSON 배열로 반환된다

### Requirement: Zone 설정 로드

시스템은 watch_tower.zone.load_zone_config()를 사용하여 YAML 파일을 로드하고 ZoneConfig JSON을 반환해야 한다 (SHALL).

#### Scenario: 설정 로드
- **WHEN** GET /api/zones/{config_name} 요청 시
- **THEN** ZoneConfig가 JSON으로 반환된다

### Requirement: Zone 설정 저장

시스템은 watch_tower.zone.save_zone_config()를 사용하여 ZoneConfig JSON을 YAML 파일로 저장해야 한다 (SHALL).

#### Scenario: 설정 저장
- **WHEN** POST /api/zones/{config_name}에 ZoneConfig JSON body가 전달될 때
- **THEN** YAML 파일이 생성/덮어쓰기되고 성공 응답이 반환된다
