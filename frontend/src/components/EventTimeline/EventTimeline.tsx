import { useState } from "react";
import type { AnnotationEvent, ZoneDefinition } from "../../types";
import { ZONE_BORDER_COLORS } from "../../types";
import styles from "./EventTimeline.module.css";

interface Props {
  events: AnnotationEvent[];
  zones: ZoneDefinition[];
  selectedZoneId: string | null;
  currentFrame: number;
  totalFrames: number;
  fps: number;
  mode: "zone-edit" | "annotation";
  onAddEvent: (event: AnnotationEvent) => void;
  onDeleteEvent: (index: number) => void;
  onSeekToFrame: (frame: number) => void;
}

export function EventTimeline({
  events,
  zones,
  selectedZoneId,
  currentFrame,
  totalFrames,
  fps,
  mode,
  onAddEvent,
  onDeleteEvent,
  onSeekToFrame,
}: Props) {
  const [markingStart, setMarkingStart] = useState<number | null>(null);
  const [markingZoneId, setMarkingZoneId] = useState<string | null>(null);

  const formatTime = (frame: number) => {
    const t = frame / fps;
    const m = Math.floor(t / 60);
    const s = (t % 60).toFixed(1);
    return `${m}:${s.padStart(4, "0")}`;
  };

  const handleStartMark = () => {
    let zoneId = selectedZoneId;

    if (!zoneId) {
      if (zones.length === 1) {
        zoneId = zones[0].zone_id;
      } else {
        alert("zone을 선택하세요");
        return;
      }
    }

    setMarkingStart(currentFrame);
    setMarkingZoneId(zoneId);
  };

  const handleEndMark = () => {
    if (markingStart === null || !markingZoneId) return;

    onAddEvent({
      zone_id: markingZoneId,
      start_frame: markingStart,
      end_frame: currentFrame,
    });

    setMarkingStart(null);
    setMarkingZoneId(null);
  };

  const isMarking = markingStart !== null;
  const isAnnotationMode = mode === "annotation";

  return (
    <div className={styles.container}>
      {/* 타임라인 시각화 */}
      {totalFrames > 0 && (
        <div className={styles.timeline}>
          <div className={styles.timelineBar}>
            {events.map((ev, i) => {
              const left = (ev.start_frame / totalFrames) * 100;
              const width = ((ev.end_frame - ev.start_frame) / totalFrames) * 100;
              const zone = zones.find((z) => z.zone_id === ev.zone_id);
              const color = zone
                ? ZONE_BORDER_COLORS[zone.zone_type]
                : "#888";
              return (
                <div
                  key={i}
                  className={styles.eventBlock}
                  style={{
                    left: `${left}%`,
                    width: `${Math.max(width, 0.3)}%`,
                    background: color,
                  }}
                  onClick={() => onSeekToFrame(ev.start_frame)}
                  title={`${ev.zone_id}: ${formatTime(ev.start_frame)} ~ ${formatTime(ev.end_frame)}`}
                />
              );
            })}
            {/* 현재 위치 인디케이터 */}
            <div
              className={styles.playhead}
              style={{ left: `${(currentFrame / Math.max(totalFrames, 1)) * 100}%` }}
            />
          </div>
        </div>
      )}

      {/* 마킹 버튼 */}
      {isAnnotationMode && (
        <div className={styles.markingRow}>
          <button
            onClick={handleStartMark}
            className={`${styles.btn} ${isMarking ? styles.btnActive : ""}`}
          >
            {isMarking ? `🔴 재시작 (${markingStart})` : "침입 시작"}
          </button>
          <button
            onClick={handleEndMark}
            disabled={!isMarking}
            className={styles.btn}
          >
            침입 끝
          </button>
          {isMarking && (
            <span className={styles.markingInfo}>
              기록 중... {markingZoneId} (프레임 {markingStart}~)
            </span>
          )}
          <span className={styles.eventCount}>이벤트: {events.length}건</span>
        </div>
      )}

      {/* 이벤트 목록 */}
      {events.length > 0 && (
        <div className={styles.eventList}>
          <table className={styles.table}>
            <thead>
              <tr>
                <th>#</th>
                <th>Zone</th>
                <th>시작</th>
                <th>끝</th>
                <th>길이</th>
                {isAnnotationMode && <th></th>}
              </tr>
            </thead>
            <tbody>
              {events.map((ev, i) => {
                const duration = (ev.end_frame - ev.start_frame) / fps;
                return (
                  <tr
                    key={i}
                    className={styles.eventRow}
                    onClick={() => onSeekToFrame(ev.start_frame)}
                  >
                    <td>{i + 1}</td>
                    <td>{zones.find((z) => z.zone_id === ev.zone_id)?.zone_name ?? ev.zone_id}</td>
                    <td>{formatTime(ev.start_frame)}</td>
                    <td>{formatTime(ev.end_frame)}</td>
                    <td>{duration.toFixed(1)}초</td>
                    {isAnnotationMode && (
                      <td>
                        <button
                          onClick={(e) => {
                            e.stopPropagation();
                            onDeleteEvent(i);
                          }}
                          className={styles.deleteBtn}
                        >
                          X
                        </button>
                      </td>
                    )}
                  </tr>
                );
              })}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
}
