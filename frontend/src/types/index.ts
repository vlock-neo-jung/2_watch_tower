export interface VideoInfo {
  filename: string;
  fps: number;
  width: number;
  height: number;
  duration: number;
  total_frames: number;
}

export interface GeoJSONPolygon {
  type: "Polygon";
  coordinates: number[][][];
}

export interface ZoneDefinition {
  zone_id: string;
  zone_name: string;
  zone_type: "danger" | "warning" | "entry";
  geometry: GeoJSONPolygon;
  triggering_anchor: string;
  target_classes: number[];
  min_consecutive_frames: number;
  cooldown_ms: number;
}

export interface ZoneConfig {
  zones: ZoneDefinition[];
}

export interface AnnotationEvent {
  zone_id: string;
  start_frame: number;
  end_frame: number;
}

export interface AnnotationData {
  video: string;
  video_fps: number;
  video_width: number;
  video_height: number;
  total_frames: number;
  zones: ZoneDefinition[];
  events: AnnotationEvent[];
}

export type AppMode = "zone-edit" | "annotation";

export type ZoneColor = Record<string, string>;

export const ZONE_COLORS: Record<string, string> = {
  danger: "rgba(255, 0, 0, 0.3)",
  warning: "rgba(255, 200, 0, 0.3)",
  entry: "rgba(0, 100, 255, 0.3)",
};

export const ZONE_BORDER_COLORS: Record<string, string> = {
  danger: "#ff0000",
  warning: "#ffc800",
  entry: "#0064ff",
};
