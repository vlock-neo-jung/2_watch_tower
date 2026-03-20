import { useRef, useEffect, useCallback, useState } from "react";
import { Canvas, Polygon, Circle, Line, controlsUtils, FabricObject } from "fabric";
import type { ZoneDefinition } from "../../types";
import { ZONE_COLORS, ZONE_BORDER_COLORS } from "../../types";

type EditorState = "idle" | "drawing" | "editing";

interface Props {
  canvasWidth: number;
  canvasHeight: number;
  zones: ZoneDefinition[];
  selectedZoneId: string | null;
  mode: "zone-edit" | "annotation";
  startDrawing?: boolean;
  onZoneCreated: (points: number[][]) => void;
  onZoneUpdated: (zoneId: string, points: number[][]) => void;
  onZoneSelected: (zoneId: string | null) => void;
}

export function ZoneEditor({
  canvasWidth,
  canvasHeight,
  zones,
  selectedZoneId,
  mode,
  startDrawing: startDrawingProp = false,
  onZoneCreated,
  onZoneUpdated,
  onZoneSelected,
}: Props) {
  const fabricCanvasRef = useRef<Canvas | null>(null);
  const canvasElRef = useRef<HTMLCanvasElement>(null);
  const [editorState, setEditorState] = useState<EditorState>(
    startDrawingProp ? "drawing" : "idle"
  );
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
    const toRemove = fc.getObjects().filter((o) => (o as any).__zoneId);
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

      (poly as any).__zoneId = zone.zone_id;

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
      if (target && (target as any).__zoneId) {
        onZoneSelected((target as any).__zoneId);
      }
    };

    const handleDeselected = () => {
      if (editorState !== "drawing") {
        onZoneSelected(null);
      }
    };

    const handleModified = (e: any) => {
      const target = e.target;
      if (!target || !(target as any).__zoneId) return;

      const zoneId = (target as any).__zoneId as string;
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
    setEditorState("idle");
    fc.requestRenderAll();
  }, []);

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
    setEditorState("idle");

    onZoneCreated(normalizedPoints);
    fc.requestRenderAll();
  }, [canvasWidth, canvasHeight, cancelDrawing, onZoneCreated]);

  // canvas 클릭/마우스 이벤트 (drawing 모드)
  useEffect(() => {
    const fc = fabricCanvasRef.current;
    if (!fc || editorState !== "drawing") return;

    const handleClick = (e: any) => {
      if (e.e.button === 2) {
        // 우클릭: polygon 닫기
        e.e.preventDefault();
        finishDrawing();
        return;
      }

      const pointer = fc.getScenePoint(e.e);
      const point = { x: pointer.x, y: pointer.y };
      drawingPointsRef.current.push(point);

      // 꼭짓점 표시
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

      // 이전 꼭짓점과 선 연결
      const points = drawingPointsRef.current;
      if (points.length >= 2) {
        const prev = points[points.length - 2];
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

    const handleMouseMove = (e: any) => {
      const points = drawingPointsRef.current;
      if (points.length === 0) return;

      const pointer = fc.getScenePoint(e.e);
      const last = points[points.length - 1];

      // 점선 미리보기 업데이트
      if (previewLineRef.current) {
        fc.remove(previewLineRef.current);
      }
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

    const handleContextMenu = (e: Event) => {
      e.preventDefault();
    };

    const canvasEl = fc.getSelectionElement();
    canvasEl?.addEventListener("contextmenu", handleContextMenu);

    fc.on("mouse:down", handleClick);
    fc.on("mouse:move", handleMouseMove);

    return () => {
      canvasEl?.removeEventListener("contextmenu", handleContextMenu);
      fc.off("mouse:down", handleClick);
      fc.off("mouse:move", handleMouseMove);
    };
  }, [editorState, finishDrawing]);

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
      <canvas
        ref={canvasElRef}
        style={{
          position: "absolute",
          top: 0,
          left: 0,
          pointerEvents: mode === "zone-edit" ? "auto" : "none",
        }}
      />
      {editorState === "drawing" && (
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
          }}
        >
          클릭: 꼭짓점 배치 | 우클릭: 완성 | Esc: 취소
          ({drawingPointsRef.current.length}개 꼭짓점)
        </div>
      )}
    </>
  );
}

// 외부에서 Drawing 시작을 호출할 수 있도록 export
export { type EditorState };
