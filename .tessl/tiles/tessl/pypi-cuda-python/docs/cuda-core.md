# High-Level CUDA Core APIs

Pythonic, object-oriented CUDA programming interface that provides automatic resource management and idiomatic Python patterns for CUDA development. The `cuda.core.experimental` module offers high-level abstractions over the low-level CUDA C APIs, making GPU programming more accessible and productive.

**Note**: These APIs are marked as experimental and may change in future releases.

## Capabilities

### Device Management

High-level device selection, querying, and context management with automatic resource cleanup.

```python { .api }
class Device:
    """
    CUDA device representation with Pythonic interface.
    
    Args:
        device_id (int): Device identifier (0-based index)
    """
    def __init__(self, device_id: int = 0): ...
    
    @property
    def name(self) -> str:
        """Device name as reported by CUDA driver"""
        
    @property
    def compute_capability(self) -> tuple[int, int]:
        """Device compute capability as (major, minor) tuple"""
        
    @property
    def properties(self) -> DeviceProperties:
        """Device properties and attributes"""
        
    def set_current(self) -> None:
        """Set this device as the current CUDA device"""
        
    def synchronize(self) -> None:
        """Block until all device operations complete"""

class DeviceProperties:
    """
    Read-only device attribute queries.
    
    Note: Cannot be instantiated directly, accessed via Device.properties
    """
    @property
    def max_threads_per_block(self) -> int:
        """Maximum number of threads per block"""
        
    @property
    def max_block_dim_x(self) -> int:
        """Maximum x-dimension of a block"""
        
    @property
    def max_block_dim_y(self) -> int:
        """Maximum y-dimension of a block"""
        
    @property
    def max_block_dim_z(self) -> int:
        """Maximum z-dimension of a block"""
        
    @property
    def max_grid_dim_x(self) -> int:
        """Maximum x-dimension of a grid"""
        
    @property
    def max_grid_dim_y(self) -> int:
        """Maximum y-dimension of a grid"""
        
    @property
    def max_grid_dim_z(self) -> int:
        """Maximum z-dimension of a grid"""
        
    @property
    def max_shared_memory_per_block(self) -> int:
        """Maximum shared memory per block in bytes"""
        
    @property
    def total_constant_memory(self) -> int:
        """Total constant memory in bytes"""
        
    @property
    def warp_size(self) -> int:
        """Warp size in threads"""
        
    @property
    def multiprocessor_count(self) -> int:
        """Number of streaming multiprocessors"""
```

### Memory Management

Object-oriented memory allocation with automatic resource management and NumPy integration.

```python { .api }
class Buffer:
    """
    High-level GPU memory buffer with automatic resource management.
    """
    @classmethod
    def from_array(cls, array, device: Device) -> Buffer:
        """
        Create Buffer from NumPy array, copying data to device.
        
        Args:
            array: NumPy array or array-like object
            device: Target CUDA device
            
        Returns:
            Buffer: GPU memory buffer containing array data
        """
        
    def to_array(self) -> np.ndarray:
        """
        Copy buffer contents to NumPy array on host.
        
        Returns:
            np.ndarray: Host array containing buffer data
        """
        
    @property
    def device(self) -> Device:
        """Device where buffer is allocated"""
        
    @property
    def size(self) -> int:
        """Buffer size in bytes"""
        
    @property
    def ptr(self) -> int:
        """Raw device pointer as integer"""

class MemoryResource:
    """
    Abstract base for memory resource management.
    """
    def allocate(self, size: int, alignment: int = 1) -> int:
        """Allocate device memory"""
        
    def deallocate(self, ptr: int, size: int, alignment: int = 1) -> None:
        """Deallocate device memory"""

class DeviceMemoryResource(MemoryResource):
    """
    Standard device memory allocator using cudaMalloc/cudaFree.
    """
    def __init__(self, device: Device): ...

class LegacyPinnedMemoryResource(MemoryResource):
    """
    Page-locked host memory allocator using cudaMallocHost/cudaFreeHost.
    """
    def __init__(self): ...
```

### Stream and Event Management

Asynchronous execution management with CUDA streams and events for optimal GPU utilization.

```python { .api }
class Stream:
    """
    CUDA stream for asynchronous operations.
    
    Args:
        device (Device): Device to create stream on
        options (StreamOptions, optional): Stream creation options
    """
    def __init__(self, device: Device, options: StreamOptions = None): ...
    
    def synchronize(self) -> None:
        """Wait for all operations in this stream to complete"""
        
    def record(self, event: Event) -> None:
        """Record an event in this stream"""
        
    def wait(self, event: Event) -> None:
        """Make this stream wait for an event"""
        
    @property
    def device(self) -> Device:
        """Device this stream belongs to"""
        
    @property
    def handle(self) -> int:
        """Raw CUDA stream handle"""

class StreamOptions:
    """
    Options for stream creation.
    
    Args:
        non_blocking (bool): Create non-blocking stream
        priority (int): Stream priority (-1 to 0, higher is more priority)
    """
    def __init__(self, non_blocking: bool = False, priority: int = 0): ...

class Event:
    """
    CUDA event for synchronization and timing.
    
    Args:
        device (Device): Device to create event on
        options (EventOptions, optional): Event creation options
    """
    def __init__(self, device: Device, options: EventOptions = None): ...
    
    def synchronize(self) -> None:
        """Wait for this event to complete"""
        
    def elapsed_time(self, end_event: Event) -> float:
        """
        Calculate elapsed time between this event and end_event.
        
        Args:
            end_event (Event): End event for timing calculation
            
        Returns:
            float: Elapsed time in milliseconds
        """
        
    @property
    def device(self) -> Device:
        """Device this event belongs to"""

class EventOptions:
    """
    Options for event creation.
    
    Args:
        timing (bool): Enable timing capabilities
        blocking_sync (bool): Use blocking synchronization
        interprocess (bool): Enable interprocess event sharing
    """
    def __init__(self, timing: bool = True, blocking_sync: bool = False, interprocess: bool = False): ...
```

### Program Compilation and Execution

Runtime CUDA program compilation and kernel execution with automatic resource management.

```python { .api }
class Program:
    """
    CUDA program containing compilable source code.
    
    Args:
        code (str): CUDA C++ source code
        options (ProgramOptions, optional): Compilation options
    """
    def __init__(self, code: str, options: ProgramOptions = None): ...
    
    def compile(self) -> None:
        """Compile the program source code"""
        
    def get_kernel(self, name: str) -> Kernel:
        """
        Get a kernel function from the compiled program.
        
        Args:
            name (str): Kernel function name
            
        Returns:
            Kernel: Compiled kernel ready for launch
        """
        
    @property
    def compiled(self) -> bool:
        """Whether program has been successfully compiled"""

class ProgramOptions:
    """
    Options for CUDA program compilation.
    
    Args:
        include_paths (list[str]): Additional include directories
        defines (dict[str, str]): Preprocessor definitions
        debug (bool): Generate debug information
        optimization_level (int): Optimization level (0-3)
    """
    def __init__(self, include_paths: list[str] = None, defines: dict[str, str] = None, 
                 debug: bool = False, optimization_level: int = 2): ...

class Kernel:
    """
    Compiled CUDA kernel ready for execution.
    """
    def launch(self, config: LaunchConfig, *args) -> None:
        """
        Launch kernel with specified configuration and arguments.
        
        Args:
            config (LaunchConfig): Grid and block dimensions
            *args: Kernel arguments
        """
        
    @property
    def name(self) -> str:
        """Kernel function name"""
        
    @property
    def max_threads_per_block(self) -> int:
        """Maximum threads per block for this kernel"""

class LaunchConfig:
    """
    Kernel launch configuration specifying grid and block dimensions.
    
    Args:
        grid_dim (tuple): Grid dimensions as (x, y, z)
        block_dim (tuple): Block dimensions as (x, y, z)
        shared_memory_size (int): Dynamic shared memory size in bytes
        stream (Stream, optional): Stream for asynchronous execution
    """
    def __init__(self, grid_dim: tuple, block_dim: tuple, 
                 shared_memory_size: int = 0, stream: Stream = None): ...

def launch(kernel: Kernel, config: LaunchConfig, *args) -> None:
    """
    Launch a kernel with specified configuration and arguments.
    
    Args:
        kernel (Kernel): Compiled kernel to launch
        config (LaunchConfig): Grid and block dimensions
        *args: Kernel arguments
    """
```

### CUDA Graph Execution

CUDA graph capture and execution for optimized kernel launch sequences.

```python { .api }
class Graph:
    """
    CUDA graph containing a sequence of operations for optimized execution.
    """
    def launch(self, stream: Stream = None) -> None:
        """
        Launch the graph on specified stream.
        
        Args:
            stream (Stream, optional): Stream for graph execution
        """
        
    def update(self, other_graph: Graph) -> None:
        """
        Update this graph with topology from another graph.
        
        Args:
            other_graph (Graph): Source graph for update
        """

class GraphBuilder:
    """
    Builder for constructing CUDA graphs through capture.
    
    Args:
        device (Device): Device to build graph on
    """
    def __init__(self, device: Device): ...
    
    def capture_begin(self, stream: Stream) -> None:
        """
        Begin capturing operations into the graph.
        
        Args:
            stream (Stream): Stream to capture operations from
        """
        
    def capture_end(self) -> Graph:
        """
        End capture and return the constructed graph.
        
        Returns:
            Graph: Captured CUDA graph ready for execution
        """

class GraphCompleteOptions:
    """Options for completing graph construction."""
    def __init__(self): ...

class GraphDebugPrintOptions:
    """Options for debug printing of graph structure."""
    def __init__(self): ...
```

### System Management

System-wide CUDA initialization and management utilities.

```python { .api }
class System:
    """
    System-wide CUDA management and initialization.
    
    Note: Automatically instantiated as 'system' module attribute
    """
    def num_devices(self) -> int:
        """
        Get number of available CUDA devices.
        
        Returns:
            int: Number of CUDA-capable devices
        """
        
    def get_device(self, device_id: int) -> Device:
        """
        Get Device object for specified device ID.
        
        Args:
            device_id (int): Device identifier
            
        Returns:
            Device: Device object for the specified ID
        """

# Pre-instantiated system object
system: System
```

## Usage Examples

### Basic Device and Memory Operations

```python
from cuda.core.experimental import Device, Buffer
import numpy as np

# Select device
device = Device(0)
print(f"Using device: {device.name}")
print(f"Compute capability: {device.compute_capability}")

# Create data and transfer to GPU
host_data = np.array([1.0, 2.0, 3.0, 4.0], dtype=np.float32)
gpu_buffer = Buffer.from_array(host_data, device=device)

# Transfer back to host
result = gpu_buffer.to_array()
print(f"Result: {result}")
```

### Stream and Event Management

```python
from cuda.core.experimental import Device, Stream, Event
import time

device = Device(0)
stream1 = Stream(device)
stream2 = Stream(device)

# Create events for timing
start_event = Event(device)
end_event = Event(device)

# Record timing
stream1.record(start_event)
# ... perform operations on stream1 ...
stream1.record(end_event)

# Synchronize and get timing
end_event.synchronize()
elapsed_ms = start_event.elapsed_time(end_event)
print(f"Operations took {elapsed_ms:.2f} ms")
```

### Program Compilation and Kernel Execution

```python
from cuda.core.experimental import Device, Program, LaunchConfig, Buffer
import numpy as np

device = Device(0)

# CUDA kernel source
kernel_source = '''
extern "C" __global__ void vector_add(float* a, float* b, float* c, int n) {
    int idx = blockIdx.x * blockDim.x + threadIdx.x;
    if (idx < n) {
        c[idx] = a[idx] + b[idx];
    }
}
'''

# Compile program
program = Program(kernel_source)
program.compile()
kernel = program.get_kernel("vector_add")

# Prepare data
n = 1024
a = np.random.rand(n).astype(np.float32)
b = np.random.rand(n).astype(np.float32)

buffer_a = Buffer.from_array(a, device=device)
buffer_b = Buffer.from_array(b, device=device)
buffer_c = Buffer.from_array(np.zeros(n, dtype=np.float32), device=device)

# Launch kernel
config = LaunchConfig(
    grid_dim=(n // 256 + 1, 1, 1),
    block_dim=(256, 1, 1)
)
kernel.launch(config, buffer_a.ptr, buffer_b.ptr, buffer_c.ptr, n)

# Get result
device.synchronize()
result = buffer_c.to_array()
print(f"Vector addition completed: {result[:5]}...")
```