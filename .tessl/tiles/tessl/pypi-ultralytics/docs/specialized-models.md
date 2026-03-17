# Specialized Models

Specialized model implementations for specific computer vision tasks including open-vocabulary detection, promptable segmentation, efficient segmentation, transformer-based detection, and neural architecture search.

## Capabilities

### YOLOWorld - Open Vocabulary Detection

YOLO-World model enables open-vocabulary object detection, allowing detection of custom classes without retraining.

```python { .api }
class YOLOWorld:
    def __init__(self, model="yolov8s-world.pt", verbose=False):
        """
        Initialize YOLOv8-World model.
        
        Parameters:
        - model (str | Path): Path to pre-trained model file
        - verbose (bool): Enable verbose output during initialization
        """
    
    def set_classes(self, classes: List[str]):
        """
        Set custom classes for detection.
        
        Parameters:
        - classes (List[str]): List of class names to detect
        """
```

**Usage Examples:**

```python
from ultralytics import YOLOWorld

# Initialize YOLOWorld model
model = YOLOWorld("yolov8s-world.pt")

# Set custom classes
model.set_classes(["person", "bicycle", "car", "motorcycle"])

# Perform detection with custom classes
results = model("image.jpg")

# Update classes dynamically
model.set_classes(["apple", "banana", "orange"])
results = model("fruit_image.jpg")
```

### SAM - Segment Anything Model

Segment Anything Model provides promptable segmentation using bounding boxes, points, or text prompts.

```python { .api }
class SAM:
    def __init__(self, model="sam_b.pt"):
        """
        Initialize SAM model.
        
        Parameters:
        - model (str | Path): Path to SAM model file
        """
    
    def predict(self, source, stream=False, bboxes=None, points=None, labels=None, **kwargs) -> List[Results]:
        """
        Perform segmentation with prompts.
        
        Parameters:
        - source: Input image source
        - stream (bool): Stream processing mode
        - bboxes (List[List[float]], optional): Bounding box prompts [[x1, y1, x2, y2], ...]
        - points (List[List[float]], optional): Point prompts [[x, y], ...]
        - labels (List[int], optional): Point labels (1 for foreground, 0 for background)
        - **kwargs: Additional arguments
        
        Returns:
        List[Results]: Segmentation results
        """
    
    def __call__(self, source=None, stream=False, bboxes=None, points=None, labels=None, **kwargs) -> List[Results]:
        """Callable interface for predict method."""
```

**Usage Examples:**

```python
from ultralytics import SAM

# Initialize SAM model
model = SAM("sam_b.pt")  # or sam_l.pt, sam_h.pt for larger models

# Segment with bounding box prompts
results = model("image.jpg", bboxes=[[100, 100, 200, 200]])

# Segment with point prompts
results = model("image.jpg", points=[[150, 150]], labels=[1])

# Combine prompts
results = model("image.jpg", 
                bboxes=[[100, 100, 200, 200]], 
                points=[[150, 150], [180, 180]], 
                labels=[1, 0])

# Process results
for r in results:
    masks = r.masks.data  # Segmentation masks
    r.show()            # Display results
```

### FastSAM - Fast Segment Anything

FastSAM provides efficient segmentation with significantly faster inference than SAM while maintaining competitive accuracy.

```python { .api }
class FastSAM:
    def __init__(self, model="FastSAM-x.pt"):
        """
        Initialize FastSAM model.
        
        Parameters:
        - model (str | Path): Path to FastSAM model file
        """
    
    def predict(self, source, **kwargs) -> List[Results]:
        """
        Perform fast segmentation.
        
        Parameters:
        - source: Input image source  
        - **kwargs: Additional arguments
        
        Returns:
        List[Results]: Segmentation results
        """
```

**Usage Examples:**

```python
from ultralytics import FastSAM

# Initialize FastSAM model
model = FastSAM("FastSAM-x.pt")  # or FastSAM-s.pt for smaller/faster model

# Perform segmentation
results = model("image.jpg")

# With custom parameters
results = model("image.jpg", conf=0.4, iou=0.9)

# Process results
for r in results:
    masks = r.masks.data  # Segmentation masks
    boxes = r.boxes.data  # Bounding boxes
    r.save("output.jpg")  # Save results
```

### RTDETR - Real-Time Detection Transformer

Real-Time Detection Transformer provides state-of-the-art object detection using transformer architecture.

```python { .api }
class RTDETR:
    def __init__(self, model="rtdetr-l.pt"):
        """
        Initialize RTDETR model.
        
        Parameters:
        - model (str | Path): Path to RTDETR model file
        """
```

**Usage Examples:**

```python
from ultralytics import RTDETR

# Initialize RTDETR model
model = RTDETR("rtdetr-l.pt")  # or rtdetr-x.pt for extra large

# Perform detection
results = model("image.jpg")

# With custom parameters
results = model("image.jpg", conf=0.5, imgsz=640)
```

### NAS - Neural Architecture Search

Neural Architecture Search models for automated architecture optimization.

```python { .api }
class NAS:
    def __init__(self, model="yolo_nas_s.pt"):
        """
        Initialize NAS model.
        
        Parameters:
        - model (str | Path): Path to NAS model file
        """
```

**Usage Examples:**

```python
from ultralytics import NAS

# Initialize NAS model
model = NAS("yolo_nas_s.pt")  # or yolo_nas_m.pt, yolo_nas_l.pt

# Perform detection
results = model("image.jpg")

# Training (if supported)
model.train(data="coco8.yaml", epochs=100)
```

## Model Comparison

| Model | Primary Use Case | Speed | Accuracy | Prompt Support |
|-------|------------------|-------|----------|---------------|
| YOLO | General detection/segmentation | Fast | High | No |
| YOLOWorld | Open vocabulary detection | Fast | High | Text classes |
| SAM | Precise segmentation | Slow | Very High | Bbox/Points |
| FastSAM | Fast segmentation | Very Fast | High | Limited |
| RTDETR | Transformer detection | Medium | Very High | No |
| NAS | Optimized architectures | Fast | High | No |

## Types

```python { .api }
from typing import List, Optional, Union
from ultralytics.engine.results import Results

# Common types for specialized models
BboxPrompt = List[float]  # [x1, y1, x2, y2]
PointPrompt = List[float]  # [x, y]
ClassList = List[str]     # ["class1", "class2", ...]
LabelList = List[int]     # [1, 0, 1, ...]  (1=foreground, 0=background)
```