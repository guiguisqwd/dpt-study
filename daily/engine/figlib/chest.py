#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Chest wall base art: right side, anterior view, local coordinates (anterior midline x=700).
Reused by every day that touches pectoral / anterior chest structures."""
from .fig import *

PEC_C = "M680,104 C620,112 540,92 470,88 L298,300 L300,330 C420,240 560,160 680,140 Z"
PEC_S = "M680,140 C560,160 420,240 300,330 L292,388 C400,470 560,515 690,470 L690,140 Z"
DELT_A = "M470,88 C420,84 340,70 270,80 C215,95 200,160 205,240 C210,350 240,450 262,520 C285,440 300,340 330,250 C370,170 420,115 470,88 Z"
PMIN = "M345,140 L560,212 L566,262 L572,316 Z"
SUBCL = "M640,112 C600,108 540,100 480,96 L478,106 C540,112 600,120 640,124 Z"
RED_F, RED_S = "#e9a596", RED
PMIN_F, PMIN_S = "#d9b3a6", "#8f4a3c"
SUB_F, SUB_S = "#f0c7a8", "#b46a2c"

def rib_y(k, x):
    ys, yl = 118 + (k - 1) * 46, 128 + (k - 1) * 50
    return ys + (yl - ys) * (688 - x) / 298

def chest_base(f, show_pecmaj=True, op=1.0, pecmin="dashed", subcl=True, delt=True, rib_nums=False):
    """右侧胸前区前面观，局部坐标：前正中线 x=700。"""
    f.path("M392,230 C385,380 395,560 420,720", "#999", 1.4, dash="5 6", rough=False)  # 胸外侧轮廓
    for k in range(1, 8):
        ys, yl = 118 + (k - 1) * 46, 128 + (k - 1) * 50
        f.path(f"M688,{ys} Q545,{ys+16} 392,{yl}", "#c9bfa9", 13, rough=False)
        f.path(f"M688,{ys} Q545,{ys+16} 392,{yl}", BONE, 9, rough=False)
        if rib_nums: f.text(378, yl + 5, str(k), 13, "#8a7f6c", "end", "700")
    f.path("M672,95 L728,95 L722,170 L678,170 Z", BONE_E, 1.8, BONE)
    f.path("M680,170 L720,170 L714,470 L686,470 Z", BONE_E, 1.8, BONE)
    f.path("M690,470 L710,470 L700,510 Z", BONE_E, 1.6, BONE)
    f.path("M250,190 L240,720 L285,720 L300,195 Z", BONE_E, 2, BONE)
    f.raw(f'<circle cx="270" cy="150" r="55" fill="{BONE}" stroke="{BONE_E}" stroke-width="2"/>')
    f.path("M330,108 Q352,126 362,146 Q352,154 338,146 Z", BONE_E, 2, BONE)  # 喙突
    if delt: f.path(DELT_A, "#8a8a8a", 1.5, "#ece6da", dash="5 5", op=0.9)
    if pecmin == "solid": f.path(PMIN, PMIN_S, 2.2, PMIN_F, op=0.9)
    f.path("M262,200 L266,430", "#b5ab98", 1.2, dash="4 5", rough=False)  # 结节间沟（示意）
    if show_pecmaj:
        for d in (PEC_C, PEC_S): f.path(d, RED_S, 2.2, RED_F, op=op)
        f.path("M300,306 L268,330 L268,358 L300,384 Z", RED_S, 1.6, "#d98472", op=op)  # 止点腱：从肱骨前面跨到结节间沟外侧唇
        for ox, oy in [(640, 108), (560, 96), (690, 200), (690, 280), (690, 360), (690, 440), (600, 485), (520, 470)]:
            f.raw(f'<path d="M{ox},{oy} Q{(ox+295)/2},{(oy+345)/2+10} 295,345" stroke="{RED_S}" stroke-width="1.1" fill="none" opacity="{0.5*op:.2f}"/>')
    if pecmin == "dashed": f.path(PMIN, PMIN_S, 2, "none", dash="7 5")
    if subcl: f.path(SUBCL, SUB_S, 1.8, SUB_F, op=0.95)
    f.path("M680,100 C600,112 520,70 440,80 C390,86 340,78 300,80", BONE_E, 22)
    f.path("M680,100 C600,112 520,70 440,80 C390,86 340,78 300,80", BONE, 17, rough=False)
    f.path("M228,70 Q270,52 318,68 Q322,86 300,92 Q260,96 232,90 Z", BONE_E, 2, BONE)


# ------------------------------------------------------------------ 02-04 O/I
def chest_oi(num, name, en, zh, which, o_pts, i_pt, oen, ozh, ien, izh, col):
    # 只取胸前区（局部 x 180–745, y 40–560），放大到卡片宽度，图例放在图下方，不压骨头
    f = Fig(num, 760, 1000, f"{en}: origin and insertion", f"{zh}：起点与止点")
    X0, Y0, S = 40 - 180 * 1.22, 150 - 40 * 1.22, 1.22
    f.raw(f'<clipPath id="{f.id("crop")}"><rect x="180" y="40" width="565" height="520"/></clipPath>')
    f.g(f"translate({X0:.1f},{Y0:.1f}) scale({S})"); f.raw(f'<g clip-path="url(#{f.id("crop")})">')
    chest_base(f, show_pecmaj=(which == "pmaj"), op=0.9, pecmin=("solid" if which == "pmin" else "none"), subcl=(which == "sub"), delt=False, rib_nums=True)
    f.end(); f.end()
    P = lambda x, y: T(X0, Y0, S, x, y)
    ix, iy = P(*i_pt)
    for o in o_pts:
        ox, oy = P(*o)
        f.path(f"M{ox:.0f},{oy:.0f} Q{(ox+ix)/2:.0f},{min(oy,iy)-30:.0f} {ix:.0f},{iy:.0f}", INK, 2.2, dash="8 6", rough=False)
    for o in o_pts:
        ox, oy = P(*o); f.circle(ox, oy, 17, col, "#fff", 3); f.text(ox, oy + 7, "O", 19, "#fff", "middle", "700")
    f.circle(ix, iy, 19, INK, "#fff", 3); f.text(ix, iy + 7.5, "I", 21, "#fff", "middle", "700")
    f.bi(38, 124, "Dashed line = attachment order, not force · grey numbers = ribs", "虚线 = 起点 → 止点的附着顺序，不是受力方向；灰色数字 = 肋骨序号", 16, "#666", weight="400", zsize=15)
    f.bi(38, 838, f"O = Origin: {oen}", f"起点：{ozh}", 21, col, gap=28, zsize=20)
    f.bi(38, 906, f"I = Insertion: {ien}", f"止点：{izh}", 21, INK, gap=28, zsize=20)
    f.save(zh + "起止点")

