## Context

Watch Tower 프로젝트의 Zone 침입 감지 검증(Phase 3)을 위한 어노테이션 도구.
`src/watch_tower/zone/` 모듈(Pydantic 모델, YAML I/O)은 이미 구현 완료.
상세 사양: `tmp/zone-intrusion-plan/03-1-annotation-tool-spec.md`

## Goals / Non-Goals

**Goals:**
- Zone 편집 모드: 영상 위에 polygon을 그리고 편집하여 zone 설정 YAML 생성
- 어노테이션 모드: 영상을 재생하며 침입 이벤트 구간을 마킹하여 GT JSON 생성
- 이후 Phase 5 대시보드로 확장 가능한 구조

**Non-Goals:**
- 실시간 RTSP 스트림 연동 (Phase 5)
- 사용자 인증/권한 관리
- 모바일 지원
- 다국어 지원

## Decisions

### 1. drawImage 2-Canvas 스택

**선택**: `<video>` (hidden, 디코딩 전용) + video-canvas (drawImage 렌더링) + fabric-canvas (Fabric.js polygon 편집)
**대안**: `<video>` 요소 위에 단일 canvas 오버레이

**이유**:
- 크기 동기화 문제 소멸 (하나의 div 안에 같은 크기로 겹침)
- 좌표계 통일 (canvas 크기 = 표시 크기)
- 프레임 캡처 용이
- canvas 비율을 영상 원본 비율에 맞춰서 좌표 변환이 단순 곱셈/나눗셈으로 유지

### 2. Fabric.js polygon 편집 MVP 범위

**선택**: 그리기 + 꼭짓점 드래그 + 전체 이동 + polygon 삭제
**대안**: 꼭짓점 추가/삭제/Undo-Redo까지 구현

**이유**:
- Fabric.js의 `fabric.Polygon`은 개별 꼭짓점 편집을 기본 지원하지 않아 커스텀 구현 필요
- MVP에서 꼭짓점 추가/삭제는 "polygon 삭제 후 다시 그리기"로 대체 가능
- 건설 현장 zone은 4~6개 꼭짓점의 단순 형태
- 구현 전 Fabric.js polygon vertex editing 기술 스파이크 권장

### 3. 키보드 단축키 최소화

**선택**: `←/→` (프레임 이동)만 지원
**대안**: S, E, Space, Ctrl+S, Delete 등 다수 단축키

**이유**: 나머지 모든 동작은 버튼으로 충분. MVP 복잡도 감소.

### 4. GT 포맷 — zone geometry 스냅샷 내장

**선택**: GT JSON에 zone geometry를 복사하여 포함 (자체 완결)
**대안**: zone 설정 파일 경로만 참조

**이유**: GT는 평가용 정답지이므로 생성 시점의 zone 정보가 고정되어야 한다. zone 설정을 나중에 수정해도 기존 GT는 영향받지 않아야 한다.

### 5. 영상 서빙 — FileResponse

**선택**: FastAPI FileResponse 한 줄 (Range Request 자동 지원)
**대안**: 커스텀 StreamingResponse + chunk 처리

**이유**: 현재 단계에서 단순함이 최우선. 성능 문제는 실제로 발생할 때 최적화.

### 6. 영상 선택 — 서버 파일 브라우저

**선택**: API가 DATA_ROOT/samples/ 목록을 반환, UI에서 드롭다운 선택
**대안**: 브라우저 파일 업로드 다이얼로그

**이유**: 영상은 이미 서버에 있고, 수백 MB 파일을 브라우저로 업로드하는 것은 비효율적.

### 7. 마킹 중 시작 버튼 재입력

**선택**: 이전 마킹 취소 + 현재 프레임이 새 시작점
**대안**: 무시하고 "이미 마킹 중입니다" 표시

**이유**: 시작점을 잘못 찍었을 때 빠르게 교정 가능.

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│ 브라우저 (React, Vite dev :5173)                             │
│                                                              │
│   VideoPlayer          ZoneEditor         ZonePanel          │
│   ├─ video-canvas      ├─ fabric-canvas   ├─ zone 목록      │
│   ├─ hidden <video>    ├─ Drawing 상태    ├─ [+추가][-삭제]  │
│   ├─ 재생/프레임 제어   └─ Editing 상태    └─ 선택/강조       │
│   └─ 속도 조절                                               │
│                                                              │
│   EventTimeline                                              │
│   ├─ [침입 시작][침입 끝]                                    │
│   ├─ 이벤트 목록 (클릭→시작 프레임 이동)                     │
│   └─ 타임라인 시각화                                         │
│                                                              │
│              │ Vite proxy                                    │
├──────────────┼───────────────────────────────────────────────┤
│ FastAPI (:8000)                                              │
│                                                              │
│   /api/videos/          → 목록, 서빙, 메타데이터             │
│   /api/zones/           → CRUD (watch_tower.zone 모듈 사용)  │
│   /api/annotations/     → CRUD                               │
└─────────────────────────────────────────────────────────────┘
```

## Risks / Trade-offs

- **Fabric.js polygon vertex editing**: 커스텀 control point 구현이 필요. 기술 스파이크로 검증 후 진행
- **프레임 정확도**: HTML5 video의 currentTime seek은 ±2-5프레임 오차 가능. Event-level 평가에서는 허용 범위
- **ffprobe 의존성**: 영상 메타데이터 추출에 ffprobe 필요. 시스템에 ffmpeg 설치가 전제
- **대용량 영상**: FileResponse는 단순하지만 수 GB 영상에서 메모리 문제 가능. 현재 단계에서는 수백 MB 수준이므로 문제 없음
