# Array Searching and Sorting

Functions for finding, sorting, and organizing array elements. Includes search operations, sorting algorithms, and set operations for array analysis and data organization.

## Capabilities

### Searching Functions

Find elements and their positions in arrays.

```python { .api }
def where(condition, x=None, y=None):
    """
    Return elements chosen from x or y depending on condition.
    
    Parameters:
    - condition: array_like, bool, condition to evaluate
    - x, y: array_like, values to choose from
    
    Returns:
    ndarray or tuple: Indices or selected elements
    """

def argwhere(a):
    """
    Find indices of non-zero elements.
    
    Parameters:
    - a: array_like, input array
    
    Returns:
    ndarray: Indices of non-zero elements
    """

def nonzero(a):
    """
    Return indices of non-zero elements.
    
    Parameters:
    - a: array_like, input array
    
    Returns:
    tuple of arrays: Indices of non-zero elements
    """

def argmax(a, axis=None, out=None, keepdims=False):
    """
    Return indices of maximum values along axis.
    
    Parameters:
    - a: array_like, input array
    - axis: int, axis along which to search
    - out: array, output array
    - keepdims: bool, keep reduced dimensions
    
    Returns:
    ndarray: Indices of maximum values
    """

def argmin(a, axis=None, out=None, keepdims=False):
    """
    Return indices of minimum values along axis.
    
    Parameters:
    - a: array_like, input array
    - axis: int, axis along which to search
    - out: array, output array
    - keepdims: bool, keep reduced dimensions
    
    Returns:
    ndarray: Indices of minimum values
    """

def searchsorted(a, v, side='left', sorter=None):
    """
    Find indices where elements should be inserted to maintain order.
    
    Parameters:
    - a: array_like, sorted input array
    - v: array_like, values to insert
    - side: {'left', 'right'}, insertion side
    - sorter: array_like, optional sorting indices
    
    Returns:
    ndarray: Insertion indices
    """
```

### Sorting Functions

Sort array elements using various algorithms.

```python { .api }
def sort(a, axis=-1, kind=None, order=None, stable=None):
    """
    Return a sorted copy of an array.
    
    Parameters:
    - a: array_like, array to sort
    - axis: int, axis to sort along
    - kind: {'quicksort', 'mergesort', 'heapsort', 'stable'}, sorting algorithm
    - order: str or list of str, field order for structured arrays
    - stable: bool, stable sorting
    
    Returns:
    ndarray: Sorted array
    """

def argsort(a, axis=-1, kind=None, order=None, stable=None):
    """
    Return indices that would sort an array.
    
    Parameters:
    - a: array_like, array to sort
    - axis: int, axis to sort along
    - kind: {'quicksort', 'mergesort', 'heapsort', 'stable'}, sorting algorithm
    - order: str or list of str, field order for structured arrays
    - stable: bool, stable sorting
    
    Returns:
    ndarray: Indices for sorting
    """

def partition(a, kth, axis=-1, kind='introselect', order=None):
    """
    Return a partitioned copy of an array.
    
    Parameters:
    - a: array_like, array to partition
    - kth: int or sequence of ints, element index to partition around
    - axis: int, axis to partition along
    - kind: {'introselect'}, selection algorithm
    - order: str or list of str, field order for structured arrays
    
    Returns:
    ndarray: Partitioned array
    """

def argpartition(a, kth, axis=-1, kind='introselect', order=None):
    """
    Return indices that would partition an array.
    
    Parameters:
    - a: array_like, array to partition
    - kth: int or sequence of ints, element index to partition around
    - axis: int, axis to partition along
    - kind: {'introselect'}, selection algorithm
    - order: str or list of str, field order for structured arrays
    
    Returns:
    ndarray: Indices for partitioning
    """

def lexsort(keys, axis=-1):
    """
    Perform indirect stable sort using sequence of keys.
    
    Parameters:
    - keys: sequence of array_like, sorting keys
    - axis: int, axis to sort along
    
    Returns:
    ndarray: Indices for lexicographic sorting
    """
```

### Set Operations

Set-like operations on arrays.

```python { .api }
def unique(ar, return_index=False, return_inverse=False, return_counts=False, axis=None, equal_nan=True):
    """
    Find unique elements of an array.
    
    Parameters:
    - ar: array_like, input array
    - return_index: bool, return indices of unique elements
    - return_inverse: bool, return indices to reconstruct input
    - return_counts: bool, return counts of unique elements
    - axis: int, axis to operate along
    - equal_nan: bool, treat NaN values as equal
    
    Returns:
    ndarray or tuple: Unique elements and optional extra arrays
    """

def in1d(ar1, ar2, assume_unique=False, invert=False, kind=None):
    """
    Test whether elements of 1-D array are in second array.
    
    Parameters:
    - ar1, ar2: array_like, input arrays
    - assume_unique: bool, assume input arrays contain unique elements
    - invert: bool, invert boolean result
    - kind: {None, 'sort', 'table'}, algorithm to use
    
    Returns:
    ndarray: Boolean array of same shape as ar1
    """

def isin(element, test_elements, assume_unique=False, invert=False, kind=None):
    """
    Calculates element in test_elements, broadcasting over element only.
    
    Parameters:
    - element: array_like, input array
    - test_elements: array_like, values against which to test
    - assume_unique: bool, assume test_elements contains unique elements
    - invert: bool, invert boolean result
    - kind: {None, 'sort', 'table'}, algorithm to use
    
    Returns:
    ndarray: Boolean array of same shape as element
    """

def intersect1d(ar1, ar2, assume_unique=False, return_indices=False):
    """
    Find intersection of two arrays.
    
    Parameters:
    - ar1, ar2: array_like, input arrays
    - assume_unique: bool, assume input arrays are unique
    - return_indices: bool, return indices of intersection
    
    Returns:
    ndarray or tuple: Intersection and optional indices
    """

def union1d(ar1, ar2):
    """
    Find union of two arrays.
    
    Parameters:
    - ar1, ar2: array_like, input arrays
    
    Returns:
    ndarray: Unique, sorted union of input arrays
    """

def setdiff1d(ar1, ar2, assume_unique=False):
    """
    Find set difference of two arrays.
    
    Parameters:
    - ar1, ar2: array_like, input arrays
    - assume_unique: bool, assume input arrays are unique
    
    Returns:
    ndarray: Unique values in ar1 not in ar2
    """

def setxor1d(ar1, ar2, assume_unique=False):
    """
    Find set exclusive-or of two arrays.
    
    Parameters:
    - ar1, ar2: array_like, input arrays
    - assume_unique: bool, assume input arrays are unique
    
    Returns:
    ndarray: Unique values in either ar1 or ar2 but not both
    """
```

## Usage Examples

### Searching Arrays

```python
import numpy as np

# Sample data
data = np.array([3, 1, 4, 1, 5, 9, 2, 6])

# Find indices of elements
max_idx = np.argmax(data)        # 5 (index of maximum value 9)
min_idx = np.argmin(data)        # 1 (index of minimum value 1)

# Find where condition is true
large_indices = np.where(data > 4)  # (array([4, 5, 7]),)
large_values = data[data > 4]       # [5, 9, 6]

# Non-zero elements
arr_with_zeros = np.array([0, 1, 0, 3, 0, 5])
nonzero_indices = np.nonzero(arr_with_zeros)  # (array([1, 3, 5]),)
```

### Sorting Operations

```python
import numpy as np

data = np.array([3, 1, 4, 1, 5, 9, 2, 6])

# Sort array
sorted_data = np.sort(data)       # [1, 1, 2, 3, 4, 5, 6, 9]

# Get indices for sorting
sort_indices = np.argsort(data)   # [1, 3, 6, 0, 2, 4, 7, 5]
manually_sorted = data[sort_indices]  # Same as sorted_data

# Partial sorting with partition
partitioned = np.partition(data, 3)  # Elements 0-3 are <= element at index 3
```

### Set Operations

```python
import numpy as np

arr1 = np.array([1, 2, 3, 4, 5])
arr2 = np.array([3, 4, 5, 6, 7])

# Unique elements
unique_vals = np.unique([1, 1, 2, 2, 3, 3])  # [1, 2, 3]

# Set operations
intersection = np.intersect1d(arr1, arr2)     # [3, 4, 5]
union = np.union1d(arr1, arr2)               # [1, 2, 3, 4, 5, 6, 7]
difference = np.setdiff1d(arr1, arr2)        # [1, 2]
symmetric_diff = np.setxor1d(arr1, arr2)     # [1, 2, 6, 7]

# Membership testing
is_member = np.isin(arr1, arr2)              # [False, False, True, True, True]
```