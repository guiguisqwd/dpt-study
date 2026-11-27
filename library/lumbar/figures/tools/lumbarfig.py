#!/usr/bin/env python3
"""Lumbar figure kit: draws vertebrae, sacrum, pelvis, ribs and the right lower limb from outlines.json (projected from
the 3D model by project-outlines.py) with the shared hand-drawn Fig class from daily/engine/figlib, so library and daily
figures look the same. Adapted from library/hip/figures/tools/hipfig.py (same helpers and conventions).

Coordinates: points are 3D model coordinates [x, y, z] (metres; x<0 = right side, y up, z anterior).
A Stage places one view of the model on the figure; stage.P(point3d) gives figure pixels; stage.at(name) a named point."""
import json, math, re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(ROOT / 'daily'))
from engine.figlib.fig import Fig, set_out, esc, RED, BLUE, INK, GREEN, PURP, GOLD, GREY, TEAL, ZH, BONE, BONE_E  # noqa: E402,F401

HERE = Path(__file__).resolve().parent
OUTLINES = json.loads((HERE / 'outlines.json').read_text(encoding='utf-8'))
_content = HERE.parents[1] / 'content.json'
CONTENT = json.loads(_content.read_text(encoding='utf-8')) if _content.is_file() else {'muscles': []}
# AN-11: one colour per muscle for the whole chapter. The table lives in content.json (muscle "color"/"letter");
# these defaults only bootstrap figures before a record exists and must match it.
DEFAULT = {
    'iliocostalis-lumborum': ('#a8423a', 'IL'), 'longissimus-thoracis': ('#c96f3b', 'LT'), 'spinalis-thoracis': ('#8c6239', 'ST'),
    'multifidus': ('#365e91', 'MF'), 'rotatores': ('#2b6c7c', 'RO'), 'interspinales': ('#4f8a4a', 'IS'),
    'intertransversarii': ('#7d8f2e', 'IT'), 'quadratus-lumborum': ('#9c3f6e', 'QL'), 'psoas-major': ('#6a4fa3', 'PM'),
    'serratus-posterior-inferior': ('#5f6f80', 'SP')}
COLOR = {k: v[0] for k, v in DEFAULT.items()}
LETTER = {k: v[1] for k, v in DEFAULT.items()}
for _m in CONTENT.get('muscles', []):
    COLOR[_m['id']] = _m.get('color', COLOR.get(_m['id'], RED)); LETTER[_m['id']] = _m.get('letter', LETTER.get(_m['id'], ''))
NERVE = '#c69014'  # AN-11: nerves gold
ORIGIN_C, INSERT_C = '#245e50', '#8c2f39'
SHADE = '#ece2cc'  # bone surfaces further from the viewer

LEVELS = [f't{i}' for i in range(6, 13)] + [f'l{i}' for i in range(1, 6)]
VERT = {lvl: f'skeleton-vertebra-{lvl}' for lvl in LEVELS}
RIB_N = {6: 'sixth', 7: 'seventh', 8: 'eighth', 9: 'ninth', 10: 'tenth', 11: 'eleventh', 12: 'twelfth'}
BONES = {'sacrum': 'skeleton-sacrum', 'coccyx': 'skeleton-coccyx', 'hip-bone': 'skeleton-hip-bone-right',
         'hip-bone-left': 'skeleton-hip-bone-left', 'femur-left': 'appendicular-skeleton-femur-left',
         **{f'rib{n}': f'skeleton-{w}-rib-right' for n, w in RIB_N.items()},
         **{f'rib{n}-left': f'skeleton-{w}-rib-left' for n, w in RIB_N.items()}, **VERT}
LEG = [k for k in OUTLINES['ant'] if k.startswith('appendicular-skeleton-') and k.endswith('-right')]
MODEL_MUSCLES = {'quadratus-lumborum': 'quadratus-lumborum-quadratus-lumborum-muscle-right',
                 'quadratus-lumborum-left': 'quadratus-lumborum-quadratus-lumborum-muscle-left',
                 'transversus-abdominis': 'transversus-abdominis-transversus-abdominis-muscle-right',
                 'internal-oblique': 'internal-abdominal-obliques-internal-abdominal-oblique-muscle-right',
                 'external-oblique': 'external-abdominal-obliques-external-abdominal-oblique-muscle-right'}
LM = dict(OUTLINES['points'])  # computed from the meshes (project-outlines.py points()); approximate teaching positions


def mirror(p): return [-p[0], p[1], p[2]]  # the same point on the left side


def V(view, p):
    x, y, z = p
    return {'ant': (x, -y), 'post': (-x, -y), 'lat': (z, -y), 'med': (-z, -y), 'sup': (-x, -z)}[view]


class Stage:
    """One view of the model placed at figure (fx, fy) for model 2D point (mx, my), at `scale` px per metre."""
    def __init__(s, f, view, mx, my, fx, fy, scale):
        s.f, s.view, s.mx, s.my, s.fx, s.fy, s.k = f, view, mx, my, fx, fy, scale

    def P2(s, x, y): return (s.fx + (x - s.mx) * s.k, s.fy + (y - s.my) * s.k)
    def P(s, p): return s.P2(*V(s.view, p))
    def at(s, name, dx=0, dy=0, dz=0):
        p = LM[name]; return s.P([p[0] + dx, p[1] + dy, p[2] + dz])

    def d(s, rings):
        return ' '.join('M' + ' L'.join('%.1f,%.1f' % s.P2(*pt) for pt in ring) + 'Z' for ring in rings)

    def shape(s, sid, col, fill, w=1.6, op=None, dash=None, rough=True, layer=None):
        rings = OUTLINES[layer or s.view].get(sid)
        if rings: s.f.path(s.d(rings), col, w, fill, dash=dash, rough=rough, op=op, extra='fill-rule="evenodd"')

    def bones(s, names, w=1.6, op=None, fill=BONE):
        for n in names: s.shape(BONES.get(n, n), BONE_E, fill, w, op=op)

    def spine(s, levels=('t12', 'l1', 'l2', 'l3', 'l4', 'l5'), sacrum=True, w=1.5, op=None):
        """Vertebrae drawn back to front from depth slabs, so spinous processes, laminae and articular processes keep
        their edges (silhouettes alone would hide them). Works in the post, lat and ant views; sup uses one silhouette."""
        ids = [VERT[l] for l in levels] + (['skeleton-sacrum'] if sacrum else [])
        if s.view == 'sup':
            for sid in ids: s.shape(sid, BONE_E, BONE, w, op=op)
            return
        layers = {'post': ['post-0', 'post-1', 'post-2', 'post-3'], 'lat': ['lat-0', 'lat-1', 'lat-2'], 'ant': ['ant-0', 'ant-1']}[s.view]
        for i, layer in enumerate(layers):
            for sid in ids:
                if sid in OUTLINES[layer]: s.shape(sid, BONE_E, SHADE if i == 0 else BONE, w, op=op, layer=layer)
                elif i == 0: s.shape(sid, BONE_E, BONE, w, op=op)  # thoracic levels above the slabs: plain silhouette

    def muscle(s, mid, op=0.85, w=1.6, dash=None, fill=True, col=None):
        col = col or COLOR.get(mid.replace('-left', ''), RED)
        s.shape(MODEL_MUSCLES[mid], col, tint(col) if fill else 'none', w, op=op, dash=dash)

    def skin(s, col='#b7ab95', fill='#f7efe2', key='skin'):
        s.shape(key, col, fill, 1.6, rough=False)

    def band(s, mid, origin, insertion, bow=None, op=0.85, w=1.6, col=None):
        """Schematic muscle for structures the model lacks: a smooth band from an origin line to an insertion line (3D points)."""
        col = col or COLOR.get(mid, RED)
        o = [s.P(p) if len(p) == 3 else p for p in origin]; i = [s.P(p) if len(p) == 3 else p for p in insertion]
        s.f.path(smooth_band(o, i, bow), col, w, tint(col), op=op)
        return o, i


def tint(hexcol, k=0.62):
    r, g, b = (int(hexcol[i:i + 2], 16) for i in (1, 3, 5))
    return '#%02x%02x%02x' % tuple(int(c + (255 - c) * k) for c in (r, g, b))


def smooth_band(o, i, bow=None):
    """Closed path: origin edge o[0]→o[-1], side to i[-1], insertion edge back to i[0], side to o[0].
    Sides bow away from the band's centre by `bow` px (default: a little more than the wider end)."""
    pts_all = o + i
    cx, cy = sum(p[0] for p in pts_all) / len(pts_all), sum(p[1] for p in pts_all) / len(pts_all)
    width = max(math.dist(o[0], o[-1]), math.dist(i[0], i[-1]))
    def ctrl(a, b):
        mx, my = (a[0] + b[0]) / 2, (a[1] + b[1]) / 2
        dx, dy = b[0] - a[0], b[1] - a[1]
        n = math.hypot(dx, dy) or 1
        nx, ny = -dy / n, dx / n
        k = bow if bow is not None else 0.3 * width + 4
        c1, c2 = (mx + nx * k, my + ny * k), (mx - nx * k, my - ny * k)
        return c1 if math.dist(c1, (cx, cy)) > math.dist(c2, (cx, cy)) else c2
    d = 'M%.1f,%.1f ' % o[0] + ' '.join('L%.1f,%.1f' % p for p in o[1:])
    d += ' Q%.1f,%.1f %.1f,%.1f' % (*ctrl(o[-1], i[-1]), *i[-1])
    d += ' ' + ' '.join('L%.1f,%.1f' % p for p in reversed(i[:-1]))
    d += ' Q%.1f,%.1f %.1f,%.1f Z' % (*ctrl(i[0], o[0]), *o[0])
    return d


def strip(f, pts, col, w=10, op=0.75):
    """A thin muscle drawn as a thick stroke along figure points (fascicles, small segmental muscles)."""
    d = 'M' + ' L'.join('%.1f,%.1f' % p for p in pts)
    f.raw(f'<path d="{d}" fill="none" stroke="{col}" stroke-width="{w}" stroke-opacity="{op}" stroke-linecap="round" stroke-linejoin="round"/>')
    f.path(d, col, 1.2, rough=False)


def area(f, pts, col, label=None):
    """Attachment area (AN-14): dashed outline around the given figure points."""
    if len(pts) == 1:
        x, y = pts[0]; f.raw(f'<ellipse cx="{x:.1f}" cy="{y:.1f}" rx="10" ry="7" fill="{col}" fill-opacity=".18" stroke="{col}" stroke-width="2" stroke-dasharray="5 4"/>')
    else:
        d = 'M' + ' L'.join('%.1f,%.1f' % p for p in pts)
        f.raw(f'<path d="{d}" fill="none" stroke="{col}" stroke-width="9" stroke-opacity=".28" stroke-linecap="round" stroke-linejoin="round"/>')
        f.path(d, col, 2, dash='6 4', rough=False)


def oi(f, o_pts, i_pts, letter_o='O', letter_i='I', tags=True):
    """Origin and insertion areas plus the dashed O→I attachment line (AN-13)."""
    area(f, o_pts, ORIGIN_C); area(f, i_pts, INSERT_C)
    oc = centroid(o_pts); ic = centroid(i_pts)
    f.raw(f'<path d="M{oc[0]:.1f},{oc[1]:.1f} L{ic[0]:.1f},{ic[1]:.1f}" stroke="#324c44" stroke-width="1.6" stroke-dasharray="7 5" fill="none"/>')
    if tags:
        oc, ic = free_spot(f, oc), free_spot(f, ic)
        tag(f, *oc, letter_o, ORIGIN_C); tag(f, *ic, letter_i, INSERT_C)
    return oc, ic


def free_spot(f, p, r=25):
    """Nudge a tag sideways so it does not sit on another tag of the same figure."""
    used = f.__dict__.setdefault('tags', [])
    cands = [p] + [(p[0] + dx * r, p[1] + dy * r * 0.8) for dx, dy in
                   [(1, 0), (-1, 0), (1, 1), (1, -1), (-1, 1), (-1, -1), (2, 0), (-2, 0), (0, 1.3), (0, -1.3)]]
    spot = next((c for c in cands if all(math.dist(c, q) >= r for q in used)), cands[-1])
    used.append(spot)
    return spot


def centroid(pts): return (sum(p[0] for p in pts) / len(pts), sum(p[1] for p in pts) / len(pts))


def tag(f, x, y, txt, col, r=12):
    f.circle(x, y, r, col, '#fff', 2); f.text(x, y + 4.5, txt, 13 if len(txt) < 3 else 10, '#fff', 'middle', '700')


TEXTS = {}  # figure number → [(en, zh)] structure labels drawn with label(); written to figure-labels.json


def label(f, x, y, en, zh, col=INK, anchor='start', size=15, to=None):
    """Bilingual label; optional leader line to the point `to`. Recorded in TEXTS for content.json diagram labels."""
    TEXTS.setdefault(f.n, []).append((en, zh))
    if to:
        w = text_width(en, zh, size)
        left = x - w if anchor == 'end' else (x - w / 2 if anchor == 'middle' else x)
        if to[0] < left: lx = left - 6
        elif to[0] > left + w: lx = left + w + 6
        else: lx = to[0]
        ly = y - 5 if lx != to[0] else (y + size + 10 if to[1] > y else y - size - 2)
        f.leader(lx, ly, to[0], to[1], col)
        f.circle(to[0], to[1], 3.2, col, '#fff', 1)
    f.bi(x, y, en, zh, size, col, anchor, '600')


def text_width(en, zh, size=15):
    """Rough rendered width of a bilingual label (Arial / PingFang)."""
    wide = sum(1 for ch in en if ch.isupper() or ch in 'mwMW')
    return max(len(en) * size * 0.53 + wide * size * 0.12, len(zh) * (size - 2) * 1.0)


NAMES = {'iliocostalis-lumborum': ('Iliocostalis lumborum', '腰髂肋肌'), 'longissimus-thoracis': ('Longissimus thoracis', '胸最长肌'),
         'spinalis-thoracis': ('Spinalis thoracis', '胸棘肌'), 'multifidus': ('Multifidus', '多裂肌'), 'rotatores': ('Rotatores', '回旋肌'),
         'interspinales': ('Interspinales', '棘间肌'), 'intertransversarii': ('Intertransversarii', '横突间肌'),
         'quadratus-lumborum': ('Quadratus lumborum', '腰方肌'), 'psoas-major': ('Psoas major', '腰大肌'),
         'serratus-posterior-inferior': ('Serratus posterior inferior', '下后锯肌')}


def name_of(mid):
    rec = next((m['name'] for m in CONTENT.get('muscles', []) if m['id'] == mid), None)
    return rec or {'en': NAMES[mid][0], 'zh': NAMES[mid][1]}


LABELS = {}  # figure number → O/I legend rows; build-figures.py writes them to figure-labels.json for content.json


def legend_oi(f, x, y, rows, width=None):
    """rows: [(muscle id, origin en, origin zh, insertion en, insertion zh)] → stacked bilingual O/I legend.
    The texts are the short figure labels; diagrams in content.json repeat them as Origin:/Insertion: labels."""
    LABELS.setdefault(f.n, []).extend(rows)
    yy = y
    for mid, oen, ozh, ien, izh in rows:
        col = COLOR.get(mid, RED)
        name = name_of(mid)
        tag(f, x + 12, yy - 6, LETTER.get(mid, ''), col, 13)
        f.bi(x + 32, yy, name['en'], name['zh'], 16, col, 'start', '700')
        f.bi(x + 32, yy + 40, 'Origin: ' + oen, '起点：' + ozh, 13, ORIGIN_C, 'start', '600')
        f.bi(x + 32, yy + 76, 'Insertion: ' + ien, '止点：' + izh, 13, INSERT_C, 'start', '600')
        yy += 118
    return yy


def key_oi(f, x, y):
    """Small key: green dashed = origin, red dashed = insertion, dashed line = O→I attachment order (AN-13)."""
    area(f, [(x, y), (x + 34, y)], ORIGIN_C); f.bi(x + 46, y + 4, 'Origin area', '起点区', 13, ORIGIN_C, 'start', '600')
    area(f, [(x + 170, y), (x + 204, y)], INSERT_C); f.bi(x + 216, y + 4, 'Insertion area', '止点区', 13, INSERT_C, 'start', '600')
    f.raw(f'<path d="M{x + 350},{y} L{x + 400},{y}" stroke="#324c44" stroke-width="1.6" stroke-dasharray="7 5"/>')
    f.bi(x + 410, y + 4, 'Origin → insertion', '起点 → 止点', 13, INK, 'start', '600')


def note(f, x, y, lines_en, lines_zh, col=ZH, size=13):
    for k, (en, zh) in enumerate(zip(lines_en, lines_zh)):
        f.bi(x, y + k * (2 * size + 12), en, zh, size, col, 'start', '400')


def curve(pts, tension=0.5):
    """Open smooth path (Catmull-Rom → cubic Bézier) through figure points."""
    d = 'M%.1f,%.1f' % pts[0]
    n = len(pts)
    for k in range(n - 1):
        p0, p1, p2 = pts[max(k - 1, 0)], pts[k], pts[k + 1]
        p3 = pts[min(k + 2, n - 1)]
        c1 = (p1[0] + (p2[0] - p0[0]) * tension / 3, p1[1] + (p2[1] - p0[1]) * tension / 3)
        c2 = (p2[0] - (p3[0] - p1[0]) * tension / 3, p2[1] - (p3[1] - p1[1]) * tension / 3)
        d += ' C%.1f,%.1f %.1f,%.1f %.1f,%.1f' % (*c1, *c2, *p2)
    return d


def nerve(f, pts, w=4, dash=None, col=NERVE, smooth=False):
    """Nerve drawn as a gold cord along figure points (AN-11, AN-12)."""
    if smooth: d = curve(pts)
    else: d = 'M' + ' L'.join('%.1f,%.1f' % p for p in pts) if len(pts) != 3 else 'M%.1f,%.1f Q%.1f,%.1f %.1f,%.1f' % (*pts[0], *pts[1], *pts[2])
    f.raw(f'<path d="{d}" fill="none" stroke="#8a6a10" stroke-width="{w + 2}" stroke-linecap="round" stroke-linejoin="round"' + (f' stroke-dasharray="{dash}"' if dash else '') + ' opacity=".55"/>')
    f.raw(f'<path d="{d}" fill="none" stroke="{col}" stroke-width="{w}" stroke-linecap="round" stroke-linejoin="round"' + (f' stroke-dasharray="{dash}"' if dash else '') + '/>')


def point(f, x, y, code, r=7):
    """Acupoint: red dot with its code (AN-11, AN-21)."""
    f.circle(x, y, r, '#c0392b', '#fff', 2)
    f.text(x, y - r - 5, code, 13, '#a3271a', 'middle', '700')


def step_cards(f, x, y, steps, w=420, col=GOLD, size=13):
    """Numbered step cards for a nerve pathway (CH-01 02): steps = [(en, zh)]; returns the y after the last card."""
    yy = y
    for n, (en, zh) in enumerate(steps, 1):
        lines_en, lines_zh = wrap(en, int(w / (size * 0.55))), wrap(zh, int(w / size))
        h = 18 + (len(lines_en) + len(lines_zh)) * (size + 6)
        f.box(x, yy, w, h, col, '#fffdf7')
        f.step(x + 4, yy + 4, n, col)
        ty = yy + 24
        for ln in lines_en: f.text(x + 26, ty, ln, size, INK, 'start', '600'); ty += size + 6
        for ln in lines_zh: f.text(x + 26, ty, ln, size - 1, ZH, 'start', '400', 'zh-CN'); ty += size + 6
        yy += h + 10
    return yy


def wrap(text, n):
    """Greedy line wrap: words for English, characters for Chinese."""
    if any('一' <= ch <= '鿿' for ch in text):  # Chinese: by width, never splitting a Latin/number run such as L4–S3
        lines, cur, width = [], '', 0.0
        for tok in re.findall(r'[A-Za-z0-9.–-]+|.', text):
            w = len(tok) * (0.55 if tok.isascii() and tok.strip() else 1.0)
            if width + w > n and cur.strip(): lines.append(cur.rstrip()); cur, width = tok.lstrip(), w
            else: cur, width = cur + tok, width + w
        return lines + ([cur] if cur else [])
    lines, cur = [], ''
    for word in text.split():
        if len(cur) + len(word) + 1 > n and cur: lines.append(cur); cur = word
        else: cur = (cur + ' ' + word).strip()
    return lines + ([cur] if cur else [])


def clip_begin(f, x, y, w, h):
    """Start a group clipped to a figure rectangle; close it with f.end()."""
    cid = f.id('clip' + str(len(f.p)))
    f.raw(f'<clipPath id="{cid}"><rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}"/></clipPath><g clip-path="url(#{cid})">')


def ell(st, x, z, rx, rz, n=14):
    """Ellipse in the superior view, as model points converted to figure points (x, z in metres)."""
    return [st.P([x + rx * math.cos(2 * math.pi * k / n), 1.0, z + rz * math.sin(2 * math.pi * k / n)]) for k in range(n)]


def blob(pts, tension=0.5):
    """Closed smooth path (Catmull-Rom → cubic Bézier) through figure points: schematic muscle bellies."""
    n = len(pts); d = 'M%.1f,%.1f' % pts[0]
    for k in range(n):
        p0, p1, p2, p3 = pts[k - 1], pts[k], pts[(k + 1) % n], pts[(k + 2) % n]
        c1 = (p1[0] + (p2[0] - p0[0]) * tension / 3, p1[1] + (p2[1] - p0[1]) * tension / 3)
        c2 = (p2[0] - (p3[0] - p1[0]) * tension / 3, p2[1] - (p3[1] - p1[1]) * tension / 3)
        d += ' C%.1f,%.1f %.1f,%.1f %.1f,%.1f' % (*c1, *c2, *p2)
    return d + 'Z'
