## Why

P2-2(Detection + Tracking 정성 평가)에 건설 현장 영상이 필요하다. 현재 PoC 영상 1개(construction_helmets.avi)뿐이라 다양한 조건의 영상을 YouTube에서 확보해야 한다. 영상 다운로드를 반복할 수 있는 유틸 스크립트가 필요하다.

## What Changes

- YouTube URL에서 영상을 다운로드하여 samples/에 저장하는 스크립트 추가
- yt-dlp를 dev 의존성에 추가
- 해상도 제한, 구간 추출, 파일명 지정 기능 제공

## Capabilities

### New Capabilities

- `video-download`: YouTube URL로 영상을 다운로드하고 samples/에 저장한다

### Modified Capabilities

(없음)

## Impact

- `scripts/`: 다운로드 스크립트 추가
- `pyproject.toml`: yt-dlp dev 의존성 추가
- 시스템 의존성: ffmpeg (구간 추출 시 필요)
