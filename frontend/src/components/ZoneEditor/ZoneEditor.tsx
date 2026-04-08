import { useRef, useEffect, useCallback, useState, forwardRef, useImperativeHandle } from "react";
import { Canvas, Polygon, Circle, Line, controlsUtils, FabricObject } from "fabric";
import type { ZoneDefinition } from "../../types";
import { ZONE_COLORS, ZONE_BORDER_COLORS } from "../../types";

type EditorState = "idle" | "drawing" | "editing";

const zoneIdMap = new WeakMap<FabricObject, string>();

export interface ZoneEditorHandle {
  startDrawing: () => void;
}

interface Props {
  canvasWidth: number;
  canvasHeight: number;
  zones: ZoneDefinition[];
  selectedZoneId: string | null;
  mode: "zone-edit" | "annotation";
  onZoneCreated: (points: number[][]) => void;
  onZoneUpdated: (zoneId: string, points: number[][]) => void;
  onZoneSelected: (zoneId: string | null) => void;
}

export const ZoneEditor = forwardRef<ZoneEditorHandle, Props>(function ZoneEditor({
  canvasWidth,
  canvasHeight,
  zones,
  selectedZoneId,
  mode,
  onZoneCreated,
  onZoneUpdated,
  onZoneSelected,
}, ref) {
  const fabricCanvasRef = useRef<Canvas | null>(null);
  const canvasElRef = useRef<HTMLCanvasElement>(null);
  const [editorState, setEditorState] = useState<EditorState>("idle");
  const [vertexCount, setVertexCount] = useState(0);
  const drawingPointsRef = useRef<{ x: number; y: number }[]>([]);
  const drawingObjectsRef = useRef<FabricObject[]>([]);
  const previewLineRef = useRef<Line | null>(null);

  // Fabric.js canvas 초기화
  useEffect(() => {
    const el = canvasElRef.current;
    if (!el || canvasWidth === 0 || canvasHeight === 0) return;

    const fc = new Canvas(el, {
      width: canvasWidth,
      height: canvasHeight,
      selection: false,
      backgroundColor: "transparent",
    });
    fabricCanvasRef.current = fc;

    return () => {
      fc.dispose();
      fabricCanvasRef.current = null;
    };
  }, [canvasWidth, canvasHeight]);

  // zone polygons 렌더링
  useEffect(() => {
    const fc = fabricCanvasRef.current;
    if (!fc) return;

    // 기존 polygon 제거 (drawing 오브젝트 제외)
    const toRemove = fc.getObjects().filter((o) => zoneIdMap.has(o));
    toRemove.forEach((o) => fc.remove(o));

    // zone polygon 추가
    zones.forEach((zone) => {
      const coords = zone.geometry.coordinates[0];
      const points = coords.slice(0, -1).map(([x, y]) => ({
        x: x * canvasWidth,
        y: y * canvasHeight,
      }));

      const color = ZONE_COLORS[zone.zone_type] ?? ZONE_COLORS.danger;
      const borderColor = ZONE_BORDER_COLORS[zone.zone_type] ?? ZONE_BORDER_COLORS.danger;
      const isSelected = zone.zone_id === selectedZoneId;

      const poly = new Polygon(points, {
        fill: color,
        stroke: borderColor,
        strokeWidth: isSelected ? 3 : 2,
        objectCaching: false,
        transparentCorners: false,
        cornerColor: borderColor,
        cornerStyle: "circle",
        cornerSize: 10,
        hasBorders: false,
        selectable: mode === "zone-edit",
        evented: mode === "zone-edit",
      });

      zoneIdMap.set(poly, zone.zone_id);

      if (isSelected && mode === "zone-edit") {
        poly.controls = controlsUtils.createPolyControls(poly);
      }

      fc.add(poly);
    });

    fc.requestRenderAll();
  }, [zones, selectedZoneId, canvasWidth, canvasHeight, mode]);

  // polygon 선택/수정 이벤트
  useEffect(() => {
    const fc = fabricCanvasRef.current;
    if (!fc) return;

    const handleSelected = (e: any) => {
      const target = e.selected?.[0];
      const zoneId = target && zoneIdMap.get(target);
      if (zoneId) {
        onZoneSelected(zoneId);
      }
    };

    const handleDeselected = () => {
      if (editorState !== "drawing") {
        onZoneSelected(null);
      }
    };

    const handleModified = (e: any) => {
      const target = e.target;
      const zoneId = target && zoneIdMap.get(target);
      if (!zoneId) return;
      const poly = target as Polygon;
      const matrix = poly.calcTransformMatrix();

      const normalizedPoints = poly.points.map((p) => {
        const transformed = {
          x: p.x - poly.pathOffset.x,
          y: p.y - poly.pathOffset.y,
        };
        const tx = matrix[0] * transformed.x + matrix[2] * transformed.y + matrix[4];
        const ty = matrix[1] * transformed.x + matrix[3] * transformed.y + matrix[5];
        return [tx / canvasWidth, ty / canvasHeight];
      });

      onZoneUpdated(zoneId, normalizedPoints);
    };

    fc.on("selection:created", handleSelected);
    fc.on("selection:updated", handleSelected);
    fc.on("selection:cleared", handleDeselected);
    fc.on("object:modified", handleModified);

    return () => {
      fc.off("selection:created", handleSelected);
      fc.off("selection:updated", handleSelected);
      fc.off("selection:cleared", handleDeselected);
      fc.off("object:modified", handleModified);
    };
  }, [canvasWidth, canvasHeight, editorState, onZoneSelected, onZoneUpdated]);

  // Drawing 상태: 클릭으로 꼭짓점 배치
  const cancelDrawing = useCallback(() => {
    const fc = fabricCanvasRef.current;
    if (!fc) return;

    drawingObjectsRef.current.forEach((o) => fc.remove(o));
    if (previewLineRef.current) fc.remove(previewLineRef.current);
    drawingPointsRef.current = [];
    drawingObjectsRef.current = [];
    previewLineRef.current = null;
    setVertexCount(0);
    setEditorState("idle");
    fc.requestRenderAll();
  }, []);

  useImperativeHandle(ref, () => ({
    startDrawing: () => {
      cancelDrawing();
      setEditorState("drawing");
    },
  }), [cancelDrawing]);

  const finishDrawing = useCallback(() => {
    const fc = fabricCanvasRef.current;
    if (!fc) return;

    const points = drawingPointsRef.current;
    if (points.length < 3) {
      cancelDrawing();
      return;
    }

    // drawing 오브젝트 제거
    drawingObjectsRef.current.forEach((o) => fc.remove(o));
    if (previewLineRef.current) fc.remove(previewLineRef.current);

    // 정규화 좌표로 변환
    const normalizedPoints = points.map((p) => [p.x / canvasWidth, p.y / canvasHeight]);

    drawingPointsRef.current = [];
    drawingObjectsRef.current = [];
    previewLineRef.current = null;
    setVertexCount(0);
    setEditorState("idle");

    onZoneCreated(normalizedPoints);
    fc.requestRenderAll();
  }, [canvasWidth, canvasHeight, cancelDrawing, onZoneCreated]);

  // 투명 오버레이 ref — drawing 모드에서 Fabric 위에 올려 이벤트를 가로챔
  const overlayRef = useRef<HTMLDivElement>(null);

  // 오버레이 좌표 → Fabric canvas 좌표 변환
  const toCanvasPoint = useCallback((e: MouseEvent): { x: number; y: number } | null => {
    const fc = fabricCanvasRef.current;
    const overlay = overlayRef.current;
    if (!fc || !overlay) return null;
    const rect = overlay.getBoundingClientRect();
    return {
      x: ((e.clientX - rect.left) / rect.width) * fc.width,
      y: ((e.clientY - rect.top) / rect.height) * fc.height,
    };
  }, []);

  // drawing 모드: 투명 오버레이에 이벤트 리스너 부착 (Fabric 간섭 완전 차단)
  useEffect(() => {
    const fc = fabricCanvasRef.current;
    const overlay = overlayRef.current;
    if (!fc || !overlay || editorState !== "drawing") return;

    // drawing 중 기존 zone polygon 클릭 방지
    fc.discardActiveObject();
    fc.getObjects().forEach((o) => {
      o.selectable = false;
      o.evented = false;
    });

    const addVertex = (point: { x: number; y: number }) => {
      drawingPointsRef.current.push(point);
      setVertexCount(drawingPointsRef.current.length);

      const circle = new Circle({
        left: point.x - 5,
        top: point.y - 5,
        radius: 5,
        fill: "#0064ff",
        stroke: "#fff",
        strokeWidth: 1,
        selectable: false,
        evented: false,
      });
      drawingObjectsRef.current.push(circle);
      fc.add(circle);

      const pts = drawingPointsRef.current;
      if (pts.length >= 2) {
        const prev = pts[pts.length - 2];
        const line = new Line([prev.x, prev.y, point.x, point.y], {
          stroke: "#0064ff",
          strokeWidth: 2,
          selectable: false,
          evented: false,
        });
        drawingObjectsRef.current.push(line);
        fc.add(line);
      }
      fc.requestRenderAll();
    };

    const handleMouseDown = (e: MouseEvent) => {
      if (e.button !== 0) return;
      e.preventDefault();
      e.stopPropagation();
      const point = toCanvasPoint(e);
      if (point) addVertex(point);
    };

    const handleContextMenu = (e: MouseEvent) => {
      e.preventDefault();
      e.stopPropagation();
      finishDrawing();
    };

    const handleDblClick = (e: MouseEvent) => {
      e.preventDefault();
      e.stopPropagation();
      const pts = drawingPointsRef.current;
      const objs = drawingObjectsRef.current;
      for (let i = 0; i < 2 && pts.length > 3; i++) {
        pts.pop();
        const removed = objs.pop();
        if (removed) fc.remove(removed);
        const removedLine = objs.pop();
        if (removedLine) fc.remove(removedLine);
      }
      finishDrawing();
    };

    const handleMouseMove = (e: MouseEvent) => {
      const pts = drawingPointsRef.current;
      if (pts.length === 0) return;
      const pointer = toCanvasPoint(e);
      if (!pointer) return;

      const last = pts[pts.length - 1];
      if (previewLineRef.current) fc.remove(previewLineRef.current);
      const preview = new Line([last.x, last.y, pointer.x, pointer.y], {
        stroke: "#0064ff",
        strokeWidth: 1,
        strokeDashArray: [5, 5],
        selectable: false,
        evented: false,
      });
      previewLineRef.current = preview;
      fc.add(preview);
      fc.requestRenderAll();
    };

    overlay.addEventListener("mousedown", handleMouseDown);
    overlay.addEventListener("contextmenu", handleContextMenu);
    overlay.addEventListener("dblclick", handleDblClick);
    overlay.addEventListener("mousemove", handleMouseMove);

    return () => {
      overlay.removeEventListener("mousedown", handleMouseDown);
      overlay.removeEventListener("contextmenu", handleContextMenu);
      overlay.removeEventListener("dblclick", handleDblClick);
      overlay.removeEventListener("mousemove", handleMouseMove);
    };
  }, [editorState, finishDrawing, toCanvasPoint]);

  // Esc 키: 그리기 취소
  useEffect(() => {
    if (editorState !== "drawing") return;

    const handleKey = (e: KeyboardEvent) => {
      if (e.key === "Escape") {
        cancelDrawing();
      }
    };
    window.addEventListener("keydown", handleKey);
    return () => window.removeEventListener("keydown", handleKey);
  }, [editorState, cancelDrawing]);

  return (
    <>
      <div
        style={{
          position: "absolute",
          top: 0,
          left: 0,
          pointerEvents: mode === "zone-edit" ? "auto" : "none",
        }}
      >
        <canvas ref={canvasElRef} />
      </div>
      {editorState === "drawing" && (
        <>
          {/* 투명 오버레이: Fabric 위에서 모든 마우스 이벤트를 가로챔 */}
          <div
            ref={overlayRef}
            style={{
              position: "absolute",
              top: 0,
              left: 0,
              width: canvasWidth,
              height: canvasHeight,
              cursor: "crosshair",
              zIndex: 5,
            }}
          />
          <div
            style={{
              position: "absolute",
              top: 8,
              left: 8,
              background: "rgba(0,0,0,0.7)",
              color: "#fff",
              padding: "6px 12px",
              borderRadius: 4,
              fontSize: 13,
              zIndex: 10,
              pointerEvents: "none",
            }}
          >
            클릭: 꼭짓점 배치 | 더블클릭/우클릭: 완성 | Esc: 취소
            ({vertexCount}개 꼭짓점)
          </div>
        </>
      )}
    </>
  );
});

export { type EditorState };
