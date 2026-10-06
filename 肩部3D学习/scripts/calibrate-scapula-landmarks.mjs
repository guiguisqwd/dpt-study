/** Reproduce model-specific scapular region markers on the original bilateral GLB meshes. */
import { readFile, writeFile } from 'node:fs/promises';
import { createHash } from 'node:crypto';
import { Vector3, Triangle, Raycaster, DoubleSide } from 'three';
import { GLTFLoader } from 'three/examples/jsm/loaders/GLTFLoader.js';

const root = new URL('../', import.meta.url);
const bytes = await readFile(new URL('public/models/z-anatomy-1.4.0-skeletal.glb', root));
const gltf = await new GLTFLoader().parseAsync(bytes.buffer.slice(bytes.byteOffset, bytes.byteOffset + bytes.byteLength), '');
gltf.scene.updateMatrixWorld(true);
const previous = JSON.parse(await readFile(new URL('public/calibration-evidence.json', root), 'utf8')).references;
const source = 'https://openstax.org/books/anatomy-and-physiology-2e/pages/8-1-the-pectoral-girdle';
const definitions = [
  ['scapular-spine', 'Scapular spine', '肩胛冈', 'back', 'The prominent ridge on the back of the scapula. The dot represents one point on this extended ridge. / 肩胛骨后面的骨嵴；点标记骨嵴上的代表位置。'],
  ['inferior-angle', 'Inferior angle', '肩胛骨下角', 'back', 'The lowest corner of the scapula. / 肩胛骨最下方的角。'],
  ['acromion', 'Acromion', '肩峰', 'back', 'The expanded lateral continuation of the scapular spine, above the shoulder joint. / 肩胛冈向外延续形成的肩部骨性突出。'],
  ['infraspinous-fossa', 'Infraspinous fossa', '冈下窝', 'back', 'The broad posterior scapular region below the spine. The dot identifies a representative bone-surface position, not the whole boundary. / 肩胛冈下方的后面骨区；点表示区域中的骨面位置，不代表完整边界。'],
  ['supraspinous-fossa', 'Supraspinous fossa', '冈上窝', 'back', 'The smaller posterior scapular region above the spine. The dot identifies a representative bone-surface position, not the whole boundary. / 肩胛冈上方的后面骨区；点表示区域中的骨面位置，不代表完整边界。'],
  ['anterolateral-acromion', 'Anterolateral acromion', '肩峰前外侧', 'front', 'The front and lateral part of the acromion, shown by a representative bone-surface point. / 肩峰前外侧区域的代表性骨面标记。'],
  ['posterolateral-acromion', 'Posterolateral acromion', '肩峰后外侧', 'back', 'The back and lateral part of the acromion, shown by a representative bone-surface point. / 肩峰后外侧区域的代表性骨面标记。'],
];
const records = definitions.map(([id, english, chinese, view, description]) => ({id, english, chinese, anatomy: 'appendicular-skeleton-scapula', positions: {}, view, description, basis: 'Model-specific representative bone-surface point; region boundaries are not segmented. / 本模型上的骨面代表位置，未分割完整结构边界。', sourceURLs: [source]}));
const evidence = { coordinateSystem: 'Original GLB metres; Y superior; X positive to anatomical left; Z anterior.', modelSHA256: createHash('sha256').update(bytes).digest('hex'), meaning: 'Model-specific anatomical surface annotations, not segmented structures or clinical acupoints.', sourceURLs: [source], validationToleranceMetres: 1e-7, sides: {} };
const plotData = {};
for (const side of ['right','left']) {
  const meshes = [], triangles = [];
  gltf.scene.traverse(mesh => {
    if (!mesh.isMesh || mesh.userData.anatomyId !== `appendicular-skeleton-scapula-${side}`) return;
    meshes.push(mesh);
    for (const material of Array.isArray(mesh.material) ? mesh.material : [mesh.material]) material.side = DoubleSide;
    const position = mesh.geometry.attributes.position, index = mesh.geometry.index;
    const get = i => new Vector3().fromBufferAttribute(position, index ? index.getX(i) : i).applyMatrix4(mesh.matrixWorld);
    for(let i=0;i<(index?.count ?? position.count);i+=3) triangles.push(new Triangle(get(i), get(i+1), get(i+2)));
  });
  if (!meshes.length) throw Error(`Scapula missing: ${side}`);
  const nearest = seed => {
    const p = new Vector3(...seed), q = new Vector3();
    let best = Infinity, position;
    for (const triangle of triangles) { triangle.closestPointToPoint(p,q); const d = p.distanceToSquared(q); if(d<best) { best=d; position=q.toArray(); } }
    return { position, distanceMetres: Math.sqrt(best) };
  };
  const posterior = (x,y) => {
    const hits = new Raycaster(new Vector3(x,y,-1), new Vector3(0,0,1)).intersectObjects(meshes,false);
    if (!hits.length) throw Error(`No posterior scapular surface at ${x},${y}`);
    return { position: hits[0].point.toArray(), rayIntersectionCount: hits.length };
  };
  const si11 = previous[`SI11-${side}`], si12 = previous[`SI12-${side}`];
  await writeFile(`/private/tmp/scapula-${side}-triangles.json`, JSON.stringify(triangles.map(t=>[t.a.toArray(),t.b.toArray(),t.c.toArray()])));
  const anteriorAnchor = previous[`LI15-${side}`].anchors[0].position;
  const posteriorAnchor = previous[`TE14-${side}`].anchors[0].position;
  const acromionSeed = anteriorAnchor.map((v,i)=>(v+posteriorAnchor[i])/2);
  const acromionHits = new Raycaster(new Vector3(acromionSeed[0],2,acromionSeed[2]),new Vector3(0,-1,0)).intersectObjects(meshes,false);
  if (!acromionHits.length) throw Error('No acromial superior surface');
  const selected = {
    'scapular-spine': { ...nearest(si11.landmarks.spineCrestMidpointApprox), method: 'Nearest triangle projection of prior ridge arc-length midpoint, independently evaluated on each side.' },
    'inferior-angle': { position: triangles.flatMap(t=>[t.a,t.b,t.c]).reduce((a,b)=>a.y<b.y?a:b).toArray(), method: 'Minimum Y scapula vertex, independently evaluated on each side.' },
    'acromion': { position: acromionHits[0].point.toArray(), method: 'Midpoint XZ between prior anterior/posterior acromial region anchors; downward ray picks actual superior scapular surface.' },
    'infraspinous-fossa': { ...posterior(si11.oneThirdOnLandmarkLine[0],si11.oneThirdOnLandmarkLine[1]), method: 'Posterior-to-anterior ray at prior below-spine regional XY, first actual scapular surface hit. This is bone, not the infraspinatus-muscle center.' },
    'supraspinous-fossa': { ...posterior(side === 'right' ? -0.087 : 0.087,1.388), method: 'Posterior-to-anterior ray at manually identified medial supraspinous-fossa XY (absolute X 0.087 m, Y 1.388 m), first actual scapular surface hit on each side. The earlier supraspinatus center projects outside the bone and is deliberately not reused.' },
    'anterolateral-acromion': { ...nearest(anteriorAnchor), method: 'Nearest triangle projection of prior anterolateral acromion region anchor, independently evaluated on each side.' },
    'posterolateral-acromion': { ...nearest(posteriorAnchor), method: 'Nearest triangle projection of prior posterolateral acromion region anchor, independently evaluated on each side.' },
  };
  evidence.sides[side] = {};
  for(const [id,record] of Object.entries(selected)) {
    const position=record.position.map(v=>Number(v.toFixed(9)));
    const distance=nearest(position).distanceMetres;
    if(distance>evidence.validationToleranceMetres) throw Error(`Off mesh: ${id}-${side}: ${distance}`);
    records.find(r=>r.id===id).positions[side]=position;
    evidence.sides[side][id]={...record, position, verifiedDistanceToActualBoneSurfaceMetres: distance, passed: true};
  }
  plotData[side]={triangles:triangles.map(t=>[t.a.toArray(),t.b.toArray(),t.c.toArray()]),points: Object.entries(selected).map(([id,r])=>({id,position:r.position}))};
}
evidence.passedCount = 14;
await writeFile(new URL('src/scapula-landmarks.json', root), JSON.stringify(records,null,2)+'\n');
await writeFile(new URL('public/scapula-landmark-evidence.json', root), JSON.stringify(evidence,null,2)+'\n');
await writeFile('/private/tmp/scapula-landmark-plot-data.json',JSON.stringify(plotData));
console.log(JSON.stringify({passed: true, count:14, records},null,2));
