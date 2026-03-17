## Context

Phase 1 완료 후, 프로젝트 내 대용량 파일 관리 방식을 재구성한다. 현재 data/, models/, outputs/, experiments/가 프로젝트 내에 있고 .gitignore로 제외 중이나, share 디렉토리로 통합하여 git repo를 코드 전용으로 만든다.

## Goals / Non-Goals

**Goals:**
- 모든 대용량 데이터를 /home/neo/share/watch-tower_data/로 통합
- DATA_ROOT 환경변수 하나로 모든 데이터 경로를 제어
- 환경변수 없을 때 기본값으로 동작 (개발 편의)
- 기존 스크립트 3개 + conftest 수정

**Non-Goals:**
- .env 파일 자동 로딩 (python-dotenv 등)
- 프로젝트 내 data/, models/, experiments/ 디렉토리 자체 삭제 (gitignore만 정리)

## Decisions

### 1. config 모듈 위치: src/watch_tower/config.py
- 환경변수 `WATCH_TOWER_DATA_ROOT`를 읽음
- 기본값: `/home/neo/share/watch-tower_data`
- 하위 경로: samples/, models/, outputs/, dataset/, experiments/

### 2. 환경변수 이름: WATCH_TOWER_DATA_ROOT
- 프로젝트 고유 접두사로 충돌 방지
- 설정 안 하면 기본값 사용 (로컬 개발에서 별도 설정 불필요)

### 3. git 추적 변경
- data/samples/.gitkeep → git rm (share로 이동하므로 불필요)
- experiments/README.md → git rm (share의 experiments/에 이동)
- experiments/README.md 내용은 docs나 config 모듈 docstring에 보존
- .gitignore에서 data/*, experiments/* 관련 복잡한 규칙 제거 → 단순화

### 4. 물리 파일 이동
- data/samples/* → /home/neo/share/watch-tower_data/samples/
- models/*.pt → /home/neo/share/watch-tower_data/models/
- outputs/* → /home/neo/share/watch-tower_data/outputs/
- experiments/* → /home/neo/share/watch-tower_data/experiments/
- workspace_watch-tower/dataset/ → /home/neo/share/watch-tower_data/dataset/

### 5. models/README.md 유지
- git 추적 유지 (모델 목록/출처 문서이므로 코드의 일부)
- 다운로드 경로 안내만 업데이트

## Risks / Trade-offs

- **[share 디렉토리 마운트 안 됨]** → 환경변수로 다른 경로 지정 가능. config 모듈이 디렉토리 부재 시 명확한 에러 메시지 출력.
- **[기존 실행 명령어 변경]** → run_inference.py의 --source 경로가 달라짐. 문서 업데이트 필요.
