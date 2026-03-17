# Geometry Classes

The fundamental geometry types in Shapely that represent spatial objects. All geometries inherit from the base `Geometry` class and provide both object-oriented methods and functional array-based operations.

## Capabilities

### Point Geometry

Represents a single point in 2D or 3D space.

```python { .api }
class Point(Geometry):
    def __init__(self, x=None, y=None, z=None):
        """
        Create a Point geometry.
        
        Parameters:
        - x (float): X-coordinate
        - y (float): Y-coordinate  
        - z (float, optional): Z-coordinate for 3D points
        """
    
    @property
    def x(self) -> float:
        """X-coordinate of the point."""
    
    @property  
    def y(self) -> float:
        """Y-coordinate of the point."""
        
    @property
    def z(self) -> float:
        """Z-coordinate of the point (0 if 2D)."""
```

**Usage Example:**

```python
from shapely.geometry import Point

# Create 2D point
point_2d = Point(1.5, 2.5)
print(f"X: {point_2d.x}, Y: {point_2d.y}")

# Create 3D point
point_3d = Point(1.5, 2.5, 3.5)
print(f"X: {point_3d.x}, Y: {point_3d.y}, Z: {point_3d.z}")
```

### LineString Geometry

Represents a sequence of points connected by straight line segments.

```python { .api }
class LineString(Geometry):
    def __init__(self, coordinates=None):
        """
        Create a LineString geometry.
        
        Parameters:
        - coordinates: sequence of (x, y[, z]) coordinate tuples
        """
    
    @property
    def coords(self):
        """Coordinate sequence of the linestring."""
        
    @property
    def is_closed(self) -> bool:
        """True if linestring is closed (first and last points are the same)."""
        
    @property
    def is_simple(self) -> bool:
        """True if linestring does not cross itself."""
```

**Usage Example:**

```python
from shapely.geometry import LineString

# Create a simple line
line = LineString([(0, 0), (1, 1), (2, 0)])
print(f"Length: {line.length}")
print(f"Is closed: {line.is_closed}")

# Create a 3D line
line_3d = LineString([(0, 0, 0), (1, 1, 1), (2, 0, 2)])
```

### LinearRing Geometry

A closed LineString that forms the boundary of a polygon.

```python { .api }
class LinearRing(Geometry):
    def __init__(self, coordinates=None):
        """
        Create a LinearRing geometry (closed linestring).
        
        Parameters:
        - coordinates: sequence of (x, y[, z]) coordinate tuples
                      First and last points will be automatically connected
        """
    
    @property
    def coords(self):
        """Coordinate sequence of the ring."""
        
    @property
    def is_ccw(self) -> bool:
        """True if ring is oriented counter-clockwise."""
```

### Polygon Geometry

Represents a filled area bounded by a LinearRing exterior with optional holes.

```python { .api }
class Polygon(Geometry):
    def __init__(self, shell=None, holes=None):
        """
        Create a Polygon geometry.
        
        Parameters:
        - shell: exterior boundary as coordinate sequence or LinearRing
        - holes: sequence of interior holes as coordinate sequences or LinearRings
        """
    
    @property
    def exterior(self) -> LinearRing:
        """Exterior boundary of the polygon."""
        
    @property
    def interiors(self):
        """Sequence of interior holes."""
        
    @property
    def coords(self):
        """Coordinate sequence of exterior boundary."""
```

**Usage Example:**

```python
from shapely.geometry import Polygon

# Simple rectangle
rect = Polygon([(0, 0), (2, 0), (2, 2), (0, 2)])
print(f"Area: {rect.area}")

# Polygon with hole
exterior = [(0, 0), (4, 0), (4, 4), (0, 4)]
hole = [(1, 1), (3, 1), (3, 3), (1, 3)]
poly_with_hole = Polygon(exterior, [hole])
print(f"Area: {poly_with_hole.area}")  # 16 - 4 = 12
```

### MultiPoint Geometry

Collection of Point geometries.

```python { .api }
class MultiPoint(Geometry):
    def __init__(self, points=None):
        """
        Create a MultiPoint geometry.
        
        Parameters:
        - points: sequence of Point objects or coordinate tuples
        """
    
    @property
    def geoms(self):
        """Sequence of Point geometries."""
        
    def __len__(self) -> int:
        """Number of points in the collection."""
        
    def __getitem__(self, index) -> Point:
        """Get point by index."""
```

### MultiLineString Geometry

Collection of LineString geometries.

```python { .api }
class MultiLineString(Geometry):
    def __init__(self, linestrings=None):
        """
        Create a MultiLineString geometry.
        
        Parameters:
        - linestrings: sequence of LineString objects or coordinate sequences
        """
    
    @property
    def geoms(self):
        """Sequence of LineString geometries."""
        
    def __len__(self) -> int:
        """Number of linestrings in the collection."""
        
    def __getitem__(self, index) -> LineString:
        """Get linestring by index."""
```

### MultiPolygon Geometry

Collection of Polygon geometries.

```python { .api }
class MultiPolygon(Geometry):
    def __init__(self, polygons=None, context_type='polygon'):
        """
        Create a MultiPolygon geometry.
        
        Parameters:
        - polygons: sequence of Polygon objects or coordinate sequences
        - context_type: context type for coordinate interpretation
        """
    
    @property
    def geoms(self):
        """Sequence of Polygon geometries."""
        
    def __len__(self) -> int:
        """Number of polygons in the collection."""
        
    def __getitem__(self, index) -> Polygon:
        """Get polygon by index."""
```

### GeometryCollection

Collection of mixed geometry types.

```python { .api }
class GeometryCollection(Geometry):
    def __init__(self, geometries=None):
        """
        Create a GeometryCollection.
        
        Parameters:
        - geometries: sequence of any Geometry objects
        """
    
    @property
    def geoms(self):
        """Sequence of geometries in the collection."""
        
    def __len__(self) -> int:
        """Number of geometries in the collection."""
        
    def __getitem__(self, index) -> Geometry:
        """Get geometry by index."""
```

**Usage Example:**

```python
from shapely.geometry import Point, LineString, Polygon, GeometryCollection

# Create mixed collection
point = Point(0, 0)
line = LineString([(1, 1), (2, 2)])  
poly = Polygon([(3, 3), (4, 3), (4, 4), (3, 4)])

collection = GeometryCollection([point, line, poly])
print(f"Number of geometries: {len(collection)}")

# Iterate through geometries
for geom in collection.geoms:
    print(f"Geometry type: {geom.geom_type}")
```

## Common Properties and Methods

All geometry classes inherit common properties and methods from the base `Geometry` class:

```python { .api }
class Geometry:
    @property
    def area(self) -> float:
        """Area of the geometry (0 for non-areal geometries)."""
    
    @property
    def bounds(self) -> tuple:
        """Bounding box as (minx, miny, maxx, maxy)."""
    
    @property
    def length(self) -> float:
        """Length/perimeter of the geometry."""
    
    @property
    def geom_type(self) -> str:
        """Geometry type name."""
    
    @property
    def is_empty(self) -> bool:
        """True if geometry is empty."""
    
    @property
    def is_valid(self) -> bool:
        """True if geometry is topologically valid."""
    
    def buffer(self, distance: float, **kwargs) -> 'Geometry':
        """Create buffer around geometry."""
    
    def contains(self, other: 'Geometry') -> bool:
        """Test if this geometry contains other."""
    
    def intersects(self, other: 'Geometry') -> bool:
        """Test if this geometry intersects other."""
    
    def within(self, other: 'Geometry') -> bool:
        """Test if this geometry is within other."""
    
    def touches(self, other: 'Geometry') -> bool:
        """Test if this geometry touches other."""
    
    def crosses(self, other: 'Geometry') -> bool:
        """Test if this geometry crosses other."""
    
    def overlaps(self, other: 'Geometry') -> bool:
        """Test if this geometry overlaps other."""
    
    def equals(self, other: 'Geometry') -> bool:
        """Test if this geometry equals other spatially."""
    
    def distance(self, other: 'Geometry') -> float:
        """Compute minimum distance to other geometry."""
    
    def intersection(self, other: 'Geometry') -> 'Geometry':
        """Compute intersection with other geometry."""
    
    def union(self, other: 'Geometry') -> 'Geometry':
        """Compute union with other geometry."""
    
    def difference(self, other: 'Geometry') -> 'Geometry':
        """Compute difference from other geometry."""
    
    def symmetric_difference(self, other: 'Geometry') -> 'Geometry':
        """Compute symmetric difference with other geometry."""
```