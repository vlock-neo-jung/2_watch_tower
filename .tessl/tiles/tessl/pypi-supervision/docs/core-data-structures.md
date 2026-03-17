# Core Data Structures

The fundamental data classes that standardize computer vision results across different frameworks. These structures provide a unified interface for detections, classifications, and keypoints.

## Capabilities

### Detections

The primary data structure for object detection and segmentation results. Standardizes outputs from various models into a consistent format for downstream processing.

```python { .api }
@dataclass
class Detections:
    """
    Standardizes detection/segmentation results from various models.
    
    Attributes:
        xyxy (np.ndarray): Bounding boxes in [x1, y1, x2, y2] format, shape (n, 4)
        mask (np.ndarray | None): Segmentation masks, shape (n, H, W) 
        confidence (np.ndarray | None): Detection confidence scores, shape (n,)
        class_id (np.ndarray | None): Class IDs for detections, shape (n,)
        tracker_id (np.ndarray | None): Tracking IDs, shape (n,)
        data (dict[str, np.ndarray | list]): Additional detection data
        metadata (dict[str, Any]): Collection-level metadata
    """
    xyxy: np.ndarray
    mask: np.ndarray | None = None
    confidence: np.ndarray | None = None
    class_id: np.ndarray | None = None
    tracker_id: np.ndarray | None = None
    data: dict[str, np.ndarray | list] = field(default_factory=dict)
    metadata: dict[str, Any] = field(default_factory=dict)

    def __len__(self) -> int:
        """Returns the number of detections."""

    def __iter__(self) -> Iterator[tuple[
        np.ndarray, np.ndarray | None, float | None, 
        int | None, int | None, dict[str, np.ndarray | list]
    ]]:
        """Iterates over detections yielding (xyxy, mask, confidence, class_id, tracker_id, data)."""

    @classmethod
    def from_ultralytics(cls, ultralytics_results) -> "Detections":
        """Create from Ultralytics YOLO results (detection, segmentation, OBB)."""

    @classmethod
    def from_yolov5(cls, yolov5_results) -> "Detections":
        """Create from YOLOv5 results."""

    @classmethod
    def from_transformers(cls, transformers_results: dict, id2label: dict[int, str] | None = None) -> "Detections":
        """Create from HuggingFace Transformers results."""

    @classmethod
    def from_mmdetection(cls, mmdet_results) -> "Detections":
        """Create from MMDetection results."""

    @classmethod
    def from_tensorflow(cls, tensorflow_results: dict, resolution_wh: tuple) -> "Detections":
        """Create from TensorFlow Hub results."""

    @classmethod
    def from_detectron2(cls, detectron2_results) -> "Detections":
        """Create from Detectron2 results."""

    @classmethod
    def from_inference(cls, roboflow_results: dict) -> "Detections":
        """Create from Roboflow Inference API results."""

    @classmethod
    def from_detr(cls, detr_results) -> "Detections":
        """Create from DETR model results."""

    @classmethod
    def from_sam(cls, sam_results: list) -> "Detections":
        """Create from Segment Anything Model results."""

    @classmethod
    def from_yolo_nas(cls, yolo_nas_results) -> "Detections":
        """Create from YOLO-NAS results."""

    @classmethod
    def from_deepsparse(cls, deepsparse_results) -> "Detections":
        """Create from DeepSparse results."""

    @classmethod
    def empty(cls) -> "Detections":
        """Create empty Detections instance."""

    def with_nms(self, threshold: float = 0.5, class_agnostic: bool = False) -> "Detections":
        """Apply Non-Maximum Suppression filtering."""

    def with_nmm(self, threshold: float = 0.5, class_agnostic: bool = False) -> "Detections":
        """Apply Non-Maximum Merging."""

    def get_anchors_coordinates(self, anchor: Position) -> np.ndarray:
        """Get anchor point coordinates for each detection."""

    def clip_to_image(self, resolution_wh: tuple[int, int]) -> "Detections":
        """Clip detections to image boundaries."""

    def pad(self, px: int) -> "Detections":
        """Add padding to bounding boxes."""

    def scale(self, factor: float, center: tuple[float, float] | None = None) -> "Detections":
        """Scale detections by a factor."""

    def shift(self, shift: np.ndarray) -> "Detections":
        """Shift detections by offset."""

    def crop_image(self, image: np.ndarray) -> list[np.ndarray]:
        """Extract cropped regions from image."""

    def filter(self, mask: np.ndarray, inplace: bool = False) -> "Detections":
        """Filter detections using boolean mask."""

    def merge(self, detections_list: list["Detections"]) -> "Detections":
        """Merge multiple Detections instances."""

    def tracker_id_is_duplicate(self, tracker_id: int) -> bool:
        """Check if tracker ID appears multiple times."""

    def is_equal(self, other: "Detections") -> bool:
        """Check equality with another Detections instance."""
```

#### Usage Example

```python
import supervision as sv
import cv2
from ultralytics import YOLO

# Load model and image
model = YOLO("yolov8n.pt")
image = cv2.imread("image.jpg")

# Get detections
results = model(image)[0]
detections = sv.Detections.from_ultralytics(results)

# Access detection data
print(f"Found {len(detections)} objects")
for xyxy, mask, confidence, class_id, tracker_id, data in detections:
    print(f"Box: {xyxy}, Confidence: {confidence}, Class: {class_id}")

# Filter by confidence
high_conf = detections[detections.confidence > 0.5]

# Apply NMS
filtered = detections.with_nms(threshold=0.4)
```

### Classifications

Data structure for classification results from various models.

```python { .api }
@dataclass
class Classifications:
    """
    Standardizes classification results.
    
    Attributes:
        class_id (np.ndarray): Class IDs, shape (n,)
        confidence (np.ndarray | None): Classification confidence scores, shape (n,)
    """
    class_id: np.ndarray
    confidence: np.ndarray | None = None

    def __len__(self) -> int:
        """Returns the number of classifications."""

    @classmethod
    def from_clip(cls, clip_results) -> "Classifications":
        """Create from CLIP model results."""
```

#### Usage Example

```python
import supervision as sv

# Create classifications from raw results
class_ids = np.array([0, 1, 2])
confidences = np.array([0.95, 0.87, 0.92])
classifications = sv.Classifications(
    class_id=class_ids,
    confidence=confidences
)

print(f"Number of classifications: {len(classifications)}")
```

### KeyPoints

Data structure for keypoint detection results.

```python { .api }
class KeyPoints:
    """
    Represents keypoint detection results for pose estimation and facial landmarks.
    
    Handles keypoint coordinates, visibility, and confidence scores.
    """
    
    @classmethod
    def from_ultralytics(cls, ultralytics_results) -> "KeyPoints":
        """Create from Ultralytics pose estimation results."""

    @classmethod
    def from_mediapipe(cls, mediapipe_results) -> "KeyPoints":
        """Create from MediaPipe results."""
```

#### Usage Example

```python
import supervision as sv
from ultralytics import YOLO

# Load pose estimation model
model = YOLO("yolov8n-pose.pt")
image = cv2.imread("person.jpg")

# Get keypoints
results = model(image)[0]
keypoints = sv.KeyPoints.from_ultralytics(results)
```

## Types

```python { .api }
# Type aliases for common data structures
DetectionDataset = Any  # Dataset containing detection annotations
ClassificationDataset = Any  # Dataset containing classification labels

# Common numpy array shapes used throughout
BoundingBoxes = np.ndarray  # Shape: (n, 4) - [x1, y1, x2, y2]
Masks = np.ndarray  # Shape: (n, H, W) - boolean masks
Confidences = np.ndarray  # Shape: (n,) - confidence scores
ClassIds = np.ndarray  # Shape: (n,) - integer class identifiers
TrackerIds = np.ndarray  # Shape: (n,) - integer tracker identifiers
```