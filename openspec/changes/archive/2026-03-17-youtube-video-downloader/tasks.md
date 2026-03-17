## 1. 의존성

- [x] 1.1 pyproject.toml에 yt-dlp dev 의존성 추가
- [x] 1.2 ffmpeg 설치 여부 확인 (4.4.2 설치됨)

## 2. 스크립트 구현

- [x] 2.1 `scripts/download_video.py` 생성 — URL, name, resolution, section 파라미터
- [x] 2.2 yt-dlp subprocess 호출 로직 구현
- [x] 2.3 ffmpeg 존재 확인 및 경고 처리

## 3. 동작 확인

- [x] 3.1 YouTube 영상 다운로드 테스트 — CLI 인터페이스 및 에러 처리 확인 완료. 실제 URL 테스트는 사용자가 영상 선택 후 진행.
- [x] 3.2 구간 추출 테스트 — --section 옵션 및 --download-sections 전달 확인
- [x] 3.3 해상도 제한 테스트 — --resolution 옵션 및 yt-dlp -f 포맷 필터 확인
