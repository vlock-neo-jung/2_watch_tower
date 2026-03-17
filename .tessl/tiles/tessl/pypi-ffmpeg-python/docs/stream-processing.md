# Stream Processing

Advanced stream manipulation including concatenation, splitting, trimming, timestamp adjustment, and custom filter application for complex multimedia workflows.

## Capabilities

### Stream Concatenation

Join multiple video and audio streams together sequentially.

```python { .api }
def concat(*streams, **kwargs) -> Stream:
    """
    Concatenate audio and video streams, joining them one after another.
    
    Parameters:
    - *streams: Stream objects to concatenate
    - v: int, number of video streams per segment (default: 1)
    - a: int, number of audio streams per segment (default: 0)
    - n: int, number of segments (automatically calculated)
    - unsafe: bool, do not fail if segments have different formats
    
    Returns:
    Stream object with concatenated content
    
    Note: All segments must start at timestamp 0 and have the same
    parameters (resolution, codec settings, etc.)
    """
```

**Usage Example:**
```python
# Concatenate video clips
clip1 = ffmpeg.input('part1.mp4')
clip2 = ffmpeg.input('part2.mp4')
clip3 = ffmpeg.input('part3.mp4')

concatenated = ffmpeg.concat(clip1, clip2, clip3)

# Concatenate with both video and audio
concatenated_av = ffmpeg.concat(
    clip1.video, clip1.audio,
    clip2.video, clip2.audio,
    v=1, a=1
)

# Mixed content concatenation
video_only = ffmpeg.concat(
    ffmpeg.input('clip1.mp4'),
    ffmpeg.input('clip2.mp4'), 
    ffmpeg.input('clip3.mp4')
)
```

### Stream Splitting

Split single streams into multiple identical streams for parallel processing.

```python { .api }
def split(stream) -> FilterNode:
    """
    Split video stream into multiple identical streams.
    
    Parameters:
    - stream: Stream, input video stream to split
    
    Returns:
    FilterNode that can generate multiple output streams
    """

def asplit(stream) -> FilterNode:
    """
    Split audio stream into multiple identical streams.
    
    Parameters:
    - stream: Stream, input audio stream to split
    
    Returns:
    FilterNode that can generate multiple output streams
    """
```

**Usage Example:**
```python
input_stream = ffmpeg.input('input.mp4')

# Split video for multiple outputs
split_video = input_stream.video.split()
stream1 = split_video.stream(0)  # First copy
stream2 = split_video.stream(1)  # Second copy

# Process each copy differently
processed1 = stream1.hflip()
processed2 = stream2.vflip()

# Multiple outputs
output1 = ffmpeg.output(processed1, 'flipped_h.mp4')
output2 = ffmpeg.output(processed2, 'flipped_v.mp4')
```

### Stream Trimming

Extract specific time ranges from input streams.

```python { .api }
def trim(stream, **kwargs) -> Stream:
    """
    Trim input to contain one continuous subpart.
    
    Parameters:
    - stream: Stream, input stream to trim
    - start: str/float, start time in seconds
    - end: str/float, end time in seconds
    - start_pts: int, start timestamp in timebase units
    - end_pts: int, end timestamp in timebase units
    - duration: str/float, maximum duration in seconds
    - start_frame: int, first frame number to include
    - end_frame: int, first frame number to exclude
    
    Returns:
    Stream object with specified time range
    """
```

**Usage Example:**
```python
# Trim by time (seconds)
trimmed = ffmpeg.input('long_video.mp4').trim(start=30, duration=60)

# Trim by frame numbers
frame_trimmed = ffmpeg.input('video.mp4').trim(start_frame=100, end_frame=500)

# Trim with precise timestamps
precise_trim = ffmpeg.input('video.mp4').trim(
    start='00:01:30.500',
    end='00:02:45.750'
)
```

### Timestamp Manipulation

Adjust presentation timestamps for synchronization and timing control.

```python { .api }
def setpts(stream, expr: str) -> Stream:
    """
    Change presentation timestamp (PTS) of input frames.
    
    Parameters:
    - stream: Stream, input stream to modify
    - expr: str, expression evaluated for each frame timestamp
    
    Returns:
    Stream object with modified timestamps
    
    Common expressions:
    - 'PTS-STARTPTS': Reset timestamps to start from zero
    - '0.5*PTS': Double playback speed (half duration)
    - '2.0*PTS': Half playback speed (double duration)
    - 'PTS+10/TB': Add 10 timebase units delay
    """
```

**Usage Example:**
```python
# Reset timestamps to start from zero
reset_pts = ffmpeg.input('video.mp4').setpts('PTS-STARTPTS')

# Double playback speed
fast_video = ffmpeg.input('video.mp4').setpts('0.5*PTS')

# Slow motion (half speed)
slow_video = ffmpeg.input('video.mp4').setpts('2.0*PTS')

# Complex timing adjustment
delayed = ffmpeg.input('video.mp4').setpts('PTS+5/TB')
```

### Custom Filters

Apply any FFmpeg filter with custom parameters when specific filter functions are not available.

```python { .api }
def filter(stream_spec, filter_name: str, *args, **kwargs) -> Stream:
    """
    Apply custom FFmpeg filter with one output.
    
    Parameters:
    - stream_spec: Stream, list of Streams, or label-to-Stream dictionary
    - filter_name: str, FFmpeg filter name
    - *args: positional arguments passed to FFmpeg verbatim
    - **kwargs: keyword arguments passed to FFmpeg verbatim
    
    Returns:
    Stream object with filter applied
    """

def filter_(stream_spec, filter_name: str, *args, **kwargs) -> Stream:
    """
    Alternate name for filter() to avoid collision with Python built-in.
    
    Same parameters and behavior as filter().
    """

def filter_multi_output(stream_spec, filter_name: str, *args, **kwargs) -> FilterNode:
    """
    Apply custom FFmpeg filter that can produce multiple outputs.
    
    Parameters:
    - stream_spec: Stream, list of Streams, or label-to-Stream dictionary  
    - filter_name: str, FFmpeg filter name
    - *args: positional arguments passed to FFmpeg verbatim
    - **kwargs: keyword arguments passed to FFmpeg verbatim
    
    Returns:
    FilterNode that can generate multiple output streams
    """
```

**Usage Example:**
```python
# Apply custom filter with parameters
blurred = ffmpeg.input('input.mp4').filter('boxblur', '10:1')

# Complex custom filter
sharpened = ffmpeg.input('input.mp4').filter(
    'unsharp', 
    luma_msize_x=5,
    luma_msize_y=5,
    luma_amount=1.5
)

# Multi-output filter
input_stream = ffmpeg.input('input.mp4')
histogram = input_stream.filter_multi_output('histogram')
hist_video = histogram.stream(0)
hist_data = histogram.stream(1)

# Using filter_ to avoid name collision
filtered = ffmpeg.input('input.mp4').filter_('scale', 640, 480)
```

## Advanced Stream Processing Patterns

### Complex Filter Graphs

```python
# Create complex processing pipeline
input_video = ffmpeg.input('input.mp4')

# Split for parallel processing  
split_node = input_video.split()
stream_a = split_node.stream(0)
stream_b = split_node.stream(1)

# Process each stream differently
processed_a = stream_a.hflip().filter('blur', '5')
processed_b = stream_b.vflip().filter('sharpen', '1')

# Concatenate processed streams
final = ffmpeg.concat(processed_a, processed_b)
```

### Time-based Processing

```python
# Extract specific scenes and process
scene1 = ffmpeg.input('movie.mp4').trim(start=0, duration=30)
scene2 = ffmpeg.input('movie.mp4').trim(start=120, duration=45)
scene3 = ffmpeg.input('movie.mp4').trim(start=300, duration=60)

# Process each scene
enhanced_scene1 = scene1.filter('eq', brightness=0.1)
enhanced_scene2 = scene2.hue(s=1.2)
enhanced_scene3 = scene3.filter('unsharp', '5:5:1.0')

# Combine into highlight reel
highlights = ffmpeg.concat(enhanced_scene1, enhanced_scene2, enhanced_scene3)
```

### Stream Synchronization

```python
# Synchronize audio and video streams
video = ffmpeg.input('video.mp4').video.setpts('PTS-STARTPTS')
audio = ffmpeg.input('audio.mp3').audio.filter('asetpts', 'PTS-STARTPTS')

# Combine synchronized streams
synchronized = ffmpeg.output(video, audio, 'synced.mp4')
```