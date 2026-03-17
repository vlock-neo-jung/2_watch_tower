# ArUco Marker Detection

ArUco markers are square fiducial markers used for camera pose estimation, augmented reality, and object tracking. The `cv2.aruco` module provides tools for detecting ArUco markers, estimating their poses, and using them for camera calibration.

## Overview

ArUco markers are binary square patterns with a unique identifier. They're commonly used in:
- Camera calibration
- Pose estimation for AR/VR applications
- Robot navigation and localization
- Object tracking
- Measurement and 3D reconstruction

## Capabilities

### Dictionary Management

ArUco dictionaries define the set of valid marker patterns. OpenCV provides predefined dictionaries with various marker sizes and counts.

```python { .api }
def aruco.getPredefinedDictionary(name: int) -> aruco.Dictionary:
    """
    Get a predefined ArUco dictionary.

    Args:
        name: Dictionary identifier (e.g., cv2.aruco.DICT_4X4_50)

    Returns: ArUco dictionary object
    """
    ...

class aruco.Dictionary:
    """
    Dictionary of ArUco marker patterns.
    Contains all valid marker codes for a specific marker configuration.
    """
    bytesList: np.ndarray  # Array of marker bit patterns
    markerSize: int        # Size of marker in bits (e.g., 4, 5, 6, 7)
    maxCorrectionBits: int # Maximum number of bits that can be corrected

    def __init__(self, bytesList, markerSize, maxCorrectionBits): ...
    def getDistanceToId(self, bits, id, allRotations=True): ...
    def identify(self, onlyBits, idx, rotation, maxCorrectionRate): ...
```

**Predefined Dictionary Constants:**

```python { .api }
# 4x4 bit markers
cv2.aruco.DICT_4X4_50: int      # 50 markers, 4x4 bits
cv2.aruco.DICT_4X4_100: int     # 100 markers, 4x4 bits
cv2.aruco.DICT_4X4_250: int     # 250 markers, 4x4 bits
cv2.aruco.DICT_4X4_1000: int    # 1000 markers, 4x4 bits

# 5x5 bit markers
cv2.aruco.DICT_5X5_50: int      # 50 markers, 5x5 bits
cv2.aruco.DICT_5X5_100: int     # 100 markers, 5x5 bits
cv2.aruco.DICT_5X5_250: int     # 250 markers, 5x5 bits
cv2.aruco.DICT_5X5_1000: int    # 1000 markers, 5x5 bits

# 6x6 bit markers
cv2.aruco.DICT_6X6_50: int      # 50 markers, 6x6 bits
cv2.aruco.DICT_6X6_100: int     # 100 markers, 6x6 bits
cv2.aruco.DICT_6X6_250: int     # 250 markers, 6x6 bits
cv2.aruco.DICT_6X6_1000: int    # 1000 markers, 6x6 bits

# 7x7 bit markers
cv2.aruco.DICT_7X7_50: int      # 50 markers, 7x7 bits
cv2.aruco.DICT_7X7_100: int     # 100 markers, 7x7 bits
cv2.aruco.DICT_7X7_250: int     # 250 markers, 7x7 bits
cv2.aruco.DICT_7X7_1000: int    # 1000 markers, 7x7 bits

# Original ArUco dictionary
cv2.aruco.DICT_ARUCO_ORIGINAL: int  # Original ArUco dictionary (1024 markers, 5x5 bits)
```

### Marker Detection

Detect ArUco markers in images using the ArucoDetector class or legacy functions.

```python { .api }
class aruco.ArucoDetector:
    """
    ArUco marker detector (recommended for OpenCV 4.7+).
    Encapsulates dictionary and detection parameters.
    """
    def __init__(self, dictionary: aruco.Dictionary, detectorParams: aruco.DetectorParameters = None): ...

    def detectMarkers(self, image: np.ndarray, corners=None, ids=None, rejectedImgPoints=None):
        """
        Detect ArUco markers in an image.

        Args:
            image: Input image (grayscale or color)
            corners: Output vector of detected marker corners
            ids: Output vector of detected marker identifiers
            rejectedImgPoints: Output vector of rejected candidate markers

        Returns: Tuple of (corners, ids, rejected)
            - corners: List of marker corners (list of 4x2 arrays)
            - ids: Array of marker IDs
            - rejected: List of rejected marker corner candidates
        """
        ...

class aruco.DetectorParameters:
    """
    Parameters for ArUco marker detection.
    Controls detection sensitivity, accuracy, and performance.
    """
    def __init__(self): ...

    # Adaptive thresholding parameters
    adaptiveThreshWinSizeMin: int       # Minimum window size for adaptive thresholding
    adaptiveThreshWinSizeMax: int       # Maximum window size for adaptive thresholding
    adaptiveThreshWinSizeStep: int      # Step size for window size search
    adaptiveThreshConstant: float       # Constant subtracted from mean in adaptive thresholding

    # Contour filtering
    minMarkerPerimeterRate: float       # Minimum perimeter as ratio of image diagonal
    maxMarkerPerimeterRate: float       # Maximum perimeter as ratio of image diagonal
    polygonalApproxAccuracyRate: float  # Accuracy for polygon approximation

    # Marker identification
    minCornerDistanceRate: float        # Minimum distance between corners
    minDistanceToBorder: int            # Minimum distance from image border
    minMarkerDistanceRate: float        # Minimum distance between markers

    # Bit extraction
    markerBorderBits: int               # Width of marker border (usually 1)
    perspectiveRemovePixelPerCell: int  # Number of pixels per cell for perspective removal
    perspectiveRemoveIgnoredMarginPerCell: float  # Margin to ignore in each cell

    # Error correction
    maxErroneousBitsInBorderRate: float # Maximum allowed erroneous bits in border
    minOtsuStdDev: float                # Minimum standard deviation for Otsu threshold
    errorCorrectionRate: float          # Error correction rate (0.0-1.0)

    # Corner refinement
    cornerRefinementMethod: int         # Corner refinement method
    cornerRefinementWinSize: int        # Window size for corner refinement
    cornerRefinementMaxIterations: int  # Max iterations for corner refinement
    cornerRefinementMinAccuracy: float  # Minimum accuracy for corner refinement
```

**Legacy Detection Function:**

```python { .api }
def aruco.detectMarkers(image, dictionary, parameters=None, corners=None, ids=None, rejectedImgPoints=None):
    """
    Detect ArUco markers (legacy function, use ArucoDetector for new code).

    Args:
        image: Input image
        dictionary: ArUco dictionary
        parameters: Detector parameters
        corners: Output marker corners
        ids: Output marker IDs
        rejectedImgPoints: Output rejected candidates

    Returns: Tuple of (corners, ids, rejected)
    """
    ...
```

**Usage Example:**

```python
import cv2
import numpy as np

# Load ArUco dictionary
aruco_dict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_6X6_250)

# Create detector parameters
parameters = cv2.aruco.DetectorParameters()
parameters.adaptiveThreshConstant = 7

# Create detector
detector = cv2.aruco.ArucoDetector(aruco_dict, parameters)

# Read image
image = cv2.imread('markers.jpg')
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Detect markers
corners, ids, rejected = detector.detectMarkers(gray)

print(f"Detected {len(corners)} markers")
if ids is not None:
    print(f"Marker IDs: {ids.flatten()}")
```

### Marker Visualization

Draw detected markers and marker axes on images.

```python { .api }
def aruco.drawDetectedMarkers(image, corners, ids=None, borderColor=(0, 255, 0)):
    """
    Draw detected markers on an image.

    Args:
        image: Input/output image
        corners: Detected marker corners (from detectMarkers)
        ids: Detected marker IDs (optional)
        borderColor: Color for marker borders (B, G, R)

    Returns: Image with drawn markers
    """
    ...

def aruco.drawMarker(dictionary, id, sidePixels, img=None, borderBits=1):
    """
    Generate an ArUco marker image.

    Args:
        dictionary: ArUco dictionary
        id: Marker ID to generate (0 to dictionary size - 1)
        sidePixels: Size of output image in pixels
        img: Output image (if None, creates new image)
        borderBits: Width of marker border in bits (usually 1)

    Returns: Marker image
    """
    ...

def aruco.drawAxis(image, cameraMatrix, distCoeffs, rvec, tvec, length):
    """
    Draw coordinate system axes for a marker pose.

    Args:
        image: Input/output image
        cameraMatrix: Camera intrinsic matrix (3x3)
        distCoeffs: Camera distortion coefficients
        rvec: Rotation vector for marker pose
        tvec: Translation vector for marker pose
        length: Length of axes in same units as tvec

    Returns: Image with drawn axes (X=red, Y=green, Z=blue)
    """
    ...
```

**Usage Example:**

```python
# Draw detected markers
if ids is not None:
    cv2.aruco.drawDetectedMarkers(image, corners, ids)

# Generate a marker for printing
marker_image = cv2.aruco.drawMarker(aruco_dict, id=42, sidePixels=200)
cv2.imwrite('marker_42.png', marker_image)
```

### Pose Estimation

Estimate the 3D pose (position and orientation) of markers relative to the camera.

```python { .api }
def aruco.estimatePoseSingleMarkers(corners, markerLength, cameraMatrix, distCoeffs, rvecs=None, tvecs=None):
    """
    Estimate pose of single ArUco markers.

    Args:
        corners: Detected marker corners (from detectMarkers)
        markerLength: Physical marker side length in meters
        cameraMatrix: Camera intrinsic matrix (3x3)
        distCoeffs: Camera distortion coefficients
        rvecs: Output rotation vectors for each marker
        tvecs: Output translation vectors for each marker

    Returns: Tuple of (rvecs, tvecs, objPoints)
        - rvecs: Rotation vectors (axis-angle representation)
        - tvecs: Translation vectors (camera to marker center)
        - objPoints: 3D corner points in marker coordinate system
    """
    ...
```

**Usage Example:**

```python
# Estimate marker poses
if ids is not None:
    # Camera calibration parameters
    camera_matrix = np.array([[800, 0, 320], [0, 800, 240], [0, 0, 1]], dtype=float)
    dist_coeffs = np.zeros(5)
    marker_length = 0.05  # 5 cm markers

    # Estimate poses
    rvecs, tvecs, _ = cv2.aruco.estimatePoseSingleMarkers(
        corners, marker_length, camera_matrix, dist_coeffs
    )

    # Draw axes on each marker
    for i in range(len(ids)):
        cv2.aruco.drawAxis(image, camera_matrix, dist_coeffs,
                          rvecs[i], tvecs[i], marker_length * 0.5)

    # Print distance to first marker
    distance = np.linalg.norm(tvecs[0])
    print(f"Marker 0 distance: {distance:.3f} meters")
```

### Board Detection

ArUco boards are collections of markers with known spatial arrangement, useful for camera calibration and more robust pose estimation.

```python { .api }
class aruco.Board:
    """
    Base class for ArUco marker boards.
    """
    dictionary: aruco.Dictionary  # Dictionary used by the board
    ids: np.ndarray              # Marker IDs in the board
    objPoints: list              # 3D positions of marker corners

class aruco.GridBoard(aruco.Board):
    """
    Grid board of ArUco markers.
    """
    @staticmethod
    def create(markersX, markersY, markerLength, markerSeparation, dictionary, firstMarker=0):
        """
        Create a grid board.

        Args:
            markersX: Number of markers in X direction
            markersY: Number of markers in Y direction
            markerLength: Marker side length (same units as markerSeparation)
            markerSeparation: Separation between markers
            dictionary: ArUco dictionary
            firstMarker: ID of first marker in board

        Returns: GridBoard object
        """
        ...

def aruco.estimatePoseBoard(corners, ids, board, cameraMatrix, distCoeffs, rvec=None, tvec=None):
    """
    Estimate pose of an ArUco board.

    Args:
        corners: Detected marker corners
        ids: Detected marker IDs
        board: Board object
        cameraMatrix: Camera intrinsic matrix
        distCoeffs: Camera distortion coefficients
        rvec: Initial/output rotation vector
        tvec: Initial/output translation vector

    Returns: Tuple of (num_markers, rvec, tvec)
        - num_markers: Number of markers used for pose estimation
        - rvec: Rotation vector
        - tvec: Translation vector
    """
    ...
```

### ChArUco Boards

ChArUco boards combine a chessboard pattern with ArUco markers, providing benefits of both (corner accuracy + robust detection).

```python { .api }
class aruco.CharucoBoard(aruco.Board):
    """
    ChArUco board - chessboard + ArUco markers.
    Provides accurate corners from chessboard and robust detection from markers.
    """
    @staticmethod
    def create(squaresX, squaresY, squareLength, markerLength, dictionary):
        """
        Create a ChArUco board.

        Args:
            squaresX: Number of chessboard squares in X direction
            squaresY: Number of chessboard squares in Y direction
            squareLength: Chessboard square side length
            markerLength: ArUco marker side length
            dictionary: ArUco dictionary

        Returns: CharucoBoard object
        """
        ...

class aruco.CharucoDetector:
    """
    ChArUco pattern detector.
    """
    def __init__(self, board, charucoParams=None, detectorParams=None, refineParams=None): ...

    def detectBoard(self, image, charucoCorners=None, charucoIds=None, markerCorners=None, markerIds=None):
        """
        Detect ChArUco board corners.

        Args:
            image: Input image
            charucoCorners: Output chessboard corner coordinates
            charucoIds: Output chessboard corner IDs
            markerCorners: Output ArUco marker corners
            markerIds: Output ArUco marker IDs

        Returns: Tuple of (charucoCorners, charucoIds, markerCorners, markerIds)
        """
        ...

def aruco.interpolateCornersCharuco(markerCorners, markerIds, image, board, charucoCorners=None, charucoIds=None, cameraMatrix=None, distCoeffs=None, minMarkers=2):
    """
    Interpolate ChArUco corners from detected ArUco markers.

    Args:
        markerCorners: Detected ArUco marker corners
        markerIds: Detected ArUco marker IDs
        image: Input image
        board: ChArUco board
        charucoCorners: Output ChArUco corner coordinates
        charucoIds: Output ChArUco corner IDs
        cameraMatrix: Optional camera matrix for refinement
        distCoeffs: Optional distortion coefficients
        minMarkers: Minimum number of adjacent markers for corner interpolation

    Returns: Tuple of (num_corners, charucoCorners, charucoIds)
    """
    ...

def aruco.drawDetectedCornersCharuco(image, charucoCorners, charucoIds=None, cornerColor=(255, 0, 0)):
    """
    Draw detected ChArUco corners.

    Args:
        image: Input/output image
        charucoCorners: Detected ChArUco corners
        charucoIds: Detected ChArUco corner IDs
        cornerColor: Color for corners

    Returns: Image with drawn corners
    """
    ...
```

### Camera Calibration with ArUco

Use ArUco markers or ChArUco boards for camera calibration.

```python { .api }
def aruco.calibrateCameraAruco(corners, ids, counter, board, imageSize, cameraMatrix, distCoeffs, rvecs=None, tvecs=None, flags=0, criteria=None):
    """
    Calibrate camera using ArUco board.

    Args:
        corners: Vector of detected marker corners for each image
        ids: Vector of detected marker IDs for each image
        counter: Number of markers detected in each image
        board: ArUco board
        imageSize: Image size
        cameraMatrix: Input/output camera matrix
        distCoeffs: Input/output distortion coefficients
        rvecs: Output rotation vectors for each image
        tvecs: Output translation vectors for each image
        flags: Calibration flags (same as cv2.calibrateCamera)
        criteria: Termination criteria

    Returns: Tuple of (reprojection_error, cameraMatrix, distCoeffs, rvecs, tvecs)
    """
    ...

def aruco.calibrateCameraCharuco(charucoCorners, charucoIds, board, imageSize, cameraMatrix, distCoeffs, rvecs=None, tvecs=None, flags=0, criteria=None):
    """
    Calibrate camera using ChArUco board (more accurate than ArUco-only).

    Args:
        charucoCorners: Vector of detected ChArUco corners for each image
        charucoIds: Vector of detected ChArUco corner IDs for each image
        board: ChArUco board
        imageSize: Image size
        cameraMatrix: Input/output camera matrix
        distCoeffs: Input/output distortion coefficients
        rvecs: Output rotation vectors for each image
        tvecs: Output translation vectors for each image
        flags: Calibration flags
        criteria: Termination criteria

    Returns: Tuple of (reprojection_error, cameraMatrix, distCoeffs, rvecs, tvecs)
    """
    ...
```

## Complete Workflow Example

```python
import cv2
import numpy as np

# 1. Create and print markers
aruco_dict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_6X6_250)

# Generate markers for printing
for marker_id in range(4):
    marker_img = cv2.aruco.drawMarker(aruco_dict, marker_id, 200)
    cv2.imwrite(f'marker_{marker_id}.png', marker_img)

# 2. Detect markers in video
detector = cv2.aruco.ArucoDetector(aruco_dict)
cap = cv2.VideoCapture(0)

# Camera calibration (replace with your calibrated values)
camera_matrix = np.array([[800, 0, 320], [0, 800, 240], [0, 0, 1]], dtype=float)
dist_coeffs = np.zeros(5)
marker_length = 0.05  # 5 cm

while True:
    ret, frame = cap.read()
    if not ret:
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detect markers
    corners, ids, rejected = detector.detectMarkers(gray)

    if ids is not None:
        # Draw detected markers
        cv2.aruco.drawDetectedMarkers(frame, corners, ids)

        # Estimate poses
        rvecs, tvecs, _ = cv2.aruco.estimatePoseSingleMarkers(
            corners, marker_length, camera_matrix, dist_coeffs
        )

        # Draw axes for each marker
        for i in range(len(ids)):
            cv2.aruco.drawAxis(frame, camera_matrix, dist_coeffs,
                              rvecs[i], tvecs[i], marker_length * 0.5)

    cv2.imshow('ArUco Detection', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
```
