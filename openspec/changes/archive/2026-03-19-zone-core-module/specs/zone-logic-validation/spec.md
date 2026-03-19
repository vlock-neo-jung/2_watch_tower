## ADDED Requirements

### Requirement: BOTTOM_CENTER anchor 판정 검증

supervision PolygonZone의 BOTTOM_CENTER anchor 판정이 기대대로 동작하는지 단위 테스트로 검증해야 한다 (SHALL).

#### Scenario: zone 내부 중앙의 사람
- **WHEN** bbox의 foot point (하단 중앙)가 polygon zone 한가운데에 있을 때
- **THEN** trigger() 결과가 True이다

#### Scenario: zone 완전 외부의 사람
- **WHEN** bbox의 foot point가 polygon zone 완전히 밖에 있을 때
- **THEN** trigger() 결과가 False이다

#### Scenario: 상반신은 zone 안, 발은 밖
- **WHEN** bbox 상단이 zone 내부이지만 foot point는 zone 밖에 있을 때
- **THEN** BOTTOM_CENTER 기준 trigger() 결과가 False이다

#### Scenario: 상반신은 밖, 발만 zone 안
- **WHEN** bbox 대부분이 zone 밖이지만 foot point만 zone 안에 있을 때
- **THEN** BOTTOM_CENTER 기준 trigger() 결과가 True이다

### Requirement: anchor point별 판정 차이 검증

BOTTOM_CENTER와 CENTER anchor의 판정 차이를 단위 테스트로 확인해야 한다 (SHALL).

#### Scenario: 동일 bbox에 대한 anchor별 결과 차이
- **WHEN** bbox의 CENTER는 zone 안이지만 BOTTOM_CENTER는 zone 밖인 경우
- **THEN** CENTER anchor는 True, BOTTOM_CENTER anchor는 False를 반환한다

### Requirement: 경계선 동작 검증

polygon 경계선 위와 근처의 판정 동작을 단위 테스트로 파악해야 한다 (SHALL).

#### Scenario: 경계선 바로 안쪽
- **WHEN** foot point가 polygon 경계에서 1px 안쪽에 있을 때
- **THEN** trigger() 결과가 True이다

#### Scenario: 경계선 바로 바깥
- **WHEN** foot point가 polygon 경계에서 1px 바깥에 있을 때
- **THEN** trigger() 결과가 False이다

### Requirement: 다중 감지 및 엣지 케이스

여러 명의 감지와 빈 감지 등 엣지 케이스를 검증해야 한다 (SHALL).

#### Scenario: 여러 사람 중 일부만 zone 안
- **WHEN** 3명의 bbox가 제공되고 1명만 zone 안에 있을 때
- **THEN** trigger() 결과가 [False, True, False] 형태의 배열이다

#### Scenario: 빈 감지
- **WHEN** detections가 비어있을 때
- **THEN** trigger() 결과가 빈 배열이다

#### Scenario: 오목 polygon
- **WHEN** L자형 오목 polygon이 정의되고 foot point가 오목부 내부에 있을 때
- **THEN** trigger() 결과가 True이다

### Requirement: 정규화 좌표 → 픽셀 좌표 변환 정확성

ZoneDefinition.to_polygon_zone()의 좌표 변환이 정확한지 검증해야 한다 (SHALL).

#### Scenario: 1920x1080 해상도 변환
- **WHEN** 정규화 좌표 [0.5, 0.5]를 1920x1080 해상도로 변환할 때
- **THEN** 픽셀 좌표 (960, 540)이 된다

#### Scenario: 다른 해상도에서도 정확한 변환
- **WHEN** 동일한 정규화 좌표를 3840x2160 해상도로 변환할 때
- **THEN** 비례에 맞는 픽셀 좌표 (1920, 1080)이 된다
