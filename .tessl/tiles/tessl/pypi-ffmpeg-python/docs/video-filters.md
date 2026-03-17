# Video Filters

Essential video processing filters including geometric transformations, visual effects, overlays, cropping, and drawing operations for comprehensive video manipulation.

## Capabilities

### Geometric Transformations

Basic video transformations for flipping and rotating video content.

```python { .api }
def hflip(stream) -> Stream:
    """
    Flip the input video horizontally.
    
    Parameters:
    - stream: Stream, input video stream
    
    Returns:
    Stream object with horizontal flip applied
    """

def vflip(stream) -> Stream:
    """
    Flip the input video vertically.
    
    Parameters:
    - stream: Stream, input video stream
    
    Returns:
    Stream object with vertical flip applied
    """
```

**Usage Example:**
```python
# Horizontal flip
flipped = ffmpeg.input('input.mp4').hflip()

# Vertical flip
vertically_flipped = ffmpeg.input('input.mp4').vflip()

# Both flips (180-degree rotation)
rotated = ffmpeg.input('input.mp4').hflip().vflip()
```

### Video Cropping

Extract specific rectangular regions from video frames.

```python { .api }
def crop(stream, x: int, y: int, width: int, height: int, **kwargs) -> Stream:
    """
    Crop the input video to a rectangular region.
    
    Parameters:
    - stream: Stream, input video stream
    - x: int, horizontal position of left edge in input video
    - y: int, vertical position of top edge in input video  
    - width: int, width of output video (must be > 0)
    - height: int, height of output video (must be > 0)
    - Additional FFmpeg crop filter options as keyword arguments
    
    Returns:
    Stream object with cropping applied
    """
```

**Usage Example:**
```python
# Crop to center 640x480 region of 1920x1080 video
cropped = ffmpeg.input('fullhd.mp4').crop(640, 300, 640, 480)

# Top-left corner crop
corner = ffmpeg.input('input.mp4').crop(0, 0, 320, 240)
```

### Video Overlays

Composite multiple video streams by overlaying one video on top of another.

```python { .api }
def overlay(main_stream, overlay_stream, eof_action: str = 'repeat', **kwargs) -> Stream:
    """
    Overlay one video on top of another.
    
    Parameters:
    - main_stream: Stream, main background video
    - overlay_stream: Stream, video to overlay on top
    - eof_action: str, action when overlay ends ('repeat', 'endall', 'pass')
    - x: int/str, x position expression for overlay (default: 0)
    - y: int/str, y position expression for overlay (default: 0)
    - eval: str, when to evaluate position expressions ('init', 'frame')
    - shortest: int, terminate when shortest input ends (0/1)
    - format: str, output pixel format ('yuv420', 'yuv422', 'yuv444', 'rgb', 'gbrp')
    - repeatlast: int, repeat last overlay frame (0/1, default: 1)
    
    Returns:
    Stream object with overlay applied
    """
```

**Usage Example:**
```python
main_video = ffmpeg.input('background.mp4')
watermark = ffmpeg.input('logo.png')

# Simple overlay at top-left
overlaid = main_video.overlay(watermark)

# Positioned overlay with transparency
positioned = main_video.overlay(
    watermark,
    x=10,
    y=10,
    eof_action='pass'
)

# Complex positioning using expressions
centered = main_video.overlay(
    watermark,
    x='(main_w-overlay_w)/2',
    y='(main_h-overlay_h)/2'
)
```

### Drawing Operations

Add graphical elements like boxes and text directly onto video frames.

```python { .api }
def drawbox(stream, x: int, y: int, width: int, height: int, color: str, thickness: int = None, **kwargs) -> Stream:
    """
    Draw a colored box on the input video.
    
    Parameters:
    - stream: Stream, input video stream
    - x: int, x coordinate of box top-left corner
    - y: int, y coordinate of box top-left corner  
    - width: int, box width (0 = input width)
    - height: int, box height (0 = input height)
    - color: str, box color (color name, hex, or 'invert')
    - thickness: int, box edge thickness (default: 3)
    - w: int, alias for width
    - h: int, alias for height
    - c: str, alias for color
    - t: int, alias for thickness
    
    Returns:
    Stream object with box drawn
    """

def drawtext(stream, text: str = None, x: int = 0, y: int = 0, escape_text: bool = True, **kwargs) -> Stream:
    """
    Draw text string on top of video using libfreetype.
    
    Parameters:
    - stream: Stream, input video stream
    - text: str, text to draw (required if textfile not specified)
    - x: int, x position for text (default: 0)
    - y: int, y position for text (default: 0)
    - escape_text: bool, automatically escape special characters
    - textfile: str, file containing text to draw
    - fontfile: str, path to font file
    - font: str, font family name (default: Sans)
    - fontsize: int, font size in points (default: 16)
    - fontcolor: str, text color (default: black)
    - box: int, draw background box (0/1)
    - boxcolor: str, background box color (default: white)
    - boxborderw: int, box border width
    - shadowcolor: str, text shadow color (default: black)
    - shadowx: int, shadow x offset (default: 0)
    - shadowy: int, shadow y offset (default: 0)
    - alpha: float, text transparency (0.0-1.0, default: 1.0)
    
    Returns:
    Stream object with text drawn
    """
```

**Usage Example:**
```python
# Draw red box
boxed = ffmpeg.input('input.mp4').drawbox(50, 50, 200, 100, 'red', thickness=3)

# Draw text with custom styling
texted = ffmpeg.input('input.mp4').drawtext(
    'Hello World',
    x=10,
    y=10,
    fontsize=24,
    fontcolor='white',
    box=1,
    boxcolor='black@0.5'
)

# Dynamic text with expressions
dynamic_text = ffmpeg.input('input.mp4').drawtext(
    'Frame: %{n}',
    x='(w-text_w)/2',
    y='h-th-10',
    fontsize=20,
    fontcolor='yellow'
)
```

### Special Effects

Advanced video effects for creative processing.

```python { .api }
def zoompan(stream, **kwargs) -> Stream:
    """
    Apply zoom and pan effects to video.
    
    Parameters:
    - stream: Stream, input video stream
    - zoom: str, zoom expression (default: 1)
    - x: str, x position expression (default: 0)
    - y: str, y position expression (default: 0)
    - d: str, duration in frames for effect
    - s: str, output size (default: hd720)
    - fps: int, output frame rate (default: 25)
    - z: str, alias for zoom
    
    Returns:
    Stream object with zoom/pan applied
    """

def hue(stream, **kwargs) -> Stream:
    """
    Modify hue and saturation of input video.
    
    Parameters:
    - stream: Stream, input video stream
    - h: str, hue angle in degrees (default: 0)
    - s: str, saturation multiplier -10 to 10 (default: 1)
    - H: str, hue angle in radians (default: 0)  
    - b: str, brightness -10 to 10 (default: 0)
    
    Returns:
    Stream object with hue/saturation modified
    """

def colorchannelmixer(stream, *args, **kwargs) -> Stream:
    """
    Adjust video by re-mixing color channels.
    
    Parameters:
    - stream: Stream, input video stream
    - Color channel mixing parameters as keyword arguments
    
    Returns:
    Stream object with color channels adjusted
    """
```

**Usage Example:**
```python
# Zoom in slowly
zoomed = ffmpeg.input('input.mp4').zoompan(
    zoom='min(zoom+0.0015,1.5)',
    d=125
)

# Adjust hue and saturation
color_adjusted = ffmpeg.input('input.mp4').hue(h=30, s=1.2)

# Advanced color mixing
mixed = ffmpeg.input('input.mp4').colorchannelmixer(
    rr=0.393, rg=0.769, rb=0.189,
    gr=0.349, gg=0.686, gb=0.168,
    br=0.272, bg=0.534, bb=0.131
)
```

## Complex Filter Chains

Video filters can be chained together for sophisticated processing:

```python
# Complex video processing pipeline
result = (
    ffmpeg
    .input('input.mp4')
    .crop(100, 100, 800, 600)
    .hflip()
    .drawtext('Processed Video', x=10, y=10, fontsize=20, fontcolor='white')
    .hue(s=1.2)
    .output('processed.mp4')
)
```