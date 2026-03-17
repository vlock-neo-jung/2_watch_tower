# Dataset Management

Tools for loading, processing, and converting datasets between popular computer vision formats like COCO, YOLO, and Pascal VOC. Provides unified interfaces for working with detection and classification datasets.

## Capabilities

### Base Dataset Class

Abstract base class that defines the common interface for all dataset types.

```python { .api }
class BaseDataset(ABC):
    """
    Abstract base class for all dataset types.
    """
    
    @abstractmethod
    def __len__(self) -> int:
        """Return the number of samples in the dataset."""
        
    @abstractmethod
    def split(
        self,
        split_ratio: float = 0.8,
        random_state: int | None = None,
        shuffle: bool = True
    ) -> tuple["BaseDataset", "BaseDataset"]:
        """Split the dataset into train and validation sets."""
```

### Detection Dataset

Comprehensive dataset class for object detection tasks with support for multiple annotation formats.

```python { .api }
class DetectionDataset(BaseDataset):
    """
    Contains information about a detection dataset. Handles lazy image loading
    and annotation retrieval, dataset splitting, conversions into multiple formats.

    Attributes:
        classes (list[str]): List containing dataset class names
        images (list[str] | dict[str, np.ndarray]): List of image paths or dictionary of loaded images
        annotations (dict[str, Detections]): Dictionary mapping image path to annotations
    """
    
    def __init__(
        self,
        classes: list[str],
        images: list[str] | dict[str, np.ndarray],
        annotations: dict[str, Detections]
    ) -> None: ...

    def __len__(self) -> int:
        """Return the number of images in the dataset."""

    def __getitem__(self, i: int) -> tuple[str, np.ndarray, Detections]:
        """Get image path, image data, and annotations at index i."""

    def __iter__(self) -> Iterator[tuple[str, np.ndarray, Detections]]:
        """Iterate over images and annotations in the dataset."""

    def split(
        self,
        split_ratio: float = 0.8,
        random_state: int | None = None,
        shuffle: bool = True
    ) -> tuple["DetectionDataset", "DetectionDataset"]:
        """Split dataset into train and validation sets."""

    @classmethod
    def merge(cls, dataset_list: list["DetectionDataset"]) -> "DetectionDataset":
        """Merge multiple DetectionDataset instances into one."""

    @classmethod
    def from_pascal_voc(
        cls,
        images_directory_path: str,
        annotations_directory_path: str,
        force_masks: bool = False
    ) -> "DetectionDataset":
        """Create dataset from Pascal VOC format annotations."""

    def as_pascal_voc(
        self,
        images_directory_path: str | None = None,
        annotations_directory_path: str | None = None,
        min_image_area_percentage: float = 0.0,
        max_image_area_percentage: float = 1.0,
        approximation_percentage: float = 0.0
    ) -> None:
        """Export dataset to Pascal VOC format."""

    @classmethod
    def from_yolo(
        cls,
        images_directory_path: str,
        annotations_directory_path: str,
        data_yaml_path: str,
        force_masks: bool = False,
        is_obb: bool = False
    ) -> "DetectionDataset":
        """Create dataset from YOLO format annotations."""

    def as_yolo(
        self,
        images_directory_path: str | None = None,
        annotations_directory_path: str | None = None,
        data_yaml_path: str | None = None,
        min_image_area_percentage: float = 0.0,
        max_image_area_percentage: float = 1.0,
        approximation_percentage: float = 0.0
    ) -> None:
        """Export dataset to YOLO format."""

    @classmethod
    def from_coco(
        cls,
        images_directory_path: str,
        annotations_path: str,
        force_masks: bool = False
    ) -> "DetectionDataset":
        """Create dataset from COCO format annotations."""

    def as_coco(
        self,
        images_directory_path: str | None = None,
        annotations_path: str | None = None,
        min_image_area_percentage: float = 0.0,
        max_image_area_percentage: float = 1.0,
        approximation_percentage: float = 0.0
    ) -> None:
        """Export dataset to COCO format."""
```

### Classification Dataset

Dataset class for image classification tasks with folder structure support.

```python { .api }
class ClassificationDataset(BaseDataset):
    """
    Contains information about a classification dataset, handles lazy image
    loading, dataset splitting.

    Attributes:
        classes (list[str]): List containing dataset class names
        images (list[str] | dict[str, np.ndarray]): List of image paths or dictionary of images
        annotations (dict[str, Classifications]): Dictionary mapping image name to annotations
    """
    
    def __init__(
        self,
        classes: list[str],
        images: list[str] | dict[str, np.ndarray],
        annotations: dict[str, Classifications]
    ) -> None: ...

    def __len__(self) -> int:
        """Return the number of images in the dataset."""

    def __getitem__(self, i: int) -> tuple[str, np.ndarray, Classifications]:
        """Get image path, image data, and classification at index i."""

    def __iter__(self) -> Iterator[tuple[str, np.ndarray, Classifications]]:
        """Iterate over images and classifications in the dataset."""

    def split(
        self,
        split_ratio: float = 0.8,
        random_state: int | None = None,
        shuffle: bool = True
    ) -> tuple["ClassificationDataset", "ClassificationDataset"]:
        """Split dataset into train and validation sets."""

    def as_folder_structure(self, root_directory_path: str) -> None:
        """Export dataset as folder structure with class subdirectories."""

    @classmethod
    def from_folder_structure(cls, root_directory_path: str) -> "ClassificationDataset":
        """Create dataset from folder structure with class subdirectories."""
```

### Dataset Utilities

Helper functions for dataset operations and format conversions.

```python { .api }
def get_coco_class_index_mapping(annotations_path: str) -> dict[int, str]:
    """Get mapping from COCO category IDs to class names."""

def mask_to_rle(mask: np.ndarray) -> dict[str, Any]:
    """Convert binary mask to COCO RLE format."""

def rle_to_mask(rle: dict[str, Any]) -> np.ndarray:
    """Convert COCO RLE format to binary mask."""
```

## Usage Examples

### Loading Different Dataset Formats

```python
import supervision as sv

# Load YOLO dataset
dataset = sv.DetectionDataset.from_yolo(
    images_directory_path="./images",
    annotations_directory_path="./labels", 
    data_yaml_path="./data.yaml"
)

# Load COCO dataset
coco_dataset = sv.DetectionDataset.from_coco(
    images_directory_path="./coco/images",
    annotations_path="./coco/annotations.json"
)

# Load Pascal VOC dataset
voc_dataset = sv.DetectionDataset.from_pascal_voc(
    images_directory_path="./images",
    annotations_directory_path="./annotations"
)

print(f"Dataset classes: {dataset.classes}")
print(f"Number of images: {len(dataset)}")
```

### Dataset Splitting and Processing

```python
import supervision as sv

# Load dataset
dataset = sv.DetectionDataset.from_yolo(
    images_directory_path="./images",
    annotations_directory_path="./labels",
    data_yaml_path="./data.yaml"
)

# Split into train and validation sets
train_dataset, val_dataset = dataset.split(
    split_ratio=0.8,
    random_state=42,
    shuffle=True
)

print(f"Train set: {len(train_dataset)} images")
print(f"Validation set: {len(val_dataset)} images")

# Iterate through dataset
for image_path, image, detections in train_dataset:
    print(f"Processing {image_path}")
    print(f"Found {len(detections)} objects")
    # Process image and annotations
```

### Format Conversions

```python
import supervision as sv

# Load YOLO dataset
dataset = sv.DetectionDataset.from_yolo(
    images_directory_path="./yolo/images",
    annotations_directory_path="./yolo/labels",
    data_yaml_path="./yolo/data.yaml"
)

# Convert to COCO format
dataset.as_coco(
    images_directory_path="./coco/images",
    annotations_path="./coco/annotations.json"
)

# Convert to Pascal VOC format
dataset.as_pascal_voc(
    images_directory_path="./voc/images",
    annotations_directory_path="./voc/annotations"
)

print("Dataset converted to multiple formats!")
```

### Merging Multiple Datasets

```python
import supervision as sv

# Load multiple datasets
dataset1 = sv.DetectionDataset.from_yolo(
    images_directory_path="./dataset1/images",
    annotations_directory_path="./dataset1/labels",
    data_yaml_path="./dataset1/data.yaml"
)

dataset2 = sv.DetectionDataset.from_coco(
    images_directory_path="./dataset2/images", 
    annotations_path="./dataset2/annotations.json"
)

# Merge datasets
merged_dataset = sv.DetectionDataset.merge([dataset1, dataset2])

print(f"Merged dataset: {len(merged_dataset)} images")
print(f"Combined classes: {merged_dataset.classes}")
```

### Classification Dataset Example

```python
import supervision as sv

# Load classification dataset from folder structure
# Expected structure:
# root/
#   ├── class1/
#   │   ├── img1.jpg
#   │   └── img2.jpg
#   └── class2/
#       ├── img3.jpg
#       └── img4.jpg

classification_dataset = sv.ClassificationDataset.from_folder_structure(
    root_directory_path="./classification_data"
)

# Split the dataset
train_cls, val_cls = classification_dataset.split(split_ratio=0.7)

# Export back to folder structure
train_cls.as_folder_structure("./output/train")
val_cls.as_folder_structure("./output/val")

# Iterate through classifications
for image_path, image, classification in classification_dataset:
    print(f"Image: {image_path}")
    print(f"Class ID: {classification.class_id}")
    print(f"Confidence: {classification.confidence}")
```