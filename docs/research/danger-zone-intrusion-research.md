# 위험구역 침입 감지 기술 조사
**작성일:** 2026-03-12 | **목적:** Watch Tower의 위험구역 침입/출입통제 기능 설계를 위한 참고 문서

---

## 1. 핵심 결론

위험구역 침입 감지는 보통 새로운 대형 모델을 학습해서 푸는 문제가 아니다. 실무에서는 `사람/차량 검출 + 객체 추적 + 구역 규칙 엔진` 조합으로 구현한다. 즉, 모델은 `person`, `vehicle` 같은 공통 객체를 안정적으로 찾고, 실제 위험 판단은 카메라별 구역 설정과 운영 규칙이 담당한다.

건설현장 특성상 중요한 것은 모델보다 설정 가능성이다. 현장은 공정 진행에 따라 위험구역이 자주 바뀌므로, 상용 솔루션들은 공통적으로 `polygon ROI`, `virtual line`, `체류시간`, `활성 시간대`, `객체 크기 필터`, `알림 연계`, `변경 로그`를 제공한다.

따라서 Watch Tower도 위험구역 기능을 만들 때 `새로운 CV 모델`보다 `Zone Rule Engine`과 `운영 UI`를 우선 설계하는 편이 현실적이다.

---

## 2. 구현 원리

### 2.1 기본 파이프라인

위험구역 침입 감지의 기본 흐름은 다음과 같다.

1. 카메라별 위험구역을 화면 위에 다각형 또는 선으로 정의한다.
2. 모델이 프레임에서 `person`, `vehicle` 등을 검출한다.
3. Tracker가 동일 객체를 `track_id`로 유지한다.
4. 객체의 판정점이 zone 안에 들어왔는지 계산한다.
5. `N프레임 연속`, `T초 이상 체류` 같은 조건을 만족하면 이벤트를 생성한다.
6. 이벤트 발생 시 스냅샷, 전후 영상 클립, 대시보드 알림, 외부 알림을 발송한다.

### 2.2 판정 방식

실무에서 많이 쓰는 판정 방식은 아래와 같다.

| 방식 | 설명 | 장점 | 주의점 |
|------|------|------|--------|
| `bottom-center in polygon` | bbox 하단 중앙점이 polygon 안에 들어오면 침입으로 판정 | 가장 단순하고 오탐이 적음 | 카메라 각도에 따라 보정 필요 |
| bbox overlap ratio | bbox와 zone의 겹침 비율이 임계값 이상이면 침입 | 객체가 큰 경우 안정적 | 경계선 근처 오탐 가능 |
| virtual line crossing | 가상선을 특정 방향으로 넘으면 이벤트 발생 | 출입구, 통로, 펜스 경계에 적합 | 체류 상황은 표현이 약함 |
| dwell time | zone 안에 일정 시간 이상 머무르면 이벤트 발생 | 경계선 스치기 오탐 감소 | 빠른 침입은 놓칠 수 있음 |

실무에서는 이 중 하나만 쓰기보다 `polygon + dwell time`, `line crossing + 방향`, `danger zone + warning zone` 조합으로 운영하는 경우가 많다.

### 2.3 왜 tracking이 중요한가

추적이 없으면 프레임 단위로 같은 사람을 계속 새 객체로 보게 된다. 그러면 경계선 근처에서 오탐이 많아지고, 동일 인물에 대한 중복 경보도 늘어난다. 따라서 위험구역 감지는 객체 검출만으로 끝나지 않고, `track_id 기반 상태 누적`이 필수에 가깝다.

---

## 3. 실제 솔루션들의 설정 방식

공개 자료 기준으로 상용 솔루션들은 거의 비슷한 설정 모델을 사용한다.

### 3.1 구역 직접 그리기

가장 일반적인 방식은 사용자가 카메라 화면 위에 직접 구역을 그리는 방식이다.

- polygon ROI를 마우스로 그림
- zone 이름 지정
- 사람/차량 등 감시 대상 선택
- 구역별 활성 시간 설정
- 위반 시 알림 채널 선택

`viAct`는 사용자가 custom area를 직접 정의하고, 한 시야각 안에 여러 danger zone을 둘 수 있다고 설명한다. 또한 프로젝트 요구에 따라 zone별 활성 시간을 다르게 둘 수 있고, zone 수정 로그를 남긴다고 공개한다.

### 3.2 가상선 기반 설정

일반 지능형 CCTV 업계에서는 line crossing detection이 매우 흔하다. `Hikvision` 계열 설정 가이드는 다음 항목을 제공한다.

- `Draw Area`
- `Direction`
- `Time Threshold`
- `Sensitivity`
- `Min/Max Size`
- `Arming Schedule`
- `Linkage Method`

이 구조는 위험구역 침입 감지의 업계 표준 UI에 가깝다.

### 3.3 체류시간과 스케줄

현장에서는 사람이 경계선을 잠깐 스치는 경우가 많다. 이 때문에 많은 솔루션이 즉시 알림 대신 `체류시간(Time Threshold)` 또는 `N프레임 연속 감지`를 둔다. 또한 건설현장은 공정 시간대가 다르므로 `Arming Schedule`이나 `zone activation time`도 기본 기능으로 제공하는 경우가 많다.

### 3.4 동적 위험구역

건설현장 특화 솔루션은 일반 CCTV보다 한 단계 더 나간다.

- 여러 zone을 한 카메라에 동시에 설정
- 매일 바뀌는 공정에 따라 zone을 자주 수정
- 누가 zone을 바꿨는지 로그 저장
- 울타리나 개구부 기반 자동 danger zone 보조 탐지

`viAct`는 danger zone의 일별 변경과 zone modification log를 강조하며, 일부 페이지에서는 holes, fencing 기반의 dynamic AI auto-detection도 언급한다.

### 3.5 출입통제와의 차이

침입 감지와 출입통제는 비슷해 보이지만 다르다.

- 침입 감지: 구역에 들어왔는지 판단
- 출입통제: 들어온 사람이 허가된 사람인지 판단

후자는 얼굴 인식, 카드/QR, 교육 이수, 작업 허가, 근태 시스템, 게이트 장비 연동까지 필요하다. 공개 자료에서 `viAct`는 training, permit, facial recognition, zone mapping과의 결합을 설명하고, 국내 보안 업계는 얼굴인식 리더와 출입통제 시스템을 별도 제품군으로 운영한다. 따라서 초기 제품에서는 `위험구역 침입 감지`와 `물리 출입통제`를 분리하는 편이 현실적이다.

---

## 4. 건설현장 운영 관점에서 중요한 설정값

위험구역 기능을 실사용하려면 최소 아래 설정이 필요하다.

| 항목 | 설명 |
|------|------|
| `camera_id` | 어느 카메라 설정인지 식별 |
| `zone_id`, `zone_name` | 구역 식별자와 운영용 이름 |
| `zone_type` | `danger`, `warning`, `entry`, `exit` 등 |
| `geometry` | polygon 좌표 또는 line 좌표 |
| `target_class` | `person`, `vehicle`, `all` |
| `direction` | `in`, `out`, `both` |
| `min_dwell_ms` | 체류시간 임계값 |
| `cooldown_ms` | 같은 객체 반복 알림 억제 시간 |
| `min_size`, `max_size` | 원거리 소형 오탐 필터용 |
| `active_schedule` | 요일/시간대별 활성 정책 |
| `required_ppe` | 특정 zone에 필수 PPE 연결 |
| `alert_channels` | dashboard, siren, SMS, webhook 등 |
| `revision_log` | 누가 언제 구역을 수정했는지 기록 |

건설현장에서는 특히 `active_schedule`, `required_ppe`, `revision_log`가 중요하다. 위험구역 자체가 공정에 따라 바뀌기 때문이다.

---

## 5. Watch Tower에 적용하는 방식

현재 시스템 아키텍처 문서는 이미 `검출 → 추적 → 규칙 → 이벤트` 구조를 전제하고 있다.

- `YOLO11m` 기반 검출
- `ByteTrack` 기반 추적
- `PPE Rule Engine`
- `Event Generator`

이 구조에 위험구역 기능을 추가할 때는 별도 대형 모델보다 `Zone Rule Engine`을 붙이는 방식이 가장 자연스럽다.

### 5.1 권장 최소 구조

1. `person` 검출
2. `ByteTrack`으로 `track_id` 유지
3. 카메라별 polygon/line zone 적용
4. `bottom-center in polygon` 또는 `line crossing` 계산
5. `N프레임 연속` 또는 `min_dwell_ms` 만족 시 이벤트 생성
6. 이벤트에 zone 정보, track 정보, 스냅샷, 클립 저장

### 5.2 권장 이벤트 정책

- `warning zone`: 즉시 경고가 아니라 주의 알림
- `danger zone`: 짧은 체류만으로 경고
- `entry gate`: line crossing 방향 기반 이벤트
- `high-risk zone`: 필수 PPE 규칙과 결합

예를 들어 `크레인 회전 반경`은 `danger zone`, `장비 접근 외곽`은 `warning zone`, `전기실 입구`는 `entry gate`로 나눌 수 있다.

### 5.3 구현 우선순위

Watch Tower 기준 우선순위는 아래가 적절하다.

1. polygon ROI 기반 `person intrusion`
2. dwell time, cooldown, schedule 추가
3. zone별 required PPE 연결
4. line crossing과 vehicle-human proximity 확장
5. 외부 출입통제 시스템 연동 검토

초기 범위에서 `허가자/비허가자 식별`까지 바로 넣는 것은 권장하지 않는다. 그 단계부터는 CV보다 권한 시스템 통합 난도가 더 커진다.

---

## 6. 설계 시 주의사항

### 6.1 오탐을 줄이는 방법

- bbox 전체가 아닌 `bottom-center` 기준으로 판정
- 경계선 바로 위에 `cooldown` 적용
- 너무 작은 bbox는 무시
- 카메라별 원근 왜곡을 고려해 zone을 실제보다 약간 안쪽으로 설정
- 즉시 경보 대신 `N프레임 연속` 또는 `체류시간` 사용

### 6.2 현장 운영 리스크

- 공정 변경으로 zone이 자주 바뀜
- 야간 조명, 비, 먼지, 역광으로 검출 품질 변동
- 카메라 재설치 시 zone 재설정 필요
- 장비와 작업자가 겹치면 추적 품질 저하 가능

따라서 위험구역 기능의 품질은 모델 성능만이 아니라 `설정 UI`, `수정 이력`, `현장 튜닝 프로세스`에 크게 좌우된다.

---

## 7. 권장 결론

위험구역 침입 기능은 Watch Tower가 비교적 빠르게 구현할 수 있는 영역이다. 이유는 복잡한 신규 학습보다 검출, 추적, zone rule, 이벤트 정책 조합이 핵심이기 때문이다. 반면 출입통제는 물리 장비와 권한 시스템 통합이 필요하므로 초기 직접 개발 범위로 잡기에는 부담이 크다.

따라서 1차 목표는 `위험구역 침입 감지`이고, 2차 목표는 `zone별 PPE 규칙`, 3차 목표는 `외부 출입통제 연동`으로 잡는 것이 현실적이다.

---

## 8. 참고 자료

### 외부 공개 자료

1. [viAct Area Control Safety System](https://www.viact.ai/solutions/area-control-safety-system)
2. [viAct Danger Zone Alert](https://www.viact.ai/dangerzonedetection)
3. [SAIGE SAFETY 건설 현장 솔루션 소개](https://saige.ai/usecase/construction/)
4. [Hikvision Line Crossing / Intrusion Detection 설정 가이드 요약](https://ness.zendesk.com/hc/en-us/articles/360040077994-Setting-Line-Crossing-and-Intrusion-Detection-in-Hikvision-IPC)

### 내부 문서

1. `docs/system-architecture.md`
2. `docs/overview.md`
