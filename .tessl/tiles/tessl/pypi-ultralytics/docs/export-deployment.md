# Export and Deployment

Export trained models to various formats for deployment including ONNX, TensorRT, CoreML, TensorFlow, OpenVINO, and mobile formats with optimization options.

## Capabilities

### Model Export

Export models to different formats for deployment across various platforms and frameworks.

```python { .api }
def export(self, format='torchscript', imgsz=640, keras=False, optimize=False, **kwargs) -> str:
    """
    Export model to various formats for deployment.
    
    Parameters:
    - format (str): Export format ('torchscript', 'onnx', 'openvino', 'engine', 
                   'coreml', 'saved_model', 'pb', 'tflite', 'edgetpu', 'tfjs', 'paddle')
    - imgsz (int | List[int]): Image size for export (default: 640)
    - keras (bool): Use Keras for TensorFlow exports (default: False)
    - optimize (bool): TorchScript optimization (default: False)
    - half (bool): FP16 quantization (default: False)
    - dynamic (bool): ONNX/TensorRT dynamic axes (default: False)
    - simplify (bool): ONNX simplification (default: False)
    - opset (int): ONNX opset version (default: None)
    - workspace (int): TensorRT workspace size in GB (default: 4)
    - nms (bool): Add NMS module to model (default: False)
    - lr (float): CoreML learning rate (default: 0.01)
    - batch_size (int): Batch size for export (default: 1)
    - device (str): Device to export from ('cpu', '0', etc.)
    - verbose (bool): Verbose output (default: False)
    
    Returns:
    str: Path to exported model
    """
```

**Supported Export Formats:**

| Format | Description | Platform | Extension |
|--------|-------------|----------|-----------|
| `torchscript` | TorchScript | PyTorch | `.torchscript` |
| `onnx` | ONNX | Multi-platform | `.onnx` |
| `openvino` | OpenVINO | Intel | `_openvino_model/` |
| `engine` | TensorRT | NVIDIA | `.engine` |
| `coreml` | CoreML | Apple | `.mlpackage` |
| `saved_model` | TensorFlow SavedModel | TensorFlow | `_saved_model/` |
| `pb` | TensorFlow GraphDef | TensorFlow | `.pb` |
| `tflite` | TensorFlow Lite | Mobile/Edge | `.tflite` |
| `edgetpu` | Edge TPU | Google Coral | `_edgetpu.tflite` |
| `tfjs` | TensorFlow.js | Web | `_web_model/` |
| `paddle` | PaddlePaddle | Baidu | `_paddle_model/` |

**Usage Examples:**

```python
from ultralytics import YOLO

# Load a trained model
model = YOLO("yolo11n.pt")

# Export to ONNX
onnx_path = model.export(format='onnx')

# Export to TensorRT with optimization
trt_path = model.export(
    format='engine',
    imgsz=640,
    half=True,
    workspace=8,
    verbose=True
)

# Export to CoreML for iOS
coreml_path = model.export(
    format='coreml',
    imgsz=640,
    half=True,
    nms=True
)

# Export to TensorFlow Lite for mobile
tflite_path = model.export(
    format='tflite',
    imgsz=320,
    half=True
)

# Export with dynamic input shapes (ONNX)
onnx_path = model.export(
    format='onnx',
    dynamic=True,
    simplify=True,
    opset=12
)

# Export for Edge TPU
edgetpu_path = model.export(format='edgetpu')

# Export to TensorFlow.js for web deployment
tfjs_path = model.export(format='tfjs')
```

### Model Benchmarking

Benchmark exported models across different formats to compare inference performance.

```python { .api }
def benchmark(self, **kwargs) -> dict:
    """
    Benchmark model across export formats.
    
    Parameters:
    - data (str): Dataset YAML path for benchmarking
    - imgsz (int): Image size for benchmarking (default: 640)
    - half (bool): FP16 inference (default: False)
    - int8 (bool): INT8 quantization (default: False)
    - device (str): Device to benchmark on ('cpu', '0', etc.)
    - verbose (bool): Verbose output (default: False)
    
    Returns:
    dict: Benchmark results including speed and accuracy metrics
    """
```

**Usage Examples:**

```python
# Basic benchmarking
results = model.benchmark()

# Benchmark with specific parameters
results = model.benchmark(
    data="coco8.yaml",
    imgsz=640,
    half=True,
    device='0'
)

# Print benchmark results
for format_name, metrics in results.items():
    print(f"{format_name}: {metrics['inference_time']:.2f}ms")
```

### Deployment Examples

#### ONNX Runtime Deployment

```python
import onnxruntime as ort
import numpy as np
from PIL import Image
import cv2

# Load ONNX model
session = ort.InferenceSession("yolo11n.onnx")

# Preprocess image
def preprocess(image_path):
    image = cv2.imread(image_path)
    image = cv2.resize(image, (640, 640))
    image = image.transpose(2, 0, 1)  # HWC to CHW
    image = np.expand_dims(image, axis=0)  # Add batch dimension
    image = image.astype(np.float32) / 255.0
    return image

# Run inference
input_data = preprocess("image.jpg")
outputs = session.run(None, {"images": input_data})
```

#### TensorRT Deployment

```python
import tensorrt as trt
import pycuda.driver as cuda
import pycuda.autoinit

# Load TensorRT engine
def load_engine(engine_path):
    with open(engine_path, 'rb') as f:
        runtime = trt.Runtime(trt.Logger(trt.Logger.WARNING))
        return runtime.deserialize_cuda_engine(f.read())

engine = load_engine("yolo11n.engine")

# Create execution context
context = engine.create_execution_context()

# Allocate memory
def allocate_buffers(engine):
    inputs = []
    outputs = []
    bindings = []
    
    for binding in engine:
        size = trt.volume(engine.get_binding_shape(binding))
        dtype = trt.nptype(engine.get_binding_dtype(binding))
        
        # Allocate host and device buffers
        host_mem = cuda.pagelocked_empty(size, dtype)
        device_mem = cuda.mem_alloc(host_mem.nbytes)
        
        bindings.append(int(device_mem))
        
        if engine.binding_is_input(binding):
            inputs.append({'host': host_mem, 'device': device_mem})
        else:
            outputs.append({'host': host_mem, 'device': device_mem})
    
    return inputs, outputs, bindings

inputs, outputs, bindings = allocate_buffers(engine)
```

#### CoreML Deployment (iOS)

```swift
import CoreML
import Vision

// Load CoreML model
guard let model = try? yolo11n(configuration: MLModelConfiguration()) else {
    fatalError("Failed to load model")
}

// Create Vision request
let request = VNCoreMLRequest(model: model.model) { request, error in
    guard let results = request.results as? [VNRecognizedObjectObservation] else {
        return
    }
    
    // Process detection results
    for result in results {
        let boundingBox = result.boundingBox
        let confidence = result.confidence
        let label = result.labels.first?.identifier ?? "Unknown"
        
        print("Detected: \\(label) (\\(confidence))")
    }
}

// Perform inference
let handler = VNImageRequestHandler(cgImage: cgImage, options: [:])
try? handler.perform([request])
```

#### TensorFlow Lite Deployment (Android)

```java
import org.tensorflow.lite.Interpreter;
import org.tensorflow.lite.support.image.TensorImage;
import org.tensorflow.lite.support.image.ImageProcessor;

// Load TFLite model
Interpreter tflite = new Interpreter(loadModelFile("yolo11n.tflite"));

// Preprocess image
ImageProcessor imageProcessor = new ImageProcessor.Builder()
    .add(new ResizeOp(640, 640, ResizeOp.ResizeMethod.BILINEAR))
    .add(new NormalizeOp(0.0f, 255.0f))
    .build();

TensorImage tensorImage = new TensorImage(DataType.FLOAT32);
tensorImage.load(bitmap);
tensorImage = imageProcessor.process(tensorImage);

// Run inference
float[][][][] output = new float[1][25200][85]; // Adjust based on model
tflite.run(tensorImage.getBuffer(), output);
```

### Optimization Techniques

#### Quantization

```python
# INT8 quantization during export
model.export(format='onnx', int8=True, data="calibration_data.yaml")

# Half precision (FP16)
model.export(format='onnx', half=True)

# Dynamic quantization (TensorFlow)
model.export(format='saved_model', keras=True, int8=True)
```

#### Model Pruning

```python
# Structured pruning during training
model.train(
    data="dataset.yaml",
    epochs=100,
    prune=0.3  # Remove 30% of parameters
)

# Export pruned model
model.export(format='onnx', optimize=True)
```

#### Knowledge Distillation

```python
# Train smaller model with teacher model guidance
teacher_model = YOLO("yolo11x.pt")
student_model = YOLO("yolo11n.pt")

# Distillation training (custom implementation required)
student_model.train(
    data="dataset.yaml",
    teacher=teacher_model,
    distillation_alpha=0.7
)
```

## Types

```python { .api }
from typing import Dict, Any, Optional, Union, List
from pathlib import Path

# Export configuration types
ExportFormat = str  # 'onnx', 'engine', 'coreml', etc.
ExportConfig = Dict[str, Any]
BenchmarkResults = Dict[str, Dict[str, float]]

# Platform-specific types
class DeploymentTarget:
    cpu: str = "cpu"
    gpu: str = "gpu" 
    mobile: str = "mobile"
    web: str = "web"
    edge: str = "edge"

# Optimization options
class OptimizationConfig:
    half: bool = False      # FP16 precision
    int8: bool = False      # INT8 quantization
    dynamic: bool = False   # Dynamic input shapes
    simplify: bool = False  # Model simplification
    optimize: bool = False  # Framework optimization
```