import { Html, Line } from "@react-three/drei";
import { useFrame, useThree } from "@react-three/fiber";
import { Fragment, useMemo, useRef } from "react";
import { Vector3 } from "three";
import { layoutProbeCallouts } from "./probeLayout.js";
import type { VanatomeProbe, VanatomeVector3 } from "./types.js";

type ProbeLayerProps = {
  probes?: readonly VanatomeProbe[];
  modelScale: number;
  modelPosition: VanatomeVector3;
};

// Probes draw after the model and ignore depth so they stay visible inside muscle and bone.
const PROBE_RENDER_ORDER = 1001;
const DOCK_COLUMN = 190; // AnnotationLayer docks labels in the right-hand 182 px.
const noRaycast = () => undefined;
const points = (a: VanatomeVector3, b: VanatomeVector3) => [[...a], [...b]] as [number, number, number][];

function ProbeCallouts({ probe, modelScale, modelPosition }: {
  probe: VanatomeProbe;
  modelScale: number;
  modelPosition: VanatomeVector3;
}) {
  const { camera, size } = useThree();
  const callouts = probe.callouts ?? [];
  const containerRef = useRef<HTMLDivElement>(null);
  const labelRefs = useRef<(HTMLDivElement | null)[]>([]);
  const lineRefs = useRef<(SVGLineElement | null)[]>([]);
  const scratch = useMemo(() => new Vector3(), []);
  const compact = size.width < 520;
  const width = compact ? 124 : 150;

  useFrame(() => {
    const container = containerRef.current;
    if (!container || !callouts.length || size.width <= 0 || size.height <= 0) return;
    const toScreen = (p: VanatomeVector3) => {
      scratch.set(p[0] * modelScale + modelPosition[0], p[1] * modelScale + modelPosition[1], p[2] * modelScale + modelPosition[2]).project(camera);
      return { x: (scratch.x + 1) * size.width / 2, y: (1 - scratch.y) * size.height / 2, inFront: scratch.z > -1 && scratch.z < 1 };
    };
    const anchor = toScreen(probe.start);
    const end = toScreen(probe.end);
    const targets = callouts.map(callout => toScreen(callout.position));
    if (!anchor.inFront || !end.inFront || targets.some(t => !t.inFront || !Number.isFinite(t.x) || !Number.isFinite(t.y))) {
      container.style.visibility = "hidden";
      return;
    }
    const heights = callouts.map((_, i) => labelRefs.current[i]?.offsetHeight || 30);
    const layout = layoutProbeCallouts({
      targets,
      extent: [anchor, end, ...targets],
      heights,
      width,
      viewport: size,
      reservedRight: DOCK_COLUMN,
      reservedTop: 46,
      reservedBottom: 34,
    });
    callouts.forEach((_, i) => {
      const label = labelRefs.current[i], line = lineRefs.current[i];
      if (!label || !line) return;
      const left = layout.x - anchor.x, top = layout.ys[i] - anchor.y;
      label.style.left = `${left}px`;
      label.style.top = `${top}px`;
      line.setAttribute("x1", String(targets[i].x - anchor.x));
      line.setAttribute("y1", String(targets[i].y - anchor.y));
      line.setAttribute("x2", String(layout.side === "left" ? left + width : left));
      line.setAttribute("y2", String(top + heights[i] / 2));
    });
    // Shown only after the first layout, so labels never flash beside the anchor.
    container.style.visibility = "visible";
  });

  if (!callouts.length) return null;
  return <group position={[...probe.start]}>
    <Html occlude={false} zIndexRange={[110, 105]} style={{ pointerEvents: "none" }}>
      <div ref={containerRef} style={{ position: "relative", width: 0, height: 0, pointerEvents: "none", visibility: "hidden" }}>
        <svg aria-hidden="true" width="1" height="1" style={{ position: "absolute", left: 0, top: 0, overflow: "visible", pointerEvents: "none" }}>
          {callouts.map((callout, i) => <line key={callout.id} ref={el => { lineRefs.current[i] = el; }} x1="0" y1="0" x2="0" y2="0" stroke={callout.color} strokeWidth={callout.emphasis ? 1.3 : 0.9} strokeOpacity={0.85} />)}
        </svg>
        {callouts.map((callout, i) => <div key={callout.id} ref={el => { labelRefs.current[i] = el; }} className="vanatome-probe-callout" data-emphasis={callout.emphasis || undefined}
          style={{ position: "absolute", left: 0, top: 0, width, boxSizing: "border-box", padding: compact ? "2px 6px" : "3px 7px", borderRadius: 5, borderLeft: `3px solid ${callout.color}`, background: "rgba(13,22,19,.9)", boxShadow: "0 2px 8px rgba(0,0,0,.28)", color: "#f1f5f2", fontSize: compact ? 10 : 11, lineHeight: 1.35, whiteSpace: "pre-line", overflowWrap: "anywhere", pointerEvents: "none" }}>{callout.label}</div>)}
      </div>
    </Html>
  </group>;
}

function ProbeGeometry({ probe }: { probe: VanatomeProbe }) {
  // Probes are rebuilt only when the probe changes, not on every hover re-render of the scene.
  const lines = useMemo(() => ({
    base: points(probe.start, probe.end),
    dashed: probe.dashedUntil ? points(probe.start, probe.dashedUntil) : null,
    segments: (probe.segments ?? []).map(segment => ({ points: points(segment.start, segment.end), color: segment.color })),
  }), [probe]);
  return <>
    <Line points={lines.base} color={probe.color ?? "#e8efe9"} lineWidth={1.4} transparent opacity={0.75} depthTest={false} depthWrite={false} renderOrder={PROBE_RENDER_ORDER} raycast={noRaycast} />
    {lines.dashed && <Line points={lines.dashed} color="#f4f7f5" lineWidth={2.2} dashed dashSize={0.0025} gapSize={0.0018} transparent opacity={0.9} depthTest={false} depthWrite={false} renderOrder={PROBE_RENDER_ORDER + 1} raycast={noRaycast} />}
    {lines.segments.map((segment, i) => <Line key={i} points={segment.points} color={segment.color} lineWidth={4.5} transparent opacity={0.95} depthTest={false} depthWrite={false} renderOrder={PROBE_RENDER_ORDER + 2} raycast={noRaycast} />)}
    {probe.ticks?.map((tick, i) => <mesh key={i} position={[...tick]} renderOrder={PROBE_RENDER_ORDER + 3} raycast={noRaycast}>
      <sphereGeometry args={[0.0011, 10, 8]} />
      <meshBasicMaterial color="#f8faf8" transparent depthTest={false} depthWrite={false} />
    </mesh>)}
    {probe.marker && <mesh position={[...probe.marker.position]} renderOrder={PROBE_RENDER_ORDER + 4} raycast={noRaycast}>
      <sphereGeometry args={[0.0052, 18, 14]} />
      <meshBasicMaterial color={probe.marker.color} transparent opacity={0.38} depthTest={false} depthWrite={false} />
    </mesh>}
  </>;
}

/** Generic study axes drawn through the model; the viewer assigns them no anatomical meaning. */
export function ProbeLayer({ probes = [], modelScale, modelPosition }: ProbeLayerProps) {
  if (!probes.length) return null;
  return (
    <group scale={modelScale} position={[...modelPosition]}>
      {probes.map(probe => (
        <Fragment key={probe.id}>
          <ProbeGeometry probe={probe} />
          <ProbeCallouts probe={probe} modelScale={modelScale} modelPosition={modelPosition} />
        </Fragment>
      ))}
    </group>
  );
}
