# PPE Detection for Construction Sites: Technical Research Report
**Date:** 2026-02-24 | **Purpose:** Design input for commercial construction site safety system

---

## 1. Pre-trained Models on Roboflow Universe

### Top Datasets & Models

| Dataset / Model | Classes | Images | Format | Notes |
|----------------|---------|--------|--------|-------|
| **Construction Site Safety** (Roboflow Universe Projects) | Hard-hat, Safety-vest, Person | 717 | YOLOv5/v8/v11 TXT + YAML | v27 trained with YOLOv8s; v28 with YOLOv5s |
| **Construction PPE Detection** (Huiyao Hu) | Boots, Gloves, Helmet, Human, Vest | ~500+ | YOLOv8 compatible | 5-class model with gloves |
| **PPE Detection** (KinetixPro) | Multiple PPE classes | 1,000 | YOLOv8 | Pre-trained model + API available |
| **Hard Hat Universe** (Universe Datasets) | Safety Helmet, Safety Vest | 8,100 | YOLOv5-v11 | Large dataset, good for fine-tuning |
| **PPE Detection with YOLOv8** (school) | PPE classes | 1,000 | YOLOv8 | Pre-trained model available |
| **Construction-PPE** (Ultralytics official) | 11 classes: helmet, gloves, vest, boots, goggles, none, Person, no_helmet, no_goggle, no_gloves, no_boots | 1,416 (1132 train / 143 val / 141 test) | YOLO native | Dual-labeling (worn + not-worn); 178.4 MB download |
| **SH17 Dataset** (Academic) | 17 classes across 5 body-part categories (head, upper body, hands, feet, whole body) | 8,099 images / 75,994 instances | Multiple | YOLOv9-e achieved 70.9% mAP; CC BY-NC-SA 4.0 license |

### Key Observations
- The **Ultralytics Construction-PPE dataset** is the most complete for compliance monitoring (detects both presence AND absence of PPE).
- The **SH17 dataset** is the largest academic PPE dataset (17 classes, 8K+ images) but is licensed CC BY-NC-SA 4.0 (non-commercial).
- **Hard Hat Universe** (8.1K images) is the largest open dataset focused on helmets/vests.
- Most Roboflow datasets export directly to YOLOv8/YOLO11 format with one click.
- Specific mAP scores are typically not published on Roboflow Universe model cards; you must evaluate on your own validation set.

### Download Example (Roboflow)
```python
from roboflow import Roboflow
rf = Roboflow(api_key="YOUR_KEY")
project = rf.workspace("roboflow-universe-projects").project("construction-site-safety")
dataset = project.version(27).download("yolov8")
```

---

## 2. YOLOv8 vs YOLO11 for PPE Detection

### Model Comparison Tables

**YOLOv8 Detection Models (COCO val2017)**

| Model | mAP50-95 | CPU ONNX (ms) | A100 TRT (ms) | Params (M) | FLOPs (B) |
|-------|----------|---------------|---------------|------------|-----------|
| YOLOv8n | 37.3 | 80.4 | 0.99 | 3.2 | 8.7 |
| YOLOv8s | 44.9 | 128.4 | 1.20 | 11.2 | 28.6 |
| YOLOv8m | 50.2 | 234.7 | 1.83 | 25.9 | 78.9 |
| YOLOv8l | 52.9 | 375.2 | 2.39 | 43.7 | 165.2 |
| YOLOv8x | 53.9 | 479.1 | 3.53 | 68.2 | 257.8 |

**YOLO11 Detection Models (COCO val2017)**

| Model | mAP50-95 | CPU ONNX (ms) | T4 TRT10 (ms) | Params (M) | FLOPs (B) |
|-------|----------|---------------|---------------|------------|-----------|
| YOLO11n | 39.5 | 56.1 | 1.5 | 2.6 | 6.5 |
| YOLO11s | 47.0 | 90.0 | 2.5 | 9.4 | 21.5 |
| YOLO11m | 51.5 | 183.2 | 4.7 | 20.1 | 68.0 |
| YOLO11l | 53.4 | 238.6 | 6.2 | 25.3 | 86.9 |
| YOLO11x | 54.7 | 462.8 | 11.3 | 56.9 | 194.9 |

### Head-to-Head Comparison

| Metric | YOLOv8m | YOLO11m | Delta |
|--------|---------|---------|-------|
| mAP50-95 | 50.2 | 51.5 | +1.3 |
| Parameters | 25.9M | 20.1M | **-22%** |
| FLOPs | 78.9B | 68.0B | -14% |
| CPU Latency | 234.7ms | 183.2ms | -22% |

### License: AGPL-3.0
- **Both YOLOv8 and YOLO11** are released under AGPL-3.0.
- **Commercial implication:** Any software that uses Ultralytics YOLO (including trained weights) must be open-sourced under AGPL-3.0, OR you must purchase an Ultralytics Enterprise License.
- **Enterprise License:** Removes open-source requirement; allows private deployment and proprietary use. Pricing is not public -- contact sales@ultralytics.com.
- **Trained weights inherit the license.** Even if you train on your own data, the resulting model is AGPL-3.0 because it derives from AGPL-3.0 code.

### Recommendation for PPE
- **YOLO11s** is the sweet spot for edge PPE detection: 47.0 mAP on COCO, 9.4M params, 2.5ms on T4.
- **YOLO11m** if accuracy is prioritized: 51.5 mAP, still 22% lighter than YOLOv8m.
- Use YOLO11 over YOLOv8 -- it is strictly better at every model size.

---

## 3. Apache 2.0 Licensed Alternatives

### Option A: RF-DETR (Roboflow) -- RECOMMENDED

Released March 2025, accepted at ICLR 2026. Uses DINOv2 vision transformer backbone.

| Model | mAP50 | mAP50-95 | T4 TRT FP16 (ms) | Params (M) | Resolution | License |
|-------|-------|----------|-------------------|------------|------------|---------|
| RF-DETR Nano | 67.6 | 48.4 | 2.3 | 30.5 | 384x384 | Apache 2.0 |
| RF-DETR Small | 72.1 | 53.0 | 3.5 | 32.1 | 512x512 | Apache 2.0 |
| RF-DETR Medium | 73.6 | 54.7 | 4.4 | 33.7 | 576x576 | Apache 2.0 |
| RF-DETR Large | 75.1 | 56.5 | 6.8 | 33.9 | 704x704 | Apache 2.0 |
| RF-DETR XLarge | 77.4 | 58.6 | 11.5 | 126.4 | 700x700 | PML 1.0* |
| RF-DETR 2XLarge | 78.5 | 60.1 | 17.2 | 126.9 | 880x880 | PML 1.0* |

*PML 1.0 = Roboflow's proprietary model license for XLarge+ variants.

Key advantage: **RF-DETR Small beats YOLO11x** (53.0 vs 54.7 mAP50-95) while being **3.4x faster** (3.5ms vs 11.3ms).

```python
pip install rfdetr
from rfdetr import RFDETRBase
model = RFDETRBase()
model.train(dataset_dir="path/to/dataset", epochs=50)
```

### Option B: RT-DETR (Baidu / PaddlePaddle)

| Model | mAP50-95 (COCO) | FPS on T4 | License |
|-------|-----------------|-----------|---------|
| RT-DETR-L | 53.0 | 114 | Apache 2.0 |
| RT-DETR-X | 54.8 | 74 | Apache 2.0 |

- No NMS required (end-to-end detection).
- Available through both PaddlePaddle and Ultralytics (WARNING: Ultralytics wrapper is AGPL-3.0; use the official PaddlePaddle implementation for Apache 2.0).
- RT-DETRv3 and v4 released with further improvements.

### Option C: YOLOX (Megvii)

| Property | Detail |
|----------|--------|
| License | **Apache 2.0** |
| Architecture | Anchor-free, decoupled head, SimOTA assignment |
| Best PPE result | YOLOX-m achieved 89.84% mAP for PPE detection in published research |
| Pre-trained models | COCO weights available; no PPE-specific weights published |
| Maintenance status | Low activity -- last significant update was 2022; community reports it is not actively maintained |
| Edge deployment | Supports TensorRT, ONNX, ncnn, OpenVINO |

**WARNING:** YOLOX is largely unmaintained. While the Apache 2.0 license is ideal, the lack of active development makes it risky for a production system.

**WARNING:** MMDetection (open-mmlab) includes YOLOX configs but MMYOLO is released under **GPL 3.0** -- check which package you use.

### Option D: Other Alternatives

| Model | License | Status |
|-------|---------|--------|
| D-FINE | Apache 2.0 | Strong COCO performance; less community adoption |
| LW-DETR | Apache 2.0 | Lightweight DETR variant |
| YOLO-NAS (Deci.ai) | Custom (free for research) | Requires Deci license for commercial |

### Practical Recommendation

For a **commercial construction safety product avoiding AGPL**:
1. **Primary choice: RF-DETR Small/Medium** -- Best accuracy/speed, Apache 2.0, actively maintained, ICLR-accepted.
2. **Backup: RT-DETR-L** (PaddlePaddle native) -- Proven, fast, Apache 2.0, but PaddlePaddle ecosystem is less familiar to most teams.
3. **Avoid YOLOX** for new projects unless you have existing infrastructure.

---

## 4. Glove Detection Challenges

### Why Glove Detection is Hard

| Challenge | Description |
|-----------|-------------|
| **Small object size** | Gloves occupy a tiny fraction of the image (often < 32x32 px at typical surveillance distances) |
| **Frequent occlusion** | Hands are occluded by tools, materials, other body parts, or railings |
| **Visual similarity** | Work gloves can blend with skin tones or dirty construction environments |
| **Pose variation** | Hands appear in highly varied poses -- gripping, pointing, hanging, folded |
| **Distance from camera** | Standard overhead cameras place gloves at the far edge of detectable size |
| **Dynamic backgrounds** | Construction sites have cluttered, constantly changing backgrounds |
| **Weather/lighting** | Rain, dust, shadows, and harsh sunlight degrade visibility |

### Best Practices for Improving Glove Detection

1. **Camera placement:** Mount cameras at entry/exit points or tool cribs where workers' hands are close to the camera (1-3m distance). Avoid distant overhead angles for glove detection.
2. **Resolution:** Use at least 1080p cameras; crop ROI (Region of Interest) to the hand region to increase effective resolution.
3. **Two-stage detection:** First detect persons, then crop hand regions and run a specialized glove classifier on the crop. This dramatically improves accuracy for small objects.
4. **Specialized architecture:** YOLOv8-AFPN-M-C2f (published 2024) substitutes the YOLOv8 head with AFPN-M-C2f network and adds a shallow feature layer, yielding +2.6% mAP50, +63.8% FPS, and -13% parameters compared to baseline YOLOv8.
5. **Data augmentation:** Heavy mosaic augmentation, copy-paste augmentation of gloved/ungloved hands, and targeted data collection at hand-level.
6. **Negative class labeling:** Include "no_gloves" / "bare_hand" as explicit classes (as in the Ultralytics Construction-PPE dataset).

### Available Glove Detection Datasets

| Dataset | Images | Classes | Source |
|---------|--------|---------|--------|
| Hand in Glove Detection (Roboflow) | 1,290 | glove, no-glove | universe.roboflow.com |
| Glove Detection (Roboflow) | 1,084 | glove classes + pre-trained model | universe.roboflow.com |
| Gloves and Bare Hands (Roboflow) | 868 | glove, bare hand | universe.roboflow.com |
| Construction-PPE (Ultralytics) | 1,416 | gloves, no_gloves (among 11 total) | docs.ultralytics.com |
| SH17 | 8,099 | hand/glove categories (among 17 total) | CC BY-NC-SA 4.0 |

### Recommended Approach for Production
- Use **person detection** (high accuracy) as the first stage.
- Crop the lower-body/hand region based on detected person bounding box.
- Run a **dedicated glove classifier** (binary: gloves vs no-gloves) on the crop at higher resolution.
- For entry-point monitoring, use a **dedicated low-mount camera** at ~1.5m height aimed at hand level.

---

## 5. MediaPipe Pose vs YOLOv8-Pose / YOLO11-Pose

### Comparison Table

| Feature | MediaPipe Pose | YOLOv8-Pose / YOLO11-Pose |
|---------|---------------|---------------------------|
| **License** | Apache 2.0 | AGPL-3.0 |
| **Keypoints** | 33 (full body + face + hands + feet) | 17 (COCO body keypoints) |
| **Multi-person** | Single person only (requires person detector first) | Native multi-person |
| **Input resolution** | 256x256 (optimized) | 640x640 (default) |
| **Edge performance** | Excellent (designed for mobile/edge) | Good with TensorRT |
| **Occlusion handling** | Moderate | Superior (better in crowded scenes) |
| **3D estimation** | Yes (33 3D landmarks) | 2D only (x, y, confidence) |
| **Framework** | TensorFlow Lite / MediaPipe Tasks | PyTorch / ONNX / TensorRT |

### For Fall Detection Integration

| Consideration | MediaPipe | YOLO-Pose |
|---------------|-----------|-----------|
| Sufficient keypoints for fall detection? | Yes (33 is more than enough) | Yes (17 covers all major joints) |
| Extra keypoints useful? | Face/hand keypoints not needed for falls | 17 body keypoints are sufficient |
| Processing overhead | Lower (smaller input, optimized pipeline) | Higher (640x640 input) |
| Multi-worker scenarios | Needs separate person detector | Built-in multi-person |
| Commercial license | Apache 2.0 (free) | AGPL-3.0 (requires enterprise license) |

### Recommended Architecture for PPE + Fall Detection

**If using Ultralytics (with Enterprise License):**
- YOLO11-Pose for both PPE bbox extraction and fall detection in one pass
- Simplest pipeline; one model handles both tasks

**If Apache 2.0 is required:**
- **RF-DETR** for PPE object detection (Apache 2.0)
- **MediaPipe Pose** for fall detection (Apache 2.0)
- Hybrid pipeline: RF-DETR detects persons + PPE, MediaPipe runs pose estimation on detected persons
- Published research shows this hybrid approach achieves 96.06% accuracy and 100% recall for fall detection at ~20 FPS on average hardware

---

## 6. Inference Performance on Edge Devices

### YOLOv8 on Jetson Devices (640x640, TensorRT)

**Jetson Orin Nano (8GB)**

| Model | FP16 (FPS) | INT8 (FPS) | Notes |
|-------|-----------|-----------|-------|
| YOLOv8n | ~25-35 | ~40-50 | Suitable for real-time single-stream |
| YOLOv8s | ~15-20 | ~25-35 | Marginal for real-time |
| YOLOv8m | ~8-12 | ~15-20 | Not real-time; batch processing only |

**Jetson Orin NX (16GB)**

| Model | FP16 (FPS) | INT8 (FPS) | Notes |
|-------|-----------|-----------|-------|
| YOLOv8n | ~40-55 | ~55-65 | Comfortable real-time |
| YOLOv8s | ~25-35 | ~35-50 | Real-time capable |
| YOLOv8m | ~15-20 | ~20-30 | Near real-time |

**Jetson AGX Orin (32GB)**

| Model | FP16 (FPS) | INT8 (FPS) | Notes |
|-------|-----------|-----------|-------|
| YOLOv8n | ~100+ | ~130+ | Multi-stream capable |
| YOLOv8s | ~60-80 | ~80-100 | Comfortable real-time |
| YOLOv8m | ~35-50 | ~50-70 | Real-time capable |
| YOLOv8x | ~25-35 | ~60-75 | Real-time at INT8 |

*Note: These are approximate ranges compiled from multiple benchmark sources (Seeed Studio, NVIDIA forums, academic papers). Actual FPS depends on pipeline overhead (pre/post processing, NMS, video decode). At 640x480 (vs 640x640), expect ~10-15% higher FPS due to reduced pixel count.*

### Simultaneous PPE Detection + Pose Estimation

**Can it be done?** Yes, with careful pipeline design.

**Architecture options:**

| Approach | Jetson Orin Nano | Jetson AGX Orin | Combined FPS |
|----------|-----------------|-----------------|-------------|
| YOLOv8n-det + YOLOv8n-pose (sequential) | ~12-18 FPS | ~50-60 FPS | Viable on AGX |
| YOLO11n-det + MediaPipe Pose (hybrid) | ~15-22 FPS | ~40-55 FPS | Better on Nano (MediaPipe uses CPU) |
| RF-DETR Nano + MediaPipe Pose | ~10-15 FPS* | ~35-45 FPS* | *RF-DETR TRT support maturing |
| Single YOLO11s-pose (pose only, derive PPE from bbox) | ~20-30 FPS | ~60-80 FPS | Simplest but limited PPE classes |

**Optimization strategies:**
1. **DeepStream SDK:** NVIDIA's multi-stream pipeline with TensorRT backend. Handles video decode, inference, and post-processing on GPU. Supports running multiple models in the same pipeline.
2. **Async pipeline:** Run detection and pose estimation on alternating frames.
3. **ROI-based pose:** Only run pose estimation on detected persons (reduces computation).
4. **INT8 quantization:** Critical for Jetson Orin Nano -- 40-60% speedup over FP16.
5. **C++ inference:** Avoids Python GIL bottleneck; 2-3x throughput improvement over Python.

### Expected FPS at 640x480 for PPE Detection (Single Model)

| Device | YOLOv8n INT8 | YOLO11n FP16 | RF-DETR Nano FP16 |
|--------|-------------|-------------|-------------------|
| Jetson Orin Nano 8GB | 45-55 FPS | 35-45 FPS | 15-25 FPS* |
| Jetson Orin NX 16GB | 65-75 FPS | 55-65 FPS | 30-40 FPS* |
| Jetson AGX Orin 32GB | 140+ FPS | 110+ FPS | 60-80 FPS* |

*RF-DETR Jetson benchmarks are less established; transformer models historically have worse edge/TRT optimization than CNN-based YOLO. These are estimates extrapolated from T4 benchmarks.*

---

## Summary Recommendations for Commercial System Design

### Architecture Decision Matrix

| Requirement | Recommended Choice | Rationale |
|------------|-------------------|-----------|
| License must be Apache 2.0 | RF-DETR Small + MediaPipe Pose | Best-in-class accuracy with permissive license |
| Maximum edge FPS | YOLO11n + INT8 + TensorRT | Smallest, fastest CNN model with best edge support |
| Best PPE accuracy | YOLO11m or RF-DETR Medium | 51.5+ mAP on COCO; fine-tune on Construction-PPE |
| Glove detection | Two-stage: person detector + hand-crop classifier | Single-stage detection unreliable for small objects |
| Fall detection | MediaPipe Pose (Apache 2.0) or YOLO11-pose (AGPL) | 33 keypoints vs 17; both sufficient for falls |
| Budget edge device | Jetson Orin Nano + YOLO11n INT8 | ~45-55 FPS single stream at 640x480 |
| Multi-camera (4-8 streams) | Jetson AGX Orin + DeepStream + YOLO11s INT8 | Handles 8+ streams at 15+ FPS each |

### Suggested Training Data Pipeline
1. Start with **Ultralytics Construction-PPE dataset** (11 classes, dual-labeled) as base.
2. Supplement with **Hard Hat Universe** (8.1K images) for helmet/vest diversity.
3. Add **Hand in Glove Detection** (1.3K images) for specialized glove training.
4. Collect **site-specific data** (500+ images per class) from your actual deployment cameras.
5. Use Roboflow for annotation, augmentation, and dataset versioning.

### Cost Considerations
- **Ultralytics Enterprise License:** Required for YOLO commercial use. Pricing is custom (contact sales). Typically $thousands/year.
- **RF-DETR (Apache 2.0):** No license cost. Free for commercial use. Nano-Large variants.
- **MediaPipe (Apache 2.0):** No license cost.
- **Roboflow:** Free tier available; paid plans for team features and deployment.

---

## Sources

- [Roboflow Universe - Construction Site Safety Dataset](https://universe.roboflow.com/roboflow-universe-projects/construction-site-safety)
- [Ultralytics YOLO11 Documentation](https://docs.ultralytics.com/models/yolo11/)
- [Ultralytics YOLOv8 Documentation](https://docs.ultralytics.com/models/yolov8/)
- [Ultralytics YOLOv8 vs YOLO11 Comparison](https://docs.ultralytics.com/compare/yolov8-vs-yolo11/)
- [Ultralytics License Page](https://www.ultralytics.com/license)
- [Ultralytics Enterprise Plans](https://www.ultralytics.com/plans)
- [Ultralytics Construction-PPE Dataset](https://docs.ultralytics.com/datasets/detect/construction-ppe/)
- [RF-DETR GitHub Repository (Apache 2.0)](https://github.com/roboflow/rf-detr)
- [RF-DETR Blog Post](https://blog.roboflow.com/rf-detr/)
- [RF-DETR Nano/Small/Medium Blog Post](https://blog.roboflow.com/rf-detr-nano-small-medium/)
- [RT-DETR Official Repository](https://github.com/lyuwenyu/RT-DETR)
- [YOLOX GitHub Repository (Apache 2.0)](https://github.com/Megvii-BaseDetection/YOLOX)
- [Best Object Detection Models 2025 (Roboflow)](https://blog.roboflow.com/best-object-detection-models/)
- [YOLOv8 Alternatives Guide (Roboflow)](https://roboflow.com/model-alternatives/yolov8)
- [Glove-Wearing Detection with Improved YOLOv8 (MDPI Sensors)](https://www.mdpi.com/1424-8220/23/24/9906)
- [SH17 Dataset for PPE Detection](https://github.com/ahmadmughees/SH17dataset)
- [SH17 Paper (arXiv)](https://arxiv.org/abs/2407.04590)
- [MediaPipe Pose Documentation](https://github.com/google-ai-edge/mediapipe/blob/master/docs/solutions/pose.md)
- [YOLO and MediaPipe Fall Detection System (ScienceDirect)](https://www.sciencedirect.com/science/article/pii/S2215016125004674)
- [MediaPipe vs YOLOv8 Pose Comparison (Springer)](https://link.springer.com/chapter/10.1007/978-3-032-00232-7_13)
- [YOLOv8 Benchmarks on Jetson (Seeed Studio)](https://www.seeedstudio.com/blog/2023/03/30/yolov8-performance-benchmarks-on-nvidia-jetson-devices/)
- [YOLOv8 on Jetson with TensorRT (Seeed Studio Wiki)](https://wiki.seeedstudio.com/YOLOv8-TRT-Jetson/)
- [Jetson Benchmarks (NVIDIA)](https://developer.nvidia.com/embedded/jetson-benchmarks)
- [Benchmarking YOLOv8 on Jetson Orin NX (MDPI)](https://www.mdpi.com/2073-431X/15/2/74)
- [YOLO11 License Information (Roboflow)](https://roboflow.com/model-licenses/yolo11)
- [YOLOX PPE Detection Study (Taylor & Francis)](https://www.tandfonline.com/doi/full/10.1080/23311916.2024.2333209)
- [YOLOv8m Protective Equipment Detection (Hugging Face)](https://huggingface.co/keremberke/yolov8m-protective-equipment-detection)
- [Roboflow Pose Estimation Guide](https://blog.roboflow.com/best-pose-estimation-models/)
- [Fall Detection with YOLOv8 and MediaPipe (GitHub)](https://github.com/InvictusRex/Fall-Detection-and-Pose-Classification)
- [Computer Vision for Construction Safety (AECbytes)](https://www.aecbytes.com/feature/2025/ComputerVision-Construction.html)
- [PPE Detection with YOLOv10 and Transformers (Nature)](https://www.nature.com/articles/s41598-025-12468-8)
