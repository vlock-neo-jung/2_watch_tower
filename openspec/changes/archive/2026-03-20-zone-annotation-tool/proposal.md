## Why

Zone 침입 감지 검증(Phase 3)을 위해 두 가지가 필요하다: (1) 카메라 화면에 위험구역 polygon을 그려서 zone 설정 YAML을 생성하는 도구, (2) 영상을 재생하며 침입 이벤트 구간을 마킹하여 GT(Ground Truth) JSON을 생성하는 도구. 현재 이 작업을 수행할 UI가 없으며, 수동으로 좌표를 입력하거나 프레임 번호를 세는 것은 비현실적이다.

이 도구는 Phase 5 대시보드의 Zone 설정 UI 프로토타입이기도 하다.

## What Changes

- FastAPI 백엔드 추가: 영상 파일 서빙(FileResponse), 영상 메타데이터 API, Zone 설정 CRUD, GT 어노테이션 CRUD
- React (Vite + TypeScript) 프론트엔드 추가: drawImage 2-Canvas 스택 영상 렌더링, Fabric.js polygon 편집, Zone 패널, 이벤트 타임라인
- Zone 편집 모드: polygon 그리기/편집(꼭짓점 드래그, 전체 이동) → YAML 저장
- 어노테이션 모드: 영상 재생 + 침입 이벤트 구간 마킹 → GT JSON 저장 (zone geometry 스냅샷 내장)
- pyproject.toml에 api optional dependency 그룹 추가 (fastapi, uvicorn)

## Capabilities

### New Capabilities

- `video-serving`: 영상 파일 목록 조회, FileResponse 서빙(Range Request), ffprobe 기반 메타데이터(fps, width, height, duration, total_frames)
- `zone-crud-api`: Zone 설정 파일 CRUD API. 기존 watch_tower.zone 모듈의 load/save를 HTTP로 노출
- `annotation-crud-api`: GT 어노테이션 파일 CRUD API. GT JSON 읽기/쓰기
- `video-canvas-renderer`: drawImage 2-Canvas 스택 기반 영상 프레임 렌더링. 재생/일시정지, 프레임 단위 이동, 시간 슬라이더, 재생 속도 조절
- `zone-polygon-editor`: Fabric.js 기반 polygon 그리기(클릭→꼭짓점→닫기), 꼭짓점 드래그 편집, 전체 polygon 이동. 상태 머신: Idle → Drawing → Editing
- `zone-panel-ui`: Zone 목록 패널 — 추가(이름, 타입 입력), 삭제, 선택/강조. zone 타입별 색상 구분
- `event-timeline-ui`: 침입 이벤트 마킹(시작/끝 버튼), 이벤트 목록(클릭→시작 프레임 이동, 삭제), 타임라인 시각화(슬라이더 위 이벤트 구간 표시)
- `gt-export`: GT JSON 생성 — zone geometry 스냅샷 내장, 영상 메타데이터 포함, 자체 완결 포맷

### Modified Capabilities

(없음 — 기존 zone-models, zone-config-io, zone-logic-validation은 변경 없이 사용)

## Impact

- 새 디렉토리: `api/` (FastAPI 백엔드), `frontend/` (React 프론트엔드)
- 새 의존성: fastapi, uvicorn[standard], python-multipart (optional "api" 그룹)
- 새 의존성 (frontend): react, vite, typescript, fabric
- 기존 `src/watch_tower/zone/` 모듈: 변경 없이 API에서 import하여 사용
- 기존 코드 수정: `pyproject.toml`에 optional dependency 추가만
