# File Utilities

Utilities for working with files, directories, and different file formats. These utilities provide convenient functions for reading and writing JSON, YAML, and text files, as well as directory operations.

## Capabilities

### Directory Operations

List and filter files in directories with optional extension filtering.

```python { .api }
def list_files_with_extensions(
    directory: str | Path, 
    extensions: list[str] | None = None
) -> list[Path]:
    """
    List files in a directory with specified extensions or all files if no extensions are provided.

    Args:
        directory: The directory path as a string or Path object
        extensions: A list of file extensions to filter. Default is None, which lists all files

    Returns:
        A list of Path objects for the matching files

    Examples:
        ```python
        import supervision as sv

        # List all files in the directory
        files = sv.list_files_with_extensions(directory='my_directory')

        # List only files with '.txt' and '.md' extensions
        files = sv.list_files_with_extensions(
            directory='my_directory', extensions=['txt', 'md'])
        ```
    """
```

### JSON File Operations

Read and write JSON files with automatic numpy array serialization support.

```python { .api }
def read_json_file(file_path: str | Path) -> dict:
    """
    Read and parse a JSON file.

    Args:
        file_path: Path to the JSON file

    Returns:
        Dictionary containing the parsed JSON data
    """

def save_json_file(data: dict, file_path: str | Path, indent: int = 3) -> None:
    """
    Save dictionary data to a JSON file with numpy array support.

    Args:
        data: Dictionary data to save
        file_path: Path where to save the JSON file
        indent: JSON indentation for pretty printing
    """

class NumpyJsonEncoder(json.JSONEncoder):
    """
    JSON encoder that handles numpy data types.
    
    Automatically converts:
    - numpy integers to Python int
    - numpy floats to Python float  
    - numpy arrays to Python lists
    """
```

### YAML File Operations

Read and write YAML configuration files.

```python { .api }
def read_yaml_file(file_path: str | Path) -> dict:
    """
    Read and parse a YAML file.

    Args:
        file_path: Path to the YAML file

    Returns:
        Dictionary containing the parsed YAML data
    """

def save_yaml_file(data: dict, file_path: str | Path) -> None:
    """
    Save dictionary data to a YAML file.

    Args:
        data: Dictionary data to save
        file_path: Path where to save the YAML file
    """
```

### Text File Operations

Basic text file reading and writing utilities.

```python { .api }
def read_txt_file(file_path: str | Path, skip_empty: bool = False) -> list[str]:
    """
    Read a text file and return lines as a list.

    Args:
        file_path: Path to the text file
        skip_empty: Whether to skip empty lines

    Returns:
        List of strings, one per line
    """

def save_text_file(lines: list[str], file_path: str | Path) -> None:
    """
    Save a list of strings to a text file.

    Args:
        lines: List of strings to write
        file_path: Path where to save the text file
    """
```

## Usage Examples

### Working with Project Configurations

```python
import supervision as sv
from pathlib import Path

# Read configuration from YAML
config = sv.read_yaml_file("config.yaml")

# Process some data
results = {
    "detections": 150,
    "confidence_scores": np.array([0.95, 0.87, 0.92]),
    "processed_files": ["image1.jpg", "image2.jpg"]
}

# Save results as JSON (numpy arrays automatically handled)
sv.save_json_file(results, "results.json")

# List all image files in a directory
image_files = sv.list_files_with_extensions(
    directory="./images", 
    extensions=["jpg", "jpeg", "png"]
)

print(f"Found {len(image_files)} image files")
```

### Data Export Workflows

```python
import supervision as sv

# Export detection results in multiple formats
detection_data = {
    "model": "yolov8n",
    "boxes": detections.xyxy.tolist(),
    "scores": detections.confidence.tolist(),
    "classes": detections.class_id.tolist()
}

# Save as JSON
sv.save_json_file(detection_data, "detections.json")

# Save as YAML for human readability
sv.save_yaml_file(detection_data, "detections.yaml")

# Export class names as text file
class_names = ["person", "car", "truck", "bus"]
sv.save_text_file(class_names, "classes.txt")
```