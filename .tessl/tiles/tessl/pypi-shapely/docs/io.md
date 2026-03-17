# Input/Output

Convert geometries to and from standard spatial data formats including Well-Known Text (WKT), Well-Known Binary (WKB), and GeoJSON. These functions enable interoperability with other spatial libraries and data storage systems.

## Capabilities

### Well-Known Text (WKT)

Text-based representation of geometries using OGC standard format.

```python { .api }
def to_wkt(geometry, rounding_precision=None, trim=True, output_dimension=None, old_3d=False, **kwargs):
    """
    Convert geometry to Well-Known Text format.
    
    Parameters:
    - geometry: input geometry or array of geometries
    - rounding_precision: decimal places for coordinates (None for no rounding)
    - trim: remove trailing zeros from coordinates
    - output_dimension: force 2D or 3D output (None for auto-detect)
    - old_3d: use old-style 3D WKT format
    
    Returns:
    str or ndarray of str: WKT representation
    """

def from_wkt(wkt, on_invalid='raise', **kwargs):
    """
    Create geometry from Well-Known Text string.
    
    Parameters:
    - wkt: WKT string or array of WKT strings
    - on_invalid: error handling ('raise', 'warn', 'ignore', 'fix')
    
    Returns:
    Geometry or ndarray of geometries
    """
```

**Usage Example:**

```python
import shapely
from shapely.geometry import Point, Polygon

# Convert to WKT
point = Point(1.123456, 2.654321)
point_wkt = shapely.to_wkt(point)
print(point_wkt)  # 'POINT (1.123456 2.654321)'

# With rounding
point_wkt_rounded = shapely.to_wkt(point, rounding_precision=2)
print(point_wkt_rounded)  # 'POINT (1.12 2.65)'

# Complex geometry
polygon = Polygon([(0, 0), (1, 0), (1, 1), (0, 1)])
poly_wkt = shapely.to_wkt(polygon)
print(poly_wkt)  # 'POLYGON ((0 0, 1 0, 1 1, 0 1, 0 0))'

# Convert from WKT
wkt_string = "LINESTRING (0 0, 1 1, 2 0)"
line = shapely.from_wkt(wkt_string)
print(f"Line length: {line.length:.2f}")

# Array operations
wkt_array = [
    "POINT (0 0)",
    "POINT (1 1)", 
    "LINESTRING (0 0, 2 2)"
]
geometries = shapely.from_wkt(wkt_array)
print(f"Created {len(geometries)} geometries")
```

### Well-Known Binary (WKB)

Binary representation for efficient storage and transmission.

```python { .api }
def to_wkb(geometry, hex=False, output_dimension=None, byte_order=None, include_srid=False, flavor='extended', **kwargs):
    """
    Convert geometry to Well-Known Binary format.
    
    Parameters:
    - geometry: input geometry or array of geometries
    - hex: return hexadecimal string instead of bytes
    - output_dimension: force 2D or 3D output
    - byte_order: byte order (-1 for little-endian, 1 for big-endian)
    - include_srid: include SRID in output
    - flavor: WKB flavor ('extended' or 'iso')
    
    Returns:
    bytes or str (if hex=True) or ndarray
    """

def from_wkb(wkb, on_invalid='raise', **kwargs):
    """
    Create geometry from Well-Known Binary data.
    
    Parameters:
    - wkb: WKB bytes, hex string, or array of WKB data
    - on_invalid: error handling ('raise', 'warn', 'ignore', 'fix')
    
    Returns:
    Geometry or ndarray of geometries
    """
```

**Usage Example:**

```python
import shapely
from shapely.geometry import Point

# Convert to WKB
point = Point(1, 2)
wkb_bytes = shapely.to_wkb(point)
wkb_hex = shapely.to_wkb(point, hex=True)

print(f"WKB bytes length: {len(wkb_bytes)}")
print(f"WKB hex: {wkb_hex}")

# Convert back from WKB
point_from_bytes = shapely.from_wkb(wkb_bytes)
point_from_hex = shapely.from_wkb(wkb_hex)

print(f"Original: {point}")
print(f"From bytes: {point_from_bytes}")
print(f"Equal: {point.equals(point_from_bytes)}")
```

### GeoJSON

JSON-based format for web applications and data exchange.

```python { .api }
def to_geojson(geometry, indent=None, **kwargs):
    """
    Convert geometry to GeoJSON format.
    
    Parameters:
    - geometry: input geometry or array of geometries
    - indent: JSON indentation (None for compact format)
    
    Returns:
    str or ndarray of str: GeoJSON representation
    """

def from_geojson(geojson, on_invalid='raise', **kwargs):
    """
    Create geometry from GeoJSON string.
    Requires GEOS 3.10.1+.
    
    Parameters:
    - geojson: GeoJSON string or array of GeoJSON strings
    - on_invalid: error handling ('raise', 'warn', 'ignore', 'fix')
    
    Returns:
    Geometry or ndarray of geometries
    """
```

**Usage Example:**

```python
import shapely
from shapely.geometry import Point, Polygon
import json

# Convert to GeoJSON
point = Point(-122.4194, 37.7749)  # San Francisco
point_geojson = shapely.to_geojson(point)
print("Point GeoJSON:")
print(json.dumps(json.loads(point_geojson), indent=2))

# Complex geometry
polygon = Polygon([(-122.5, 37.7), (-122.3, 37.7), (-122.3, 37.8), (-122.5, 37.8)])
poly_geojson = shapely.to_geojson(polygon, indent=2)
print("Polygon GeoJSON:")
print(poly_geojson)

# Convert from GeoJSON
geojson_str = '''
{
  "type": "LineString",
  "coordinates": [[-122.4, 37.7], [-122.4, 37.8], [-122.3, 37.8]]
}
'''
line = shapely.from_geojson(geojson_str)
print(f"Line from GeoJSON length: {line.length:.4f}")
```

### Ragged Arrays

Efficient representation for coordinate data with variable-length sequences.

```python { .api }
def to_ragged_array(geometry, include_z=False, include_m=False, **kwargs):
    """
    Convert geometries to ragged coordinate arrays.
    
    Parameters:
    - geometry: input geometry or array of geometries
    - include_z: include Z coordinates
    - include_m: include M coordinates
    
    Returns:
    tuple: (coordinates, offsets) arrays
    """

def from_ragged_array(coords, offsets, geometry_type, crs=None, **kwargs):
    """
    Create geometries from ragged coordinate arrays.
    
    Parameters:
    - coords: coordinate array
    - offsets: offset array defining geometry boundaries
    - geometry_type: target geometry type
    - crs: coordinate reference system (optional)
    
    Returns:
    ndarray of geometries
    """
```

**Usage Example:**

```python
import shapely
import numpy as np

# Create multiple linestrings
lines = [
    shapely.LineString([(0, 0), (1, 1)]),
    shapely.LineString([(2, 2), (3, 3), (4, 4)]),
    shapely.LineString([(5, 5), (6, 6), (7, 7), (8, 8)])
]

# Convert to ragged arrays
coords, offsets = shapely.to_ragged_array(lines)
print(f"Coordinates shape: {coords.shape}")
print(f"Offsets: {offsets}")

# Convert back to geometries
lines_reconstructed = shapely.from_ragged_array(
    coords, offsets, geometry_type='LineString'
)
print(f"Reconstructed {len(lines_reconstructed)} lines")

# Verify reconstruction
for original, reconstructed in zip(lines, lines_reconstructed):
    print(f"Equal: {original.equals(reconstructed)}")
```

### Error Handling

Control how invalid input data is handled during conversion.

```python { .api }
# Example of error handling options
import shapely

# Invalid WKT
invalid_wkt = "POINT (not_a_number 2)"

try:
    # Default: raise exception
    geom = shapely.from_wkt(invalid_wkt, on_invalid='raise')
except Exception as e:
    print(f"Error raised: {e}")

# Ignore invalid input (returns None)
geom = shapely.from_wkt(invalid_wkt, on_invalid='ignore')
print(f"Ignored result: {geom}")

# Try to fix invalid input
try:
    geom = shapely.from_wkt(invalid_wkt, on_invalid='fix')
    print(f"Fixed result: {geom}")
except:
    print("Could not fix invalid input")
```

### Batch Processing

Efficient I/O operations on geometry arrays.

**Usage Example:**

```python
import shapely
import numpy as np

# Create large array of geometries
np.random.seed(42)
coords = np.random.rand(1000, 2) * 100
points = shapely.points(coords)

# Convert all to WKT efficiently
wkt_strings = shapely.to_wkt(points, rounding_precision=1)
print(f"Converted {len(wkt_strings)} points to WKT")

# Convert back
points_from_wkt = shapely.from_wkt(wkt_strings)
print(f"Reconstructed {len(points_from_wkt)} points")

# Binary format for efficient storage
wkb_data = shapely.to_wkb(points)
print(f"WKB data size: {sum(len(wkb) for wkb in wkb_data)} bytes")

# Hex format for database storage
wkb_hex = shapely.to_wkb(points, hex=True)
print(f"First WKB hex: {wkb_hex[0]}")
```

## Types

```python { .api }
# Error handling options
class DecodingErrorOptions:
    ignore = 0   # Skip invalid input, return None
    warn = 1     # Issue warning, return None  
    raise = 2    # Raise exception (default)
    fix = 3      # Attempt to fix invalid input

# WKB format options
class WKBFlavorOptions:
    extended = 1  # Extended WKB format (default)
    iso = 2       # ISO SQL/MM WKB format
```