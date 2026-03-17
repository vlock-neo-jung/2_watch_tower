# Shapely

Shapely is a Python package for manipulation and analysis of geometric objects in the Cartesian plane. It provides a comprehensive set of tools for creating, analyzing, and manipulating 2D and 3D geometric shapes, built on top of the industry-standard GEOS library.

## Package Information

- **Package Name**: shapely
- **Language**: Python
- **Installation**: `pip install shapely`

## Core Imports

```python
import shapely
```

Common patterns for specific functionality:

```python
from shapely.geometry import Point, LineString, Polygon
from shapely import affinity
import shapely.ops as ops
```

For array-based operations:

```python
import shapely
import numpy as np
```

## Basic Usage

```python
import shapely
from shapely.geometry import Point, LineString, Polygon

# Create geometries
point = Point(1, 1)
line = LineString([(0, 0), (1, 1), (2, 0)])
poly = Polygon([(0, 0), (2, 0), (2, 2), (0, 2)])

# Spatial predicates
print(poly.contains(point))  # True
print(line.intersects(poly))  # True

# Measurements
print(poly.area)  # 4.0
print(line.length)  # ~2.83

# Operations
buffered = point.buffer(0.5)
intersection = line.intersection(poly)

# Array-based operations for better performance
import numpy as np
points = shapely.points([(1, 1), (2, 2), (3, 3)])
boxes = shapely.box(0, 0, [1, 2, 3], [1, 2, 3])
areas = shapely.area(boxes)
```

## Architecture

Shapely provides two main APIs:

- **Object-oriented API**: Individual geometry objects with methods (`point.buffer(1.0)`)
- **Functional API**: Array-based operations for high performance (`shapely.buffer(geometries, 1.0)`)

Core geometry types form a hierarchy:
- **Base geometries**: Point, LineString, Polygon, LinearRing
- **Multi-geometries**: MultiPoint, MultiLineString, MultiPolygon
- **Collections**: GeometryCollection for mixed geometry types

All operations preserve coordinate precision and maintain topological consistency through the underlying GEOS library.

## Capabilities

### Core Geometry Classes

The fundamental geometry types that represent points, lines, polygons, and their multi-geometry collections.

```python { .api }
class Point:
    def __init__(self, x, y, z=None): ...

class LineString:
    def __init__(self, coordinates): ...
    
class Polygon:
    def __init__(self, shell, holes=None): ...

class MultiPoint:
    def __init__(self, points): ...

class MultiLineString:
    def __init__(self, linestrings): ...

class MultiPolygon:
    def __init__(self, polygons): ...

class GeometryCollection:
    def __init__(self, geometries): ...
```

[Geometry Classes](./geometry-classes.md)

### Creation Functions

High-performance functions for creating arrays of geometries from coordinate data.

```python { .api }
def points(coords, y=None, z=None, indices=None, *, handle_nan='allow', out=None, **kwargs): ...
def linestrings(coords, y=None, z=None, indices=None, *, handle_nan='allow', out=None, **kwargs): ...
def polygons(geometries, holes=None, indices=None, *, out=None, **kwargs): ...
def box(xmin, ymin, xmax, ymax, ccw=True, **kwargs): ...
```

[Creation Functions](./creation.md)

### Spatial Predicates

Boolean tests for spatial relationships and geometry properties.

```python { .api }
def contains(a, b, **kwargs) -> bool: ...
def intersects(a, b, **kwargs) -> bool: ...
def within(a, b, **kwargs) -> bool: ...
def touches(a, b, **kwargs) -> bool: ...
def is_valid(geometry, **kwargs) -> bool: ...
def is_empty(geometry, **kwargs) -> bool: ...
```

[Spatial Predicates](./predicates.md)

### Measurements

Compute geometric properties like area, length, distance, and bounds.

```python { .api }
def area(geometry, **kwargs): ...
def length(geometry, **kwargs): ...
def distance(a, b, **kwargs): ...
def bounds(geometry, **kwargs): ...
```

[Measurements](./measurements.md)

### Constructive Operations

Operations that create new geometries through transformation and analysis.

```python { .api }
def buffer(geometry, distance, quad_segs=8, cap_style='round', join_style='round', mitre_limit=5.0, single_sided=False, **kwargs): ...
def convex_hull(geometry, **kwargs): ...
def simplify(geometry, tolerance, preserve_topology=True, **kwargs): ...
def centroid(geometry, **kwargs): ...
```

[Constructive Operations](./constructive.md)

### Set Operations

Boolean operations combining geometries using union, intersection, and difference.

```python { .api }
def union(a, b, grid_size=None, **kwargs): ...
def intersection(a, b, grid_size=None, **kwargs): ...
def difference(a, b, grid_size=None, **kwargs): ...
def symmetric_difference(a, b, grid_size=None, **kwargs): ...
```

[Set Operations](./set-operations.md)

### Linear Operations

Specialized operations for working with linear geometries.

```python { .api }
def line_interpolate_point(line, distance, normalized=False, **kwargs): ...
def line_locate_point(line, point, normalized=False, **kwargs): ...
def line_merge(geometry, directed=False, **kwargs): ...
```

[Linear Operations](./linear.md)

### Coordinate Operations

Direct manipulation of coordinate arrays and coordinate transformations.

```python { .api }
def get_coordinates(geometry, include_z=False, include_m=False, return_index=False, **kwargs): ...
def set_coordinates(geometry, coordinates, include_z=None, **kwargs): ...
def transform(geometry, transformation, include_z=False, *, interleaved=True): ...
```

[Coordinate Operations](./coordinates.md)

### Input/Output

Convert geometries to and from standard formats like WKT, WKB, and GeoJSON.

```python { .api }
def to_wkt(geometry, rounding_precision=None, trim=True, output_dimension=None, old_3d=False, **kwargs): ...
def from_wkt(wkt, on_invalid='raise', **kwargs): ...
def to_geojson(geometry, indent=None, **kwargs): ...
def from_geojson(geojson, on_invalid='raise', **kwargs): ...
```

[Input/Output](./io.md)

### Affinity Transformations

Geometric transformations like rotation, scaling, translation, and skewing.

```python { .api }
def rotate(geom, angle, origin='center', use_radians=False): ...
def scale(geom, xfact=1.0, yfact=1.0, zfact=1.0, origin='center'): ...
def translate(geom, xoff=0.0, yoff=0.0, zoff=0.0): ...
```

[Affinity Transformations](./affinity.md)

### Spatial Indexing

R-tree spatial indexing for efficient spatial queries on large geometry collections.

```python { .api }
class STRtree:
    def __init__(self, geometries, node_capacity=10): ...
    def query(self, geometry, predicate=None): ...
    def nearest(self, geometry, max_distance=None, return_distance=False, exclusive=False): ...
```

[Spatial Indexing](./spatial-indexing.md)

### Geometry Introspection

Access and examine geometric properties, dimensions, coordinate information, and structure of geometry objects.

```python { .api }
def get_coordinate_dimension(geometry, **kwargs): ...
def get_dimensions(geometry, **kwargs): ...
def get_num_coordinates(geometry, **kwargs): ...
def get_num_geometries(geometry, **kwargs): ...
def get_parts(geometry, return_index=False): ...
def get_rings(geometry, return_index=False): ...
def get_type_id(geometry, **kwargs): ...
```

[Geometry Introspection](./geometry-introspection.md)

### Coverage Operations

Advanced operations for working with polygon coverages that share boundaries, requiring GEOS 3.12.0+.

```python { .api }
def coverage_is_valid(geometry, gap_width=0.0, **kwargs): ...
def coverage_invalid_edges(geometry, gap_width=0.0, **kwargs): ...
def coverage_simplify(geometry, tolerance, *, simplify_boundary=True, **kwargs): ...
def coverage_union(a, b, **kwargs): ...
def coverage_union_all(geometries, axis=None, **kwargs): ...
```

[Coverage Operations](./coverage-operations.md)

## Types

```python { .api }
# Base geometry type
class Geometry:
    @property
    def area(self) -> float: ...
    @property
    def bounds(self) -> tuple: ...
    @property
    def length(self) -> float: ...
    def buffer(self, distance: float, **kwargs) -> 'Geometry': ...
    def contains(self, other: 'Geometry') -> bool: ...
    def intersects(self, other: 'Geometry') -> bool: ...

# Enumerations
class GeometryType:
    MISSING = -1
    POINT = 0
    LINESTRING = 1
    LINEARRING = 2
    POLYGON = 3
    MULTIPOINT = 4
    MULTILINESTRING = 5
    MULTIPOLYGON = 6
    GEOMETRYCOLLECTION = 7

class BufferCapStyle:
    round = 1
    flat = 2
    square = 3

class BufferJoinStyle:
    round = 1
    mitre = 2
    bevel = 3

# I/O enumerations
class DecodingErrorOptions:
    ignore = 0
    warn = 1
    raise = 2
    fix = 3

class WKBFlavorOptions:
    extended = 1
    iso = 2

# Spatial indexing enumerations
class BinaryPredicate:
    intersects = 1
    within = 2
    contains = 3
    overlaps = 4
    crosses = 5
    touches = 6
    covers = 7
    covered_by = 8
    contains_properly = 9

# Precision handling enumerations
class SetPrecisionMode:
    valid_output = 0
    pointwise = 1
    keep_collapsed = 2

# Creation handling enumerations
class HandleNaN:
    allow = 0
    skip = 1
    error = 2
```