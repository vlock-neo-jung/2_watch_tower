# Step 2: Zone 설정 스키마 정의

## 이 단계가 왜 필요한가

위험구역은 **코드에 하드코딩하는 것이 아니라 설정 파일로 관리**해야 한다.
이유는 건설 현장의 특성에 있다:

- 공정이 바뀌면 위험구역도 바뀐다 (크레인 이동, 굴착 위치 변경 등)
- 카메라마다 다른 위험구역을 가진다
- 같은 카메라에 여러 위험구역이 있을 수 있다 (크레인 반경 = danger, 외곽 = warning)
- 구역마다 규칙이 다르다 (체류시간, 활성 시간대, 알림 방식)

따라서 **설정 파일 하나로 모든 zone 정보를 관리**하는 구조가 필요하다.
이 단계에서는 그 파일의 형식(스키마)을 확정하고, 로드/검증하는 코드를 만든다.

## Zone 설정이 담아야 하는 정보

기존 리서치(`docs/research/danger-zone-intrusion-research.md`)에서 정리한 필수 설정값을 기반으로 한다.
현재는 검증 단계이므로 최소한의 필수 항목만 포함한다.

### 설정 항목 설명

| 항목 | 의미 | 예시 | 왜 필요한가 |
|------|------|------|-----------|
| `zone_id` | 구역 고유 식별자 | `"crane_area"` | 이벤트 로그에서 어느 구역인지 식별 |
| `zone_name` | 구역 표시 이름 | `"크레인 작업 반경"` | 사람이 읽는 용도 (알림, 리포트) |
| `zone_type` | 구역 유형 | `danger` / `warning` | 유형에 따라 알림 긴급도가 다름 |
| `geometry` | 다각형 꼭짓점 좌표 | `[[0.2, 0.3], ...]` | zone의 실제 경계 정의 |
| `triggering_anchor` | 판정 기준점 | `BOTTOM_CENTER` | Step 1에서 검증한 anchor 설정 |
| `target_classes` | 감시 대상 | `[0]` (person) | 사람만 볼지, 차량도 볼지 |
| `min_consecutive_frames` | 최소 연속 프레임 | `3` | 오탐 필터링 (깜빡임 방지) |
| `cooldown_ms` | 재알림 방지 시간 | `30000` (30초) | 같은 사람에 대한 반복 알림 억제 |

### YAML 파일 형식

```yaml
# DATA_ROOT/configs/zones/sample.yaml
#
# 좌표는 0~1 범위의 정규화 좌표 (이미지 해상도에 독립적)
# [0,0]은 좌상단, [1,1]은 우하단

zones:
  - zone_id: "crane_area"
    zone_name: "크레인 작업 반경"
    zone_type: danger
    geometry:
      - [0.10, 0.25]
      - [0.55, 0.20]
      - [0.60, 0.85]
      - [0.15, 0.90]
    triggering_anchor: BOTTOM_CENTER
    target_classes: [0]               # 0 = person (COCO)
    min_consecutive_frames: 3
    cooldown_ms: 30000

  - zone_id: "excavation_warning"
    zone_name: "굴착 주의 구역"
    zone_type: warning
    geometry:
      - [0.60, 0.30]
      - [0.95, 0.30]
      - [0.95, 0.80]
      - [0.60, 0.80]
    triggering_anchor: BOTTOM_CENTER
    target_classes: [0]
    min_consecutive_frames: 5
    cooldown_ms: 60000
```

### 왜 정규화 좌표(0~1)를 사용하는가

카메라 해상도가 바뀔 수 있다 (1080p → 4K, 또는 프레임 리사이즈).
좌표를 픽셀 단위로 저장하면 해상도가 바뀔 때마다 전부 다시 설정해야 한다.
정규화 좌표는 비율로 저장하므로 해상도와 무관하게 동작한다.

## 구현 내용

### 파일 구조

```
src/watch_tower/zone/
├── __init__.py
└── config.py                             ← zone 설정 로드 및 검증
tests/
└── test_zone_config.py

DATA_ROOT/configs/zones/
└── sample.yaml                           ← 테스트용 샘플 설정
```

참고: zone 설정은 카메라/현장별로 달라지는 운영 데이터이므로 프로젝트 코드가 아닌
`DATA_ROOT` (`/home/neo/share/watch-tower_data/`) 아래에 저장한다.

### `config.py`가 하는 일

1. YAML 파일 읽기
2. 필수 필드 존재 여부 검증
3. 좌표 범위 검증 (0~1)
4. polygon 꼭짓점 수 검증 (최소 3개)
5. 정규화 좌표 → 픽셀 좌표 변환 함수
6. supervision `PolygonZone` 객체 생성

### 테스트 케이스

| # | 시나리오 | 기대 결과 |
|---|---------|----------|
| 1 | 정상 YAML 로드 | zone 목록 반환 |
| 2 | 필수 필드 누락 | 에러 + 누락 필드명 안내 |
| 3 | 좌표 범위 초과 (1.5 등) | 에러 |
| 4 | 꼭짓점 2개 이하 | 에러 (최소 3개 필요) |
| 5 | 정규화→픽셀 변환 | 1920x1080 기준 정확한 변환 |
| 6 | PolygonZone 객체 생성 | supervision zone 객체 반환 |

## 완료 기준

- [ ] `DATA_ROOT/configs/zones/sample.yaml` 작성
- [ ] `src/watch_tower/zone/config.py` 구현
- [ ] `uv run pytest tests/test_zone_config.py -v` 통과
- [ ] 샘플 YAML → PolygonZone 객체 생성까지 동작 확인

## 이 단계의 산출물

- `src/watch_tower/zone/config.py` — 설정 로드/검증 코드
- `DATA_ROOT/configs/zones/sample.yaml` — 샘플 설정 파일
- `tests/test_zone_config.py` — 설정 관련 테스트
