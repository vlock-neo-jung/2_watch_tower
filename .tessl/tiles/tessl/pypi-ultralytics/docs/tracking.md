# Object Tracking

Multi-object tracking capabilities with BOTSORT and BYTETracker algorithms for tracking objects across video frames with persistent identity assignment.

## Capabilities

### Multi-Object Tracking

Track multiple objects across video frames while maintaining consistent identity assignments.

```python { .api }
def track(self, source, stream=False, persist=False, tracker="bytetrack.yaml", **kwargs) -> List[Results]:
    """
    Perform multi-object tracking on video input.
    
    Parameters:
    - source: Video source (file path, URL, camera index, etc.)
    - stream (bool): Process video as stream (default: False)
    - persist (bool): Persist tracks between predict calls (default: False)
    - tracker (str): Tracker configuration file ('bytetrack.yaml', 'botsort.yaml')
    - conf (float): Detection confidence threshold (default: 0.3)
    - iou (float): IoU threshold for NMS (default: 0.5)
    - imgsz (int): Image size for inference (default: 640)
    - device (str): Device to run on ('cpu', '0', etc.)
    - show (bool): Display tracking results (default: False)
    - save (bool): Save tracking results (default: False)
    - save_txt (bool): Save results as txt files (default: False)
    - save_conf (bool): Include confidence in saved results (default: False)
    - save_crop (bool): Save cropped tracked objects (default: False)
    - line_width (int): Line thickness for visualization (default: None)
    - vid_stride (int): Video frame-rate stride (default: 1)
    - **kwargs: Additional arguments
    
    Returns:
    List[Results]: Tracking results with object IDs and trajectories
    """
```

**Available Trackers:**
- **ByteTrack**: High-performance tracker focusing on association accuracy
- **BoTSORT**: Combines detection and ReID features for robust tracking

**Usage Examples:**

```python
from ultralytics import YOLO

# Load a detection model
model = YOLO("yolo11n.pt")

# Track objects in video
results = model.track(source="video.mp4", show=True, save=True)

# Track with custom tracker
results = model.track(
    source="video.mp4",
    tracker="botsort.yaml",
    conf=0.3,
    iou=0.5
)

# Track from webcam
results = model.track(source=0, show=True)

# Stream tracking with persistence
for result in model.track(source="video.mp4", stream=True, persist=True):
    # Process each frame
    if result.boxes is not None:
        track_ids = result.boxes.id.cpu().numpy() if result.boxes.id is not None else []
        boxes = result.boxes.xyxy.cpu().numpy()
        
        for track_id, box in zip(track_ids, boxes):
            print(f"Track ID: {track_id}, Box: {box}")
    
    # Display frame
    result.show()
```

### Tracking Configuration

Customize tracking behavior through YAML configuration files.

#### ByteTrack Configuration (`bytetrack.yaml`)

```yaml
tracker_type: bytetrack
track_high_thresh: 0.5    # High confidence detection threshold
track_low_thresh: 0.1     # Low confidence detection threshold  
new_track_thresh: 0.6     # New track confirmation threshold
track_buffer: 30          # Number of frames to keep lost tracks
match_thresh: 0.8         # Matching threshold for association
min_box_area: 10          # Minimum bounding box area
mot20: False              # Use MOT20 evaluation protocol
```

#### BoTSORT Configuration (`botsort.yaml`)

```yaml
tracker_type: botsort
track_high_thresh: 0.5    # High confidence detection threshold
track_low_thresh: 0.1     # Low confidence detection threshold
new_track_thresh: 0.6     # New track confirmation threshold
track_buffer: 30          # Number of frames to keep lost tracks
match_thresh: 0.8         # Matching threshold for association
gmc_method: sparseOptFlow # Global motion compensation method
proximity_thresh: 0.5     # Spatial proximity threshold
appearance_thresh: 0.25   # Appearance similarity threshold
cmc_method: sparseOptFlow # Camera motion compensation
with_reid: False          # Use ReID features
```

**Custom Tracker Configuration:**

```python
# Create custom tracker config
tracker_config = {
    'tracker_type': 'bytetrack',
    'track_high_thresh': 0.6,
    'track_low_thresh': 0.2,
    'new_track_thresh': 0.7,
    'track_buffer': 50,
    'match_thresh': 0.9
}

# Save config to YAML file
import yaml
with open('custom_tracker.yaml', 'w') as f:
    yaml.dump(tracker_config, f)

# Use custom config
results = model.track(source="video.mp4", tracker="custom_tracker.yaml")
```

### Tracking Results Processing

Access and process tracking results including object IDs and trajectories.

```python { .api }
class Results:
    def __init__(self):
        self.boxes: Optional[Boxes] = None  # Detection boxes with tracking IDs
        
class Boxes:
    def __init__(self):
        self.id: Optional[torch.Tensor] = None    # Track IDs
        self.xyxy: torch.Tensor = None            # Bounding boxes
        self.conf: torch.Tensor = None            # Confidence scores
        self.cls: torch.Tensor = None             # Class predictions
```

**Usage Examples:**

```python
# Process tracking results
results = model.track(source="video.mp4")

for frame_idx, result in enumerate(results):
    if result.boxes is not None and result.boxes.id is not None:
        # Extract tracking information
        track_ids = result.boxes.id.cpu().numpy()
        boxes = result.boxes.xyxy.cpu().numpy()
        confidences = result.boxes.conf.cpu().numpy()
        classes = result.boxes.cls.cpu().numpy()
        
        print(f"Frame {frame_idx}:")
        for i, track_id in enumerate(track_ids):
            x1, y1, x2, y2 = boxes[i]
            conf = confidences[i]
            cls = classes[i]
            
            print(f"  Track ID: {track_id}, Class: {cls}, "
                  f"Conf: {conf:.2f}, Box: [{x1:.1f}, {y1:.1f}, {x2:.1f}, {y2:.1f}]")
```

### Trajectory Analysis

Analyze object trajectories and movement patterns.

```python
class TrajectoryAnalyzer:
    def __init__(self):
        self.tracks = {}  # Store trajectory data per track ID
    
    def update(self, result):
        """Update trajectory data with new frame results."""
        if result.boxes is not None and result.boxes.id is not None:
            track_ids = result.boxes.id.cpu().numpy()
            boxes = result.boxes.xyxy.cpu().numpy()
            
            for track_id, box in zip(track_ids, boxes):
                if track_id not in self.tracks:
                    self.tracks[track_id] = []
                
                # Calculate center point
                center_x = (box[0] + box[2]) / 2
                center_y = (box[1] + box[3]) / 2
                
                self.tracks[track_id].append((center_x, center_y))
    
    def get_trajectory(self, track_id):
        """Get complete trajectory for a track ID."""
        return self.tracks.get(track_id, [])
    
    def calculate_speed(self, track_id, fps=30):
        """Calculate average speed for a track."""
        trajectory = self.get_trajectory(track_id)
        if len(trajectory) < 2:
            return 0
        
        total_distance = 0
        for i in range(1, len(trajectory)):
            dx = trajectory[i][0] - trajectory[i-1][0]
            dy = trajectory[i][1] - trajectory[i-1][1]
            distance = (dx**2 + dy**2)**0.5
            total_distance += distance
        
        # Convert to pixels per second
        time_duration = len(trajectory) / fps
        return total_distance / time_duration if time_duration > 0 else 0

# Usage example
analyzer = TrajectoryAnalyzer()
results = model.track(source="video.mp4", stream=True)

for result in results:
    analyzer.update(result)
    
    # Analyze trajectories periodically
    for track_id in analyzer.tracks:
        speed = analyzer.calculate_speed(track_id)
        trajectory = analyzer.get_trajectory(track_id)
        print(f"Track {track_id}: Speed={speed:.1f} px/s, Points={len(trajectory)}")
```

### Advanced Tracking Features

#### Region of Interest (ROI) Tracking

```python
import cv2
import numpy as np

def track_in_roi(model, source, roi_polygon):
    """Track objects only within specified region."""
    results = model.track(source=source, stream=True)
    
    for result in results:
        if result.boxes is not None and result.boxes.id is not None:
            boxes = result.boxes.xyxy.cpu().numpy()
            track_ids = result.boxes.id.cpu().numpy()
            
            for i, (track_id, box) in enumerate(zip(track_ids, boxes)):
                # Calculate center point
                center_x = (box[0] + box[2]) / 2
                center_y = (box[1] + box[3]) / 2
                
                # Check if center is inside ROI
                if cv2.pointPolygonTest(roi_polygon, (center_x, center_y), False) >= 0:
                    print(f"Track {track_id} is in ROI")

# Define ROI polygon (example: quadrilateral)
roi = np.array([[100, 100], [500, 100], [500, 400], [100, 400]], np.int32)
track_in_roi(model, "video.mp4", roi)
```

#### Cross-Line Counting

```python
class LineCounter:
    def __init__(self, line_start, line_end):
        self.line_start = line_start
        self.line_end = line_end
        self.crossed_tracks = set()
        self.count = 0
    
    def check_crossing(self, track_id, prev_center, curr_center):
        """Check if track crossed the counting line."""
        # Line crossing detection using cross product
        def ccw(A, B, C):
            return (C[1] - A[1]) * (B[0] - A[0]) > (B[1] - A[1]) * (C[0] - A[0])
        
        def intersect(A, B, C, D):
            return ccw(A, C, D) != ccw(B, C, D) and ccw(A, B, C) != ccw(A, B, D)
        
        if prev_center is not None:
            if intersect(prev_center, curr_center, self.line_start, self.line_end):
                if track_id not in self.crossed_tracks:
                    self.crossed_tracks.add(track_id)
                    self.count += 1
                    return True
        return False

# Usage example
counter = LineCounter((0, 300), (640, 300))  # Horizontal line at y=300
prev_centers = {}

results = model.track(source="video.mp4", stream=True)
for result in results:
    if result.boxes is not None and result.boxes.id is not None:
        track_ids = result.boxes.id.cpu().numpy()
        boxes = result.boxes.xyxy.cpu().numpy()
        
        for track_id, box in zip(track_ids, boxes):
            center = ((box[0] + box[2]) / 2, (box[1] + box[3]) / 2)
            
            if counter.check_crossing(track_id, prev_centers.get(track_id), center):
                print(f"Track {track_id} crossed line! Total count: {counter.count}")
            
            prev_centers[track_id] = center
```

## Types

```python { .api }
from typing import List, Optional, Dict, Tuple, Any
import torch
import numpy as np

# Tracking result types
TrackID = int
Trajectory = List[Tuple[float, float]]  # List of (x, y) center points
TrackingResults = List[Results]

# Tracker configuration types
TrackerConfig = Dict[str, Any]
TrackerType = str  # 'bytetrack' or 'botsort'

# Geometry types for ROI and line counting
Point = Tuple[float, float]
Polygon = np.ndarray  # Array of points defining polygon
Line = Tuple[Point, Point]  # Start and end points of line

# Enhanced Results class for tracking
class Results:
    boxes: Optional['Boxes']
    
class Boxes:
    id: Optional[torch.Tensor]      # Track IDs [N]
    xyxy: torch.Tensor              # Bounding boxes [N, 4]
    conf: torch.Tensor              # Confidence scores [N]
    cls: torch.Tensor               # Class predictions [N]
```