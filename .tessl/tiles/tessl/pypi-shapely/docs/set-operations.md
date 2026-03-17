# Set Operations

Boolean operations that combine geometries using mathematical set theory concepts: union, intersection, difference, and symmetric difference. These operations are fundamental for spatial analysis and geometry processing.

## Capabilities

### Binary Set Operations

Operations between two geometries or geometry arrays.

```python { .api }
def union(a, b, grid_size=None, **kwargs):
    """
    Compute union of two geometries (A ∪ B).
    
    Parameters:
    - a: first geometry or array of geometries
    - b: second geometry or array of geometries  
    - grid_size: precision grid size for snap-rounding
    
    Returns:
    Geometry or array: union result
    """

def intersection(a, b, grid_size=None, **kwargs):
    """
    Compute intersection of two geometries (A ∩ B).
    
    Parameters:
    - a: first geometry or array of geometries
    - b: second geometry or array of geometries
    - grid_size: precision grid size for snap-rounding
    
    Returns:
    Geometry or array: intersection result (may be empty)
    """

def difference(a, b, grid_size=None, **kwargs):
    """
    Compute difference of two geometries (A - B).
    
    Parameters:
    - a: first geometry or array of geometries
    - b: second geometry or array of geometries
    - grid_size: precision grid size for snap-rounding
    
    Returns:
    Geometry or array: difference result (may be empty)
    """

def symmetric_difference(a, b, grid_size=None, **kwargs):
    """
    Compute symmetric difference of two geometries (A ⊕ B).
    Result contains areas in A or B but not in both.
    
    Parameters:
    - a: first geometry or array of geometries
    - b: second geometry or array of geometries
    - grid_size: precision grid size for snap-rounding
    
    Returns:
    Geometry or array: symmetric difference result
    """
```

**Usage Example:**

```python
import shapely
from shapely.geometry import Polygon

# Create two overlapping rectangles
rect1 = Polygon([(0, 0), (3, 0), (3, 2), (0, 2)])
rect2 = Polygon([(1, 1), (4, 1), (4, 3), (1, 3)])

# Set operations
union_result = shapely.union(rect1, rect2)
intersection_result = shapely.intersection(rect1, rect2)
difference_result = shapely.difference(rect1, rect2)
symmetric_diff = shapely.symmetric_difference(rect1, rect2)

print(f"Rect1 area: {rect1.area}")          # 6.0
print(f"Rect2 area: {rect2.area}")          # 6.0
print(f"Union area: {union_result.area}")   # 10.0
print(f"Intersection area: {intersection_result.area}")  # 2.0
print(f"Difference area: {difference_result.area}")      # 4.0
print(f"Symmetric diff area: {symmetric_diff.area}")     # 8.0
```

### Unary Set Operations

Operations on single geometries or geometry collections.

```python { .api }
def unary_union(geometry, grid_size=None, **kwargs):
    """
    Compute union of all geometries in a collection.
    
    Parameters:
    - geometry: geometry collection or array of geometries
    - grid_size: precision grid size for snap-rounding
    
    Returns:
    Geometry: union of all input geometries
    """

# Alias for unary_union
def union_all(geometries, grid_size=None, axis=None, **kwargs):
    """
    Compute union of multiple geometries.
    
    Parameters:
    - geometries: array of geometries
    - grid_size: precision grid size
    - axis: axis along which to compute union (for multidimensional arrays)
    
    Returns:
    Geometry or array: union result
    """
```

**Usage Example:**

```python
import shapely
import numpy as np

# Create multiple overlapping circles
centers = [(0, 0), (1, 0), (0.5, 0.8)]
circles = [shapely.Point(x, y).buffer(0.7) for x, y in centers]

# Union all circles
merged = shapely.unary_union(circles)
print(f"Individual areas: {[c.area for c in circles]}")
print(f"Union area: {merged.area:.2f}")

# Array-based union
circle_array = np.array(circles)
merged_array = shapely.union_all(circle_array)
print(f"Array union area: {merged_array.area:.2f}")
```

### Aggregate Operations

Operations that combine multiple geometries into single results.

```python { .api }
def intersection_all(geometries, axis=None, **kwargs):
    """
    Compute intersection of all geometries.
    
    Parameters:
    - geometries: array of geometries
    - axis: axis along which to compute intersection
    
    Returns:
    Geometry or array: intersection of all geometries
    """

def symmetric_difference_all(geometries, axis=None, **kwargs):
    """
    Compute symmetric difference of all geometries.
    Note: This function is deprecated.
    
    Parameters:
    - geometries: array of geometries
    - axis: axis along which to compute operation
    
    Returns:
    Geometry or array: symmetric difference result
    """
```

**Usage Example:**

```python
import shapely

# Create overlapping rectangles
rects = [
    shapely.box(0, 0, 3, 3),
    shapely.box(1, 1, 4, 4), 
    shapely.box(2, 2, 5, 5)
]

# Find common area
common = shapely.intersection_all(rects)
print(f"Common intersection area: {common.area}")  # Area where all overlap

# Union them all
total = shapely.union_all(rects)
print(f"Total union area: {total.area}")
```

### Coverage Operations

Optimized operations for non-overlapping geometry collections.

```python { .api }
def coverage_union(a, b, **kwargs):
    """
    Optimized union for non-overlapping polygons.
    Faster than regular union when polygons don't overlap.
    
    Parameters:
    - a: first geometry or array
    - b: second geometry or array
    
    Returns:
    Geometry or array: union result
    """

def coverage_union_all(geometries, axis=None, **kwargs):
    """
    Optimized union for collections of non-overlapping polygons.
    
    Parameters:
    - geometries: array of non-overlapping geometries
    - axis: axis along which to compute union
    
    Returns:
    Geometry or array: union result
    """
```

**Usage Example:**

```python
import shapely

# Create non-overlapping squares (like a grid)
squares = []
for i in range(3):
    for j in range(3):
        square = shapely.box(i*2, j*2, i*2+1, j*2+1)
        squares.append(square)

# Fast union for non-overlapping geometries
grid_union = shapely.coverage_union_all(squares)
print(f"Grid union area: {grid_union.area}")  # Should be 9.0

# Compare with regular union (slower but same result)
regular_union = shapely.union_all(squares)
print(f"Regular union area: {regular_union.area}")
print(f"Results equal: {grid_union.equals(regular_union)}")
```

### Disjoint Subset Operations

Advanced operations for disjoint geometry collections (GEOS 3.12+).

```python { .api }
def disjoint_subset_union(a, b, **kwargs):
    """
    Optimized union for disjoint geometry subsets.
    Requires GEOS 3.12+.
    
    Parameters:
    - a: first geometry or array
    - b: second geometry or array
    
    Returns:
    Geometry or array: union result
    """

def disjoint_subset_union_all(geometries, *, axis=None, **kwargs):
    """
    Union of collections containing disjoint subsets.
    Requires GEOS 3.12+.
    
    Parameters:
    - geometries: array of geometries with disjoint subsets
    - axis: axis along which to compute union
    
    Returns:
    Geometry or array: union result
    """
```

### Precision and Robustness

Handle precision issues in set operations.

**Usage Example:**

```python
import shapely

# Create geometries with precision issues
# (coordinates that are almost but not exactly aligned)
poly1 = shapely.Polygon([(0, 0), (1.000000001, 0), (1, 1), (0, 1)])
poly2 = shapely.Polygon([(1, 0), (2, 0), (2, 1), (1.000000001, 1)])

# Without grid snapping - may create tiny slivers
union_default = shapely.union(poly1, poly2)
print(f"Default union area: {union_default.area:.10f}")

# With grid snapping - cleaner result
grid_size = 1e-6  # Snap to micrometer precision
union_snapped = shapely.union(poly1, poly2, grid_size=grid_size)
print(f"Snapped union area: {union_snapped.area:.10f}")

# The snapped version should be exactly 2.0
print(f"Snapped result clean: {abs(union_snapped.area - 2.0) < 1e-10}")
```

### Advanced Usage Patterns

Complex operations combining multiple set operations.

**Usage Example:**

```python
import shapely
import numpy as np

# Create complex scenario: buildings with setback requirements
building_footprints = [
    shapely.box(0, 0, 10, 10),    # Building 1
    shapely.box(15, 0, 25, 10),   # Building 2  
    shapely.box(5, 15, 15, 25)    # Building 3
]

# Property boundary
property_boundary = shapely.box(-5, -5, 30, 30)

# Required setback from property line
setback_distance = 3
buildable_area = shapely.buffer(property_boundary, -setback_distance)

# Check which buildings violate setbacks
violations = []
compliant_buildings = []

for i, building in enumerate(building_footprints):
    if buildable_area.contains(building):
        compliant_buildings.append(building)
        print(f"Building {i+1}: Compliant")
    else:
        violations.append(building)
        # Calculate violation area
        violation_area = shapely.difference(building, buildable_area)
        print(f"Building {i+1}: Violation area = {violation_area.area:.1f}")

# Total built area
total_built = shapely.union_all(building_footprints)
print(f"Total built area: {total_built.area}")

# Remaining buildable area
remaining_buildable = shapely.difference(buildable_area, total_built)
print(f"Remaining buildable area: {remaining_buildable.area:.1f}")
```