# Feature Detection and Description

OpenCV's 2D Features Framework provides comprehensive tools for detecting, describing, and matching distinctive features in images. These features are essential for tasks like object recognition, image stitching, 3D reconstruction, and visual tracking.

## Capabilities

### Feature Detectors

#### SIFT (Scale-Invariant Feature Transform)

Patent-free since 2020, SIFT is one of the most robust feature detection algorithms, invariant to scale, rotation, and illumination changes.

```python { .api }
cv2.SIFT_create(
    nfeatures=0,                 # Number of best features to retain (0 = all)
    nOctaveLayers=3,             # Number of layers in each octave
    contrastThreshold=0.04,      # Contrast threshold for filtering weak features
    edgeThreshold=10,            # Edge threshold for filtering edge responses
    sigma=1.6                    # Gaussian sigma for the first octave
) -> cv2.SIFT
```

**Returns**: SIFT detector/descriptor object

**Common usage**:
```python
sift = cv2.SIFT_create()
keypoints, descriptors = sift.detectAndCompute(image, None)
```

#### ORB (Oriented FAST and Rotated BRIEF)

A fast, efficient alternative to SIFT and SURF, ORB is rotation invariant and resistant to noise.

```python { .api }
cv2.ORB_create(
    nfeatures=500,               # Maximum number of features to retain
    scaleFactor=1.2,             # Pyramid decimation ratio
    nlevels=8,                   # Number of pyramid levels
    edgeThreshold=31,            # Size of border where features are not detected
    firstLevel=0,                # Level of pyramid to put source image
    WTA_K=2,                     # Number of points for BRIEF descriptor (2, 3, 4)
    scoreType=cv2.ORB_HARRIS_SCORE,  # HARRIS_SCORE or FAST_SCORE
    patchSize=31,                # Size of patch used by oriented BRIEF
    fastThreshold=20             # FAST threshold
) -> cv2.ORB
```

**Returns**: ORB detector/descriptor object

**Score types**:
- `cv2.ORB_HARRIS_SCORE` - Harris corner measure for ranking features
- `cv2.ORB_FAST_SCORE` - FAST score for ranking features

#### AKAZE (Accelerated-KAZE)

A fast variant of KAZE that uses binary descriptors, providing good performance with lower computational cost.

```python { .api }
cv2.AKAZE_create(
    descriptor_type=cv2.AKAZE_DESCRIPTOR_MLDB,  # Descriptor type
    descriptor_size=0,           # Size of descriptor (0 = full size)
    descriptor_channels=3,       # Number of channels in descriptor
    threshold=0.001,             # Detector response threshold
    nOctaves=4,                  # Number of octaves
    nOctaveLayers=4,             # Number of sublevels per octave
    diffusivity=cv2.KAZE_DIFF_PM_G2  # Diffusivity type
) -> cv2.AKAZE
```

**Returns**: AKAZE detector/descriptor object

**Descriptor types**:
- `cv2.AKAZE_DESCRIPTOR_KAZE` - Upright KAZE descriptor
- `cv2.AKAZE_DESCRIPTOR_KAZE_UPRIGHT` - Upright KAZE descriptor
- `cv2.AKAZE_DESCRIPTOR_MLDB` - Modified Local Difference Binary descriptor
- `cv2.AKAZE_DESCRIPTOR_MLDB_UPRIGHT` - Upright MLDB descriptor

**Diffusivity types**:
- `cv2.KAZE_DIFF_PM_G1` - Perona-Malik diffusivity
- `cv2.KAZE_DIFF_PM_G2` - Perona-Malik diffusivity (default)
- `cv2.KAZE_DIFF_WEICKERT` - Weickert diffusivity
- `cv2.KAZE_DIFF_CHARBONNIER` - Charbonnier diffusivity

#### BRISK (Binary Robust Invariant Scalable Keypoints)

A binary descriptor algorithm that is fast and provides good performance for real-time applications.

```python { .api }
cv2.BRISK_create(
    thresh=30,                   # AGAST detection threshold score
    octaves=3,                   # Detection octaves (0 = single scale)
    patternScale=1.0             # Scale of sampling pattern
) -> cv2.BRISK
```

**Returns**: BRISK detector/descriptor object

#### KAZE

A multiscale feature detection and description algorithm using nonlinear diffusion filtering.

```python { .api }
cv2.KAZE_create(
    extended=False,              # Use extended 128-element descriptor
    upright=False,               # Use upright (non-rotation invariant) descriptor
    threshold=0.001,             # Detector response threshold
    nOctaves=4,                  # Number of octaves
    nOctaveLayers=4,             # Number of sublevels per octave
    diffusivity=cv2.KAZE_DIFF_PM_G2  # Diffusivity type
) -> cv2.KAZE
```

**Returns**: KAZE detector/descriptor object

#### SimpleBlobDetector

Detects blobs (regions of connected pixels) in images based on various properties like size, color, shape, and convexity.

```python { .api }
cv2.SimpleBlobDetector_create(
    parameters=None              # SimpleBlobDetector_Params object
) -> cv2.SimpleBlobDetector
```

**Returns**: SimpleBlobDetector object

**Parameters class**:
```python
params = cv2.SimpleBlobDetector_Params()

# Threshold parameters
params.minThreshold = 50
params.maxThreshold = 220
params.thresholdStep = 10

# Filter by area
params.filterByArea = True
params.minArea = 100
params.maxArea = 5000

# Filter by circularity
params.filterByCircularity = True
params.minCircularity = 0.1

# Filter by convexity
params.filterByConvexity = True
params.minConvexity = 0.87

# Filter by inertia
params.filterByInertia = True
params.minInertiaRatio = 0.01

# Filter by color
params.filterByColor = True
params.blobColor = 255  # 0 for dark blobs, 255 for light blobs

detector = cv2.SimpleBlobDetector_create(params)
```

#### MSER (Maximally Stable Extremal Regions)

Detects stable regions in images across different threshold levels, useful for text detection and wide baseline matching.

```python { .api }
cv2.MSER_create(
    delta=5,                     # Delta for MSER test
    min_area=60,                 # Minimum area of region
    max_area=14400,              # Maximum area of region
    max_variation=0.25,          # Maximum variation in region stability
    min_diversity=0.2,           # Minimum diversity
    max_evolution=200,           # Maximum evolution steps
    area_threshold=1.01,         # Area threshold for filtering
    min_margin=0.003,            # Minimum margin
    edge_blur_size=5             # Edge blur size
) -> cv2.MSER
```

**Returns**: MSER detector object

**Note**: MSER.detect() returns regions as contours, not KeyPoint objects.

#### FAST (Features from Accelerated Segment Test)

A high-speed corner detection algorithm, often used as the first stage in feature detection pipelines.

```python { .api }
cv2.FastFeatureDetector_create(
    threshold=10,                # Threshold on difference between intensity
    nonmaxSuppression=True,      # Apply non-maximum suppression
    type=cv2.FAST_FEATURE_DETECTOR_TYPE_9_16  # FAST detector type
) -> cv2.FastFeatureDetector
```

**Returns**: FAST detector object

**Detector types**:
- `cv2.FAST_FEATURE_DETECTOR_TYPE_5_8` - 8 pixels on circle of radius 1
- `cv2.FAST_FEATURE_DETECTOR_TYPE_7_12` - 12 pixels on circle of radius 2
- `cv2.FAST_FEATURE_DETECTOR_TYPE_9_16` - 16 pixels on circle of radius 3

#### AGAST (Adaptive and Generic Accelerated Segment Test)

An improved version of FAST with better performance and adaptivity.

```python { .api }
cv2.AgastFeatureDetector_create(
    threshold=10,                # Threshold on difference between intensity
    nonmaxSuppression=True,      # Apply non-maximum suppression
    type=cv2.AGAST_FEATURE_DETECTOR_OAST_9_16  # AGAST detector type
) -> cv2.AgastFeatureDetector
```

**Returns**: AGAST detector object

**Detector types**:
- `cv2.AGAST_FEATURE_DETECTOR_AGAST_5_8` - AGAST-5_8 decision tree
- `cv2.AGAST_FEATURE_DETECTOR_AGAST_7_12d` - AGAST-7_12d decision tree
- `cv2.AGAST_FEATURE_DETECTOR_AGAST_7_12s` - AGAST-7_12s decision tree
- `cv2.AGAST_FEATURE_DETECTOR_OAST_9_16` - OAST-9_16 decision tree

#### GFTT (Good Features To Track)

Shi-Tomasi corner detector, which finds the most prominent corners in an image.

```python { .api }
cv2.GFTTDetector_create(
    maxCorners=1000,             # Maximum number of corners to return
    qualityLevel=0.01,           # Minimal accepted quality of corners
    minDistance=1,               # Minimum distance between corners
    blockSize=3,                 # Size of averaging block
    useHarrisDetector=False,     # Use Harris detector (vs. Shi-Tomasi)
    k=0.04                       # Free parameter of Harris detector
) -> cv2.GFTTDetector
```

**Returns**: GFTT detector object

### Feature2D Base Class Interface

All feature detectors inherit from the `Feature2D` base class and share these common methods:

```python { .api }
detector.detect(
    image,                       # Input image (grayscale)
    mask=None                    # Optional mask specifying detection region
) -> keypoints
```

**Returns**: List of KeyPoint objects

```python { .api }
detector.compute(
    image,                       # Input image (grayscale)
    keypoints                    # List of KeyPoint objects to compute descriptors for
) -> keypoints, descriptors
```

**Returns**:
- `keypoints` - Input keypoints (may be modified)
- `descriptors` - Computed descriptors as numpy array (N × descriptor_size)

```python { .api }
detector.detectAndCompute(
    image,                       # Input image (grayscale)
    mask=None                    # Optional mask specifying detection region
) -> keypoints, descriptors
```

**Returns**:
- `keypoints` - List of detected KeyPoint objects
- `descriptors` - Computed descriptors as numpy array (N × descriptor_size)

**Note**: `detectAndCompute()` is more efficient than calling `detect()` and `compute()` separately.

```python { .api }
detector.empty() -> bool
```

**Returns**: True if the detector object is empty

```python { .api }
detector.getDefaultName() -> str
```

**Returns**: Algorithm name as string

### Descriptor Matching

#### BFMatcher (Brute-Force Matcher)

Matches descriptors by comparing each descriptor in the first set against all descriptors in the second set using a specified distance metric.

```python { .api }
cv2.BFMatcher_create(
    normType=cv2.NORM_L2,        # Distance norm type
    crossCheck=False             # Enable cross-check for more robust matching
) -> cv2.BFMatcher

# Alternative constructor
cv2.BFMatcher(
    normType=cv2.NORM_L2,
    crossCheck=False
) -> cv2.BFMatcher
```

**Returns**: BFMatcher object

**Norm types**:
- `cv2.NORM_L1` - L1 norm (Manhattan distance)
- `cv2.NORM_L2` - L2 norm (Euclidean distance) - for SIFT, SURF
- `cv2.NORM_HAMMING` - Hamming distance - for ORB, BRISK, BRIEF
- `cv2.NORM_HAMMING2` - Hamming distance with 2 bits per dimension
- `cv2.NORM_INF` - Infinity norm

**Cross-check**: When enabled, only returns matches (i,j) where descriptor i in set A is the best match for descriptor j in set B, and vice versa.

#### FlannBasedMatcher

Fast Library for Approximate Nearest Neighbors (FLANN) based matcher, faster than brute-force for large datasets.

```python { .api }
cv2.FlannBasedMatcher_create() -> cv2.FlannBasedMatcher

# Constructor with index parameters
cv2.FlannBasedMatcher(
    indexParams=None,            # Index parameters dictionary
    searchParams=None            # Search parameters dictionary
) -> cv2.FlannBasedMatcher
```

**Returns**: FlannBasedMatcher object

**Index parameters examples**:
```python
# For SIFT/SURF descriptors (float)
index_params = dict(algorithm=1, trees=5)  # FLANN_INDEX_KDTREE

# For ORB descriptors (binary)
index_params = dict(
    algorithm=6,                  # FLANN_INDEX_LSH
    table_number=6,
    key_size=12,
    multi_probe_level=1
)
```

**Search parameters**:
```python
search_params = dict(checks=50)  # Number of times trees should be recursively traversed
```

**FLANN algorithm constants**:
- `FLANN_INDEX_LINEAR = 0` - Linear brute-force search
- `FLANN_INDEX_KDTREE = 1` - Randomized kd-tree (for float descriptors)
- `FLANN_INDEX_KMEANS = 2` - Hierarchical k-means tree
- `FLANN_INDEX_COMPOSITE = 3` - Combination of trees and kmeans
- `FLANN_INDEX_KDTREE_SINGLE = 4` - Single kd-tree
- `FLANN_INDEX_HIERARCHICAL = 5` - Hierarchical clustering
- `FLANN_INDEX_LSH = 6` - Locality-sensitive hashing (for binary descriptors)

#### DescriptorMatcher Common Methods

Both BFMatcher and FlannBasedMatcher inherit from DescriptorMatcher and share these methods:

```python { .api }
matcher.match(
    queryDescriptors,            # Query descriptors (N1 × descriptor_size)
    trainDescriptors,            # Train descriptors (N2 × descriptor_size)
    mask=None                    # Optional mask for valid matches
) -> matches
```

**Returns**: List of DMatch objects (best match for each query descriptor)

```python { .api }
matcher.knnMatch(
    queryDescriptors,            # Query descriptors
    trainDescriptors,            # Train descriptors
    k,                           # Number of best matches to return per descriptor
    mask=None,                   # Optional mask
    compactResult=False          # Remove empty matches from result
) -> matches
```

**Returns**: List of lists of DMatch objects (k best matches per query descriptor)

**Common usage with ratio test**:
```python
matches = matcher.knnMatch(desc1, desc2, k=2)
# Apply Lowe's ratio test
good_matches = []
for m, n in matches:
    if m.distance < 0.75 * n.distance:
        good_matches.append(m)
```

```python { .api }
matcher.radiusMatch(
    queryDescriptors,            # Query descriptors
    trainDescriptors,            # Train descriptors
    maxDistance,                 # Maximum allowed distance
    mask=None,                   # Optional mask
    compactResult=False          # Remove empty matches from result
) -> matches
```

**Returns**: List of lists of DMatch objects (all matches within maxDistance)

```python { .api }
matcher.add(
    descriptors                  # List of descriptor arrays to add to training set
) -> None
```

Adds descriptors to the training set for multi-image matching.

```python { .api }
matcher.train() -> None
```

Trains the matcher (required for some FLANN-based matchers).

```python { .api }
matcher.clear() -> None
```

Clears the training descriptor set.

```python { .api }
matcher.empty() -> bool
```

**Returns**: True if the matcher has no training data

### Drawing Functions

#### drawKeypoints

Draws keypoints on an image, optionally showing their size, orientation, and other properties.

```python { .api }
cv2.drawKeypoints(
    image,                       # Source image
    keypoints,                   # List of KeyPoint objects to draw
    outImage,                    # Output image (can be the same as input)
    color=(0, 255, 0),          # Keypoint color (B, G, R)
    flags=cv2.DRAW_MATCHES_FLAGS_DEFAULT  # Drawing flags
) -> outImage
```

**Returns**: Output image with keypoints drawn

**Drawing flags**:
- `cv2.DRAW_MATCHES_FLAGS_DEFAULT` - Simple circles at keypoint locations
- `cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS` - Draw circles with size and orientation
- `cv2.DRAW_MATCHES_FLAGS_NOT_DRAW_SINGLE_POINTS` - Don't draw single points
- `cv2.DRAW_MATCHES_FLAGS_DRAW_OVER_OUTIMG` - Draw on existing output image

**Usage**:
```python
# Simple drawing
img_keypoints = cv2.drawKeypoints(img, keypoints, None, color=(0, 255, 0))

# Rich keypoints showing size and orientation
img_keypoints = cv2.drawKeypoints(
    img, keypoints, None,
    color=(0, 255, 0),
    flags=cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS
)
```

#### drawMatches

Draws matches between keypoints from two images side by side.

```python { .api }
cv2.drawMatches(
    img1,                        # First source image
    keypoints1,                  # Keypoints from first image
    img2,                        # Second source image
    keypoints2,                  # Keypoints from second image
    matches1to2,                 # List of DMatch objects
    outImg,                      # Output image (None = create new)
    matchColor=(0, 255, 0),     # Color for matches (B, G, R)
    singlePointColor=(255, 0, 0), # Color for single points
    matchesMask=None,            # Mask determining which matches to draw
    flags=cv2.DRAW_MATCHES_FLAGS_DEFAULT  # Drawing flags
) -> outImg
```

**Returns**: Output image showing both images with matches drawn between them

**Parameters**:
- `matchesMask` - List of bytes (0/1) same length as matches, 1 = draw match
- `matchColor` - Color for match lines, or tuple for random colors per match
- `singlePointColor` - Color for keypoints without matches

**Usage**:
```python
# Draw all matches
img_matches = cv2.drawMatches(
    img1, kp1, img2, kp2, matches,
    None, flags=cv2.DRAW_MATCHES_FLAGS_NOT_DRAW_SINGLE_POINTS
)

# Draw only good matches with mask
mask = [[1] if m.distance < 50 else [0] for m in matches]
img_matches = cv2.drawMatches(
    img1, kp1, img2, kp2, matches, None,
    matchesMask=mask, flags=cv2.DRAW_MATCHES_FLAGS_NOT_DRAW_SINGLE_POINTS
)
```

#### drawMatchesKnn

Draws k best matches for each keypoint from two images.

```python { .api }
cv2.drawMatchesKnn(
    img1,                        # First source image
    keypoints1,                  # Keypoints from first image
    img2,                        # Second source image
    keypoints2,                  # Keypoints from second image
    matches1to2,                 # List of lists of DMatch objects (from knnMatch)
    outImg,                      # Output image (None = create new)
    matchColor=(0, 255, 0),     # Color for matches
    singlePointColor=(255, 0, 0), # Color for single points
    matchesMask=None,            # Mask for matches (list of lists)
    flags=cv2.DRAW_MATCHES_FLAGS_DEFAULT  # Drawing flags
) -> outImg
```

**Returns**: Output image showing both images with k best matches per keypoint

**Usage with ratio test**:
```python
# Get k=2 best matches
matches = matcher.knnMatch(desc1, desc2, k=2)

# Apply ratio test and create mask
mask = []
for m, n in matches:
    if m.distance < 0.75 * n.distance:
        mask.append([1, 0])  # Draw first match only
    else:
        mask.append([0, 0])  # Don't draw

img_matches = cv2.drawMatchesKnn(
    img1, kp1, img2, kp2, matches, None,
    matchesMask=mask
)
```

### KeyPoint Class

Represents a detected feature point with its properties.

```python { .api }
cv2.KeyPoint(
    x,                           # X coordinate
    y,                           # Y coordinate
    size,                        # Diameter of meaningful keypoint neighborhood
    angle=-1,                    # Orientation in degrees [0, 360)
    response=0,                  # Response strength
    octave=0,                    # Pyramid octave where keypoint was detected
    class_id=-1                  # Object class (for categorized keypoints)
) -> cv2.KeyPoint
```

**Attributes**:
- `pt` - (x, y) tuple of keypoint coordinates
- `size` - Diameter of the meaningful keypoint neighborhood
- `angle` - Computed orientation of the keypoint (-1 if not applicable)
- `response` - Response strength (used for keypoint ranking)
- `octave` - Pyramid octave in which keypoint was detected
- `class_id` - Object ID for categorizing keypoints

**Methods**:
```python
# Convert keypoints to numpy array of (x, y) coordinates
points = cv2.KeyPoint_convert(keypoints)

# Convert numpy array to keypoints
keypoints = cv2.KeyPoint_convert(points, size=20)

# Get overlap between two keypoints
overlap = cv2.KeyPoint_overlap(kp1, kp2)  # Returns 0-1
```

### DMatch Class

Represents a match between two feature descriptors.

```python { .api }
cv2.DMatch(
    queryIdx,                    # Query descriptor index
    trainIdx,                    # Train descriptor index
    distance                     # Distance between descriptors (lower is better)
) -> cv2.DMatch

# Constructor with image index (for multi-image matching)
cv2.DMatch(
    queryIdx,
    trainIdx,
    imgIdx,                      # Train image index
    distance
) -> cv2.DMatch
```

**Attributes**:
- `queryIdx` - Index of descriptor in query set
- `trainIdx` - Index of descriptor in train set
- `imgIdx` - Index of train image (for multi-image matching)
- `distance` - Distance between descriptors (lower = better match)

**Usage**:
```python
# Sort matches by distance (best matches first)
matches = sorted(matches, key=lambda x: x.distance)

# Get top N matches
good_matches = matches[:50]

# Extract matched keypoint coordinates
src_pts = np.float32([kp1[m.queryIdx].pt for m in matches])
dst_pts = np.float32([kp2[m.trainIdx].pt for m in matches])
```

## Common Workflows

### Basic Feature Detection and Matching

```python
import cv2
import numpy as np

# Read images
img1 = cv2.imread('image1.jpg', cv2.IMREAD_GRAYSCALE)
img2 = cv2.imread('image2.jpg', cv2.IMREAD_GRAYSCALE)

# Create detector
detector = cv2.SIFT_create()

# Detect and compute
kp1, desc1 = detector.detectAndCompute(img1, None)
kp2, desc2 = detector.detectAndCompute(img2, None)

# Create matcher
matcher = cv2.BFMatcher(cv2.NORM_L2, crossCheck=False)

# Match descriptors
matches = matcher.knnMatch(desc1, desc2, k=2)

# Apply ratio test
good_matches = []
for m, n in matches:
    if m.distance < 0.75 * n.distance:
        good_matches.append(m)

# Draw matches
img_matches = cv2.drawMatches(
    img1, kp1, img2, kp2, good_matches, None,
    flags=cv2.DRAW_MATCHES_FLAGS_NOT_DRAW_SINGLE_POINTS
)

cv2.imshow('Matches', img_matches)
cv2.waitKey(0)
```

### Finding Homography from Matches

```python
# Extract matched point coordinates
if len(good_matches) >= 4:
    src_pts = np.float32([kp1[m.queryIdx].pt for m in good_matches]).reshape(-1, 1, 2)
    dst_pts = np.float32([kp2[m.trainIdx].pt for m in good_matches]).reshape(-1, 1, 2)

    # Find homography
    H, mask = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC, 5.0)

    # Use homography to transform image
    h, w = img1.shape
    img1_warped = cv2.warpPerspective(img1, H, (w, h))
```

### Feature Detection with Region of Interest

```python
# Create mask (detect features only in specific region)
mask = np.zeros(img.shape[:2], dtype=np.uint8)
mask[100:400, 200:600] = 255  # ROI

# Detect keypoints in masked region
keypoints = detector.detect(img, mask=mask)
keypoints, descriptors = detector.compute(img, keypoints)
```
