## ADDED Requirements

### Requirement: GT 파일 목록

시스템은 DATA_ROOT/zone_gt/ 디렉토리의 JSON 파일 목록을 반환해야 한다 (SHALL).

#### Scenario: GT 파일 목록 반환
- **WHEN** GET /api/annotations/ 요청 시
- **THEN** .json 파일명 리스트가 JSON 배열로 반환된다

### Requirement: GT 로드

시스템은 GT JSON 파일을 로드하여 반환해야 한다 (SHALL).

#### Scenario: GT 로드
- **WHEN** GET /api/annotations/{annotation_name} 요청 시
- **THEN** GT JSON 내용이 반환된다

### Requirement: GT 저장

시스템은 GT JSON을 파일로 저장해야 한다 (SHALL).

#### Scenario: GT 저장
- **WHEN** POST /api/annotations/{annotation_name}에 GT JSON body가 전달될 때
- **THEN** JSON 파일이 생성/덮어쓰기되고 성공 응답이 반환된다
