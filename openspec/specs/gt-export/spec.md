## ADDED Requirements

### Requirement: GT JSON 자체 완결 포맷

GT JSON은 zone geometry 스냅샷과 영상 메타데이터를 내장하여 자체 완결적이어야 한다 (SHALL).

#### Scenario: GT 저장
- **WHEN** [저장] 버튼을 클릭하면
- **THEN** GT JSON이 다음을 포함한다: video (파일명), video_fps, video_width, video_height, total_frames, zones (geometry 스냅샷 포함), events (zone_id, start_frame, end_frame)

#### Scenario: zone 설정 변경 후 기존 GT 유지
- **WHEN** GT 생성 후 zone 설정 YAML을 수정하더라도
- **THEN** 기존 GT JSON의 zone geometry는 생성 시점의 값을 유지한다
