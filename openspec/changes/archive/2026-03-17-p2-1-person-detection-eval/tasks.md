## 1. 평가 스크립트 작성

- [x] 1.1 `scripts/eval_person_detection.py` 생성 — `model.val(data="Construction-PPE.yaml", device="cuda")` 실행 및 결과 출력
- [x] 1.2 Person 클래스 mAP@50, Recall, Precision 추출 로직 추가
- [x] 1.3 전체 클래스별 성능 요약 테이블 출력

## 2. 결과 기록

- [x] 2.1 `experiments/YYYY-MM-DD-person-detection-eval/` 디렉토리에 결과 요약 마크다운 자동 생성
- [x] 2.2 `model.val()` 원본 출력(runs/) 경로를 결과 요약에 포함

## 3. 평가 실행 및 판단

- [x] 3.1 평가 스크립트 실행하여 수치 확보 (conf=0.25/0.15/0.10 3회)
- [x] 3.2 Go/No-Go 판단 (mAP@50 >= 75%, Recall >= 80%) → 조건부 Go
- [x] 3.3 Leakage 점검 (mAP > 95% 여부) → leakage 미해당, SODA 독립 검증은 FWY-51로 분리
- [x] 3.4 결과 요약 및 판단 근거를 실험 기록에 기록
