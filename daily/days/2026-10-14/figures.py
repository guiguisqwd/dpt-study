#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Week 1 Wednesday 2026-10-14: a supraspinatus tendinopathy teaching case, and the suprascapular and axillary nerves.
Run via pipeline (figures step) or: python3 figures.py <out_dir>.
01 is new (the case's review points); 02 to 04 reuse the chapter figures of library/shoulder (DL-03)."""
import pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2]))
from engine.figlib import *

MUTE = "#6b706a"
AMBER = "#b8730f"
X0, STEP, AXIS_Y = 150, 90, 312          # week 0 of care at X0; one week = STEP px


def wx(week):
    return X0 + week * STEP


def lines(f, x, y, rows, gap=20):
    """rows: (text, size, colour, weight, lang); one line each, top to bottom."""
    for k, (t, size, col, weight, lang) in enumerate(rows):
        f.text(x, y + k * gap, t, size, col, "start", weight, lang)


def callout(f, x, y, w, h, col, fill, rows, gap=20):
    f.box(x, y, w, h, col, fill, sw=1.8)
    lines(f, x + 14, y + 26, rows, gap)


# ------------------------------------------------------------------ 01 review points of the teaching case
def f01():
    f = Fig("01", 1400, 700, "Teaching case: review points over 12 weeks of care", "教学案例：12 周保守治疗里的复查节点")
    # callouts above the axis
    callout(f, 30, 106, 330, 130, GOLD, "#fff8e6", [
        ("Week 0 · first visit", 16, INK, "700", "en"),
        ("Assess, explain, start exercise.", 15, INK, "400", "en"),
        ("No imaging is needed to start (BESS 2025).", 15, INK, "400", "en"),
        ("第 0 周 · 首诊：评估、解释、开始运动", 14, ZH, "400", "zh-CN"),
        ("开始治疗不需要影像（BESS 2025）", 14, ZH, "400", "zh-CN")], 22)
    callout(f, 378, 106, 330, 130, GREEN, "#f1f7ef", [
        ("Symptoms past 6 weeks", 16, INK, "700", "en"),
        ("Take steps at work; ultrasound can rule", 15, INK, "400", "en"),
        ("out a cuff tear if indicated (Diercks 2014).", 15, INK, "400", "en"),
        ("症状超过 6 周：在工作上采取措施；", 14, ZH, "400", "zh-CN"),
        ("必要时做超声排除肩袖撕裂", 14, ZH, "400", "zh-CN")], 22)
    callout(f, 726, 106, 330, 130, AMBER, "#fdf3e4", [
        ("No improvement by 6–8 weeks", 16, INK, "700", "en"),
        ("One subacromial steroid injection can", 15, INK, "400", "en"),
        ("be considered together (BESS 2025).", 15, INK, "400", "en"),
        ("6–8 周仍无改善：可以一起商量", 14, ZH, "400", "zh-CN"),
        ("做一次肩峰下类固醇注射", 14, ZH, "400", "zh-CN")], 22)
    callout(f, 1074, 106, 300, 130, BLUE, "#eef3fa", [
        ("Every 2 weeks · review", 16, INK, "700", "en"),
        ("Raise the load at each visit", 15, INK, "400", "en"),
        ("(Holmgren 2012).", 15, INK, "400", "en"),
        ("每 2 周复查一次，", 14, ZH, "400", "zh-CN"),
        ("每次复查时加负荷", 14, ZH, "400", "zh-CN")], 22)
    # leaders from the callouts to the axis
    f.leader(wx(0), 236, wx(0), AXIS_Y - 14, GOLD)
    f.leader(wx(3), 236, wx(3), AXIS_Y - 12, GREEN)
    f.leader(wx(7), 236, wx(7), AXIS_Y - 14, AMBER)
    # axis: weeks of care, with the weeks since the pain began underneath
    f.raw(f'<rect x="{wx(6)}" y="{AXIS_Y - 12}" width="{2 * STEP}" height="24" rx="6" fill="#f6dfb8" stroke="{AMBER}" stroke-width="1.2"/>')
    f.path(f"M{wx(0) - 20},{AXIS_Y} L{wx(12) + 30},{AXIS_Y}", INK, 2.4)
    for w in range(13):
        f.leader(wx(w), AXIS_Y - 6, wx(w), AXIS_Y + 6, INK)
        f.text(wx(w), AXIS_Y + 30, str(w), 15, INK, "middle", "700")
        f.text(wx(w), AXIS_Y + 52, str(w + 3), 13, MUTE, "middle")
    for w in (2, 4, 6, 8, 10, 12):
        f.circle(wx(w), AXIS_Y, 8, BLUE)
    f.circle(wx(0), AXIS_Y, 12, GOLD)
    f.circle(wx(3), AXIS_Y, 9, GREEN)
    f.circle(wx(12), AXIS_Y, 12, RED)
    f.text(wx(12) + 44, AXIS_Y + 30, "weeks of care", 13, INK, "start", "700")
    f.text(wx(12) + 44, AXIS_Y + 52, "since pain began", 13, MUTE)
    f.text(30, AXIS_Y + 30, "治疗周数", 13, INK, "start", "700", "zh-CN")
    f.text(30, AXIS_Y + 52, "发病周数", 13, MUTE, "start", "400", "zh-CN")
    # the exercise programme runs the whole time
    f.raw(f'<rect x="{wx(0)}" y="{AXIS_Y + 76}" width="{12 * STEP}" height="64" rx="10" fill="#e3f0ee" stroke="{TEAL}" stroke-width="1.6"/>')
    f.text(wx(0) + 18, AXIS_Y + 102, "Home exercise once or twice a day · pain while exercising up to 5/10, settled before the next session (Holmgren 2012)",
           15, INK, "start", "600")
    f.text(wx(0) + 18, AXIS_Y + 126, "每天在家练 1–2 次；练习时疼痛不超过 5/10，下次练习前要回落到练前水平（Holmgren 2012）", 14, ZH, "start", "400", "zh-CN")
    # week 12 below the programme
    f.leader(wx(12), AXIS_Y + 142, wx(12), AXIS_Y + 172, RED)
    callout(f, 764, AXIS_Y + 172, 610, 112, RED, "#fbefed", [
        ("Week 12 · no improvement: refer to secondary care (BESS 2025)", 16, INK, "700", "en"),
        ("Most exercise programmes show clinically significant change by 12 weeks (Littlewood 2015).", 14, INK, "400", "en"),
        ("第 12 周仍无改善：转专科（BESS 2025）", 14, ZH, "400", "zh-CN"),
        ("多数运动方案在 12 周内应见到有临床意义的改善（Littlewood 2015）", 14, ZH, "400", "zh-CN")], 23)
    # how to read the axis
    lines(f, 30, AXIS_Y + 196, [
        ("The patient had pain for 3 weeks before the first visit.", 14, MUTE, "400", "en"),
        ("BESS counts the 12 weeks as non-operative care; for", 14, MUTE, "400", "en"),
        ("6–8 weeks it does not say where the count starts.", 14, MUTE, "400", "en"),
        ("This figure counts both from the first visit.", 14, MUTE, "400", "en"),
        ("病人首诊前已经痛了 3 周。BESS 的 12 周指保守治疗的时长；", 13, MUTE, "400", "zh-CN"),
        ("6–8 周没有说从哪天算起。本图两者都从首诊算起。", 13, MUTE, "400", "zh-CN")], 21)
    p = f.save("案例复查时间线")
    svg = p.read_text(encoding="utf-8")
    svg = svg.replace("Schematic; pathway and layers are simplified.", "Teaching case, not a real patient; time points from the sources named.") \
             .replace("解剖示意；走行与层次经过简化。", "教学案例，不是真实病人；时间点取自图中注明的来源。")
    p.write_text(svg, encoding="utf-8")


# ------------------------------------------------------------------ 04 badge area and myotomes (redrawn: chapter figure 14's arm sketch is too abstract)
# Facts: chapter figure 14 and the axillary nerve paragraph of library/shoulder/content.json.
# Where the badge area sits ("the skin over the inferior portion of the deltoid"): TeachMeAnatomy, The Axillary Nerve (a chapter source).
ARM_L = ("M246,226 C238,300 246,380 256,460 C262,520 266,580 270,640 C272,680 274,720 278,760 "                  # posterior border, shoulder → forearm
         "L396,760 C396,720 398,680 400,646 C404,590 398,520 394,460 C390,380 404,300 414,232 ")              # anterior border, forearm → shoulder
CAP = "M246,226 C252,176 288,146 336,144 C380,142 414,170 414,232"                                            # top of the shoulder
DELT_L = ("M250,214 C258,170 292,150 334,148 C376,148 406,172 410,222 C402,300 380,370 344,438 "
          "C338,446 330,446 326,438 C296,370 264,300 250,214 Z")                                                  # deltoid, apex at the tuberosity
BADGE = "M286,330 C304,312 362,312 380,330 C376,372 360,408 344,432 C336,442 328,442 322,432 C306,408 290,372 286,330 Z"


def f04():
    f = Fig("04", 1400, 900, "Axillary nerve: the badge area and the C5 and C6 myotomes", "腋神经：徽章区与 C5、C6 肌节")
    f.bi(40, 120, "Right arm, lateral view; the front of the body is on the right.", "右上肢外侧面观；身体前方在右边。", 15, MUTE, weight="400")
    f.g("translate(0,56)")
    # side of the trunk and neck, behind the arm (open strokes; the arm covers them)
    f.path("M276,100 C270,130 250,160 226,186 C206,214 198,300 198,400 C198,500 208,600 222,700", "#b9b2a3", 1.8, rough=False)
    f.path("M392,100 C396,140 410,180 430,206 C456,250 470,330 470,420 C470,500 462,600 452,700", "#b9b2a3", 1.8, rough=False)
    # arm, deltoid, badge area
    f.path(ARM_L + "Z", "none", 0, "#fffaf1", rough=False)
    f.path(DELT_L, "#a59b88", 1.6, "#ece4d4")
    f.raw(f'<path d="{BADGE}" fill="#9fb9de" fill-opacity="0.75" stroke="{BLUE}" stroke-width="2.2"/>')
    post, ant = ARM_L.split("L396,760")
    f.path(post, INK, 2.2, rough=False)                                                                     # posterior border
    f.path("M396,760" + ant, INK, 2.2, rough=False)                                                         # anterior border
    f.path(CAP, INK, 2.2, rough=False)
    f.path("M278,760 L396,760", INK, 1.4, dash="6 6", rough=False)                                         # forearm cut: the arm continues
    f.path("M300,170 C322,160 352,158 384,166", BONE_E, 1.4, dash="4 4", rough=False)                      # acromion under the skin
    f.path("M268,640 C300,652 360,654 398,642", "#b8ae9c", 1.2, rough=False)                                # elbow crease level
    # labels with leaders
    f.leader(384, 166, 470, 128, INK); f.bi(476, 124, "Acromion (felt under the skin)", "肩峰（皮下可触及）", 15, INK)
    f.leader(390, 220, 520, 236, "#8a7f6c"); f.bi(526, 232, "Deltoid", "三角肌", 15, "#6b604c")
    f.leader(372, 372, 520, 372, BLUE); f.bi(526, 360, "Regimental badge area", "徽章区", 17, BLUE, weight="700")
    f.bi(526, 410, "Skin over the inferior part of Deltoid", "三角肌下部表面的皮肤", 14, INK, weight="400")
    f.leader(344, 438, 520, 470, "#8a7f6c"); f.bi(526, 466, "Deltoid tuberosity: Deltoid inserts here", "三角肌粗隆：三角肌止于此", 14, "#6b604c", weight="400")
    f.text(200, 690, "Posterior", 14, MUTE, "end"); f.text(200, 708, "后", 13, MUTE, "end", lang="zh-CN")
    f.text(470, 690, "Anterior", 14, MUTE); f.text(470, 708, "前", 13, MUTE, lang="zh-CN")
    f.text(410, 650, "Elbow", 13, MUTE); f.text(452, 650, "肘", 12, MUTE, lang="zh-CN")
    f.end()
    # three panels on the right
    X, W = 820, 548
    callout(f, X, 150, W, 178, BLUE, "#eef3fa", [
        ("Sensory: a nerve territory, not a dermatome", 16, INK, "700", "en"),
        ("The superior lateral cutaneous nerve of the arm is a cutaneous", 14, INK, "400", "en"),
        ("branch of the axillary nerve: the posterior branch continues as it.", 14, INK, "400", "en"),
        ("Peripheral nerve territory ≠ dermatome. The lateral upper arm", 14, INK, "400", "en"),
        ("overlaps the C5 dermatome.", 14, INK, "400", "en"),
        ("感觉：这是周围神经分布区，不是皮节。腋神经后支延续为臂外上侧皮神经。", 13, ZH, "400", "zh-CN"),
        ("周围神经分布区不等同于皮节；上臂外侧区域与 C5 皮节重叠。", 13, ZH, "400", "zh-CN")], 22)
    callout(f, X, 348, W, 140, GREEN, "#f1f7ef", [
        ("Key myotomes · C5 and C6", 16, INK, "700", "en"),
        ("C5: shoulder abduction. C6: elbow flexion and wrist extension.", 14, INK, "400", "en"),
        ("These movements receive overlapping segmental contributions.", 14, INK, "400", "en"),
        ("代表性肌节：C5 肩外展；C6 屈肘和伸腕。", 13, ZH, "400", "zh-CN"),
        ("这些动作通常接受相邻神经节段的共同支配。", 13, ZH, "400", "zh-CN")], 22)
    callout(f, X, 508, W, 140, RED, "#fbefed", [
        ("Axillary nerve injury", 16, INK, "700", "en"),
        ("Deltoid weakness and badge-area sensory loss.", 14, INK, "400", "en"),
        ("Risk: a surgical-neck fracture or an anterior shoulder dislocation.", 14, INK, "400", "en"),
        ("腋神经损伤：三角肌无力和徽章区感觉减退。", 13, ZH, "400", "zh-CN"),
        ("风险因素：肱骨外科颈骨折或肩关节前脱位。", 13, ZH, "400", "zh-CN")], 22)
    lines(f, X, 686, [
        ("Facts: this week's chapter (figure 14 and the axillary nerve paragraph).", 13, MUTE, "400", "en"),
        ("Where the badge area lies: TeachMeAnatomy, The Axillary Nerve.", 13, MUTE, "400", "en"),
        ("依据：本周章节（图 14 与腋神经一段）；徽章区位置：TeachMeAnatomy「腋神经」。", 12, MUTE, "400", "zh-CN")], 19)
    p = f.save("腋神经徽章区与肌节")
    svg = p.read_text(encoding="utf-8")
    svg = svg.replace("Schematic; pathway and layers are simplified.", "Schematic; the outline of the badge area is drawn approximately.") \
             .replace("解剖示意；走行与层次经过简化。", "示意图；徽章区的边界为大致画法。")
    p.write_text(svg, encoding="utf-8")


def build(out_dir):
    set_out(out_dir)
    f01()
    copy_library_figure("shoulder", "16-肩胛上神经-后肩解剖", out_dir, "02-肩胛上神经后面观")
    copy_library_figure("shoulder", "17-腋神经-四边孔解剖", out_dir, "03-腋神经与四边孔")
    f04()


if __name__ == "__main__":
    build(sys.argv[1] if len(sys.argv) > 1 else pathlib.Path(__file__).resolve().parent / "资源")
