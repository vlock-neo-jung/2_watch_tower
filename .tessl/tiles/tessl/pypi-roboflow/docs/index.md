# Roboflow

The official Python SDK for working with the Roboflow computer vision platform. This package enables developers to create and manage machine learning projects, upload images and annotations, train vision models, and run inference on hosted or self-hosted models. It provides a comprehensive API for workspace, project, and version management following Roboflow's hierarchical structure.

## Package Information

- **Package Name**: roboflow
- **Language**: Python
- **Installation**: `pip install roboflow`

## Core Imports

```python
import roboflow
```

Primary entry point:

```python
from roboflow import Roboflow
```

High-level utility functions:

```python
from roboflow import (
    login,
    initialize_roboflow, 
    load_model,
    download_dataset
)
```

Specialized model imports:

```python
from roboflow import CLIPModel, GazeModel
```

## Basic Usage

```python
import roboflow

# Authenticate and create client
rf = roboflow.Roboflow(api_key="your_api_key")

# Access your workspace
workspace = rf.workspace()

# Get a project
project = workspace.project("your-project-name")

# Get a specific version
version = project.version(1)

# Download dataset
dataset = version.download("yolov8")

# Train a model
model = version.train()

# Run inference
prediction = model.predict("path/to/image.jpg")
```

## Architecture

The Roboflow SDK follows a hierarchical structure that mirrors the Roboflow platform organization:

- **Roboflow**: Main client providing authentication and workspace access
- **Workspace**: Container for projects and team management
- **Project**: Individual computer vision project with multiple versions
- **Version**: Specific dataset version with training capability
- **Model**: Trained model for running inference

The SDK supports various computer vision tasks including object detection, classification, instance segmentation, semantic segmentation, and keypoint detection, with specialized model classes for each task type.

## Capabilities

### Authentication and Initialization

Core authentication functionality for accessing the Roboflow platform, including API key validation, workspace configuration, and CLI-based login flows.

```python { .api }
class Roboflow:
    def __init__(self, api_key=None, model_format="undefined", notebook="undefined"): ...
    def workspace(self, the_workspace=None): ...
    def project(self, project_name, the_workspace=None): ...

def login(workspace=None, force=False): ...
def initialize_roboflow(the_workspace=None): ...
def check_key(api_key, model, notebook, num_retries=0): ...
```

[Authentication](./authentication.md)

### Workspace Management

Comprehensive workspace operations including project listing, creation, dataset uploads, and advanced workflows like active learning and CLIP-based image comparison.

```python { .api }
class Workspace:
    def __init__(self, info, api_key, default_workspace, model_format): ...
    def list_projects(self): ...
    def project(self, project_id): ...
    def create_project(self, project_name, project_type, project_license, annotation): ...
    def upload_dataset(self, dataset_path, project_name, num_workers=10, dataset_format="NOT_USED", project_license="MIT", project_type="object-detection", batch_name=None, num_retries=0): ...
```

[Workspace Management](./workspace-management.md)

### Project Operations

Project-level operations including version management, training, image uploads, annotation handling, and search functionality.

```python { .api }
class Project:
    def __init__(self, api_key: str, a_project: dict, model_format: Optional[str] = None): ...
    def version(self, version_number: int, local: Optional[str] = None): ...
    def versions(self): ...
    def generate_version(self, settings): ...
    def train(self, new_version_settings=None, speed=None, checkpoint=None, plot_in_notebook=False): ...
    def upload_image(self, image_path, hosted_image=False, image_id=None, split="train", batch_name=None, tag_names=[], inference=None, overwrite=False): ...
    def image(self, image_id: str): ...
    def get_batches(self): ...
    def get_batch(self, batch_id: str): ...
    def create_annotation_job(self, batch_id: str, annotator_email: str): ...
```

[Project Operations](./project-operations.md)

### Dataset Versions

Dataset version management including downloads, exports, training, and deployment of specific dataset versions.

```python { .api }
class Version:
    def __init__(self, version_data, project_info, model_format, api_key, name, local=None): ...
    def download(self, model_format=None, location=None, overwrite: bool = False): ...
    def export(self, model_format=None): ...
    def train(self, speed=None, model_type=None, checkpoint=None, plot_in_notebook=False): ...
    def deploy(self, model_type: str, model_path: str, filename: str = "weights/best.pt"): ...
```

[Dataset Versions](./dataset-versions.md)

### Model Inference

Comprehensive inference capabilities across different computer vision tasks, supporting both image and video inputs with various specialized model types.

```python { .api }
class InferenceModel:
    def __init__(self, api_key, version_id, colors=None, *args, **kwargs): ...
    def predict(self, image_path, prediction_type=None, **kwargs): ...
    def predict_video(self, video_path, fps=1, prediction_type=None, **kwargs): ...
    def download(self, format="pt", location="."): ...

# Specialized model classes
class ObjectDetectionModel(InferenceModel): ...
class ClassificationModel(InferenceModel): ...
class InstanceSegmentationModel(InferenceModel): ...
class SemanticSegmentationModel(InferenceModel): ...
class KeypointDetectionModel(InferenceModel): ...
class CLIPModel(InferenceModel): ...
class GazeModel(InferenceModel): ...
```

[Model Inference](./model-inference.md)

### High-Level Utilities

Convenient high-level functions for common workflows like loading models from URLs and downloading datasets directly without explicit workspace/project navigation.

```python { .api }
def load_model(model_url): ...
def download_dataset(dataset_url, model_format, location=None): ...
```

[High-Level Utilities](./high-level-utilities.md)

## Exception Handling

The SDK defines several exception classes for error handling:

```python { .api }
class RoboflowError(Exception): ...
class ImageUploadError(RoboflowError): ...
class AnnotationSaveError(RoboflowError): ...
class DeploymentApiError(Exception): ...
```

Most methods can raise `RoboflowError` or its subclasses on API failures, authentication issues, or invalid parameters. Always wrap API calls in try-catch blocks for production usage.