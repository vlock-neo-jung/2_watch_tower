# CUDA Python

CUDA Python provides comprehensive access to NVIDIA's CUDA platform from Python through a unified metapackage that combines low-level CUDA C API bindings with high-level utilities. It enables end-to-end GPU development entirely in Python while maintaining access to the full breadth of CUDA functionality, serving as the authoritative entry point to NVIDIA's CUDA ecosystem for Python developers.

## Package Information

- **Package Name**: cuda-python
- **Package Type**: metapackage
- **Language**: Python
- **Installation**: `pip install cuda-python`
- **Complete Installation**: `pip install cuda-python[all]`
- **Components**: 
  - `cuda.core@0.3.3a0` - High-level Pythonic CUDA APIs (experimental)
  - `cuda.bindings@13.0.1` - Low-level CUDA C API bindings
  - `cuda.pathfinder@1.1.1a0` - NVIDIA library discovery utilities

## Core Imports

High-level Pythonic CUDA APIs (recommended for most users):

```python
# High-level device and memory management
from cuda.core.experimental import Device, Stream, Event

# Memory resources and buffers
from cuda.core.experimental import Buffer, DeviceMemoryResource

# Program compilation and kernel execution
from cuda.core.experimental import Program, Kernel, launch

# CUDA graphs for optimization
from cuda.core.experimental import Graph, GraphBuilder
```

Low-level CUDA C API bindings:

```python
# CUDA Runtime API
from cuda.bindings import runtime

# CUDA Driver API
from cuda.bindings import driver

# Runtime compilation
from cuda.bindings import nvrtc

# Library loading utilities
from cuda.pathfinder import load_nvidia_dynamic_lib
```

Package version information:

```python
import cuda.core.experimental
import cuda.bindings
import cuda.pathfinder

print(cuda.core.experimental.__version__)  # "0.3.3a0"
print(cuda.bindings.__version__)  # "13.0.1"
print(cuda.pathfinder.__version__)  # "1.1.1a0"
```

## Basic Usage

Pythonic high-level approach (recommended):

```python
from cuda.core.experimental import Device, Stream, Buffer
import numpy as np

# Device management
device = Device(0)  # Use first CUDA device
print(f"Using device: {device.name}")

# Memory management with high-level Buffer
host_data = np.array([1.0, 2.0, 3.0, 4.0], dtype=np.float32)
buffer = Buffer.from_array(host_data, device=device)

# Stream management
stream = Stream(device)

# Synchronization
stream.synchronize()
```

Low-level approach for advanced users:

```python
from cuda.bindings import runtime
from cuda.pathfinder import load_nvidia_dynamic_lib

# Basic device management
device_count = runtime.cudaGetDeviceCount()
print(f"Available CUDA devices: {device_count}")

# Memory allocation and management
device_ptr = runtime.cudaMalloc(1024)  # Allocate 1KB on device
host_ptr = runtime.cudaMallocHost(1024)  # Allocate page-locked host memory

# Copy data between host and device
runtime.cudaMemcpy(
    device_ptr, host_ptr, 1024, 
    runtime.cudaMemcpyKind.cudaMemcpyHostToDevice
)

# Synchronize and cleanup
runtime.cudaDeviceSynchronize()
runtime.cudaFree(device_ptr)
runtime.cudaFreeHost(host_ptr)

# Load NVIDIA libraries dynamically
cudart_lib = load_nvidia_dynamic_lib("cudart")
print(f"CUDA Runtime loaded from: {cudart_lib.abs_path}")
```

## Architecture

CUDA Python is structured as a metapackage that provides unified access to multiple specialized components:

### Core Components

- **cuda.core** (v0.3.3a0): Experimental high-level Pythonic APIs for idiomatic CUDA development
- **cuda.bindings** (v13.0.1): Low-level Python bindings to CUDA C APIs providing complete coverage of CUDA functionality
- **cuda.pathfinder** (v1.1.1a0): Utility library for discovering and loading NVIDIA CUDA libraries dynamically

### API Hierarchy

The package exposes APIs at multiple abstraction levels:

- **High-level Pythonic APIs** (`cuda.core.experimental`): Object-oriented CUDA interface with Device, Stream, Buffer, Program classes
- **Runtime API** (`cuda.bindings.runtime`): Direct bindings to CUDA Runtime C API
- **Driver API** (`cuda.bindings.driver`): Direct bindings to CUDA Driver C API  
- **Compilation APIs**: Runtime compilation (NVRTC) and LLVM-based compilation (NVVM)
- **Utility APIs**: JIT linking, GPU Direct Storage, and library management

This layered approach allows developers to choose the appropriate abstraction level for their needs while maintaining interoperability between components.

## Capabilities

### High-Level Pythonic CUDA (cuda.core.experimental)

Object-oriented CUDA programming with automatic resource management and Pythonic interfaces for device management, memory allocation, stream handling, and kernel execution.

```python { .api }
# Device management
class Device:
    def __init__(self, device_id: int = 0): ...
    @property
    def name(self) -> str: ...
    @property
    def compute_capability(self) -> tuple[int, int]: ...
    def set_current(self) -> None: ...

# Memory management
class Buffer:
    @classmethod
    def from_array(cls, array, device: Device) -> Buffer: ...
    def to_array(self) -> np.ndarray: ...
    @property
    def device(self) -> Device: ...
    @property
    def size(self) -> int: ...

# Stream and event management
class Stream:
    def __init__(self, device: Device): ...
    def synchronize(self) -> None: ...
    def record(self, event: Event) -> None: ...

class Event:
    def __init__(self, device: Device): ...
    def synchronize(self) -> None: ...
    def elapsed_time(self, end_event: Event) -> float: ...

# Program compilation and kernel execution
class Program:
    def __init__(self, code: str, options: ProgramOptions): ...
    def compile(self) -> None: ...
    def get_kernel(self, name: str) -> Kernel: ...

class Kernel:
    def launch(self, config: LaunchConfig, *args) -> None: ...

def launch(kernel: Kernel, config: LaunchConfig, *args) -> None: ...
```

[High-Level CUDA Core APIs](./cuda-core.md)

### Device and Memory Management (Low-Level)

Essential CUDA device enumeration, selection, and memory allocation operations including unified memory, streams, and events for efficient GPU resource management.

```python { .api }
# Device management
def cudaGetDeviceCount() -> int: ...
def cudaSetDevice(device: int) -> None: ...
def cudaGetDevice() -> int: ...

# Memory allocation
def cudaMalloc(size: int) -> int: ...
def cudaMallocHost(size: int) -> int: ...
def cudaMemcpy(dst, src, count: int, kind: cudaMemcpyKind) -> None: ...
def cudaFree(devPtr: int) -> None: ...
```

[Device and Memory Management](./device-memory.md)

### Kernel Execution and Streams

CUDA kernel launching, execution control and asynchronous stream management for optimal GPU utilization and performance.

```python { .api }
# Stream management
def cudaStreamCreate() -> int: ...
def cudaStreamSynchronize(stream: int) -> None: ...
def cudaLaunchKernel(func, gridDim, blockDim, args, sharedMem: int, stream: int) -> None: ...

# Event management
def cudaEventCreate() -> int: ...
def cudaEventRecord(event: int, stream: int) -> None: ...
def cudaEventSynchronize(event: int) -> None: ...
```

[Kernel Execution and Streams](./kernels-streams.md)

### Low-Level Driver API

Direct CUDA Driver API access for advanced GPU programming including context management, module loading, and fine-grained resource control.

```python { .api }
# Driver initialization and devices
def cuInit(flags: int) -> None: ...
def cuDeviceGet(ordinal: int) -> int: ...
def cuCtxCreate(flags: int, device: int) -> int: ...

# Module and function management
def cuModuleLoad(fname: str) -> int: ...
def cuModuleGetFunction(hmod: int, name: str) -> int: ...
def cuLaunchKernel(f, gridDimX, gridDimY, gridDimZ, blockDimX, blockDimY, blockDimZ, sharedMemBytes: int, hStream: int, kernelParams, extra) -> None: ...
```

[Low-Level Driver API](./driver-api.md)

### Runtime Compilation

NVRTC runtime compilation of CUDA C++ source code to PTX and CUBIN formats for dynamic kernel generation and deployment.

```python { .api }
# Program creation and compilation
def nvrtcCreateProgram(src: str, name: str, numHeaders: int, headers: List[bytes], includeNames: List[bytes]) -> int: ...
def nvrtcCompileProgram(prog: int, numOptions: int, options: List[bytes]) -> None: ...
def nvrtcGetPTX(prog: int, ptx: str) -> None: ...
def nvrtcGetCUBIN(prog: int, cubin: str) -> None: ...
```

[Runtime Compilation](./runtime-compilation.md)

### JIT Compilation and Linking

NVVM LLVM-based compilation and NVJitLink just-in-time linking for advanced code generation workflows.

```python { .api }
# NVVM compilation
def create_program() -> int: ...
def compile_program(prog: int, num_options: int, options) -> None: ...

# NVJitLink linking
def create(num_options: int, options) -> int: ...
def add_data(handle: int, input_type: int, data: bytes, size: int, name: str) -> None: ...
def complete(handle: int) -> None: ...
```

[JIT Compilation and Linking](./jit-compilation.md)

### GPU Direct Storage

cuFile GPU Direct Storage API for high-performance direct GPU I/O operations bypassing CPU and system memory.

```python { .api }
# File handle management
def handle_register(descr: int) -> int: ...
def handle_deregister(fh: int) -> None: ...

# I/O operations
def read(fh: int, buf_ptr_base: int, size: int, file_offset: int, buf_ptr_offset: int) -> None: ...
def write(fh: int, buf_ptr_base: int, size: int, file_offset: int, buf_ptr_offset: int) -> None: ...
```

[GPU Direct Storage](./gpu-direct-storage.md)

### Library Management

Dynamic NVIDIA library loading and discovery utilities for runtime library management and version compatibility.

```python { .api }
def load_nvidia_dynamic_lib(libname: str) -> LoadedDL: ...

class LoadedDL:
    abs_path: Optional[str]
    was_already_loaded_from_elsewhere: bool
    _handle_uint: int
```

[Library Management](./library-management.md)

## Types

### Core Enumerations

```python { .api }
class cudaError_t:
    """CUDA Runtime API error codes"""
    cudaSuccess: int
    cudaErrorInvalidValue: int
    cudaErrorMemoryAllocation: int
    # ... additional error codes

class cudaMemcpyKind:
    """Memory copy direction types"""
    cudaMemcpyHostToHost: int
    cudaMemcpyHostToDevice: int
    cudaMemcpyDeviceToHost: int
    cudaMemcpyDeviceToDevice: int

class CUresult:
    """CUDA Driver API result codes"""
    CUDA_SUCCESS: int
    CUDA_ERROR_INVALID_VALUE: int
    CUDA_ERROR_OUT_OF_MEMORY: int
    # ... additional result codes
```

### Device Attributes

```python { .api }
class cudaDeviceAttr:
    """CUDA device attribute enumeration"""
    cudaDevAttrMaxThreadsPerBlock: int
    cudaDevAttrMaxBlockDimX: int
    cudaDevAttrMaxGridDimX: int
    cudaDevAttrMaxSharedMemoryPerBlock: int
    # ... additional device attributes

class CUdevice_attribute:
    """CUDA Driver API device attributes"""
    CU_DEVICE_ATTRIBUTE_MAX_THREADS_PER_BLOCK: int
    CU_DEVICE_ATTRIBUTE_MAX_BLOCK_DIM_X: int
    # ... additional attributes
```

### Exception Classes

```python { .api }
class nvvmError(Exception):
    """NVVM compilation exception"""
    pass

class nvJitLinkError(Exception):
    """NVJitLink exception"""
    pass

class cuFileError(Exception):
    """cuFile operation exception"""
    pass

class DynamicLibNotFoundError(Exception):
    """NVIDIA library not found exception"""
    pass
```