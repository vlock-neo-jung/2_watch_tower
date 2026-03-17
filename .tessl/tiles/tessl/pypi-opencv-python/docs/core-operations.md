# Core Operations

Core operations in OpenCV provide fundamental array manipulation, mathematical operations, and linear algebra capabilities that form the foundation for image processing and computer vision tasks. These operations work on multi-dimensional arrays (Mat objects) and include arithmetic, logical, statistical, and transformation functions.

## Capabilities

### Arithmetic Operations

Element-wise arithmetic operations on arrays with support for saturation arithmetic, masking, and multiple data types.

#### Addition

```python { .api }
cv2.add(src1, src2, dst=None, mask=None, dtype=None) -> dst
```

Calculates the per-element sum of two arrays or an array and a scalar.

**Parameters:**

- `src1` (ndarray): First input array or scalar
- `src2` (ndarray): Second input array or scalar
- `dst` (ndarray, optional): Output array of the same size and type as input arrays
- `mask` (ndarray, optional): Optional operation mask, 8-bit single channel array
- `dtype` (int, optional): Optional depth of the output array

**Returns:**

- `dst` (ndarray): Output array

#### Subtraction

```python { .api }
cv2.subtract(src1, src2, dst=None, mask=None, dtype=None) -> dst
```

Calculates the per-element difference between two arrays or an array and a scalar.

**Parameters:**

- `src1` (ndarray): First input array or scalar
- `src2` (ndarray): Second input array or scalar
- `dst` (ndarray, optional): Output array of the same size and type as input arrays
- `mask` (ndarray, optional): Optional operation mask, 8-bit single channel array
- `dtype` (int, optional): Optional depth of the output array

**Returns:**

- `dst` (ndarray): Output array

#### Multiplication

```python { .api }
cv2.multiply(src1, src2, dst=None, scale=1.0, dtype=None) -> dst
```

Calculates the per-element scaled product of two arrays.

**Parameters:**

- `src1` (ndarray): First input array
- `src2` (ndarray): Second input array
- `dst` (ndarray, optional): Output array of the same size and type as input arrays
- `scale` (float, optional): Optional scale factor
- `dtype` (int, optional): Optional depth of the output array

**Returns:**

- `dst` (ndarray): Output array

#### Division

```python { .api }
cv2.divide(src1, src2, dst=None, scale=1.0, dtype=None) -> dst
```

Performs per-element division of two arrays or a scalar by an array.

**Parameters:**

- `src1` (ndarray): First input array (dividend)
- `src2` (ndarray): Second input array (divisor)
- `dst` (ndarray, optional): Output array of the same size and type as input arrays
- `scale` (float, optional): Optional scale factor
- `dtype` (int, optional): Optional depth of the output array

**Returns:**

- `dst` (ndarray): Output array

#### Absolute Difference

```python { .api }
cv2.absdiff(src1, src2, dst=None) -> dst
```

Calculates the per-element absolute difference between two arrays or between an array and a scalar.

**Parameters:**

- `src1` (ndarray): First input array or scalar
- `src2` (ndarray): Second input array or scalar
- `dst` (ndarray, optional): Output array

**Returns:**

- `dst` (ndarray): Output array of the same size and type as input arrays

#### Weighted Addition

```python { .api }
cv2.addWeighted(src1, alpha, src2, beta, gamma, dst=None, dtype=None) -> dst
```

Calculates the weighted sum of two arrays: dst = src1 * alpha + src2 * beta + gamma.

**Parameters:**

- `src1` (ndarray): First input array
- `alpha` (float): Weight of the first array elements
- `src2` (ndarray): Second input array of the same size and channel number as src1
- `beta` (float): Weight of the second array elements
- `gamma` (float): Scalar added to each sum
- `dst` (ndarray, optional): Output array
- `dtype` (int, optional): Optional depth of the output array

**Returns:**

- `dst` (ndarray): Output array

### Logical Operations

Bitwise logical operations on arrays, commonly used for masking and binary image manipulation.

#### Bitwise AND

```python { .api }
cv2.bitwise_and(src1, src2, dst=None, mask=None) -> dst
```

Calculates the per-element bit-wise conjunction of two arrays or an array and a scalar.

**Parameters:**

- `src1` (ndarray): First input array or scalar
- `src2` (ndarray): Second input array or scalar
- `dst` (ndarray, optional): Output array
- `mask` (ndarray, optional): Optional operation mask, 8-bit single channel array

**Returns:**

- `dst` (ndarray): Output array

#### Bitwise OR

```python { .api }
cv2.bitwise_or(src1, src2, dst=None, mask=None) -> dst
```

Calculates the per-element bit-wise disjunction of two arrays or an array and a scalar.

**Parameters:**

- `src1` (ndarray): First input array or scalar
- `src2` (ndarray): Second input array or scalar
- `dst` (ndarray, optional): Output array
- `mask` (ndarray, optional): Optional operation mask, 8-bit single channel array

**Returns:**

- `dst` (ndarray): Output array

#### Bitwise XOR

```python { .api }
cv2.bitwise_xor(src1, src2, dst=None, mask=None) -> dst
```

Calculates the per-element bit-wise "exclusive or" operation on two arrays or an array and a scalar.

**Parameters:**

- `src1` (ndarray): First input array or scalar
- `src2` (ndarray): Second input array or scalar
- `dst` (ndarray, optional): Output array
- `mask` (ndarray, optional): Optional operation mask, 8-bit single channel array

**Returns:**

- `dst` (ndarray): Output array

#### Bitwise NOT

```python { .api }
cv2.bitwise_not(src, dst=None, mask=None) -> dst
```

Inverts every bit of an array.

**Parameters:**

- `src` (ndarray): Input array
- `dst` (ndarray, optional): Output array
- `mask` (ndarray, optional): Optional operation mask, 8-bit single channel array

**Returns:**

- `dst` (ndarray): Output array

### Mathematical Operations

Element-wise mathematical functions for arrays including square root, power, exponential, and logarithm.

#### Square Root

```python { .api }
cv2.sqrt(src, dst=None) -> dst
```

Calculates a square root of array elements.

**Parameters:**

- `src` (ndarray): Input floating-point array
- `dst` (ndarray, optional): Output array of the same size and type as src

**Returns:**

- `dst` (ndarray): Output array containing square roots of input elements

#### Power

```python { .api }
cv2.pow(src, power, dst=None) -> dst
```

Raises every array element to a power.

**Parameters:**

- `src` (ndarray): Input array
- `power` (float): Exponent of power
- `dst` (ndarray, optional): Output array of the same size and type as src

**Returns:**

- `dst` (ndarray): Output array with each element raised to the specified power

#### Exponential

```python { .api }
cv2.exp(src, dst=None) -> dst
```

Calculates the exponent of every array element.

**Parameters:**

- `src` (ndarray): Input array
- `dst` (ndarray, optional): Output array of the same size and type as src

**Returns:**

- `dst` (ndarray): Output array where dst[I] = e^(src(I))

#### Logarithm

```python { .api }
cv2.log(src, dst=None) -> dst
```

Calculates the natural logarithm of every array element.

**Parameters:**

- `src` (ndarray): Input array
- `dst` (ndarray, optional): Output array of the same size and type as src

**Returns:**

- `dst` (ndarray): Output array where dst(I) = log(src(I)). Output on zero, negative and special (NaN, Inf) values is undefined

#### Magnitude

```python { .api }
cv2.magnitude(x, y, magnitude=None) -> magnitude
```

Calculates the magnitude of 2D vectors.

**Parameters:**

- `x` (ndarray): Floating-point array of x-coordinates of the vectors
- `y` (ndarray): Floating-point array of y-coordinates of the vectors (same size as x)
- `magnitude` (ndarray, optional): Output array of the same size and type as x

**Returns:**

- `magnitude` (ndarray): Output array where magnitude(I) = sqrt(x(I)^2 + y(I)^2)

#### Phase

```python { .api }
cv2.phase(x, y, angle=None, angleInDegrees=False) -> angle
```

Calculates the rotation angle of 2D vectors.

**Parameters:**

- `x` (ndarray): Floating-point array of x-coordinates of the vectors
- `y` (ndarray): Floating-point array of y-coordinates of the vectors (same size as x)
- `angle` (ndarray, optional): Output array of angles (in radians or degrees)
- `angleInDegrees` (bool): When true, the function calculates the angle in degrees, otherwise in radians

**Returns:**

- `angle` (ndarray): Output array of vector angles

#### Cartesian to Polar Coordinates

```python { .api }
cv2.cartToPolar(x, y, magnitude=None, angle=None, angleInDegrees=False) -> magnitude, angle
```

Calculates the magnitude and angle of 2D vectors.

**Parameters:**

- `x` (ndarray): Array of x-coordinates (must be single-precision or double-precision floating-point)
- `y` (ndarray): Array of y-coordinates (same size and type as x)
- `magnitude` (ndarray, optional): Output array of magnitudes
- `angle` (ndarray, optional): Output array of angles (in radians or degrees)
- `angleInDegrees` (bool): When true, the angles are measured in degrees (0-360), otherwise in radians (0-2*pi)

**Returns:**

- `magnitude` (ndarray): Output array of magnitudes
- `angle` (ndarray): Output array of angles

#### Polar to Cartesian Coordinates

```python { .api }
cv2.polarToCart(magnitude, angle, x=None, y=None, angleInDegrees=False) -> x, y
```

Calculates x and y coordinates of 2D vectors from their magnitude and angle.

**Parameters:**

- `magnitude` (ndarray): Input array of magnitudes (floating-point)
- `angle` (ndarray): Input array of angles (in radians or degrees)
- `x` (ndarray, optional): Output array of x-coordinates (same size and type as magnitude)
- `y` (ndarray, optional): Output array of y-coordinates (same size and type as magnitude)
- `angleInDegrees` (bool): When true, the input angles are measured in degrees, otherwise in radians

**Returns:**

- `x` (ndarray): Output array of x-coordinates
- `y` (ndarray): Output array of y-coordinates

#### Scaled Addition

```python { .api }
cv2.scaleAdd(src1, alpha, src2, dst=None) -> dst
```

Calculates the sum of a scaled array and another array.

**Parameters:**

- `src1` (ndarray): First input array
- `alpha` (float): Scale factor for the first array
- `src2` (ndarray): Second input array (same size and type as src1)
- `dst` (ndarray, optional): Output array

**Returns:**

- `dst` (ndarray): Output array where dst = src1 * alpha + src2

### Comparison and Min/Max Operations

Element-wise comparison and minimum/maximum operations for array analysis and thresholding.

#### Comparison

```python { .api }
cv2.compare(src1, src2, cmpop) -> dst
```

Performs per-element comparison of two arrays.

**Parameters:**

- `src1` (ndarray): First input array or scalar
- `src2` (ndarray): Second input array or scalar
- `cmpop` (int): Flag specifying the relation between elements to be checked
  - `cv2.CMP_EQ`: src1 equal to src2
  - `cv2.CMP_GT`: src1 greater than src2
  - `cv2.CMP_GE`: src1 greater than or equal to src2
  - `cv2.CMP_LT`: src1 less than src2
  - `cv2.CMP_LE`: src1 less than or equal to src2
  - `cv2.CMP_NE`: src1 not equal to src2

**Returns:**

- `dst` (ndarray): Output array of type CV_8U with elements set to 255 (true) or 0 (false)

#### Element-wise Minimum

```python { .api }
cv2.min(src1, src2, dst=None) -> dst
```

Calculates per-element minimum of two arrays or an array and a scalar.

**Parameters:**

- `src1` (ndarray): First input array or scalar
- `src2` (ndarray): Second input array or scalar
- `dst` (ndarray, optional): Output array

**Returns:**

- `dst` (ndarray): Output array of the same size and type as input arrays

#### Element-wise Maximum

```python { .api }
cv2.max(src1, src2, dst=None) -> dst
```

Calculates per-element maximum of two arrays or an array and a scalar.

**Parameters:**

- `src1` (ndarray): First input array or scalar
- `src2` (ndarray): Second input array or scalar
- `dst` (ndarray, optional): Output array

**Returns:**

- `dst` (ndarray): Output array of the same size and type as input arrays

### Array Statistics

Statistical operations for analyzing array contents, including norms, means, and extrema.

#### Mean

```python { .api }
cv2.mean(src, mask=None) -> retval
```

Calculates an average (mean) of array elements.

**Parameters:**

- `src` (ndarray): Input array that should have from 1 to 4 channels so that the result can be stored in Scalar_
- `mask` (ndarray, optional): Optional operation mask

**Returns:**

- `retval` (Scalar): Mean value for each channel. When all mask elements are 0, the function returns Scalar::all(0)

#### Norm Calculation

```python { .api }
cv2.norm(src1, normType=None, mask=None) -> retval
cv2.norm(src1, src2, normType=None, mask=None) -> retval
```

Calculates an absolute array norm, absolute difference norm, or relative difference norm.

**Parameters:**

- `src1` (ndarray): First input array
- `src2` (ndarray, optional): Second input array of the same size and type as src1
- `normType` (int, optional): Type of norm to calculate
  - `cv2.NORM_INF`: Max norm
  - `cv2.NORM_L1`: L1 norm
  - `cv2.NORM_L2`: L2 norm (default)
  - `cv2.NORM_L2SQR`: Squared L2 norm
  - `cv2.NORM_HAMMING`: Hamming norm
  - `cv2.NORM_HAMMING2`: Hamming norm with two bits per element
- `mask` (ndarray, optional): Optional operation mask, 8-bit single channel array

**Returns:**

- `retval` (float): Calculated norm value

#### Normalization

```python { .api }
cv2.normalize(src, dst=None, alpha=1.0, beta=0.0, norm_type=cv2.NORM_L2,
              dtype=None, mask=None) -> dst
```

Normalizes the norm or value range of an array.

**Parameters:**

- `src` (ndarray): Input array
- `dst` (ndarray, optional): Output array of the same size as src
- `alpha` (float): Norm value to normalize to or lower range boundary in range normalization
- `beta` (float): Upper range boundary in range normalization
- `norm_type` (int): Normalization type
  - `cv2.NORM_INF`, `cv2.NORM_L1`, `cv2.NORM_L2`: For norm normalization
  - `cv2.NORM_MINMAX`: For range normalization
- `dtype` (int, optional): Output array depth
- `mask` (ndarray, optional): Optional operation mask

**Returns:**

- `dst` (ndarray): Normalized array

#### Mean and Standard Deviation

```python { .api }
cv2.meanStdDev(src, mean=None, stddev=None, mask=None) -> mean, stddev
```

Calculates mean and standard deviation of array elements.

**Parameters:**

- `src` (ndarray): Input array
- `mean` (ndarray, optional): Output parameter for calculated mean
- `stddev` (ndarray, optional): Output parameter for calculated standard deviation
- `mask` (ndarray, optional): Optional operation mask

**Returns:**

- `mean` (ndarray): Mean value of array elements per channel
- `stddev` (ndarray): Standard deviation of array elements per channel

#### Global Minimum and Maximum

```python { .api }
cv2.minMaxLoc(src, mask=None) -> minVal, maxVal, minLoc, maxLoc
```

Finds the global minimum and maximum in an array.

**Parameters:**

- `src` (ndarray): Input single-channel array
- `mask` (ndarray, optional): Optional mask to select a sub-array

**Returns:**

- `minVal` (float): Minimum value
- `maxVal` (float): Maximum value
- `minLoc` (tuple): Position of minimum value (x, y)
- `maxLoc` (tuple): Position of maximum value (x, y)

#### Count Non-Zero Elements

```python { .api }
cv2.countNonZero(src) -> retval
```

Counts non-zero array elements.

**Parameters:**

- `src` (ndarray): Single-channel array

**Returns:**

- `retval` (int): Number of non-zero elements

#### Sum of Elements

```python { .api }
cv2.sum(src) -> retval
cv2.sumElems(src) -> retval
```

Calculates the sum of array elements.

**Parameters:**

- `src` (ndarray): Input array

**Returns:**

- `retval` (Scalar): Sum of array elements per channel

### Channel Operations

Operations for manipulating multi-channel arrays, essential for working with color images.

#### Split Channels

```python { .api }
cv2.split(src) -> mv
```

Divides a multi-channel array into several single-channel arrays.

**Parameters:**

- `src` (ndarray): Input multi-channel array

**Returns:**

- `mv` (list of ndarray): List of single-channel arrays

#### Merge Channels

```python { .api }
cv2.merge(mv, dst=None) -> dst
```

Merges several single-channel arrays into a multi-channel array.

**Parameters:**

- `mv` (list of ndarray): Input list of single-channel arrays to be merged
- `dst` (ndarray, optional): Output array

**Returns:**

- `dst` (ndarray): Output multi-channel array

#### Mix Channels

```python { .api }
cv2.mixChannels(src, dst, fromTo) -> dst
```

Copies specified channels from input arrays to specified channels of output arrays.

**Parameters:**

- `src` (list of ndarray): Input array or list of input arrays
- `dst` (list of ndarray): Output array or list of output arrays
- `fromTo` (list of int): List of index pairs specifying which channels are copied
  - Format: [from_channel, to_channel, from_channel, to_channel, ...]

**Returns:**

- `dst` (list of ndarray): Output arrays

#### Extract Channel

```python { .api }
cv2.extractChannel(src, coi, dst=None) -> dst
```

Extracts a single channel from a multi-channel array.

**Parameters:**

- `src` (ndarray): Input multi-channel array
- `coi` (int): Index of channel to extract (0-based)
- `dst` (ndarray, optional): Output array

**Returns:**

- `dst` (ndarray): Single-channel output array

#### Insert Channel

```python { .api }
cv2.insertChannel(src, dst, coi) -> dst
```

Inserts a single channel into a multi-channel array.

**Parameters:**

- `src` (ndarray): Input single-channel array to be inserted
- `dst` (ndarray): Target multi-channel array
- `coi` (int): Index of channel to insert into (0-based)

**Returns:**

- `dst` (ndarray): Modified multi-channel array

### Array Transformations

Geometric transformations and manipulations of array structure.

#### Flip

```python { .api }
cv2.flip(src, flipCode, dst=None) -> dst
```

Flips an array around vertical, horizontal, or both axes.

**Parameters:**

- `src` (ndarray): Input array
- `flipCode` (int): Flag to specify how to flip the array
  - `0`: Flip vertically (around x-axis)
  - `> 0`: Flip horizontally (around y-axis)
  - `< 0`: Flip both vertically and horizontally
- `dst` (ndarray, optional): Output array

**Returns:**

- `dst` (ndarray): Output array of the same type as src

#### Rotate

```python { .api }
cv2.rotate(src, rotateCode, dst=None) -> dst
```

Rotates an array by 90, 180, or 270 degrees.

**Parameters:**

- `src` (ndarray): Input array
- `rotateCode` (int): Rotation direction
  - `cv2.ROTATE_90_CLOCKWISE`: Rotate 90 degrees clockwise
  - `cv2.ROTATE_180`: Rotate 180 degrees
  - `cv2.ROTATE_90_COUNTERCLOCKWISE`: Rotate 90 degrees counterclockwise
- `dst` (ndarray, optional): Output array

**Returns:**

- `dst` (ndarray): Output rotated array

#### Transpose

```python { .api }
cv2.transpose(src, dst=None) -> dst
```

Transposes a matrix (swaps rows and columns).

**Parameters:**

- `src` (ndarray): Input array
- `dst` (ndarray, optional): Output array

**Returns:**

- `dst` (ndarray): Transposed array

#### Repeat

```python { .api }
cv2.repeat(src, ny, nx, dst=None) -> dst
```

Fills the output array with repeated copies of the input array.

**Parameters:**

- `src` (ndarray): Input array to replicate
- `ny` (int): Number of times to repeat the array along the vertical axis
- `nx` (int): Number of times to repeat the array along the horizontal axis
- `dst` (ndarray, optional): Output array

**Returns:**

- `dst` (ndarray): Output array

#### Horizontal Concatenation

```python { .api }
cv2.hconcat(src, dst=None) -> dst
```

Applies horizontal concatenation to given matrices.

**Parameters:**

- `src` (list of ndarray): Input arrays to concatenate (must have the same number of rows)
- `dst` (ndarray, optional): Output array

**Returns:**

- `dst` (ndarray): Horizontally concatenated array

#### Vertical Concatenation

```python { .api }
cv2.vconcat(src, dst=None) -> dst
```

Applies vertical concatenation to given matrices.

**Parameters:**

- `src` (list of ndarray): Input arrays to concatenate (must have the same number of columns)
- `dst` (ndarray, optional): Output array

**Returns:**

- `dst` (ndarray): Vertically concatenated array

### Range and LUT Operations

Operations for value range checking and lookup table transformations.

#### In Range

```python { .api }
cv2.inRange(src, lowerb, upperb, dst=None) -> dst
```

Checks if array elements lie between the elements of two other arrays or scalars.

**Parameters:**

- `src` (ndarray): Input array
- `lowerb` (ndarray or scalar): Inclusive lower boundary array or scalar
- `upperb` (ndarray or scalar): Inclusive upper boundary array or scalar
- `dst` (ndarray, optional): Output array

**Returns:**

- `dst` (ndarray): Output array of type CV_8U with elements set to 255 (within range) or 0 (outside range)

#### Look-Up Table Transform

```python { .api }
cv2.LUT(src, lut, dst=None) -> dst
```

Performs a look-up table transform of an array.

**Parameters:**

- `src` (ndarray): Input array of 8-bit elements
- `lut` (ndarray): Look-up table of 256 elements; should have the same depth as the output array
- `dst` (ndarray, optional): Output array

**Returns:**

- `dst` (ndarray): Output array of the same size and number of channels as src

### Reduction Operations

Operations that reduce arrays to vectors or scalars.

#### Reduce

```python { .api }
cv2.reduce(src, dim, rtype, dst=None, dtype=None) -> dst
```

Reduces a matrix to a vector.

**Parameters:**

- `src` (ndarray): Input 2D matrix
- `dim` (int): Dimension index along which the reduction is performed
  - `0`: Reduce to a single row
  - `1`: Reduce to a single column
- `rtype` (int): Reduction operation type
  - `cv2.REDUCE_SUM`: Sum over all rows/columns
  - `cv2.REDUCE_AVG`: Mean over all rows/columns
  - `cv2.REDUCE_MAX`: Maximum over all rows/columns
  - `cv2.REDUCE_MIN`: Minimum over all rows/columns
- `dst` (ndarray, optional): Output vector
- `dtype` (int, optional): Output array depth

**Returns:**

- `dst` (ndarray): Output vector

### Linear Algebra Operations

Matrix operations and linear algebra computations.

#### Solve Linear System

```python { .api }
cv2.solve(src1, src2, flags=cv2.DECOMP_LU) -> retval, dst
```

Solves one or more linear systems or least-squares problems.

**Parameters:**

- `src1` (ndarray): Input matrix on the left-hand side of the system
- `src2` (ndarray): Input matrix on the right-hand side of the system
- `flags` (int): Solution method
  - `cv2.DECOMP_LU`: Gaussian elimination with optimal pivot element
  - `cv2.DECOMP_SVD`: Singular value decomposition (SVD)
  - `cv2.DECOMP_EIG`: Eigenvalue decomposition
  - `cv2.DECOMP_CHOLESKY`: Cholesky factorization
  - `cv2.DECOMP_QR`: QR factorization
  - `cv2.DECOMP_NORMAL`: Use normal equations (for overdetermined systems)

**Returns:**

- `retval` (bool): True if the system has a solution
- `dst` (ndarray): Output solution

#### Matrix Inversion

```python { .api }
cv2.invert(src, flags=cv2.DECOMP_LU) -> retval, dst
```

Finds the inverse or pseudo-inverse of a matrix.

**Parameters:**

- `src` (ndarray): Input floating-point M×N matrix
- `flags` (int): Inversion method
  - `cv2.DECOMP_LU`: Gaussian elimination (for square matrices)
  - `cv2.DECOMP_SVD`: Singular value decomposition (for any matrices)
  - `cv2.DECOMP_CHOLESKY`: Cholesky factorization (for symmetric positive-definite matrices)

**Returns:**

- `retval` (float): Inverse condition number (DECOMP_LU) or 0 if singular
- `dst` (ndarray): Output inverse matrix

#### Eigenvalues and Eigenvectors

```python { .api }
cv2.eigen(src, computeEigenvectors=True) -> retval, eigenvalues, eigenvectors
```

Calculates eigenvalues and eigenvectors of a symmetric matrix.

**Parameters:**

- `src` (ndarray): Input symmetric square matrix
- `computeEigenvectors` (bool): Flag indicating whether eigenvectors should be computed

**Returns:**

- `retval` (bool): True if eigenvalues/eigenvectors were computed successfully
- `eigenvalues` (ndarray): Output vector of eigenvalues (sorted in descending order)
- `eigenvectors` (ndarray): Output matrix of eigenvectors (one per row)

#### Determinant

```python { .api }
cv2.determinant(src) -> retval
```

Returns the determinant of a square floating-point matrix.

**Parameters:**

- `src` (ndarray): Input square matrix

**Returns:**

- `retval` (float): Determinant of the matrix

#### Singular Value Decomposition

```python { .api }
cv2.SVDecomp(src, flags=0) -> retval, w, u, vt
```

Performs singular value decomposition of a matrix.

**Parameters:**

- `src` (ndarray): Input M×N matrix
- `flags` (int): Operation flags
  - `cv2.SVD_MODIFY_A`: Allows the function to modify the input matrix
  - `cv2.SVD_NO_UV`: Only singular values are computed
  - `cv2.SVD_FULL_UV`: Full-size U and V are computed

**Returns:**

- `retval` (bool): True if decomposition was successful
- `w` (ndarray): Output vector of singular values
- `u` (ndarray): Output left singular vectors (M×M or M×min(M,N))
- `vt` (ndarray): Output right singular vectors transposed (N×N or min(M,N)×N)

#### Principal Component Analysis

```python { .api }
cv2.PCACompute(data, mean, maxComponents=0) -> mean, eigenvectors, eigenvalues
cv2.PCACompute2(data, mean, maxComponents=0, retainedVariance=0) -> mean, eigenvectors, eigenvalues
```

Performs Principal Component Analysis on a set of vectors.

**Parameters:**

- `data` (ndarray): Input data matrix where each row is a sample vector
- `mean` (ndarray): Input/output mean vector (if empty, computed from data)
- `maxComponents` (int): Maximum number of components to retain
- `retainedVariance` (float, PCACompute2 only): Percentage of variance to retain (0-1)

**Returns:**

- `mean` (ndarray): Mean vector of the input data
- `eigenvectors` (ndarray): Principal components (eigenvectors of covariance matrix)
- `eigenvalues` (ndarray): Eigenvalues corresponding to the eigenvectors

#### General Matrix Multiplication

```python { .api }
cv2.gemm(src1, src2, alpha, src3, beta, flags=0, dst=None) -> dst
```

Performs generalized matrix multiplication: dst = alpha * src1 * src2 + beta * src3.

**Parameters:**

- `src1` (ndarray): First input matrix
- `src2` (ndarray): Second input matrix
- `alpha` (float): Weight of the matrix product
- `src3` (ndarray): Third input matrix added to the product
- `beta` (float): Weight of src3
- `flags` (int): Operation flags
  - `cv2.GEMM_1_T`: Transpose src1
  - `cv2.GEMM_2_T`: Transpose src2
  - `cv2.GEMM_3_T`: Transpose src3
- `dst` (ndarray, optional): Output matrix

**Returns:**

- `dst` (ndarray): Output matrix

#### Transform

```python { .api }
cv2.transform(src, m, dst=None) -> dst
```

Performs matrix transformation of every array element.

**Parameters:**

- `src` (ndarray): Input array (must be of floating-point type)
- `m` (ndarray): Transformation matrix (2×2, 2×3, 3×3, or 3×4)
- `dst` (ndarray, optional): Output array

**Returns:**

- `dst` (ndarray): Output array with the same size and depth as src

#### Perspective Transform

```python { .api }
cv2.perspectiveTransform(src, m, dst=None) -> dst
```

Performs perspective transformation of vectors.

**Parameters:**

- `src` (ndarray): Input two-channel or three-channel floating-point array (each element is a 2D/3D vector)
- `m` (ndarray): 3×3 or 4×4 floating-point transformation matrix
- `dst` (ndarray, optional): Output array

**Returns:**

- `dst` (ndarray): Output array with the same size and type as src

#### Mahalanobis Distance

```python { .api }
cv2.Mahalanobis(v1, v2, icovar) -> retval
```

Calculates the Mahalanobis distance between two vectors.

**Parameters:**

- `v1` (ndarray): First input vector
- `v2` (ndarray): Second input vector
- `icovar` (ndarray): Inverse covariance matrix

**Returns:**

- `retval` (float): Mahalanobis distance

#### Multiply Transposed

```python { .api }
cv2.mulTransposed(src, aTa, dst=None, delta=None, scale=1.0, dtype=None) -> dst
```

Calculates the product of a matrix and its transpose.

**Parameters:**

- `src` (ndarray): Input single-channel matrix
- `aTa` (bool): Flag specifying multiplication ordering
  - `True`: dst = scale * (src - delta)^T * (src - delta)
  - `False`: dst = scale * (src - delta) * (src - delta)^T
- `dst` (ndarray, optional): Output square matrix
- `delta` (ndarray, optional): Optional delta matrix subtracted from src
- `scale` (float): Optional scale factor
- `dtype` (int, optional): Output matrix depth

**Returns:**

- `dst` (ndarray): Output matrix

#### Set Identity

```python { .api }
cv2.setIdentity(mtx, s=1.0) -> mtx
```

Initializes a scaled identity matrix.

**Parameters:**

- `mtx` (ndarray): Matrix to initialize (not necessarily square)
- `s` (Scalar): Value to assign to diagonal elements

**Returns:**

- `mtx` (ndarray): Modified matrix

### Random Number Generation

Random number generation and shuffling operations.

#### Set RNG Seed

```python { .api }
cv2.setRNGSeed(seed) -> None
```

Sets the state of the default random number generator.

**Parameters:**

- `seed` (int): New random number generator seed value

**Returns:**

- None

#### Uniform Random Numbers

```python { .api }
cv2.randu(dst, low, high) -> dst
```

Generates a uniformly distributed random numbers.

**Parameters:**

- `dst` (ndarray): Output array of random numbers (pre-allocated)
- `low` (ndarray or scalar): Inclusive lower boundary of generated random numbers
- `high` (ndarray or scalar): Exclusive upper boundary of generated random numbers

**Returns:**

- `dst` (ndarray): Output array filled with random numbers

#### Normal Random Numbers

```python { .api }
cv2.randn(dst, mean, stddev) -> dst
```

Fills the array with normally distributed random numbers.

**Parameters:**

- `dst` (ndarray): Output array of random numbers (pre-allocated)
- `mean` (ndarray or scalar): Mean value (expectation) of the generated random numbers
- `stddev` (ndarray or scalar): Standard deviation of the generated random numbers

**Returns:**

- `dst` (ndarray): Output array filled with random numbers

#### Random Shuffle

```python { .api }
cv2.randShuffle(dst, iterFactor=1.0) -> dst
```

Shuffles the array elements randomly.

**Parameters:**

- `dst` (ndarray): Input/output array to shuffle
- `iterFactor` (float): Scale factor that determines the number of random swap operations

**Returns:**

- `dst` (ndarray): Shuffled array

### Clustering and Advanced Statistics

K-means clustering and advanced statistical computations.

#### K-Means Clustering

```python { .api }
cv2.kmeans(data, K, bestLabels, criteria, attempts, flags) -> retval, bestLabels, centers
```

Finds centers of clusters and groups input samples around the clusters.

**Parameters:**

- `data` (ndarray): Data for clustering (each row is a sample, floating-point type)
- `K` (int): Number of clusters to split the set into
- `bestLabels` (ndarray): Input/output integer array storing cluster indices for every sample
- `criteria` (tuple): Termination criteria (type, max_iter, epsilon)
  - Type can be `cv2.TERM_CRITERIA_EPS`, `cv2.TERM_CRITERIA_MAX_ITER`, or both
- `attempts` (int): Number of times the algorithm is executed with different initial labelings
- `flags` (int): Flag to specify initial center selection
  - `cv2.KMEANS_RANDOM_CENTERS`: Random initial centers
  - `cv2.KMEANS_PP_CENTERS`: K-means++ center initialization
  - `cv2.KMEANS_USE_INITIAL_LABELS`: Use supplied bestLabels as initial labeling

**Returns:**

- `retval` (float): Compactness measure (sum of squared distances from samples to centers)
- `bestLabels` (ndarray): Output integer array of labels (cluster indices)
- `centers` (ndarray): Output matrix of cluster centers (one row per cluster)

### Fourier Transforms

Discrete Fourier Transform operations for frequency domain analysis.

#### Discrete Fourier Transform

```python { .api }
cv2.dft(src, dst=None, flags=0, nonzeroRows=0) -> dst
```

Performs a forward or inverse Discrete Fourier Transform of a 1D or 2D array.

**Parameters:**

- `src` (ndarray): Input array that could be real or complex
- `dst` (ndarray, optional): Output array whose size and type depends on the flags
- `flags` (int, optional): Transformation flags, representing a combination of DftFlags:
  - `cv2.DFT_INVERSE`: Perform inverse transform
  - `cv2.DFT_SCALE`: Scale the result
  - `cv2.DFT_ROWS`: Perform forward or inverse transform of every row
  - `cv2.DFT_COMPLEX_OUTPUT`: Output is complex array with 2 channels
  - `cv2.DFT_REAL_OUTPUT`: Output is real array (for inverse transform only)
- `nonzeroRows` (int, optional): When not zero, the function assumes that only the first nonzeroRows rows of the input array contain non-zeros

**Returns:**

- `dst` (ndarray): Output array

#### Inverse Discrete Fourier Transform

```python { .api }
cv2.idft(src, dst=None, flags=0, nonzeroRows=0) -> dst
```

Calculates the inverse Discrete Fourier Transform of a 1D or 2D array.

**Parameters:**

- `src` (ndarray): Input floating-point real or complex array
- `dst` (ndarray, optional): Output array whose size and type depend on the flags
- `flags` (int, optional): Operation flags (see dft and DftFlags)
- `nonzeroRows` (int, optional): Number of dst rows to process; the rest have undefined content

**Returns:**

- `dst` (ndarray): Output array. Note: idft(src, dst, flags) is equivalent to dft(src, dst, flags | DFT_INVERSE). Neither dft nor idft scales the result by default, so you should pass DFT_SCALE to one of them explicitly to make these transforms mutually inverse

### Image Border Operations

Operations for creating borders around images.

#### Copy and Make Border

```python { .api }
cv2.copyMakeBorder(src, top, bottom, left, right, borderType, dst=None, value=None) -> dst
```

Forms a border around an image.

**Parameters:**

- `src` (ndarray): Source image
- `top` (int): Number of top pixels to extrapolate
- `bottom` (int): Number of bottom pixels to extrapolate
- `left` (int): Number of left pixels to extrapolate
- `right` (int): Number of right pixels to extrapolate
- `borderType` (int): Border type. See borderInterpolate for details:
  - `cv2.BORDER_CONSTANT`: Border filled with constant value
  - `cv2.BORDER_REPLICATE`: Border filled with replicated edge pixels
  - `cv2.BORDER_REFLECT`: Border reflects border elements
  - `cv2.BORDER_WRAP`: Border wraps around
  - `cv2.BORDER_REFLECT_101` or `cv2.BORDER_DEFAULT`: Similar to BORDER_REFLECT but with slight difference
- `dst` (ndarray, optional): Destination image of the same type as src and size Size(src.cols+left+right, src.rows+top+bottom)
- `value` (Scalar, optional): Border value if borderType==BORDER_CONSTANT

**Returns:**

- `dst` (ndarray): Output image with border. The function copies the source image into the middle of the destination image and fills border areas
