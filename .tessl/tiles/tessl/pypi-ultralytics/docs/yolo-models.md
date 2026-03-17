# YOLO Models

The YOLO class is the primary interface for working with YOLO models, supporting multiple computer vision tasks including object detection, instance segmentation, image classification, pose estimation, and oriented bounding box detection.

## Capabilities

### Model Initialization

Create YOLO model instances with various pretrained models or custom configurations.

```python { .api }
class YOLO:
    def __init__(self, model="yolo11n.pt", task=None, verbose=False):
        """
        Initialize YOLO model.
        
        Parameters:
        - model (str | Path): Model path or name (default: "yolo11n.pt")
        - task (str, optional): Task type (detect, segment, classify, pose, obb)
        - verbose (bool): Enable verbose output (default: False)
        """
```

**Supported Tasks:**
- `detect`: Object detection
- `segment`: Instance segmentation
- `classify`: Image classification
- `pose`: Pose estimation
- `obb`: Oriented bounding box detection

**Usage Examples:**

```python
from ultralytics import YOLO

# Load different model sizes
model_nano = YOLO("yolo11n.pt")      # Nano model (fastest)
model_small = YOLO("yolo11s.pt")     # Small model
model_medium = YOLO("yolo11m.pt")    # Medium model
model_large = YOLO("yolo11l.pt")     # Large model
model_xlarge = YOLO("yolo11x.pt")    # Extra Large model (most accurate)

# Load task-specific models
detect_model = YOLO("yolo11n.pt")           # Detection model
segment_model = YOLO("yolo11n-seg.pt")     # Segmentation model
classify_model = YOLO("yolo11n-cls.pt")    # Classification model
pose_model = YOLO("yolo11n-pose.pt")       # Pose estimation model
obb_model = YOLO("yolo11n-obb.pt")         # Oriented bounding box model

# Load from custom path
custom_model = YOLO("/path/to/custom/model.pt")

# Initialize with specific task
model = YOLO("yolo11n.pt", task="detect")
```

### Prediction

Perform inference on images, videos, or other sources with comprehensive configuration options.

```python { .api }
def predict(self, source, stream=False, predictor=None, **kwargs) -> List[Results]:
    """
    Perform predictions on the given image source.
    
    Parameters:
    - source (str | Path | int | PIL.Image | np.ndarray | torch.Tensor | List | Tuple): 
      Source of image(s) to make predictions on
    - stream (bool): If True, treats input as continuous stream
    - predictor (BasePredictor, optional): Custom predictor instance
    - **kwargs: Additional configuration options
    
    Returns:
    List[Results]: Prediction results encapsulated in Results objects
    """

def __call__(self, source=None, stream=False, **kwargs) -> List[Results]:
    """
    Alias for predict method, enabling model instance to be callable.
    """
```

**Common Prediction Parameters:**
- `conf` (float): Confidence threshold (default: 0.25)
- `iou` (float): IoU threshold for NMS (default: 0.7)
- `imgsz` (int | tuple): Image size for inference (default: 640)
- `device` (str): Device to run on ('cpu', '0', '0,1', etc.)
- `half` (bool): Use FP16 inference (default: False)
- `max_det` (int): Maximum detections per image (default: 300)
- `vid_stride` (int): Video frame-rate stride (default: 1)
- `save` (bool): Save prediction results (default: False)
- `save_txt` (bool): Save results as txt files (default: False)
- `save_crop` (bool): Save cropped prediction boxes (default: False)
- `show` (bool): Show results (default: False)
- `verbose` (bool): Verbose output (default: True)

**Usage Examples:**

```python
# Single image prediction
results = model("image.jpg")

# Multiple images
results = model(["image1.jpg", "image2.jpg", "image3.jpg"])

# Video prediction
results = model("video.mp4")

# Webcam (device 0)
results = model(0)

# With custom parameters
results = model("image.jpg", conf=0.5, iou=0.7, imgsz=1280)

# Streaming prediction
for result in model("video.mp4", stream=True):
    # Process each frame
    result.show()
```

### Model Information

Get detailed information about the model architecture and parameters.

```python { .api }
def info(self, detailed=False, verbose=True):
    """
    Log or return model information.
    
    Parameters:
    - detailed (bool): Show detailed model information
    - verbose (bool): Control verbosity of output
    """

@property
def names(self) -> dict:
    """Get class names dictionary."""

@property  
def device(self):
    """Get model device."""

def fuse(self):
    """Fuse Conv2d and BatchNorm2d layers for optimized inference."""
```

### Model Management

Load, save, and manage model weights and configurations.

```python { .api }
def load(self, weights="yolo11n.pt"):
    """
    Load model weights from specified file.
    
    Parameters:
    - weights (str | Path): Path to weights file
    
    Returns:
    Model: Model instance with loaded weights
    """

def save(self, filename="saved_model.pt"):
    """
    Save current model state to file.
    
    Parameters:
    - filename (str | Path): Filename to save model to
    """

def reset_weights(self):
    """
    Reset model weights to initial state.
    
    Returns:
    Model: Model instance with reset weights
    """
```

**Usage Examples:**

```python
# Model information
model.info()                    # Basic info
model.info(detailed=True)       # Detailed info
print(model.names)             # Class names
print(model.device)            # Current device

# Model management
model.load("custom_weights.pt")    # Load weights
model.save("my_model.pt")          # Save model
model.reset_weights()              # Reset to initial state
model.fuse()                       # Optimize for inference
```

## Types

```python { .api }
from typing import List, Union, Optional
from pathlib import Path
from PIL import Image
import numpy as np
import torch

# Input source types
SourceType = Union[str, Path, int, Image.Image, list, tuple, np.ndarray, torch.Tensor]

# Results type
from ultralytics.engine.results import Results
```