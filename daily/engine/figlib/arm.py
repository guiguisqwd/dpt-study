#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Upper limb, anterior view (right side, anatomical position, palm forward, thumb lateral = viewer's left).
Upper-arm cun = 40 px, forearm cun = 34 px (each segment divided on its own). Reused for LU / PC / HT meridians."""
from .fig import *

# 上肢前面观底图（右侧，解剖学姿势，掌心向前，拇指在外侧 = 观者左侧）。
# 纵向 1 寸 = 40 px：腋前纹头 y=470（0 寸）→ 肘横纹 y=830（9 寸）→ 腕掌侧远端横纹 y=1310（12 寸）。
# 胸部横向 1 寸 ≈ 33.7 px：前正中线 x=1080，旁开 6 寸 x=878。后面几天的肺经、心包经、心经都复用这张底图。
# 两段的“1 寸”长度不同（骨度分寸按段等分）：上臂 1 寸 = 40 px，前臂 1 寸 = 34 px，比例接近真人。
import re as _re
UP_CUN, FORE_CUN = 40, 34
ARM_Y = {"fold": 470, "elbow": 830, "wrist": 830 + 12 * FORE_CUN}
MID_X, CHEST_CUN = 1080, (1080 - 878) / 6
def arm_y(seg, cun):  # seg: "upper"（从腋前纹头往下）或 "fore"（从肘横纹往下）
    return ARM_Y["fold"] + cun * UP_CUN if seg == "upper" else ARM_Y["elbow"] + cun * FORE_CUN
def fy(y):  # 草图坐标（前臂按 40 px/寸 画的）→ 实际坐标
    return y if y <= 830 else (830 + (y - 830) * FORE_CUN / 40 if y <= 1310 else y - 1310 + ARM_Y["wrist"])
def xfy(d):
    return _re.sub(r"(-?\d+(?:\.\d+)?),(-?\d+(?:\.\d+)?)", lambda m: f"{m.group(1)},{fy(float(m.group(2))):.0f}", d)
SIL_FILL = ("M800,222 C762,226 730,262 728,330 C727,400 740,450 748,500 C744,560 742,650 742,740 L742,830 "
            "C730,880 722,960 722,1050 C722,1150 724,1250 725,1305 C714,1330 694,1370 678,1405 C668,1428 660,1450 666,1462 "
            "C674,1472 690,1460 700,1440 C708,1424 716,1410 722,1402 C722,1460 724,1530 728,1574 C730,1590 750,1592 753,1580 C756,1600 776,1602 778,1588 "
            "C781,1600 800,1598 802,1584 C806,1592 822,1586 825,1570 C832,1530 832,1470 828,1430 C824,1380 818,1340 815,1310 C830,1200 850,1050 862,930 "
            "C866,880 874,850 872,830 C864,760 860,650 862,560 C863,520 864,495 865,482 C850,420 830,300 800,222 Z")
SIL_FILL = xfy(SIL_FILL)
SIL_LINE = SIL_FILL.rsplit(" C850,420", 1)[0]
DELT_F = "M850,236 C820,228 790,226 770,236 C740,252 728,300 728,340 C728,400 738,450 752,500 C765,470 790,440 805,425 C830,380 848,330 868,296 C860,272 855,252 850,236 Z"
PECM_F = ("M905,246 C890,262 876,288 868,300 C850,340 826,395 802,440 L815,455 C840,470 855,478 865,482 "
          "C920,540 990,590 1066,600 L1070,256 C1010,262 950,246 905,246 Z")
BIC_F = "M790,450 C772,520 766,600 770,680 C776,760 796,805 802,826 L814,826 C822,800 846,740 850,660 C853,580 846,500 836,452 Z"
BRAD_F = xfy("M748,700 C740,760 736,830 736,890 C736,1000 738,1150 734,1290 L746,1292 C756,1150 774,1000 780,900 C784,840 772,760 760,700 Z")
CLAV = "M1064,252 C1000,262 950,240 900,238 C860,236 830,228 800,226"
def arm_base(f, pec=True):
    f.path("M1010,140 C1006,175 992,192 950,200 C900,212 840,212 800,222", "#9a958a", 1.6, rough=False)   # 颈、斜方肌轮廓
    f.path("M865,482 C875,520 882,560 886,610", "#9a958a", 1.6, rough=False)                          # 胸外侧轮廓
    f.path(SIL_FILL, "none", 0, "#fffaf1", rough=False)
    if pec:
        f.raw(f'<clipPath id="{f.id("pecm")}"><path d="{PECM_F}"/></clipPath>')
        f.path(PECM_F, "#d99a8b", 1.4, "#f6ddd5")
        for ox, oy in [(940, 246), (1010, 254), (1068, 320), (1068, 400), (1068, 480), (1060, 560), (990, 584), (930, 540)]:
            f.raw(f'<path d="M{ox},{oy} Q{(ox+810)/2},{(oy+445)/2+8} 810,445" stroke="#d99a8b" stroke-width="1" fill="none" opacity=".55" clip-path="url(#{f.id("pecm")})"/>')
    f.path("M850,236 L905,246 L868,296 Z", "none", 0, "#efe6d6", rough=False)                       # 锁骨下窝（三角肌胸大肌三角）
    f.path(DELT_F, "#a59b88", 1.4, "#ece4d4", op=0.95)
    f.raw(f'<ellipse cx="856" cy="284" rx="11" ry="8" fill="#efe6d6" stroke="#8a7f6c" stroke-width="1.4" stroke-dasharray="3 3"/>')  # 喙突（深面，可触及）
    f.path(BIC_F, "#c9a98f", 1.4, "#f3e6d6")
    f.path(BRAD_F, "#c9a98f", 1.4, "#f1e2cf")
    f.path(SIL_LINE, INK, 2.2, rough=False)
    for x, y2 in ((753, 1580), (778, 1588), (802, 1584)): f.path(xfy(f"M{x-2},1478 L{x},{y2}"), "#b8ae9c", 1.1, rough=False)   # 指缝
    f.path(xfy("M772,1318 C752,1350 742,1378 734,1406"), "#b8ae9c", 1.1, rough=False)                # 鱼际纹
    f.path(CLAV, BONE_E, 19); f.path(CLAV, BONE, 14, rough=False)
    f.path("M1062,252 Q1080,262 1098,252", "#9a958a", 1.4, rough=False)                              # 胸骨上窝
    f.path(f"M{MID_X},150 L{MID_X},610", "#b9b4a8", 1.4, dash="4 6", rough=False)
    f.path(xfy("M868,262 C855,300 830,370 805,430 C785,470 765,520 758,590 C754,660 752,760 750,830 C746,900 740,1000 736,1100"),
           BLUE, 1.8, op=0.55)                                                                        # 头静脉

def acu_box(f, x, y, zh, py, col=RED, w=190):
    f.raw(f'<rect x="{x-8}" y="{y-24}" width="{w}" height="34" rx="6" fill="#fff8f0" stroke="{col}" stroke-width="1.4"/>')
    f.text(x + 2, y, zh, 21, col, weight="700", lang="zh-CN"); f.text(x + 52, y - 1, py, 16, col)

LU_TODAY = [("中府", "Zhōngfǔ", 878, 310), ("云门", "Yúnmén", 878, 270), ("天府", "Tiānfǔ", 770, arm_y("upper", 3)),
            ("侠白", "Xiábái", 769, arm_y("upper", 4)), ("尺泽", "Chǐzé", 790, arm_y("fore", 0)), ("孔最", "Kǒngzuì", 768, arm_y("fore", 5))]  # 尺泽(790,830)–太渊(738,腕横纹) 连线上
LU_LATER = [("列缺", 730, arm_y("fore", 10.5)), ("经渠", 738, arm_y("fore", 11)), ("太渊", 738, arm_y("fore", 12)), ("鱼际", 705, fy(1385)), ("少商", 668, fy(1448))]
