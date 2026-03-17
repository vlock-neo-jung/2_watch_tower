# Input and Output Operations

Core functionality for creating input streams from media files, URLs, or pipes, and defining output destinations with format specifications and encoding parameters.

## Capabilities

### Input Stream Creation

Create input streams from media files, URLs, devices, or pipes. Supports format specification, input options, and FFmpeg input parameters.

```python { .api }
def input(filename: str, **kwargs) -> Stream:
    """
    Input file URL (ffmpeg -i option).
    
    Parameters:
    - filename: str, input file path, URL, or 'pipe:' for stdin
    - f: str, input format (alias for 'format')
    - format: str, input format specification
    - video_size: tuple, video dimensions for raw input (width, height)
    - t: str/int/float, duration to read from input
    - ss: str/int/float, start time offset
    - r: str/int/float, input frame rate
    - Any other FFmpeg input options as keyword arguments
    
    Returns:
    Stream object representing the input
    """
```

**Usage Example:**
```python
# Basic file input
input_stream = ffmpeg.input('video.mp4')

# Input with format and options
raw_input = ffmpeg.input('pipe:', format='rawvideo', pix_fmt='rgb24', s='640x480')

# Input with time range
trimmed_input = ffmpeg.input('long_video.mp4', ss=30, t=60)  # Start at 30s, duration 60s
```

### Output Stream Creation

Create output streams with destination files, encoding parameters, and output format specifications.

```python { .api }
def output(*streams_and_filename, **kwargs) -> Stream:
    """
    Output file URL.
    
    Parameters:
    - *streams_and_filename: Stream objects followed by output filename
    - filename: str, output file path or 'pipe:' for stdout
    - f: str, output format (alias for 'format')
    - format: str, output format specification
    - video_bitrate: int, video bitrate (-b:v parameter)
    - audio_bitrate: int, audio bitrate (-b:a parameter)
    - video_size: str/tuple, output video dimensions
    - vcodec: str, video codec
    - acodec: str, audio codec
    - Any other FFmpeg output options as keyword arguments
    
    Returns:
    Stream object representing the output
    """
```

**Usage Example:**
```python
# Single stream output
stream = ffmpeg.input('input.mp4').hflip()
output = ffmpeg.output(stream, 'output.mp4')

# Multiple streams to single output
video = ffmpeg.input('video.mp4').video
audio = ffmpeg.input('audio.mp3').audio
output = ffmpeg.output(video, audio, 'combined.mp4')

# Output with encoding parameters
output = ffmpeg.output(
    stream, 
    'output.mp4',
    vcodec='libx264',
    acodec='aac',
    video_bitrate=1000,
    audio_bitrate=128
)
```

### Multiple Output Management

Merge multiple outputs into a single FFmpeg command to improve efficiency and avoid temporary files.

```python { .api }
def merge_outputs(*streams) -> Stream:
    """
    Include all given outputs in one ffmpeg command line.
    
    Parameters:
    - *streams: OutputStream objects to merge
    
    Returns:
    Stream object representing merged outputs
    """
```

**Usage Example:**
```python
input_stream = ffmpeg.input('input.mp4')

# Create multiple outputs
output1 = ffmpeg.output(input_stream.video, 'video_only.mp4')
output2 = ffmpeg.output(input_stream.audio, 'audio_only.mp3')
output3 = ffmpeg.output(input_stream, 'copy.mp4')

# Merge into single command
merged = ffmpeg.merge_outputs(output1, output2, output3)
ffmpeg.run(merged)
```

### Global Command Options

Add global FFmpeg command-line arguments that apply to the entire command.

```python { .api }
def overwrite_output(stream) -> Stream:
    """
    Overwrite output files without asking (ffmpeg -y option).
    
    Parameters:
    - stream: OutputStream to modify
    
    Returns:
    Stream object with overwrite flag
    """

def global_args(stream, *args) -> Stream:
    """
    Add extra global command-line arguments.
    
    Parameters:
    - stream: OutputStream to modify
    - *args: Global arguments to add
    
    Returns:
    Stream object with global arguments
    """
```

**Usage Example:**
```python
# Overwrite existing output files
stream = (
    ffmpeg
    .input('input.mp4')
    .output('output.mp4')
    .overwrite_output()
)

# Add custom global arguments
stream = (
    ffmpeg
    .input('input.mp4')
    .output('output.mp4')
    .global_args('-progress', 'progress.txt', '-loglevel', 'debug')
)
```

## Common Patterns

### Pipe-based Processing

```python
# Read from stdin, write to stdout
(
    ffmpeg
    .input('pipe:', format='rawvideo', pix_fmt='rgb24', s='640x480')
    .output('pipe:', format='rawvideo', pix_fmt='yuv420p')
    .run(pipe_stdin=True, pipe_stdout=True)
)
```

### Format Conversion

```python
# Convert between formats
(
    ffmpeg
    .input('input.avi')
    .output('output.mp4', vcodec='libx264', acodec='aac')
    .run()
)
```

### Quality Control

```python
# High quality encoding
(
    ffmpeg
    .input('input.mp4')
    .output(
        'high_quality.mp4',
        vcodec='libx264',
        video_bitrate=5000,
        acodec='aac',
        audio_bitrate=320
    )
    .run()
)
```