# 모델 가중치

이 디렉토리에는 모델 가중치 파일(.pt, .onnx, .engine)이 저장된다.
가중치 파일은 .gitignore에 의해 추적되지 않으며, 다운로드 스크립트로 재현 가능하다.

## 다운로드

```bash
uv run python scripts/download_models.py
```

## 모델 목록

| 모델 | 파일명 | 출처 | 용도 |
|------|--------|------|------|
| YOLO11m Construction Hazard | yolo11m-construction-hazard.pt | [yihong1120/Construction-Hazard-Detection](https://huggingface.co/yihong1120/Construction-Hazard-Detection) | Person Detection, PPE 감지 (11클래스) |

## 클래스 (11개)

Hardhat, Mask, NO-Hardhat, NO-Mask, NO-Safety Vest, Person, Safety Cone, Safety Vest, machinery, utility pole, vehicle
