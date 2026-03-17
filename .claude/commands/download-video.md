---
name: "Download Video"
description: YouTube 영상을 다운로드하여 samples/에 저장
category: Data
tags: [data, video, youtube]
---

YouTube 영상을 다운로드하여 평가용 샘플 데이터로 저장한다.

사용자가 제공한 인자: $ARGUMENTS

인자 형식 예시:
- `https://youtube.com/watch?v=... site_01`
- `https://youtube.com/watch?v=... site_02 --section "1:30-3:00"`
- `https://youtube.com/watch?v=... site_03 --resolution 720 --section "0:00-2:00"`

## 실행 방법

1. 인자에서 URL과 이름을 파싱한다. 첫 번째 인자가 URL, 두 번째가 name이다.
2. 나머지 옵션(--section, --resolution)이 있으면 그대로 전달한다.
3. 다음 명령을 실행한다:

```bash
uv run python scripts/download_video.py --url "<URL>" --name "<NAME>" [추가 옵션]
```

4. 다운로드 완료 후 결과를 알려준다.

인자가 비어있으면 사용법을 안내한다:
```
/download-video <YouTube URL> <파일명> [--section "시작-끝"] [--resolution 숫자]
```
