# Measurements

Compute geometric properties and metrics of geometries including area, length, distance, and bounds. These functions provide quantitative analysis of spatial objects.

## Capabilities

### Area and Length

Compute area and perimeter measurements.

```python { .api }
def area(geometry, **kwargs):
    """
    Compute area of polygon geometries.
    
    Parameters:
    - geometry: input geometry or array of geometries
    
    Returns:
    float or ndarray: area (0 for non-polygonal geometries)
    """

def length(geometry, **kwargs):
    """
    Compute length of linear geometries or perimeter of polygonal geometries.
    
    Parameters:
    - geometry: input geometry or array of geometries
    
    Returns:
    float or ndarray: length/perimeter
    """
```

**Usage Example:**

```python
import shapely
from shapely.geometry import Point, LineString, Polygon

# Area measurements
square = Polygon([(0, 0), (2, 0), (2, 2), (0, 2)])
print(f"Square area: {shapely.area(square)}")  # 4.0

circle_approx = Point(0, 0).buffer(1.0)
print(f"Circle area: {shapely.area(circle_approx):.2f}")  # ~3.14

# Length measurements
line = LineString([(0, 0), (3, 4)])
print(f"Line length: {shapely.length(line)}")  # 5.0

print(f"Square perimeter: {shapely.length(square)}")  # 8.0
```

### Distance Measurements

Compute distances between geometries.

```python { .api }
def distance(a, b, **kwargs):
    """
    Compute minimum Cartesian distance between geometries.
    
    Parameters:
    - a: first geometry or array of geometries
    - b: second geometry or array of geometries
    
    Returns:
    float or ndarray: minimum distance (0 if geometries touch/overlap)
    """

def hausdorff_distance(a, b, densify=None, **kwargs):
    """
    Compute Hausdorff distance between geometries.
    
    Parameters:
    - a: first geometry or array of geometries
    - b: second geometry or array of geometries
    - densify: optional densification fraction
    
    Returns:
    float or ndarray: Hausdorff distance
    """

def frechet_distance(a, b, densify=None, **kwargs):
    """
    Compute Fréchet distance between geometries.
    
    Parameters:
    - a: first geometry or array of geometries
    - b: second geometry or array of geometries
    - densify: optional densification fraction
    
    Returns:
    float or ndarray: Fréchet distance
    """
```

**Usage Example:**

```python
import shapely
from shapely.geometry import Point, LineString

# Simple distance
point1 = Point(0, 0)
point2 = Point(3, 4)
print(f"Point distance: {shapely.distance(point1, point2)}")  # 5.0

# Distance to polygon
polygon = shapely.box(5, 5, 7, 7)
print(f"Distance to polygon: {shapely.distance(point1, polygon):.2f}")

# Advanced distance metrics
line1 = LineString([(0, 0), (1, 1)])
line2 = LineString([(0, 1), (1, 0)])
hausdorff = shapely.hausdorff_distance(line1, line2)
frechet = shapely.frechet_distance(line1, line2)
print(f"Hausdorff distance: {hausdorff:.2f}")
print(f"Fréchet distance: {frechet:.2f}")
```

### Bounds and Extents

Get bounding box information and spatial extents.

```python { .api }
def bounds(geometry, **kwargs):
    """
    Compute bounding box of geometry.
    
    Parameters:
    - geometry: input geometry or array of geometries
    
    Returns:
    ndarray: bounding box as [minx, miny, maxx, maxy] or array of boxes
    """

def total_bounds(geometry, **kwargs):
    """
    Compute total bounds of geometry array.
    
    Parameters:
    - geometry: array of geometries
    
    Returns:
    ndarray: total bounding box as [minx, miny, maxx, maxy]
    """
```

**Usage Example:**

```python
import shapely
import numpy as np

# Single geometry bounds
polygon = shapely.Polygon([(1, 2), (5, 2), (5, 6), (1, 6)])
bounds = shapely.bounds(polygon)
print(f"Bounds: {bounds}")  # [1, 2, 5, 6]

# Multiple geometries
geometries = [
    shapely.Point(0, 0),
    shapely.Point(10, 10),
    shapely.Polygon([(2, 2), (8, 2), (8, 8), (2, 8)])
]
all_bounds = shapely.bounds(geometries)
print(f"Individual bounds shape: {all_bounds.shape}")  # (3, 4)

total_bounds = shapely.total_bounds(geometries)
print(f"Total bounds: {total_bounds}")  # [0, 0, 10, 10]
```

### Specialized Measurements

Advanced geometric measurements and analysis.

```python { .api }
def minimum_clearance(geometry, **kwargs):
    """
    Compute minimum clearance distance (robustness measure).
    
    Parameters:
    - geometry: input geometry or array of geometries
    
    Returns:
    float or ndarray: minimum clearance distance
    """

def minimum_bounding_radius(geometry, **kwargs):
    """
    Compute radius of minimum bounding circle.
    
    Parameters:
    - geometry: input geometry or array of geometries
    
    Returns:
    float or ndarray: minimum bounding circle radius
    """
```

**Usage Example:**

```python
import shapely

# Create polygon with narrow feature
polygon = shapely.Polygon([
    (0, 0), (10, 0), (10, 1), (5, 1), (5, 0.1), (4.9, 0.1), (4.9, 1), (0, 1)
])

clearance = shapely.minimum_clearance(polygon)
print(f"Minimum clearance: {clearance}")  # Shows narrowest gap

# Bounding circle radius
circle_polygon = shapely.Point(0, 0).buffer(5.0)
radius = shapely.minimum_bounding_radius(circle_polygon)
print(f"Bounding radius: {radius:.1f}")  # ~5.0
```

### Array Operations

Efficient measurements on geometry arrays.

**Usage Example:**

```python
import shapely
import numpy as np

# Create array of random polygons
np.random.seed(42)
centers = np.random.rand(100, 2) * 10
radii = np.random.rand(100) * 0.5 + 0.1

polygons = [shapely.Point(x, y).buffer(r) for (x, y), r in zip(centers, radii)]

# Vectorized measurements
areas = shapely.area(polygons)
perimeters = shapely.length(polygons)
bounds_array = shapely.bounds(polygons)

print(f"Total area: {np.sum(areas):.2f}")
print(f"Average perimeter: {np.mean(perimeters):.2f}")
print(f"Overall bounds: {shapely.total_bounds(polygons)}")

# Distance matrix between first 5 polygons
first_five = polygons[:5]
distances = np.array([
    [shapely.distance(a, b) for b in first_five] 
    for a in first_five
])
print(f"Distance matrix shape: {distances.shape}")
```