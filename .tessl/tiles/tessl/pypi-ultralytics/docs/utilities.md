# Utilities and Configuration

Comprehensive utility functions for system checks, file downloads, configuration management, and dataset operations that support the core Ultralytics functionality.

## Capabilities

### System Checks

Validate system requirements, environment setup, and package dependencies.

```python { .api }
def checks(**kwargs):
    """
    Perform comprehensive system and environment checks.
    
    Parameters:
    - verbose (bool): Enable verbose output (default: True)
    - requirements (str): Path to requirements file to check
    - exclude (list): List of requirements to exclude from checks
    
    Returns:
    bool: True if all checks pass
    """
```

**Usage Examples:**

```python
from ultralytics import checks

# Basic system checks
checks()

# Verbose system checks
checks(verbose=True)

# Check specific requirements file
checks(requirements="requirements.txt")

# Check with exclusions
checks(exclude=["opencv-python", "pillow"])
```

### File Downloads

Download models, datasets, and other assets with progress tracking and caching.

```python { .api }
def download(url, dir=None, unzip=True, delete=False, curl=False, threads=1, retry=3, **kwargs):
    """
    Download files from URL with optional extraction and caching.
    
    Parameters:
    - url (str): URL to download from
    - dir (str | Path): Directory to save file (default: current directory)
    - unzip (bool): Extract ZIP files after download (default: True)
    - delete (bool): Delete ZIP file after extraction (default: False)
    - curl (bool): Use curl instead of urllib (default: False)
    - threads (int): Number of download threads (default: 1)
    - retry (int): Number of retry attempts (default: 3)
    - **kwargs: Additional arguments
    
    Returns:
    Path: Path to downloaded file
    """
```

**Usage Examples:**

```python
from ultralytics import download

# Download model file
model_path = download("https://github.com/ultralytics/assets/releases/download/v0.0.0/yolo11n.pt")

# Download and extract dataset
dataset_path = download(
    "https://github.com/ultralytics/yolov5/releases/download/v1.0/coco128.zip",
    dir="datasets",
    unzip=True,
    delete=True
)

# Download with custom options
file_path = download(
    "https://example.com/large_file.zip",
    dir="downloads", 
    curl=True,
    threads=4,
    retry=5
)
```

### Settings Management

Global configuration management for Ultralytics package behavior.

```python { .api }
settings: SettingsManager

class SettingsManager:
    def __init__(self):
        self.yaml_file: Path         # Path to settings YAML file
        self._settings: dict         # Internal settings dictionary
    
    def __getitem__(self, key: str) -> Any: ...
    def __setitem__(self, key: str, value: Any): ...
    def update(self, *args, **kwargs): ...
    def reset(self): ...
    def save(self): ...
    def load(self): ...
```

**Available Settings:**
- `datasets_dir`: Directory for datasets (default: './datasets')
- `weights_dir`: Directory for model weights (default: './weights')
- `runs_dir`: Directory for training runs (default: './runs')
- `uuid`: Unique user identifier
- `sync`: Enable analytics and crash reporting
- `api_key`: Ultralytics Hub API key
- `clearml`: Enable ClearML logging
- `comet`: Enable Comet logging
- `dvc`: Enable DVC logging
- `hub`: Enable Ultralytics Hub features
- `mlflow`: Enable MLflow logging
- `neptune`: Enable Neptune logging
- `raytune`: Enable Ray Tune hyperparameter tuning
- `tensorboard`: Enable TensorBoard logging
- `wandb`: Enable Weights & Biases logging

**Usage Examples:**

```python
from ultralytics import settings

# View current settings
print(settings)

# Get specific setting
datasets_dir = settings['datasets_dir']
print(f"Datasets directory: {datasets_dir}")

# Update settings
settings.update({'datasets_dir': '/data/datasets'})
settings['weights_dir'] = '/models/weights'

# Reset to defaults
settings.reset()

# Save settings
settings.save()

# Load settings from file
settings.load()
```

### Asset Management

Access to default assets and sample data for testing and examples.

```python { .api }
ASSETS: Path  # Path to default assets directory

# Default assets include:
# - Sample images (bus.jpg, zidane.jpg, etc.)
# - Sample videos 
# - Configuration files
# - Model architectures
```

**Usage Examples:**

```python
from ultralytics import ASSETS

# Use default sample image
sample_image = ASSETS / "bus.jpg"
results = model(sample_image)

# List available assets
print(list(ASSETS.glob("*")))

# Use in predictions when no source specified
results = model()  # Automatically uses ASSETS
```

### Configuration Utilities

Load and manage YAML configuration files for datasets, models, and training.

```python { .api }
def yaml_load(file):
    """
    Load YAML file safely.
    
    Parameters:
    - file (str | Path): Path to YAML file
    
    Returns:
    dict: Loaded YAML content
    """

def yaml_save(file, data):
    """
    Save data to YAML file.
    
    Parameters:
    - file (str | Path): Path to save YAML file
    - data (dict): Data to save
    """

def get_cfg(cfg=DEFAULT_CFG_DICT, overrides=None):
    """
    Load and merge configuration from various sources.
    
    Parameters:
    - cfg (str | Path | dict): Base configuration
    - overrides (dict): Configuration overrides
    
    Returns:
    dict: Merged configuration
    """
```

**Usage Examples:**

```python
from ultralytics.utils import yaml_load, yaml_save, get_cfg

# Load configuration file
config = yaml_load("config.yaml")

# Save configuration
yaml_save("new_config.yaml", {"epochs": 100, "batch_size": 16})

# Get merged configuration
cfg = get_cfg("yolo11n.yaml", {"epochs": 200, "imgsz": 1280})
```

### Environment Detection

Detect the current runtime environment and available resources.

```python { .api }
def is_colab() -> bool:
    """Check if running in Google Colab."""

def is_kaggle() -> bool:
    """Check if running in Kaggle environment."""

def is_jupyter() -> bool:
    """Check if running in Jupyter notebook."""

def is_docker() -> bool:
    """Check if running in Docker container."""

def is_pip_package(name: str) -> bool:
    """Check if package is installed via pip."""

def is_github_actions_ci() -> bool:
    """Check if running in GitHub Actions CI."""
```

**Usage Examples:**

```python
from ultralytics.utils import is_colab, is_kaggle, is_jupyter, is_docker

# Adapt behavior based on environment
if is_colab():
    print("Running in Google Colab")
    # Use Colab-specific settings
elif is_kaggle():
    print("Running in Kaggle")
    # Use Kaggle-specific settings
elif is_jupyter():
    print("Running in Jupyter notebook")
    # Enable inline plotting
elif is_docker():
    print("Running in Docker container")
    # Use containerized settings
```

### System Information

Get detailed information about the system, hardware, and software environment.

```python { .api }
def get_git_info() -> dict:
    """Get Git repository information."""

def get_cpu_info() -> dict:
    """Get CPU information."""

def get_gpu_info() -> dict:
    """Get GPU information."""

def get_environment_info() -> dict:
    """Get comprehensive environment information."""

def print_environment_info():
    """Print formatted environment information."""
```

**Usage Examples:**

```python
from ultralytics.utils import get_environment_info, print_environment_info

# Get environment info as dictionary
env_info = get_environment_info()
print(f"Python version: {env_info['python']}")
print(f"PyTorch version: {env_info['torch']}")

# Print formatted environment information
print_environment_info()
```

### Path and File Utilities

Utilities for working with file paths, directories, and file operations.

```python { .api }
def increment_path(path, exist_ok=False, sep='', mkdir=False):
    """
    Increment file or directory path if it exists.
    
    Parameters:
    - path (str | Path): Path to increment
    - exist_ok (bool): If True, return path as-is if it exists
    - sep (str): Separator for incremented number
    - mkdir (bool): Create directory if it doesn't exist
    
    Returns:
    Path: Incremented path
    """

def make_dirs(dir):
    """Create directories recursively."""

def clean_str(s):
    """Clean string for use in filenames."""

def file_size(path):
    """Get file size in MB."""
```

**Usage Examples:**

```python
from ultralytics.utils import increment_path, make_dirs, clean_str

# Increment path to avoid overwriting
save_dir = increment_path("runs/train/exp", mkdir=True)  # runs/train/exp2
print(f"Saving to: {save_dir}")

# Create directories
make_dirs("data/images/train")

# Clean string for filename
clean_name = clean_str("My Model (v1.0)")  # "My_Model_v1_0_"
```

### Logging and Debugging

Enhanced logging capabilities with context managers and debugging utilities.

```python { .api }
LOGGER: logging.Logger  # Global logger instance

def set_logging(name=None, verbose=True):
    """Configure logging settings."""

class TryExcept:
    """Context manager for graceful exception handling."""
    def __init__(self, msg=''):
        self.msg = msg
    
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, value, traceback):
        if exc_type is not None:
            LOGGER.warning(f'{self.msg}: {exc_type.__name__}: {value}')
        return True
```

**Usage Examples:**

```python
from ultralytics.utils import LOGGER, set_logging, TryExcept

# Configure logging
set_logging(name='my_app', verbose=True)

# Use global logger
LOGGER.info("Starting training process")
LOGGER.warning("Low confidence detections")
LOGGER.error("Failed to load model")

# Graceful exception handling
with TryExcept("Loading model"):
    model = YOLO("nonexistent_model.pt")
    # If this fails, it logs a warning instead of crashing
```

### Callback System

Register and manage callback functions for various events.

```python { .api }
default_callbacks = {
    'on_pretrain_routine_start': [],
    'on_pretrain_routine_end': [],
    'on_train_start': [],
    'on_train_epoch_start': [],
    'on_train_batch_start': [],
    'on_optimizer_step': [],
    'on_before_zero_grad': [],
    'on_train_batch_end': [],
    'on_train_epoch_end': [],
    'on_val_start': [],
    'on_val_batch_start': [],
    'on_val_batch_end': [],
    'on_val_end': [],
    'on_fit_epoch_end': [],
    'on_model_save': [],
    'on_train_end': [],
    'teardown': []
}

def add_integration_callbacks(instance):
    """Add integration callbacks for logging platforms."""
```

## Types

```python { .api }
from typing import Dict, Any, Optional, Union, List, Callable
from pathlib import Path
import logging

# Configuration types
ConfigDict = Dict[str, Any]
SettingsDict = Dict[str, Any]

# Environment detection types
EnvironmentInfo = Dict[str, str]

# Callback types
CallbackDict = Dict[str, List[Callable]]
CallbackFunction = Callable[..., None]

# Path and file types
PathLike = Union[str, Path]

# Logger type
Logger = logging.Logger
```