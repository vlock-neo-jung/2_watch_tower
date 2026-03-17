# FFmpeg Python

Python bindings for FFmpeg with complex filtering support. FFmpeg-python provides a fluent, Pythonic interface for constructing FFmpeg command lines, enabling sophisticated video and audio processing workflows without dealing with complex command-line arguments directly.

## Package Information

- **Package Name**: ffmpeg-python
- **Language**: Python
- **Installation**: `pip install ffmpeg-python`
- **Dependencies**: `future` (built-in), `graphviz` (optional, for visualization)

## Core Imports

```python
import ffmpeg
```

## Basic Usage

```python
import ffmpeg

# Simple horizontal flip
(
    ffmpeg
    .input('input.mp4')
    .hflip()
    .output('output.mp4')
    .run()
)

# Complex filter chain with overlay
in_file = ffmpeg.input('input.mp4')
overlay_file = ffmpeg.input('overlay.png')
(
    ffmpeg
    .concat(
        in_file.trim(start_frame=10, end_frame=20),
        in_file.trim(start_frame=30, end_frame=40),
    )
    .overlay(overlay_file.hflip())
    .drawbox(50, 50, 120, 120, color='red', thickness=5)
    .output('out.mp4')
    .run()
)

# Get media information
probe_data = ffmpeg.probe('input.mp4')
```

## Architecture

FFmpeg-python uses a node-based architecture to represent FFmpeg command graphs:

- **Stream Objects**: Represent data flow between processing nodes
- **Input Nodes**: Media input sources (files, pipes, etc.)
- **Filter Nodes**: Video/audio processing operations
- **Output Nodes**: Media output destinations  
- **DAG Structure**: Directed acyclic graph for complex filter chains

This design enables arbitrarily complex signal graphs while maintaining a readable, fluent Python interface that mirrors FFmpeg's filter graph concepts.

## Capabilities

### Input and Output Operations

Core functionality for creating input streams from media files, URLs, or pipes, and defining output destinations with format specifications and encoding parameters.

```python { .api }
def input(filename: str, **kwargs) -> Stream
def output(*streams_and_filename, **kwargs) -> Stream
def merge_outputs(*streams) -> Stream
def overwrite_output(stream) -> Stream
def global_args(stream, *args) -> Stream
```

[Input and Output Operations](./input-output.md)

### Video Filters

Essential video processing filters including geometric transformations, visual effects, overlays, cropping, and drawing operations for comprehensive video manipulation.

```python { .api }
def hflip(stream) -> Stream
def vflip(stream) -> Stream
def crop(stream, x: int, y: int, width: int, height: int, **kwargs) -> Stream
def overlay(main_stream, overlay_stream, eof_action: str = 'repeat', **kwargs) -> Stream
def drawbox(stream, x: int, y: int, width: int, height: int, color: str, thickness: int = None, **kwargs) -> Stream
def drawtext(stream, text: str = None, x: int = 0, y: int = 0, escape_text: bool = True, **kwargs) -> Stream
```

[Video Filters](./video-filters.md)

### Stream Processing

Advanced stream manipulation including concatenation, splitting, trimming, timestamp adjustment, and custom filter application for complex multimedia workflows.

```python { .api }
def concat(*streams, **kwargs) -> Stream
def split(stream) -> FilterNode
def asplit(stream) -> FilterNode
def trim(stream, **kwargs) -> Stream
def setpts(stream, expr: str) -> Stream
def filter(stream_spec, filter_name: str, *args, **kwargs) -> Stream
def filter_multi_output(stream_spec, filter_name: str, *args, **kwargs) -> FilterNode
```

[Stream Processing](./stream-processing.md)

### Execution and Control

Functions for executing FFmpeg commands synchronously or asynchronously, building command-line arguments, and handling process control with comprehensive error management.

```python { .api }
def run(stream_spec, cmd: str = 'ffmpeg', capture_stdout: bool = False, capture_stderr: bool = False, input=None, quiet: bool = False, overwrite_output: bool = False) -> tuple
def run_async(stream_spec, cmd: str = 'ffmpeg', pipe_stdin: bool = False, pipe_stdout: bool = False, pipe_stderr: bool = False, quiet: bool = False, overwrite_output: bool = False)
def compile(stream_spec, cmd: str = 'ffmpeg', overwrite_output: bool = False) -> list
def get_args(stream_spec, overwrite_output: bool = False) -> list
```

[Execution and Control](./execution.md)

### Media Analysis and Visualization

Tools for analyzing media file properties, extracting metadata, and visualizing complex filter graphs for debugging and development purposes.

```python { .api }
def probe(filename: str, cmd: str = 'ffprobe', **kwargs) -> dict
def view(stream_spec, detail: bool = False, filename: str = None, pipe: bool = False, **kwargs)
```

[Media Analysis and Visualization](./analysis-visualization.md)

## Exception Handling

```python { .api }
class Error(Exception):
    """Exception raised when ffmpeg/ffprobe returns non-zero exit code."""
    stdout: bytes
    stderr: bytes
```

FFmpeg-python raises `ffmpeg.Error` exceptions when FFmpeg commands fail. The exception includes both stdout and stderr output for debugging failed operations.

## Stream Object API

```python { .api }
class Stream:
    """Represents the outgoing edge of an upstream node."""
    
    @property
    def audio(self) -> Stream
        """Select audio portion of stream (shorthand for ['a'])."""
    
    @property  
    def video(self) -> Stream
        """Select video portion of stream (shorthand for ['v'])."""
    
    def __getitem__(self, index: str) -> Stream
        """Select stream component ('a' for audio, 'v' for video, etc.)."""
```

All filter functions return Stream objects that support method chaining and component selection for building complex processing pipelines.