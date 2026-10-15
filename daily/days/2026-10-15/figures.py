#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Week 1 Thursday 2026-10-15: reading the Hando 2026 dry-needling trial, and the glenohumeral capsule and ligaments.
Run via pipeline (figures step) or: python3 figures.py <out_dir>.
01 plots the numbers of daily/papers/hando-2026-dry-needling.json; 02 to 04 are new drawings (the chapter has no
capsule or ligament figure). Attachments follow TeachMeAnatomy and Kenhub (the chapter's shoulder-joint sources)
and Radiopaedia; see the chapter text for where they differ."""
import math, pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2]))
from engine.figlib import *

MUTE = "#6b706a"


def foot(p, en, zh):
    svg = p.read_text(encoding="utf-8")
    svg = svg.replace("Schematic; pathway and layers are simplified.", en).replace("解剖示意；走行与层次经过简化。", zh)
    p.write_text(svg, encoding="utf-8")


# ------------------------------------------------------------------ 01 effect sizes of the trial (abstract numbers only)
def f01():
    f = Fig("01", 1400, 900, "Hando 2026: what the results abstract reports", "Hando 2026：结果摘要报告的效应量")
    f.bi(38, 116, "Each row compares PT + DN with one control group. Square = reported estimate; line = its 95% confidence interval.",
         "每一行是干针组（PT + DN）和一个对照组的比较。方块是报告的估计值，横线是 95% 置信区间。", 15, MUTE, weight="400")

    def panel(x0, label_w, px0, px1, lo, hi, ticks, rows, head, sub, fav_l, fav_r, zero_col):
        sc = (px1 - px0) / (hi - lo)
        X = lambda v: px0 + (v - lo) * sc
        f.text(x0, 182, head[0], 19, INK, "start", "700")
        f.text(x0, 205, head[1], 16, ZH, "start", "400", "zh-CN")
        f.text(x0, 234, sub[0], 14, MUTE)
        f.text(x0, 254, sub[1], 13, MUTE, "start", "400", "zh-CN")
        top, axis = 276, 276 + 78 * len(rows) + 6
        f.path(f"M{X(0):.1f},{top} L{X(0):.1f},{axis}", zero_col, 1.6, dash="5 5", rough=False)
        for i, (lab_en, lab_zh, est, a, b, txt) in enumerate(rows):
            y = top + 40 + 78 * i
            f.text(x0, y - 12, lab_en, 16, INK, "start", "700")
            f.text(x0, y + 8, lab_zh, 14, ZH, "start", "400", "zh-CN")
            f.text(x0, y + 28, txt, 14, INK)
            f.path(f"M{X(a):.1f},{y} L{X(b):.1f},{y}", INK, 2.6, rough=False)
            f.path(f"M{X(a):.1f},{y - 8} L{X(a):.1f},{y + 8} M{X(b):.1f},{y - 8} L{X(b):.1f},{y + 8}", INK, 2, rough=False)
            f.raw(f'<rect x="{X(est) - 9:.1f}" y="{y - 9}" width="18" height="18" fill="{BLUE}" stroke="#fff" stroke-width="1.5"/>')
        f.path(f"M{px0},{axis} L{px1},{axis}", INK, 1.8, rough=False)
        for t in ticks:
            f.leader(X(t), axis, X(t), axis + 7, INK)
            f.text(X(t), axis + 26, (f"+{t}" if t > 0 else ("0" if t == 0 else f"−{-t}")), 14, INK, "middle")
        f.text(X(0) - 10, axis + 54, fav_l[0], 14, INK, "end", "700")
        f.text(X(0) - 10, axis + 73, fav_l[1], 13, ZH, "end", "400", "zh-CN")
        f.text(X(0) + 10, axis + 54, fav_r[0], 14, INK, "start", "700")
        f.text(X(0) + 10, axis + 73, fav_r[1], 13, ZH, "start", "400", "zh-CN")
        return axis

    ax1 = panel(38, 250, 300, 650, -20, 10, (-20, -15, -10, -5, 0, 5, 10), [
        ("PT + DN vs PT", "干针组 对比 物理治疗组", -7.51, -16.57, 1.54, "−7.51 (−16.57 to 1.54)"),
        ("PT + DN vs PT + SDN", "干针组 对比 假干针组", -9.85, -18.98, 0.73, "−9.85 (−18.98 to 0.73) *"),
    ], ("Primary outcome: SPADI at 1 year", "主要结局：1 年时的 SPADI"),
       ("Difference in points; lower SPADI = less pain and disability", "分差；SPADI 越低，疼痛与功能障碍越轻"),
       ("← favours PT + DN", "← 有利于干针组"), ("favours control →", "有利于对照组 →"), RED)
    ax2 = panel(720, 200, 930, 1350, -10, 60, (-10, 0, 10, 20, 30, 40, 50, 60), [
        ("6 months · vs PT", "6 个月 · 对比物理治疗组", 34, 14, 55, "+34 (+14 to +55)"),
        ("6 months · vs PT + SDN", "6 个月 · 对比假干针组", 24, 4, 45, "+24 (+4 to +45)"),
        ("1 year · vs PT + SDN", "1 年 · 对比假干针组", 28, 7, 49, "+28 (+7 to +49)"),
    ], ("Secondary outcome: PASS", "次要结局：患者可接受症状状态（PASS）"),
       ("Absolute difference in percentage points of people who call their symptoms acceptable", "认为症状可以接受的人所占比例的绝对差值（百分点）"),
       ("← favours control", "← 有利于对照组"), ("favours PT + DN →", "有利于干针组 →"), RED)

    y = max(ax1, ax2) + 128
    f.path(f"M38,{y - 26} L1362,{y - 26}", "#d8d2c2", 1, rough=False)
    notes = [
        ("Both SPADI intervals include 0: no statistically significant difference on the primary outcome. That is not proof that the groups are equal.", "en"),
        ("SPADI 的两个区间都包含 0：主要结局没有统计学显著差异；这不等于证明两组效果相同。", "zh-CN"),
        ("* As printed: −9.85 lies 9.13 points above the lower limit and 10.58 below the upper limit, so the interval is not centred on the estimate. Kept as printed (see text).", "en"),
        ("* 按原文照录：−9.85 距下限 9.13 分，距上限 10.58 分，区间并不以估计值为中心。数字未改（见正文）。", "zh-CN"),
        ("The three PASS intervals lie above 0, but these are secondary outcomes; whether the authors adjusted for multiple comparisons is not verified.", "en"),
        ("PASS 的三个区间都在 0 以上，但这些是次要结局；作者是否做了多重比较校正尚未核实。", "zh-CN"),
        ("Not plotted: the odds ratio for further shoulder care, 0.35 (95% CI 0.13–0.95), because the abstract does not say which group is the reference.", "en"),
        ("没有画出：再次因肩部就医的比值比 0.35（95% CI 0.13–0.95），因为摘要没有说明参照组是哪一组。", "zh-CN"),
    ]
    for i, (t, lang) in enumerate(notes):
        f.text(38, y + i * 21 + (6 * (i // 2)), t, 14 if lang == "en" else 13, INK if lang == "en" else ZH, "start", "400", lang)
    p = f.save("干针试验效应量")
    foot(p, "Plotted from the numbers reported in the results abstract (PubMed 41476428), via the paper record; nothing estimated.",
         "按结果摘要（PubMed 41476428）报告的数字绘制（取自论文记录），没有自行估算。")


# ------------------------------------------------------------------ 02/03 right glenoid seen from the side, humerus removed
# Clock-style angle t: 0 = top, 90 = front of the body (viewer's right), 180 = bottom, 270 = back.
CX, CY = 700, 560
A0, A1, B = 88, 20, 140          # glenoid half-width A0 + A1*(-cos t): narrower at the top, like a pear
LAB, CAPS, CUFF = 22, 70, 120    # offsets: labrum outer edge, capsule cut edge, cuff tendon outer edge


def P(t, off=0):
    r = math.radians(t)
    a = A0 + A1 * (-math.cos(r))
    return CX + (a + off) * math.sin(r), CY - (B + off) * math.cos(r)


def pts(t1, t2, off, step=3):
    n = max(2, int(abs(t2 - t1) / step) + 1)
    return [P(t1 + (t2 - t1) * k / (n - 1), off) for k in range(n)]


def poly(points):
    return "M" + " L".join(f"{x:.1f},{y:.1f}" for x, y in points) + " Z"


def ring(off):
    return poly(pts(0, 357, off))


def band(t1, t2, o1, o2, u1=None, u2=None):
    """Area between offsets o1 (inner, from t1 to t2) and o2 (outer, from u2 back to u1; defaults to t1, t2)."""
    u1 = t1 if u1 is None else u1
    u2 = t2 if u2 is None else u2
    return poly(pts(t1, t2, o1) + pts(u2, u1, o2))


CUFF_FILL = {"supra": "#f1d3cc", "infra": "#d6e1ef", "teres": "#d9ebd5", "subsc": "#e6dcf2"}
CUFF_T = {"supra": (322, 8), "infra": (268, 318), "teres": (230, 264), "subsc": (56, 140)}
CAPS_FILL, CAPS_E = "#d5e9e9", TEAL
LIG_FILL, LIG_E = "#efc1b6", RED
CHL_FILL, CHL_E = "#f2dc9e", GOLD
CAL_FILL, CAL_E = "#cfe3c5", GREEN
LHB_FILL, LHB_E = "#e5cba8", "#8a5a2b"
LAB_FILL, LAB_E = "#bcd0e8", BLUE


def glenoid_face(f):
    # scapula seen edge-on: the body runs down from the glenoid (cut); spine and coracoid base lie deeper, not drawn
    f.path("M640,690 C650,760 676,860 682,950 L716,950 C722,860 748,760 760,690 Z", BONE_E, 2.2, BONE)
    f.path("M682,950 L716,950", MUTE, 1.4, dash="4 4", rough=False)
    # acromion (back, top) and coracoid process (front, top)
    f.path("M500,214 C532,192 612,186 664,204 C682,214 678,246 660,262 C612,284 556,290 520,280 C490,270 484,236 500,214 Z", BONE_E, 2.2, BONE)
    f.path("M792,262 C800,236 840,226 880,234 C930,246 970,270 990,298 C1000,314 990,334 970,332 C934,326 890,316 852,314 C820,312 796,300 792,262 Z", BONE_E, 2.2, BONE)
    # coracoacromial ligament: the roof above the cuff
    f.path("M900,262 Q772,214 650,240", CAL_E, 22, rough=False)
    f.path("M900,262 Q772,214 650,240", CAL_FILL, 17, rough=False)
    # cuff tendons cut close to the joint (outside the capsule)
    for k, (t1, t2) in CUFF_T.items():
        f.path(band(t1, t2 if t2 > t1 else t2 + 360, CAPS, CUFF), GREY, 1.6, CUFF_FILL[k], rough=False)
    # rotator interval: the gap between supraspinatus and subscapularis
    f.path(band(10, 54, CAPS + 2, CUFF - 2), MUTE, 1.4, "none", dash="3 4", rough=False)
    # capsule, cut short: a sleeve seen end-on
    f.path(ring(CAPS), CAPS_E, 2.2, CAPS_FILL, rough=False)
    f.path(band(126, 226, LAB, CAPS), "none", 0, "#b9dadb", rough=False)            # axillary pouch, the lowest part
    # glenohumeral ligaments: thickenings of the front and bottom of the capsule
    for t1, t2, u1, u2 in ((16, 26, 20, 30), (44, 57, 74, 88), (94, 118, 100, 124), (234, 256, 230, 252)):
        f.path(band(t1, t2, LAB - 2, CAPS - 1, u1, u2), LIG_E, 1.8, LIG_FILL, rough=False)
    # labrum and glenoid cavity
    f.path(ring(LAB), LAB_E, 1.8, LAB_FILL, rough=False)
    f.path(ring(0), "#7f95ab", 1.6, "#eef2f5", rough=False)
    # long head of biceps from the top of the labrum, cut where it leaves the joint
    x1, y1 = P(2, -6)
    x2, y2 = P(12, 52)
    f.path(f"M{x1:.1f},{y1:.1f} L{x2:.1f},{y2:.1f}", LHB_E, 18, rough=False)
    f.path(f"M{x1:.1f},{y1:.1f} L{x2:.1f},{y2:.1f}", LHB_FILL, 13, rough=False)
    f.raw(f'<ellipse cx="{x2:.1f}" cy="{y2:.1f}" rx="10" ry="6" fill="{LHB_FILL}" stroke="{LHB_E}" stroke-width="1.6" transform="rotate(14 {x2:.1f} {y2:.1f})"/>')
    # coracohumeral ligament: from the base of the coracoid into the rotator interval, cut
    cx, cy = P(34, 100)
    f.raw(f'<path d="M800,296 L832,312 L{cx + 12:.1f},{cy + 4:.1f} L{cx - 12:.1f},{cy - 4:.1f} Z" fill="{CHL_FILL}" stroke="{CHL_E}" stroke-width="1.8" stroke-linejoin="round"/>')


# label rows: (letter, en, zh, side, y, anchor); letter None = orientation label kept on the self-test figure
GLENOID_LABELS = [
    (None, "Acromion", "肩峰", "L", 226, (560, 240)),
    (None, "Supraspinatus tendon (cut)", "冈上肌腱（切断）", "L", 300, P(345, 95)),
    ("H", "Long head of biceps tendon", "肱二头肌长头腱", "L", 374, P(7, 22)),
    (None, "Infraspinatus tendon (cut)", "冈下肌腱（切断）", "L", 452, P(292, 95)),
    ("I", "Glenoid labrum", "盂唇", "L", 530, P(272, 11)),
    ("E", "Inferior glenohumeral ligament, posterior band", "盂肱下韧带后束", "L", 624, P(243, 40)),
    (None, "Teres minor tendon (cut)", "小圆肌腱（切断）", "L", 712, P(244, 100)),
    ("D", "Axillary pouch (inferior capsule)", "腋囊（关节囊下部）", "L", 806, P(196, 46)),
    ("G", "Coracoacromial ligament", "喙肩韧带", "T", 160, (772, 238)),
    (None, "Coracoid process", "喙突", "R", 290, (976, 306)),
    ("F", "Coracohumeral ligament", "喙肱韧带", "R", 346, (806, 333)),
    ("K", "Rotator interval", "肩袖间隙", "R", 398, P(46, 104)),
    ("A", "Superior glenohumeral ligament", "盂肱上韧带", "R", 452, P(21, 44)),
    ("B", "Middle glenohumeral ligament", "盂肱中韧带", "R", 506, P(66, 50)),
    ("J", "Joint capsule (cut edge)", "关节囊（切缘）", "R", 556, P(93, 69)),
    (None, "Subscapularis tendon (cut)", "肩胛下肌腱（切断）", "R", 606, P(100, 104)),
    ("C", "Inferior glenohumeral ligament, anterior band", "盂肱下韧带前束", "R", 676, P(108, 46)),
    (None, "Body of the scapula (cut)", "肩胛骨体（切断）", "R", 880, (700, 880)),
]


def put_labels(f, labels, lx, rx, letters):
    for letter, en, zh, side, y, (ax, ay) in labels:
        quiz = letters and letter
        if side == "L":
            tx, anchor, sx = lx, "end", lx + 8
        elif side == "R":
            tx, anchor, sx = rx, "start", rx - 8
        else:
            tx, anchor, sx = ax, "middle", ax
        sy = y - 5 if side != "T" else y + 26
        f.leader(sx, sy, ax, ay, "#555")
        f.circle(ax, ay, 3.2, INK, "#fff", 1)
        if quiz:
            cx = tx - 16 if side == "L" else (tx + 16 if side == "R" else tx)
            cy = y - 5 if side != "T" else y + 6
            f.circle(cx, cy, 16, "#fff", INK, 2)
            f.text(cx, cy + 6, letter, 17, INK, "middle", "700")
        else:
            f.bi(tx, y, en, zh, 15, INK if letter else MUTE, anchor, "700" if letter else "600", gap=19, zsize=13)


def f02(letters=False):
    if letters:
        f = Fig("03", 1400, 1000, "Self-test: name the lettered structures", "自测：说出每个字母指的结构")
    else:
        f = Fig("02", 1400, 1000, "Right glenoid from the side: labrum, capsule and ligaments", "右侧关节盂外侧面观：盂唇、关节囊与韧带")
    f.bi(38, 116, "Looking into the right socket from the side, humerus removed. Front of the body on the right, top of the shoulder at the top.",
         "从外侧看进右侧关节盂（肱骨已移除）。身体前方在右边，肩顶在上方。", 15, MUTE, weight="400")
    glenoid_face(f)
    f.bi(CX, CY - 4, "Glenoid cavity", "关节盂", 15, MUTE, "middle", "600", gap=19, zsize=13)
    put_labels(f, GLENOID_LABELS, 462, 1010, letters)
    p = f.save("盂肱关节囊与韧带-看图标注" if letters else "盂肱关节囊与韧带外侧面观")
    foot(p, "Schematic: the capsule and cuff tendons are cut close to the glenoid; sizes and band widths are simplified.",
         "示意图：关节囊和肩袖肌腱在靠近关节盂处切断；大小和韧带宽度经过简化。")


# ------------------------------------------------------------------ 04 right shoulder from the front: the capsule as a sleeve
# Head: centre (400,360), radius 80; the anatomical neck runs from (343,303) to (440,429).
HUM = ("M305,296 C290,300 282,318 281,345 C280,380 290,420 298,460 C304,520 306,620 306,856 L370,856 "
       "C370,640 371,540 378,500 C384,470 404,448 440,429 A80,80 0 1 0 343.4,303.4 C330,298 316,295 305,296 Z")
SCAPULA = "M494,296 C500,286 520,280 540,278 L664,268 L652,420 L600,640 L572,640 C556,560 530,490 500,440 C506,392 506,340 494,296 Z"
CAPSULE = ("M508,290 C470,262 390,262 343,303 C360,350 395,400 440,429 C446,470 456,500 474,502 "
           "C496,504 510,476 512,442 C514,392 514,336 508,290 Z")


def f04():
    f = Fig("04", 1400, 1000, "Right shoulder from the front: the capsule as a sleeve", "右肩前面观：像袖套一样的关节囊")
    f.bi(38, 116, "Front view, arm by the side. The humerus is on the viewer's left; the scapula (cut) is on the right.",
         "前面观，手臂垂在体侧。肱骨在左边，肩胛骨（切断）在右边。", 15, MUTE, weight="400")
    f.g("translate(170,80)")
    f.path(SCAPULA, BONE_E, 2.2, BONE)
    f.path("M664,268 L652,420 L600,640", BONE, 4, rough=False)
    f.path("M664,268 L652,420 L600,640", MUTE, 1.4, dash="4 4", rough=False)
    f.path("M535,280 C534,262 536,248 540,240 C520,236 498,234 480,231 C462,228 458,210 474,205 "
           "C508,198 548,194 570,196 C582,204 586,240 580,278 Z", BONE_E, 2.2, BONE)                        # coracoid process
    f.path("M258,196 C310,182 370,180 418,188 C430,196 428,216 414,222 C366,226 310,228 266,226 C250,220 248,204 258,196 Z",
           BONE_E, 2.2, BONE)                                                                                 # acromion
    f.path(HUM, BONE_E, 2.2, BONE)
    f.path("M338,318 C356,322 364,342 358,372", BONE_E, 1.4, rough=False)                                    # lesser tubercle
    f.path("M318,312 C317,370 318,430 320,500 M334,316 C334,372 335,430 336,500", BONE_E, 1.2, rough=False)  # lips of the groove
    f.path("M343,303 C360,350 395,400 440,429", BONE_E, 1.8, dash="3 4", rough=False)                        # anatomical neck
    f.path("M492,298 C504,340 504,390 494,430", LAB_E, 10, rough=False)
    f.path("M492,298 C504,340 504,390 494,430", LAB_FILL, 6, rough=False)                                    # labrum
    f.path("M500,288 C470,266 390,266 326,312", LHB_E, 7, dash="9 6", rough=False)                            # biceps tendon inside the joint
    f.path("M326,312 C325,390 327,470 330,620", LHB_E, 11, rough=False)
    f.path("M326,312 C325,390 327,470 330,620", LHB_FILL, 7, rough=False)                                    # ... and in the groove
    f.raw(f'<path d="{CAPSULE}" fill="{CAPS_FILL}" fill-opacity="0.32" stroke="{CAPS_E}" stroke-width="2.2" stroke-linejoin="round"/>')
    f.raw(f'<path d="M440,429 A80,80 0 1 0 343.4,303.4" fill="none" stroke="{BONE_E}" stroke-width="1.6" opacity="0.55"/>')   # head seen through the capsule
    f.raw(f'<rect x="309" y="346" width="36" height="16" rx="4" fill="#ddd0ee" stroke="{PURP}" stroke-width="1.8"/>')   # transverse humeral ligament
    f.raw(f'<path d="M536,244 C470,250 380,262 305,294 L342,318 C410,292 480,276 536,268 Z" fill="{CHL_FILL}" fill-opacity="0.8" '
          f'stroke="{CHL_E}" stroke-width="1.8" stroke-linejoin="round"/>')                                    # coracohumeral ligament
    f.path("M492,234 L420,212", CAL_E, 14, rough=False)
    f.path("M492,234 L420,212", CAL_FILL, 10, rough=False)                                                   # coracoacromial ligament
    f.bi(428, 352, "Humeral head", "肱骨头", 14, MUTE, "middle", "600", gap=18, zsize=12)
    labels = [
        ("Acromion", "肩峰", "L", 214, (300, 212)),
        ("Coracohumeral ligament (to both tubercles)", "喙肱韧带（到大、小结节）", "L", 272, (318, 292)),
        ("Greater tubercle", "大结节", "L", 350, (290, 352)),
        ("Transverse humeral ligament (over the groove)", "肱横韧带（跨过结节间沟）", "L", 426, (327, 356)),
        ("Long head of biceps tendon", "肱二头肌长头腱", "L", 564, (328, 562)),
        ("Coracoacromial ligament", "喙肩韧带", "T", 78, (452, 223)),
        ("Coracoid process", "喙突", "R", 204, (572, 214)),
        ("Glenoid labrum", "盂唇", "R", 300, (500, 316)),
        ("Joint capsule (see-through)", "关节囊（画成透明）", "R", 392, (512, 394)),
        ("Scapula (cut)", "肩胛骨（切断）", "R", 470, (610, 470)),
        ("Axillary pouch: slack with the arm by the side", "腋囊：手臂垂在体侧时松弛", "R", 548, (478, 500)),
    ]
    for en, zh, side, y, (ax, ay) in labels:
        tx, anchor, sx = {"L": (200, "end", 208), "R": (740, "start", 732), "T": (ax, "middle", ax)}[side]
        sy = y - 5 if side != "T" else y + 26
        f.leader(sx, sy, ax, ay, "#555")
        f.circle(ax, ay, 3.2, INK, "#fff", 1)
        f.bi(tx, y, en, zh, 15, INK, anchor, "600", gap=19, zsize=13)
    f.leader(398, 680, 418, 414, "#555")                                                                   # anatomical neck, from below
    f.circle(418, 414, 3.2, INK, "#fff", 1)
    f.bi(404, 698, "Anatomical neck: the capsule attaches here", "解剖颈：关节囊在肱骨上的附着处", 15, INK, "start", "600", gap=19, zsize=13)
    f.end()
    p = f.save("盂肱关节囊前面观")
    foot(p, "Schematic: the capsule is drawn see-through, and the glenohumeral ligaments (thickenings of its front and lower parts) are not drawn.",
         "示意图：关节囊画成透明；关节囊前部和下部增厚形成的盂肱韧带没有画出。")


def build(out_dir):
    set_out(out_dir)
    f01()
    f02()
    f02(letters=True)
    f04()


if __name__ == "__main__":
    build(sys.argv[1] if len(sys.argv) > 1 else "资源")
