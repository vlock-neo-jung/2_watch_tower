# Runtime Compilation

NVRTC runtime compilation of CUDA C++ source code to PTX and CUBIN formats for dynamic kernel generation and deployment. This module enables just-in-time compilation of CUDA kernels from source code strings, allowing for dynamic code generation and optimization at runtime.

## Capabilities

### Program Creation and Management

Create and manage NVRTC compilation programs for CUDA C++ source code.

```python { .api }
def nvrtcCreateProgram(
    src: str,
    name: str,
    numHeaders: int,
    headers: List[bytes],
    includeNames: List[bytes]
) -> int:
    """
    Create an NVRTC program from CUDA C++ source code.
    
    Args:
        src (str): CUDA C++ source code
        name (str): Program name for debugging
        numHeaders (int): Number of header files
        headers (List[bytes]): Header file contents
        includeNames (List[bytes]): Header file names for #include
    
    Returns:
        int: Program handle
    
    Note:
        Headers enable inclusion of custom code and libraries
    """

def nvrtcDestroyProgram(prog: int) -> None:
    """
    Destroy an NVRTC program and free associated resources.
    
    Args:
        prog (int): Program handle to destroy
    """
```

### Program Compilation

Compile CUDA C++ source code to PTX or CUBIN with customizable compilation options.

```python { .api }
def nvrtcCompileProgram(prog: int, numOptions: int, options: List[bytes]) -> None:
    """
    Compile an NVRTC program with specified options.
    
    Args:
        prog (int): Program handle
        numOptions (int): Number of compilation options
        options (List[bytes]): Compilation option strings
    
    Raises:
        nvrtcResult: If compilation fails
    
    Note:
        Options include target architecture, optimization level, etc.
    """

def nvrtcGetProgramLogSize(prog: int) -> int:
    """
    Get the size of the compilation log.
    
    Args:
        prog (int): Program handle
    
    Returns:
        int: Log size in bytes
    """

def nvrtcGetProgramLog(prog: int, log: str) -> None:
    """
    Retrieve the compilation log messages.
    
    Args:
        prog (int): Program handle
        log (str): Buffer to receive log (must be pre-allocated)
    
    Note:
        Use nvrtcGetProgramLogSize to determine required buffer size
    """
```

### Code Generation

Extract compiled PTX and CUBIN code from successful compilation.

```python { .api }
def nvrtcGetPTXSize(prog: int) -> int:
    """
    Get the size of the compiled PTX code.
    
    Args:
        prog (int): Program handle (must be compiled successfully)
    
    Returns:
        int: PTX code size in bytes
    """

def nvrtcGetPTX(prog: int, ptx: str) -> None:
    """
    Retrieve the compiled PTX code.
    
    Args:
        prog (int): Program handle
        ptx (str): Buffer to receive PTX code (must be pre-allocated)
    
    Note:
        PTX is portable assembly for NVIDIA GPUs
    """

def nvrtcGetCUBINSize(prog: int) -> int:
    """
    Get the size of the compiled CUBIN code.
    
    Args:
        prog (int): Program handle (must be compiled successfully)
    
    Returns:
        int: CUBIN code size in bytes
    """

def nvrtcGetCUBIN(prog: int, cubin: str) -> None:
    """
    Retrieve the compiled CUBIN code.
    
    Args:
        prog (int): Program handle
        cubin (str): Buffer to receive CUBIN code (must be pre-allocated)
    
    Note:
        CUBIN is device-specific binary code
    """
```

### Low-Level Code Access

Access compiled code at various intermediate representation levels.

```python { .api }
def nvrtcGetLTOIRSize(prog: int) -> int:
    """
    Get the size of the LTO-IR (Link Time Optimization Intermediate Representation).
    
    Args:
        prog (int): Program handle
    
    Returns:
        int: LTO-IR size in bytes
    """

def nvrtcGetLTOIR(prog: int, ltoir: str) -> None:
    """
    Retrieve the LTO-IR code for link-time optimization.
    
    Args:
        prog (int): Program handle
        ltoir (str): Buffer to receive LTO-IR code
    """

def nvrtcGetOptiXIRSize(prog: int) -> int:
    """
    Get the size of OptiX IR code.
    
    Args:
        prog (int): Program handle
    
    Returns:
        int: OptiX IR size in bytes
    """

def nvrtcGetOptiXIR(prog: int, optixir: str) -> None:
    """
    Retrieve OptiX IR for ray tracing applications.
    
    Args:
        prog (int): Program handle
        optixir (str): Buffer to receive OptiX IR code
    """
```

### Version and Error Information

Query NVRTC version and get detailed error information.

```python { .api }
def nvrtcVersion() -> tuple:
    """
    Get the NVRTC version information.
    
    Returns:
        tuple[int, int]: (major_version, minor_version)
    """

def nvrtcGetErrorString(result: nvrtcResult) -> str:
    """
    Get a descriptive string for an NVRTC result code.
    
    Args:
        result (nvrtcResult): NVRTC result code
    
    Returns:
        str: Human-readable error description
    """
```

### Symbol and Name Management

Query compiled program symbols and manage name mangling.

```python { .api }
def nvrtcGetLoweredName(prog: int, name_expression: str, lowered_name: str) -> None:
    """
    Get the lowered (mangled) name for a program symbol.
    
    Args:
        prog (int): Program handle (must be compiled)
        name_expression (str): Original symbol name
        lowered_name (str): Buffer to receive lowered name
    
    Note:
        Useful for finding mangled kernel names in compiled code
    """

def nvrtcAddNameExpression(prog: int, name_expression: str) -> None:
    """
    Add a name expression to be tracked during compilation.
    
    Args:
        prog (int): Program handle (before compilation)
        name_expression (str): Symbol name to track
    
    Note:
        Must be called before compilation to track symbol names
    """
```

## Types

### Result Codes

```python { .api }
class nvrtcResult:
    """NVRTC compilation result codes"""
    NVRTC_SUCCESS: int  # Compilation succeeded
    NVRTC_ERROR_OUT_OF_MEMORY: int  # Out of memory
    NVRTC_ERROR_PROGRAM_CREATION_FAILURE: int  # Program creation failed
    NVRTC_ERROR_INVALID_INPUT: int  # Invalid input parameter
    NVRTC_ERROR_INVALID_PROGRAM: int  # Invalid program handle
    NVRTC_ERROR_INVALID_OPTION: int  # Invalid compilation option
    NVRTC_ERROR_COMPILATION: int  # Compilation failed
    NVRTC_ERROR_BUILTIN_OPERATION_FAILURE: int  # Built-in operation failed
    NVRTC_ERROR_NO_NAME_EXPRESSIONS_AFTER_COMPILATION: int  # Name expressions accessed after compilation
    NVRTC_ERROR_NO_LOWERED_NAMES_BEFORE_COMPILATION: int  # Lowered names accessed before compilation
    NVRTC_ERROR_NAME_EXPRESSION_NOT_VALID: int  # Invalid name expression
    NVRTC_ERROR_INTERNAL_ERROR: int  # Internal compiler error
```

## Usage Examples

### Basic Kernel Compilation

```python
from cuda.bindings import nvrtc

# CUDA kernel source code
kernel_source = '''
extern "C" __global__ void vector_add(float* a, float* b, float* c, int n) {
    int idx = blockIdx.x * blockDim.x + threadIdx.x;
    if (idx < n) {
        c[idx] = a[idx] + b[idx];
    }
}
'''

# Create program
program = nvrtc.nvrtcCreateProgram(
    kernel_source,
    "vector_add.cu",  # program name
    0,  # no headers
    [],  # empty headers list
    []   # empty include names list
)

# Compilation options
options = [
    b"--gpu-architecture=compute_70",
    b"--use_fast_math",
    b"-O3"
]

try:
    # Compile program
    nvrtc.nvrtcCompileProgram(program, len(options), options)
    
    # Get PTX code
    ptx_size = nvrtc.nvrtcGetPTXSize(program)
    ptx_code = ' ' * ptx_size
    nvrtc.nvrtcGetPTX(program, ptx_code)
    
    print("Compilation successful!")
    print(f"PTX size: {ptx_size} bytes")
    
except Exception as e:
    # Get compilation log on error
    log_size = nvrtc.nvrtcGetProgramLogSize(program)
    if log_size > 0:
        log = ' ' * log_size
        nvrtc.nvrtcGetProgramLog(program, log)
        print(f"Compilation error: {log}")

finally:
    # Cleanup
    nvrtc.nvrtcDestroyProgram(program)
```

### Template Kernel with Headers

```python
from cuda.bindings import nvrtc

# Header with template definition
template_header = b'''
template<typename T>
__device__ T atomic_add_wrapper(T* address, T val) {
    return atomicAdd(address, val);
}
'''

# Kernel source using template
kernel_source = '''
#include "atomic_ops.cuh"

extern "C" __global__ void atomic_sum(float* data, float* result, int n) {
    int idx = blockIdx.x * blockDim.x + threadIdx.x;
    if (idx < n) {
        atomic_add_wrapper(result, data[idx]);
    }
}
'''

# Create program with header
program = nvrtc.nvrtcCreateProgram(
    kernel_source,
    "atomic_kernel.cu",
    1,  # one header
    [template_header],  # header contents
    [b"atomic_ops.cuh"]  # header names
)

# Add name expression to track kernel name
nvrtc.nvrtcAddNameExpression(program, "atomic_sum")

# Compile with specific target
options = [b"--gpu-architecture=compute_75"]
nvrtc.nvrtcCompileProgram(program, len(options), options)

# Get lowered kernel name
lowered_name = ' ' * 256
nvrtc.nvrtcGetLoweredName(program, "atomic_sum", lowered_name)
print(f"Kernel name: {lowered_name.strip()}")

# Get both PTX and CUBIN
ptx_size = nvrtc.nvrtcGetPTXSize(program)
ptx_code = ' ' * ptx_size
nvrtc.nvrtcGetPTX(program, ptx_code)

cubin_size = nvrtc.nvrtcGetCUBINSize(program)
cubin_code = ' ' * cubin_size
nvrtc.nvrtcGetCUBIN(program, cubin_code)

print(f"Generated PTX: {ptx_size} bytes")
print(f"Generated CUBIN: {cubin_size} bytes")

nvrtc.nvrtcDestroyProgram(program)
```

### Dynamic Kernel Generation

```python
from cuda.bindings import nvrtc

def compile_parametric_kernel(block_size, data_type):
    """Generate and compile a kernel with runtime parameters."""
    
    # Generate kernel source with parameters
    kernel_template = f'''
    extern "C" __global__ void process_data_{data_type}(
        {data_type}* input, 
        {data_type}* output, 
        int n
    ) {{
        const int BLOCK_SIZE = {block_size};
        __shared__ {data_type} shared_data[BLOCK_SIZE];
        
        int idx = blockIdx.x * blockDim.x + threadIdx.x;
        int tid = threadIdx.x;
        
        // Load to shared memory
        if (idx < n) {{
            shared_data[tid] = input[idx];
        }} else {{
            shared_data[tid] = 0;
        }}
        
        __syncthreads();
        
        // Process in shared memory
        if (tid < BLOCK_SIZE / 2) {{
            shared_data[tid] += shared_data[tid + BLOCK_SIZE / 2];
        }}
        
        __syncthreads();
        
        // Write result
        if (idx < n && tid == 0) {{
            output[blockIdx.x] = shared_data[0];
        }}
    }}
    '''
    
    program = nvrtc.nvrtcCreateProgram(
        kernel_template,
        f"kernel_{data_type}_{block_size}.cu",
        0, [], []
    )
    
    options = [
        b"--gpu-architecture=compute_70",
        b"--maxrregcount=32"
    ]
    
    nvrtc.nvrtcCompileProgram(program, len(options), options)
    
    # Extract PTX
    ptx_size = nvrtc.nvrtcGetPTXSize(program)
    ptx_code = ' ' * ptx_size
    nvrtc.nvrtcGetPTX(program, ptx_code)
    
    nvrtc.nvrtcDestroyProgram(program)
    
    return ptx_code

# Generate different kernel variants
float_kernel_256 = compile_parametric_kernel(256, "float")
int_kernel_512 = compile_parametric_kernel(512, "int")
double_kernel_128 = compile_parametric_kernel(128, "double")

print("Generated three kernel variants dynamically")
```

### Error Handling and Debugging

```python
from cuda.bindings import nvrtc

# Intentionally broken kernel for error demonstration
broken_kernel = '''
extern "C" __global__ void broken_kernel(float* data) {
    int idx = blockIdx.x * blockDim.x + threadIdx.x;
    // Syntax error: missing semicolon
    data[idx] = idx * 2.0f  // Missing semicolon
    
    // Type error: undefined variable
    undeclared_variable = 42;
}
'''

program = nvrtc.nvrtcCreateProgram(broken_kernel, "broken.cu", 0, [], [])

try:
    nvrtc.nvrtcCompileProgram(program, 0, [])
    print("Unexpected: compilation succeeded")
    
except Exception as e:
    print(f"Compilation failed: {e}")
    
    # Get detailed error log
    log_size = nvrtc.nvrtcGetProgramLogSize(program)
    if log_size > 1:  # Size includes null terminator
        error_log = ' ' * log_size
        nvrtc.nvrtcGetProgramLog(program, error_log)
        
        print("Compilation errors:")
        print(error_log.strip())
    
    # Get NVRTC version for debugging
    major, minor = nvrtc.nvrtcVersion()
    print(f"NVRTC Version: {major}.{minor}")

finally:
    nvrtc.nvrtcDestroyProgram(program)
```