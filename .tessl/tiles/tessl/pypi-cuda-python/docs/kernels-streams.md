# Kernel Execution and Streams

CUDA kernel launching, execution control and asynchronous stream management for optimal GPU utilization and performance. This module provides the essential functionality for executing parallel code on CUDA devices and managing concurrent operations through streams and events.

## Capabilities

### Stream Management

Create and manage CUDA streams for asynchronous execution and concurrent operations.

```python { .api }
def cudaStreamCreate() -> int:
    """
    Create a new CUDA stream for asynchronous operations.
    
    Returns:
        int: Stream handle
    
    Note:
        Stream enables asynchronous kernel launches and memory transfers
    """

def cudaStreamCreateWithFlags(flags: int) -> int:
    """
    Create a CUDA stream with specific behavior flags.
    
    Args:
        flags (int): Stream creation flags (cudaStreamDefault, cudaStreamNonBlocking)
    
    Returns:
        int: Stream handle
    """

def cudaStreamDestroy(stream: int) -> None:
    """
    Destroy a CUDA stream and free associated resources.
    
    Args:
        stream (int): Stream handle to destroy
    
    Note:
        Blocks until all operations in stream complete
    """

def cudaStreamSynchronize(stream: int) -> None:
    """
    Wait for all operations in a stream to complete.
    
    Args:
        stream (int): Stream handle to synchronize
    
    Note:
        Blocks until stream operations finish
    """

def cudaStreamQuery(stream: int) -> cudaError_t:
    """
    Query the status of operations in a stream.
    
    Args:
        stream (int): Stream handle to query
    
    Returns:
        cudaError_t: cudaSuccess if complete, cudaErrorNotReady if pending
    """
```

### Event Management

Create and manage CUDA events for timing and synchronization between operations.

```python { .api }
def cudaEventCreate() -> int:
    """
    Create a CUDA event for timing and synchronization.
    
    Returns:
        int: Event handle
    """

def cudaEventCreateWithFlags(flags: int) -> int:
    """
    Create a CUDA event with specific behavior flags.
    
    Args:
        flags (int): Event creation flags (cudaEventDefault, cudaEventBlockingSync, etc.)
    
    Returns:
        int: Event handle
    """

def cudaEventDestroy(event: int) -> None:
    """
    Destroy a CUDA event and free associated resources.
    
    Args:
        event (int): Event handle to destroy
    """

def cudaEventRecord(event: int, stream: int = 0) -> None:
    """
    Record an event in a stream.
    
    Args:
        event (int): Event handle
        stream (int): Stream handle (0 for default stream)
    
    Note:
        Event will be triggered when stream reaches this point
    """

def cudaEventSynchronize(event: int) -> None:
    """
    Wait for an event to complete.
    
    Args:
        event (int): Event handle to wait for
    
    Note:
        Blocks until event completes
    """

def cudaEventQuery(event: int) -> cudaError_t:
    """
    Query the status of an event.
    
    Args:
        event (int): Event handle to query
    
    Returns:
        cudaError_t: cudaSuccess if complete, cudaErrorNotReady if pending
    """
```

### Event Timing

Measure execution time between events for performance analysis.

```python { .api }
def cudaEventElapsedTime(start: int, end: int) -> float:
    """
    Calculate elapsed time between two events.
    
    Args:
        start (int): Start event handle
        end (int): End event handle
    
    Returns:
        float: Elapsed time in milliseconds
    
    Note:
        Both events must have completed recording
    """
```

### Stream Synchronization

Coordinate execution between multiple streams using events and dependencies.

```python { .api }
def cudaStreamWaitEvent(stream: int, event: int, flags: int = 0) -> None:
    """
    Make a stream wait for an event to complete.
    
    Args:
        stream (int): Stream that should wait
        event (int): Event to wait for
        flags (int): Wait flags (reserved, must be 0)
    
    Note:
        Stream operations after this call wait for event completion
    """

def cudaDeviceSynchronize() -> None:
    """
    Wait for all operations on the current device to complete.
    
    Note:
        Blocks until all streams and operations finish
    """
```

### Kernel Execution

Launch CUDA kernels with specified grid and block dimensions.

```python { .api }
def cudaLaunchKernel(
    func,
    gridDim: tuple,
    blockDim: tuple, 
    args,
    sharedMem: int = 0,
    stream: int = 0
) -> None:
    """
    Launch a CUDA kernel with specified configuration.
    
    Args:
        func: Kernel function handle
        gridDim (tuple): Grid dimensions (x, y, z)
        blockDim (tuple): Block dimensions (x, y, z)  
        args: Kernel arguments
        sharedMem (int): Dynamic shared memory per block in bytes
        stream (int): Stream for asynchronous execution
    
    Note:
        Kernel launches are asynchronous by default
    """

def cudaLaunchCooperativeKernel(
    func,
    gridDim: tuple,
    blockDim: tuple,
    args,
    sharedMem: int = 0,
    stream: int = 0
) -> None:
    """
    Launch a cooperative CUDA kernel where blocks can synchronize.
    
    Args:
        func: Cooperative kernel function handle
        gridDim (tuple): Grid dimensions (x, y, z)
        blockDim (tuple): Block dimensions (x, y, z)
        args: Kernel arguments
        sharedMem (int): Dynamic shared memory per block in bytes
        stream (int): Stream for asynchronous execution
    
    Note:
        Requires compute capability 6.0+ and cooperative launch support
    """
```

### Occupancy Analysis

Analyze kernel occupancy to optimize grid and block dimensions for maximum performance.

```python { .api }
def cudaOccupancyMaxActiveBlocksPerMultiprocessor(
    func,
    blockSize: int,
    dynamicSMemSize: int
) -> int:
    """
    Calculate maximum active blocks per SM for a kernel configuration.
    
    Args:
        func: Kernel function handle
        blockSize (int): Block size (number of threads per block)
        dynamicSMemSize (int): Dynamic shared memory per block
    
    Returns:
        int: Maximum active blocks per multiprocessor
    """

def cudaOccupancyMaxPotentialBlockSize(
    func,
    dynamicSMemSize: int = 0,
    blockSizeLimit: int = 0
) -> tuple:
    """
    Calculate optimal block size for maximum occupancy.
    
    Args:
        func: Kernel function handle
        dynamicSMemSize (int): Dynamic shared memory per block
        blockSizeLimit (int): Maximum block size limit (0 for device max)
    
    Returns:
        tuple[int, int]: (minGridSize, blockSize) for maximum occupancy
    """
```

## Types

### Stream Flags

```python { .api }
# Stream creation flag constants
cudaStreamDefault: int  # Default stream behavior
cudaStreamNonBlocking: int  # Non-blocking stream (does not synchronize with default stream)
```

### Event Flags

```python { .api }
# Event creation flag constants
cudaEventDefault: int  # Default event behavior
cudaEventBlockingSync: int  # Use blocking synchronization
cudaEventDisableTiming: int  # Disable timing (faster recording)
cudaEventInterprocess: int  # Enable inter-process sharing
```

### Kernel Launch Parameters

```python { .api }
class dim3:
    """3D dimension structure for grid and block sizes"""
    x: int  # X dimension
    y: int  # Y dimension  
    z: int  # Z dimension
    
    def __init__(self, x: int = 1, y: int = 1, z: int = 1): ...
```

### Error Codes

```python { .api }
class cudaError_t:
    """CUDA error code enumeration"""
    cudaSuccess: int  # No error
    cudaErrorNotReady: int  # Operation not yet complete
    cudaErrorInvalidResourceHandle: int  # Invalid stream/event handle
    cudaErrorInvalidValue: int  # Invalid parameter value
    cudaErrorLaunchFailure: int  # Kernel launch failed
    cudaErrorLaunchTimeout: int  # Kernel execution timed out
    cudaErrorLaunchOutOfResources: int  # Too many resources requested
```

## Usage Examples

### Basic Stream Operations

```python
from cuda.bindings import runtime

# Create streams for concurrent execution
stream1 = runtime.cudaStreamCreate()
stream2 = runtime.cudaStreamCreate()

# Launch operations in different streams
runtime.cudaMemcpyAsync(dst1, src1, size, 
                       runtime.cudaMemcpyKind.cudaMemcpyHostToDevice, 
                       stream1)
runtime.cudaMemcpyAsync(dst2, src2, size,
                       runtime.cudaMemcpyKind.cudaMemcpyHostToDevice,
                       stream2)

# Synchronize streams
runtime.cudaStreamSynchronize(stream1)
runtime.cudaStreamSynchronize(stream2)

# Cleanup
runtime.cudaStreamDestroy(stream1)
runtime.cudaStreamDestroy(stream2)
```

### Event Timing

```python
from cuda.bindings import runtime

# Create events for timing
start_event = runtime.cudaEventCreate()
end_event = runtime.cudaEventCreate()

# Record start time
runtime.cudaEventRecord(start_event)

# Execute operations to be timed
runtime.cudaLaunchKernel(kernel_func, (grid_x, grid_y, 1), 
                        (block_x, block_y, 1), kernel_args)

# Record end time
runtime.cudaEventRecord(end_event)

# Wait for completion and calculate elapsed time
runtime.cudaEventSynchronize(end_event)
elapsed_ms = runtime.cudaEventElapsedTime(start_event, end_event)
print(f"Kernel execution time: {elapsed_ms:.3f} ms")

# Cleanup
runtime.cudaEventDestroy(start_event)
runtime.cudaEventDestroy(end_event)
```

### Stream Dependencies

```python
from cuda.bindings import runtime

# Create streams and events
compute_stream = runtime.cudaStreamCreate()
copy_stream = runtime.cudaStreamCreate()
compute_done = runtime.cudaEventCreate()

# Launch compute kernel
runtime.cudaLaunchKernel(compute_kernel, grid_dim, block_dim, 
                        compute_args, 0, compute_stream)

# Record event when compute completes
runtime.cudaEventRecord(compute_done, compute_stream)

# Make copy stream wait for compute to finish
runtime.cudaStreamWaitEvent(copy_stream, compute_done)

# Launch copy operation that depends on compute
runtime.cudaMemcpyAsync(host_dst, device_src, size,
                       runtime.cudaMemcpyKind.cudaMemcpyDeviceToHost,
                       copy_stream)

# Synchronize final stream
runtime.cudaStreamSynchronize(copy_stream)
```

### Occupancy Optimization

```python
from cuda.bindings import runtime

# Analyze kernel occupancy
max_blocks = runtime.cudaOccupancyMaxActiveBlocksPerMultiprocessor(
    kernel_func, block_size=256, dynamicSMemSize=0
)

# Find optimal block size
min_grid_size, optimal_block_size = runtime.cudaOccupancyMaxPotentialBlockSize(
    kernel_func, dynamicSMemSize=0
)

print(f"Max blocks per SM: {max_blocks}")
print(f"Optimal block size: {optimal_block_size}")
print(f"Minimum grid size: {min_grid_size}")

# Use optimal configuration
grid_size = (data_size + optimal_block_size - 1) // optimal_block_size
runtime.cudaLaunchKernel(kernel_func, (grid_size, 1, 1), 
                        (optimal_block_size, 1, 1), kernel_args)
```