# Coordinate Operations

Direct manipulation and analysis of coordinate arrays that make up geometries. These functions provide efficient access to the underlying coordinate data and coordinate transformations.

## Capabilities

### Coordinate Access

Extract and manipulate coordinate arrays from geometries.

```python { .api }
def get_coordinates(geometry, include_z=False, include_m=False, return_index=False, **kwargs):
    """
    Get coordinate array from geometry.
    
    Parameters:
    - geometry: input geometry or array of geometries
    - include_z: include Z coordinates in output
    - include_m: include M coordinates in output  
    - return_index: also return indices mapping coordinates to geometries
    
    Returns:
    ndarray: coordinate array, optionally with indices
    """

def set_coordinates(geometry, coordinates, include_z=None, **kwargs):
    """
    Set coordinates of geometry (modifies geometry in-place).
    
    Parameters:
    - geometry: input geometry or array of geometries
    - coordinates: new coordinate array
    - include_z: whether coordinates include Z dimension
    
    Returns:
    Geometry or array: modified geometry (same object)
    """

def count_coordinates(geometry, **kwargs):
    """
    Count number of coordinates in geometry.
    
    Parameters:
    - geometry: input geometry or array of geometries
    
    Returns:
    int or ndarray: coordinate count
    """
```

**Usage Example:**

```python
import shapely
import numpy as np
from shapely.geometry import LineString, Polygon

# Extract coordinates from geometry
line = LineString([(0, 0), (1, 1), (2, 0)])
coords = shapely.get_coordinates(line)
print(f"Line coordinates:\n{coords}")

# Count coordinates
count = shapely.count_coordinates(line)
print(f"Coordinate count: {count}")

# Modify coordinates
new_coords = coords * 2  # Scale by 2
shapely.set_coordinates(line, new_coords)
print(f"Modified line: {line}")

# Work with 3D coordinates
line_3d = LineString([(0, 0, 0), (1, 1, 1), (2, 0, 2)])
coords_3d = shapely.get_coordinates(line_3d, include_z=True)
print(f"3D coordinates shape: {coords_3d.shape}")
```

### Coordinate Transformations

Apply custom transformations to coordinate data.

```python { .api }
def transform(geometry, transformation, include_z=False, *, interleaved=True):
    """
    Apply coordinate transformation to geometry.
    
    Parameters:
    - geometry: input geometry or array of geometries
    - transformation: transformation function (x, y[, z]) -> (x', y'[, z'])
    - include_z: whether to include Z coordinates in transformation
    - interleaved: whether coordinates are interleaved (x, y, x, y, ...)
    
    Returns:
    Geometry or array: transformed geometry
    """
```

**Usage Example:**

```python
import shapely
import numpy as np
from shapely.geometry import Point, Polygon

# Define transformation function (rotate 45 degrees)
def rotate_45(x, y):
    cos_a = np.cos(np.pi/4)
    sin_a = np.sin(np.pi/4)
    x_new = x * cos_a - y * sin_a
    y_new = x * sin_a + y * cos_a
    return x_new, y_new

# Apply transformation
square = Polygon([(0, 0), (1, 0), (1, 1), (0, 1)])
rotated_square = shapely.transform(square, rotate_45)

print(f"Original area: {square.area}")
print(f"Rotated area: {rotated_square.area:.6f}")  # Should be same
print(f"Areas equal: {abs(square.area - rotated_square.area) < 1e-10}")

# Transform with projection (example: simple scaling)
def scale_transform(x, y):
    return x * 1000, y * 2000  # Scale to different units

point = Point(1.5, 2.5)
scaled_point = shapely.transform(point, scale_transform)
print(f"Original point: {point}")
print(f"Scaled point: {scaled_point}")
```

### Array-Based Operations

Efficient coordinate operations on geometry arrays.

**Usage Example:**

```python
import shapely
import numpy as np

# Create array of geometries
np.random.seed(42)
points = shapely.points(np.random.rand(100, 2) * 10)

# Get all coordinates at once
all_coords = shapely.get_coordinates(points)
print(f"All coordinates shape: {all_coords.shape}")

# Count coordinates for each geometry
coord_counts = shapely.count_coordinates(points)
print(f"Coordinate counts (should all be 1): {np.unique(coord_counts)}")

# Apply transformation to entire array
def shift_transform(x, y):
    return x + 100, y + 200

shifted_points = shapely.transform(points, shift_transform)

# Verify transformation
original_bounds = shapely.total_bounds(points)
shifted_bounds = shapely.total_bounds(shifted_points)
print(f"Original bounds: {original_bounds}")
print(f"Shifted bounds: {shifted_bounds}")
print(f"Shift correct: {np.allclose(shifted_bounds - original_bounds, [100, 200, 100, 200])}")
```

### Advanced Coordinate Manipulation

Working with complex coordinate structures and indices.

**Usage Example:**

```python
import shapely
from shapely.geometry import MultiLineString

# Create complex geometry with multiple parts
lines = [
    [(0, 0), (1, 1)],
    [(2, 2), (3, 3), (4, 4)],
    [(5, 5), (6, 6), (7, 7), (8, 8)]
]
multi_line = MultiLineString(lines)

# Get coordinates with indices
coords, indices = shapely.get_coordinates(multi_line, return_index=True)
print(f"Total coordinates: {len(coords)}")
print(f"Indices: {indices}")
print(f"Coordinates per geometry: {np.bincount(indices)}")

# Modify specific geometry's coordinates
# Find coordinates belonging to first geometry (index 0)
mask = indices == 0
first_geom_coords = coords[mask]
print(f"First geometry coordinates:\n{first_geom_coords}")

# Scale just the first geometry
new_coords = coords.copy()
new_coords[mask] *= 2

# Create new geometry with modified coordinates
new_multi_line = shapely.set_coordinates(multi_line, new_coords)
print(f"Modified geometry: {new_multi_line}")
```