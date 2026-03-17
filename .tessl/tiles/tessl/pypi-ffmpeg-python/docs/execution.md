# Execution and Control

Functions for executing FFmpeg commands synchronously or asynchronously, building command-line arguments, and handling process control with comprehensive error management.

## Capabilities

### Synchronous Execution

Execute FFmpeg commands and wait for completion with comprehensive output capture and error handling.

```python { .api }
def run(stream_spec, cmd: str = 'ffmpeg', capture_stdout: bool = False, capture_stderr: bool = False, input=None, quiet: bool = False, overwrite_output: bool = False) -> tuple:
    """
    Invoke FFmpeg for the supplied node graph and wait for completion.
    
    Parameters:
    - stream_spec: Stream or stream specification to execute
    - cmd: str, FFmpeg command path (default: 'ffmpeg')
    - capture_stdout: bool, capture stdout for pipe: outputs
    - capture_stderr: bool, capture stderr for debugging
    - input: bytes, data to send to stdin for pipe: inputs
    - quiet: bool, suppress output (sets capture_stdout and capture_stderr)
    - overwrite_output: bool, add -y flag to overwrite existing files
    
    Returns:
    tuple: (stdout_data, stderr_data) as bytes objects
    
    Raises:
    ffmpeg.Error: if FFmpeg returns non-zero exit code
    """
```

**Usage Example:**
```python
import ffmpeg

# Simple execution
stream = ffmpeg.input('input.mp4').hflip().output('output.mp4')
ffmpeg.run(stream)

# Execution with output capture
try:
    stdout, stderr = ffmpeg.run(
        stream, 
        capture_stdout=True, 
        capture_stderr=True
    )
    print("Command succeeded")
except ffmpeg.Error as e:
    print(f"Command failed: {e}")
    print(f"stderr: {e.stderr.decode()}")

# Quiet execution (suppress all output)
ffmpeg.run(stream, quiet=True, overwrite_output=True)
```

### Asynchronous Execution

Start FFmpeg processes without waiting for completion, enabling real-time processing and pipeline control.

```python { .api }
def run_async(stream_spec, cmd: str = 'ffmpeg', pipe_stdin: bool = False, pipe_stdout: bool = False, pipe_stderr: bool = False, quiet: bool = False, overwrite_output: bool = False):
    """
    Asynchronously invoke FFmpeg for the supplied node graph.
    
    Parameters:
    - stream_spec: Stream or stream specification to execute
    - cmd: str, FFmpeg command path (default: 'ffmpeg')
    - pipe_stdin: bool, connect pipe to subprocess stdin
    - pipe_stdout: bool, connect pipe to subprocess stdout  
    - pipe_stderr: bool, connect pipe to subprocess stderr
    - quiet: bool, shorthand for pipe_stdout and pipe_stderr
    - overwrite_output: bool, add -y flag to overwrite existing files
    
    Returns:
    subprocess.Popen: Process object for the running FFmpeg command
    """
```

**Usage Example:**
```python
import subprocess

# Basic async execution
stream = ffmpeg.input('input.mp4').output('output.mp4')
process = ffmpeg.run_async(stream)
process.wait()  # Wait for completion

# Streaming input and output
input_stream = ffmpeg.input('pipe:', format='rawvideo', pix_fmt='rgb24', s='640x480')
output_stream = ffmpeg.output(input_stream, 'pipe:', format='rawvideo', pix_fmt='yuv420p')

process = ffmpeg.run_async(
    output_stream, 
    pipe_stdin=True, 
    pipe_stdout=True
)

# Send data and receive results
stdout, stderr = process.communicate(input=raw_video_data)

# Real-time processing example
process1 = ffmpeg.run_async(
    ffmpeg.input('input.mp4').output('pipe:', format='rawvideo'),
    pipe_stdout=True
)

process2 = ffmpeg.run_async(
    ffmpeg.input('pipe:', format='rawvideo', s='1920x1080').output('processed.mp4'),
    pipe_stdin=True
)

# Stream data between processes
while True:
    chunk = process1.stdout.read(1920 * 1080 * 3)  # One frame
    if not chunk:
        break
    process2.stdin.write(chunk)

process2.stdin.close()
process1.wait()
process2.wait()
```

### Command Building

Generate FFmpeg command-line arguments for debugging or manual execution.

```python { .api }
def get_args(stream_spec, overwrite_output: bool = False) -> list:
    """
    Build command-line arguments for FFmpeg execution.
    
    Parameters:
    - stream_spec: Stream or stream specification
    - overwrite_output: bool, add -y flag to overwrite files
    
    Returns:
    list: Command-line arguments (without 'ffmpeg' command)
    """

def compile(stream_spec, cmd: str = 'ffmpeg', overwrite_output: bool = False) -> list:
    """
    Build complete command line for invoking FFmpeg.
    
    Parameters:
    - stream_spec: Stream or stream specification
    - cmd: str/list, FFmpeg command (default: 'ffmpeg')
    - overwrite_output: bool, add -y flag to overwrite files
    
    Returns:
    list: Complete command including FFmpeg executable
    """
```

**Usage Example:**
```python
# Build arguments for debugging
stream = ffmpeg.input('input.mp4').hflip().output('output.mp4')
args = ffmpeg.get_args(stream)
print(' '.join(args))
# Output: -i input.mp4 -filter_complex [0]hflip[s0] -map [s0] output.mp4

# Build complete command
cmd = ffmpeg.compile(stream, overwrite_output=True)
print(' '.join(cmd))
# Output: ffmpeg -i input.mp4 -filter_complex [0]hflip[s0] -map [s0] -y output.mp4

# Use custom FFmpeg path
custom_cmd = ffmpeg.compile(stream, cmd='/usr/local/bin/ffmpeg')

# Execute manually with subprocess
import subprocess
result = subprocess.run(custom_cmd, capture_output=True)
```

## Error Handling

```python { .api }
class Error(Exception):
    """
    Exception raised when FFmpeg returns non-zero exit code.
    
    Attributes:
    - stdout: bytes, captured stdout data
    - stderr: bytes, captured stderr data  
    """
    
    def __init__(self, cmd: str, stdout: bytes, stderr: bytes):
        """
        Initialize error with command information.
        
        Parameters:
        - cmd: str, command that failed
        - stdout: bytes, stdout data
        - stderr: bytes, stderr data
        """
```

**Error Handling Patterns:**
```python
try:
    ffmpeg.run(stream)
except ffmpeg.Error as e:
    print(f"FFmpeg failed with error: {e}")
    
    # Decode error messages
    if e.stderr:
        error_msg = e.stderr.decode('utf-8')
        print(f"Error details: {error_msg}")
    
    # Check for specific error conditions
    if b'No such file or directory' in e.stderr:
        print("Input file not found")
    elif b'Invalid data found' in e.stderr:
        print("Corrupt or invalid input file")
    elif b'Permission denied' in e.stderr:
        print("Insufficient permissions")
```

## Advanced Execution Patterns

### Progress Monitoring

```python
# Monitor progress with global args
stream = (
    ffmpeg
    .input('large_video.mp4')
    .output('compressed.mp4', vcodec='libx264')
    .global_args('-progress', 'progress.txt', '-nostats')
)

process = ffmpeg.run_async(stream)

# Read progress in real-time
import time
while process.poll() is None:
    try:
        with open('progress.txt', 'r') as f:
            progress_data = f.read()
            print(f"Progress: {progress_data}")
    except FileNotFoundError:
        pass
    time.sleep(1)
```

### Resource Management

```python
import contextlib

@contextlib.contextmanager
def ffmpeg_process(stream_spec, **kwargs):
    """Context manager for FFmpeg processes."""
    process = ffmpeg.run_async(stream_spec, **kwargs)
    try:
        yield process
    finally:
        if process.poll() is None:  # Still running
            process.terminate()
            process.wait()

# Usage
with ffmpeg_process(stream, pipe_stdout=True) as process:
    output_data = process.stdout.read()
# Process automatically terminated if exception occurs
```

### Batch Processing

```python
def process_videos(input_files, output_dir):
    """Process multiple videos in parallel."""
    processes = []
    
    for input_file in input_files:
        output_file = f"{output_dir}/{input_file.stem}_processed.mp4"
        stream = ffmpeg.input(str(input_file)).hflip().output(str(output_file))
        process = ffmpeg.run_async(stream)
        processes.append((process, input_file))
    
    # Wait for all to complete
    for process, input_file in processes:
        try:
            process.wait()
            print(f"Completed: {input_file}")
        except Exception as e:
            print(f"Failed: {input_file} - {e}")
```