# Video Streaming Framework Research: Construction Site AI Safety Monitoring

**Date:** 2026-02-24
**Context:** Edge-deployed (Jetson / local server) system receiving 1-50 IP camera RTSP streams, running YOLO object detection (~84ms/frame), and relaying annotated live video to a web browser dashboard.

---

## Table of Contents

1. [Architecture Overview](#architecture-overview)
2. [Framework Deep-Dives](#framework-deep-dives)
3. [Comparison Table](#comparison-table)
4. [Recommended Architectures](#recommended-architectures)
5. [Final Recommendation](#final-recommendation)

---

## Architecture Overview

The target pipeline is:

```
[IP Camera] --RTSP--> [Ingestion] --frames--> [YOLO AI] --annotated--> [Web Browser]
```

Key architectural decisions:
- **Ingestion layer**: Must receive RTSP from IP cameras and decode frames
- **AI processing layer**: Must access raw frames (numpy arrays) for YOLO inference
- **Delivery layer**: Must encode annotated frames and deliver to browsers (WebRTC preferred for low latency)
- **Resilience**: Network disconnection/reconnection must be handled gracefully
- **Scale**: 1 camera (MVP) to 50 cameras (production)

---

## Framework Deep-Dives

### 1. LiveKit

**What it is:** Open-source WebRTC platform designed for real-time audio/video applications, with a strong focus on AI agent integration. Written in Go, backed by a VC-funded company.

| Attribute | Details |
|---|---|
| **License** | Apache 2.0 (commercial-friendly) |
| **RTSP Ingestion** | **No native RTSP support.** Ingress service supports RTMP and WHIP only. An [open GitHub issue (#270)](https://github.com/livekit/ingress/issues/270) requests RTSP support. Workaround: use FFmpeg to convert RTSP to RTMP, then feed to LiveKit Ingress. |
| **AI Integration** | **Excellent.** The [Agents framework](https://docs.livekit.io/agents/) lets Python programs join rooms as participants. `VideoStream` provides async iteration over raw video frames. You can process frames, run YOLO inference, draw annotations, and publish the annotated stream back via `VideoSource`. |
| **Browser Delivery** | **Excellent.** Native WebRTC delivery to browsers with mature client SDKs (JS, React, Flutter, Swift, Kotlin). |
| **Latency** | Sub-second WebRTC (typically 200-500ms glass-to-glass for relay). Add ~84ms for AI inference. |
| **Scalability** | Designed for multi-room, multi-participant scenarios. However, each RTSP camera requires an FFmpeg transcoding process, which adds CPU overhead per stream. |
| **Edge/Jetson** | Self-hostable, but recommends 4 CPU + 4GB RAM per ingress instance. Go binary runs on ARM64. The transcoding overhead for 50 RTSP-to-RTMP conversions would be significant on edge hardware. |
| **Python SDK** | [livekit/python-sdks](https://github.com/livekit/python-sdks) -- mature, well-documented, purpose-built for AI agent workflows. |
| **Maturity** | ~22k GitHub stars. Very active development. Production-used by many companies. Strong community. |
| **Complexity** | Medium-High. Requires deploying LiveKit server + Ingress service + Redis + your agent process. The RTSP workaround (FFmpeg per camera) adds operational complexity. |

**Architecture for our use case:**
```
[IP Camera] --RTSP--> [FFmpeg] --RTMP--> [LiveKit Ingress] --> [LiveKit Room]
                                                                    |
                                              [Python Agent] <------+
                                              (VideoStream -> YOLO -> VideoSource)
                                                                    |
                                              [Web Browser] <------+
                                              (WebRTC via JS SDK)
```

**Verdict:** Excellent AI agent integration and browser delivery, but the lack of native RTSP ingestion is a significant gap for an IP camera system. The FFmpeg workaround per camera is clunky and resource-intensive.

---

### 2. Janus Gateway

**What it is:** General-purpose, modular WebRTC server written in C. One of the oldest and most battle-tested WebRTC servers, developed by Meetecho.

| Attribute | Details |
|---|---|
| **License** | **GPLv3** (copyleft -- any modifications to Janus itself must be open-sourced; however, using Janus as a service alongside your proprietary code is generally considered acceptable) |
| **RTSP Ingestion** | **Yes, native.** The [Streaming plugin](https://janus.conf.meetecho.com/docs/streaming) has built-in RTSP support with reconnect handling (`rtsp_reconnect_delay`), session timeout management, and authentication. |
| **AI Integration** | **Poor for direct frame access.** Janus is a C media server that forwards RTP packets. It does not expose decoded video frames to external processes. To access frames, you would need to: (a) write a custom C plugin, (b) use RTP forwarding to a separate decoder, or (c) tap the stream externally with FFmpeg/GStreamer. |
| **Browser Delivery** | **Excellent.** Purpose-built WebRTC gateway with mature browser-side JavaScript API. |
| **Latency** | Sub-second WebRTC delivery. Janus is highly optimized as an SFU. |
| **Scalability** | Proven at scale. Efficient C implementation. Can handle many streams. |
| **Edge/Jetson** | Compiles on ARM. A dedicated [jetson-janus](https://github.com/SeanAvery/jetson-janus) Docker project exists for Jetson deployment. Lightweight C binary. |
| **Python SDK** | **No official Python SDK.** Interaction is via HTTP/WebSocket REST API or custom plugins. Python integration requires building your own signaling layer. |
| **Maturity** | ~8k+ GitHub stars. 10+ years old. Battle-tested in production by telecom companies. Active maintainer (Lorenzo Miniero). |
| **Complexity** | High. C codebase, custom plugin development requires C knowledge. Configuration is complex. The AI integration gap means you end up building significant glue code. |

**Architecture for our use case:**
```
[IP Camera] --RTSP--> [Janus Streaming Plugin] --WebRTC--> [Web Browser]
                  |
                  +--RTSP--> [FFmpeg/GStreamer] --frames--> [Python YOLO]
                                                                |
                  (Annotations sent as data channel or separate overlay stream)
```

**Verdict:** Great RTSP-to-WebRTC gateway, but the AI processing gap is a dealbreaker for this use case. You would essentially need two parallel pipelines: one for viewing and one for AI. Getting annotated frames back to the browser would require a second ingestion path.

---

### 3. MediaMTX (formerly rtsp-simple-server)

**What it is:** Zero-dependency, multi-protocol media server and proxy written in Go. Automatically converts between protocols.

| Attribute | Details |
|---|---|
| **License** | **MIT** (fully commercial-friendly) |
| **RTSP Ingestion** | **Excellent.** Purpose-built for RTSP proxying. Supports RTSP/RTSPS (UDP/TCP), multi-stream, authentication, and automatic reconnection. |
| **AI Integration** | **Indirect.** MediaMTX is a media relay, not a processing engine. It does not expose decoded frames. However, it can serve as the RTSP proxy layer, and you read from it via FFmpeg/OpenCV in your Python AI pipeline, then publish annotated streams back to MediaMTX. |
| **Browser Delivery** | **Good.** Automatic protocol conversion: any RTSP input is simultaneously available as WebRTC, HLS, LL-HLS, and RTMP. Built-in WebRTC/WHEP support for browser playback. |
| **Latency** | WebRTC path: sub-second. LL-HLS: 2-3 seconds. Standard HLS: 6-30 seconds. |
| **Scalability** | Lightweight Go binary. Handles many concurrent streams efficiently. Configuration is simple YAML. |
| **Edge/Jetson** | Single static binary, runs on ARM64/ARM. Minimal resource usage. Ideal for edge deployment. |
| **Python SDK** | No SDK needed. Python code reads RTSP from MediaMTX via OpenCV/FFmpeg, processes frames, and publishes annotated stream back to MediaMTX via RTSP/RTMP. |
| **Maturity** | ~13k+ GitHub stars. Very actively maintained. Large user base in surveillance/NVR community. |
| **Complexity** | **Very Low.** Single binary, single YAML config file. Proxying RTSP cameras is literally a few lines of config. |

**Architecture for our use case:**
```
[IP Camera] --RTSP--> [MediaMTX] --RTSP--> [Python: OpenCV + YOLO]
                          |                        |
                          |                  [Annotated RTSP/RTMP]
                          |                        |
                          +<----- publish ---------+
                          |
                    [Web Browser]
                    (WebRTC via WHEP / LL-HLS)
```

**Verdict:** Excellent as the RTSP proxy + protocol converter layer. Does not do AI processing itself, but integrates cleanly into a pipeline where Python handles AI and publishes back. The combination of MediaMTX + Python + OpenCV is a very pragmatic architecture.

---

### 4. GStreamer (+ DeepStream)

**What it is:** Low-level multimedia framework with a plugin-based pipeline architecture. NVIDIA's DeepStream SDK is built on top of GStreamer with GPU-accelerated AI inference plugins.

| Attribute | Details |
|---|---|
| **License** | **LGPL 2.1+** (commercial-friendly, can link proprietary code) |
| **RTSP Ingestion** | **Excellent.** `rtspsrc` element handles RTSP with reconnection, authentication, UDP/TCP transport. Extremely mature. |
| **AI Integration** | **Excellent (especially with DeepStream).** `appsink` exposes decoded frames as numpy arrays to Python. DeepStream's `nvinfer` plugin runs TensorRT-optimized YOLO directly in the pipeline. Direct frame access via Python bindings (GObject Introspection). |
| **Browser Delivery** | **Moderate.** `webrtcsink` element exists (Rust-based) but requires a signaling server. Not as turnkey as dedicated WebRTC servers. More commonly outputs RTSP, which then needs another layer for browser delivery. |
| **Latency** | Pipeline-internal latency is minimal (hardware-accelerated decode + inference). End-to-end depends on output method. |
| **Scalability** | DeepStream handles 8-16 streams per Jetson Orin AGX, 4-8 on Orin NX. Batched inference across streams is highly optimized. |
| **Edge/Jetson** | **Best-in-class.** DeepStream is purpose-built for Jetson. Hardware-accelerated decode (NVDEC), inference (TensorRT on GPU/DLA), and encode (NVENC). |
| **Python SDK** | GStreamer has Python bindings (`gi.repository.Gst`). DeepStream has [deepstream_python_apps](https://github.com/NVIDIA-AI-IOT/deepstream_python_apps). Learning curve is steep. |
| **Maturity** | GStreamer: 20+ years, industry standard. DeepStream: production-ready, NVIDIA-supported. |
| **Complexity** | **High.** GStreamer pipeline syntax is notoriously difficult. DeepStream adds NVIDIA-specific complexity. Debugging is challenging. However, once set up, extremely performant. |

**Architecture for our use case (DeepStream):**
```
[IP Camera] --RTSP--> [rtspsrc] --> [nvstreammux] --> [nvinfer (YOLO/TensorRT)]
                                                            |
                                                      [nvosd (overlay)]
                                                            |
                                                      [nvvideoconvert]
                                                            |
                                          +--[RTSP sink]-->[MediaMTX/go2rtc]-->[Browser WebRTC]
                                          |
                                          +--[WebRTC sink] (experimental)
```

**Verdict:** The most performant option, especially on Jetson. DeepStream is purpose-built for exactly this use case (multi-camera AI video analytics on edge). The main downsides are steep learning curve, NVIDIA lock-in, and the browser delivery gap (needs an additional relay layer for clean WebRTC).

---

### 5. FFmpeg + Custom Python Pipeline

**What it is:** Using FFmpeg (or OpenCV's FFmpeg backend) to decode RTSP, process in Python, and re-encode for delivery.

| Attribute | Details |
|---|---|
| **License** | LGPL 2.1+ / GPL (depending on codecs enabled) |
| **RTSP Ingestion** | **Excellent.** FFmpeg handles virtually every RTSP implementation. `cv2.VideoCapture("rtsp://...")` uses FFmpeg under the hood. |
| **AI Integration** | **Excellent.** Direct numpy array access per frame. This is the most common approach in the Python AI community. |
| **Browser Delivery** | **Poor natively.** FFmpeg can output HLS (high latency) or RTMP. For WebRTC, you need an additional server (go2rtc, MediaMTX, Janus). |
| **Latency** | Decode + inference: ~100-200ms. Delivery depends on output method. |
| **Scalability** | CPU-intensive. Each camera = 1 FFmpeg decode process. 50 cameras on edge hardware is very demanding without GPU decode. |
| **Edge/Jetson** | Works, but misses Jetson's hardware acceleration unless you use GStreamer backend or NVIDIA's codec SDK. |
| **Python SDK** | This IS the Python-native approach. OpenCV, ffmpegcv, PyAV, subprocess. |
| **Maturity** | FFmpeg: 20+ years. OpenCV: 25+ years. The most proven combination. |
| **Complexity** | **Low to start, high to scale.** A single-camera proof of concept is 20 lines of Python. Scaling to 50 cameras with reconnection handling, frame synchronization, and browser delivery requires significant engineering. |

**Known issues:**
- `cv2.VideoCapture` was not designed for network streams; it buffers aggressively causing stale frames
- Frame drops and artifacts are common with RTSP over unreliable networks
- No built-in reconnection logic; must be hand-coded
- CPU-only decode is a bottleneck at scale

**Architecture for our use case:**
```
[IP Camera] --RTSP--> [Python: OpenCV/FFmpeg] --> [YOLO inference]
                                                        |
                                                  [annotated frame]
                                                        |
                                          [RTSP/RTMP publish to MediaMTX or go2rtc]
                                                        |
                                                  [Web Browser]
                                                  (WebRTC / LL-HLS)
```

**Verdict:** Great for prototyping and single-camera PoC. Falls apart at scale without significant infrastructure around it. Best used as the AI processing component within a larger architecture.

---

### 6. NVIDIA DeepStream SDK

**What it is:** End-to-end AI video analytics SDK built on GStreamer, optimized for NVIDIA GPUs and Jetson.

| Attribute | Details |
|---|---|
| **License** | **Proprietary NVIDIA license** (free to use on NVIDIA hardware, but not open source; requires agreement to NVIDIA DeepStream SDK Software License Agreement) |
| **RTSP Ingestion** | **Excellent.** Native multi-stream RTSP input via `nvurisrcbin`. Handles reconnection, batching, and synchronization. |
| **AI Integration** | **Best-in-class.** `nvinfer` plugin runs TensorRT-optimized models (including YOLO) directly in the pipeline. GPU-accelerated pre/post-processing. Batched inference across multiple streams. [DeepStream-Yolo](https://github.com/marcoslucianops/DeepStream-Yolo) supports YOLOv5 through YOLO26. |
| **Browser Delivery** | **RTSP output only (natively).** Uses `nvrtspoutsinkbin` to output annotated RTSP. For browser delivery, pair with MediaMTX or go2rtc for WebRTC conversion. WebRTC sink exists but is experimental. |
| **Latency** | **Lowest possible on Jetson.** Hardware-accelerated decode (NVDEC) + TensorRT inference + hardware encode (NVENC). End-to-end pipeline latency can be <100ms before network delivery. |
| **Scalability** | Jetson Orin AGX: up to 16 streams. Orin NX: up to 8 streams. Orin Nano: 4 streams. On dGPU servers: 30+ streams per GPU. Batched inference amortizes GPU cost across streams. |
| **Edge/Jetson** | **Purpose-built.** This is THE NVIDIA solution for edge video analytics on Jetson. |
| **Python SDK** | [deepstream_python_apps](https://github.com/NVIDIA-AI-IOT/deepstream_python_apps) provides Python bindings. Probe functions allow accessing metadata and frames at pipeline points. Learning curve is steep. |
| **Maturity** | Production-ready. Used in smart cities, retail, industrial safety. NVIDIA-supported. |
| **Complexity** | **Very High.** Requires understanding GStreamer pipelines, TensorRT model conversion, DeepStream configuration files, and NVIDIA-specific APIs. Debugging is difficult. Initial setup takes days to weeks. |

**Architecture for our use case:**
```
[IP Camera x50] --RTSP--> [DeepStream Pipeline]
                                |
                          [nvstreammux (batching)]
                                |
                          [nvinfer (YOLO/TensorRT)]
                                |
                          [nvtracker (optional)]
                                |
                          [nvosd (bounding boxes + labels)]
                                |
                          [nvrtspoutsinkbin] --RTSP--> [go2rtc/MediaMTX] --WebRTC--> [Browser]
```

**Verdict:** The gold standard for performance and scalability on Jetson. If you are committed to NVIDIA hardware and can invest the setup time, this is the most efficient pipeline. The browser delivery gap is easily solved by pairing with go2rtc or MediaMTX.

---

### 7. go2rtc

**What it is:** Lightweight, universal camera streaming gateway. Written in Go. Born from the Home Assistant / Frigate NVR ecosystem.

| Attribute | Details |
|---|---|
| **License** | **MIT** (fully commercial-friendly) |
| **RTSP Ingestion** | **Excellent.** Designed specifically for IP camera RTSP streams. Handles authentication, reconnection, multiple codecs. Battle-tested with hundreds of camera models via Frigate. |
| **AI Integration** | **Indirect but practical.** Provides `/api/frame.jpeg` endpoint for frame snapshots. Used alongside Frigate for AI detection. Does not provide continuous decoded frame streams to external processes natively, but can relay RTSP to a Python consumer. |
| **Browser Delivery** | **Excellent.** WebRTC, MSE (Media Source Extensions), HLS, MJPEG -- all from a single RTSP input. WebRTC latency as low as 0.5 seconds. |
| **Latency** | **~0.5 seconds** via WebRTC. Among the lowest latency RTSP-to-browser solutions available. |
| **Scalability** | Very lightweight. Used in Frigate to handle many cameras simultaneously. Minimal CPU usage (codec passthrough, no transcoding). |
| **Edge/Jetson** | Single binary, ARM64 support. Docker images for amd64, arm64, arm. Runs well on Raspberry Pi, so Jetson is no problem. Comes pre-installed with FFmpeg and Python in Docker image. |
| **Python SDK** | HTTP API accessible from Python. Frame access via `/api/frame.jpeg`. Stream URLs available for OpenCV consumption. |
| **Maturity** | ~7k+ GitHub stars. Integrated into Home Assistant core (2024.11+). Proven in Frigate NVR (the leading open-source NVR with AI detection). Very active development. |
| **Complexity** | **Very Low.** Single binary or Docker container. YAML configuration. Adding a camera is one line of config. |

**Architecture for our use case (Frigate-style):**
```
[IP Camera] --RTSP--> [go2rtc] --RTSP--> [Python: OpenCV + YOLO]
                          |                       |
                          |                 [annotated RTSP]
                          |                       |
                          +<--- publish ----------+
                          |
                    [Web Browser]
                    (WebRTC ~0.5s latency)
```

**Verdict:** Excellent lightweight relay for RTSP-to-browser with very low latency. Pairs naturally with a Python AI pipeline. The Frigate project proves this architecture works at scale for AI-powered camera monitoring. A strong contender for the relay layer.

---

### 8. Other Notable Frameworks

#### mediasoup
- **License:** ISC (permissive)
- **Strengths:** High-performance WebRTC SFU, excellent scalability, Node.js native
- **Weaknesses:** No RTSP ingestion (requires FFmpeg/GStreamer bridge), no Python SDK, primarily designed for videoconferencing
- **Verdict:** Overkill for camera monitoring; better suited for interactive communication apps

#### Pion WebRTC
- **License:** MIT
- **Strengths:** Pure Go WebRTC implementation, [RTSPtoWebRTC](https://github.com/deepch/RTSPtoWebRTC) project exists, very lightweight
- **Weaknesses:** Low-level library (not a turnkey server), no AI integration, requires Go development
- **Verdict:** Good building block if you want to build a custom Go-based relay, but go2rtc is essentially a productized version of this concept

#### RTSPtoWeb / RTSPtoWebRTC
- **License:** MIT
- **Strengths:** Purpose-built RTSP-to-browser relay, simple setup
- **Weaknesses:** Less actively maintained than go2rtc/MediaMTX, limited features
- **Verdict:** Viable but superseded by go2rtc in functionality and community support

---

## Comparison Table

| Criteria | LiveKit | Janus | MediaMTX | GStreamer | FFmpeg+Python | DeepStream | go2rtc |
|---|---|---|---|---|---|---|---|
| **RTSP Ingestion** | No (RTMP only) | Yes (native) | Yes (excellent) | Yes (excellent) | Yes (excellent) | Yes (excellent) | Yes (excellent) |
| **AI Frame Access** | Yes (VideoStream) | No (RTP only) | No (relay only) | Yes (appsink) | Yes (native) | Yes (nvinfer) | Indirect (API) |
| **Browser Delivery** | WebRTC (excellent) | WebRTC (excellent) | WebRTC+HLS+LL-HLS | WebRTC (moderate) | Needs relay | Needs relay | WebRTC+MSE+HLS |
| **Latency** | <1s | <1s | <1s (WebRTC) | <1s (pipeline) | Varies | <100ms (pipeline) | ~0.5s |
| **50-Camera Scale** | Heavy (FFmpeg/cam) | Good | Good | Good (DeepStream) | Very Heavy | Best (batched) | Good |
| **Jetson/ARM** | Possible (heavy) | Yes (C binary) | Yes (Go binary) | Yes (native) | Yes (limited accel) | Purpose-built | Yes (Go binary) |
| **Python Ecosystem** | Excellent (Agents) | Poor | Good (via OpenCV) | Moderate (steep) | Excellent | Moderate (steep) | Good (via API) |
| **License** | Apache 2.0 | GPLv3 | MIT | LGPL 2.1+ | LGPL/GPL | Proprietary (free) | MIT |
| **Maturity** | High (~22k stars) | High (10+ years) | High (~13k stars) | Very High (20+ yr) | Very High | High (NVIDIA) | High (~7k stars) |
| **Setup Complexity** | Medium-High | High | Very Low | High | Low (single cam) | Very High | Very Low |
| **Reconnection** | Via Ingress | Native RTSP plugin | Native | rtspsrc element | Manual coding | Native | Native |

### Scoring Matrix (1-5, where 5 = best for our use case)

| Criteria (Weight) | LiveKit | Janus | MediaMTX | GStreamer | FFmpeg+Py | DeepStream | go2rtc |
|---|---|---|---|---|---|---|---|
| RTSP Ingestion (20%) | 2 | 4 | 5 | 5 | 4 | 5 | 5 |
| AI Integration (25%) | 5 | 1 | 2 | 4 | 5 | 5 | 2 |
| Browser Delivery (15%) | 5 | 5 | 4 | 3 | 1 | 2 | 5 |
| Edge/Jetson (15%) | 2 | 4 | 5 | 5 | 3 | 5 | 5 |
| Python Ease (10%) | 5 | 1 | 3 | 2 | 5 | 2 | 3 |
| Scalability (10%) | 3 | 4 | 4 | 4 | 2 | 5 | 4 |
| Simplicity (5%) | 2 | 2 | 5 | 1 | 3 | 1 | 5 |
| **Weighted Score** | **3.35** | **2.85** | **3.65** | **3.70** | **3.40** | **3.90** | **3.80** |

---

## Recommended Architectures

### Option A: Maximum Performance (Jetson-First)
**DeepStream + go2rtc/MediaMTX**

```
[IP Cameras x50] --RTSP--> [NVIDIA DeepStream]
                                  |
                            [TensorRT YOLO]
                            [nvosd overlay]
                                  |
                            [RTSP output] ---> [go2rtc] --WebRTC--> [Browser Dashboard]
```

- **Pros:** Highest throughput, lowest latency, best GPU utilization, handles 16+ streams on Orin AGX
- **Cons:** Steep learning curve (2-4 weeks), NVIDIA lock-in, difficult to customize beyond standard detection
- **Best for:** Production deployment with 20-50 cameras on Jetson hardware
- **Estimated latency:** ~200-500ms glass-to-glass

### Option B: Pragmatic Python-First
**go2rtc (or MediaMTX) + Python/OpenCV + YOLO**

```
[IP Cameras] --RTSP--> [go2rtc] --RTSP--> [Python Workers]
                           |                     |
                           |               [OpenCV decode]
                           |               [YOLO inference]
                           |               [Draw annotations]
                           |               [RTSP/RTMP publish]
                           |                     |
                           +<--------------------+
                           |
                     [Browser Dashboard]
                     (WebRTC via go2rtc)
```

- **Pros:** Fastest to build, pure Python AI pipeline, easy to debug and iterate, go2rtc handles all protocol complexity
- **Cons:** CPU-intensive decode (unless using GStreamer backend with Jetson), per-camera Python processes
- **Best for:** MVP/PoC, 1-10 cameras, rapid iteration, teams without GStreamer/DeepStream expertise
- **Estimated latency:** ~500ms-1.5s glass-to-glass
- **Scaling tip:** Use `ffmpegcv` instead of `cv2.VideoCapture` for better RTSP handling

### Option C: Hybrid (Recommended for Production)
**DeepStream for AI + go2rtc for Browser Delivery + Python for Business Logic**

```
[IP Cameras] --RTSP--> [DeepStream Pipeline]
                              |
                        [TensorRT YOLO]
                        [nvosd overlay]
                              |
                   +----------+----------+
                   |                     |
             [RTSP output]         [Metadata output]
                   |                     |
              [go2rtc]            [Python Service]
                   |              (alerts, logging,
             [Browser]            dashboards, API)
             (WebRTC)
```

- **Pros:** Best of both worlds. DeepStream handles heavy video processing with GPU acceleration. go2rtc provides turnkey WebRTC browser delivery. Python handles business logic without being in the video hot path.
- **Cons:** Requires DeepStream expertise for initial setup. Two separate systems to maintain.
- **Best for:** Production deployment, 10-50 cameras, Jetson hardware, teams willing to invest in DeepStream setup
- **Estimated latency:** ~300-700ms glass-to-glass

### Option D: LiveKit AI Agents (if RTSP gap is bridged)
**LiveKit + Python Agents**

```
[IP Cameras] --RTSP--> [FFmpeg bridge] --RTMP--> [LiveKit Ingress]
                                                        |
                                                  [LiveKit Room]
                                                        |
                                                  [Python Agent]
                                                  (VideoStream -> YOLO -> VideoSource)
                                                        |
                                                  [Browser]
                                                  (LiveKit JS SDK)
```

- **Pros:** Most elegant Python developer experience for AI. Built-in room management, participant tracking, data channels for metadata.
- **Cons:** No native RTSP (FFmpeg bridge per camera is heavy). Ingress service requires significant resources. Relatively heavyweight for a camera relay.
- **Best for:** If you also need bidirectional communication (e.g., talk-back to workers), or if LiveKit adds RTSP support in the future.

---

## Final Recommendation

### For MVP / Proof of Concept (1-5 cameras):
**go2rtc + Python/OpenCV + YOLO**

Start here. You can have a working demo in a day:
1. Deploy go2rtc with camera RTSP URLs in config
2. Python script reads RTSP from go2rtc, runs YOLO, draws boxes
3. Publish annotated stream back to go2rtc
4. Browser connects via WebRTC

### For Production (10-50 cameras on Jetson):
**DeepStream + go2rtc + Python (Option C)**

This is the architecture used by commercial construction site AI monitoring systems:
1. DeepStream handles RTSP ingestion, GPU-accelerated decoding, batched YOLO inference (TensorRT), and annotation overlay
2. go2rtc converts DeepStream's RTSP output to WebRTC for the browser dashboard
3. Python service consumes DeepStream metadata for alerts, logging, and dashboard APIs
4. Network resilience is handled at each layer (DeepStream reconnects RTSP, go2rtc handles browser reconnection)

### Why NOT the others for this specific use case:
- **LiveKit:** Would be the top choice IF it supported RTSP natively. The FFmpeg-per-camera workaround is impractical for 50 cameras on edge hardware. Revisit if RTSP ingress is added.
- **Janus:** Great WebRTC gateway but the AI integration gap is too large. You end up building two parallel pipelines.
- **MediaMTX:** Nearly interchangeable with go2rtc for the relay role. go2rtc edges ahead due to its proven integration with AI detection systems (Frigate) and slightly lower WebRTC latency. MediaMTX is an excellent alternative.
- **Pure FFmpeg+Python:** Good for PoC but doesn't scale. No built-in reconnection, no browser delivery, CPU-bound decoding.
- **GStreamer (without DeepStream):** All the complexity of DeepStream without the GPU acceleration benefits. Only choose if you need to run on non-NVIDIA hardware.

---

## Sources

- [LiveKit GitHub Repository](https://github.com/livekit/livekit)
- [LiveKit Ingress Documentation](https://docs.livekit.io/home/ingress/overview/)
- [LiveKit RTSP Support Issue](https://github.com/livekit/ingress/issues/270)
- [LiveKit Agents Framework](https://docs.livekit.io/agents/)
- [LiveKit Python SDKs](https://github.com/livekit/python-sdks)
- [LiveKit Raw Media Tracks](https://docs.livekit.io/transport/media/raw-tracks/)
- [Janus Gateway GitHub](https://github.com/meetecho/janus-gateway)
- [Janus Streaming Plugin Documentation](https://janus.conf.meetecho.com/docs/streaming)
- [Janus on Jetson (jetson-janus)](https://github.com/SeanAvery/jetson-janus)
- [MediaMTX GitHub Repository](https://github.com/bluenviron/mediamtx)
- [go2rtc GitHub Repository](https://github.com/AlexxIT/go2rtc)
- [go2rtc Protocol Support](https://go2rtc.com/which-protocols-does-go2rtc-support-for-input-and-output-e-g-rtsp-webrtc-hls/)
- [Frigate go2rtc Configuration](https://docs.frigate.video/guides/configuring_go2rtc/)
- [NVIDIA DeepStream SDK](https://developer.nvidia.com/deepstream-sdk)
- [DeepStream Performance Documentation](https://docs.nvidia.com/metropolis/deepstream/dev-guide/text/DS_Performance.html)
- [DeepStream YOLO Integration](https://github.com/marcoslucianops/DeepStream-Yolo)
- [DeepStream Python Apps](https://github.com/NVIDIA-AI-IOT/deepstream_python_apps)
- [GStreamer webrtcsink](https://gstreamer.freedesktop.org/documentation/rswebrtc/webrtcsink.html)
- [GStreamer webrtcbin](https://gstreamer.freedesktop.org/documentation/webrtc/index.html)
- [Pion WebRTC](https://github.com/pion/webrtc)
- [RTSPtoWebRTC (Pion-based)](https://github.com/deepch/RTSPtoWebRTC)
- [mediasoup](https://github.com/versatica/mediasoup)
- [AI Video Analytics for Construction 2025](https://www.spot.ai/blog/ai-video-analytics-tools-construction-2025-guide)
- [Edge AI Construction Site Monitoring (ACM 2025)](https://dl.acm.org/doi/10.1145/3756423.3756551)
- [WebRTC vs HLS Latency Comparison](https://cloudinary.com/guides/live-streaming-video/low-latency-hls-ll-hls-cmaf-and-webrtc-which-is-best)
- [ffmpegcv (Alternative to OpenCV for RTSP)](https://pypi.org/project/ffmpegcv/)
