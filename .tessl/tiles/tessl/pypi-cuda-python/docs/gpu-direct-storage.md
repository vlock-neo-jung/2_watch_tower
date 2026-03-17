# GPU Direct Storage

cuFile GPU Direct Storage API for high-performance direct GPU I/O operations bypassing CPU and system memory. This module enables direct data transfers between storage devices and GPU memory, significantly reducing I/O latency and CPU overhead for large-scale data processing workloads.

## Capabilities

### Driver and System Management

Initialize and manage the cuFile driver for GPU Direct Storage operations.

```python { .api }
def driver_open() -> None:
    """
    Open the cuFile driver for GPU Direct Storage.
    
    Note:
        Must be called before any other cuFile operations
        
    Raises:
        cuFileError: If driver initialization fails
    """

def driver_close() -> None:
    """
    Close the cuFile driver and release system resources.
    
    Note:
        Should be called when GPU Direct Storage is no longer needed
    """

def get_version() -> int:
    """
    Get the cuFile library version.
    
    Returns:
        int: Version number in packed format
    """
```

### File Handle Management

Register and manage file handles for GPU Direct Storage operations.

```python { .api }
def handle_register(descr: int) -> int:
    """
    Register a file descriptor for GPU Direct Storage.
    
    Args:
        descr (int): File descriptor (from open() syscall)
    
    Returns:
        int: cuFile handle for GPU operations
    
    Note:
        File must be opened with appropriate flags for direct I/O
        
    Raises:
        cuFileError: If registration fails
    """

def handle_deregister(fh: int) -> None:
    """
    Deregister a cuFile handle and release associated resources.
    
    Args:
        fh (int): cuFile handle to deregister
    
    Note:
        Handle becomes invalid after deregistration
    """
```

### Buffer Management

Register GPU memory buffers for direct I/O operations.

```python { .api }
def buf_register(devPtr_base: int, size: int, flags: int) -> None:
    """
    Register a GPU memory buffer for cuFile operations.
    
    Args:
        devPtr_base (int): Base address of GPU memory buffer
        size (int): Buffer size in bytes
        flags (int): Registration flags
    
    Note:
        Buffer must remain valid for duration of registration
        
    Raises:
        cuFileError: If buffer registration fails
    """

def buf_deregister(devPtr_base: int) -> None:
    """
    Deregister a GPU memory buffer.
    
    Args:
        devPtr_base (int): Base address of previously registered buffer
    """
```

### Synchronous I/O Operations

Perform synchronous read and write operations between storage and GPU memory.

```python { .api }
def read(
    fh: int,
    buf_ptr_base: int,
    size: int,
    file_offset: int,
    buf_ptr_offset: int
) -> None:
    """
    Synchronously read data from file to GPU memory.
    
    Args:
        fh (int): cuFile handle
        buf_ptr_base (int): GPU buffer base address
        size (int): Number of bytes to read  
        file_offset (int): Offset in file to read from
        buf_ptr_offset (int): Offset in GPU buffer to write to
    
    Note:
        Blocks until read operation completes
        
    Raises:
        cuFileError: If read operation fails
    """

def write(
    fh: int,
    buf_ptr_base: int,
    size: int,
    file_offset: int,
    buf_ptr_offset: int
) -> None:
    """
    Synchronously write data from GPU memory to file.
    
    Args:
        fh (int): cuFile handle
        buf_ptr_base (int): GPU buffer base address
        size (int): Number of bytes to write
        file_offset (int): Offset in file to write to
        buf_ptr_offset (int): Offset in GPU buffer to read from
    
    Note:
        Blocks until write operation completes
        
    Raises:
        cuFileError: If write operation fails
    """

def pread(
    fh: int,
    buf_ptr_base: int,
    size: int,
    file_offset: int,
    buf_ptr_offset: int
) -> int:
    """
    Synchronously read with explicit file positioning.
    
    Args:
        fh (int): cuFile handle
        buf_ptr_base (int): GPU buffer base address
        size (int): Number of bytes to read
        file_offset (int): File position to read from
        buf_ptr_offset (int): Buffer offset to write to
    
    Returns:
        int: Number of bytes actually read
    """

def pwrite(
    fh: int,
    buf_ptr_base: int,
    size: int,
    file_offset: int,
    buf_ptr_offset: int
) -> int:
    """
    Synchronously write with explicit file positioning.
    
    Args:
        fh (int): cuFile handle
        buf_ptr_base (int): GPU buffer base address
        size (int): Number of bytes to write
        file_offset (int): File position to write to
        buf_ptr_offset (int): Buffer offset to read from
    
    Returns:
        int: Number of bytes actually written
    """
```

### Asynchronous I/O Operations

Perform asynchronous I/O operations for maximum throughput and concurrency.

```python { .api }
def read_async(
    fh: int,
    buf_ptr_base: int,
    size: int,
    file_offset: int,
    buf_ptr_offset: int,
    bytes_read_ptr: int,
    stream: int
) -> None:
    """
    Asynchronously read data from file to GPU memory.
    
    Args:
        fh (int): cuFile handle
        buf_ptr_base (int): GPU buffer base address
        size (int): Number of bytes to read
        file_offset (int): Offset in file to read from
        buf_ptr_offset (int): Offset in GPU buffer to write to
        bytes_read_ptr (int): Pointer to receive actual bytes read
        stream (int): CUDA stream for asynchronous execution
    
    Note:
        Returns immediately; use stream synchronization to wait
    """

def write_async(
    fh: int,
    buf_ptr_base: int,
    size: int,
    file_offset: int,
    buf_ptr_offset: int,
    bytes_written_ptr: int,
    stream: int
) -> None:
    """
    Asynchronously write data from GPU memory to file.
    
    Args:
        fh (int): cuFile handle
        buf_ptr_base (int): GPU buffer base address
        size (int): Number of bytes to write
        file_offset (int): Offset in file to write to
        buf_ptr_offset (int): Offset in GPU buffer to read from
        bytes_written_ptr (int): Pointer to receive actual bytes written
        stream (int): CUDA stream for asynchronous execution
    
    Note:
        Returns immediately; use stream synchronization to wait
    """
```

### Batch I/O Operations

Perform multiple I/O operations efficiently using batch APIs.

```python { .api }
def readv(
    fh: int,
    iov: list,
    iovcnt: int,
    file_offset: int,
    bytes_read_ptr: int
) -> None:
    """
    Vector read operation - read into multiple buffers.
    
    Args:
        fh (int): cuFile handle
        iov (list): List of I/O vector structures
        iovcnt (int): Number of I/O vectors
        file_offset (int): Starting file offset
        bytes_read_ptr (int): Pointer to receive total bytes read
    
    Note:
        Enables efficient reading into scattered GPU memory regions
    """

def writev(
    fh: int,
    iov: list,
    iovcnt: int,
    file_offset: int,
    bytes_written_ptr: int
) -> None:
    """
    Vector write operation - write from multiple buffers.
    
    Args:
        fh (int): cuFile handle
        iov (list): List of I/O vector structures
        iovcnt (int): Number of I/O vectors
        file_offset (int): Starting file offset
        bytes_written_ptr (int): Pointer to receive total bytes written
    
    Note:
        Enables efficient writing from scattered GPU memory regions
    """
```

### Properties and Configuration

Query and configure cuFile properties and behavior.

```python { .api }
def get_file_properties(fh: int) -> dict:
    """
    Get properties of a registered file handle.
    
    Args:
        fh (int): cuFile handle
    
    Returns:
        dict: File properties including direct I/O capabilities
    """

def set_file_properties(fh: int, props: dict) -> None:
    """
    Set properties for a file handle.
    
    Args:
        fh (int): cuFile handle
        props (dict): Properties to set
    """
```

## Types

### Status and Error Codes

```python { .api }
class Status:
    """cuFile operation status codes"""
    CU_FILE_SUCCESS: int  # Operation successful
    CU_FILE_INVALID_VALUE: int  # Invalid parameter value
    CU_FILE_INVALID_HANDLE: int  # Invalid file handle
    CU_FILE_CUDA_MEMORY_TYPE_NOT_SUPPORTED: int  # Memory type not supported
    CU_FILE_IO_NOT_SUPPORTED: int  # I/O operation not supported
    CU_FILE_PERMISSION_DENIED: int  # Permission denied
    CU_FILE_INVALID_FILE_OPEN_FLAG: int  # Invalid file open flags
    CU_FILE_MEMORY_ALREADY_REGISTERED: int  # Memory already registered
    CU_FILE_MEMORY_NOT_REGISTERED: int  # Memory not registered
    CU_FILE_PLATFORM_NOT_SUPPORTED: int  # Platform not supported
    CU_FILE_FILE_SYSTEM_NOT_SUPPORTED: int  # File system not supported
```

### Operation Error Codes

```python { .api }
class OpError:
    """cuFile detailed operation error codes"""
    CU_FILE_OP_SUCCESS: int  # Operation successful
    CU_FILE_OP_FAILED: int  # Operation failed
    CU_FILE_OP_INVALID_ARG: int  # Invalid argument
    CU_FILE_OP_IO_FAILED: int  # I/O operation failed
    CU_FILE_OP_MEMORY_INVALID: int  # Memory access error
    CU_FILE_OP_PARTIAL_COMPLETION: int  # Partial operation completion
```

### Feature Flags

```python { .api }
class FeatureFlags:
    """cuFile feature availability flags"""
    CU_FILE_FEATURE_GDS_SUPPORTED: int  # GPU Direct Storage supported
    CU_FILE_FEATURE_BATCH_IO_SUPPORTED: int  # Batch I/O supported
    CU_FILE_FEATURE_ASYNC_IO_SUPPORTED: int  # Async I/O supported
    CU_FILE_FEATURE_VECTOR_IO_SUPPORTED: int  # Vector I/O supported
```

### File Handle Types

```python { .api }
class FileHandleType:
    """cuFile handle type enumeration"""
    CU_FILE_HANDLE_TYPE_OPAQUE_FD: int  # Opaque file descriptor
    CU_FILE_HANDLE_TYPE_OPAQUE_WIN32: int  # Windows handle
```

### Buffer Registration Flags

```python { .api }
# Buffer registration flag constants
CU_FILE_BUF_REGISTER_FLAGS_NONE: int  # No special flags
CU_FILE_BUF_REGISTER_FLAGS_READ_ONLY: int  # Buffer for read operations only
CU_FILE_BUF_REGISTER_FLAGS_WRITE_ONLY: int  # Buffer for write operations only
```

### Exception Classes

```python { .api }
class cuFileError(Exception):
    """cuFile operation exception"""
    def __init__(self, status: Status, message: str): ...
```

### I/O Vector Structure

```python { .api }
class IOVec:
    """I/O vector structure for batch operations"""
    ptr: int  # GPU memory pointer
    size: int  # Transfer size in bytes
    file_offset: int  # File offset for this vector
    buf_offset: int  # Buffer offset for this vector
```

## Usage Examples

### Basic File I/O

```python
from cuda.bindings import cufile, runtime
import os

# Initialize cuFile driver
cufile.driver_open()

try:
    # Open file for direct I/O
    fd = os.open("large_dataset.dat", os.O_RDONLY | os.O_DIRECT)
    cufile_handle = cufile.handle_register(fd)
    
    # Allocate GPU memory
    buffer_size = 1024 * 1024 * 64  # 64MB
    gpu_buffer = runtime.cudaMalloc(buffer_size)
    
    # Register GPU buffer
    cufile.buf_register(gpu_buffer, buffer_size, 
                       cufile.CU_FILE_BUF_REGISTER_FLAGS_NONE)
    
    # Read data directly to GPU
    cufile.read(cufile_handle, gpu_buffer, buffer_size, 0, 0)
    
    print(f"Read {buffer_size} bytes directly to GPU memory")
    
    # Process data on GPU...
    
    # Cleanup
    cufile.buf_deregister(gpu_buffer)
    runtime.cudaFree(gpu_buffer)
    cufile.handle_deregister(cufile_handle)
    os.close(fd)
    
finally:
    cufile.driver_close()
```

### Asynchronous I/O with Streams

```python
from cuda.bindings import cufile, runtime
import os

def async_gpu_io_pipeline():
    """Demonstrate asynchronous GPU I/O with CUDA streams."""
    
    cufile.driver_open()
    
    # Create CUDA streams for overlapping operations
    compute_stream = runtime.cudaStreamCreate()
    io_stream = runtime.cudaStreamCreate()
    
    try:
        # Open input and output files
        input_fd = os.open("input.dat", os.O_RDONLY | os.O_DIRECT)
        output_fd = os.open("output.dat", os.O_WRONLY | os.O_CREAT | os.O_DIRECT, 0o644)
        
        input_handle = cufile.handle_register(input_fd)
        output_handle = cufile.handle_register(output_fd)
        
        # Allocate double-buffered GPU memory
        chunk_size = 1024 * 1024 * 32  # 32MB chunks
        buffer1 = runtime.cudaMalloc(chunk_size)
        buffer2 = runtime.cudaMalloc(chunk_size)
        
        # Register buffers
        cufile.buf_register(buffer1, chunk_size, cufile.CU_FILE_BUF_REGISTER_FLAGS_NONE)
        cufile.buf_register(buffer2, chunk_size, cufile.CU_FILE_BUF_REGISTER_FLAGS_NONE)
        
        file_offset = 0
        current_buffer = buffer1
        next_buffer = buffer2
        
        # Allocate space for async result tracking
        bytes_read_ptr = runtime.cudaMalloc(8)  # sizeof(size_t)
        bytes_written_ptr = runtime.cudaMalloc(8)
        
        while True:
            # Start async read into next buffer
            cufile.read_async(
                input_handle, next_buffer, chunk_size, 
                file_offset + chunk_size, 0, bytes_read_ptr, io_stream
            )
            
            # Process current buffer on compute stream
            # ... kernel launch on current_buffer using compute_stream ...
            
            # Write processed data asynchronously
            cufile.write_async(
                output_handle, current_buffer, chunk_size,
                file_offset, 0, bytes_written_ptr, io_stream
            )
            
            # Synchronize I/O stream
            runtime.cudaStreamSynchronize(io_stream)
            
            # Check bytes read
            bytes_read = runtime.cudaMemcpy(
                bytes_read_ptr, None, 8, 
                runtime.cudaMemcpyKind.cudaMemcpyDeviceToHost
            )
            
            if bytes_read < chunk_size:
                break  # End of file
            
            # Swap buffers
            current_buffer, next_buffer = next_buffer, current_buffer
            file_offset += chunk_size
        
        print(f"Processed {file_offset} bytes with async I/O")
        
    finally:
        # Cleanup
        runtime.cudaFree(bytes_read_ptr)
        runtime.cudaFree(bytes_written_ptr)
        cufile.buf_deregister(buffer1)
        cufile.buf_deregister(buffer2)
        runtime.cudaFree(buffer1)
        runtime.cudaFree(buffer2)
        cufile.handle_deregister(input_handle)
        cufile.handle_deregister(output_handle)
        os.close(input_fd)
        os.close(output_fd)
        runtime.cudaStreamDestroy(compute_stream)
        runtime.cudaStreamDestroy(io_stream)
        cufile.driver_close()

# Run the pipeline
async_gpu_io_pipeline()
```

### Vector I/O for Scattered Data

```python
from cuda.bindings import cufile, runtime
import os

def scattered_io_example():
    """Demonstrate vector I/O for scattered data access."""
    
    cufile.driver_open()
    
    try:
        # Open sparse data file
        fd = os.open("sparse_matrix.dat", os.O_RDONLY | os.O_DIRECT)
        cufile_handle = cufile.handle_register(fd)
        
        # Allocate multiple GPU buffers for different matrix blocks
        block_size = 1024 * 1024  # 1MB per block
        num_blocks = 4
        gpu_buffers = []
        
        for i in range(num_blocks):
            buffer = runtime.cudaMalloc(block_size)
            cufile.buf_register(buffer, block_size, 
                               cufile.CU_FILE_BUF_REGISTER_FLAGS_READ_ONLY)
            gpu_buffers.append(buffer)
        
        # Define I/O vectors for scattered reads
        iov_list = []
        file_offsets = [0, 1024*1024*10, 1024*1024*50, 1024*1024*100]  # Sparse offsets
        
        for i, (buffer, offset) in enumerate(zip(gpu_buffers, file_offsets)):
            iov = cufile.IOVec()
            iov.ptr = buffer
            iov.size = block_size
            iov.file_offset = offset
            iov.buf_offset = 0
            iov_list.append(iov)
        
        # Perform vector read
        bytes_read_ptr = runtime.cudaMalloc(8)
        cufile.readv(cufile_handle, iov_list, len(iov_list), 0, bytes_read_ptr)
        
        # Get total bytes read
        total_bytes = runtime.cudaMemcpy(
            bytes_read_ptr, None, 8,
            runtime.cudaMemcpyKind.cudaMemcpyDeviceToHost
        )
        
        print(f"Vector read {total_bytes} bytes from {len(iov_list)} scattered locations")
        
        # Process each block on GPU...
        
        # Cleanup
        runtime.cudaFree(bytes_read_ptr)
        for buffer in gpu_buffers:
            cufile.buf_deregister(buffer)
            runtime.cudaFree(buffer)
        cufile.handle_deregister(cufile_handle)
        os.close(fd)
        
    finally:
        cufile.driver_close()

# Run scattered I/O example
scattered_io_example()
```

### Performance Monitoring and Tuning

```python
from cuda.bindings import cufile, runtime
import os
import time

class GPUIOProfiler:
    """Profile GPU Direct Storage performance."""
    
    def __init__(self):
        self.stats = {
            'total_bytes': 0,
            'total_time': 0,
            'operations': 0
        }
    
    def profile_read(self, file_path, buffer_size, num_iterations=10):
        """Profile read performance."""
        
        cufile.driver_open()
        
        try:
            # Setup
            fd = os.open(file_path, os.O_RDONLY | os.O_DIRECT)
            cufile_handle = cufile.handle_register(fd)
            
            gpu_buffer = runtime.cudaMalloc(buffer_size)
            cufile.buf_register(gpu_buffer, buffer_size, 
                               cufile.CU_FILE_BUF_REGISTER_FLAGS_READ_ONLY)
            
            # Create events for timing
            start_event = runtime.cudaEventCreate()
            end_event = runtime.cudaEventCreate()
            
            total_time = 0
            
            for i in range(num_iterations):
                # Record start time
                runtime.cudaEventRecord(start_event)
                
                # Perform read
                cufile.read(cufile_handle, gpu_buffer, buffer_size, 
                           i * buffer_size, 0)
                
                # Record end time
                runtime.cudaEventRecord(end_event)
                runtime.cudaEventSynchronize(end_event)
                
                # Calculate elapsed time
                elapsed_ms = runtime.cudaEventElapsedTime(start_event, end_event)
                total_time += elapsed_ms
                
                self.stats['total_bytes'] += buffer_size
                self.stats['operations'] += 1
            
            self.stats['total_time'] += total_time / 1000  # Convert to seconds
            
            # Calculate metrics
            avg_time_ms = total_time / num_iterations
            throughput_gbps = (buffer_size * num_iterations / (1024**3)) / (total_time / 1000)
            
            print(f"GPU Direct Storage Read Performance:")
            print(f"  Buffer Size: {buffer_size // (1024*1024)} MB")
            print(f"  Iterations: {num_iterations}")
            print(f"  Average Time: {avg_time_ms:.3f} ms")
            print(f"  Throughput: {throughput_gbps:.2f} GB/s")
            
            # Cleanup
            runtime.cudaEventDestroy(start_event)
            runtime.cudaEventDestroy(end_event)
            cufile.buf_deregister(gpu_buffer)
            runtime.cudaFree(gpu_buffer)
            cufile.handle_deregister(cufile_handle)
            os.close(fd)
            
        finally:
            cufile.driver_close()
    
    def get_summary(self):
        """Get overall performance summary."""
        if self.stats['operations'] > 0:
            avg_throughput = (self.stats['total_bytes'] / (1024**3)) / self.stats['total_time']
            return {
                'total_data_gb': self.stats['total_bytes'] / (1024**3),
                'total_time_s': self.stats['total_time'],
                'operations': self.stats['operations'],
                'avg_throughput_gbps': avg_throughput
            }
        return self.stats

# Example usage
profiler = GPUIOProfiler()

# Profile different buffer sizes
buffer_sizes = [1024*1024, 16*1024*1024, 64*1024*1024]  # 1MB, 16MB, 64MB

for size in buffer_sizes:
    try:
        profiler.profile_read("test_data.dat", size, num_iterations=5)
    except Exception as e:
        print(f"Profiling failed for {size} bytes: {e}")

# Print summary
summary = profiler.get_summary()
if summary:
    print(f"\nOverall Summary:")
    print(f"  Total Data: {summary['total_data_gb']:.2f} GB")
    print(f"  Total Time: {summary['total_time_s']:.2f} s")
    print(f"  Operations: {summary['operations']}")
    print(f"  Average Throughput: {summary['avg_throughput_gbps']:.2f} GB/s")
```