#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Week 1 Tuesday 2026-10-13: subacromial pain syndrome (assessment to treatment) and the bony landmarks of the scapula and humerus.
Run via pipeline (figures step) or: python3 figures.py <out_dir>."""
import pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2]))
from engine.figlib import *

MUTE = "#6b706a"

# ------------------------------------------------------------------ bones (right side, posterior view, base coordinates)
# The anterior view draws the same scapula mirrored. The humerus is pulled away from the glenoid ("exploded")
# so that the glenoid rim, the notches and the tubercles can be seen.
SCAP_P = ("M85,72 L288,64 C294,64 296,86 304,86 C312,86 312,66 318,66 C340,70 360,82 372,100 "
          "C390,112 400,140 400,166 C400,192 392,210 380,220 C350,262 320,310 300,352 C270,420 230,500 190,580 "
          "C184,594 176,602 170,598 C150,560 132,520 118,480 C96,430 70,380 62,340 C62,290 68,220 76,160 Z")
SPINE_P = "M86,160 L250,118 L392,76 L420,104 C396,114 360,132 334,150 L250,146 L90,188 Z"
ACROM_P = "M392,72 Q470,42 542,56 Q556,72 542,86 Q470,96 420,104 Z"
CORAC_A = "M318,68 C326,44 350,24 382,20 C404,18 418,28 412,40 C396,38 374,44 356,58 C346,66 340,74 334,80 Z"
GLEN_A = "M392,118 C404,134 406,190 392,212 C386,196 384,140 392,118 Z"
HEAD = (548, 200, 56)
HUM_SHAFT = ("M520,248 C516,300 518,380 520,460 C522,560 520,640 518,720 L566,720 C566,640 568,560 572,470 "
             "C576,400 580,340 586,300 C592,276 600,262 606,250 Z")
GT_P = "M590,160 C616,150 640,172 640,206 C640,236 626,256 604,258 C588,246 584,190 590,160 Z"   # greater tubercle (lateral)
LT_A = "M540,254 C550,246 562,252 562,266 C562,282 552,290 542,284 C534,278 532,262 540,254 Z"   # lesser tubercle (anterior, below the head)
DT = "M574,440 C588,456 592,486 584,516"                                                       # deltoid tuberosity (lateral)


def bones(f, view):
    """Scapula + exploded humerus in base coordinates (the caller's group transform places and mirrors it)."""
    f.path(SCAP_P, BONE_E, 2, BONE)
    if view == "post":
        f.path("M336,150 C350,170 376,170 392,152", "#8a8273", 1.4, dash="4 4", rough=False)        # depth of the spinoglenoid notch
        f.path(SPINE_P, BONE_E, 1.8, "#efe5cf")
    else:
        for d in ("M120,200 C200,230 280,250 350,250", "M110,300 C190,320 260,330 320,330", "M120,400 C180,410 230,420 270,420"):
            f.path(d, "#c9bfa9", 1.4, rough=False)                                                    # ridges on the subscapular fossa
        f.path("M300,102 L392,76 L420,104 C396,114 360,132 334,150 L300,152", "#9a958a", 1.2, dash="5 5", rough=False)  # lateral spine, on the back
        f.path(GLEN_A, BONE_E, 1.6, "#e8dcc2")
        f.path(CORAC_A, BONE_E, 1.8, BONE)
    f.path(ACROM_P, BONE_E, 1.8, BONE)
    f.path(HUM_SHAFT, BONE_E, 2, BONE)
    f.path(GT_P, BONE_E, 1.8, BONE)
    f.raw(f'<circle cx="{HEAD[0]}" cy="{HEAD[1]}" r="{HEAD[2]}" fill="{BONE}" stroke="{BONE_E}" stroke-width="2"/>')
    if view == "ant":
        f.path("M576,262 C574,310 568,360 562,404", "#e3d5b8", 10, rough=False)                     # intertubercular groove
        f.path("M588,260 C584,300 576,352 570,404", BONE_E, 1.3, rough=False)                       # lateral lip of the groove
        f.path("M562,284 C560,322 556,362 553,404", BONE_E, 1.3, rough=False)                       # medial lip of the groove
        f.path(LT_A, BONE_E, 1.6, BONE)
    f.path("M520,304 C540,312 562,312 582,304", "#8a8273", 1.4, dash="5 4", rough=False)            # surgical neck
    f.path(DT, BONE_E, 3, rough=False)
    f.path("M512,720 L574,720", "#fcfaf4", 6, rough=False)                                          # shaft cut


def marker(f, x, y, letter, col=INK):
    f.circle(x, y, 15, "#fffdf7", col, 2.2)
    f.text(x, y + 6, letter, 17, col, "middle", "700")


# ------------------------------------------------------------------ 03 bony landmarks (lettered, for labelling)
LM_POST = [  # letter, base point on the bone, marker offset (dx, dy) in canvas px
    ("A", (480, 66), (0, -40)), ("B", (200, 146), (0, 0)), ("C", (200, 98), (0, 0)), ("D", (200, 320), (0, 0)),
    ("E", (362, 156), (-30, 46)), ("F", (304, 82), (-18, -46)), ("G", (66, 330), (-40, 0)), ("H", (300, 352), (38, 14)),
    ("I", (172, 598), (-36, 22)), ("J", (628, 206), (40, -6)), ("K", (582, 305), (44, 4)), ("L", (586, 478), (40, 0)),
]
LM_ANT = [
    ("M", (390, 26), (0, -40)), ("N", (396, 166), (-6, 64)), ("O", (230, 340), (0, 0)), ("P", (548, 268), (40, 34)),
    ("Q", (568, 340), (-46, 24)),
]


def f03():
    f = Fig("03", 1500, 1000, "Bony landmarks of the right scapula and humerus", "右侧肩胛骨与肱骨的骨性标志")
    f.bi(40, 118, "Name each lettered landmark, then check the quiz answers.", "先说出每个字母指的骨性标志，再看自测答案。", 15, INK, weight="400")
    sa, xa, ya = 0.92, 40, 170               # posterior view: subject's right is the viewer's right
    sb, xb, yb = 0.92, 1460, 170             # anterior view: mirrored, so the lateral side is on the viewer's left
    pa = lambda x, y: (xa + sa * x, ya + sa * y)
    pb = lambda x, y: (xb - sb * x, yb + sb * y)
    f.bi(60, 175, "Posterior view", "后面观", 20, INK, weight="700")
    f.bi(830, 175, "Anterior view", "前面观", 20, INK, weight="700")
    f.g(f"translate({xa},{ya}) scale({sa})"); bones(f, "post"); f.end()
    f.g(f"translate({xb},{yb}) scale({-sb},{sb})"); bones(f, "ant"); f.end()
    for pts, p, col in ((LM_POST, pa, INK), (LM_ANT, pb, INK)):
        for letter, (bx, by), (dx, dy) in pts:
            x, y = p(bx, by)
            if dx or dy:
                f.leader(x, y, x + dx, y + dy, "#555")
                f.circle(x, y, 3.5, INK, INK, 0)
            marker(f, x + dx, y + dy, letter, col)
    f.bi(60, 880, "Exploded view: the humerus is drawn a little away from the scapula so the glenoid and the notches show.",
         "分离示意：肱骨画得离肩胛骨稍远，好看清关节盂和两个切迹。", 14, MUTE, weight="400")
    f.bi(60, 920, "In the anterior view the glenoid is seen edge-on; it faces laterally toward the humeral head.",
         "前面观里关节盂只看到侧边；它朝外侧，对着肱骨头。", 14, MUTE, weight="400")
    f.save("肩胛骨与肱骨标志-看图标注")


# ------------------------------------------------------------------ 01 subacromial space
def f01():
    f = Fig("01", 1400, 860, "The subacromial space", "肩峰下间隙")
    f.bi(40, 120, "Right shoulder, front view, coronal schematic: lateral is on the left.", "右肩前面观，冠状面示意：左边是外侧。", 15, INK, weight="400")
    # scapula: glenoid facing the humeral head, superior border running medially under the supraspinatus
    f.path("M560,372 C574,352 600,340 640,338 L900,330 L900,354 L660,364 C638,384 630,430 634,470 C640,530 660,600 700,700 "
           "L652,712 C622,640 600,590 584,566 C570,560 562,552 560,548 C548,520 546,410 560,372 Z", BONE_E, 2, BONE)
    f.path("M562,380 C552,420 552,500 562,544", BONE_E, 4, rough=False)                                       # glenoid articular surface
    # humerus: shaft + neck, then head and greater tubercle on top
    f.path("M352,350 C318,380 300,452 310,520 C318,600 330,700 334,800 L452,800 C454,720 466,650 492,600 C506,580 520,566 530,556", BONE_E, 2, BONE)
    f.raw(f'<circle cx="440" cy="468" r="112" fill="{BONE}" stroke="{BONE_E}" stroke-width="2"/>')
    f.path("M306,456 C300,408 318,364 352,348 C372,374 382,420 374,470 C352,480 324,474 306,456 Z", BONE_E, 2, BONE)   # greater tubercle (lateral)
    # roof: acromion
    f.path("M246,250 C320,232 440,230 560,238 C620,242 660,248 690,256 L684,290 C640,282 590,278 540,278 C430,276 330,280 260,292 C242,284 238,258 246,250 Z", BONE_E, 2, BONE)
    # supraspinatus: belly over the scapula (in the fossa) → tendon between head and acromion → superior facet of the greater tubercle
    f.path("M900,290 C800,286 700,292 620,300 C540,306 460,316 400,330 C372,338 352,348 340,360 L354,378 C380,366 420,356 470,350 "
           "C540,344 600,342 660,338 C760,334 840,332 900,332 Z", RED, 1.8, "#e9a596", op=0.92)
    # subacromial (subdeltoid) bursa: between the tendon and the acromion, running out laterally under the deltoid
    f.path("M600,296 C520,298 430,302 370,314 C320,326 286,344 270,372 C290,362 330,346 380,334 C450,320 530,312 600,308 Z", BLUE, 1.4, "#cfe0f2", op=0.95)
    # deltoid outline
    f.path("M244,256 C190,310 176,420 200,560 C214,640 246,700 290,744", "#999", 1.6, dash="6 6", rough=False)
    for (x, y), (lx, ly), en, zh, col in [((560, 256), (960, 200), "Acromion: the bony roof of the space", "肩峰：间隙的骨性顶", INK),
                                         ((780, 312), (960, 300), "Supraspinatus: muscle belly → tendon under the acromion", "冈上肌：肌腹 → 肩峰下方的肌腱", RED),
                                         ((470, 450), (960, 450), "Humeral head: the floor of the space", "肱骨头：间隙的底", INK),
                                         ((556, 470), (960, 540), "Glenoid cavity of the scapula", "肩胛骨关节盂", INK),
                                         ((780, 342), (960, 380), "Scapula: floor of the supraspinous fossa", "肩胛骨：冈上窝底", INK)]:
        f.leader(x, y, lx - 8, ly - 5, col); f.bi(lx, ly, en, zh, 15, col)
    for (x, y), (lx, ly, w), en, zh, col in [((282, 360), (40, 330, 228), "Subacromial (subdeltoid) bursa", "肩峰下（三角肌下）滑囊", BLUE),
                                            ((190, 480), (40, 480, 140), "Deltoid (dashed)", "三角肌（虚线）", "#6b706a"),
                                            ((340, 372), (40, 640, 226), "Greater tubercle, superior facet", "大结节上小面", INK)]:
        f.leader(x, y, lx + w, ly - 5, col); f.bi(lx, ly, en, zh, 15, col)
    f.bi(960, 640, "About 1–1.5 cm high; it narrows as the arm is raised.", "这个间隙高约 1–1.5 cm，抬臂时会变窄。", 14, MUTE, weight="400")
    f.bi(960, 690, "Source: StatPearls, Shoulder Impingement Syndrome.", "依据：StatPearls「肩峰下撞击综合征」。", 14, MUTE, weight="400")
    f.save("肩峰下间隙")

# ------------------------------------------------------------------ 02 painful arc
CORE = (70, 100)         # inside every opened source's range
WIDE = (60, 120)         # union of the opened sources: AAFP 2008 60–100, StatPearls ~70–120, TeachMeAnatomy 60–120


def f02():
    import math
    f = Fig("02", 1400, 820, "The painful arc during abduction", "外展时的疼痛弧")
    f.bi(40, 120, "Right arm raised sideways, front view. The angle is shoulder abduction from the side of the body.", "右臂向侧方抬起，前面观。角度是从体侧算起的肩外展。", 15, INK, weight="400")
    cx, cy, R = 560, 470, 270
    pt = lambda deg, r: (cx - r * math.sin(math.radians(deg)), cy + r * math.cos(math.radians(deg)))   # 0° = arm down, 90° = sideways (left), 180° = overhead
    def sector(a, b, fill, edge):
        x1, y1 = pt(a, R); x2, y2 = pt(b, R); xi1, yi1 = pt(a, R - 70); xi2, yi2 = pt(b, R - 70)
        f.path(f"M{xi1:.1f},{yi1:.1f} L{x1:.1f},{y1:.1f} A{R},{R} 0 0 1 {x2:.1f},{y2:.1f} L{xi2:.1f},{yi2:.1f} A{R-70},{R-70} 0 0 0 {xi1:.1f},{yi1:.1f} Z", edge, 1.4, fill, rough=False)
    GREEN_F, LIGHT_F, CORE_F = "#e3eadb", "#f8dcd4", "#f1a898"
    sector(0, WIDE[0], GREEN_F, "#8aa07a"); sector(WIDE[0], CORE[0], LIGHT_F, RED); sector(CORE[0], CORE[1], CORE_F, RED)
    sector(CORE[1], WIDE[1], LIGHT_F, RED); sector(WIDE[1], 180, GREEN_F, "#8aa07a")
    # trunk and head (simple outline), shoulder at the centre
    f.path(f"M{cx+10},{cy-20} C{cx+60},{cy-30} {cx+120},{cy-24} {cx+150},{cy} L{cx+150},{cy+300} L{cx+10},{cy+300} Z", "#b9b2a3", 1.4, "#f8f3e8")
    f.raw(f'<circle cx="{cx+80}" cy="{cy-90}" r="48" fill="#f8f3e8" stroke="#b9b2a3" stroke-width="1.4"/>')
    for deg, strong in ((0, False), (85, True)):        # arm at the side (faint) and in the middle of the arc
        x, y = pt(deg, R - 90)
        f.path(f"M{cx},{cy} L{x:.1f},{y:.1f}", INK if strong else "#9a958a", 10 if strong else 7, rough=False, op=1.0 if strong else 0.4)
    f.circle(cx, cy, 9, INK, "#fff", 2)
    for deg in (0, 30, 60, 90, 120, 150, 180):
        x, y = pt(deg, R + 26)
        f.text(x, y + 6, f"{deg}°", 15, INK, "middle", "700")
    for deg in CORE:
        x, y = pt(deg, R + 24)
        f.text(x, y + 5, f"{deg}°", 14, RED, "middle", "700")
    f.bi(236, 560, "Painful arc", "疼痛弧", 16, RED, "end")
    # key and the ranges in the opened sources
    X = 900
    for i, (fill, edge, en, zh) in enumerate([(CORE_F, RED, "About 70–100°: inside every source's range", "约 70–100°：几个来源都包括"),
                                               (LIGHT_F, RED, "60–70° and 100–120°: only some sources", "60–70° 与 100–120°：只有部分来源包括"),
                                               (GREEN_F, "#8aa07a", "Outside the arc", "弧外")]):
        y = 230 + i * 62
        f.raw(f'<rect x="{X}" y="{y - 16}" width="26" height="26" rx="4" fill="{fill}" stroke="{edge}" stroke-width="1.4"/>')
        f.bi(X + 40, y, en, zh, 15, INK, weight="400")
    f.bi(X, 440, "How the opened sources define it", "查到的来源怎么写", 16, INK)
    for i, (en, zh) in enumerate([("AAFP 2008: 60–100° of active abduction", "AAFP 2008：主动外展 60–100°"),
                                  ("StatPearls: about 70–120°, relief above it", "StatPearls：约 70–120°，再往上相对缓解"),
                                  ("TeachMeAnatomy: 60–120°", "TeachMeAnatomy：60–120°")]):
        f.bi(X, 492 + i * 54, en, zh, 15, INK, weight="400")
    f.bi(X, 680, "The patient raises the arm actively.", "检查时让病人自己抬臂（主动运动）。", 15, MUTE, weight="400")
    f.save("疼痛弧")


def build(out_dir):
    set_out(out_dir)
    f01(); f02(); f03()


if __name__ == "__main__":
    build(sys.argv[1] if len(sys.argv) > 1 else pathlib.Path(__file__).resolve().parent / "资源")
