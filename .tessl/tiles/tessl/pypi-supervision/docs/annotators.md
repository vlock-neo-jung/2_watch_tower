# Annotators

Comprehensive visualization tools for adding annotations to images. All annotators inherit from `BaseAnnotator` and provide consistent APIs for drawing boxes, labels, masks, shapes, and visual effects on detection results.

## Capabilities

### Basic Shape Annotators

Core geometric shape annotations for highlighting detected objects.

```python { .api }
class BoxAnnotator(BaseAnnotator):
    """
    Draw bounding boxes around detections.
    
    Args:
        color (Color | ColorPalette): Box color or color palette
        thickness (int): Line thickness in pixels
        color_lookup (ColorLookup): Color mapping strategy (CLASS, TRACK, INDEX)
    """
    def __init__(
        self,
        color: Color | ColorPalette = ColorPalette.DEFAULT,
        thickness: int = 2,
        color_lookup: ColorLookup = ColorLookup.CLASS
    ): ...

    def annotate(
        self,
        scene: ImageType,
        detections: Detections,
        custom_color_lookup: np.ndarray | None = None
    ) -> ImageType:
        """Draw bounding boxes on the image."""

class BoxCornerAnnotator(BaseAnnotator):
    """
    Draw corner markers on bounding boxes.
    
    Args:
        color (Color | ColorPalette): Corner color or color palette  
        thickness (int): Line thickness in pixels
        corner_length (int): Length of corner lines in pixels
        color_lookup (ColorLookup): Color mapping strategy
    """
    def __init__(
        self,
        color: Color | ColorPalette = ColorPalette.DEFAULT,
        thickness: int = 4,
        corner_length: int = 15,
        color_lookup: ColorLookup = ColorLookup.CLASS
    ): ...

class RoundBoxAnnotator(BaseAnnotator):
    """Draw bounding boxes with rounded corners."""

class OrientedBoxAnnotator(BaseAnnotator):
    """Draw oriented/rotated bounding boxes for OBB detection."""

class CircleAnnotator(BaseAnnotator):
    """
    Draw circles around detections.
    
    Args:
        color (Color | ColorPalette): Circle color or color palette
        thickness (int): Circle line thickness  
        color_lookup (ColorLookup): Color mapping strategy
    """

class EllipseAnnotator(BaseAnnotator):
    """
    Draw ellipses around detections.
    
    Args:
        color (Color | ColorPalette): Ellipse color
        thickness (int): Line thickness
        start_angle (int): Starting angle of ellipse
        end_angle (int): Ending angle of ellipse
        color_lookup (ColorLookup): Color mapping strategy
    """

class DotAnnotator(BaseAnnotator):
    """Draw center dots on detections."""

class TriangleAnnotator(BaseAnnotator):
    """Draw triangular markers on detections."""
```

### Mask and Region Annotators

Annotations for segmentation masks and polygonal regions.

```python { .api }
class MaskAnnotator(BaseAnnotator):
    """
    Overlay segmentation masks with transparency.
    
    Args:
        color (Color | ColorPalette): Mask color or color palette
        opacity (float): Mask transparency (0.0 to 1.0)
        color_lookup (ColorLookup): Color mapping strategy
    """
    def __init__(
        self,
        color: Color | ColorPalette = ColorPalette.DEFAULT,
        opacity: float = 0.5,
        color_lookup: ColorLookup = ColorLookup.CLASS
    ): ...

class PolygonAnnotator(BaseAnnotator):
    """
    Draw polygon outlines from masks or polygon data.
    
    Args:
        color (Color | ColorPalette): Polygon color
        thickness (int): Line thickness
        color_lookup (ColorLookup): Color mapping strategy
    """

class HaloAnnotator(BaseAnnotator):
    """
    Add halo effects around segmentation masks.
    
    Args:
        color (Color | ColorPalette): Halo color
        opacity (float): Halo transparency
        kernel_size (int): Blur kernel size for halo effect
        color_lookup (ColorLookup): Color mapping strategy
    """
```

### Text and Label Annotators

Annotations for adding text labels and information overlays.

```python { .api }
class LabelAnnotator(BaseAnnotator):
    """
    Add text labels to detections.
    
    Args:
        color (Color | ColorPalette): Label background color
        text_color (Color | ColorPalette): Label text color
        text_padding (int): Padding around text in pixels
        text_position (Position): Label position relative to detection
        text_scale (float): Text size scaling factor
        text_thickness (int): Text line thickness
        font (int): OpenCV font type
        color_lookup (ColorLookup): Color mapping strategy
        border_radius (int): Background corner radius
        smart_position (bool): Auto-adjust position to avoid overlaps
    """
    def __init__(
        self,
        color: Color | ColorPalette = ColorPalette.DEFAULT,
        text_color: Color | ColorPalette = Color.WHITE,
        text_padding: int = 10,
        text_position: Position = Position.TOP_LEFT,
        text_scale: float = 0.5,
        text_thickness: int = 1,
        font: int = cv2.FONT_HERSHEY_SIMPLEX,
        color_lookup: ColorLookup = ColorLookup.CLASS,
        border_radius: int = 0,
        smart_position: bool = False
    ): ...

class RichLabelAnnotator(BaseAnnotator):
    """Enhanced labels with advanced formatting and styling options."""

class PercentageBarAnnotator(BaseAnnotator):
    """
    Display confidence or progress bars.
    
    Args:
        height (int): Bar height in pixels
        width (int): Bar width in pixels  
        color_lookup (ColorLookup): Color mapping strategy
        border_color (Color): Bar border color
        background_color (Color): Bar background color
    """
```

### Effect and Style Annotators

Advanced visual effects and image processing annotations.

```python { .api }
class BlurAnnotator(BaseAnnotator):
    """
    Apply blur effects to detection regions.
    
    Args:
        kernel_size (int): Blur kernel size (must be odd)
    """
    def __init__(self, kernel_size: int = 15): ...

class PixelateAnnotator(BaseAnnotator):
    """
    Apply pixelation effects to detection regions.
    
    Args:
        pixel_size (int): Size of pixelation blocks
    """

class ColorAnnotator(BaseAnnotator):
    """Apply color overlays to detection regions."""

class BackgroundOverlayAnnotator(BaseAnnotator):
    """Overlay background images or patterns."""

class HeatMapAnnotator(BaseAnnotator):
    """
    Generate heat map visualizations from detection density.
    
    Args:
        opacity (float): Heat map transparency
        kernel_size (int): Smoothing kernel size
        colormap (int): OpenCV colormap for visualization
    """

class IconAnnotator(BaseAnnotator):
    """
    Overlay custom icons on detections.
    
    Args:
        icon_path (str): Path to icon image file
        icon_size (tuple[int, int]): Icon dimensions (width, height)
        position (Position): Icon position relative to detection
    """

class CropAnnotator(BaseAnnotator):
    """Crop and display detection regions as overlays."""

class ComparisonAnnotator(BaseAnnotator):
    """Create side-by-side image comparisons."""
```

### Tracking Annotators

Specialized annotations for object tracking visualization.

```python { .api }
class TraceAnnotator(BaseAnnotator):
    """
    Draw object movement traces/trails.
    
    Args:
        color (Color | ColorPalette): Trace line color
        position (Position): Point to track (center, top_center, etc.)
        trace_length (int): Maximum trace history length
        thickness (int): Line thickness
        color_lookup (ColorLookup): Color mapping strategy
    """
    def __init__(
        self,
        color: Color | ColorPalette = ColorPalette.DEFAULT,
        position: Position = Position.CENTER,
        trace_length: int = 30,
        thickness: int = 2,
        color_lookup: ColorLookup = ColorLookup.CLASS
    ): ...
```

### Keypoint Annotators

Specialized annotations for keypoint and pose visualization.

```python { .api }
class VertexAnnotator(BaseAnnotator):
    """
    Draw keypoint vertices/markers.
    
    Args:
        color (Color | ColorPalette): Vertex color
        radius (int): Vertex marker radius
        color_lookup (ColorLookup): Color mapping strategy
    """

class EdgeAnnotator(BaseAnnotator):
    """
    Draw connections between keypoints.
    
    Args:
        color (Color | ColorPalette): Edge line color
        thickness (int): Line thickness
        edges (list[tuple[int, int]]): Pairs of keypoint indices to connect
        color_lookup (ColorLookup): Color mapping strategy
    """

class VertexLabelAnnotator(BaseAnnotator):
    """Add labels to keypoint vertices."""
```

## Usage Examples

### Basic Box and Label Annotation

```python
import supervision as sv
import cv2

# Create annotators
box_annotator = sv.BoxAnnotator(
    color=sv.ColorPalette.DEFAULT,
    thickness=2,
    color_lookup=sv.ColorLookup.CLASS
)

label_annotator = sv.LabelAnnotator(
    color=sv.ColorPalette.DEFAULT,
    text_color=sv.Color.WHITE,
    text_position=sv.Position.TOP_LEFT
)

# Apply annotations
annotated_frame = box_annotator.annotate(
    scene=image.copy(),
    detections=detections
)

annotated_frame = label_annotator.annotate(
    scene=annotated_frame,
    detections=detections,
    labels=class_names
)
```

### Advanced Multi-Annotator Pipeline

```python
import supervision as sv

# Create multiple annotators
annotators = [
    sv.MaskAnnotator(opacity=0.3),
    sv.BoxAnnotator(thickness=2),
    sv.LabelAnnotator(text_position=sv.Position.TOP_LEFT),
    sv.TraceAnnotator(trace_length=50)
]

# Apply all annotations
annotated_frame = image.copy()
for annotator in annotators:
    annotated_frame = annotator.annotate(
        scene=annotated_frame,
        detections=detections
    )
```

### Custom Color Mapping

```python
# Use custom colors
custom_colors = np.array([
    [255, 0, 0],    # Red for class 0
    [0, 255, 0],    # Green for class 1  
    [0, 0, 255]     # Blue for class 2
])

box_annotator = sv.BoxAnnotator(color_lookup=sv.ColorLookup.CLASS)
annotated_frame = box_annotator.annotate(
    scene=image,
    detections=detections,
    custom_color_lookup=custom_colors
)
```

## Types

```python { .api }
# Base annotator type
class BaseAnnotator:
    """Base class for all annotators providing common interface."""
    
    def annotate(
        self,
        scene: ImageType,
        detections: Detections,
        **kwargs
    ) -> ImageType:
        """Apply annotation to the scene."""

# Image type union
ImageType = np.ndarray | Image.Image

# Color lookup strategy
class ColorLookup(Enum):
    CLASS = "CLASS"     # Color by detection class
    TRACK = "TRACK"     # Color by tracking ID
    INDEX = "INDEX"     # Color by detection index
```