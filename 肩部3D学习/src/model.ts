import type { VanatomeAtlas, VanatomeVector3 } from './vendor/types';

// Shared atlas coordinates; regional topics supply only their structure mappings.
export const modelVersion = 'vanatome-1.4.0-994e6cc8ffbb212e';
export const modelScale = 7;
export const modelPosition: VanatomeVector3 = [0, -6.1, 0];

export async function loadAtlases(): Promise<VanatomeAtlas[]> {
  return Promise.all(['muscular', 'skeletal'].map(async system => {
    const res = await fetch(`./models/${system}.metadata.json`);
    if (!res.ok) throw new Error('Unable to load model metadata / 无法读取模型结构清单');
    const meta = await res.json();
    return {
      id: 'vanatome-human-' + system,
      name: 'Vanatome ' + system,
      version: meta.atlasVersion,
      buildId: meta.buildId,
      modelUrl: `./models/z-anatomy-1.4.0-${system}.glb`,
      structures: meta.structures,
      attribution: 'Z-Anatomy / BodyParts3D · CC BY-SA 4.0 · Vanatome',
    };
  }));
}
