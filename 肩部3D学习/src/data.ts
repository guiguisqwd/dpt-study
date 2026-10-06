import type { VanatomeAtlas, VanatomeVector3 } from './vendor/types';

export type PointKind = 'unconfirmed' | 'surface-reference' | 'deep-reference';
export type Placement = { position: [number, number, number]; anatomyId: string; kind: PointKind; note: string };
export type Placements = Record<string, Placement>;
export const storageKey = 'shoulder-spatial-study-v1';
export const modelVersion = 'vanatome-1.4.0-994e6cc8ffbb212e';
export const modelScale = 7;
export const modelPosition: VanatomeVector3 = [0, -6.1, 0];

export const points = [
  { id: 'SI11', name: '天宗', english: 'Tianzong', color: '#e6b96b', anatomy: 'rotator-cuff-muscles-infraspinatus-muscle', location: '肩胛冈中点至肩胛下角连线，上 1/3 与下 2/3 交界的凹陷。', cue: '先在模型中辨认肩胛冈与下角，再核对位置。', related: '冈下窝、冈下肌、肩胛骨', page: '93' },
  { id: 'SI12', name: '秉风', english: 'Bingfeng', color: '#ed8a79', anatomy: 'rotator-cuff-muscles-supraspinatus-muscle', location: '冈上窝内，肩胛冈中点上方。', cue: '肩胛冈是区分冈上窝与冈下窝的关键标志。', related: '冈上窝、冈上肌、肩胛冈', page: '93' },
  { id: 'SI9', name: '肩贞', english: 'Jianzhen', color: '#85bfad', anatomy: 'rotator-cuff-muscles-teres-minor-muscle', location: '肩关节后下方，腋后纹上 1 骨度分寸。', cue: '标准定位涉及上臂内收姿势与腋后纹。', related: '肩后区、小圆肌、三角肌后部', page: '92' },
  { id: 'LI15', name: '肩髃', english: 'Jianyu', color: '#8cb5e8', anatomy: 'deltoid-muscles-acromial-part-of-deltoid-muscle', location: '肩峰外侧缘前端与肱骨大结节之间的凹陷。', cue: '标准定位涉及上臂外展姿势；需要核对姿势差异。', related: '肩峰前外侧、肱骨大结节、三角肌', page: '41' },
  { id: 'TE14', name: '肩髎', english: 'Jianliao', color: '#ba9ad9', anatomy: 'deltoid-muscles-scapular-spinal-part-of-deltoid-muscle', location: '肩峰角与肱骨大结节之间的凹陷。', cue: '标准定位涉及屈肘、上臂外展姿势。', related: '肩峰后外侧、肱骨大结节、三角肌后部', page: '164' },
] as const;

export const anatomyNames: Record<string, string> = {
  'rotator-cuff-muscles-supraspinatus-muscle': '冈上肌',
  'rotator-cuff-muscles-infraspinatus-muscle': '冈下肌',
  'rotator-cuff-muscles-teres-minor-muscle': '小圆肌',
  'rotator-cuff-muscles-subscapularis-muscle': '肩胛下肌',
  'deltoid-muscles-acromial-part-of-deltoid-muscle': '三角肌 · 肩峰部',
  'deltoid-muscles-clavicular-part-of-deltoid-muscle': '三角肌 · 锁骨部',
  'deltoid-muscles-scapular-spinal-part-of-deltoid-muscle': '三角肌 · 肩胛冈部',
  'appendicular-skeleton-scapula': '肩胛骨',
  'appendicular-skeleton-clavicle': '锁骨',
  'appendicular-skeleton-humerus': '肱骨',
};

export const anatomyEnglish: Record<string, string> = {
  'rotator-cuff-muscles-supraspinatus-muscle': 'Supraspinatus',
  'rotator-cuff-muscles-infraspinatus-muscle': 'Infraspinatus',
  'rotator-cuff-muscles-teres-minor-muscle': 'Teres minor',
  'rotator-cuff-muscles-subscapularis-muscle': 'Subscapularis',
  'deltoid-muscles-acromial-part-of-deltoid-muscle': 'Deltoid · acromial part',
  'deltoid-muscles-clavicular-part-of-deltoid-muscle': 'Deltoid · clavicular part',
  'deltoid-muscles-scapular-spinal-part-of-deltoid-muscle': 'Deltoid · spinal part',
  'appendicular-skeleton-scapula': 'Scapula',
  'appendicular-skeleton-clavicle': 'Clavicle',
  'appendicular-skeleton-humerus': 'Humerus',
};
export const relatedEnglish: Record<string,string> = {
  SI11: 'Infraspinous fossa · Infraspinatus · Scapula',
  SI12: 'Supraspinous fossa · Supraspinatus · Spine of scapula',
  SI9: 'Posterior shoulder · Teres minor · Posterior deltoid',
  LI15: 'Anterolateral acromion · Greater tubercle of humerus · Deltoid',
  TE14: 'Posterolateral acromion · Greater tubercle of humerus · Posterior deltoid',
};

export function anatomyLabel(id: string, showChinese = true) {
  const side = id.endsWith('-right') ? 'Right · ' : id.endsWith('-left') ? 'Left · ' : '';
  const base = id.replace(/-(right|left)$/, '');
  return side + (anatomyEnglish[base] || base) + (showChinese && anatomyNames[base] ? '\n' + anatomyNames[base] : '');
}
export function validatePlacements(value: unknown): Placements {
  if (!value || typeof value !== 'object' || Array.isArray(value)) throw new Error('位置数据格式不正确');
  const result: Placements = {};
  for (const [id, raw] of Object.entries(value)) {
    if (!points.some(p => id === p.id + '-right' || id === p.id + '-left')) throw new Error('包含未知标记');
    if (!raw || typeof raw !== 'object') throw new Error('标记格式不正确');
    const point = raw as Placement;
    if (!Array.isArray(point.position) || point.position.length !== 3 || !point.position.every(v => typeof v === 'number' && Number.isFinite(v))) throw new Error('坐标必须包含三个有限数值');
    const [x, y, z] = point.position;
    if (Math.abs(x) > 0.7 || y < 0 || y > 2 || Math.abs(z) > 0.7) throw new Error('坐标超出此人体模型的范围');
    if (!['unconfirmed', 'surface-reference', 'deep-reference'].includes(point.kind)) throw new Error('标记类型不正确');
    if (typeof point.anatomyId !== 'string' || typeof point.note !== 'string') throw new Error('标记说明不完整');
    const side = id.endsWith('-right') ? 'right' : 'left';
    if (!Object.keys(anatomyNames).some(base => point.anatomyId === `${base}-${side}`)) throw new Error('起点结构不属于该侧肩部');
    if ((side === 'right' && x > 0) || (side === 'left' && x < 0)) throw new Error('坐标与左右侧别不一致');
    result[id] = { position: [...point.position], anatomyId: point.anatomyId, kind: point.kind, note: point.note.slice(0, 3000) };
  }
  return result;
}
export async function loadAtlases(): Promise<VanatomeAtlas[]> {
  return Promise.all(['muscular', 'skeletal'].map(async system => {
    const res = await fetch(`./models/${system}.metadata.json`);
    if (!res.ok) throw new Error('无法读取模型结构清单');
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
