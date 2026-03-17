# Polynomial Operations

A sub-package for efficiently dealing with polynomials of different mathematical bases. NumPy provides convenience classes for six different polynomial types, each optimized for their respective mathematical foundations.

## Capabilities

### Convenience Classes

High-level polynomial classes providing consistent interfaces for creation, manipulation, and fitting across different polynomial bases.

```python { .api }
class Polynomial:
    """Power series polynomial class."""
    def __init__(self, coef, domain=None, window=None, symbol='x'): ...
    @classmethod
    def fit(cls, x, y, deg, **kwargs): ...
    def __call__(self, arg): ...
    def deriv(self, m=1): ...
    def integ(self, m=1, k=[], **kwargs): ...
    def roots(self): ...
    def degree(self): ...

class Chebyshev:
    """Chebyshev series polynomial class."""
    def __init__(self, coef, domain=None, window=None, symbol='x'): ...
    @classmethod
    def fit(cls, x, y, deg, **kwargs): ...
    def __call__(self, arg): ...
    def deriv(self, m=1): ...
    def integ(self, m=1, k=[], **kwargs): ...
    def roots(self): ...

class Legendre:
    """Legendre series polynomial class."""
    def __init__(self, coef, domain=None, window=None, symbol='x'): ...
    @classmethod
    def fit(cls, x, y, deg, **kwargs): ...
    def __call__(self, arg): ...
    def deriv(self, m=1): ...
    def integ(self, m=1, k=[], **kwargs): ...
    def roots(self): ...

class Laguerre:
    """Laguerre series polynomial class."""
    def __init__(self, coef, domain=None, window=None, symbol='x'): ...
    @classmethod
    def fit(cls, x, y, deg, **kwargs): ...
    def __call__(self, arg): ...
    def deriv(self, m=1): ...
    def integ(self, m=1, k=[], **kwargs): ...
    def roots(self): ...

class Hermite:
    """Hermite series polynomial class."""
    def __init__(self, coef, domain=None, window=None, symbol='x'): ...
    @classmethod
    def fit(cls, x, y, deg, **kwargs): ...
    def __call__(self, arg): ...
    def deriv(self, m=1): ...
    def integ(self, m=1, k=[], **kwargs): ...
    def roots(self): ...

class HermiteE:
    """HermiteE series polynomial class."""
    def __init__(self, coef, domain=None, window=None, symbol='x'): ...
    @classmethod
    def fit(cls, x, y, deg, **kwargs): ...
    def __call__(self, arg): ...
    def deriv(self, m=1): ...
    def integ(self, m=1, k=[], **kwargs): ...
    def roots(self): ...
```

### Legacy Functions

Traditional polynomial functions for backward compatibility, primarily focused on power series.

```python { .api }
def poly(seq_of_zeros):
    """
    Find the coefficients of a polynomial with the given sequence of roots.
    
    Parameters:
    - seq_of_zeros: array_like, sequence of polynomial zeros
    
    Returns:
    ndarray: Polynomial coefficients from highest to lowest degree
    """

def polyval(p, x):
    """
    Evaluate a polynomial at specific values.
    
    Parameters:
    - p: array_like, polynomial coefficients (highest to lowest degree)
    - x: array_like, values at which to evaluate the polynomial
    
    Returns:
    ndarray: Polynomial values at x
    """

def polyfit(x, y, deg, **kwargs):
    """
    Least squares polynomial fit.
    
    Parameters:
    - x: array_like, x-coordinates of data points
    - y: array_like, y-coordinates of data points  
    - deg: int, degree of fitting polynomial
    
    Returns:
    ndarray: Polynomial coefficients (highest to lowest degree)
    """

def polyder(p, m=1):
    """
    Return the derivative of the specified order of a polynomial.
    
    Parameters:
    - p: array_like, polynomial coefficients
    - m: int, order of derivative
    
    Returns:
    ndarray: Coefficients of derivative polynomial
    """

def polyint(p, m=1, k=None):
    """
    Return an antiderivative (indefinite integral) of a polynomial.
    
    Parameters:
    - p: array_like, polynomial coefficients
    - m: int, order of integration
    - k: array_like, integration constants
    
    Returns:
    ndarray: Coefficients of integrated polynomial
    """

def roots(p):
    """
    Return the roots of a polynomial with coefficients given in p.
    
    Parameters:
    - p: array_like, polynomial coefficients
    
    Returns:
    ndarray: Roots of the polynomial
    """

class poly1d:
    """
    A one-dimensional polynomial class.
    
    Note: This class is considered legacy. For new code, use
    numpy.polynomial.Polynomial instead.
    """
    def __init__(self, c_or_r, r=False, variable=None): ...
    def __call__(self, val): ...
    def deriv(self, m=1): ...
    def integ(self, m=1, k=0): ...
    @property
    def roots(self): ...
    @property 
    def coeffs(self): ...
```

## Usage Examples

### Modern Polynomial Classes

```python
import numpy as np
from numpy.polynomial import Polynomial, Chebyshev

# Create and work with power series polynomial
p = Polynomial([1, 2, 3])  # 1 + 2*x + 3*x^2
print(p(2))  # Evaluate at x=2

# Fit polynomial to data
x = np.linspace(0, 10, 11)
y = x**2 + 2*x + 1
fitted = Polynomial.fit(x, y, deg=2)
print(fitted.convert().coef)  # Show coefficients

# Work with Chebyshev polynomials
cheb = Chebyshev.fit(x, y, deg=2)
print(cheb(x))  # Evaluate Chebyshev polynomial
```

### Legacy Polynomial Functions

```python
import numpy as np

# Traditional polynomial operations
coeffs = [3, 2, 1]  # 3*x^2 + 2*x + 1
x_vals = [0, 1, 2, 3]
result = np.polyval(coeffs, x_vals)

# Fit polynomial to data (legacy)
x = np.array([0, 1, 2, 3])
y = np.array([1, 3, 7, 13]) 
coeffs = np.polyfit(x, y, deg=2)

# Find roots
roots = np.roots([1, -5, 6])  # roots of x^2 - 5x + 6
print(roots)  # [2, 3]
```