import type { VideoInfo, ZoneConfig, AnnotationData } from "../types";

const BASE = "/api";

async function checkResponse(res: Response): Promise<Response> {
  if (!res.ok) {
    const detail = await res.text().catch(() => res.statusText);
    throw new Error(`API 에러 (${res.status}): ${detail}`);
  }
  return res;
}

export async function fetchVideos(): Promise<string[]> {
  const res = await fetch(`${BASE}/videos/`);
  return (await checkResponse(res)).json();
}

export async function fetchVideoInfo(filename: string): Promise<VideoInfo> {
  const res = await fetch(`${BASE}/videos/${encodeURIComponent(filename)}/info`);
  return (await checkResponse(res)).json();
}

export function videoUrl(filename: string): string {
  return `${BASE}/videos/${encodeURIComponent(filename)}`;
}

export async function fetchZoneConfigs(): Promise<string[]> {
  const res = await fetch(`${BASE}/zones/`);
  return (await checkResponse(res)).json();
}

export async function fetchZoneConfig(name: string): Promise<ZoneConfig> {
  const res = await fetch(`${BASE}/zones/${encodeURIComponent(name)}`);
  return (await checkResponse(res)).json();
}

export async function saveZoneConfig(
  name: string,
  config: ZoneConfig
): Promise<void> {
  const res = await fetch(`${BASE}/zones/${encodeURIComponent(name)}`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(config),
  });
  await checkResponse(res);
}

export async function fetchAnnotations(): Promise<string[]> {
  const res = await fetch(`${BASE}/annotations/`);
  return (await checkResponse(res)).json();
}

export async function fetchAnnotation(name: string): Promise<AnnotationData> {
  const res = await fetch(`${BASE}/annotations/${encodeURIComponent(name)}`);
  return (await checkResponse(res)).json();
}

export async function saveAnnotation(
  name: string,
  data: AnnotationData
): Promise<void> {
  const res = await fetch(`${BASE}/annotations/${encodeURIComponent(name)}`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data),
  });
  await checkResponse(res);
}
