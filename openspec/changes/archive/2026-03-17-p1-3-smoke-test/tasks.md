## 1. 환경 준비

- [x] 1.1 scripts/setup_settings.py 실행 (ultralytics datasets_dir 설정)
- [x] 1.2 scripts/download_models.py 실행 (yolo11m-construction-hazard.pt 39MB 다운로드 완료)

## 2. 추론 스크립트 작성

- [x] 2.1 scripts/run_inference.py 작성 (--source, --model, --output, --conf 인자)
- [x] 2.2 outputs/ 디렉토리 자동 생성 로직 포함 (mkdir parents=True)

## 3. Smoke Test 실행

- [x] 3.1 이미지 추론 테스트 (Person 2, Hardhat 1, Safety Vest 2, 67.6ms)
- [x] 3.2 영상 추론 테스트 (207프레임, 12.0ms/frame, 83.1 FPS)
- [x] 3.3 결과 확인: Person 954, Hardhat 443, NO-Safety Vest 843, NO-Mask 4
