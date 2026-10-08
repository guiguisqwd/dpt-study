#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Day 1 (2026-10-07) figures: anterior chest muscles + lung meridian LU1–LU6.
Run via pipeline (figures step) or: python3 figures.py <out_dir>."""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2]))
from engine.figlib import *

# ------------------------------------------------------------------ 01 overview
def f01():
    f = Fig("01", 1340, 920, "Anterior chest wall: pectoral muscles", "胸前区：胸大肌、胸小肌与锁骨下肌（右侧前面观）")
    X0, Y0, S = 80, 130, 1.0
    f.g(f"translate({X0},{Y0}) scale({S})"); chest_base(f, op=0.85); f.end()
    P = lambda x, y: T(X0, Y0, S, x, y)
    labs = [((560, 380), "Pectoralis major (sternocostal head)", "胸大肌胸肋部", (900, 560), RED),
            ((560, 120), "Pectoralis major (clavicular head)", "胸大肌锁骨部", (900, 210), RED),
            ((470, 250), "Pectoralis minor (deep, dashed)", "胸小肌（深层，虚线）", (900, 360), "#8f4a3c"),
            ((560, 106), "Subclavius (under the clavicle)", "锁骨下肌（锁骨下方）", (900, 150), "#b46a2c"),
            ((350, 132), "Coracoid process", "喙突", (900, 290), INK),
            ((220, 300), "Deltoid (dashed outline)", "三角肌（虚线轮廓）", (40, 640), "#777"),
            ((268, 344), "Intertubercular groove, lateral lip", "结节间沟外侧唇（胸大肌止点）", (40, 720), INK),
            ((700, 300), "Sternum (midline)", "胸骨（前正中线）", (900, 450), INK),
            ((470, 70), "Clavicle", "锁骨", (40, 160), INK)]
    for (x, y), en, zh, (lx, ly), c in labs:
        X, Y = P(x, y); f.leader(X, Y, lx + (0 if lx > X else 230), ly - 5, c); f.bi(lx, ly, en, zh, 15, c)
    f.text(40, 112, "Right side, anterior view · 右侧，前面观（前正中线在右）", 15, INK, weight="700", lang="zh-CN")
    f.save("胸前区肌肉总览")


# ------------------------------------------------------------------ 05 nerves
def f05():
    f = Fig("05", 1300, 820, "Brachial plexus: nerves to the pectoral muscles", "臂丛：支配胸前肌肉的神经")
    f.box(38, 96, 560, 64, "#cfd8cc", "#eef3ec")
    f.text(54, 122, "C = Cervical 颈部 · T = Thoracic 胸部", 15, INK, weight="700", lang="zh-CN")
    f.text(54, 146, "Grey blocks are vertebrae (bones); lines are spinal nerves. 灰块为椎骨，线为脊神经。", 13, "#444", lang="zh-CN")
    verts = [("C4", 230), ("C5", 300), ("C6", 370), ("C7", 440), ("T1", 510), ("T2", 580)]
    f.path("M95,195 L95,620", "#d9d2bf", 22, rough=False)
    for n, cy in verts:
        f.raw(f'<rect x="62" y="{cy-24}" width="86" height="48" rx="11" fill="#e6e1d3" stroke="{BONE_E}" stroke-width="1.8"/>')
        f.text(105, cy + 6, f"{n} vertebra", 13, INK, "middle", "700")
    roots = {"C5": 265, "C6": 335, "C7": 405, "C8": 475, "T1": 545}
    for r, y in roots.items(): f.text(162, y - 9, f"{r} nerve", 14, INK, "start", "700")
    TR = {"sup": (430, 300), "mid": (430, 405), "inf": (430, 510)}
    rc = {"C5": BLUE, "C6": BLUE, "C7": GREY, "C8": PURP, "T1": PURP}
    for r, t in [("C5", "sup"), ("C6", "sup"), ("C7", "mid"), ("C8", "inf"), ("T1", "inf")]:
        y = roots[r]; tx, ty = TR[t]
        f.path(f"M150,{y} C260,{y} 300,{ty} {tx},{ty}", rc[r], 4)
    for k, (x, y), en, zh, c in [("sup", TR["sup"], "Superior trunk", "上干", BLUE), ("mid", TR["mid"], "Middle trunk", "中干", GREY), ("inf", TR["inf"], "Inferior trunk", "下干", PURP)]:
        f.circle(x, y, 9, c)
        f.bi(x - 38, y + 34, en, zh, 14, c)
    CD = {"lat": (720, 330), "post": (720, 420), "med": (720, 505)}
    for a, b, c, w in [("sup", "lat", RED, 4.5), ("mid", "lat", RED, 4.5), ("sup", "post", GREY, 2.4), ("mid", "post", GREY, 2.4), ("inf", "post", GREY, 2.4), ("inf", "med", PURP, 4.5)]:
        (x1, y1), (x2, y2) = TR[a], CD[b]
        f.path(f"M{x1},{y1} L540,{y1} C620,{y1} 640,{y2} {x2},{y2}", c, w)
    for k, en, zh, c in [("lat", "Lateral cord", "外侧束", RED), ("post", "Posterior cord", "后束", GREY), ("med", "Medial cord", "内侧束", PURP)]:
        x, y = CD[k]; f.circle(x, y, 9, c)
        f.text(x + 14, {"lat": y + 28, "post": y + 26, "med": y - 18}[k], f"{en} {zh}", 13, c, "start", "700", "zh-CN")
    f.path("M732,330 C780,300 800,270 850,262", RED, 4)
    f.bi(858, 258, "Lateral pectoral n. (C5–C7)", "胸外侧神经 → 胸大肌（以锁骨部为主）", 15, RED)
    f.path("M732,505 C780,540 800,560 850,566", PURP, 4)
    f.bi(858, 562, "Medial pectoral n. (C8–T1)", "胸内侧神经 → 胸小肌 + 胸大肌胸肋部", 15, PURP)
    f.path("M732,420 L850,420", GREY, 2, rough=False); f.text(858, 425, "Axillary, radial nn. … (shoulder chapter) 腋神经、桡神经等", 13, "#777", lang="zh-CN")
    f.path("M445,300 C470,250 520,205 590,190", BLUE, 4)
    f.bi(598, 186, "Nerve to subclavius (C5–C6)", "锁骨下肌神经：由上干发出 → 锁骨下肌", 15, BLUE)
    f.bi(40, 700, "“Lateral” and “medial” pectoral nerves are named for the cords they leave, not for where they lie on the chest.",
         "胸外侧、胸内侧神经是按发出它们的“外侧束、内侧束”命名的，不是按它们在胸前的位置。", 15, INK)
    f.save("支配胸前肌肉的神经")

# ------------------------------------------------------------------ 06 movement
def f06():
    f = Fig("06", 1300, 800, "Line of pull: what the pectoral muscles do", "从力线推出动作：胸前三块肌肉")
    # ---- A 胸大肌：右侧前面观，手臂外展约 60°
    f.bi(220, 150, "A · Pectoralis major, anterior view", "A · 胸大肌，右侧前面观", 15, RED, "middle")
    f.path("M400,200 L400,640", "#bbb", 1.4, dash="4 5", rough=False); f.bi(406, 632, "Midline", "前正中线", 12, "#888", weight="400")
    f.path("M380,205 C350,232 300,240 262,250", "#9a958a", 1.5, rough=False)                     # 颈肩轮廓
    f.path("M300,372 C304,450 306,530 310,620", "#9a958a", 1.5, rough=False)                      # 胸外侧轮廓
    f.path("M262,250 C220,250 190,262 160,282 L70,350 C58,362 66,384 84,386 L120,372 C170,350 230,330 282,345 Z", INK, 2, "#fffaf1")  # 上臂（外展）
    f.path("M246,276 L96,364", BONE_E, 16, rough=False); f.path("M246,276 L96,364", BONE, 11, rough=False)   # 肱骨
    f.raw(f'<circle cx="250" cy="274" r="17" fill="{BONE}" stroke="{BONE_E}" stroke-width="2"/>')
    f.path("M386,240 L414,240 L410,480 L390,480 Z", BONE_E, 1.8, BONE)                            # 胸骨
    PM = "M392,236 C350,236 310,242 286,250 L212,306 L222,322 C280,330 330,420 392,470 Z"
    f.raw(f'<clipPath id="{f.id("pmA")}"><path d="{PM}"/></clipPath>')
    f.path(PM, RED, 2, "#eeb3a6", op=0.92)
    for ox, oy in [(360, 238), (320, 244), (392, 280), (392, 330), (392, 380), (392, 430), (380, 462)]:
        f.raw(f'<path d="M{ox},{oy} L216,314" stroke="{RED}" stroke-width="1" opacity=".5" clip-path="url(#{f.id("pmA")})"/>')
    f.path("M394,236 C350,246 300,238 262,248", BONE_E, 15); f.path("M394,236 C350,246 300,238 262,248", BONE, 10, rough=False)  # 锁骨
    f.arrow("M372,392 L246,322", "#7d2a20", 3.2)
    f.bi(318, 430, "Line of pull", "力线", 13, "#7d2a20", weight="600")
    f.arrow("M66,400 C80,470 120,520 180,548", RED, 3.4)
    f.bi(40, 586, "Adduction: arm pulled toward the body", "内收：手臂被拉回躯干", 15, RED)
    # ---- B 俯视肱骨头 → 内旋
    bx, by = 650, 400
    f.bi(bx, 150, "B · Superior view of the right humeral head", "B · 俯视右肱骨头", 15, RED, "middle")
    f.raw(f'<circle cx="{bx}" cy="{by}" r="80" fill="{BONE}" stroke="{BONE_E}" stroke-width="2.4"/>'); f.circle(bx, by, 6, INK, INK, 0)
    f.bi(bx + 12, by - 6, "Long axis", "长轴", 12, "#555", weight="400")
    for x, y, en, zh in [(bx, by - 112, "Posterior", "后"), (bx, by + 128, "Anterior", "前"), (bx + 122, by + 4, "Lateral", "外"), (bx - 152, by + 4, "Medial", "内")]:
        f.bi(x, y, en, zh, 12, "#777", "middle", "400")
    f.raw(f'<ellipse cx="{bx+55}" cy="{by+55}" rx="16" ry="11" fill="{BONE}" stroke="{BONE_E}" stroke-width="2"/>')
    f.arrow(f"M{bx+55},{by+55} C{bx},{by+110} {bx-90},{by+110} {bx-160},{by+70}", RED, 3)
    f.bi(bx - 210, by + 168, "Inserts in front of the long axis, pulls medially", "止点在长轴前方，向内拉", 13, RED)
    f.arrow(f"M{bx+86},{by+40} A95,95 0 0 1 {bx+20},{by+92}", RED, 2.6); f.bi(bx + 92, by + 112, "→ Internal rotation", "内旋", 14, RED)
    # ---- C 胸小肌：右侧面观（前方在右）
    f.bi(1050, 150, "C · Pectoralis minor, right lateral view", "C · 胸小肌，右侧面观", 15, "#8f4a3c", "middle")
    f.bi(1180, 196, "Front →", "前", 12, "#777", "middle", "400"); f.bi(920, 196, "← Back", "后", 12, "#777", "middle", "400")
    f.path("M1030,226 C960,232 920,330 925,440 C930,560 980,640 1060,646 C1140,640 1180,560 1182,440 C1184,330 1120,230 1030,226 Z", "#b9b2a3", 1.6, "#f6f1e7")  # 胸廓侧面
    for k, y in enumerate((300, 350, 400, 450, 500, 550)):
        f.path(f"M{938+ (k>3)*6},{y} C1000,{y+10} 1100,{y+36} 1176,{y+58}", "#d6ccb8", 7, rough=False)  # 肋骨（前低后高）
    for y, lab in ((350, "3"), (400, "4"), (450, "5")):
        f.text(1192, y + 64, lab, 13, "#8f4a3c", weight="700")
    f.path("M950,262 L978,258 L992,520 L966,526 Z", BONE_E, 2, BONE)                               # 肩胛骨（侧面看呈一条边）
    f.path("M972,286 C995,262 1040,262 1066,292 C1062,304 1046,300 1030,292 C1012,286 994,292 982,300 Z", BONE_E, 2, BONE)  # 喙突
    PMN = "M1066,296 L1160,402 L1168,456 L1170,512 L1046,306 Z"
    f.path(PMN, "#8f4a3c", 2, "#d9b3a6", op=0.92)
    f.arrow("M1060,300 L1112,360", "#8f4a3c", 3.4)
    f.arrow("M974,530 C958,532 936,524 916,508", "#8f4a3c", 2.8)
    f.bi(1076, 262, "Coracoid", "喙突", 12, INK, weight="600")
    f.bi(1192, 344, "Ribs", "肋", 12, "#8f4a3c", weight="600")
    f.bi(820, 400, "Scapula", "肩胛骨", 12, INK, weight="600"); f.leader(870, 396, 960, 400, "#999")
    f.bi(770, 560, "Inferior angle tips back", "下角向后翘（前倾）", 12, "#8f4a3c", weight="600")
    f.bi(790, 690, "Coracoid pulled forward and down", "喙突被拉向前下方 →", 14, "#8f4a3c")
    f.bi(790, 736, "= protraction, depression, anterior tilt", "肩胛骨前伸、下降、前倾", 14, "#8f4a3c")
    f.bi(40, 700, "Rule: the bone moves toward the side of the joint axis that the line of pull crosses.", "规则：力线经过关节轴的哪一侧，骨头就向哪一侧转。", 14, INK)
    f.save("从力线推出动作")


def f07():
    f = Fig("07", 980, 1640, "Lung meridian of hand-taiyin: LU1–LU6", "手太阴肺经：今天的 6 个穴位（右侧，解剖学姿势前面观）")
    f.bi(38, 118, "Bone-proportional cun: axillary fold → cubital crease = 9 cun; cubital crease → wrist crease = 12 cun.",
         "骨度分寸：腋前纹头至肘横纹 9 寸；肘横纹至腕掌侧远端横纹 12 寸。", 15, INK, weight="400")
    f.g("translate(-360,0)")  # 底图坐标不变，整体左移，去掉左侧空白
    arm_base(f)
    # 肺经线：今天实线，明天虚线
    kz = LU_TODAY[5]
    f.path(f"M878,310 L878,270 C860,330 815,400 792,470 C780,520 771,555 770,590 L769,630 C772,700 785,780 790,830 L{kz[2]},{kz[3]}", RED, 3.4)
    f.path(f"M{kz[2]},{kz[3]} " + " ".join(f"L{x},{y:.0f}" for _, x, y in LU_LATER), "#c9a59c", 2.6, dash="7 6")
    for n, x, y in LU_LATER: f.circle(x, y, 7, "#c9a59c", "#fff", 2)
    for n, p, x, y in LU_TODAY: f.circle(x, y, 11, RED, "#fff", 3)
    # 寸尺：放在上肢内侧（观者右侧），不与穴位标签交叉
    RX = 900
    f.path(f"M{RX},{ARM_Y['fold']} L{RX},{ARM_Y['wrist']}", INK, 1.6, rough=False)
    hot = {("upper", 3), ("upper", 4), ("fore", 5)}
    for seg, n in (("upper", 9), ("fore", 12)):
        for i in range(n + 1):
            y = arm_y(seg, i)
            if seg == "fore" and i == 0: continue
            f.path(f"M{RX-8},{y} L{RX+8},{y}", INK, 1.4, rough=False)
            lab = "9 | 0" if (seg == "upper" and i == 9) else str(i)
            f.text(RX + 14, y + 5, lab, 15 if (seg, i) in hot else 13, RED if (seg, i) in hot else "#555", weight="700" if (seg, i) in hot else "400")
    f.text(RX + 14, ARM_Y["fold"] - 18, "寸 cun", 14, "#555", lang="zh-CN")
    for key, en, zh in [("fold", "Anterior axillary fold (0)", "腋前纹头（0 寸）"), ("elbow", "Cubital crease", "肘横纹"), ("wrist", "Distal wrist crease", "腕掌侧远端横纹")]:
        y = ARM_Y[key]; f.path(f"M722,{y} L{RX-10},{y}", "#8f8a7e", 1.1, dash="3 4", rough=False); f.bi(962, y - 2, en, zh, 15, "#555", weight="600")
    f.bi(962, 640, "Tianfu 3 cun, Xiabai 4 cun below the fold", "天府：腋前纹头下 3 寸；侠白：下 4 寸", 15, RED)
    f.bi(962, 720, "Upper arm = 9 cun", "上臂 = 9 寸", 14, "#777", weight="400")
    f.bi(962, arm_y("fore", 5), "Kongzui: 7 cun above the wrist crease", "孔最：腕横纹上 7 寸（= 肘横纹下 5 寸）", 15, RED)
    f.bi(962, arm_y("fore", 7.3), "Forearm = 12 cun", "前臂 = 12 寸", 14, "#777", weight="400")
    f.bi(962, arm_y("fore", 9), "Each segment is divided on its own,", "骨度分寸按段各自等分，", 13, "#777", weight="400")
    f.bi(962, arm_y("fore", 9) + 40, "so a forearm cun is shorter.", "所以前臂的 1 寸比上臂短。", 13, "#777", weight="400")
    # 胸部：旁开 6 寸
    f.path("M878,322 L878,372", "#8f8a7e", 1, dash="3 3", rough=False)
    f.arrow(f"M{(878+MID_X)/2},372 L882,372", "#555", 1.4, rough=False); f.arrow(f"M{(878+MID_X)/2},372 L{MID_X-4},372", "#555", 1.4, rough=False)
    f.bi((878 + MID_X) / 2, 396, "6 cun from the midline", "前正中线旁开 6 寸", 14, "#555", "middle")
    f.bi(948, 470 + 70, "Pectoralis major", "胸大肌", 14, "#b0705f", weight="600")
    # 穴位标签
    for n, p, x, y in LU_TODAY[:2]:
        f.leader(x + 12, y, 1112, y, RED, "3 3"); acu_box(f, 1120, y + 8, n, p, w=170)
    for (n, p, x, y), ly in zip(LU_TODAY[2:], (560, 662, 838, arm_y("fore", 5) + 8)):
        f.leader(x - 12, y, 612, ly - 7, RED, "3 3"); acu_box(f, 420, ly, n, p)
    # 结构标签（观者左侧）
    for (tx, ty), (px, py), en, zh, c in [((420, 178), (812, 226), "Clavicle", "锁骨", INK),
                                          ((420, 252), (846, 284), "Coracoid process (deep, palpable)", "喙突（深面，可摸到）", "#6f6656"),
                                          ((420, 338), (742, 340), "Deltoid", "三角肌", "#7d7362"),
                                          ((420, 440), (803, 432), "Cephalic vein (deltopectoral groove)", "头静脉（走在三角肌胸大肌间沟）", BLUE),
                                          ((420, 752), (806, 720), "Biceps brachii", "肱二头肌", "#9a7a5f"),
                                          ((420, 912), (752, 912), "Brachioradialis", "肱桡肌", "#9a7a5f")]:
        f.leader(tx + (230 if len(en) < 20 else 300), ty - 6, px, py, "#a8a294"); f.bi(tx, ty, en, zh, 15, c)
    f.bi(420, arm_y("fore", 10), "Grey: LU7–LU11, tomorrow", "灰点：列缺、经渠、太渊、鱼际、少商（明天学）", 14, "#a07d74")
    f.bi(1090, 160, "Anterior midline", "前正中线", 13, "#888", weight="400")
    f.end()
    f.save("手太阴肺经-前6穴")


def f08():
    f = Fig("08", 1300, 700, "What lies beneath Zhongfu and Yunmen", "中府、云门深面有什么：层次示意")
    f.bi(38, 116, "Not to scale; layers only, not needling depth or direction.", "不按比例，只表示层次，不表示进针深度或方向。", 14, RED, weight="400")
    stack(f, 40, 170, 560, "Zhongfu (LU1) · 1st intercostal space", "中府 · 第 1 肋间隙",
          [("Skin", "皮肤", 34, "#f6e7da", "#d8c3ae", ""), ("Subcutaneous tissue", "皮下组织", 40, "#fbf2e3", "#e0d2b8", ""),
           ("Pectoralis major", "胸大肌", 74, "#e9a596", RED, ""), ("Pectoralis minor", "胸小肌", 60, "#d9b3a6", "#8f4a3c", ""),
           ("Intercostal muscles", "肋间肌", 46, "#e2d5c0", "#b9a888", ""), ("Pleura", "胸膜", 24, "#f2c9c3", RED, "危险层"),
           ("Lung", "肺", 90, "#f7d9d4", RED, "")],
          "Danger: needling toward the midline can reach the pleura and lung.", "危险：向内深刺可能伤及胸膜和肺。")
    stack(f, 690, 170, 560, "Yunmen (LU2) · medial to the coracoid", "云门 · 喙突内缘",
          [("Skin", "皮肤", 34, "#f6e7da", "#d8c3ae", ""), ("Subcutaneous tissue (cephalic vein nearby)", "皮下组织（附近有头静脉）", 40, "#fbf2e3", "#e0d2b8", ""),
           ("Deltopectoral groove", "三角肌与胸大肌之间", 60, "#efe1d0", "#c9b296", ""), ("Clavipectoral fascia", "锁胸筋膜", 30, "#e6dccb", "#b9a888", ""),
           ("Axillary artery and vein, brachial plexus", "腋动静脉、臂丛", 74, "#f1d48c", GOLD, "神经血管"),
           ("Toward the pleural apex (medially)", "向内：靠近胸膜顶", 60, "#f2c9c3", RED, "危险方向")],
          "Danger: the neurovascular bundle lies deep; the pleura lies medial.", "危险：深面是神经血管束，内侧靠近胸膜。")
    f.save("中府云门-层次示意")


def build(out_dir):
    set_out(out_dir)
    f01()
    chest_oi("02", "pmaj", "Pectoralis major", "胸大肌", "pmaj", [(600, 98), (690, 300)], (270, 344), "clavicle, sternum, costal cartilages 1–6", "锁骨内侧半、胸骨、第 1–6 肋软骨", "lateral lip of the intertubercular groove", "结节间沟外侧唇", RED)
    chest_oi("03", "pmin", "Pectoralis minor", "胸小肌", "pmin", [(560, 216), (566, 264), (572, 314)], (345, 140), "ribs 3–5", "第 3–5 肋", "coracoid process", "喙突", "#8f4a3c")
    chest_oi("04", "sub", "Subclavius", "锁骨下肌", "sub", [(640, 118)], (480, 101), "1st rib and its cartilage", "第 1 肋及肋软骨", "underside of the middle third of the clavicle", "锁骨中 1/3 下面", "#b46a2c")
    f05(); f06(); f07(); f08()

if __name__ == "__main__":
    build(sys.argv[1] if len(sys.argv) > 1 else pathlib.Path(__file__).resolve().parent / "资源")
