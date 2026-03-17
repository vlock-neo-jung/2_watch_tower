# Image Processing

OpenCV's image processing module (`imgproc`) provides comprehensive functionality for image filtering, geometric transformations, color space conversion, feature detection, segmentation, and more. All functions are accessed through the `cv2` namespace.

## Capabilities

### Filtering

Image filtering operations for smoothing, sharpening, edge detection, and noise reduction.

#### Smoothing Filters

```python { .api }
cv2.blur(src, ksize, dst=None, anchor=None, borderType=None) -> dst
```

Applies average blur filter (box filter normalized).

- **src**: Input image
- **ksize**: Kernel size (width, height) tuple
- **anchor**: Anchor point (default: kernel center)
- **borderType**: Border extrapolation method
- **Returns**: Blurred image

```python { .api }
cv2.GaussianBlur(src, ksize, sigmaX, dst=None, sigmaY=None, borderType=None) -> dst
```

Applies Gaussian blur filter using a Gaussian kernel.

- **src**: Input image
- **ksize**: Kernel size (width, height) - must be positive and odd
- **sigmaX**: Gaussian kernel standard deviation in X direction
- **sigmaY**: Gaussian kernel standard deviation in Y direction (default: sigmaX)
- **borderType**: Border extrapolation method
- **Returns**: Blurred image

```python { .api }
cv2.medianBlur(src, ksize, dst=None) -> dst
```

Applies median blur filter. Effective for salt-and-pepper noise removal.

- **src**: Input image
- **ksize**: Aperture linear size (must be odd and greater than 1)
- **Returns**: Blurred image

```python { .api }
cv2.bilateralFilter(src, d, sigmaColor, sigmaSpace, dst=None, borderType=None) -> dst
```

Applies bilateral filter for edge-preserving smoothing.

- **src**: Input image (8-bit or floating-point, 1 or 3 channels)
- **d**: Diameter of pixel neighborhood
- **sigmaColor**: Filter sigma in color space
- **sigmaSpace**: Filter sigma in coordinate space
- **borderType**: Border extrapolation method
- **Returns**: Filtered image

```python { .api }
cv2.boxFilter(src, ddepth, ksize, dst=None, anchor=None, normalize=True, borderType=None) -> dst
```

Applies box filter (unnormalized if normalize=False).

- **src**: Input image
- **ddepth**: Output image depth (-1 uses source depth)
- **ksize**: Kernel size
- **normalize**: Whether to normalize the kernel
- **Returns**: Filtered image

```python { .api }
cv2.sqrBoxFilter(src, ddepth, ksize, dst=None, anchor=None, normalize=True, borderType=None) -> dst
```

Calculates normalized squared box filter (useful for local variance computation).

- **src**: Input image
- **ddepth**: Output image depth (-1 uses source depth)
- **ksize**: Kernel size
- **normalize**: Whether to normalize the kernel
- **Returns**: Filtered image

#### Custom Convolution

```python { .api }
cv2.filter2D(src, ddepth, kernel, dst=None, anchor=None, delta=0, borderType=None) -> dst
```

Convolves image with a custom kernel.

- **src**: Input image
- **ddepth**: Desired depth of destination image (-1 uses source depth)
- **kernel**: Convolution kernel (single-channel floating-point matrix)
- **anchor**: Anchor point within kernel (default: kernel center)
- **delta**: Value added to filtered results
- **borderType**: Border extrapolation method
- **Returns**: Filtered image

```python { .api }
cv2.sepFilter2D(src, ddepth, kernelX, kernelY, dst=None, anchor=None, delta=0, borderType=None) -> dst
```

Applies separable linear filter (more efficient for separable kernels).

- **src**: Input image
- **ddepth**: Output image depth
- **kernelX**: Coefficients for filtering rows
- **kernelY**: Coefficients for filtering columns
- **Returns**: Filtered image

#### Derivative Filters

```python { .api }
cv2.Sobel(src, ddepth, dx, dy, ksize=3, scale=1, delta=0, borderType=None) -> dst
```

Calculates image derivatives using Sobel operator.

- **src**: Input image
- **ddepth**: Output image depth
- **dx**: Order of derivative in x direction
- **dy**: Order of derivative in y direction
- **ksize**: Size of extended Sobel kernel (1, 3, 5, or 7)
- **scale**: Scale factor for computed derivative values
- **delta**: Value added to results
- **Returns**: Derivative image

```python { .api }
cv2.Scharr(src, ddepth, dx, dy, scale=1, delta=0, borderType=None) -> dst
```

Calculates image derivatives using Scharr operator (more accurate than 3x3 Sobel).

- **src**: Input image
- **ddepth**: Output image depth
- **dx**: Order of derivative in x (0 or 1)
- **dy**: Order of derivative in y (0 or 1)
- **scale**: Scale factor
- **delta**: Value added to results
- **Returns**: Derivative image

```python { .api }
cv2.Laplacian(src, ddepth, ksize=1, scale=1, delta=0, borderType=None) -> dst
```

Calculates Laplacian of image (sum of second derivatives).

- **src**: Input image
- **ddepth**: Output image depth
- **ksize**: Aperture size (must be positive and odd)
- **scale**: Scale factor
- **delta**: Value added to results
- **Returns**: Laplacian image

#### Edge Detection

```python { .api }
cv2.Canny(image, threshold1, threshold2, edges=None, apertureSize=3, L2gradient=False) -> edges
```

Detects edges using the Canny algorithm.

- **image**: 8-bit input image
- **threshold1**: First threshold for hysteresis
- **threshold2**: Second threshold for hysteresis
- **apertureSize**: Aperture size for Sobel operator
- **L2gradient**: Use L2 norm for gradient magnitude (more accurate but slower)
- **Returns**: Binary edge map

#### Corner Detection

Corner detection algorithms for identifying salient points in images, useful for feature tracking and image matching.

```python { .api }
cv2.goodFeaturesToTrack(image, maxCorners, qualityLevel, minDistance, corners=None, mask=None, blockSize=3, useHarrisDetector=False, k=0.04) -> corners
```

Determines strong corners on an image using Shi-Tomasi corner detection method.

- **image**: Input 8-bit or floating-point 32-bit, single-channel image
- **maxCorners**: Maximum number of corners to return (if ≤ 0, no limit is set)
- **qualityLevel**: Parameter characterizing minimal accepted quality of image corners (multiplied by best corner quality measure)
- **minDistance**: Minimum possible Euclidean distance between returned corners
- **mask**: Optional region of interest (CV_8UC1, same size as image)
- **blockSize**: Size of average block for computing derivative covariation matrix
- **useHarrisDetector**: Whether to use Harris detector (true) or cornerMinEigenVal (false)
- **k**: Free parameter of Harris detector (used if useHarrisDetector=True)
- **Returns**: Array of detected corners

```python { .api }
cv2.cornerHarris(src, blockSize, ksize, k, dst=None, borderType=cv2.BORDER_DEFAULT) -> dst
```

Harris corner detector.

- **src**: Input single-channel 8-bit or floating-point image
- **blockSize**: Neighborhood size (see cornerEigenValsAndVecs)
- **ksize**: Aperture parameter for the Sobel operator
- **k**: Harris detector free parameter
- **borderType**: Pixel extrapolation method (BORDER_WRAP not supported)
- **Returns**: Image to store the Harris detector responses (type CV_32FC1, same size as src)

```python { .api }
cv2.cornerSubPix(image, corners, winSize, zeroZone, criteria) -> corners
```

Refines the corner locations to sub-pixel accuracy.

- **image**: Input single-channel, 8-bit or float image
- **corners**: Initial coordinates of input corners and refined coordinates provided for output
- **winSize**: Half of the side length of the search window (e.g., if winSize=Size(5,5), then an 11×11 search window is used)
- **zeroZone**: Half of size of the dead region in the middle of the search zone (value of (-1,-1) indicates no such size)
- **criteria**: Criteria for termination of the iterative corner refinement process (TermCriteria)
- **Returns**: Refined corner coordinates (modifies corners in-place)

#### Hough Transforms

Hough transforms detect lines, circles, and other shapes in images, typically applied after edge detection.

```python { .api }
cv2.HoughLines(image, rho, theta, threshold, lines=None, srn=0, stn=0, min_theta=0, max_theta=np.pi) -> lines
```

Detects lines using the standard Hough Line Transform.

- **image**: 8-bit, single-channel binary source image (typically edge map from Canny)
- **rho**: Distance resolution in pixels of the Hough accumulator
- **theta**: Angle resolution in radians of the Hough accumulator
- **threshold**: Accumulator threshold parameter (minimum votes to detect a line)
- **srn**: For multi-scale Hough transform (default 0 for classical)
- **stn**: For multi-scale Hough transform (default 0 for classical)
- **min_theta**: Minimum angle to check for lines (default 0)
- **max_theta**: Maximum angle to check for lines (default π)
- **Returns**: Array of lines in (rho, theta) representation, or None

```python { .api }
cv2.HoughLinesP(image, rho, theta, threshold, lines=None, minLineLength=0, maxLineGap=0) -> lines
```

Detects line segments using the Probabilistic Hough Line Transform.

- **image**: 8-bit, single-channel binary source image
- **rho**: Distance resolution in pixels of the Hough accumulator
- **theta**: Angle resolution in radians of the Hough accumulator
- **threshold**: Accumulator threshold parameter
- **minLineLength**: Minimum line length (shorter lines are rejected)
- **maxLineGap**: Maximum gap between points on the same line to link them
- **Returns**: Array of line segments as (x1, y1, x2, y2), or None

```python { .api }
cv2.HoughCircles(image, method, dp, minDist, circles=None, param1=100, param2=100, minRadius=0, maxRadius=0) -> circles
```

Detects circles using the Hough Circle Transform.

- **image**: 8-bit, single-channel grayscale input image
- **method**: Detection method (use cv2.HOUGH_GRADIENT or cv2.HOUGH_GRADIENT_ALT)
- **dp**: Inverse ratio of accumulator resolution to image resolution
- **minDist**: Minimum distance between detected circle centers
- **param1**: For HOUGH_GRADIENT: higher threshold for Canny edge detector
- **param2**: For HOUGH_GRADIENT: accumulator threshold for circle centers
- **minRadius**: Minimum circle radius
- **maxRadius**: Maximum circle radius (0 = no limit)
- **Returns**: Array of detected circles as (x, y, radius), or None

**Usage Example:**

```python
import cv2
import numpy as np

# Detect lines
edges = cv2.Canny(image, 50, 150)
lines = cv2.HoughLinesP(edges, 1, np.pi/180, threshold=100, minLineLength=50, maxLineGap=10)

if lines is not None:
    for line in lines:
        x1, y1, x2, y2 = line[0]
        cv2.line(image, (x1, y1), (x2, y2), (0, 255, 0), 2)

# Detect circles
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, dp=1, minDist=20,
                           param1=50, param2=30, minRadius=10, maxRadius=50)

if circles is not None:
    circles = np.uint16(np.around(circles))
    for circle in circles[0, :]:
        cv2.circle(image, (circle[0], circle[1]), circle[2], (0, 255, 0), 2)
```

#### Border Handling Constants

```python { .api }
cv2.BORDER_CONSTANT      # Constant border (iiiiii|abcdefgh|iiiiiii)
cv2.BORDER_REPLICATE     # Replicate border (aaaaaa|abcdefgh|hhhhhhh)
cv2.BORDER_REFLECT       # Reflect border (fedcba|abcdefgh|hgfedcb)
cv2.BORDER_WRAP          # Wrap border (cdefgh|abcdefgh|abcdefg)
cv2.BORDER_REFLECT_101   # Reflect 101 border (gfedcb|abcdefgh|gfedcba)
cv2.BORDER_DEFAULT       # Same as BORDER_REFLECT_101
cv2.BORDER_ISOLATED      # Do not extrapolate beyond image
```

### Morphological Operations

Mathematical morphology operations for shape processing and noise removal.

```python { .api }
cv2.erode(src, kernel, dst=None, anchor=None, iterations=1, borderType=None, borderValue=None) -> dst
```

Erodes image using specified structuring element.

- **src**: Input image
- **kernel**: Structuring element
- **anchor**: Anchor position within element
- **iterations**: Number of times erosion is applied
- **borderType**: Border extrapolation method
- **borderValue**: Border value for constant border
- **Returns**: Eroded image

```python { .api }
cv2.dilate(src, kernel, dst=None, anchor=None, iterations=1, borderType=None, borderValue=None) -> dst
```

Dilates image using specified structuring element.

- **src**: Input image
- **kernel**: Structuring element
- **anchor**: Anchor position within element
- **iterations**: Number of times dilation is applied
- **borderType**: Border extrapolation method
- **borderValue**: Border value for constant border
- **Returns**: Dilated image

```python { .api }
cv2.morphologyEx(src, op, kernel, dst=None, anchor=None, iterations=1, borderType=None, borderValue=None) -> dst
```

Performs advanced morphological transformations.

- **src**: Input image
- **op**: Type of morphological operation (see constants below)
- **kernel**: Structuring element
- **anchor**: Anchor position within element
- **iterations**: Number of times operation is applied
- **Returns**: Result image

```python { .api }
cv2.getStructuringElement(shape, ksize, anchor=None) -> retval
```

Creates structuring element for morphological operations.

- **shape**: Element shape (MORPH_RECT, MORPH_CROSS, MORPH_ELLIPSE)
- **ksize**: Size of structuring element
- **anchor**: Anchor position (default: center)
- **Returns**: Structuring element matrix

#### Morphological Operation Types

```python { .api }
cv2.MORPH_ERODE       # Erosion
cv2.MORPH_DILATE      # Dilation
cv2.MORPH_OPEN        # Opening (erosion followed by dilation)
cv2.MORPH_CLOSE       # Closing (dilation followed by erosion)
cv2.MORPH_GRADIENT    # Morphological gradient (difference between dilation and erosion)
cv2.MORPH_TOPHAT      # Top hat (difference between source and opening)
cv2.MORPH_BLACKHAT    # Black hat (difference between closing and source)
cv2.MORPH_HITMISS     # Hit-or-miss transform
```

#### Structuring Element Shapes

```python { .api }
cv2.MORPH_RECT        # Rectangular structuring element
cv2.MORPH_CROSS       # Cross-shaped structuring element
cv2.MORPH_ELLIPSE     # Elliptical structuring element
```

### Geometric Transformations

Functions for resizing, rotating, warping, and remapping images.

#### Resizing and Rescaling

```python { .api }
cv2.resize(src, dsize, dst=None, fx=0, fy=0, interpolation=cv2.INTER_LINEAR) -> dst
```

Resizes image to specified size or by scale factors.

- **src**: Input image
- **dsize**: Output image size (width, height). If 0, computed from fx and fy
- **fx**: Scale factor along horizontal axis
- **fy**: Scale factor along vertical axis
- **interpolation**: Interpolation method (see constants below)
- **Returns**: Resized image

```python { .api }
cv2.pyrDown(src, dst=None, dstsize=None, borderType=None) -> dst
```

Downsamples image using Gaussian pyramid.

- **src**: Input image
- **dstsize**: Size of output image (default: (src.width/2, src.height/2))
- **borderType**: Border extrapolation method
- **Returns**: Downsampled image

```python { .api }
cv2.pyrUp(src, dst=None, dstsize=None, borderType=None) -> dst
```

Upsamples image using Gaussian pyramid.

- **src**: Input image
- **dstsize**: Size of output image (default: (src.width*2, src.height*2))
- **borderType**: Border extrapolation method
- **Returns**: Upsampled image

```python { .api }
cv2.buildPyramid(src, maxlevel, dst=None, borderType=None) -> dst
```

Constructs Gaussian pyramid for an image.

- **src**: Input image
- **maxlevel**: Number of pyramid levels
- **borderType**: Border extrapolation method
- **Returns**: List of pyramid levels

#### Affine Transformations

```python { .api }
cv2.warpAffine(src, M, dsize, dst=None, flags=cv2.INTER_LINEAR, borderMode=None, borderValue=None) -> dst
```

Applies affine transformation to image.

- **src**: Input image
- **M**: 2x3 transformation matrix
- **dsize**: Size of output image
- **flags**: Combination of interpolation method and optional flags
- **borderMode**: Border extrapolation method
- **borderValue**: Value for constant border
- **Returns**: Transformed image

```python { .api }
cv2.getRotationMatrix2D(center, angle, scale) -> retval
```

Calculates 2D rotation matrix for rotating around a center point.

- **center**: Center of rotation (x, y)
- **angle**: Rotation angle in degrees (positive: counter-clockwise)
- **scale**: Isotropic scale factor
- **Returns**: 2x3 rotation matrix

```python { .api }
cv2.getAffineTransform(src, dst) -> retval
```

Calculates affine transform from three pairs of corresponding points.

- **src**: Coordinates of triangle vertices in source image (3x2 array)
- **dst**: Coordinates of corresponding triangle vertices in destination image
- **Returns**: 2x3 affine transformation matrix

```python { .api }
cv2.invertAffineTransform(M, iM=None) -> iM
```

Inverts affine transformation.

- **M**: Original 2x3 affine transformation matrix
- **Returns**: Inverse affine transformation matrix

#### Perspective Transformations

```python { .api }
cv2.warpPerspective(src, M, dsize, dst=None, flags=cv2.INTER_LINEAR, borderMode=None, borderValue=None) -> dst
```

Applies perspective transformation to image.

- **src**: Input image
- **M**: 3x3 transformation matrix
- **dsize**: Size of output image
- **flags**: Combination of interpolation method and optional flags
- **borderMode**: Border extrapolation method
- **borderValue**: Value for constant border
- **Returns**: Transformed image

```python { .api }
cv2.getPerspectiveTransform(src, dst, solveMethod=cv2.DECOMP_LU) -> retval
```

Calculates perspective transform from four pairs of corresponding points.

- **src**: Coordinates of quadrangle vertices in source image (4x2 array)
- **dst**: Coordinates of corresponding quadrangle vertices in destination image
- **solveMethod**: Method for solving the linear system
- **Returns**: 3x3 perspective transformation matrix

#### Generic Remapping

```python { .api }
cv2.remap(src, map1, map2, interpolation, dst=None, borderMode=None, borderValue=None) -> dst
```

Applies generic geometrical transformation using mapping arrays.

- **src**: Source image
- **map1**: First map (x coordinates or both xy as CV_32FC2)
- **map2**: Second map (y coordinates or empty if map1 is CV_32FC2)
- **interpolation**: Interpolation method
- **borderMode**: Border extrapolation method
- **borderValue**: Value for constant border
- **Returns**: Remapped image

```python { .api }
cv2.convertMaps(map1, map2, dstmap1type, dstmap1=None, dstmap2=None, nninterpolation=False) -> dstmap1, dstmap2
```

Converts image transformation maps from one representation to another.

- **map1**: First input map
- **map2**: Second input map
- **dstmap1type**: Type of first output map
- **nninterpolation**: Flag for nearest-neighbor interpolation
- **Returns**: Converted maps (dstmap1, dstmap2)

```python { .api }
cv2.getRectSubPix(image, patchSize, center, patch=None, patchType=-1) -> patch
```

Retrieves pixel rectangle from image with sub-pixel accuracy.

- **image**: Input image
- **patchSize**: Size of extracted patch
- **center**: Floating-point center coordinates of extracted rectangle
- **patchType**: Depth of extracted pixels (-1 uses source type)
- **Returns**: Extracted patch

#### Interpolation Methods

```python { .api }
cv2.INTER_NEAREST      # Nearest-neighbor interpolation
cv2.INTER_LINEAR       # Bilinear interpolation
cv2.INTER_CUBIC        # Bicubic interpolation
cv2.INTER_AREA         # Resampling using pixel area relation (best for decimation)
cv2.INTER_LANCZOS4     # Lanczos interpolation over 8x8 neighborhood
cv2.INTER_LINEAR_EXACT # Bit-exact bilinear interpolation
cv2.INTER_NEAREST_EXACT # Bit-exact nearest-neighbor interpolation
cv2.INTER_MAX          # Mask for interpolation codes
cv2.WARP_FILL_OUTLIERS # Fill all pixels outside source image
cv2.WARP_INVERSE_MAP   # Inverse transformation (dst->src instead of src->dst)
```

### Color Space Conversion

Functions for converting between different color representations.

```python { .api }
cv2.cvtColor(src, code, dst=None, dstCn=0) -> dst
```

Converts image from one color space to another.

- **src**: Input image
- **code**: Color space conversion code (see constants below)
- **dstCn**: Number of channels in destination image (0 = automatic)
- **Returns**: Converted image

```python { .api }
cv2.cvtColorTwoPlane(src1, src2, code, dst=None) -> dst
```

Converts two-plane YUV format to RGB/BGR.

- **src1**: Y plane
- **src2**: UV plane
- **code**: Color conversion code
- **Returns**: Converted image

#### Color Conversion Codes

**RGB/BGR conversions:**

```python { .api }
cv2.COLOR_BGR2RGB
cv2.COLOR_RGB2BGR
cv2.COLOR_BGR2BGRA
cv2.COLOR_RGB2RGBA
cv2.COLOR_BGRA2BGR
cv2.COLOR_RGBA2RGB
cv2.COLOR_BGR2RGBA
cv2.COLOR_RGB2BGRA
cv2.COLOR_RGBA2BGR
cv2.COLOR_BGRA2RGB
```

**Grayscale conversions:**

```python { .api }
cv2.COLOR_BGR2GRAY
cv2.COLOR_RGB2GRAY
cv2.COLOR_GRAY2BGR
cv2.COLOR_GRAY2RGB
cv2.COLOR_GRAY2BGRA
cv2.COLOR_GRAY2RGBA
cv2.COLOR_BGRA2GRAY
cv2.COLOR_RGBA2GRAY
```

**HSV conversions:**

```python { .api }
cv2.COLOR_BGR2HSV
cv2.COLOR_RGB2HSV
cv2.COLOR_HSV2BGR
cv2.COLOR_HSV2RGB
cv2.COLOR_BGR2HSV_FULL
cv2.COLOR_RGB2HSV_FULL
cv2.COLOR_HSV2BGR_FULL
cv2.COLOR_HSV2RGB_FULL
```

**HLS conversions:**

```python { .api }
cv2.COLOR_BGR2HLS
cv2.COLOR_RGB2HLS
cv2.COLOR_HLS2BGR
cv2.COLOR_HLS2RGB
cv2.COLOR_BGR2HLS_FULL
cv2.COLOR_RGB2HLS_FULL
cv2.COLOR_HLS2BGR_FULL
cv2.COLOR_HLS2RGB_FULL
```

**Lab conversions:**

```python { .api }
cv2.COLOR_BGR2Lab
cv2.COLOR_RGB2Lab
cv2.COLOR_Lab2BGR
cv2.COLOR_Lab2RGB
cv2.COLOR_LBGR2Lab
cv2.COLOR_LRGB2Lab
cv2.COLOR_Lab2LBGR
cv2.COLOR_Lab2LRGB
```

**Luv conversions:**

```python { .api }
cv2.COLOR_BGR2Luv
cv2.COLOR_RGB2Luv
cv2.COLOR_Luv2BGR
cv2.COLOR_Luv2RGB
cv2.COLOR_LBGR2Luv
cv2.COLOR_LRGB2Luv
cv2.COLOR_Luv2LBGR
cv2.COLOR_Luv2LRGB
```

**YUV conversions:**

```python { .api }
cv2.COLOR_BGR2YUV
cv2.COLOR_RGB2YUV
cv2.COLOR_YUV2BGR
cv2.COLOR_YUV2RGB
cv2.COLOR_YUV2RGB_NV12
cv2.COLOR_YUV2BGR_NV12
cv2.COLOR_YUV2RGB_NV21
cv2.COLOR_YUV2BGR_NV21
cv2.COLOR_YUV2RGBA_NV12
cv2.COLOR_YUV2BGRA_NV12
cv2.COLOR_YUV2RGBA_NV21
cv2.COLOR_YUV2BGRA_NV21
cv2.COLOR_YUV2RGB_YV12
cv2.COLOR_YUV2BGR_YV12
cv2.COLOR_YUV2RGB_IYUV
cv2.COLOR_YUV2BGR_IYUV
cv2.COLOR_YUV2RGBA_YV12
cv2.COLOR_YUV2BGRA_YV12
cv2.COLOR_YUV2RGBA_IYUV
cv2.COLOR_YUV2BGRA_IYUV
cv2.COLOR_YUV2GRAY_420
cv2.COLOR_YUV2GRAY_NV21
cv2.COLOR_YUV2GRAY_NV12
cv2.COLOR_YUV2GRAY_YV12
cv2.COLOR_YUV2GRAY_IYUV
```

**YCrCb conversions:**

```python { .api }
cv2.COLOR_BGR2YCrCb
cv2.COLOR_RGB2YCrCb
cv2.COLOR_YCrCb2BGR
cv2.COLOR_YCrCb2RGB
```

**XYZ conversions:**

```python { .api }
cv2.COLOR_BGR2XYZ
cv2.COLOR_RGB2XYZ
cv2.COLOR_XYZ2BGR
cv2.COLOR_XYZ2RGB
```

**Bayer pattern conversions:**

```python { .api }
cv2.COLOR_BayerBG2BGR
cv2.COLOR_BayerGB2BGR
cv2.COLOR_BayerRG2BGR
cv2.COLOR_BayerGR2BGR
cv2.COLOR_BayerBG2RGB
cv2.COLOR_BayerGB2RGB
cv2.COLOR_BayerRG2RGB
cv2.COLOR_BayerGR2RGB
cv2.COLOR_BayerBG2GRAY
cv2.COLOR_BayerGB2GRAY
cv2.COLOR_BayerRG2GRAY
cv2.COLOR_BayerGR2GRAY
```

### Histograms

Operations for computing and analyzing image histograms.

```python { .api }
cv2.calcHist(images, channels, mask, histSize, ranges, hist=None, accumulate=False) -> hist
```

Calculates histogram of image(s).

- **images**: Source images list (must be same depth, 8-bit or 32-bit)
- **channels**: List of channel indices to compute histogram
- **mask**: Optional mask (None to use whole image)
- **histSize**: Histogram size in each dimension (list)
- **ranges**: Array of histogram bin boundaries in each dimension
- **accumulate**: Accumulation flag (add to existing histogram if True)
- **Returns**: Output histogram

```python { .api }
cv2.calcBackProject(images, channels, hist, ranges, scale, dst=None) -> dst
```

Calculates back projection of histogram.

- **images**: Source images
- **channels**: List of channels used
- **hist**: Input histogram
- **ranges**: Array of histogram bin boundaries
- **scale**: Scale factor for output back projection
- **Returns**: Back projection image

```python { .api }
cv2.compareHist(H1, H2, method) -> retval
```

Compares two histograms.

- **H1**: First histogram
- **H2**: Second histogram
- **method**: Comparison method (see constants below)
- **Returns**: Comparison result (interpretation depends on method)

```python { .api }
cv2.equalizeHist(src, dst=None) -> dst
```

Equalizes histogram of grayscale image.

- **src**: Source 8-bit single-channel image
- **Returns**: Equalized image

```python { .api }
cv2.createCLAHE(clipLimit=40.0, tileGridSize=(8,8)) -> retval
```

Creates CLAHE (Contrast Limited Adaptive Histogram Equalization) object.

- **clipLimit**: Threshold for contrast limiting
- **tileGridSize**: Size of grid for histogram equalization
- **Returns**: CLAHE object with apply() method

#### Histogram Comparison Methods

```python { .api }
cv2.HISTCMP_CORREL        # Correlation
cv2.HISTCMP_CHISQR        # Chi-Square
cv2.HISTCMP_INTERSECT     # Intersection
cv2.HISTCMP_BHATTACHARYYA # Bhattacharyya distance
cv2.HISTCMP_HELLINGER     # Synonym for BHATTACHARYYA
cv2.HISTCMP_CHISQR_ALT    # Alternative Chi-Square
cv2.HISTCMP_KL_DIV        # Kullback-Leibler divergence
```

### Thresholding

Binary and adaptive thresholding operations.

```python { .api }
cv2.threshold(src, thresh, maxval, type, dst=None) -> retval, dst
```

Applies fixed-level threshold to image.

- **src**: Input array (8-bit or 32-bit)
- **thresh**: Threshold value
- **maxval**: Maximum value for THRESH_BINARY and THRESH_BINARY_INV
- **type**: Thresholding type (see constants below)
- **Returns**: Tuple of (threshold value used, thresholded image)

```python { .api }
cv2.adaptiveThreshold(src, maxValue, adaptiveMethod, thresholdType, blockSize, C, dst=None) -> dst
```

Applies adaptive threshold (threshold varies across image).

- **src**: Source 8-bit single-channel image
- **maxValue**: Non-zero value assigned to pixels exceeding threshold
- **adaptiveMethod**: Adaptive method (ADAPTIVE_THRESH_MEAN_C or ADAPTIVE_THRESH_GAUSSIAN_C)
- **thresholdType**: Thresholding type (THRESH_BINARY or THRESH_BINARY_INV)
- **blockSize**: Size of pixel neighborhood (odd number)
- **C**: Constant subtracted from mean or weighted mean
- **Returns**: Thresholded image

#### Threshold Types

```python { .api }
cv2.THRESH_BINARY       # dst = (src > thresh) ? maxval : 0
cv2.THRESH_BINARY_INV   # dst = (src > thresh) ? 0 : maxval
cv2.THRESH_TRUNC        # dst = (src > thresh) ? thresh : src
cv2.THRESH_TOZERO       # dst = (src > thresh) ? src : 0
cv2.THRESH_TOZERO_INV   # dst = (src > thresh) ? 0 : src
cv2.THRESH_MASK         # Mask for threshold types
cv2.THRESH_OTSU         # Use Otsu's algorithm (flag, combine with type)
cv2.THRESH_TRIANGLE     # Use Triangle algorithm (flag, combine with type)
```

#### Adaptive Threshold Methods

```python { .api }
cv2.ADAPTIVE_THRESH_MEAN_C     # Threshold = mean of neighborhood - C
cv2.ADAPTIVE_THRESH_GAUSSIAN_C # Threshold = weighted sum (Gaussian) - C
```

### Image Segmentation

Advanced segmentation algorithms for partitioning images into regions.

```python { .api }
cv2.watershed(image, markers) -> markers
```

Performs marker-based image segmentation using watershed algorithm.

- **image**: Input 8-bit 3-channel image
- **markers**: Input/output 32-bit single-channel marker image. Modified in-place
- **Returns**: None (markers modified in-place with segment labels)

```python { .api }
cv2.grabCut(img, mask, rect, bgdModel, fgdModel, iterCount, mode=cv2.GC_EVAL) -> mask, bgdModel, fgdModel
```

Segments foreground using GrabCut algorithm.

- **img**: Input 8-bit 3-channel image
- **mask**: Input/output 8-bit single-channel mask
- **rect**: ROI containing segmented object (used with GC_INIT_WITH_RECT)
- **bgdModel**: Temporary array for background model (13x5)
- **fgdModel**: Temporary array for foreground model (13x5)
- **iterCount**: Number of iterations
- **mode**: Operation mode (GC_INIT_WITH_RECT, GC_INIT_WITH_MASK, or GC_EVAL)
- **Returns**: Updated mask, bgdModel, fgdModel

```python { .api }
cv2.connectedComponents(image, labels=None, connectivity=8, ltype=cv2.CV_32S) -> retval, labels
```

Computes the connected components labeled image of boolean image.

- **image**: The 8-bit single-channel image to be labeled
- **labels**: Destination labeled image
- **connectivity**: 8 or 4 for 8-way or 4-way connectivity respectively
- **ltype**: Output image label type (currently CV_32S and CV_16U are supported)
- **Returns**: Tuple of (number of labels [0, N-1] where 0 is background, labels array)

```python { .api }
cv2.connectedComponentsWithStats(image, labels=None, stats=None, centroids=None, connectivity=8, ltype=cv2.CV_32S) -> retval, labels, stats, centroids
```

Computes the connected components labeled image and produces statistics.

- **image**: The 8-bit single-channel image to be labeled
- **labels**: Destination labeled image
- **stats**: Statistics output for each label including background (accessed via stats(label, COLUMN)). Data type is CV_32S
- **centroids**: Centroid output for each label including background. Centroids are accessed via centroids(label, 0) for x and centroids(label, 1) for y. Data type CV_64F
- **connectivity**: 8 or 4 for 8-way or 4-way connectivity respectively
- **ltype**: Output image label type (currently CV_32S and CV_16U are supported)
- **Returns**: Tuple of (number of labels [0, N-1] where 0 is background, labels array, stats array, centroids array)

```python { .api }
cv2.distanceTransform(src, distanceType, maskSize, dst=None, dstType=cv2.CV_32F) -> dst, labels
```

Calculates distance to nearest zero pixel for each pixel.

- **src**: 8-bit single-channel source image (binary)
- **distanceType**: Type of distance (DIST_L1, DIST_L2, DIST_C, etc.)
- **maskSize**: Size of distance transform mask (3 or 5, or DIST_MASK_PRECISE)
- **dstType**: Type of output image (CV_8U or CV_32F)
- **Returns**: Distance transform output and labels

```python { .api }
cv2.floodFill(image, mask, seedPoint, newVal, loDiff=None, upDiff=None, flags=None) -> retval, image, mask, rect
```

Fills connected component with specified color.

- **image**: Input/output 1- or 3-channel image (modified in-place)
- **mask**: Operation mask (should be 2 pixels wider and taller than image)
- **seedPoint**: Starting point for flood fill
- **newVal**: New value for repainted domain pixels
- **loDiff**: Maximal lower brightness/color difference
- **upDiff**: Maximal upper brightness/color difference
- **flags**: Operation flags (connectivity, mask fill value, etc.)
- **Returns**: Tuple of (area filled, image, mask, bounding rect)

#### GrabCut Constants

```python { .api }
cv2.GC_BGD         # Background pixel (0)
cv2.GC_FGD         # Foreground pixel (1)
cv2.GC_PR_BGD      # Probably background pixel (2)
cv2.GC_PR_FGD      # Probably foreground pixel (3)
cv2.GC_INIT_WITH_RECT  # Initialize with rectangle
cv2.GC_INIT_WITH_MASK  # Initialize with mask
cv2.GC_EVAL        # Evaluate mode
```

#### Distance Types

```python { .api }
cv2.DIST_USER      # User-defined distance
cv2.DIST_L1        # Distance = |x1-x2| + |y1-y2|
cv2.DIST_L2        # Euclidean distance
cv2.DIST_C         # Distance = max(|x1-x2|, |y1-y2|)
cv2.DIST_L12       # L1-L2 metric
cv2.DIST_FAIR      # Distance = c^2(|x|/c - log(1+|x|/c))
cv2.DIST_WELSCH    # Distance = c^2/2(1-exp(-(x/c)^2))
cv2.DIST_HUBER     # Distance = |x|<c ? x^2/2 : c(|x|-c/2)
cv2.DIST_MASK_3    # Mask size 3
cv2.DIST_MASK_5    # Mask size 5
cv2.DIST_MASK_PRECISE # Precise distance calculation
```

### Template Matching

Template matching for finding pattern locations in images.

```python { .api }
cv2.matchTemplate(image, templ, method, result=None, mask=None) -> result
```

Compares template against overlapping image regions.

- **image**: Image where search is running (8-bit or 32-bit floating-point)
- **templ**: Searched template (same type as image, not larger than image)
- **method**: Comparison method (see constants below)
- **mask**: Optional mask of searched template (same size as templ, 8-bit)
- **Returns**: Map of comparison results (single-channel 32-bit floating-point)

#### Template Matching Methods

```python { .api }
cv2.TM_SQDIFF        # Sum of squared differences (minimum is best)
cv2.TM_SQDIFF_NORMED # Normalized SQDIFF (minimum is best)
cv2.TM_CCORR         # Cross-correlation (maximum is best)
cv2.TM_CCORR_NORMED  # Normalized cross-correlation (maximum is best)
cv2.TM_CCOEFF        # Correlation coefficient (maximum is best)
cv2.TM_CCOEFF_NORMED # Normalized correlation coefficient (maximum is best)
```

### Image Pyramids

Multi-scale image representation using Gaussian pyramids.

```python { .api }
cv2.pyrDown(src, dst=None, dstsize=None, borderType=None) -> dst
```

Blurs and downsamples image (builds next pyramid level down).

- **src**: Input image
- **dstsize**: Size of output image (default: ((src.cols+1)/2, (src.rows+1)/2))
- **borderType**: Border extrapolation method
- **Returns**: Downsampled image

```python { .api }
cv2.pyrUp(src, dst=None, dstsize=None, borderType=None) -> dst
```

Upsamples and blurs image (builds next pyramid level up).

- **src**: Input image
- **dstsize**: Size of output image (default: (src.cols*2, src.rows*2))
- **borderType**: Border extrapolation method
- **Returns**: Upsampled image

```python { .api }
cv2.buildPyramid(src, maxlevel, dst=None, borderType=None) -> dst
```

Constructs Gaussian pyramid.

- **src**: Source image
- **maxlevel**: Number of pyramid levels (0-based)
- **borderType**: Border extrapolation method
- **Returns**: List containing pyramid levels

### Other Image Transformations

Additional transformation and accumulation operations.

```python { .api }
cv2.integral(src, sum=None, sdepth=-1) -> sum
cv2.integral2(src, sum=None, sqsum=None, sdepth=-1, sqdepth=-1) -> sum, sqsum
cv2.integral3(src, sum=None, sqsum=None, tilted=None, sdepth=-1, sqdepth=-1) -> sum, sqsum, tilted
```

Calculates integral image(s) for fast area sum computation.

- **src**: Input image
- **sdepth**: Desired depth of integral image (-1 = automatic)
- **sqdepth**: Desired depth of squared integral image
- **Returns**: Integral image(s)

```python { .api }
cv2.accumulate(src, dst, mask=None) -> dst
```

Adds image to accumulator.

- **src**: Input image (1- or 3-channel, 8-bit or 32-bit)
- **dst**: Accumulator image (same channels as src, 32-bit or 64-bit)
- **mask**: Optional operation mask
- **Returns**: None (dst modified in-place)

```python { .api }
cv2.accumulateSquare(src, dst, mask=None) -> dst
```

Adds square of source image to accumulator.

- **src**: Input image
- **dst**: Accumulator image
- **mask**: Optional operation mask
- **Returns**: None (dst modified in-place)

```python { .api }
cv2.accumulateProduct(src1, src2, dst, mask=None) -> dst
```

Adds product of two images to accumulator.

- **src1**: First input image
- **src2**: Second input image
- **dst**: Accumulator image
- **mask**: Optional operation mask
- **Returns**: None (dst modified in-place)

```python { .api }
cv2.accumulateWeighted(src, dst, alpha, mask=None) -> dst
```

Updates running average (exponentially weighted).

- **src**: Input image
- **dst**: Accumulator image (same channels and depth as src)
- **alpha**: Weight of input image (dst = (1-alpha)*dst + alpha*src)
- **mask**: Optional operation mask
- **Returns**: None (dst modified in-place)

```python { .api }
cv2.createHanningWindow(winSize, type) -> dst
```

Creates Hanning window (used for DFT-based trackers).

- **winSize**: Window size
- **type**: Created matrix type
- **Returns**: Hanning window

```python { .api }
cv2.phaseCorrelate(src1, src2, window=None) -> retval, response
```

Detects translational shift between two images using phase correlation.

- **src1**: First source floating-point array (grayscale or single color channel)
- **src2**: Second source array (same size and type as src1)
- **window**: Optional Hanning window
- **Returns**: Tuple of (detected phase shift, peak response value)
