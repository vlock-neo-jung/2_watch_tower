# Coordinate and Data Conversion

Utilities for converting between different coordinate formats, processing masks and polygons, and transforming data between various computer vision frameworks.

## Capabilities

### Box Coordinate Conversion

Functions for converting between different bounding box coordinate formats.

```python { .api }
def xyxy_to_xywh(xyxy: np.ndarray) -> np.ndarray:
    """
    Convert bounding boxes from (x1, y1, x2, y2) to (x, y, width, height) format.
    
    Args:
        xyxy (np.ndarray): Bounding boxes in [x1, y1, x2, y2] format, shape (n, 4)
        
    Returns:
        np.ndarray: Bounding boxes in [x, y, width, height] format, shape (n, 4)
    """

def xywh_to_xyxy(xywh: np.ndarray) -> np.ndarray:
    """
    Convert bounding boxes from (x, y, width, height) to (x1, y1, x2, y2) format.
    
    Args:
        xywh (np.ndarray): Bounding boxes in [x, y, width, height] format, shape (n, 4)
        
    Returns:
        np.ndarray: Bounding boxes in [x1, y1, x2, y2] format, shape (n, 4)
    """

def xcycwh_to_xyxy(xcycwh: np.ndarray) -> np.ndarray:
    """
    Convert from center format (x_center, y_center, width, height) to corner format.
    
    Args:
        xcycwh (np.ndarray): Boxes in [x_center, y_center, width, height] format
        
    Returns:
        np.ndarray: Boxes in [x1, y1, x2, y2] format
    """

def xyxy_to_xcycarh(xyxy: np.ndarray) -> np.ndarray:
    """
    Convert to center format with aspect ratio and height.
    
    Args:
        xyxy (np.ndarray): Boxes in [x1, y1, x2, y2] format
        
    Returns:
        np.ndarray: Boxes in [x_center, y_center, aspect_ratio, height] format
    """
```

### Mask and Polygon Conversion

Functions for converting between masks, polygons, and bounding boxes.

```python { .api }
def mask_to_polygons(mask: np.ndarray) -> list[np.ndarray]:
    """
    Convert segmentation mask to polygon representation.
    
    Args:
        mask (np.ndarray): Binary mask, shape (H, W)
        
    Returns:
        list[np.ndarray]: List of polygons, each as (n, 2) coordinate arrays
    """

def polygon_to_mask(polygon: np.ndarray, resolution_wh: tuple[int, int]) -> np.ndarray:
    """
    Convert polygon to binary mask.
    
    Args:
        polygon (np.ndarray): Polygon coordinates, shape (n, 2)
        resolution_wh (tuple[int, int]): Output mask size (width, height)
        
    Returns:
        np.ndarray: Binary mask, shape (H, W)
    """

def mask_to_xyxy(mask: np.ndarray) -> np.ndarray:
    """
    Extract bounding boxes from segmentation masks.
    
    Args:
        mask (np.ndarray): Binary masks, shape (n, H, W)
        
    Returns:
        np.ndarray: Bounding boxes in [x1, y1, x2, y2] format, shape (n, 4)
    """

def polygon_to_xyxy(polygon: np.ndarray) -> np.ndarray:
    """
    Extract bounding box from polygon coordinates.
    
    Args:
        polygon (np.ndarray): Polygon coordinates, shape (n, 2)
        
    Returns:
        np.ndarray: Bounding box [x1, y1, x2, y2]
    """

def xyxy_to_polygons(xyxy: np.ndarray) -> list[np.ndarray]:
    """
    Convert bounding boxes to polygon representation.
    
    Args:
        xyxy (np.ndarray): Bounding boxes in [x1, y1, x2, y2] format
        
    Returns:
        list[np.ndarray]: List of polygon arrays, each shape (4, 2)
    """
```

### Box Manipulation

Utilities for manipulating bounding box coordinates.

```python { .api }
def clip_boxes(xyxy: np.ndarray, resolution_wh: tuple[int, int]) -> np.ndarray:
    """
    Clip bounding boxes to image boundaries.
    
    Args:
        xyxy (np.ndarray): Bounding boxes in [x1, y1, x2, y2] format
        resolution_wh (tuple[int, int]): Image dimensions (width, height)
        
    Returns:
        np.ndarray: Clipped bounding boxes
    """

def pad_boxes(xyxy: np.ndarray, px: int) -> np.ndarray:
    """
    Add padding to bounding boxes.
    
    Args:
        xyxy (np.ndarray): Bounding boxes in [x1, y1, x2, y2] format
        px (int): Padding in pixels
        
    Returns:
        np.ndarray: Padded bounding boxes
    """

def scale_boxes(xyxy: np.ndarray, factor: float) -> np.ndarray:
    """
    Scale bounding boxes by a factor.
    
    Args:
        xyxy (np.ndarray): Bounding boxes in [x1, y1, x2, y2] format  
        factor (float): Scaling factor
        
    Returns:
        np.ndarray: Scaled bounding boxes
    """

def move_boxes(xyxy: np.ndarray, offset: np.ndarray) -> np.ndarray:
    """
    Translate bounding boxes by offset.
    
    Args:
        xyxy (np.ndarray): Bounding boxes in [x1, y1, x2, y2] format
        offset (np.ndarray): Translation offset [dx, dy]
        
    Returns:
        np.ndarray: Translated bounding boxes
    """

def denormalize_boxes(xyxy: np.ndarray, resolution_wh: tuple[int, int]) -> np.ndarray:
    """
    Convert normalized coordinates [0-1] to absolute pixel coordinates.
    
    Args:
        xyxy (np.ndarray): Normalized bounding boxes
        resolution_wh (tuple[int, int]): Image dimensions (width, height)
        
    Returns:
        np.ndarray: Absolute coordinate bounding boxes
    """
```

### Dataset Format Conversion

Functions for converting between different dataset annotation formats.

```python { .api }
def mask_to_rle(mask: np.ndarray) -> dict:
    """
    Convert binary mask to Run Length Encoding (RLE) format.
    
    Args:
        mask (np.ndarray): Binary mask, shape (H, W)
        
    Returns:
        dict: RLE encoded mask in COCO format
    """

def rle_to_mask(rle: dict) -> np.ndarray:
    """
    Convert RLE encoded mask back to binary mask.
    
    Args:
        rle (dict): RLE encoded mask in COCO format
        
    Returns:
        np.ndarray: Binary mask, shape (H, W)  
    """

def get_coco_class_index_mapping() -> dict[str, int]:
    """
    Get mapping from COCO class names to indices.
    
    Returns:
        dict[str, int]: Mapping from class names to indices
    """
```

## Usage Examples

### Basic Coordinate Conversion

```python
import supervision as sv
import numpy as np

# Convert from corner to center format
xyxy_boxes = np.array([[100, 100, 200, 200], [300, 150, 400, 250]])
xywh_boxes = sv.xyxy_to_xywh(xyxy_boxes)
print(xywh_boxes)  # [[100, 100, 100, 100], [300, 150, 100, 100]]

# Convert back to corner format
xyxy_converted = sv.xywh_to_xyxy(xywh_boxes)
```

### Mask to Polygon Conversion

```python
import supervision as sv
import cv2

# Load segmentation mask
mask = cv2.imread("mask.png", cv2.IMREAD_GRAYSCALE) > 0

# Convert to polygons
polygons = sv.mask_to_polygons(mask)

# Convert back to mask
reconstructed_mask = sv.polygon_to_mask(
    polygon=polygons[0], 
    resolution_wh=(mask.shape[1], mask.shape[0])
)
```

### Box Manipulation Pipeline

```python
import supervision as sv
import numpy as np

# Original boxes
boxes = np.array([[50, 50, 150, 150], [200, 100, 300, 200]])

# Apply transformations
padded_boxes = sv.pad_boxes(boxes, px=10)
scaled_boxes = sv.scale_boxes(padded_boxes, factor=1.2)
moved_boxes = sv.move_boxes(scaled_boxes, offset=np.array([20, 30]))

# Clip to image boundaries
image_size = (640, 480)
final_boxes = sv.clip_boxes(moved_boxes, resolution_wh=image_size)
```

### Dataset Format Conversion

```python
import supervision as sv

# Convert mask to COCO RLE format
mask = np.zeros((480, 640), dtype=bool)
mask[100:200, 100:200] = True

rle = sv.mask_to_rle(mask)
print(rle)  # {'size': [480, 640], 'counts': ...}

# Convert back to mask
reconstructed_mask = sv.rle_to_mask(rle)
```

## Types

```python { .api }
# Coordinate format type aliases
XYXYFormat = np.ndarray  # Shape: (n, 4) - [x1, y1, x2, y2]
XYWHFormat = np.ndarray  # Shape: (n, 4) - [x, y, width, height]  
XCYCWHFormat = np.ndarray  # Shape: (n, 4) - [x_center, y_center, width, height]

# Polygon and mask types
Polygon = np.ndarray  # Shape: (n, 2) - [(x, y), ...]
PolygonList = list[np.ndarray]  # List of polygon coordinate arrays
BinaryMask = np.ndarray  # Shape: (H, W) - boolean mask
RLEMask = dict  # Run Length Encoded mask in COCO format

# Image resolution type
Resolution = tuple[int, int]  # (width, height)
```