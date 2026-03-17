# Array Statistics and Aggregations

Statistical and reduction operations for analyzing array data. These functions compute summary statistics, perform aggregations along specified axes, and include NaN-aware versions for handling missing data.

## Capabilities

### Basic Statistical Functions

Fundamental statistical measures for array data.

```python { .api }
def sum(a, axis=None, dtype=None, out=None, keepdims=False, initial=None, where=True):
    """
    Sum of array elements over given axis.
    
    Parameters:
    - a: array_like, input array
    - axis: None or int or tuple of ints, axis to sum over
    - dtype: data-type, type of returned array and accumulator
    - out: ndarray, output array to place result
    - keepdims: bool, keep reduced dimensions as size 1
    - initial: scalar, starting value for sum
    - where: array_like of bool, elements to include in sum
    
    Returns:
    ndarray or scalar: Sum of array elements
    """

def prod(a, axis=None, dtype=None, out=None, keepdims=False, initial=None, where=True):
    """
    Return product of array elements over given axis.
    
    Parameters:
    - a: array_like, input array
    - axis: None or int or tuple of ints, axis to compute product over
    - dtype: data-type, type of returned array and accumulator
    - out: ndarray, output array to place result
    - keepdims: bool, keep reduced dimensions as size 1
    - initial: scalar, starting value for product
    - where: array_like of bool, elements to include in product
    
    Returns:
    ndarray or scalar: Product of array elements
    """

def mean(a, axis=None, dtype=None, out=None, keepdims=False, where=True):
    """
    Compute arithmetic mean along specified axis.
    
    Parameters:
    - a: array_like, input array
    - axis: None or int or tuple of ints, axis to compute mean over
    - dtype: data-type, type of returned array and accumulator
    - out: ndarray, output array to place result
    - keepdims: bool, keep reduced dimensions as size 1
    - where: array_like of bool, elements to include in mean
    
    Returns:
    ndarray or scalar: Arithmetic mean of array elements
    """

def std(a, axis=None, dtype=None, out=None, ddof=0, keepdims=False, where=True):
    """
    Compute standard deviation along specified axis.
    
    Parameters:
    - a: array_like, input array
    - axis: None or int or tuple of ints, axis to compute std over
    - dtype: data-type, type of returned array and accumulator
    - out: ndarray, output array to place result
    - ddof: int, delta degrees of freedom
    - keepdims: bool, keep reduced dimensions as size 1
    - where: array_like of bool, elements to include in std
    
    Returns:
    ndarray or scalar: Standard deviation of array elements
    """

def var(a, axis=None, dtype=None, out=None, ddof=0, keepdims=False, where=True):
    """
    Compute variance along specified axis.
    
    Parameters:
    - a: array_like, input array
    - axis: None or int or tuple of ints, axis to compute variance over
    - dtype: data-type, type of returned array and accumulator
    - out: ndarray, output array to place result
    - ddof: int, delta degrees of freedom
    - keepdims: bool, keep reduced dimensions as size 1
    - where: array_like of bool, elements to include in variance
    
    Returns:
    ndarray or scalar: Variance of array elements
    """
```

### Minimum and Maximum Functions

Find minimum and maximum values in arrays.

```python { .api }
def min(a, axis=None, out=None, keepdims=False, initial=None, where=True):
    """
    Return minimum of array or minimum along axis.
    
    Parameters:
    - a: array_like, input array
    - axis: None or int or tuple of ints, axis to find minimum over
    - out: ndarray, output array to place result
    - keepdims: bool, keep reduced dimensions as size 1
    - initial: scalar, maximum value of output element
    - where: array_like of bool, elements to compare for minimum
    
    Returns:
    ndarray or scalar: Minimum of array elements
    """

def max(a, axis=None, out=None, keepdims=False, initial=None, where=True):
    """
    Return maximum of array or maximum along axis.
    
    Parameters:
    - a: array_like, input array
    - axis: None or int or tuple of ints, axis to find maximum over
    - out: ndarray, output array to place result
    - keepdims: bool, keep reduced dimensions as size 1
    - initial: scalar, minimum value of output element
    - where: array_like of bool, elements to compare for maximum
    
    Returns:
    ndarray or scalar: Maximum of array elements
    """

def amin(a, axis=None, out=None, keepdims=False, initial=None, where=True):
    """
    Return minimum of array or minimum along axis.
    
    Parameters:
    - a: array_like, input array
    - axis: None or int or tuple of ints, axis to find minimum over
    - out: ndarray, output array to place result
    - keepdims: bool, keep reduced dimensions as size 1
    - initial: scalar, maximum value of output element
    - where: array_like of bool, elements to compare for minimum
    
    Returns:
    ndarray or scalar: Minimum of array elements
    """

def amax(a, axis=None, out=None, keepdims=False, initial=None, where=True):
    """
    Return maximum of array or maximum along axis.
    
    Parameters:
    - a: array_like, input array
    - axis: None or int or tuple of ints, axis to find maximum over
    - out: ndarray, output array to place result
    - keepdims: bool, keep reduced dimensions as size 1
    - initial: scalar, minimum value of output element
    - where: array_like of bool, elements to compare for maximum
    
    Returns:
    ndarray or scalar: Maximum of array elements
    """

def ptp(a, axis=None, out=None, keepdims=False):
    """
    Range of values (maximum - minimum) along axis.
    
    Parameters:
    - a: array_like, input array
    - axis: None or int or tuple of ints, axis along which to find range
    - out: ndarray, output array to place result
    - keepdims: bool, keep reduced dimensions as size 1
    
    Returns:
    ndarray or scalar: Range of array elements
    """
```

### Percentile and Quantile Functions

Statistical measures based on data distribution.

```python { .api }
def median(a, axis=None, out=None, overwrite_input=False, keepdims=False):
    """
    Compute median along specified axis.
    
    Parameters:
    - a: array_like, input array
    - axis: None or int or tuple of ints, axis to compute median over
    - out: ndarray, output array to place result
    - overwrite_input: bool, allow overwriting input array
    - keepdims: bool, keep reduced dimensions as size 1
    
    Returns:
    ndarray or scalar: Median of array elements
    """

def percentile(a, q, axis=None, out=None, overwrite_input=False, method='linear', keepdims=False):
    """
    Compute qth percentile along specified axis.
    
    Parameters:
    - a: array_like, input array
    - q: array_like of float, percentile(s) to compute (0-100)
    - axis: None or int or tuple of ints, axis to compute percentiles over
    - out: ndarray, output array to place result
    - overwrite_input: bool, allow overwriting input array
    - method: str, interpolation method
    - keepdims: bool, keep reduced dimensions as size 1
    
    Returns:
    ndarray or scalar: Percentile(s) of array elements
    """

def quantile(a, q, axis=None, out=None, overwrite_input=False, method='linear', keepdims=False):
    """
    Compute qth quantile along specified axis.
    
    Parameters:
    - a: array_like, input array
    - q: array_like of float, quantile(s) to compute (0-1)
    - axis: None or int or tuple of ints, axis to compute quantiles over
    - out: ndarray, output array to place result
    - overwrite_input: bool, allow overwriting input array
    - method: str, interpolation method
    - keepdims: bool, keep reduced dimensions as size 1
    
    Returns:
    ndarray or scalar: Quantile(s) of array elements
    """
```

### Logical Aggregation Functions

Boolean reduction operations.

```python { .api }
def all(a, axis=None, out=None, keepdims=False, where=True):
    """
    Test whether all array elements along axis evaluate to True.
    
    Parameters:
    - a: array_like, input array
    - axis: None or int or tuple of ints, axis to evaluate over
    - out: ndarray, output array to place result
    - keepdims: bool, keep reduced dimensions as size 1
    - where: array_like of bool, elements to include in evaluation
    
    Returns:
    ndarray or bool: True if all elements evaluate to True
    """

def any(a, axis=None, out=None, keepdims=False, where=True):
    """
    Test whether any array element along axis evaluates to True.
    
    Parameters:
    - a: array_like, input array
    - axis: None or int or tuple of ints, axis to evaluate over
    - out: ndarray, output array to place result
    - keepdims: bool, keep reduced dimensions as size 1
    - where: array_like of bool, elements to include in evaluation
    
    Returns:
    ndarray or bool: True if any element evaluates to True
    """

def count_nonzero(a, axis=None, keepdims=False):
    """
    Count number of nonzero values in array.
    
    Parameters:
    - a: array_like, input array
    - axis: None or int or tuple of ints, axis to count over
    - keepdims: bool, keep reduced dimensions as size 1
    
    Returns:
    ndarray or int: Number of nonzero values
    """
```

### Cumulative Functions

Cumulative operations along array axes.

```python { .api }
def cumsum(a, axis=None, dtype=None, out=None):
    """
    Return cumulative sum of elements along axis.
    
    Parameters:
    - a: array_like, input array
    - axis: int, axis along which cumulative sum is computed
    - dtype: data-type, type of returned array
    - out: ndarray, output array to place result
    
    Returns:
    ndarray: Cumulative sum along specified axis
    """

def cumprod(a, axis=None, dtype=None, out=None):
    """
    Return cumulative product of elements along axis.
    
    Parameters:
    - a: array_like, input array
    - axis: int, axis along which cumulative product is computed
    - dtype: data-type, type of returned array
    - out: ndarray, output array to place result
    
    Returns:
    ndarray: Cumulative product along specified axis
    """

def cumulative_sum(a, axis=None, dtype=None, out=None):
    """
    Return cumulative sum of elements along axis.
    
    Parameters:
    - a: array_like, input array
    - axis: int, axis along which cumulative sum is computed
    - dtype: data-type, type of returned array
    - out: ndarray, output array to place result
    
    Returns:
    ndarray: Cumulative sum along specified axis
    """

def cumulative_prod(a, axis=None, dtype=None, out=None):
    """
    Return cumulative product of elements along axis.
    
    Parameters:
    - a: array_like, input array
    - axis: int, axis along which cumulative product is computed
    - dtype: data-type, type of returned array
    - out: ndarray, output array to place result
    
    Returns:
    ndarray: Cumulative product along specified axis
    """
```

### NaN-aware Statistical Functions

Statistical functions that handle NaN values appropriately.

```python { .api }
def nansum(a, axis=None, dtype=None, out=None, keepdims=False, where=True):
    """
    Return sum of array elements over given axis treating NaNs as zero.
    
    Parameters:
    - a: array_like, input array
    - axis: None or int or tuple of ints, axis to sum over
    - dtype: data-type, type of returned array and accumulator
    - out: ndarray, output array to place result
    - keepdims: bool, keep reduced dimensions as size 1
    - where: array_like of bool, elements to include in sum
    
    Returns:
    ndarray or scalar: Sum ignoring NaN values
    """

def nanprod(a, axis=None, dtype=None, out=None, keepdims=False, where=True):
    """
    Return product of array elements over given axis treating NaNs as one.
    
    Parameters:
    - a: array_like, input array
    - axis: None or int or tuple of ints, axis to compute product over
    - dtype: data-type, type of returned array and accumulator
    - out: ndarray, output array to place result
    - keepdims: bool, keep reduced dimensions as size 1
    - where: array_like of bool, elements to include in product
    
    Returns:
    ndarray or scalar: Product ignoring NaN values
    """

def nanmean(a, axis=None, dtype=None, out=None, keepdims=False, where=True):
    """
    Compute arithmetic mean along specified axis, ignoring NaNs.
    
    Parameters:
    - a: array_like, input array
    - axis: None or int or tuple of ints, axis to compute mean over
    - dtype: data-type, type of returned array and accumulator
    - out: ndarray, output array to place result
    - keepdims: bool, keep reduced dimensions as size 1
    - where: array_like of bool, elements to include in mean
    
    Returns:
    ndarray or scalar: Mean ignoring NaN values
    """

def nanstd(a, axis=None, dtype=None, out=None, ddof=0, keepdims=False, where=True):
    """
    Compute standard deviation along specified axis, ignoring NaNs.
    
    Parameters:
    - a: array_like, input array
    - axis: None or int or tuple of ints, axis to compute std over
    - dtype: data-type, type of returned array and accumulator
    - out: ndarray, output array to place result
    - ddof: int, delta degrees of freedom
    - keepdims: bool, keep reduced dimensions as size 1
    - where: array_like of bool, elements to include in std
    
    Returns:
    ndarray or scalar: Standard deviation ignoring NaN values
    """

def nanvar(a, axis=None, dtype=None, out=None, ddof=0, keepdims=False, where=True):
    """
    Compute variance along specified axis, ignoring NaNs.
    
    Parameters:
    - a: array_like, input array
    - axis: None or int or tuple of ints, axis to compute variance over
    - dtype: data-type, type of returned array and accumulator
    - out: ndarray, output array to place result
    - ddof: int, delta degrees of freedom
    - keepdims: bool, keep reduced dimensions as size 1
    - where: array_like of bool, elements to include in variance
    
    Returns:
    ndarray or scalar: Variance ignoring NaN values
    """

def nanmin(a, axis=None, out=None, keepdims=False, initial=None, where=True):
    """
    Return minimum of array or minimum along axis, ignoring NaNs.
    
    Parameters:
    - a: array_like, input array
    - axis: None or int or tuple of ints, axis to find minimum over
    - out: ndarray, output array to place result
    - keepdims: bool, keep reduced dimensions as size 1
    - initial: scalar, maximum value of output element
    - where: array_like of bool, elements to compare for minimum
    
    Returns:
    ndarray or scalar: Minimum ignoring NaN values
    """

def nanmax(a, axis=None, out=None, keepdims=False, initial=None, where=True):
    """
    Return maximum of array or maximum along axis, ignoring NaNs.
    
    Parameters:
    - a: array_like, input array
    - axis: None or int or tuple of ints, axis to find maximum over
    - out: ndarray, output array to place result
    - keepdims: bool, keep reduced dimensions as size 1
    - initial: scalar, minimum value of output element
    - where: array_like of bool, elements to compare for maximum
    
    Returns:
    ndarray or scalar: Maximum ignoring NaN values
    """

def nanmedian(a, axis=None, out=None, overwrite_input=False, keepdims=False):
    """
    Compute median along specified axis, ignoring NaNs.
    
    Parameters:
    - a: array_like, input array
    - axis: None or int or tuple of ints, axis to compute median over
    - out: ndarray, output array to place result
    - overwrite_input: bool, allow overwriting input array
    - keepdims: bool, keep reduced dimensions as size 1
    
    Returns:
    ndarray or scalar: Median ignoring NaN values
    """

def nanpercentile(a, q, axis=None, out=None, overwrite_input=False, method='linear', keepdims=False):
    """
    Compute qth percentile along specified axis, ignoring NaNs.
    
    Parameters:
    - a: array_like, input array
    - q: array_like of float, percentile(s) to compute (0-100)
    - axis: None or int or tuple of ints, axis to compute percentiles over
    - out: ndarray, output array to place result
    - overwrite_input: bool, allow overwriting input array
    - method: str, interpolation method
    - keepdims: bool, keep reduced dimensions as size 1
    
    Returns:
    ndarray or scalar: Percentile(s) ignoring NaN values
    """

def nanquantile(a, q, axis=None, out=None, overwrite_input=False, method='linear', keepdims=False):
    """
    Compute qth quantile along specified axis, ignoring NaNs.
    
    Parameters:
    - a: array_like, input array
    - q: array_like of float, quantile(s) to compute (0-1)
    - axis: None or int or tuple of ints, axis to compute quantiles over
    - out: ndarray, output array to place result
    - overwrite_input: bool, allow overwriting input array
    - method: str, interpolation method
    - keepdims: bool, keep reduced dimensions as size 1
    
    Returns:
    ndarray or scalar: Quantile(s) ignoring NaN values
    """

def nancumsum(a, axis=None, dtype=None, out=None):
    """
    Return cumulative sum along axis, treating NaNs as zero.
    
    Parameters:
    - a: array_like, input array
    - axis: int, axis along which cumulative sum is computed
    - dtype: data-type, type of returned array
    - out: ndarray, output array to place result
    
    Returns:
    ndarray: Cumulative sum ignoring NaN values
    """

def nancumprod(a, axis=None, dtype=None, out=None):
    """
    Return cumulative product along axis, treating NaNs as one.
    
    Parameters:
    - a: array_like, input array
    - axis: int, axis along which cumulative product is computed
    - dtype: data-type, type of returned array
    - out: ndarray, output array to place result
    
    Returns:
    ndarray: Cumulative product ignoring NaN values
    """
```

## Usage Examples

### Basic Statistics

```python
import numpy as np

# Sample data
data = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])

# Basic statistics
total_sum = np.sum(data)          # 45
mean_val = np.mean(data)          # 5.0
std_val = np.std(data)            # 2.58
min_val = np.min(data)            # 1
max_val = np.max(data)            # 9

# Along specific axes
row_sums = np.sum(data, axis=1)   # [6, 15, 24]
col_means = np.mean(data, axis=0) # [4.0, 5.0, 6.0]
```

### Percentiles and Quantiles

```python
import numpy as np

data = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])

# Percentiles
median = np.median(data)               # 5.5
q25 = np.percentile(data, 25)         # 3.25
q75 = np.percentile(data, 75)         # 7.75

# Multiple percentiles
quartiles = np.percentile(data, [25, 50, 75])  # [3.25, 5.5, 7.75]
```

### Handling NaN Values

```python
import numpy as np

# Data with NaN values
data_with_nan = np.array([1, 2, np.nan, 4, 5, np.nan])

# Regular functions return NaN
regular_mean = np.mean(data_with_nan)    # nan
regular_sum = np.sum(data_with_nan)      # nan

# NaN-aware functions ignore NaN
nan_mean = np.nanmean(data_with_nan)     # 3.0
nan_sum = np.nansum(data_with_nan)       # 12.0
nan_max = np.nanmax(data_with_nan)       # 5.0
```

### Cumulative Operations

```python
import numpy as np

arr = np.array([1, 2, 3, 4, 5])

# Cumulative operations
cumsum = np.cumsum(arr)    # [1, 3, 6, 10, 15]
cumprod = np.cumprod(arr)  # [1, 2, 6, 24, 120]

# Along specific axis for multi-dimensional arrays
matrix = np.array([[1, 2], [3, 4]])
cumsum_axis0 = np.cumsum(matrix, axis=0)  # [[1, 2], [4, 6]]
cumsum_axis1 = np.cumsum(matrix, axis=1)  # [[1, 3], [3, 7]]
```