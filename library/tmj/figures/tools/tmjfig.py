#!/usr/bin/env python3
"""Head and jaw figure kit: draws the skull, mandible, muscles, nerves and vessels from outlines.json (projected from the
Z-Anatomy model by export-head.py + project-outlines.py) with the shared hand-drawn Fig class from daily/engine/figlib.
Adapted from library/lumbar/figures/tools/lumbarfig.py (same helpers and conventions).

Coordinates: 3D model points [x, y, z] in metres (x<0 = right side, y up, z anterior).
A Stage places one view on the figure; stage.P(point3d) gives figure pixels."""
import json, math, re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(ROOT / 'daily'))
from engine.figlib.fig import Fig, set_out, esc, RED, BLUE, INK, GREEN, PURP, GOLD, GREY, TEAL, ZH, BONE, BONE_E  # noqa: E402,F401

HERE = Path(__file__).resolve().parent
OUTLINES = json.loads((HERE / 'outlines.json').read_text(encoding='utf-8'))
_content = HERE.parents[1] / 'content.json'
CONTENT = json.loads(_content.read_text(encoding='utf-8')) if _content.is_file() else {'muscles': []}
# AN-11: one colour per muscle for the whole chapter; the table lives in content.json (muscle "color"/"letter").
DEFAULT = {'masseter': ('#c2573a', 'Ma'), 'temporalis': ('#2f7f8f', 'Te'), 'medial-pterygoid': ('#7a5aa6', 'MP'), 'lateral-pterygoid': ('#3f8f5f', 'LP'),
           'digastric': ('#b8862b', 'Di'), 'mylohyoid': ('#4f7fb5', 'My'), 'geniohyoid': ('#8a6d3b', 'Ge'), 'stylohyoid': ('#a0527a', 'St'),
           'occipitofrontalis': ('#c98a2b', 'OF'), 'orbicularis-oculi': ('#5b8fd1', 'OOc'), 'zygomaticus-major': ('#d1675b', 'ZM'),
           'orbicularis-oris': ('#b55a8a', 'OOr'), 'buccinator': ('#6aa35a', 'Bu'), 'platysma': ('#7d8a99', 'Pl')}
COLOR = {k: v[0] for k, v in DEFAULT.items()}
LETTER = {k: v[1] for k, v in DEFAULT.items()}
NAMES = {'masseter': {'en': 'Masseter', 'zh': '咬肌'}, 'temporalis': {'en': 'Temporalis', 'zh': '颞肌'}, 'medial-pterygoid': {'en': 'Medial pterygoid', 'zh': '翼内肌'},
         'lateral-pterygoid': {'en': 'Lateral pterygoid', 'zh': '翼外肌'}}  # bootstrap; content.json muscle names replace these
for _m in CONTENT.get('muscles', []):
    COLOR[_m['id']] = _m.get('color', COLOR.get(_m['id'], RED)); LETTER[_m['id']] = _m.get('letter', LETTER.get(_m['id'], '')); NAMES[_m['id']] = _m['name']
NERVE = '#c69014'  # AN-11: nerves gold
ARTERY, VEIN = '#b8383a', '#3d5fa8'
ORIGIN_C, INSERT_C = '#245e50', '#8c2f39'
SHADE = '#ece2cc'
SKIN, SKIN_F = '#b7ab95', '#f7efe2'

MESH = {'masseter': ['Superficial part of masseter', 'Deep part of masseter'], 'masseter-superficial': ['Superficial part of masseter'], 'masseter-deep': ['Deep part of masseter'],
        'temporalis': ['Temporalis muscle'], 'medial-pterygoid': ['Medial pterygoid muscle'],
        'lateral-pterygoid': ['Superior head of lateral pterygoid muscle', 'Inferior head of lateral pterygoid muscle'],
        'lateral-pterygoid-superior': ['Superior head of lateral pterygoid muscle'], 'lateral-pterygoid-inferior': ['Inferior head of lateral pterygoid muscle'],
        'digastric': ['Anterior belly of digastric muscle', 'Posterior belly of digastric muscle', 'Intermediate tendon of digastric muscle'],
        'digastric-anterior': ['Anterior belly of digastric muscle'], 'digastric-posterior': ['Posterior belly of digastric muscle'],
        'mylohyoid': ['Mylohyoid muscle'], 'geniohyoid': ['Geniohyoid muscle'], 'stylohyoid': ['Stylohyoid muscle'],
        'occipitofrontalis': ['Frontalis muscle', 'Occipitalis muscle'], 'frontalis': ['Frontalis muscle'], 'occipitalis': ['Occipitalis muscle'],
        'orbicularis-oculi': ['Orbital part of orbicularis oculi', 'Palpebral part of orbicularis oculi'], 'zygomaticus-major': ['Zygomaticus major muscle'],
        'orbicularis-oris': ['Orbicularis oris muscle'], 'buccinator': ['Bucinator'], 'platysma': ['Platysma']}
PT = dict(OUTLINES['points'])


def V(view, p):
    x, y, z = p
    return {'lat': (z, -y), 'ant': (x, -y), 'med': (-z, -y), 'inf': (x, -z)}[view]


class Stage:
    """One view of the model placed at figure (fx, fy) for model 2D point (mx, my), at `scale` px per metre."""
    def __init__(s, f, view, mx, my, fx, fy, scale):
        s.f, s.view, s.mx, s.my, s.fx, s.fy, s.k = f, view, mx, my, fx, fy, scale

    def P2(s, x, y): return (s.fx + (x - s.mx) * s.k, s.fy + (y - s.my) * s.k)
    def P(s, p): return s.P2(*V(s.view, p))
    def L(s, a, b):
        """Figure point from the two model coordinates this view shows (lat/med: z, y; ant: x, y; inf: x, z)."""
        return s.P({'lat': [0, b, a], 'med': [0, b, a], 'ant': [a, b, 0], 'inf': [a, 0, b]}[s.view])

    def d(s, rings):
        return ' '.join('M' + ' L'.join('%.1f,%.1f' % s.P2(*pt) for pt in ring) + 'Z' for ring in rings)

    def rings(s, name, side='r'):
        o = OUTLINES[s.view]
        for key in (name, f'{name}.{side}'):
            if key in o: return o[key]
        return None

    def shape(s, name, col, fill, w=1.6, op=None, dash=None, rough=True, side='r', outer=False):
        rings = s.rings(name, side)
        if rings:
            if outer: rings = [max(rings, key=len)]
            s.f.path(s.d(rings), col, w, fill, dash=dash, rough=rough, op=op, extra='fill-rule="evenodd"')
        return rings

    def bone(s, name, w=1.5, op=None, fill=BONE, side='r', outer=False): return s.shape(name, BONE_E, fill, w, op=op, side=side, outer=outer)

    def muscle(s, mid, op=0.85, w=1.5, dash=None, fill=True, col=None, side='r', parts=None):
        col = col or COLOR.get(mid.split('|')[0], COLOR.get(re.sub(r'-(superficial|deep|superior|inferior|anterior|posterior)$', '', mid), RED))
        for name in parts or MESH[mid]:
            s.shape(name, col, tint(col) if fill else 'none', w, op=op, dash=dash, side=side, outer=True)

    def curve3(s, name, splines=None, side='r'):
        """Figure polylines of a nerve or vessel centre line from the model."""
        sp = OUTLINES['curves'].get(f'{name}.{side}') or OUTLINES['curves'].get(name) or []
        return [[s.P(p) for p in pl] for i, pl in enumerate(sp) if splines is None or i in splines]

    def cord(s, name, col=NERVE, w=3.5, splines=None, side='r', dash=None, op=None):
        for pl in s.curve3(name, splines, side): cord(s.f, pl, col, w, dash, op)

    def grid(s, x0, x1, y0, y1, step=0.01):
        """Debug: model-coordinate grid (centimetres) to read positions for labels."""
        a = x0
        while a <= x1 + 1e-9:
            p, q = s.L(a, y0), s.L(a, y1)
            s.f.raw(f'<path d="M{p[0]:.1f},{p[1]:.1f} L{q[0]:.1f},{q[1]:.1f}" stroke="#09f" stroke-width=".5" opacity=".6"/><text x="{q[0]:.1f}" y="{q[1] - 3:.1f}" font-size="9" fill="#06c">{a * 100:.0f}</text>')
            a += step
        b = y0
        while b <= y1 + 1e-9:
            p, q = s.L(x0, b), s.L(x1, b)
            s.f.raw(f'<path d="M{p[0]:.1f},{p[1]:.1f} L{q[0]:.1f},{q[1]:.1f}" stroke="#09f" stroke-width=".5" opacity=".6"/><text x="{p[0] - 22:.1f}" y="{p[1] + 3:.1f}" font-size="9" fill="#06c">{b * 100:.0f}</text>')
            b += step


def cord(f, pts, col=NERVE, w=3.5, dash=None, op=None, smooth=True):
    """Nerve or vessel drawn as a cord along figure points (AN-11, AN-12)."""
    d = curve(pts) if smooth and len(pts) > 2 else 'M' + ' L'.join('%.1f,%.1f' % p for p in pts)
    dark = shade(col)
    extra = (f' stroke-dasharray="{dash}"' if dash else '') + (f' opacity="{op}"' if op else '')
    f.raw(f'<path d="{d}" fill="none" stroke="{dark}" stroke-width="{w + 1.6}" stroke-linecap="round" stroke-linejoin="round" opacity="{0.5 * (op or 1):.2f}"' + (f' stroke-dasharray="{dash}"' if dash else '') + '/>')
    f.raw(f'<path d="{d}" fill="none" stroke="{col}" stroke-width="{w}" stroke-linecap="round" stroke-linejoin="round"{extra}/>')


def nerve(f, pts, w=3.5, dash=None, col=NERVE, smooth=True): cord(f, pts, col, w, dash, smooth=smooth)


def shade(hexcol, k=0.7):
    r, g, b = (int(hexcol[i:i + 2], 16) for i in (1, 3, 5))
    return '#%02x%02x%02x' % tuple(int(c * k) for c in (r, g, b))


def tint(hexcol, k=0.62):
    r, g, b = (int(hexcol[i:i + 2], 16) for i in (1, 3, 5))
    return '#%02x%02x%02x' % tuple(int(c + (255 - c) * k) for c in (r, g, b))


def skull_lat(st, mandible=True, teeth=True, arch=True, op=None, calvaria=True, hyoid=False, w=1.5, zyg=True):
    """Right side of the skull seen from the right, drawn back to front."""
    if calvaria:
        for n in ('Occipital bone|right', 'Parietal bone', 'Frontal bone|right'): st.bone(n, w, op, outer=True)
    st.bone('Sphenoid bone|right', w, op, fill=SHADE, outer=True)
    st.bone('Temporal bone', w, op, outer=True)
    st.bone('Maxilla', w, op, outer=True); st.bone('Nasal bone', w, op)
    if teeth:
        for n in OUTLINES['lat']:
            if n.endswith('.r') and n.startswith('Upper'): st.shape(n, BONE_E, '#fffdf8', 1.0, op=op, rough=False, outer=True)
    if mandible:
        if teeth:
            for n in OUTLINES['lat']:
                if n.endswith('.r') and n.startswith('Lower'): st.shape(n, BONE_E, '#fffdf8', 1.0, op=op, rough=False, outer=True)
        st.bone('Mandible|right', w, op, outer=True)
    if zyg: st.bone('Zygomatic bone', w, op, outer=True)
    if arch: st.bone('Temporal bone.r|near', w, op, outer=True)
    if hyoid: st.bone('Hyoid bone|right', w, op, outer=True)


def skin_lat(st, ear=True, op=None):
    """Soft head outline (schematic; the model has no skin) with the model's auricle."""
    st.shape('skin', SKIN, SKIN_F, 1.6, rough=False, op=op)


def ear_lat(st, op=None, fill='#f3e6d3', region=True):
    if region: st.shape('Auricular region', SKIN, fill, 1.4, rough=False, op=op, outer=True)
    for n in ('Helix', 'Antihelix', 'Tragus', 'Antitragus', 'Lobule of auricle', 'Concha of auricle'): st.shape(n, SKIN, 'none', 1.0, rough=False, op=op, outer=True)


def smooth_band(o, i, bow=None):
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


def band(f, mid, o, i, bow=None, op=0.85, w=1.6, col=None):
    """Schematic muscle: a smooth band from an origin line to an insertion line (figure points)."""
    col = col or COLOR.get(mid, RED)
    f.path(smooth_band(o, i, bow), col, w, tint(col), op=op)


def fibres(f, o, i, col, n=5, op=0.5, w=1.0):
    """Fibre lines from points spread along the origin edge to points spread along the insertion edge."""
    def along(pts, t):
        segs = [(pts[k], pts[k + 1], math.dist(pts[k], pts[k + 1])) for k in range(len(pts) - 1)]
        total = sum(sg[2] for sg in segs) or 1; d = t * total
        for a, b, ln in segs:
            if d <= ln or (a, b, ln) == segs[-1]:
                u = d / ln if ln else 0
                return (a[0] + (b[0] - a[0]) * u, a[1] + (b[1] - a[1]) * u)
            d -= ln
    for k in range(n):
        t = (k + 0.5) / n
        a, b = along(o, t) if len(o) > 1 else o[0], along(i, t) if len(i) > 1 else i[0]
        f.raw(f'<path d="M{a[0]:.1f},{a[1]:.1f} L{b[0]:.1f},{b[1]:.1f}" stroke="{col}" stroke-width="{w}" opacity="{op}" fill="none"/>')


def strip(f, pts, col, w=10, op=0.75):
    d = 'M' + ' L'.join('%.1f,%.1f' % p for p in pts)
    f.raw(f'<path d="{d}" fill="none" stroke="{col}" stroke-width="{w}" stroke-opacity="{op}" stroke-linecap="round" stroke-linejoin="round"/>')
    f.path(d, col, 1.2, rough=False)


def area(f, pts, col):
    """Attachment area (AN-14): dashed outline around the given figure points."""
    if len(pts) == 1:
        x, y = pts[0]; f.raw(f'<ellipse cx="{x:.1f}" cy="{y:.1f}" rx="10" ry="7" fill="{col}" fill-opacity=".18" stroke="{col}" stroke-width="2" stroke-dasharray="5 4"/>')
    else:
        d = 'M' + ' L'.join('%.1f,%.1f' % p for p in pts)
        f.raw(f'<path d="{d}" fill="none" stroke="{col}" stroke-width="9" stroke-opacity=".28" stroke-linecap="round" stroke-linejoin="round"/>')
        f.path(d, col, 2, dash='6 4', rough=False)


def oi(f, o_pts, i_pts, letter_o='O', letter_i='I', tags=True, line=True):
    """Origin and insertion areas plus the dashed O→I attachment line (AN-13)."""
    area(f, o_pts, ORIGIN_C); area(f, i_pts, INSERT_C)
    oc = centroid(o_pts); ic = centroid(i_pts)
    if line: f.raw(f'<path d="M{oc[0]:.1f},{oc[1]:.1f} L{ic[0]:.1f},{ic[1]:.1f}" stroke="#324c44" stroke-width="1.6" stroke-dasharray="7 5" fill="none"/>')
    if tags:
        oc, ic = free_spot(f, oc), free_spot(f, ic)
        tag(f, *oc, letter_o, ORIGIN_C); tag(f, *ic, letter_i, INSERT_C)
    return oc, ic


def free_spot(f, p, r=25):
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


def label(f, x, y, en, zh, col=INK, anchor='start', size=15, to=None, dot=True):
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
        if dot: f.circle(to[0], to[1], 3.2, col, '#fff', 1)
    f.bi(x, y, en, zh, size, col, anchor, '600')


def text_width(en, zh, size=15):
    wide = sum(1 for ch in en if ch.isupper() or ch in 'mwMW')
    return max(len(en) * size * 0.53 + wide * size * 0.12, len(zh) * (size - 2) * 1.0)


def name_of(mid): return NAMES.get(mid) or {'en': mid, 'zh': mid}


LABELS = {}  # figure number → O/I legend rows; build-figures.py writes them to figure-labels.json for content.json


def legend_oi(f, x, y, rows, wrap_at=None):
    """rows: [(muscle id, origin en, origin zh, insertion en, insertion zh)] → stacked bilingual O/I legend."""
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


def blob(pts, tension=0.5):
    """Closed smooth path through figure points."""
    n = len(pts); d = 'M%.1f,%.1f' % pts[0]
    for k in range(n):
        p0, p1, p2, p3 = pts[k - 1], pts[k], pts[(k + 1) % n], pts[(k + 2) % n]
        c1 = (p1[0] + (p2[0] - p0[0]) * tension / 3, p1[1] + (p2[1] - p0[1]) * tension / 3)
        c2 = (p2[0] - (p3[0] - p1[0]) * tension / 3, p2[1] - (p3[1] - p1[1]) * tension / 3)
        d += ' C%.1f,%.1f %.1f,%.1f %.1f,%.1f' % (*c1, *c2, *p2)
    return d + 'Z'


def point(f, x, y, code, r=7, dx=0, dy=None, anchor='middle'):
    """Acupoint: red dot with its code (AN-11, AN-21)."""
    f.circle(x, y, r, '#c0392b', '#fff', 2)
    f.text(x + dx, y + (dy if dy is not None else -r - 5), code, 13, '#a3271a', anchor, '700')


def wrap(text, n):
    if any('一' <= ch <= '鿿' for ch in text):
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


def card(f, x, y, w, en, zh, col=INK, size=13, title=None, fill='#fffdf7', num=None):
    """Text card with wrapped English then Chinese; returns the y below the card."""
    le, lz = wrap(en, int((w - 30) / (size * 0.52))), wrap(zh, int((w - 30) / size))
    th = 44 if title else 0
    h = 20 + th + (len(le) + len(lz)) * (size + 6)
    f.box(x, y, w, h, col, fill)
    ty = y + 24
    if title:
        f.bi(x + (34 if num else 14), ty, title[0], title[1], size + 2, col, 'start', '700'); ty += th
        if num: f.step(x + 16, y + 20, num, col)
    for ln in le: f.text(x + 14, ty, ln, size, INK, 'start', '600'); ty += size + 6
    for ln in lz: f.text(x + 14, ty, ln, size - 1, ZH, 'start', '400', 'zh-CN'); ty += size + 6
    return y + h + 10


def clip_begin(f, x, y, w, h):
    cid = f.id('clip' + str(len(f.p)))
    f.raw(f'<clipPath id="{cid}"><rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}"/></clipPath><g clip-path="url(#{cid})">')


def arrow(f, pts, col, w=3, dash=None):
    """Solid arrow along figure points (AN-13 action arrows)."""
    d = curve(pts) if len(pts) > 2 else 'M%.1f,%.1f L%.1f,%.1f' % (*pts[0], *pts[1])
    f.arrow(d, col, w, dash)


def column(f, x, y, dy, items, anchor='start', size=15, col=INK):
    """Stack bilingual labels in a column; items = [(en, zh, target point or None)]."""
    for en, zh, to in items:
        label(f, x, y, en, zh, col, anchor, size, to=to); y += dy
    return y


def lerp(a, b, t): return (a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t)


FOSSA = [(-150, 30), (-112, -2), (-70, -10), (-42, -48), (0, -70), (40, -54), (70, -20), (96, -5), (126, -16), (170, -40), (230, -52)]


def tmj_sag(f, cx, cy, k=1.0, turn=0.0, slide=0.0, disc='normal', muscles=True, ghost=False):
    """Schematic sagittal section of the right temporomandibular joint, anterior to the right.
    turn = rotation of the mandible in degrees, slide = 0..1 forward translation of the condyle,
    disc = 'normal' (on the condyle), 'anterior' (in front of the condyle) or 'recaptured'.
    Returns named figure points for labels."""
    P = lambda x, y: (cx + x * k, cy + y * k)
    R = 34 * k
    head = lerp((0, -14), (98, 38), slide); hc = P(*head)
    # temporal bone above the fossa curve
    top = [P(230, -120), P(120, -150), P(-120, -150), P(-190, -110), P(-190, 60), P(-150, 60)]
    d = curve([P(*p) for p in FOSSA]) + ' L' + ' L'.join('%.1f,%.1f' % p for p in top) + ' Z'
    f.path(d, BONE_E, 1.8, BONE)
    f.raw(f'<path d="{curve([P(*p) for p in FOSSA[2:10]])}" fill="none" stroke="#8fb4c9" stroke-width="{5 * k:.1f}" stroke-linecap="round" opacity=".8"/>')  # fibrocartilage
    mea = P(-112, 40); f.raw(f'<ellipse cx="{mea[0]:.1f}" cy="{mea[1]:.1f}" rx="{24 * k:.1f}" ry="{20 * k:.1f}" fill="#fcfaf4" stroke="{BONE_E}" stroke-width="1.6"/>')
    # mandible: head, neck and upper ramus, rotated about the head centre
    a = math.radians(turn)
    def M(x, y):  # local mandible coords (origin = head centre, y down) → figure
        xr, yr = x * math.cos(a) - y * math.sin(a), x * math.sin(a) + y * math.cos(a)
        return (hc[0] + xr * k, hc[1] + yr * k)
    ram = [M(-30, 6), M(-27, 60), M(-34, 150), M(-30, 215), M(70, 215), M(60, 150), M(34, 78), M(31, 6)]
    f.path(blob([M(0, -34), M(26, -22), M(33, 4)] + ram[::-1][:1] + [M(34, 78), M(60, 150), M(70, 215), M(-30, 215), M(-34, 150), M(-27, 60), M(-33, 4), M(-26, -22)], 0.6),
           BONE_E, 1.8, BONE, op=0.45 if ghost else None, dash='6 5' if ghost else None)
    if not ghost:
        f.raw(f'<path d="M{M(-30, -16)[0]:.1f},{M(-30, -16)[1]:.1f} A{R:.1f},{R:.1f} 0 0 1 {M(30, -16)[0]:.1f},{M(30, -16)[1]:.1f}" fill="none" stroke="#8fb4c9" stroke-width="{5 * k:.1f}" stroke-linecap="round" opacity=".8"/>')
    pts = {'head': hc, 'neck': M(0, 62), 'fovea': M(30, 40), 'ramus': M(15, 170), 'fossa': P(0, -70), 'tubercle': P(96, -5), 'postglenoid': P(-70, -10), 'meatus': mea,
           'bone': P(-60, -110)}
    if ghost: return pts
    # disc: band around the head, thick-thin-thick
    centre = {'normal': 22 - 30 * slide - turn * 0.25, 'recaptured': 22 - 30 * slide - turn * 0.25, 'anterior': 92}[disc]
    span = 112
    def ring(u, outer):
        ang = math.radians(centre - span / 2 + span * u + turn * 0)  # from up, positive towards anterior
        thick = (5 + 12 * abs(2 * u - 1) ** 1.6) * k
        r = R + 3 * k + (thick if outer else 0)
        return (hc[0] + r * math.sin(ang), hc[1] - r * math.cos(ang))
    us = [i / 14 for i in range(15)]
    poly = [ring(u, True) for u in us] + [ring(u, False) for u in reversed(us)]
    f.path(blob(poly, 0.35), '#3f6f8f', 1.6, '#bcd6e6')
    post, ant = lerp(ring(0, True), ring(0, False), 0.5), lerp(ring(1, True), ring(1, False), 0.5)
    pts.update({'disc': lerp(ring(0.5, True), ring(0.5, False), 0.5), 'post-band': lerp(ring(0.08, True), ring(0.08, False), 0.5), 'ant-band': lerp(ring(0.92, True), ring(0.92, False), 0.5),
                'upper': lerp(ring(0.3, True), P(*head), -0.12), 'lower': lerp(ring(0.3, False), hc, 0.05)})
    # retrodiscal tissue: two laminae from the posterior band back to the temporal bone and the neck
    back_up, back_low = P(-62, -6), M(-30, 30)
    f.raw(f'<path d="{curve([post, lerp(post, back_up, 0.5), back_up, lerp(back_up, back_low, 0.5), back_low, lerp(back_low, post, 0.5)])} Z" fill="#f2c9c4" stroke="#c0706a" stroke-width="1.4" opacity=".85"/>')
    pts['retro'] = centroid([post, back_up, back_low])
    # capsule in front
    f.path(curve([ant, lerp(ant, P(150, -26), 0.55), P(150, -26)]), '#7a6f5c', 1.4, dash='3 3', rough=False)
    if muscles:
        lp = COLOR['lateral-pterygoid']
        band(f, 'lateral-pterygoid', [P(250, 6), P(250, 32)], [ant, M(31, 16)], bow=3, col=lp)
        band(f, 'lateral-pterygoid', [P(250, 58), P(250, 112)], [M(32, 22), M(34, 58)], bow=5, col=lp)
        pts.update({'lp-sup': P(215, 17), 'lp-inf': P(215, 76)})
    return pts


def edge(st, name, where, frac=0.12, n=5, side='r', lo=0.0, hi=1.0):
    """Figure points along one edge of a projected structure: where = top / bottom / front / back (of the drawing);
    lo..hi trims the run along the edge (0..1)."""
    ring = max(st.rings(name, side), key=len)
    xs, ys = [p[0] for p in ring], [p[1] for p in ring]
    ax = 1 if where in ('top', 'bottom') else 0
    vals = ys if ax else xs
    a, b = min(vals), max(vals)
    keep = [p for p in ring if (p[ax] <= a + frac * (b - a) if where in ('top', 'back') else p[ax] >= b - frac * (b - a))]
    keep.sort(key=lambda p: p[1 - ax])
    keep = keep[int(lo * len(keep)):max(int(hi * len(keep)), int(lo * len(keep)) + 1)]
    step = max(1, len(keep) // n)
    pts = keep[::step][:n] + ([keep[-1]] if len(keep) > 1 else [])
    return [st.P2(*p) for p in pts]


def orbits_ant(st):
    """Orbits and nasal opening drawn by hand on the anterior skull (the projected bones are silhouettes)."""
    for sx in (-1, 1):
        c = st.L(sx * 0.0335, 1.5935)
        st.f.raw(f'<ellipse cx="{c[0]:.1f}" cy="{c[1]:.1f}" rx="{0.019 * st.k:.1f}" ry="{0.0165 * st.k:.1f}" fill="#d9ceb8" stroke="{BONE_E}" stroke-width="1.4"/>')
    n = [st.L(0, 1.583), st.L(-0.012, 1.562), st.L(0, 1.557), st.L(0.012, 1.562)]
    st.f.raw('<path d="M' + ' L'.join('%.1f,%.1f' % p for p in n) + f' Z" fill="#d9ceb8" stroke="{BONE_E}" stroke-width="1.4"/>')


def skull_ant(st, op=None, w=1.5, teeth=True):
    for n in ['Occipital bone', 'Parietal bone.r', 'Parietal bone.l', 'Temporal bone.r', 'Temporal bone.l', 'Sphenoid bone', 'Frontal bone', 'Zygomatic bone.r', 'Zygomatic bone.l',
              'Maxilla.r', 'Maxilla.l', 'Nasal bone.r', 'Nasal bone.l', 'Mandible']:
        r = OUTLINES['ant'].get(n)
        if r: st.f.path(st.d([max(r, key=len)]), BONE_E, w, BONE, op=op)
    if teeth:
        for n in OUTLINES['ant']:
            if n.startswith(('Upper', 'Lower')): st.shape(n, BONE_E, '#fffdf8', 0.9, rough=False, op=op, outer=True)
    orbits_ant(st)
