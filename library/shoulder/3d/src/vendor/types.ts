import type { CSSProperties, ReactNode } from "react";

export type VanatomeVector3 = readonly [number, number, number];

/** A user-authored point in the atlas's original model coordinate system. */
export type VanatomeAnnotation = {
  id: string;
  label: string;
  position: VanatomeVector3;
  color?: string;
  visible?: boolean;
  /** Show the text label; the spatial marker remains selectable. */
  showLabel?: boolean;
  /** Place the text in a screen-space right column, linked to the spatial marker. */
  labelDockIndex?: number;
  /** Number of rows in the label column. */
  labelDockCount?: number;
  /** A construction guide in original model coordinates, not a procedure path. */
  guidePath?: readonly VanatomeVector3[];
  guideLabels?: readonly { label: string; position: VanatomeVector3 }[];
};

/**
 * A straight study axis drawn over the model in original model coordinates.
 * The viewer draws it through all geometry and assigns it no anatomical meaning.
 */
export type VanatomeProbe = {
  id: string;
  start: VanatomeVector3;
  end: VanatomeVector3;
  /** Colour of the thin base line. */
  color?: string;
  /** Portion drawn dashed, e.g. outside the outermost modeled surface. */
  dashedUntil?: VanatomeVector3;
  segments?: readonly { start: VanatomeVector3; end: VanatomeVector3; color: string }[];
  ticks?: readonly VanatomeVector3[];
  marker?: { position: VanatomeVector3; color: string };
  /** Text callouts stacked beside the probe with leader lines. */
  callouts?: readonly { id: string; label: string; position: VanatomeVector3; color: string; emphasis?: boolean }[];
};

export type VanatomeSurfacePickEvent = {
  /** The anatomy structure that owns the picked surface. */
  id: string;
  /** Position and normal before modelScale/modelPosition are applied. */
  position: VanatomeVector3;
  normal?: VanatomeVector3;
  modelUrl: string;
};

export type VanatomeStructure = {
  id: string;
  name: string;
  kind?: "system" | "organ" | "part";
  system: string;
  layer: string;
  parentId?: string;
  selectable?: boolean;
  objectCount?: number;
  color?: string;
  position: VanatomeVector3;
  summary?: string;
  function?: string;
  fact?: string;
};

export type VanatomeAtlas = {
  id: string;
  name: string;
  version: string;
  buildId?: string;
  modelUrl: string;
  structures: readonly VanatomeStructure[];
  attribution: string;
};

export type VanatomeAtlasComposition = {
  atlases: readonly VanatomeAtlas[];
  modelUrls: readonly string[];
  structures: readonly VanatomeStructure[];
};

export type VanatomeHierarchyNode = VanatomeStructure & {
  children: VanatomeHierarchyNode[];
};

export type VanatomeDisplayMode = "normal" | "xray" | "ghost";

export type VanatomeIsolationMode =
  | "selected"
  | "parent"
  | "parent-context";

export type VanatomeIsolationState = {
  id: string;
  mode: VanatomeIsolationMode;
};

export type VanatomeContextMenuEvent = {
  id: string;
  clientX: number;
  clientY: number;
};

export type VanatomeViewState = {
  position: VanatomeVector3;
  target: VanatomeVector3;
};

export type VanatomeLoadProgress = {
  loaded: number;
  total: number;
  percentage: number;
};

export type VanatomeFocusRejectionReason =
  | "structure-not-found"
  | "structure-not-visible"
  | "structure-has-no-visible-geometry";

/** One explicit camera action. Give every new action a unique id. */
export type VanatomeCameraRequest =
  | {
      id: number;
      kind: "point";
      /** Position in original GLB coordinates, before model scale/translation. */
      target: VanatomeVector3;
      /** World-space viewing direction; omit to retain the current angle. */
      direction?: VanatomeVector3;
      distance?: number;
      preserveDistance?: boolean;
    }
  | {
      id: number;
      kind: "structure";
      structureId: string;
      direction?: VanatomeVector3;
      /** Minimum framing distance, unless preserveDistance is true. */
      distance?: number;
      preserveDistance?: boolean;
    }
  | {
      id: number;
      kind: "orbit";
      /** Rotate around the current target while retaining the current distance. */
      direction: VanatomeVector3;
    };

export type VanatomeViewerError = {
  code: "model-load-failed" | "webgl-context-lost";
  message: string;
  modelUrl: string;
  cause?: unknown;
};

export type VanatomeViewerAppearance = {
  bodyShellId?: string | null;
  skeletonId?: string | null;
  defaultOpacity?: number;
  xrayOpacity?: number;
  ghostOpacity?: number;
  parentContextOpacity?: number;
  hoverEmissiveIntensity?: number;
  selectedDescendantEmissiveIntensity?: number;
  selectedEmissiveIntensity?: number;
  pulseSelection?: boolean;
};

type VanatomeViewerBaseProps = {
  /** When supplied (including null), camera motion is controlled only by these
   * one-shot requests. Selection, visibility, labels and resize do not refocus. */
  cameraRequest?: VanatomeCameraRequest | null;
  annotations?: readonly VanatomeAnnotation[];
  /** Study axes drawn on top of the model (see VanatomeProbe). */
  probes?: readonly VanatomeProbe[];
  selectedAnnotationId?: string | null;
  onAnnotationSelect?: (id: string) => void;
  /** Editing consumes a surface click instead of selecting an anatomy structure. */
  annotationEditing?: boolean;
  onSurfacePick?: (event: VanatomeSurfacePickEvent) => void;
  annotationFocusPosition?: VanatomeVector3 | null;
  /** Change this key to focus the same annotation again. */
  annotationFocusKey?: string | number;
  /** Optional direction for an explicit view change; omit to preserve the orbit angle. */
  annotationFocusDirection?: VanatomeVector3 | null;
  /** Keep the current orbit distance when moving between nearby landmarks. */
  preserveAnnotationFocusDistance?: boolean;
  selectedId?: string | null;
  hoveredId?: string | null;
  isolatedId?: string | null;
  isolation?: VanatomeIsolationState | null;
  visibleLayers?: readonly string[];
  alwaysVisibleIds?: readonly string[];
  hiddenIds?: readonly string[];
  displayMode?: VanatomeDisplayMode;
  focusRequestKey?: string | number;
  resetViewKey?: string | number;
  onSelect?: (id: string | null) => void;
  onHover?: (id: string | null) => void;
  onStructureContextMenu?: (event: VanatomeContextMenuEvent) => void;
  onEscape?: () => void;
  onLoadStart?: (modelUrl: string) => void;
  onLoadProgress?: (progress: VanatomeLoadProgress) => void;
  onModelReady?: (modelUrl: string) => void;
  onReady?: () => void;
  onError?: (error: VanatomeViewerError) => void;
  onFocusRejected?: (
    id: string,
    reason: VanatomeFocusRejectionReason,
  ) => void;
  onCameraChange?: (view: VanatomeViewState) => void;
  onInteractionStart?: () => void;
  onInteractionEnd?: () => void;
  className?: string;
  style?: CSSProperties;
  ariaLabel?: string;
  loadingFallback?: ReactNode;
  incrementalLoadingFallback?: ReactNode;
  errorFallback?: ReactNode | ((error: VanatomeViewerError) => ReactNode);
  modelScale?: number;
  modelPosition?: VanatomeVector3;
  initialCameraPosition?: VanatomeVector3;
  initialCameraTarget?: VanatomeVector3;
  focusDistance?: number;
  focusPadding?: number;
  cameraAnimationDuration?: number;
  respectReducedMotion?: boolean;
  enablePan?: boolean;
  minDistance?: number;
  maxDistance?: number;
  appearance?: VanatomeViewerAppearance;
};

export type VanatomeViewerProps = VanatomeViewerBaseProps & (
  | {
      /** Existing single-model source. */
      atlas: VanatomeAtlas;
      atlases?: never;
    }
  | {
      /** Additive multi-model source. */
      atlas?: never;
      atlases: readonly VanatomeAtlas[];
    }
);

export type VanatomeController = {
  selectedId: string | null;
  isolatedId: string | null;
  visibleLayers: readonly string[];
  focusRequestKey: number;
  resetViewKey: number;
  select: (id: string | null) => void;
  focus: (id?: string | null) => void;
  isolate: (id?: string | null) => void;
  reset: () => void;
  setVisibleLayers: (layers: readonly string[]) => void;
  toggleLayer: (layer: string) => void;
};

export type VanatomeControllerState = Omit<
  VanatomeController,
  "isolate"
> & {
  isolation: VanatomeIsolationState | null;
  isolate: (
    id?: string | null,
    mode?: VanatomeIsolationMode,
  ) => void;
  clear: () => void;
};
