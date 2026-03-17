"""Detection + Tracking 정성 평가 스크립트.

건설 현장 영상에 YOLO Detection + ByteTrack을 적용하고,
supervision으로 bbox + track ID + 궤적을 오버레이한 결과 영상을 생성한다.

사용법:
    uv run python scripts/run_tracking.py --source /home/neo/share/watch-tower_data/samples/construction_subway_cctv.mp4
    uv run python scripts/run_tracking.py --source 영상경로 --conf 0.15
"""

import argparse
from pathlib import Path

import cv2
import numpy as np
import supervision as sv
from ultralytics import YOLO

from watch_tower.config import MODELS_DIR, OUTPUTS_DIR

DEFAULT_MODEL = MODELS_DIR / "yolo11m-construction-hazard.pt"
OUTPUT_DIR = OUTPUTS_DIR / "tracking"

PERSON_CLASS_INDEX = 5  # yolo11m-construction-hazard의 Person 클래스


def run(source: str, model_path: Path, output_dir: Path, conf: float) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)

    source_name = Path(source).stem
    output_path = output_dir / f"{source_name}_tracked.mp4"

    model = YOLO(str(model_path))

    # 영상 정보 확인
    cap = cv2.VideoCapture(source)
    w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = cap.get(cv2.CAP_PROP_FPS)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    cap.release()

    print(f"모델: {model_path.name}")
    print(f"입력: {source}")
    print(f"해상도: {w}x{h}, FPS: {fps:.1f}, 프레임: {total_frames}")
    print(f"출력: {output_path}")
    print(f"신뢰도 임계값: {conf}")
    print()

    # Annotator 설정
    box_annotator = sv.BoxAnnotator(thickness=2)
    label_annotator = sv.LabelAnnotator(text_scale=0.5, text_thickness=1)
    trace_annotator = sv.TraceAnnotator(thickness=2, trace_length=90)

    # 영상 처리
    frame_generator = sv.get_video_frames_generator(source)
    video_info = sv.VideoInfo.from_video_path(source)

    with sv.VideoSink(str(output_path), video_info) as sink:
        for i, frame in enumerate(frame_generator):
            results = model.track(
                frame,
                device="cuda",
                conf=conf,
                persist=True,
                tracker="bytetrack.yaml",
                verbose=False,
            )[0]

            detections = sv.Detections.from_ultralytics(results)

            # track ID가 있는 경우만 처리
            if results.boxes.id is not None:
                detections.tracker_id = results.boxes.id.cpu().numpy().astype(int)

            # 라벨 생성: "Person #3" 형식
            labels = []
            for j in range(len(detections)):
                cls_name = results.names[int(detections.class_id[j])]
                tid = detections.tracker_id[j] if detections.tracker_id is not None else "?"
                labels.append(f"{cls_name} #{tid}")

            # 시각화
            annotated = frame.copy()
            annotated = box_annotator.annotate(annotated, detections)
            annotated = label_annotator.annotate(annotated, detections, labels=labels)
            if detections.tracker_id is not None and len(detections.tracker_id) > 0:
                annotated = trace_annotator.annotate(annotated, detections)

            sink.write_frame(annotated)

            if (i + 1) % 100 == 0 or i == 0:
                person_count = int(np.sum(detections.class_id == PERSON_CLASS_INDEX)) if len(detections) > 0 else 0
                print(f"  프레임 {i+1}/{total_frames} — 감지: {len(detections)}, Person: {person_count}")

    print(f"\n결과 영상 저장: {output_path}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Detection + Tracking 정성 평가")
    parser.add_argument("--source", required=True, help="입력 영상 경로")
    parser.add_argument("--model", default=str(DEFAULT_MODEL), help="모델 가중치 경로")
    parser.add_argument("--output", default=str(OUTPUT_DIR), help="출력 디렉토리")
    parser.add_argument("--conf", type=float, default=0.25, help="신뢰도 임계값")
    args = parser.parse_args()

    run(
        source=args.source,
        model_path=Path(args.model),
        output_dir=Path(args.output),
        conf=args.conf,
    )


if __name__ == "__main__":
    main()
