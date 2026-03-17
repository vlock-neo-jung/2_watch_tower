# Ultralytics YOLO

Ultralytics YOLO is a comprehensive computer vision library implementing state-of-the-art YOLO (You Only Look Once) models for object detection, multi-object tracking, instance segmentation, pose estimation, and image classification. It provides a unified API for training and inference with various YOLO model versions (YOLOv8, YOLOv9, YOLOv10, YOLO11), supports multiple export formats, and includes advanced features like model pruning, quantization, and hyperparameter optimization.

## Package Information

- **Package Name**: ultralytics
- **Language**: Python
- **Installation**: `pip install ultralytics`

## Core Imports

```python
from ultralytics import YOLO
```

For specialized models:

```python
from ultralytics import YOLO, YOLOWorld, SAM, FastSAM, RTDETR, NAS
```

For utilities:

```python
from ultralytics import checks, download, settings
```

## Basic Usage

```python
from ultralytics import YOLO
from PIL import Image

# Load a model
model = YOLO("yolo11n.pt")  # load a pretrained model

# Predict on an image
results = model("https://ultralytics.com/images/bus.jpg")  # predict on an image

# Display the results
for r in results:
    im_array = r.plot()  # plot a BGR numpy array of predictions
    im = Image.fromarray(im_array[..., ::-1])  # RGB PIL image
    im.show()  # show image
    
# Train the model
model.train(data="coco8.yaml", epochs=3)  # train the model

# Validate the model
metrics = model.val()  # evaluate model performance on the validation set

# Export the model
model.export(format="onnx")  # export the model to ONNX format
```

## Architecture

The Ultralytics package is organized around several key components:

- **Model Classes**: Core model implementations (YOLO, YOLOWorld, SAM, FastSAM, RTDETR, NAS)
- **Engine**: Base model functionality, results handling, and training infrastructure
- **Utils**: Comprehensive utilities for downloads, plotting, system checks, and configuration
- **Data**: Dataset loaders, augmentations, and preprocessing pipelines
- **NN**: Neural network architectures and model definitions
- **Trackers**: Multi-object tracking algorithms (BOTSORT, BYTETracker)
- **Solutions**: Pre-built computer vision solutions and analytics tools

## Capabilities

### YOLO Models

The primary YOLO model class supporting multiple computer vision tasks including object detection, instance segmentation, image classification, pose estimation, and oriented bounding box detection.

```python { .api }
class YOLO:
    def __init__(self, model="yolo11n.pt", task=None, verbose=False): ...
    def predict(self, source, **kwargs) -> List[Results]: ...
    def train(self, **kwargs) -> dict: ...
    def val(self, **kwargs) -> dict: ...
    def export(self, **kwargs) -> str: ...
```

[YOLO Models](./yolo-models.md)

### Specialized Models

Specialized model implementations including YOLOWorld for open-vocabulary detection, SAM for promptable segmentation, FastSAM for efficient segmentation, RTDETR for transformer-based detection, and NAS for neural architecture search.

```python { .api }
class YOLOWorld:
    def set_classes(self, classes: List[str]): ...

class SAM:
    def predict(self, source, bboxes=None, points=None, labels=None, **kwargs): ...
    
class FastSAM:
    def predict(self, source, **kwargs): ...
```

[Specialized Models](./specialized-models.md)

### Model Training and Validation

Comprehensive training and validation capabilities with support for custom datasets, hyperparameter tuning, distributed training, and model optimization techniques.

```python { .api }
def train(self, data=None, epochs=100, **kwargs) -> dict: ...
def val(self, data=None, **kwargs) -> dict: ...  
def tune(self, data=None, **kwargs) -> dict: ...
```

[Training and Validation](./training-validation.md)

### Model Export and Deployment

Export trained models to various formats for deployment including ONNX, TensorRT, CoreML, TensorFlow, OpenVINO, and mobile formats with optimization options.

```python { .api }
def export(self, format="torchscript", **kwargs) -> str: ...
def benchmark(self, **kwargs) -> dict: ...
```

[Export and Deployment](./export-deployment.md)

### Object Tracking

Multi-object tracking capabilities with BOTSORT and BYTETracker algorithms for tracking objects across video frames.

```python { .api }
def track(self, source, **kwargs) -> List[Results]: ...
```

[Object Tracking](./tracking.md)

### Utilities and Configuration

Comprehensive utility functions for system checks, file downloads, plotting results, configuration management, and dataset operations.

```python { .api }
def checks(**kwargs): ...
def download(url: str, **kwargs): ...
settings: SettingsManager
```

[Utilities](./utilities.md)

### Results and Visualization

Rich result objects containing detection outputs with built-in visualization, annotation, and export capabilities.

```python { .api }
class Results:
    def plot(self, **kwargs) -> np.ndarray: ...
    def save(self, filename: str): ...
    def show(self): ...
```

[Results and Visualization](./results-visualization.md)