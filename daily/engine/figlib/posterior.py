#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Posterior view of the upper trunk (both sides). Viewer looks at the back, so the subject's RIGHT
side is on the viewer's RIGHT. Midline x = 650. Reused for trapezius, levator scapulae, rhomboids,
latissimus dorsi, and the posterior acupoints (SI, BL, GV) later.

Vertebral levels (spinous process tips): C2 y=185 … C7 y=325 (28 px steps), T1 y=361 … T12 y=757
(36 px steps). Right scapula: superior angle ≈ T2, root of spine ≈ T3, inferior angle ≈ T7."""
from .fig import *

MID = 650


def sp_y(level):
    """y of a spinous process tip, level like 'C7', 'T4'."""
    k = int(level[1:])
    return 185 + (k - 2) * 28 if level[0] == "C" else 325 + k * 36


def mirror(d, mid=MID):
    """Mirror an SVG path (absolute M/L/C/Q/Z commands with x,y pairs) to the other side."""
    import re
    return re.sub(r"(-?\d+(?:\.\d+)?),(-?\d+(?:\.\d+)?)", lambda m: f"{2 * mid - float(m.group(1)):g},{m.group(2)}", d)


# right scapula (viewer's right)
SCAP_R = ("M748,392 C790,384 830,378 862,382 L878,372 C892,380 900,396 906,414 C912,440 902,470 890,500 "
          "C870,540 830,585 788,606 C778,610 772,600 772,590 C766,540 756,470 748,392 Z")
SPINE_R = "M752,446 C800,428 860,400 912,372 L946,356 C956,362 958,374 948,382 L918,392 C866,416 806,446 756,462 Z"
ACROM_R = "M912,372 C934,352 966,348 986,358 C996,368 990,382 970,386 C950,390 932,388 918,392 Z"
CLAV_R = "M980,352 C930,342 880,336 846,333"
HUM_R = "M962,410 C972,470 980,560 984,700 L1018,700 C1016,560 1010,470 1004,410 Z"
TRAP_UP_R = "M650,140 C672,138 690,138 706,142 C712,206 738,264 790,300 C840,330 896,344 940,352 L912,374 C850,380 760,368 650,325 Z"
TRAP_MID_R = "M650,325 C760,368 850,380 912,374 C860,402 800,428 752,446 C720,452 690,460 650,469 Z"
TRAP_LOW_R = "M650,469 C690,460 720,452 752,446 L756,462 C730,520 690,640 650,757 Z"


def posterior_base(f, scap=True, ribs=True, both=True, hum=True, head=True, labels=True):
    """Bones and outline. Muscles are drawn by the caller on top."""
    if head:
        f.raw(f'<ellipse cx="{MID}" cy="58" rx="112" ry="98" fill="#f6efe2" stroke="#9a958a" stroke-width="1.6"/>')
        f.path(f"M560,128 C600,142 630,146 {MID},140 C670,146 700,142 740,128", "#9a958a", 1.4, rough=False)   # superior nuchal line
        f.circle(MID, 140, 5, BONE_E, "#fff", 1.5)                                                          # EOP
    f.path("M594,142 C588,206 562,264 510,300 C460,330 404,344 360,352 C330,358 300,372 300,400 L300,800 L1000,800 L1000,400 C1000,372 970,358 940,352 "
           "C896,344 840,330 790,300 C738,264 712,206 706,142", "#b9b2a3", 1.4, "#f8f3e8")                       # neck + shoulder contour = trapezius edge                                                                          # body outline
    if ribs:
        for k in range(2, 11):
            y = sp_y(f"T{k}") - 10
            for side in (1, -1) if both else (1,):
                x1 = MID + side * 18
                f.path(f"M{x1},{y} C{MID + side * 120},{y - 26} {MID + side * 250},{y + 10} {MID + side * 300},{y + 70}", "#ddd3c0", 5, rough=False)
    for k in range(2, 8):
        y = sp_y(f"C{k}")
        f.raw(f'<rect x="{MID - 11}" y="{y - 7}" width="22" height="14" rx="5" fill="{BONE}" stroke="{BONE_E}" stroke-width="1.4"/>')
    for k in range(1, 13):
        y = sp_y(f"T{k}")
        f.raw(f'<rect x="{MID - 13}" y="{y - 8}" width="26" height="16" rx="5" fill="{BONE}" stroke="{BONE_E}" stroke-width="1.4"/>')
    if labels:
        for lv in ("C7", "T1", "T4", "T7", "T12"):
            f.text(MID - 22, sp_y(lv) + 5, lv, 13, "#6b6458", "end", "700")
    if scap:
        for side in ("R", "L") if both else ("R",):
            tr = (lambda d: d) if side == "R" else mirror
            if hum:
                f.path(tr(HUM_R), BONE_E, 1.6, BONE)
                cx = 984 if side == "R" else 2 * MID - 984
                f.raw(f'<circle cx="{cx}" cy="412" r="38" fill="{BONE}" stroke="{BONE_E}" stroke-width="1.6"/>')
            f.path(tr(SCAP_R), BONE_E, 2, BONE)
            f.path(tr(SPINE_R), BONE_E, 1.8, "#efe5cf")
            f.path(tr(ACROM_R), BONE_E, 1.8, BONE)
            f.path(tr(CLAV_R), "#a59a86", 8, rough=False, op=0.35)


TRAP_COL = {"up": ("#e9a596", RED), "mid": ("#eab98f", "#a0522d"), "low": ("#d9b3a6", "#8f4a3c")}


def trapezius(f, op=0.8, left_op=0.3, both=True, fibers=True):
    for key, d in (("up", TRAP_UP_R), ("mid", TRAP_MID_R), ("low", TRAP_LOW_R)):
        fill, edge = TRAP_COL[key]
        f.path(d, edge, 1.8, fill, op=op)
        if both:
            f.path(mirror(d), edge, 1.2, fill, op=left_op)
    if fibers:   # fibre direction hints (right side)
        for a, b in [((664, 180), (900, 352)), ((664, 250), (880, 360)), ((664, 330), (880, 372)), ((664, 380), (840, 400)),
                     ((664, 430), (790, 430)), ((664, 520), (752, 455)), ((664, 620), (750, 460)), ((660, 700), (752, 462))]:
            f.raw(f'<path d="M{a[0]},{a[1]} L{b[0]},{b[1]}" stroke="#ffffff" stroke-width="1.3" opacity=".55"/>')
