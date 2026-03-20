## ADDED Requirements

### Requirement: 영상 파일 목록 조회

시스템은 DATA_ROOT/samples/ 디렉토리의 영상 파일(.mp4) 목록을 반환해야 한다 (SHALL).

#### Scenario: 영상 파일 목록 반환
- **WHEN** GET /api/videos/ 요청 시
- **THEN** .mp4 파일명 리스트가 JSON 배열로 반환된다

### Requirement: 영상 파일 서빙

시스템은 FileResponse로 영상 파일을 서빙해야 한다 (SHALL). Range Request를 지원하여 영상 seek이 가능해야 한다.

#### Scenario: 영상 파일 스트리밍
- **WHEN** GET /api/videos/{filename} 요청 시
- **THEN** 해당 영상 파일이 FileResponse로 반환되고 Range Request 헤더가 지원된다

#### Scenario: 존재하지 않는 영상
- **WHEN** GET /api/videos/{filename}에서 파일이 존재하지 않을 때
- **THEN** 404 응답이 반환된다

### Requirement: 영상 메타데이터 조회

시스템은 영상의 fps, width, height, duration, total_frames를 반환해야 한다 (SHALL).

#### Scenario: 메타데이터 반환
- **WHEN** GET /api/videos/{filename}/info 요청 시
- **THEN** { fps, width, height, duration, total_frames } JSON이 반환된다
