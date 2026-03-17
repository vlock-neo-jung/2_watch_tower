# JIT Compilation and Linking

NVVM LLVM-based compilation and NVJitLink just-in-time linking for advanced code generation workflows. This module provides access to NVIDIA's LLVM-based compiler infrastructure for compiling LLVM IR to PTX and advanced JIT linking capabilities for combining multiple device code modules.

## Capabilities

### NVVM LLVM-Based Compilation

Compile LLVM IR to PTX using NVIDIA's LLVM-based compiler backend.

```python { .api }
def create_program() -> int:
    """
    Create a new NVVM compilation program.
    
    Returns:
        int: Program handle
    
    Note:
        Program manages compilation of LLVM IR modules to PTX
    """

def destroy_program(prog: int) -> None:
    """
    Destroy an NVVM program and free associated resources.
    
    Args:
        prog (int): Program handle to destroy
    """

def add_module_to_program(prog: int, buffer: bytes, size: int, name: str) -> None:
    """
    Add an LLVM IR module to the compilation program.
    
    Args:
        prog (int): Program handle
        buffer (bytes): LLVM IR module data
        size (int): Size of IR data in bytes
        name (str): Module name for debugging
    
    Note:
        Multiple modules can be added to a single program
    """

def compile_program(prog: int, num_options: int, options) -> None:
    """
    Compile all modules in the program to PTX.
    
    Args:
        prog (int): Program handle with added modules
        num_options (int): Number of compilation options
        options: Compilation option array
    
    Raises:
        nvvmError: If compilation fails
    """

def get_compiled_result_size(prog: int) -> int:
    """
    Get the size of the compiled PTX result.
    
    Args:
        prog (int): Compiled program handle
    
    Returns:
        int: PTX size in bytes
    """

def get_compiled_result(prog: int, buffer: str) -> None:
    """
    Retrieve the compiled PTX code.
    
    Args:
        prog (int): Compiled program handle
        buffer (str): Pre-allocated buffer for PTX (use get_compiled_result_size)
    """
```

### NVVM Version and IR Information

Query NVVM compiler version and supported IR formats.

```python { .api }
def version() -> tuple:
    """
    Get the NVVM compiler version.
    
    Returns:
        tuple[int, int]: (major_version, minor_version)
    """

def ir_version() -> tuple:
    """
    Get the supported LLVM IR version.
    
    Returns:
        tuple[int, int]: (major_version, minor_version)
    
    Note:
        Indicates which LLVM IR versions are supported
    """
```

### NVJitLink Just-In-Time Linking

Link multiple device code modules into a single executable using NVJitLink.

```python { .api }
def create(num_options: int, options) -> int:
    """
    Create a new NVJitLink linker handle.
    
    Args:
        num_options (int): Number of linker options
        options: Linker option array
    
    Returns:
        int: Linker handle
    
    Note:
        Linker combines multiple device code modules
    """

def destroy(handle: int) -> None:
    """
    Destroy an NVJitLink linker handle.
    
    Args:
        handle (int): Linker handle to destroy
    """

def add_data(
    handle: int,
    input_type: int,
    data: bytes,
    size: int,
    name: str
) -> None:
    """
    Add input data to the linker.
    
    Args:
        handle (int): Linker handle
        input_type (int): Type of input data (PTX, CUBIN, FATBIN, etc.)
        data (bytes): Input data
        size (int): Data size in bytes
        name (str): Input name for debugging
    """

def add_file(handle: int, input_type: int, file_name: str) -> None:
    """
    Add input file to the linker.
    
    Args:
        handle (int): Linker handle
        input_type (int): Type of input file
        file_name (str): Path to input file
    """

def complete(handle: int) -> None:
    """
    Complete the linking process.
    
    Args:
        handle (int): Linker handle with added inputs
    
    Raises:
        nvJitLinkError: If linking fails
    
    Note:
        Must be called after adding all inputs
    """
```

### Linked Code Retrieval

Extract the linked device code in various formats.

```python { .api }
def get_linked_cubin_size(handle: int) -> int:
    """
    Get the size of the linked CUBIN code.
    
    Args:
        handle (int): Completed linker handle
    
    Returns:
        int: CUBIN size in bytes
    """

def get_linked_cubin(handle: int, cubin: bytes) -> None:
    """
    Retrieve the linked CUBIN code.
    
    Args:
        handle (int): Completed linker handle
        cubin (bytes): Pre-allocated buffer for CUBIN
    """

def get_linked_ptx_size(handle: int) -> int:
    """
    Get the size of the linked PTX code.
    
    Args:
        handle (int): Completed linker handle
    
    Returns:
        int: PTX size in bytes
    """

def get_linked_ptx(handle: int, ptx: bytes) -> None:
    """
    Retrieve the linked PTX code.
    
    Args:
        handle (int): Completed linker handle
        ptx (bytes): Pre-allocated buffer for PTX
    """
```

### Link Information and Debugging

Access linking information and error details.

```python { .api }
def get_error_log_size(handle: int) -> int:
    """
    Get the size of the linker error log.
    
    Args:
        handle (int): Linker handle
    
    Returns:
        int: Error log size in bytes
    """

def get_error_log(handle: int, log: str) -> None:
    """
    Retrieve the linker error log.
    
    Args:
        handle (int): Linker handle
        log (str): Pre-allocated buffer for error log
    """

def get_info_log_size(handle: int) -> int:
    """
    Get the size of the linker information log.
    
    Args:
        handle (int): Linker handle
    
    Returns:
        int: Info log size in bytes
    """

def get_info_log(handle: int, log: str) -> None:
    """
    Retrieve the linker information log.
    
    Args:
        handle (int): Linker handle
        log (str): Pre-allocated buffer for info log
    """

def version() -> tuple:
    """
    Get the NVJitLink version.
    
    Returns:
        tuple[int, int]: (major_version, minor_version)
    """
```

## Types

### NVVM Result Codes

```python { .api }
class Result:
    """NVVM compilation result codes"""
    NVVM_SUCCESS: int  # Compilation succeeded
    NVVM_ERROR_OUT_OF_MEMORY: int  # Out of memory
    NVVM_ERROR_PROGRAM_CREATION_FAILURE: int  # Program creation failed
    NVVM_ERROR_IR_VERSION_MISMATCH: int  # IR version not supported
    NVVM_ERROR_INVALID_INPUT: int  # Invalid input data
    NVVM_ERROR_INVALID_PROGRAM: int  # Invalid program handle
    NVVM_ERROR_INVALID_IR: int  # Invalid LLVM IR
    NVVM_ERROR_INVALID_OPTION: int  # Invalid compilation option
    NVVM_ERROR_COMPILATION: int  # Compilation failed
```

### NVJitLink Result Codes

```python { .api }
class Result:
    """NVJitLink operation result codes"""
    NVJITLINK_SUCCESS: int  # Operation succeeded
    NVJITLINK_ERROR_UNRECOGNIZED_OPTION: int  # Unrecognized linker option
    NVJITLINK_ERROR_MISSING_ARCH: int  # Missing target architecture
    NVJITLINK_ERROR_INVALID_INPUT: int  # Invalid input data
    NVJITLINK_ERROR_PTX_COMPILE: int  # PTX compilation error
    NVJITLINK_ERROR_NVVM_COMPILE: int  # NVVM compilation error
    NVJITLINK_ERROR_INTERNAL: int  # Internal linker error
```

### Input Types

```python { .api }
class InputType:
    """NVJitLink input data type enumeration"""
    NVJITLINK_INPUT_NONE: int  # No input
    NVJITLINK_INPUT_CUBIN: int  # CUBIN binary
    NVJITLINK_INPUT_PTX: int  # PTX assembly
    NVJITLINK_INPUT_FATBIN: int  # Fat binary (multi-architecture)
    NVJITLINK_INPUT_OBJECT: int  # Object file
    NVJITLINK_INPUT_LIBRARY: int  # Static library
    NVJITLINK_INPUT_NVVM_IR: int  # NVVM LLVM IR
    NVJITLINK_INPUT_NVVM_BITCODE: int  # NVVM bitcode
```

### Exception Classes

```python { .api }
class nvvmError(Exception):
    """NVVM compilation exception"""
    def __init__(self, result: Result, message: str): ...

class nvJitLinkError(Exception):
    """NVJitLink operation exception"""
    def __init__(self, result: Result, message: str): ...
```

## Usage Examples

### NVVM LLVM IR Compilation

```python
from cuda.bindings import nvvm

# Sample LLVM IR for a simple kernel
llvm_ir = b'''
target datalayout = "e-p:64:64:64-i1:8:8-i8:8:8-i16:16:16-i32:32:32-i64:64:64-f32:32:32-f64:64:64-v16:16:16-v32:32:32-v64:64:64-v128:128:128-n16:32:64"
target triple = "nvptx64-nvidia-cuda"

define void @simple_kernel(float* %input, float* %output, i32 %n) {
entry:
  %tid = call i32 @llvm.nvvm.read.ptx.sreg.tid.x()
  %bid = call i32 @llvm.nvvm.read.ptx.sreg.ctaid.x()
  %bdim = call i32 @llvm.nvvm.read.ptx.sreg.ntid.x()
  
  %tmp1 = mul i32 %bid, %bdim
  %idx = add i32 %tmp1, %tid
  
  %cond = icmp slt i32 %idx, %n
  br i1 %cond, label %if.then, label %if.end

if.then:
  %input_ptr = getelementptr float, float* %input, i32 %idx
  %val = load float, float* %input_ptr
  %result = fmul float %val, 2.0
  %output_ptr = getelementptr float, float* %output, i32 %idx
  store float %result, float* %output_ptr
  br label %if.end

if.end:
  ret void
}

declare i32 @llvm.nvvm.read.ptx.sreg.tid.x() nounwind readnone
declare i32 @llvm.nvvm.read.ptx.sreg.ctaid.x() nounwind readnone
declare i32 @llvm.nvvm.read.ptx.sreg.ntid.x() nounwind readnone
'''

try:
    # Create NVVM program
    program = nvvm.create_program()
    
    # Add LLVM IR module
    nvvm.add_module_to_program(program, llvm_ir, len(llvm_ir), "simple_kernel.ll")
    
    # Compilation options
    options = ["-arch=compute_70", "-opt=3"]
    
    # Compile to PTX
    nvvm.compile_program(program, len(options), options)
    
    # Get compiled PTX
    ptx_size = nvvm.get_compiled_result_size(program)
    ptx_buffer = ' ' * ptx_size
    nvvm.get_compiled_result(program, ptx_buffer)
    
    print(f"Compiled {len(llvm_ir)} bytes of LLVM IR to {ptx_size} bytes of PTX")
    print("First 200 characters of PTX:")
    print(ptx_buffer[:200])

except nvvm.nvvmError as e:
    print(f"NVVM compilation failed: {e}")

finally:
    nvvm.destroy_program(program)
    
# Check NVVM version
major, minor = nvvm.version()
ir_major, ir_minor = nvvm.ir_version()
print(f"NVVM Version: {major}.{minor}")
print(f"Supported IR Version: {ir_major}.{ir_minor}")
```

### NVJitLink Module Linking

```python
from cuda.bindings import nvjitlink

# Sample PTX modules (simplified)
module1_ptx = b'''
.version 7.0
.target sm_70
.address_size 64

.visible .entry kernel_part1(.param .u64 kernel_part1_param_0) {
    .reg .u64 %rd<2>;
    ld.param.u64 %rd1, [kernel_part1_param_0];
    // Kernel implementation...
    ret;
}
'''

module2_ptx = b'''
.version 7.0  
.target sm_70
.address_size 64

.visible .entry kernel_part2(.param .u64 kernel_part2_param_0) {
    .reg .u64 %rd<2>;
    ld.param.u64 %rd1, [kernel_part2_param_0];
    // Kernel implementation...
    ret;
}
'''

try:
    # Create linker with options
    linker_options = ["-arch=sm_70", "-optimize"]
    linker = nvjitlink.create(len(linker_options), linker_options)
    
    # Add PTX modules
    nvjitlink.add_data(
        linker,
        nvjitlink.InputType.NVJITLINK_INPUT_PTX,
        module1_ptx,
        len(module1_ptx),
        "module1.ptx"
    )
    
    nvjitlink.add_data(
        linker,
        nvjitlink.InputType.NVJITLINK_INPUT_PTX,
        module2_ptx,
        len(module2_ptx),
        "module2.ptx"
    )
    
    # Complete linking
    nvjitlink.complete(linker)
    
    # Get linked CUBIN
    cubin_size = nvjitlink.get_linked_cubin_size(linker)
    cubin_data = bytearray(cubin_size)
    nvjitlink.get_linked_cubin(linker, cubin_data)
    
    print(f"Linked {len(module1_ptx) + len(module2_ptx)} bytes of PTX")
    print(f"Generated {cubin_size} bytes of CUBIN")
    
    # Get info log
    info_size = nvjitlink.get_info_log_size(linker)
    if info_size > 0:
        info_log = ' ' * info_size
        nvjitlink.get_info_log(linker, info_log)
        print("Linker info:", info_log.strip())

except nvjitlink.nvJitLinkError as e:
    print(f"JIT linking failed: {e}")
    
    # Get error log
    error_size = nvjitlink.get_error_log_size(linker)
    if error_size > 0:
        error_log = ' ' * error_size
        nvjitlink.get_error_log(linker, error_log)
        print("Linker errors:", error_log.strip())

finally:
    nvjitlink.destroy(linker)

# Check NVJitLink version
major, minor = nvjitlink.version()
print(f"NVJitLink Version: {major}.{minor}")
```

### Advanced Multi-Module Linking

```python
from cuda.bindings import nvjitlink
import os

def link_cuda_modules(ptx_files, cubin_files, output_name):
    """Link multiple CUDA modules from files."""
    
    linker_options = [
        "-arch=sm_75",
        "-optimize",
        f"-o={output_name}"
    ]
    
    linker = nvjitlink.create(len(linker_options), linker_options)
    
    try:
        # Add PTX files
        for ptx_file in ptx_files:
            nvjitlink.add_file(
                linker,
                nvjitlink.InputType.NVJITLINK_INPUT_PTX,
                ptx_file
            )
        
        # Add CUBIN files
        for cubin_file in cubin_files:
            nvjitlink.add_file(
                linker,
                nvjitlink.InputType.NVJITLINK_INPUT_CUBIN,
                cubin_file
            )
        
        # Complete linking
        nvjitlink.complete(linker)
        
        # Extract results
        results = {}
        
        # Get CUBIN
        cubin_size = nvjitlink.get_linked_cubin_size(linker)
        if cubin_size > 0:
            cubin_data = bytearray(cubin_size)
            nvjitlink.get_linked_cubin(linker, cubin_data)
            results['cubin'] = cubin_data
        
        # Get PTX  
        try:
            ptx_size = nvjitlink.get_linked_ptx_size(linker)
            if ptx_size > 0:
                ptx_data = bytearray(ptx_size)
                nvjitlink.get_linked_ptx(linker, ptx_data)
                results['ptx'] = ptx_data
        except:
            # PTX not available for this link
            pass
        
        return results
        
    finally:
        nvjitlink.destroy(linker)

# Example usage
if __name__ == "__main__":
    # Link example modules
    ptx_modules = ["kernel1.ptx", "kernel2.ptx"]
    cubin_modules = ["library.cubin"]
    
    # Note: This assumes the files exist
    try:
        linked_code = link_cuda_modules(ptx_modules, cubin_modules, "combined")
        
        if 'cubin' in linked_code:
            print(f"Generated CUBIN: {len(linked_code['cubin'])} bytes")
            
        if 'ptx' in linked_code:
            print(f"Generated PTX: {len(linked_code['ptx'])} bytes")
            
    except FileNotFoundError as e:
        print(f"Input file not found: {e}")
    except nvjitlink.nvJitLinkError as e:
        print(f"Linking failed: {e}")
```

### NVVM and NVJitLink Pipeline

```python
from cuda.bindings import nvvm, nvjitlink

def llvm_to_cubin_pipeline(llvm_modules, target_arch="sm_70"):
    """Complete pipeline from LLVM IR to CUBIN via NVVM and NVJitLink."""
    
    ptx_modules = []
    
    # Step 1: Compile LLVM IR to PTX using NVVM
    for i, llvm_ir in enumerate(llvm_modules):
        program = nvvm.create_program()
        
        try:
            nvvm.add_module_to_program(
                program, llvm_ir, len(llvm_ir), f"module_{i}.ll"
            )
            
            options = [f"-arch=compute_{target_arch[2:]}", "-opt=3"]
            nvvm.compile_program(program, len(options), options)
            
            ptx_size = nvvm.get_compiled_result_size(program)
            ptx_buffer = bytearray(ptx_size)
            nvvm.get_compiled_result(program, ptx_buffer)
            
            ptx_modules.append(bytes(ptx_buffer))
            
        finally:
            nvvm.destroy_program(program)
    
    # Step 2: Link PTX modules to CUBIN using NVJitLink
    linker_options = [f"-arch={target_arch}"]
    linker = nvjitlink.create(len(linker_options), linker_options)
    
    try:
        for i, ptx_data in enumerate(ptx_modules):
            nvjitlink.add_data(
                linker,
                nvjitlink.InputType.NVJITLINK_INPUT_PTX,
                ptx_data,
                len(ptx_data),
                f"module_{i}.ptx"
            )
        
        nvjitlink.complete(linker)
        
        cubin_size = nvjitlink.get_linked_cubin_size(linker)
        cubin_data = bytearray(cubin_size)
        nvjitlink.get_linked_cubin(linker, cubin_data)
        
        return bytes(cubin_data)
        
    finally:
        nvjitlink.destroy(linker)

# Example usage with mock LLVM IR
sample_llvm_modules = [
    b'target triple = "nvptx64-nvidia-cuda"\ndefine void @kernel1() { ret void }',
    b'target triple = "nvptx64-nvidia-cuda"\ndefine void @kernel2() { ret void }'
]

try:
    final_cubin = llvm_to_cubin_pipeline(sample_llvm_modules, "sm_75")
    print(f"Pipeline generated {len(final_cubin)} bytes of CUBIN")
except Exception as e:
    print(f"Pipeline failed: {e}")
```