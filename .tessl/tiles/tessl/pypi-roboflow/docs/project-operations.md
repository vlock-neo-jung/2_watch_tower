# Project Operations

Project-level operations including version management, training, image uploads, annotation handling, and search functionality. Projects represent individual computer vision tasks with their datasets, annotations, and trained models.

## Capabilities

### Project Class

Main interface for project-level operations and dataset management.

```python { .api }
class Project:
    def __init__(self, api_key: str, a_project: dict, model_format: Optional[str] = None):
        """
        Initialize project object.
        
        Parameters:
        - api_key: str - Roboflow API key
        - a_project: dict - Project information from API
        - model_format: str, optional - Preferred model format
        """
```

### Version Management

Functions for managing dataset versions within a project.

```python { .api }
def get_version_information(self):
    """
    Get information about all versions in the project.
    
    Returns:
    dict - Version information including counts and metadata
    """

def list_versions(self):
    """
    List all versions in the project.
    
    Returns:
    list - Version information dictionaries
    """

def versions(self):
    """
    Get list of version objects.
    
    Returns:
    list - List of Version objects for the project
    """

def version(self, version_number: int, local: Optional[str] = None):
    """
    Access a specific version by number.
    
    Parameters:
    - version_number: int - Version number to access
    - local: str, optional - Local path for version data
    
    Returns:
    Version object for the specified version
    """

def generate_version(self, settings):
    """
    Create a new version with specified settings.
    
    Parameters:
    - settings: dict - Version generation settings including augmentation options
    
    Returns:
    Version object for the newly created version
    """
```

### Model Training

Train machine learning models on project datasets.

```python { .api }
def train(self, new_version_settings=None, speed=None, checkpoint=None, plot_in_notebook=False):
    """
    Train a model on the project's latest version or create a new version with settings.
    
    Parameters:
    - new_version_settings: dict, optional - Settings for creating a new version before training
    - speed: str, optional - Training speed ("fast" for free tier, "accurate" for paid tier)
    - checkpoint: str, optional - Checkpoint to resume training from
    - plot_in_notebook: bool - Whether to display training plots in notebook (default: False)
    
    Returns:
    Training job information and status
    """
```

### Image Upload

Upload images to the project with optional annotations.

```python { .api }
def check_valid_image(self, image_path: str) -> bool:
    """
    Validate if an image file is in an accepted format.
    
    Parameters:
    - image_path: str - Path to image file
    
    Returns:
    bool - True if image format is valid, False otherwise
    """

def upload_image(self, image_path, hosted_image=False, image_id=None, split="train", batch_name=None, tag_names=[], inference=None, overwrite=False):
    """
    Upload an image to the project.
    
    Parameters:
    - image_path: str - Path to image file
    - hosted_image: bool - Whether image is hosted externally (default: False)
    - image_id: str, optional - Custom ID for the image
    - split: str - Dataset split ("train", "valid", "test")
    - batch_name: str, optional - Batch name for organization
    - tag_names: list[str] - Tags to apply to the image
    - inference: dict, optional - Inference results to attach
    - overwrite: bool - Whether to overwrite existing image (default: False)
    
    Returns:
    dict - Upload response with image information
    """

def upload(self, image_path, annotation_path=None, hosted_image=False, image_id=None, is_prediction=False, prediction_confidence=None, prediction_classes=None, bbox=None, polygon=None, keypoints=None, is_duplicate=False, batch_name=None, tag_names=[], overwrite=False):
    """
    Upload image with annotation data.
    
    Parameters:
    - image_path: str - Path to image file
    - annotation_path: str, optional - Path to annotation file
    - hosted_image: bool - Whether image is hosted externally
    - image_id: str, optional - Custom ID for the image
    - is_prediction: bool - Whether annotation is from prediction
    - prediction_confidence: float, optional - Confidence score for predictions
    - prediction_classes: list, optional - Predicted class names
    - bbox: list, optional - Bounding box coordinates
    - polygon: list, optional - Polygon coordinates for segmentation
    - keypoints: list, optional - Keypoint coordinates
    - is_duplicate: bool - Whether image is a duplicate
    - batch_name: str, optional - Batch name for organization
    - tag_names: list[str] - Tags to apply to the image
    - overwrite: bool - Whether to overwrite existing data
    
    Returns:
    dict - Upload response with image and annotation information
    """
```

### Annotation Management

Manage annotations separately from image uploads.

```python { .api }
def save_annotation(self, image_id, annotation_path=None, is_prediction=False, prediction_confidence=None, prediction_classes=None, image_width=None, image_height=None, overwrite=False):
    """
    Save annotation for an existing image.
    
    Parameters:
    - image_id: str - ID of the target image
    - annotation_path: str, optional - Path to annotation file
    - is_prediction: bool - Whether annotation is from prediction
    - prediction_confidence: float, optional - Confidence score
    - prediction_classes: list, optional - Predicted class names
    - image_width: int, optional - Image width for coordinate normalization
    - image_height: int, optional - Image height for coordinate normalization
    - overwrite: bool - Whether to overwrite existing annotation
    
    Returns:
    dict - Annotation save response
    """

def single_upload(self, image_path, annotation_path=None, hosted_image=False, image_id=None, split="train", is_prediction=False, prediction_confidence=None, prediction_classes=None, batch_name=None, tag_names=[], inference=None, overwrite=False):
    """
    Upload single image with annotation in one operation.
    
    Parameters:
    - image_path: str - Path to image file
    - annotation_path: str, optional - Path to annotation file
    - hosted_image: bool - Whether image is hosted externally
    - image_id: str, optional - Custom ID for the image
    - split: str - Dataset split ("train", "valid", "test")
    - is_prediction: bool - Whether annotation is from prediction
    - prediction_confidence: float, optional - Confidence score
    - prediction_classes: list, optional - Predicted class names
    - batch_name: str, optional - Batch name for organization
    - tag_names: list[str] - Tags to apply to the image
    - inference: dict, optional - Inference results to attach
    - overwrite: bool - Whether to overwrite existing data
    
    Returns:
    dict - Combined upload response
    """
```

### Image Search

Search and filter images within the project.

```python { .api }
def search(self, query="", stroke_width=1, limit=100, offset=0, sort_by="created", sort_order="desc", fields=["id", "created", "name", "labels"]):
    """
    Search images in the project with filtering options.
    
    Parameters:
    - query: str - Search query string
    - stroke_width: int - Visualization stroke width
    - limit: int - Maximum number of results (default: 100)
    - offset: int - Result offset for pagination (default: 0)
    - sort_by: str - Field to sort by ("created", "name", etc.)
    - sort_order: str - Sort order ("asc", "desc")
    - fields: list[str] - Fields to return in results
    
    Returns:
    dict - Search results with image metadata
    """

def search_all(self, query="", stroke_width=1, sort_by="created", sort_order="desc", fields=["id", "created", "name", "labels"]):
    """
    Search all images in the project without pagination limits.
    
    Parameters:
    - query: str - Search query string
    - stroke_width: int - Visualization stroke width
    - sort_by: str - Field to sort by
    - sort_order: str - Sort order ("asc", "desc")
    - fields: list[str] - Fields to return in results
    
    Returns:
    dict - Complete search results
    """
```

## Usage Examples

### Basic Project Operations

```python
import roboflow

rf = roboflow.Roboflow(api_key="your_api_key")
project = rf.workspace().project("my-project")

# Get project versions
versions = project.versions()
print(f"Project has {len(versions)} versions")

# Access specific version
version = project.version(1)

# Create new version with augmentations
new_version = project.generate_version({
    "preprocessing": {"auto-orient": True, "resize": [416, 416]},
    "augmentation": {"flip": "horizontal", "rotate": 15}
})
```

### Training Models

```python
# Train with default settings
model = project.train()

# Train with custom settings
model = project.train(
    speed="medium",
    model_type="yolov8n",
    epochs=100,
    batch_size=16,
    plot_in_notebook=True
)
```

### Image and Annotation Upload

```python
# Simple image upload
response = project.upload_image(
    image_path="/path/to/image.jpg",
    split="train",
    batch_name="My Upload Batch"
)

# Upload with annotation
response = project.upload(
    image_path="/path/to/image.jpg",
    annotation_path="/path/to/annotation.txt",
    batch_name="Annotated Upload"
)

# Bulk upload with annotations
import os
for image_file in os.listdir("/path/to/images"):
    if image_file.endswith('.jpg'):
        image_path = f"/path/to/images/{image_file}"
        annotation_path = f"/path/to/labels/{image_file.replace('.jpg', '.txt')}"
        
        project.single_upload(
            image_path=image_path,
            annotation_path=annotation_path,
            batch_name="Bulk Upload"
        )
```

### Image Management

Retrieve and manage individual images and their details.

```python { .api }
def image(self, image_id: str):
    """
    Get detailed information about a specific image.
    
    Parameters:
    - image_id: str - Unique identifier for the image
    
    Returns:
    dict - Image details including metadata, annotations, and URLs
    """
```

### Batch Management

Manage upload batches for organizing and tracking groups of images.

```python { .api }
def get_batches(self):
    """
    Get all batches associated with the project.
    
    Returns:
    dict - List of batches with their metadata and status
    """

def get_batch(self, batch_id: str):
    """
    Get detailed information about a specific batch.
    
    Parameters:
    - batch_id: str - Unique identifier for the batch
    
    Returns:
    dict - Batch details including images, status, and metadata
    """
```

### Annotation Jobs

Create and manage annotation jobs for labeling workflows.

```python { .api }
def create_annotation_job(self, batch_id: str, annotator_email: str):
    """
    Create an annotation job for a specific batch.
    
    Parameters:
    - batch_id: str - Batch to be annotated
    - annotator_email: str - Email of the annotator
    
    Returns:
    dict - Annotation job details and assignment information
    """
```

### Image Search and Management

```python
# Get specific image details
image_info = project.image("image_12345")
print(f"Image size: {image_info['width']}x{image_info['height']}")

# Get all batches
batches = project.get_batches()
for batch in batches['batches']:
    print(f"Batch: {batch['name']} - {batch['image_count']} images")

# Search for images with specific labels
results = project.search(
    query="person car",
    limit=50,
    sort_by="created",
    sort_order="desc"
)

# Get all images for analysis
all_images = project.search_all(
    fields=["id", "name", "labels", "created", "width", "height"]
)
```

## Supported Image Formats

The project accepts the following image formats:
- JPEG (`.jpg`, `.jpeg`)
- PNG (`.png`)
- BMP (`.bmp`)
- WebP (`.webp`)
- TIFF (`.tiff`, `.tif`)
- AVIF (`.avif`)
- HEIC (`.heic`)

## Error Handling

Project operations can raise several types of exceptions:

```python
from roboflow.adapters.rfapi import ImageUploadError, AnnotationSaveError

try:
    project.upload_image("/invalid/path.jpg")
except ImageUploadError as e:
    print(f"Image upload failed: {e}")

try:
    project.save_annotation("invalid_id", "/path/to/annotation.txt")
except AnnotationSaveError as e:
    print(f"Annotation save failed: {e}")
```