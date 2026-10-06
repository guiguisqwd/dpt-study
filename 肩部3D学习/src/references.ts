import raw from './model-references.json';
import type { Placement } from './data';
import type { VanatomeVector3 } from './vendor/types';

export type ModelReference = Placement & {
  status: 'model-reference';
  basis: 'bone-landmarks' | 'anatomical-region';
  method: string;
  limitation: string;
  guidePath?: VanatomeVector3[];
  guideLabels?: { label: string; position: VanatomeVector3 }[];
};
export const referenceVersion = 'shoulder-model-reference-2026-10-06-v1';
export const modelReferences = raw as unknown as Record<string, ModelReference>;
