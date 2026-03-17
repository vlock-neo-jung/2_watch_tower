# Low-Level Driver API

Direct CUDA Driver API access for advanced GPU programming including context management, module loading, and fine-grained resource control. The Driver API provides the lowest-level interface to CUDA functionality, offering maximum flexibility and control over GPU resources.

## Capabilities

### Driver Initialization

Initialize the CUDA driver and enumerate available devices.

```python { .api }
def cuInit(flags: int) -> None:
    """
    Initialize the CUDA driver API.
    
    Args:
        flags (int): Initialization flags (must be 0)
    
    Note:
        Must be called before any other driver API functions
    
    Raises:
        CUresult: If initialization fails
    """

def cuDriverGetVersion() -> int:
    """
    Get the version of the CUDA driver.
    
    Returns:
        int: Driver version number
    """
```

### Device Management

Enumerate and query CUDA devices at the driver level.

```python { .api }
def cuDeviceGet(ordinal: int) -> int:
    """
    Get a device handle for a specific device ordinal.
    
    Args:
        ordinal (int): Device index (0-based)
    
    Returns:
        int: Device handle
    
    Raises:
        CUresult: If device ordinal is invalid
    """

def cuDeviceGetCount() -> int:
    """
    Get the number of CUDA-capable devices.
    
    Returns:
        int: Number of available devices
    """

def cuDeviceGetName(device: int) -> str:
    """
    Get the name of a CUDA device.
    
    Args:
        device (int): Device handle
    
    Returns:
        str: Device name string
    """

def cuDeviceGetAttribute(attrib: CUdevice_attribute, device: int) -> int:
    """
    Get a specific attribute value from a device.
    
    Args:
        attrib (CUdevice_attribute): Attribute to query
        device (int): Device handle
    
    Returns:
        int: Attribute value
    """

def cuDeviceTotalMem(device: int) -> int:
    """
    Get the total amount of memory on a device.
    
    Args:
        device (int): Device handle
    
    Returns:
        int: Total memory in bytes
    """
```

### Context Management

Create and manage CUDA contexts for device operations.

```python { .api }
def cuCtxCreate(flags: int, device: int) -> int:
    """
    Create a CUDA context for a device.
    
    Args:
        flags (int): Context creation flags
        device (int): Device handle
    
    Returns:
        int: Context handle
    
    Note:
        Context becomes current upon creation
    """

def cuCtxDestroy(ctx: int) -> None:
    """
    Destroy a CUDA context and free associated resources.
    
    Args:
        ctx (int): Context handle to destroy
    """

def cuCtxGetCurrent() -> int:
    """
    Get the current CUDA context.
    
    Returns:
        int: Current context handle (0 if no current context)
    """

def cuCtxSetCurrent(ctx: int) -> None:
    """
    Set the current CUDA context.
    
    Args:
        ctx (int): Context handle to make current
    """

def cuCtxPushCurrent(ctx: int) -> None:
    """
    Push a context onto the current CPU thread's context stack.
    
    Args:
        ctx (int): Context handle to push
    """

def cuCtxPopCurrent() -> int:
    """
    Pop the current context from the CPU thread's context stack.
    
    Returns:
        int: Popped context handle
    """

def cuCtxSynchronize() -> None:
    """
    Block until all operations in the current context complete.
    
    Note:
        Equivalent to cudaDeviceSynchronize() for current context
    """
```

### Memory Management

Low-level memory allocation and management operations.

```python { .api }
def cuMemAlloc(bytesize: int) -> int:
    """
    Allocate device memory.
    
    Args:
        bytesize (int): Number of bytes to allocate
    
    Returns:
        int: Device memory pointer
    
    Raises:
        CUresult: If allocation fails
    """

def cuMemFree(dptr: int) -> None:
    """
    Free device memory.
    
    Args:
        dptr (int): Device pointer to free
    """

def cuMemAllocHost(bytesize: int) -> int:
    """
    Allocate page-locked host memory.
    
    Args:
        bytesize (int): Number of bytes to allocate
    
    Returns:
        int: Host memory pointer
    """

def cuMemFreeHost(p: int) -> None:
    """
    Free page-locked host memory.
    
    Args:
        p (int): Host pointer to free
    """

def cuMemcpyHtoD(dstDevice: int, srcHost, ByteCount: int) -> None:
    """
    Copy memory from host to device.
    
    Args:
        dstDevice (int): Destination device pointer
        srcHost: Source host pointer
        ByteCount (int): Number of bytes to copy
    """

def cuMemcpyDtoH(dstHost, srcDevice: int, ByteCount: int) -> None:
    """
    Copy memory from device to host.
    
    Args:
        dstHost: Destination host pointer
        srcDevice (int): Source device pointer
        ByteCount (int): Number of bytes to copy
    """

def cuMemcpyDtoD(dstDevice: int, srcDevice: int, ByteCount: int) -> None:
    """
    Copy memory from device to device.
    
    Args:
        dstDevice (int): Destination device pointer
        srcDevice (int): Source device pointer
        ByteCount (int): Number of bytes to copy
    """
```

### Module and Function Management

Load CUDA modules and manage kernel functions.

```python { .api }
def cuModuleLoad(fname: str) -> int:
    """
    Load a CUDA module from file.
    
    Args:
        fname (str): Path to .cubin or .ptx file
    
    Returns:
        int: Module handle
    
    Raises:
        CUresult: If module loading fails
    """

def cuModuleLoadData(image: bytes) -> int:
    """
    Load a CUDA module from memory.
    
    Args:
        image (bytes): Module binary data (.cubin or .ptx)
    
    Returns:
        int: Module handle
    """

def cuModuleUnload(hmod: int) -> None:
    """
    Unload a CUDA module.
    
    Args:
        hmod (int): Module handle to unload
    """

def cuModuleGetFunction(hmod: int, name: str) -> int:
    """
    Get a function handle from a loaded module.
    
    Args:
        hmod (int): Module handle
        name (str): Function name
    
    Returns:
        int: Function handle
    
    Raises:
        CUresult: If function not found in module
    """

def cuModuleGetGlobal(hmod: int, name: str) -> tuple:
    """
    Get a global variable from a loaded module.
    
    Args:
        hmod (int): Module handle
        name (str): Global variable name
    
    Returns:
        tuple[int, int]: (device_pointer, size_in_bytes)
    """
```

### Kernel Execution

Launch kernels with low-level control over execution parameters.

```python { .api }
def cuLaunchKernel(
    f: int,
    gridDimX: int, gridDimY: int, gridDimZ: int,
    blockDimX: int, blockDimY: int, blockDimZ: int,
    sharedMemBytes: int,
    hStream: int,
    kernelParams,
    extra
) -> None:
    """
    Launch a CUDA kernel.
    
    Args:
        f (int): Function handle
        gridDimX, gridDimY, gridDimZ (int): Grid dimensions
        blockDimX, blockDimY, blockDimZ (int): Block dimensions
        sharedMemBytes (int): Dynamic shared memory per block
        hStream (int): Stream handle (0 for default stream)
        kernelParams: Kernel parameter array
        extra: Extra options (typically None)
    
    Note:
        Provides maximum control over kernel launch parameters
    """

def cuFuncSetAttribute(hfunc: int, attrib: CUfunction_attribute, value: int) -> None:
    """
    Set an attribute for a kernel function.
    
    Args:
        hfunc (int): Function handle
        attrib (CUfunction_attribute): Attribute to set
        value (int): Attribute value
    """

def cuFuncGetAttribute(attrib: CUfunction_attribute, hfunc: int) -> int:
    """
    Get an attribute value from a kernel function.
    
    Args:
        attrib (CUfunction_attribute): Attribute to query
        hfunc (int): Function handle
    
    Returns:
        int: Attribute value
    """
```

### Stream Operations

Low-level stream management for asynchronous operations.

```python { .api }
def cuStreamCreate(flags: int) -> int:
    """
    Create a CUDA stream.
    
    Args:
        flags (int): Stream creation flags
    
    Returns:
        int: Stream handle
    """

def cuStreamDestroy(hStream: int) -> None:
    """
    Destroy a CUDA stream.
    
    Args:
        hStream (int): Stream handle to destroy
    """

def cuStreamSynchronize(hStream: int) -> None:
    """
    Wait for all operations in a stream to complete.
    
    Args:
        hStream (int): Stream handle to synchronize
    """

def cuStreamQuery(hStream: int) -> CUresult:
    """
    Query the status of operations in a stream.
    
    Args:
        hStream (int): Stream handle to query
    
    Returns:
        CUresult: CUDA_SUCCESS if complete, CUDA_ERROR_NOT_READY if pending
    """
```

## Types

### Result Codes

```python { .api }
class CUresult:
    """CUDA Driver API result codes"""
    CUDA_SUCCESS: int  # No error
    CUDA_ERROR_INVALID_VALUE: int  # Invalid parameter
    CUDA_ERROR_OUT_OF_MEMORY: int  # Out of memory
    CUDA_ERROR_NOT_INITIALIZED: int  # Driver not initialized
    CUDA_ERROR_DEINITIALIZED: int  # Driver deinitialized
    CUDA_ERROR_NO_DEVICE: int  # No CUDA-capable device available
    CUDA_ERROR_INVALID_DEVICE: int  # Invalid device ordinal
    CUDA_ERROR_INVALID_CONTEXT: int  # Invalid context handle
    CUDA_ERROR_CONTEXT_ALREADY_CURRENT: int  # Context already current
    CUDA_ERROR_MAP_FAILED: int  # Memory mapping failed
    CUDA_ERROR_UNMAP_FAILED: int  # Memory unmapping failed
    CUDA_ERROR_ARRAY_IS_MAPPED: int  # Array is mapped
    CUDA_ERROR_ALREADY_MAPPED: int  # Resource already mapped
    CUDA_ERROR_NO_BINARY_FOR_GPU: int  # No binary for GPU
    CUDA_ERROR_ALREADY_ACQUIRED: int  # Resource already acquired
    CUDA_ERROR_NOT_MAPPED: int  # Resource not mapped
    CUDA_ERROR_INVALID_SOURCE: int  # Invalid source
    CUDA_ERROR_FILE_NOT_FOUND: int  # File not found
    CUDA_ERROR_INVALID_HANDLE: int  # Invalid handle
    CUDA_ERROR_NOT_FOUND: int  # Resource not found
    CUDA_ERROR_NOT_READY: int  # Operation not ready
    CUDA_ERROR_LAUNCH_FAILED: int  # Kernel launch failed
    CUDA_ERROR_LAUNCH_OUT_OF_RESOURCES: int  # Too many resources requested
    CUDA_ERROR_LAUNCH_TIMEOUT: int  # Kernel execution timed out
    CUDA_ERROR_UNKNOWN: int  # Unknown error
```

### Device Attributes

```python { .api }
class CUdevice_attribute:
    """CUDA device attributes"""
    CU_DEVICE_ATTRIBUTE_MAX_THREADS_PER_BLOCK: int
    CU_DEVICE_ATTRIBUTE_MAX_BLOCK_DIM_X: int
    CU_DEVICE_ATTRIBUTE_MAX_BLOCK_DIM_Y: int
    CU_DEVICE_ATTRIBUTE_MAX_BLOCK_DIM_Z: int
    CU_DEVICE_ATTRIBUTE_MAX_GRID_DIM_X: int
    CU_DEVICE_ATTRIBUTE_MAX_GRID_DIM_Y: int
    CU_DEVICE_ATTRIBUTE_MAX_GRID_DIM_Z: int
    CU_DEVICE_ATTRIBUTE_SHARED_MEMORY_PER_BLOCK: int
    CU_DEVICE_ATTRIBUTE_TOTAL_CONSTANT_MEMORY: int
    CU_DEVICE_ATTRIBUTE_WARP_SIZE: int
    CU_DEVICE_ATTRIBUTE_MAX_PITCH: int
    CU_DEVICE_ATTRIBUTE_MULTIPROCESSOR_COUNT: int
    CU_DEVICE_ATTRIBUTE_CLOCK_RATE: int
    CU_DEVICE_ATTRIBUTE_MEMORY_CLOCK_RATE: int
    CU_DEVICE_ATTRIBUTE_GLOBAL_MEMORY_BUS_WIDTH: int
    CU_DEVICE_ATTRIBUTE_COMPUTE_CAPABILITY_MAJOR: int
    CU_DEVICE_ATTRIBUTE_COMPUTE_CAPABILITY_MINOR: int
```

### Context Creation Flags

```python { .api }
# Context creation flag constants
CU_CTX_SCHED_AUTO: int  # Automatic scheduling
CU_CTX_SCHED_SPIN: int  # Spin when waiting for results
CU_CTX_SCHED_YIELD: int  # Yield when waiting for results
CU_CTX_SCHED_BLOCKING_SYNC: int  # Use blocking synchronization
CU_CTX_MAP_HOST: int  # Enable mapped pinned allocations
CU_CTX_LMEM_RESIZE_TO_MAX: int  # Resize local memory to maximum
```

### Function Attributes

```python { .api }
class CUfunction_attribute:
    """Kernel function attributes"""
    CU_FUNC_ATTRIBUTE_MAX_THREADS_PER_BLOCK: int
    CU_FUNC_ATTRIBUTE_SHARED_SIZE_BYTES: int
    CU_FUNC_ATTRIBUTE_CONST_SIZE_BYTES: int
    CU_FUNC_ATTRIBUTE_LOCAL_SIZE_BYTES: int
    CU_FUNC_ATTRIBUTE_NUM_REGS: int
    CU_FUNC_ATTRIBUTE_PTX_VERSION: int
    CU_FUNC_ATTRIBUTE_BINARY_VERSION: int
    CU_FUNC_ATTRIBUTE_CACHE_MODE_CA: int
    CU_FUNC_ATTRIBUTE_MAX_DYNAMIC_SHARED_SIZE_BYTES: int
    CU_FUNC_ATTRIBUTE_PREFERRED_SHARED_MEMORY_CARVEOUT: int
```

### Stream Flags

```python { .api }
# Stream creation flag constants  
CU_STREAM_DEFAULT: int  # Default stream behavior
CU_STREAM_NON_BLOCKING: int  # Non-blocking stream
```

## Usage Examples

### Basic Driver API Setup

```python
from cuda.bindings import driver

# Initialize driver
driver.cuInit(0)

# Get device count and select device
device_count = driver.cuDeviceGetCount()
device = driver.cuDeviceGet(0)

# Get device info
device_name = driver.cuDeviceGetName(device)
total_mem = driver.cuDeviceTotalMem(device)
print(f"Device: {device_name}, Memory: {total_mem // (1024**3)} GB")

# Create context
context = driver.cuCtxCreate(driver.CU_CTX_SCHED_AUTO, device)
```

### Module Loading and Kernel Execution

```python
from cuda.bindings import driver

# Load module from PTX or CUBIN file
module = driver.cuModuleLoad("kernel.ptx")

# Get kernel function
kernel_func = driver.cuModuleGetFunction(module, "my_kernel")

# Allocate memory
device_ptr = driver.cuMemAlloc(1024)
host_data = b"x" * 1024
driver.cuMemcpyHtoD(device_ptr, host_data, 1024)

# Launch kernel
grid_dim = (1, 1, 1)
block_dim = (256, 1, 1)
kernel_params = [device_ptr, 1024]

driver.cuLaunchKernel(
    kernel_func,
    grid_dim[0], grid_dim[1], grid_dim[2],
    block_dim[0], block_dim[1], block_dim[2],
    0,  # shared memory
    0,  # stream
    kernel_params,
    None  # extra
)

# Synchronize and retrieve results
driver.cuCtxSynchronize()
result_data = bytearray(1024)
driver.cuMemcpyDtoH(result_data, device_ptr, 1024)

# Cleanup
driver.cuMemFree(device_ptr)
driver.cuModuleUnload(module)
```

### Context Management

```python
from cuda.bindings import driver

# Initialize and create contexts for multiple devices
driver.cuInit(0)
contexts = []

for i in range(driver.cuDeviceGetCount()):
    device = driver.cuDeviceGet(i)
    ctx = driver.cuCtxCreate(driver.CU_CTX_SCHED_AUTO, device)
    contexts.append(ctx)
    # Context is automatically current after creation
    print(f"Created context for device {i}")

# Switch between contexts
for i, ctx in enumerate(contexts):
    driver.cuCtxSetCurrent(ctx)
    current_ctx = driver.cuCtxGetCurrent()
    print(f"Context {i} is current: {current_ctx == ctx}")

# Cleanup contexts
for ctx in contexts:
    driver.cuCtxDestroy(ctx)
```