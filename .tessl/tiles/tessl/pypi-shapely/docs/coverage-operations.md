# Coverage Operations

Advanced operations specifically designed for working with polygon coverages - collections of polygons that share boundaries without gaps or overlaps. These operations are optimized for processing large collections of adjacent polygons such as cadastral maps, administrative boundaries, or ecological zones.

**Note**: All coverage operations require GEOS 3.12.0 or later.

## Capabilities

### Coverage Validation

Validate the integrity and correctness of polygon coverages.

```python { .api }
def coverage_is_valid(geometry, gap_width=0.0, **kwargs):
    """
    Check if polygon coverage is valid (no gaps or overlaps).
    
    Parameters:
    - geometry: polygon or multi-polygon coverage to validate
    - gap_width: tolerance for small gaps (default 0.0)
    
    Returns:
    bool or ndarray indicating coverage validity
    
    Note:
    Requires GEOS 3.12.0+
    """
```

**Usage Example:**

```python
import shapely

# Create adjacent polygons forming a coverage
poly1 = shapely.box(0, 0, 1, 1)
poly2 = shapely.box(1, 0, 2, 1)  # Shares edge with poly1
poly3 = shapely.box(0, 1, 1, 2)  # Shares edge with poly1

coverage = shapely.union_all([poly1, poly2, poly3])

# Validate coverage
is_valid = shapely.coverage_is_valid(coverage)
print(f"Coverage is valid: {is_valid}")

# Allow small gaps
is_valid_with_tolerance = shapely.coverage_is_valid(coverage, gap_width=0.01)
```

### Coverage Error Detection

Identify specific edges that cause coverage invalidity.

```python { .api }
def coverage_invalid_edges(geometry, gap_width=0.0, **kwargs):
    """
    Find edges that make a polygon coverage invalid.
    
    Parameters:
    - geometry: polygon or multi-polygon coverage to analyze
    - gap_width: tolerance for small gaps (default 0.0)
    
    Returns:
    LineString or MultiLineString of invalid edges, or empty geometry if valid
    
    Note:
    Requires GEOS 3.12.0+
    """
```

**Usage Example:**

```python
import shapely

# Create coverage with gaps
poly1 = shapely.box(0, 0, 1, 1)
poly2 = shapely.box(1.1, 0, 2.1, 1)  # Small gap between polygons
coverage = shapely.union_all([poly1, poly2])

# Find invalid edges
invalid_edges = shapely.coverage_invalid_edges(coverage)
if not shapely.is_empty(invalid_edges):
    print(f"Found {shapely.get_num_geometries(invalid_edges)} invalid edges")
```

### Coverage Simplification

Simplify polygon coverages while maintaining shared boundaries.

```python { .api }
def coverage_simplify(geometry, tolerance, *, simplify_boundary=True, **kwargs):
    """
    Simplify polygon coverage while preserving topology and shared boundaries.
    
    Parameters:
    - geometry: polygon or multi-polygon coverage to simplify
    - tolerance: simplification tolerance
    - simplify_boundary: whether to simplify coverage boundary (default True)
    
    Returns:
    Simplified coverage geometry
    
    Note:
    Requires GEOS 3.12.0+
    """
```

**Usage Example:**

```python
import shapely
import numpy as np

# Create complex coverage with many vertices
def create_detailed_polygon(bounds, num_points=100):
    xmin, ymin, xmax, ymax = bounds
    # Create polygon with many random vertices
    angles = np.linspace(0, 2*np.pi, num_points, endpoint=False)
    x = xmin + (xmax - xmin) * (0.5 + 0.3 * np.cos(angles))
    y = ymin + (ymax - ymin) * (0.5 + 0.3 * np.sin(angles))
    return shapely.Polygon(list(zip(x, y)))

poly1 = create_detailed_polygon([0, 0, 1, 1])
poly2 = create_detailed_polygon([1, 0, 2, 1])
coverage = shapely.union_all([poly1, poly2])

print(f"Original coordinates: {shapely.get_num_coordinates(coverage)}")

# Simplify coverage
simplified = shapely.coverage_simplify(coverage, tolerance=0.1)
print(f"Simplified coordinates: {shapely.get_num_coordinates(simplified)}")

# Simplify without boundary simplification
simplified_interior = shapely.coverage_simplify(
    coverage, tolerance=0.1, simplify_boundary=False
)
```

### Coverage Union Operations

Union operations optimized for polygon coverages.

```python { .api }
def coverage_union(a, b, **kwargs):
    """
    Union two polygon coverages efficiently.
    
    Parameters:
    - a: first polygon coverage
    - b: second polygon coverage
    
    Returns:
    Union of the two coverages
    
    Note:
    More efficient than regular union for coverages.
    Requires GEOS 3.12.0+
    """

def coverage_union_all(geometries, axis=None, **kwargs):
    """
    Union multiple polygon coverages efficiently.
    
    Parameters:
    - geometries: array of polygon coverages
    - axis: axis along which to perform union (optional)
    
    Returns:
    Union of all input coverages
    
    Note:
    More efficient than regular union_all for coverages.
    Requires GEOS 3.12.0+
    """
```

**Usage Example:**

```python
import shapely

# Create multiple coverage polygons
coverage1 = shapely.union_all([
    shapely.box(0, 0, 1, 1),
    shapely.box(1, 0, 2, 1)
])

coverage2 = shapely.union_all([
    shapely.box(0, 1, 1, 2), 
    shapely.box(1, 1, 2, 2)
])

coverage3 = shapely.union_all([
    shapely.box(2, 0, 3, 1),
    shapely.box(2, 1, 3, 2)
])

# Union two coverages
combined = shapely.coverage_union(coverage1, coverage2)

# Union multiple coverages
all_coverages = [coverage1, coverage2, coverage3]
full_coverage = shapely.coverage_union_all(all_coverages)

print(f"Final coverage area: {shapely.area(full_coverage)}")
```

## Coverage Workflow Example

Here's a complete example of working with polygon coverages:

```python
import shapely
import numpy as np

def validate_and_process_coverage(polygons):
    """Process and validate a polygon coverage."""
    
    # Combine polygons into coverage
    coverage = shapely.union_all(polygons)
    
    # Validate coverage
    if shapely.coverage_is_valid(coverage):
        print("✓ Coverage is valid")
    else:
        print("✗ Coverage has issues")
        
        # Find problematic edges
        invalid_edges = shapely.coverage_invalid_edges(coverage)
        if not shapely.is_empty(invalid_edges):
            print(f"Found {shapely.get_num_geometries(invalid_edges)} invalid edges")
            
            # You might want to fix the issues here
            # For example, by buffering slightly to close small gaps
            coverage = shapely.buffer(coverage, 0.001).buffer(-0.001)
            
            # Re-validate
            if shapely.coverage_is_valid(coverage):
                print("✓ Coverage fixed")
    
    # Simplify if needed
    original_coords = shapely.get_num_coordinates(coverage)
    simplified = shapely.coverage_simplify(coverage, tolerance=0.01)
    simplified_coords = shapely.get_num_coordinates(simplified)
    
    print(f"Simplified from {original_coords} to {simplified_coords} coordinates")
    
    return simplified

# Example usage
polygons = [
    shapely.box(0, 0, 1, 1),
    shapely.box(1, 0, 2, 1),
    shapely.box(0, 1, 1, 2),
    shapely.box(1, 1, 2, 2)
]

processed_coverage = validate_and_process_coverage(polygons)
```

## Performance Benefits

Coverage operations are specifically optimized for polygon collections that share boundaries:

1. **coverage_union**: More efficient than regular union for adjacent polygons
2. **coverage_simplify**: Maintains shared boundaries while reducing vertex count
3. **coverage_is_valid**: Quickly validates coverage topology
4. **coverage_invalid_edges**: Precisely identifies problem areas

These functions are particularly useful for:
- **Cadastral mapping**: Land parcel boundaries
- **Administrative boundaries**: Political divisions
- **Ecological zones**: Habitat or climate regions  
- **Urban planning**: Zoning and land use maps
- **Geological surveys**: Rock formations and soil types

## Requirements

All coverage operations require:
- **GEOS 3.12.0 or later**
- Input geometries should be **valid polygons**
- Best performance with **adjacent, non-overlapping polygons**