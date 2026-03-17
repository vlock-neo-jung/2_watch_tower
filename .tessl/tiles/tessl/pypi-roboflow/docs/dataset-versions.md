# Dataset Versions

Dataset version management including downloads, exports, training, and deployment of specific dataset versions. Versions represent snapshots of a dataset with specific preprocessing and augmentation settings applied.

## Capabilities

### Version Class

Interface for managing individual dataset versions and their associated operations.

```python { .api }
class Version:
    def __init__(self, version_data, project_info, model_format, api_key, name, local=None):
        """
        Initialize version object.
        
        Parameters:
        - version_data: dict - Version information from API
        - project_info: dict - Parent project information
        - model_format: str - Preferred model format
        - api_key: str - Roboflow API key
        - name: str - Version name/identifier
        - local: str, optional - Local path for version data
        """
    
    # Properties
    model: InferenceModel  # Associated trained model for inference
```

### Dataset Download

Download dataset versions in various formats for local development and training.

```python { .api }
def download(self, model_format=None, location=None, overwrite: bool = False):
    """
    Download the dataset version in specified format.
    
    Parameters:
    - model_format: str, optional - Format to download ("yolov8", "yolov5", "pascal_voc", "coco", "tfrecord", "createml", "darknet", "pytorch", "tensorflow", "clip")
    - location: str, optional - Download directory path (default: current directory)
    - overwrite: bool - Whether to overwrite existing files (default: False)
    
    Returns:
    Dataset - Dataset object with location information
    """
```

### Dataset Export

Export dataset versions to different formats without downloading.

```python { .api }
def export(self, model_format=None):
    """
    Export dataset in specified format.
    
    Parameters:
    - model_format: str, optional - Export format ("yolov8", "yolov5", "pascal_voc", "coco", etc.)
    
    Returns:
    bool or None - Export success status
    """
```

### Model Training

Train machine learning models on specific dataset versions.

```python { .api }
def train(self, speed=None, model_type=None, checkpoint=None, plot_in_notebook=False):
    """
    Train a model on this dataset version.
    
    Parameters:
    - speed: str, optional - Training speed ("fast", "medium", "slow")
    - model_type: str, optional - Model architecture ("yolov8n", "yolov8s", "yolov8m", "yolov8l", "yolov8x")
    - checkpoint: str, optional - Checkpoint to resume training from
    - plot_in_notebook: bool - Whether to display training plots in notebook (default: False)
    
    Returns:
    InferenceModel - Trained model ready for inference
    """
```

### Model Deployment

Deploy trained models to production environments.

```python { .api }
def deploy(self, model_type: str, model_path: str, filename: str = "weights/best.pt"):
    """
    Deploy a trained model to production.
    
    Parameters:
    - model_type: str - Type of model being deployed
    - model_path: str - Path to model files
    - filename: str - Model filename within the path (default: "weights/best.pt")
    
    Returns:
    None - Deployment is asynchronous
    """
```

## Dataset Object

The download operation returns a Dataset object with location information.

```python { .api }
class Dataset:
    location: str  # Path where dataset was downloaded
```

## Usage Examples

### Dataset Download

```python
import roboflow

rf = roboflow.Roboflow(api_key="your_api_key")
project = rf.workspace().project("my-project")
version = project.version(1)

# Download in YOLO format
dataset = version.download("yolov8")
print(f"Dataset downloaded to: {dataset.location}")

# Download to specific location
dataset = version.download(
    model_format="pascal_voc",
    location="/path/to/my/datasets",
    overwrite=True
)

# Download in COCO format
dataset = version.download("coco")
```

### Model Training

```python
# Train with default settings
model = version.train()

# Train with specific configuration
model = version.train(
    speed="medium",
    model_type="yolov8s",
    plot_in_notebook=True
)

# Use trained model for inference
prediction = model.predict("/path/to/test/image.jpg")
```

### Dataset Export

```python
# Export without downloading
export_success = version.export("yolov8")

if export_success:
    print("Export completed successfully")
```

### Model Deployment

```python
# Deploy a trained model
version.deploy(
    model_type="yolov8",
    model_path="/path/to/trained/model",
    filename="best.pt"
)
```

## Supported Formats

### Download/Export Formats

The version supports multiple dataset formats:

- **YOLO Formats**: `"yolov8"`, `"yolov5"`, `"yolov7"`, `"darknet"`
- **Standard Formats**: `"pascal_voc"`, `"coco"`, `"tfrecord"`
- **Framework Formats**: `"pytorch"`, `"tensorflow"`
- **Mobile Formats**: `"createml"` (for iOS)
- **Specialized**: `"clip"` (for CLIP embeddings)

### Model Types

Training supports various YOLO model architectures:

- **YOLOv8**: `"yolov8n"`, `"yolov8s"`, `"yolov8m"`, `"yolov8l"`, `"yolov8x"`
- **YOLOv5**: `"yolov5n"`, `"yolov5s"`, `"yolov5m"`, `"yolov5l"`, `"yolov5x"`
- **Custom**: User-provided model configurations

### Training Speeds

- **"fast"**: Quick training with fewer epochs
- **"medium"**: Balanced training time and accuracy
- **"slow"**: Comprehensive training for maximum accuracy

## Version Information

Dataset versions contain metadata about:

- **Image Count**: Total images in train/valid/test splits
- **Class Information**: Number and names of labeled classes
- **Preprocessing**: Applied image preprocessing steps
- **Augmentation**: Data augmentation techniques used
- **Creation Date**: When the version was generated
- **Parent Version**: Source version if derived from another

## Error Handling

Version operations can encounter various errors:

```python
try:
    dataset = version.download("invalid_format")
except ValueError as e:
    print(f"Invalid format: {e}")

try:
    model = version.train(model_type="invalid_model")
except RuntimeError as e:
    print(f"Training failed: {e}")
```

## Integration with Inference

Once training is complete, models are automatically available for inference:

```python
# Train model
model = version.train()

# Immediate inference
prediction = model.predict("image.jpg")

# Or access model later via version.model property
model = version.model
prediction = model.predict("another_image.jpg")
```