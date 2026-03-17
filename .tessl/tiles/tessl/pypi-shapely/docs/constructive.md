# Constructive Operations

Operations that create new geometries through geometric analysis, transformation, and construction. These functions generate derived geometries from input geometries while preserving topological relationships.

## Capabilities

### Buffer Operations

Create buffer zones around geometries.

```python { .api }
def buffer(geometry, distance, quad_segs=8, cap_style='round', join_style='round', mitre_limit=5.0, single_sided=False, **kwargs):
    """
    Create buffer around geometry.
    
    Parameters:
    - geometry: input geometry or array of geometries
    - distance: buffer distance (positive for outward, negative for inward)
    - quad_segs: number of segments for quarter-circle approximation
    - cap_style: end cap style ('round', 'flat', 'square')
    - join_style: join style ('round', 'mitre', 'bevel')
    - mitre_limit: mitre ratio limit for mitre joins
    - single_sided: create single-sided buffer
    
    Returns:
    Buffered geometry or array of geometries
    """
```

**Usage Example:**

```python
import shapely
from shapely.geometry import Point, LineString

# Buffer a point (creates circle)
point = Point(0, 0)
circle = shapely.buffer(point, 1.0)
print(f"Circle area: {circle.area:.2f}")  # ~3.14

# Buffer a line with different cap styles
line = LineString([(0, 0), (2, 0)])
rounded_buffer = shapely.buffer(line, 0.5, cap_style='round')
flat_buffer = shapely.buffer(line, 0.5, cap_style='flat')
square_buffer = shapely.buffer(line, 0.5, cap_style='square')

# Negative buffer (shrink)
polygon = shapely.box(0, 0, 4, 4)
smaller = shapely.buffer(polygon, -0.5)
```

### Hull Operations

Compute convex and concave hulls.

```python { .api }
def convex_hull(geometry, **kwargs):
    """
    Compute convex hull of geometry.
    
    Parameters:
    - geometry: input geometry or array of geometries
    
    Returns:
    Convex hull geometry
    """

def concave_hull(geometry, ratio, allow_holes=False, **kwargs):
    """
    Compute concave hull (alpha shape) of geometry.
    Requires GEOS 3.11+.
    
    Parameters:
    - geometry: input geometry or array of geometries
    - ratio: length ratio for concaveness (0=convex hull, 1=very concave)
    - allow_holes: whether to allow holes in result
    
    Returns:
    Concave hull geometry
    """
```

**Usage Example:**

```python
import shapely
import numpy as np

# Create scattered points
np.random.seed(42)
coords = np.random.rand(20, 2) * 10
points = shapely.multipoints([coords])

# Compute hulls
convex = shapely.convex_hull(points)
concave = shapely.concave_hull(points, ratio=0.3, allow_holes=False)

print(f"Convex hull area: {convex.area:.2f}")
print(f"Concave hull area: {concave.area:.2f}")
```

### Geometric Centers and Representatives

Find representative points and centers.

```python { .api }
def centroid(geometry, **kwargs):
    """
    Compute geometric centroid of geometry.
    
    Parameters:
    - geometry: input geometry or array of geometries
    
    Returns:
    Point geometry representing centroid
    """

def point_on_surface(geometry, **kwargs):
    """
    Get a point guaranteed to be on the geometry surface.
    
    Parameters:
    - geometry: input geometry or array of geometries
    
    Returns:
    Point geometry on the surface
    """
```

**Usage Example:**

```python
import shapely

# Centroid might be outside complex polygons
c_shape = shapely.Polygon([(0, 0), (0, 2), (1, 2), (1, 1), (2, 1), (2, 0)])
centroid = shapely.centroid(c_shape)
surface_point = shapely.point_on_surface(c_shape)

print(f"Centroid inside shape: {c_shape.contains(centroid)}")
print(f"Surface point inside shape: {c_shape.contains(surface_point)}")
```

### Bounding Shapes

Create various bounding shapes around geometries.

```python { .api }
def envelope(geometry, **kwargs):
    """
    Compute axis-aligned bounding box.
    
    Parameters:
    - geometry: input geometry or array of geometries
    
    Returns:
    Rectangular polygon bounding box
    """

def minimum_rotated_rectangle(geometry, **kwargs):
    """
    Compute minimum area oriented bounding rectangle.
    
    Parameters:
    - geometry: input geometry or array of geometries
    
    Returns:
    Rotated rectangular polygon
    """

def minimum_bounding_circle(geometry, **kwargs):
    """
    Compute minimum bounding circle.
    
    Parameters:
    - geometry: input geometry or array of geometries
    
    Returns:
    Circular polygon approximation
    """

def maximum_inscribed_circle(geometry, tolerance=0.01, **kwargs):
    """
    Find maximum inscribed circle (pole of inaccessibility).
    
    Parameters:
    - geometry: input polygon geometry
    - tolerance: precision tolerance
    
    Returns:
    Point at circle center with radius as additional coordinate
    """
```

**Usage Example:**

```python
import shapely

# Create irregular polygon
polygon = shapely.Polygon([(0, 0), (3, 1), (2, 3), (0, 2)])

# Various bounding shapes
bbox = shapely.envelope(polygon)
min_rect = shapely.minimum_rotated_rectangle(polygon)
min_circle = shapely.minimum_bounding_circle(polygon)
max_inscribed = shapely.maximum_inscribed_circle(polygon)

print(f"Original area: {polygon.area:.2f}")
print(f"Bounding box area: {bbox.area:.2f}")
print(f"Min rectangle area: {min_rect.area:.2f}")
```

### Simplification

Reduce geometry complexity while preserving essential shape.

```python { .api }
def simplify(geometry, tolerance, preserve_topology=True, **kwargs):
    """
    Simplify geometry by removing vertices.
    
    Parameters:
    - geometry: input geometry or array of geometries
    - tolerance: simplification tolerance
    - preserve_topology: maintain topological relationships
    
    Returns:
    Simplified geometry
    """

def remove_repeated_points(geometry, tolerance=0.0, **kwargs):
    """
    Remove repeated/duplicate points from geometry.
    Requires GEOS 3.11+.
    
    Parameters:
    - geometry: input geometry or array of geometries
    - tolerance: coordinate tolerance for duplicate detection
    
    Returns:
    Geometry with repeated points removed
    """
```

**Usage Example:**

```python
import shapely

# Create complex polygon
detailed_coords = [(0, 0), (0.1, 0.01), (0.2, 0.02), (1, 0), (1, 1), (0, 1)]
detailed_polygon = shapely.Polygon(detailed_coords)

# Simplify with different tolerances
simplified = shapely.simplify(detailed_polygon, tolerance=0.05)
aggressive = shapely.simplify(detailed_polygon, tolerance=0.2)

print(f"Original vertices: {len(detailed_polygon.exterior.coords)}")
print(f"Simplified vertices: {len(simplified.exterior.coords)}")
print(f"Aggressive vertices: {len(aggressive.exterior.coords)}")
```

### Geometry Repair and Validation

Make invalid geometries valid and repair common issues.

```python { .api }
def make_valid(geometry, **kwargs):
    """
    Repair invalid geometries to make them valid.
    
    Parameters:
    - geometry: input geometry or array of geometries
    
    Returns:
    Valid geometry (may change geometry type)
    """

def normalize(geometry, **kwargs):
    """
    Convert geometry to canonical/normalized form.
    
    Parameters:
    - geometry: input geometry or array of geometries
    
    Returns:
    Normalized geometry
    """

def snap(geometry, reference, tolerance, **kwargs):
    """
    Snap vertices of geometry to reference geometry.
    
    Parameters:
    - geometry: geometry to snap
    - reference: reference geometry to snap to
    - tolerance: snapping tolerance
    
    Returns:
    Snapped geometry
    """
```

**Usage Example:**

```python
import shapely
from shapely.geometry import Polygon

# Create invalid self-intersecting polygon
invalid = Polygon([(0, 0), (2, 2), (2, 0), (0, 2)])
print(f"Original valid: {shapely.is_valid(invalid)}")

# Repair it
valid = shapely.make_valid(invalid)
print(f"Repaired valid: {shapely.is_valid(valid)}")
print(f"Result type: {valid.geom_type}")
```

### Triangulation

Create triangulated representations of geometries.

```python { .api }
def delaunay_triangles(geometry, tolerance=0.0, only_edges=False, **kwargs):
    """
    Compute Delaunay triangulation.
    
    Parameters:
    - geometry: input geometry or array of geometries
    - tolerance: coordinate tolerance
    - only_edges: return only triangle edges instead of filled triangles
    
    Returns:
    GeometryCollection of triangles or edges
    """

def constrained_delaunay_triangles(geometry, **kwargs):
    """
    Compute constrained Delaunay triangulation.
    
    Parameters:
    - geometry: input geometry or array of geometries
    
    Returns:
    GeometryCollection of triangles
    """
```

### Advanced Operations

Specialized geometric constructions.

```python { .api }
def voronoi_polygons(geometry, envelope=None, tolerance=0.0, only_edges=False, **kwargs):
    """
    Compute Voronoi diagram.
    
    Parameters:
    - geometry: input point geometry
    - envelope: clipping envelope for diagram
    - tolerance: coordinate tolerance
    - only_edges: return only diagram edges
    
    Returns:
    GeometryCollection of Voronoi cells or edges
    """

def build_area(geometry, **kwargs):
    """
    Build polygonal area from linework.
    
    Parameters:
    - geometry: input linear geometry
    
    Returns:
    Polygon geometry constructed from lines
    """

def node(geometry, **kwargs):
    """
    Node linear geometry at intersections.
    
    Parameters:
    - geometry: input linear geometry
    
    Returns:
    MultiLineString with all intersections noded
    """

def extract_unique_points(geometry, **kwargs):
    """
    Extract all unique vertex points from geometry.
    
    Parameters:
    - geometry: input geometry
    
    Returns:
    MultiPoint containing all unique vertices
    """
```

**Usage Example:**

```python
import shapely

# Voronoi diagram from random points
import numpy as np
np.random.seed(42)
points = shapely.points(np.random.rand(10, 2) * 10)
envelope = shapely.box(0, 0, 10, 10)

voronoi = shapely.voronoi_polygons(points, envelope=envelope)
print(f"Voronoi cells: {len(voronoi.geoms)}")

# Extract vertices from polygon
polygon = shapely.box(0, 0, 2, 2)
vertices = shapely.extract_unique_points(polygon)
print(f"Polygon vertices: {len(vertices.geoms)}")
```

### Additional Constructive Operations

Other geometric construction and transformation operations.

```python { .api }
def boundary(geometry, **kwargs):
    """
    Get the topological boundary of geometries.
    
    Parameters:
    - geometry: input geometry or array of geometries
    
    Returns:
    Boundary geometry (points for polygons, endpoints for lines)
    """

def clip_by_rect(geometry, xmin, ymin, xmax, ymax, **kwargs):
    """
    Clip geometries by rectangular bounds.
    
    Parameters:
    - geometry: input geometry or array of geometries
    - xmin, ymin, xmax, ymax: clipping rectangle bounds
    
    Returns:
    Clipped geometry within the rectangle
    """

def minimum_clearance_line(geometry, **kwargs):
    """
    Get the line representing minimum clearance of geometries.
    
    Parameters:
    - geometry: input geometry or array of geometries
    
    Returns:
    LineString representing minimum clearance
    """

def offset_curve(geometry, distance, quad_segs=8, join_style='round', mitre_limit=5.0, **kwargs):
    """
    Create offset curves from linestring geometries.
    
    Parameters:
    - geometry: linestring geometry or array
    - distance: offset distance (positive for left, negative for right)
    - quad_segs: segments for quarter-circle approximation
    - join_style: join style ('round', 'mitre', 'bevel')
    - mitre_limit: mitre ratio limit
    
    Returns:
    Offset curve geometry
    """

def orient_polygons(geometry, *, exterior_cw=False, **kwargs):
    """
    Orient polygon rings consistently.
    
    Parameters:
    - geometry: polygon geometry or array of polygons
    - exterior_cw: orient exterior rings clockwise if True
    
    Returns:
    Consistently oriented polygons
    """

def oriented_envelope(geometry, **kwargs):
    """
    Get the minimum rotated rectangle that encloses geometries.
    
    Parameters:
    - geometry: input geometry or array of geometries
    
    Returns:
    Minimum rotated rectangle (oriented envelope)
    """

def polygonize(geometries, **kwargs):
    """
    Create polygons from a collection of linestrings.
    
    Parameters:
    - geometries: array of linestring geometries
    
    Returns:
    GeometryCollection of polygons formed by input lines
    """

def polygonize_full(geometries, **kwargs):
    """
    Create polygons and return additional topology information.
    
    Parameters:
    - geometries: array of linestring geometries
    
    Returns:
    Tuple of (polygons, cuts, dangles, invalid_rings)
    """

def reverse(geometry, **kwargs):
    """
    Reverse the coordinate order of geometries.
    
    Parameters:
    - geometry: input geometry or array of geometries
    
    Returns:
    Geometry with reversed coordinate order
    """

def segmentize(geometry, max_segment_length, **kwargs):
    """
    Add vertices to geometries to limit segment length.
    
    Parameters:
    - geometry: input geometry or array of geometries
    - max_segment_length: maximum allowed segment length
    
    Returns:
    Segmentized geometry with additional vertices
    """
```

## Types

```python { .api }
# Buffer style enumerations
class BufferCapStyle:
    round = 1
    flat = 2
    square = 3

class BufferJoinStyle:
    round = 1
    mitre = 2
    bevel = 3
```