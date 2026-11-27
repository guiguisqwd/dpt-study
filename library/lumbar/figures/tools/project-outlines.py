#!/usr/bin/env python3
"""Project 3D model meshes to 2D outlines and sections, so the chapter's figures sit on the same bones as the 3D viewer.

Run once when the structure list changes (needs: pip install trimesh shapely):
    python3 library/lumbar/figures/tools/project-outlines.py
Writes outlines.json next to this file: {view: {structureId: [[ [x, y], ... ], ...]}} in model metres, y pointing down.
Views: ant (from the front), post (from behind), lat (right side seen from the right), sup (from above, anterior up).
Sections: midsag (cut at the midline, seen from the right) and axial-l3 / axial-l4 (horizontal cut through the middle of
that vertebral body, seen from above, anterior up). build-figures.py only reads the JSON (no 3D libraries needed).
Adapted from library/hip/figures/tools/project-outlines.py."""
import json
from pathlib import Path
import numpy as np
import trimesh
from shapely.geometry import LineString, Polygon
from shapely.ops import polygonize, unary_union

ROOT = Path(__file__).resolve().parents[4]
MODELS = ROOT / 'library/shoulder/3d/public/models'
VERTEBRAE = [f'skeleton-vertebra-t{i}' for i in range(6, 13)] + [f'skeleton-vertebra-l{i}' for i in range(1, 6)]
RIBS = [f'skeleton-{n}-rib-{side}' for n in ['sixth', 'seventh', 'eighth', 'ninth', 'tenth', 'eleventh', 'twelfth'] for side in ['right', 'left']]
LEG = ['appendicular-skeleton-' + b + '-right' for b in ['femur', 'tibia', 'fibula', 'patella', 'talus', 'calcaneus', 'navicular-bone',
       'cuboid-bone', 'first-metatarsal-bone', 'third-metatarsal-bone', 'fifth-metatarsal-bone', 'proximal-phalanx-of-first-finger-of-foot',
       'proximal-phalanx-of-third-finger-of-foot', 'proximal-phalanx-of-fifth-finger-of-foot']]
STRUCTURES = {
    'skeletal': VERTEBRAE + RIBS + LEG + ['skeleton-sacrum', 'skeleton-coccyx', 'skeleton-hip-bone-right', 'skeleton-hip-bone-left',
                                          'appendicular-skeleton-femur-left'],
    'muscular': ['quadratus-lumborum-quadratus-lumborum-muscle-right', 'quadratus-lumborum-quadratus-lumborum-muscle-left',
                 'transversus-abdominis-transversus-abdominis-muscle-right',
                 'internal-abdominal-obliques-internal-abdominal-oblique-muscle-right',
                 'external-abdominal-obliques-external-abdominal-oblique-muscle-right'],
}
VIEWS = {'ant': lambda v: np.c_[v[:, 0], -v[:, 1]], 'post': lambda v: np.c_[-v[:, 0], -v[:, 1]],
         'lat': lambda v: np.c_[v[:, 2], -v[:, 1]], 'sup': lambda v: np.c_[-v[:, 0], -v[:, 2]]}
SUP_ONLY = {'skeleton-vertebra-l4', 'skeleton-vertebra-l1', 'skeleton-vertebra-l5', 'skeleton-sacrum'}


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
    if faces is not None: shape = shape.buffer(0.0005, join_style=1).buffer(-0.0005, join_style=1)  # round the slab edges
    shape = shape.simplify(0.0003)
    return rings_of(shape)


def section(mesh, origin, normal, to2d):
    """Cut the mesh with a plane and return the cut faces as rings (segments polygonized with shapely)."""
    segments = trimesh.intersections.mesh_plane(mesh, plane_normal=normal, plane_origin=origin)
    if len(segments) == 0: return []
    lines = [LineString(to2d(np.asarray(seg))) for seg in segments]
    polys = [p.buffer(0) for p in polygonize(unary_union(lines))]
    polys = [p for p in polys if p.area > 1e-7]
    if not polys: return []
    return rings_of(unary_union(polys).simplify(0.0002))


def points(m):
    """Landmark points (3D model coordinates, right side) computed from the meshes, so labels and attachment areas
    follow the same bones as the 3D viewer. Approximate teaching positions, not measured anatomical landmarks."""
    P = {}
    r = lambda a: [round(float(x), 4) for x in a]
    for sid in VERTEBRAE:
        v = m[sid].vertices; lvl = sid.rsplit('-', 1)[1]
        z0, z1 = m[sid].bounds[:, 2]; frac = (v[:, 2] - z0) / (z1 - z0)
        arch, body = v[frac <= 0.5], v[frac > 0.6]
        P[lvl + '-body'] = r(body.mean(axis=0))
        P[lvl + '-body-ant'] = r([0, body[:, 1].mean(), body[:, 2].max()])
        P[lvl + '-body-post'] = r([0, body[:, 1].mean(), body[:, 2].min()])
        P[lvl + '-sp'] = r(v[v[:, 2].argmin()])
        mid = arch[np.abs(arch[:, 0]) < 0.006]
        P[lvl + '-sp-base'] = r([0, mid[:, 1].mean(), mid[:, 2].max() - 0.004]) if len(mid) else P[lvl + '-sp']
        right = arch[arch[:, 0] < -0.004]
        tp = right[right[:, 0].argmin()]
        P[lvl + '-tp'] = r(tp)
        P[lvl + '-tp-root'] = r([tp[0] * 0.45, tp[1], tp[2]])
        near = right[(right[:, 0] > -0.03)]
        P[lvl + '-sap'] = r(near[near[:, 1].argmax()])
        P[lvl + '-iap'] = r(near[near[:, 1].argmin()])
        sap = near[near[:, 1] > near[:, 1].max() - 0.008]
        P[lvl + '-mammillary'] = r(sap[sap[:, 2].argmin()])
        P[lvl + '-lamina'] = r((np.array(P[lvl + '-sp-base']) + np.array(P[lvl + '-iap'])) / 2)
        ped = v[(v[:, 0] < -0.008) & (v[:, 0] > -0.022) & (frac > 0.45) & (frac < 0.6)]
        P[lvl + '-pedicle'] = r(ped.mean(axis=0)) if len(ped) else r([-0.015, P[lvl + '-body'][1], (z0 + z1) / 2])
    v = m['skeleton-hip-bone-right'].vertices
    P['iliac-crest-top'] = r(v[v[:, 1].argmax()])
    post = v[v[:, 1] > 0.93]
    P['psis'] = r(post[post[:, 2].argmin()])
    P['iliac-crest-post'] = r(v[(v[:, 2] < -0.06)][v[(v[:, 2] < -0.06)][:, 1].argmax()])
    v = m['skeleton-sacrum'].vertices
    top = v[v[:, 1] > v[:, 1].max() - 0.012]
    P['sacral-promontory'] = r(top[top[:, 2].argmax()])
    midl = v[np.abs(v[:, 0]) < 0.006]
    P['median-sacral-crest'] = r(midl[midl[:, 2].argmin()])
    P['sacrum-base'] = r([0, v[:, 1].max(), top[:, 2].mean()])
    v = m['skeleton-twelfth-rib-right'].vertices
    P['rib12-tip'] = r(v[v[:, 1].argmin()])
    P['rib12-head'] = r(v[v[:, 0].argmax()])
    for n, w in [(6, 'sixth'), (7, 'seventh'), (8, 'eighth'), (9, 'ninth'), (10, 'tenth'), (11, 'eleventh'), (12, 'twelfth')]:
        v = m[f'skeleton-{w}-rib-right'].vertices
        P[f'rib{n}-angle'] = r(v[v[:, 2].argmin()])           # most posterior point ≈ rib angle
        P[f'rib{n}-head'] = r(v[v[:, 0].argmax()])            # most medial point ≈ head/neck
        low = v[v[:, 1] < v[:, 1].min() + 0.03]
        P[f'rib{n}-low'] = r(low[low[:, 0].argmin()])         # lowest lateral part (inferior border, far end)
    v = m['appendicular-skeleton-femur-right'].vertices
    lt = v[(v[:, 1] > 0.78) & (v[:, 1] < 0.81)]
    P['lesser-trochanter'] = r(lt[lt[:, 0].argmax()])         # most medial bump just below the neck
    v = m['skeleton-coccyx'].vertices
    P['coccyx-tip'] = r(v[v[:, 1].argmin()])
    return P


def sagittal(m):
    """Midsagittal schematic of each lumbar vertebra from its midline vertices (the meshes are not closed, so a true
    plane section fails): body quadrilateral and posterior arch (lamina + spinous process) quadrilateral, as (z, y)
    corners [anterior-superior, anterior-inferior, posterior-inferior, posterior-superior]. Model metres."""
    out = {}
    for sid in VERTEBRAE[4:] + ['skeleton-sacrum']:
        v = m[sid].vertices
        mid = v[np.abs(v[:, 0]) < 0.008]
        z0, z1 = m[sid].bounds[:, 2]
        if sid == 'skeleton-sacrum':
            top = mid[mid[:, 1] > mid[:, 1].max() - 0.03]
            body = top[top[:, 2] > -0.045]
        else:
            body = mid[(mid[:, 2] - z0) / (z1 - z0) > 0.55]
        def quad(pts):
            zz, yy = pts[:, 2], pts[:, 1]
            return [[round(float(pts[i][2]), 4), round(float(pts[i][1]), 4)] for i in
                    [np.argmax(zz + yy), np.argmax(zz - yy), np.argmax(-zz - yy), np.argmax(-zz + yy)]]
        rec = {'body': quad(body)}
        if sid != 'skeleton-sacrum':
            back = mid[(mid[:, 2] - z0) / (z1 - z0) < 0.42]
            rec['arch'] = quad(back)
        out[sid.rsplit('-', 1)[1]] = rec
    return out


def main():
    out = {view: {} for view in [*VIEWS, 'midsag', 'axial-l3', 'axial-l4']}
    body = {view: [] for view in VIEWS}
    all_meshes = {}
    legs = {}
    for kind in STRUCTURES:
        for sid, mesh in meshes(kind).items():
            all_meshes[sid] = mesh
            for view in VIEWS:
                if view == 'sup' and sid not in SUP_ONLY: continue
                out[view][sid] = outline(mesh, view)
                if kind == 'muscular':  # thin, folded muscle sheets leave false holes; keep the outer outline only
                    out[view][sid] = [max(out[view][sid], key=lambda r: Polygon(r).area)]
                if kind == 'skeletal' and 'appendicular' not in sid and sid not in RIBS[:8]:
                    body[view].append(Polygon(out[view][sid][0]).buffer(0))
                if kind == 'skeletal' and (sid in LEG or 'hip-bone' in sid or sid == 'skeleton-sacrum'):
                    legs.setdefault(view, []).append(unary_union([Polygon(r).buffer(0) for r in out[view][sid]]))
    # LAYERS: projections are silhouettes, so interior edges (spinous processes, laminae, articular processes) would
    # vanish. Each vertebra is split into depth slabs drawn back to front: post-0 body, post-1 whole arch,
    # post-2 laminae and spinous process, post-3 spinous process only (z fractions of the bone's depth); lat-0 far
    # (left) half, lat-1 near (right) half, lat-2 the near half's lateral parts (transverse and articular processes).
    for sid in VERTEBRAE + ['skeleton-sacrum']:
        if sid in VERTEBRAE[:4]: continue  # T6-T9 only need the plain silhouette
        mesh = all_meshes[sid]
        c = mesh.triangles_center
        z0, z1 = mesh.bounds[:, 2]
        frac = (c[:, 2] - z0) / (z1 - z0)
        for i, keep in enumerate([frac > 0.5, frac <= 0.52, frac <= 0.27, frac <= 0.17]):
            if keep.any(): out.setdefault(f'post-{i}', {})[sid] = outline(mesh, 'post', mesh.faces[keep])
        for i, keep in enumerate([c[:, 0] > -0.002, c[:, 0] <= 0.002, c[:, 0] <= -0.014]):
            if keep.any(): out.setdefault(f'lat-{i}', {})[sid] = outline(mesh, 'lat', mesh.faces[keep])
        for i, keep in enumerate([frac <= 0.55, frac > 0.5]):
            if keep.any(): out.setdefault(f'ant-{i}', {})[sid] = outline(mesh, 'ant', mesh.faces[keep])
    # Superior view slabs for single vertebrae: sup-1 upper half, sup-2 top quarter (superior articular processes and
    # the upper rim of the body stand out against the rest).
    for sid in ['skeleton-vertebra-l1', 'skeleton-vertebra-l4', 'skeleton-vertebra-l5']:
        mesh = all_meshes[sid]; c = mesh.triangles_center
        y0, y1 = mesh.bounds[:, 1]; fy = (c[:, 1] - y0) / (y1 - y0)
        for i, keep in [(1, fy > 0.5), (2, fy > 0.72)]:
            out.setdefault(f'sup-{i}', {})[sid] = outline(mesh, 'sup', mesh.faces[keep])
    # Midsagittal section (x = 0), seen from the right like the lat view.
    for sid in VERTEBRAE + ['skeleton-sacrum', 'skeleton-coccyx']:
        out['midsag'][sid] = section(all_meshes[sid], [0, 0, 0], [1, 0, 0], lambda p: np.c_[p[:, 2], -p[:, 1]])
    # Axial sections through the middle of the L3 and L4 bodies, seen from above (anterior up).
    for level in ['l3', 'l4']:
        vb = all_meshes[f'skeleton-vertebra-{level}']
        y = float(vb.bounds[:, 1].mean())
        out[f'axial-{level}']['_y'] = round(y, 4)
        for sid, mesh in all_meshes.items():
            if mesh.bounds[0, 1] < y < mesh.bounds[1, 1]:
                rings = section(mesh, [0, y, 0], [0, 1, 0], lambda p: np.c_[-p[:, 0], -p[:, 2]])
                if rings: out[f'axial-{level}'][sid] = rings
    # SKIN: a soft outline around the lumbar spine, pelvis and lower ribs, for surface-anatomy figures (schematic).
    for view in ['ant', 'post', 'lat']:
        shape = unary_union(body[view]).buffer(0.035, join_style=1).buffer(-0.012, join_style=1).simplify(0.001)
        out[view]['skin'] = rings_of(shape)[:1]
    # LEG-SKIN: a soft outline of the pelvis and right lower limb (for the dermatome figure; schematic).
    for view in ['ant', 'post']:
        shape = unary_union(legs[view]).buffer(0.04, join_style=1).buffer(-0.015, join_style=1).simplify(0.002)
        out[view]['leg-skin'] = rings_of(shape)[:1]
    out['points'] = points(all_meshes)
    out['sag'] = sagittal(all_meshes)
    path = Path(__file__).with_name('outlines.json')
    path.write_text(json.dumps({'_note': __doc__.splitlines()[0], 'source': 'Z-Anatomy 1.4.0 via Vanatome (CC BY-SA 4.0)', **out}), encoding='utf-8')
    print('wrote', path.relative_to(ROOT), {k: len(v) for k, v in out.items()})


if __name__ == '__main__':
    main()
