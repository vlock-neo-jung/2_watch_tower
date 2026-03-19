# Step 1: Zone Logic 단위 테스트

## 이 단계가 왜 필요한가

"사람이 위험구역 안에 있는가?"는 결국 **"특정 좌표가 다각형(polygon) 안에 있는가?"** 라는 기하학 문제다.
단순해 보이지만, 실제로는 몇 가지 결정에 따라 결과가 크게 달라진다:

### 판정점(anchor point) 선택 문제

사람을 감지하면 사각형 박스(bounding box)를 얻는다. 이 박스의 **어느 점**을 기준으로 "안에 있다"를 판단할 것인가?

```
   ┌──────────┐
   │          │  ← TOP_CENTER
   │  사람    │  ← CENTER (중앙)
   │          │
   │          │
   └────●─────┘  ← BOTTOM_CENTER (발 위치)
```

- **BOTTOM_CENTER (하단 중앙)**: 사람의 발 위치를 근사한다. 업계 표준.
  - 장점: 사람이 실제로 "서 있는" 위치를 가장 잘 반영
  - 예: 사람 상반신이 zone 위로 넘어와도, 발이 밖이면 침입 아님
- **CENTER (중앙)**: 박스의 정중앙
  - 문제: 사람이 zone 경계에 서 있을 때 상반신이 안에 들어오면 침입으로 판정 → 오탐
- **전체 박스 겹침**: 박스와 zone이 일정 비율 이상 겹치면 침입
  - 문제: 계산 복잡, 임계값 설정이 추가로 필요

**결론**: BOTTOM_CENTER를 기본으로 사용하되, 다른 anchor와의 차이를 테스트로 확인해둔다.

### 경계선(boundary) 문제

사람이 위험구역 경계선 바로 위에 서 있으면 어떻게 되는가?
프레임마다 감지 박스가 미세하게 흔들리면서 "안 → 밖 → 안 → 밖"을 반복할 수 있다.
이게 매 프레임 알림으로 이어지면 쓸모없는 시스템이 된다.

이 문제는 Step 4의 temporal logic(연속 N프레임 판정)으로 해결하지만,
zone logic 자체가 경계선에서 어떻게 동작하는지 먼저 이해해야 한다.

## 구체적으로 무엇을 테스트하는가

### 영상이나 모델은 필요 없다

이 테스트는 **순수한 좌표 계산 검증**이다.
카메라도, 영상도, AI 모델도 쓰지 않는다.
코드로 "가짜 사각형 박스"를 만들고, "가짜 다각형 영역"을 만든 다음,
PolygonZone 함수에 넣어서 예상한 답이 나오는지 확인하는 것이다.

### 테스트 파일: `tests/test_zone_logic.py`

supervision 라이브러리의 `PolygonZone` API를 사용한다 (이미 설치됨).

```python
import numpy as np
import supervision as sv
from supervision.geometry.core import Position

# 가짜 zone: (20,20)~(80,80) 사각형. 화면 위의 좌표일 뿐, 실제 카메라와 무관.
polygon = np.array([[20, 20], [80, 20], [80, 80], [20, 80]])
zone = sv.PolygonZone(
    polygon=polygon,
    triggering_anchors=[Position.BOTTOM_CENTER]
)

# 가짜 사람 bbox: 실제 감지 결과가 아니라, 직접 만든 좌표.
# xyxy 형식 = [x1, y1, x2, y2] = 박스의 좌상단(x1,y1), 우하단(x2,y2)
detections = sv.Detections(
    xyxy=np.array([[30, 30, 50, 70]])
)
# foot point(하단 중앙) = ((30+50)/2, 70) = (40, 70) → zone(20~80) 안 → True

is_inside = zone.trigger(detections)
assert is_inside[0] == True  # 통과하면 이 로직이 올바르게 동작하는 것
```

### 테스트 케이스 목록

아래 모든 케이스는 위처럼 **직접 만든 좌표**를 사용한다. 영상 없음.

| # | 시나리오 | 입력 | 기대 결과 | 검증 목적 |
|---|---------|------|----------|----------|
| 1 | zone 중앙의 사람 | foot point가 zone 한가운데 | True | 기본 동작 |
| 2 | zone 완전 외부 | foot point가 zone 밖 | False | 기본 동작 |
| 3 | 몸은 안, 발은 밖 | bbox 상단이 zone 내, foot은 밖 | BOTTOM_CENTER=False, CENTER=True | anchor 차이 |
| 4 | 몸은 밖, 발은 안 | bbox 대부분 밖, foot만 안 | BOTTOM_CENTER=True | anchor가 발 기준임을 확인 |
| 5 | 경계선 위 | foot point가 정확히 polygon 변 위 | 결과 기록 | 경계 동작 파악 |
| 6 | 경계선 바로 안쪽 | foot이 경계에서 1px 안쪽 | True | 경계 민감도 |
| 7 | 경계선 바로 바깥 | foot이 경계에서 1px 바깥 | False | 경계 민감도 |
| 8 | 오목 polygon | L자형 zone | 오목부 안의 점 = True | 비정형 zone |
| 9 | 감지 없음 | 빈 detections | 빈 배열 | 엣지 케이스 |
| 10 | 여러 사람 | 3명 중 1명만 안 | [False, True, False] | 다중 감지 |

### 정규화 좌표 변환 테스트

zone 설정은 0~1 범위의 정규화 좌표로 저장한다 (해상도가 바뀌어도 유효하도록).
실제 사용 시 이미지 해상도에 맞게 픽셀 좌표로 변환해야 한다.

```python
# 정규화 좌표 (0-1)
normalized = [[0.2, 0.3], [0.8, 0.3], [0.8, 0.9], [0.2, 0.9]]

# 1920x1080 해상도로 변환
pixel_coords = [[int(x*1920), int(y*1080)] for x, y in normalized]
# → [[384, 324], [1536, 324], [1536, 972], [384, 972]]
```

이 변환의 정확성도 테스트한다.

## 완료 기준

- [ ] 모든 테스트 케이스 통과: `uv run pytest tests/test_zone_logic.py -v`
- [ ] BOTTOM_CENTER vs CENTER 차이가 구체적 수치로 문서화됨
- [ ] 경계선 동작이 파악됨 (polygon 변 위의 점이 True인지 False인지)

## 이 단계의 산출물

- `tests/test_zone_logic.py` — 단위 테스트 코드
- anchor 선택에 따른 동작 차이 기록 (테스트 결과에 포함)
