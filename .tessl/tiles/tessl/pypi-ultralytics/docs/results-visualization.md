# Results and Visualization

Rich result objects containing detection outputs with built-in visualization, annotation, and export capabilities for comprehensive analysis and presentation of model predictions.

## Capabilities

### Results Object

The Results class encapsulates all prediction outputs and provides methods for visualization and data export.

```python { .api }
class Results:
    def __init__(self, orig_img, path, names, boxes=None, masks=None, probs=None, keypoints=None, obb=None):
        """
        Initialize Results object.
        
        Parameters:
        - orig_img (np.ndarray): Original input image
        - path (str): Image file path
        - names (dict): Class names dictionary
        - boxes (Boxes, optional): Detection boxes
        - masks (Masks, optional): Segmentation masks  
        - probs (Probs, optional): Classification probabilities
        - keypoints (Keypoints, optional): Pose keypoints
        - obb (OBB, optional): Oriented bounding boxes
        """
    
    # Core properties
    orig_img: np.ndarray        # Original input image
    orig_shape: tuple           # Original image shape (height, width)
    boxes: Optional[Boxes]      # Detection boxes
    masks: Optional[Masks]      # Segmentation masks
    probs: Optional[Probs]      # Classification probabilities
    keypoints: Optional[Keypoints]  # Pose estimation keypoints
    obb: Optional[OBB]          # Oriented bounding boxes
    speed: dict                 # Inference speed metrics
    names: dict                 # Class names dictionary
    path: str                   # Source image path
    
    def plot(self, conf=True, line_width=None, font_size=None, font='Arial.ttf', 
             pil=False, img=None, im_gpu=None, kpt_radius=5, kpt_line=True, 
             labels=True, boxes=True, masks=True, probs=True, **kwargs) -> np.ndarray:
        """
        Plot prediction results on image.
        
        Parameters:
        - conf (bool): Plot confidence scores (default: True)
        - line_width (int): Line thickness (default: auto)
        - font_size (int): Font size (default: auto)
        - font (str): Font file path (default: 'Arial.ttf')
        - pil (bool): Return PIL Image instead of numpy array (default: False)
        - img (np.ndarray): Custom image to plot on (default: self.orig_img)
        - im_gpu (torch.Tensor): GPU image tensor for faster plotting
        - kpt_radius (int): Keypoint radius (default: 5)
        - kpt_line (bool): Draw keypoint connections (default: True)
        - labels (bool): Plot class labels (default: True)
        - boxes (bool): Plot bounding boxes (default: True)
        - masks (bool): Plot segmentation masks (default: True)
        - probs (bool): Plot classification probabilities (default: True)
        
        Returns:
        np.ndarray: Annotated image as numpy array
        """
    
    def show(self, *args, **kwargs):
        """Display the annotated image."""
    
    def save(self, filename=None, *args, **kwargs):
        """Save the annotated image to file."""
    
    def verbose(self) -> str:
        """Return verbose string representation of results."""
    
    def save_txt(self, txt_file, save_conf=False):
        """Save results to txt file in YOLO format."""
    
    def save_crop(self, save_dir, file_name=None):
        """Save cropped detections to directory."""
    
    def tojson(self, normalize=False):
        """Convert results to JSON format."""
    
    def pandas(self):
        """Convert results to pandas DataFrame."""
```

**Usage Examples:**

```python
from ultralytics import YOLO
import cv2

# Load model and make predictions
model = YOLO("yolo11n.pt")
results = model("image.jpg")

# Access result properties
result = results[0]
print(f"Image shape: {result.orig_shape}")
print(f"Number of detections: {len(result.boxes)}")
print(f"Speed: {result.speed}")

# Plot results with custom styling
annotated_img = result.plot(
    conf=True,
    line_width=2,
    font_size=12,
    labels=True,
    boxes=True
)

# Display result
result.show()

# Save annotated result
result.save("annotated_image.jpg")

# Save crops of detected objects
result.save_crop("crops/")

# Export to different formats
result.save_txt("detections.txt", save_conf=True)
json_data = result.tojson(normalize=True)
df = result.pandas()
```

### Detection Boxes

Container for object detection bounding boxes with associated metadata.

```python { .api }
class Boxes:
    def __init__(self, boxes, orig_shape):
        """
        Initialize Boxes object.
        
        Parameters:
        - boxes (torch.Tensor): Detection boxes tensor [N, 6] (x1, y1, x2, y2, conf, cls)
        - orig_shape (tuple): Original image shape
        """
    
    # Core properties
    xyxy: torch.Tensor          # Bounding boxes in xyxy format [N, 4]
    conf: torch.Tensor          # Confidence scores [N]
    cls: torch.Tensor           # Class predictions [N]
    id: Optional[torch.Tensor]  # Track IDs [N] (for tracking)
    xywh: torch.Tensor          # Boxes in xywh format [N, 4]
    xyxyn: torch.Tensor         # Normalized xyxy boxes [N, 4]
    xywhn: torch.Tensor         # Normalized xywh boxes [N, 4]
    
    def __len__(self) -> int:
        """Return number of boxes."""
    
    def __getitem__(self, idx) -> 'Boxes':
        """Get subset of boxes by index."""
    
    @property
    def cpu(self) -> 'Boxes':
        """Return boxes on CPU."""
    
    @property
    def numpy(self) -> 'Boxes':
        """Return boxes as numpy arrays."""
```

**Usage Examples:**

```python
# Access detection boxes
if result.boxes is not None:
    boxes = result.boxes
    
    # Get box coordinates
    xyxy = boxes.xyxy.cpu().numpy()  # [[x1, y1, x2, y2], ...]
    xywh = boxes.xywh.cpu().numpy()  # [[x, y, w, h], ...]
    
    # Get confidence scores and classes
    confidences = boxes.conf.cpu().numpy()
    classes = boxes.cls.cpu().numpy()
    
    # Iterate through detections
    for i, (box, conf, cls) in enumerate(zip(xyxy, confidences, classes)):
        x1, y1, x2, y2 = box
        print(f"Detection {i}: class={cls}, conf={conf:.2f}, box=[{x1:.1f}, {y1:.1f}, {x2:.1f}, {y2:.1f}]")
    
    # Filter high-confidence detections
    high_conf_mask = boxes.conf > 0.5
    high_conf_boxes = boxes[high_conf_mask]
    
    # Get tracking IDs (if available)
    if boxes.id is not None:
        track_ids = boxes.id.cpu().numpy()
        print(f"Track IDs: {track_ids}")
```

### Segmentation Masks

Container for instance segmentation masks with polygon and bitmap representations.

```python { .api }
class Masks:
    def __init__(self, masks, orig_shape):
        """
        Initialize Masks object.
        
        Parameters:
        - masks (torch.Tensor): Segmentation masks tensor
        - orig_shape (tuple): Original image shape
        """
    
    # Core properties
    data: torch.Tensor          # Raw mask data
    xy: List[np.ndarray]        # Mask polygons in xy format
    xyn: List[np.ndarray]       # Normalized mask polygons
    
    def __len__(self) -> int:
        """Return number of masks."""
    
    def __getitem__(self, idx) -> 'Masks':
        """Get subset of masks by index."""
    
    @property
    def cpu(self) -> 'Masks':
        """Return masks on CPU."""
    
    @property
    def numpy(self) -> 'Masks':
        """Return masks as numpy arrays."""
```

**Usage Examples:**

```python
# Access segmentation masks
if result.masks is not None:
    masks = result.masks
    
    # Get mask data
    mask_data = masks.data.cpu().numpy()  # [N, H, W]
    
    # Get polygon representations
    polygons = masks.xy  # List of [n_points, 2] arrays
    normalized_polygons = masks.xyn  # Normalized coordinates
    
    # Process each mask
    for i, (mask, polygon) in enumerate(zip(mask_data, polygons)):
        print(f"Mask {i}: {mask.shape}, polygon points: {len(polygon)}")
        
        # Convert mask to binary image
        binary_mask = (mask > 0.5).astype(np.uint8) * 255
        
        # Save individual mask
        cv2.imwrite(f"mask_{i}.png", binary_mask)
        
        # Use polygon for further processing
        # polygon is shape [n_points, 2] with (x, y) coordinates
```

### Classification Probabilities

Container for image classification results with class probabilities.

```python { .api }
class Probs:
    def __init__(self, probs, orig_shape=None):
        """
        Initialize Probs object.
        
        Parameters:
        - probs (torch.Tensor): Classification probabilities
        - orig_shape (tuple): Original image shape
        """
    
    # Core properties
    data: torch.Tensor          # Raw probability data [num_classes]
    top1: int                   # Index of top-1 class
    top5: List[int]             # Indices of top-5 classes
    top1conf: float             # Confidence of top-1 class
    top5conf: List[float]       # Confidences of top-5 classes
    
    @property
    def cpu(self) -> 'Probs':
        """Return probabilities on CPU."""
    
    @property  
    def numpy(self) -> 'Probs':
        """Return probabilities as numpy arrays."""
```

**Usage Examples:**

```python
# Access classification probabilities
if result.probs is not None:
    probs = result.probs
    
    # Get top predictions
    top1_class = probs.top1
    top1_conf = probs.top1conf
    top5_classes = probs.top5
    top5_confs = probs.top5conf
    
    print(f"Top-1: class {top1_class} ({top1_conf:.3f})")
    print("Top-5:")
    for cls, conf in zip(top5_classes, top5_confs):
        class_name = result.names[cls]
        print(f"  {class_name}: {conf:.3f}")
    
    # Get all probabilities
    all_probs = probs.data.cpu().numpy()
    for i, prob in enumerate(all_probs):
        if prob > 0.01:  # Only show significant probabilities
            print(f"{result.names[i]}: {prob:.3f}")
```

### Pose Keypoints

Container for pose estimation keypoints with skeletal connections.

```python { .api }
class Keypoints:
    def __init__(self, keypoints, orig_shape):
        """
        Initialize Keypoints object.
        
        Parameters:
        - keypoints (torch.Tensor): Keypoint coordinates and visibility
        - orig_shape (tuple): Original image shape
        """
    
    # Core properties
    data: torch.Tensor          # Raw keypoint data [N, num_keypoints, 3] (x, y, visibility)
    xy: torch.Tensor            # Keypoint coordinates [N, num_keypoints, 2]
    xyn: torch.Tensor           # Normalized keypoint coordinates
    conf: torch.Tensor          # Keypoint confidence/visibility scores
    
    def __len__(self) -> int:
        """Return number of pose instances."""
    
    def __getitem__(self, idx) -> 'Keypoints':
        """Get subset of keypoints by index."""
    
    @property
    def cpu(self) -> 'Keypoints':
        """Return keypoints on CPU."""
    
    @property
    def numpy(self) -> 'Keypoints':
        """Return keypoints as numpy arrays."""
```

**Usage Examples:**

```python
# Access pose keypoints
if result.keypoints is not None:
    keypoints = result.keypoints
    
    # Get keypoint data
    kpts_data = keypoints.data.cpu().numpy()  # [N, num_keypoints, 3]
    kpts_xy = keypoints.xy.cpu().numpy()      # [N, num_keypoints, 2]
    kpts_conf = keypoints.conf.cpu().numpy()  # [N, num_keypoints]
    
    # Process each person
    for person_idx, (kpts, confs) in enumerate(zip(kpts_xy, kpts_conf)):
        print(f"Person {person_idx}:")
        
        # Standard COCO keypoint names
        keypoint_names = [
            'nose', 'left_eye', 'right_eye', 'left_ear', 'right_ear',
            'left_shoulder', 'right_shoulder', 'left_elbow', 'right_elbow',
            'left_wrist', 'right_wrist', 'left_hip', 'right_hip',
            'left_knee', 'right_knee', 'left_ankle', 'right_ankle'
        ]
        
        for kpt_idx, ((x, y), conf) in enumerate(zip(kpts, confs)):
            if conf > 0.5:  # Only show visible keypoints
                kpt_name = keypoint_names[kpt_idx] if kpt_idx < len(keypoint_names) else f"kpt_{kpt_idx}"
                print(f"  {kpt_name}: ({x:.1f}, {y:.1f}) conf={conf:.2f}")
```

### Visualization Customization

Advanced visualization options for different use cases and presentation needs.

```python { .api }
# Custom color palettes
def generate_colors(n, colormap='hsv'):
    """Generate n distinct colors."""

def plot_masks(img, masks, colors, alpha=0.3):
    """Plot segmentation masks with transparency."""

def plot_keypoints(img, keypoints, skeleton=None, kpt_color=None, limb_color=None):
    """Plot pose keypoints with skeletal connections."""

def draw_text(img, text, pos, font_scale=0.4, color=(255, 255, 255), thickness=1):
    """Draw text on image with background rectangle."""
```

**Usage Examples:**

```python
# Custom visualization
annotated = result.plot(
    conf=True,          # Show confidence scores
    line_width=3,       # Thick bounding boxes
    font_size=16,       # Large font
    labels=True,        # Show class labels
    boxes=True,         # Show bounding boxes
    masks=True,         # Show segmentation masks
    kpt_radius=8,       # Large keypoint circles
    kpt_line=True       # Show pose connections
)

# Save high-quality result
result.save("high_quality_result.png")

# Custom color scheme for specific classes
colors = {0: (255, 0, 0), 1: (0, 255, 0), 2: (0, 0, 255)}  # Red, Green, Blue
custom_annotated = result.plot(colors=colors)
```

## Types

```python { .api }
from typing import List, Optional, Dict, Tuple, Any, Union
import torch
import numpy as np
from PIL import Image

# Core result types
ResultsList = List[Results]

# Bounding box formats
BboxXYXY = torch.Tensor     # [N, 4] - (x1, y1, x2, y2)
BboxXYWH = torch.Tensor     # [N, 4] - (x_center, y_center, width, height)
BboxNormalized = torch.Tensor  # [N, 4] - normalized coordinates [0, 1]

# Mask types
MaskBitmap = torch.Tensor   # [N, H, W] - binary masks
MaskPolygon = List[np.ndarray]  # List of polygon coordinates

# Keypoint types
KeypointData = torch.Tensor  # [N, num_keypoints, 3] - (x, y, visibility)
KeypointXY = torch.Tensor    # [N, num_keypoints, 2] - (x, y) coordinates

# Classification types
ClassProbs = torch.Tensor    # [num_classes] - class probabilities
ClassIndices = List[int]     # List of class indices

# Visualization types
ColorTuple = Tuple[int, int, int]  # RGB color (0-255)
ColorDict = Dict[int, ColorTuple]  # Class ID to color mapping
ImageArray = np.ndarray            # HWC image array
PILImage = Image.Image             # PIL Image object

# Export types
JSONDict = Dict[str, Any]          # JSON export format
DataFrameType = 'pandas.DataFrame' # Pandas DataFrame type
```