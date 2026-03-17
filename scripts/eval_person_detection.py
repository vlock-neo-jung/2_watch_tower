"""Person Detection 정량 평가 스크립트.

Construction-PPE 데이터셋으로 yolo11m-construction-hazard 모델의
Person Detection 성능(mAP@50, Recall)을 측정한다.

사용법:
    uv run python scripts/eval_person_detection.py
    uv run python scripts/eval_person_detection.py --conf 0.15
"""

import argparse
import json
from datetime import datetime
from pathlib import Path

from ultralytics import YOLO

from watch_tower.config import DATASET_DIR, EXPERIMENTS_DIR, MODELS_DIR

DEFAULT_MODEL = MODELS_DIR / "yolo11m-construction-hazard.pt"

# Go/No-Go 기준
THRESHOLD_MAP50 = 0.75
THRESHOLD_RECALL = 0.80
LEAKAGE_THRESHOLD = 0.95


DEFAULT_DATA_YAML = DATASET_DIR / "construction-ppe-remapped" / "construction-ppe-remapped.yaml"


def run_eval(model_path: Path, conf: float, data_yaml: Path = DEFAULT_DATA_YAML) -> dict:
    """model.val()을 실행하고 결과를 딕셔너리로 반환한다."""
    model = YOLO(str(model_path))

    results = model.val(
        data=str(data_yaml),
        device="cuda",
        conf=conf,
        project=str(DATASET_DIR),
        name="construction-ppe-val",
        exist_ok=True,
    )

    class_names = results.names
    ap_class_indices = results.box.ap_class_index

    # 클래스별 성능 추출 (GT가 있는 클래스만 결과 배열에 포함됨)
    class_results = []
    person_result = None

    for arr_idx, cls_idx in enumerate(ap_class_indices):
        name = class_names[int(cls_idx)]
        entry = {
            "class": name,
            "precision": float(results.box.p[arr_idx]),
            "recall": float(results.box.r[arr_idx]),
            "map50": float(results.box.ap50[arr_idx]),
            "map50_95": float(results.box.ap[arr_idx]),
        }
        class_results.append(entry)
        if name.lower() == "person":
            person_result = entry

    return {
        "model": model_path.name,
        "dataset": "Construction-PPE",
        "conf_threshold": conf,
        "overall": {
            "map50": float(results.box.map50),
            "map50_95": float(results.box.map),
            "precision": float(results.box.mp),
            "recall": float(results.box.mr),
        },
        "person": person_result,
        "class_results": class_results,
        "val_dir": str(DATASET_DIR / "construction-ppe-val"),
    }


def judge(eval_result: dict) -> dict:
    """Go/No-Go 판단을 수행한다."""
    person = eval_result["person"]

    if person is None:
        return {
            "decision": "No-Go",
            "reason": "Person 클래스를 찾을 수 없음",
            "leakage_warning": False,
        }

    map50 = person["map50"]
    recall = person["recall"]

    map50_pass = map50 >= THRESHOLD_MAP50
    recall_pass = recall >= THRESHOLD_RECALL
    leakage = map50 > LEAKAGE_THRESHOLD

    if map50_pass and recall_pass:
        decision = "Go"
    else:
        decision = "No-Go"

    reasons = []
    if not map50_pass:
        reasons.append(f"mAP@50 {map50:.1%} < {THRESHOLD_MAP50:.0%} → SODA 독립 검증 필요")
    if not recall_pass:
        reasons.append(f"Recall {recall:.1%} < {THRESHOLD_RECALL:.0%} → 신뢰도 임계값 조정 후 재평가")
    if leakage:
        reasons.append(f"mAP@50 {map50:.1%} > {LEAKAGE_THRESHOLD:.0%} → 데이터 leakage 의심, SODA 독립 검증 필요")

    return {
        "decision": decision,
        "reason": "; ".join(reasons) if reasons else "모든 기준 충족",
        "leakage_warning": leakage,
        "thresholds": {
            "map50": {"value": map50, "threshold": THRESHOLD_MAP50, "pass": map50_pass},
            "recall": {"value": recall, "threshold": THRESHOLD_RECALL, "pass": recall_pass},
        },
    }


def print_results(eval_result: dict, judgment: dict) -> None:
    """결과를 터미널에 출력한다."""
    person = eval_result["person"]
    overall = eval_result["overall"]

    print()
    print("=" * 60)
    print("Person Detection 정량 평가 결과")
    print("=" * 60)
    print(f"모델: {eval_result['model']}")
    print(f"데이터셋: {eval_result['dataset']}")
    print(f"신뢰도 임계값: {eval_result['conf_threshold']}")
    print()

    # Person 클래스 결과
    print("[ Person 클래스 ]")
    if person:
        print(f"  mAP@50:    {person['map50']:.1%}")
        print(f"  mAP@50:95: {person['map50_95']:.1%}")
        print(f"  Precision: {person['precision']:.1%}")
        print(f"  Recall:    {person['recall']:.1%}")
    else:
        print("  Person 클래스를 찾을 수 없음")
    print()

    # 전체 클래스별 요약
    print("[ 클래스별 성능 ]")
    print(f"  {'클래스':<15} {'mAP@50':>8} {'Recall':>8} {'Precision':>10}")
    print(f"  {'-'*15} {'-'*8} {'-'*8} {'-'*10}")
    for cr in eval_result["class_results"]:
        print(f"  {cr['class']:<15} {cr['map50']:>7.1%} {cr['recall']:>7.1%} {cr['precision']:>9.1%}")
    print()
    print(f"  {'전체 평균':<15} {overall['map50']:>7.1%} {overall['recall']:>7.1%} {overall['precision']:>9.1%}")
    print()

    # Go/No-Go 판단
    print("[ Go/No-Go 판단 ]")
    print(f"  판정: {judgment['decision']}")
    print(f"  근거: {judgment['reason']}")
    if judgment["leakage_warning"]:
        print("  ⚠️  Leakage 경고: mAP가 비정상적으로 높음")
    print("=" * 60)


def save_report(eval_result: dict, judgment: dict) -> Path:
    """결과 요약 마크다운을 experiments/에 저장한다."""
    today = datetime.now().strftime("%Y-%m-%d")
    report_dir = EXPERIMENTS_DIR / f"{today}-person-detection-eval"
    report_dir.mkdir(parents=True, exist_ok=True)

    person = eval_result["person"]
    overall = eval_result["overall"]

    lines = [
        "# Person Detection 정량 평가 결과",
        "",
        f"- 날짜: {today}",
        f"- 모델: {eval_result['model']}",
        f"- 데이터셋: {eval_result['dataset']}",
        f"- 신뢰도 임계값: {eval_result['conf_threshold']}",
        "",
        "## Person 클래스 결과",
        "",
    ]

    if person:
        lines += [
            f"| 지표 | 값 | 기준 | 통과 |",
            f"|------|-----|------|------|",
            f"| mAP@50 | {person['map50']:.1%} | >= {THRESHOLD_MAP50:.0%} | {'✅' if judgment['thresholds']['map50']['pass'] else '❌'} |",
            f"| Recall | {person['recall']:.1%} | >= {THRESHOLD_RECALL:.0%} | {'✅' if judgment['thresholds']['recall']['pass'] else '❌'} |",
            f"| Precision | {person['precision']:.1%} | - | - |",
            f"| mAP@50:95 | {person['map50_95']:.1%} | - | - |",
        ]
    else:
        lines.append("Person 클래스를 찾을 수 없음")

    lines += [
        "",
        "## 클래스별 성능",
        "",
        f"| 클래스 | mAP@50 | Recall | Precision |",
        f"|--------|--------|--------|-----------|",
    ]
    for cr in eval_result["class_results"]:
        lines.append(f"| {cr['class']} | {cr['map50']:.1%} | {cr['recall']:.1%} | {cr['precision']:.1%} |")
    lines.append(f"| **전체 평균** | **{overall['map50']:.1%}** | **{overall['recall']:.1%}** | **{overall['precision']:.1%}** |")

    lines += [
        "",
        "## Go/No-Go 판단",
        "",
        f"- **판정: {judgment['decision']}**",
        f"- 근거: {judgment['reason']}",
    ]
    if judgment["leakage_warning"]:
        lines.append("- ⚠️ Leakage 경고: mAP가 비정상적으로 높음. SODA 독립 검증 필요.")

    lines += [
        "",
        "## 원본 출력",
        "",
        f"- `model.val()` 출력: `{eval_result['val_dir']}`",
    ]

    report_path = report_dir / "report.md"
    report_path.write_text("\n".join(lines), encoding="utf-8")

    # JSON 원본도 저장
    json_path = report_dir / "results.json"
    json_path.write_text(
        json.dumps({"eval": eval_result, "judgment": judgment}, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )

    return report_path


def main() -> None:
    parser = argparse.ArgumentParser(description="Person Detection 정량 평가")
    parser.add_argument("--model", default=str(DEFAULT_MODEL), help="모델 가중치 경로")
    parser.add_argument("--conf", type=float, default=0.25, help="신뢰도 임계값")
    parser.add_argument("--data", default=str(DEFAULT_DATA_YAML), help="데이터셋 yaml 경로")
    args = parser.parse_args()

    model_path = Path(args.model)
    data_yaml = Path(args.data)

    # 평가 실행
    eval_result = run_eval(model_path, args.conf, data_yaml)

    # Go/No-Go 판단
    judgment = judge(eval_result)

    # 터미널 출력
    print_results(eval_result, judgment)

    # 실험 기록 저장
    report_path = save_report(eval_result, judgment)
    print(f"\n리포트 저장: {report_path}")


if __name__ == "__main__":
    main()
