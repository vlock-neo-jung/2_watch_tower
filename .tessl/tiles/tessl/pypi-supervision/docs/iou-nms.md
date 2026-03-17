# IOU and NMS Operations

Intersection over Union calculations and Non-Maximum Suppression algorithms for filtering and merging detection results.

## Capabilities

### IOU Calculation

```python { .api }
def box_iou(boxes_true: np.ndarray, boxes_detection: np.ndarray) -> np.ndarray:
    """Calculate IoU between two sets of boxes."""

def box_iou_batch(boxes_true: np.ndarray, boxes_detection: np.ndarray) -> np.ndarray:
    """Batch IoU calculation between box sets."""

def mask_iou_batch(masks_true: np.ndarray, masks_detection: np.ndarray) -> np.ndarray:
    """Calculate IoU between segmentation masks."""

def oriented_box_iou_batch(boxes_true: np.ndarray, boxes_detection: np.ndarray) -> np.ndarray:
    """IoU calculation for oriented bounding boxes."""
```

### Non-Maximum Suppression

```python { .api }
def box_non_max_suppression(predictions: np.ndarray, iou_threshold: float = 0.5) -> np.ndarray:
    """Apply NMS to remove overlapping boxes."""

def mask_non_max_suppression(predictions: np.ndarray, masks: np.ndarray, iou_threshold: float = 0.5) -> np.ndarray:
    """Apply NMS using mask IoU."""

def box_non_max_merge(predictions: np.ndarray, iou_threshold: float = 0.5) -> np.ndarray:
    """Merge overlapping boxes instead of suppressing."""

class OverlapMetric(Enum):
    IOU = "iou"
    IOS = "ios"

class OverlapFilter(Enum):
    NMS = "nms"
    NMM = "nmm"
```