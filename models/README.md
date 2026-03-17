# 모델 가중치

모델 가중치 파일은 프로젝트 외부 데이터 디렉토리에 저장된다.
기본 경로: `/home/neo/share/watch-tower_data/models/`
(환경변수 `WATCH_TOWER_DATA_ROOT`로 변경 가능)

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
