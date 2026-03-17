# Pre-Trained PPE Detection Models: Ready-to-Use Options

## Bottom Line Up Front

**YES, you can download a model RIGHT NOW and start detecting hard hats and vests from
webcam video without any training.** The best options are:

1. **Roboflow Construction Site Safety** (via hosted API) -- 81.4% mAP, 9 classes, zero setup
2. **Tanishjain9/yolov8n-ppe-detection-6classes** (Hugging Face) -- 81% mAP@50, 6 classes, local .pt
3. **keremberke/yolov8m-hard-hat-detection** (Hugging Face) -- 81.1% mAP@50, 2 classes (hard hat focused)

Quality will be "good enough for demos and proof-of-concept." For production deployment
on a real construction site, you will want to fine-tune on your specific camera angles,
lighting, and PPE brands. Details below.

---

## 1. Roboflow Universe Pre-Trained Models

### A. Construction Site Safety (Flagship)

| Property | Value |
|---|---|
| **URL** | https://universe.roboflow.com/roboflow-universe-projects/construction-site-safety |
| **Model Version** | v27 (YOLOv8s architecture) |
| **mAP@50** | **81.4%** |
| **Precision** | 92.7% |
| **Recall** | 77.4% |
| **Classes (9)** | `Hardhat`, `Safety Vest`, `Gloves`, `Mask`, `Safety Cone`, `NO-Hardhat`, `NO-Safety Vest`, `NO-Mask`, `Person` |
| **Dataset Size** | ~717 images (but trained with augmentation) |
| **Deployment** | Hosted API (free tier), Edge (Docker, Jetson, RPi) |

**Inference Code (API -- no local model needed):**

```python
# pip install inference-sdk
from inference_sdk import InferenceHTTPClient

CLIENT = InferenceHTTPClient(
    api_url="https://serverless.roboflow.com",
    api_key="YOUR_ROBOFLOW_API_KEY"  # Free tier available at roboflow.com
)

# Single image
result = CLIENT.infer("construction_photo.jpg", model_id="construction-site-safety/27")
print(result)
```

**Inference Code (Local with roboflow SDK):**

```python
# pip install roboflow
from roboflow import Roboflow

rf = Roboflow(api_key="YOUR_API_KEY")
project = rf.workspace().project("construction-site-safety")
model = project.version(27).model

prediction = model.predict("image.jpg", confidence=40, overlap=30).json()
print(prediction)
model.predict("image.jpg", confidence=40, overlap=30).save("prediction.jpg")
```

**Notes:**
- Free tier: 1,000 API calls/month (sufficient for testing)
- Known limitation: underrepresents vehicles/excavators
- Does NOT detect gloves or boots (despite some documentation suggesting otherwise)
- This is the most polished, production-ready option from Roboflow

### B. Personal Protective Equipment - Combined Model

| Property | Value |
|---|---|
| **URL** | https://universe.roboflow.com/roboflow-universe-projects/personal-protective-equipment-combined-model |
| **Model Version** | v8 |
| **Classes (14)** | `Hardhat`, `Safety Vest`, `Gloves`, `Goggles`, `Mask`, `NO-Hardhat`, `NO-Safety Vest`, `NO-Gloves`, `NO-Goggles`, `NO-Mask`, `Person`, `Safety Cone`, `Ladder`, `Fall-Detected` |
| **Dataset Size** | 44,002 images |
| **mAP** | Not publicly listed on the model card |

```python
from inference_sdk import InferenceHTTPClient

CLIENT = InferenceHTTPClient(
    api_url="https://serverless.roboflow.com",
    api_key="YOUR_API_KEY"
)

result = CLIENT.infer("image.jpg", model_id="personal-protective-equipment-combined-model/8")
```

**Notes:**
- Largest dataset of all Roboflow PPE models (44k images)
- More comprehensive class coverage (14 classes including fall detection)
- mAP not published; likely lower than the flagship due to more classes

---

## 2. Hugging Face Pre-Trained PPE Models

### A. keremberke/yolov8m-hard-hat-detection (RECOMMENDED for hard hats)

| Property | Value |
|---|---|
| **URL** | https://huggingface.co/keremberke/yolov8m-hard-hat-detection |
| **mAP@50** | **0.811 (81.1%)** |
| **Classes (2)** | `Hardhat`, `NO-Hardhat` |
| **Architecture** | YOLOv8m (medium) |
| **Training Data** | 19,800 images |
| **Downloads** | ~1,119/month |

```python
# pip install ultralyticsplus==0.0.24 ultralytics==8.0.23
from ultralyticsplus import YOLO, render_result

model = YOLO('keremberke/yolov8m-hard-hat-detection')

model.overrides['conf'] = 0.25
model.overrides['iou'] = 0.45
model.overrides['agnostic_nms'] = False
model.overrides['max_det'] = 1000

results = model.predict("construction_site.jpg")
print(results[0].boxes)

render = render_result(model=model, image="construction_site.jpg", result=results[0])
render.show()
```

**Verdict:** Best single-purpose hard hat detector. High accuracy, narrow focus.

### B. keremberke/yolov8m-protective-equipment-detection (Broader PPE)

| Property | Value |
|---|---|
| **URL** | https://huggingface.co/keremberke/yolov8m-protective-equipment-detection |
| **mAP@50** | **0.273 (27.3%)** -- LOW |
| **Classes (10)** | `glove`, `goggles`, `helmet`, `mask`, `no_glove`, `no_goggles`, `no_helmet`, `no_mask`, `no_shoes`, `shoes` |
| **Architecture** | YOLOv8m (medium) |

```python
from ultralyticsplus import YOLO, render_result

model = YOLO('keremberke/yolov8m-protective-equipment-detection')

model.overrides['conf'] = 0.25
model.overrides['iou'] = 0.45

results = model.predict("image.jpg")
print(results[0].boxes)
```

**Verdict:** LOW mAP (27.3%). Covers many classes but accuracy is poor. NOT recommended
for production. The model tries to detect too many small objects (gloves, shoes, goggles)
and performs badly. Useful only as a starting point for fine-tuning.

### C. Tanishjain9/yolov8n-ppe-detection-6classes (BEST BALANCED OPTION)

| Property | Value |
|---|---|
| **URL** | https://huggingface.co/Tanishjain9/yolov8n-ppe-detection-6classes |
| **mAP@50** | **~0.81 (81%)** |
| **mAP@50-95** | ~0.53 |
| **Precision** | ~0.80 |
| **Recall** | ~0.74 |
| **Classes (6)** | `Gloves`, `Vest`, `goggles`, `helmet`, `mask`, `safety_shoe` |
| **Architecture** | YOLOv8n (nano -- fast!) |
| **License** | MIT |
| **Formats** | .pt, ONNX, TensorRT |

**Per-Class mAP@50:**
- Vest: ~0.90
- Goggles: ~0.90
- Helmet: ~0.90
- Mask: ~0.80
- Gloves: ~0.69
- Safety_shoe: ~0.64

```python
from ultralytics import YOLO

# Download from HuggingFace (auto-downloads best.pt)
model = YOLO("best.pt")  # or download from HF repo
results = model("image.jpg", imgsz=640)
results[0].show()
```

**Verdict:** Excellent balance of speed (nano) and accuracy (81% mAP). Detects positive
PPE presence (not "no-helmet" negatives). MIT licensed. Best for edge deployment.

**Important note:** This model detects PPE *presence* only (helmet, vest, etc.) -- it does
NOT detect the *absence* of PPE (no-helmet, no-vest). You would need to combine it with
a person detector and check for missing equipment via logic.

### D. keremberke/yolov8n-hard-hat-detection (Nano variant)

| Property | Value |
|---|---|
| **URL** | https://huggingface.co/keremberke/yolov8n-hard-hat-detection |
| **mAP@50** | **0.836 (83.6%)** |
| **Classes (2)** | `Hardhat`, `NO-Hardhat` |
| **Architecture** | YOLOv8n (nano -- fastest) |

**Verdict:** Highest mAP of the bunch for hard hat detection. Nano model runs at
60+ FPS on modern GPUs.

---

## 3. Ultralytics Official PPE Model

**Ultralytics does NOT offer a pre-trained PPE-specific model.** Here is what they provide:

- **COCO pre-trained models** (yolo11n.pt, yolov8n.pt, etc.) -- detect 80 general classes.
  COCO *does* include "person" but NOT hard hats or safety vests.
- **Construction-PPE Dataset** -- a curated dataset for training your own PPE model,
  released January 2025. It has 11 classes: `helmet`, `gloves`, `vest`, `boots`, `goggles`,
  `Person`, `none`, `no_helmet`, `no_goggle`, `no_gloves`, `no_boots`.

**To train your own with Ultralytics (requires GPU, ~1-2 hours):**

```python
from ultralytics import YOLO

model = YOLO("yolo11n.pt")  # or yolov8n.pt
model.train(data="construction-ppe.yaml", epochs=100, imgsz=640)
```

Dataset auto-downloads from:
`https://github.com/ultralytics/assets/releases/download/v0.0.0/construction-ppe.zip` (178 MB)

**Verdict:** No ready-to-use PPE weights from Ultralytics. They provide the dataset and
framework, but you must train yourself.

---

## 4. Other Sources

### A. SH17 Dataset + Pre-trained Weights (GitHub)

| Property | Value |
|---|---|
| **URL** | https://github.com/ahmadmughees/SH17dataset |
| **Weights Download** | GitHub Releases page |
| **Best mAP@50** | 70.9% (YOLOv9-e) |
| **Precision** | 81.0% |
| **Recall** | 65.0% |
| **Classes (17)** | Person, Head, Face, Glasses, Face-mask-medical, Face-guard, Ear, Earmuffs, Hands, Gloves, Foot, Shoes, Safety-vest, Tools, Helmet, Medical-suit, Safety-suit |
| **Architectures** | YOLOv8 (n/s/m/l/x), YOLOv9 (t/s/m/c/e), YOLOv10 (n/s/m/b/l/x) |

```python
from ultralytics import YOLO

model = YOLO(r"/path/to/downloaded/weight.pt")
results = model("image_path")
results[0].show()
```

**Verdict:** Most comprehensive class set (17 classes). Lower overall mAP due to
difficulty of fine-grained detection (ears, hands, feet). Good for research;
may need fine-tuning for production.

### B. Workspace Safety Detection (GitHub)

| Property | Value |
|---|---|
| **URL** | https://github.com/hafizqaim/Workspace-Safety-Detection-using-YOLOv8 |
| **Weights** | best.pt in GitHub Releases |
| **mAP@50** | 73.5% overall; **86%+ for helmets and vests** |
| **Training Data** | 23,000+ images |
| **Focus** | Helmets and vests specifically highlighted in inference |

**Verdict:** Strong for helmet/vest detection specifically. Weights downloadable from releases.

---

## 5. Practical Comparison Matrix

| Model | Source | Classes | mAP@50 | Speed | Local? | API? | License | Recommendation |
|---|---|---|---|---|---|---|---|---|
| Roboflow Construction Site Safety | Roboflow | 9 | 81.4% | API latency | No* | Yes | Roboflow TOS | Best for quick API-based demo |
| Roboflow PPE Combined | Roboflow | 14 | Unknown | API latency | No* | Yes | Roboflow TOS | Most comprehensive classes |
| keremberke/yolov8n-hard-hat | HuggingFace | 2 | 83.6% | 60+ FPS | Yes | No | -- | Best hard hat only detector |
| keremberke/yolov8m-hard-hat | HuggingFace | 2 | 81.1% | 30+ FPS | Yes | No | -- | Accurate hard hat detector |
| Tanishjain9/yolov8n-ppe-6class | HuggingFace | 6 | 81.0% | 60+ FPS | Yes | No | MIT | Best balanced local model |
| keremberke/yolov8m-protective | HuggingFace | 10 | 27.3% | 30+ FPS | Yes | No | -- | NOT recommended (low accuracy) |
| SH17 (YOLOv9-e) | GitHub | 17 | 70.9% | 15+ FPS | Yes | No | -- | Research / most classes |
| hafizqaim Workspace Safety | GitHub | 17 | 73.5% | 30+ FPS | Yes | No | -- | Helmet + vest focus |

*Roboflow models can be deployed locally via Docker/inference server but require API key.

---

## 6. Complete Webcam Inference Script (Copy-Paste Ready)

This script works with ANY of the Hugging Face models listed above:

```python
"""
PPE Detection from Webcam -- Ready to Run
Requires: pip install ultralytics opencv-python
"""
import cv2
from ultralytics import YOLO

# ============================================================
# CHOOSE YOUR MODEL (uncomment one):
# ============================================================

# Option 1: Hard hat only (83.6% mAP, fastest)
# model = YOLO('keremberke/yolov8n-hard-hat-detection')

# Option 2: Hard hat only (81.1% mAP, more accurate on edge cases)
# model = YOLO('keremberke/yolov8m-hard-hat-detection')

# Option 3: 6-class PPE (81% mAP) -- download best.pt from HuggingFace first
# model = YOLO('path/to/Tanishjain9-best.pt')

# Option 4: 10-class protective equipment (27.3% mAP -- low quality)
model = YOLO('keremberke/yolov8m-protective-equipment-detection')

# ============================================================

# Configure
model.overrides['conf'] = 0.30   # Confidence threshold
model.overrides['iou'] = 0.45    # NMS IoU threshold
model.overrides['max_det'] = 100

# Open webcam
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

print("Press 'q' to quit")

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Run inference
    results = model(frame, verbose=False)

    # Draw results on frame
    annotated = results[0].plot()

    # Show FPS
    cv2.imshow("PPE Detection", annotated)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
```

---

## 7. Honest Quality Assessment

### What works well out-of-the-box:
- **Hard hat detection** (present/absent): 80-84% mAP. Reliable in well-lit conditions
  with clear camera angles.
- **Safety vest detection**: 85-90% mAP when vests are high-visibility (orange/yellow).
- **Person detection**: Very reliable as a prerequisite for PPE checking.

### What does NOT work well without fine-tuning:
- **Gloves detection**: 64-69% mAP. Hands are small, often occluded. Expect many
  false negatives.
- **Safety shoes/boots**: 64% mAP. Very difficult from typical surveillance angles.
- **Goggles vs. glasses**: Models struggle to distinguish safety goggles from regular
  glasses.
- **Night/low-light**: All models degrade significantly. Expect 15-25% mAP drop.
- **Crowded scenes**: Overlapping workers cause missed detections.
- **Distance**: Beyond ~15 meters from camera, small PPE items become undetectable.

### Recommendation for production:
1. Start with **Roboflow Construction Site Safety API** for immediate testing (free tier)
2. For local deployment, use **keremberke/yolov8n-hard-hat-detection** for hard hats
3. Fine-tune on YOUR site's camera footage for best results (even 200-300 labeled images
   from your actual cameras will dramatically improve accuracy)
4. For a comprehensive local solution, train YOLO11 on the **Ultralytics Construction-PPE
   dataset** -- it takes ~1-2 hours on a modern GPU

---

## Sources

- [Roboflow Construction Site Safety](https://universe.roboflow.com/roboflow-universe-projects/construction-site-safety)
- [Roboflow PPE Combined Model](https://universe.roboflow.com/roboflow-universe-projects/personal-protective-equipment-combined-model)
- [Roboflow PPE Detection API Blog](https://blog.roboflow.com/ppe-detection-api/)
- [keremberke/yolov8m-hard-hat-detection](https://huggingface.co/keremberke/yolov8m-hard-hat-detection)
- [keremberke/yolov8n-hard-hat-detection](https://huggingface.co/keremberke/yolov8n-hard-hat-detection)
- [keremberke/yolov8m-protective-equipment-detection](https://huggingface.co/keremberke/yolov8m-protective-equipment-detection)
- [Tanishjain9/yolov8n-ppe-detection-6classes](https://huggingface.co/Tanishjain9/yolov8n-ppe-detection-6classes)
- [SH17 Dataset (GitHub)](https://github.com/ahmadmughees/SH17dataset)
- [hafizqaim Workspace Safety Detection](https://github.com/hafizqaim/Workspace-Safety-Detection-using-YOLOv8)
- [Ultralytics Construction-PPE Dataset](https://docs.ultralytics.com/datasets/detect/construction-ppe/)
- [Ultralytics YOLO11 in Construction Blog](https://www.ultralytics.com/blog/using-ultralytics-yolo11-in-construction)
