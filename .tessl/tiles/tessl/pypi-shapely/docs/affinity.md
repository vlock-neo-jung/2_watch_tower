# Affinity Transformations

Geometric transformations that preserve straight lines and ratios of distances along straight lines. These transformations include rotation, scaling, translation, skewing, and general affine transformations using transformation matrices.

## Capabilities

### Translation

Move geometries by specified offset distances.

```python { .api }
def translate(geom, xoff=0.0, yoff=0.0, zoff=0.0):
    """
    Translate (move) geometry by offset distances.
    
    Parameters:
    - geom: input geometry
    - xoff: offset distance in X direction
    - yoff: offset distance in Y direction  
    - zoff: offset distance in Z direction (for 3D geometries)
    
    Returns:
    Geometry: translated geometry
    """
```

**Usage Example:**

```python
from shapely import affinity
from shapely.geometry import Point, Polygon

# Translate a point
point = Point(1, 2)
moved_point = affinity.translate(point, xoff=5, yoff=3)
print(f"Original: {point}")
print(f"Translated: {moved_point}")

# Translate a polygon
square = Polygon([(0, 0), (1, 0), (1, 1), (0, 1)])
moved_square = affinity.translate(square, xoff=10, yoff=5)
print(f"Original bounds: {square.bounds}")
print(f"Translated bounds: {moved_square.bounds}")
```

### Rotation

Rotate geometries around a specified origin point.

```python { .api }
def rotate(geom, angle, origin='center', use_radians=False):
    """
    Rotate geometry around an origin point.
    
    Parameters:
    - geom: input geometry
    - angle: rotation angle (degrees by default, radians if use_radians=True)
    - origin: rotation origin ('center', 'centroid', or (x, y) coordinate)
    - use_radians: if True, angle is in radians instead of degrees
    
    Returns:
    Geometry: rotated geometry
    """
```

**Usage Example:**

```python
from shapely import affinity
from shapely.geometry import Polygon
import math

# Create a rectangle
rect = Polygon([(0, 0), (2, 0), (2, 1), (0, 1)])

# Rotate 45 degrees around center
rotated_45 = affinity.rotate(rect, 45)
print(f"Original area: {rect.area}")
print(f"Rotated area: {rotated_45.area:.6f}")  # Should be same

# Rotate around specific point
rotated_around_origin = affinity.rotate(rect, 90, origin=(0, 0))
print(f"Rotated around origin bounds: {rotated_around_origin.bounds}")

# Rotate using radians
rotated_radians = affinity.rotate(rect, math.pi/2, use_radians=True)
print(f"90° rotation matches π/2 radians: {rotated_around_origin.equals(rotated_radians)}")
```

### Scaling

Scale geometries by specified factors along each axis.

```python { .api }
def scale(geom, xfact=1.0, yfact=1.0, zfact=1.0, origin='center'):
    """
    Scale geometry by specified factors.
    
    Parameters:
    - geom: input geometry
    - xfact: scaling factor for X direction
    - yfact: scaling factor for Y direction
    - zfact: scaling factor for Z direction (for 3D geometries)
    - origin: scaling origin ('center', 'centroid', or (x, y) coordinate)
    
    Returns:
    Geometry: scaled geometry
    """
```

**Usage Example:**

```python
from shapely import affinity
from shapely.geometry import Polygon

# Create a square
square = Polygon([(0, 0), (2, 0), (2, 2), (0, 2)])
print(f"Original area: {square.area}")

# Uniform scaling (double size)
double_size = affinity.scale(square, xfact=2.0, yfact=2.0)
print(f"2x scaled area: {double_size.area}")  # Should be 4x original

# Non-uniform scaling
stretched = affinity.scale(square, xfact=3.0, yfact=0.5)
print(f"Stretched area: {stretched.area}")  # Should be 1.5x original

# Scale around specific origin
scaled_from_corner = affinity.scale(square, xfact=2.0, yfact=2.0, origin=(0, 0))
print(f"Scaled from corner bounds: {scaled_from_corner.bounds}")
```

### Skewing

Apply shear transformations to geometries.

```python { .api }
def skew(geom, xs=0.0, ys=0.0, origin='center', use_radians=False):
    """
    Skew (shear) geometry by specified angles.
    
    Parameters:
    - geom: input geometry
    - xs: skew angle in X direction
    - ys: skew angle in Y direction
    - origin: skew origin ('center', 'centroid', or (x, y) coordinate)
    - use_radians: if True, angles are in radians instead of degrees
    
    Returns:
    Geometry: skewed geometry
    """
```

**Usage Example:**

```python
from shapely import affinity
from shapely.geometry import Polygon

# Create a square
square = Polygon([(0, 0), (2, 0), (2, 2), (0, 2)])

# Skew in X direction (creates parallelogram)
skewed_x = affinity.skew(square, xs=30)  # 30 degree skew
print(f"Original area: {square.area}")
print(f"Skewed area: {skewed_x.area:.6f}")  # Area should be preserved

# Skew in both directions
skewed_both = affinity.skew(square, xs=15, ys=10)
print(f"Double skewed bounds: {skewed_both.bounds}")
```

### General Affine Transformation

Apply arbitrary affine transformations using transformation matrices.

```python { .api }
def affine_transform(geom, matrix):
    """
    Apply affine transformation using transformation matrix.
    
    Parameters:
    - geom: input geometry
    - matrix: 6-element transformation matrix [a, b, d, e, xoff, yoff]
             representing the transformation:
             x' = a*x + b*y + xoff
             y' = d*x + e*y + yoff
    
    Returns:
    Geometry: transformed geometry
    """
```

**Usage Example:**

```python
from shapely import affinity
from shapely.geometry import Point
import math

# Identity transformation (no change)
point = Point(1, 2)
identity_matrix = [1, 0, 0, 1, 0, 0]  # [a, b, d, e, xoff, yoff]
unchanged = affinity.affine_transform(point, identity_matrix)
print(f"Identity transform: {point.equals(unchanged)}")

# Translation using matrix
translate_matrix = [1, 0, 0, 1, 5, 3]  # translate by (5, 3)
translated = affinity.affine_transform(point, translate_matrix)
print(f"Matrix translated: {translated}")

# Compare with translate function
also_translated = affinity.translate(point, 5, 3)
print(f"Methods equivalent: {translated.equals(also_translated)}")

# Rotation using matrix (45 degrees)
cos_45 = math.cos(math.pi/4)
sin_45 = math.sin(math.pi/4)
rotation_matrix = [cos_45, -sin_45, sin_45, cos_45, 0, 0]
rotated = affinity.affine_transform(point, rotation_matrix)
print(f"Matrix rotated: {rotated}")

# Complex transformation: scale + rotate + translate
# Scale by 2, rotate 30°, translate by (10, 5)
cos_30 = math.cos(math.pi/6)
sin_30 = math.sin(math.pi/6)
complex_matrix = [
    2 * cos_30,   # a = 2 * cos(30°)
    -2 * sin_30,  # b = -2 * sin(30°) 
    2 * sin_30,   # d = 2 * sin(30°)
    2 * cos_30,   # e = 2 * cos(30°)
    10,           # xoff = 10
    5             # yoff = 5
]
complex_transformed = affinity.affine_transform(point, complex_matrix)
print(f"Complex transform result: {complex_transformed}")
```

### Chaining Transformations

Combine multiple transformations for complex effects.

**Usage Example:**

```python
from shapely import affinity
from shapely.geometry import Polygon

# Create original shape
triangle = Polygon([(0, 0), (2, 0), (1, 2)])

# Chain transformations
result = triangle
result = affinity.translate(result, xoff=5, yoff=3)    # Move to new position
result = affinity.rotate(result, 45)                  # Rotate 45 degrees
result = affinity.scale(result, xfact=1.5, yfact=1.5) # Scale up by 50%
result = affinity.skew(result, xs=10)                 # Add slight skew

print(f"Original centroid: {triangle.centroid}")
print(f"Final centroid: {result.centroid}")
print(f"Area change: {result.area / triangle.area:.2f}x")
```

## Import Note

The affinity module is not imported automatically with shapely and must be imported separately:

```python
from shapely import affinity
# or
import shapely.affinity as affinity
```