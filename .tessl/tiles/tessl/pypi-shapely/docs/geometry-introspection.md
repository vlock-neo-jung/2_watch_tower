# Geometry Introspection

Functions for accessing and examining geometric properties, dimensions, coordinate information, and structural details of geometry objects. These functions provide detailed insight into geometry composition and characteristics.

## Capabilities

### Dimension and Coordinate Information

Get dimensional properties and coordinate counts of geometries.

```python { .api }
def get_coordinate_dimension(geometry, **kwargs):
    """
    Get the coordinate dimension of geometries.
    
    Parameters:
    - geometry: geometry or array of geometries
    
    Returns:
    int or ndarray of coordinate dimensions (2 for 2D, 3 for 3D)
    """

def get_dimensions(geometry, **kwargs):
    """
    Get the geometric dimension of geometries.
    
    Parameters:
    - geometry: geometry or array of geometries
    
    Returns:
    int or ndarray of dimensions (0=point, 1=line, 2=area)
    """

def get_num_coordinates(geometry, **kwargs):
    """
    Get the number of coordinate points in geometries.
    
    Parameters:
    - geometry: geometry or array of geometries
    
    Returns:
    int or ndarray of coordinate counts
    """
```

**Usage Example:**

```python
import shapely

# Create various geometries
point = shapely.Point(1, 1)
line = shapely.LineString([(0, 0), (1, 1), (2, 0)])
poly = shapely.Polygon([(0, 0), (2, 0), (2, 2), (0, 2)])

# Get dimensions
print(shapely.get_coordinate_dimension(point))  # 2 (2D coordinates)
print(shapely.get_dimensions(point))           # 0 (point)
print(shapely.get_dimensions(line))            # 1 (line)
print(shapely.get_dimensions(poly))            # 2 (area)

# Get coordinate counts
print(shapely.get_num_coordinates(point))      # 1
print(shapely.get_num_coordinates(line))       # 3
print(shapely.get_num_coordinates(poly))       # 5 (including closing point)
```

### Geometry Structure Analysis

Examine the internal structure and composition of complex geometries.

```python { .api }
def get_num_geometries(geometry, **kwargs):
    """
    Get the number of geometries in multi-geometries or collections.
    
    Parameters:
    - geometry: geometry or array of geometries
    
    Returns:
    int or ndarray of geometry counts
    """

def get_num_interior_rings(geometry, **kwargs):
    """
    Get the number of interior rings (holes) in polygon geometries.
    
    Parameters:
    - geometry: polygon geometry or array of polygons
    
    Returns:
    int or ndarray of hole counts
    """

def get_num_points(geometry, **kwargs):
    """
    Get the number of points in linestring or linearring geometries.
    
    Parameters:
    - geometry: linestring/linearring geometry or array
    
    Returns:
    int or ndarray of point counts
    """
```

### Geometry Part Extraction

Extract component parts and rings from complex geometries.

```python { .api }
def get_parts(geometry, return_index=False):
    """
    Extract individual geometry parts from multi-geometries and collections.
    
    Parameters:
    - geometry: geometry or array of geometries
    - return_index: if True, return indices indicating source geometry
    
    Returns:
    ndarray of individual geometries, optionally with indices
    """

def get_rings(geometry, return_index=False):
    """
    Extract rings (exterior and interior) from polygon geometries.
    
    Parameters:
    - geometry: polygon geometry or array of polygons
    - return_index: if True, return indices indicating source geometry
    
    Returns:
    ndarray of LinearRing objects, optionally with indices
    """
```

**Usage Example:**

```python
import shapely

# Create multi-geometry
points = [shapely.Point(0, 0), shapely.Point(1, 1), shapely.Point(2, 2)]
multipoint = shapely.MultiPoint(points)

# Extract parts
parts = shapely.get_parts(multipoint)
print(len(parts))  # 3

# Create polygon with hole
exterior = [(0, 0), (4, 0), (4, 4), (0, 4)]
hole = [(1, 1), (3, 1), (3, 3), (1, 3)]
poly_with_hole = shapely.Polygon(exterior, [hole])

# Extract rings
rings = shapely.get_rings(poly_with_hole)
print(len(rings))  # 2 (exterior + interior)
```

### Type and Identification

Get geometry type information and identifiers.

```python { .api }
def get_type_id(geometry, **kwargs):
    """
    Get the geometry type ID of geometries.
    
    Parameters:
    - geometry: geometry or array of geometries
    
    Returns:
    int or ndarray of geometry type IDs (see GeometryType enum)
    """
```

### Individual Component Access

Access specific components of geometries by index.

```python { .api }
def get_geometry(geometry, index, **kwargs):
    """
    Get a specific geometry from a multi-geometry or collection by index.
    
    Parameters:
    - geometry: multi-geometry or collection
    - index: index of geometry to extract
    
    Returns:
    Individual geometry at the specified index
    """

def get_point(geometry, index, **kwargs):
    """
    Get a specific point from a linestring geometry by index.
    
    Parameters:
    - geometry: linestring or linearring geometry
    - index: index of point to extract
    
    Returns:
    Point geometry at the specified index
    """

def get_exterior_ring(geometry, **kwargs):
    """
    Get the exterior ring of polygon geometries.
    
    Parameters:
    - geometry: polygon geometry or array of polygons
    
    Returns:
    LinearRing representing the exterior boundary
    """

def get_interior_ring(geometry, index, **kwargs):
    """
    Get a specific interior ring (hole) from polygon geometries.
    
    Parameters:
    - geometry: polygon geometry or array of polygons
    - index: index of interior ring to extract
    
    Returns:
    LinearRing representing the interior hole
    """
```

### Coordinate Access

Direct access to coordinate values from point geometries.

```python { .api }
def get_x(point, **kwargs):
    """
    Get the x-coordinate of point geometries.
    
    Parameters:
    - point: point geometry or array of points
    
    Returns:
    float or ndarray of x-coordinates
    """

def get_y(point, **kwargs):
    """
    Get the y-coordinate of point geometries.
    
    Parameters:
    - point: point geometry or array of points
    
    Returns:
    float or ndarray of y-coordinates
    """

def get_z(point, **kwargs):
    """
    Get the z-coordinate of 3D point geometries.
    
    Parameters:
    - point: 3D point geometry or array of 3D points
    
    Returns:
    float or ndarray of z-coordinates
    """

def get_m(point, **kwargs):
    """
    Get the m-coordinate (measure) of point geometries (requires GEOS 3.12.0+).
    
    Parameters:
    - point: point geometry with m-coordinate
    
    Returns:
    float or ndarray of m-coordinates
    """
```

### Precision and SRID

Access and modify geometry precision and spatial reference information.

```python { .api }
def get_precision(geometry, **kwargs):
    """
    Get the precision of geometries.
    
    Parameters:
    - geometry: geometry or array of geometries
    
    Returns:
    float or ndarray of precision values
    """

def set_precision(geometry, grid_size, mode='valid_output', **kwargs):
    """
    Set the precision of geometries.
    
    Parameters:
    - geometry: geometry or array of geometries
    - grid_size: precision grid size
    - mode: precision mode ('valid_output', 'pointwise', 'keep_collapsed')
    
    Returns:
    Geometry with modified precision
    """

def get_srid(geometry, **kwargs):
    """
    Get the SRID (Spatial Reference ID) of geometries.
    
    Parameters:
    - geometry: geometry or array of geometries
    
    Returns:
    int or ndarray of SRID values
    """

def set_srid(geometry, srid, **kwargs):
    """
    Set the SRID (Spatial Reference ID) of geometries.
    
    Parameters:
    - geometry: geometry or array of geometries
    - srid: spatial reference identifier
    
    Returns:
    Geometry with modified SRID
    """
```

### Force Dimensionality

Control the dimensionality of geometries.

```python { .api }
def force_2d(geometry, **kwargs):
    """
    Force geometries to 2D by removing z-coordinates.
    
    Parameters:
    - geometry: geometry or array of geometries
    
    Returns:
    2D geometry with z-coordinates removed
    """

def force_3d(geometry, z=0.0, **kwargs):
    """
    Force geometries to 3D by adding z-coordinates.
    
    Parameters:
    - geometry: geometry or array of geometries
    - z: default z-coordinate value to add
    
    Returns:
    3D geometry with z-coordinates added
    """
```

**Usage Example:**

```python
import shapely

# Create 3D point
point_3d = shapely.Point(1, 1, 5)

# Get coordinates
print(shapely.get_x(point_3d))  # 1.0
print(shapely.get_y(point_3d))  # 1.0
print(shapely.get_z(point_3d))  # 5.0

# Force to 2D
point_2d = shapely.force_2d(point_3d)
print(shapely.get_coordinate_dimension(point_2d))  # 2

# Set precision
precise_point = shapely.set_precision(point_3d, 0.1)
print(shapely.get_precision(precise_point))  # 0.1
```

## Types

```python { .api }
# Precision mode enumeration
class SetPrecisionMode:
    valid_output = 0    # Ensure output is valid (default)
    pointwise = 1       # Apply precision pointwise
    keep_collapsed = 2  # Keep collapsed geometries
```