/**
 * Calibrate proximal-humerus study labels against actual transformed triangles.
 * Run: node scripts/calibrate-humerus-landmarks.mjs
 * Optional inspection exports: --dump (triangles), --sections (anterior sections).
 * Anatomical region choices were visually checked in five orthographic views and
 * checked against the anatomical descriptions in OpenStax Anatomy & Physiology 2e, section 8.2.
 * Projection verifies surface membership, not anatomical accuracy. The source
 * humerus has only 1,796 triangles; groove margins and neck rings are simplified.
 * Both sides are projected independently. Output coordinates are original GLB
 * metres, not the scaled / translated presentation coordinates.
 */
import { readFile, writeFile } from 'node:fs/promises';
import { createHash } from 'node:crypto';
import { Vector3, Triangle, DoubleSide, Raycaster } from 'three';
import { GLTFLoader } from 'three/examples/jsm/loaders/GLTFLoader.js';
const root=new URL('../',import.meta.url);
const bytes=await readFile(new URL('public/models/z-anatomy-1.4.0-skeletal.glb',root));
const gltf=await new GLTFLoader().parseAsync(bytes.buffer.slice(bytes.byteOffset,bytes.byteOffset+bytes.byteLength),'');
gltf.scene.updateMatrixWorld(true);
const entries={};
gltf.scene.traverse(mesh=>{
 const id=mesh.userData.anatomyId;
 if(!mesh.isMesh||!/^appendicular-skeleton-humerus-(left|right)$/.test(id))return;
 const side=id.split('-').at(-1);const a=mesh.geometry.attributes.position,idx=mesh.geometry.index;
 const triangles=[];
 const at=i=>new Vector3().fromBufferAttribute(a,idx?idx.getX(i):i).applyMatrix4(mesh.matrixWorld);
 for(let i=0;i<(idx?idx.count:a.count);i+=3)triangles.push(new Triangle(at(i),at(i+1),at(i+2)));
 for(const material of Array.isArray(mesh.material)?mesh.material:[mesh.material])material.side=DoubleSide;
 entries[side]={id,mesh,triangles};
});
if(process.argv.includes('--dump')){
 await writeFile('/private/tmp/humerus-triangles.json',JSON.stringify(Object.fromEntries(Object.entries(entries).map(([side,e])=>[side,e.triangles.map(t=>[t.a.toArray(),t.b.toArray(),t.c.toArray()])]))));
 console.log(Object.fromEntries(Object.entries(entries).map(([s,e])=>[s,e.triangles.length])));
}
if(process.argv.includes('--sections')){
 const r=entries.right;const sections=[];
 for(let y=1.402;y>1.366;y-=.004){const points=[];for(let x=-.2;x<-.13;x+=.0005){const hits=new Raycaster(new Vector3(x,y,.1),new Vector3(0,0,-1)).intersectObject(r.mesh,false);if(hits.length)points.push(hits[0].point.toArray());}sections.push({y,points});}
 await writeFile('/private/tmp/humerus-sections.json',JSON.stringify(sections));
}
const sourceURLs=['https://openstax.org/books/anatomy-and-physiology-2e/pages/8-2-bones-of-the-upper-limb'];
const definitions=[
 {id:'humeral-head',english:'Humeral head',chinese:'肱骨头',view:'front',x:-.149,y:1.390,description:'Rounded proximal articular region, facing medially toward the scapula. / 近端朝向肩胛骨的圆形关节面区域。',basis:'Anterior surface sample within the smooth medial head region identified in anterior and medial mesh views.'},
 {id:'greater-tubercle',english:'Greater tubercle',chinese:'肱骨大结节',view:'front',seed:[-.180375,1.402916,-.022097],description:'Lateral prominence beside the humeral head. / 位于肱骨头外侧的骨性隆起。',basis:'Reprojected existing LI15 superior-lateral greater-tubercle evidence anchor onto this side\'s own humerus mesh.'},
 {id:'lesser-tubercle',english:'Lesser tubercle',chinese:'肱骨小结节',view:'front',x:-.1695,y:1.388,description:'Anterior prominence; the intertubercular groove separates it from the greater tubercle. / 前方的骨性隆起，与大结节之间为结节间沟。',basis:'Anterior positive-Z prominence in the proximal surface section; visually identified between the groove and medial head.'},
 {id:'intertubercular-groove',english:'Intertubercular groove',chinese:'结节间沟',view:'front',x:-.18,y:1.392,description:'Shallow channel between the greater and lesser tubercles; its fine margins are simplified in this mesh. / 大、小结节之间的浅沟；此网格简化了沟的细部边界。',basis:'Anterior surface trough between the lateral greater-tubercle bulge and more anterior lesser-tubercle bulge at Y=1.392 m. A regional surface pointer, not an exact traced groove.'},
 {id:'anatomical-neck',english:'Anatomical neck',chinese:'肱骨解剖颈',view:'front',x:-.15,y:1.371,description:'Margin around the humeral head; this dot shows one inferior-anterior part of that region. / 肱骨头周缘；此点示意该区域前下方的一处，并非完整环线。',basis:'Anterior-inferior transition of the rounded head region, inspected in anterior, anteromedial and medial mesh views; approximate regional example.'},
 {id:'surgical-neck',english:'Surgical neck',chinese:'肱骨外科颈',view:'front',x:-.180,y:1.356,description:'Narrowing below the proximal expansion, where it joins the shaft; the dot marks one anterior part. / 近端膨大与骨干相接的收窄区域；此点示意其前方的一处。',basis:'Anterior surface at the narrowing below the tubercles and head, before the relatively uniform shaft; approximate regional example.'},
];
function nearest(entry,seed){const p=new Vector3(...seed),q=new Vector3(),best=new Vector3();let d=Infinity,ti=-1;entry.triangles.forEach((t,i)=>{t.closestPointToPoint(p,q);const dist=q.distanceToSquared(p);if(dist<d){d=dist;ti=i;best.copy(q);}});return{position:best,triangleIndex:ti,distance:Math.sqrt(d)};}
function frontSample(entry,x,y){const ray=new Raycaster(new Vector3(x,y,.1),new Vector3(0,0,-1));const hits=ray.intersectObject(entry.mesh,false);if(!hits.length)throw new Error(`No mesh intersection: ${entry.id} ${x} ${y}`);return {position:hits[0].point,triangleIndex:hits[0].faceIndex,rayOrigin:ray.ray.origin.toArray(),rayDirection:ray.ray.direction.toArray(),intersectionCount:hits.length};}
const evidence=[];
const records=definitions.map(def=>{
 const positions={};
 for(const side of ['right','left']){
  const entry=entries[side];const sign=side==='right'?1:-1;
  const sample=def.seed?nearest(entry,[def.seed[0]*sign,def.seed[1],def.seed[2]]):frontSample(entry,def.x*sign,def.y);
  positions[side]=sample.position.toArray().map(n=>Number(n.toFixed(9)));
  const check=nearest(entry,positions[side]);
  if(check.distance>1e-7)throw new Error(`${def.id}-${side} off-surface ${check.distance}`);
  evidence.push({id:def.id,side,anatomyId:entry.id,position:positions[side],method:def.seed?'Nearest triangle projection of prior bone anchor, independently on each side':'First positive-Z-to-negative-Z ray hit, independently on each side',triangleIndex:sample.triangleIndex,rayOrigin:sample.rayOrigin,rayDirection:sample.rayDirection,rayIntersectionCount:sample.intersectionCount,distanceToMeshMetres:check.distance,passed:true,basis:def.basis});
 }
 return{id:def.id,english:def.english,chinese:def.chinese,anatomy:'appendicular-skeleton-humerus',positions,view:def.view,description:def.description,basis:def.basis,sourceURLs,precision:'Approximate model-surface study label; no subregion segmentation or exact boundary.'};
});
await writeFile(new URL('src/humerus-landmarks.json',root),JSON.stringify(records,null,2)+'\n');
await writeFile(new URL('public/humerus-landmark-evidence.json',root),JSON.stringify({model:'z-anatomy-1.4.0-skeletal.glb',sha256:createHash('sha256').update(bytes).digest('hex'),coordinateSystem:'Original shared GLB coordinates, metres; Y up; X left-positive; Z anterior-positive',scope:'Proximal humerus only; approximate anatomical study pointers on the existing simplified bone mesh. Surface membership is geometric evidence, not proof of expert anatomical accuracy. Circumferential necks and groove margins are not reconstructed or segmented.',triangleCounts:Object.fromEntries(Object.entries(entries).map(([s,e])=>[s,e.triangles.length])),sourceURLs,passed:evidence.every(e=>e.passed),validatedCount:evidence.length,results:evidence},null,2)+'\n');
await writeFile('/private/tmp/humerus-picks.json',JSON.stringify(Object.fromEntries(records.map(r=>[r.id,r.positions.right]))));
console.log(JSON.stringify({landmarks:records.length,validated:evidence.length,maximumSurfaceDistanceMetres:Math.max(...evidence.map(e=>e.distanceToMeshMetres)),positions:records.map(r=>({id:r.id,right:r.positions.right}))},null,2));
