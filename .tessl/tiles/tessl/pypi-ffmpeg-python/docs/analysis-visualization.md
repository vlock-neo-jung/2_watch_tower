# Media Analysis and Visualization

Tools for analyzing media file properties, extracting metadata, and visualizing complex filter graphs for debugging and development purposes.

## Capabilities

### Media Analysis and Probing

Extract comprehensive metadata and technical information from media files using FFprobe.

```python { .api }
def probe(filename: str, cmd: str = 'ffprobe', **kwargs) -> dict:
    """
    Run ffprobe on the specified file and return JSON representation.
    
    Parameters:
    - filename: str, path to media file to analyze
    - cmd: str, ffprobe command path (default: 'ffprobe')
    - **kwargs: additional ffprobe options as keyword arguments
    
    Returns:
    dict: JSON data containing streams, format, and metadata information
    
    Raises:
    ffmpeg.Error: if ffprobe returns non-zero exit code
    """
```

**Usage Example:**
```python
import ffmpeg
import json

# Basic media probing
probe_data = ffmpeg.probe('video.mp4')

# Access format information
format_info = probe_data['format']
print(f"Duration: {format_info['duration']} seconds")
print(f"Bitrate: {format_info['bit_rate']} bps")
print(f"Size: {format_info['size']} bytes")

# Access stream information
streams = probe_data['streams']
for i, stream in enumerate(streams):
    print(f"Stream {i}:")
    print(f"  Codec: {stream['codec_name']}")
    print(f"  Type: {stream['codec_type']}")
    
    if stream['codec_type'] == 'video':
        print(f"  Resolution: {stream['width']}x{stream['height']}")
        print(f"  Frame rate: {stream['r_frame_rate']}")
        print(f"  Pixel format: {stream['pix_fmt']}")
    elif stream['codec_type'] == 'audio':
        print(f"  Sample rate: {stream['sample_rate']} Hz")
        print(f"  Channels: {stream['channels']}")
        print(f"  Sample format: {stream.get('sample_fmt', 'N/A')}")

# Probe with custom options
detailed_probe = ffmpeg.probe(
    'video.mp4',
    select_streams='v:0',  # Only video stream 0
    show_entries='stream=width,height,duration,bit_rate'
)
```

**Common Probe Data Structure:**
```python
{
    "streams": [
        {
            "index": 0,
            "codec_name": "h264",
            "codec_type": "video",
            "width": 1920,
            "height": 1080,
            "r_frame_rate": "30/1",
            "duration": "120.5",
            "bit_rate": "2000000",
            "pix_fmt": "yuv420p"
        },
        {
            "index": 1,
            "codec_name": "aac",
            "codec_type": "audio",
            "sample_rate": "48000",
            "channels": 2,
            "duration": "120.5",
            "bit_rate": "128000"
        }
    ],
    "format": {
        "filename": "video.mp4",
        "nb_streams": 2,
        "format_name": "mov,mp4,m4a,3gp,3g2,mj2",
        "duration": "120.500000",
        "size": "32000000",
        "bit_rate": "2128000"
    }
}
```

### Filter Graph Visualization

Visualize complex FFmpeg filter graphs using Graphviz for debugging and development.

```python { .api }
def view(stream_spec, detail: bool = False, filename: str = None, pipe: bool = False, **kwargs):
    """
    Visualize the filter graph using Graphviz.
    
    Parameters:
    - stream_spec: Stream or stream specification to visualize
    - detail: bool, show detailed node information (args, kwargs)
    - filename: str, output filename for visualization (auto-generated if None)
    - pipe: bool, return raw graphviz data instead of saving to file
    - show_labels: bool, show edge labels (default: True)
    
    Returns:
    Stream specification (for chaining) or bytes (if pipe=True)
    
    Raises:
    ImportError: if graphviz package is not installed
    ValueError: if both filename and pipe are specified
    """
```

**Usage Example:**
```python
import ffmpeg

# Create complex filter graph
input1 = ffmpeg.input('video1.mp4')
input2 = ffmpeg.input('video2.mp4')
overlay = ffmpeg.input('logo.png')

complex_graph = (
    ffmpeg
    .concat(
        input1.trim(start=0, duration=30),
        input2.trim(start=60, duration=30)
    )
    .overlay(overlay.hflip(), x=10, y=10)
    .drawtext('Processed', x=100, y=50, fontsize=24)
    .output('result.mp4')
)

# Basic visualization
complex_graph.view(filename='graph.png')

# Detailed visualization with node parameters
complex_graph.view(detail=True, filename='detailed_graph.png')

# Get visualization data without saving
graph_data = complex_graph.view(pipe=True)

# Visualization in Jupyter notebooks
from IPython.display import Image, display
graph_bytes = complex_graph.view(pipe=True)
display(Image(graph_bytes))
```

## Analysis Helper Functions

### Media Information Extraction

```python
def get_video_info(filename):
    """Extract key video information."""
    probe_data = ffmpeg.probe(filename)
    
    video_stream = None
    audio_stream = None
    
    for stream in probe_data['streams']:
        if stream['codec_type'] == 'video' and video_stream is None:
            video_stream = stream
        elif stream['codec_type'] == 'audio' and audio_stream is None:
            audio_stream = stream
    
    info = {
        'duration': float(probe_data['format']['duration']),
        'size': int(probe_data['format']['size']),
        'bitrate': int(probe_data['format']['bit_rate'])
    }
    
    if video_stream:
        info.update({
            'width': video_stream['width'],
            'height': video_stream['height'],
            'fps': eval(video_stream['r_frame_rate']),
            'video_codec': video_stream['codec_name'],
            'pixel_format': video_stream['pix_fmt']
        })
    
    if audio_stream:
        info.update({
            'audio_codec': audio_stream['codec_name'],
            'sample_rate': int(audio_stream['sample_rate']),
            'channels': audio_stream['channels']
        })
    
    return info

# Usage
info = get_video_info('video.mp4')
print(f"Video: {info['width']}x{info['height']} at {info['fps']} fps")
print(f"Duration: {info['duration']} seconds")
```

### Stream Validation

```python
def validate_streams(*filenames):
    """Validate that multiple files have compatible streams for processing."""
    stream_info = []
    
    for filename in filenames:
        try:
            probe_data = ffmpeg.probe(filename)
            video_streams = [s for s in probe_data['streams'] if s['codec_type'] == 'video']
            audio_streams = [s for s in probe_data['streams'] if s['codec_type'] == 'audio']
            
            stream_info.append({
                'filename': filename,
                'video_streams': len(video_streams),
                'audio_streams': len(audio_streams),
                'video_codec': video_streams[0]['codec_name'] if video_streams else None,
                'audio_codec': audio_streams[0]['codec_name'] if audio_streams else None,
                'resolution': f"{video_streams[0]['width']}x{video_streams[0]['height']}" if video_streams else None
            })
        except ffmpeg.Error as e:
            print(f"Error probing {filename}: {e}")
            stream_info.append({'filename': filename, 'error': str(e)})
    
    return stream_info

# Usage
files = ['clip1.mp4', 'clip2.mp4', 'clip3.mp4']
validation_results = validate_streams(*files)

for result in validation_results:
    if 'error' in result:
        print(f"ERROR: {result['filename']} - {result['error']}")
    else:
        print(f"OK: {result['filename']} - {result['resolution']} - {result['video_codec']}")
```

## Development and Debugging Patterns

### Command Inspection

```python
# Build and inspect commands before execution
stream = (
    ffmpeg
    .input('input.mp4')
    .filter('scale', 640, 480)
    .filter('fps', fps=30)
    .output('output.mp4', vcodec='libx264')
)

# Get the command that would be executed
cmd = ffmpeg.compile(stream)
print("Command:", ' '.join(cmd))

# Visualize the processing graph
stream.view(detail=True)

# Execute with error capture for debugging
try:
    ffmpeg.run(stream, capture_stderr=True)
except ffmpeg.Error as e:
    print("FFmpeg stderr:")
    print(e.stderr.decode())
```

### Performance Analysis

```python
import time
import tempfile

def benchmark_processing(input_file, operations):
    """Benchmark different processing operations."""
    results = {}
    
    for name, operation in operations.items():
        with tempfile.NamedTemporaryFile(suffix='.mp4', delete=False) as temp_file:
            temp_path = temp_file.name
        
        try:
            stream = operation(ffmpeg.input(input_file)).output(temp_path)
            
            start_time = time.time()
            ffmpeg.run(stream, quiet=True, overwrite_output=True)
            end_time = time.time()
            
            # Get output file info
            probe_data = ffmpeg.probe(temp_path)
            size = int(probe_data['format']['size'])
            
            results[name] = {
                'duration': end_time - start_time,
                'output_size': size
            }
            
        except ffmpeg.Error as e:
            results[name] = {'error': str(e)}
        finally:
            try:
                os.unlink(temp_path)
            except:
                pass
    
    return results

# Usage
operations = {
    'hflip': lambda input_stream: input_stream.hflip(),
    'scale_720p': lambda input_stream: input_stream.filter('scale', 1280, 720),
    'blur': lambda input_stream: input_stream.filter('boxblur', '10:1'),
}

benchmark_results = benchmark_processing('test_video.mp4', operations)
for op, result in benchmark_results.items():
    if 'error' in result:
        print(f"{op}: ERROR - {result['error']}")
    else:
        print(f"{op}: {result['duration']:.2f}s, {result['output_size']} bytes")
```

### Interactive Development

```python
# Create reusable processing functions
def create_thumbnail(input_file, output_file, timestamp=1.0, size="320x240"):
    """Generate video thumbnail at specific timestamp."""
    return (
        ffmpeg
        .input(input_file, ss=timestamp)
        .filter('scale', *size.split('x'))
        .output(output_file, vframes=1)
    )

def add_watermark(input_file, watermark_file, output_file, position='bottom-right'):
    """Add watermark to video."""
    input_stream = ffmpeg.input(input_file)
    watermark = ffmpeg.input(watermark_file)
    
    if position == 'bottom-right':
        x, y = 'main_w-overlay_w-10', 'main_h-overlay_h-10'
    elif position == 'top-left':
        x, y = '10', '10'
    else:
        x, y = '10', '10'  # Default
    
    return input_stream.overlay(watermark, x=x, y=y).output(output_file)

# Use in development workflow
input_video = 'source.mp4'

# Generate thumbnail for preview
thumbnail = create_thumbnail(input_video, 'thumb.jpg', timestamp=5.0)
thumbnail.view()  # Visualize processing
ffmpeg.run(thumbnail)

# Add watermark with visualization
watermarked = add_watermark(input_video, 'logo.png', 'final.mp4')
watermarked.view(detail=True)  # Debug the graph
ffmpeg.run(watermarked)
```