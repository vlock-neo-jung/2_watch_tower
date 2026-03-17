# Spatial Predicates

Boolean tests for spatial relationships between geometries and properties of individual geometries. These functions support both individual geometry objects and arrays of geometries for vectorized operations.

## Capabilities

### Binary Spatial Predicates

Test spatial relationships between two geometries.

```python { .api }
def contains(a, b, **kwargs) -> bool:
    """
    Test if geometry A contains geometry B.
    
    Parameters:
    - a: first geometry or array of geometries
    - b: second geometry or array of geometries
    
    Returns:
    bool or ndarray of bool
    """

def intersects(a, b, **kwargs) -> bool:
    """
    Test if geometry A intersects geometry B.
    
    Parameters:
    - a: first geometry or array of geometries
    - b: second geometry or array of geometries
    
    Returns:
    bool or ndarray of bool
    """

def within(a, b, **kwargs) -> bool:
    """
    Test if geometry A is within geometry B.
    
    Parameters:
    - a: first geometry or array of geometries
    - b: second geometry or array of geometries
    
    Returns:
    bool or ndarray of bool
    """

def touches(a, b, **kwargs) -> bool:
    """
    Test if geometry A touches geometry B.
    
    Parameters:
    - a: first geometry or array of geometries
    - b: second geometry or array of geometries
    
    Returns:
    bool or ndarray of bool
    """

def crosses(a, b, **kwargs) -> bool:
    """
    Test if geometry A crosses geometry B.
    
    Parameters:
    - a: first geometry or array of geometries
    - b: second geometry or array of geometries
    
    Returns:
    bool or ndarray of bool
    """

def overlaps(a, b, **kwargs) -> bool:
    """
    Test if geometry A overlaps geometry B.
    
    Parameters:
    - a: first geometry or array of geometries
    - b: second geometry or array of geometries
    
    Returns:
    bool or ndarray of bool
    """

def disjoint(a, b, **kwargs) -> bool:
    """
    Test if geometry A is disjoint from geometry B.
    
    Parameters:
    - a: first geometry or array of geometries
    - b: second geometry or array of geometries
    
    Returns:
    bool or ndarray of bool
    """

def equals(a, b, **kwargs) -> bool:
    """
    Test if geometry A equals geometry B spatially.
    
    Parameters:
    - a: first geometry or array of geometries
    - b: second geometry or array of geometries
    
    Returns:
    bool or ndarray of bool
    """
```

**Usage Example:**

```python
import shapely
from shapely.geometry import Point, Polygon

# Individual geometries
point = Point(1, 1)
polygon = Polygon([(0, 0), (2, 0), (2, 2), (0, 2)])

print(polygon.contains(point))  # True
print(point.within(polygon))    # True
print(polygon.intersects(point)) # True

# Array operations
points = shapely.points([(1, 1), (3, 3), (0.5, 0.5)])
contains_results = shapely.contains(polygon, points)
print(contains_results)  # [True, False, True]
```

### Advanced Binary Predicates

More specialized spatial relationship tests.

```python { .api }
def contains_properly(a, b, **kwargs) -> bool:
    """
    Test if geometry A properly contains geometry B.
    B is properly contained if it is contained and does not touch the boundary of A.
    
    Parameters:
    - a: first geometry or array of geometries
    - b: second geometry or array of geometries
    
    Returns:
    bool or ndarray of bool
    """

def covers(a, b, **kwargs) -> bool:
    """
    Test if geometry A covers geometry B.
    
    Parameters:
    - a: first geometry or array of geometries  
    - b: second geometry or array of geometries
    
    Returns:
    bool or ndarray of bool
    """

def covered_by(a, b, **kwargs) -> bool:
    """
    Test if geometry A is covered by geometry B.
    
    Parameters:
    - a: first geometry or array of geometries
    - b: second geometry or array of geometries
    
    Returns:
    bool or ndarray of bool
    """

def equals_exact(a, b, tolerance=0.0, *, normalize=False, **kwargs) -> bool:
    """
    Test if geometry A equals geometry B exactly within tolerance.
    
    Parameters:
    - a: first geometry or array of geometries
    - b: second geometry or array of geometries
    - tolerance: coordinate tolerance for comparison
    - normalize: normalize geometries before comparison
    
    Returns:
    bool or ndarray of bool
    """

def dwithin(a, b, distance, **kwargs) -> bool:
    """
    Test if geometry A is within distance of geometry B.
    
    Parameters:
    - a: first geometry or array of geometries
    - b: second geometry or array of geometries
    - distance: maximum distance
    
    Returns:
    bool or ndarray of bool
    """
```

### Point-in-Geometry Tests

Efficient tests for point containment without creating Point objects.

```python { .api }
def contains_xy(geometry, x, y=None, **kwargs) -> bool:
    """
    Test if geometry contains points at coordinates (x, y).
    
    Parameters:
    - geometry: geometry or array of geometries
    - x: x-coordinate(s) or array of (x, y) coordinates
    - y: y-coordinate(s) (optional if x contains both coordinates)
    
    Returns:
    bool or ndarray of bool
    """

def intersects_xy(geometry, x, y=None, **kwargs) -> bool:
    """
    Test if geometry intersects points at coordinates (x, y).
    
    Parameters:
    - geometry: geometry or array of geometries
    - x: x-coordinate(s) or array of (x, y) coordinates
    - y: y-coordinate(s) (optional if x contains both coordinates)
    
    Returns:
    bool or ndarray of bool
    """
```

**Usage Example:**

```python
import shapely

# Create polygon
polygon = shapely.box(0, 0, 2, 2)

# Test multiple points efficiently
x_coords = [1, 3, 0.5]
y_coords = [1, 3, 0.5]
results = shapely.contains_xy(polygon, x_coords, y_coords)
print(results)  # [True, False, True]

# Alternative syntax with coordinate pairs
coords = [(1, 1), (3, 3), (0.5, 0.5)]
results = shapely.contains_xy(polygon, coords)
```

### Geometry Property Tests

Test properties of individual geometries.

```python { .api }
def is_empty(geometry, **kwargs) -> bool:
    """Test if geometry is empty."""

def is_valid(geometry, **kwargs) -> bool:
    """Test if geometry is topologically valid."""

def is_simple(geometry, **kwargs) -> bool:
    """Test if geometry is simple (no self-intersections)."""

def is_closed(geometry, **kwargs) -> bool:
    """Test if linestring geometry is closed."""

def is_ring(geometry, **kwargs) -> bool:
    """Test if linestring is a valid ring (closed and simple)."""

def is_ccw(geometry, **kwargs) -> bool:
    """Test if ring is oriented counter-clockwise."""

def has_z(geometry, **kwargs) -> bool:
    """Test if geometry has Z (3D) coordinates."""

def has_m(geometry, **kwargs) -> bool:
    """Test if geometry has M (measure) coordinates. Requires GEOS 3.12.0+."""
```

**Usage Example:**

```python
import shapely
from shapely.geometry import LineString, Polygon

# Test line properties
line = LineString([(0, 0), (1, 1), (2, 0)])
print(shapely.is_simple(line))  # True
print(shapely.is_closed(line))  # False

# Test polygon validity
valid_poly = Polygon([(0, 0), (1, 0), (1, 1), (0, 1)])
invalid_poly = Polygon([(0, 0), (1, 1), (1, 0), (0, 1)])  # Self-intersecting
print(shapely.is_valid(valid_poly))    # True
print(shapely.is_valid(invalid_poly))  # False
```

### Object Type Tests

Test object types and states.

```python { .api }
def is_geometry(obj, **kwargs) -> bool:
    """Test if object is a geometry."""

def is_missing(obj, **kwargs) -> bool:
    """Test if object is None/missing."""

def is_valid_input(obj, **kwargs) -> bool:
    """Test if object is valid geometry input (geometry or None)."""

def is_prepared(geometry, **kwargs) -> bool:
    """Test if geometry is prepared for efficient operations."""
```

### Validity Analysis

Get detailed information about geometry validity.

```python { .api }
def is_valid_reason(geometry, **kwargs) -> str:
    """
    Get reason why geometry is invalid.
    
    Parameters:
    - geometry: geometry or array of geometries
    
    Returns:
    str or ndarray of str: reason for invalidity, or "Valid Geometry" if valid
    """
```

**Usage Example:**

```python
import shapely
from shapely.geometry import Polygon

# Create invalid polygon (self-intersecting)
invalid_poly = Polygon([(0, 0), (2, 2), (2, 0), (0, 2)])

print(shapely.is_valid(invalid_poly))  # False
print(shapely.is_valid_reason(invalid_poly))  # "Self-intersection[1 1]"
```

### Topological Relations

Get detailed topological relationship information.

```python { .api }
def relate(a, b, **kwargs) -> str:
    """
    Get DE-9IM intersection matrix string describing relationship between A and B.
    
    Parameters:
    - a: first geometry or array of geometries
    - b: second geometry or array of geometries
    
    Returns:
    str or ndarray of str: DE-9IM matrix string
    """

def relate_pattern(a, b, pattern, **kwargs) -> bool:
    """
    Test if relationship between A and B matches DE-9IM pattern.
    
    Parameters:
    - a: first geometry or array of geometries
    - b: second geometry or array of geometries
    - pattern: DE-9IM pattern string to match
    
    Returns:
    bool or ndarray of bool
    """
```

**Usage Example:**

```python
import shapely
from shapely.geometry import Point, Polygon

point = Point(1, 1)
polygon = Polygon([(0, 0), (2, 0), (2, 2), (0, 2)])

# Get full topological relationship
matrix = shapely.relate(point, polygon)
print(matrix)  # "0FFFFF212"

# Test specific pattern
is_inside = shapely.relate_pattern(point, polygon, "0FFFFF212")
print(is_inside)  # True
```