## Context

P2-2를 위해 건설 현장 영상을 YouTube에서 확보해야 한다. 반복적으로 영상을 다운로드할 유틸 스크립트가 필요하다. 기존 `scripts/download_models.py` 패턴을 따른다.

## Goals / Non-Goals

**Goals:**
- YouTube URL → samples/에 mp4 저장
- 해상도 제한 (720p/1080p)
- 구간 추출 (시작~끝 시간 지정)
- 영상만 저장 (오디오 불필요)

**Non-Goals:**
- 일괄 다운로드 (URL 목록 처리)
- 메타데이터 관리
- 자막/오디오 추출

## Decisions

### 1. yt-dlp 직접 호출 (subprocess)

yt-dlp Python API도 있지만 CLI가 더 안정적이고 문서화가 잘 되어있다. subprocess로 호출한다.

대안: yt-dlp Python 라이브러리 → API가 자주 바뀌고 CLI 대비 장점 없음.

### 2. 의존성: yt-dlp (dev 그룹)

프로덕션에는 불필요하므로 dev 의존성으로 추가. ffmpeg는 시스템 패키지로 가정 (이미 설치되어 있음).

### 3. 저장 경로: SAMPLES_DIR

config.py의 `SAMPLES_DIR`(`/home/neo/share/watch-tower_data/samples/`)을 사용.

## Risks / Trade-offs

- **YouTube 정책 변경**: yt-dlp가 깨질 수 있음 → `uv update yt-dlp`로 대응
- **ffmpeg 미설치**: 구간 추출 실패 → 스크립트에서 ffmpeg 존재 확인 후 경고
