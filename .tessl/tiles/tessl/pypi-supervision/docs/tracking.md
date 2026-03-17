# Tracking

Multi-object tracking algorithms for maintaining object identities across video frames.

## Capabilities

### ByteTrack Algorithm

```python { .api }
class ByteTrack:
    """
    Multi-object tracking using the ByteTracker algorithm.
    
    Args:
        track_thresh (float): Detection confidence threshold for tracking
        track_buffer (int): Number of frames to keep lost tracks
        match_thresh (float): Matching threshold for track association
        frame_rate (int): Video frame rate for track management
    """
    def __init__(
        self,
        track_thresh: float = 0.25,
        track_buffer: int = 30,
        match_thresh: float = 0.8,
        frame_rate: int = 30,
    ): ...

    def update_with_detections(self, detections: Detections) -> Detections:
        """
        Update tracker with new detections and return tracked results.
        
        Args:
            detections (Detections): Current frame detections
            
        Returns:
            Detections: Detections with assigned tracker_id values
        """
```

## Usage Example

```python
import supervision as sv
from ultralytics import YOLO

# Setup model and tracker
model = YOLO("yolov8n.pt") 
tracker = sv.ByteTrack()

# Process video frames
for frame in sv.get_video_frames_generator("video.mp4"):
    # Get detections
    results = model(frame)[0]
    detections = sv.Detections.from_ultralytics(results)
    
    # Update tracker
    detections = tracker.update_with_detections(detections)
    
    # Now detections have tracker_id assigned
    print("Tracked objects:", len(detections))
```