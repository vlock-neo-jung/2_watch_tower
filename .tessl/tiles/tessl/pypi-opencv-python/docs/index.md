# OpenCV-Python

Pre-built Python bindings for OpenCV (Open Source Computer Vision Library), providing comprehensive computer vision and image processing capabilities with over 2500 algorithms. OpenCV is the industry-standard library for computer vision tasks including image and video processing, object detection, face recognition, feature extraction, camera calibration, machine learning, and real-time analysis.

## Package Information

- **Package Name**: opencv-python
- **Language**: Python
- **Installation**: `pip install opencv-python`
- **Official Documentation**: https://docs.opencv.org/4.x/

## Package Variants

OpenCV-Python is available in four variants (install only one):

1. **opencv-python** - Main modules for desktop environments (includes GUI)
2. **opencv-contrib-python** - Main + contrib/extra experimental modules (includes GUI)
3. **opencv-python-headless** - Main modules without GUI dependencies (for servers/Docker)
4. **opencv-contrib-python-headless** - Main + contrib modules without GUI (for servers/Docker)

## Core Imports

```python
import cv2
```

All OpenCV functionality is accessed through the `cv2` module.

## Basic Usage

```python
import cv2
import numpy as np

# Read an image
image = cv2.imread('photo.jpg')

# Convert to grayscale
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Apply Gaussian blur
blurred = cv2.GaussianBlur(gray, (5, 5), 0)

# Detect edges using Canny
edges = cv2.Canny(blurred, 50, 150)

# Display the result (requires GUI)
cv2.imshow('Edges', edges)
cv2.waitKey(0)
cv2.destroyAllWindows()

# Save the result
cv2.imwrite('edges.jpg', edges)

# Video capture from camera
cap = cv2.VideoCapture(0)
ret, frame = cap.read()
cap.release()
```

## Architecture

OpenCV is organized into modular components:

- **Core Module** - Fundamental data structures (Mat arrays), basic operations, linear algebra
- **Image Processing** - Filtering, transformations, color conversion, histograms, feature detection
- **Video I/O** - Reading and writing video files and camera streams
- **GUI Module** - Window management, event handling, simple UI elements (highgui)
- **Video Analysis** - Motion analysis, object tracking, background subtraction
- **Camera Calibration** - Camera calibration, stereo vision, 3D reconstruction
- **2D Features** - Feature detection and description (SIFT, ORB, AKAZE)
- **Object Detection** - Cascade classifiers, HOG descriptor, DNN module
- **Deep Learning** - DNN inference engine supporting multiple frameworks
- **Machine Learning** - Statistical ML algorithms (SVM, KNN, Decision Trees, Neural Networks)

### Image Representation

OpenCV represents images as NumPy arrays:
- **Color images**: `(height, width, channels)` - default BGR color order
- **Grayscale images**: `(height, width)`
- **Default data type**: `numpy.uint8` (values 0-255)
- **Coordinate system**: Origin (0,0) at top-left, X-axis right, Y-axis down

**Important**: OpenCV uses **BGR** color order (not RGB). Use `cv2.cvtColor()` to convert between color spaces.

## Capabilities

### Core Operations and Array Manipulation

Core functionality for working with multi-dimensional arrays (images, matrices) including arithmetic operations, logical operations, array transformations, linear algebra, and random number generation.

```python { .api }
# Arithmetic operations
def add(src1, src2, dst=None, mask=None, dtype=None): ...
def subtract(src1, src2, dst=None, mask=None, dtype=None): ...
def multiply(src1, src2, dst=None, scale=None, dtype=None): ...
def divide(src1, src2, dst=None, scale=None, dtype=None): ...
def addWeighted(src1, alpha, src2, beta, gamma, dst=None, dtype=None): ...

# Logical operations
def bitwise_and(src1, src2, dst=None, mask=None): ...
def bitwise_or(src1, src2, dst=None, mask=None): ...
def bitwise_xor(src1, src2, dst=None, mask=None): ...
def bitwise_not(src, dst=None, mask=None): ...

# Array transformations
def flip(src, flipCode, dst=None): ...
def rotate(src, rotateCode, dst=None): ...
def transpose(src, dst=None): ...
def split(m): ...
def merge(mv, dst=None): ...

# Statistics and analysis
def mean(src, mask=None): ...
def norm(src1, normType=None, mask=None): ...
def normalize(src, dst, alpha=None, beta=None, norm_type=None, dtype=None, mask=None): ...
def minMaxLoc(src, mask=None): ...
def meanStdDev(src, mean=None, stddev=None, mask=None): ...
def countNonZero(src): ...

# Mathematical operations
def sqrt(src, dst=None): ...
def pow(src, power, dst=None): ...
def exp(src, dst=None): ...
def log(src, dst=None): ...

# Fourier transforms
def dft(src, dst=None, flags=0, nonzeroRows=0): ...
def idft(src, dst=None, flags=0, nonzeroRows=0): ...

# Image border operations
def copyMakeBorder(src, top, bottom, left, right, borderType, dst=None, value=None): ...
```

[Core Operations](./core-operations.md)

### Image I/O and Video Capture

Reading and writing images and videos, capturing from cameras and video files, codec configuration.

```python { .api }
# Image I/O
def imread(filename, flags=None): ...
def imwrite(filename, img, params=None): ...
def imdecode(buf, flags): ...
def imencode(ext, img, params=None): ...
def imreadmulti(filename, mats, flags=None): ...
def imcount(filename, flags=None): ...
def haveImageReader(filename): ...
def haveImageWriter(filename): ...

# Video capture
class VideoCapture:
    def __init__(self, index): ...
    def read(self): ...
    def grab(self): ...
    def retrieve(self, image=None, flag=None): ...
    def get(self, propId): ...
    def set(self, propId, value): ...
    def release(self): ...
    def isOpened(self): ...

# Video writing
class VideoWriter:
    def __init__(self, filename, fourcc, fps, frameSize, isColor=True): ...
    def write(self, image): ...
    def release(self): ...
    def isOpened(self): ...

def VideoWriter_fourcc(*args): ...
```

[Image and Video I/O](./image-video-io.md)

### Image Processing and Filtering

Comprehensive image processing including smoothing, edge detection, morphological operations, geometric transformations, color space conversion, and histogram operations.

```python { .api }
# Filtering
def blur(src, ksize, dst=None, anchor=None, borderType=None): ...
def GaussianBlur(src, ksize, sigmaX, dst=None, sigmaY=None, borderType=None): ...
def medianBlur(src, ksize, dst=None): ...
def bilateralFilter(src, d, sigmaColor, sigmaSpace, dst=None, borderType=None): ...
def filter2D(src, ddepth, kernel, dst=None, anchor=None, delta=None, borderType=None): ...
def Sobel(src, ddepth, dx, dy, dst=None, ksize=None, scale=None, delta=None, borderType=None): ...
def Laplacian(src, ddepth, dst=None, ksize=None, scale=None, delta=None, borderType=None): ...
def Canny(image, threshold1, threshold2, edges=None, apertureSize=None, L2gradient=None): ...

# Corner detection
def goodFeaturesToTrack(image, maxCorners, qualityLevel, minDistance, corners=None, mask=None, blockSize=3, useHarrisDetector=False, k=0.04): ...
def cornerHarris(src, blockSize, ksize, k, dst=None, borderType=None): ...
def cornerSubPix(image, corners, winSize, zeroZone, criteria): ...

# Morphological operations
def erode(src, kernel, dst=None, anchor=None, iterations=None, borderType=None, borderValue=None): ...
def dilate(src, kernel, dst=None, anchor=None, iterations=None, borderType=None, borderValue=None): ...
def morphologyEx(src, op, kernel, dst=None, anchor=None, iterations=None, borderType=None, borderValue=None): ...
def getStructuringElement(shape, ksize, anchor=None): ...

# Geometric transformations
def resize(src, dsize, dst=None, fx=None, fy=None, interpolation=None): ...
def warpAffine(src, M, dsize, dst=None, flags=None, borderMode=None, borderValue=None): ...
def warpPerspective(src, M, dsize, dst=None, flags=None, borderMode=None, borderValue=None): ...
def getRotationMatrix2D(center, angle, scale): ...
def getAffineTransform(src, dst): ...
def getPerspectiveTransform(src, dst): ...

# Color conversion
def cvtColor(src, code, dst=None, dstCn=None): ...

# Thresholding
def threshold(src, thresh, maxval, type, dst=None): ...
def adaptiveThreshold(src, maxValue, adaptiveMethod, thresholdType, blockSize, C, dst=None): ...

# Segmentation
def connectedComponents(image, labels=None, connectivity=8, ltype=None): ...
def connectedComponentsWithStats(image, labels=None, stats=None, centroids=None, connectivity=8, ltype=None): ...
def grabCut(img, mask, rect, bgdModel, fgdModel, iterCount, mode=None): ...
```

[Image Processing](./image-processing.md)

### Contour Detection and Shape Analysis

Finding and analyzing contours, calculating shape properties, fitting geometric primitives, and shape matching.

```python { .api }
# Contour detection
def findContours(image, mode, method, contours=None, hierarchy=None, offset=None): ...
def drawContours(image, contours, contourIdx, color, thickness=None, lineType=None, hierarchy=None, maxLevel=None, offset=None): ...

# Contour analysis
def contourArea(contour, oriented=None): ...
def arcLength(curve, closed): ...
def approxPolyDP(curve, epsilon, closed, approxCurve=None): ...
def convexHull(points, hull=None, clockwise=None, returnPoints=None): ...
def boundingRect(array): ...
def minAreaRect(points): ...
def minEnclosingCircle(points): ...
def fitEllipse(points): ...
def moments(array, binaryImage=None): ...
def HuMoments(m, hu=None): ...
def matchShapes(contour1, contour2, method, parameter): ...
def pointPolygonTest(contour, pt, measureDist): ...
```

[Contours and Shapes](./contours-shapes.md)

### Feature Detection and Description

Detecting and describing features for image matching, object recognition, and tracking.

```python { .api }
# SIFT (Scale-Invariant Feature Transform)
class SIFT(cv2.Feature2D):
    @staticmethod
    def create(nfeatures=None, nOctaveLayers=None, contrastThreshold=None, edgeThreshold=None, sigma=None): ...

# ORB (Oriented FAST and Rotated BRIEF)
class ORB(cv2.Feature2D):
    @staticmethod
    def create(nfeatures=None, scaleFactor=None, nlevels=None, edgeThreshold=None, firstLevel=None, WTA_K=None, scoreType=None, patchSize=None, fastThreshold=None): ...

# AKAZE
class AKAZE(cv2.Feature2D):
    @staticmethod
    def create(descriptor_type=None, descriptor_size=None, descriptor_channels=None, threshold=None, nOctaves=None, nOctaveLayers=None, diffusivity=None): ...

# Feature2D base class methods
class Feature2D:
    def detect(self, image, mask=None): ...
    def compute(self, image, keypoints, descriptors=None): ...
    def detectAndCompute(self, image, mask, descriptors=None): ...

# Feature matching
class BFMatcher(cv2.DescriptorMatcher):
    def __init__(self, normType=None, crossCheck=None): ...

class FlannBasedMatcher(cv2.DescriptorMatcher):
    def __init__(self, indexParams=None, searchParams=None): ...

class DescriptorMatcher:
    def match(self, queryDescriptors, trainDescriptors, mask=None): ...
    def knnMatch(self, queryDescriptors, trainDescriptors, k, mask=None, compactResult=None): ...

# Drawing
def drawKeypoints(image, keypoints, outImage, color=None, flags=None): ...
def drawMatches(img1, keypoints1, img2, keypoints2, matches1to2, outImg, matchColor=None, singlePointColor=None, matchesMask=None, flags=None): ...
```

[Feature Detection](./feature-detection.md)

### Object Detection and Recognition

Pre-trained classifiers for detecting faces, eyes, pedestrians, and other objects, plus QR code detection.

```python { .api }
# Cascade classifier
class CascadeClassifier:
    def __init__(self, filename=None): ...
    def load(self, filename): ...
    def detectMultiScale(self, image, scaleFactor=None, minNeighbors=None, flags=None, minSize=None, maxSize=None): ...

# HOG descriptor
class HOGDescriptor:
    def __init__(self): ...
    def compute(self, img, winStride=None, padding=None, locations=None): ...
    def detectMultiScale(self, img, hitThreshold=None, winStride=None, padding=None, scale=None, finalThreshold=None, useMeanshiftGrouping=None): ...
    def setSVMDetector(self, _svmdetector): ...
    @staticmethod
    def getDefaultPeopleDetector(): ...

# QR code detection
class QRCodeDetector:
    def __init__(self): ...
    def detect(self, img, points=None): ...
    def decode(self, img, points, straight_qrcode=None): ...
    def detectAndDecode(self, img, points=None, straight_qrcode=None): ...
```

**Data files**: Haar cascade XML files are included via `cv2.data.haarcascades` path.

[Object Detection](./object-detection.md)

### Camera Calibration and 3D Reconstruction

Camera calibration, stereo vision, pose estimation, and 3D reconstruction from 2D images.

```python { .api }
# Camera calibration
def calibrateCamera(objectPoints, imagePoints, imageSize, cameraMatrix, distCoeffs, rvecs=None, tvecs=None, flags=None, criteria=None): ...
def findChessboardCorners(image, patternSize, corners=None, flags=None): ...
def findCirclesGrid(image, patternSize, centers=None, flags=None, blobDetector=None): ...
def drawChessboardCorners(image, patternSize, corners, patternWasFound): ...
def cornerSubPix(image, corners, winSize, zeroZone, criteria): ...

# Pose estimation
def solvePnP(objectPoints, imagePoints, cameraMatrix, distCoeffs, rvec=None, tvec=None, useExtrinsicGuess=None, flags=None): ...
def projectPoints(objectPoints, rvec, tvec, cameraMatrix, distCoeffs, imagePoints=None, jacobian=None, aspectRatio=None): ...
def Rodrigues(src, dst=None, jacobian=None): ...

# Undistortion
def undistort(src, cameraMatrix, distCoeffs, dst=None, newCameraMatrix=None): ...
def undistortPoints(src, cameraMatrix, distCoeffs, dst=None, R=None, P=None): ...
def getOptimalNewCameraMatrix(cameraMatrix, distCoeffs, imageSize, alpha, newImgSize=None, centerPrincipalPoint=None): ...
def initUndistortRectifyMap(cameraMatrix, distCoeffs, R, newCameraMatrix, size, m1type, map1=None, map2=None): ...

# Stereo
def stereoCalibrate(objectPoints, imagePoints1, imagePoints2, cameraMatrix1, distCoeffs1, cameraMatrix2, distCoeffs2, imageSize, R=None, T=None, E=None, F=None, flags=None, criteria=None): ...
def stereoRectify(cameraMatrix1, distCoeffs1, cameraMatrix2, distCoeffs2, imageSize, R, T, R1=None, R2=None, P1=None, P2=None, Q=None, flags=None, alpha=None, newImageSize=None): ...

# Homography and fundamental matrix
def findHomography(srcPoints, dstPoints, method=None, ransacReprojThreshold=None, mask=None, maxIters=None, confidence=None): ...
def findFundamentalMat(points1, points2, method=None, param1=None, param2=None, mask=None): ...
```

[Camera Calibration](./camera-calibration.md)

### Video Analysis and Object Tracking

Motion estimation, optical flow, background subtraction, and object tracking algorithms.

```python { .api }
# Optical flow
def calcOpticalFlowPyrLK(prevImg, nextImg, prevPts, nextPts, status=None, err=None, winSize=None, maxLevel=None, criteria=None, flags=None, minEigThreshold=None): ...
def calcOpticalFlowFarneback(prev, next, flow, pyr_scale, levels, winsize, iterations, poly_n, poly_sigma, flags): ...
def buildOpticalFlowPyramid(img, pyramid, winSize, maxLevel, withDerivatives=True, pyrBorder=None, derivBorder=None, tryReuseInputImage=True): ...
def readOpticalFlow(path): ...
def writeOpticalFlow(path, flow): ...

# Background subtraction
class BackgroundSubtractorMOG2(cv2.BackgroundSubtractor):
    def apply(self, image, fgmask=None, learningRate=None): ...
    def getBackgroundImage(self, backgroundImage=None): ...

class BackgroundSubtractorKNN(cv2.BackgroundSubtractor):
    def apply(self, image, fgmask=None, learningRate=None): ...
    def getBackgroundImage(self, backgroundImage=None): ...

def createBackgroundSubtractorMOG2(history=None, varThreshold=None, detectShadows=None): ...
def createBackgroundSubtractorKNN(history=None, dist2Threshold=None, detectShadows=None): ...

# Mean shift
def meanShift(probImage, window, criteria): ...
def CamShift(probImage, window, criteria): ...

# Tracking (newer API)
class TrackerDaSiamRPN(cv2.Tracker): ...
class TrackerMIL(cv2.Tracker): ...
class TrackerKCF(cv2.Tracker): ...

# Kalman filter
class KalmanFilter:
    def __init__(self, dynamParams, measureParams, controlParams=None, type=None): ...
    def predict(self, control=None): ...
    def correct(self, measurement): ...
```

[Video Analysis](./video-analysis.md)

### Deep Neural Networks (DNN Module)

Deep learning inference engine supporting models from TensorFlow, PyTorch, Caffe, ONNX, and Darknet.

```python { .api }
# Loading models
def dnn.readNet(model, config=None, framework=None): ...
def dnn.readNetFromCaffe(prototxt, caffeModel=None): ...
def dnn.readNetFromTensorflow(model, config=None): ...
def dnn.readNetFromONNX(onnxFile): ...
def dnn.readNetFromDarknet(cfgFile, darknetModel=None): ...

# Blob operations
def dnn.blobFromImage(image, scalefactor=None, size=None, mean=None, swapRB=None, crop=None, ddepth=None): ...
def dnn.blobFromImages(images, scalefactor=None, size=None, mean=None, swapRB=None, crop=None, ddepth=None): ...

# Neural network class
class dnn.Net:
    def setInput(self, blob, name=None, scalefactor=None, mean=None): ...
    def forward(self, outputName=None): ...
    def setPreferableBackend(self, backendId): ...
    def setPreferableTarget(self, targetId): ...
    def getLayerNames(self): ...
    def getUnconnectedOutLayersNames(self): ...

# Non-maximum suppression
def dnn.NMSBoxes(bboxes, scores, score_threshold, nms_threshold, eta=None, top_k=None): ...
```

[Deep Neural Networks](./dnn.md)

### Machine Learning

Statistical machine learning algorithms including SVM, decision trees, neural networks, k-nearest neighbors, and clustering.

```python { .api }
# SVM
class ml.SVM(cv2.ml.StatModel):
    @staticmethod
    def create(): ...
    def train(self, samples, layout, responses): ...
    def predict(self, samples, results=None, flags=None): ...
    def setKernel(self, kernelType): ...
    def setType(self, val): ...

# K-Nearest Neighbors
class ml.KNearest(cv2.ml.StatModel):
    @staticmethod
    def create(): ...
    def findNearest(self, samples, k, results=None, neighborResponses=None, dist=None): ...

# Decision Trees
class ml.DTrees(cv2.ml.StatModel):
    @staticmethod
    def create(): ...

# Random Forest
class ml.RTrees(cv2.ml.DTrees):
    @staticmethod
    def create(): ...

# Neural Networks
class ml.ANN_MLP(cv2.ml.StatModel):
    @staticmethod
    def create(): ...
    def setLayerSizes(self, _layer_sizes): ...
    def setActivationFunction(self, type, param1=None, param2=None): ...
    def setTrainMethod(self, method, param1=None, param2=None): ...

# Base class
class ml.StatModel:
    def train(self, samples, layout, responses): ...
    def predict(self, samples, results=None, flags=None): ...
    def save(self, filename): ...
    @staticmethod
    def load(filename): ...

# K-means clustering
def kmeans(data, K, bestLabels, criteria, attempts, flags, centers=None): ...
```

[Machine Learning](./machine-learning.md)

### GUI and Visualization

Window management, image display, trackbars, mouse event handling, and user interaction (not available in headless packages).

```python { .api }
# Window operations
def imshow(winname, mat): ...
def namedWindow(winname, flags=None): ...
def destroyWindow(winname): ...
def destroyAllWindows(): ...
def waitKey(delay=None): ...
def resizeWindow(winname, width, height): ...
def moveWindow(winname, x, y): ...
def setWindowTitle(winname, title): ...

# Trackbar
def createTrackbar(trackbarname, winname, value, count, onChange): ...
def getTrackbarPos(trackbarname, winname): ...
def setTrackbarPos(trackbarname, winname, pos): ...
def setTrackbarMin(trackbarname, winname, minval): ...
def setTrackbarMax(trackbarname, winname, maxval): ...

# Mouse events
def setMouseCallback(winname, onMouse, param=None): ...

# ROI selection
def selectROI(windowName, img, showCrosshair=None, fromCenter=None): ...
def selectROIs(windowName, img, showCrosshair=None, fromCenter=None): ...

# Drawing functions
def line(img, pt1, pt2, color, thickness=None, lineType=None, shift=None): ...
def circle(img, center, radius, color, thickness=None, lineType=None, shift=None): ...
def rectangle(img, pt1, pt2, color, thickness=None, lineType=None, shift=None): ...
def ellipse(img, center, axes, angle, startAngle, endAngle, color, thickness=None, lineType=None, shift=None): ...
def polylines(img, pts, isClosed, color, thickness=None, lineType=None, shift=None): ...
def fillPoly(img, pts, color, lineType=None, shift=None, offset=None): ...
def putText(img, text, org, fontFace, fontScale, color, thickness=None, lineType=None, bottomLeftOrigin=None): ...
```

[GUI and Drawing](./gui-drawing.md)

### Computational Photography

Advanced image processing for inpainting, denoising, HDR imaging, seamless cloning, and artistic effects.

```python { .api }
# Inpainting
def inpaint(src, inpaintMask, inpaintRadius, flags, dst=None): ...

# Denoising
def fastNlMeansDenoising(src, dst=None, h=None, templateWindowSize=None, searchWindowSize=None): ...
def fastNlMeansDenoisingColored(src, dst=None, h=None, hColor=None, templateWindowSize=None, searchWindowSize=None): ...

# Seamless cloning
def seamlessClone(src, dst, mask, p, flags, blend=None): ...

# Stylization
def stylization(src, dst=None, sigma_s=None, sigma_r=None): ...
def pencilSketch(src, dst1=None, dst2=None, sigma_s=None, sigma_r=None, shade_factor=None): ...
def detailEnhance(src, dst=None, sigma_s=None, sigma_r=None): ...
def edgePreservingFilter(src, dst=None, flags=None, sigma_s=None, sigma_r=None): ...

# HDR
def createMergeMertens(contrast_weight=None, saturation_weight=None, exposure_weight=None): ...
def createTonemapDrago(gamma=None, saturation=None, bias=None): ...
def createTonemapReinhard(gamma=None, intensity=None, light_adapt=None, color_adapt=None): ...
```

[Computational Photography](./computational-photography.md)

### Image Stitching

Creating panoramas from multiple images.

```python { .api }
class Stitcher:
    @staticmethod
    def create(mode=None): ...
    def stitch(self, images, masks=None): ...
    def estimateTransform(self, images, masks=None): ...
    def composePanorama(self, images=None): ...

def createStitcher(try_use_gpu=None): ...
```

### ArUco Marker Detection

Detecting and using ArUco fiducial markers for augmented reality and camera pose estimation.

```python { .api }
# Dictionary
def aruco.getPredefinedDictionary(name): ...

# Detection
class aruco.ArucoDetector:
    def __init__(self, dictionary, detectorParams=None): ...
    def detectMarkers(self, image, corners=None, ids=None, rejectedImgPoints=None): ...

# Drawing
def aruco.drawDetectedMarkers(image, corners, ids=None, borderColor=None): ...
def aruco.drawMarker(dictionary, id, sidePixels, img=None, borderBits=None): ...

# Pose estimation
def aruco.estimatePoseSingleMarkers(corners, markerLength, cameraMatrix, distCoeffs, rvecs=None, tvecs=None): ...
```

[ArUco Markers](./aruco.md)

## Types

### Core Data Structures

```python { .api }
class Mat:
    """
    Multi-dimensional dense array class - the primary data structure for images and matrices.
    In Python, Mat objects are represented as NumPy arrays.

    Images are stored with shape (height, width) for grayscale or (height, width, channels) for color.
    OpenCV uses BGR color order by default, not RGB.
    """
    pass

class UMat:
    """
    Unified memory array for transparent GPU acceleration via OpenCL.
    Provides the same interface as Mat but can execute operations on GPU when available.
    """
    pass

# Scalar type
"""
4-element vector used to pass pixel values. In Python bindings, scalars are represented as tuples.
For BGR images: (b, g, r) or (b, g, r, alpha)
For grayscale: (value,) or just value
Example: cv2.circle(img, (100, 100), 50, (255, 0, 0), 2)  # Blue circle
"""

# Point types
"""
Points are represented as tuples in Python bindings:
- Point (2D integer): (x, y)
- Point2f (2D float): (x, y)
- Point3 (3D integer): (x, y, z)
- Point3f (3D float): (x, y, z)

Examples:
  center = (100, 200)  # Point
  corner = (50.5, 75.3)  # Point2f
  vertex = (10, 20, 30)  # Point3
"""

# Size type
"""
Size of a 2D rectangle. In Python bindings, sizes are represented as tuples (width, height).
Example: img_resized = cv2.resize(img, (640, 480))  # Resize to 640x480
"""

# Rect type
"""
Rectangle defined by top-left corner and size. In Python bindings, rectangles are represented as tuples.
Format: (x, y, width, height)
Example: roi = (50, 100, 200, 150)  # Rectangle at (50,100) with 200x150 size
"""

class RotatedRect:
    """Rotated rectangle represented by center, size, and angle"""
    center: tuple  # (x, y) center coordinates
    size: tuple  # (width, height)
    angle: float  # rotation angle in degrees
    def __init__(self, center, size, angle): ...

# Range type
"""
Integer range [start, end) - includes start, excludes end.
In Python bindings, ranges are represented as tuples (start, end) or use Python slice notation.
Example: subarray = array[0:10] or with tuple (0, 10) in certain functions
"""

# TermCriteria type
"""
Termination criteria for iterative algorithms. In Python bindings, represented as a tuple.
Format: (type, maxCount, epsilon)
- type: cv2.TERM_CRITERIA_COUNT, cv2.TERM_CRITERIA_EPS, or combined with | operator
- maxCount: maximum number of iterations
- epsilon: required accuracy

Example: criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_COUNT, 30, 0.001)
"""

class KeyPoint:
    """Data structure for salient point detectors"""
    pt: tuple  # (x, y) coordinates of the keypoint
    size: float  # diameter of the meaningful keypoint neighborhood
    angle: float  # computed orientation of the keypoint (-1 if not applicable)
    response: float  # response by which the strongest keypoints have been selected
    octave: int  # octave (pyramid layer) from which the keypoint has been extracted
    class_id: int  # object class (if the keypoints need to be clustered by an object they belong to)

class DMatch:
    """Match between two keypoint descriptors"""
    queryIdx: int  # query descriptor index
    trainIdx: int  # train descriptor index
    imgIdx: int  # train image index
    distance: float  # distance between descriptors (lower is better)

# Random Number Generation
"""
Note: The cv2.RNG class is not directly available in Python bindings.
For random number generation, use NumPy's random module instead:
- np.random.uniform(a, b) - Generate uniform random numbers
- np.random.normal(mean, std) - Generate Gaussian random numbers
- np.random.randint(low, high) - Generate random integers

Example:
  import numpy as np
  random_values = np.random.uniform(0, 255, (100, 100, 3)).astype(np.uint8)
"""
```

### Common Constants

Color conversion codes (partial list):
```python { .api }
COLOR_BGR2GRAY: int
COLOR_BGR2RGB: int
COLOR_BGR2HSV: int
COLOR_BGR2LAB: int
COLOR_GRAY2BGR: int
COLOR_HSV2BGR: int
COLOR_LAB2BGR: int
```

Interpolation methods:
```python { .api }
INTER_NEAREST: int  # nearest neighbor interpolation
INTER_LINEAR: int  # bilinear interpolation
INTER_CUBIC: int  # bicubic interpolation
INTER_LANCZOS4: int  # Lanczos interpolation over 8x8 neighborhood
```

Threshold types:
```python { .api }
THRESH_BINARY: int
THRESH_BINARY_INV: int
THRESH_TRUNC: int
THRESH_TOZERO: int
THRESH_TOZERO_INV: int
THRESH_OTSU: int  # Otsu's algorithm
```

Data types:
```python { .api }
CV_8U: int   # 8-bit unsigned integer
CV_8S: int   # 8-bit signed integer
CV_16U: int  # 16-bit unsigned integer
CV_16S: int  # 16-bit signed integer
CV_32S: int  # 32-bit signed integer
CV_32F: int  # 32-bit floating point
CV_64F: int  # 64-bit floating point
```

Norm types:
```python { .api }
NORM_L1: int        # L1 norm (sum of absolute values)
NORM_L2: int        # L2 norm (Euclidean distance)
NORM_INF: int       # Infinity norm (maximum absolute value)
NORM_HAMMING: int   # Hamming distance for binary descriptors
NORM_HAMMING2: int  # Hamming distance with 2-bit precision
```

Comparison operators:
```python { .api }
CMP_EQ: int  # Equal (==)
CMP_GT: int  # Greater than (>)
CMP_GE: int  # Greater than or equal (>=)
CMP_LT: int  # Less than (<)
CMP_LE: int  # Less than or equal (<=)
CMP_NE: int  # Not equal (!=)
```

K-means clustering flags:
```python { .api }
KMEANS_RANDOM_CENTERS: int     # Random initial centers
KMEANS_PP_CENTERS: int         # K-means++ center initialization
KMEANS_USE_INITIAL_LABELS: int # Use user-provided initial labels
```

TermCriteria types:
```python { .api }
TermCriteria_COUNT: int   # Stop after maxCount iterations
TermCriteria_EPS: int     # Stop when desired accuracy (epsilon) is reached
TermCriteria_MAX_ITER: int  # Same as TermCriteria_COUNT
```

## Error Handling

```python { .api }
class error(Exception):
    """OpenCV error exception"""
    pass
```

OpenCV raises `cv2.error` exceptions when operations fail. Common scenarios include:
- Invalid image format or dimensions
- File not found or cannot be read
- Unsupported operation or invalid parameters
- Insufficient memory

## Platform Notes

### Headless vs GUI Packages

- **Standard packages** (`opencv-python`, `opencv-contrib-python`): Include GUI functionality via highgui module
- **Headless packages** (`opencv-python-headless`, `opencv-contrib-python-headless`): No GUI dependencies, smaller Docker images

Headless packages do not support:
- `cv2.imshow()`, `cv2.namedWindow()`, and other highgui functions
- Interactive windows, trackbars, and mouse callbacks
- Use headless packages for servers, Docker containers, or when using alternative GUI frameworks

### Data Files

Haar cascade XML files for object detection are included in all packages:

```python
import cv2
import os

# Access Haar cascades directory
cascades_path = cv2.data.haarcascades

# Load a cascade classifier
face_cascade = cv2.CascadeClassifier(
    os.path.join(cascades_path, 'haarcascade_frontalface_default.xml')
)
```

## Additional Resources

- Official OpenCV documentation: https://docs.opencv.org/4.x/
- OpenCV-Python tutorials: https://docs.opencv.org/4.x/d6/d00/tutorial_py_root.html
- OpenCV GitHub repository: https://github.com/opencv/opencv
- OpenCV-Python package repository: https://github.com/opencv/opencv-python
