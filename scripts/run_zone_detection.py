"""Zone 침입 감지 스크립트.

Detection + Tracking + Zone 처리를 통합하여 침입 감지 결과 영상을 생성한다.

사용법:
    uv run python scripts/run_zone_detection.py \\
        --source /home/neo/share/watch-tower_data/samples/construction_subway_cctv.mp4 \\
        --zone-config /home/neo/share/watch-tower_data/configs/zones/sample.yaml

    uv run python scripts/run_zone_detection.py \\
        --source 영상경로 --zone-config zone.yaml --conf 0.25
"""

import argparse
from pathlib import Path

import cv2
import numpy as np
import supervision as sv
from ultralytics import YOLO

from watch_tower.config import MODELS_DIR, OUTPUTS_DIR
from watch_tower.zone import load_zone_config
from watch_tower.zone.logic import ZoneEventType, ZoneProcessor
from watch_tower.zone.models import ZoneDefinition, ZoneType

DEFAULT_MODEL = MODELS_DIR / "yolo11m-construction-hazard.pt"
OUTPUT_DIR = OUTPUTS_DIR / "zone_detection"
DEFAULT_ZONE_CONFIG = "/home/neo/share/watch-tower_data/configs/zones/sample.yaml"

# Zone 타입별 오버레이 색상 (BGR tuple for cv2)
_ZONE_BGR: dict[str, tuple[int, int, int]] = {
    ZoneType.DANGER: (50, 50, 220),
    ZoneType.WARNING: (30, 165, 220),
    ZoneType.ENTRY: (50, 200, 50),
}
_ALERT_BGR = (0, 0, 255)
_TEXT_NORMAL_BGR = (0, 200, 0)


def _draw_zone_overlay(
    frame: np.ndarray,
    zone_def: ZoneDefinition,
    polygon_pixels: np.ndarray,
    has_intruder: bool,
) -> np.ndarray:
    """Zone polygon을 반투명 오버레이로 그린다."""
    color = _ALERT_BGR if has_intruder else _ZONE_BGR.get(zone_def.zone_type, (100, 100, 100))
    overlay = frame.copy()
    pts = polygon_pixels.astype(np.int32).reshape((-1, 1, 2))
    cv2.fillPoly(overlay, [pts], color)
    frame = cv2.addWeighted(overlay, 0.25, frame, 0.75, 0)
    cv2.polylines(frame, [pts], isClosed=True, color=color, thickness=2)
    return frame


def run(
    source: str,
    model_path: Path,
    zone_config_path: str,
    output_dir: Path,
    conf: float,
) -> None:
    model_name = model_path.stem
    run_output_dir = output_dir / model_name
    run_output_dir.mkdir(parents=True, exist_ok=True)

    source_name = Path(source).stem
    output_path = run_output_dir / f"{source_name}_zone.mp4"

    # Zone 설정 로드
    zone_config = load_zone_config(zone_config_path)
    print(f"Zone 설정: {len(zone_config.zones)}개 ({', '.join(z.zone_id for z in zone_config.zones)})")

    # 영상 정보
    cap = cv2.VideoCapture(source)
    w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = cap.get(cv2.CAP_PROP_FPS) or 30.0
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    cap.release()

    print(f"모델: {model_path.name}")
    print(f"입력: {source} ({w}x{h}, FPS={fps:.1f}, {total_frames}프레임)")
    print(f"신뢰도 임계값: {conf}")
    print(f"출력: {output_path}")
    print()

    # Zone 프로세서 및 픽셀 좌표 초기화
    processors: dict[str, ZoneProcessor] = {
        z.zone_id: ZoneProcessor(z, w, h) for z in zone_config.zones
    }
    zone_polygons_px: dict[str, np.ndarray] = {
        z.zone_id: processors[z.zone_id].polygon_zone.polygon for z in zone_config.zones
    }

    # Annotator
    box_annotator = sv.BoxAnnotator(thickness=2)
    label_annotator = sv.LabelAnnotator(text_scale=0.5, text_thickness=1)
    trace_annotator = sv.TraceAnnotator(thickness=2, trace_length=60)

    # 통계
    event_counts: dict[str, dict[str, int]] = {
        z.zone_id: {"enter": 0, "exit": 0} for z in zone_config.zones
    }

    model = YOLO(str(model_path))
    video_info = sv.VideoInfo.from_video_path(source)
    frame_generator = sv.get_video_frames_generator(source)

    with sv.VideoSink(str(output_path), video_info) as sink:
        for frame_idx, frame in enumerate(frame_generator):
            results = model.track(
                frame,
                device="cuda",
                conf=conf,
                persist=True,
                tracker="bytetrack.yaml",
                verbose=False,
            )[0]

            detections = sv.Detections.from_ultralytics(results)
            if results.boxes.id is not None:
                detections.tracker_id = results.boxes.id.cpu().numpy().astype(int)

            # Zone 처리
            for proc in processors.values():
                events = proc.process(detections, fps=fps)
                for e in events:
                    if e.event_type == ZoneEventType.ENTER:
                        event_counts[e.zone_id]["enter"] += 1
                        print(
                            f"  [ENTER] zone={e.zone_id}, "
                            f"tracker={e.tracker_id}, frame={frame_idx}"
                        )
                    elif e.event_type == ZoneEventType.EXIT:
                        event_counts[e.zone_id]["exit"] += 1
                        print(
                            f"  [EXIT]  zone={e.zone_id}, "
                            f"tracker={e.tracker_id}, "
                            f"dwell={e.dwell_frames}f, frame={frame_idx}"
                        )

            # 시각화 — zone 오버레이
            annotated = frame.copy()
            for zone_def in zone_config.zones:
                has_intruder = len(processors[zone_def.zone_id].inside_tracker_ids) > 0
                annotated = _draw_zone_overlay(
                    annotated,
                    zone_def,
                    zone_polygons_px[zone_def.zone_id],
                    has_intruder,
                )

            # 시각화 — detection
            annotated = box_annotator.annotate(annotated, detections)
            if detections.tracker_id is not None and len(detections) > 0:
                labels = [
                    f"{results.names[int(detections.class_id[j])]} #{detections.tracker_id[j]}"
                    for j in range(len(detections))
                ]
                annotated = label_annotator.annotate(annotated, detections, labels=labels)
                annotated = trace_annotator.annotate(annotated, detections)

            # 시각화 — 상태 텍스트
            y = 30
            for zone_def in zone_config.zones:
                inside_count = len(processors[zone_def.zone_id].inside_tracker_ids)
                text = f"{zone_def.zone_name}: {inside_count}명 내부"
                color = _ALERT_BGR if inside_count > 0 else _TEXT_NORMAL_BGR
                cv2.putText(annotated, text, (10, y), cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)
                y += 30

            sink.write_frame(annotated)

            if (frame_idx + 1) % 100 == 0:
                print(f"  프레임 {frame_idx + 1}/{total_frames}")

    print(f"\n결과 영상: {output_path}")
    print("\n이벤트 통계:")
    for zone_id, counts in event_counts.items():
        print(f"  {zone_id}: enter={counts['enter']}, exit={counts['exit']}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Zone 침입 감지")
    parser.add_argument("--source", required=True, help="입력 영상 경로")
    parser.add_argument("--zone-config", default=DEFAULT_ZONE_CONFIG, help="Zone YAML 설정 경로")
    parser.add_argument("--model", default=str(DEFAULT_MODEL), help="모델 가중치 경로")
    parser.add_argument("--output", default=str(OUTPUT_DIR), help="출력 디렉토리")
    parser.add_argument("--conf", type=float, default=0.25, help="신뢰도 임계값")
    args = parser.parse_args()

    run(
        source=args.source,
        model_path=Path(args.model),
        zone_config_path=args.zone_config,
        output_dir=Path(args.output),
        conf=args.conf,
    )


if __name__ == "__main__":
    main()
