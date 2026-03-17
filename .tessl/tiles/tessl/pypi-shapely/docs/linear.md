# Linear Operations

Operations specialized for working with linear geometries like LineStrings and LinearRings. These functions provide capabilities for interpolation, location, merging, and analysis of linear features.

## Capabilities

### Line Interpolation and Location

Find points along lines and locate points on lines.

```python { .api }
def line_interpolate_point(line, distance, normalized=False, **kwargs):
    """
    Interpolate a point along a line at specified distance.
    
    Parameters:
    - line: input LineString geometry or array of LineStrings
    - distance: distance along line (or fraction if normalized=True)
    - normalized: if True, distance is fraction of total length (0.0 to 1.0)
    
    Returns:
    Point geometry or array of Points
    """

def line_locate_point(line, point, normalized=False, **kwargs):
    """
    Locate the distance of a point along a line.
    
    Parameters:
    - line: input LineString geometry or array of LineStrings
    - point: Point geometry to locate on line
    - normalized: if True, return fraction of total length
    
    Returns:
    float or ndarray: distance along line
    """
```

**Usage Example:**

```python
import shapely
from shapely.geometry import LineString, Point

# Create a line
line = LineString([(0, 0), (10, 0), (10, 10)])

# Interpolate points along line
point_at_5 = shapely.line_interpolate_point(line, 5.0)
point_at_half = shapely.line_interpolate_point(line, 0.5, normalized=True)

print(f"Point at distance 5: {point_at_5}")
print(f"Point at 50% of length: {point_at_half}")

# Locate existing point on line
test_point = Point(10, 5)
distance = shapely.line_locate_point(line, test_point)
fraction = shapely.line_locate_point(line, test_point, normalized=True)

print(f"Test point distance: {distance}")
print(f"Test point fraction: {fraction:.2f}")
```

### Line Merging

Combine connected linear features into longer lines.

```python { .api }
def line_merge(geometry, directed=False, **kwargs):
    """
    Merge connected LineStrings into longer LineStrings.
    
    Parameters:
    - geometry: LineString, MultiLineString, or array of linear geometries
    - directed: if True, only merge lines with same direction
    
    Returns:
    LineString, MultiLineString, or array: merged line geometry
    """
```

**Usage Example:**

```python
import shapely
from shapely.geometry import LineString, MultiLineString

# Create connected line segments
line1 = LineString([(0, 0), (1, 1)])
line2 = LineString([(1, 1), (2, 0)])
line3 = LineString([(2, 0), (3, 1)])

# Combine into MultiLineString
multi_line = MultiLineString([line1, line2, line3])

# Merge connected segments
merged = shapely.line_merge(multi_line)
print(f"Original segments: {len(multi_line.geoms)}")
print(f"Merged geometry type: {merged.geom_type}")
print(f"Merged coordinates: {list(merged.coords)}")
```

### Shared Paths

Find common segments between linear geometries.

```python { .api }
def shared_paths(a, b, **kwargs):
    """
    Find shared paths between two linear geometries.
    
    Parameters:
    - a: first linear geometry
    - b: second linear geometry
    
    Returns:
    GeometryCollection: shared path segments
    """
```

### Shortest Line

Find shortest connecting line between geometries.

```python { .api }
def shortest_line(a, b, **kwargs):
    """
    Find shortest line connecting two geometries.
    
    Parameters:
    - a: first geometry
    - b: second geometry
    
    Returns:
    LineString: shortest connecting line
    """
```

**Usage Example:**

```python
import shapely
from shapely.geometry import Point, Polygon

# Find shortest line between geometries
point = Point(0, 0)
polygon = Polygon([(5, 2), (8, 2), (8, 5), (5, 5)])

shortest = shapely.shortest_line(point, polygon)
print(f"Shortest line length: {shortest.length:.2f}")
print(f"Shortest line coords: {list(shortest.coords)}")

# Verify this matches the distance
distance = shapely.distance(point, polygon)
print(f"Distance matches line length: {abs(shortest.length - distance) < 1e-10}")
```