# Mathematical Functions

Universal functions (ufuncs) providing element-wise mathematical operations with automatic broadcasting. These functions operate on arrays element-by-element and support output to pre-allocated arrays for memory efficiency.

## Capabilities

### Arithmetic Operations

Basic arithmetic operations between arrays and scalars.

```python { .api }
def add(x1, x2, out=None, **kwargs):
    """
    Add arguments element-wise.
    
    Parameters:
    - x1, x2: array_like, input arrays to add
    - out: ndarray, array to store results
    - **kwargs: ufunc keyword arguments
    
    Returns:
    ndarray: Element-wise sum of x1 and x2
    """

def subtract(x1, x2, out=None, **kwargs):
    """
    Subtract arguments element-wise.
    
    Parameters:
    - x1, x2: array_like, input arrays
    - out: ndarray, array to store results
    - **kwargs: ufunc keyword arguments
    
    Returns:
    ndarray: Element-wise difference x1 - x2
    """

def multiply(x1, x2, out=None, **kwargs):
    """
    Multiply arguments element-wise.
    
    Parameters:
    - x1, x2: array_like, input arrays
    - out: ndarray, array to store results
    - **kwargs: ufunc keyword arguments
    
    Returns:
    ndarray: Element-wise product of x1 and x2
    """

def divide(x1, x2, out=None, **kwargs):
    """
    Returns element-wise true division of inputs.
    
    Parameters:
    - x1, x2: array_like, input arrays
    - out: ndarray, array to store results
    - **kwargs: ufunc keyword arguments
    
    Returns:
    ndarray: Element-wise division x1 / x2
    """

def true_divide(x1, x2, out=None, **kwargs):
    """
    Returns element-wise true division of inputs.
    
    Parameters:
    - x1, x2: array_like, input arrays
    - out: ndarray, array to store results
    - **kwargs: ufunc keyword arguments
    
    Returns:
    ndarray: Element-wise true division x1 / x2
    """

def floor_divide(x1, x2, out=None, **kwargs):
    """
    Returns element-wise floor division of inputs.
    
    Parameters:
    - x1, x2: array_like, input arrays
    - out: ndarray, array to store results
    - **kwargs: ufunc keyword arguments
    
    Returns:
    ndarray: Element-wise floor division x1 // x2
    """

def power(x1, x2, out=None, **kwargs):
    """
    First array elements raised to powers from second array, element-wise.
    
    Parameters:
    - x1, x2: array_like, input arrays
    - out: ndarray, array to store results
    - **kwargs: ufunc keyword arguments
    
    Returns:
    ndarray: Element-wise power x1 ** x2
    """

def mod(x1, x2, out=None, **kwargs):
    """
    Returns element-wise remainder of division.
    
    Parameters:
    - x1, x2: array_like, input arrays
    - out: ndarray, array to store results
    - **kwargs: ufunc keyword arguments
    
    Returns:
    ndarray: Element-wise remainder x1 % x2
    """

def remainder(x1, x2, out=None, **kwargs):
    """
    Returns element-wise remainder of division.
    
    Parameters:
    - x1, x2: array_like, input arrays
    - out: ndarray, array to store results
    - **kwargs: ufunc keyword arguments
    
    Returns:
    ndarray: Element-wise remainder
    """

def divmod(x1, x2, out1=None, out2=None, **kwargs):
    """
    Returns element-wise quotient and remainder simultaneously.
    
    Parameters:
    - x1, x2: array_like, input arrays
    - out1, out2: ndarray, arrays to store quotient and remainder
    - **kwargs: ufunc keyword arguments
    
    Returns:
    tuple of ndarrays: (quotient, remainder)
    """
```

### Unary Arithmetic Functions

Arithmetic operations on single arrays.

```python { .api }
def negative(x, out=None, **kwargs):
    """
    Numerical negative, element-wise.
    
    Parameters:
    - x: array_like, input array
    - out: ndarray, array to store results
    - **kwargs: ufunc keyword arguments
    
    Returns:
    ndarray: Element-wise negation -x
    """

def positive(x, out=None, **kwargs):
    """
    Numerical positive, element-wise.
    
    Parameters:
    - x: array_like, input array
    - out: ndarray, array to store results
    - **kwargs: ufunc keyword arguments
    
    Returns:
    ndarray: Element-wise positive +x
    """

def absolute(x, out=None, **kwargs):
    """
    Calculate absolute value element-wise.
    
    Parameters:
    - x: array_like, input array
    - out: ndarray, array to store results
    - **kwargs: ufunc keyword arguments
    
    Returns:
    ndarray: Element-wise absolute values
    """

def abs(x, out=None, **kwargs):
    """
    Calculate absolute value element-wise (alias for absolute).
    
    Parameters:
    - x: array_like, input array
    - out: ndarray, array to store results
    - **kwargs: ufunc keyword arguments
    
    Returns:
    ndarray: Element-wise absolute values
    """

def sign(x, out=None, **kwargs):
    """
    Returns element-wise sign of number.
    
    Parameters:
    - x: array_like, input array
    - out: ndarray, array to store results
    - **kwargs: ufunc keyword arguments
    
    Returns:
    ndarray: Element-wise sign (-1, 0, or 1)
    """

def reciprocal(x, out=None, **kwargs):
    """
    Return reciprocal of argument, element-wise.
    
    Parameters:
    - x: array_like, input array
    - out: ndarray, array to store results
    - **kwargs: ufunc keyword arguments
    
    Returns:
    ndarray: Element-wise reciprocal 1/x
    """
```

### Trigonometric Functions

Trigonometric operations in radians.

```python { .api }
def sin(x, out=None, **kwargs):
    """
    Trigonometric sine, element-wise.
    
    Parameters:
    - x: array_like, input array in radians
    - out: ndarray, array to store results
    - **kwargs: ufunc keyword arguments
    
    Returns:
    ndarray: Element-wise sine values
    """

def cos(x, out=None, **kwargs):
    """
    Cosine, element-wise.
    
    Parameters:
    - x: array_like, input array in radians
    - out: ndarray, array to store results
    - **kwargs: ufunc keyword arguments
    
    Returns:
    ndarray: Element-wise cosine values
    """

def tan(x, out=None, **kwargs):
    """
    Compute tangent element-wise.
    
    Parameters:
    - x: array_like, input array in radians
    - out: ndarray, array to store results
    - **kwargs: ufunc keyword arguments
    
    Returns:
    ndarray: Element-wise tangent values
    """

def arcsin(x, out=None, **kwargs):
    """
    Inverse sine, element-wise.
    
    Parameters:
    - x: array_like, input array in [-1, 1]
    - out: ndarray, array to store results
    - **kwargs: ufunc keyword arguments
    
    Returns:
    ndarray: Element-wise arcsine in radians
    """

def arccos(x, out=None, **kwargs):
    """
    Trigonometric inverse cosine, element-wise.
    
    Parameters:
    - x: array_like, input array in [-1, 1]
    - out: ndarray, array to store results
    - **kwargs: ufunc keyword arguments
    
    Returns:
    ndarray: Element-wise arccosine in radians
    """

def arctan(x, out=None, **kwargs):
    """
    Trigonometric inverse tangent, element-wise.
    
    Parameters:
    - x: array_like, input array
    - out: ndarray, array to store results
    - **kwargs: ufunc keyword arguments
    
    Returns:
    ndarray: Element-wise arctangent in radians
    """

def arctan2(x1, x2, out=None, **kwargs):
    """
    Element-wise arc tangent of x1/x2 choosing quadrant correctly.
    
    Parameters:
    - x1, x2: array_like, y and x coordinates
    - out: ndarray, array to store results
    - **kwargs: ufunc keyword arguments
    
    Returns:
    ndarray: Element-wise arctangent of x1/x2 in radians
    """
```

### Hyperbolic Functions

Hyperbolic trigonometric functions.

```python { .api }
def sinh(x, out=None, **kwargs):
    """
    Hyperbolic sine, element-wise.
    
    Parameters:
    - x: array_like, input array
    - out: ndarray, array to store results
    - **kwargs: ufunc keyword arguments
    
    Returns:
    ndarray: Element-wise hyperbolic sine
    """

def cosh(x, out=None, **kwargs):
    """
    Hyperbolic cosine, element-wise.
    
    Parameters:
    - x: array_like, input array
    - out: ndarray, array to store results
    - **kwargs: ufunc keyword arguments
    
    Returns:
    ndarray: Element-wise hyperbolic cosine
    """

def tanh(x, out=None, **kwargs):
    """
    Compute hyperbolic tangent element-wise.
    
    Parameters:
    - x: array_like, input array
    - out: ndarray, array to store results
    - **kwargs: ufunc keyword arguments
    
    Returns:
    ndarray: Element-wise hyperbolic tangent
    """

def arcsinh(x, out=None, **kwargs):
    """
    Inverse hyperbolic sine element-wise.
    
    Parameters:
    - x: array_like, input array
    - out: ndarray, array to store results
    - **kwargs: ufunc keyword arguments
    
    Returns:
    ndarray: Element-wise inverse hyperbolic sine
    """

def arccosh(x, out=None, **kwargs):
    """
    Inverse hyperbolic cosine, element-wise.
    
    Parameters:
    - x: array_like, input array with x >= 1
    - out: ndarray, array to store results
    - **kwargs: ufunc keyword arguments
    
    Returns:
    ndarray: Element-wise inverse hyperbolic cosine
    """

def arctanh(x, out=None, **kwargs):
    """
    Inverse hyperbolic tangent element-wise.
    
    Parameters:
    - x: array_like, input array in (-1, 1)
    - out: ndarray, array to store results
    - **kwargs: ufunc keyword arguments
    
    Returns:
    ndarray: Element-wise inverse hyperbolic tangent
    """
```

### Exponential and Logarithmic Functions

Exponential and logarithmic operations.

```python { .api }
def exp(x, out=None, **kwargs):
    """
    Calculate exponential of all elements in input array.
    
    Parameters:
    - x: array_like, input array
    - out: ndarray, array to store results
    - **kwargs: ufunc keyword arguments
    
    Returns:
    ndarray: Element-wise exponential e^x
    """

def exp2(x, out=None, **kwargs):
    """
    Calculate 2**p for all p in input array.
    
    Parameters:
    - x: array_like, input array
    - out: ndarray, array to store results
    - **kwargs: ufunc keyword arguments
    
    Returns:
    ndarray: Element-wise 2^x
    """

def expm1(x, out=None, **kwargs):
    """
    Calculate exp(x) - 1 for all elements in array.
    
    Parameters:
    - x: array_like, input array
    - out: ndarray, array to store results
    - **kwargs: ufunc keyword arguments
    
    Returns:
    ndarray: Element-wise exp(x) - 1
    """

def log(x, out=None, **kwargs):
    """
    Natural logarithm, element-wise.
    
    Parameters:
    - x: array_like, input array
    - out: ndarray, array to store results
    - **kwargs: ufunc keyword arguments
    
    Returns:
    ndarray: Element-wise natural logarithm
    """

def log2(x, out=None, **kwargs):
    """
    Base-2 logarithm of x.
    
    Parameters:
    - x: array_like, input array
    - out: ndarray, array to store results
    - **kwargs: ufunc keyword arguments
    
    Returns:
    ndarray: Element-wise base-2 logarithm
    """

def log10(x, out=None, **kwargs):
    """
    Return base 10 logarithm of input array, element-wise.
    
    Parameters:
    - x: array_like, input array
    - out: ndarray, array to store results
    - **kwargs: ufunc keyword arguments
    
    Returns:
    ndarray: Element-wise base-10 logarithm
    """

def log1p(x, out=None, **kwargs):
    """
    Return natural logarithm of one plus input array, element-wise.
    
    Parameters:
    - x: array_like, input array
    - out: ndarray, array to store results
    - **kwargs: ufunc keyword arguments
    
    Returns:
    ndarray: Element-wise log(1 + x)
    """

def logaddexp(x1, x2, out=None, **kwargs):
    """
    Logarithm of sum of exponentials of inputs.
    
    Parameters:
    - x1, x2: array_like, input arrays
    - out: ndarray, array to store results
    - **kwargs: ufunc keyword arguments
    
    Returns:
    ndarray: Element-wise log(exp(x1) + exp(x2))
    """

def logaddexp2(x1, x2, out=None, **kwargs):
    """
    Logarithm of sum of exponentials of inputs in base-2.
    
    Parameters:
    - x1, x2: array_like, input arrays
    - out: ndarray, array to store results
    - **kwargs: ufunc keyword arguments
    
    Returns:
    ndarray: Element-wise log2(2^x1 + 2^x2)
    """
```

### Power and Root Functions

Power and square root operations.

```python { .api }
def sqrt(x, out=None, **kwargs):
    """
    Return non-negative square-root of array, element-wise.
    
    Parameters:
    - x: array_like, input array
    - out: ndarray, array to store results
    - **kwargs: ufunc keyword arguments
    
    Returns:
    ndarray: Element-wise square root
    """

def square(x, out=None, **kwargs):
    """
    Return element-wise square of input.
    
    Parameters:
    - x: array_like, input array
    - out: ndarray, array to store results
    - **kwargs: ufunc keyword arguments
    
    Returns:
    ndarray: Element-wise square x^2
    """

def cbrt(x, out=None, **kwargs):
    """
    Return cube-root of array, element-wise.
    
    Parameters:
    - x: array_like, input array
    - out: ndarray, array to store results
    - **kwargs: ufunc keyword arguments
    
    Returns:
    ndarray: Element-wise cube root
    """
```

### Comparison Functions

Element-wise comparison operations.

```python { .api }
def equal(x1, x2, out=None, **kwargs):
    """
    Return (x1 == x2) element-wise.
    
    Parameters:
    - x1, x2: array_like, input arrays to compare
    - out: ndarray, array to store results
    - **kwargs: ufunc keyword arguments
    
    Returns:
    ndarray: Boolean array of equality comparison
    """

def not_equal(x1, x2, out=None, **kwargs):
    """
    Return (x1 != x2) element-wise.
    
    Parameters:
    - x1, x2: array_like, input arrays to compare
    - out: ndarray, array to store results
    - **kwargs: ufunc keyword arguments
    
    Returns:
    ndarray: Boolean array of inequality comparison
    """

def less(x1, x2, out=None, **kwargs):
    """
    Return truth value of (x1 < x2) element-wise.
    
    Parameters:
    - x1, x2: array_like, input arrays to compare
    - out: ndarray, array to store results
    - **kwargs: ufunc keyword arguments
    
    Returns:
    ndarray: Boolean array of less-than comparison
    """

def less_equal(x1, x2, out=None, **kwargs):
    """
    Return truth value of (x1 <= x2) element-wise.
    
    Parameters:
    - x1, x2: array_like, input arrays to compare
    - out: ndarray, array to store results
    - **kwargs: ufunc keyword arguments
    
    Returns:
    ndarray: Boolean array of less-than-or-equal comparison
    """

def greater(x1, x2, out=None, **kwargs):
    """
    Return truth value of (x1 > x2) element-wise.
    
    Parameters:
    - x1, x2: array_like, input arrays to compare
    - out: ndarray, array to store results
    - **kwargs: ufunc keyword arguments
    
    Returns:
    ndarray: Boolean array of greater-than comparison
    """

def greater_equal(x1, x2, out=None, **kwargs):
    """
    Return truth value of (x1 >= x2) element-wise.
    
    Parameters:
    - x1, x2: array_like, input arrays to compare
    - out: ndarray, array to store results
    - **kwargs: ufunc keyword arguments
    
    Returns:
    ndarray: Boolean array of greater-than-or-equal comparison
    """

def maximum(x1, x2, out=None, **kwargs):
    """
    Element-wise maximum of array elements.
    
    Parameters:
    - x1, x2: array_like, input arrays
    - out: ndarray, array to store results
    - **kwargs: ufunc keyword arguments
    
    Returns:
    ndarray: Element-wise maximum values
    """

def minimum(x1, x2, out=None, **kwargs):
    """
    Element-wise minimum of array elements.
    
    Parameters:
    - x1, x2: array_like, input arrays
    - out: ndarray, array to store results
    - **kwargs: ufunc keyword arguments
    
    Returns:
    ndarray: Element-wise minimum values
    """

def fmax(x1, x2, out=None, **kwargs):
    """
    Element-wise maximum, ignoring NaNs.
    
    Parameters:
    - x1, x2: array_like, input arrays
    - out: ndarray, array to store results
    - **kwargs: ufunc keyword arguments
    
    Returns:
    ndarray: Element-wise maximum ignoring NaN
    """

def fmin(x1, x2, out=None, **kwargs):
    """
    Element-wise minimum, ignoring NaNs.
    
    Parameters:
    - x1, x2: array_like, input arrays
    - out: ndarray, array to store results
    - **kwargs: ufunc keyword arguments
    
    Returns:
    ndarray: Element-wise minimum ignoring NaN
    """
```

### Logical Functions

Element-wise logical operations.

```python { .api }
def logical_and(x1, x2, out=None, **kwargs):
    """
    Compute truth value of x1 AND x2 element-wise.
    
    Parameters:
    - x1, x2: array_like, input arrays
    - out: ndarray, array to store results
    - **kwargs: ufunc keyword arguments
    
    Returns:
    ndarray: Boolean array of logical AND
    """

def logical_or(x1, x2, out=None, **kwargs):
    """
    Compute truth value of x1 OR x2 element-wise.
    
    Parameters:
    - x1, x2: array_like, input arrays
    - out: ndarray, array to store results
    - **kwargs: ufunc keyword arguments
    
    Returns:
    ndarray: Boolean array of logical OR
    """

def logical_not(x, out=None, **kwargs):
    """
    Compute truth value of NOT x element-wise.
    
    Parameters:
    - x: array_like, input array
    - out: ndarray, array to store results
    - **kwargs: ufunc keyword arguments
    
    Returns:
    ndarray: Boolean array of logical NOT
    """

def logical_xor(x1, x2, out=None, **kwargs):
    """
    Compute truth value of x1 XOR x2 element-wise.
    
    Parameters:
    - x1, x2: array_like, input arrays
    - out: ndarray, array to store results
    - **kwargs: ufunc keyword arguments
    
    Returns:
    ndarray: Boolean array of logical XOR
    """
```

### Bitwise Operations

Bitwise operations on integer arrays.

```python { .api }
def bitwise_and(x1, x2, out=None, **kwargs):
    """
    Compute bitwise AND of two arrays element-wise.
    
    Parameters:
    - x1, x2: array_like, input arrays (integers only)
    - out: ndarray, array to store results
    - **kwargs: ufunc keyword arguments
    
    Returns:
    ndarray: Element-wise bitwise AND
    """

def bitwise_or(x1, x2, out=None, **kwargs):
    """
    Compute bitwise OR of two arrays element-wise.
    
    Parameters:
    - x1, x2: array_like, input arrays (integers only)
    - out: ndarray, array to store results
    - **kwargs: ufunc keyword arguments
    
    Returns:
    ndarray: Element-wise bitwise OR
    """

def bitwise_xor(x1, x2, out=None, **kwargs):
    """
    Compute bitwise XOR of two arrays element-wise.
    
    Parameters:
    - x1, x2: array_like, input arrays (integers only)
    - out: ndarray, array to store results
    - **kwargs: ufunc keyword arguments
    
    Returns:
    ndarray: Element-wise bitwise XOR
    """

def bitwise_not(x, out=None, **kwargs):
    """
    Compute bit-wise inversion, or bit-wise NOT, element-wise.
    
    Parameters:
    - x: array_like, input array (integers only)
    - out: ndarray, array to store results
    - **kwargs: ufunc keyword arguments
    
    Returns:
    ndarray: Element-wise bitwise NOT
    """

def invert(x, out=None, **kwargs):
    """
    Compute bit-wise inversion, or bit-wise NOT, element-wise.
    
    Parameters:
    - x: array_like, input array (integers only)
    - out: ndarray, array to store results
    - **kwargs: ufunc keyword arguments
    
    Returns:
    ndarray: Element-wise bitwise inversion
    """

def left_shift(x1, x2, out=None, **kwargs):
    """
    Shift bits of integer to the left.
    
    Parameters:
    - x1, x2: array_like, input arrays (integers only)
    - out: ndarray, array to store results
    - **kwargs: ufunc keyword arguments
    
    Returns:
    ndarray: Element-wise left bit shift
    """

def right_shift(x1, x2, out=None, **kwargs):
    """
    Shift bits of integer to the right.
    
    Parameters:
    - x1, x2: array_like, input arrays (integers only)
    - out: ndarray, array to store results
    - **kwargs: ufunc keyword arguments
    
    Returns:
    ndarray: Element-wise right bit shift
    """
```

### Floating Point Functions

Floating point specific operations and tests.

```python { .api }
def isfinite(x, out=None, **kwargs):
    """
    Test element-wise for finiteness (not infinity and not NaN).
    
    Parameters:
    - x: array_like, input array
    - out: ndarray, array to store results
    - **kwargs: ufunc keyword arguments
    
    Returns:
    ndarray: Boolean array indicating finite elements
    """

def isinf(x, out=None, **kwargs):
    """
    Test element-wise for positive or negative infinity.
    
    Parameters:
    - x: array_like, input array
    - out: ndarray, array to store results
    - **kwargs: ufunc keyword arguments
    
    Returns:
    ndarray: Boolean array indicating infinite elements
    """

def isnan(x, out=None, **kwargs):
    """
    Test element-wise for NaN and return result as boolean array.
    
    Parameters:
    - x: array_like, input array
    - out: ndarray, array to store results
    - **kwargs: ufunc keyword arguments
    
    Returns:
    ndarray: Boolean array indicating NaN elements
    """

def signbit(x, out=None, **kwargs):
    """
    Returns element-wise True where signbit is set (less than zero).
    
    Parameters:
    - x: array_like, input array
    - out: ndarray, array to store results
    - **kwargs: ufunc keyword arguments
    
    Returns:
    ndarray: Boolean array indicating negative sign bit
    """

def copysign(x1, x2, out=None, **kwargs):
    """
    Change sign of x1 to that of x2, element-wise.
    
    Parameters:
    - x1, x2: array_like, input arrays
    - out: ndarray, array to store results
    - **kwargs: ufunc keyword arguments
    
    Returns:
    ndarray: Element-wise copy of sign from x2 to x1
    """

def nextafter(x1, x2, out=None, **kwargs):
    """
    Return next floating-point value after x1 towards x2, element-wise.
    
    Parameters:
    - x1, x2: array_like, input arrays
    - out: ndarray, array to store results
    - **kwargs: ufunc keyword arguments
    
    Returns:
    ndarray: Next representable floating-point values
    """

def spacing(x, out=None, **kwargs):
    """
    Return distance between x and adjacent number, element-wise.
    
    Parameters:
    - x: array_like, input array
    - out: ndarray, array to store results
    - **kwargs: ufunc keyword arguments
    
    Returns:
    ndarray: Spacing to next floating-point number
    """

def ldexp(x1, x2, out=None, **kwargs):
    """
    Returns x1 * 2**x2, element-wise.
    
    Parameters:
    - x1, x2: array_like, mantissa and exponent arrays
    - out: ndarray, array to store results
    - **kwargs: ufunc keyword arguments
    
    Returns:
    ndarray: Element-wise x1 * 2**x2
    """

def frexp(x, out1=None, out2=None, **kwargs):
    """
    Decompose elements of x into mantissa and twos exponent.
    
    Parameters:
    - x: array_like, input array
    - out1, out2: ndarray, arrays to store mantissa and exponent
    - **kwargs: ufunc keyword arguments
    
    Returns:
    tuple of ndarrays: (mantissa, exponent)
    """

def floor(x, out=None, **kwargs):
    """
    Return floor of input, element-wise.
    
    Parameters:
    - x: array_like, input array
    - out: ndarray, array to store results
    - **kwargs: ufunc keyword arguments
    
    Returns:
    ndarray: Element-wise floor values
    """

def ceil(x, out=None, **kwargs):
    """
    Return ceiling of input, element-wise.
    
    Parameters:
    - x: array_like, input array
    - out: ndarray, array to store results
    - **kwargs: ufunc keyword arguments
    
    Returns:
    ndarray: Element-wise ceiling values
    """

def trunc(x, out=None, **kwargs):
    """
    Return truncated value of input, element-wise.
    
    Parameters:
    - x: array_like, input array
    - out: ndarray, array to store results
    - **kwargs: ufunc keyword arguments
    
    Returns:
    ndarray: Element-wise truncated values
    """

def rint(x, out=None, **kwargs):
    """
    Round elements to nearest integers.
    
    Parameters:
    - x: array_like, input array
    - out: ndarray, array to store results
    - **kwargs: ufunc keyword arguments
    
    Returns:
    ndarray: Element-wise rounded to nearest integers
    """

def modf(x, out1=None, out2=None, **kwargs):
    """
    Return fractional and integral parts of array, element-wise.
    
    Parameters:
    - x: array_like, input array
    - out1, out2: ndarray, arrays to store fractional and integral parts
    - **kwargs: ufunc keyword arguments
    
    Returns:
    tuple of ndarrays: (fractional_part, integral_part)
    """
```

## Usage Examples

### Basic Arithmetic Operations

```python
import numpy as np

# Element-wise arithmetic
a = np.array([1, 2, 3, 4])
b = np.array([5, 6, 7, 8])

sum_result = np.add(a, b)        # [6, 8, 10, 12]
diff_result = np.subtract(b, a)  # [4, 4, 4, 4]
prod_result = np.multiply(a, b)  # [5, 12, 21, 32]
div_result = np.divide(b, a)     # [5.0, 3.0, 2.33, 2.0]

# Broadcasting with scalars
scaled = np.multiply(a, 10)      # [10, 20, 30, 40]
```

### Trigonometric Functions

```python
import numpy as np

# Trigonometric operations
angles = np.array([0, np.pi/4, np.pi/2, np.pi])
sin_vals = np.sin(angles)        # [0, 0.707, 1, 0]
cos_vals = np.cos(angles)        # [1, 0.707, 0, -1]

# Convert degrees to radians first
degrees = np.array([0, 45, 90, 180])
radians = np.radians(degrees)    # Convert to radians
sin_degrees = np.sin(radians)    # Sine of degree values
```

### Exponential and Logarithmic Functions

```python
import numpy as np

# Exponential functions
x = np.array([1, 2, 3])
exp_vals = np.exp(x)            # [2.718, 7.389, 20.086]
exp2_vals = np.exp2(x)          # [2, 4, 8]

# Logarithmic functions
y = np.array([1, 10, 100])
log_vals = np.log(y)            # [0, 2.303, 4.605]
log10_vals = np.log10(y)        # [0, 1, 2]
```