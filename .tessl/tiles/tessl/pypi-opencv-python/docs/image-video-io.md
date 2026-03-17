# Image and Video I/O

OpenCV provides comprehensive functionality for reading and writing images and videos through its `imgcodecs` and `videoio` modules. All functions and classes are accessible directly from the `cv2` namespace, supporting a wide variety of image formats (JPEG, PNG, TIFF, BMP, etc.) and video codecs.

## Capabilities

### Image Reading

Read images from files using various formats and loading modes.

```python { .api }
cv2.imread(filename: str, flags: int = cv2.IMREAD_COLOR) -> np.ndarray | None
```

Loads an image from the specified file.

**Parameters:**
- `filename` (str): Path to the image file
- `flags` (int, optional): Read mode flag. Defaults to `cv2.IMREAD_COLOR`
  - `cv2.IMREAD_COLOR` - Load as 3-channel BGR color image (default)
  - `cv2.IMREAD_GRAYSCALE` - Load as single-channel grayscale image
  - `cv2.IMREAD_UNCHANGED` - Load image with alpha channel if present
  - `cv2.IMREAD_ANYDEPTH` - Load 16-bit or 32-bit image when available
  - `cv2.IMREAD_ANYCOLOR` - Load in any color format available
  - `cv2.IMREAD_REDUCED_GRAYSCALE_2` - Load as grayscale at 1/2 size
  - `cv2.IMREAD_REDUCED_GRAYSCALE_4` - Load as grayscale at 1/4 size
  - `cv2.IMREAD_REDUCED_GRAYSCALE_8` - Load as grayscale at 1/8 size
  - `cv2.IMREAD_REDUCED_COLOR_2` - Load as color at 1/2 size
  - `cv2.IMREAD_REDUCED_COLOR_4` - Load as color at 1/4 size
  - `cv2.IMREAD_REDUCED_COLOR_8` - Load as color at 1/8 size

**Returns:**
- `np.ndarray | None`: Image as NumPy array in BGR format, or `None` if reading failed

**Example:**
```python
import cv2

# Read color image
img = cv2.imread('photo.jpg')

# Read as grayscale
gray = cv2.imread('photo.jpg', cv2.IMREAD_GRAYSCALE)

# Read with alpha channel
rgba = cv2.imread('logo.png', cv2.IMREAD_UNCHANGED)

# Read at reduced resolution
small = cv2.imread('large.jpg', cv2.IMREAD_REDUCED_COLOR_2)
```

---

```python { .api }
cv2.imdecode(buf: np.ndarray, flags: int) -> np.ndarray | None
```

Decodes an image from a memory buffer.

**Parameters:**
- `buf` (np.ndarray): Input byte array containing encoded image data
- `flags` (int): Read mode flag (same as `cv2.imread()`)

**Returns:**
- `np.ndarray | None`: Decoded image as NumPy array, or `None` if decoding failed

**Example:**
```python
import cv2
import numpy as np

# Read image file as bytes
with open('image.jpg', 'rb') as f:
    img_bytes = f.read()

# Decode from bytes
buf = np.frombuffer(img_bytes, dtype=np.uint8)
img = cv2.imdecode(buf, cv2.IMREAD_COLOR)
```

---

```python { .api }
cv2.imreadmulti(filename: str, mats: list, flags: int = cv2.IMREAD_ANYCOLOR) -> tuple[bool, list]
```

Loads a multi-page image from a file.

**Parameters:**
- `filename` (str): Name of file to be loaded
- `mats` (list): Output vector of Mat objects holding each page
- `flags` (int, optional): Flag that can take values of ImreadModes. Defaults to `cv2.IMREAD_ANYCOLOR`

**Returns:**
- `tuple[bool, list]`: Tuple of (success flag, list of images). Returns `True` if successful, `False` otherwise. Useful for reading multi-page TIFF files or animated image formats

**Example:**
```python
import cv2

# Read multi-page TIFF
success, images = cv2.imreadmulti('multipage.tiff', [], cv2.IMREAD_ANYCOLOR)
if success:
    print(f'Read {len(images)} pages')
    for i, img in enumerate(images):
        cv2.imshow(f'Page {i}', img)
```

**Alternative with range:**
```python { .api }
cv2.imreadmulti(filename: str, mats: list, start: int, count: int, flags: int = cv2.IMREAD_ANYCOLOR) -> tuple[bool, list]
```

Loads images of a multi-page image from a file with specified range.

**Parameters:**
- `filename` (str): Name of file to be loaded
- `mats` (list): Output vector of Mat objects holding each page
- `start` (int): Start index of the image to load
- `count` (int): Count number of images to load
- `flags` (int, optional): Flag that can take values of ImreadModes

**Returns:**
- `tuple[bool, list]`: Tuple of (success flag, list of images)

---

```python { .api }
cv2.imcount(filename: str, flags: int = cv2.IMREAD_ANYCOLOR) -> int
```

Returns the number of images inside the given file.

**Parameters:**
- `filename` (str): Name of file to be loaded
- `flags` (int, optional): Flag that can take values of ImreadModes. Defaults to `cv2.IMREAD_ANYCOLOR`

**Returns:**
- `int`: Number of images/pages/frames in the file. Returns the number of pages in a multi-page image (e.g. TIFF), the number of frames in an animation (e.g. AVIF), and 1 otherwise. If the image cannot be decoded, 0 is returned

**Example:**
```python
import cv2

# Check number of pages in TIFF file
num_pages = cv2.imcount('multipage.tiff')
print(f'File contains {num_pages} pages')

# Read only if multiple pages exist
if num_pages > 1:
    success, images = cv2.imreadmulti('multipage.tiff', [])
```

---

```python { .api }
cv2.haveImageReader(filename: str) -> bool
```

Checks if an image reader for the specified format is available.

**Parameters:**
- `filename` (str): File path or filename with extension

**Returns:**
- `bool`: `True` if reader is available, `False` otherwise

**Example:**
```python
if cv2.haveImageReader('test.webp'):
    img = cv2.imread('test.webp')
```

### Image Writing

Write images to files with format-specific parameters.

```python { .api }
cv2.imwrite(filename: str, img: np.ndarray, params: list[int] = None) -> bool
```

Saves an image to a file. The format is determined by the file extension.

**Parameters:**
- `filename` (str): Path to save the image file
- `img` (np.ndarray): Image array to save
- `params` (list[int], optional): Format-specific parameters as list of (flag, value) pairs
  - `cv2.IMWRITE_JPEG_QUALITY` - JPEG quality (0-100, default 95)
  - `cv2.IMWRITE_PNG_COMPRESSION` - PNG compression level (0-9, default 3)
  - Additional codec-specific parameters available

**Returns:**
- `bool`: `True` if successful, `False` otherwise

**Example:**
```python
import cv2

img = cv2.imread('input.png')

# Save as JPEG with quality 90
cv2.imwrite('output.jpg', img, [cv2.IMWRITE_JPEG_QUALITY, 90])

# Save as PNG with maximum compression
cv2.imwrite('output.png', img, [cv2.IMWRITE_PNG_COMPRESSION, 9])

# Save with default settings
cv2.imwrite('output.bmp', img)
```

---

```python { .api }
cv2.imencode(ext: str, img: np.ndarray, params: list[int] = None) -> tuple[bool, np.ndarray]
```

Encodes an image into a memory buffer.

**Parameters:**
- `ext` (str): File extension defining output format (e.g., '.jpg', '.png')
- `img` (np.ndarray): Image array to encode
- `params` (list[int], optional): Format-specific parameters (same as `cv2.imwrite()`)

**Returns:**
- `tuple[bool, np.ndarray]`: Tuple of (success, encoded_buffer)
  - `success` (bool): `True` if encoding succeeded
  - `encoded_buffer` (np.ndarray): Encoded image as byte array

**Example:**
```python
import cv2

img = cv2.imread('photo.jpg')

# Encode as JPEG
success, buffer = cv2.imencode('.jpg', img, [cv2.IMWRITE_JPEG_QUALITY, 85])

if success:
    # Write buffer to file
    with open('encoded.jpg', 'wb') as f:
        f.write(buffer.tobytes())

    # Or send over network
    # socket.send(buffer.tobytes())
```

---

```python { .api }
cv2.haveImageWriter(filename: str) -> bool
```

Checks if an image writer for the specified format is available.

**Parameters:**
- `filename` (str): File path or filename with extension

**Returns:**
- `bool`: `True` if writer is available, `False` otherwise

**Example:**
```python
if cv2.haveImageWriter('output.jp2'):
    cv2.imwrite('output.jp2', img)
else:
    cv2.imwrite('output.jpg', img)
```

### Video Capture

The `VideoCapture` class provides functionality for capturing video from files or cameras.

```python { .api }
class cv2.VideoCapture:
    def __init__(self, index: int | str, apiPreference: int = cv2.CAP_ANY)
```

Creates a video capture object for reading from a camera or video file.

**Parameters:**
- `index` (int | str): Device index (0, 1, 2, ...) or video file path
- `apiPreference` (int, optional): Preferred capture API backend

**Example:**
```python
import cv2

# Open default camera
cap = cv2.VideoCapture(0)

# Open video file
cap = cv2.VideoCapture('video.mp4')

# Open camera with specific API
cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)  # DirectShow on Windows
```

---

```python { .api }
VideoCapture.isOpened(self) -> bool
```

Checks if video capture has been initialized successfully.

**Returns:**
- `bool`: `True` if capture is opened, `False` otherwise

**Example:**
```python
cap = cv2.VideoCapture('video.mp4')
if not cap.isOpened():
    print("Error opening video file")
```

---

```python { .api }
VideoCapture.read(self) -> tuple[bool, np.ndarray]
```

Grabs, decodes, and returns the next video frame.

**Returns:**
- `tuple[bool, np.ndarray]`: Tuple of (success, frame)
  - `success` (bool): `True` if frame was read successfully
  - `frame` (np.ndarray): Decoded frame image

**Example:**
```python
cap = cv2.VideoCapture('video.mp4')

while True:
    ret, frame = cap.read()
    if not ret:
        break

    cv2.imshow('Frame', frame)
    if cv2.waitKey(25) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
```

---

```python { .api }
VideoCapture.grab(self) -> bool
```

Grabs the next frame from video source without decoding.

**Returns:**
- `bool`: `True` if frame was grabbed successfully

**Note:** Use with `retrieve()` for fine-grained control over frame capture. Useful when synchronizing multiple cameras.

---

```python { .api }
VideoCapture.retrieve(self, image: np.ndarray = None, flag: int = 0) -> tuple[bool, np.ndarray]
```

Decodes and returns the grabbed video frame.

**Parameters:**
- `image` (np.ndarray, optional): Pre-allocated array for output
- `flag` (int, optional): Channel selection flag

**Returns:**
- `tuple[bool, np.ndarray]`: Tuple of (success, frame)

**Example:**
```python
# Fine-grained frame capture
cap1 = cv2.VideoCapture(0)
cap2 = cv2.VideoCapture(1)

# Synchronize capture
grabbed1 = cap1.grab()
grabbed2 = cap2.grab()

if grabbed1 and grabbed2:
    ret1, frame1 = cap1.retrieve()
    ret2, frame2 = cap2.retrieve()
```

---

```python { .api }
VideoCapture.get(self, propId: int) -> float
```

Gets a video capture property value.

**Parameters:**
- `propId` (int): Property identifier (see Video Capture Properties section)

**Returns:**
- `float`: Property value

**Example:**
```python
cap = cv2.VideoCapture('video.mp4')

# Get video properties
width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
fps = cap.get(cv2.CAP_PROP_FPS)
frame_count = cap.get(cv2.CAP_PROP_FRAME_COUNT)

print(f"Video: {width}x{height} @ {fps} fps, {frame_count} frames")
```

---

```python { .api }
VideoCapture.set(self, propId: int, value: float) -> bool
```

Sets a video capture property.

**Parameters:**
- `propId` (int): Property identifier
- `value` (float): New property value

**Returns:**
- `bool`: `True` if property was set successfully

**Example:**
```python
cap = cv2.VideoCapture(0)

# Set camera resolution
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)

# Set camera FPS
cap.set(cv2.CAP_PROP_FPS, 30)

# Jump to specific frame in video file
cap.set(cv2.CAP_PROP_POS_FRAMES, 100)
```

---

```python { .api }
VideoCapture.release(self) -> None
```

Closes video file or capturing device and releases resources.

**Example:**
```python
cap = cv2.VideoCapture('video.mp4')
# ... process video ...
cap.release()
```

### Video Capture Properties

Property constants for use with `VideoCapture.get()` and `VideoCapture.set()`.

```python { .api }
# Position properties
cv2.CAP_PROP_POS_MSEC       # Current position in milliseconds
cv2.CAP_PROP_POS_FRAMES     # 0-based index of next frame
cv2.CAP_PROP_POS_AVI_RATIO  # Relative position (0.0 to 1.0)

# Frame properties
cv2.CAP_PROP_FRAME_WIDTH    # Width of frames
cv2.CAP_PROP_FRAME_HEIGHT   # Height of frames
cv2.CAP_PROP_FPS            # Frame rate (frames per second)
cv2.CAP_PROP_FOURCC         # 4-character codec code
cv2.CAP_PROP_FRAME_COUNT    # Total number of frames

# Camera properties
cv2.CAP_PROP_BRIGHTNESS     # Brightness setting
cv2.CAP_PROP_CONTRAST       # Contrast setting
cv2.CAP_PROP_SATURATION     # Saturation setting
cv2.CAP_PROP_HUE            # Hue setting
cv2.CAP_PROP_GAIN           # Gain setting
cv2.CAP_PROP_EXPOSURE       # Exposure setting

# Auto settings
cv2.CAP_PROP_AUTOFOCUS      # Auto-focus enable (0 or 1)
cv2.CAP_PROP_AUTO_EXPOSURE  # Auto-exposure mode
```

**Example:**
```python
import cv2

cap = cv2.VideoCapture('video.mp4')

# Read video metadata
properties = {
    'Width': cap.get(cv2.CAP_PROP_FRAME_WIDTH),
    'Height': cap.get(cv2.CAP_PROP_FRAME_HEIGHT),
    'FPS': cap.get(cv2.CAP_PROP_FPS),
    'Frame Count': cap.get(cv2.CAP_PROP_FRAME_COUNT),
    'FourCC': int(cap.get(cv2.CAP_PROP_FOURCC)),
}

# Navigate video
current_frame = cap.get(cv2.CAP_PROP_POS_FRAMES)
cap.set(cv2.CAP_PROP_POS_FRAMES, current_frame + 100)  # Skip 100 frames

# Seek by time
cap.set(cv2.CAP_PROP_POS_MSEC, 5000)  # Jump to 5 seconds
```

### Video Writing

The `VideoWriter` class enables writing video files with various codecs.

```python { .api }
class cv2.VideoWriter:
    def __init__(self, filename: str, fourcc: int, fps: float,
                 frameSize: tuple[int, int], isColor: bool = True)
```

Creates a video writer object.

**Parameters:**
- `filename` (str): Output video file path
- `fourcc` (int): 4-character codec code (use `cv2.VideoWriter_fourcc()`)
- `fps` (float): Frame rate of output video
- `frameSize` (tuple[int, int]): Frame size as (width, height)
- `isColor` (bool, optional): If `True`, write color frames; if `False`, grayscale

**Example:**
```python
import cv2

# Create video writer for MP4 file
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
out = cv2.VideoWriter('output.mp4', fourcc, 30.0, (640, 480))

# Create grayscale video writer
out_gray = cv2.VideoWriter('output.avi', fourcc, 25.0, (640, 480), False)
```

---

```python { .api }
VideoWriter.isOpened(self) -> bool
```

Checks if video writer has been initialized successfully.

**Returns:**
- `bool`: `True` if writer is ready, `False` otherwise

**Example:**
```python
fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter('output.avi', fourcc, 20.0, (640, 480))

if not out.isOpened():
    print("Error: Could not open video writer")
```

---

```python { .api }
VideoWriter.write(self, image: np.ndarray) -> None
```

Writes a frame to the video file.

**Parameters:**
- `image` (np.ndarray): Frame to write (must match size and color format)

**Example:**
```python
import cv2
import numpy as np

fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter('output.avi', fourcc, 20.0, (640, 480))

# Write frames
for i in range(100):
    # Create or capture frame
    frame = np.random.randint(0, 255, (480, 640, 3), dtype=np.uint8)
    out.write(frame)

out.release()
```

---

```python { .api }
VideoWriter.release(self) -> None
```

Closes the video writer and finalizes the output file.

**Example:**
```python
out = cv2.VideoWriter('output.avi', fourcc, 20.0, (640, 480))
# ... write frames ...
out.release()  # Important: finalizes the video file
```

---

```python { .api }
VideoWriter.get(self, propId: int) -> float
```

Gets a video writer property value.

**Parameters:**
- `propId` (int): Property identifier

**Returns:**
- `float`: Property value

---

```python { .api }
VideoWriter.set(self, propId: int, value: float) -> bool
```

Sets a video writer property.

**Parameters:**
- `propId` (int): Property identifier
- `value` (float): New property value

**Returns:**
- `bool`: `True` if successful

### Video Codec Selection

```python { .api }
cv2.VideoWriter_fourcc(c1: str, c2: str, c3: str, c4: str) -> int
```

Creates a 4-character code (FourCC) for specifying video codecs.

**Parameters:**
- `c1, c2, c3, c4` (str): Four characters identifying the codec

**Returns:**
- `int`: FourCC code as integer

**Common Codecs:**
```python
# XVID (AVI container)
fourcc = cv2.VideoWriter_fourcc(*'XVID')

# MJPEG (AVI container)
fourcc = cv2.VideoWriter_fourcc(*'MJPG')

# H264 (MP4 container)
fourcc = cv2.VideoWriter_fourcc(*'H264')
fourcc = cv2.VideoWriter_fourcc(*'X264')

# MP4V (MP4 container)
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
fourcc = cv2.VideoWriter_fourcc(*'MP4V')

# FFV1 (lossless, AVI/MKV container)
fourcc = cv2.VideoWriter_fourcc(*'FFV1')

# Uncompressed (very large files)
fourcc = cv2.VideoWriter_fourcc(*'RGBA')

# Windows Media Video
fourcc = cv2.VideoWriter_fourcc(*'WMV1')
fourcc = cv2.VideoWriter_fourcc(*'WMV2')

# Motion JPEG 2000
fourcc = cv2.VideoWriter_fourcc(*'MJ2C')

# Platform-specific default
fourcc = cv2.VideoWriter_fourcc(*'DIVX')  # Windows
fourcc = cv2.VideoWriter_fourcc(*'avc1')  # macOS
```

**Example:**
```python
import cv2

cap = cv2.VideoCapture(0)
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

# Create writer with XVID codec
fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter('recording.avi', fourcc, 20.0, (width, height))

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Process frame
    out.write(frame)

    cv2.imshow('Recording', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
out.release()
cv2.destroyAllWindows()
```

### Complete Video Processing Example

```python
import cv2

# Read from video file
input_video = cv2.VideoCapture('input.mp4')

# Get video properties
fps = input_video.get(cv2.CAP_PROP_FPS)
width = int(input_video.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(input_video.get(cv2.CAP_PROP_FRAME_HEIGHT))
total_frames = int(input_video.get(cv2.CAP_PROP_FRAME_COUNT))

print(f"Processing video: {width}x{height} @ {fps} fps, {total_frames} frames")

# Create video writer
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
output_video = cv2.VideoWriter('output.mp4', fourcc, fps, (width, height))

if not output_video.isOpened():
    print("Error: Could not create output video")
    input_video.release()
    exit()

# Process each frame
frame_count = 0
while True:
    ret, frame = input_video.read()
    if not ret:
        break

    # Apply processing (example: convert to grayscale and back to BGR)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    processed = cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)

    # Write processed frame
    output_video.write(processed)

    frame_count += 1
    if frame_count % 30 == 0:
        print(f"Processed {frame_count}/{total_frames} frames")

# Release resources
input_video.release()
output_video.release()

print(f"Video processing complete: {frame_count} frames written")
```

### Camera Capture Example

```python
import cv2

# Open default camera
cap = cv2.VideoCapture(0)

# Set camera properties
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
cap.set(cv2.CAP_PROP_FPS, 30)

# Optional: adjust camera settings
cap.set(cv2.CAP_PROP_BRIGHTNESS, 128)
cap.set(cv2.CAP_PROP_CONTRAST, 128)
cap.set(cv2.CAP_PROP_SATURATION, 128)

if not cap.isOpened():
    print("Error: Could not open camera")
    exit()

# Get actual properties (may differ from requested)
actual_width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
actual_height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
actual_fps = cap.get(cv2.CAP_PROP_FPS)

print(f"Camera: {actual_width}x{actual_height} @ {actual_fps} fps")

# Create video writer for recording
fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter('camera_recording.avi', fourcc, actual_fps,
                      (int(actual_width), int(actual_height)))

recording = False

while True:
    ret, frame = cap.read()
    if not ret:
        print("Error: Failed to capture frame")
        break

    # Display recording status
    if recording:
        cv2.putText(frame, "REC", (10, 30), cv2.FONT_HERSHEY_SIMPLEX,
                    1, (0, 0, 255), 2)
        out.write(frame)

    cv2.imshow('Camera', frame)

    # Handle keyboard input
    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        break
    elif key == ord('r'):
        recording = not recording
        print("Recording:", "ON" if recording else "OFF")
    elif key == ord('s'):
        # Save snapshot
        cv2.imwrite('snapshot.jpg', frame, [cv2.IMWRITE_JPEG_QUALITY, 95])
        print("Snapshot saved")

# Release resources
cap.release()
out.release()
cv2.destroyAllWindows()
```
