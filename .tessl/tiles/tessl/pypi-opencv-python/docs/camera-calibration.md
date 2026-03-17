# Camera Calibration and 3D Reconstruction

OpenCV's calib3d module provides comprehensive tools for camera calibration, 3D reconstruction, pose estimation, and geometric computer vision. This module enables you to calibrate cameras, correct lens distortion, perform stereo vision, estimate object poses, and reconstruct 3D scenes from 2D images.

## Capabilities

### Camera Calibration

Camera calibration determines the intrinsic parameters (focal length, optical center, distortion coefficients) and extrinsic parameters (rotation, translation) of a camera. This is essential for accurate 3D reconstruction and measurement tasks.

```python { .api }
retval, cameraMatrix, distCoeffs, rvecs, tvecs = cv2.calibrateCamera(
    objectPoints,           # List of 3D points in world coordinate space
    imagePoints,           # List of 2D points in image plane
    imageSize,             # Image size as (width, height)
    cameraMatrix=None,     # Initial camera matrix (3x3)
    distCoeffs=None,       # Initial distortion coefficients
    flags=0,               # Calibration flags
    criteria=None          # Termination criteria for iterative optimization
)
# Returns: reprojection error, camera matrix, distortion coefficients,
#          rotation vectors, translation vectors for each pattern view
```

```python { .api }
retval, corners = cv2.findChessboardCorners(
    image,                 # Source chessboard view (8-bit grayscale or color)
    patternSize,           # Number of inner corners per chessboard row and column
    corners=None,          # Output array of detected corners
    flags=None             # Various operation flags (CALIB_CB_*)
)
# Returns: boolean success indicator, array of detected corner coordinates
# Common flags:
#   cv2.CALIB_CB_ADAPTIVE_THRESH - Use adaptive thresholding
#   cv2.CALIB_CB_NORMALIZE_IMAGE - Normalize image gamma
#   cv2.CALIB_CB_FAST_CHECK - Fast check for chessboard presence
```

```python { .api }
corners = cv2.cornerSubPix(
    image,                 # Input grayscale image
    corners,               # Initial coordinates of corners
    winSize,               # Half of side length of search window
    zeroZone,              # Half of dead region size (-1, -1 to disable)
    criteria               # Termination criteria (type, maxCount, epsilon)
)
# Refines corner locations to subpixel accuracy
# Returns: refined corner coordinates
```

```python { .api }
image = cv2.drawChessboardCorners(
    image,                 # Destination image (must be color or 8-bit grayscale)
    patternSize,           # Number of inner corners per row and column
    corners,               # Array of detected corners
    patternWasFound        # Indicates whether pattern was found
)
# Draws individual chessboard corners or entire pattern
# Returns: image with rendered corners
```

```python { .api }
retval, centers = cv2.findCirclesGrid(
    image,                 # Grid view of input circles (8-bit grayscale or color)
    patternSize,           # Number of circles per row and column (points_per_row, points_per_column)
    centers=None,          # Output array of detected centers
    flags=cv2.CALIB_CB_SYMMETRIC_GRID,  # Operation flags
    blobDetector=None      # Feature detector that finds blobs (default: SimpleBlobDetector)
)
# Finds centers in the grid of circles pattern
# Returns: boolean success indicator (True if all centers found and ordered), array of detected centers
# Common flags:
#   cv2.CALIB_CB_SYMMETRIC_GRID - Uses symmetric pattern of circles
#   cv2.CALIB_CB_ASYMMETRIC_GRID - Uses asymmetric pattern of circles
#   cv2.CALIB_CB_CLUSTERING - Uses special algorithm for grid detection (more robust to perspective distortions)
# Requires white space around the board for robust detection
```

**Calibration Flags:**

```python { .api }
# Camera calibration flags for cv2.calibrateCamera():
cv2.CALIB_USE_INTRINSIC_GUESS      # Use provided cameraMatrix as initial guess
cv2.CALIB_FIX_PRINCIPAL_POINT      # Fix the principal point at the center
cv2.CALIB_FIX_ASPECT_RATIO         # Fix fx/fy ratio
cv2.CALIB_ZERO_TANGENT_DIST        # Tangential distortion coefficients set to zero
cv2.CALIB_FIX_K1                   # Fix k1 distortion coefficient
cv2.CALIB_FIX_K2                   # Fix k2 distortion coefficient
cv2.CALIB_FIX_K3                   # Fix k3 distortion coefficient
cv2.CALIB_FIX_K4                   # Fix k4 distortion coefficient
cv2.CALIB_FIX_K5                   # Fix k5 distortion coefficient
cv2.CALIB_FIX_K6                   # Fix k6 distortion coefficient
cv2.CALIB_RATIONAL_MODEL           # Enable k4, k5, k6 coefficients
cv2.CALIB_THIN_PRISM_MODEL         # Enable s1, s2, s3, s4 coefficients
cv2.CALIB_FIX_S1_S2_S3_S4          # Fix thin prism distortion coefficients
cv2.CALIB_TILTED_MODEL             # Enable tauX, tauY coefficients
cv2.CALIB_FIX_TAUX_TAUY            # Fix tilted sensor coefficients
```

### Pose Estimation

Pose estimation determines the position and orientation of an object or camera relative to a coordinate system using correspondences between 3D points and their 2D image projections.

```python { .api }
retval, rvec, tvec = cv2.solvePnP(
    objectPoints,          # Array of 3D object points
    imagePoints,           # Array of corresponding 2D image points
    cameraMatrix,          # Camera intrinsic matrix (3x3)
    distCoeffs,            # Distortion coefficients
    rvec=None,             # Output rotation vector
    tvec=None,             # Output translation vector
    useExtrinsicGuess=False,  # Use provided rvec/tvec as initial guess
    flags=cv2.SOLVEPNP_ITERATIVE  # Method to use for pose estimation
)
# Returns: success indicator, rotation vector (3x1), translation vector (3x1)
```

```python { .api }
retval, rvec, tvec, inliers = cv2.solvePnPRansac(
    objectPoints,          # Array of 3D object points
    imagePoints,           # Array of corresponding 2D image points
    cameraMatrix,          # Camera intrinsic matrix (3x3)
    distCoeffs,            # Distortion coefficients
    rvec=None,             # Output rotation vector
    tvec=None,             # Output translation vector
    useExtrinsicGuess=False,  # Use provided rvec/tvec as initial guess
    iterationsCount=100,   # Number of iterations
    reprojectionError=8.0, # Inlier threshold value
    confidence=0.99,       # Required confidence level
    inliers=None,          # Output vector of inlier indices
    flags=cv2.SOLVEPNP_ITERATIVE  # Method to use
)
# Robust pose estimation using RANSAC outlier rejection
# Returns: success indicator, rotation vector, translation vector, inlier indices
```

```python { .api }
imagePoints, jacobian = cv2.projectPoints(
    objectPoints,          # Array of 3D object points
    rvec,                  # Rotation vector (3x1 or 3x3 matrix)
    tvec,                  # Translation vector (3x1)
    cameraMatrix,          # Camera intrinsic matrix (3x3)
    distCoeffs,            # Distortion coefficients
    imagePoints=None,      # Output 2D image points
    jacobian=None,         # Optional output Jacobian matrix
    aspectRatio=0          # Optional aspect ratio parameter
)
# Projects 3D points to image plane using camera parameters
# Returns: 2D image points, Jacobian matrix (optional)
```

```python { .api }
dst = cv2.Rodrigues(
    src,                   # Input rotation vector (3x1) or rotation matrix (3x3)
    dst=None,              # Output rotation matrix (3x3) or rotation vector (3x1)
    jacobian=None          # Optional output Jacobian matrix
)
# Converts rotation vector to rotation matrix or vice versa
# Returns: rotation matrix (if input is vector) or rotation vector (if input is matrix),
#          optional Jacobian
```

**PnP Solution Methods:**

```python { .api }
# Pose estimation methods for cv2.solvePnP() and cv2.solvePnPRansac():
cv2.SOLVEPNP_ITERATIVE             # Iterative method based on Levenberg-Marquardt
cv2.SOLVEPNP_EPNP                  # EPnP: Efficient Perspective-n-Point (4+ points)
cv2.SOLVEPNP_P3P                   # P3P: Perspective-3-Point (exactly 3 points)
cv2.SOLVEPNP_DLS                   # DLS: Direct Least-Squares (4+ points)
cv2.SOLVEPNP_UPNP                  # UPnP: Unified Perspective-n-Point
cv2.SOLVEPNP_AP3P                  # AP3P: Alternative P3P (exactly 3 points)
cv2.SOLVEPNP_IPPE                  # IPPE: Infinitesimal Plane-Based Pose Estimation
cv2.SOLVEPNP_IPPE_SQUARE           # IPPE for square planar objects
cv2.SOLVEPNP_SQPNP                 # SQPnP: Sequential Quadratic Programming PnP
```

### Undistortion

Lens distortion causes straight lines to appear curved in images. Undistortion removes radial and tangential distortion effects to produce geometrically correct images.

```python { .api }
dst = cv2.undistort(
    src,                   # Input (distorted) image
    cameraMatrix,          # Camera intrinsic matrix (3x3)
    distCoeffs,            # Distortion coefficients (4, 5, 8, 12 or 14 elements)
    dst=None,              # Output (undistorted) image
    newCameraMatrix=None   # New camera matrix (3x3), default uses original
)
# Transforms image to compensate for lens distortion
# Returns: undistorted image
```

```python { .api }
newCameraMatrix, roi = cv2.getOptimalNewCameraMatrix(
    cameraMatrix,          # Input camera matrix
    distCoeffs,            # Distortion coefficients
    imageSize,             # Original image size (width, height)
    alpha,                 # Free scaling parameter (0=no invalid pixels, 1=all pixels)
    newImgSize=None,       # New image size (width, height), default uses imageSize
    centerPrincipalPoint=False  # Whether to center principal point
)
# Computes optimal new camera matrix for undistortion
# Returns: new camera matrix, valid pixel ROI (x, y, width, height)
```

```python { .api }
map1, map2 = cv2.initUndistortRectifyMap(
    cameraMatrix,          # Input camera matrix
    distCoeffs,            # Distortion coefficients
    R,                     # Optional rectification transformation (3x3)
    newCameraMatrix,       # New camera matrix (3x3)
    size,                  # Undistorted image size (width, height)
    m1type,                # Type of first output map (CV_32FC1 or CV_16SC2)
    map1=None,             # First output map
    map2=None              # Second output map
)
# Computes undistortion and rectification transformation maps
# Use with cv2.remap() for efficient repeated undistortion
# Returns: map1 (x-coordinates or x-coordinates + y-coordinates),
#          map2 (y-coordinates or interpolation weights)
```

```python { .api }
dst = cv2.undistortPoints(
    src,                   # Observed point coordinates (2xN/Nx2 1-channel or 1xN/Nx1 2-channel)
    cameraMatrix,          # Camera matrix [fx 0 cx; 0 fy cy; 0 0 1]
    distCoeffs,            # Input vector of distortion coefficients (k1,k2,p1,p2[,k3[,k4,k5,k6[,s1,s2,s3,s4[,τx,τy]]]])
    dst=None,              # Output ideal point coordinates after undistortion and reverse perspective transformation
    R=None,                # Rectification transformation in object space (3x3 matrix), R1 or R2 from stereoRectify
    P=None                 # New camera matrix (3x3) or new projection matrix (3x4), P1 or P2 from stereoRectify
)
# Computes the ideal point coordinates from the observed point coordinates
# Performs reverse transformation to projectPoints, working on sparse set of points instead of raster image
# If matrix P is identity or omitted, dst will contain normalized point coordinates
# Returns: undistorted point coordinates
```

### Stereo Vision

Stereo vision uses two cameras to capture the same scene from different viewpoints, enabling depth perception and 3D reconstruction.

```python { .api }
retval, cameraMatrix1, distCoeffs1, cameraMatrix2, distCoeffs2, R, T, E, F = cv2.stereoCalibrate(
    objectPoints,          # Vector of vectors of 3D calibration pattern points
    imagePoints1,          # Vector of vectors of 2D points in first camera
    imagePoints2,          # Vector of vectors of 2D points in second camera
    cameraMatrix1,         # Input/output first camera matrix
    distCoeffs1,           # Input/output first camera distortion coefficients
    cameraMatrix2,         # Input/output second camera matrix
    distCoeffs2,           # Input/output second camera distortion coefficients
    imageSize,             # Size of image (width, height)
    R=None,                # Output rotation matrix between cameras
    T=None,                # Output translation vector between cameras
    E=None,                # Output essential matrix
    F=None,                # Output fundamental matrix
    flags=cv2.CALIB_FIX_INTRINSIC,  # Calibration flags
    criteria=None          # Termination criteria for optimization
)
# Calibrates stereo camera system
# Returns: reprojection error, camera matrices, distortion coefficients,
#          rotation matrix, translation vector, essential matrix, fundamental matrix
```

```python { .api }
R1, R2, P1, P2, Q, roi1, roi2 = cv2.stereoRectify(
    cameraMatrix1,         # First camera matrix
    distCoeffs1,           # First camera distortion coefficients
    cameraMatrix2,         # Second camera matrix
    distCoeffs2,           # Second camera distortion coefficients
    imageSize,             # Size of image (width, height)
    R,                     # Rotation matrix between cameras
    T,                     # Translation vector between cameras
    R1=None,               # Output rectification transform for first camera
    R2=None,               # Output rectification transform for second camera
    P1=None,               # Output projection matrix for first camera (3x4)
    P2=None,               # Output projection matrix for second camera (3x4)
    Q=None,                # Output disparity-to-depth mapping matrix (4x4)
    flags=cv2.CALIB_ZERO_DISPARITY,  # Operation flags
    alpha=-1,              # Free scaling parameter
    newImageSize=None      # New image size after rectification
)
# Computes rectification transforms for stereo camera pair
# Returns: rectification transforms (R1, R2), projection matrices (P1, P2),
#          disparity-to-depth matrix (Q), valid pixel ROIs (roi1, roi2)
```

**Stereo Calibration Flags:**

```python { .api }
# Stereo calibration flags for cv2.stereoCalibrate():
cv2.CALIB_FIX_INTRINSIC            # Fix intrinsic parameters (optimize only extrinsic)
cv2.CALIB_USE_INTRINSIC_GUESS      # Optimize intrinsic parameters starting from provided values
cv2.CALIB_FIX_PRINCIPAL_POINT      # Fix the principal points during optimization
cv2.CALIB_FIX_FOCAL_LENGTH         # Fix fx and fy
cv2.CALIB_FIX_ASPECT_RATIO         # Fix fx/fy ratio
cv2.CALIB_SAME_FOCAL_LENGTH        # Enforce fx1=fx2 and fy1=fy2
cv2.CALIB_ZERO_TANGENT_DIST        # Tangential distortion coefficients set to zero
cv2.CALIB_RATIONAL_MODEL           # Enable k4, k5, k6 distortion coefficients
```

#### Stereo Correspondence

Stereo correspondence algorithms compute disparity maps (pixel displacement between stereo images), which can be converted to depth maps for 3D reconstruction.

```python { .api }
class StereoBM:
    """
    Block Matching stereo correspondence algorithm.
    Fast but less accurate than SGBM, works best with textured scenes.
    """
    @staticmethod
    def create(numDisparities=0, blockSize=21): ...

    def compute(self, left, right, disparity=None) -> disparity:
        """
        Computes disparity map for a rectified stereo pair.

        Args:
            left: Left 8-bit single-channel or 3-channel image
            right: Right image of the same size and type
            disparity: Output disparity map (16-bit signed, fixed-point)

        Returns: Disparity map (divide by 16 to get pixel disparity)
        """
        ...

    def setPreFilterCap(self, preFilterCap): ...
    def setPreFilterSize(self, preFilterSize): ...
    def setPreFilterType(self, preFilterType): ...
    def setBlockSize(self, blockSize): ...  # Block size (odd, typically 15-21)
    def setNumDisparities(self, numDisparities): ...  # Max disparity (multiple of 16)
    def setTextureThreshold(self, textureThreshold): ...
    def setUniquenessRatio(self, uniquenessRatio): ...
    def setSpeckleWindowSize(self, speckleWindowSize): ...
    def setSpeckleRange(self, speckleRange): ...
    def setDisp12MaxDiff(self, disp12MaxDiff): ...
    def setMinDisparity(self, minDisparity): ...
    def setROI1(self, roi1): ...
    def setROI2(self, roi2): ...

class StereoSGBM:
    """
    Semi-Global Block Matching stereo correspondence algorithm.
    More accurate than StereoBM, produces smoother disparity maps, handles textureless regions better.
    """
    @staticmethod
    def create(minDisparity=0, numDisparities=16, blockSize=3, P1=0, P2=0, disp12MaxDiff=0,
               preFilterCap=0, uniquenessRatio=0, speckleWindowSize=0, speckleRange=0, mode=None): ...

    def compute(self, left, right, disparity=None) -> disparity:
        """
        Computes disparity map for a rectified stereo pair.

        Args:
            left: Left 8-bit single-channel or 3-channel image
            right: Right image of the same size and type
            disparity: Output disparity map (16-bit signed, fixed-point)

        Returns: Disparity map (divide by 16 to get pixel disparity)
        """
        ...

    def setMinDisparity(self, minDisparity): ...
    def setNumDisparities(self, numDisparities): ...  # Max disparity minus min (multiple of 16)
    def setBlockSize(self, blockSize): ...  # Block size (odd, typically 3-11)
    def setP1(self, P1): ...  # Penalty for disparity change of 1 pixel
    def setP2(self, P2): ...  # Penalty for disparity change > 1 pixel (should be > P1)
    def setDisp12MaxDiff(self, disp12MaxDiff): ...  # Max allowed difference in left-right check
    def setPreFilterCap(self, preFilterCap): ...
    def setUniquenessRatio(self, uniquenessRatio): ...
    def setSpeckleWindowSize(self, speckleWindowSize): ...
    def setSpeckleRange(self, speckleRange): ...
    def setMode(self, mode): ...  # MODE_SGBM (default) or MODE_HH (full-scale two-pass)

# Create stereo matchers
stereo_bm = cv2.StereoBM.create(numDisparities=16*5, blockSize=15)
stereo_sgbm = cv2.StereoSGBM.create(minDisparity=0, numDisparities=16*6, blockSize=5)
```

**SGBM Mode Constants:**

```python { .api }
cv2.StereoSGBM_MODE_SGBM: int      # Standard SGBM mode
cv2.StereoSGBM_MODE_HH: int        # Full-scale two-pass dynamic programming algorithm
cv2.StereoSGBM_MODE_SGBM_3WAY: int # 3-way mode for improved results
```

**Usage Example:**

```python
import cv2
import numpy as np

# Load rectified stereo pair
left_img = cv2.imread('left_rect.jpg', cv2.IMREAD_GRAYSCALE)
right_img = cv2.imread('right_rect.jpg', cv2.IMREAD_GRAYSCALE)

# Create SGBM object (more accurate than BM)
stereo = cv2.StereoSGBM.create(
    minDisparity=0,
    numDisparities=16*6,  # Must be divisible by 16
    blockSize=5,          # Odd number, typically 3-11
    P1=8 * 3 * 5**2,     # Smoothness penalty for disparity changes
    P2=32 * 3 * 5**2,    # Larger penalty for larger disparity changes
    disp12MaxDiff=1,
    uniquenessRatio=10,
    speckleWindowSize=100,
    speckleRange=32,
    mode=cv2.StereoSGBM_MODE_SGBM_3WAY
)

# Compute disparity
disparity = stereo.compute(left_img, right_img)

# Convert to float and normalize for visualization
disparity_normalized = cv2.normalize(disparity, None, 0, 255, cv2.NORM_MINMAX, cv2.CV_8U)

# Convert disparity to depth using Q matrix from stereoRectify
# depth_map = cv2.reprojectImageTo3D(disparity, Q)
```

### Fisheye Camera

Fisheye lenses have extreme wide-angle views with significant barrel distortion. OpenCV provides specialized calibration and undistortion functions for fisheye cameras.

```python { .api }
retval, K, D, rvecs, tvecs = cv2.fisheye.calibrate(
    objectPoints,          # Vector of vectors of 3D calibration pattern points
    imagePoints,           # Vector of vectors of 2D image points
    image_size,            # Image size (width, height)
    K,                     # Input/output camera intrinsic matrix (3x3)
    D,                     # Input/output distortion coefficients (4x1)
    rvecs=None,            # Output rotation vectors
    tvecs=None,            # Output translation vectors
    flags=0,               # Calibration flags
    criteria=None          # Termination criteria
)
# Calibrates fisheye camera model
# Returns: reprojection error, camera matrix, distortion coefficients,
#          rotation vectors, translation vectors
```

```python { .api }
undistorted = cv2.fisheye.undistortImage(
    distorted,             # Input distorted image
    K,                     # Camera intrinsic matrix (3x3)
    D,                     # Distortion coefficients (4x1)
    Knew=None,             # New camera matrix (default uses K)
    new_size=None          # Output image size (default uses input size)
)
# Undistorts fisheye image
# Returns: undistorted image
```

**Fisheye Calibration Flags:**

```python { .api }
# Fisheye calibration flags for cv2.fisheye.calibrate():
cv2.fisheye.CALIB_USE_INTRINSIC_GUESS       # Use provided K as initial estimate
cv2.fisheye.CALIB_RECOMPUTE_EXTRINSIC       # Recompute extrinsic parameters
cv2.fisheye.CALIB_CHECK_COND                # Check condition number for stability
cv2.fisheye.CALIB_FIX_SKEW                  # Fix skew coefficient at zero
cv2.fisheye.CALIB_FIX_K1                    # Fix k1 distortion coefficient
cv2.fisheye.CALIB_FIX_K2                    # Fix k2 distortion coefficient
cv2.fisheye.CALIB_FIX_K3                    # Fix k3 distortion coefficient
cv2.fisheye.CALIB_FIX_K4                    # Fix k4 distortion coefficient
cv2.fisheye.CALIB_FIX_INTRINSIC             # Fix intrinsic parameters
cv2.fisheye.CALIB_FIX_PRINCIPAL_POINT       # Fix principal point
```

### Geometric Relationships

Fundamental matrix, essential matrix, and homography describe geometric relationships between two views of a scene, essential for structure from motion and image alignment.

```python { .api }
H, mask = cv2.findHomography(
    srcPoints,             # Source points (Nx2 or Nx1x2 array)
    dstPoints,             # Destination points (Nx2 or Nx1x2 array)
    method=0,              # Method to compute homography (0, RANSAC, LMEDS, RHO)
    ransacReprojThreshold=3.0,  # Maximum reprojection error (RANSAC/RHO only)
    mask=None,             # Output mask of inliers
    maxIters=2000,         # Maximum number of RANSAC iterations
    confidence=0.995       # Confidence level for RANSAC
)
# Finds perspective transformation (homography) between two planes
# Returns: 3x3 homography matrix, mask of inlier points
```

```python { .api }
F, mask = cv2.findFundamentalMat(
    points1,               # Points from first image (Nx2 or Nx1x2 array)
    points2,               # Points from second image (Nx2 or Nx1x2 array)
    method=cv2.FM_RANSAC,  # Method (FM_7POINT, FM_8POINT, FM_RANSAC, FM_LMEDS)
    ransacReprojThreshold=3.0,  # Distance threshold for RANSAC
    confidence=0.99,       # Confidence level (0 to 1)
    mask=None              # Output mask of inlier points
)
# Calculates fundamental matrix from corresponding points in two images
# Returns: 3x3 fundamental matrix (or multiple matrices for FM_7POINT), inlier mask
```

```python { .api }
E, mask = cv2.findEssentialMat(
    points1,               # Points from first image (Nx2 or Nx1x2 array)
    points2,               # Points from second image (Nx2 or Nx1x2 array)
    cameraMatrix=None,     # Camera intrinsic matrix (or focal length if scalar)
    method=cv2.RANSAC,     # Method (RANSAC, LMEDS)
    prob=0.999,            # Confidence level
    threshold=1.0,         # Distance threshold for RANSAC
    mask=None              # Output mask of inlier points
)
# Calculates essential matrix from corresponding points in two images
# Essential matrix relates corresponding points in calibrated cameras
# Returns: 3x3 essential matrix, inlier mask
```

**Geometric Estimation Methods:**

```python { .api }
# Methods for homography and fundamental matrix estimation:
cv2.FM_7POINT                      # 7-point algorithm (exactly 7 points)
cv2.FM_8POINT                      # 8-point algorithm (8+ points)
cv2.FM_RANSAC                      # RANSAC-based robust method
cv2.FM_LMEDS                       # Least-Median robust method

cv2.RANSAC                         # RANSAC (RANdom SAmple Consensus)
cv2.LMEDS                          # LMedS (Least-Median of Squares)
cv2.RHO                            # RHO algorithm (faster RANSAC variant)
```

### 3D Reconstruction

3D reconstruction recovers 3D structure from 2D images by triangulating corresponding points and estimating camera poses.

```python { .api }
points4D = cv2.triangulatePoints(
    projMatr1,             # Projection matrix for first camera (3x4)
    projMatr2,             # Projection matrix for second camera (3x4)
    projPoints1,           # 2D points in first image (2xN array)
    projPoints2            # 2D points in second image (2xN array)
)
# Reconstructs 3D points from two views via triangulation
# Returns: 4xN array of homogeneous 3D points (divide by 4th coordinate)
```

```python { .api }
retval, R, t, mask = cv2.recoverPose(
    E,                     # Essential matrix
    points1,               # Points from first image (Nx2 array)
    points2,               # Points from second image (Nx2 array)
    cameraMatrix=None,     # Camera intrinsic matrix (or focal length if scalar)
    R=None,                # Output rotation matrix
    t=None,                # Output translation vector
    mask=None,             # Input/output mask of inlier points
    distanceThresh=None    # Distance threshold for point validity
)
# Recovers relative camera rotation and translation from essential matrix
# Returns: number of inliers, rotation matrix, translation vector, inlier mask
```

```python { .api }
image3D = cv2.reprojectImageTo3D(
    disparity,             # Input disparity map (single-channel floating-point)
    Q,                     # 4x4 disparity-to-depth mapping matrix (from stereoRectify)
    image3D=None,          # Output 3-channel floating-point image (X, Y, Z)
    handleMissingValues=False,  # Whether to handle invalid disparity values
    ddepth=-1              # Depth of output image (default uses CV_32F)
)
# Reprojects disparity image to 3D space
# Returns: 3-channel image where each pixel contains (X, Y, Z) coordinates
```

### Transformation Estimation

These functions estimate various geometric transformations between sets of points, useful for image registration, alignment, and tracking.

```python { .api }
retval, inliers = cv2.estimateAffine2D(
    from_,                 # Source 2D points (Nx2 or Nx1x2 array)
    to,                    # Destination 2D points (Nx2 or Nx1x2 array)
    inliers=None,          # Output vector of inlier indices
    method=cv2.RANSAC,     # Robust estimation method (RANSAC or LMEDS)
    ransacReprojThreshold=3.0,  # Maximum reprojection error
    maxIters=2000,         # Maximum number of iterations
    confidence=0.99,       # Confidence level
    refineIters=10         # Number of refinement iterations
)
# Estimates 2D affine transformation (6 DOF: rotation, translation, scale, shear)
# Returns: 2x3 affine transformation matrix, inlier mask
```

```python { .api }
retval, inliers, scale = cv2.estimateAffine3D(
    src,                   # Source 3D points (Nx3 or Nx1x3 array)
    dst,                   # Destination 3D points (Nx3 or Nx1x3 array)
    out=None,              # Output 3x4 affine transformation matrix
    inliers=None,          # Output vector of inlier indices
    ransacThreshold=3.0,   # Maximum reprojection error for RANSAC
    confidence=0.99        # Confidence level (0 to 1)
)
# Estimates 3D affine transformation between two 3D point sets
# Returns: 3x4 affine transformation matrix, inlier mask, scale factor
```

```python { .api }
retval, inliers = cv2.estimateAffinePartial2D(
    from_,                 # Source 2D points (Nx2 or Nx1x2 array)
    to,                    # Destination 2D points (Nx2 or Nx1x2 array)
    inliers=None,          # Output vector of inlier indices
    method=cv2.RANSAC,     # Robust estimation method (RANSAC or LMEDS)
    ransacReprojThreshold=3.0,  # Maximum reprojection error
    maxIters=2000,         # Maximum number of iterations
    confidence=0.99,       # Confidence level
    refineIters=10         # Number of refinement iterations
)
# Estimates partial 2D affine transformation (4 DOF: rotation, translation, uniform scale)
# No shear or non-uniform scaling allowed
# Returns: 2x3 affine transformation matrix, inlier mask
```

**Robust Estimation Methods:**

```python { .api }
# Methods for robust transformation estimation:
cv2.RANSAC                         # RANSAC (RANdom SAmple Consensus) - handles outliers
cv2.LMEDS                          # LMedS (Least-Median of Squares) - robust to 50% outliers
cv2.RHO                            # RHO algorithm - faster RANSAC variant
```
