# Contour Detection and Shape Analysis

OpenCV provides a comprehensive suite of functions for detecting contours in binary images and analyzing their geometric properties. Contours are curves that join continuous points along a boundary, representing the outline of objects in images. These tools are essential for object detection, shape recognition, and image segmentation tasks.

## Capabilities

### Contour Detection

Find and draw contours in binary images. Contours are typically found after edge detection or thresholding operations.

```python { .api }
cv2.findContours(image, mode, method) -> contours, hierarchy
```
Finds contours in a binary image.

**Parameters:**
- `image` (ndarray): Source, an 8-bit single-channel image. Non-zero pixels are treated as 1's, zero pixels remain 0's.
- `mode` (int): Contour retrieval mode (see constants below).
- `method` (int): Contour approximation method (see constants below).

**Returns:**
- `contours` (list): List of contours found. Each contour is a NumPy array of (x,y) coordinates of boundary points.
- `hierarchy` (ndarray): Optional output vector containing information about the image topology. It has as many elements as the number of contours.

```python { .api }
cv2.drawContours(image, contours, contourIdx, color, thickness=None, lineType=None, hierarchy=None, maxLevel=None, offset=None) -> image
```
Draws contours outlines or filled contours on an image.

**Parameters:**
- `image` (ndarray): Destination image.
- `contours` (list): All the input contours. Each contour is stored as a point vector.
- `contourIdx` (int): Parameter indicating a contour to draw. If it is negative, all the contours are drawn.
- `color` (tuple): Color of the contours (BGR format).
- `thickness` (int, optional): Thickness of lines the contours are drawn with. If negative (e.g., -1), the contour interiors are drawn. Default is 1.
- `lineType` (int, optional): Line connectivity. See `cv2.LINE_4`, `cv2.LINE_8`, `cv2.LINE_AA`.
- `hierarchy` (ndarray, optional): Optional information about hierarchy. Only needed if you want to draw only some of the contours.
- `maxLevel` (int, optional): Maximal level for drawn contours. If 0, only the specified contour is drawn. If 1, the function draws the contour and all nested contours. If 2, the function draws the contours, all nested contours, and so on.
- `offset` (tuple, optional): Optional contour shift parameter. Shift all the drawn contours by the specified offset=(dx,dy).

**Returns:**
- `image` (ndarray): The modified image with contours drawn.

**Contour Retrieval Modes:**

```python { .api }
cv2.RETR_EXTERNAL
```
Retrieves only the extreme outer contours. It sets `hierarchy[i][2]=hierarchy[i][3]=-1` for all contours.

```python { .api }
cv2.RETR_LIST
```
Retrieves all contours without establishing any hierarchical relationships.

```python { .api }
cv2.RETR_CCOMP
```
Retrieves all contours and organizes them into a two-level hierarchy. At the top level, there are external boundaries of the components. At the second level, there are boundaries of the holes. If there is another contour inside a hole of a connected component, it is still put at the top level.

```python { .api }
cv2.RETR_TREE
```
Retrieves all contours and reconstructs a full hierarchy of nested contours.

**Contour Approximation Methods:**

```python { .api }
cv2.CHAIN_APPROX_NONE
```
Stores absolutely all the contour points. This means no approximation - every point on the contour boundary is stored.

```python { .api }
cv2.CHAIN_APPROX_SIMPLE
```
Compresses horizontal, vertical, and diagonal segments and leaves only their end points. For example, an up-right rectangular contour is encoded with 4 points.

```python { .api }
cv2.CHAIN_APPROX_TC89_L1
```
Applies one of the flavors of the Teh-Chin chain approximation algorithm using the L1 distance metric.

```python { .api }
cv2.CHAIN_APPROX_TC89_KCOS
```
Applies one of the flavors of the Teh-Chin chain approximation algorithm using the cosine metric.

### Contour Properties

Calculate basic properties of contours such as area, perimeter, and convexity.

```python { .api }
cv2.contourArea(contour, oriented=None) -> area
```
Calculates a contour area.

**Parameters:**
- `contour` (ndarray): Input vector of 2D points (contour vertices).
- `oriented` (bool, optional): Oriented area flag. If True, the function returns a signed area value, depending on the contour orientation (clockwise or counter-clockwise). Using this feature, you can determine the orientation of a contour by taking the sign of the area. Default is False.

**Returns:**
- `area` (float): Area enclosed by the contour in pixels.

```python { .api }
cv2.arcLength(curve, closed) -> perimeter
```
Calculates a contour perimeter or a curve length.

**Parameters:**
- `curve` (ndarray): Input vector of 2D points.
- `closed` (bool): Flag indicating whether the curve is closed.

**Returns:**
- `perimeter` (float): Length of the curve in pixels.

```python { .api }
cv2.isContourConvex(contour) -> bool
```
Tests a contour convexity.

**Parameters:**
- `contour` (ndarray): Input vector of 2D points.

**Returns:**
- `bool`: True if the contour is convex, False otherwise.

### Contour Approximation

Approximate contours to simpler shapes with fewer vertices.

```python { .api }
cv2.approxPolyDP(curve, epsilon, closed) -> approxCurve
```
Approximates a polygonal curve with the specified precision using the Douglas-Peucker algorithm.

**Parameters:**
- `curve` (ndarray): Input vector of 2D points stored in NumPy array.
- `epsilon` (float): Parameter specifying the approximation accuracy. This is the maximum distance between the original curve and its approximation. Typically, epsilon = 0.01 to 0.1 * perimeter.
- `closed` (bool): If True, the approximated curve is closed (its first and last vertices are connected). Otherwise, it is not closed.

**Returns:**
- `approxCurve` (ndarray): Result of the approximation. The type should match the type of the input curve.

```python { .api }
cv2.convexHull(points, hull=None, clockwise=None, returnPoints=None) -> hull
```
Finds the convex hull of a point set.

**Parameters:**
- `points` (ndarray): Input 2D point set, stored in NumPy array.
- `hull` (ndarray, optional): Output convex hull. It is either an array of indices of the hull points or an array of the hull points themselves.
- `clockwise` (bool, optional): Orientation flag. If True, the output convex hull is oriented clockwise. Otherwise, it is oriented counter-clockwise. Default is False.
- `returnPoints` (bool, optional): Operation flag. If True, the function returns convex hull points. Otherwise, it returns indices of the convex hull points. Default is True.

**Returns:**
- `hull` (ndarray): Output convex hull as an array of points or indices.

### Bounding Shapes

Calculate various bounding shapes around contours for object localization and orientation detection.

```python { .api }
cv2.boundingRect(array) -> (x, y, width, height)
```
Calculates the up-right bounding rectangle of a point set or non-zero pixels of gray-scale image.

**Parameters:**
- `array` (ndarray): Input gray-scale image or 2D point set.

**Returns:**
- `x` (int): X-coordinate of the top-left corner of the bounding rectangle.
- `y` (int): Y-coordinate of the top-left corner of the bounding rectangle.
- `width` (int): Width of the bounding rectangle.
- `height` (int): Height of the bounding rectangle.

```python { .api }
cv2.minAreaRect(points) -> ((center_x, center_y), (width, height), angle)
```
Finds a rotated rectangle of the minimum area enclosing the input 2D point set.

**Parameters:**
- `points` (ndarray): Input vector of 2D points.

**Returns:**
- `center` (tuple): Center of the rectangle as (center_x, center_y).
- `size` (tuple): Size of the rectangle as (width, height).
- `angle` (float): Rotation angle in degrees. The angle is measured in a clockwise direction with respect to the horizontal axis. Values range from -90 to 0 degrees.

```python { .api }
cv2.minEnclosingCircle(points) -> ((center_x, center_y), radius)
```
Finds a circle of the minimum area enclosing a 2D point set.

**Parameters:**
- `points` (ndarray): Input vector of 2D points.

**Returns:**
- `center` (tuple): Center of the circle as (center_x, center_y).
- `radius` (float): Radius of the circle.

```python { .api }
cv2.minEnclosingTriangle(points) -> retval, triangle
```
Finds a triangle of minimum area enclosing a 2D point set and returns its area.

**Parameters:**
- `points` (ndarray): Input vector of 2D points.

**Returns:**
- `retval` (float): Area of the minimum enclosing triangle.
- `triangle` (ndarray): Output vector of three 2D points defining the vertices of the triangle.

```python { .api }
cv2.boxPoints(box) -> points
```
Finds the four vertices of a rotated rectangle. Useful for drawing rotated rectangles from minAreaRect output.

**Parameters:**
- `box` (tuple): Rotated rectangle as returned by minAreaRect: ((center_x, center_y), (width, height), angle).

**Returns:**
- `points` (ndarray): Array of four points (4x2 float32 array), one for each vertex of the rotated rectangle.

```python { .api }
cv2.fitEllipse(points) -> ((center_x, center_y), (width, height), angle)
```
Fits an ellipse around a set of 2D points.

**Parameters:**
- `points` (ndarray): Input vector of 2D points. Must have at least 5 points.

**Returns:**
- `center` (tuple): Center of the ellipse as (center_x, center_y).
- `axes` (tuple): Length of the ellipse axes as (major_axis, minor_axis).
- `angle` (float): Rotation angle of the ellipse in degrees.

```python { .api }
cv2.fitLine(points, distType, param, reps, aeps) -> line
```
Fits a line to a 2D or 3D point set.

**Parameters:**
- `points` (ndarray): Input vector of 2D or 3D points.
- `distType` (int): Distance used by the M-estimator (e.g., `cv2.DIST_L2`, `cv2.DIST_L1`, `cv2.DIST_L12`, `cv2.DIST_FAIR`, `cv2.DIST_WELSCH`, `cv2.DIST_HUBER`).
- `param` (float): Numerical parameter (C) for some types of distances. If it is 0, an optimal value is chosen.
- `reps` (float): Sufficient accuracy for the radius (distance between the coordinate origin and the line).
- `aeps` (float): Sufficient accuracy for the angle. 0.01 would be a good default value.

**Returns:**
- `line` (ndarray): Output line parameters. For 2D fitting, it contains (vx, vy, x0, y0) where (vx, vy) is a normalized vector collinear to the line and (x0, y0) is a point on the line. For 3D fitting, it contains (vx, vy, vz, x0, y0, z0).

### Shape Moments

Calculate image moments for shape analysis and feature extraction. Moments are weighted averages of image pixel intensities.

```python { .api }
cv2.moments(array, binaryImage=None) -> moments_dict
```
Calculates all of the moments up to the third order of a polygon or rasterized shape.

**Parameters:**
- `array` (ndarray): Raster image (single-channel, 8-bit or floating-point 2D array) or an array of 2D points (contour vertices).
- `binaryImage` (bool, optional): If True, all non-zero image pixels are treated as 1's. Default is False.

**Returns:**
- `moments_dict` (dict): Dictionary containing spatial moments (m00, m10, m01, m20, m11, m02, m30, m21, m12, m03), central moments (mu20, mu11, mu02, mu30, mu21, mu12, mu03), and normalized central moments (nu20, nu11, nu02, nu30, nu21, nu12, nu03).

**Notable moment values:**
- `m00`: Area (for binary images) or sum of pixel intensities
- `m10/m00` and `m01/m00`: Centroid coordinates (center of mass)

```python { .api }
cv2.HuMoments(moments) -> hu
```
Calculates seven Hu invariants from spatial moments.

**Parameters:**
- `moments` (dict): Input moments computed with `cv2.moments()`.

**Returns:**
- `hu` (ndarray): Output Hu invariants as a 7x1 array. These values are invariant to translation, scale, and rotation, making them useful for shape matching.

### Shape Comparison

Compare shapes using contour matching to determine similarity between different contours.

```python { .api }
cv2.matchShapes(contour1, contour2, method, parameter) -> similarity
```
Compares two shapes using Hu moments.

**Parameters:**
- `contour1` (ndarray): First contour or grayscale image.
- `contour2` (ndarray): Second contour or grayscale image.
- `method` (int): Comparison method. One of:
  - `cv2.CONTOURS_MATCH_I1`: I1 = sum_i |1/m_i^A - 1/m_i^B|
  - `cv2.CONTOURS_MATCH_I2`: I2 = sum_i |m_i^A - m_i^B|
  - `cv2.CONTOURS_MATCH_I3`: I3 = max_i |m_i^A - m_i^B| / |m_i^A|
- `parameter` (float): Method-specific parameter (not supported now, use 0).

**Returns:**
- `similarity` (float): Similarity measure. A value of 0 indicates a perfect match, while higher values indicate greater dissimilarity.

### Point Tests

Test spatial relationships between points and contours.

```python { .api }
cv2.pointPolygonTest(contour, pt, measureDist) -> result
```
Performs a point-in-contour test.

**Parameters:**
- `contour` (ndarray): Input contour.
- `pt` (tuple): Point tested against the contour as (x, y).
- `measureDist` (bool): If True, the function estimates the signed distance from the point to the nearest contour edge. If False, the function only checks if the point is inside, outside, or on the edge.

**Returns:**
- `result` (float):
  - If `measureDist=False`: Returns +1 (inside), -1 (outside), or 0 (on edge).
  - If `measureDist=True`: Returns the signed distance. Positive for inside, negative for outside, zero for on edge.
