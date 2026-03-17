# Vision-Language Model Integration

Support for integrating various vision-language models (VLMs) for zero-shot object detection and image analysis tasks. These models can perform object detection, segmentation, and other computer vision tasks using natural language prompts.

## Capabilities

### VLM Enums

Supported vision-language models with standardized interfaces.

```python { .api }
class VLM(Enum):
    """
    Enum specifying supported Vision-Language Models (VLMs).

    Attributes:
        PALIGEMMA: Google's PaliGemma vision-language model
        FLORENCE_2: Microsoft's Florence-2 vision-language model
        QWEN_2_5_VL: Qwen2.5-VL open vision-language model from Alibaba
        GOOGLE_GEMINI_2_0: Google Gemini 2.0 vision-language model
        GOOGLE_GEMINI_2_5: Google Gemini 2.5 vision-language model
        MOONDREAM: The Moondream vision-language model
    """
    PALIGEMMA = "paligemma"
    FLORENCE_2 = "florence_2"
    QWEN_2_5_VL = "qwen_2_5_vl"
    GOOGLE_GEMINI_2_0 = "gemini_2_0"
    GOOGLE_GEMINI_2_5 = "gemini_2_5"
    MOONDREAM = "moondream"

    @classmethod
    def list(cls) -> list[str]:
        """Return list of all VLM values."""

    @classmethod
    def from_value(cls, value: "VLM" | str) -> "VLM":
        """Create VLM enum from string value."""

@deprecated("LMM enum is deprecated, use VLM instead")
class LMM(Enum):
    """
    Deprecated. Use VLM instead.
    Enum specifying supported Large Multimodal Models (LMMs).
    """
    PALIGEMMA = "paligemma"
    FLORENCE_2 = "florence_2"
    QWEN_2_5_VL = "qwen_2_5_vl"
    GOOGLE_GEMINI_2_0 = "gemini_2_0"
    GOOGLE_GEMINI_2_5 = "gemini_2_5"
    MOONDREAM = "moondream"
```

### VLM Parameter Validation

Utility for validating VLM parameters and result types.

```python { .api }
def validate_vlm_parameters(vlm: VLM | str, result: Any, kwargs: dict[str, Any]) -> VLM:
    """
    Validates the parameters and result type for a given Vision-Language Model (VLM).

    Args:
        vlm: The VLM enum or string specifying the model
        result: The result object to validate (type depends on VLM)
        kwargs: Dictionary of arguments to validate against required/allowed lists

    Returns:
        The validated VLM enum value

    Raises:
        ValueError: If the VLM, result type, or arguments are invalid
    """
```

### Model-Specific Parsers

Functions to parse results from different vision-language models into standardized formats.

```python { .api }
def from_paligemma(
    result: str, 
    resolution_wh: tuple[int, int], 
    classes: list[str] | None = None
) -> tuple[np.ndarray, np.ndarray | None, np.ndarray]:
    """
    Parse bounding boxes from PaliGemma-formatted text and scale to specified resolution.

    Args:
        result: String containing PaliGemma-formatted locations and labels
        resolution_wh: Target resolution (width, height) for scaling coordinates
        classes: Optional list of valid class names for filtering

    Returns:
        Tuple of (xyxy, class_names, confidence_scores)
    """

def from_qwen_2_5_vl(
    result: str,
    input_wh: tuple[int, int],
    resolution_wh: tuple[int, int],
    classes: list[str] | None = None
) -> tuple[np.ndarray, np.ndarray | None, np.ndarray]:
    """
    Parse bounding boxes from Qwen2.5-VL formatted text.

    Args:
        result: String containing Qwen2.5-VL formatted locations and labels
        input_wh: Input image resolution (width, height)
        resolution_wh: Target resolution (width, height) for scaling coordinates
        classes: Optional list of valid class names for filtering

    Returns:
        Tuple of (xyxy, class_names, confidence_scores)
    """

def from_florence_2(
    result: dict, 
    resolution_wh: tuple[int, int]
) -> tuple[np.ndarray, np.ndarray | None, np.ndarray]:
    """
    Parse bounding boxes from Florence-2 model results.

    Args:
        result: Dictionary containing Florence-2 model output
        resolution_wh: Target resolution (width, height) for scaling coordinates

    Returns:
        Tuple of (xyxy, class_names, confidence_scores)
    """

def from_google_gemini_2_0(
    result: str,
    resolution_wh: tuple[int, int],
    classes: list[str] | None = None
) -> tuple[np.ndarray, np.ndarray | None, np.ndarray]:
    """
    Parse bounding boxes from Google Gemini 2.0 formatted text.

    Args:
        result: String containing Gemini 2.0 formatted locations and labels
        resolution_wh: Target resolution (width, height) for scaling coordinates
        classes: Optional list of valid class names for filtering

    Returns:
        Tuple of (xyxy, class_names, confidence_scores)
    """

def from_google_gemini_2_5(
    result: str,
    resolution_wh: tuple[int, int],
    classes: list[str] | None = None
) -> tuple[np.ndarray, np.ndarray | None, np.ndarray]:
    """
    Parse bounding boxes from Google Gemini 2.5 formatted text.

    Args:
        result: String containing Gemini 2.5 formatted locations and labels
        resolution_wh: Target resolution (width, height) for scaling coordinates
        classes: Optional list of valid class names for filtering

    Returns:
        Tuple of (xyxy, class_names, confidence_scores)
    """

def from_moondream(
    result: dict,
    resolution_wh: tuple[int, int]
) -> tuple[np.ndarray, np.ndarray | None, np.ndarray]:
    """
    Parse bounding boxes from Moondream model results.

    Args:
        result: Dictionary containing Moondream model output
        resolution_wh: Target resolution (width, height) for scaling coordinates

    Returns:
        Tuple of (xyxy, class_names, confidence_scores)
    """
```

## Usage Examples

### Using PaliGemma for Object Detection

```python
import supervision as sv
import numpy as np

# PaliGemma result string
paligemma_result = "person <loc_123><loc_456><loc_789><loc_234> car <loc_345><loc_567><loc_890><loc_123>"

# Parse the results
xyxy, class_names, confidence = sv.from_paligemma(
    result=paligemma_result,
    resolution_wh=(1280, 720),
    classes=["person", "car", "bicycle"]  # Optional filtering
)

# Create Detections object
detections = sv.Detections(
    xyxy=xyxy,
    class_id=np.arange(len(xyxy)),
    confidence=confidence
)

print(f"Found {len(detections)} objects")
```

### Working with Florence-2 Model

```python
import supervision as sv

# Florence-2 model result dictionary
florence_result = {
    "<OD>": {
        "bboxes": [[100, 200, 300, 400], [500, 100, 800, 300]],
        "labels": ["person", "car"]
    }
}

# Parse Florence-2 results
xyxy, class_names, confidence = sv.from_florence_2(
    result=florence_result,
    resolution_wh=(1920, 1080)
)

# Create detections
detections = sv.Detections(
    xyxy=xyxy,
    class_id=np.arange(len(xyxy)),
    confidence=confidence
)

# Annotate the image
box_annotator = sv.BoxAnnotator()
label_annotator = sv.LabelAnnotator()

annotated_image = box_annotator.annotate(image, detections)
annotated_image = label_annotator.annotate(annotated_image, detections)
```

### Validating VLM Parameters

```python
import supervision as sv

# Validate VLM configuration
try:
    vlm = sv.validate_vlm_parameters(
        vlm="florence_2",
        result={"<OD>": {"bboxes": [], "labels": []}},
        kwargs={"resolution_wh": (640, 480)}
    )
    print(f"Valid VLM: {vlm}")
except ValueError as e:
    print(f"Invalid VLM configuration: {e}")
```

### Integration with Detections.from_* Methods

The VLM parsers can be used with the core Detections class through custom integration:

```python
import supervision as sv

def create_detections_from_vlm(vlm_type: str, result, **kwargs):
    """Helper function to create Detections from VLM results."""
    
    if vlm_type == "paligemma":
        xyxy, class_names, confidence = sv.from_paligemma(result, **kwargs)
    elif vlm_type == "florence_2":
        xyxy, class_names, confidence = sv.from_florence_2(result, **kwargs)
    # Add other VLM types...
    
    return sv.Detections(
        xyxy=xyxy,
        confidence=confidence,
        class_id=np.arange(len(xyxy)) if len(xyxy) > 0 else np.array([])
    )

# Usage
detections = create_detections_from_vlm(
    vlm_type="paligemma",
    result=paligemma_result,
    resolution_wh=(1280, 720),
    classes=["person", "car"]
)
```

## Supported Tasks

### Florence-2 Supported Tasks

Florence-2 supports multiple computer vision tasks through different task prompts:

- `<OD>`: Object Detection
- `<CAPTION_TO_PHRASE_GROUNDING>`: Caption to phrase grounding
- `<DENSE_REGION_CAPTION>`: Dense region captioning
- `<REGION_PROPOSAL>`: Region proposal generation
- `<OCR_WITH_REGION>`: OCR with region detection
- `<REFERRING_EXPRESSION_SEGMENTATION>`: Referring expression segmentation
- `<REGION_TO_SEGMENTATION>`: Region to segmentation
- `<OPEN_VOCABULARY_DETECTION>`: Open vocabulary detection
- `<REGION_TO_CATEGORY>`: Region to category classification
- `<REGION_TO_DESCRIPTION>`: Region to description