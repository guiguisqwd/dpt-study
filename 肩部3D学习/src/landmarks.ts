import humerus from './humerus-landmarks.json';
import scapula from './scapula-landmarks.json';
import type { VanatomeVector3 } from './vendor/types';

export type BoneName = 'humerus' | 'scapula';
export type BoneLandmark = {
  id: string;
  english: string;
  chinese: string;
  anatomy: string;
  positions: { right: VanatomeVector3; left: VanatomeVector3 };
  view: 'front' | 'back' | 'side';
  description: string;
  basis: string;
  sourceURLs: string[];
};

export const boneLandmarks = [...humerus, ...scapula] as unknown as BoneLandmark[];
export const landmarkById = Object.fromEntries(boneLandmarks.map(item => [item.id, item]));
export const landmarksForBone = (bone: BoneName) => boneLandmarks.filter(item => item.anatomy === `appendicular-skeleton-${bone}`);
export function boneFocus(bone: BoneName, side: 'right' | 'left'): VanatomeVector3 {
  const items = landmarksForBone(bone);
  if (bone === 'scapula') return [0, 1, 2].map(axis => {
    const values = items.map(item => item.positions[side][axis]);
    return (Math.min(...values) + Math.max(...values)) / 2;
  }) as unknown as VanatomeVector3;
  return [0, 1, 2].map(axis => items.reduce((sum, item) => sum + item.positions[side][axis], 0) / items.length) as unknown as VanatomeVector3;
}
