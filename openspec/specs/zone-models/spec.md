## ADDED Requirements

### Requirement: ZoneDefinition Pydantic 모델

시스템은 zone 정의를 Pydantic BaseModel로 표현해야 한다 (SHALL).
모델은 다음 필드를 포함해야 한다: zone_id (str), zone_name (str), zone_type (ZoneType enum), geometry (GeoJSONPolygon), triggering_anchor (str, 기본값 "BOTTOM_CENTER"), target_classes (list[int], 기본값 [0]), min_consecutive_frames (int, 기본값 3), cooldown_ms (int, 기본값 30000).

#### Scenario: 유효한 zone 정의 생성
- **WHEN** 모든 필수 필드가 유효한 값으로 제공될 때
- **THEN** ZoneDefinition 인스턴스가 생성된다

#### Scenario: zone_id 빈 문자열 거부
- **WHEN** zone_id가 빈 문자열 또는 공백만으로 제공될 때
- **THEN** ValidationError가 발생한다

#### Scenario: 기본값 적용
- **WHEN** triggering_anchor, target_classes, min_consecutive_frames, cooldown_ms가 생략될 때
- **THEN** 각각 "BOTTOM_CENTER", [0], 3, 30000으로 설정된다

### Requirement: ZoneType enum

시스템은 zone 유형을 문자열 enum으로 정의해야 한다 (SHALL).
허용 값: "danger", "warning", "entry".

#### Scenario: 유효한 zone_type
- **WHEN** zone_type이 "danger", "warning", "entry" 중 하나일 때
- **THEN** 모델 생성이 성공한다

#### Scenario: 잘못된 zone_type 거부
- **WHEN** zone_type이 허용 값이 아닐 때 (예: "unknown")
- **THEN** ValidationError가 발생한다

### Requirement: GeoJSON Polygon geometry

시스템은 zone geometry를 GeoJSON Polygon 포맷으로 표현해야 한다 (SHALL).
coordinates는 정규화 좌표 (0-1 범위)를 사용한다.

#### Scenario: 유효한 GeoJSON Polygon
- **WHEN** type이 "Polygon"이고 coordinates가 닫힌 고리 (첫 점 = 마지막 점)이고 모든 좌표가 0-1 범위일 때
- **THEN** GeoJSONPolygon 인스턴스가 생성된다

#### Scenario: 좌표 범위 초과 거부
- **WHEN** 좌표 값이 0 미만 또는 1 초과일 때
- **THEN** ValidationError가 발생한다

#### Scenario: 꼭짓점 부족 거부
- **WHEN** 고유 꼭짓점이 3개 미만일 때 (closing point 제외)
- **THEN** ValidationError가 발생한다

#### Scenario: closing point 자동 추가
- **WHEN** 첫 점과 마지막 점이 다를 때
- **THEN** validator가 자동으로 첫 점을 마지막에 추가하여 닫힌 고리를 만든다

### Requirement: ZoneConfig 컨테이너

시스템은 여러 ZoneDefinition을 하나의 ZoneConfig 모델로 묶어야 한다 (SHALL).

#### Scenario: 여러 zone 포함
- **WHEN** 2개 이상의 ZoneDefinition이 제공될 때
- **THEN** ZoneConfig.zones 리스트에 모두 포함된다

#### Scenario: zone_id 중복 거부
- **WHEN** 같은 zone_id를 가진 ZoneDefinition이 2개 이상 포함될 때
- **THEN** ValidationError가 발생한다

#### Scenario: 빈 zones 허용
- **WHEN** zones 리스트가 비어있을 때
- **THEN** ZoneConfig 인스턴스가 정상 생성된다

### Requirement: PolygonZone 변환

ZoneDefinition은 supervision PolygonZone 객체로 변환할 수 있어야 한다 (SHALL).
변환 시 프레임 해상도 (width, height)를 받아 정규화 좌표를 픽셀 좌표로 변환한다.

#### Scenario: 정규화 좌표 → 픽셀 좌표 변환
- **WHEN** to_polygon_zone(1920, 1080)이 호출되고 geometry 좌표가 [[0.5, 0.5], ...]일 때
- **THEN** 반환된 PolygonZone의 polygon 좌표에 (960, 540)이 포함된다

#### Scenario: triggering_anchor 반영
- **WHEN** triggering_anchor가 "CENTER"이고 to_polygon_zone()이 호출될 때
- **THEN** 반환된 PolygonZone의 triggering_anchors가 Position.CENTER이다
