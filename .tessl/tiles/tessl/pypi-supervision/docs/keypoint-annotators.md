# Keypoint Annotators

Specialized annotators for drawing keypoints, skeletal connections, and pose estimation results. These annotators work with KeyPoints data structures to visualize human poses, facial landmarks, and other keypoint-based detections.

## Capabilities

### Vertex Annotation

Draw individual keypoints as circles on the image.

```python { .api }
class VertexAnnotator(BaseKeyPointAnnotator):
    """
    A class that specializes in drawing skeleton vertices on images using specified keypoints.

    Args:
        color (Color): The color to use for annotating keypoints
        radius (int): The radius of the circles used to represent keypoints
    """
    def __init__(
        self,
        color: Color = Color.ROBOFLOW,
        radius: int = 4
    ) -> None: ...

    def annotate(self, scene: ImageType, key_points: KeyPoints) -> ImageType:
        """
        Annotates the given scene with skeleton vertices based on the provided keypoints.

        Args:
            scene: The image where skeleton vertices will be drawn
            key_points: A collection of keypoints with x,y coordinates

        Returns:
            The annotated image matching the input type

        Example:
            ```python
            import supervision as sv

            image = ...
            key_points = sv.KeyPoints(...)

            vertex_annotator = sv.VertexAnnotator(
                color=sv.Color.GREEN,
                radius=10
            )
            annotated_frame = vertex_annotator.annotate(
                scene=image.copy(),
                key_points=key_points
            )
            ```
        """
```

### Edge Annotation

Draw lines connecting keypoints to form skeletal structures.

```python { .api }
class EdgeAnnotator(BaseKeyPointAnnotator):
    """
    A class that specializes in drawing skeleton edges on images using specified keypoints. 
    It connects keypoints with lines to form the skeleton structure.

    Args:
        color (Color): The color to use for the edges
        thickness (int): The thickness of the edges
        edges (list[tuple[int, int]] | None): The edges to draw. If None, will attempt to select automatically
    """
    def __init__(
        self,
        color: Color = Color.ROBOFLOW,
        thickness: int = 2,
        edges: list[tuple[int, int]] | None = None
    ) -> None: ...

    def annotate(self, scene: ImageType, key_points: KeyPoints) -> ImageType:
        """
        Annotates the given scene by drawing lines between specified keypoints to form edges.

        Args:
            scene: The image where skeleton edges will be drawn
            key_points: A collection of keypoints with x,y coordinates

        Returns:
            The annotated image matching the input type

        Example:
            ```python
            import supervision as sv

            image = ...
            key_points = sv.KeyPoints(...)

            edge_annotator = sv.EdgeAnnotator(
                color=sv.Color.GREEN,
                thickness=5
            )
            annotated_frame = edge_annotator.annotate(
                scene=image.copy(),
                key_points=key_points
            )
            ```
        """
```

### Vertex Label Annotation

Add text labels to keypoints showing vertex indices or names.

```python { .api }
class VertexLabelAnnotator:
    """
    A class that draws labels of skeleton vertices on images using specified keypoints.

    Args:
        color (Color): The color to use for the text labels
        text_color (Color): The color of the text
        text_scale (float): The scale factor for text size
        text_thickness (int): The thickness of the text
        text_padding (int): Padding around the text
        border_radius (int): Radius for rounded text background
    """
    def __init__(
        self,
        color: Color = Color.ROBOFLOW,
        text_color: Color = Color.WHITE,
        text_scale: float = 0.5,
        text_thickness: int = 1,
        text_padding: int = 10,
        border_radius: int = 0
    ) -> None: ...

    def annotate(
        self,
        scene: ImageType,
        key_points: KeyPoints,
        labels: list[str] | None = None
    ) -> ImageType:
        """
        Annotates the given scene with labels at keypoint locations.

        Args:
            scene: The image where vertex labels will be drawn
            key_points: A collection of keypoints with x,y coordinates
            labels: Optional list of custom labels. If None, uses vertex indices

        Returns:
            The annotated image matching the input type
        """
```

### Base Class

Abstract base class for all keypoint annotators.

```python { .api }
class BaseKeyPointAnnotator(ABC):
    """Abstract base class for keypoint annotators."""
    
    @abstractmethod
    def annotate(self, scene: ImageType, key_points: KeyPoints) -> ImageType:
        """Abstract method for annotating keypoints on an image."""
```

## Usage Examples

### Basic Pose Visualization

```python
import supervision as sv
import cv2
from ultralytics import YOLO

# Load pose estimation model
model = YOLO("yolov8n-pose.pt")
image = cv2.imread("person.jpg")

# Get pose keypoints
results = model(image)[0]
keypoints = sv.KeyPoints.from_ultralytics(results)

# Create annotators
vertex_annotator = sv.VertexAnnotator(
    color=sv.Color.RED,
    radius=6
)
edge_annotator = sv.EdgeAnnotator(
    color=sv.Color.BLUE,
    thickness=3
)

# Annotate the image
annotated_image = vertex_annotator.annotate(image.copy(), keypoints)
annotated_image = edge_annotator.annotate(annotated_image, keypoints)

cv2.imshow("Pose Estimation", annotated_image)
cv2.waitKey(0)
```

### Custom Skeleton with Labels

```python
import supervision as sv

# Define custom skeleton connections
custom_edges = [
    (1, 2), (2, 3), (3, 4),  # Head to shoulders
    (2, 5), (5, 6), (6, 7),  # Left arm
    (2, 8), (8, 9), (9, 10), # Right arm
    (2, 11), (11, 12),       # Torso
    (11, 13), (13, 14), (14, 15), # Left leg
    (11, 16), (16, 17), (17, 18)  # Right leg
]

# Create annotators with custom configuration
edge_annotator = sv.EdgeAnnotator(
    color=sv.Color.GREEN,
    thickness=2,
    edges=custom_edges
)

vertex_annotator = sv.VertexAnnotator(
    color=sv.Color.YELLOW,
    radius=5
)

label_annotator = sv.VertexLabelAnnotator(
    color=sv.Color.BLACK,
    text_color=sv.Color.WHITE,
    text_scale=0.4,
    text_padding=5,
    border_radius=3
)

# Keypoint names for labeling
keypoint_names = [
    "nose", "left_eye", "right_eye", "left_ear", "right_ear",
    "left_shoulder", "right_shoulder", "left_elbow", "right_elbow",
    "left_wrist", "right_wrist", "left_hip", "right_hip",
    "left_knee", "right_knee", "left_ankle", "right_ankle"
]

# Apply all annotations
annotated_image = edge_annotator.annotate(image.copy(), keypoints)
annotated_image = vertex_annotator.annotate(annotated_image, keypoints)
annotated_image = label_annotator.annotate(
    annotated_image, keypoints, labels=keypoint_names
)
```

### Multi-Person Pose Visualization

```python
import supervision as sv

# Process multiple people in the image
for i, person_keypoints in enumerate(all_keypoints):
    # Use different colors for each person
    colors = [sv.Color.RED, sv.Color.BLUE, sv.Color.GREEN, sv.Color.YELLOW]
    person_color = colors[i % len(colors)]
    
    # Create person-specific annotators
    vertex_annotator = sv.VertexAnnotator(
        color=person_color,
        radius=4
    )
    edge_annotator = sv.EdgeAnnotator(
        color=person_color,
        thickness=2
    )
    
    # Annotate each person
    image = vertex_annotator.annotate(image, person_keypoints)
    image = edge_annotator.annotate(image, person_keypoints)

# Display the result
cv2.imshow("Multi-Person Poses", image)
```

### Automatic Skeleton Detection

The EdgeAnnotator automatically detects appropriate skeleton structures based on the number of keypoints:

```python
import supervision as sv

# EdgeAnnotator will automatically select skeleton based on keypoint count
edge_annotator = sv.EdgeAnnotator(
    color=sv.Color.BLUE,
    thickness=2
    # edges=None (automatic selection)
)

# Works with different pose models:
# - 17 keypoints: COCO pose format
# - 21 keypoints: MediaPipe hand landmarks  
# - 68 keypoints: Facial landmark detection
# - Custom formats: Define your own edges

annotated_image = edge_annotator.annotate(image, keypoints)
```