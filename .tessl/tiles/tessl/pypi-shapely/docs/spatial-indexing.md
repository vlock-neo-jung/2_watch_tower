# Spatial Indexing

R-tree spatial indexing for efficient spatial queries on large collections of geometries. The STRtree (Sort-Tile-Recursive tree) provides fast spatial queries by organizing geometries into a hierarchical bounding box structure.

## Capabilities

### STRtree Index

High-performance spatial index for geometry collections.

```python { .api }
class STRtree:
    def __init__(self, geometries, node_capacity=10):
        """
        Create spatial index from geometry collection.
        
        Parameters:
        - geometries: array-like of geometries to index
        - node_capacity: maximum number of geometries per tree node
        """
    
    @property
    def geometries(self):
        """Array of indexed geometries."""
    
    def query(self, geometry, predicate=None):
        """
        Query index for geometries that satisfy spatial predicate.
        
        Parameters:
        - geometry: query geometry
        - predicate: spatial predicate ('intersects', 'within', 'contains', etc.)
                    If None, returns geometries with overlapping bounding boxes
        
        Returns:
        ndarray: indices of matching geometries
        """
    
    def query_items(self, geometry, predicate=None):
        """
        Query index and return actual geometries instead of indices.
        
        Parameters:
        - geometry: query geometry
        - predicate: spatial predicate
        
        Returns:
        ndarray: matching geometries
        """
    
    def nearest(self, geometry, max_distance=None, return_distance=False, exclusive=False):
        """
        Find nearest geometries to query geometry.
        
        Parameters:
        - geometry: query geometry
        - max_distance: maximum search distance (None for unlimited)
        - return_distance: if True, return distances along with geometries
        - exclusive: if True, exclude query geometry from results
        
        Returns:
        ndarray or tuple: nearest geometry indices, optionally with distances
        """
```

**Usage Example:**

```python
import shapely
import numpy as np

# Create a collection of geometries to index
np.random.seed(42)
points = shapely.points(np.random.rand(1000, 2) * 100)
polygons = [shapely.Point(x, y).buffer(2) for x, y in np.random.rand(100, 2) * 100]

# Create spatial index
tree = shapely.STRtree(polygons)
print(f"Indexed {len(tree.geometries)} polygons")

# Query geometries intersecting a region
query_region = shapely.box(20, 20, 30, 30)
intersecting_indices = tree.query(query_region, predicate='intersects')
print(f"Found {len(intersecting_indices)} intersecting polygons")

# Get actual geometries instead of indices
intersecting_geoms = tree.query_items(query_region, predicate='intersects')
print(f"Retrieved {len(intersecting_geoms)} geometry objects")

# Find nearest polygons to a point
query_point = shapely.Point(50, 50)
nearest_indices = tree.nearest(query_point)
print(f"Nearest polygon index: {nearest_indices[0] if len(nearest_indices) > 0 else 'None'}")

# Get nearest with distance
nearest_with_dist = tree.nearest(query_point, return_distance=True)
if len(nearest_with_dist[0]) > 0:
    index, distance = nearest_with_dist[0][0], nearest_with_dist[1][0]
    print(f"Nearest polygon at index {index}, distance {distance:.2f}")
```

### Spatial Predicates for Queries

Available predicates for spatial index queries.

```python { .api }
class BinaryPredicate:
    intersects = 1      # Geometries that intersect query
    within = 2          # Geometries within query geometry
    contains = 3        # Geometries that contain query geometry
    overlaps = 4        # Geometries that overlap query
    crosses = 5         # Geometries that cross query
    touches = 6         # Geometries that touch query
    covers = 7          # Geometries that cover query
    covered_by = 8      # Geometries covered by query
    contains_properly = 9  # Geometries that properly contain query
```

**Usage Example:**

```python
import shapely

# Create test geometries
large_polygon = shapely.box(0, 0, 20, 20)
small_polygons = [
    shapely.box(5, 5, 8, 8),      # inside
    shapely.box(15, 15, 25, 25),  # overlapping
    shapely.box(25, 25, 30, 30),  # outside
    shapely.box(-5, 10, 5, 15),   # touching edge
]

# Index the small polygons
tree = shapely.STRtree(small_polygons)

# Different query types
within_results = tree.query(large_polygon, predicate='within')
overlaps_results = tree.query(large_polygon, predicate='overlaps')  
touches_results = tree.query(large_polygon, predicate='touches')

print(f"Polygons within large polygon: {len(within_results)}")
print(f"Polygons overlapping large polygon: {len(overlaps_results)}")
print(f"Polygons touching large polygon: {len(touches_results)}")
```

### Performance Optimization

Spatial indexing provides significant performance improvements for large datasets.

**Usage Example:**

```python
import shapely
import numpy as np
import time

# Create large dataset
np.random.seed(42)
n_geoms = 10000
centers = np.random.rand(n_geoms, 2) * 1000
radii = np.random.rand(n_geoms) * 5 + 1
polygons = [shapely.Point(x, y).buffer(r) for (x, y), r in zip(centers, radii)]

print(f"Created {len(polygons)} test polygons")

# Query region
query_box = shapely.box(400, 400, 600, 600)

# Method 1: Brute force (no index)
start_time = time.time()
brute_force_results = []
for i, poly in enumerate(polygons):
    if query_box.intersects(poly):
        brute_force_results.append(i)
brute_force_time = time.time() - start_time

# Method 2: Using spatial index
start_time = time.time()
tree = shapely.STRtree(polygons)
index_build_time = time.time() - start_time

start_time = time.time()
indexed_results = tree.query(query_box, predicate='intersects')
index_query_time = time.time() - start_time

print(f"Brute force: {len(brute_force_results)} results in {brute_force_time:.3f}s")
print(f"Index build time: {index_build_time:.3f}s")
print(f"Index query: {len(indexed_results)} results in {index_query_time:.3f}s")
print(f"Speedup: {brute_force_time / index_query_time:.1f}x (excluding build time)")
print(f"Results match: {set(brute_force_results) == set(indexed_results)}")
```

### Advanced Usage Patterns

Complex spatial queries and analysis patterns.

**Usage Example:**

```python
import shapely
import numpy as np

# Create urban planning scenario: buildings and points of interest
np.random.seed(42)

# Buildings (rectangles)
building_coords = np.random.rand(500, 2) * 1000
buildings = [
    shapely.box(x-5, y-5, x+5, y+5) 
    for x, y in building_coords
]

# Points of interest
poi_coords = np.random.rand(100, 2) * 1000
pois = shapely.points(poi_coords)

# Create indexes
building_tree = shapely.STRtree(buildings)
poi_tree = shapely.STRtree(pois)

# Analysis: Find buildings near each POI
analysis_results = []
for i, poi in enumerate(pois):
    # 50-unit buffer around POI
    poi_buffer = shapely.buffer(poi, 50)
    
    # Find nearby buildings
    nearby_building_indices = building_tree.query(poi_buffer, predicate='intersects')
    
    analysis_results.append({
        'poi_index': i,
        'poi_location': (poi.x, poi.y),
        'nearby_buildings': len(nearby_building_indices),
        'building_indices': nearby_building_indices
    })

# Summary statistics
nearby_counts = [r['nearby_buildings'] for r in analysis_results]
print(f"POI analysis complete:")
print(f"Average buildings within 50 units: {np.mean(nearby_counts):.1f}")
print(f"Max buildings near one POI: {np.max(nearby_counts)}")
print(f"POIs with no nearby buildings: {sum(1 for c in nearby_counts if c == 0)}")

# Find POI clusters: POIs within 100 units of each other
cluster_threshold = 100
poi_clusters = []

for i, poi in enumerate(pois):
    cluster_buffer = shapely.buffer(poi, cluster_threshold)
    nearby_poi_indices = poi_tree.query(cluster_buffer, predicate='intersects')
    
    # Remove self from results
    nearby_poi_indices = nearby_poi_indices[nearby_poi_indices != i]
    
    if len(nearby_poi_indices) > 0:
        poi_clusters.append({
            'center_poi': i,
            'cluster_size': len(nearby_poi_indices) + 1,  # Include self
            'cluster_members': nearby_poi_indices
        })

print(f"Found {len(poi_clusters)} POI clusters")
if poi_clusters:
    largest_cluster = max(poi_clusters, key=lambda x: x['cluster_size'])
    print(f"Largest cluster has {largest_cluster['cluster_size']} POIs")
```