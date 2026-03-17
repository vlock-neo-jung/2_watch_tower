# Model Inference

Comprehensive inference capabilities across different computer vision tasks, supporting both image and video inputs with various specialized model types. The inference system provides both hosted and self-hosted model execution.

## Capabilities

### Base Inference Model

The foundation class for all model inference operations.

```python { .api }
class InferenceModel:
    def __init__(self, api_key, version_id, colors=None, *args, **kwargs):
        """
        Create an InferenceModel for running predictions.
        
        Parameters:
        - api_key: str - Roboflow API key
        - version_id: str - Model version identifier in format "workspace/project/version"
        - colors: dict, optional - Custom color mapping for visualizations
        """
    
    # Properties
    id: str  # Model version identifier
    dataset_id: str  # Associated dataset identifier
    version: str  # Version number
    colors: dict  # Color mapping for classes
```

### Image Inference

Run inference on individual images with various prediction types.

```python { .api }
def predict(self, image_path, prediction_type=None, **kwargs):
    """
    Run inference on a single image.
    
    Parameters:
    - image_path: str or numpy.ndarray - Path to image file or numpy array
    - prediction_type: str, optional - Override default prediction type
    - **kwargs: Additional parameters for specific model types:
        - confidence: float - Minimum confidence threshold (0.0-1.0)
        - overlap_threshold: float - NMS IoU threshold for object detection
        - stroke_width: int - Visualization stroke width
        - labels: bool - Whether to include labels in output
        - format: str - Output format ("json", "image")
    
    Returns:
    dict - Prediction results with bounding boxes, classes, confidences
    """
```

### Video Inference

Process video files with frame-by-frame inference.

```python { .api }
def predict_video(self, video_path, fps=1, prediction_type=None, **kwargs):
    """
    Run inference on video file.
    
    Parameters:
    - video_path: str - Path to video file
    - fps: int - Frames per second to process (default: 1)
    - prediction_type: str, optional - Override default prediction type
    - **kwargs: Additional inference parameters
    
    Returns:
    dict - Job information for polling results
    """

def poll_for_video_results(self, job_id: Optional[str] = None):
    """
    Check status of video inference job.
    
    Parameters:
    - job_id: str, optional - Job ID to check (uses last job if not provided)
    
    Returns:
    dict - Job status and results if complete
    """

def poll_until_video_results(self, job_id):
    """
    Wait for video inference job to complete.
    
    Parameters:
    - job_id: str - Job ID to wait for
    
    Returns:
    dict - Final results when job completes
    """
```

### Model Download

Download trained model weights for local inference.

```python { .api }
def download(self, format="pt", location="."):
    """
    Download model weights for local inference.
    
    Parameters:
    - format: str - Model format ("pt", "onnx", "tflite", "coreml")
    - location: str - Download directory (default: current directory)
    
    Returns:
    str - Path to downloaded model file
    """
```

## Specialized Model Classes

### Object Detection

Specialized model for detecting and localizing objects in images.

```python { .api }
class ObjectDetectionModel(InferenceModel):
    """Object detection model with bounding box predictions."""
```

**Prediction Output Format:**
```python
{
    "predictions": [
        {
            "x": 320.0,           # Center X coordinate
            "y": 240.0,           # Center Y coordinate
            "width": 100.0,       # Bounding box width
            "height": 80.0,       # Bounding box height
            "confidence": 0.85,   # Prediction confidence
            "class": "person",    # Predicted class name
            "class_id": 0         # Class index
        }
    ],
    "image": {
        "width": 640,
        "height": 480
    }
}
```

### Classification

Model for image classification tasks.

```python { .api }
class ClassificationModel(InferenceModel):
    """Image classification model with class predictions."""
```

**Prediction Output Format:**
```python
{
    "predictions": [
        {
            "class": "cat",
            "confidence": 0.92
        },
        {
            "class": "dog", 
            "confidence": 0.08
        }
    ],
    "top": "cat"  # Top prediction class
}
```

### Instance Segmentation

Model for pixel-level object segmentation.

```python { .api }
class InstanceSegmentationModel(InferenceModel):
    """Instance segmentation model with masks and bounding boxes."""
```

**Prediction Output Format:**
```python
{
    "predictions": [
        {
            "x": 320.0,
            "y": 240.0,
            "width": 100.0,
            "height": 80.0,
            "confidence": 0.85,
            "class": "person",
            "class_id": 0,
            "points": [  # Polygon points for mask
                {"x": 275, "y": 200},
                {"x": 365, "y": 200},
                {"x": 365, "y": 280},
                {"x": 275, "y": 280}
            ]
        }
    ]
}
```

### Semantic Segmentation

Model for pixel-level semantic classification.

```python { .api }
class SemanticSegmentationModel(InferenceModel):
    """Semantic segmentation model with pixel-wise classifications."""
```

### Keypoint Detection

Model for detecting keypoints and pose estimation.

```python { .api }
class KeypointDetectionModel(InferenceModel):
    """Keypoint detection model for pose estimation."""
```

**Prediction Output Format:**
```python
{
    "predictions": [
        {
            "x": 320.0,
            "y": 240.0,
            "width": 100.0,
            "height": 120.0,
            "confidence": 0.90,
            "class": "person",
            "keypoints": [
                {"x": 315, "y": 210, "confidence": 0.95, "name": "nose"},
                {"x": 310, "y": 215, "confidence": 0.88, "name": "left_eye"},
                {"x": 320, "y": 215, "confidence": 0.91, "name": "right_eye"}
                # ... additional keypoints
            ]
        }
    ]
}
```

### CLIP Model

CLIP-based model for image embedding and comparison.

```python { .api }
class CLIPModel(InferenceModel):
    """CLIP model for image embeddings and similarity."""
```

### Gaze Detection

Model for detecting gaze direction and attention.

```python { .api }
class GazeModel(InferenceModel):
    """Gaze detection model for eye tracking applications."""
```

### Video Inference

Specialized model for video-based inference tasks.

```python { .api }
class VideoInferenceModel(InferenceModel):
    """Video inference model for temporal analysis."""
```

## Usage Examples

### Basic Image Inference

```python
import roboflow

# Load model from trained version
rf = roboflow.Roboflow(api_key="your_api_key")
project = rf.workspace().project("my-project")
version = project.version(1)
model = version.model

# Run inference
prediction = model.predict("path/to/image.jpg")
print(f"Found {len(prediction['predictions'])} objects")

# With custom parameters
prediction = model.predict(
    "image.jpg",
    confidence=0.7,
    overlap_threshold=0.3
)
```

### Specialized Model Usage

```python
# Object detection with specific model
from roboflow.models.object_detection import ObjectDetectionModel

model = ObjectDetectionModel(
    api_key="your_api_key",
    version_id="workspace/project/1"
)

prediction = model.predict("image.jpg", confidence=0.5)
for obj in prediction['predictions']:
    print(f"Found {obj['class']} with {obj['confidence']:.2f} confidence")

# Classification model
from roboflow.models.classification import ClassificationModel

classifier = ClassificationModel(
    api_key="your_api_key", 
    version_id="workspace/classifier-project/1"
)

result = classifier.predict("image.jpg")
print(f"Classified as: {result['top']}")
```

### Video Processing

```python
# Start video inference
job = model.predict_video("video.mp4", fps=2)
job_id = job['id']

# Poll for results
import time
while True:
    status = model.poll_for_video_results(job_id)
    if status['status'] == 'complete':
        print("Video processing complete!")
        results = status['results']
        break
    elif status['status'] == 'failed':
        print("Video processing failed")
        break
    
    time.sleep(10)  # Wait 10 seconds before checking again

# Or wait until complete
results = model.poll_until_video_results(job_id)
```

### Model Download and Local Inference

```python
# Download model weights
model_path = model.download(format="pt", location="./models")
print(f"Model downloaded to: {model_path}")

# Download in different formats
onnx_path = model.download(format="onnx", location="./models")
tflite_path = model.download(format="tflite", location="./models")
```

### Batch Processing

```python
import os

# Process multiple images
image_dir = "/path/to/images"
results = []

for filename in os.listdir(image_dir):
    if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
        image_path = os.path.join(image_dir, filename)
        prediction = model.predict(image_path)
        results.append({
            'filename': filename,
            'prediction': prediction
        })

print(f"Processed {len(results)} images")
```

## Error Handling

Inference operations can raise various exceptions:

```python
try:
    prediction = model.predict("nonexistent.jpg")
except FileNotFoundError:
    print("Image file not found")
except Exception as e:
    print(f"Inference failed: {e}")

# Handle video processing errors
try:
    job = model.predict_video("large_video.mp4")
    results = model.poll_until_video_results(job['id'])
except RuntimeError as e:
    print(f"Video processing failed: {e}")
```

## Performance Considerations

- **Batch Processing**: Process multiple images in batches for efficiency
- **Video FPS**: Lower FPS values reduce processing time and cost
- **Confidence Thresholds**: Higher thresholds reduce false positives but may miss objects
- **Image Size**: Larger images provide more detail but increase processing time
- **Local Models**: Downloaded models enable offline inference but require local compute resources