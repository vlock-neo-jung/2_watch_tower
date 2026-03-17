# Training and Validation

Comprehensive training and validation capabilities with support for custom datasets, hyperparameter tuning, distributed training, and model optimization techniques.

## Capabilities

### Model Training

Train YOLO models on custom datasets with extensive configuration options and built-in optimization techniques.

```python { .api }
def train(self, data=None, epochs=100, imgsz=640, batch=16, **kwargs) -> dict:
    """
    Train the model on a dataset.
    
    Parameters:
    - data (str | Path): Path to dataset YAML file
    - epochs (int): Number of training epochs (default: 100)
    - imgsz (int): Image size for training (default: 640)
    - batch (int): Batch size (default: 16)
    - lr0 (float): Initial learning rate (default: 0.01)
    - lrf (float): Final learning rate factor (default: 0.01)
    - momentum (float): SGD momentum (default: 0.937)
    - weight_decay (float): Optimizer weight decay (default: 0.0005)
    - warmup_epochs (float): Warmup epochs (default: 3.0)
    - warmup_momentum (float): Warmup momentum (default: 0.8)
    - warmup_bias_lr (float): Warmup bias learning rate (default: 0.1)
    - box (float): Box loss gain (default: 7.5)
    - cls (float): Classification loss gain (default: 0.5)
    - dfl (float): Distribution focal loss gain (default: 1.5)
    - pose (float): Pose loss gain (default: 12.0)
    - kobj (float): Keypoint objectness loss gain (default: 2.0)
    - dropout (float): Use dropout regularization (default: 0.0)
    - val (bool): Validate during training (default: True)
    - save (bool): Save training checkpoints (default: True)
    - save_period (int): Save checkpoint every x epochs (default: -1)
    - cache (str): Cache images for faster training ('ram', 'disk', False)
    - device (str): Device to train on ('cpu', '0', '0,1', etc.)
    - workers (int): Number of worker threads (default: 8)
    - project (str): Project name (default: 'runs/train')
    - name (str): Experiment name (default: 'exp')
    - exist_ok (bool): Overwrite existing experiment (default: False)
    - pretrained (bool | str): Use pretrained model (default: True)
    - optimizer (str): Optimizer ('SGD', 'Adam', 'AdamW', 'RMSProp')
    - verbose (bool): Verbose output (default: False)
    - seed (int): Random seed (default: 0)
    - deterministic (bool): Deterministic mode (default: True)
    - single_cls (bool): Train as single-class dataset (default: False)
    - rect (bool): Rectangular training (default: False)
    - cos_lr (bool): Cosine learning rate scheduler (default: False)
    - close_mosaic (int): Close mosaic augmentation at this epoch (default: 10)
    - resume (bool | str): Resume training from checkpoint (default: False)
    - amp (bool): Automatic Mixed Precision training (default: True)
    - fraction (float): Dataset fraction to train on (default: 1.0)
    - profile (bool): Profile ONNX and TensorRT speeds (default: False)
    - freeze (int | List[int]): Freeze layers (default: None)
    
    Returns:
    dict: Training results and metrics
    """
```

**Usage Examples:**

```python
from ultralytics import YOLO

# Load a model
model = YOLO("yolo11n.pt")

# Basic training
results = model.train(data="coco8.yaml", epochs=100, imgsz=640)

# Advanced training configuration
results = model.train(
    data="custom_dataset.yaml",
    epochs=300,
    imgsz=1280,
    batch=8,
    lr0=0.001,
    optimizer='AdamW',
    augment=True,
    mixup=0.1,
    copy_paste=0.1,
    device='0,1',  # Multi-GPU training
    workers=16,
    project='my_project',
    name='custom_experiment'
)

# Resume training
results = model.train(resume=True)

# Train with custom callbacks
def on_epoch_end(trainer):
    print(f"Epoch {trainer.epoch} completed")

results = model.train(
    data="dataset.yaml", 
    epochs=100,
    callbacks={'on_epoch_end': on_epoch_end}
)
```

### Model Validation

Validate trained models on test datasets to evaluate performance metrics.

```python { .api }
def val(self, data=None, split='val', imgsz=640, batch=16, **kwargs) -> dict:
    """
    Validate the model on a dataset.
    
    Parameters:
    - data (str | Path): Path to dataset YAML file
    - split (str): Dataset split to validate on ('val', 'test')
    - imgsz (int): Image size for validation (default: 640)
    - batch (int): Batch size (default: 16) 
    - conf (float): Confidence threshold (default: 0.001)
    - iou (float): IoU threshold for NMS (default: 0.6)
    - max_det (int): Maximum detections per image (default: 300)
    - half (bool): Use FP16 inference (default: True)
    - device (str): Device to run on ('cpu', '0', '0,1', etc.)
    - dnn (bool): Use OpenCV DNN for ONNX inference (default: False)
    - plots (bool): Save prediction plots (default: False)
    - save_txt (bool): Save results as txt files (default: False)
    - save_conf (bool): Include confidence in txt files (default: False)
    - save_json (bool): Save results as JSON (default: False)
    - project (str): Project name (default: 'runs/val')
    - name (str): Experiment name (default: 'exp')
    - exist_ok (bool): Overwrite existing experiment (default: False)
    - verbose (bool): Verbose output (default: True)
    - workers (int): Number of worker threads (default: 8)
    
    Returns:
    dict: Validation metrics including mAP, precision, recall
    """
```

**Usage Examples:**

```python
# Basic validation
metrics = model.val()

# Validate on specific dataset
metrics = model.val(data="custom_dataset.yaml")

# Validate with custom parameters
metrics = model.val(
    data="dataset.yaml",
    split='test',
    imgsz=1280,
    conf=0.25,
    iou=0.5,
    save_json=True
)

# Access validation metrics
print(f"mAP50: {metrics.box.map50}")
print(f"mAP50-95: {metrics.box.map}")
print(f"Precision: {metrics.box.mp}")
print(f"Recall: {metrics.box.mr}")
```

### Hyperparameter Tuning

Automatically optimize hyperparameters using various search strategies.

```python { .api }
def tune(self, data=None, space=None, grace_period=10, gpu_per_trial=None, **kwargs) -> dict:
    """
    Perform hyperparameter tuning using Ray Tune.
    
    Parameters:
    - data (str | Path): Path to dataset YAML file
    - space (dict): Hyperparameter search space
    - grace_period (int): Grace period for early stopping
    - gpu_per_trial (float): GPU fraction per trial
    - iterations (int): Number of tuning iterations (default: 10)
    - **kwargs: Additional training arguments
    
    Returns:
    dict: Best hyperparameters and results
    """
```

**Usage Examples:**

```python
# Basic hyperparameter tuning
best_params = model.tune(data="dataset.yaml", iterations=30)

# Custom search space
search_space = {
    'lr0': (0.0001, 0.01),
    'momentum': (0.8, 0.95),
    'weight_decay': (0.0001, 0.001),
    'batch': [8, 16, 32]
}

best_params = model.tune(
    data="dataset.yaml", 
    space=search_space,
    iterations=50,
    gpu_per_trial=0.5
)
```

### Training Callbacks

Customize training behavior with callback functions.

```python { .api }
def add_callback(self, event: str, callback):
    """
    Add callback function for specific training event.
    
    Parameters:
    - event (str): Event name ('on_epoch_end', 'on_batch_end', etc.)
    - callback: Callback function
    """

def clear_callback(self, event: str):
    """Clear all callbacks for specific event."""

def reset_callbacks(self):
    """Reset all callbacks to default functions."""
```

**Available Events:**
- `on_pretrain_routine_start`
- `on_pretrain_routine_end`
- `on_train_start`
- `on_train_epoch_start`
- `on_train_batch_start`
- `on_optimizer_step`
- `on_before_zero_grad`
- `on_train_batch_end`
- `on_train_epoch_end`
- `on_val_start`
- `on_val_batch_start`
- `on_val_batch_end`
- `on_val_end`
- `on_fit_epoch_end`
- `on_model_save`
- `on_train_end`
- `teardown`

**Usage Examples:**

```python
# Add custom callbacks
def log_predictions(trainer):
    # Custom logging logic
    print(f"Epoch {trainer.epoch}: Loss = {trainer.loss}")

def save_best_model(trainer):
    if trainer.best_fitness == trainer.fitness:
        trainer.model.save(f"best_model_epoch_{trainer.epoch}.pt")

model.add_callback('on_train_epoch_end', log_predictions)
model.add_callback('on_fit_epoch_end', save_best_model)

# Train with callbacks
results = model.train(data="dataset.yaml", epochs=100)

# Clear specific callback
model.clear_callback('on_train_epoch_end')

# Reset all callbacks
model.reset_callbacks()
```

## Training Data Format

### Dataset YAML Configuration

```yaml
# dataset.yaml
path: /path/to/dataset  # dataset root dir
train: images/train     # train images (relative to path)
val: images/val         # val images (relative to path)
test: images/test       # test images (optional)

# Classes
names:
  0: person
  1: bicycle
  2: car
  3: motorcycle
  # ... more classes
```

### Directory Structure

```
dataset/
├── images/
│   ├── train/
│   │   ├── image1.jpg
│   │   ├── image2.jpg
│   │   └── ...
│   ├── val/
│   │   ├── image1.jpg
│   │   ├── image2.jpg
│   │   └── ...
│   └── test/
│       ├── image1.jpg
│       └── ...
└── labels/
    ├── train/
    │   ├── image1.txt
    │   ├── image2.txt
    │   └── ...
    ├── val/
    │   ├── image1.txt
    │   ├── image2.txt
    │   └── ...
    └── test/
        ├── image1.txt
        └── ...
```

## Types

```python { .api }
from typing import Dict, Any, Optional, Union, List, Callable
from pathlib import Path

# Training configuration types
TrainingConfig = Dict[str, Any]
ValidationMetrics = Dict[str, float]
CallbackFunction = Callable[['BaseTrainer'], None]

# Common metric types
class MetricsClass:
    map: float      # mAP@0.5:0.95
    map50: float    # mAP@0.5
    map75: float    # mAP@0.75
    mp: float       # mean precision
    mr: float       # mean recall
    fitness: float  # weighted combination of metrics
```