# NumPy

The fundamental package for scientific computing with Python. NumPy provides a powerful N-dimensional array object, sophisticated broadcasting functions, tools for integrating C/C++ and Fortran code, and linear algebra, Fourier transform, and random number capabilities. It serves as the foundation for the entire Python scientific computing ecosystem.

## Package Information

- **Package Name**: numpy
- **Language**: Python
- **Installation**: `pip install numpy`

## Core Imports

```python
import numpy as np
```

For specific submodules:

```python
import numpy.linalg as la
import numpy.random as rng
import numpy.fft as fft
```

## Basic Usage

```python
import numpy as np

# Create arrays
arr = np.array([1, 2, 3, 4, 5])
matrix = np.array([[1, 2], [3, 4]])

# Array creation
zeros = np.zeros((3, 4))
ones = np.ones((2, 3))
range_arr = np.arange(0, 10, 2)
linspace_arr = np.linspace(0, 1, 5)

# Mathematical operations
result = np.sqrt(arr)
sum_result = np.sum(matrix, axis=0)
mean_result = np.mean(arr)

# Array manipulation
reshaped = matrix.reshape(4, 1)
transposed = matrix.T
```

## Architecture

NumPy's architecture provides the foundation for scientific computing in Python:

- **ndarray**: Core N-dimensional array object with optimized C/Fortran implementations
- **dtype**: Flexible type system supporting numeric, string, and structured data
- **ufuncs**: Universal functions enabling vectorized operations with broadcasting
- **Submodules**: Specialized functionality organized into logical domains (linalg, random, fft, polynomial)

This design enables high-performance numerical computing while maintaining Python's ease of use, serving as the base layer for libraries like pandas, scikit-learn, matplotlib, and the entire scientific Python ecosystem.

## Capabilities

### Array Creation and Manipulation

Core functionality for creating, reshaping, joining, and manipulating N-dimensional arrays. Includes array creation functions, shape manipulation, joining/splitting operations, and element access patterns.

```python { .api }
def array(object, dtype=None, **kwargs): ...
def zeros(shape, dtype=float, **kwargs): ...
def ones(shape, dtype=None, **kwargs): ...
def empty(shape, dtype=float, **kwargs): ...
def arange(start, stop=None, step=1, dtype=None): ...
def linspace(start, stop, num=50, **kwargs): ...
def reshape(a, newshape, order='C'): ...
def concatenate(arrays, axis=0, **kwargs): ...
```

[Array Creation and Manipulation](./array-creation.md)

### Mathematical Functions

Universal functions (ufuncs) providing element-wise mathematical operations including arithmetic, trigonometric, exponential, logarithmic, and bitwise operations with automatic broadcasting.

```python { .api }
def add(x1, x2, **kwargs): ...
def multiply(x1, x2, **kwargs): ...
def sin(x, **kwargs): ...
def cos(x, **kwargs): ...
def exp(x, **kwargs): ...
def log(x, **kwargs): ...
def sqrt(x, **kwargs): ...
```

[Mathematical Functions](./mathematical-functions.md)

### Array Statistics and Aggregations

Statistical and reduction operations for analyzing array data, including basic statistics, cumulative operations, and NaN-aware versions of statistical functions.

```python { .api }
def sum(a, axis=None, **kwargs): ...
def mean(a, axis=None, **kwargs): ...
def std(a, axis=None, **kwargs): ...
def min(a, axis=None, **kwargs): ...
def max(a, axis=None, **kwargs): ...
def median(a, axis=None, **kwargs): ...
def percentile(a, q, axis=None, **kwargs): ...
```

[Array Statistics](./array-statistics.md)

### Linear Algebra Operations

Core linear algebra functionality including matrix products, decompositions, eigenvalue problems, and solving linear systems through the numpy.linalg module.

```python { .api }
def dot(a, b, out=None): ...
def matmul(x1, x2, **kwargs): ...
def linalg.inv(a): ...
def linalg.solve(a, b): ...
def linalg.eig(a): ...
def linalg.svd(a, **kwargs): ...
```

[Linear Algebra](./linear-algebra.md)

### Array Searching and Sorting

Functions for finding, sorting, and organizing array elements including search operations, sorting algorithms, and set operations for array analysis.

```python { .api }
def where(condition, x=None, y=None): ...
def sort(a, axis=-1, **kwargs): ...
def argsort(a, axis=-1, **kwargs): ...
def unique(ar, **kwargs): ...
def searchsorted(a, v, **kwargs): ...
```

[Searching and Sorting](./searching-sorting.md)

### Random Number Generation

Comprehensive random number generation capabilities through numpy.random, including various probability distributions, random sampling, and BitGenerator infrastructure.

```python { .api }
def random.random(size=None): ...
def random.randint(low, high=None, size=None): ...
def random.normal(loc=0.0, scale=1.0, size=None): ...
def random.choice(a, size=None, **kwargs): ...
def random.default_rng(seed=None): ...
```

[Random Number Generation](./random-generation.md)

### Fast Fourier Transform

Discrete Fourier Transform operations through numpy.fft for signal processing and frequency domain analysis, including 1D, 2D, and N-D transforms.

```python { .api }
def fft.fft(a, n=None, axis=-1, **kwargs): ...
def fft.ifft(a, n=None, axis=-1, **kwargs): ...
def fft.fft2(a, s=None, axes=(-2, -1), **kwargs): ...
def fft.rfft(a, n=None, axis=-1, **kwargs): ...
```

[Fast Fourier Transform](./fft.md)

### Input/Output Operations

File I/O operations for saving and loading array data in various formats, including binary and text formats with support for compressed files.

```python { .api }
def save(file, arr, **kwargs): ...
def load(file, **kwargs): ...
def loadtxt(fname, **kwargs): ...
def savetxt(fname, X, **kwargs): ...
```

[Input/Output](./input-output.md)

### Data Types and Type Operations

NumPy's flexible data type system including scalar types, structured arrays, and type conversion operations for handling diverse data formats.

```python { .api }
class dtype: ...
def astype(dtype, **kwargs): ...
def can_cast(from_, to, casting='safe'): ...
class finfo: ...
class iinfo: ...
```

[Data Types](./data-types.md)

### Polynomial Operations

Polynomial classes and functions for working with polynomials of different mathematical bases including power series, Chebyshev, Legendre, Laguerre, and Hermite polynomials.

```python { .api }
class Polynomial: ...
class Chebyshev: ...
class Legendre: ...
def poly(seq_of_zeros): ...
def polyval(p, x): ...
def polyfit(x, y, deg): ...
```

[Polynomial Operations](./polynomial.md)

### Masked Array Operations

Array operations that handle missing or invalid data through masking, providing robust statistical computations on incomplete datasets.

```python { .api }
class MaskedArray: ...
def masked_array(data, mask=False, **kwargs): ...
def masked_where(condition, a): ...
def masked_invalid(a): ...
```

[Masked Arrays](./masked-arrays.md)

## Constants and Configuration

```python { .api }
# Mathematical constants
pi = 3.141592653589793
e = 2.718281828459045
euler_gamma = 0.5772156649015329
inf = float('inf')
nan = float('nan')
NINF = float('-inf')
PINF = float('inf')
NZERO = -0.0
PZERO = 0.0
newaxis = None

# Version information
__version__: str  # NumPy version string
__array_api_version__: str  # Array API standard version

# Configuration
def show_config():
    """Display NumPy build configuration information."""
```

## Types

```python { .api }
class ndarray:
    """N-dimensional array object."""
    def __init__(self, shape, dtype=float, **kwargs): ...
    def reshape(self, newshape, order='C'): ...
    def astype(self, dtype, **kwargs): ...
    def sum(self, axis=None, **kwargs): ...
    def mean(self, axis=None, **kwargs): ...
    def transpose(self, axes=None): ...
    @property
    def shape: tuple
    @property
    def dtype: dtype
    @property
    def size: int
    @property
    def ndim: int
    @property
    def T: ndarray

class dtype:
    """Data type object describing array element type."""
    def __init__(self, obj, **kwargs): ...
    @property
    def name: str
    @property
    def kind: str
    @property
    def itemsize: int

class ufunc:
    """Universal function object."""
    def __call__(self, *args, **kwargs): ...
    def reduce(self, a, axis=0, **kwargs): ...
    def accumulate(self, a, axis=0, **kwargs): ...

# Scalar types
class generic: ...  # Base class for all scalar types
class number(generic): ...  # Base class for all number types
class integer(number): ...  # Base class for all integer types
class signedinteger(integer): ...  # Base class for signed integers
class unsignedinteger(integer): ...  # Base class for unsigned integers
class inexact(number): ...  # Base class for inexact types
class floating(inexact): ...  # Base class for floating types
class complexfloating(inexact): ...  # Base class for complex types
class flexible(generic): ...  # Base class for flexible types
class character(flexible): ...  # Base class for character types

# Integer scalar types
class int8(signedinteger): ...
class int16(signedinteger): ...  
class int32(signedinteger): ...
class int64(signedinteger): ...
class uint8(unsignedinteger): ...
class uint16(unsignedinteger): ...
class uint32(unsignedinteger): ...
class uint64(unsignedinteger): ...

# Platform-dependent integer types
class int_(signedinteger): ...  # Platform integer (usually int64)
class intc(signedinteger): ...  # C int type
class intp(signedinteger): ...  # Pointer-sized integer
class uint(unsignedinteger): ...  # Platform unsigned integer
class uintc(unsignedinteger): ...  # C unsigned int
class uintp(unsignedinteger): ...  # Pointer-sized unsigned integer

# Floating point types
class float16(floating): ...  # Half precision
class float32(floating): ...  # Single precision
class float64(floating): ...  # Double precision
class longdouble(floating): ...  # Extended precision

# Complex types
class complex64(complexfloating): ...  # Single precision complex
class complex128(complexfloating): ...  # Double precision complex
class clongdouble(complexfloating): ...  # Extended precision complex

# Other types
class bool_(generic): ...  # Boolean type
class bytes_(character): ...  # Bytes type
class str_(character): ...  # Unicode string type
class void(flexible): ...  # Void type for structured arrays
class object_(generic): ...  # Python object type

# Date/time types
class datetime64(generic): ...  # Date and time
class timedelta64(generic): ...  # Time differences
```