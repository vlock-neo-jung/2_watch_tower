# Supervision

A comprehensive computer vision toolkit that provides model-agnostic utilities for object detection, classification, and segmentation. Supervision offers connectors for popular frameworks like Ultralytics YOLO, Transformers, and MMDetection, along with highly customizable annotation tools and dataset utilities.

## Package Information

- **Package Name**: supervision
- **Language**: Python
- **Installation**: `pip install supervision`

## Core Imports

```python
import supervision as sv
```

## Basic Usage

```python
import supervision as sv
import cv2
from ultralytics import YOLO

# Load image and model
image = cv2.imread("path/to/image.jpg")
model = YOLO("yolov8n.pt")

# Run inference
results = model(image)[0]
detections = sv.Detections.from_ultralytics(results)

# Annotate detections
box_annotator = sv.BoxAnnotator()
label_annotator = sv.LabelAnnotator()

# Add boxes and labels
annotated_frame = box_annotator.annotate(
    scene=image, detections=detections
)
annotated_frame = label_annotator.annotate(
    scene=annotated_frame, detections=detections
)

# Display result
cv2.imshow("Annotated Frame", annotated_frame)
cv2.waitKey(0)
```

## Architecture

Supervision is built around several core concepts:

- **Detections**: Central data structure that standardizes results from various models
- **Annotators**: Visualization tools for adding boxes, labels, masks, and effects  
- **Zones**: Spatial analysis tools (LineZone, PolygonZone) for counting and tracking
- **Trackers**: Multi-object tracking algorithms (ByteTrack)
- **Utilities**: Image/video processing, format conversion, and data manipulation tools

This design enables seamless integration across different computer vision frameworks while providing consistent APIs for common tasks like annotation, tracking, and dataset management.

## Capabilities

### Core Data Structures

The fundamental data classes for representing detection, classification, and keypoint results in a standardized format.

```python { .api }
@dataclass
class Detections:
    xyxy: np.ndarray
    mask: np.ndarray | None = None
    confidence: np.ndarray | None = None
    class_id: np.ndarray | None = None
    tracker_id: np.ndarray | None = None
    data: dict[str, np.ndarray | list] = field(default_factory=dict)
    metadata: dict[str, Any] = field(default_factory=dict)

@dataclass  
class Classifications:
    class_id: np.ndarray
    confidence: np.ndarray | None = None

class KeyPoints: ...
```

[Core Data Structures](./core-data-structures.md)

### Annotators

Comprehensive visualization tools for adding boxes, labels, masks, shapes, and visual effects to images. Includes basic shapes, text labels, tracking trails, and advanced effects.

```python { .api }
class BoxAnnotator: ...
class LabelAnnotator: ...
class MaskAnnotator: ...
class CircleAnnotator: ...
class DotAnnotator: ...
class TraceAnnotator: ...
```

[Annotators](./annotators.md)

### Detection Tools

Spatial analysis tools for counting, tracking, and analyzing objects within defined zones and regions.

```python { .api }
class LineZone: ...
class PolygonZone: ...
class InferenceSlicer: ...
class DetectionsSmoother: ...
```

[Detection Tools](./detection-tools.md)

### Coordinate and Data Conversion

Utilities for converting between different coordinate formats, processing masks and polygons, and transforming data between various computer vision frameworks.

```python { .api }
def xyxy_to_xywh(xyxy: np.ndarray) -> np.ndarray: ...
def mask_to_polygons(mask: np.ndarray) -> list[np.ndarray]: ...
def polygon_to_mask(polygon: np.ndarray, resolution_wh: tuple[int, int]) -> np.ndarray: ...
```

[Coordinate Conversion](./coordinate-conversion.md)

### IOU and NMS Operations

Intersection over Union calculations and Non-Maximum Suppression algorithms for boxes, masks, and oriented boxes.

```python { .api }
def box_iou(boxes_true: np.ndarray, boxes_detection: np.ndarray) -> np.ndarray: ...
def box_non_max_suppression(predictions: np.ndarray, iou_threshold: float = 0.5) -> np.ndarray: ...
```

[IOU and NMS](./iou-nms.md)

### Dataset Management

Tools for loading, processing, and converting datasets between popular formats like COCO, YOLO, and Pascal VOC.

```python { .api }
class BaseDataset: ...
class DetectionDataset: ...
class ClassificationDataset: ...
```

[Dataset Management](./dataset-management.md)

### Drawing and Colors

Low-level drawing utilities and color management for creating custom visualizations and annotations.

```python { .api }
class Color: ...
class ColorPalette: ...
def draw_polygon(image: np.ndarray, polygon: np.ndarray, color: Color) -> np.ndarray: ...
```

[Drawing and Colors](./drawing-colors.md)

### Video and Image Processing

Utilities for processing video streams, handling image operations, and managing video input/output.

```python { .api }
class VideoInfo: ...
class VideoSink: ...
def process_video(source_path: str, target_path: str, callback: callable) -> None: ...
```

[Video Processing](./video-processing.md)

### Tracking

Multi-object tracking algorithms for maintaining object identities across video frames.

```python { .api }
class ByteTrack: ...
```

[Tracking](./tracking.md)

### Metrics and Evaluation

Tools for evaluating model performance including confusion matrices and mean average precision calculations.

```python { .api }
class ConfusionMatrix: ...
class MeanAveragePrecision: ...
```

[Metrics](./metrics.md)

### Vision-Language Model Integration

Support for integrating various vision-language models for zero-shot object detection and image analysis tasks.

```python { .api }
class VLM(Enum):
    PALIGEMMA = "paligemma" 
    FLORENCE_2 = "florence_2"
    QWEN_2_5_VL = "qwen_2_5_vl"
    GOOGLE_GEMINI_2_0 = "gemini_2_0"
    GOOGLE_GEMINI_2_5 = "gemini_2_5"
    MOONDREAM = "moondream"

class LMM(Enum):  # Deprecated, use VLM
    PALIGEMMA = "paligemma"
    FLORENCE_2 = "florence_2" 
    QWEN_2_5_VL = "qwen_2_5_vl"
    GOOGLE_GEMINI_2_0 = "gemini_2_0"
    GOOGLE_GEMINI_2_5 = "gemini_2_5"
    MOONDREAM = "moondream"
```

[VLM Support](./vlm-support.md)

### File Utilities

Utilities for working with files, directories, and different file formats including JSON, YAML, and text files.

```python { .api }
def list_files_with_extensions(directory: str | Path, extensions: list[str] | None = None) -> list[Path]: ...
def read_json_file(file_path: str | Path) -> dict: ...
def save_json_file(data: dict, file_path: str | Path, indent: int = 3) -> None: ...
def read_yaml_file(file_path: str | Path) -> dict: ...
def save_yaml_file(data: dict, file_path: str | Path) -> None: ...
```

[File Utilities](./file-utilities.md)

### Keypoint Annotators

Specialized annotators for drawing keypoints, skeletal connections, and pose estimation results.

```python { .api }
class VertexAnnotator: ...
class EdgeAnnotator: ...
class VertexLabelAnnotator: ...
```

[Keypoint Annotators](./keypoint-annotators.md)

### Conversion Utilities

Utilities for converting between different image formats and computer vision libraries.

```python { .api }
def cv2_to_pillow(opencv_image: np.ndarray) -> Image.Image: ...
def pillow_to_cv2(pillow_image: Image.Image) -> np.ndarray: ...
```

### Notebook Utilities

Utilities for displaying images and visualizations in Jupyter notebooks.

```python { .api }
def plot_image(image: np.ndarray, title: str | None = None) -> None: ...
def plot_images_grid(images: list[np.ndarray], grid_size: tuple[int, int] | None = None) -> None: ...
```

## Types

```python { .api }
# Geometry types
@dataclass
class Point:
    x: float
    y: float

@dataclass  
class Rect:
    x: float
    y: float
    width: float
    height: float

class Position(Enum):
    CENTER = "CENTER"
    TOP_LEFT = "TOP_LEFT"
    TOP_RIGHT = "TOP_RIGHT"
    BOTTOM_LEFT = "BOTTOM_LEFT"
    BOTTOM_RIGHT = "BOTTOM_RIGHT"
    # Additional position values...

# Enums
class ColorLookup(Enum):
    CLASS = "CLASS"
    TRACK = "TRACK"
    INDEX = "INDEX"

class OverlapMetric(Enum):
    IOU = "iou"
    IOS = "ios"
```