# Video Processing

Utilities for processing video streams, handling image operations, and managing video input/output workflows. Provides comprehensive tools for video analysis, frame extraction, and image manipulation.

## Capabilities

### Video Information and Metadata

Extract and manage video properties and metadata.

```python { .api }
@dataclass
class VideoInfo:
    """
    A class to store video information, including width, height, fps and total number of frames.

    Attributes:
        width (int): Width of the video in pixels
        height (int): Height of the video in pixels  
        fps (int): Frames per second of the video
        total_frames (int | None): Total number of frames in the video
    """
    width: int
    height: int
    fps: int
    total_frames: int | None = None

    @classmethod
    def from_video_path(cls, video_path: str) -> "VideoInfo":
        """Create VideoInfo from video file path."""

    @property
    def resolution_wh(self) -> tuple[int, int]:
        """Get video resolution as (width, height) tuple."""
```

### Video Output and Writing

Save processed video frames to files with flexible codec support.

```python { .api }
class VideoSink:
    """
    Context manager that saves video frames to a file using OpenCV.

    Attributes:
        target_path (str): The path to the output file where the video will be saved
        video_info (VideoInfo): Information about the video resolution, fps, and total frame count
        codec (str): FOURCC code for video format
    """
    def __init__(self, target_path: str, video_info: VideoInfo, codec: str = "mp4v") -> None: ...

    def write_frame(self, frame: np.ndarray) -> None:
        """
        Writes a single video frame to the target video file.

        Args:
            frame: The video frame to be written to the file. Must be in BGR color format
        """

    def __enter__(self): ...
    def __exit__(self, exc_type, exc_value, exc_traceback): ...
```

### Video Frame Generation

Generate frames from video files with flexible control over playback.

```python { .api }
def get_video_frames_generator(
    source_path: str,
    stride: int = 1,
    start: int = 0,
    end: int | None = None,
    iterative_seek: bool = False
) -> Generator[np.ndarray]:
    """
    Get a generator that yields the frames of the video.

    Args:
        source_path: The path of the video file
        stride: Indicates the interval at which frames are returned, skipping stride - 1 frames between each
        start: Indicates the starting position from which video should generate frames
        end: Indicates the ending position at which video should stop generating frames. If None, video will be read to the end
        iterative_seek: If True, the generator will seek to the start frame by grabbing each frame, which is much slower

    Returns:
        A generator that yields the frames of the video

    Examples:
        ```python
        import supervision as sv

        for frame in sv.get_video_frames_generator(source_path="video.mp4"):
            # Process each frame
            pass
        ```
    """
```

### Video Processing Pipeline

Process entire videos with custom callback functions.

```python { .api }
def process_video(
    source_path: str,
    target_path: str,
    callback: Callable[[np.ndarray, int], np.ndarray],
    max_frames: int | None = None,
    show_progress: bool = False
) -> None:
    """
    Process video with callback function for each frame.

    Args:
        source_path: Path to the input video file
        target_path: Path to the output video file
        callback: Function that processes each frame. Takes (frame, frame_index) and returns processed frame
        max_frames: Maximum number of frames to process. If None, processes entire video
        show_progress: Whether to show a progress bar during processing

    Examples:
        ```python
        import supervision as sv

        def callback(scene: np.ndarray, index: int) -> np.ndarray:
            # Process frame here
            return annotated_scene

        sv.process_video(
            source_path="input.mp4",
            target_path="output.mp4", 
            callback=callback,
            show_progress=True
        )
        ```
    """
```

### Performance Monitoring

Track processing frame rate and performance metrics.

```python { .api }
class FPSMonitor:
    """
    Track processing frame rate and performance.
    """
    def __init__(self, window_size: int = 30) -> None: ...

    @property
    def fps(self) -> float:
        """Get current frames per second."""

    def tick(self) -> None:
        """Record a frame processing event."""

    def reset(self) -> None:
        """Reset the FPS monitor."""
```

### Image Processing

Core image manipulation functions for computer vision workflows.

```python { .api }
class ImageSink:
    """
    Save image sequences to files with automatic naming and organization.
    """
    def __init__(
        self,
        target_dir_path: str,
        overwrite: bool = False,
        image_name_pattern: str = "image_{:05d}.png"
    ) -> None: ...

    def save_image(self, image: np.ndarray, image_name: str | None = None) -> None:
        """Save a single image to the target directory."""

def crop_image(
    image: ImageType,
    xyxy: np.ndarray | list[int] | tuple[int, int, int, int]
) -> ImageType:
    """
    Crops the given image based on the given bounding box.

    Args:
        image: The image to be cropped
        xyxy: A bounding box coordinates in format (x_min, y_min, x_max, y_max)

    Returns:
        The cropped image matching the input type

    Examples:
        ```python
        import cv2
        import supervision as sv

        image = cv2.imread("image.jpg")
        xyxy = [200, 400, 600, 800]
        cropped_image = sv.crop_image(image=image, xyxy=xyxy)
        ```
    """

def scale_image(image: ImageType, scale_factor: float) -> ImageType:
    """
    Scales the given image based on the given scale factor.

    Args:
        image: The image to be scaled
        scale_factor: The factor by which the image will be scaled

    Returns:
        The scaled image matching the input type
    """

def resize_image(
    image: ImageType,
    resolution_wh: tuple[int, int]
) -> ImageType:
    """
    Resize image to target resolution.

    Args:
        image: The image to be resized
        resolution_wh: Target resolution as (width, height)

    Returns:
        The resized image matching the input type
    """

def letterbox_image(
    image: ImageType,
    resolution_wh: tuple[int, int],
    color: tuple[int, int, int] = (114, 114, 114)
) -> ImageType:
    """
    Resize image with letterboxing (padding) to maintain aspect ratio.

    Args:
        image: The image to be letterboxed
        resolution_wh: Target resolution as (width, height)  
        color: RGB color for padding areas

    Returns:
        The letterboxed image matching the input type
    """

def overlay_image(
    background: ImageType,
    overlay: ImageType,
    anchor: Point,
    scale_factor: float = 1.0
) -> ImageType:
    """
    Overlay one image onto another at specified position.

    Args:
        background: The background image
        overlay: The image to overlay
        anchor: Position where to place the overlay
        scale_factor: Scale factor for the overlay image

    Returns:
        The combined image matching the background type
    """

def create_tiles(
    images: list[ImageType],
    grid_size: tuple[int, int] | None = None,
    single_tile_size: tuple[int, int] | None = None,
    titles: list[str] | None = None,
    titles_scale: float = 1.0,
    border_color: tuple[int, int, int] = (0, 0, 0),
    border_thickness: int = 5
) -> ImageType:
    """
    Create image tile grids for visualization.

    Args:
        images: List of images to combine into tiles
        grid_size: Grid dimensions as (columns, rows). If None, automatically determined
        single_tile_size: Size of each tile as (width, height). If None, uses original sizes
        titles: Optional list of titles for each image
        titles_scale: Scale factor for title text
        border_color: RGB color for borders between tiles
        border_thickness: Thickness of borders in pixels

    Returns:
        Combined image grid
    """
```

## Usage Examples

### Video Processing Pipeline

```python
import supervision as sv
import cv2

def process_frame(frame: np.ndarray, frame_index: int) -> np.ndarray:
    # Apply object detection
    detections = model(frame)
    
    # Annotate frame
    annotated_frame = annotator.annotate(frame, detections)
    
    return annotated_frame

# Process entire video
sv.process_video(
    source_path="input_video.mp4",
    target_path="output_video.mp4",
    callback=process_frame,
    show_progress=True
)
```

### Manual Video Processing with Performance Monitoring

```python
import supervision as sv

# Get video info
video_info = sv.VideoInfo.from_video_path("input.mp4")
fps_monitor = sv.FPSMonitor()

# Process frames manually
frames_generator = sv.get_video_frames_generator("input.mp4")

with sv.VideoSink("output.mp4", video_info) as sink:
    for frame in frames_generator:
        # Process frame
        processed_frame = your_processing_function(frame)
        
        # Write to output
        sink.write_frame(processed_frame)
        
        # Update FPS tracking
        fps_monitor.tick()
        
        print(f"Processing at {fps_monitor.fps:.1f} FPS")
```

### Image Manipulation Workflows

```python
import supervision as sv
import cv2

# Load images
image1 = cv2.imread("image1.jpg")
image2 = cv2.imread("image2.jpg")

# Crop regions of interest
bbox = [100, 100, 500, 400]
cropped = sv.crop_image(image1, bbox)

# Scale and resize operations  
scaled = sv.scale_image(image2, scale_factor=0.5)
resized = sv.resize_image(scaled, resolution_wh=(640, 480))

# Create comparison grid
images = [image1, cropped, scaled, resized]
titles = ["Original", "Cropped", "Scaled", "Resized"]

tile_grid = sv.create_tiles(
    images=images,
    titles=titles,
    grid_size=(2, 2),
    single_tile_size=(320, 240)
)

cv2.imshow("Image Processing Results", tile_grid)
cv2.waitKey(0)
```

### Video Frame Extraction

```python
import supervision as sv

# Extract every 10th frame from a video segment
frames = []
for i, frame in enumerate(sv.get_video_frames_generator(
    source_path="video.mp4",
    stride=10,      # Every 10th frame
    start=1000,     # Start at frame 1000
    end=2000        # End at frame 2000
)):
    frames.append(frame)
    if len(frames) >= 100:  # Limit to 100 frames
        break

print(f"Extracted {len(frames)} frames")

# Save frames using ImageSink
with sv.ImageSink("./extracted_frames/") as sink:
    for i, frame in enumerate(frames):
        sink.save_image(frame, f"frame_{i:05d}.jpg")
```