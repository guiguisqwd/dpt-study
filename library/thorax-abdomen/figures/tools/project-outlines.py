#!/usr/bin/env python3
"""Project 3D model meshes to 2D outlines, so the chapter's figures sit on the same bones as the 3D viewer.

Run once when the structure list changes (needs: pip install trimesh shapely):
    python3 library/thorax-abdomen/figures/tools/project-outlines.py
Writes outlines.json next to this file: {view: {structureId: [[ [x, y], ... ], ...]}} in model metres, y pointing down.
Views: ant (from the front), post (from behind), lat (right side seen from the right), sup (from above, anterior up),
inf (from below, anterior up; right side on image left, the lithotomy view of the perineum).
build-figures.py only reads the JSON (no 3D libraries needed).
Adapted from library/lumbar/figures/tools/project-outlines.py."""
import json
from pathlib import Path
import numpy as np
import trimesh
from shapely.geometry import Polygon
from shapely.ops import unary_union

ROOT = Path(__file__).resolve().parents[4]
MODELS = ROOT / 'library/shoulder/3d/public/models'
ORD = ['first', 'second', 'third', 'fourth', 'fifth', 'sixth', 'seventh', 'eighth', 'ninth', 'tenth', 'eleventh', 'twelfth']
VERTEBRAE = ['skeleton-vertebra-c7'] + [f'skeleton-vertebra-t{i}' for i in range(1, 13)] + [f'skeleton-vertebra-l{i}' for i in range(1, 6)]
RIBS = [f'skeleton-{n}-rib-{side}' for n in ORD for side in ['right', 'left']]
STERNUM = ['skeleton-manubrium-of-sternum', 'skeleton-body-of-sternum', 'skeleton-xiphoid-process']
PELVIS = ['skeleton-sacrum', 'skeleton-coccyx', 'skeleton-hip-bone-right', 'skeleton-hip-bone-left']
EXTRA = ['appendicular-skeleton-clavicle-right', 'appendicular-skeleton-clavicle-left', 'appendicular-skeleton-femur-right',
         'appendicular-skeleton-femur-left']
ABDO = ['rectus-abdominis-rectus-abdominis-muscle', 'external-abdominal-obliques-external-abdominal-oblique-muscle',
        'internal-abdominal-obliques-internal-abdominal-oblique-muscle', 'transversus-abdominis-transversus-abdominis-muscle',
        'pyramidalis-muscles-pyramidalis-muscle', 'inguinal-ligaments-inguinal-ligament']
STRUCTURES = {
    'skeletal': VERTEBRAE + RIBS + STERNUM + PELVIS + EXTRA,
    'muscular': [m + '-' + s for m in ABDO for s in ['right', 'left']] + ['linea-alba'],
}
VIEWS = {'ant': lambda v: np.c_[v[:, 0], -v[:, 1]], 'post': lambda v: np.c_[-v[:, 0], -v[:, 1]],
         'lat': lambda v: np.c_[v[:, 2], -v[:, 1]], 'sup': lambda v: np.c_[-v[:, 0], -v[:, 2]],
         'inf': lambda v: np.c_[v[:, 0], -v[:, 2]]}
PLAN = set(PELVIS + ['skeleton-vertebra-t6', 'skeleton-vertebra-t7', 'skeleton-sixth-rib-right', 'skeleton-sixth-rib-left',
                     'skeleton-seventh-rib-right', 'skeleton-seventh-rib-left', 'skeleton-body-of-sternum',
                     'appendicular-skeleton-femur-right', 'appendicular-skeleton-femur-left'])  # drawn in sup / inf


def meshes(kind):
    scene = trimesh.load(MODELS / f'z-anatomy-1.4.0-{kind}.glb')
    found = {}
    for node in scene.graph.nodes_geometry:
        sid = node.split('__')[0]
        if sid in STRUCTURES[kind]:
            transform, geom = scene.graph[node]
            mesh = scene.geometry[geom].copy(); mesh.apply_transform(transform); found[sid] = mesh
    missing = set(STRUCTURES[kind]) - set(found)
    if missing: raise SystemExit('Not in the model: ' + ', '.join(sorted(missing)))
    return found


def rings_of(shape, min_area=2e-7):
    rings = []
    for poly in getattr(shape, 'geoms', [shape]):
        if poly.is_empty: continue
        for ring in [poly.exterior, *poly.interiors]:
            if Polygon(ring).area > min_area: rings.append([[round(x, 5), round(y, 5)] for x, y in ring.coords])
    return rings


def outline(mesh, view, faces=None):
    pts = VIEWS[view](mesh.vertices)
    tris = [Polygon(pts[f]) for f in (mesh.faces if faces is None else faces)]
    shape = unary_union([t for t in tris if t.is_valid and t.area > 1e-12])
    if faces is not None: shape = shape.buffer(0.0005, join_style=1).buffer(-0.0005, join_style=1)
    return rings_of(shape.simplify(0.0003))


def points(m):
    """Landmark points (3D model coordinates, right side unless midline) computed from the meshes. Approximate teaching
    positions, not measured anatomical landmarks."""
    P = {}
    r = lambda a: [round(float(x), 4) for x in a]
    for sid in VERTEBRAE:
        v = m[sid].vertices; lvl = sid.rsplit('-', 1)[1]
        z0, z1 = m[sid].bounds[:, 2]; frac = (v[:, 2] - z0) / (z1 - z0)
        body = v[frac > 0.6]
        P[lvl + '-body'] = r([0, body[:, 1].mean(), body[:, 2].mean()])
        P[lvl + '-body-ant'] = r([0, body[:, 1].mean(), body[:, 2].max()])
        P[lvl + '-sp'] = r(v[v[:, 2].argmin()])
        right = v[(frac <= 0.5) & (v[:, 0] < -0.004)]
        P[lvl + '-tp'] = r(right[right[:, 0].argmin()])
    for n, w in enumerate(ORD, 1):
        v = m[f'skeleton-{w}-rib-right'].vertices
        P[f'rib{n}-head'] = r(v[v[:, 0].argmax()])                 # most medial point (posterior end) ≈ head
        P[f'rib{n}-angle'] = r(v[v[:, 2].argmin()])                # most posterior point ≈ angle
        P[f'rib{n}-lat'] = r(v[v[:, 0].argmin()])                  # most lateral point (midaxillary region)
        front = v[v[:, 2] > v[:, 2].max() - 0.012]
        P[f'rib{n}-end'] = r(front[front[:, 0].argmax()])          # anterior (sternal) end of the bony rib
    v = m['skeleton-manubrium-of-sternum'].vertices
    top = v[np.abs(v[:, 0]) < 0.006]
    P['jugular-notch'] = r([0, top[:, 1].max(), top[top[:, 1].argmax()][2]])
    P['sternal-angle'] = r([0, m['skeleton-body-of-sternum'].bounds[1, 1], m['skeleton-body-of-sternum'].vertices[:, 2].max() - 0.02])
    b = m['skeleton-body-of-sternum']
    P['sternum-body'] = r([0, b.bounds[:, 1].mean(), b.bounds[1, 2]])
    P['sternum-body-right'] = r([b.bounds[0, 0], b.bounds[:, 1].mean(), b.bounds[1, 2] - 0.01])
    x = m['skeleton-xiphoid-process']
    P['xiphisternal'] = r([0, x.bounds[1, 1], x.bounds[1, 2]])
    P['xiphoid-tip'] = r([0, x.bounds[0, 1], x.bounds[1, 2]])
    v = m['skeleton-hip-bone-right'].vertices
    P['iliac-crest-top'] = r(v[v[:, 1].argmax()])
    hi = v[v[:, 1] > 0.93]
    P['asis'] = r(hi[hi[:, 2].argmax()])
    P['psis'] = r(hi[hi[:, 2].argmin()])
    lo = v[v[:, 1] < 0.88]
    front = lo[lo[:, 2] > lo[:, 2].max() - 0.012]
    P['pubic-tubercle'] = r(front[front[:, 1].argmax()])
    med = v[v[:, 0] > v[:, 0].max() - 0.006]
    P['pubic-symphysis'] = r([0, med[:, 1].mean(), med[:, 2].mean()])
    P['pubic-symphysis-top'] = r([0, med[:, 1].max(), med[med[:, 1].argmax()][2]])
    P['pubic-symphysis-low'] = r([0, med[:, 1].min(), med[med[:, 1].argmin()][2]])
    P['pubic-body'] = r([med[:, 0].mean() - 0.012, med[:, 1].mean(), med[:, 2].mean() - 0.004])
    P['ischial-tuberosity'] = r(v[v[:, 1].argmin()])
    back = v[(v[:, 1] > 0.83) & (v[:, 1] < 0.90) & (v[:, 2] < -0.02)]
    P['ischial-spine'] = r(back[back[:, 0].argmax()])              # most medial point of the posterior border
    v = m['skeleton-sacrum'].vertices
    topv = v[v[:, 1] > v[:, 1].max() - 0.012]
    P['sacral-promontory'] = r(topv[topv[:, 2].argmax()])
    lowv = v[v[:, 1] < v[:, 1].min() + 0.01]
    P['sacrum-apex'] = r([0, lowv[:, 1].mean(), lowv[:, 2].mean()])
    side = v[(v[:, 1] < 0.90) & (v[:, 0] < 0)]
    P['sacrum-lower-border'] = r(side[side[:, 0].argmin()])
    v = m['skeleton-coccyx'].vertices
    P['coccyx-tip'] = r(v[v[:, 1].argmin()])
    P['coccyx-base'] = r([0, v[:, 1].max(), v[:, 2].mean()])
    P['coccyx-side'] = r(v[v[:, 0].argmin()])
    return P


def main():
    out = {view: {} for view in VIEWS}
    all_meshes = {}
    trunk = {v: [] for v in VIEWS}
    for kind in STRUCTURES:
        for sid, mesh in meshes(kind).items():
            all_meshes[sid] = mesh
            for view in VIEWS:
                if view in ('sup', 'inf') and sid not in PLAN: continue
                rings = outline(mesh, view)
                if kind == 'muscular' and rings:  # thin, folded sheets leave false holes; keep the outer outline only
                    rings = [max(rings, key=lambda r: Polygon(r).area)]
                out[view][sid] = rings
                if kind == 'skeletal' and 'appendicular' not in sid and view in ('ant', 'post', 'lat') and rings:
                    trunk[view].append(Polygon(rings[0]).buffer(0))
    # Depth slabs so the sternum and the front of the cage read in front of the back of the ribs: ant-front holds
    # the anterior half of each rib (z above the rib's mid depth); post-back the posterior half.
    for sid in RIBS:
        mesh = all_meshes[sid]; c = mesh.triangles_center
        zmid = mesh.bounds[:, 2].mean()
        for name, view, keep in [('ant-front', 'ant', c[:, 2] > zmid), ('post-back', 'post', c[:, 2] <= zmid),
                                 ('lat-near', 'lat', c[:, 0] <= 0.0)]:
            if keep.sum() > 3: out.setdefault(name, {})[sid] = outline(mesh, view, mesh.faces[keep])
    # Hip bone slabs for the plan views: sup-rim keeps the upper pelvis out, so the pelvic outlet shows (levator ani).
    for sid in PELVIS:
        mesh = all_meshes[sid]; c = mesh.triangles_center
        keep = c[:, 1] < 0.905
        if keep.sum() > 3:
            out.setdefault('sup-low', {})[sid] = outline(mesh, 'sup', mesh.faces[keep])
            out.setdefault('inf-low', {})[sid] = outline(mesh, 'inf', mesh.faces[keep])
    # SKIN: a soft outline around the trunk skeleton, for surface-anatomy figures (schematic).
    for view in ['ant', 'post', 'lat']:
        shape = unary_union(trunk[view]).buffer(0.04, join_style=1).buffer(-0.018, join_style=1).simplify(0.001)
        out[view]['skin'] = rings_of(shape)[:1]
    out['points'] = points(all_meshes)
    path = Path(__file__).with_name('outlines.json')
    path.write_text(json.dumps({'_note': __doc__.splitlines()[0], 'source': 'Z-Anatomy 1.4.0 via Vanatome (CC BY-SA 4.0)', **out}), encoding='utf-8')
    print('wrote', path.relative_to(ROOT), {k: len(v) for k, v in out.items()})
    for k in ['asis', 'psis', 'pubic-tubercle', 'pubic-symphysis', 'ischial-tuberosity', 'ischial-spine', 'coccyx-tip', 'sacrum-apex',
              'jugular-notch', 'sternal-angle', 'xiphisternal', 'xiphoid-tip', 'rib7-end', 'rib10-end', 'rib12-lat', 't12-body', 'l3-body']:
        print(k, out['points'][k])


if __name__ == '__main__':
    main()
