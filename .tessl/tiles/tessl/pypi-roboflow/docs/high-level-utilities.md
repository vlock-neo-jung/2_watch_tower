# High-Level Utilities

Convenient high-level functions for common workflows like loading models from URLs and downloading datasets directly without explicit workspace/project navigation. These utilities simplify common operations and provide shortcuts for frequent tasks.

## Capabilities

### Model Loading

Load models directly from Roboflow URLs without manually navigating the workspace/project hierarchy.

```python { .api }
def load_model(model_url):
    """
    High-level function to load Roboflow models from URLs.
    
    Parameters:
    - model_url: str - Model URL from app.roboflow.com or universe.roboflow.com
                      Format: "https://app.roboflow.com/workspace/project/version"
                      or: "https://universe.roboflow.com/workspace/project/version"
    
    Returns:
    InferenceModel - Model object ready for inference
    
    Raises:
    ValueError - If URL is not from a supported domain
    """
```

### Dataset Download

Download datasets directly from URLs without workspace/project navigation.

```python { .api }
def download_dataset(dataset_url, model_format, location=None):
    """
    High-level function to download data from Roboflow URLs.
    
    Parameters:
    - dataset_url: str - Dataset URL from app.roboflow.com or universe.roboflow.com
                        Format: "https://app.roboflow.com/workspace/project/version"
                        or: "https://universe.roboflow.com/workspace/project/version"
    - model_format: str - Format to download dataset in ("yolov8", "yolov5", "pascal_voc", "coco", etc.)
    - location: str, optional - Directory to download to (default: current directory)
    
    Returns:
    Dataset - Dataset object with location information
    
    Raises:
    ValueError - If URL is not from a supported domain
    """
```

## Usage Examples

### Loading Models from URLs

```python
import roboflow

# Load model directly from app.roboflow.com URL
model = roboflow.load_model("https://app.roboflow.com/my-workspace/my-project/1")

# Run inference immediately
prediction = model.predict("path/to/image.jpg")
print(prediction)

# Load from Universe (public models)
public_model = roboflow.load_model("https://universe.roboflow.com/roboflow/microsoft-coco/1")
prediction = public_model.predict("test_image.jpg")
```

### Downloading Datasets from URLs

```python
import roboflow

# Download dataset in YOLO format
dataset = roboflow.download_dataset(
    dataset_url="https://app.roboflow.com/my-workspace/my-project/2",
    model_format="yolov8",
    location="./datasets"
)

print(f"Dataset downloaded to: {dataset.location}")

# Download public dataset from Universe
public_dataset = roboflow.download_dataset(
    dataset_url="https://universe.roboflow.com/roboflow/microsoft-coco/1", 
    model_format="coco",
    location="./public_datasets"
)

# Download in different formats
pascal_dataset = roboflow.download_dataset(
    dataset_url="https://app.roboflow.com/my-workspace/my-project/1",
    model_format="pascal_voc"
)
```

### Combining with Training Workflows

```python
import roboflow

# Download dataset and train model in one workflow
dataset = roboflow.download_dataset(
    dataset_url="https://app.roboflow.com/my-workspace/my-project/1",
    model_format="yolov8",
    location="./training_data"
)

# Use the dataset location for training
# (Note: This requires additional YOLOv8 training code)
print(f"Training data ready at: {dataset.location}")

# Or load pre-trained model for inference
model = roboflow.load_model("https://app.roboflow.com/my-workspace/my-project/1")
prediction = model.predict("new_image.jpg")
```

### URL Format Validation

```python
import roboflow

# Valid URLs - these will work
valid_urls = [
    "https://app.roboflow.com/workspace/project/1",
    "https://universe.roboflow.com/user/project/2",
    "https://app.roboflow.com/my-team/detection-project/3"
]

# Invalid URLs - these will raise ValueError
invalid_urls = [
    "https://example.com/project/1",           # Wrong domain
    "https://app.roboflow.com/project",        # Missing version
    "https://roboflow.com/workspace/project/1" # Wrong subdomain
]

try:
    model = roboflow.load_model("https://example.com/project/1")
except ValueError as e:
    print(f"Invalid URL: {e}")
```

### Batch Operations

```python
import roboflow

# Download multiple datasets
dataset_urls = [
    "https://app.roboflow.com/workspace/cars/1",
    "https://app.roboflow.com/workspace/people/2", 
    "https://app.roboflow.com/workspace/animals/1"
]

datasets = []
for url in dataset_urls:
    dataset = roboflow.download_dataset(
        dataset_url=url,
        model_format="yolov8",
        location=f"./datasets/{url.split('/')[-2]}"  # Use project name as folder
    )
    datasets.append(dataset)

print(f"Downloaded {len(datasets)} datasets")

# Load multiple models for ensemble inference
model_urls = [
    "https://app.roboflow.com/workspace/detector-v1/3",
    "https://app.roboflow.com/workspace/detector-v2/1"
]

models = []
for url in model_urls:
    model = roboflow.load_model(url)
    models.append(model)

# Run ensemble predictions
image_path = "test_image.jpg"
predictions = []
for model in models:
    prediction = model.predict(image_path)
    predictions.append(prediction)

print(f"Got {len(predictions)} predictions from ensemble")
```

## URL Parsing

The utilities automatically parse URLs to extract workspace, project, and version information:

- **URL Structure**: `https://{subdomain}.roboflow.com/{workspace}/{project}/{version}`
- **Supported Subdomains**: `app` (private projects), `universe` (public projects)
- **Workspace**: Team or individual workspace identifier
- **Project**: Project name within the workspace
- **Version**: Dataset/model version number

## Authentication

These utilities use the same authentication as the main SDK:

```python
import roboflow

# Set API key for private models/datasets
roboflow.Roboflow(api_key="your_api_key")

# Now utilities will use the authenticated session
model = roboflow.load_model("https://app.roboflow.com/private-workspace/project/1")

# Public Universe models don't require authentication
public_model = roboflow.load_model("https://universe.roboflow.com/roboflow/coco/1")
```

## Error Handling

The utilities provide clear error messages for common issues:

```python
import roboflow

try:
    # Invalid domain
    model = roboflow.load_model("https://example.com/workspace/project/1")
except ValueError as e:
    print(f"URL error: {e}")

try:
    # Invalid format
    dataset = roboflow.download_dataset(
        "https://app.roboflow.com/workspace/project/1",
        "invalid_format"
    )
except ValueError as e:
    print(f"Format error: {e}")

try:
    # Network/authentication error
    model = roboflow.load_model("https://app.roboflow.com/private/project/1")
except RuntimeError as e:
    print(f"Access error: {e}")
```

## Performance Tips

- **URL Validation**: URLs are validated before making API calls to catch errors early
- **Caching**: Consider caching downloaded models and datasets for repeated use
- **Authentication**: Set up authentication once to avoid repeated API key prompts
- **Location Management**: Use descriptive location paths to organize downloaded content

## Integration with Main SDK

These utilities work seamlessly with the main SDK:

```python
import roboflow

# Initialize SDK
rf = roboflow.Roboflow(api_key="your_api_key")

# Use utilities with authenticated session
model = roboflow.load_model("https://app.roboflow.com/workspace/project/1")

# Or access the same model through SDK
workspace = rf.workspace("workspace")
project = workspace.project("project")
version = project.version(1)
same_model = version.model

# Both models are equivalent
assert model.id == same_model.id
```