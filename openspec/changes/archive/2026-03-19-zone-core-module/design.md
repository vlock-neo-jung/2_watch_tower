## Context

Watch Tower는 건설 현장 AI 안전 모니터링 시스템이다. Phase 2에서 Person Detection + Tracking을 검증 중이며, Phase 3에서 위험구역 침입 감지 + 인원 탐지를 구현한다.

현재 `src/watch_tower/`에는 `config.py` (경로 설정), `detection/`, `utils/`가 있다. Zone 관련 코드는 없다. 데이터는 `DATA_ROOT` (`/home/neo/share/watch-tower_data/`) 패턴으로 관리한다.

이 모듈은 이후 PoC 스크립트, 어노테이션 도구 (FastAPI + React), 평가 스크립트, 실시간 파이프라인에서 모두 사용된다.

## Goals / Non-Goals

**Goals:**
- Zone 정의를 Pydantic 모델로 표현하여 검증, 직렬화, API 스키마 통합
- GeoJSON Polygon 포맷으로 geometry를 표현하여 표준 호환성 확보
- YAML 파일 기반 zone 설정 로드/저장
- supervision PolygonZone 변환 및 anchor point 판정 검증

**Non-Goals:**
- ZoneTracker (이벤트 판정 로직) — Step 4에서 구현
- FastAPI 라우트 — 어노테이션 도구 구현 시 추가
- 데이터베이스 저장 — Phase 5 이후
- Zone 그리기 UI — Step 3a에서 구현

## Decisions

### 1. Pydantic 모델 (dataclass 대신)

**선택**: Pydantic BaseModel
**대안**: dataclass, TypedDict, attrs

**이유**:
- 검증 로직을 validator로 모델 안에 내장 (좌표 범위, 꼭짓점 수, zone_id 중복)
- FastAPI에서 request/response 스키마로 그대로 사용 가능 (변환 코드 불필요)
- JSON/dict 직렬화 내장 (`model_dump()`, `model_validate()`)
- pydantic은 ultralytics 의존성에 이미 포함 → 새 의존성 추가 없음

### 2. GeoJSON Polygon (단순 좌표 리스트 대신)

**선택**: GeoJSON Polygon 포맷 (`{"type": "Polygon", "coordinates": [[[x,y], ...]]}`)
**대안**: 단순 좌표 리스트 (`[[x,y], [x,y], ...]`)

**이유**:
- 표준 포맷으로 PostGIS, Leaflet, Fabric.js 등과 호환
- 타입 필드로 향후 다른 geometry 타입 (LineString 등) 확장 가능
- 단점: 닫힌 고리(closing point) 규칙이 있어 약간 장황함 → validator로 자동 처리

### 3. 모델과 I/O 파일 분리

**선택**: `models.py` (Pydantic 모델) + `config.py` (YAML I/O) 분리
**대안**: 단일 파일

**이유**:
- `models.py`는 API 라우트에서 직접 import (스키마 용도)
- `config.py`는 파일 시스템 접근 (YAML 읽기/쓰기)
- 관심사 분리: 데이터 정의 ≠ 파일 I/O

### 4. 정규화 좌표 (0-1)

**선택**: 모든 geometry 좌표를 0-1 범위로 저장, 사용 시점에 픽셀 좌표로 변환
**대안**: 픽셀 좌표 직접 저장

**이유**:
- 카메라 해상도 변경 시 zone 재설정 불필요
- 프레임 리사이즈에도 zone이 유효
- 변환은 `to_polygon_zone(width, height)` 메서드에서 처리

## Risks / Trade-offs

- **GeoJSON 닫힌 고리 규칙**: GeoJSON Polygon은 첫 점과 마지막 점이 같아야 한다. 프론트엔드에서 보내는 좌표에 closing point가 없을 수 있다. → `validator에서 자동으로 closing point 추가`
- **YAML 포맷 결합**: 설정 파일이 YAML에 묶인다. → 현재는 YAML이 적합. 향후 DB 저장 시 models.py의 Pydantic 모델은 그대로 쓰고 config.py의 I/O만 교체하면 됨
- **pydantic 버전**: ultralytics가 pydantic v2를 사용하는지 확인 필요 → v2 API (model_dump, model_validate) 기준으로 작성
