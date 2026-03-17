# Video Analysis and Object Tracking

OpenCV provides powerful capabilities for analyzing motion in video sequences, tracking objects across frames, and modeling temporal dynamics. These tools enable applications ranging from surveillance and activity recognition to augmented reality and autonomous navigation.

## Capabilities

### Optical Flow

Optical flow algorithms estimate the motion of pixels or features between consecutive frames, providing dense or sparse motion vectors that describe scene dynamics.

#### Lucas-Kanade Sparse Optical Flow

```python { .api }
next_pts, status, err = cv2.calcOpticalFlowPyrLK(
    prevImg, nextImg, prevPts, nextPts,
    winSize=None, maxLevel=None, criteria=None,
    flags=None, minEigThreshold=None
)
```

Calculates sparse optical flow using the iterative Lucas-Kanade method with pyramids. Tracks a sparse set of feature points from one frame to the next.

**Parameters:**
- `prevImg`: First 8-bit input image (grayscale)
- `nextImg`: Second input image of the same size and type
- `prevPts`: Vector of 2D points for which flow needs to be found (Nx1x2 or Nx2 array)
- `nextPts`: Output vector of 2D points (with single-precision floating-point coordinates)
- `winSize`: Size of the search window at each pyramid level (default: (21, 21))
- `maxLevel`: 0-based maximal pyramid level number (default: 3)
- `criteria`: Termination criteria for iterative search (default: 30 iterations or 0.01 epsilon)
- `flags`: Operation flags (e.g., cv2.OPTFLOW_USE_INITIAL_FLOW, cv2.OPTFLOW_LK_GET_MIN_EIGENVALS)
- `minEigThreshold`: Minimum eigenvalue threshold for feature selection (default: 1e-4)

**Returns:**
- `next_pts`: Calculated new positions of input features in second image
- `status`: Status vector (1 if flow found, 0 otherwise)
- `err`: Error vector containing the difference between patches around original and moved points

**Example:**
```python
# Detect good features to track
prev_gray = cv2.cvtColor(prev_frame, cv2.COLOR_BGR2GRAY)
prev_pts = cv2.goodFeaturesToTrack(prev_gray, maxCorners=100, qualityLevel=0.3, minDistance=7)

# Calculate optical flow
next_gray = cv2.cvtColor(next_frame, cv2.COLOR_BGR2GRAY)
next_pts, status, err = cv2.calcOpticalFlowPyrLK(prev_gray, next_gray, prev_pts, None)

# Select good points
good_new = next_pts[status == 1]
good_old = prev_pts[status == 1]
```

#### Farneback Dense Optical Flow

```python { .api }
flow = cv2.calcOpticalFlowFarneback(
    prev, next, flow, pyr_scale, levels, winsize,
    iterations, poly_n, poly_sigma, flags
)
```

Computes dense optical flow using the Gunnar Farneback's algorithm. Produces a flow field for every pixel in the image.

**Parameters:**
- `prev`: First 8-bit single-channel input image
- `next`: Second input image of the same size and type
- `flow`: Computed flow image (same size as prev, 2-channel float)
- `pyr_scale`: Pyramid scale (< 1), typical value: 0.5 (each layer is half the size)
- `levels`: Number of pyramid layers including the initial image
- `winsize`: Averaging window size (larger = more robust to noise but more blurred)
- `iterations`: Number of iterations at each pyramid level
- `poly_n`: Size of pixel neighborhood used for polynomial expansion (typically 5 or 7)
- `poly_sigma`: Standard deviation for Gaussian used to smooth derivatives (typically 1.1 or 1.5)
- `flags`: Operation flags (cv2.OPTFLOW_USE_INITIAL_FLOW, cv2.OPTFLOW_FARNEBACK_GAUSSIAN)

**Returns:**
- `flow`: 2-channel array containing horizontal (dx) and vertical (dy) flow vectors

**Example:**
```python
prev_gray = cv2.cvtColor(prev_frame, cv2.COLOR_BGR2GRAY)
next_gray = cv2.cvtColor(next_frame, cv2.COLOR_BGR2GRAY)

flow = cv2.calcOpticalFlowFarneback(
    prev_gray, next_gray, None,
    pyr_scale=0.5, levels=3, winsize=15,
    iterations=3, poly_n=5, poly_sigma=1.2, flags=0
)

# Visualize flow with HSV color encoding
mag, ang = cv2.cartToPolar(flow[..., 0], flow[..., 1])
hsv = np.zeros((flow.shape[0], flow.shape[1], 3), dtype=np.uint8)
hsv[..., 0] = ang * 180 / np.pi / 2
hsv[..., 1] = 255
hsv[..., 2] = cv2.normalize(mag, None, 0, 255, cv2.NORM_MINMAX)
flow_rgb = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)
```

#### Optical Flow Pyramid

```python { .api }
pyramid = cv2.buildOpticalFlowPyramid(
    img, winSize, maxLevel,
    withDerivatives=True, pyrBorder=None,
    derivBorder=None, tryReuseInputImage=True
)
```

Constructs a pyramid which can be used as input for subsequent optical flow calculations. Pre-building pyramids improves performance when tracking multiple features.

**Parameters:**
- `img`: 8-bit input image
- `winSize`: Window size for optical flow
- `maxLevel`: 0-based maximal pyramid level number
- `withDerivatives`: Flag to specify whether to precompute gradients
- `pyrBorder`: Border mode for pyramid layers (default: cv2.BORDER_REFLECT_101)
- `derivBorder`: Border mode for derivatives (default: cv2.BORDER_CONSTANT)
- `tryReuseInputImage`: Optimization flag to reuse input image

**Returns:**
- `pyramid`: Output pyramid list

**Example:**
```python
gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
pyramid = cv2.buildOpticalFlowPyramid(
    gray, winSize=(21, 21), maxLevel=3,
    withDerivatives=True
)
```

#### Optical Flow File I/O

```python { .api }
flow = cv2.readOpticalFlow(path)
```

Read optical flow from a .flo file.

**Parameters:**
- `path` (str): Path to the file to be loaded

**Returns:**
- `flow`: Optical flow field as CV_32FC2 matrix (2-channel float). First channel corresponds to the flow in the horizontal direction (u), second - vertical (v)

**Example:**
```python
# Read optical flow from file
flow = cv2.readOpticalFlow('flow.flo')
print(f'Flow shape: {flow.shape}')  # (height, width, 2)

# Extract horizontal and vertical components
flow_x = flow[..., 0]  # u component
flow_y = flow[..., 1]  # v component
```

---

```python { .api }
success = cv2.writeOpticalFlow(path, flow)
```

Write optical flow to a .flo file on disk.

**Parameters:**
- `path` (str): Path to the file to be written
- `flow`: Flow field to be stored. Must be CV_32FC2 (2-channel float). First channel corresponds to the flow in the horizontal direction (u), second - vertical (v)

**Returns:**
- `success` (bool): True on success, False otherwise

**Example:**
```python
# Calculate optical flow
flow = cv2.calcOpticalFlowFarneback(prev_gray, next_gray, None, 0.5, 3, 15, 3, 5, 1.2, 0)

# Save to file
success = cv2.writeOpticalFlow('flow.flo', flow)
if success:
    print('Flow saved successfully')

# Later, read it back
loaded_flow = cv2.readOpticalFlow('flow.flo')
```

### Background Subtraction

Background subtraction algorithms model the static background and identify moving foreground objects, essential for surveillance and object detection in static camera scenarios.

#### MOG2 Background Subtractor

```python { .api }
cv2.BackgroundSubtractorMOG2
```

Gaussian Mixture-based Background/Foreground Segmentation Algorithm. An improved adaptive algorithm that models each pixel as a mixture of Gaussians and selects appropriate components to represent the background.

**Key Methods:**
- `apply(image, fgmask=None, learningRate=-1)`: Compute foreground mask
- `getBackgroundImage(backgroundImage=None)`: Compute background image
- `setHistory(history)`: Set number of frames in history
- `setVarThreshold(threshold)`: Set variance threshold for pixel-model matching
- `setDetectShadows(detect)`: Enable/disable shadow detection

**Example:**
```python
bg_subtractor = cv2.createBackgroundSubtractorMOG2(
    history=500, varThreshold=16, detectShadows=True
)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    fg_mask = bg_subtractor.apply(frame)

    # Optional: get background image
    bg_image = bg_subtractor.getBackgroundImage()
```

#### KNN Background Subtractor

```python { .api }
cv2.BackgroundSubtractorKNN
```

K-nearest neighbors based Background/Foreground Segmentation Algorithm. Uses k-nearest neighbors to classify pixels as background or foreground.

**Key Methods:**
- `apply(image, fgmask=None, learningRate=-1)`: Compute foreground mask
- `getBackgroundImage(backgroundImage=None)`: Compute background image
- `setHistory(history)`: Set number of frames in history
- `setDist2Threshold(threshold)`: Set threshold on squared distance
- `setDetectShadows(detect)`: Enable/disable shadow detection

**Example:**
```python
bg_subtractor = cv2.createBackgroundSubtractorKNN(
    history=500, dist2Threshold=400.0, detectShadows=True
)

fg_mask = bg_subtractor.apply(frame, learningRate=0.01)
```

#### Creating Background Subtractors

```python { .api }
bg_subtractor = cv2.createBackgroundSubtractorMOG2(
    history=500, varThreshold=16, detectShadows=True
)
```

Creates a MOG2 background subtractor.

**Parameters:**
- `history`: Length of history (number of frames)
- `varThreshold`: Threshold on squared Mahalanobis distance between pixel and model
- `detectShadows`: If True, algorithm detects and marks shadows (slower but more accurate)

**Returns:**
- Background subtractor object

```python { .api }
bg_subtractor = cv2.createBackgroundSubtractorKNN(
    history=500, dist2Threshold=400.0, detectShadows=True
)
```

Creates a KNN background subtractor.

**Parameters:**
- `history`: Length of history
- `dist2Threshold`: Threshold on squared distance between pixel and sample
- `detectShadows`: If True, algorithm detects and marks shadows

**Returns:**
- Background subtractor object

**Comparison Example:**
```python
# MOG2 - better for complex scenarios, detects shadows
mog2 = cv2.createBackgroundSubtractorMOG2(history=500, varThreshold=16, detectShadows=True)

# KNN - faster, good for simpler scenarios
knn = cv2.createBackgroundSubtractorKNN(history=500, dist2Threshold=400, detectShadows=False)

# Apply both and compare
fg_mask_mog2 = mog2.apply(frame)
fg_mask_knn = knn.apply(frame)
```

### Mean Shift Tracking

Mean shift algorithms iteratively move a search window toward regions of higher density, useful for tracking objects based on color histograms or appearance models.

#### Mean Shift

```python { .api }
retval, window = cv2.meanShift(
    probImage, window, criteria
)
```

Finds the object center using mean shift algorithm. The algorithm shifts a window to the location with maximum probability density.

**Parameters:**
- `probImage`: Back projection of the object histogram (probability map)
- `window`: Initial search window (x, y, width, height)
- `criteria`: Stop criteria (type, max iterations, epsilon)

**Returns:**
- `retval`: Number of iterations performed
- `window`: Converged window position (x, y, width, height)

**Example:**
```python
# Setup the initial tracking window
x, y, w, h = 300, 200, 100, 150
track_window = (x, y, w, h)

# Calculate histogram of ROI
roi = frame[y:y+h, x:x+w]
hsv_roi = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)
mask = cv2.inRange(hsv_roi, np.array((0., 60., 32.)), np.array((180., 255., 255.)))
roi_hist = cv2.calcHist([hsv_roi], [0], mask, [180], [0, 180])
cv2.normalize(roi_hist, roi_hist, 0, 255, cv2.NORM_MINMAX)

# Tracking loop
while True:
    ret, frame = cap.read()
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    dst = cv2.calcBackProject([hsv], [0], roi_hist, [0, 180], 1)

    # Apply meanshift
    ret, track_window = cv2.meanShift(dst, track_window,
                                      (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 1))

    x, y, w, h = track_window
    cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
```

#### CamShift (Continuously Adaptive Mean Shift)

```python { .api }
rotated_rect, window = cv2.CamShift(
    probImage, window, criteria
)
```

Continuously Adaptive Mean Shift algorithm. An extension of mean shift that adapts the size and orientation of the search window based on the zeroth moment.

**Parameters:**
- `probImage`: Back projection of the object histogram
- `window`: Initial search window (x, y, width, height)
- `criteria`: Stop criteria for iterative algorithm

**Returns:**
- `rotated_rect`: Rotated rectangle containing position, size, and angle ((x, y), (width, height), angle)
- `window`: Converged window position (x, y, width, height)

**Example:**
```python
# Similar setup as meanShift
track_window = (x, y, w, h)

# Tracking loop
while True:
    ret, frame = cap.read()
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    dst = cv2.calcBackProject([hsv], [0], roi_hist, [0, 180], 1)

    # Apply CamShift
    ret, track_window = cv2.CamShift(dst, track_window,
                                     (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 1))

    # Draw rotated rectangle
    pts = cv2.boxPoints(ret)
    pts = np.int0(pts)
    cv2.polylines(frame, [pts], True, (0, 255, 0), 2)
```

### Object Tracking

OpenCV provides multiple tracking algorithms with different trade-offs between speed and accuracy. Modern trackers can handle occlusions, scale changes, and appearance variations.

#### Tracker Base Class

```python { .api }
cv2.Tracker
```

Base class for visual object tracking algorithms (legacy API). Provides a common interface for all tracker implementations.

**Common Methods:**
- `init(image, boundingBox)`: Initialize tracker with image and bounding box
- `update(image)`: Update tracker state with new frame
- `empty()`: Check if tracker is empty
- `clear()`: Clear internal state

#### DaSiamRPN Tracker

```python { .api }
cv2.TrackerDaSiamRPN
```

Distractor-aware Siamese Region Proposal Network tracker. State-of-the-art deep learning tracker with high accuracy, particularly robust to distractors and appearance changes.

**Creation:**
```python
tracker = cv2.TrackerDaSiamRPN_create()
```

**Example:**
```python
# Initialize tracker
tracker = cv2.TrackerDaSiamRPN_create()
bbox = cv2.selectROI('Select Object', frame, fromCenter=False)
tracker.init(frame, bbox)

# Tracking loop
while True:
    ret, frame = cap.read()
    success, bbox = tracker.update(frame)

    if success:
        x, y, w, h = [int(v) for v in bbox]
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
```

#### MIL Tracker

```python { .api }
cv2.TrackerMIL
```

Multiple Instance Learning tracker. Uses an online learning approach that updates the appearance model during tracking. Good balance between accuracy and speed.

**Creation:**
```python
tracker = cv2.TrackerMIL_create()
```

**Characteristics:**
- Good tracking performance
- Handles partial occlusions well
- Moderate computational cost
- Suitable for real-time applications

#### KCF Tracker

```python { .api }
cv2.TrackerKCF
```

Kernelized Correlation Filters tracker. Fast and efficient tracker using correlation filters in Fourier domain. Good for objects with limited appearance variation.

**Creation:**
```python
tracker = cv2.TrackerKCF_create()
```

**Characteristics:**
- Very fast
- Good accuracy for rigid objects
- Struggles with fast motion and scale changes
- Excellent for real-time tracking

#### CSRT Tracker

```python { .api }
cv2.TrackerCSRT
```

Discriminative Correlation Filter tracker with Channel and Spatial Reliability (CSRT). More accurate than KCF but slower, uses spatial reliability maps.

**Creation:**
```python
tracker = cv2.TrackerCSRT_create()
```

**Characteristics:**
- High accuracy
- Handles non-rectangular objects
- Slower than KCF
- Good for complex objects

#### GOTURN Tracker

```python { .api }
cv2.TrackerGOTURN
```

Generic Object Tracking Using Regression Networks. Deep learning-based tracker trained offline on large datasets. Requires Caffe model files.

**Creation:**
```python
tracker = cv2.TrackerGOTURN_create()
```

**Characteristics:**
- Deep learning-based
- Very robust to appearance changes
- Requires model files
- Faster than DaSiamRPN

#### Multi-Tracker Example

```python
# Create multiple trackers for different objects
trackers = cv2.MultiTracker_create()

# Add trackers for each object
for bbox in bboxes:
    tracker = cv2.TrackerKCF_create()
    trackers.add(tracker, frame, bbox)

# Update all trackers
while True:
    ret, frame = cap.read()
    success, boxes = trackers.update(frame)

    for i, box in enumerate(boxes):
        x, y, w, h = [int(v) for v in box]
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
```

### Kalman Filter

The Kalman filter provides optimal state estimation for linear dynamic systems, widely used for predicting object positions and reducing measurement noise in tracking applications.

```python { .api }
cv2.KalmanFilter(dynamParams, measureParams, controlParams=0, type=CV_32F)
```

Kalman filter implementation for state estimation and prediction. Models system dynamics and measurement process to optimally estimate hidden states.

**Parameters:**
- `dynamParams`: Dimensionality of the state vector
- `measureParams`: Dimensionality of the measurement vector
- `controlParams`: Dimensionality of the control vector (default: 0)
- `type`: Data type (CV_32F or CV_64F)

**Key Attributes:**
- `statePre`: Predicted state (x'(k))
- `statePost`: Corrected state (x(k))
- `transitionMatrix`: State transition matrix (A)
- `measurementMatrix`: Measurement matrix (H)
- `processNoiseCov`: Process noise covariance matrix (Q)
- `measurementNoiseCov`: Measurement noise covariance matrix (R)
- `errorCovPre`: Priori error estimate covariance matrix (P'(k))
- `errorCovPost`: Posteriori error estimate covariance matrix (P(k))
- `gain`: Kalman gain matrix (K(k))

**Key Methods:**
- `predict(control=None)`: Computes predicted state
- `correct(measurement)`: Updates state with measurement

**Example - Tracking a Moving Point:**
```python
# Create Kalman filter for 2D point tracking
# State: [x, y, dx, dy], Measurement: [x, y]
kalman = cv2.KalmanFilter(4, 2)

# Transition matrix (constant velocity model)
kalman.transitionMatrix = np.array([
    [1, 0, 1, 0],  # x = x + dx
    [0, 1, 0, 1],  # y = y + dy
    [0, 0, 1, 0],  # dx = dx
    [0, 0, 0, 1]   # dy = dy
], dtype=np.float32)

# Measurement matrix
kalman.measurementMatrix = np.array([
    [1, 0, 0, 0],
    [0, 1, 0, 0]
], dtype=np.float32)

# Process and measurement noise
kalman.processNoiseCov = np.eye(4, dtype=np.float32) * 0.03
kalman.measurementNoiseCov = np.eye(2, dtype=np.float32) * 0.1

# Initialize state
kalman.statePost = np.array([[x], [y], [0], [0]], dtype=np.float32)

# Tracking loop
while True:
    # Predict
    prediction = kalman.predict()
    pred_x, pred_y = int(prediction[0]), int(prediction[1])

    # Get measurement (e.g., from detection)
    measurement = np.array([[measured_x], [measured_y]], dtype=np.float32)

    # Update
    kalman.correct(measurement)

    # Use prediction for display
    cv2.circle(frame, (pred_x, pred_y), 5, (0, 255, 0), -1)
```

**Example - Tracking with Missing Measurements:**
```python
# When no measurement is available
if object_detected:
    measurement = np.array([[x], [y]], dtype=np.float32)
    kalman.correct(measurement)

# Always predict (even without measurement)
prediction = kalman.predict()
estimated_position = (int(prediction[0]), int(prediction[1]))
```

### Motion Analysis

Advanced motion analysis tools for estimating geometric transformations and aligning images based on motion models.

#### Enhanced Correlation Coefficient (ECC) Transform

```python { .api }
retval, warp_matrix = cv2.findTransformECC(
    templateImage, inputImage,
    warpMatrix, motionType,
    criteria=None, inputMask=None,
    gaussFiltSize=5
)
```

Finds the geometric transformation between two images by maximizing the Enhanced Correlation Coefficient. Useful for image alignment and registration.

**Parameters:**
- `templateImage`: Reference image (single-channel 8-bit or 32-bit float)
- `inputImage`: Image to align (same type and size as template)
- `warpMatrix`: Initial transformation matrix (2x3 for affine/euclidean, 3x3 for homography)
- `motionType`: Type of transformation (MOTION_TRANSLATION, MOTION_EUCLIDEAN, MOTION_AFFINE, MOTION_HOMOGRAPHY)
- `criteria`: Termination criteria (max iterations and epsilon)
- `inputMask`: Optional mask for template image
- `gaussFiltSize`: Size of Gaussian filter for smoothing (1 = no smoothing)

**Returns:**
- `retval`: Final correlation coefficient
- `warp_matrix`: Estimated transformation matrix

**Motion Types:**
- `cv2.MOTION_TRANSLATION`: Only translation (2 parameters)
- `cv2.MOTION_EUCLIDEAN`: Rotation + translation (3 parameters)
- `cv2.MOTION_AFFINE`: Affine transformation (6 parameters)
- `cv2.MOTION_HOMOGRAPHY`: Perspective transformation (8 parameters)

**Example - Image Stabilization:**
```python
# Reference frame
prev_gray = cv2.cvtColor(prev_frame, cv2.COLOR_BGR2GRAY)

# Initialize transformation matrix
warp_matrix = np.eye(2, 3, dtype=np.float32)

# Current frame
curr_gray = cv2.cvtColor(curr_frame, cv2.COLOR_BGR2GRAY)

# Define termination criteria
criteria = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 50, 0.001)

# Find transformation
try:
    cc, warp_matrix = cv2.findTransformECC(
        prev_gray, curr_gray, warp_matrix,
        cv2.MOTION_EUCLIDEAN, criteria
    )

    # Apply transformation to stabilize
    stabilized = cv2.warpAffine(
        curr_frame, warp_matrix,
        (curr_frame.shape[1], curr_frame.shape[0]),
        flags=cv2.INTER_LINEAR + cv2.WARP_INVERSE_MAP
    )
except cv2.error:
    print("ECC optimization failed")
```

**Example - Video Alignment:**
```python
# Align sequence of frames to first frame
first_frame = cv2.cvtColor(frames[0], cv2.COLOR_BGR2GRAY)
aligned_frames = [frames[0]]

for frame in frames[1:]:
    curr_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Use affine transformation for better alignment
    warp_matrix = np.eye(2, 3, dtype=np.float32)

    try:
        _, warp_matrix = cv2.findTransformECC(
            first_frame, curr_gray, warp_matrix,
            cv2.MOTION_AFFINE,
            criteria=(cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 100, 1e-5)
        )

        aligned = cv2.warpAffine(
            frame, warp_matrix,
            (frame.shape[1], frame.shape[0])
        )
        aligned_frames.append(aligned)
    except:
        aligned_frames.append(frame)  # Use original if alignment fails
```

## See Also

- [Image Processing](image-processing.md) - Filtering and transformations used in video preprocessing
- [Feature Detection](feature-detection.md) - Corner and feature detection for tracking
- [Object Detection](object-detection.md) - Detecting objects in video frames
- [Camera Calibration](camera-calibration.md) - Camera calibration for accurate motion estimation
