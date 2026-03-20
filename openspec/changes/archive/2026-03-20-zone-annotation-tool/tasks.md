## 1. 프로젝트 셋업

- [x] 1.1 pyproject.toml에 api optional dependency 추가 (fastapi, uvicorn[standard], python-multipart)
- [x] 1.2 api/ 디렉토리 구조 생성 (app.py, routes/, schemas.py)
- [x] 1.3 frontend/ React 프로젝트 초기화 (Vite + TypeScript)
- [x] 1.4 frontend/ Fabric.js 의존성 설치
- [x] 1.5 Vite proxy 설정 (/api → localhost:8000)
- [x] 1.6 FastAPI + Vite dev server 동시 실행 확인

## 2. FastAPI 백엔드 — 영상 서빙

- [x] 2.1 GET /api/videos/ — DATA_ROOT/samples/ 내 .mp4 파일 목록 반환
- [x] 2.2 GET /api/videos/{filename} — FileResponse로 영상 서빙
- [x] 2.3 GET /api/videos/{filename}/info — ffprobe로 메타데이터 반환 (fps, width, height, duration, total_frames)

## 3. FastAPI 백엔드 — Zone/GT CRUD

- [x] 3.1 GET /api/zones/ — zone 설정 파일 목록
- [x] 3.2 GET /api/zones/{config_name} — zone 설정 로드 (watch_tower.zone.load_zone_config)
- [x] 3.3 POST /api/zones/{config_name} — zone 설정 저장 (watch_tower.zone.save_zone_config)
- [x] 3.4 GET /api/annotations/ — GT 파일 목록
- [x] 3.5 GET /api/annotations/{name} — GT 로드
- [x] 3.6 POST /api/annotations/{name} — GT 저장
- [x] 3.7 CORS 설정 (Vite dev server 허용)

## 4. 프론트엔드 — VideoPlayer 컴포넌트

- [x] 4.1 hidden <video> 요소 + video-canvas 생성
- [x] 4.2 영상 선택 드롭다운 (GET /api/videos/ 목록)
- [x] 4.3 drawImage() 렌더링 루프 (requestAnimationFrame)
- [x] 4.4 canvas 비율을 영상 원본 비율에 맞추기 (/api/videos/{filename}/info)
- [x] 4.5 재생/일시정지 버튼
- [x] 4.6 프레임 단위 이동 버튼 + ←/→ 키보드
- [x] 4.7 5초 점프 버튼
- [x] 4.8 시간 슬라이더 (seek)
- [x] 4.9 현재 시간 / 프레임 번호 표시
- [x] 4.10 재생 속도 버튼 (0.5x, 1x, 2x, 4x)

## 5. 프론트엔드 — ZoneEditor 컴포넌트 (기술 스파이크 포함)

- [x] 5.1 기술 스파이크: Fabric.js polygon vertex editing 구현 방법 조사 (30분~1시간)
- [x] 5.2 fabric-canvas를 video-canvas 위에 겹치기 (같은 div, 같은 크기, position: absolute)
- [x] 5.3 Drawing 상태: 클릭으로 꼭짓점 배치, 선 연결
- [x] 5.4 Drawing 상태: 마우스 위치까지 점선 미리보기
- [x] 5.5 Drawing 상태: 우클릭으로 polygon 닫기 → Editing 전환
- [x] 5.6 Drawing 상태: Esc로 그리기 취소 → Idle 복귀
- [x] 5.7 Editing 상태: 꼭짓점 핸들 표시 + 드래그 이동
- [x] 5.8 Editing 상태: polygon 내부 드래그로 전체 이동
- [x] 5.9 zone 타입별 색상 적용 (danger=빨강, warning=노랑, entry=파랑, 반투명)
- [x] 5.10 좌표 정규화: canvas 픽셀 ↔ 0-1 정규화 좌표 변환
- [x] 5.11 어노테이션 모드에서 polygon 정적 표시 (편집 비활성화)

## 6. 프론트엔드 — ZonePanel 컴포넌트

- [x] 6.1 zone 목록 렌더링 (이름, 타입, 색상)
- [x] 6.2 zone 선택/강조 (클릭 시 해당 polygon Editing 상태 전환)
- [x] 6.3 [+추가] 버튼 + 이름/타입 입력 다이얼로그
- [x] 6.4 [-삭제] 버튼 (선택된 zone 제거)
- [x] 6.5 zone 설정 저장 버튼 (POST /api/zones/)
- [x] 6.6 zone 설정 불러오기 (GET /api/zones/, 드롭다운 선택)

## 7. 프론트엔드 — EventTimeline 컴포넌트

- [x] 7.1 [침입 시작] / [침입 끝] 버튼 + 기록 중 상태 표시
- [x] 7.2 마킹 중 [침입 시작] 재입력 시 이전 취소 + 새 시작점
- [x] 7.3 zone 미선택 시 마킹 처리 (1개면 자동선택, 2개+면 안내)
- [x] 7.4 이벤트 목록 렌더링 (zone, 시작, 끝, 길이, 삭제 버튼)
- [x] 7.5 이벤트 클릭 → 시작 프레임으로 영상 이동
- [x] 7.6 타임라인 시각화 (슬라이더 위 이벤트 구간 색상 바)
- [x] 7.7 GT JSON 저장 버튼 (POST /api/annotations/, zone geometry 스냅샷 내장)
- [x] 7.8 GT JSON 불러오기 (GET /api/annotations/)

## 8. 모드 전환

- [x] 8.1 상단 바 모드 전환 UI (Zone 편집 ↔ 어노테이션)
- [x] 8.2 Zone 편집 모드: ZoneEditor 편집 활성화, EventTimeline 마킹 비활성화
- [x] 8.3 어노테이션 모드: ZoneEditor 정적 표시, EventTimeline 마킹 활성화

## 9. 통합 테스트

- [x] 9.1 FastAPI 엔드포인트 테스트 (영상 목록, zone CRUD, GT CRUD)
- [ ] 9.2 end-to-end: 영상 선택 → zone 그리기 → 저장 → 어노테이션 → GT 저장 흐름 수동 확인
