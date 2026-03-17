# Library Management

Dynamic NVIDIA library loading and discovery utilities for runtime library management and version compatibility. This module provides utilities for discovering, loading, and managing NVIDIA CUDA libraries dynamically at runtime, enabling flexible deployment and version management.

## Capabilities

### Dynamic Library Loading

Load NVIDIA libraries dynamically with automatic discovery and caching.

```python { .api }
def load_nvidia_dynamic_lib(libname: str) -> LoadedDL:
    """
    Load an NVIDIA dynamic library by name with automatic discovery.
    
    Args:
        libname (str): Library name (e.g., "cudart", "cublas", "cufft")
    
    Returns:
        LoadedDL: Information about the loaded library
    
    Raises:
        DynamicLibNotFoundError: If library cannot be found or loaded
    
    Note:
        Results are cached for subsequent calls with the same library name
    """
```

### Library Discovery

Discover and locate NVIDIA libraries in the system.

```python { .api }
def find_nvidia_lib_path(libname: str) -> str:
    """
    Find the full path to an NVIDIA library.
    
    Args:
        libname (str): Library name to locate
    
    Returns:
        str: Absolute path to the library file
    
    Raises:
        DynamicLibNotFoundError: If library cannot be found
    """

def get_nvidia_lib_directories() -> list:
    """
    Get list of directories searched for NVIDIA libraries.
    
    Returns:
        list[str]: List of search directory paths
    
    Note:
        Includes system library paths, CUDA toolkit paths, and environment-specific paths
    """
```

### Library Information

Query information about loaded libraries and supported library types.

```python { .api }
def get_supported_libraries() -> tuple:
    """
    Get tuple of all supported NVIDIA library names.
    
    Returns:
        tuple[str]: Supported library names
    
    Note:
        Includes core CUDA libraries, math libraries, and specialized libraries
    """

def is_library_available(libname: str) -> bool:
    """
    Check if a specific NVIDIA library is available on the system.
    
    Args:
        libname (str): Library name to check
    
    Returns:
        bool: True if library is available, False otherwise
    """

def get_library_version(libname: str) -> str:
    """
    Get the version of a loaded NVIDIA library.
    
    Args:
        libname (str): Library name
    
    Returns:
        str: Library version string
    
    Raises:
        DynamicLibNotFoundError: If library is not loaded or available
    """
```

### CUDA Bindings Utilities

Utility functions for working with CUDA objects and version information.

```python { .api }
def get_cuda_native_handle(obj) -> int:
    """
    Get the native CUDA handle from a Python CUDA object.
    
    Args:
        obj: Python CUDA object (stream, event, etc.)
    
    Returns:
        int: Native CUDA handle as integer
    
    Note:
        Enables interoperability between different CUDA Python libraries
    """

def get_ptx_ver(ptx: str) -> str:
    """
    Extract PTX ISA version from PTX source code.
    
    Args:
        ptx (str): PTX source code string
    
    Returns:
        str: PTX ISA version string
    
    Note:
        Useful for determining PTX compatibility requirements
    """

def get_minimal_required_cuda_ver_from_ptx_ver(ptx_version: str) -> int:
    """
    Map PTX ISA version to minimum required CUDA driver version.
    
    Args:
        ptx_version (str): PTX ISA version string
    
    Returns:
        int: Minimum CUDA driver version required
    
    Note:
        Helps determine driver compatibility for PTX code
    """
```

### Platform Compatibility

Handle platform-specific library loading and compatibility checks.

```python { .api }
def get_platform_lib_extension() -> str:
    """
    Get the platform-specific library file extension.
    
    Returns:
        str: Library extension (".so" on Linux, ".dll" on Windows, ".dylib" on macOS)
    """

def get_platform_lib_prefix() -> str:
    """
    Get the platform-specific library name prefix.
    
    Returns:
        str: Library prefix ("lib" on Unix-like systems, "" on Windows)
    """

def resolve_library_name(libname: str) -> str:
    """
    Resolve a library name to the platform-specific filename.
    
    Args:
        libname (str): Base library name
    
    Returns:
        str: Platform-specific library filename
    
    Example:
        "cudart" -> "libcudart.so" (Linux), "cudart64_12.dll" (Windows)
    """
```

## Types

### Loaded Library Information

```python { .api }
class LoadedDL:
    """Information about a loaded dynamic library"""
    
    abs_path: Optional[str]
    """
    Absolute path to the loaded library file.
    None if library was loaded from memory or path unavailable.
    """
    
    was_already_loaded_from_elsewhere: bool
    """
    True if library was already loaded by another component.
    False if this call loaded the library for the first time.
    """
    
    _handle_uint: int
    """
    Platform-agnostic library handle as integer pointer.
    Used internally for library management operations.
    """
```

### Exception Classes

```python { .api }
class DynamicLibNotFoundError(Exception):
    """
    Exception raised when an NVIDIA library cannot be found or loaded.
    
    This exception is raised when:
    - Library file doesn't exist in search paths
    - Library file exists but cannot be loaded (missing dependencies, wrong architecture)
    - Library name is not in the supported libraries list
    """
    
    def __init__(self, libname: str, message: str): ...
```

### Supported Library Names

```python { .api }
SUPPORTED_NVIDIA_LIBNAMES: tuple = (
    # Core CUDA Libraries
    "cudart",      # CUDA Runtime
    "nvfatbin",    # Fat Binary utilities
    "nvJitLink",   # JIT Linking
    "nvrtc",       # Runtime Compilation
    "nvvm",        # NVVM Compiler
    
    # Math Libraries
    "cublas",      # Basic Linear Algebra Subprograms
    "cublasLt",    # BLAS-like Linear Algebra
    "cufft",       # Fast Fourier Transform
    "cufftw",      # FFTW-compatible interface
    "curand",      # Random Number Generation
    "cusolver",    # Dense and Sparse Linear Algebra
    "cusolverMg",  # Multi-GPU Linear Algebra  
    "cusparse",    # Sparse Matrix Operations
    
    # NVIDIA Performance Primitives (NPP)
    "nppc",        # NPP Core
    "nppial",      # NPP Image Arithmetic and Logic
    "nppicc",      # NPP Image Color Conversion
    "nppidei",     # NPP Image Data Exchange and Initialization
    "nppif",       # NPP Image Filtering
    "nppig",       # NPP Image Geometry
    "nppim",       # NPP Image Morphological
    "nppist",      # NPP Image Statistics
    "nppisu",      # NPP Image Support
    "nppitc",      # NPP Image Threshold and Compare
    "npps",        # NPP Signal Processing
    
    # Specialized Libraries
    "nvblas",      # Drop-in BLAS replacement
    "nvjpeg",      # JPEG encode/decode
    "cufile"       # GPU Direct Storage (Linux only)
)
```

### Version Information

```python { .api }
__version__: str  # cuda.pathfinder version string "1.1.1a0"
```

## Usage Examples

### Basic Library Loading

```python
from cuda.pathfinder import load_nvidia_dynamic_lib, DynamicLibNotFoundError

try:
    # Load CUDA Runtime library
    cudart_lib = load_nvidia_dynamic_lib("cudart")
    
    print(f"CUDA Runtime loaded from: {cudart_lib.abs_path}")
    print(f"Library handle: {cudart_lib._handle_uint}")
    print(f"Was already loaded: {cudart_lib.was_already_loaded_from_elsewhere}")
    
    # Load cuBLAS library
    cublas_lib = load_nvidia_dynamic_lib("cublas")
    print(f"cuBLAS loaded from: {cublas_lib.abs_path}")
    
except DynamicLibNotFoundError as e:
    print(f"Failed to load library: {e}")
```

### Library Discovery and Availability

```python
from cuda.pathfinder import (
    get_supported_libraries, 
    is_library_available,
    find_nvidia_lib_path,
    DynamicLibNotFoundError
)

# Check all supported libraries
supported_libs = get_supported_libraries()
print(f"Supported libraries: {len(supported_libs)}")

available_libs = []
unavailable_libs = []

for libname in supported_libs:
    if is_library_available(libname):
        available_libs.append(libname)
        try:
            path = find_nvidia_lib_path(libname)
            print(f"✓ {libname}: {path}")
        except DynamicLibNotFoundError:
            print(f"✓ {libname}: available but path not found")
    else:
        unavailable_libs.append(libname)
        print(f"✗ {libname}: not available")

print(f"\nSummary:")
print(f"  Available: {len(available_libs)}/{len(supported_libs)}")
print(f"  Unavailable: {len(unavailable_libs)}")
```

### Conditional Library Loading

```python
from cuda.pathfinder import (
    load_nvidia_dynamic_lib, 
    is_library_available,
    DynamicLibNotFoundError
)

class CUDALibraryManager:
    """Manages conditional loading of CUDA libraries."""
    
    def __init__(self):
        self.loaded_libs = {}
        self.core_libs = ["cudart", "nvrtc"]
        self.math_libs = ["cublas", "cufft", "curand"]
        self.optional_libs = ["cufile", "nvjpeg"]
    
    def load_core_libraries(self):
        """Load essential CUDA libraries."""
        for libname in self.core_libs:
            try:
                lib = load_nvidia_dynamic_lib(libname)
                self.loaded_libs[libname] = lib
                print(f"Core library {libname} loaded successfully")
            except DynamicLibNotFoundError:
                print(f"ERROR: Core library {libname} not found!")
                raise
    
    def load_math_libraries(self):
        """Load mathematical computation libraries."""
        for libname in self.math_libs:
            try:
                lib = load_nvidia_dynamic_lib(libname)
                self.loaded_libs[libname] = lib
                print(f"Math library {libname} loaded successfully")
            except DynamicLibNotFoundError:
                print(f"Warning: Math library {libname} not available")
    
    def load_optional_libraries(self):
        """Load optional/specialized libraries."""
        for libname in self.optional_libs:
            if is_library_available(libname):
                try:
                    lib = load_nvidia_dynamic_lib(libname)
                    self.loaded_libs[libname] = lib
                    print(f"Optional library {libname} loaded successfully")
                except DynamicLibNotFoundError:
                    print(f"Optional library {libname} failed to load")
            else:
                print(f"Optional library {libname} not available on this system")
    
    def get_loaded_libraries(self):
        """Get list of successfully loaded libraries."""
        return list(self.loaded_libs.keys())
    
    def has_library(self, libname):
        """Check if a specific library is loaded."""
        return libname in self.loaded_libs

# Example usage
manager = CUDALibraryManager()

# Load libraries in order of importance
try:
    manager.load_core_libraries()
    manager.load_math_libraries()
    manager.load_optional_libraries()
    
    print(f"\nLoaded libraries: {manager.get_loaded_libraries()}")
    
    # Check for specific capabilities
    if manager.has_library("cufft"):
        print("FFT operations available")
    
    if manager.has_library("cufile"):
        print("GPU Direct Storage available")
    
    if manager.has_library("nvjpeg"):
        print("Hardware JPEG encoding/decoding available")

except DynamicLibNotFoundError as e:
    print(f"Critical library loading failed: {e}")
```

### Platform-Specific Library Handling

```python
from cuda.pathfinder import (
    get_platform_lib_extension,
    get_platform_lib_prefix,
    resolve_library_name,
    get_nvidia_lib_directories,
    load_nvidia_dynamic_lib
)
import platform

def show_platform_info():
    """Display platform-specific library information."""
    
    print(f"Platform: {platform.system()} {platform.architecture()[0]}")
    print(f"Library prefix: '{get_platform_lib_prefix()}'")
    print(f"Library extension: '{get_platform_lib_extension()}'")
    
    # Show how library names are resolved
    test_libs = ["cudart", "cublas", "cufft"]
    print(f"\nLibrary name resolution:")
    for libname in test_libs:
        resolved = resolve_library_name(libname)
        print(f"  {libname} -> {resolved}")
    
    # Show search directories
    search_dirs = get_nvidia_lib_directories()
    print(f"\nLibrary search directories:")
    for i, directory in enumerate(search_dirs):
        print(f"  {i+1}. {directory}")

def cross_platform_library_loader(libname):
    """Cross-platform library loading with detailed information."""
    
    print(f"Loading {libname}...")
    
    try:
        # Show resolved name
        resolved_name = resolve_library_name(libname)
        print(f"  Resolved name: {resolved_name}")
        
        # Load library
        lib = load_nvidia_dynamic_lib(libname)
        
        print(f"  ✓ Successfully loaded")
        print(f"  Path: {lib.abs_path}")
        print(f"  Handle: 0x{lib._handle_uint:x}")
        
        if lib.was_already_loaded_from_elsewhere:
            print(f"  Note: Library was already loaded by another component")
        
        return lib
        
    except Exception as e:
        print(f"  ✗ Failed to load: {e}")
        return None

# Example usage
show_platform_info()

print(f"\n" + "="*50)
print("Loading test libraries:")

test_libraries = ["cudart", "cublas", "nvrtc", "cufile"]
loaded = {}

for libname in test_libraries:
    result = cross_platform_library_loader(libname)
    if result:
        loaded[libname] = result
    print()

print(f"Successfully loaded {len(loaded)} out of {len(test_libraries)} libraries")
```

### Library Version Management

```python
from cuda.pathfinder import (
    load_nvidia_dynamic_lib,
    get_library_version,
    DynamicLibNotFoundError
)
import cuda.pathfinder

def check_library_versions():
    """Check versions of loaded NVIDIA libraries."""
    
    print(f"cuda.pathfinder version: {cuda.pathfinder.__version__}")
    print(f"\nNVIDIA Library Versions:")
    
    # Libraries that typically provide version information
    version_libs = [
        "cudart",   # CUDA Runtime
        "cublas",   # cuBLAS
        "cufft",    # cuFFT
        "nvrtc",    # NVRTC
    ]
    
    for libname in version_libs:
        try:
            # Load library
            lib = load_nvidia_dynamic_lib(libname)
            
            # Try to get version (this might not be implemented for all libraries)
            try:
                version = get_library_version(libname)
                print(f"  {libname}: {version}")
            except (NotImplementedError, AttributeError):
                print(f"  {libname}: loaded, version info not available")
                
        except DynamicLibNotFoundError:
            print(f"  {libname}: not available")

def version_compatibility_check():
    """Check version compatibility between libraries."""
    
    try:
        # Load CUDA Runtime
        cudart = load_nvidia_dynamic_lib("cudart")
        print(f"CUDA Runtime: {cudart.abs_path}")
        
        # Load NVRTC (should be compatible with runtime)
        nvrtc = load_nvidia_dynamic_lib("nvrtc")
        print(f"NVRTC: {nvrtc.abs_path}")
        
        # Check if both libraries exist in same directory (common for compatible versions)
        if cudart.abs_path and nvrtc.abs_path:
            cudart_dir = cudart.abs_path.rsplit('/', 1)[0]
            nvrtc_dir = nvrtc.abs_path.rsplit('/', 1)[0]
            
            if cudart_dir == nvrtc_dir:
                print("✓ Libraries appear to be from the same CUDA installation")
            else:
                print("⚠ Libraries from different directories - version mismatch possible")
                print(f"  CUDA Runtime directory: {cudart_dir}")
                print(f"  NVRTC directory: {nvrtc_dir}")
        
    except DynamicLibNotFoundError as e:
        print(f"Version compatibility check failed: {e}")

# Run version checks
check_library_versions()
print("\n" + "="*50)
version_compatibility_check()
```