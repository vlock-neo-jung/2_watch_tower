# Input/Output Operations

File I/O operations for saving and loading array data in various formats. Supports both binary and text formats with options for compression and structured data handling.

## Capabilities

### Binary File Operations

Efficient binary storage and loading of NumPy arrays.

```python { .api }
def save(file, arr, allow_pickle=True, fix_imports=True):
    """
    Save array to binary file in NumPy .npy format.
    
    Parameters:
    - file: file, str, or pathlib.Path, file to write
    - arr: array_like, array to save
    - allow_pickle: bool, allow pickling of object arrays
    - fix_imports: bool, fix Python 2/3 compatibility
    
    Returns:
    None: Saves array to file
    """

def load(file, mmap_mode=None, allow_pickle=False, fix_imports=True, encoding='ASCII'):
    """
    Load arrays from .npy, .npz or pickled files.
    
    Parameters:
    - file: file, str, or pathlib.Path, file to read
    - mmap_mode: {None, 'r+', 'r', 'w+', 'c'}, memory-map mode
    - allow_pickle: bool, allow loading pickled object arrays
    - fix_imports: bool, fix Python 2/3 compatibility
    - encoding: str, encoding for ASCII strings
    
    Returns:
    ndarray or NpzFile: Loaded array(s)
    """

def savez(file, *args, **kwds):
    """
    Save several arrays into single uncompressed .npz file.
    
    Parameters:
    - file: str or file, output file
    - *args: array_like, arrays to save
    - **kwds: array_like, arrays to save with keyword names
    
    Returns:
    None: Saves arrays to npz file
    """

def savez_compressed(file, *args, **kwds):
    """
    Save several arrays into single compressed .npz file.
    
    Parameters:
    - file: str or file, output file
    - *args: array_like, arrays to save
    - **kwds: array_like, arrays to save with keyword names
    
    Returns:
    None: Saves arrays to compressed npz file
    """
```

### Text File Operations

Human-readable text format I/O operations.

```python { .api }
def loadtxt(fname, dtype=float, comments='#', delimiter=None, converters=None, 
           skiprows=0, usecols=None, unpack=False, ndmin=0, encoding='bytes', 
           max_rows=None, like=None):
    """
    Load data from text file.
    
    Parameters:
    - fname: file, str, or pathlib.Path, file to read
    - dtype: data-type, data type of array
    - comments: str or sequence, comment character(s)
    - delimiter: str, field delimiter
    - converters: dict, column conversion functions
    - skiprows: int, number of rows to skip
    - usecols: int or sequence, columns to read
    - unpack: bool, return separate arrays for columns
    - ndmin: int, minimum number of dimensions
    - encoding: str, encoding to decode input
    - max_rows: int, maximum rows to read
    - like: array_like, reference object
    
    Returns:
    ndarray: Data read from text file
    """

def savetxt(fname, X, fmt='%.18e', delimiter=' ', newline='\n', header='', 
           footer='', comments='# ', encoding=None):
    """
    Save array to text file.
    
    Parameters:
    - fname: filename or file handle, output file
    - X: 1-D or 2-D array_like, data to save
    - fmt: str or sequence of strs, format for each column
    - delimiter: str, string or character separating columns
    - newline: str, string separating lines
    - header: str, string written at beginning of file
    - footer: str, string written at end of file
    - comments: str, string prepended to header and footer
    - encoding: {None, str}, encoding for output
    
    Returns:
    None: Saves array to text file
    """

def genfromtxt(fname, dtype=float, comments='#', delimiter=None, skip_header=0,
              skip_footer=0, converters=None, missing_values=None, filling_values=None,
              usecols=None, names=None, excludelist=None, deletechars=None,
              defaultfmt="f%i", autostrip=False, replace_space='_', case_sensitive=True,
              unpack=None, invalid_raise=True, max_rows=None, encoding='bytes', like=None):
    """
    Load data from text file, handling missing values.
    
    Parameters:
    - fname: file, str, list, or generator, input data
    - dtype: numpy data type, data type of array
    - comments: str, comment character
    - delimiter: str, field separator
    - skip_header: int, number of lines to skip from beginning
    - skip_footer: int, number of lines to skip from end
    - converters: dict, column converters
    - missing_values: set of str, strings indicating missing data
    - filling_values: scalar or dict, values for missing data
    - usecols: sequence, columns to read
    - names: {None, True, str, sequence}, field names for structured array
    - excludelist: sequence, names of fields to exclude
    - deletechars: str, characters to remove from field names
    - defaultfmt: str, default format for field names
    - autostrip: bool, automatically strip whitespace
    - replace_space: str, character to replace spaces in field names
    - case_sensitive: bool, case sensitivity for field names
    - unpack: bool, return separate arrays for columns
    - invalid_raise: bool, raise exception on inconsistent data
    - max_rows: int, maximum rows to read
    - encoding: str, encoding to decode input
    - like: array_like, reference object
    
    Returns:
    ndarray: Data from text file with missing value handling
    """

def fromregex(file, regexp, dtype, encoding=None):
    """
    Construct array from text file using regular expression parsing.
    
    Parameters:
    - file: file or str, input file
    - regexp: str or regexp, regular expression
    - dtype: data-type, data type for array
    - encoding: str, encoding to decode input
    
    Returns:
    ndarray: Array constructed from regex parsing
    """
```

### Binary Data Construction

Create arrays from various binary data sources.

```python { .api }
def frombuffer(buffer, dtype=float, count=-1, offset=0, like=None):
    """
    Interpret buffer as 1-D array.
    
    Parameters:
    - buffer: buffer_like, object exposing buffer interface
    - dtype: data-type, data type of array
    - count: int, number of items to read (-1 for all)
    - offset: int, start reading from this offset
    - like: array_like, reference object
    
    Returns:
    ndarray: 1-D array from buffer
    """

def fromfile(file, dtype=float, count=-1, sep='', offset=0, like=None):
    """
    Construct array from data in text or binary file.
    
    Parameters:
    - file: file or str, input file
    - dtype: data-type, data type of returned array
    - count: int, number of items to read (-1 for all)
    - sep: str, separator between items ('' for binary)
    - offset: int, offset in bytes from current position
    - like: array_like, reference object
    
    Returns:
    ndarray: Array from file data
    """

def fromstring(string, dtype=float, count=-1, sep='', like=None):
    """
    Create array from string data.
    
    Parameters:
    - string: str, string containing array data
    - dtype: data-type, data type of array
    - count: int, number of items to read (-1 for all)
    - sep: str, separator between items
    - like: array_like, reference object
    
    Returns:
    ndarray: Array from string data
    """

def fromiter(iterable, dtype, count=-1, like=None):
    """
    Create array from iterable object.
    
    Parameters:
    - iterable: iterable, object to convert to array
    - dtype: data-type, data type of returned array
    - count: int, number of items to read (-1 for all)
    - like: array_like, reference object
    
    Returns:
    ndarray: Array from iterable
    """
```

### Bit Packing Operations

Pack and unpack binary data.

```python { .api }
def packbits(a, axis=None, bitorder='big'):
    """
    Pack elements of uint8 array into bits in uint8 array.
    
    Parameters:
    - a: array_like, input array of integers or booleans
    - axis: int, dimension over which to pack bits
    - bitorder: {'big', 'little'}, bit order within bytes
    
    Returns:
    ndarray: Packed array
    """

def unpackbits(a, axis=None, count=None, bitorder='big'):
    """
    Unpack elements of uint8 array into binary-valued output array.
    
    Parameters:
    - a: ndarray, input array (uint8 type)
    - axis: int, dimension over which to unpack bits
    - count: int, number of elements to unpack
    - bitorder: {'big', 'little'}, bit order within bytes
    
    Returns:
    ndarray: Unpacked array with binary values
    """
```

### Memory Mapping

Memory-mapped file access for large arrays.

```python { .api }
class memmap(ndarray):
    """
    Create memory-map to array stored in binary file on disk.
    
    Parameters:
    - filename: str, pathlib.Path, or file object, file name
    - dtype: data-type, data type of array
    - mode: {'r+', 'r', 'w+', 'c'}, file access mode
    - offset: int, offset in bytes from beginning of file
    - shape: tuple, shape of array
    - order: {'C', 'F'}, row or column major order
    
    Returns:
    memmap: Memory-mapped array
    """
    def __new__(subtype, filename, dtype=float, mode='r+', offset=0, shape=None, order='C'): ...
```

## Usage Examples

### Basic File Operations

```python
import numpy as np

# Create sample data
data = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])

# Save to binary format (.npy)
np.save('data.npy', data)

# Load from binary format
loaded_data = np.load('data.npy')

# Save multiple arrays to compressed file
extra_data = np.array([10, 20, 30])
np.savez_compressed('multiple_arrays.npz', main=data, extra=extra_data)

# Load from npz file
with np.load('multiple_arrays.npz') as npz_file:
    main_array = npz_file['main']
    extra_array = npz_file['extra']
```

### Text File Operations

```python
import numpy as np

# Sample data
data = np.array([[1.1, 2.2, 3.3],
                 [4.4, 5.5, 6.6],
                 [7.7, 8.8, 9.9]])

# Save to text file
np.savetxt('data.txt', data, fmt='%.2f', delimiter=',', 
           header='col1,col2,col3', comments='')

# Load from text file
loaded_text = np.loadtxt('data.txt', delimiter=',', skiprows=1)

# Load CSV with headers and missing values
csv_data = """# Weather data
# Date,Temperature,Humidity,Pressure
2023-01-01,22.5,65,1013.2
2023-01-02,,70,1015.8
2023-01-03,25.1,NaN,1012.4"""

with open('weather.csv', 'w') as f:
    f.write(csv_data)

# Load with missing value handling
weather = np.genfromtxt('weather.csv', delimiter=',', skip_header=2,
                       missing_values=['', 'NaN'], filling_values=np.nan,
                       usecols=(1, 2, 3))
```

### Working with Large Files

```python
import numpy as np

# Create large array for demonstration
large_data = np.random.random((1000, 1000))
np.save('large_data.npy', large_data)

# Use memory mapping for large files (doesn't load into memory)
mmapped = np.load('large_data.npy', mmap_mode='r')

# Access parts of the array without loading everything
subset = mmapped[100:200, 200:300]  # Only loads needed section
row_sum = np.sum(mmapped[0, :])     # Efficient row operations

# Create memory-mapped array directly
mmap_array = np.memmap('temp_mmap.dat', dtype='float32', mode='w+', shape=(1000, 1000))
mmap_array[:] = np.random.random((1000, 1000)).astype('float32')
mmap_array.flush()  # Ensure data is written to disk
```

### Binary Data Handling

```python
import numpy as np

# Pack bits for efficient storage
binary_data = np.array([0, 1, 1, 0, 1, 0, 0, 1], dtype=np.uint8)
packed = np.packbits(binary_data)  # Pack 8 bits into 1 byte

# Unpack bits
unpacked = np.unpackbits(packed)

# Create array from buffer (e.g., from bytes)
byte_data = b'\x01\x02\x03\x04'
from_buffer = np.frombuffer(byte_data, dtype=np.uint8)

# Create array from iterator
squares = np.fromiter((x**2 for x in range(10)), dtype=int)
```