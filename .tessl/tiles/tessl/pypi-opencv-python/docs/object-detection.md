# Object Detection

OpenCV provides robust tools for detecting and recognizing objects in images and videos. The object detection module includes traditional computer vision methods like Haar cascades and HOG descriptors, as well as modern deep learning-based detectors. These capabilities enable applications such as face detection, pedestrian detection, QR code scanning, and custom object recognition.

## Capabilities

### Cascade Classifiers

Cascade classifiers use a machine learning approach based on Haar features or LBP features to detect objects. They are fast and efficient for real-time detection tasks.

**CascadeClassifier Class**

```python { .api }
cv2.CascadeClassifier(filename=None)
```

Creates a cascade classifier object for object detection. If `filename` is provided, loads the cascade from the specified XML file.

**Loading a Cascade**

```python { .api }
classifier.load(filename)
```

Loads a cascade classifier from an XML file. Returns `True` if successful, `False` otherwise.

**Detecting Objects**

```python { .api }
objects = classifier.detectMultiScale(
    image,
    scaleFactor=1.1,
    minNeighbors=3,
    flags=0,
    minSize=(0, 0),
    maxSize=(0, 0)
)
```

Detects objects of different sizes in the input image. Returns a list of rectangles where objects were found, as `(x, y, width, height)` tuples.

- `image`: Input image (grayscale recommended for better performance)
- `scaleFactor`: Parameter specifying how much the image size is reduced at each scale (e.g., 1.1 means 10% reduction)
- `minNeighbors`: Specifies how many neighbors each candidate rectangle should have to retain it (higher value results in fewer detections but higher quality)
- `flags`: Legacy parameter from old API, typically set to 0
- `minSize`: Minimum object size in pixels
- `maxSize`: Maximum object size in pixels (0 means no limit)

**Detecting with Level Information**

```python { .api }
objects, numDetections = classifier.detectMultiScale2(
    image,
    scaleFactor=1.1,
    minNeighbors=3,
    flags=0,
    minSize=(0, 0),
    maxSize=(0, 0)
)
```

Similar to `detectMultiScale()`, but also returns the number of neighbor rectangles for each detection, which can be used as a confidence measure.

**Detecting with Weights**

```python { .api }
objects, rejectLevels, levelWeights = classifier.detectMultiScale3(
    image,
    scaleFactor=1.1,
    minNeighbors=3,
    flags=0,
    minSize=(0, 0),
    maxSize=(0, 0),
    outputRejectLevels=True
)
```

Extended detection that returns reject levels and level weights for each detection, providing more detailed information about detection confidence.

**Example: Face Detection**

```python { .api }
import cv2

# Load the cascade classifier
face_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
)

# Load image
img = cv2.imread('image.jpg')
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# Detect faces
faces = face_cascade.detectMultiScale(
    gray,
    scaleFactor=1.1,
    minNeighbors=5,
    minSize=(30, 30)
)

# Draw rectangles around faces
for (x, y, w, h) in faces:
    cv2.rectangle(img, (x, y), (x+w, y+h), (255, 0, 0), 2)
```

### HOG Descriptor

Histogram of Oriented Gradients (HOG) is a feature descriptor used for object detection, particularly effective for pedestrian detection.

**HOGDescriptor Class**

```python
hog = cv2.HOGDescriptor()
```

Creates a HOG descriptor and detector object with default parameters.

**Computing HOG Descriptors**

```python { .api }
descriptors = hog.compute(
    img,
    winStride=(8, 8),
    padding=(0, 0),
    locations=None
)
```

Computes HOG descriptors for the image.

- `img`: Input image
- `winStride`: Step size for sliding window (in pixels)
- `padding`: Padding around the image
- `locations`: Optional list of detection locations

Returns a numpy array of HOG descriptors.

**Setting the SVM Detector**

```python { .api }
hog.setSVMDetector(detector)
```

Sets the SVM (Support Vector Machine) detector coefficients for object detection. OpenCV provides pre-trained detectors.

**Getting Default People Detector**

```python { .api }
detector = cv2.HOGDescriptor_getDefaultPeopleDetector()
```

Returns the default people/pedestrian detector coefficients trained on the INRIA person dataset.

**Detecting Objects with HOG**

```python { .api }
found, weights = hog.detectMultiScale(
    img,
    hitThreshold=0,
    winStride=(8, 8),
    padding=(0, 0),
    scale=1.05,
    finalThreshold=2.0,
    useMeanshiftGrouping=False
)
```

Detects objects (e.g., people) in the image using the HOG descriptor and SVM classifier.

- `img`: Input image
- `hitThreshold`: Threshold for detection decision (lower values increase detections but also false positives)
- `winStride`: Step size for sliding window
- `padding`: Padding around the image
- `scale`: Scale factor for image pyramid
- `finalThreshold`: Threshold for the final detection grouping
- `useMeanshiftGrouping`: Use mean-shift grouping instead of NMS

Returns detected object rectangles and their weights.

**Example: Pedestrian Detection**

```python { .api }
import cv2

# Initialize HOG descriptor with default people detector
hog = cv2.HOGDescriptor()
hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())

# Load image
img = cv2.imread('street.jpg')

# Detect people
found, weights = hog.detectMultiScale(
    img,
    winStride=(8, 8),
    padding=(4, 4),
    scale=1.05
)

# Draw rectangles around detected people
for (x, y, w, h) in found:
    cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 2)
```

### QR Code Detection

OpenCV provides dedicated tools for detecting and decoding QR codes in images.

**QRCodeDetector Class**

```python
detector = cv2.QRCodeDetector()
```

Creates a QR code detector object.

**Detecting QR Codes**

```python { .api }
retval, points = detector.detect(img)
```

Detects a QR code in the image. Returns `True` if found, and the corner points of the QR code.

**Decoding QR Codes**

```python { .api }
data, points, straight_qrcode = detector.decode(img, points)
```

Decodes a QR code given its corner points. Returns the decoded string, corner points, and the rectified QR code image.

**Detecting and Decoding in One Call**

```python { .api }
data, points, straight_qrcode = detector.detectAndDecode(img)
```

Detects and decodes a QR code in a single operation. Returns:
- `data`: Decoded string from QR code (empty if no QR code found)
- `points`: Corner points of the QR code
- `straight_qrcode`: Rectified QR code image

**Detecting Multiple QR Codes**

```python { .api }
retval, points = detector.detectMulti(img)
```

Detects multiple QR codes in the image. Returns `True` if any QR codes are found, and a list of corner points for each detected QR code.

**Decoding Multiple QR Codes**

```python { .api }
retval, decoded_info, points, straight_qrcodes = detector.decodeMulti(img, points)
```

Decodes multiple QR codes given their corner points. Returns:
- `retval`: `True` if successful
- `decoded_info`: List of decoded strings
- `points`: List of corner points for each QR code
- `straight_qrcodes`: List of rectified QR code images

**Example: QR Code Detection and Decoding**

```python { .api }
import cv2

# Create QR code detector
detector = cv2.QRCodeDetector()

# Load image
img = cv2.imread('qrcode.jpg')

# Detect and decode
data, points, straight_qrcode = detector.detectAndDecode(img)

if data:
    print(f"QR Code detected: {data}")

    # Draw boundary around QR code
    if points is not None:
        points = points.reshape(-1, 2).astype(int)
        for i in range(4):
            cv2.line(img, tuple(points[i]), tuple(points[(i+1)%4]), (0, 255, 0), 3)
else:
    print("No QR Code detected")
```

### QRCodeDetectorAruco

```python
detector = cv2.QRCodeDetectorAruco()
```

An enhanced QR code detector that uses ArUco markers for improved detection. Provides the same interface as `QRCodeDetector` but with better robustness in challenging conditions.

### Face Detection (DNN-based)

Modern face detection using deep neural networks provides more accurate results than traditional cascade classifiers.

**FaceDetectorYN Class**

```python { .api }
detector = cv2.FaceDetectorYN.create(
    model,
    config,
    input_size,
    score_threshold=0.9,
    nms_threshold=0.3,
    top_k=5000,
    backend_id=0,
    target_id=0
)
```

Creates a YuNet face detector. YuNet is a lightweight and accurate face detection model.

- `model`: Path to the ONNX model file
- `config`: Path to the config file (can be empty string)
- `input_size`: Input size for the neural network as (width, height)
- `score_threshold`: Confidence threshold for face detection
- `nms_threshold`: Non-maximum suppression threshold
- `top_k`: Keep top K detections before NMS
- `backend_id`: Backend identifier (e.g., default, OpenCV, CUDA)
- `target_id`: Target device identifier (e.g., CPU, GPU)

**Detecting Faces**

```python { .api }
faces = detector.detect(img)
```

Detects faces in the input image. Returns a tuple containing:
- Return value (1 if faces detected, 0 otherwise)
- Face detections as numpy array where each row contains: [x, y, w, h, x_re, y_re, x_le, y_le, x_nt, y_nt, x_rcm, y_rcm, x_lcm, y_lcm, confidence]
  - First 4 values: Bounding box (x, y, width, height)
  - Next values: Facial landmarks (right eye, left eye, nose tip, right corner of mouth, left corner of mouth)
  - Last value: Detection confidence score

### Face Recognition

**FaceRecognizerSF Class**

```python { .api }
recognizer = cv2.FaceRecognizerSF.create(
    model,
    config,
    backend_id=0,
    target_id=0
)
```

Creates a face recognition model based on SFace. Used to extract face features and compare faces for recognition tasks.

**Extracting Face Features**

```python { .api }
feature = recognizer.feature(aligned_face)
```

Extracts a feature vector from an aligned face image. The feature vector can be used for face comparison and recognition.

**Comparing Faces**

```python { .api }
score = recognizer.match(
    face_feature1,
    face_feature2,
    dis_type=cv2.FaceRecognizerSF_FR_COSINE
)
```

Computes the similarity score between two face features. Higher scores indicate more similar faces.

Distance types:
- `cv2.FaceRecognizerSF_FR_COSINE`: Cosine distance
- `cv2.FaceRecognizerSF_FR_NORM_L2`: L2 norm distance

## Haar Cascade Data Files

OpenCV includes pre-trained Haar cascade classifiers for various object detection tasks. These XML files are distributed with the opencv-python package and can be accessed via the `cv2.data.haarcascades` path.

**Accessing Haar Cascade Files**

```python { .api }
import cv2

# Get the path to the haarcascades directory
cascade_path = cv2.data.haarcascades

# Load a specific cascade
face_cascade = cv2.CascadeClassifier(cascade_path + 'haarcascade_frontalface_default.xml')
```

**Available Cascade Files**

OpenCV provides the following pre-trained Haar cascade classifiers:

**Face Detection:**
- `haarcascade_frontalface_default.xml` - Default frontal face detector (most commonly used)
- `haarcascade_frontalface_alt.xml` - Alternative frontal face detector
- `haarcascade_frontalface_alt2.xml` - Another alternative frontal face detector
- `haarcascade_frontalface_alt_tree.xml` - Tree-based frontal face detector
- `haarcascade_profileface.xml` - Profile (side view) face detector

**Eye Detection:**
- `haarcascade_eye.xml` - Generic eye detector
- `haarcascade_eye_tree_eyeglasses.xml` - Eye detector that works with eyeglasses
- `haarcascade_lefteye_2splits.xml` - Left eye detector
- `haarcascade_righteye_2splits.xml` - Right eye detector

**Facial Features:**
- `haarcascade_smile.xml` - Smile detector

**Body Detection:**
- `haarcascade_fullbody.xml` - Full body detector
- `haarcascade_upperbody.xml` - Upper body detector
- `haarcascade_lowerbody.xml` - Lower body detector

**Animal Detection:**
- `haarcascade_frontalcatface.xml` - Cat face detector
- `haarcascade_frontalcatface_extended.xml` - Extended cat face detector

**Other Objects:**
- `haarcascade_licence_plate_rus_16stages.xml` - Russian license plate detector

**Example: Loading Multiple Cascades**

```python
import cv2

cascade_path = cv2.data.haarcascades

# Load face and eye cascades
face_cascade = cv2.CascadeClassifier(
    cascade_path + 'haarcascade_frontalface_default.xml'
)
eye_cascade = cv2.CascadeClassifier(
    cascade_path + 'haarcascade_eye.xml'
)
smile_cascade = cv2.CascadeClassifier(
    cascade_path + 'haarcascade_smile.xml'
)

# Load image and convert to grayscale
img = cv2.imread('people.jpg')
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# Detect faces
faces = face_cascade.detectMultiScale(gray, 1.3, 5)

# For each face, detect eyes and smile
for (x, y, w, h) in faces:
    cv2.rectangle(img, (x, y), (x+w, y+h), (255, 0, 0), 2)
    roi_gray = gray[y:y+h, x:x+w]
    roi_color = img[y:y+h, x:x+w]

    # Detect eyes in face region
    eyes = eye_cascade.detectMultiScale(roi_gray)
    for (ex, ey, ew, eh) in eyes:
        cv2.rectangle(roi_color, (ex, ey), (ex+ew, ey+eh), (0, 255, 0), 2)

    # Detect smile in face region
    smiles = smile_cascade.detectMultiScale(roi_gray, 1.8, 20)
    for (sx, sy, sw, sh) in smiles:
        cv2.rectangle(roi_color, (sx, sy), (sx+sw, sy+sh), (0, 0, 255), 2)
```

**Performance Tips for Cascade Classifiers:**

1. **Convert to Grayscale**: Cascade classifiers work faster on grayscale images
2. **Adjust scaleFactor**: Smaller values (e.g., 1.05) are more thorough but slower; larger values (e.g., 1.3) are faster but may miss objects
3. **Tune minNeighbors**: Higher values reduce false positives but may miss some objects
4. **Set Size Limits**: Use `minSize` and `maxSize` to restrict detection to expected object sizes
5. **Process at Lower Resolution**: Resize large images before detection for better performance
6. **Region of Interest**: If possible, detect only in specific regions of the image

**Cascade Classifier Limitations:**

- Haar cascades are sensitive to object orientation and scale
- Performance decreases with variations in lighting, pose, and occlusion
- For more robust detection, consider using DNN-based detectors (see cv2.dnn module)
- Profile face detection is generally less accurate than frontal face detection
- Eye detection works best on frontal faces with open eyes
