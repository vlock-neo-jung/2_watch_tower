# Random Number Generation

Comprehensive random number generation through numpy.random. Provides random sampling from various probability distributions, random choice operations, and modern BitGenerator infrastructure for high-quality pseudorandom numbers.

## Core Generator Interface

### Modern Generator API

The recommended interface for random number generation.

```python { .api }
def random.default_rng(seed=None):
    """
    Construct new Generator with default BitGenerator (PCG64).
    
    Parameters:
    - seed: {None, int, array_like, BitGenerator}, random seed
    
    Returns:
    Generator: New random number generator
    """

class random.Generator:
    """
    Container for BitGenerator and provides random number generation methods.
    """
    def random(self, size=None, dtype=float, out=None):
        """Random floats in [0.0, 1.0)"""
    
    def integers(self, low, high=None, size=None, dtype=int, endpoint=False):
        """Random integers from low to high"""
    
    def normal(self, loc=0.0, scale=1.0, size=None):
        """Normal (Gaussian) distribution"""
    
    def uniform(self, low=0.0, high=1.0, size=None):
        """Uniform distribution"""
    
    def choice(self, a, size=None, replace=True, p=None, axis=0, shuffle=True):
        """Random sample from array"""
```

### Legacy RandomState Interface

Compatibility interface (legacy, use Generator for new code).

```python { .api }
class random.RandomState:
    """
    Legacy random number generator interface.
    """
    def __init__(self, seed=None):
        """Initialize RandomState"""
    
    def random_sample(self, size=None):
        """Random floats in [0.0, 1.0)""" 
    
    def randint(self, low, high=None, size=None, dtype=int):
        """Random integers"""
    
    def normal(self, loc=0.0, scale=1.0, size=None):
        """Normal distribution"""
```

## Distribution Functions (Legacy Interface)

### Uniform Distributions

```python { .api }
def random.random(size=None):
    """
    Return random floats in half-open interval [0.0, 1.0).
    
    Parameters:
    - size: int or tuple, output shape
    
    Returns:
    ndarray or float: Random values
    """

def random.rand(*dn):
    """
    Random values in given shape from uniform distribution [0, 1).
    
    Parameters:
    - *dn: int, shape dimensions
    
    Returns:
    ndarray: Random values
    """

def random.randn(*dn):
    """
    Random values from standard normal distribution.
    
    Parameters:
    - *dn: int, shape dimensions
    
    Returns:
    ndarray: Random values from N(0, 1)
    """

def random.uniform(low=0.0, high=1.0, size=None):
    """
    Draw samples from uniform distribution.
    
    Parameters:
    - low, high: float, distribution bounds
    - size: int or tuple, output shape
    
    Returns:
    ndarray: Random samples
    """
```

### Discrete Distributions

```python { .api }
def random.randint(low, high=None, size=None, dtype=int):
    """
    Random integers from low (inclusive) to high (exclusive).
    
    Parameters:
    - low, high: int, range bounds
    - size: int or tuple, output shape
    - dtype: data-type, output type
    
    Returns:
    ndarray: Random integers
    """

def random.binomial(n, p, size=None):
    """
    Draw samples from binomial distribution.
    
    Parameters:
    - n: int or array_like, number of trials
    - p: float or array_like, probability of success
    - size: int or tuple, output shape
    
    Returns:
    ndarray: Random samples
    """

def random.poisson(lam=1.0, size=None):
    """
    Draw samples from Poisson distribution.
    
    Parameters:
    - lam: float or array_like, expected intervals
    - size: int or tuple, output shape
    
    Returns:
    ndarray: Random samples
    """

def random.geometric(p, size=None):
    """
    Draw samples from geometric distribution.
    
    Parameters:
    - p: float or array_like, success probability
    - size: int or tuple, output shape
    
    Returns:
    ndarray: Random samples
    """
```

### Continuous Distributions

```python { .api }
def random.normal(loc=0.0, scale=1.0, size=None):
    """
    Draw samples from normal (Gaussian) distribution.
    
    Parameters:
    - loc: float or array_like, mean
    - scale: float or array_like, standard deviation
    - size: int or tuple, output shape
    
    Returns:
    ndarray: Random samples
    """

def random.exponential(scale=1.0, size=None):
    """
    Draw samples from exponential distribution.
    
    Parameters:
    - scale: float or array_like, scale parameter
    - size: int or tuple, output shape
    
    Returns:
    ndarray: Random samples
    """

def random.gamma(shape, scale=1.0, size=None):
    """
    Draw samples from Gamma distribution.
    
    Parameters:
    - shape: float or array_like, shape parameter
    - scale: float or array_like, scale parameter
    - size: int or tuple, output shape
    
    Returns:
    ndarray: Random samples
    """

def random.beta(a, b, size=None):
    """
    Draw samples from Beta distribution.
    
    Parameters:
    - a, b: float or array_like, shape parameters
    - size: int or tuple, output shape
    
    Returns:
    ndarray: Random samples
    """

def random.lognormal(mean=0.0, sigma=1.0, size=None):
    """
    Draw samples from log-normal distribution.
    
    Parameters:
    - mean: float or array_like, mean of underlying normal
    - sigma: float or array_like, std of underlying normal
    - size: int or tuple, output shape
    
    Returns:
    ndarray: Random samples
    """
```

### Sampling and Permutation

```python { .api }
def random.choice(a, size=None, replace=True, p=None):
    """
    Generate random sample from given 1-D array.
    
    Parameters:
    - a: 1-D array_like or int, array to sample from
    - size: int or tuple, output shape
    - replace: bool, whether sample with replacement
    - p: 1-D array_like, probabilities for each element
    
    Returns:
    ndarray or scalar: Random samples
    """

def random.shuffle(x):
    """
    Modify sequence in-place by shuffling its contents.
    
    Parameters:
    - x: array_like, sequence to shuffle
    
    Returns:
    None: Modifies x in-place
    """

def random.permutation(x):
    """
    Randomly permute sequence or return permuted range.
    
    Parameters:
    - x: int or array_like, sequence to permute
    
    Returns:
    ndarray: Permuted sequence
    """
```

### Seeding and State Management

```python { .api }
def random.seed(seed=None):
    """
    Seed the legacy random number generator.
    
    Parameters:
    - seed: {None, int, array_like}, seed value
    
    Returns:
    None: Seeds global RandomState
    """

def random.get_state():
    """
    Return tuple representing internal state of generator.
    
    Returns:
    tuple: Current state of RandomState
    """

def random.set_state(state):
    """
    Set internal state of generator from tuple.
    
    Parameters:
    - state: tuple, state from get_state()
    
    Returns:
    None: Sets RandomState to given state
    """
```

## BitGenerators

### Core BitGenerator Classes

```python { .api }
class random.BitGenerator:
    """Base class for bit generators."""

class random.PCG64(BitGenerator):
    """PCG-64 bit generator (default, recommended)."""
    def __init__(self, seed=None): ...

class random.MT19937(BitGenerator):
    """Mersenne Twister bit generator."""
    def __init__(self, seed=None): ...

class random.Philox(BitGenerator):
    """Philox bit generator."""
    def __init__(self, seed=None, counter=None, key=None): ...

class random.SFC64(BitGenerator):
    """SFC-64 bit generator."""
    def __init__(self, seed=None): ...

class random.SeedSequence:
    """Seed sequence for initializing bit generators."""
    def __init__(self, entropy=None, spawn_key=(), pool_size=4): ...
```

## Usage Examples

### Modern Generator Interface

```python
import numpy as np

# Create generator (recommended approach)
rng = np.random.default_rng(seed=42)

# Generate random numbers
random_floats = rng.random(5)           # [0.374, 0.950, 0.731, 0.598, 0.156]
random_ints = rng.integers(1, 10, 5)    # [6, 2, 7, 8, 1]

# Sample from distributions
normal_vals = rng.normal(0, 1, 100)     # 100 samples from N(0,1)
uniform_vals = rng.uniform(-1, 1, 50)   # 50 samples from Uniform(-1,1)

# Random choice and sampling
data = np.array([1, 2, 3, 4, 5])
sample = rng.choice(data, size=3, replace=False)  # Random sample without replacement
```

### Legacy Interface Examples

```python
import numpy as np

# Set seed for reproducibility
np.random.seed(42)

# Basic random generation
random_array = np.random.random(10)     # 10 random floats [0, 1)
int_array = np.random.randint(1, 100, 5)  # 5 random integers [1, 100)

# Distribution sampling
normal_data = np.random.normal(50, 15, 1000)  # Mean=50, std=15
exponential_data = np.random.exponential(2, 500)  # Scale=2

# Random sampling and permutation
original = np.array([1, 2, 3, 4, 5])
shuffled = np.random.permutation(original)  # Random permutation
random_choice = np.random.choice(original, 3)  # Random sample with replacement
```

### Custom BitGenerator Usage

```python
import numpy as np

# Use specific BitGenerator
pcg = np.random.PCG64(seed=12345)
rng = np.random.Generator(pcg)

# Generate samples
samples = rng.normal(0, 1, 1000)

# Multiple independent streams
seeds = np.random.SeedSequence(entropy=42).spawn(4)
generators = [np.random.Generator(np.random.PCG64(s)) for s in seeds]

# Each generator produces independent sequences
results = [gen.random(100) for gen in generators]
```