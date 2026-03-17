# Workspace Management

Comprehensive workspace operations including project listing, creation, dataset uploads, and advanced workflows like active learning and CLIP-based image comparison. Workspaces represent team or organizational containers for computer vision projects.

## Capabilities

### Workspace Class

Main interface for workspace-level operations and project management.

```python { .api }
class Workspace:
    def __init__(self, info, api_key, default_workspace, model_format):
        """
        Initialize workspace object.
        
        Parameters:
        - info: dict - Workspace information from API
        - api_key: str - Roboflow API key
        - default_workspace: str - Default workspace identifier
        - model_format: str - Preferred model format
        """
    
    # Properties
    name: str  # Workspace name
    project_list: list  # List of projects in workspace
    members: list  # Workspace members (if available)
    url: str  # Workspace URL
```

### Project Listing and Access

Functions for discovering and accessing projects within a workspace.

```python { .api }
def list_projects(self):
    """
    List all projects in the workspace.
    
    Returns:
    list - Project information dictionaries
    """

def projects(self):
    """
    Get projects list.
    
    Returns:
    list - List of project objects
    """

def project(self, project_id):
    """
    Access a specific project by ID.
    
    Parameters:
    - project_id: str - Project identifier or name
    
    Returns:
    Project object for the specified project
    """
```

### Project Creation

Create new computer vision projects within the workspace.

```python { .api }
def create_project(self, project_name, project_type, project_license="MIT", annotation="manual"):
    """
    Create a new project in the workspace.
    
    Parameters:
    - project_name: str - Name for the new project
    - project_type: str - Type of project ("object-detection", "classification", etc.)
    - project_license: str - License for the project (default: "MIT")
    - annotation: str - Annotation method (default: "manual")
    
    Returns:
    Project object for the newly created project
    """
```

### Dataset Upload

Bulk dataset upload functionality with support for various formats and parallel processing.

```python { .api }
def upload_dataset(self, dataset_path, project_name, num_workers=10, dataset_format="NOT_USED", project_license="MIT", project_type="object-detection", batch_name=None, num_retries=0):
    """
    Upload a dataset to the workspace, creating or updating a project.
    
    Parameters:
    - dataset_path: str - Path to dataset directory
    - project_name: str - Name of the project to upload to
    - num_workers: int - Number of parallel upload workers (default: 10)
    - dataset_format: str - Deprecated parameter, kept for compatibility (default: "NOT_USED")
    - project_license: str - License for created projects (default: "MIT")
    - project_type: str - Type of projects to create (default: "object-detection")
    - batch_name: str, optional - Name for the upload batch (default: None)
    - num_retries: int - Number of retry attempts on failure (default: 0)
    
    Returns:
    dict - Upload results and project information
    """
```

### CLIP Image Comparison

Advanced image comparison using CLIP embeddings for similarity analysis.

```python { .api }
def clip_compare(self, dir="", image_ext=".png", target_image=""):
    """
    Compare images using CLIP embeddings to find similar images.
    
    Parameters:
    - dir: str - Directory containing images to compare
    - image_ext: str - Image file extension to process (default: ".png")
    - target_image: str - Target image for similarity comparison
    
    Returns:
    list[dict] - List of image similarity results with scores
    """
```

### Two-Stage Workflows

Advanced workflows combining multiple AI models for enhanced computer vision pipelines.

```python { .api }
def two_stage(self, dir, image_ext, target_image, model_type, num_images=10, upload_to_project=None):
    """
    Execute two-stage AI workflow combining models.
    
    Parameters:
    - dir: str - Directory containing images
    - image_ext: str - Image file extension
    - target_image: str - Target/reference image
    - model_type: str - Type of model for second stage
    - num_images: int - Number of images to process (default: 10)
    - upload_to_project: str, optional - Project to upload results to
    
    Returns:
    dict - Two-stage processing results
    """

def two_stage_ocr(self, dir, image_ext, target_image, model_type, num_images=10, upload_to_project=None):
    """
    Execute two-stage workflow with OCR processing.
    
    Parameters:
    - dir: str - Directory containing images
    - image_ext: str - Image file extension
    - target_image: str - Target/reference image
    - model_type: str - Type of model for processing
    - num_images: int - Number of images to process (default: 10)
    - upload_to_project: str, optional - Project to upload results to
    
    Returns:
    dict - OCR and processing results
    """
```

### Active Learning

Automated active learning workflows for improving model performance with minimal labeling effort.

```python { .api }
def active_learning(self, raw_data_location, raw_data_extension=".jpg", label_assist_class=None, upload_destination=None):
    """
    Execute active learning workflow to identify valuable images for labeling.
    
    Parameters:
    - raw_data_location: str - Directory containing unlabeled images
    - raw_data_extension: str - Image file extension (default: ".jpg")
    - label_assist_class: str, optional - Specific class to focus active learning on
    - upload_destination: str, optional - Project to upload selected images to
    
    Returns:
    dict - Active learning results and recommendations
    """
```

### Model Deployment

Deploy trained models to production environments.

```python { .api }
def deploy_model(self, model_path, model_type, model_name):
    """
    Deploy a trained model to production.
    
    Parameters:
    - model_path: str - Path to model files
    - model_type: str - Type of model being deployed
    - model_name: str - Name for the deployed model
    
    Returns:
    dict - Deployment information and endpoints
    """
```

## Usage Examples

### Basic Workspace Operations

```python
import roboflow

rf = roboflow.Roboflow(api_key="your_api_key")
workspace = rf.workspace()

# List all projects
projects = workspace.list_projects()
print(f"Found {len(projects)} projects")

# Access specific project
project = workspace.project("my-project-name")

# Create new project
new_project = workspace.create_project(
    project_name="new-detection-project",
    project_type="object-detection",
    project_license="MIT"
)
```

### Dataset Upload

```python
# Upload a dataset directory
upload_result = workspace.upload_dataset(
    dataset_path="/path/to/my/dataset",
    project_name="my-project-name",
    num_workers=5,
    project_type="object-detection",
    batch_name="My Dataset Upload"
)
```

### Advanced Workflows

```python
# CLIP image comparison
similar_images = workspace.clip_compare(
    dir="/path/to/images",
    image_ext=".jpg",
    target_image="/path/to/target.jpg"
)

# Active learning workflow
learning_results = workspace.active_learning(
    raw_data_location="/path/to/unlabeled/images",
    raw_data_extension=".png",
    label_assist_class="person",
    upload_destination="my-project"
)
```

## Configuration

Workspace behavior can be configured through:

- **API Key**: Required for authentication and access control
- **Model Format**: Default format for downloads and processing
- **Upload Settings**: Batch names, retry policies, worker counts
- **Active Learning**: Class focus, similarity thresholds

## Error Handling

Workspace operations can raise various exceptions:

```python
from roboflow.adapters.rfapi import RoboflowError, ImageUploadError

try:
    workspace.upload_dataset("/invalid/path")
except ImageUploadError as e:
    print(f"Upload failed: {e}")
except RoboflowError as e:
    print(f"API error: {e}")
```