import { Html, Line } from "@react-three/drei";
import { useFrame, useThree } from "@react-three/fiber";
import { Fragment, useRef } from "react";
import { Vector3 } from "three";
import type { VanatomeAnnotation, VanatomeVector3 } from "./types.js";

type AnnotationLayerProps = {
  annotations?: readonly VanatomeAnnotation[];
  selectedAnnotationId?: string | null;
  onAnnotationSelect?: (id: string) => void;
  modelScale: number;
  modelPosition: VanatomeVector3;
};

function AnnotationMarker({ annotation, selected, onSelect, modelScale, modelPosition }: {
  annotation: VanatomeAnnotation;
  selected: boolean;
  onSelect?: (id: string) => void;
  modelScale: number;
  modelPosition: VanatomeVector3;
}) {
  const { camera, size } = useThree();
  const labelRef = useRef<HTMLButtonElement>(null);
  const lineRef = useRef<SVGLineElement>(null);
  const projected = useRef(new Vector3());
  const color = annotation.color ?? "#f59e0b";
  const showLabel = selected || annotation.showLabel !== false;
  const docked = Number.isFinite(annotation.labelDockIndex) && annotation.labelDockIndex! >= 0;
  const dockIndex = Math.max(0, Math.floor(annotation.labelDockIndex ?? 0));
  const dockCount = Math.max(1, Math.floor(annotation.labelDockCount ?? 1), dockIndex + 1);
  const usableHeight = Math.max(0, size.height - 100);
  const dockRowHeight = Math.min(50, usableHeight / dockCount);
  const compactDock = docked && dockRowHeight < 46;

  useFrame(() => {
    if (!docked || !showLabel || !labelRef.current || !lineRef.current) return;
    if (size.width <= 0 || size.height <= 0) return;
    const point = projected.current.set(
      annotation.position[0] * modelScale + modelPosition[0],
      annotation.position[1] * modelScale + modelPosition[1],
      annotation.position[2] * modelScale + modelPosition[2],
    ).project(camera);
    const px = (point.x + 1) * size.width / 2;
    const py = (1 - point.y) * size.height / 2;
    if (!Number.isFinite(px) || !Number.isFinite(py)) return;
    const targetX = Math.max(12, size.width - 182);
    const targetY = 60 + (usableHeight - dockRowHeight * dockCount) / 2 + dockRowHeight * (dockIndex + 0.5);
    const dx = targetX - px;
    const dy = targetY - py;
    labelRef.current.style.left = `${dx}px`;
    labelRef.current.style.top = `${dy}px`;
    lineRef.current.setAttribute("x2", String(dx));
    lineRef.current.setAttribute("y2", String(dy));
    // Docked labels and their leaders become visible only after projection.
    // Their initial DOM coordinates are beside the point, not in the dock.
    labelRef.current.style.visibility = "visible";
    lineRef.current.style.visibility = "visible";
  });

  const select = (event: React.MouseEvent<HTMLButtonElement>) => {
    event.stopPropagation();
    onSelect?.(annotation.id);
  };
  const stop = (event: React.SyntheticEvent) => event.stopPropagation();
  return <group position={[...annotation.position]}>
    <mesh renderOrder={1000} raycast={() => undefined}>
      <sphereGeometry args={[selected ? 0.004 : 0.003, 16, 12]} />
      <meshBasicMaterial color={color} transparent depthTest={false} depthWrite={false} />
    </mesh>
    <Html occlude={false} zIndexRange={selected ? [140, 130] : [120, 100]} style={{ pointerEvents: "none" }}>
      <div style={{ position: "relative", width: 0, height: 0, pointerEvents: "none" }}>
        {docked && showLabel && <svg aria-hidden="true" width="1" height="1" style={{ position: "absolute", left: 0, top: 0, overflow: "visible", pointerEvents: "none" }}>
          <line ref={lineRef} x1="0" y1="0" x2="0" y2="0" stroke={color} strokeWidth={selected ? 1.25 : 0.85} strokeOpacity={selected ? 0.85 : 0.55} style={{ visibility: "hidden" }} />
        </svg>}
        <button type="button" className="vanatome-annotation" aria-label={`选择标记：${annotation.label}`} aria-pressed={selected} title={annotation.label}
          onPointerDown={stop} onPointerUp={stop} onDoubleClick={stop} onClick={select}
          style={{ position: "absolute", left: 0, top: 0, transform: "translate(-50%, -50%)", width: 16, height: 16, padding: 0, border: `2px solid ${color}`, borderRadius: "50%", background: selected ? color : "rgba(15,23,42,.6)", boxShadow: "0 0 0 2px rgba(15,23,42,.5)", cursor: "pointer", pointerEvents: "auto" }} />
        {showLabel && <button ref={labelRef} type="button" className="vanatome-annotation" data-compact={compactDock || undefined} aria-label={`聚焦标记：${annotation.label}`} aria-pressed={selected} title={annotation.label}
          onPointerDown={stop} onPointerUp={stop} onDoubleClick={stop} onClick={select}
          style={{ position: "absolute", left: 14, top: 0, visibility: docked ? "hidden" : "visible", transform: "translateY(-50%)", width: docked ? 170 : "max-content", maxWidth: 180, minHeight: docked ? Math.max(0, Math.min(42, dockRowHeight - 3)) : undefined, padding: compactDock ? "2px 7px" : "4px 7px", borderRadius: 6, border: `1px solid ${selected ? color : "rgba(148,163,184,.5)"}`, background: "rgba(15,23,42,.93)", boxShadow: "0 2px 8px rgba(0,0,0,.24)", color: "#f8fafc", textAlign: "left", font: "inherit", fontSize: compactDock ? 10 : 12, lineHeight: compactDock ? 1.2 : 1.45, whiteSpace: "pre-line", overflowWrap: "anywhere", cursor: "pointer", pointerEvents: "auto" }}><span>{annotation.label}</span></button>}
      </div>
    </Html>
  </group>;
}

/** Generic study annotations; the viewer does not assign anatomical meaning. */
export function AnnotationLayer({
  annotations = [],
  selectedAnnotationId,
  onAnnotationSelect,
  modelScale,
  modelPosition,
}: AnnotationLayerProps) {
  return (
    <group scale={modelScale} position={[...modelPosition]}>
      {annotations.filter((annotation) => annotation.visible !== false).map((annotation) => {
        const selected = annotation.id === selectedAnnotationId;
        return (
          <Fragment key={annotation.id}>
          {annotation.guidePath && annotation.guidePath.length > 1 && <Line points={annotation.guidePath.map(p => [...p] as [number, number, number])} color="#b6c3ab" lineWidth={1.5} dashed dashSize={0.012} gapSize={0.008} depthTest={false} transparent opacity={0.8} raycast={() => undefined} />}
          {annotation.guideLabels?.map(guide => <group key={guide.label} position={[...guide.position]}>
            <mesh renderOrder={999} raycast={() => undefined}><sphereGeometry args={[0.002, 10, 8]} /><meshBasicMaterial color="#c8d6c0" depthTest={false} /></mesh>
            <Html occlude={false} zIndexRange={[90,80]} style={{pointerEvents:'none'}}><span className="landmark-label">{guide.label}</span></Html>
          </group>)}
          <AnnotationMarker annotation={annotation} selected={selected} onSelect={onAnnotationSelect} modelScale={modelScale} modelPosition={modelPosition} />
          </Fragment>
        );
      })}
    </group>
  );
}
