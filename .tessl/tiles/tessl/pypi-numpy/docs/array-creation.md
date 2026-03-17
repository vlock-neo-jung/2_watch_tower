# Array Creation and Manipulation

Core NumPy functionality for creating, reshaping, joining, and manipulating N-dimensional arrays. These operations form the foundation of array-based computing in Python.

## Capabilities

### Basic Array Creation

Create arrays from existing data or initialize new arrays with specific patterns.

```python { .api }
def array(object, dtype=None, copy=True, order='K', subok=False, ndmin=0, like=None):
    """
    Create an array from an array-like object.
    
    Parameters:
    - object: array_like, sequence to convert to array
    - dtype: data-type, desired data type
    - copy: bool, whether to copy the data
    - order: {'K', 'A', 'C', 'F'}, memory layout
    - subok: bool, whether to pass through subclasses
    - ndmin: int, minimum number of dimensions
    - like: array_like, reference object for array creation
    
    Returns:
    ndarray: New array object
    """

def asarray(a, dtype=None, order=None, like=None):
    """
    Convert input to an array.
    
    Parameters:
    - a: array_like, input data
    - dtype: data-type, desired data type
    - order: {'C', 'F', 'A', 'K'}, memory layout
    - like: array_like, reference object
    
    Returns:
    ndarray: Array interpretation of input
    """

def asanyarray(a, dtype=None, order=None, like=None):
    """
    Convert input to ndarray, preserving subclasses.
    
    Parameters:
    - a: array_like, input data
    - dtype: data-type, desired data type
    - order: {'C', 'F', 'A', 'K'}, memory layout
    - like: array_like, reference object
    
    Returns:
    ndarray: Array interpretation preserving subclass
    """

def ascontiguousarray(a, dtype=None, like=None):
    """
    Return a contiguous array in memory (C order).
    
    Parameters:
    - a: array_like, input array
    - dtype: data-type, desired data type
    - like: array_like, reference object
    
    Returns:
    ndarray: Contiguous array
    """

def asfortranarray(a, dtype=None, like=None):
    """
    Return an array laid out in Fortran order in memory.
    
    Parameters:
    - a: array_like, input array
    - dtype: data-type, desired data type
    - like: array_like, reference object
    
    Returns:
    ndarray: Fortran-ordered array
    """
```

### Array Initialization

Create arrays filled with specific values or uninitialized arrays of given shapes.

```python { .api }
def empty(shape, dtype=float, order='C', like=None):
    """
    Return a new array of given shape without initializing entries.
    
    Parameters:
    - shape: int or tuple of ints, shape of new array
    - dtype: data-type, desired data type
    - order: {'C', 'F'}, memory layout
    - like: array_like, reference object
    
    Returns:
    ndarray: Uninitialized array
    """

def zeros(shape, dtype=float, order='C', like=None):
    """
    Return a new array of given shape filled with zeros.
    
    Parameters:
    - shape: int or tuple of ints, shape of new array
    - dtype: data-type, desired data type
    - order: {'C', 'F'}, memory layout
    - like: array_like, reference object
    
    Returns:
    ndarray: Array of zeros
    """

def ones(shape, dtype=None, order='C', like=None):
    """
    Return a new array of given shape filled with ones.
    
    Parameters:
    - shape: int or tuple of ints, shape of new array
    - dtype: data-type, desired data type
    - order: {'C', 'F'}, memory layout
    - like: array_like, reference object
    
    Returns:
    ndarray: Array of ones
    """

def full(shape, fill_value, dtype=None, order='C', like=None):
    """
    Return a new array of given shape filled with fill_value.
    
    Parameters:
    - shape: int or tuple of ints, shape of new array
    - fill_value: scalar, fill value
    - dtype: data-type, desired data type
    - order: {'C', 'F'}, memory layout
    - like: array_like, reference object
    
    Returns:
    ndarray: Array filled with fill_value
    """
```

### Array Creation from Existing Arrays

Create arrays with the same shape as existing arrays.

```python { .api }
def empty_like(prototype, dtype=None, order='K', subok=True, shape=None):
    """
    Return a new array with the same shape as a given array.
    
    Parameters:
    - prototype: array_like, shape and data-type of prototype define these
    - dtype: data-type, override data type
    - order: {'C', 'F', 'A', 'K'}, memory layout
    - subok: bool, return a subarray if True
    - shape: int or tuple of ints, override shape
    
    Returns:
    ndarray: Uninitialized array with same shape as prototype
    """

def zeros_like(a, dtype=None, order='K', subok=True, shape=None):
    """
    Return an array of zeros with the same shape as a given array.
    
    Parameters:
    - a: array_like, shape and data-type of a define these
    - dtype: data-type, override data type
    - order: {'C', 'F', 'A', 'K'}, memory layout
    - subok: bool, return a subarray if True
    - shape: int or tuple of ints, override shape
    
    Returns:
    ndarray: Array of zeros with same shape as a
    """

def ones_like(a, dtype=None, order='K', subok=True, shape=None):
    """
    Return an array of ones with the same shape as a given array.
    
    Parameters:
    - a: array_like, shape and data-type of a define these
    - dtype: data-type, override data type
    - order: {'C', 'F', 'A', 'K'}, memory layout  
    - subok: bool, return a subarray if True
    - shape: int or tuple of ints, override shape
    
    Returns:
    ndarray: Array of ones with same shape as a
    """

def full_like(a, fill_value, dtype=None, order='K', subok=True, shape=None):
    """
    Return a full array with the same shape as a given array.
    
    Parameters:
    - a: array_like, shape and data-type of a define these
    - fill_value: scalar, fill value
    - dtype: data-type, override data type
    - order: {'C', 'F', 'A', 'K'}, memory layout
    - subok: bool, return a subarray if True
    - shape: int or tuple of ints, override shape
    
    Returns:
    ndarray: Array filled with fill_value with same shape as a
    """
```

### Numerical Ranges

Create arrays containing sequences of numbers.

```python { .api }
def arange(start, stop=None, step=1, dtype=None, like=None):
    """
    Return evenly spaced values within a given interval.
    
    Parameters:
    - start: number, start of interval
    - stop: number, end of interval (not included)
    - step: number, spacing between values
    - dtype: data-type, type of output array
    - like: array_like, reference object
    
    Returns:
    ndarray: Array of evenly spaced values
    """

def linspace(start, stop, num=50, endpoint=True, retstep=False, dtype=None, axis=0):
    """
    Return evenly spaced numbers over a specified interval.
    
    Parameters:
    - start: array_like, starting value of sequence
    - stop: array_like, end value of sequence
    - num: int, number of samples to generate
    - endpoint: bool, whether to include stop in samples
    - retstep: bool, whether to return spacing between samples
    - dtype: data-type, type of output array
    - axis: int, axis in result to store samples
    
    Returns:
    ndarray: Array of evenly spaced samples
    """

def logspace(start, stop, num=50, endpoint=True, base=10.0, dtype=None, axis=0):
    """
    Return numbers spaced evenly on a log scale.
    
    Parameters:
    - start: array_like, base**start is starting value
    - stop: array_like, base**stop is final value
    - num: int, number of samples to generate
    - endpoint: bool, whether to include stop in samples
    - base: array_like, base of log space
    - dtype: data-type, type of output array
    - axis: int, axis in result to store samples
    
    Returns:
    ndarray: Array of samples on log scale
    """

def geomspace(start, stop, num=50, endpoint=True, dtype=None, axis=0):
    """
    Return numbers spaced evenly on a log scale (geometric progression).
    
    Parameters:
    - start: array_like, starting value of sequence
    - stop: array_like, final value of sequence
    - num: int, number of samples to generate
    - endpoint: bool, whether to include stop in samples
    - dtype: data-type, type of output array
    - axis: int, axis in result to store samples
    
    Returns:
    ndarray: Array of samples on geometric progression
    """
```

### Identity and Diagonal Arrays

Create identity matrices and arrays with values on diagonals.

```python { .api }
def identity(n, dtype=None, like=None):
    """
    Return the identity array.
    
    Parameters:
    - n: int, number of rows (and columns) in output
    - dtype: data-type, data type of output
    - like: array_like, reference object
    
    Returns:
    ndarray: Identity array of shape (n, n)
    """

def eye(N, M=None, k=0, dtype=float, order='C', like=None):
    """
    Return a 2-D array with ones on the diagonal and zeros elsewhere.
    
    Parameters:
    - N: int, number of rows in output
    - M: int, number of columns in output (defaults to N)
    - k: int, index of diagonal (0 for main diagonal)
    - dtype: data-type, data type of output
    - order: {'C', 'F'}, memory layout
    - like: array_like, reference object
    
    Returns:
    ndarray: Array with ones on k-th diagonal
    """
```

### Shape Manipulation

Change the shape and organization of arrays without changing the data.

```python { .api }
def reshape(a, newshape, order='C'):
    """
    Give a new shape to an array without changing its data.
    
    Parameters:
    - a: array_like, array to reshape
    - newshape: int or tuple of ints, new shape
    - order: {'C', 'F', 'A'}, index order
    
    Returns:
    ndarray: Reshaped array
    """

def resize(a, new_shape):
    """
    Return a new array with the specified shape.
    
    Parameters:
    - a: array_like, array to resize
    - new_shape: int or tuple of ints, shape of resized array
    
    Returns:
    ndarray: Resized array with new_shape
    """

def ravel(a, order='C'):
    """
    Return a contiguous flattened array.
    
    Parameters:
    - a: array_like, input array
    - order: {'C', 'F', 'A', 'K'}, flattening order
    
    Returns:
    ndarray: 1-D array containing elements of input
    """

def flatten(order='C'):
    """
    Return a copy of the array collapsed into one dimension.
    
    Parameters:
    - order: {'C', 'F', 'A', 'K'}, flattening order
    
    Returns:
    ndarray: 1-D array containing copy of input elements
    """
```

### Array Transposition and Axis Manipulation

Rearrange the axes and dimensions of arrays.

```python { .api }
def transpose(a, axes=None):
    """
    Return an array with axes transposed.
    
    Parameters:
    - a: array_like, input array
    - axes: tuple or list of ints, permutation of axes
    
    Returns:
    ndarray: Array with transposed axes
    """

def swapaxes(a, axis1, axis2):
    """
    Interchange two axes of an array.
    
    Parameters:
    - a: array_like, input array
    - axis1: int, first axis
    - axis2: int, second axis
    
    Returns:
    ndarray: Array with swapped axes
    """

def moveaxis(a, source, destination):
    """
    Move axes of an array to new positions.
    
    Parameters:
    - a: array_like, array whose axes should be reordered
    - source: int or sequence of ints, original positions of axes
    - destination: int or sequence of ints, destination positions
    
    Returns:
    ndarray: Array with moved axes
    """

def rollaxis(a, axis, start=0):
    """
    Roll the specified axis backwards.
    
    Parameters:
    - a: array_like, input array
    - axis: int, axis to roll backwards
    - start: int, position where rolled axis starts
    
    Returns:
    ndarray: Array with rolled axis
    """

def roll(a, shift, axis=None):
    """
    Roll array elements along a given axis.
    
    Parameters:
    - a: array_like, input array
    - shift: int or tuple of ints, number of places to shift
    - axis: int or tuple of ints, axis along which to roll
    
    Returns:
    ndarray: Array with elements rolled
    """
```

### Dimension Manipulation

Add or remove array dimensions.

```python { .api }
def squeeze(a, axis=None):
    """
    Remove axes of length one from array.
    
    Parameters:
    - a: array_like, input array
    - axis: None or int or tuple of ints, axes to squeeze
    
    Returns:
    ndarray: Input array with length-one axes removed
    """

def expand_dims(a, axis):
    """
    Expand the shape of an array.
    
    Parameters:
    - a: array_like, input array
    - axis: int or tuple of ints, position of new axes
    
    Returns:
    ndarray: Array with expanded dimensions
    """
```

### Array Joining

Combine multiple arrays into single arrays.

```python { .api }
def concatenate(arrays, axis=0, out=None, dtype=None, casting="same_kind"):
    """
    Join a sequence of arrays along an existing axis.
    
    Parameters:
    - arrays: sequence of array_like, arrays to concatenate
    - axis: int, axis along which arrays are joined
    - out: ndarray, destination for result
    - dtype: data-type, type of output array
    - casting: {'no', 'equiv', 'safe', 'same_kind', 'unsafe'}, casting rule
    
    Returns:
    ndarray: Concatenated array
    """

def stack(arrays, axis=0, out=None, dtype=None, casting="same_kind"):
    """
    Join a sequence of arrays along a new axis.
    
    Parameters:
    - arrays: sequence of array_like, arrays to stack
    - axis: int, axis in result array along which input arrays are stacked
    - out: ndarray, destination for result
    - dtype: data-type, type of output array
    - casting: {'no', 'equiv', 'safe', 'same_kind', 'unsafe'}, casting rule
    
    Returns:
    ndarray: Stacked array with one more dimension than input arrays
    """

def hstack(tup, dtype=None, casting="same_kind"):
    """
    Stack arrays in sequence horizontally (column wise).
    
    Parameters:
    - tup: sequence of ndarrays, arrays to stack
    - dtype: data-type, type of output array
    - casting: {'no', 'equiv', 'safe', 'same_kind', 'unsafe'}, casting rule
    
    Returns:
    ndarray: Stacked array
    """

def vstack(tup, dtype=None, casting="same_kind"):
    """
    Stack arrays in sequence vertically (row wise).
    
    Parameters:
    - tup: sequence of ndarrays, arrays to stack
    - dtype: data-type, type of output array
    - casting: {'no', 'equiv', 'safe', 'same_kind', 'unsafe'}, casting rule
    
    Returns:
    ndarray: Stacked array
    """

def dstack(tup):
    """
    Stack arrays in sequence depth wise (along third axis).
    
    Parameters:
    - tup: sequence of arrays, arrays to stack
    
    Returns:
    ndarray: Stacked array along third axis
    """

def block(arrays):
    """
    Assemble an nd-array from nested lists of blocks.
    
    Parameters:
    - arrays: nested list of array_like or scalars, block structure
    
    Returns:
    ndarray: Block array assembled from input arrays
    """
```

### Array Splitting

Split arrays into multiple sub-arrays.

```python { .api }
def split(ary, indices_or_sections, axis=0):
    """
    Split an array into multiple sub-arrays as views.
    
    Parameters:
    - ary: ndarray, array to split
    - indices_or_sections: int or 1-D array, split points or number of sections
    - axis: int, axis along which to split
    
    Returns:
    list of ndarrays: Sub-arrays as views of ary
    """

def hsplit(ary, indices_or_sections):
    """
    Split an array into multiple sub-arrays horizontally.
    
    Parameters:
    - ary: ndarray, array to split
    - indices_or_sections: int or 1-D array, split points or sections
    
    Returns:
    list of ndarrays: Horizontally split sub-arrays
    """

def vsplit(ary, indices_or_sections):
    """
    Split an array into multiple sub-arrays vertically.
    
    Parameters:
    - ary: ndarray, array to split
    - indices_or_sections: int or 1-D array, split points or sections
    
    Returns:
    list of ndarrays: Vertically split sub-arrays
    """

def dsplit(ary, indices_or_sections):
    """
    Split array into multiple sub-arrays along 3rd axis (depth).
    
    Parameters:
    - ary: ndarray, array to split
    - indices_or_sections: int or 1-D array, split points or sections
    
    Returns:
    list of ndarrays: Sub-arrays split along third axis
    """
```

### Array Tiling and Repetition

Create arrays by tiling or repeating existing arrays.

```python { .api }
def tile(A, reps):
    """
    Construct an array by repeating A the number of times given by reps.
    
    Parameters:
    - A: array_like, input array
    - reps: int or tuple of ints, repetitions along each axis
    
    Returns:
    ndarray: Tiled array
    """

def repeat(a, repeats, axis=None):
    """
    Repeat elements of an array.
    
    Parameters:
    - a: array_like, input array
    - repeats: int or array of ints, repetitions for each element
    - axis: int, axis along which to repeat values
    
    Returns:
    ndarray: Array with repeated elements
    """
```

### Broadcasting and Indexing Utilities

Functions for advanced array indexing and broadcasting operations.

```python { .api }
def broadcast(*args):
    """
    Produce an object that mimics broadcasting.
    
    Parameters:
    - *args: array_like, arrays to broadcast
    
    Returns:
    broadcast object: Iterator that broadcasts input arrays
    """

def broadcast_arrays(*args, subok=False):
    """
    Broadcast any number of arrays against each other.
    
    Parameters:
    - *args: array_like, arrays to broadcast
    - subok: bool, whether to return subclasses
    
    Returns:
    list of arrays: Broadcasted arrays
    """

def broadcast_to(array, shape, subok=False):
    """
    Broadcast an array to a new shape.
    
    Parameters:
    - array: array_like, array to broadcast
    - shape: tuple, desired shape
    - subok: bool, whether to return subclasses
    
    Returns:
    ndarray: Broadcast array
    """

def ix_(*args):
    """
    Construct an open mesh from multiple sequences.
    
    Parameters:
    - *args: 1-D sequences, coordinate vectors
    
    Returns:
    tuple of ndarrays: N-D coordinate arrays for N-D grid
    """

def indices(dimensions, dtype=int, sparse=False):
    """
    Return an array representing the indices of a grid.
    
    Parameters:
    - dimensions: sequence of ints, shape of the grid
    - dtype: dtype, data type of result
    - sparse: bool, return sparse representation
    
    Returns:
    ndarray: Grid indices
    """

def unravel_index(indices, shape, order='C'):
    """
    Convert flat index into tuple of coordinate arrays.
    
    Parameters:
    - indices: array_like, array of flat indices
    - shape: tuple of ints, shape of array into which indices index
    - order: {'C', 'F'}, index order
    
    Returns:
    tuple of ndarrays: Tuple of coordinate arrays
    """

def ravel_multi_index(multi_index, dims, mode='raise', order='C'):
    """
    Convert a tuple of index arrays into flat indices.
    
    Parameters:
    - multi_index: tuple of array_like, tuple of index arrays
    - dims: tuple of ints, shape of array into which indices are applied
    - mode: {'raise', 'wrap', 'clip'}, specifies how out-of-bounds indices are handled
    - order: {'C', 'F'}, index order
    
    Returns:
    ndarray: Array of flat indices
    """

# Index construction shortcuts
mgrid: MGridClass  # Dense multi-dimensional meshgrid
ogrid: OGridClass  # Open (sparse) multi-dimensional meshgrid  
r_: RClass        # Concatenate slices along first axis
c_: CClass        # Concatenate slices along second axis
s_: IndexExpression  # Convert slice objects to concatenation along first axis
```

## Usage Examples

### Creating and Reshaping Arrays

```python
import numpy as np

# Basic array creation
arr = np.array([1, 2, 3, 4, 5])
matrix = np.array([[1, 2, 3], [4, 5, 6]])

# Initialize arrays
zeros = np.zeros((3, 4))
ones = np.ones((2, 5))
identity = np.eye(3)

# Create ranges
range_arr = np.arange(0, 10, 2)  # [0, 2, 4, 6, 8] 
linear = np.linspace(0, 1, 5)    # [0, 0.25, 0.5, 0.75, 1]

# Reshape arrays
reshaped = matrix.reshape(6, 1)   # 6x1 column vector
flattened = matrix.ravel()        # 1D array [1, 2, 3, 4, 5, 6]
```

### Joining and Splitting Arrays

```python
import numpy as np

arr1 = np.array([1, 2, 3])
arr2 = np.array([4, 5, 6])

# Join arrays
concatenated = np.concatenate([arr1, arr2])  # [1, 2, 3, 4, 5, 6]
stacked = np.stack([arr1, arr2])             # [[1, 2, 3], [4, 5, 6]]
hstacked = np.hstack([arr1, arr2])           # [1, 2, 3, 4, 5, 6]

# Split arrays
arr = np.array([1, 2, 3, 4, 5, 6])
split_arrays = np.split(arr, 3)              # [array([1, 2]), array([3, 4]), array([5, 6])]
```