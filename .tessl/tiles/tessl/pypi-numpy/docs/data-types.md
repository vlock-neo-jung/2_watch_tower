# Data Types and Type Operations

NumPy's flexible data type system including scalar types, structured arrays, and type conversion operations. Provides comprehensive support for handling diverse data formats and precise type control.

## Capabilities

### Core Data Type Classes

Fundamental classes for working with NumPy data types.

```python { .api }
class dtype:
    """
    Data type object describing array element format and layout.
    
    Parameters:
    - obj: data type specification (str, type, dtype, etc.)
    - align: bool, align fields to improve performance
    - copy: bool, create copy of dtype object
    
    Attributes:
    - name: str, canonical name of dtype
    - kind: str, character code for dtype category
    - char: str, unique character code for dtype
    - type: type, scalar type corresponding to dtype
    - itemsize: int, size of dtype in bytes
    - byteorder: str, byte order (endianness)
    - fields: dict or None, field information for structured dtypes
    - shape: tuple, shape for sub-array dtypes
    """
    def __init__(self, obj, align=False, copy=False): ...
    
    @property
    def name(self): """Canonical name of dtype"""
    
    @property
    def kind(self): """Character code ('i', 'f', 'U', etc.)"""
    
    @property
    def itemsize(self): """Size in bytes"""
    
    @property
    def byteorder(self): """Byte order ('=', '<', '>', '|')"""

def astype(dtype, order='K', casting='unsafe', subok=True, copy=True):
    """
    Cast array to specified type.
    
    Parameters:
    - dtype: str or dtype, target data type
    - order: {'C', 'F', 'A', 'K'}, memory layout
    - casting: {'no', 'equiv', 'safe', 'same_kind', 'unsafe'}, casting rule
    - subok: bool, return subclass if possible
    - copy: bool, force copy even if unnecessary
    
    Returns:
    ndarray: Array cast to new type
    """
```

### Type Information Classes

Classes providing detailed information about numeric types.

```python { .api }
class finfo:
    """
    Machine limits for floating point types.
    
    Parameters:
    - dtype: floating point data type
    
    Attributes:
    - eps: float, difference between 1.0 and next float
    - epsneg: float, difference between 1.0 and previous float
    - max: float, largest representable number
    - min: float, smallest representable positive number
    - tiny: float, smallest positive normalized number
    - precision: int, approximate decimal precision
    - resolution: float, approximate decimal resolution
    """
    def __init__(self, dtype): ...
    
    @property
    def eps(self): """Machine epsilon"""
    
    @property
    def max(self): """Maximum representable value"""
    
    @property
    def min(self): """Minimum representable positive value"""

class iinfo:
    """
    Machine limits for integer types.
    
    Parameters:
    - dtype: integer data type
    
    Attributes:
    - min: int, minimum representable value
    - max: int, maximum representable value
    - dtype: dtype, integer data type
    - kind: str, kind of integer ('i' or 'u')
    - bits: int, number of bits
    """
    def __init__(self, dtype): ...
    
    @property
    def min(self): """Minimum representable value"""
    
    @property
    def max(self): """Maximum representable value"""
    
    @property
    def bits(self): """Number of bits"""
```

### Type Conversion Functions

Functions for type casting and conversion operations.

```python { .api }
def can_cast(from_, to, casting='safe'):
    """
    Returns True if cast between data types can occur according to casting rule.
    
    Parameters:
    - from_: data type or array, source type
    - to: data type, target type  
    - casting: {'no', 'equiv', 'safe', 'same_kind', 'unsafe'}, casting rule
    
    Returns:
    bool: True if cast is possible
    """

def promote_types(type1, type2):
    """
    Returns the data type with the smallest size and smallest scalar kind.
    
    Parameters:
    - type1, type2: data types to promote
    
    Returns:
    dtype: Promoted data type
    """

def result_type(*arrays_and_dtypes):
    """
    Returns the type that results from applying NumPy type promotion rules.
    
    Parameters:
    - *arrays_and_dtypes: arrays and data types
    
    Returns:
    dtype: Result data type
    """

def min_scalar_type(a):
    """
    Return the scalar dtype of minimal size and lowest kind to represent a.
    
    Parameters:
    - a: ndarray or scalar, input to find minimal type for
    
    Returns:
    dtype: Minimal scalar type
    """

def find_common_type(array_types, scalar_types):
    """
    Determine common type following scalar-array type promotion rules.
    
    Parameters:
    - array_types: list of dtypes or None, array types
    - scalar_types: list of dtypes or None, scalar types
    
    Returns:
    dtype: Common data type
    """
```

### Type Testing Functions

Functions to test and identify data types and array properties.

```python { .api }
def isscalar(element):
    """
    Returns True if the type of element is a scalar type.
    
    Parameters:
    - element: any, input to test
    
    Returns:
    bool: True if element is scalar
    """

def issubdtype(arg1, arg2):
    """
    Returns True if first argument is a typecode lower/equal in type hierarchy.
    
    Parameters:
    - arg1, arg2: data types to compare
    
    Returns:
    bool: True if arg1 is subtype of arg2
    """

def isdtype(obj, kind):
    """
    Check if data type is of specified kind.
    
    Parameters:
    - obj: data type to check
    - kind: str, kind to check against
    
    Returns:
    bool: True if dtype matches kind
    """

def isfortran(a):
    """
    Check if array is Fortran contiguous but not C contiguous.
    
    Parameters:
    - a: ndarray, input array
    
    Returns:
    bool: True if Fortran contiguous
    """

def isreal(x):
    """
    Returns a bool array, where True if input element is real.
    
    Parameters:
    - x: array_like, input array
    
    Returns:
    ndarray: Boolean array indicating real elements
    """

def iscomplex(x):
    """
    Returns a bool array, where True if input element is complex.
    
    Parameters:
    - x: array_like, input array
    
    Returns:
    ndarray: Boolean array indicating complex elements
    """

def iscomplexobj(x):
    """
    Check for complex number or dtype.
    
    Parameters:
    - x: any, input to test
    
    Returns:
    bool: True if x is complex type or array
    """

def isrealobj(x):
    """
    Return True if x is not complex type or array.
    
    Parameters:
    - x: any, input to test
    
    Returns:
    bool: True if x is real type or array
    """
```

### String and Character Operations

Type conversion for string and character data.

```python { .api }
def typename(char):
    """
    Return description for given data type code.
    
    Parameters:
    - char: str, data type code
    
    Returns:
    str: Description of data type
    """

def mintypecode(typechars, typeset='GDFgdf', default='d'):
    """
    Return character for minimum-size type in given set.
    
    Parameters:
    - typechars: list of str, type codes
    - typeset: str, set of type codes to choose from
    - default: str, default type code
    
    Returns:
    str: Minimum type code
    """
```

### Structured Array Support

Support for structured arrays with named fields.

```python { .api }
class recarray(ndarray):
    """
    Construct ndarray that allows field access using attributes.
    
    Parameters:
    - shape: tuple, array shape
    - dtype: data-type, record structure
    - buf: buffer, data buffer
    - offset: int, buffer offset
    - strides: tuple, memory strides
    - formats: list, field formats (alternative to dtype)
    - names: list, field names (alternative to dtype)
    - titles: list, field titles
    - byteorder: str, byte order
    - aligned: bool, align fields
    """
    def __new__(subtype, shape, dtype=None, buf=None, offset=0, strides=None,
                formats=None, names=None, titles=None, byteorder=None, aligned=False): ...

class record(void):
    """
    A scalar record type for structured arrays.
    """
    def __new__(subtype, obj, dtype=None, shape=None, offset=0, formats=None,
                names=None, titles=None, byteorder=None, aligned=False): ...
```

### Memory Layout Classes

Classes for managing memory layout and views.

```python { .api }
class memmap(ndarray):
    """
    Create memory-map to array stored in binary file.
    
    Parameters:
    - filename: str or file-like, file to map
    - dtype: data-type, data type of array
    - mode: str, file access mode
    - offset: int, file offset in bytes
    - shape: tuple, desired array shape
    - order: {'C', 'F'}, memory layout order
    """
    def __new__(subtype, filename, dtype=float, mode='r+', offset=0, shape=None, order='C'): ...
```

## Common NumPy Data Types

### Integer Types

```python { .api }
# Signed integers
int8     # 8-bit signed integer (-128 to 127)
int16    # 16-bit signed integer (-32,768 to 32,767)  
int32    # 32-bit signed integer (-2^31 to 2^31-1)
int64    # 64-bit signed integer (-2^63 to 2^63-1)

# Unsigned integers  
uint8    # 8-bit unsigned integer (0 to 255)
uint16   # 16-bit unsigned integer (0 to 65,535)
uint32   # 32-bit unsigned integer (0 to 2^32-1)
uint64   # 64-bit unsigned integer (0 to 2^64-1)

# Platform-dependent integers
int_     # Platform integer (same as C long)
uint     # Platform unsigned integer (same as C unsigned long)
intp     # Platform integer used for indexing
uintp    # Platform unsigned integer used for indexing
```

### Floating Point Types

```python { .api }
float16  # 16-bit half precision float
float32  # 32-bit single precision float
float64  # 64-bit double precision float (default)
float_   # Platform double (same as float64)

# Extended precision (platform dependent)
longfloat # Extended precision float
float128  # 128-bit extended precision (if available)
```

### Complex Types

```python { .api }
complex64   # Complex number with float32 real and imaginary parts
complex128  # Complex number with float64 real and imaginary parts (default)
complex_    # Platform complex (same as complex128)
complexfloating # Base class for complex types
```

### String and Unicode Types

```python { .api }
# Fixed-length strings
str_     # Unicode string (same as <U)
bytes_   # Byte string (same as |S)

# Parameterized string types
'U10'    # Unicode string of length 10
'S20'    # Byte string of length 20
'<U5'    # Little-endian Unicode string of length 5
```

## Usage Examples

### Basic Data Type Operations

```python
import numpy as np

# Create arrays with specific data types
int_array = np.array([1, 2, 3], dtype=np.int32)
float_array = np.array([1.0, 2.0, 3.0], dtype=np.float64)
complex_array = np.array([1+2j, 3+4j], dtype=np.complex128)

# Check data type properties
print(int_array.dtype)        # int32
print(int_array.dtype.name)   # int32
print(int_array.dtype.kind)   # i (integer)
print(int_array.itemsize)     # 4 bytes

# Type conversion
float_from_int = int_array.astype(np.float64)
int_from_float = float_array.astype(np.int32)
```

### Type Information and Limits

```python
import numpy as np

# Get information about floating point types
f32_info = np.finfo(np.float32)
print(f"Float32 precision: {f32_info.precision}")
print(f"Float32 max: {f32_info.max}")
print(f"Float32 eps: {f32_info.eps}")

# Get information about integer types  
i32_info = np.iinfo(np.int32)
print(f"Int32 min: {i32_info.min}")
print(f"Int32 max: {i32_info.max}")

# Check casting compatibility
can_cast_safe = np.can_cast(np.int32, np.float64, 'safe')  # True
can_cast_unsafe = np.can_cast(np.float64, np.int32, 'unsafe')  # True
can_cast_safe_reverse = np.can_cast(np.float64, np.int32, 'safe')  # False
```

### Structured Arrays

```python
import numpy as np

# Define structured data type
person_dtype = np.dtype([
    ('name', 'U20'),
    ('age', 'i4'),
    ('height', 'f4'),
    ('married', '?')
])

# Create structured array
people = np.array([
    ('Alice', 25, 165.5, True),
    ('Bob', 30, 175.0, False),
    ('Charlie', 35, 180.2, True)
], dtype=person_dtype)

# Access fields
names = people['name']
ages = people['age']
alice_age = people[0]['age']

# Create record array for attribute access
rec_people = np.rec.fromarrays([names, ages, people['height'], people['married']],
                               names=['name', 'age', 'height', 'married'])
print(rec_people.age)  # Access age field as attribute
```

### Type Promotion and Conversion

```python
import numpy as np

# Automatic type promotion
a = np.array([1, 2, 3], dtype=np.int32)
b = np.array([1.0, 2.0, 3.0], dtype=np.float64)
result = a + b  # Result is float64

# Find promoted type
promoted = np.promote_types(np.int32, np.float32)  # float32

# Find result type for operations
result_type = np.result_type(np.int32, np.float64, np.complex64)  # complex128

# Find minimal type for scalar
minimal = np.min_scalar_type(100)  # int8 (smallest type that fits 100)
```