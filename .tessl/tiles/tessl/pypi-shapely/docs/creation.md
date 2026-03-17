# Creation Functions

High-performance functions for creating arrays of geometries from coordinate data. These functions are optimized for creating large numbers of geometries efficiently and support vectorized operations with NumPy arrays.

## Capabilities

### Point Creation

Create arrays of Point geometries from coordinate data.

```python { .api }
def points(coords, y=None, z=None, indices=None, *, handle_nan='allow', out=None, **kwargs):
    """
    Create an array of Point geometries.
    
    Parameters:
    - coords: array-like of coordinates, or x-coordinates if y is provided
    - y: array-like of y-coordinates (optional)
    - z: array-like of z-coordinates (optional)
    - indices: array-like of indices for coordinate grouping (optional)
    - handle_nan: how to handle NaN coordinates ('allow', 'skip', 'error')
    - out: output array (optional)
    
    Returns:
    ndarray of Point geometries
    """
```

**Usage Example:**

```python
import shapely
import numpy as np

# Create points from coordinate pairs
coords = [(0, 0), (1, 1), (2, 2)]
points = shapely.points(coords)

# Create points from separate x, y arrays
x = [0, 1, 2]
y = [0, 1, 2]
points = shapely.points(x, y)

# Create 3D points
x = [0, 1, 2]
y = [0, 1, 2] 
z = [0, 1, 2]
points_3d = shapely.points(x, y, z)

# Handle NaN coordinates
coords_with_nan = [(0, 0), (np.nan, np.nan), (2, 2)]
points = shapely.points(coords_with_nan, handle_nan='skip')
```

### LineString Creation

Create arrays of LineString geometries from coordinate sequences.

```python { .api }
def linestrings(coords, y=None, z=None, indices=None, *, handle_nan='allow', out=None, **kwargs):
    """
    Create an array of LineString geometries.
    
    Parameters:
    - coords: array-like of coordinate sequences
    - y: array-like of y-coordinates (optional)
    - z: array-like of z-coordinates (optional) 
    - indices: array-like of indices for coordinate grouping
    - handle_nan: how to handle NaN coordinates ('allow', 'skip', 'error')
    - out: output array (optional)
    
    Returns:
    ndarray of LineString geometries
    """
```

**Usage Example:**

```python
import shapely
import numpy as np

# Create linestrings from nested coordinate sequences
coords = [
    [(0, 0), (1, 1), (2, 0)],
    [(3, 0), (4, 1), (5, 0)]
]
lines = shapely.linestrings(coords)

# Create linestrings using indices for grouping
all_coords = [(0, 0), (1, 1), (2, 0), (3, 0), (4, 1), (5, 0)]
indices = [0, 0, 0, 1, 1, 1]  # Group coords into two linestrings
lines = shapely.linestrings(all_coords, indices=indices)
```

### LinearRing Creation

Create arrays of LinearRing geometries (closed linestrings).

```python { .api }
def linearrings(coords, y=None, z=None, indices=None, *, handle_nan='allow', out=None, **kwargs):
    """
    Create an array of LinearRing geometries.
    
    Parameters:
    - coords: array-like of coordinate sequences
    - y: array-like of y-coordinates (optional)
    - z: array-like of z-coordinates (optional)
    - indices: array-like of indices for coordinate grouping
    - handle_nan: how to handle NaN coordinates ('allow', 'skip', 'error')
    - out: output array (optional)
    
    Returns:
    ndarray of LinearRing geometries
    """
```

### Polygon Creation

Create arrays of Polygon geometries from shell and hole definitions.

```python { .api }
def polygons(geometries, holes=None, indices=None, *, out=None, **kwargs):
    """
    Create an array of Polygon geometries.
    
    Parameters:
    - geometries: array-like of LinearRing objects or coordinate sequences
    - holes: array-like of hole definitions (optional)
    - indices: array-like of indices for hole grouping
    - out: output array (optional)
    
    Returns:
    ndarray of Polygon geometries
    """
```

**Usage Example:**

```python
import shapely

# Create simple polygons from coordinate sequences
geometries = [
    [(0, 0), (2, 0), (2, 2), (0, 2)],  # Square
    [(3, 0), (5, 0), (4, 2)]           # Triangle
]
polygons = shapely.polygons(geometries)

# Create polygons with holes
geometries = [[(0, 0), (4, 0), (4, 4), (0, 4)]]  # Outer square
holes = [[(1, 1), (3, 1), (3, 3), (1, 3)]]   # Inner square hole
polygons_with_holes = shapely.polygons(geometries, holes)
```

### Box Creation

Create rectangular Polygon geometries from bounding coordinates.

```python { .api }
def box(xmin, ymin, xmax, ymax, ccw=True, **kwargs):
    """
    Create rectangular Polygon geometries.
    
    Parameters:
    - xmin: minimum x-coordinate(s)
    - ymin: minimum y-coordinate(s)
    - xmax: maximum x-coordinate(s)
    - ymax: maximum y-coordinate(s)
    - ccw: create counter-clockwise oriented polygons
    
    Returns:
    Polygon geometry or ndarray of Polygon geometries
    """
```

**Usage Example:**

```python
import shapely
import numpy as np

# Create single box
box = shapely.box(0, 0, 1, 1)

# Create multiple boxes
xmin = [0, 2, 4]
ymin = [0, 0, 0]
xmax = [1, 3, 5]
ymax = [1, 1, 1]
boxes = shapely.box(xmin, ymin, xmax, ymax)
```

### Multi-Geometry Creation

Create collections of geometries.

```python { .api }
def multipoints(geometries, indices=None, *, out=None, **kwargs):
    """Create MultiPoint geometries from Point arrays."""

def multilinestrings(geometries, indices=None, *, out=None, **kwargs):
    """Create MultiLineString geometries from LineString arrays."""

def multipolygons(geometries, indices=None, *, out=None, **kwargs):
    """Create MultiPolygon geometries from Polygon arrays."""

def geometrycollections(geometries, indices=None, out=None, **kwargs):
    """Create GeometryCollection geometries from mixed geometry arrays."""
```

**Usage Example:**

```python
import shapely

# Create individual geometries
points = shapely.points([(0, 0), (1, 1), (2, 2)])

# Group into multi-geometry
indices = [0, 0, 1]  # First two points in one MultiPoint, third in another
multipoints = shapely.multipoints(points, indices=indices)
```

### Empty Geometry Creation

Create arrays of empty geometries.

```python { .api }
def empty(shape, geom_type=None, order='C'):
    """
    Create an array of empty geometries.
    
    Parameters:
    - shape: shape of output array
    - geom_type: geometry type (optional, defaults to generic geometry)
    - order: array order ('C' for C-contiguous, 'F' for Fortran-contiguous)
    
    Returns:
    ndarray of empty geometries
    """
```

### Geometry Preparation

Prepare geometries for efficient repeated operations.

```python { .api }
def prepare(geometry, **kwargs):
    """
    Prepare geometries for efficient repeated spatial operations.
    
    Parameters:
    - geometry: geometry or array of geometries to prepare
    
    Returns:
    Prepared geometry objects
    """

def destroy_prepared(geometry, **kwargs):
    """
    Destroy prepared geometry data.
    
    Parameters:
    - geometry: prepared geometry to destroy
    """
```

**Usage Example:**

```python
import shapely

# Create and prepare geometry for efficient queries
polygon = shapely.box(0, 0, 10, 10)
prepared_poly = shapely.prepare(polygon)

# Now spatial queries against prepared_poly will be faster
points = shapely.points([(1, 1), (5, 5), (15, 15)])
contains_results = shapely.contains(prepared_poly, points)
```

## Types

```python { .api }
# Enumeration for NaN handling
class HandleNaN:
    allow = 0   # Allow NaN coordinates (default)
    skip = 1    # Skip NaN coordinates  
    error = 2   # Raise error on NaN coordinates
```