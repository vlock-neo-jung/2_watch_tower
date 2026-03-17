# Detection Tools

Spatial analysis tools for counting, tracking, and analyzing objects within defined regions. These tools enable zone-based analytics like counting objects crossing lines or entering specific areas.

## Capabilities

### Zone-Based Detection

Tools for defining spatial regions and detecting object interactions with those zones.

```python { .api }
class LineZone:
    """
    Count objects crossing a predefined line.
    
    Attributes:
        in_count (int): Objects crossed from outside to inside
        out_count (int): Objects crossed from inside to outside
        in_count_per_class (dict[int, int]): Per-class inside crossings
        out_count_per_class (dict[int, int]): Per-class outside crossings
    
    Args:
        start (Point): Line starting point
        end (Point): Line ending point
        triggering_anchors (Iterable[Position]): Detection anchors to consider
        minimum_crossing_threshold (int): Frames required to confirm crossing
    """
    def __init__(
        self,
        start: Point,
        end: Point,
        triggering_anchors: Iterable[Position] = (
            Position.TOP_LEFT,
            Position.TOP_RIGHT,
            Position.BOTTOM_LEFT,
            Position.BOTTOM_RIGHT,
        ),
        minimum_crossing_threshold: int = 1,
    ): ...

    def trigger(self, detections: Detections) -> tuple[np.ndarray, np.ndarray]:
        """
        Update line zone with new detections.
        
        Args:
            detections (Detections): Current frame detections with tracker_id
            
        Returns:
            tuple[np.ndarray, np.ndarray]: (crossed_in, crossed_out) boolean arrays
        """

class PolygonZone:
    """
    Define polygon-shaped zones for object detection and counting.
    
    Attributes:
        polygon (np.ndarray): Zone polygon coordinates, shape (N, 2)
        triggering_anchors (Iterable[Position]): Detection anchors to consider
        current_count (int): Current objects within zone
        mask (np.ndarray): 2D boolean mask for the zone
    
    Args:
        polygon (np.ndarray): Polygon vertices as (x, y) coordinates
        triggering_anchors (Iterable[Position]): Detection anchor points
    """
    def __init__(
        self,
        polygon: np.ndarray,
        triggering_anchors: Iterable[Position] = (Position.BOTTOM_CENTER,),
    ): ...

    def trigger(self, detections: Detections) -> np.ndarray:
        """
        Check which detections are within the polygon zone.
        
        Args:
            detections (Detections): Detections to check
            
        Returns:
            np.ndarray: Boolean array indicating detections within zone
        """
```

### Zone Visualization

Annotators for visualizing zones and their status.

```python { .api }
class LineZoneAnnotator:
    """
    Visualize LineZone with crossing counts.
    
    Args:
        thickness (int): Line thickness in pixels
        color (Color): Line color
        text_thickness (int): Text thickness
        text_color (Color): Text color
        text_scale (float): Text size scaling
        text_offset (float): Text position offset from line
        text_padding (int): Text background padding
        custom_in_text (str | None): Custom text for in count
        custom_out_text (str | None): Custom text for out count
        display_in_count (bool): Whether to show in count
        display_out_count (bool): Whether to show out count
    """
    def __init__(
        self,
        thickness: int = 2,
        color: Color = Color.WHITE,
        text_thickness: int = 2,
        text_color: Color = Color.BLACK,
        text_scale: float = 0.5,
        text_offset: float = 1.5,
        text_padding: int = 10,
        custom_in_text: str | None = None,
        custom_out_text: str | None = None,
        display_in_count: bool = True,
        display_out_count: bool = True,
    ): ...

    def annotate(self, frame: np.ndarray, line_counter: LineZone) -> np.ndarray:
        """Draw line zone with counts on frame."""

class LineZoneAnnotatorMulticlass:
    """Multi-class version of LineZoneAnnotator with per-class counting."""

class PolygonZoneAnnotator:
    """
    Visualize PolygonZone with object counts.
    
    Args:
        color (Color): Zone boundary color
        thickness (int): Boundary line thickness
        text_color (Color): Count text color
        text_scale (float): Text size scaling
        text_thickness (int): Text thickness
        text_padding (int): Text background padding
        display_in_zone (bool): Whether to show objects in zone count
    """
    def __init__(
        self,
        color: Color = Color.RED,
        thickness: int = 2,
        text_color: Color = Color.WHITE,
        text_scale: float = 0.5,
        text_thickness: int = 1,
        text_padding: int = 10,
        display_in_zone: bool = True,
    ): ...

    def annotate(self, scene: np.ndarray, zone: PolygonZone, label: str | None = None) -> np.ndarray:
        """Draw polygon zone with count on scene."""
```

### Processing and Analysis Tools

Tools for advanced detection processing and analysis.

```python { .api }
class InferenceSlicer:
    """
    Slice large images into smaller tiles for inference, then reconstruct results.
    
    Useful for processing high-resolution images that exceed model input limitations.
    
    Args:
        slice_wh (tuple[int, int]): Slice dimensions (width, height)
        overlap_ratio_wh (tuple[float, float]): Overlap ratios (width, height)
        iou_threshold (float): IoU threshold for NMS across slices
        callback (callable): Inference callback function
        thread_workers (int): Number of worker threads
    """
    def __init__(
        self,
        slice_wh: tuple[int, int] = (320, 320),
        overlap_ratio_wh: tuple[float, float] = (0.2, 0.2),
        iou_threshold: float = 0.5,
        callback: callable = None,
        thread_workers: int = 1,
    ): ...

    def __call__(self, image: np.ndarray) -> Detections:
        """Process image through slicing and return merged detections."""

class DetectionsSmoother:
    """
    Smooth detection results over time to reduce jitter and noise.
    
    Args:
        length (int): Number of frames to smooth over
    """
    def __init__(self, length: int): ...

    def update_with_detections(self, detections: Detections) -> Detections:
        """
        Update smoother with new detections and return smoothed results.
        
        Args:
            detections (Detections): Current frame detections
            
        Returns:
            Detections: Smoothed detections
        """
```

### Data Export Tools

Tools for exporting detection results to various formats.

```python { .api }
class CSVSink:
    """
    Export detection results to CSV format.
    
    Args:
        file_name (str): Output CSV file path
        overwrite (bool): Whether to overwrite existing file
    """
    def __init__(self, file_name: str, overwrite: bool = True): ...

    def append(self, detections: Detections, custom_data: dict = None) -> None:
        """Add detection results to CSV file."""

    def __enter__(self) -> "CSVSink": ...
    def __exit__(self, exc_type, exc_val, exc_tb) -> None: ...

class JSONSink:
    """
    Export detection results to JSON format.
    
    Args:
        file_name (str): Output JSON file path
        overwrite (bool): Whether to overwrite existing file
    """
    def __init__(self, file_name: str, overwrite: bool = True): ...

    def append(self, detections: Detections, custom_data: dict = None) -> None:
        """Add detection results to JSON file."""

    def __enter__(self) -> "JSONSink": ...
    def __exit__(self, exc_type, exc_val, exc_tb) -> None: ...
```

## Usage Examples

### Line Crossing Counter

```python
import supervision as sv
from ultralytics import YOLO

# Setup model and tracker
model = YOLO("yolov8n.pt")
tracker = sv.ByteTrack()

# Define line zone
start = sv.Point(x=0, y=400)
end = sv.Point(x=1280, y=400)
line_zone = sv.LineZone(start=start, end=end)
line_annotator = sv.LineZoneAnnotator()

# Process video frames
for frame in sv.get_video_frames_generator("video.mp4"):
    # Run inference and tracking
    results = model(frame)[0]
    detections = sv.Detections.from_ultralytics(results)
    detections = tracker.update_with_detections(detections)
    
    # Update line zone
    crossed_in, crossed_out = line_zone.trigger(detections)
    
    # Annotate frame
    annotated_frame = line_annotator.annotate(frame, line_zone)
    
    print(f"In: {line_zone.in_count}, Out: {line_zone.out_count}")
```

### Polygon Zone Analysis

```python
import supervision as sv
import numpy as np

# Define polygon zone
polygon = np.array([
    [100, 200],
    [300, 200], 
    [400, 400],
    [100, 400]
])

zone = sv.PolygonZone(polygon=polygon)
zone_annotator = sv.PolygonZoneAnnotator()

# Process detections
for frame in frames:
    detections = get_detections(frame)  # Your detection logic
    
    # Check zone occupancy
    in_zone = zone.trigger(detections)
    
    # Annotate
    annotated_frame = zone_annotator.annotate(frame, zone)
    
    print(f"Objects in zone: {zone.current_count}")
```

### High-Resolution Image Processing

```python
import supervision as sv

def yolo_callback(image_slice: np.ndarray) -> sv.Detections:
    """Callback for processing image slices."""
    results = model(image_slice)[0]
    return sv.Detections.from_ultralytics(results)

# Setup slicer for large images
slicer = sv.InferenceSlicer(
    slice_wh=(640, 640),
    overlap_ratio_wh=(0.2, 0.2),
    iou_threshold=0.5,
    callback=yolo_callback
)

# Process large image
large_image = cv2.imread("large_image.jpg")
detections = slicer(large_image)
```

### Export Detection Results

```python
import supervision as sv

# Export to CSV
with sv.CSVSink("detections.csv") as csv_sink:
    for frame_idx, detections in enumerate(detection_stream):
        csv_sink.append(detections, custom_data={"frame": frame_idx})

# Export to JSON  
with sv.JSONSink("detections.json") as json_sink:
    for frame_idx, detections in enumerate(detection_stream):
        json_sink.append(detections, custom_data={"frame": frame_idx})
```

## Types

```python { .api }
# Zone trigger results
ZoneTriggerResult = np.ndarray  # Boolean array indicating detections in zone
LineCrossingResult = tuple[np.ndarray, np.ndarray]  # (crossed_in, crossed_out)

# Callback function signature for InferenceSlicer
InferenceCallback = Callable[[np.ndarray], Detections]
```