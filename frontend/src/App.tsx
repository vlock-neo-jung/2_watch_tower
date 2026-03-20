import { useState, useEffect, useRef, useCallback } from "react";
import { VideoPlayer } from "./components/VideoPlayer";
import type { VideoPlayerHandle } from "./components/VideoPlayer";
import { ZoneEditor } from "./components/ZoneEditor";
import { ZonePanel } from "./components/ZonePanel";
import { EventTimeline } from "./components/EventTimeline";
import {
  fetchVideos,
  fetchVideoInfo,
  videoUrl,
  fetchZoneConfigs,
  fetchZoneConfig,
  saveZoneConfig,
  fetchAnnotations,
  fetchAnnotation,
  saveAnnotation,
} from "./api/client";
import type {
  VideoInfo,
  AppMode,
  ZoneDefinition,
  ZoneConfig,
  AnnotationEvent,
  AnnotationData,
  GeoJSONPolygon,
} from "./types";
import "./App.css";

let zoneIdCounter = 0;

function App() {
  // 영상 상태
  const [videos, setVideos] = useState<string[]>([]);
  const [selectedVideo, setSelectedVideo] = useState<string | null>(null);
  const [videoInfo, setVideoInfo] = useState<VideoInfo | null>(null);

  // 모드
  const [mode, setMode] = useState<AppMode>("zone-edit");

  // Zone 상태
  const [zones, setZones] = useState<ZoneDefinition[]>([]);
  const [selectedZoneId, setSelectedZoneId] = useState<string | null>(null);
  const [zoneConfigs, setZoneConfigs] = useState<string[]>([]);
  const [selectedConfig, setSelectedConfig] = useState("");

  // 이벤트 상태
  const [events, setEvents] = useState<AnnotationEvent[]>([]);
  const [currentFrame, setCurrentFrame] = useState(0);

  // refs
  const playerRef = useRef<VideoPlayerHandle>(null);
  const [canvasSize, setCanvasSize] = useState({ width: 0, height: 0 });

  // 시작할 drawing 상태를 ZoneEditor에 전달하기 위한 트리거
  const [drawingTrigger, setDrawingTrigger] = useState(0);
  const [pendingZoneMeta, setPendingZoneMeta] = useState<{
    name: string;
    type: "danger" | "warning" | "entry";
  } | null>(null);

  // 영상 목록 + zone 설정 목록 로드
  useEffect(() => {
    fetchVideos().then(setVideos);
    fetchZoneConfigs().then(setZoneConfigs);
  }, []);

  // 영상 선택 시 메타데이터 로드
  useEffect(() => {
    if (!selectedVideo) {
      setVideoInfo(null);
      return;
    }
    fetchVideoInfo(selectedVideo).then(setVideoInfo);
  }, [selectedVideo]);

  const handleCanvasReady = useCallback((canvas: HTMLCanvasElement) => {
    setCanvasSize({ width: canvas.width, height: canvas.height });
  }, []);

  const handleFrameChange = useCallback((frame: number) => {
    setCurrentFrame(frame);
  }, []);

  // Zone 추가: 메타데이터 설정 → drawing 트리거
  const handleAddZone = useCallback(
    (name: string, type: "danger" | "warning" | "entry") => {
      setPendingZoneMeta({ name, type });
      setDrawingTrigger((t) => t + 1);
    },
    []
  );

  // Drawing 완료: polygon 좌표를 받아 zone 생성
  const handleZoneCreated = useCallback(
    (points: number[][]) => {
      const meta = pendingZoneMeta;
      if (!meta) return;

      const zoneId = `zone_${++zoneIdCounter}_${Date.now()}`;
      const closedPoints = [...points, points[0]];
      const geometry: GeoJSONPolygon = {
        type: "Polygon",
        coordinates: [closedPoints],
      };

      const newZone: ZoneDefinition = {
        zone_id: zoneId,
        zone_name: meta.name,
        zone_type: meta.type,
        geometry,
        triggering_anchor: "BOTTOM_CENTER",
        target_classes: [0],
        min_consecutive_frames: 3,
        cooldown_ms: 30000,
      };

      setZones((prev) => [...prev, newZone]);
      setSelectedZoneId(zoneId);
      setPendingZoneMeta(null);
    },
    [pendingZoneMeta]
  );

  // Zone 업데이트 (vertex 편집 후)
  const handleZoneUpdated = useCallback(
    (zoneId: string, points: number[][]) => {
      setZones((prev) =>
        prev.map((z) =>
          z.zone_id === zoneId
            ? {
                ...z,
                geometry: {
                  type: "Polygon" as const,
                  coordinates: [[...points, points[0]]],
                },
              }
            : z
        )
      );
    },
    []
  );

  // Zone 삭제
  const handleDeleteZone = useCallback((zoneId: string) => {
    setZones((prev) => prev.filter((z) => z.zone_id !== zoneId));
    setSelectedZoneId(null);
  }, []);

  // Zone 설정 저장
  const handleSaveConfig = useCallback(
    async (configName: string) => {
      const config: ZoneConfig = { zones };
      await saveZoneConfig(configName, config);
      const updated = await fetchZoneConfigs();
      setZoneConfigs(updated);
      setSelectedConfig(configName);
    },
    [zones]
  );

  // Zone 설정 로드
  const handleLoadConfig = useCallback(async (configName: string) => {
    if (!configName) return;
    const config = await fetchZoneConfig(configName);
    setZones(config.zones);
    setSelectedConfig(configName);
    setSelectedZoneId(null);
  }, []);

  // 이벤트 추가/삭제
  const handleAddEvent = useCallback((event: AnnotationEvent) => {
    setEvents((prev) => [...prev, event]);
  }, []);

  const handleDeleteEvent = useCallback((index: number) => {
    setEvents((prev) => prev.filter((_, i) => i !== index));
  }, []);

  // GT 저장
  const handleSaveGT = useCallback(async () => {
    if (!selectedVideo || !videoInfo) return;
    const name = prompt(
      "GT 파일명 (예: gt_test.json)",
      `gt_${selectedVideo.replace(".mp4", "")}.json`
    );
    if (!name) return;

    const data: AnnotationData = {
      video: selectedVideo,
      video_fps: videoInfo.fps,
      video_width: videoInfo.width,
      video_height: videoInfo.height,
      total_frames: videoInfo.total_frames,
      zones,
      events,
    };
    await saveAnnotation(name, data);
    alert("GT 저장 완료");
  }, [selectedVideo, videoInfo, zones, events]);

  // GT 로드
  const handleLoadGT = useCallback(async () => {
    const list = await fetchAnnotations();
    if (list.length === 0) {
      alert("저장된 GT 파일이 없습니다");
      return;
    }
    const name = prompt(`GT 파일 선택:\n${list.join("\n")}`);
    if (!name || !list.includes(name)) return;

    const data = await fetchAnnotation(name);
    setEvents(data.events);
    if (data.zones) setZones(data.zones);
  }, []);

  // seek to frame
  const handleSeekToFrame = useCallback(
    (frame: number) => {
      playerRef.current?.seekToFrame(frame);
    },
    []
  );

  return (
    <div className="app">
      <header className="header">
        <div className="header-left">
          <select
            value={mode}
            onChange={(e) => setMode(e.target.value as AppMode)}
            className="mode-select"
          >
            <option value="zone-edit">Zone 편집</option>
            <option value="annotation">어노테이션</option>
          </select>

          <select
            value={selectedVideo ?? ""}
            onChange={(e) => setSelectedVideo(e.target.value || null)}
            className="video-select"
          >
            <option value="">영상 선택...</option>
            {videos.map((v) => (
              <option key={v} value={v}>
                {v}
              </option>
            ))}
          </select>

          {mode === "annotation" && (
            <>
              <button onClick={handleSaveGT} className="header-btn">
                GT 저장
              </button>
              <button onClick={handleLoadGT} className="header-btn">
                GT 불러오기
              </button>
            </>
          )}
        </div>
      </header>

      <div className="main">
        <div className="video-area">
          <div style={{ position: "relative" }}>
            <VideoPlayer
              ref={playerRef}
              videoUrl={selectedVideo ? videoUrl(selectedVideo) : null}
              videoInfo={videoInfo}
              onCanvasReady={handleCanvasReady}
              onFrameChange={handleFrameChange}
            />
            <ZoneEditor
              canvasWidth={canvasSize.width}
              canvasHeight={canvasSize.height}
              zones={zones}
              selectedZoneId={selectedZoneId}
              mode={mode}
              startDrawing={pendingZoneMeta !== null}
              onZoneCreated={handleZoneCreated}
              onZoneUpdated={handleZoneUpdated}
              onZoneSelected={setSelectedZoneId}
              key={drawingTrigger}
            />
          </div>
        </div>

        <div className="side-panel">
          <ZonePanel
            zones={zones}
            selectedZoneId={selectedZoneId}
            mode={mode}
            zoneConfigs={zoneConfigs}
            selectedConfig={selectedConfig}
            onSelectZone={setSelectedZoneId}
            onAddZone={handleAddZone}
            onDeleteZone={handleDeleteZone}
            onSaveConfig={handleSaveConfig}
            onLoadConfig={handleLoadConfig}
          />
        </div>
      </div>

      <div className="bottom-panel">
        <EventTimeline
          events={events}
          zones={zones}
          selectedZoneId={selectedZoneId}
          currentFrame={currentFrame}
          totalFrames={videoInfo?.total_frames ?? 0}
          fps={videoInfo?.fps ?? 25}
          mode={mode}
          onAddEvent={handleAddEvent}
          onDeleteEvent={handleDeleteEvent}
          onSeekToFrame={handleSeekToFrame}
        />
      </div>
    </div>
  );
}

export default App;
