# Masked Arrays

Arrays that can contain invalid or missing data. Masked arrays suppress invalid values during operations, allowing for robust statistical and mathematical computations on datasets with missing or undefined values.

## Capabilities

### Core Masked Array Classes

Main classes for creating and working with masked arrays that handle missing or invalid data.

```python { .api }
class MaskedArray:
    """N-dimensional array with masked values."""
    def __init__(self, data, mask=False, dtype=None, **kwargs): ...
    def __array__(self, dtype=None): ...
    def __getitem__(self, indx): ...
    def __setitem__(self, indx, value): ...
    def filled(self, fill_value=None): ...
    def compressed(self): ...
    def count(self, axis=None, keepdims=False): ...
    def sum(self, axis=None, **kwargs): ...
    def mean(self, axis=None, **kwargs): ...
    def std(self, axis=None, **kwargs): ...
    def var(self, axis=None, **kwargs): ...
    def min(self, axis=None, **kwargs): ...
    def max(self, axis=None, **kwargs): ...
    @property
    def mask(self): ...
    @property
    def data(self): ...
    @property
    def fill_value(self): ...

def masked_array(data, mask=False, dtype=None, **kwargs):
    """
    An array class with possibly masked values.
    
    Parameters:
    - data: array_like, input data
    - mask: sequence, condition to mask invalid entries
    - dtype: dtype, desired data type
    - fill_value: scalar, value used to fill masked array
    
    Returns:
    MaskedArray: Masked array object
    """

def array(data, dtype=None, **kwargs):
    """
    Shortcut to MaskedArray constructor.
    
    Parameters:
    - data: array_like, input data
    - dtype: dtype, desired data type
    
    Returns:
    MaskedArray: Masked array object
    """
```

### Mask Creation Functions

Functions for creating and manipulating masks to identify invalid or missing data.

```python { .api }
def make_mask(m, copy=False, shrink=True, dtype=None):
    """
    Create a boolean mask from an array.
    
    Parameters:
    - m: array_like, potential mask
    - copy: bool, whether to copy the mask
    - shrink: bool, whether to shrink mask to nomask if no values masked
    - dtype: dtype, data type of mask
    
    Returns:
    ndarray or nomask: Boolean mask array
    """

def mask_or(m1, m2, copy=False, shrink=True):
    """
    Combine two masks with the logical_or operator.
    
    Parameters:
    - m1, m2: array_like, input masks
    - copy: bool, whether to copy result
    - shrink: bool, whether to shrink result
    
    Returns:
    ndarray or nomask: Combined mask
    """

def mask_and(m1, m2, copy=False, shrink=True):
    """
    Combine two masks with the logical_and operator.
    
    Parameters:
    - m1, m2: array_like, input masks
    - copy: bool, whether to copy result
    - shrink: bool, whether to shrink result
    
    Returns:
    ndarray or nomask: Combined mask
    """

def masked_where(condition, a, copy=True):
    """
    Mask an array where a condition is met.
    
    Parameters:
    - condition: array_like, masking condition
    - a: array_like, array to mask
    - copy: bool, whether to copy array
    
    Returns:
    MaskedArray: Masked version of array
    """

def masked_invalid(a, copy=True):
    """
    Mask an array where invalid values occur (NaNs or infs).
    
    Parameters:
    - a: array_like, array to mask
    - copy: bool, whether to copy array
    
    Returns:
    MaskedArray: Masked array with invalid values masked
    """

def masked_equal(x, value, copy=True):
    """
    Mask an array where equal to a given value.
    
    Parameters:
    - x: array_like, array to mask
    - value: scalar, value to mask
    - copy: bool, whether to copy array
    
    Returns:
    MaskedArray: Masked array
    """

def masked_not_equal(x, value, copy=True):
    """
    Mask an array where not equal to a given value.
    
    Parameters:
    - x: array_like, array to mask  
    - value: scalar, comparison value
    - copy: bool, whether to copy array
    
    Returns:
    MaskedArray: Masked array
    """

def masked_less(x, value, copy=True):
    """
    Mask an array where less than a given value.
    
    Parameters:
    - x: array_like, array to mask
    - value: scalar, comparison value
    - copy: bool, whether to copy array
    
    Returns:
    MaskedArray: Masked array
    """

def masked_greater(x, value, copy=True):
    """
    Mask an array where greater than a given value.
    
    Parameters:
    - x: array_like, array to mask
    - value: scalar, comparison value  
    - copy: bool, whether to copy array
    
    Returns:
    MaskedArray: Masked array
    """

def masked_inside(x, v1, v2, copy=True):
    """
    Mask an array inside a given interval.
    
    Parameters:
    - x: array_like, array to mask
    - v1, v2: scalar, interval endpoints
    - copy: bool, whether to copy array
    
    Returns:
    MaskedArray: Masked array
    """

def masked_outside(x, v1, v2, copy=True):
    """
    Mask an array outside a given interval.
    
    Parameters:
    - x: array_like, array to mask
    - v1, v2: scalar, interval endpoints
    - copy: bool, whether to copy array
    
    Returns:
    MaskedArray: Masked array
    """
```

### Operations on Masked Arrays

Statistical and mathematical operations that properly handle masked data.

```python { .api }
def count(a, axis=None, keepdims=False):
    """
    Count the non-masked elements of the array along the given axis.
    
    Parameters:
    - a: array_like, input data
    - axis: None or int or tuple, axis along which to count
    - keepdims: bool, whether to keep dimensions
    
    Returns:
    ndarray: Number of non-masked elements
    """

def sum(a, axis=None, **kwargs):
    """Sum of array elements over a given axis, ignoring masked values."""

def mean(a, axis=None, **kwargs): 
    """Compute the arithmetic mean along the specified axis, ignoring masked values."""

def std(a, axis=None, **kwargs):
    """Compute the standard deviation along the specified axis, ignoring masked values."""

def var(a, axis=None, **kwargs):
    """Compute the variance along the specified axis, ignoring masked values."""

def min(a, axis=None, **kwargs):
    """Return the minimum along a given axis, ignoring masked values."""

def max(a, axis=None, **kwargs):
    """Return the maximum along a given axis, ignoring masked values."""

def compressed(x):
    """
    Return all the non-masked data as a 1-D array.
    
    Parameters:
    - x: MaskedArray, input array
    
    Returns:
    ndarray: Compressed array with only non-masked values
    """

def filled(a, fill_value=None):
    """
    Return input as an array with masked data replaced by a fill value.
    
    Parameters:
    - a: MaskedArray, input array
    - fill_value: scalar, value to use for masked entries
    
    Returns:
    ndarray: Filled array
    """
```

### Mask Manipulation

Functions for working with and modifying masks.

```python { .api }
def getmask(a):
    """
    Return the mask of a masked array, or nomask.
    
    Parameters:
    - a: array_like, input array
    
    Returns:
    ndarray or nomask: Mask array
    """

def getmaskarray(arr):
    """
    Return the mask of a masked array, or full boolean array of False.
    
    Parameters:
    - arr: array_like, input array
    
    Returns:
    ndarray: Mask array
    """

def is_mask(m):
    """
    Return True if m is a valid, standard mask.
    
    Parameters:
    - m: array_like, array to test
    
    Returns:
    bool: Whether array is a valid mask
    """

def is_masked(x):
    """
    Determine whether input has masked values.
    
    Parameters:
    - x: array_like, array to test
    
    Returns:
    bool: Whether array has masked values
    """

def isMA(x):
    """
    Test whether input is an instance of MaskedArray.
    
    Parameters:
    - x: object, object to test
    
    Returns:
    bool: Whether object is MaskedArray
    """
```

## Usage Examples

### Basic Masked Array Operations

```python
import numpy as np
import numpy.ma as ma

# Create array with missing values
data = [1, 2, np.nan, 4, 5]
masked_data = ma.masked_invalid(data)
print(masked_data)
# masked_array(data=[1.0, 2.0, --, 4.0, 5.0], mask=[False, False, True, False, False])

# Calculate statistics ignoring masked values
print(ma.mean(masked_data))  # 3.0
print(ma.std(masked_data))   # 1.58...

# Get non-masked data
print(masked_data.compressed())  # [1. 2. 4. 5.]
```

### Creating Custom Masks

```python
import numpy as np
import numpy.ma as ma

# Create masked array with custom conditions
data = np.array([1, 2, 3, 4, 5, 6])
masked_data = ma.masked_where(data > 3, data)
print(masked_data)
# masked_array(data=[1, 2, 3, --, --, --], mask=[False, False, False, True, True, True])

# Combine masks
mask1 = data < 2
mask2 = data > 5  
combined_mask = ma.mask_or(mask1, mask2)
result = ma.array(data, mask=combined_mask)
print(result)
# masked_array(data=[--, 2, 3, 4, 5, --], mask=[True, False, False, False, False, True])
```

### Fill Missing Values

```python
import numpy as np
import numpy.ma as ma

# Create masked array and fill missing values
data = ma.array([1, 2, 3, 4], mask=[0, 0, 1, 0])
filled = data.filled(fill_value=-999)
print(filled)  # [1 2 -999 4]

# Use different fill values
data.fill_value = 0
print(data.filled())  # [1 2 0 4]
```