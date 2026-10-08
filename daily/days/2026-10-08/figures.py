#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Day 2 (2026-10-08) figures: serratus anterior + trapezius, lung meridian LU7–LU11 and LI1.
Run via pipeline (figures step) or: python3 figures.py <out_dir>."""
import math, sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2]))
from engine.figlib import *
from engine.figlib import posterior as P, thorax_lateral as TL, hand as H

TRAP_E = {"up": RED, "mid": "#a0522d", "low": "#8f4a3c"}
SA_C = "#b4664d"
LI_C = "#2b6c7c"


def marker(f, x, y, txt, col, r=15, size=16):
    f.circle(x, y, r, col, "#fff", 2.6)
    f.text(x, y + size * 0.36, txt, size, "#fff", "middle", "700")


# ------------------------------------------------------------------ 01 overview
def f01():
    f = Fig("01", 1400, 900, "Today's two scapular muscles", "今天的两块肩胛骨肌肉：斜方肌与前锯肌")
    f.bi(270, 128, "A · Trapezius, posterior view", "A · 斜方肌，后面观", 17, RED, "middle")
    f.bi(940, 128, "B · Serratus anterior, right lateral view", "B · 前锯肌，右侧面观（已移去上肢）", 17, SA_C, "middle")
    S, X0, Y0 = 0.6, -132, 200
    f.g(f"translate({X0},{Y0}) scale({S})"); P.posterior_base(f, labels=False); P.trapezius(f); f.end()
    p = lambda x, y: (X0 + S * x, Y0 + S * y)
    for lv in ("C7", "T4", "T12"):
        x, y = p(P.MID - 20, P.sp_y(lv) + 5); f.text(x, y, lv, 13, "#6b6458", "end", "700")
    for (px, py), (lx, ly), en, zh, c in [((780, 250), (505, 300), "Upper (descending) part", "上部（降部）", TRAP_E["up"]),
                                          ((760, 395), (505, 400), "Middle (transverse) part", "中部（横部）", TRAP_E["mid"]),
                                          ((690, 560), (505, 610), "Lower (ascending) part", "下部（升部）", TRAP_E["low"]),
                                          ((870, 400), (505, 500), "Spine of scapula", "肩胛冈", INK)]:
        X, Y = p(px, py); f.leader(X, Y, lx - 6, ly - 5, c); f.bi(lx, ly, en, zh, 14, c)
    S2, X1, Y1 = 0.62, 560, 150
    f.g(f"translate({X1},{Y1}) scale({S2})"); TL.thorax_lateral_base(f, scap=False, nums=False); pts = TL.serratus(f)
    f.path(TL.SCAP_LAT, "#6b6458", 1.8, "#efe6d4", dash="7 5", op=0.55); f.end()
    q = lambda x, y: (X1 + S2 * x, Y1 + S2 * y)
    for k in (1, 4, 8):
        x, y = q(*TL.rib_pts(k)[0]); f.text(x - 8, y + 4, f"{k}", 12, "#8a7f6c", "end", "700")
    for pt, (lx, ly), en, zh, c in [(TL.rib_point(2, 0.78), (1150, 300), "Serratus anterior: 8 digitations", "前锯肌：8 个肌齿", SA_C),
                                          ((572, 300), (1150, 220), "Scapula (see-through)", "肩胛骨（透视）", "#6b6458"),
                                          ((548, 420), (1150, 420), "Long thoracic nerve", "胸长神经", "#9a7414"),
                                          (TL.rib_point(6, 0.95), (1150, 520), "Ribs 1–8 (outer surfaces)", "第 1–8 肋外面", "#8a7f6c")]:
        X, Y = q(*pt)
        f.leader(X, Y, lx - 6, ly - 5, c); f.bi(lx, ly, en, zh, 14, c)
    f.text(q(250, 0)[0], 196, "← Back 后", 13, "#777", "middle")
    f.text(q(1010, 0)[0] - 40, 196, "Front 前 →", 13, "#777", "middle")
    f.bi(40, 820, "Both muscles move the scapula, not the humerus: they set the shoulder blade so the arm can rise.",
         "这两块肌肉都作用于肩胛骨而不是肱骨：它们摆好肩胛骨，手臂才能上举。", 15, INK)
    f.save("今日两块肌肉总览")


# ------------------------------------------------------------------ 02 serratus O/I
def f02():
    f = Fig("02", 760, 1000, "Serratus anterior: origin and insertion", "前锯肌：起点与止点")
    S = 1.2; X0, Y0 = 40 - 330 * S, 150 - 170 * S
    f.raw(f'<clipPath id="{f.id("crop")}"><rect x="330" y="170" width="575" height="540"/></clipPath>')
    f.g(f"translate({X0:.1f},{Y0:.1f}) scale({S})"); f.raw(f'<g clip-path="url(#{f.id("crop")})">')
    TL.thorax_lateral_base(f, scap=False); pts = TL.serratus(f, nerve=False)
    f.path(TL.SCAP_LAT, "#6b6458", 1.8, "#efe6d4", dash="7 5", op=0.5)
    f.end(); f.end()
    P_ = lambda x, y: (X0 + S * x, Y0 + S * y)
    ins = {1: TL.medial_border(0.03), 4: TL.medial_border(0.46), 8: TL.medial_border(0.97)}
    for k in (1, 4, 8):
        ox, oy = P_(*pts[k][0]); ix, iy = P_(*ins[k])
        f.path(f"M{ox:.0f},{oy:.0f} Q{(ox + ix) / 2:.0f},{min(oy, iy) - 40:.0f} {ix:.0f},{iy:.0f}", INK, 2.2, dash="8 6", rough=False)
    for k in (1, 4, 8):
        ox, oy = P_(*pts[k][0]); marker(f, ox, oy, "O", SA_C, 17, 19)
    for k in (1, 4, 8):
        ix, iy = P_(*ins[k]); marker(f, ix, iy, "I", INK, 18, 20)
    f.bi(38, 124, "Dashed line = attachment order, not force · grey numbers = ribs", "虚线 = 起点 → 止点的附着顺序，不是受力方向；灰色数字 = 肋骨序号", 16, "#666", weight="400", zsize=15)
    f.text(600, 186, "Front 前 →", 15, "#777", "middle")
    f.bi(38, 838, "O = Origin: outer surfaces of ribs 1–8", "起点：第 1–8 肋外面（部分教材为 1–9）", 21, SA_C, gap=28, zsize=20)
    f.bi(38, 906, "I = Insertion: costal surface of the medial border", "止点：肩胛骨内侧缘的肋面（上角 → 下角）", 21, INK, gap=28, zsize=20)
    f.save("前锯肌起止点")


# ------------------------------------------------------------------ 03 trapezius O/I
def f03():
    f = Fig("03", 760, 1060, "Trapezius: origin and insertion", "斜方肌：起点与止点")
    S = 1.02; X0, Y0 = 70 - 608 * S, 150 - 70 * S
    f.raw(f'<clipPath id="{f.id("crop")}"><rect x="608" y="70" width="410" height="720"/></clipPath>')
    f.g(f"translate({X0:.1f},{Y0:.1f}) scale({S})"); f.raw(f'<g clip-path="url(#{f.id("crop")})">')
    P.posterior_base(f, labels=False); P.trapezius(f, left_op=0.0)
    f.end(); f.end()
    p = lambda x, y: (X0 + S * x, Y0 + S * y)
    for lv in ("C7", "T4", "T12"):
        x, y = p(P.MID + 22, P.sp_y(lv) + 5); f.text(x, y, lv, 15, "#6b6458", "start", "700")
    O = [((650, 140), "up"), ((650, 250), "up"), ((650, P.sp_y("T2")), "mid"), ((650, P.sp_y("T7")), "low"), ((650, P.sp_y("T12") - 6), "low")]
    I = [((872, 346), "up"), ((952, 370), "mid"), ((812, 424), "mid"), ((760, 452), "low")]
    for (o, ko), (i, ki) in [(O[0], I[0]), (O[2], I[1]), (O[2], I[2]), (O[3], I[3])]:
        (ox, oy), (ix, iy) = p(*o), p(*i)
        f.path(f"M{ox:.0f},{oy:.0f} Q{(ox + ix) / 2:.0f},{min(oy, iy) - 30:.0f} {ix:.0f},{iy:.0f}", INK, 2, dash="8 6", rough=False)
    for o, k in O:
        x, y = p(*o); marker(f, x, y, "O", TRAP_E[k], 15, 17)
    for i, k in I:
        x, y = p(*i); marker(f, x, y, "I", INK, 16, 18)
    f.bi(38, 124, "Colours: upper · middle · lower parts", "颜色：上部 · 中部 · 下部", 16, "#666", weight="400", zsize=15)
    f.bi(38, 880, "O = Origin: occiput (EOP, superior nuchal line), nuchal ligament, C7–T12", "起点：枕外隆凸、上项线内 1/3、项韧带、C7–T12 棘突", 19, RED, gap=27, zsize=18)
    f.bi(38, 950, "I = Insertion: lateral ⅓ clavicle · acromion · spine of scapula", "止点：上部→锁骨外 1/3；中部→肩峰、肩胛冈上缘；下部→冈根", 19, INK, gap=27, zsize=18)
    f.save("斜方肌起止点")


# ------------------------------------------------------------------ 04 nerves
def f04():
    f = Fig("04", 1340, 900, "Nerves: long thoracic nerve and spinal accessory nerve", "神经：胸长神经与副神经")
    f.box(38, 96, 600, 64, "#cfd8cc", "#eef3ec")
    f.text(54, 122, "C = Cervical 颈部 · CN XI = cranial nerve 11 第 11 对脑神经", 15, INK, weight="700", lang="zh-CN")
    f.text(54, 146, "Grey blocks are vertebrae; numbers on lines are spinal nerves. 灰块为椎骨，线上的号为脊神经。", 13, "#444", lang="zh-CN")
    # ---- A long thoracic nerve: from the roots
    f.bi(330, 200, "A · Long thoracic nerve (C5–C7) → serratus anterior", "A · 胸长神经（C5–C7）→ 前锯肌", 16, "#9a7414", "middle")
    verts = {"C4": 250, "C5": 310, "C6": 370, "C7": 430, "T1": 490}
    f.path("M95,230 L95,520", "#d9d2bf", 22, rough=False)
    for n, cy in verts.items():
        f.raw(f'<rect x="62" y="{cy - 22}" width="86" height="44" rx="11" fill="#e6e1d3" stroke="{BONE_E}" stroke-width="1.8"/>')
        f.text(105, cy + 6, f"{n} vertebra", 12, INK, "middle", "700")
    roots = {"C5": 280, "C6": 340, "C7": 400}
    for r, y in roots.items():
        f.path(f"M150,{y} L250,{y}", BLUE, 4); f.text(160, y - 8, f"{r} nerve", 13, INK, weight="700")
    f.path("M250,280 L420,286 M250,340 L420,330", "#c8cfdc", 3, rough=False)                     # plexus continues (faint)
    f.text(428, 300, "→ trunks of the brachial plexus 臂丛各干", 12, "#8a94a6", lang="zh-CN")
    f.path("M232,280 C250,320 262,360 266,402 M232,340 C246,360 256,380 266,402 M240,400 L266,402", "#9a7414", 3.2)
    f.path("M266,402 C276,470 300,540 320,610 C332,660 340,720 346,790", "#9a7414", 4)
    for k, y in enumerate(range(560, 800, 34)):
        f.path(f"M{360 - k},{y} C{390},{y - 6} {430},{y + 4} {470},{y + 14}", "#ecb9a4", 16, rough=False, op=0.85)
    f.path("M266,402 C276,470 300,540 320,610 C332,660 340,720 346,790", "#9a7414", 4)
    for y in range(570, 790, 34):
        x = 300 + (y - 540) * 0.2
        f.path(f"M{x + 16:.0f},{y} L{x + 44:.0f},{y + 6}", "#9a7414", 1.6, rough=False)
    f.bi(500, 600, "Serratus anterior", "前锯肌肌齿", 13, SA_C, weight="600")
    f.leader(496, 596, 470, 610, SA_C)
    f.bi(40, 580, "Arises from the roots,", "直接起自神经根，", 13, "#9a7414", weight="600")
    f.bi(40, 622, "before the trunks form", "在形成干之前", 13, "#9a7414", weight="600")
    f.leader(170, 600, 268, 470, "#9a7414")
    f.bi(500, 700, "Runs down the mid-axillary line on", "沿腋中线走在前锯肌浅面，", 13, INK, weight="400")
    f.bi(500, 742, "the muscle's surface: exposed, easily hurt", "位置表浅，容易受伤", 13, INK, weight="400")
    # ---- B spinal accessory nerve: from the upper cervical cord (lateral neck, front = right)
    f.bi(1000, 190, "B · Spinal accessory nerve (CN XI) → trapezius", "B · 副神经（CN XI）→ 斜方肌", 16, RED, "middle")
    f.raw('<rect x="682" y="262" width="26" height="250" rx="12" fill="#f3ead2" stroke="#b9ab94" stroke-width="1.4"/>')   # cervical cord
    for k, y in enumerate(range(290, 512, 48)):
        f.path(f"M668,{y} L682,{y}", "#b9ab94", 1.2, rough=False); f.text(664, y + 4, f"C{k + 1}", 11, "#8a7f6c", "end", "700")
    f.bi(712, 542, "Upper cervical cord C1–C5", "颈髓上段 C1–C5（副神经脊髓核）", 12, "#6b6458", "end", "600")
    f.path("M700,262 C698,252 694,244 686,240", "#8a7f6c", 1.4, rough=False)
    f.text(680, 244, "Foramen magnum 枕骨大孔", 11, "#6b6458", "end", lang="zh-CN")
    f.path("M750,262 C820,244 900,240 960,248 C1020,256 1070,272 1100,296", "#9a958a", 2, rough=False)               # skull base
    f.raw('<ellipse cx="968" cy="282" rx="18" ry="28" fill="#f1e9da" stroke="#9a958a" stroke-width="1.6"/>')          # mastoid
    f.path("M800,262 C820,380 870,500 930,640 L736,640 L736,262 Z", RED, 1.6, "#f0c2b6", op=0.7)                    # trapezius
    f.bi(748, 596, "Trapezius", "斜方肌", 13, RED, weight="600")
    f.path("M958,300 C1006,392 1086,520 1170,640 L1222,616 C1136,500 1046,370 986,290 Z", "#8c6b52", 1.4, "#e7c8b0", op=0.85)  # SCM
    f.bi(1150, 470, "Sternocleidomastoid", "胸锁乳突肌", 13, "#8c6b52", weight="600")
    f.path("M930,640 C890,540 850,430 818,320 C870,330 920,326 962,312 C1010,420 1070,540 1130,640 Z", "none", 0, "#fbe3a0", op=0.4)
    f.bi(1000, 600, "Posterior triangle", "颈后三角", 13, "#9a7414", "middle", "600")
    f.path("M800,650 L1230,650", BONE_E, 10, rough=False, op=0.35); f.text(1230, 678, "Clavicle 锁骨", 12, "#6b6458", "end", lang="zh-CN")
    f.path("M695,330 C696,290 700,250 716,236 C760,222 880,224 950,240", RED, 3, dash="6 5")                           # up through foramen magnum, out of the jugular foramen
    f.path("M950,240 C962,270 970,300 976,340", RED, 3.4, dash="7 5")                                                 # deep to SCM
    f.path("M976,340 C970,372 952,400 928,430 C904,462 884,488 868,512", RED, 3.6)                                    # across the triangle
    f.path("M868,512 C850,560 834,604 818,660 C808,700 798,740 790,790", RED, 3.4, dash="7 5")                         # on the deep surface of trapezius
    f.circle(950, 240, 6, RED, "#fff", 2)
    f.leader(956, 236, 1040, 226, "#a8a294"); f.text(1046, 230, "Jugular foramen 颈静脉孔", 12, "#6b6458", lang="zh-CN")
    f.path("M996,380 C978,392 960,410 938,426", "#7a5aa6", 2.4, dash="3 4", rough=False)
    f.path("M1010,410 C990,430 966,456 912,468", "#7a5aa6", 2.4, dash="3 4", rough=False)
    f.text(1002, 376, "C3", 13, "#7a5aa6", weight="700"); f.text(1016, 410, "C4", 13, "#7a5aa6", weight="700")
    f.bi(1070, 360, "Superficial here: a lymph-node", "此段表浅：颈部淋巴结", 13, RED, weight="600")
    f.bi(1070, 402 - 2, "biopsy can cut it", "活检时易误伤", 13, RED, weight="600")
    f.leader(1066, 372, 940, 412, RED)
    f.bi(840, 730, "Then runs on the deep surface", "随后在斜方肌深面下行（虚线）", 13, INK, weight="400")
    f.bi(840, 772, "of trapezius (dashed)", "", 13, INK, weight="400")
    f.bi(1060, 720, "C3–C4 ventral rami join it:", "C3–C4 前支加入：", 13, "#7a5aa6", weight="600")
    f.bi(1060, 762, "sensory / proprioceptive", "感觉 / 本体感觉纤维", 13, "#7a5aa6", weight="400")
    f.save("胸长神经与副神经")


# ------------------------------------------------------------------ 05 upward rotation force couple
SCAP_GROUP = (P.SCAP_R, P.SPINE_R, P.ACROM_R)


def scapula(f, tr="", op=1.0, dash=None):
    f.g(tr)
    for d, fill in zip(SCAP_GROUP, (BONE, "#efe5cf", BONE)):
        f.path(d, BONE_E if not dash else "#9a958a", 2, fill if not dash else "none", dash=dash, op=op)
    f.end()


def f05():
    f = Fig("05", 1360, 900, "Upward rotation: a force couple", "上回旋：三股力组成的力偶（右肩胛骨，后面观）")
    f.bi(330, 128, "A · Three pulls, one rotation", "A · 三股拉力，合成一个转动", 16, INK, "middle")
    S = 1.15; X0, Y0 = 110 - 650 * S, 260 - 340 * S
    f.g(f"translate({X0:.1f},{Y0:.1f}) scale({S})")
    for k in range(1, 10):
        y = P.sp_y(f"T{k}")
        f.raw(f'<rect x="{P.MID - 13}" y="{y - 8}" width="26" height="16" rx="5" fill="{BONE}" stroke="{BONE_E}" stroke-width="1.2"/>')
    scapula(f)
    f.end()
    p = lambda x, y: (X0 + S * x, Y0 + S * y)
    for lv in ("T2", "T4", "T7"):
        x, y = p(P.MID - 20, P.sp_y(lv) + 5); f.text(x, y, lv, 13, "#6b6458", "end", "700")
    a, b, c = p(930, 366), p(756, 452), p(786, 600)
    f.arrow(f"M{a[0]:.0f},{a[1]:.0f} L{a[0] - 110:.0f},{a[1] - 100:.0f}", TRAP_E["up"], 6)
    f.arrow(f"M{b[0]:.0f},{b[1]:.0f} L{b[0] - 60:.0f},{b[1] + 120:.0f}", TRAP_E["low"], 6)
    f.arrow(f"M{c[0]:.0f},{c[1]:.0f} L{c[0] + 150:.0f},{c[1] + 14:.0f}", SA_C, 6)
    f.bi(a[0] - 28, a[1] - 92, "Upper trapezius:", "斜方肌上部：把肩峰拉向内上", 15, TRAP_E["up"])
    f.bi(a[0] - 28, a[1] - 92 + 44, "pulls the acromion up and in", "", 14, TRAP_E["up"], weight="600")
    f.bi(40, b[1] + 300, "Lower trapezius: pulls the root of the spine down", "斜方肌下部：把冈根拉向下", 15, TRAP_E["low"])
    f.leader(140, b[1] + 282, b[0] - 60, b[1] + 128, TRAP_E["low"])
    f.bi(c[0] + 170, c[1] + 20, "Serratus anterior (lower part):", "前锯肌下部：把下角拉向外、向前", 15, SA_C)
    f.bi(c[0] + 170, c[1] + 64, "pulls the inferior angle out and forward", "", 14, SA_C, weight="600")
    cx, cy, r = p(830, 470)[0], p(830, 470)[1], 175
    a1, a2 = math.radians(115), math.radians(-35)
    f.arrow(f"M{cx + r * math.cos(a1):.0f},{cy + r * math.sin(a1):.0f} A{r},{r} 0 0 0 {cx + r * math.cos(a2):.0f},{cy + r * math.sin(a2):.0f}", "#2b6c7c", 4)
    f.bi(cx + r * math.cos(a2) + 58, cy + r * math.sin(a2) + 8, "Result: upward rotation", "合力：上回旋（关节盂转向上）", 16, "#2b6c7c")
    # ---- B: who works when (qualitative)
    bx, by, bw = 760, 220, 540
    f.bi(bx, 128, "B · Who drives it during arm elevation", "B · 抬臂过程中由谁主导（定性示意，不是肌电数值）", 16, INK)
    rows = [("Serratus anterior 前锯肌", SA_C, [(0, 1, 0.95)]),
            ("Upper trapezius 斜方肌上部", TRAP_E["up"], [(0, 0.5, 0.95), (0.5, 1, 0.4)]),
            ("Lower trapezius 斜方肌下部", TRAP_E["low"], [(0, 0.5, 0.35), (0.5, 1, 0.95)]),
            ("Middle trapezius 斜方肌中部", TRAP_E["mid"], [(0, 1, 0.45)])]
    for r_, (lab, col, segs) in enumerate(rows):
        y = by + r_ * 56
        f.text(bx, y - 6, lab, 13, col, weight="700", lang="zh-CN")
        for a0, a1_, o in segs:
            f.raw(f'<rect x="{bx + a0 * bw:.0f}" y="{y}" width="{(a1_ - a0) * bw:.0f}" height="16" rx="5" fill="{col}" opacity="{o}"/>')
    ay = by + 250
    f.path(f"M{bx},{ay} L{bx + bw},{ay}", INK, 1.6, rough=False)
    for k, lab in enumerate(["0°", "90°", "180°"]):
        x = bx + k * bw / 2
        f.path(f"M{x},{ay - 6} L{x},{ay + 6}", INK, 1.4, rough=False); f.text(x, ay + 26, lab, 13, "#555", "middle")
    f.text(bx + bw / 2, ay + 50, "Arm elevation · 上肢上举", 13, "#555", "middle", lang="zh-CN")
    f.bi(bx, ay + 100, "Axis: near the SC joint early; it moves to the AC joint", "轴：早期在胸锁关节附近；肋锁韧带拉紧后", 14, INK, weight="400")
    f.bi(bx, ay + 142, "once the costoclavicular ligament is taut.", "移到肩锁关节。", 14, INK, weight="400")
    f.bi(bx, ay + 196, "Upper trapezius + SA early → lower trapezius + SA late.", "早期：斜方肌上部 + 前锯肌；后期：斜方肌下部 + 前锯肌。", 14, "#2b6c7c")
    f.bi(bx, ay + 250, "Opposing downward rotators (levator scapulae, rhomboids)", "对抗的下回旋肌（肩胛提肌、菱形肌，明天学）", 14, INK, weight="400")
    f.bi(bx, ay + 292, "lengthen under control.", "被控制地拉长。", 14, INK, weight="400")
    f.bi(40, 820, "Middle trapezius balances serratus protraction, so the scapula turns instead of sliding forward.",
         "斜方肌中部平衡前锯肌的前伸，让肩胛骨原地转动而不向前滑。", 14, INK, weight="400")
    f.save("上回旋力偶")


# ------------------------------------------------------------------ 06 scapular winging
def f06():
    f = Fig("06", 1300, 780, "Scapular winging: which nerve, which muscle", "翼状肩胛：哪条神经、哪块肌肉（右侧，后面观）")
    for i, (title, sub, col, dx, dy, ang, en, zh) in enumerate([
            ("A · Medial winging", "A · 内侧型翼状肩胛", SA_C, 0, -36, 9,
             ["Long thoracic nerve → serratus anterior weak", "Scapula moves UP; inferior angle turns toward the midline", "Medial border lifts off the ribs; worst in a wall push"],
             ["胸长神经 → 前锯肌无力", "肩胛骨上移，下角转向中线", "内侧缘离开胸壁；推墙时最明显"]),
            ("B · Lateral winging", "B · 外侧型翼状肩胛", RED, 0, 44, -10,
             ["Spinal accessory nerve → trapezius weak", "Scapula moves DOWN; inferior angle turns outward", "Shoulder droops; a resisted shrug is weak"],
             ["副神经 → 斜方肌无力", "肩胛骨下移，下角转向外", "肩下垂；抗阻耸肩无力"])]):
        ox = 40 + i * 650
        f.bi(ox + 280, 128, title, sub, 17, col, "middle")
        S, X0, Y0 = 0.82, ox - 420, -60
        f.g(f"translate({X0},{Y0}) scale({S})")
        for k in range(1, 10):
            y = P.sp_y(f"T{k}")
            f.raw(f'<rect x="{P.MID - 13}" y="{y - 8}" width="26" height="16" rx="5" fill="{BONE}" stroke="{BONE_E}" stroke-width="1.2"/>')
            f.path(f"M{P.MID + 18},{y - 10} C{P.MID + 120},{y - 36} {P.MID + 250},{y} {P.MID + 300},{y + 60}", "#ddd3c0", 5, rough=False)
        scapula(f, op=0.9, dash="6 6")                                                      # normal position
        cx, cy = 790, 400
        tr = f"translate({dx},{dy}) rotate({ang} {cx} {cy})"
        if i == 0:   # lifted medial border: a shadow strip along it
            f.g(tr); f.path("M748,392 C756,470 766,540 772,590", "#3a3a3a", 9, op=0.18, rough=False); f.end()
        scapula(f, tr=tr)
        f.end()
        ix, iy = X0 + S * 786, Y0 + S * 600
        nx = X0 + S * (cx + dx + (786 - cx) * math.cos(math.radians(ang)) - (600 - cy) * math.sin(math.radians(ang)))
        ny = Y0 + S * (cy + dy + (786 - cx) * math.sin(math.radians(ang)) + (600 - cy) * math.cos(math.radians(ang)))
        f.arrow(f"M{ix:.0f},{iy:.0f} L{nx:.0f},{ny:.0f}", col, 3.4, rough=False)
        f.text(ox + 120, 542, "Dashed = normal position · 虚线 = 正常位置", 12, "#777", lang="zh-CN")
        for j, (e, z) in enumerate(zip(en, zh)):
            f.bi(ox + 20, 570 + j * 58, e, z, 15, col if j == 0 else INK, weight="600" if j == 0 else "400")
    f.save("翼状肩胛")


# ------------------------------------------------------------------ 07 LU7–LU11 + LI1 (hand chart)
PTS = [("列缺", "Lièquē", 384, H.above(1.5), RED), ("经渠", "Jīngqú", 407, H.above(1), RED), ("太渊", "Tàiyuān", 421, H.WRIST, RED),
       ("鱼际", "Yújì", 334, 704, RED), ("少商", "Shàoshāng", 266, 858, RED), ("商阳", "Shāngyáng", 409, 1046, LI_C)]


def f07():
    f = Fig("07", 1140, 1320, "Lung meridian LU7–LU11 and LI1", "手太阴肺经 LU7–LU11 与手阳明大肠经起点 LI1（右手，掌面，解剖学姿势）")
    f.bi(38, 118, "Forearm: cubital crease → wrist crease = 12 cun. Ruler on the right counts up from the wrist crease.",
         "骨度：肘横纹至腕掌侧远端横纹 12 寸；右侧标尺从腕横纹往上数。", 15, INK, weight="400")
    X, YO = 150, 120
    f.g(f"translate({X},{YO})")
    H.hand_palmar_base(f)
    # meridian
    f.path(f"M412,170 C408,300 392,400 384,{H.above(1.5)} L407,{H.above(1)} L421,{H.WRIST} C400,600 360,650 334,704 C318,760 292,812 266,858", RED, 4.2)
    f.path(f"M384,{H.above(1.5)} C392,600 400,760 404,900 C406,960 408,1010 409,1046", RED, 2, dash="3 5", rough=False)
    f.path("M409,1046 C420,980 440,920 470,880", LI_C, 3, dash="8 6", rough=False)
    for n, py, x, y, c in PTS:
        f.circle(x, y, 10, c, "#fff", 3)
    # ruler (ulnar side)
    RX = 700
    f.path(f"M{RX},{H.WRIST} L{RX},{H.above(4)}", INK, 1.6, rough=False)
    for c in (0, 0.5, 1, 1.5, 2, 3, 4):
        y = H.above(c); hot = c in (1, 1.5)
        f.path(f"M{RX - 8},{y} L{RX + 8},{y}", INK, 1.4, rough=False)
        f.text(RX + 14, y + 5, f"{c:g}", 15 if hot else 13, RED if hot else "#555", weight="700" if hot else "400")
    f.text(RX - 30, H.above(4) - 16, "寸 cun", 14, "#555", lang="zh-CN")
    f.path(f"M{H.RAD_X},{H.WRIST} L{RX - 10},{H.WRIST}", "#8f8a7e", 1, dash="3 4", rough=False)
    f.end()
    T = lambda x, y: (X + x, YO + y)
    # point labels (left)
    for (n, py, x, y, c), ly in zip(PTS, (460, 550, 670, 780, 940, 1160)):
        X1, Y1 = T(x, y)
        f.leader(X1 - 12, Y1, 236, ly - 6, c, "3 3")
        f.raw(f'<rect x="42" y="{ly - 24}" width="196" height="34" rx="6" fill="#fff8f0" stroke="{c}" stroke-width="1.4"/>')
        f.text(52, ly, n, 21, c, weight="700", lang="zh-CN"); f.text(100, ly - 1, py, 15, c)
    # cun notes at the ruler
    rx = X + 700 + 40
    f.bi(rx, YO + H.above(1.5) + 4, "Lieque: 1.5 cun", "列缺：腕横纹上 1.5 寸", 14, RED)
    f.bi(rx, YO + H.above(1) + 20, "Jingqu: 1 cun", "经渠：腕横纹上 1 寸", 14, RED)
    f.bi(rx, YO + H.WRIST + 4, "Taiyuan: on the crease", "太渊：腕横纹上，桡动脉搏动处", 14, RED)
    # forearm structures: labels in a row above the forearm, fan-shaped leaders that never cross
    for cx, (sx, sy), en, zh, c in [(330, (396, H.above(4) + 14), "Brachioradialis tendon", "肱桡肌腱", "#8c6b52"),
                                    (520, (428, H.above(4.6) + 14), "Radial artery", "桡动脉", H.ARTERY),
                                    (720, (462, H.above(4) + 14), "Flexor carpi radialis tendon", "桡侧腕屈肌腱", "#8c6b52"),
                                    (940, (500, H.above(4) + 14), "Median nerve", "正中神经", "#9a7414")]:
        X1, Y1 = T(sx, sy); f.leader(cx, 224, X1, Y1, "#a8a294"); f.bi(cx, 196, en, zh, 14, c, "middle", "600")
    # hand structures: labels on the right, ordered so their leaders do not cross
    for (sx, sy), ly, en, zh, c in [((520, 470), 770, "Pronator quadratus (deep)", "旋前方肌（深层）", "#8a7f6c"),
                                    ((372, 604), 840, "Radial artery → snuffbox", "桡动脉转向手背鼻烟窝", H.ARTERY),
                                    ((380, 700), 900, "Thenar eminence", "鱼际（大鱼际肌群）", "#8c6b52")]:
        X1, Y1 = T(sx, sy); f.leader(X1, Y1, rx - 8, ly - 6, "#a8a294"); f.bi(rx, ly, en, zh, 14, c, weight="600")
    f.bi(rx, 990, "Thick red: lung meridian", "粗红线：肺经", 13, RED, weight="600")
    f.bi(rx, 1032, "Dotted: branch from Lieque", "点线：从列缺分出的支脉，", 13, "#777", weight="400")
    f.bi(rx, 1074, "to the index finger (LI1)", "到食指桡侧接商阳", 13, "#777", weight="400")
    f.bi(rx, 1150, "Lieque is on the radial edge:", "列缺在桡侧缘：", 13, INK, weight="600")
    f.bi(rx, 1192, "side view in Figure 08", "侧面观见图 08", 13, INK, weight="400")
    f.save("肺经LU7-LU11与商阳")


# ------------------------------------------------------------------ 08 how to find
def f08():
    f = Fig("08", 1320, 960, "How to find Lieque and the nail-corner points", "怎么找：列缺（桡侧面观）与指甲角的井穴")
    # ---- A radial side of the right wrist (dorsal = left, palmar = right, hand below)
    f.bi(320, 128, "A · Right wrist, radial side", "A · 右腕，桡侧面观（拇指一侧）", 16, RED, "middle")
    f.path("M200,170 L210,470 C214,520 230,560 262,590 L460,590 C470,540 470,500 466,470 L460,170 Z", "#b9b2a3", 1.4, "#fffaf1")   # forearm
    f.path("M262,590 C250,660 262,740 300,790 L470,790 C478,720 474,640 460,590", "#b9b2a3", 1.4, "#fffaf1")                        # hand edge
    f.path("M226,560 C250,600 300,610 330,600", BONE_E, 1.6, "none")
    f.raw(f'<ellipse cx="300" cy="566" rx="34" ry="20" fill="{BONE}" stroke="{BONE_E}" stroke-width="1.6"/>')  # radial styloid
    f.text(190, 548, "Radial styloid process", 13, INK, "end", "700"); f.text(190, 566, "桡骨茎突", 12, "#68726a", "end", lang="zh-CN")
    f.path("M340,170 C330,330 320,450 316,520 C312,580 300,640 286,700", "#b98c64", 9, rough=False)   # APL
    f.path("M372,170 C360,330 350,450 344,520 C338,590 326,650 312,710", "#c6a789", 8, rough=False)   # EPB
    f.path("M250,300 C262,420 270,520 262,600 C258,660 266,720 290,760", "#a5856a", 7, rough=False, op=0.8)  # EPL (dorsal)
    f.raw('<path d="M262,604 C276,640 290,680 300,700 L312,700 C300,660 300,624 314,600 Z" fill="#f4e0b0" opacity=".7"/>')  # snuffbox
    f.path("M420,170 C410,330 380,500 330,600 C310,630 296,660 290,700", RED, 3, dash="6 4", rough=False)
    for y, lab in ((170, "Abductor pollicis longus 拇长展肌腱"), (200, "Extensor pollicis brevis 拇短伸肌腱")):
        pass
    f.leader(340, 200, 520, 200, "#a8a294"); f.bi(526, 204, "Abductor pollicis longus tendon", "拇长展肌腱", 13, "#8c6b52", weight="600")
    f.leader(368, 250, 520, 260, "#a8a294"); f.bi(526, 264, "Extensor pollicis brevis tendon", "拇短伸肌腱", 13, "#8c6b52", weight="600")
    f.leader(258, 400, 190, 420, "#a8a294"); f.bi(184, 424, "EPL tendon", "拇长伸肌腱", 13, "#8c6b52", "end", weight="600")
    f.leader(300, 680, 190, 690, "#a8a294"); f.bi(184, 694, "Anatomical snuffbox", "解剖学鼻烟窝", 13, "#9a7414", "end", weight="600")
    f.leader(400, 380, 520, 330, RED); f.bi(526, 334, "Radial artery (to the snuffbox)", "桡动脉（转入鼻烟窝）", 13, RED, weight="600")
    # Lieque: 1.5 cun above the crease in the APL groove, just above the styloid
    lx, ly = 330, 470
    f.raw(f'<rect x="520" y="420" width="190" height="34" rx="6" fill="#fff8f0" stroke="{RED}" stroke-width="1.4"/>')
    f.text(530, 444, "列缺", 21, RED, weight="700", lang="zh-CN"); f.text(578, 443, "Lièquē", 15, RED)
    f.leader(342, ly, 514, 437, RED, "3 3")
    # crossed-hands method: the other hand's index finger along the radius, tip on the point
    # the other hand's index finger: a capsule from the upper left, fingertip on the point
    (x1, y1), (x2, y2) = (96, 236), (lx - 4, ly - 6)
    L = math.hypot(x2 - x1, y2 - y1); ux, uy = (x2 - x1) / L, (y2 - y1) / L; px_, py2 = -uy * 21, ux * 21
    f.path(f"M{x1 + px_:.0f},{y1 + py2:.0f} L{x2 + px_:.0f},{y2 + py2:.0f} A21,21 0 0 0 {x2 - px_:.0f},{y2 - py2:.0f} L{x1 - px_:.0f},{y1 - py2:.0f} Z",
           "#6f8fb5", 1.6, "#dbe6f3", op=0.8)
    nx, ny = x2 - ux * 30, y2 - uy * 30
    f.path(f"M{nx + px_ * .6:.0f},{ny + py2 * .6:.0f} L{x2 - ux * 6 + px_ * .6:.0f},{y2 - uy * 6 + py2 * .6:.0f} M{nx - px_ * .6:.0f},{ny - py2 * .6:.0f} L{x2 - ux * 6 - px_ * .6:.0f},{y2 - uy * 6 - py2 * .6:.0f}",
           "#6f8fb5", 1.2, rough=False)
    for k in (0.35, 0.6):   # finger joint creases
        cx_, cy_ = x1 + (x2 - x1) * k, y1 + (y2 - y1) * k
        f.path(f"M{cx_ + px_ * .8:.0f},{cy_ + py2 * .8:.0f} L{cx_ - px_ * .8:.0f},{cy_ - py2 * .8:.0f}", "#6f8fb5", 1, rough=False)
    f.circle(lx, ly, 11, RED, "#fff", 3)
    f.bi(40, 200, "Other hand's index finger", "另一手食指", 13, "#4a6a92", weight="600")
    f.bi(40, 820, "Cross the two webs (hukou jiaocha) and lay the index finger on the styloid:", "两手虎口交叉，一手食指按在另一手桡骨茎突上，", 13, INK, weight="400")
    f.bi(40, 862, "the hollow under the fingertip is Lieque, 1.5 cun above the crease.", "指尖下的凹陷就是列缺（腕横纹上 1.5 寸）。", 13, INK, weight="400")
    # ---- B nail-corner points
    bx = 820
    f.bi(bx + 220, 128, "B · Jing-well points at the nail corner", "B · 井穴：指甲根角旁 0.1 寸（右手背面观）", 16, LI_C, "middle")
    for i, (name, py, title, w, col) in enumerate([("少商", "Shàoshāng", "Thumb 拇指", 120, RED), ("商阳", "Shāngyáng", "Index 食指", 96, LI_C)]):
        x0 = bx + i * 240; y0 = 220
        f.path(f"M{x0},{y0 + 360} L{x0},{y0 + 60} C{x0},{y0 + 10} {x0 + w},{y0 + 10} {x0 + w},{y0 + 60} L{x0 + w},{y0 + 360}", INK, 2.2, "#fffaf1")
        nx0, nx1, ny0, ny1 = x0 + 18, x0 + w - 18, y0 + 40, y0 + 150
        f.path(f"M{nx0},{ny1} L{nx0},{ny0 + 20} C{nx0},{ny0} {nx1},{ny0} {nx1},{ny0 + 20} L{nx1},{ny1} Z", "#b9ab94", 1.6, "#f6eadb")
        f.path(f"M{nx0},{ny0 - 10} L{nx0},{ny1 + 70}", "#7a8a9a", 1.2, dash="4 4", rough=False)          # along the radial nail border
        f.path(f"M{nx0 - 40},{ny1} L{nx1 + 10},{ny1}", "#7a8a9a", 1.2, dash="4 4", rough=False)          # along the nail base
        px, py_ = nx0 - 9, ny1 + 9
        f.circle(px, py_, 9, col, "#fff", 2.6)
        f.text(x0 + w / 2, y0 + 400, title, 14, INK, "middle", "700", "zh-CN")
        f.raw(f'<rect x="{x0 - 20}" y="{y0 + 420}" width="{w + 60}" height="34" rx="6" fill="#fff8f0" stroke="{col}" stroke-width="1.4"/>')
        f.text(x0 - 10, y0 + 444, name, 20, col, weight="700", lang="zh-CN"); f.text(x0 + 36, y0 + 443, py, 13, col)
        f.text(x0 - 6, y0 + 20, "radial 桡侧 ←", 12, "#777", lang="zh-CN")
    f.bi(bx, 760, "Draw one line along the radial edge of the nail and one", "沿指甲桡侧缘画一条线、沿甲根画一条线，", 13, INK, weight="400")
    f.bi(bx, 802, "along its base: the point is 0.1 F-cun out from the corner.", "两线交点外 0.1 指寸（沿角平分线）即是。", 13, INK, weight="400")
    f.save("怎么找列缺与井穴")


# ------------------------------------------------------------------ 09 layers
def f09():
    f = Fig("09", 1300, 600, "What lies beneath Taiyuan and Lieque", "太渊、列缺深面有什么：层次示意")
    f.bi(38, 116, "Not to scale; layers only, not needling depth or direction.", "不按比例，只表示层次，不表示进针深度或方向。", 14, RED, weight="400")
    stack2(f, 40, 170, 580, "Taiyuan (LU9) · wrist crease, radial side", "太渊 · 腕掌侧远端横纹桡侧",
           [("Skin", "皮肤", 40, "#f6e7da", "#d8c3ae", ""),
            ("Subcutaneous: lateral antebrachial cutaneous n., superficial radial n.", "皮下组织：前臂外侧皮神经、桡神经浅支的混合支", 56, "#fbf2e3", "#e0d2b8", ""),
            ("Between the FCR tendon (ulnar) and the APL tendon (radial)", "桡侧腕屈肌腱（尺侧）与拇长展肌腱（桡侧）之间", 56, "#efe1d0", "#c9b296", ""),
            ("Radial artery and veins: the pulse under your finger", "桡动脉、桡静脉：就是手指下摸到的脉", 60, "#f2c9c3", RED, "危险")],
           "Feel the pulse first, then stay off the artery.", "先摸到脉，再避开桡动脉。")
    stack2(f, 680, 170, 580, "Lieque (LU7) · 1.5 cun above the crease", "列缺 · 腕横纹上 1.5 寸",
           [("Skin", "皮肤", 40, "#f6e7da", "#d8c3ae", ""),
            ("Subcutaneous: cephalic vein tributaries, superficial radial n.", "皮下组织：头静脉属支、桡神经浅支", 56, "#fbf2e3", "#e0d2b8", "留意"),
            ("Between the tendons (GB/T: EPB and APL; older text: BR and APL)", "两腱之间（国标：拇短伸肌腱与拇长展肌腱）", 56, "#efe1d0", "#c9b296", ""),
            ("Radial edge of pronator quadratus", "旋前方肌桡侧缘", 48, "#e2d5c0", "#b9a888", ""),
            ("Deep: branches of the radial artery and veins", "深层：桡动、静脉分支", 48, "#f2c9c3", RED, "")],
           "Nerve and vein lie shallow: textbooks needle it obliquely toward the elbow.", "浅层有神经和静脉：教材为向肘部斜刺。")
    f.save("太渊列缺-层次示意")


def build(out_dir):
    set_out(out_dir)
    f01(); f02(); f03(); f04(); f05(); f06(); f07(); f08(); f09()


if __name__ == "__main__":
    build(sys.argv[1] if len(sys.argv) > 1 else pathlib.Path(__file__).resolve().parent / "资源")
