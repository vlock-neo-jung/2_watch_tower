# Fast Fourier Transform

Discrete Fourier Transform operations through numpy.fft for signal processing and frequency domain analysis. Provides 1D, 2D, and N-D transforms with both complex and real-valued inputs.

## Capabilities

### Standard FFTs

Standard discrete Fourier transforms for complex inputs.

```python { .api }
def fft.fft(a, n=None, axis=-1, norm=None, plan=None):
    """
    Compute 1-D discrete Fourier Transform.
    
    Parameters:
    - a: array_like, input array
    - n: int, length of transformed axis
    - axis: int, axis over which to compute FFT
    - norm: {None, 'ortho', 'forward', 'backward'}, normalization mode
    - plan: plan object (future use)
    
    Returns:
    ndarray: Complex-valued FFT result
    """

def fft.ifft(a, n=None, axis=-1, norm=None, plan=None):
    """
    Compute 1-D inverse discrete Fourier Transform.
    
    Parameters:
    - a: array_like, input array
    - n: int, length of transformed axis
    - axis: int, axis over which to compute IFFT
    - norm: {None, 'ortho', 'forward', 'backward'}, normalization mode
    - plan: plan object (future use)
    
    Returns:
    ndarray: Complex-valued inverse FFT result
    """

def fft.fft2(a, s=None, axes=(-2, -1), norm=None, plan=None):
    """
    Compute 2-D discrete Fourier Transform.
    
    Parameters:
    - a: array_like, input array
    - s: sequence of ints, shape of result
    - axes: sequence of ints, axes over which to compute FFT
    - norm: {None, 'ortho', 'forward', 'backward'}, normalization mode
    - plan: plan object (future use)
    
    Returns:
    ndarray: Complex-valued 2D FFT result
    """

def fft.ifft2(a, s=None, axes=(-2, -1), norm=None, plan=None):
    """
    Compute 2-D inverse discrete Fourier Transform.
    
    Parameters:
    - a: array_like, input array
    - s: sequence of ints, shape of result
    - axes: sequence of ints, axes over which to compute IFFT
    - norm: {None, 'ortho', 'forward', 'backward'}, normalization mode
    - plan: plan object (future use)
    
    Returns:
    ndarray: Complex-valued 2D inverse FFT result
    """

def fft.fftn(a, s=None, axes=None, norm=None, plan=None):
    """
    Compute N-D discrete Fourier Transform.
    
    Parameters:
    - a: array_like, input array
    - s: sequence of ints, shape of result
    - axes: sequence of ints, axes over which to compute FFT
    - norm: {None, 'ortho', 'forward', 'backward'}, normalization mode
    - plan: plan object (future use)
    
    Returns:
    ndarray: Complex-valued N-D FFT result
    """

def fft.ifftn(a, s=None, axes=None, norm=None, plan=None):
    """
    Compute N-D inverse discrete Fourier Transform.
    
    Parameters:
    - a: array_like, input array
    - s: sequence of ints, shape of result
    - axes: sequence of ints, axes over which to compute IFFT
    - norm: {None, 'ortho', 'forward', 'backward'}, normalization mode
    - plan: plan object (future use)
    
    Returns:
    ndarray: Complex-valued N-D inverse FFT result
    """
```

### Real FFTs

Optimized transforms for real-valued inputs.

```python { .api }
def fft.rfft(a, n=None, axis=-1, norm=None, plan=None):
    """
    Compute 1-D discrete Fourier Transform for real input.
    
    Parameters:
    - a: array_like, real-valued input array
    - n: int, length of transformed axis
    - axis: int, axis over which to compute FFT
    - norm: {None, 'ortho', 'forward', 'backward'}, normalization mode
    - plan: plan object (future use)
    
    Returns:
    ndarray: Complex-valued FFT result (length n//2 + 1)
    """

def fft.irfft(a, n=None, axis=-1, norm=None, plan=None):
    """
    Compute inverse of rfft.
    
    Parameters:
    - a: array_like, complex input array
    - n: int, length of output (should be even)
    - axis: int, axis over which to compute IFFT
    - norm: {None, 'ortho', 'forward', 'backward'}, normalization mode
    - plan: plan object (future use)
    
    Returns:
    ndarray: Real-valued inverse FFT result
    """

def fft.rfft2(a, s=None, axes=(-2, -1), norm=None, plan=None):
    """
    Compute 2-D discrete Fourier Transform for real input.
    
    Parameters:
    - a: array_like, real-valued input array
    - s: sequence of ints, shape of result
    - axes: sequence of ints, axes over which to compute FFT
    - norm: {None, 'ortho', 'forward', 'backward'}, normalization mode
    - plan: plan object (future use)
    
    Returns:
    ndarray: Complex-valued 2D FFT result
    """

def fft.irfft2(a, s=None, axes=(-2, -1), norm=None, plan=None):
    """
    Compute 2-D inverse discrete Fourier Transform for real output.
    
    Parameters:
    - a: array_like, complex input array
    - s: sequence of ints, shape of output
    - axes: sequence of ints, axes over which to compute IFFT
    - norm: {None, 'ortho', 'forward', 'backward'}, normalization mode
    - plan: plan object (future use)
    
    Returns:
    ndarray: Real-valued 2D inverse FFT result
    """

def fft.rfftn(a, s=None, axes=None, norm=None, plan=None):
    """
    Compute N-D discrete Fourier Transform for real input.
    
    Parameters:
    - a: array_like, real-valued input array
    - s: sequence of ints, shape of result
    - axes: sequence of ints, axes over which to compute FFT
    - norm: {None, 'ortho', 'forward', 'backward'}, normalization mode
    - plan: plan object (future use)
    
    Returns:
    ndarray: Complex-valued N-D FFT result
    """

def fft.irfftn(a, s=None, axes=None, norm=None, plan=None):
    """
    Compute N-D inverse discrete Fourier Transform for real output.
    
    Parameters:
    - a: array_like, complex input array
    - s: sequence of ints, shape of output
    - axes: sequence of ints, axes over which to compute IFFT
    - norm: {None, 'ortho', 'forward', 'backward'}, normalization mode
    - plan: plan object (future use)
    
    Returns:
    ndarray: Real-valued N-D inverse FFT result
    """
```

### Hermitian FFTs

Transforms for Hermitian symmetric inputs.

```python { .api }
def fft.hfft(a, n=None, axis=-1, norm=None, plan=None):
    """
    Compute FFT of signal with Hermitian symmetry.
    
    Parameters:
    - a: array_like, input array with Hermitian symmetry
    - n: int, length of transformed axis
    - axis: int, axis over which to compute FFT
    - norm: {None, 'ortho', 'forward', 'backward'}, normalization mode
    - plan: plan object (future use)
    
    Returns:
    ndarray: Real-valued FFT result
    """

def fft.ihfft(a, n=None, axis=-1, norm=None, plan=None):
    """
    Compute inverse FFT of signal with Hermitian symmetry.
    
    Parameters:
    - a: array_like, real-valued input array
    - n: int, length of transformed axis
    - axis: int, axis over which to compute IFFT
    - norm: {None, 'ortho', 'forward', 'backward'}, normalization mode
    - plan: plan object (future use)
    
    Returns:
    ndarray: Complex-valued inverse FFT result
    """
```

### Helper Functions

Utility functions for working with FFT results.

```python { .api }
def fft.fftfreq(n, d=1.0):
    """
    Return discrete Fourier Transform sample frequencies.
    
    Parameters:
    - n: int, window length
    - d: scalar, sample spacing (inverse of sampling rate)
    
    Returns:
    ndarray: Sample frequencies
    """

def fft.rfftfreq(n, d=1.0):
    """
    Return sample frequencies for rfft.
    
    Parameters:
    - n: int, window length
    - d: scalar, sample spacing (inverse of sampling rate)
    
    Returns:
    ndarray: Sample frequencies for rfft
    """

def fft.fftshift(x, axes=None):
    """
    Shift zero-frequency component to center of array.
    
    Parameters:
    - x: array_like, input array
    - axes: int or shape tuple, axes over which to shift
    
    Returns:
    ndarray: Shifted array
    """

def fft.ifftshift(x, axes=None):
    """
    Inverse of fftshift.
    
    Parameters:
    - x: array_like, input array
    - axes: int or shape tuple, axes over which to shift
    
    Returns:
    ndarray: Shifted array
    """
```

## Usage Examples

### Basic 1D FFT

```python
import numpy as np

# Create a simple signal: sine wave + noise
fs = 500  # Sample rate
t = np.linspace(0, 1, fs)
signal = np.sin(2 * np.pi * 50 * t) + 0.5 * np.sin(2 * np.pi * 120 * t)
noise = 0.2 * np.random.normal(size=len(t))
noisy_signal = signal + noise

# Compute FFT
fft_result = np.fft.fft(noisy_signal)
frequencies = np.fft.fftfreq(len(noisy_signal), 1/fs)

# Get magnitude spectrum (first half due to symmetry)
magnitude = np.abs(fft_result[:len(fft_result)//2])
freq_positive = frequencies[:len(frequencies)//2]
```

### Real-valued FFT for Efficiency

```python
import numpy as np

# For real-valued signals, use rfft for efficiency
real_signal = np.cos(2 * np.pi * 10 * t) + np.sin(2 * np.pi * 20 * t)

# Real FFT (more efficient for real inputs)
rfft_result = np.fft.rfft(real_signal)
rfft_freqs = np.fft.rfftfreq(len(real_signal), 1/fs)

# Magnitude spectrum
magnitude_real = np.abs(rfft_result)

# Reconstruct original signal
reconstructed = np.fft.irfft(rfft_result)
```

### 2D FFT for Images

```python
import numpy as np

# Create a 2D signal (e.g., image with frequency content)
x = np.linspace(-5, 5, 100)
y = np.linspace(-5, 5, 100)
X, Y = np.meshgrid(x, y)
image = np.sin(2 * np.pi * X) * np.cos(2 * np.pi * Y)

# 2D FFT
fft2_result = np.fft.fft2(image)
fft2_shifted = np.fft.fftshift(fft2_result)  # Center zero frequency

# Magnitude spectrum
magnitude_2d = np.abs(fft2_shifted)
phase_2d = np.angle(fft2_shifted)

# Inverse transform
reconstructed_2d = np.fft.ifft2(fft2_result)
```

### Filtering in Frequency Domain

```python
import numpy as np

# Low-pass filtering example
def lowpass_filter(signal, cutoff_freq, sample_rate):
    # Compute FFT
    fft_signal = np.fft.fft(signal)
    frequencies = np.fft.fftfreq(len(signal), 1/sample_rate)
    
    # Create filter (zero out high frequencies)
    fft_filtered = fft_signal.copy()
    fft_filtered[np.abs(frequencies) > cutoff_freq] = 0
    
    # Inverse FFT to get filtered signal
    filtered_signal = np.fft.ifft(fft_filtered).real
    return filtered_signal

# Apply filter
fs = 1000
t = np.linspace(0, 1, fs)
noisy_signal = np.sin(2 * np.pi * 10 * t) + 0.5 * np.sin(2 * np.pi * 100 * t)
filtered = lowpass_filter(noisy_signal, cutoff_freq=50, sample_rate=fs)
```