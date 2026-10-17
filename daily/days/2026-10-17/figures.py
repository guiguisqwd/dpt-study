#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Week 1 Saturday 2026-10-17: the weekly quiz (new and old mixed) and spaced review.
Run via pipeline (figures step) or: python3 figures.py <out_dir>.
Both figures are self-test versions of this week's figures, not new anatomy:
01 draws Tuesday's lettered scapula and humerus (days/2026-10-13/figures.py), renumbered, plus the superior angle (Monday, TE15);
02 draws Thursday's lettered view into the glenoid (its figure 03, days/2026-10-15/figures.py) as figure 02."""
import importlib.util, pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2]))
from engine.figlib import *

DAY_DIR = pathlib.Path(__file__).resolve().parent    # after the star import: figlib has its own HERE

MUTE = "#6b706a"


def _day(date):
    """Load another day's figures.py so its drawing code is reused, not copied."""
    spec = importlib.util.spec_from_file_location("figures_" + date.replace("-", "_"), DAY_DIR.parent / date / "figures.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


TUE = _day("2026-10-13")
THU = _day("2026-10-15")

# ------------------------------------------------------------------ 01 numbered landmarks
# number, base point on the bone (Tuesday's coordinates), marker offset (dx, dy) in canvas px
NUM_POST = [
    ("1", (480, 66), (0, -40)),      # acromion
    ("2", (200, 98), (0, 0)),        # supraspinous fossa
    ("3", (200, 320), (0, 0)),       # infraspinous fossa
    ("4", (362, 156), (-30, 46)),    # spinoglenoid notch
    ("5", (304, 82), (-18, -46)),    # suprascapular notch
    ("6", (85, 72), (-44, 12)),      # superior angle
    ("7", (300, 352), (38, 14)),     # lateral border
    ("8", (172, 598), (-36, 22)),    # inferior angle
    ("9", (628, 206), (40, -6)),     # greater tubercle
    ("10", (582, 305), (44, 4)),     # surgical neck
]
NUM_ANT = [
    ("11", (390, 26), (0, -40)),     # coracoid process
    ("12", (230, 340), (0, 0)),      # subscapular fossa
    ("13", (548, 268), (40, 34)),    # lesser tubercle
    ("14", (568, 340), (-46, 24)),   # intertubercular groove
]


def num_marker(f, x, y, label):
    f.circle(x, y, 17, "#fffdf7", INK, 2.2)
    f.text(x, y + 6, label, 16, INK, "middle", "700")


def f01():
    f = Fig("01", 1500, 1000, "Self-test: numbered landmarks of the right scapula and humerus", "自测：右侧肩胛骨与肱骨上的编号")
    f.bi(40, 118, "Tuesday's lettered drawing, renumbered; number 6 (the superior angle, Monday's TE15) is new. Answer the Part 3 questions with these numbers.",
         "周二那张字母图改用编号；6 号（肩胛骨上角，周一的天髎）是新加的。第 3 部分的题目用这些编号作答。", 15, INK, weight="400")
    sa, xa, ya = 0.92, 40, 170               # posterior view: subject's right is the viewer's right
    sb, xb, yb = 0.92, 1460, 170             # anterior view: mirrored, so the lateral side is on the viewer's left
    pa = lambda x, y: (xa + sa * x, ya + sa * y)
    pb = lambda x, y: (xb - sb * x, yb + sb * y)
    f.bi(60, 175, "Posterior view", "后面观", 20, INK, weight="700")
    f.bi(830, 175, "Anterior view", "前面观", 20, INK, weight="700")
    f.g(f"translate({xa},{ya}) scale({sa})"); TUE.bones(f, "post"); f.end()
    f.g(f"translate({xb},{yb}) scale({-sb},{sb})"); TUE.bones(f, "ant"); f.end()
    for pts, p in ((NUM_POST, pa), (NUM_ANT, pb)):
        for label, (bx, by), (dx, dy) in pts:
            x, y = p(bx, by)
            if dx or dy:
                f.leader(x, y, x + dx, y + dy, "#555")
                f.circle(x, y, 3.5, INK, INK, 0)
            num_marker(f, x + dx, y + dy, label)
    f.bi(60, 880, "Exploded view: the humerus is drawn a little away from the scapula so the glenoid and the notches show.",
         "分离示意：肱骨画得离肩胛骨稍远，好看清关节盂和两个切迹。", 14, MUTE, weight="400")
    f.bi(60, 920, "In the anterior view the glenoid is seen edge-on; it faces laterally toward the humeral head.",
         "前面观里关节盂只看到侧边；它朝外侧，对着肱骨头。", 14, MUTE, weight="400")
    p = f.save("肩胛骨与肱骨-编号自测")
    THU.foot(p, "Schematic: bone outlines are simplified; only the landmarks asked about are numbered.",
             "示意图：骨的轮廓经过简化；只给题目要问的标志编号。")


# ------------------------------------------------------------------ 02 lettered capsule and ligaments
def f02():
    f = Fig("02", 1400, 1000, "Self-test: lettered structures around the right glenoid", "自测：右侧关节盂周围的字母结构")
    f.bi(38, 116, "Thursday's figure 03: the right socket seen from the side, humerus removed. Front of the body on the right, top of the shoulder at the top.",
         "周四的图 03：从外侧看进右侧关节盂（肱骨已移除）。身体前方在右边，肩顶在上方。", 15, MUTE, weight="400")
    THU.glenoid_face(f)
    f.bi(THU.CX, THU.CY - 4, "Glenoid cavity", "关节盂", 15, MUTE, "middle", "600", gap=19, zsize=13)
    THU.put_labels(f, THU.GLENOID_LABELS, 462, 1010, True)
    p = f.save("盂肱关节囊与韧带-字母自测")
    THU.foot(p, "Schematic: the capsule and cuff tendons are cut close to the glenoid; sizes and band widths are simplified.",
             "示意图：关节囊和肩袖肌腱在靠近关节盂处切断；大小和韧带宽度经过简化。")


def build(out_dir):
    set_out(out_dir)
    f01()
    f02()


if __name__ == "__main__":
    build(sys.argv[1] if len(sys.argv) > 1 else DAY_DIR / "资源")
