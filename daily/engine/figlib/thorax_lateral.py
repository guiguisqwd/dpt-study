#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Right lateral view of the thorax (front = viewer's right), upper limb removed to show the chest
wall. Ribs 1–9, a see-through scapula on the back, helpers to place points on a rib.
Reused for serratus anterior, latissimus dorsi, the lateral thoracic points (SP21 大包, GB22–23 …)."""
from .fig import *

BACK_X, FRONT_X = 330, 900


def rib_pts(k):
    """posterior end, lateral mid, anterior bony end, sternal end of rib k (1–9)."""
    yp = 196 + 50 * k
    return (370 + max(0, 4 - k) * 18, yp), (600, yp + 52 + 4 * k), (812 - max(0, 3 - k) * 30, yp + 70 + 3 * k), (884, yp + 30 + 2 * k)


def rib_point(k, t):
    """point at fraction t (0 = posterior end, 1 = anterior bony end) along rib k (quadratic curve)."""
    (x0, y0), (x1, y1), (x2, y2), _ = rib_pts(k)
    cx, cy = 2 * x1 - (x0 + x2) / 2, 2 * y1 - (y0 + y2) / 2
    return ((1 - t) ** 2 * x0 + 2 * (1 - t) * t * cx + t * t * x2, (1 - t) ** 2 * y0 + 2 * (1 - t) * t * cy + t * t * y2)


SCAP_LAT = "M392,262 C440,258 520,262 566,276 C590,286 596,318 580,338 C548,420 488,520 446,622 C430,640 412,632 410,612 C404,500 398,380 392,262 Z"


def thorax_lateral_base(f, scap=True, nums=True):
    f.path("M560,150 C470,170 380,210 342,280 C318,360 316,520 330,640 C342,740 380,830 430,880 L860,880 C900,800 916,660 912,520 "
           "C908,380 890,260 840,200 C790,160 680,140 560,150 Z", "#b9b2a3", 1.5, "#f8f3e8")                  # chest wall outline
    for k in range(1, 10):
        p0, p1, p2, p3 = rib_pts(k)
        cx, cy = 2 * p1[0] - (p0[0] + p2[0]) / 2, 2 * p1[1] - (p0[1] + p2[1]) / 2
        d = f"M{p0[0]},{p0[1]} Q{cx:.0f},{cy:.0f} {p2[0]},{p2[1]}"
        f.path(d, "#c9bfa9", 13, rough=False); f.path(d, BONE, 9, rough=False)
        f.path(f"M{p2[0]},{p2[1]} Q{(p2[0] + p3[0]) / 2 + 10:.0f},{(p2[1] + p3[1]) / 2 + 8:.0f} {p3[0]},{p3[1]}", "#d8cfbd", 7, rough=False)  # costal cartilage
        if nums:
            f.text(p0[0] - 12, p0[1] + 5, str(k), 13, "#8a7f6c", "end", "700")
    f.path("M884,250 L892,700", BONE_E, 1.4, rough=False, op=0.5)                                              # sternum edge
    if scap:
        f.path(SCAP_LAT, "#6b6458", 1.8, "#efe6d4", dash="7 5", op=0.55)


def front_back_labels(f, y=120):
    f.bi(1010, y, "Front →", "前", 13, "#777", "middle", "400")
    f.bi(250, y, "← Back", "后", 13, "#777", "middle", "400")


SA_FILL, SA_EDGE = "#ecb9a4", "#b4664d"
LTN = "M524,176 C534,260 546,360 556,450 C562,520 568,600 572,690"          # long thoracic nerve on the serratus surface


def medial_border(t):
    """point on the scapula's medial border, t = 0 (superior angle) … 1 (inferior angle)."""
    return (392 + 20 * t, 262 + 352 * t)


SA_INS = {1: 0.03, 2: 0.09, 3: 0.26, 4: 0.46, 5: 0.80, 6: 0.86, 7: 0.92, 8: 0.97}


def serratus(f, op=0.88, nerve=True, digits=range(1, 9)):
    """Serratus anterior: eight tongue-shaped digitations. Their pointed tips arise from the outer
    surfaces of ribs 1–8 along an oblique line (upper ribs further forward); the sheet sweeps back
    deep to the scapula to its medial border (1–2 → superior angle, 3–4 → border, 5–8 → inferior angle).
    Returns {k: (origin_tip, insertion_point)}."""
    pts = {}
    for k in sorted(digits, reverse=True):
        t = 0.86 - 0.04 * k
        tip = rib_point(k, t)
        ti = SA_INS[k]
        i1, i2 = medial_border(max(0, ti - 0.035)), medial_border(min(1, ti + 0.035))
        back = rib_point(k, 0.18)
        up = (back[0] + 40, back[1] - 18 - (8 if k > 4 else 0))
        lo = (back[0] + 60, back[1] + 26)
        f.path(f"M{tip[0]:.0f},{tip[1]:.0f} C{(tip[0] + up[0]) / 2:.0f},{tip[1] - 22:.0f} {up[0]:.0f},{up[1]:.0f} {i1[0]:.0f},{i1[1]:.0f} "
               f"L{i2[0]:.0f},{i2[1]:.0f} C{lo[0]:.0f},{lo[1]:.0f} {(tip[0] + lo[0]) / 2:.0f},{tip[1] + 24:.0f} {tip[0]:.0f},{tip[1]:.0f} Z",
               SA_EDGE, 1.4, SA_FILL, op=op)
        for frac in (0.35, 0.65):   # fibre hints
            a = (tip[0] + (i1[0] - tip[0]) * 0.02, tip[1] + (frac - 0.5) * 16)
            f.raw(f'<path d="M{tip[0]:.0f},{tip[1]:.0f} Q{(tip[0] + i1[0]) / 2:.0f},{(tip[1] + i1[1]) / 2 + (frac - 0.5) * 40:.0f} {(i1[0] + i2[0]) / 2:.0f},{(i1[1] + i2[1]) / 2:.0f}" stroke="{SA_EDGE}" stroke-width=".8" fill="none" opacity=".45"/>')
        pts[k] = (tip, ((i1[0] + i2[0]) / 2, (i1[1] + i2[1]) / 2))
    if nerve:
        f.path(LTN, GOLD, 3.2, rough=False)
        for k in digits:
            tip, _ = pts[k]
            y = tip[1] - 10
            x = 524 + (y - 176) * 0.09
            f.path(f"M{x:.0f},{y:.0f} L{x + 30:.0f},{y + 6:.0f}", GOLD, 1.4, rough=False)
    return pts
