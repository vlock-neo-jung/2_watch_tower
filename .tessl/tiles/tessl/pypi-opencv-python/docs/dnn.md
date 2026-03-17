# Deep Neural Networks (DNN Module)

The `cv2.dnn` module provides a high-performance deep learning inference engine that supports multiple frameworks and model formats. It enables you to load pre-trained models and run inference for tasks like object detection, classification, semantic segmentation, and more, without requiring the original training frameworks.

OpenCV's DNN module is optimized for CPU and GPU inference, supports various backends (OpenCV, CUDA, OpenVINO), and can run models from popular frameworks like TensorFlow, PyTorch, Caffe, ONNX, and Darknet.

## Capabilities

### Loading Models

The DNN module provides multiple functions to load neural network models from different frameworks. The `readNet()` function can auto-detect the model format, while framework-specific functions offer more control.

```python { .api }
cv2.dnn.readNet(model, config=None, framework='')
```
Read a network model from file with automatic framework detection. This is the most convenient function as it automatically determines the framework based on file extensions.

**Parameters:**
- `model` (str): Path to the binary model file (e.g., `.caffemodel`, `.pb`, `.onnx`, `.weights`)
- `config` (str, optional): Path to the configuration file (e.g., `.prototxt` for Caffe, `.pbtxt` for TensorFlow, `.cfg` for Darknet)
- `framework` (str, optional): Explicit framework name to use if auto-detection fails

**Returns:** `Net` object representing the loaded neural network

**Example:**
```python
# Auto-detect framework
net = cv2.dnn.readNet('model.onnx')

# Load Darknet YOLO model
net = cv2.dnn.readNet('yolov3.weights', 'yolov3.cfg')

# Load TensorFlow model
net = cv2.dnn.readNet('frozen_graph.pb', 'graph.pbtxt')
```

---

```python { .api }
cv2.dnn.readNetFromCaffe(prototxt, caffeModel=None)
```
Read a Caffe model from prototxt and caffemodel files. Caffe is commonly used for CNN-based models.

**Parameters:**
- `prototxt` (str): Path to the `.prototxt` file (network structure)
- `caffeModel` (str, optional): Path to the `.caffemodel` file (trained weights)

**Returns:** `Net` object

**Example:**
```python
# Load pre-trained face detector
net = cv2.dnn.readNetFromCaffe(
    'deploy.prototxt',
    'res10_300x300_ssd_iter_140000.caffemodel'
)
```

---

```python { .api }
cv2.dnn.readNetFromTensorflow(model, config=None)
```
Read a TensorFlow model from frozen graph or saved model.

**Parameters:**
- `model` (str): Path to the `.pb` file (frozen graph)
- `config` (str, optional): Path to the `.pbtxt` file (text graph proto)

**Returns:** `Net` object

**Example:**
```python
# Load TensorFlow object detection model
net = cv2.dnn.readNetFromTensorflow(
    'frozen_inference_graph.pb',
    'graph.pbtxt'
)
```

---

```python { .api }
cv2.dnn.readNetFromONNX(onnxFile)
```
Read a model from ONNX format. ONNX is an open format supporting many frameworks.

**Parameters:**
- `onnxFile` (str): Path to the `.onnx` model file

**Returns:** `Net` object

**Example:**
```python
# Load ONNX model
net = cv2.dnn.readNetFromONNX('model.onnx')
```

---

```python { .api }
cv2.dnn.readNetFromDarknet(cfgFile, darknetModel=None)
```
Read a Darknet model (YOLO models). Darknet is the framework used for YOLO object detection.

**Parameters:**
- `cfgFile` (str): Path to the `.cfg` configuration file
- `darknetModel` (str, optional): Path to the `.weights` file

**Returns:** `Net` object

**Example:**
```python
# Load YOLOv4 model
net = cv2.dnn.readNetFromDarknet(
    'yolov4.cfg',
    'yolov4.weights'
)
```

---

```python { .api }
cv2.dnn.readNetFromTorch(model, isBinary=True)
```
Read a Torch model from file. Supports legacy Torch7 models.

**Parameters:**
- `model` (str): Path to the Torch model file
- `isBinary` (bool): Whether the model is in binary format (default: True)

**Returns:** `Net` object

---

```python { .api }
cv2.dnn.readNetFromModelOptimizer(xml, bin)
```
Read a model from OpenVINO Model Optimizer format (Intel).

**Parameters:**
- `xml` (str): Path to the `.xml` file (model structure)
- `bin` (str): Path to the `.bin` file (weights)

**Returns:** `Net` object

**Example:**
```python
# Load OpenVINO IR model
net = cv2.dnn.readNetFromModelOptimizer(
    'model.xml',
    'model.bin'
)
```

### Preprocessing

Before feeding images to neural networks, they typically need to be preprocessed into a specific format called a "blob". The blob functions handle resizing, scaling, mean subtraction, and channel swapping.

```python { .api }
cv2.dnn.blobFromImage(image, scalefactor=1.0, size=(0, 0), mean=(0, 0, 0),
                      swapRB=False, crop=False, ddepth=cv2.CV_32F)
```
Create a 4-dimensional blob from a single image. This is the most commonly used preprocessing function for deep learning models.

**Parameters:**
- `image` (numpy.ndarray): Input image (BGR format)
- `scalefactor` (float): Multiplier for image values (e.g., 1/255.0 to normalize to [0,1])
- `size` (tuple): Target spatial size (width, height) for the output image
- `mean` (tuple): Scalar with mean values to subtract from channels (e.g., (104.0, 177.0, 123.0))
- `swapRB` (bool): If True, swap Red and Blue channels (convert BGR to RGB)
- `crop` (bool): If True, crop image after resize; if False, just resize
- `ddepth` (int): Output blob depth (default: CV_32F for float32)

**Returns:** 4D numpy array with shape (1, channels, height, width) in NCHW format

**Example:**
```python
# Preprocess image for classification model
blob = cv2.dnn.blobFromImage(
    image,
    scalefactor=1/255.0,
    size=(224, 224),
    mean=(0, 0, 0),
    swapRB=True,
    crop=False
)

# Preprocess for face detection (Caffe SSD)
blob = cv2.dnn.blobFromImage(
    image,
    scalefactor=1.0,
    size=(300, 300),
    mean=(104.0, 177.0, 123.0),
    swapRB=False,
    crop=False
)
```

---

```python { .api }
cv2.dnn.blobFromImages(images, scalefactor=1.0, size=(0, 0), mean=(0, 0, 0),
                       swapRB=False, crop=False, ddepth=cv2.CV_32F)
```
Create a 4-dimensional blob from multiple images for batch processing.

**Parameters:**
- `images` (list of numpy.ndarray): List of input images
- Other parameters same as `blobFromImage()`

**Returns:** 4D numpy array with shape (batch_size, channels, height, width)

**Example:**
```python
# Process multiple images in a batch
images = [img1, img2, img3]
blob = cv2.dnn.blobFromImages(
    images,
    scalefactor=1/255.0,
    size=(224, 224),
    swapRB=True
)
```

---

```python { .api }
cv2.dnn.imagesFromBlob(blob)
```
Extract images from a blob after network processing. Useful for visualization or debugging.

**Parameters:**
- `blob` (numpy.ndarray): 4D blob array

**Returns:** List of images in standard OpenCV format

**Example:**
```python
# Convert blob back to images
images = cv2.dnn.imagesFromBlob(blob)
for img in images:
    cv2.imshow('Image', img)
```

### Neural Network Operations

The `Net` class provides methods for running inference, configuring backends, and querying network structure.

```python { .api }
Net.setInput(blob, name='', scalefactor=1.0, mean=(0, 0, 0))
```
Set the input blob for the network. This prepares the data for forward pass.

**Parameters:**
- `blob` (numpy.ndarray): 4D input blob (typically from `blobFromImage()`)
- `name` (str): Name of the input layer (empty string for default)
- `scalefactor` (float): Optional additional scaling
- `mean` (tuple): Optional additional mean subtraction

**Returns:** None

**Example:**
```python
net.setInput(blob)
# Or specify input layer name
net.setInput(blob, name='input_1')
```

---

```python { .api }
Net.forward(outputName=None)
```
Run forward pass to compute output of the specified layer. This performs the actual inference.

**Parameters:**
- `outputName` (str, optional): Name of the output layer. If None, returns outputs from all unconnected output layers

**Returns:** numpy.ndarray or list of numpy arrays containing network output(s)

**Example:**
```python
# Get output from final layer
output = net.forward()

# Get output from specific layer
output = net.forward('detection_out')

# Get outputs from multiple layers
layer_names = net.getUnconnectedOutLayersNames()
outputs = net.forward(layer_names)
```

---

```python { .api }
Net.forwardAsync(outputName=None)
```
Run asynchronous forward pass. Useful for pipelining and concurrent processing.

**Parameters:**
- `outputName` (str, optional): Name of the output layer

**Returns:** Async handle for retrieving results

---

```python { .api }
Net.setPreferableBackend(backendId)
```
Set the computation backend for the network. Different backends offer different performance characteristics.

**Parameters:**
- `backendId` (int): Backend identifier (see Backend Constants section)

**Returns:** None

**Example:**
```python
# Use OpenCV's implementation (CPU)
net.setPreferableBackend(cv2.dnn.DNN_BACKEND_OPENCV)

# Use CUDA for GPU acceleration
net.setPreferableBackend(cv2.dnn.DNN_BACKEND_CUDA)

# Use Intel's OpenVINO
net.setPreferableBackend(cv2.dnn.DNN_BACKEND_INFERENCE_ENGINE)
```

---

```python { .api }
Net.setPreferableTarget(targetId)
```
Set the computation target device (CPU, GPU, etc.). Must be called after `setPreferableBackend()`.

**Parameters:**
- `targetId` (int): Target device identifier (see Target Constants section)

**Returns:** None

**Example:**
```python
# Use CPU
net.setPreferableTarget(cv2.dnn.DNN_TARGET_CPU)

# Use GPU with CUDA
net.setPreferableBackend(cv2.dnn.DNN_BACKEND_CUDA)
net.setPreferableTarget(cv2.dnn.DNN_TARGET_CUDA)

# Use GPU with FP16 precision for faster inference
net.setPreferableBackend(cv2.dnn.DNN_BACKEND_CUDA)
net.setPreferableTarget(cv2.dnn.DNN_TARGET_CUDA_FP16)
```

---

```python { .api }
Net.getLayerNames()
```
Get names of all layers in the network. Useful for debugging and understanding network structure.

**Returns:** List of strings containing layer names

**Example:**
```python
layer_names = net.getLayerNames()
print(f"Network has {len(layer_names)} layers")
for name in layer_names[:5]:
    print(name)
```

---

```python { .api }
Net.getUnconnectedOutLayers()
```
Get indices of output layers (layers without consumers). These are typically the final layers you want to retrieve.

**Returns:** List of integers representing output layer indices

**Example:**
```python
output_layers = net.getUnconnectedOutLayers()
print(f"Output layer indices: {output_layers}")
```

---

```python { .api }
Net.getUnconnectedOutLayersNames()
```
Get names of output layers. More convenient than using indices.

**Returns:** List of strings containing output layer names

**Example:**
```python
# Get outputs from all output layers (e.g., for YOLO)
output_layer_names = net.getUnconnectedOutLayersNames()
outputs = net.forward(output_layer_names)
```

### Post-processing

After running inference, post-processing is often needed to filter and refine detection results. Non-Maximum Suppression (NMS) is the most common post-processing technique.

```python { .api }
cv2.dnn.NMSBoxes(bboxes, scores, score_threshold, nms_threshold,
                 eta=1.0, top_k=0)
```
Apply Non-Maximum Suppression (NMS) to bounding boxes. NMS filters out overlapping detections, keeping only the most confident ones.

**Parameters:**
- `bboxes` (list): List of bounding boxes, each as [x, y, width, height]
- `scores` (list): List of confidence scores corresponding to each box
- `score_threshold` (float): Minimum score threshold to consider a detection
- `nms_threshold` (float): IoU (Intersection over Union) threshold for NMS (typically 0.3-0.5)
- `eta` (float): Coefficient for adaptive NMS (default: 1.0)
- `top_k` (int): Maximum number of boxes to keep (0 = no limit)

**Returns:** List of indices of boxes to keep after NMS

**Example:**
```python
# Apply NMS to detections
boxes = [[10, 10, 50, 50], [12, 12, 48, 48], [100, 100, 60, 60]]
scores = [0.9, 0.85, 0.95]

indices = cv2.dnn.NMSBoxes(
    boxes,
    scores,
    score_threshold=0.5,
    nms_threshold=0.4
)

# Keep only selected boxes
kept_boxes = [boxes[i] for i in indices]
kept_scores = [scores[i] for i in indices]
```

---

```python { .api }
cv2.dnn.NMSBoxesRotated(bboxes, scores, score_threshold, nms_threshold,
                        eta=1.0, top_k=0)
```
Apply NMS to rotated bounding boxes. Used for oriented object detection where boxes can be at any angle.

**Parameters:**
- `bboxes` (list): List of rotated boxes, each as ((center_x, center_y), (width, height), angle)
- Other parameters same as `NMSBoxes()`

**Returns:** List of indices of boxes to keep

**Example:**
```python
# Rotated boxes for text detection
rotated_boxes = [
    ((100, 100), (50, 20), 30.0),  # center, size, angle
    ((150, 150), (60, 25), -15.0)
]
scores = [0.9, 0.85]

indices = cv2.dnn.NMSBoxesRotated(
    rotated_boxes,
    scores,
    score_threshold=0.5,
    nms_threshold=0.3
)
```

### Backend and Target Constants

Backend constants specify which computational backend to use:

```python { .api }
# Backend constants
cv2.dnn.DNN_BACKEND_DEFAULT        # Let OpenCV choose
cv2.dnn.DNN_BACKEND_HALIDE         # Halide backend
cv2.dnn.DNN_BACKEND_INFERENCE_ENGINE  # Intel OpenVINO
cv2.dnn.DNN_BACKEND_OPENCV         # Pure OpenCV implementation
cv2.dnn.DNN_BACKEND_VKCOM          # Vulkan compute
cv2.dnn.DNN_BACKEND_CUDA           # NVIDIA CUDA
```

Target constants specify which device to run on:

```python { .api }
# Target constants
cv2.dnn.DNN_TARGET_CPU             # CPU execution
cv2.dnn.DNN_TARGET_OPENCL          # OpenCL (GPU)
cv2.dnn.DNN_TARGET_OPENCL_FP16     # OpenCL with FP16 precision
cv2.dnn.DNN_TARGET_MYRIAD          # Intel Movidius
cv2.dnn.DNN_TARGET_VULKAN          # Vulkan API
cv2.dnn.DNN_TARGET_CUDA            # NVIDIA CUDA GPU
cv2.dnn.DNN_TARGET_CUDA_FP16       # NVIDIA CUDA with FP16
```

**Usage example:**
```python
# Configure for optimal CPU performance
net.setPreferableBackend(cv2.dnn.DNN_BACKEND_OPENCV)
net.setPreferableTarget(cv2.dnn.DNN_TARGET_CPU)

# Configure for NVIDIA GPU with FP16
net.setPreferableBackend(cv2.dnn.DNN_BACKEND_CUDA)
net.setPreferableTarget(cv2.dnn.DNN_TARGET_CUDA_FP16)

# Configure for Intel hardware with OpenVINO
net.setPreferableBackend(cv2.dnn.DNN_BACKEND_INFERENCE_ENGINE)
net.setPreferableTarget(cv2.dnn.DNN_TARGET_CPU)
```

## Practical Examples

### Example 1: Image Classification

```python
import cv2
import numpy as np

# Load a pre-trained classification model (e.g., MobileNet)
net = cv2.dnn.readNetFromCaffe('mobilenet_deploy.prototxt',
                                'mobilenet.caffemodel')

# Read and preprocess image
image = cv2.imread('image.jpg')
blob = cv2.dnn.blobFromImage(image,
                             scalefactor=1.0,
                             size=(224, 224),
                             mean=(104.0, 117.0, 123.0),
                             swapRB=False,
                             crop=False)

# Run inference
net.setInput(blob)
predictions = net.forward()

# Get top prediction
class_id = np.argmax(predictions[0])
confidence = predictions[0][class_id]

print(f"Predicted class: {class_id}, Confidence: {confidence:.2f}")
```

### Example 2: Object Detection with YOLO

```python
import cv2
import numpy as np

# Load YOLO model
net = cv2.dnn.readNetFromDarknet('yolov4.cfg', 'yolov4.weights')
net.setPreferableBackend(cv2.dnn.DNN_BACKEND_CUDA)
net.setPreferableTarget(cv2.dnn.DNN_TARGET_CUDA)

# Read image
image = cv2.imread('image.jpg')
height, width = image.shape[:2]

# Preprocess
blob = cv2.dnn.blobFromImage(image,
                             scalefactor=1/255.0,
                             size=(416, 416),
                             swapRB=True,
                             crop=False)

# Run inference
net.setInput(blob)
output_layers = net.getUnconnectedOutLayersNames()
outputs = net.forward(output_layers)

# Post-process detections
boxes = []
confidences = []
class_ids = []

for output in outputs:
    for detection in output:
        scores = detection[5:]
        class_id = np.argmax(scores)
        confidence = scores[class_id]

        if confidence > 0.5:
            # Scale bounding box back to original image
            center_x = int(detection[0] * width)
            center_y = int(detection[1] * height)
            w = int(detection[2] * width)
            h = int(detection[3] * height)

            # Rectangle coordinates
            x = int(center_x - w / 2)
            y = int(center_y - h / 2)

            boxes.append([x, y, w, h])
            confidences.append(float(confidence))
            class_ids.append(class_id)

# Apply NMS
indices = cv2.dnn.NMSBoxes(boxes, confidences,
                           score_threshold=0.5,
                           nms_threshold=0.4)

# Draw results
for i in indices:
    box = boxes[i]
    x, y, w, h = box
    cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
    cv2.putText(image, f'Class {class_ids[i]}: {confidences[i]:.2f}',
                (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

cv2.imshow('Detections', image)
cv2.waitKey(0)
```

### Example 3: Face Detection with SSD

```python
import cv2

# Load pre-trained face detection model
net = cv2.dnn.readNetFromCaffe(
    'deploy.prototxt',
    'res10_300x300_ssd_iter_140000.caffemodel'
)

# Read image
image = cv2.imread('faces.jpg')
h, w = image.shape[:2]

# Preprocess
blob = cv2.dnn.blobFromImage(
    cv2.resize(image, (300, 300)),
    scalefactor=1.0,
    size=(300, 300),
    mean=(104.0, 177.0, 123.0)
)

# Detect faces
net.setInput(blob)
detections = net.forward()

# Process detections
for i in range(detections.shape[2]):
    confidence = detections[0, 0, i, 2]

    if confidence > 0.5:
        # Get bounding box
        box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
        (x1, y1, x2, y2) = box.astype(int)

        # Draw rectangle
        cv2.rectangle(image, (x1, y1), (x2, y2), (0, 255, 0), 2)
        text = f'{confidence * 100:.1f}%'
        cv2.putText(image, text, (x1, y1 - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

cv2.imshow('Face Detection', image)
cv2.waitKey(0)
```

### Example 4: Using ONNX Models

```python
import cv2
import numpy as np

# Load ONNX model (e.g., exported from PyTorch)
net = cv2.dnn.readNetFromONNX('model.onnx')

# Optional: Use GPU
net.setPreferableBackend(cv2.dnn.DNN_BACKEND_CUDA)
net.setPreferableTarget(cv2.dnn.DNN_TARGET_CUDA)

# Read and preprocess image
image = cv2.imread('image.jpg')
blob = cv2.dnn.blobFromImage(image,
                             scalefactor=1/255.0,
                             size=(640, 640),
                             mean=(0, 0, 0),
                             swapRB=True,
                             crop=False)

# Run inference
net.setInput(blob)
output = net.forward()

print(f"Output shape: {output.shape}")
# Further processing depends on model architecture
```

### Example 5: Batch Processing

```python
import cv2
import numpy as np

# Load model
net = cv2.dnn.readNetFromCaffe('model.prototxt', 'model.caffemodel')

# Load multiple images
images = [cv2.imread(f'image{i}.jpg') for i in range(5)]

# Create batch blob
blob = cv2.dnn.blobFromImages(images,
                              scalefactor=1/255.0,
                              size=(224, 224),
                              mean=(0, 0, 0),
                              swapRB=True)

# Process batch
net.setInput(blob)
predictions = net.forward()

# Results for each image
for i, pred in enumerate(predictions):
    class_id = np.argmax(pred)
    confidence = pred[class_id]
    print(f"Image {i}: Class {class_id}, Confidence: {confidence:.2f}")
```
