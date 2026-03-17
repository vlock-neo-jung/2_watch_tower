# Metrics and Evaluation

Tools for evaluating model performance including confusion matrices and mean average precision calculations.

## Capabilities

### Detection Metrics

```python { .api }
class ConfusionMatrix:
    """
    Calculate and visualize confusion matrix for classification/detection results.
    
    Args:
        matrix (np.ndarray): Confusion matrix data
        classes (list[str]): Class names for labeling
    """
    
class MeanAveragePrecision:
    """
    Calculate mean Average Precision (mAP) for object detection evaluation.
    
    Supports COCO-style evaluation with multiple IoU thresholds.
    """
    
    def update(self, predictions: Detections, targets: Detections) -> None:
        """Update metric with prediction and ground truth pairs."""
        
    def compute(self) -> dict:
        """Compute final mAP scores and per-class metrics."""
```

## Usage Example

```python
import supervision as sv

# Initialize metrics
confusion_matrix = sv.ConfusionMatrix()
map_metric = sv.MeanAveragePrecision()

# Evaluate predictions against ground truth  
for predictions, targets in evaluation_data:
    map_metric.update(predictions, targets)
    
# Get results
map_results = map_metric.compute()
print(f"mAP@0.5: {map_results['map_50']}")
print(f"mAP@0.5:0.95: {map_results['map']}")
```