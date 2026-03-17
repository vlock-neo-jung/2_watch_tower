# Device and Memory Management

Essential CUDA device enumeration, selection, and memory allocation operations including unified memory, streams, and events for efficient GPU resource management. This module provides the foundational operations for working with CUDA devices and managing memory across CPU and GPU address spaces.

## Capabilities

### Device Information and Selection

Query available CUDA devices, select active devices, and retrieve device properties for optimal resource allocation.

```python { .api }
def cudaGetDeviceCount() -> int:
    """
    Get the number of CUDA-capable devices.
    
    Returns:
        int: Number of available CUDA devices
    
    Raises:
        cudaError_t: If CUDA driver/runtime error occurs
    """

def cudaSetDevice(device: int) -> None:
    """
    Set the current CUDA device for subsequent operations.
    
    Args:
        device (int): Device ID (0-based index)
    
    Raises:
        cudaError_t: If device ID is invalid or device not available
    """

def cudaGetDevice() -> int:
    """
    Get the currently selected CUDA device.
    
    Returns:
        int: Currently active device ID
    """

def cudaDeviceReset() -> None:
    """
    Reset the current CUDA device and destroy all associated contexts.
    
    Note:
        This function should be called to ensure clean shutdown
    """

def cudaDeviceSynchronize() -> None:
    """
    Wait for all operations on the current device to complete.
    
    Note:
        Blocks until all preceding operations complete
    """

def cudaGetErrorString(error: cudaError_t) -> str:
    """
    Get a descriptive string for a CUDA error code.
    
    Args:
        error (cudaError_t): CUDA error code
    
    Returns:
        str: Human-readable error description
    """
```

### Device Properties and Attributes

Retrieve detailed device capabilities and specifications for performance optimization.

```python { .api }
def cudaGetDeviceProperties(device: int) -> cudaDeviceProp:
    """
    Get comprehensive properties of a CUDA device.
    
    Args:
        device (int): Device ID to query
    
    Returns:
        cudaDeviceProp: Device properties structure
    """

def cudaDeviceGetAttribute(attr: cudaDeviceAttr, device: int) -> int:
    """
    Get a specific attribute value for a CUDA device.
    
    Args:
        attr (cudaDeviceAttr): Attribute to query
        device (int): Device ID
    
    Returns:
        int: Attribute value
    """
```

### Memory Allocation

Allocate memory on both device (GPU) and host (CPU) with various allocation strategies.

```python { .api }
def cudaMalloc(size: int) -> int:
    """
    Allocate memory on the CUDA device.
    
    Args:
        size (int): Number of bytes to allocate
    
    Returns:
        int: Device memory pointer (as integer address)
    
    Raises:
        cudaError_t: If allocation fails (e.g., out of memory)
    """

def cudaMallocHost(size: int) -> int:
    """
    Allocate page-locked (pinned) host memory.
    
    Args:
        size (int): Number of bytes to allocate
    
    Returns:
        int: Host memory pointer (as integer address)
    
    Note:
        Pinned memory enables faster host-device transfers
    """

def cudaMallocManaged(size: int, flags: int = 0) -> int:
    """
    Allocate unified memory accessible from both CPU and GPU.
    
    Args:
        size (int): Number of bytes to allocate
        flags (int): Allocation flags (optional)
    
    Returns:
        int: Unified memory pointer
    """

def cudaHostAlloc(size: int, flags: int) -> int:
    """
    Allocate host memory with specific allocation flags.
    
    Args:
        size (int): Number of bytes to allocate
        flags (int): Allocation flags (cudaHostAllocDefault, etc.)
    
    Returns:
        int: Host memory pointer
    """
```

### Memory Deallocation

Free allocated memory resources on both device and host.

```python { .api }
def cudaFree(devPtr: int) -> None:
    """
    Free device memory allocated with cudaMalloc.
    
    Args:
        devPtr (int): Device pointer to free
    """

def cudaFreeHost(ptr: int) -> None:
    """
    Free host memory allocated with cudaMallocHost or cudaHostAlloc.
    
    Args:
        ptr (int): Host pointer to free
    """

def cudaHostUnregister(ptr: int) -> None:
    """
    Unregister previously registered host memory.
    
    Args:
        ptr (int): Host pointer to unregister
    """
```

### Memory Transfer Operations

Copy data between host and device memory with various transfer directions and modes.

```python { .api }
def cudaMemcpy(dst, src, count: int, kind: cudaMemcpyKind) -> None:
    """
    Copy memory between host and device synchronously.
    
    Args:
        dst: Destination pointer
        src: Source pointer  
        count (int): Number of bytes to copy
        kind (cudaMemcpyKind): Copy direction
    
    Note:
        Blocks until copy completes
    """

def cudaMemcpyAsync(dst, src, count: int, kind: cudaMemcpyKind, stream: int) -> None:
    """
    Copy memory between host and device asynchronously.
    
    Args:
        dst: Destination pointer
        src: Source pointer
        count (int): Number of bytes to copy
        kind (cudaMemcpyKind): Copy direction
        stream (int): CUDA stream for asynchronous execution
    """

def cudaMemset(devPtr: int, value: int, count: int) -> None:
    """
    Set device memory to a specific value.
    
    Args:
        devPtr (int): Device pointer
        value (int): Value to set (0-255)
        count (int): Number of bytes to set
    """

def cudaMemsetAsync(devPtr: int, value: int, count: int, stream: int) -> None:
    """
    Set device memory to a specific value asynchronously.
    
    Args:
        devPtr (int): Device pointer
        value (int): Value to set (0-255)
        count (int): Number of bytes to set
        stream (int): CUDA stream for asynchronous execution
    """
```

### Memory Information

Query memory usage and availability on CUDA devices.

```python { .api }
def cudaMemGetInfo() -> tuple:
    """
    Get memory information for the current device.
    
    Returns:
        tuple[int, int]: (free_memory, total_memory) in bytes
    """

def cudaPointerGetAttributes(ptr: int) -> cudaPointerAttributes:
    """
    Get attributes of a memory pointer.
    
    Args:
        ptr (int): Memory pointer to query
    
    Returns:
        cudaPointerAttributes: Pointer attributes structure
    """
```

## Types

### Memory Copy Directions

```python { .api }
class cudaMemcpyKind:
    """Memory copy direction enumeration"""
    cudaMemcpyHostToHost: int
    cudaMemcpyHostToDevice: int  
    cudaMemcpyDeviceToHost: int
    cudaMemcpyDeviceToDevice: int
    cudaMemcpyDefault: int  # Infer direction automatically
```

### Device Attributes

```python { .api }
class cudaDeviceAttr:
    """CUDA device attribute enumeration"""
    cudaDevAttrMaxThreadsPerBlock: int
    cudaDevAttrMaxBlockDimX: int
    cudaDevAttrMaxBlockDimY: int
    cudaDevAttrMaxBlockDimZ: int
    cudaDevAttrMaxGridDimX: int
    cudaDevAttrMaxGridDimY: int
    cudaDevAttrMaxGridDimZ: int
    cudaDevAttrMaxSharedMemoryPerBlock: int
    cudaDevAttrTotalConstantMemory: int
    cudaDevAttrWarpSize: int
    cudaDevAttrMaxPitch: int
    cudaDevAttrMultiProcessorCount: int
    cudaDevAttrClockRate: int
    cudaDevAttrMemoryClockRate: int
    cudaDevAttrMemoryBusWidth: int
```

### Host Allocation Flags

```python { .api }
# Host allocation flag constants
cudaHostAllocDefault: int  # Default page-locked allocation
cudaHostAllocPortable: int  # Portable across CUDA contexts
cudaHostAllocMapped: int  # Map allocation into device address space
cudaHostAllocWriteCombined: int  # Write-combined memory
```

### Device Properties Structure

```python { .api }
class cudaDeviceProp:
    """CUDA device properties structure"""
    name: str  # Device name
    totalGlobalMem: int  # Global memory size in bytes
    sharedMemPerBlock: int  # Shared memory per block
    regsPerBlock: int  # Registers per block
    warpSize: int  # Warp size
    memPitch: int  # Maximum pitch in bytes
    maxThreadsPerBlock: int  # Maximum threads per block
    maxThreadsDim: tuple  # Maximum block dimensions
    maxGridSize: tuple  # Maximum grid dimensions
    clockRate: int  # Clock frequency in kHz
    totalConstMem: int  # Constant memory size
    major: int  # Compute capability major version
    minor: int  # Compute capability minor version
    multiProcessorCount: int  # Number of SMs
```

### Pointer Attributes

```python { .api }
class cudaPointerAttributes:
    """Memory pointer attributes structure"""
    type: int  # Memory type (host, device, managed)
    device: int  # Device where pointer resides
    devicePointer: int  # Device pointer value
    hostPointer: int  # Host pointer value
```

## Usage Examples

### Basic Device Management

```python
from cuda.bindings import runtime

# Check available devices
device_count = runtime.cudaGetDeviceCount()
print(f"Found {device_count} CUDA devices")

# Select and query device
runtime.cudaSetDevice(0)
current_device = runtime.cudaGetDevice()
print(f"Using device {current_device}")

# Get device properties
props = runtime.cudaGetDeviceProperties(0)
print(f"Device: {props.name}")
print(f"Compute Capability: {props.major}.{props.minor}")
print(f"Global Memory: {props.totalGlobalMem // (1024**3)} GB")
```

### Memory Operations

```python
from cuda.bindings import runtime

# Allocate memory
size = 1024 * 1024  # 1MB
device_ptr = runtime.cudaMalloc(size)
host_ptr = runtime.cudaMallocHost(size)

# Transfer data
runtime.cudaMemcpy(
    device_ptr, host_ptr, size,
    runtime.cudaMemcpyKind.cudaMemcpyHostToDevice
)

# Check memory usage
free_mem, total_mem = runtime.cudaMemGetInfo()
print(f"Free: {free_mem // (1024**2)} MB")
print(f"Total: {total_mem // (1024**2)} MB")

# Cleanup
runtime.cudaFree(device_ptr)
runtime.cudaFreeHost(host_ptr)
```