# Linear Algebra Operations

Core linear algebra functionality through numpy.linalg and basic array operations. Provides matrix products, decompositions, eigenvalue problems, and solving linear systems for scientific computing applications.

## Core Array Products

### Matrix and Vector Products

Basic linear algebra operations available in the main numpy namespace.

```python { .api }
def dot(a, b, out=None):
    """
    Dot product of two arrays.
    
    Parameters:
    - a, b: array_like, input arrays
    - out: ndarray, output array
    
    Returns:
    ndarray: Dot product of a and b
    """

def vdot(a, b):
    """
    Return dot product of two vectors.
    
    Parameters:
    - a, b: array_like, input arrays
    
    Returns:
    complex: Dot product (with complex conjugation)
    """

def inner(a, b):
    """
    Inner product of two arrays.
    
    Parameters:
    - a, b: array_like, input arrays
    
    Returns:
    ndarray: Inner product
    """

def outer(a, b, out=None):
    """
    Compute outer product of two vectors.
    
    Parameters:
    - a, b: array_like, input vectors
    - out: ndarray, output array
    
    Returns:
    ndarray: Outer product
    """

def matmul(x1, x2, out=None, **kwargs):
    """
    Matrix product of two arrays.
    
    Parameters:
    - x1, x2: array_like, input arrays
    - out: ndarray, output array
    - **kwargs: additional arguments
    
    Returns:
    ndarray: Matrix product
    """

def tensordot(a, b, axes=2):
    """
    Compute tensor dot product along specified axes.
    
    Parameters:
    - a, b: array_like, input arrays
    - axes: int or (2,) array_like, axes to sum over
    
    Returns:
    ndarray: Tensor dot product
    """

def einsum(subscripts, *operands, out=None, dtype=None, order='K', casting='safe', optimize=False):
    """
    Evaluates Einstein summation convention on operands.
    
    Parameters:
    - subscripts: str, subscripts for summation
    - *operands: array_like, input arrays
    - out: ndarray, output array
    - dtype: data-type, output data type
    - order: {'C', 'F', 'A', 'K'}, memory layout
    - casting: {'no', 'equiv', 'safe', 'same_kind', 'unsafe'}, casting rule
    - optimize: {False, True, 'greedy', 'optimal'}, optimization strategy
    
    Returns:
    ndarray: Calculation based on Einstein summation
    """

def kron(a, b):
    """
    Kronecker product of two arrays.
    
    Parameters:
    - a, b: array_like, input arrays
    
    Returns:
    ndarray: Kronecker product
    """

def cross(a, b, axisa=-1, axisb=-1, axisc=-1, axis=None):
    """
    Return cross product of two (arrays of) vectors.
    
    Parameters:
    - a, b: array_like, input arrays
    - axisa, axisb, axisc: int, axes of a, b, and output
    - axis: int, axis along which to take cross product
    
    Returns:
    ndarray: Cross product
    """
```

## numpy.linalg Functions

### Matrix Decompositions

Advanced matrix decomposition algorithms.

```python { .api }
def linalg.cholesky(a):
    """
    Cholesky decomposition.
    
    Parameters:
    - a: array_like, Hermitian positive-definite matrix
    
    Returns:
    ndarray: Lower triangular Cholesky factor
    """

def linalg.qr(a, mode='reduced'):
    """
    Compute QR decomposition of matrix.
    
    Parameters:
    - a: array_like, input matrix
    - mode: {'reduced', 'complete', 'r', 'raw'}, decomposition mode
    
    Returns:
    ndarray or tuple: Q and R matrices
    """

def linalg.svd(a, full_matrices=True, compute_uv=True, hermitian=False):
    """
    Singular Value Decomposition.
    
    Parameters:
    - a: array_like, input matrix
    - full_matrices: bool, compute full or reduced matrices
    - compute_uv: bool, compute U and Vh matrices
    - hermitian: bool, assume hermitian matrix
    
    Returns:
    tuple: (U, s, Vh) singular value decomposition
    """

def linalg.svdvals(a):
    """
    Compute singular values only.
    
    Parameters:
    - a: array_like, input matrix
    
    Returns:
    ndarray: Singular values in descending order
    """
```

### Eigenvalues and Eigenvectors

Eigenvalue decomposition functions.

```python { .api }
def linalg.eig(a):
    """
    Compute eigenvalues and eigenvectors.
    
    Parameters:
    - a: array_like, square matrix
    
    Returns:
    tuple: (eigenvalues, eigenvectors)
    """

def linalg.eigh(a, UPLO='L'):
    """
    Compute eigenvalues and eigenvectors of Hermitian matrix.
    
    Parameters:
    - a: array_like, Hermitian matrix
    - UPLO: {'L', 'U'}, use upper or lower triangle
    
    Returns:
    tuple: (eigenvalues, eigenvectors)
    """

def linalg.eigvals(a):
    """
    Compute eigenvalues.
    
    Parameters:
    - a: array_like, square matrix
    
    Returns:
    ndarray: Eigenvalues
    """

def linalg.eigvalsh(a, UPLO='L'):
    """
    Compute eigenvalues of Hermitian matrix.
    
    Parameters:
    - a: array_like, Hermitian matrix
    - UPLO: {'L', 'U'}, use upper or lower triangle
    
    Returns:
    ndarray: Eigenvalues in ascending order
    """
```

### Matrix Norms

Various matrix and vector norms.

```python { .api }
def linalg.norm(x, ord=None, axis=None, keepdims=False):
    """
    Matrix or vector norm.
    
    Parameters:
    - x: array_like, input array
    - ord: {non-zero int, inf, -inf, 'fro', 'nuc'}, norm order
    - axis: None or int or 2-tuple of ints, axes for norm calculation
    - keepdims: bool, keep reduced dimensions
    
    Returns:
    ndarray or float: Norm of input
    """

def linalg.matrix_norm(x, ord='fro', axis=(-2, -1), keepdims=False):
    """
    Matrix norm.
    
    Parameters:
    - x: array_like, input matrix
    - ord: {1, -1, 2, -2, inf, -inf, 'fro', 'nuc'}, norm order
    - axis: 2-tuple of ints, axes for matrix
    - keepdims: bool, keep reduced dimensions
    
    Returns:
    ndarray or float: Matrix norm
    """

def linalg.vector_norm(x, ord=2, axis=None, keepdims=False):
    """
    Vector norm.
    
    Parameters:
    - x: array_like, input vector
    - ord: {non-zero int, inf, -inf}, norm order
    - axis: None or int, axis for norm calculation
    - keepdims: bool, keep reduced dimensions
    
    Returns:
    ndarray or float: Vector norm
    """
```

### Linear System Solvers

Solving linear equations and matrix inversion.

```python { .api }
def linalg.solve(a, b):
    """
    Solve linear system ax = b for x.
    
    Parameters:
    - a: array_like, coefficient matrix
    - b: array_like, ordinate values
    
    Returns:
    ndarray: Solution to system ax = b
    """

def linalg.lstsq(a, b, rcond=None):
    """
    Least-squares solution to linear system.
    
    Parameters:
    - a: array_like, coefficient matrix
    - b: array_like, ordinate values
    - rcond: float, cutoff for small singular values
    
    Returns:
    tuple: (solution, residuals, rank, singular_values)
    """

def linalg.inv(a):
    """
    Compute multiplicative inverse of matrix.
    
    Parameters:
    - a: array_like, square matrix to invert
    
    Returns:
    ndarray: Multiplicative inverse of a
    """

def linalg.pinv(a, rcond=1e-15, hermitian=False):
    """
    Compute Moore-Penrose pseudoinverse.
    
    Parameters:
    - a: array_like, matrix to pseudoinvert
    - rcond: float, cutoff for small singular values
    - hermitian: bool, assume hermitian matrix
    
    Returns:
    ndarray: Moore-Penrose pseudoinverse
    """

def linalg.tensorsolve(a, b, axes=None):
    """
    Solve tensor equation ax = b for x.
    
    Parameters:
    - a: array_like, coefficient tensor
    - b: array_like, right-hand side tensor
    - axes: tuple of ints, axes in a to reorder
    
    Returns:
    ndarray: Solution tensor
    """

def linalg.tensorinv(a, ind=2):
    """
    Compute inverse of N-dimensional array.
    
    Parameters:
    - a: array_like, tensor to invert
    - ind: int, number of first indices forming square matrix
    
    Returns:
    ndarray: Inverse of input tensor
    """
```

### Matrix Properties

Calculate properties and characteristics of matrices.

```python { .api }
def linalg.det(a):
    """
    Compute determinant of array.
    
    Parameters:
    - a: array_like, square matrix
    
    Returns:
    ndarray or float: Determinant of a
    """

def linalg.slogdet(a):
    """
    Compute sign and natural logarithm of determinant.
    
    Parameters:
    - a: array_like, square matrix
    
    Returns:
    tuple: (sign, logdet) sign and log of absolute determinant
    """

def linalg.matrix_rank(a, tol=None, hermitian=False):
    """
    Return matrix rank using SVD method.
    
    Parameters:
    - a: array_like, input matrix
    - tol: float, threshold for singular values
    - hermitian: bool, assume hermitian matrix
    
    Returns:
    ndarray or int: Rank of matrix
    """

def linalg.cond(x, p=None):
    """
    Compute condition number of matrix.
    
    Parameters:
    - x: array_like, input matrix
    - p: {None, 1, -1, 2, -2, inf, -inf, 'fro'}, norm order
    
    Returns:
    ndarray or float: Condition number
    """

def linalg.matrix_power(a, n):
    """
    Raise square matrix to integer power.
    
    Parameters:
    - a: array_like, square matrix
    - n: int, exponent
    
    Returns:
    ndarray: Matrix raised to power n
    """

def linalg.multi_dot(arrays, out=None):
    """
    Compute dot product of two or more arrays in single function call.
    
    Parameters:
    - arrays: sequence of array_like, matrices to multiply
    - out: ndarray, output array
    
    Returns:
    ndarray: Dot product of all input arrays
    """
```

### Matrix Utilities

Additional matrix manipulation functions from linalg.

```python { .api }
def linalg.trace(x, offset=0, axis1=0, axis2=1, dtype=None, out=None):
    """
    Return sum along diagonals of array.
    
    Parameters:
    - x: array_like, input array
    - offset: int, offset from main diagonal
    - axis1, axis2: int, axes to trace over
    - dtype: data-type, output data type
    - out: ndarray, output array
    
    Returns:
    ndarray or scalar: Sum along diagonal
    """

def linalg.diagonal(x, offset=0, axis1=0, axis2=1):
    """
    Return specified diagonals.
    
    Parameters:
    - x: array_like, input array
    - offset: int, offset from main diagonal
    - axis1, axis2: int, axes for diagonal extraction
    
    Returns:
    ndarray: Diagonal elements
    """

def linalg.matrix_transpose(x):
    """
    Transpose last two dimensions of array.
    
    Parameters:
    - x: array_like, input array
    
    Returns:
    ndarray: Array with last two dimensions transposed
    """
```

### Exception

```python { .api }
class linalg.LinAlgError(Exception):
    """
    Generic Python-exception-derived object raised by linalg functions.
    """
```

## Usage Examples

### Basic Matrix Operations

```python
import numpy as np

# Matrix multiplication
A = np.array([[1, 2], [3, 4]])
B = np.array([[5, 6], [7, 8]])

# Different ways to multiply matrices
dot_product = np.dot(A, B)        # [[19, 22], [43, 50]]
matmul_product = np.matmul(A, B)  # [[19, 22], [43, 50]]
at_product = A @ B               # [[19, 22], [43, 50]]

# Vector operations
v1 = np.array([1, 2, 3])
v2 = np.array([4, 5, 6])
dot_prod = np.dot(v1, v2)        # 32
outer_prod = np.outer(v1, v2)    # [[4, 5, 6], [8, 10, 12], [12, 15, 18]]
```

### Linear System Solving

```python
import numpy as np

# Solve linear system Ax = b
A = np.array([[3, 1], [1, 2]])
b = np.array([9, 8])

# Solve for x
x = np.linalg.solve(A, b)        # [2.0, 3.0]

# Matrix inversion
A_inv = np.linalg.inv(A)         # Inverse of A
identity = A @ A_inv             # Should be identity matrix

# Least squares for overdetermined systems
A_over = np.array([[1, 1], [1, 2], [1, 3]])
b_over = np.array([6, 8, 10])
x_lstsq, residuals, rank, s = np.linalg.lstsq(A_over, b_over, rcond=None)
```

### Matrix Decompositions

```python
import numpy as np

# Sample matrix
A = np.array([[4, 2], [2, 3]], dtype=float)

# Eigenvalue decomposition
eigenvals, eigenvecs = np.linalg.eig(A)
print(f'Eigenvalues: {eigenvals}')
print(f'Eigenvectors:\n{eigenvecs}')

# SVD decomposition
U, s, Vh = np.linalg.svd(A)
reconstructed = U @ np.diag(s) @ Vh

# QR decomposition
Q, R = np.linalg.qr(A)
reconstructed_qr = Q @ R
```

### Matrix Properties

```python
import numpy as np

A = np.array([[1, 2], [3, 4]])

# Matrix properties
det_A = np.linalg.det(A)         # -2.0
rank_A = np.linalg.matrix_rank(A) # 2
cond_A = np.linalg.cond(A)       # 14.93 (condition number)

# Matrix norms
frob_norm = np.linalg.norm(A, 'fro')  # Frobenius norm
spectral_norm = np.linalg.norm(A, 2)  # Spectral norm (largest singular value)
```