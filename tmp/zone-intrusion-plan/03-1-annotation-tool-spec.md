# Zone 설정 + GT 어노테이션 도구 사양

## 도구 개요

하나의 도구가 두 가지 역할을 수행한다:

| 역할 | 목적 | 출력 |
|------|------|------|
| **Zone 편집 모드** | 카메라 화면에 위험구역 polygon을 그리고 저장 | zone 설정 YAML |
| **어노테이션 모드** | 영상을 재생하며 침입 이벤트 구간을 기록 | GT JSON (정답지) |

두 모드의 공통 핵심 인터랙션은 "영상 위에 polygon을 그리고 편집한다"이며,
어노테이션 모드는 여기에 "시간축 이벤트 마킹"이 추가된다.

---

## 기술 스택

| 레이어 | 선택 | 이유 |
|--------|------|------|
| **Backend** | FastAPI | 프로젝트 기존 계획과 일치. Python 생태계. Phase 5 대시보드 API로 확장 |
| **Frontend** | React (Vite + TypeScript) | 컴포넌트 기반으로 대시보드 확장 용이. Vite로 빌드 |
| **Canvas** | Fabric.js | polygon 생성/편집/드래그를 내장 지원. 직접 구현 대비 공수 대폭 절감 |
| **영상 렌더링** | drawImage 2-Canvas 스택 | `<video>` 요소를 디코딩 소스로만 사용. Canvas에 프레임을 직접 그림 |

### 영상 렌더링 아키텍처

`<video>` 요소를 화면에 표시하지 않고, `drawImage()`로 canvas에 직접 프레임을 그린다.
Fabric.js canvas를 그 위에 겹쳐서 polygon 편집을 처리한다.

```
┌─────────────────────────────────────────────┐
│ <div style="position: relative">            │
│                                             │
│   <canvas id="video-canvas">                │
│     ctx.drawImage(video, 0, 0, w, h)        │
│     requestAnimationFrame(render)            │
│                                             │
│   <canvas id="fabric-canvas">  (겹침)       │
│     Fabric.js (투명 배경)                    │
│     polygon 그리기/편집                      │
│                                             │
│   <video> (hidden, muted)                   │
│     디코딩 소스 전용, 화면 미표시             │
│                                             │
└─────────────────────────────────────────────┘
```

장점:
- 크기 동기화 문제 소멸 (하나의 div 안에 같은 크기로 겹침)
- 좌표계 통일 (canvas 크기 = 표시 크기)
- 프레임 캡처 용이 (스냅샷 export 가능)

### Canvas 비율

canvas를 항상 영상의 **원본 비율에 맞춘다**. 영상 메타데이터(`/api/videos/{filename}/info`)에서
width/height를 받아서 canvas 비율을 설정한다. 비율이 맞으면 좌표 변환이 단순 곱셈/나눗셈으로 유지된다.

```
브라우저 레이아웃:
┌──────────────────────────────────────┬────────┐
│                                      │        │
│     canvas (영상 비율에 맞춤)          │  Zone  │
│     width = 컨테이너 너비             │  패널  │
│     height = width × (vH/vW)         │        │
│                                      │        │
└──────────────────────────────────────┴────────┘
```

### 좌표 변환

3개의 좌표 공간이 존재한다:

```
① 정규화 좌표 (0-1)       ② 영상 원본 픽셀           ③ Canvas 표시 픽셀
   저장/API에서 사용          영상 해상도                브라우저에 실제 표시

   [0.5, 0.5]        →    [960, 540]          →    [480, 270]
                          (1920×1080)               (960×540 표시)
```

| 동작 | 변환 | 계산 |
|------|------|------|
| YAML 로드 → 화면 표시 | ① → ③ | x × canvas.width, y × canvas.height |
| 사용자가 polygon 그림 → 저장 | ③ → ① | x / canvas.width, y / canvas.height |
| to_polygon_zone() (추론용) | ① → ② | x × 영상원본width, y × 영상원본height |

영상 원본 해상도(②)는 도구 UI에서는 불필요하고, 추론 시에만 사용된다.

### 아키텍처

```
Windows 브라우저 (Chrome)
  ├── React (Vite dev server :5173)
  │   ├── video-canvas    — drawImage()로 영상 프레임 렌더링
  │   ├── fabric-canvas   — Fabric.js polygon 편집 (투명 오버레이)
  │   └── UI 컴포넌트     — zone 패널, 이벤트 목록, 타임라인
  │
  │   API 요청 (Vite proxy → :8000)
  │
WSL2 FastAPI 서버 (:8000)
  ├── 영상 파일 서빙 (FileResponse, Range Request 자동 지원)
  ├── 영상 메타데이터 (fps, width, height, duration, total_frames)
  ├── Zone 설정 CRUD (YAML 읽기/쓰기)
  └── GT 이벤트 CRUD (JSON 읽기/쓰기)
```

### 디렉토리 구조

```
2_watch_tower/
├── src/watch_tower/                # Python 패키지 (기존, 핵심 로직)
│   ├── config.py                   #   DATA_ROOT 경로 관리 (기존)
│   ├── detection/                  #   (기존)
│   ├── utils/                      #   (기존)
│   └── zone/                       #   Zone 핵심 로직 (구현 완료)
│       ├── __init__.py
│       ├── models.py               #     Pydantic 모델 (ZoneDefinition, ZoneConfig 등)
│       ├── config.py               #     zone 설정 YAML 로드/저장
│       └── tracker.py              #     ZoneTracker (이벤트 판정, Step 4)
│
├── api/                            #   FastAPI (패키지 밖, 앱 레이어)
│   ├── __init__.py
│   ├── app.py                      #     FastAPI 앱 진입점
│   ├── routes/
│   │   ├── videos.py               #     영상 파일 서빙 + 메타데이터
│   │   ├── zones.py                #     zone 설정 CRUD
│   │   └── annotations.py          #     GT 이벤트 CRUD
│   └── schemas.py                  #     Pydantic 모델 (API 전용)
│
├── frontend/                       #   React (Vite)
│   ├── package.json
│   ├── vite.config.ts
│   └── src/
│       ├── components/
│       │   ├── VideoPlayer/        #     drawImage 기반 영상 렌더링 + 프레임 제어
│       │   ├── ZoneEditor/         #     Fabric.js polygon 편집
│       │   ├── ZonePanel/          #     우측 zone 목록
│       │   └── EventTimeline/      #     하단 이벤트 마킹/타임라인
│       ├── api/                    #     FastAPI 호출 클라이언트
│       ├── hooks/
│       ├── types/
│       └── styles/
│
├── scripts/                        # 기존 CLI 스크립트
├── tests/
├── docs/
└── pyproject.toml
```

**데이터는 기존 DATA_ROOT 패턴 유지**:

```
/home/neo/share/watch-tower_data/   # DATA_ROOT (기존)
├── samples/                        #   (기존) 샘플 영상
├── models/                         #   (기존) 모델 가중치
├── outputs/                        #   (기존) 추론 결과
├── experiments/                    #   (기존) 실험 리포트
├── configs/                        #   운영 설정
│   └── zones/
│       └── sample.yaml             #     zone 설정 파일
└── zone_gt/                        #   GT 데이터
    └── test_zone_01.json           #     이벤트 정답지
```

### 설계 근거

| 결정 | 이유 |
|------|------|
| drawImage 2-Canvas 스택 | `<video>` 오버레이 대비 크기 동기화/좌표 통일 문제 해결 |
| `api/`를 `src/watch_tower/` 밖에 배치 | `watch_tower` 패키지는 핵심 로직만 포함. Jetson 배포 시 FastAPI 의존성 불필요 |
| `zone/`은 `src/watch_tower/` 안에 유지 | zone 로직은 스크립트, API, 파이프라인 모두 사용하는 핵심 도메인 로직 |
| 데이터를 프로젝트 밖 DATA_ROOT에 저장 | 기존 데이터 관리 패턴 준수. 대용량 파일은 git에 넣지 않음 |
| FastAPI를 optional dependency로 분리 | `uv pip install -e ".[api]"` — 추론 전용 환경에서는 설치하지 않음 |

### 미래 Phase 호환성

| Phase | 영향 |
|-------|------|
| Phase 4 (PPE) | `src/watch_tower/detection/`에 PPE 모듈 추가. 충돌 없음 |
| Phase 5 (파이프라인) | `api/`에 WebSocket, 카메라 관리 라우트 추가. 자연스럽게 확장 |
| Phase 5 (대시보드) | `frontend/`에 LiveGrid, EventLog 추가. ZoneEditor 컴포넌트 재사용 |
| Jetson 배포 | `src/watch_tower/`만 배포. `api/`, `frontend/` 불필요 |

---

## API 엔드포인트

### 영상

```
GET  /api/videos/                → 영상 파일 목록 (DATA_ROOT/samples/ 내 .mp4 파일)
GET  /api/videos/{filename}      → 영상 파일 서빙 (FileResponse, Range Request 자동)
GET  /api/videos/{filename}/info → 메타데이터 { fps, width, height, duration, total_frames }
```

영상 선택은 서버 파일 브라우저 방식 — DATA_ROOT/samples/ 목록을 API로 반환한다.
대용량 영상 업로드 불필요.

### Zone 설정

```
GET  /api/zones/                 → 저장된 zone 설정 파일 목록
GET  /api/zones/{config_name}    → 특정 설정 로드 (ZoneConfig JSON)
POST /api/zones/{config_name}    → 설정 저장 (ZoneConfig JSON → YAML)
```

기존 `watch_tower.zone` 모듈의 `load_zone_config` / `save_zone_config`를 그대로 호출.
Pydantic 모델이 API 스키마와 동일하므로 변환 코드 불필요.

### GT 어노테이션

```
GET  /api/annotations/                    → GT 파일 목록
GET  /api/annotations/{annotation_name}   → GT 로드
POST /api/annotations/{annotation_name}   → GT 저장
```

---

## 화면 구성

```
┌─────────────────────────────────────────────────────────────────┐
│  [모드: Zone 편집 ▼]  [영상: construction_cctv.mp4 ▼]          │
├─────────────────────────────────────────────────────────┬───────┤
│                                                         │ Zone  │
│                                                         │ 목록  │
│   ┌─────────────────────────────────────────────────┐   │───────│
│   │  video-canvas (drawImage)                       │   │ ● 크레│
│   │  ┌─────────────────────────────────────────┐    │   │   인  │
│   │  │  fabric-canvas (Fabric.js, 투명 오버레이) │    │   │   구역│
│   │  │  polygon 편집                            │    │   │       │
│   │  └─────────────────────────────────────────┘    │   │ ○ 굴착│
│   └─────────────────────────────────────────────────┘   │   주의│
│                                                         │   구역│
│                                                         │───────│
│                                                         │[+추가]│
│                                                         │[-삭제]│
├─────────────────────────────────────────────────────────┴───────┤
│  [◀◀] [◀] [▶ 재생] [▶] [▶▶]  ⏱ 00:23.12  프레임: 578/3000    │
│  [0.5x] [1x] [2x] [4x]                                        │
│  ├──────────────●───────────────────────────────────────────┤   │
│  ████  ███            ██████████       ████████████████         │
│                                                                 │
│  [침입 시작] [침입 끝]    기록된 이벤트: 3건                     │
│  ┌─ 이벤트 ──────────────────────────────────────────────┐     │
│  │ #  Zone          시작     끝       길이        [삭제] │     │
│  │ 1  크레인 구역    00:06   00:12    6.0초        [X]   │     │
│  │ 2  굴착 주의     00:41   00:58    17.0초       [X]   │     │
│  └───────────────────────────────────────────────────────┘     │
└─────────────────────────────────────────────────────────────────┘
```

4개 영역:

- **상단 바**: 모드 전환 (Zone 편집 / 어노테이션), 영상 선택 (서버 파일 목록 드롭다운)
- **중앙 좌**: 2-Canvas 스택 (video-canvas + fabric-canvas)
- **중앙 우**: Zone 목록 패널 (추가/삭제, 선택)
- **하단**: 영상 컨트롤 + 재생 속도 + 타임라인 + 이벤트 마킹/목록

---

## 작업 흐름 1: Zone 편집 모드

### 상태 머신

```
                    [+ 추가] 클릭
                         │
    ┌─────────┐     ┌────▼────┐     우클릭으로 polygon 닫기
    │  대기   │     │  그리기  │──────────────┐
    │ (Idle)  │     │(Drawing)│              │
    └────┬────┘     └────┬────┘              │
         │               │                   │
         │          클릭: 꼭짓점 추가          │
         │          Esc: 그리기 취소 → Idle    │
         │               │                   │
         │               ▼                   ▼
         │          다음 꼭짓점 ...      ┌─────────┐
         │                              │  편집   │
         ◄──────── 선택 해제 ───────────│(Editing)│
                                        └─────────┘
                                         드래그: 꼭짓점 이동
                                         드래그 내부: 전체 이동
```

### 1-1. 영상 열기

상단 바의 영상 선택 드롭다운에서 영상을 선택한다 (서버 파일 목록).
영상의 첫 프레임이 video-canvas에 표시된다.
필요하면 재생/프레임 이동으로 zone을 그리기 좋은 장면을 찾는다.
(사람이 없는 빈 화면이 zone을 그리기 가장 편하다)

### 1-2. Zone 추가

우측 패널에서 **[+ 추가]** 를 누르면 새 zone이 생기고, 이름과 타입을 입력한다:

```
┌─ 새 Zone ─────────────┐
│ 이름: 크레인 작업 반경   │
│ 타입: [danger ▼]       │
│       danger           │
│       warning          │
│       entry            │
│ [확인]  [취소]          │
└────────────────────────┘
```

### 1-3. Polygon 그리기

확인을 누르면 **Drawing 상태**에 진입한다.
영상 화면 위에서 마우스로 꼭짓점을 하나씩 클릭한다.
마우스 위치까지 **점선으로 미리보기**가 표시된다.

```
찍은 꼭짓점 3개 + 마우스 위치 미리보기:

   ●──────────●
   │            \
   │             ● (마우스 커서)
   ●· · · · · ·⤴  ← 점선 미리보기
```

- **우클릭**: polygon 닫기 완성 → Editing 상태로 전환
- **Esc**: 그리기 취소, 찍은 꼭짓점 모두 삭제 → Idle 상태로 복귀

완성되면 polygon 내부가 반투명 색상으로 채워지고, 꼭짓점에 조절점(핸들)이 표시된다.

### 1-4. Polygon 편집 (MVP 범위)

| 기능 | 조작 | MVP |
|------|------|-----|
| 꼭짓점 이동 | 조절점 드래그 | O |
| 전체 이동 | polygon 내부 드래그 | O |
| polygon 삭제 | 우측 패널 [-삭제] | O |
| 꼭짓점 추가 | edge 더블클릭 → 삽입 | 추후 |
| 꼭짓점 삭제 | 조절점 우클릭 | 추후 |
| Undo/Redo | - | 추후 |

MVP에서 꼭짓점 추가/삭제가 필요하면 polygon을 삭제하고 다시 그린다.
건설 현장 zone은 보통 4~6개 꼭짓점의 단순한 형태이므로 30초면 다시 그릴 수 있다.

**구현 참고**: Fabric.js `fabric.Polygon`은 꼭짓점 편집을 기본 지원하지 않는다.
커스텀 control point 구현이 필요하며, 구현 시작 전 기술 스파이크(30분~1시간)를 권장한다.

### 1-5. 기존 zone 재편집

우측 패널에서 zone을 클릭하면 해당 polygon이 Editing 상태로 전환된다 (꼭짓점 핸들 표시).
다른 zone 클릭 또는 빈 영역 클릭 시 현재 편집이 종료된다.

### 1-6. 여러 Zone 관리

같은 화면에 여러 zone을 그릴 수 있다.
우측 패널에서 zone을 선택하면 해당 zone이 강조 표시된다.
zone마다 다른 색상으로 구분한다 (danger=빨강, warning=노랑, entry=파랑).

### 1-7. 저장

[저장] 버튼을 누르면 zone 설정이 YAML 파일로 저장된다.
좌표는 canvas 픽셀 좌표에서 0~1 정규화 좌표로 변환되어 저장된다.
GeoJSON Polygon 포맷을 사용한다.

```yaml
zones:
  - zone_id: crane_area
    zone_name: 크레인 작업 반경
    zone_type: danger
    geometry:
      type: Polygon
      coordinates:
        - - [0.10, 0.25]
          - [0.55, 0.20]
          - [0.60, 0.85]
          - [0.15, 0.90]
          - [0.10, 0.25]
    triggering_anchor: BOTTOM_CENTER
    target_classes: [0]
    min_consecutive_frames: 3
    cooldown_ms: 30000
```

---

## 작업 흐름 2: 어노테이션 모드

### 2-1. Zone 설정 불러오기

모드를 어노테이션으로 전환하면, 기존에 저장한 zone 설정 파일을 불러온다.
화면에 zone polygon이 오버레이된 상태에서 영상이 재생된다.
어노테이션 모드에서 polygon은 **정적 표시만** 되고 편집할 수 없다 (Fabric.js 포인터 이벤트 비활성화).

### 2-2. 영상 탐색

하단 컨트롤로 영상을 탐색한다:

```
[◀◀]     : 5초 뒤로
[◀]      : 1프레임 뒤로 (← 키)
[▶ 재생]  : 재생/일시정지 토글
[▶]      : 1프레임 앞으로 (→ 키)
[▶▶]     : 5초 앞으로
─────●──── : 시간 슬라이더 (드래그로 원하는 위치로 이동)
```

키보드 단축키: `←` / `→` (프레임 이동)만 지원. 나머지는 모두 버튼.

재생 속도: `0.5x` / `1x` / `2x` / `4x` 버튼으로 변경.

### 2-3. 프레임 정확도

`video.currentTime = frame / fps`로 seek한다.
HTML5 video의 seek은 ±2-5프레임 오차가 있을 수 있다.
Event-level 평가에서는 이 오차를 허용하므로 MVP에서 문제 없다.
`requestVideoFrameCallback`이 가용하면 더 정확한 프레임 번호를 얻을 수 있으나 추후 적용.

### 2-4. 침입 이벤트 마킹

영상을 재생하다가 사람이 zone에 들어가는 장면을 발견하면:

**① 우측 패널에서 해당 zone을 선택한다**
- zone이 1개면 자동 선택
- zone이 2개 이상이고 미선택 상태면 "zone을 선택하세요" 안내 표시

**② [침입 시작] 버튼을 누른다**

```
현재 프레임: 150
→ "크레인 구역" zone에 침입 시작 기록됨

하단 표시:
  🔴 기록 중... (프레임 150~)    [침입 끝]
```

**③ 사람이 zone에서 나가는 시점까지 영상을 진행한다**

**④ [침입 끝] 버튼을 누른다**

```
현재 프레임: 300
→ 침입 이벤트 확정: 프레임 150~300 (6초간)

하단 이벤트 목록에 추가됨:
  #1  크레인 구역  00:06~00:12  (150-300)
```

이걸 반복한다.

**마킹 중 [침입 시작]을 다시 누르면**: 이전 마킹이 취소되고 현재 프레임이 새 시작점이 된다.
(시작점을 잘못 찍었을 때 빠르게 교정 가능)

**영상 시작 시 이미 zone 안에 사람이 있는 경우**: 첫 프레임에서 [침입 시작]을 누르면 된다.
특별한 처리 불필요.

### 2-5. 이벤트 확인/수정

기록한 이벤트는 하단에 목록으로 표시된다:

```
┌─ 기록된 이벤트 ──────────────────────────────────────┐
│ #   Zone          시작      끝        길이            │
│ 1   크레인 구역    00:06    00:12     6.0초   [삭제]  │
│ 2   크레인 구역    00:25    00:25     0.4초   [삭제]  │
│ 3   굴착 주의     00:41    00:58     17.0초  [삭제]  │
│ 4   크레인 구역    01:05    01:22     17.0초  [삭제]  │
└──────────────────────────────────────────────────────┘
```

- 이벤트를 클릭하면 **시작 프레임**으로 영상이 이동하여 확인할 수 있음
- 잘못 기록한 이벤트는 [삭제]로 제거
- 시작/끝 프레임을 직접 숫자로 수정할 수도 있음

### 2-6. 타임라인 시각화

시간 슬라이더 위에 기록된 이벤트 구간이 색상 바로 표시된다.
어디에 이벤트가 있고 어디가 비어있는지 한눈에 파악할 수 있다.

```
영상 타임라인:
├──────────────────────────────────────────────────────────────┤
    ██              █            ██████████       ████████████
   #1(크레인)     #2(크레인)      #3(굴착)         #4(크레인)
```

### 2-7. 저장

[저장] 버튼을 누르면 GT JSON 파일로 내보낸다.
GT는 **자체 완결적** — zone geometry를 스냅샷으로 내장하여, zone 설정 파일을 나중에 수정해도 GT는 영향받지 않는다.

```json
{
  "video": "construction_cctv.mp4",
  "video_fps": 25,
  "video_width": 1920,
  "video_height": 1080,
  "total_frames": 3012,
  "zones": [
    {
      "zone_id": "crane_area",
      "zone_name": "크레인 작업 반경",
      "zone_type": "danger",
      "geometry": {
        "type": "Polygon",
        "coordinates": [[[0.10, 0.25], [0.55, 0.20], [0.60, 0.85], [0.15, 0.90], [0.10, 0.25]]]
      }
    }
  ],
  "events": [
    {"zone_id": "crane_area",          "start_frame": 150, "end_frame": 300},
    {"zone_id": "crane_area",          "start_frame": 625, "end_frame": 635},
    {"zone_id": "excavation_warning",  "start_frame": 1025, "end_frame": 1450},
    {"zone_id": "crane_area",          "start_frame": 1625, "end_frame": 2050}
  ]
}
```

---

## 키보드 단축키

| 키 | 동작 |
|---|---|
| `←` | 1프레임 뒤로 |
| `→` | 1프레임 앞으로 |

나머지 모든 동작은 버튼으로 처리한다.

---

## 전체 작업 순서

```
1. 도구 실행 + 영상 선택 (서버 파일 목록 드롭다운)

2. [Zone 편집 모드]
   빈 화면 찾기 → [+추가] → polygon 그리기 → [저장]
                 (이 과정을 zone 개수만큼 반복)

3. [어노테이션 모드로 전환]
   zone 설정 불러오기 → 영상 재생 →
   침입 발견 시 [침입 시작] → 끝나면 [침입 끝] → [저장]
   (이 과정을 이벤트 개수만큼 반복)

4. 산출물
   - DATA_ROOT/configs/zones/sample.yaml  ← zone 설정
   - DATA_ROOT/zone_gt/gt.json            ← 정답지 (평가에 사용)
```
