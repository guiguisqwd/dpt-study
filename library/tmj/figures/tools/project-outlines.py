#!/usr/bin/env python3
"""Project the head meshes exported by export-head.py to 2D outlines for the chapter figures.

    python3 project-outlines.py head.npz        (needs numpy and shapely)
Writes outlines.json next to this file: {view: {name: [rings]}} in model metres (x<0 = right side, y up, z anterior),
2D y pointing down. Views: lat (right side seen from the right), ant (from the front), med (right half seen from the
midline), inf (from below, anterior up). 'curves' holds nerve and vessel centre lines as 3D polylines, 'points' holds 3D
landmark points taken from the model's own label leader lines. build-figures.py only reads the JSON."""
import json, sys
from pathlib import Path
import numpy as np
from shapely.geometry import Polygon
from shapely.ops import unary_union

VIEWS = {'lat': lambda v: np.c_[v[:, 2], -v[:, 1]], 'ant': lambda v: np.c_[v[:, 0], -v[:, 1]],
         'med': lambda v: np.c_[-v[:, 2], -v[:, 1]], 'inf': lambda v: np.c_[v[:, 0], -v[:, 2]]}


def rings_of(shape, min_area=1e-7):
    rings = []
    for poly in getattr(shape, 'geoms', [shape]):
        if poly.is_empty or poly.geom_type != 'Polygon': continue
        for ring in [poly.exterior, *poly.interiors]:
            if Polygon(ring).area > min_area: rings.append([[round(x, 5), round(y, 5)] for x, y in ring.coords])
    return rings


def outline(v, f, view, keep=None, simp=0.00025):
    pts = VIEWS[view](v)
    faces = f if keep is None else f[keep]
    tris = [Polygon(pts[t]) for t in faces]
    shape = unary_union([t for t in tris if t.is_valid and t.area > 1e-13])
    shape = shape.buffer(0.0004, join_style=1).buffer(-0.0004, join_style=1).simplify(simp)
    return rings_of(shape)


def main():
    src = Path(sys.argv[1])
    z = np.load(src, allow_pickle=True)
    names = list(z['names'])
    M = {n: (z[f'v{i}'], z[f'f{i}']) for i, n in enumerate(names)}
    extra = json.loads(Path(str(src) + '.json').read_text())
    out = {v: {} for v in VIEWS}
    for n, (v, f) in M.items():
        c = v[f].mean(axis=1)  # triangle centres
        side = 'l' if n.endswith('.l') else ('r' if n.endswith('.r') else '')
        out['ant'][n] = outline(v, f, 'ant')
        if side != 'l':
            out['lat'][n] = outline(v, f, 'lat')
            out['inf'][n] = outline(v, f, 'inf')
            keep = c[:, 0] < 0.0005
            if keep.any(): out['med'][n] = outline(v, f, 'med', keep)
        else:
            out['inf'][n] = outline(v, f, 'inf')
    # depth slabs for the lateral view: the near (lateral) part of the temporal bone shows the zygomatic process and
    # mastoid process in front of the squama; the near part of the mandible shows the ramus in front of the far half.
    for n, name, depth in [('Temporal bone.r', 'Temporal bone.r|near', 0.016), ('Mandible', 'Mandible|right', None), ('Sphenoid bone', 'Sphenoid bone|right', None),
                           ('Hyoid bone', 'Hyoid bone|right', None), ('Frontal bone', 'Frontal bone|right', None), ('Occipital bone', 'Occipital bone|right', None)]:
        v, f = M[n]; c = v[f].mean(axis=1)
        keep = (c[:, 0] < v[:, 0].min() + depth) if depth else (c[:, 0] < 0.0)
        out['lat'][name] = outline(v, f, 'lat', keep)
    # zygomatic process of the temporal bone alone, to redraw the arch over temporalis
    v, f = M['Temporal bone.r']; c = v[f].mean(axis=1)
    out['lat']['Temporal bone.r|arch'] = outline(v, f, 'lat', (c[:, 0] < v[:, 0].min() + 0.012) & (c[:, 2] > 0.004) & (c[:, 1] < 1.586))
    # SKIN: soft outline around the skull, facial muscles and neck muscles plus a schematic nose (the model has no skin).
    def polys(view, names):
        r = []
        for n in names:
            for ring in out[view].get(n, [])[:1]:
                p = Polygon(ring).buffer(0)
                if not p.is_empty: r.append(p)
        return r
    soft = [n for n in M if not n.endswith('.l') and not any(k in n for k in ('tooth', 'Platysma', 'Epicranial'))]
    nose = Polygon([(0.083, -1.602), (0.113, -1.566), (0.106, -1.556), (0.086, -1.553)])
    lips = Polygon([(0.086, -1.553), (0.097, -1.546), (0.094, -1.538), (0.097, -1.531), (0.090, -1.524), (0.092, -1.512), (0.080, -1.505), (0.075, -1.53)])
    neck = Polygon([(-0.075, -1.56), (0.07, -1.505), (0.035, -1.47), (0.03, -1.43), (-0.085, -1.43), (-0.08, -1.5)])
    shape = unary_union(polys('lat', soft) + [nose, lips, neck]).buffer(0.012, join_style=1).buffer(-0.007, join_style=1).simplify(0.0008)
    out['lat']['skin'] = rings_of(shape)[:1]
    softa = [n for n in M if not any(k in n for k in ('tooth', 'Epicranial'))]
    shape = unary_union(polys('ant', softa)).buffer(0.012, join_style=1).buffer(-0.007, join_style=1).simplify(0.0008)
    out['ant']['skin'] = rings_of(shape)[:1]
    out['curves'] = {k: c['splines'] for k, c in extra['curves'].items()}
    out['points'] = extra['labels']
    dst = Path(__file__).with_name('outlines.json')
    dst.write_text(json.dumps({'_note': __doc__.splitlines()[0], 'source': 'Z-Anatomy (CC BY-SA 4.0), Startup.blend', **out}), encoding='utf-8')
    print('wrote', dst, {k: len(v) for k, v in out.items()}, dst.stat().st_size)


if __name__ == '__main__':
    main()
