#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Week 1 Friday 2026-10-16: seven rotator cuff special tests, and force couples with scapulohumeral rhythm.
Run via pipeline (figures step) or: python3 figures.py <out_dir>.
01 to 04 are new schematic drawings of the test positions (the chapter only names the tests); the positions follow the
original descriptions opened for this pack (see content.sources). 05 plots the accuracy numbers quoted in chapter 1.
06 is redrawn from the chapter's figures 10 and 11; 07 is the chapter's figure 12, reused unchanged (DL-03)."""
import math, pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2]))
from engine.figlib import *
from engine.figlib.library import copy_library_figure

MUTE = "#6b706a"
SKIN, EDGE = "#fbf1e4", "#3d3a35"            # patient
ARM = "#f2c6b4"                              # the arm being tested
EXAM, EXAM_E = "#d9d5cc", "#6f6b63"          # examiner's hands
PALE, PALE_E = "#ece8df", "#b3ada1"          # start or end position
SW = 2.2
FOOT_EN, FOOT_ZH = "Schematic of the test position; body shapes are simplified.", "检查体位示意；人体形状经过简化。"


def foot(p, en, zh):
    svg = p.read_text(encoding="utf-8")
    svg = svg.replace("Schematic; pathway and layers are simplified.", en).replace("解剖示意；走行与层次经过简化。", zh)
    p.write_text(svg, encoding="utf-8")


def P(p, ang, length):
    """Point at distance length from p along ang (degrees; 0 = viewer's right, 90 = down)."""
    a = math.radians(ang)
    return (p[0] + math.cos(a) * length, p[1] + math.sin(a) * length)


# ------------------------------------------------------------------ silhouettes drawn as unions:
# every part is drawn twice, first as an outline-coloured shape with a thick stroke, then filled on top,
# so overlapping parts merge into one body with a single outline.
class Body:
    def __init__(s, f, fill=SKIN, edge=EDGE, op=None):
        s.f, s.fill, s.edge, s.op, s.parts = f, fill, edge, op, []

    def seg(s, a, b, ra, rb):
        """Tapered capsule from point a (radius ra) to point b (radius rb)."""
        dx, dy = b[0] - a[0], b[1] - a[1]
        L = math.hypot(dx, dy) or 1
        nx, ny = -dy / L, dx / L
        d = (f"M{a[0] + nx * ra:.1f},{a[1] + ny * ra:.1f} L{b[0] + nx * rb:.1f},{b[1] + ny * rb:.1f} "
             f"L{b[0] - nx * rb:.1f},{b[1] - ny * rb:.1f} L{a[0] - nx * ra:.1f},{a[1] - ny * ra:.1f} Z")
        s.parts += [("path", d), ("circle", (a[0], a[1], ra)), ("circle", (b[0], b[1], rb))]
        return s

    def ell(s, cx, cy, rx, ry, rot=0):
        s.parts.append(("ellipse", (cx, cy, rx, ry, rot)))
        return s

    def shape(s, d):
        s.parts.append(("path", d))
        return s

    def _el(s, kind, v, fill, stroke, sw):
        st = f'fill="{fill}"' + (f' stroke="{stroke}" stroke-width="{sw}" stroke-linejoin="round"' if stroke else "")
        if kind == "path":
            return f'<path d="{v}" {st}/>'
        if kind == "circle":
            return f'<circle cx="{v[0]:.1f}" cy="{v[1]:.1f}" r="{v[2]:.1f}" {st}/>'
        cx, cy, rx, ry, rot = v
        return f'<ellipse cx="{cx:.1f}" cy="{cy:.1f}" rx="{rx:.1f}" ry="{ry:.1f}" transform="rotate({rot:.1f} {cx:.1f} {cy:.1f})" {st}/>'

    def draw(s):
        op = f' opacity="{s.op}"' if s.op is not None else ""
        s.f.raw(f"<g{op}>" + "".join(s._el(k, v, s.edge, s.edge, SW * 2) for k, v in s.parts)
                + "".join(s._el(k, v, s.fill, None, 0) for k, v in s.parts) + "</g>")


def arm(f, pts, fill=ARM, pale=False, hand_ang=None, thumb=None, r=(15, 12.5, 10.5), hs=1.0):
    """Arm through shoulder, elbow, wrist; a hand at the wrist pointing along hand_ang; optional thumb direction
    (the thumb is drawn as its own part so it stays visible)."""
    fill, edge = (PALE, PALE_E) if pale else (fill, EDGE)
    b = Body(f, fill, edge)
    sh, el, wr = pts
    b.seg(sh, el, r[0], r[1]).seg(el, wr, r[1], r[2])
    hc = None
    if hand_ang is not None:
        hc = P(wr, hand_ang, 17 * hs)
        b.ell(hc[0], hc[1], 20 * hs, 14 * hs, hand_ang)
    b.draw()
    if hc is not None and thumb is not None:
        t = Body(f, fill, edge)
        base = P(hc, hand_ang + 180, 6 * hs)
        t.seg(P(base, thumb, 8 * hs), P(base, thumb, 27 * hs), 6.5 * hs, 6 * hs)
        t.draw()
        f.raw(f'<circle cx="{P(base, thumb, 27 * hs)[0]:.1f}" cy="{P(base, thumb, 27 * hs)[1]:.1f}" r="{3.2 * hs:.1f}" fill="{edge}" opacity="0.55"/>')
    return hc


def exam_hand(f, x, y, ang=0, s=1.0, op=None):
    """Examiner's hand: a mitt centred at (x, y); the fingers point along ang."""
    b = Body(f, EXAM, EXAM_E, op)
    tip, base = P((x, y), ang, 26 * s), P((x, y), ang + 180, 22 * s)
    b.seg(base, tip, 16 * s, 13 * s)
    b.seg(P(base, ang - 70, 6 * s), P(base, ang - 30, 30 * s), 6.5 * s, 5.5 * s)      # thumb
    b.draw()


def head(f, cx, cy, r=36, face=None):
    """Head; face = None (front), +1 or -1 (profile looking right or left), or 'up' (seen from above, nose to the top)."""
    b = Body(f)
    b.ell(cx, cy, r, r)
    if face in (1, -1):
        b.shape(f"M{cx + face * (r - 6):.1f},{cy - 10:.1f} L{cx + face * (r + 9):.1f},{cy + 5:.1f} L{cx + face * (r - 4):.1f},{cy + 10:.1f} Z")
    elif face == "up":
        b.shape(f"M{cx - 8:.1f},{cy - r + 4:.1f} L{cx:.1f},{cy - r - 12:.1f} L{cx + 8:.1f},{cy - r + 4:.1f} Z")
    b.draw()


def trunk_front(f, cx, top, h=230):
    """Upper body from the front (patient faces the viewer, so the patient's right side is on the viewer's LEFT).
    top = base of the neck. Returns (right shoulder joint, left shoulder joint)."""
    b = Body(f)
    b.shape(f"M{cx - 17},{top - 26} L{cx + 17},{top - 26} L{cx + 17},{top} L{cx - 17},{top} Z")
    b.shape(f"M{cx - 17},{top - 2} C{cx - 40},{top + 6} {cx - 66},{top + 10} {cx - 84},{top + 20} "
            f"C{cx - 104},{top + 30} {cx - 108},{top + 58} {cx - 98},{top + 80} L{cx - 88},{top + 102} "
            f"C{cx - 86},{top + 150} {cx - 78},{top + h - 40} {cx - 76},{top + h} L{cx + 76},{top + h} "
            f"C{cx + 78},{top + h - 40} {cx + 86},{top + 150} {cx + 88},{top + 102} L{cx + 98},{top + 80} "
            f"C{cx + 108},{top + 58} {cx + 104},{top + 30} {cx + 84},{top + 20} C{cx + 66},{top + 10} {cx + 40},{top + 6} {cx + 17},{top - 2} Z")
    b.draw()
    head(f, cx, top - 60)
    return (cx - 86, top + 46), (cx + 86, top + 46)


def trunk_side(f, cx, top, face=1, head_dx=0):
    """Upper body seen from the patient's right side, chest toward the viewer's right (face=1).
    top = base of the neck. Returns the right shoulder joint."""
    k = face
    b = Body(f)
    b.shape(f"M{cx - 16 * k},{top - 28} L{cx + 14 * k},{top - 28} L{cx + 16 * k},{top + 4} L{cx - 18 * k},{top + 4} Z")
    b.shape(f"M{cx - 18 * k},{top} C{cx - 44 * k},{top + 6} {cx - 54 * k},{top + 40} {cx - 52 * k},{top + 90} "
            f"C{cx - 50 * k},{top + 150} {cx - 60 * k},{top + 220} {cx - 50 * k},{top + 270} L{cx - 46 * k},{top + 330} "
            f"L{cx + 50 * k},{top + 330} C{cx + 62 * k},{top + 280} {cx + 66 * k},{top + 230} {cx + 54 * k},{top + 190} "
            f"C{cx + 66 * k},{top + 150} {cx + 70 * k},{top + 90} {cx + 50 * k},{top + 40} C{cx + 38 * k},{top + 14} {cx + 24 * k},{top + 4} {cx + 16 * k},{top} Z")
    b.draw()
    head(f, cx + (2 + head_dx) * k, top - 62, face=k)
    return (cx - 2 * k, top + 48)


def trunk_top(f, cx, cy):
    """Patient seen from above, facing the top of the page: the patient's right is on the viewer's RIGHT.
    Returns (right shoulder, left shoulder)."""
    b = Body(f)
    b.shape(f"M{cx - 120},{cy + 6} C{cx - 124},{cy - 30} {cx - 70},{cy - 44} {cx},{cy - 44} C{cx + 70},{cy - 44} {cx + 124},{cy - 30} {cx + 120},{cy + 6} "
            f"C{cx + 116},{cy + 40} {cx + 70},{cy + 50} {cx},{cy + 50} C{cx - 70},{cy + 50} {cx - 116},{cy + 40} {cx - 120},{cy + 6} Z")
    b.draw()
    head(f, cx, cy + 2, 38, face="up")
    return (cx + 100, cy + 2), (cx - 100, cy + 2)


def arc_arrow(f, c, r, a0, a1, col, w=3.2, dash=None):
    """Circular arrow around c from angle a0 to a1 (degrees, screen coordinates: 0 = right, 90 = down)."""
    x0, y0 = P(c, a0, r); x1, y1 = P(c, a1, r)
    large = 1 if abs(a1 - a0) > 180 else 0
    sweep = 1 if a1 > a0 else 0
    f.arrow(f"M{x0:.1f},{y0:.1f} A{r},{r} 0 {large} {sweep} {x1:.1f},{y1:.1f}", col, w, dash=dash)


def straight(f, a, b, col, w=3.4):
    f.arrow(f"M{a[0]:.1f},{a[1]:.1f} L{b[0]:.1f},{b[1]:.1f}", col, w)


def legend(f, x, y):
    f.markers = getattr(f, "markers", set()) | {RED, BLUE}
    f.raw(f'<line x1="{x}" y1="{y}" x2="{x + 40}" y2="{y}" stroke="{RED}" stroke-width="3.4" marker-end="url(#{f.id("m" + RED.strip("#"))})"/>')
    f.bi(x + 54, y + 5, "Examiner pushes or moves", "检查者施力或移动", 14, INK, weight="400")
    f.raw(f'<line x1="{x + 300}" y1="{y}" x2="{x + 340}" y2="{y}" stroke="{BLUE}" stroke-width="3.4" marker-end="url(#{f.id("m" + BLUE.strip("#"))})"/>')
    f.bi(x + 354, y + 5, "Patient pushes or holds", "病人用力或保持", 14, INK, weight="400")
    exam_hand(f, x + 640, y, 0, 0.62)
    f.bi(x + 672, y + 5, "Examiner's hand", "检查者的手", 14, INK, weight="400")
    arm(f, [(x + 880, y), (x + 900, y), (x + 918, y)], pale=True, r=(8, 8, 8))
    f.bi(x + 940, y + 5, "Start or end position", "起始或结束位置", 14, INK, weight="400")


def panel_title(f, x, y, en, zh, col=INK):
    f.bi(x, y, en, zh, 20, col, gap=26, zsize=16)


def note(f, x, y, en, zh, col=MUTE, size=14):
    f.bi(x, y, en, zh, size, col, weight="400")


# ------------------------------------------------------------------ 01 empty can and full can (supraspinatus)
def scap_plane_inset(f, x, y):
    """Seen from above: the scapular plane lies about 30° forward of the coronal plane."""
    f.bi(x, y, "Seen from above: where the arms point", "从上往下看：手臂指向哪里", 16, INK)
    cx, cy = x + 290, y + 150
    f.path(f"M{cx - 250},{cy} L{cx + 250},{cy}", GREY, 1.6, dash="7 6", rough=False)
    f.bi(cx + 150, cy + 34, "Coronal plane", "冠状面", 13, MUTE, weight="400")
    rs, ls = trunk_top(f, cx, cy)
    for sh, ang in ((rs, -30), (ls, -150)):
        arm(f, [sh, P(sh, ang, 80), P(sh, ang, 150)], hand_ang=ang, r=(13, 11, 9.5), hs=0.8)
    a = P(rs, -30, 118)
    f.path(f"M{rs[0] + 118:.1f},{rs[1]:.1f} A118,118 0 0 0 {a[0]:.1f},{a[1]:.1f}", RED, 2.2, rough=False)
    f.text(rs[0] + 124, rs[1] - 22, "30°", 16, RED, "start", "700")
    f.bi(x, cy + 86, "Scapular plane: about 30° in front of the coronal plane.", "肩胛平面：在冠状面前方约 30°。", 14, INK, weight="400")
    f.bi(x, cy + 124, "In this small drawing the front of the body faces the top.", "这张小图里身体前方朝上。", 13, MUTE, weight="400")


def can_panel(f, ox, thumb_down):
    cx, top = ox, 400
    rs, ls = trunk_front(f, cx, top, 200)
    for sh, k in ((rs, -1), (ls, 1)):
        el = (sh[0] + k * 100, sh[1] - 3)
        wr = (el[0] + k * 92, el[1] - 2)
        hc = arm(f, [sh, el, wr], hand_ang=0 if k == 1 else 180, thumb=90 if thumb_down else -90)
        hx = wr[0] - k * 30
        exam_hand(f, hx, wr[1] - 24, 180 if k == 1 else 0, 0.8)
        straight(f, (hx, wr[1] - 112), (hx, wr[1] - 50), RED)
        straight(f, (wr[0] - k * 82, wr[1] + 96), (wr[0] - k * 82, wr[1] + 26), BLUE)
        lab = ("thumb down", "拇指朝下") if thumb_down else ("thumb up", "拇指朝上")
        tip = P(P(hc, 180 if k == 1 else 0, 6), 90 if thumb_down else -90, 27)
        if k == -1:
            ty = tip[1] + (34 if thumb_down else -40)
            f.leader(tip[0], tip[1] + (6 if thumb_down else -6), tip[0] + 6, ty - 14 if thumb_down else ty + 8)
            f.bi(tip[0] - 30, ty + (4 if thumb_down else -10), lab[0], lab[1], 13, RED, weight="600")
    return rs


def f01():
    f = Fig("01", 1400, 1000, "Empty can and full can: supraspinatus", "空罐试验与满罐试验：冈上肌")
    legend(f, 40, 118)
    for k, (down, ttl, sub) in enumerate([
            (True, ("Empty can: thumbs point down", "空罐：拇指朝下"), ("Arms at 90° in the scapular plane, fully internally rotated", "手臂在肩胛平面抬到 90°，充分内旋")),
            (False, ("Full can: thumbs point up", "满罐：拇指朝上"), ("Same position, but the arms are turned out about 45° (external rotation)", "体位相同，但手臂外旋约 45°"))]):
        ox = 350 + k * 700
        panel_title(f, ox - 300, 192, *ttl)
        note(f, ox - 300, 252, *sub)
        can_panel(f, ox, down)
    f.path("M700,180 L700,640", "#ddd8cc", 1.4, rough=False)
    note(f, 50, 690, "The examiner pushes both arms down at the same time; the patient resists. Compare the two sides.",
         "检查者同时向下压两侧手臂，病人对抗。两侧对比。", INK, 15)
    scap_plane_inset(f, 760, 672)
    foot(f.save("空罐与满罐试验"), FOOT_EN, FOOT_ZH)


# ------------------------------------------------------------------ 02 Neer and Hawkins-Kennedy (impingement)
def neer_panel(f, ox):
    cx, top = ox, 470
    sh = trunk_side(f, cx, top, 1, head_dx=-12)
    arm(f, [sh, P(sh, 90, 110), P(sh, 90, 205)], pale=True, hand_ang=90)            # start: arm by the side
    up = -64                                                                         # passively raised forward, near the end of range
    el = P(sh, up, 112); wr = P(el, up, 98)
    arc_arrow(f, sh, 175, 78, -52, RED)
    arm(f, [sh, el, wr], hand_ang=up)
    exam_hand(f, sh[0] - 44, sh[1] - 50, 25, 0.85)                                  # holds the scapula down from behind
    straight(f, (sh[0] - 52, sh[1] - 150), (sh[0] - 50, sh[1] - 84), RED)
    exam_hand(f, wr[0] - 4, wr[1] + 30, -150, 0.8)                                  # raises the arm at the wrist
    return sh, el, wr


def hk_side_inset(f, x, y, s=0.5):
    """Small side view of the Hawkins-Kennedy start position: shoulder flexed 90°, elbow bent 90°, forearm up."""
    f.raw(f'<g transform="translate({x},{y}) scale({s})">')
    sh = trunk_side(f, 0, 0, 1, head_dx=-12)
    el = P(sh, 0, 112)
    arm(f, [sh, el, P(el, -90, 98)], hand_ang=-90)
    f.raw("</g>")


def hk_panel(f, ox):
    cx, top = ox, 500
    rs, ls = trunk_front(f, cx, top, 200)
    arm(f, [ls, P(ls, 86, 105), P(ls, 88, 200)], fill=SKIN, hand_ang=88)              # the other arm rests
    el = (rs[0] + 6, rs[1] + 26)                                                     # upper arm points toward the viewer
    start = P(el, -90, 104); end = P(el, 28, 104)
    arm(f, [el, P(el, -90, 52), start], pale=True, hand_ang=-90, r=(17, 13, 10.5))
    arm(f, [rs, P(rs, 70, 14), el], r=(16, 18, 21))
    arm(f, [el, P(el, 28, 52), end], hand_ang=28, r=(19, 13, 10.5))
    arc_arrow(f, el, 100, -78, 2, RED)
    exam_hand(f, el[0] - 30, el[1] + 40, -55, 0.8)                                  # supports the elbow from below
    exam_hand(f, end[0] + 38, end[1] - 8, 200, 0.8)                                  # turns the forearm down
    return rs, el, start, end


def f02():
    f = Fig("02", 1400, 960, "Neer sign and Hawkins-Kennedy test: provoking pain under the acromion", "Neer 征与 Hawkins-Kennedy 试验：在肩峰下诱发疼痛")
    legend(f, 40, 118)
    panel_title(f, 50, 192, "Neer sign (side view)", "Neer 征（侧面观）")
    note(f, 50, 252, "One hand presses down on the top of the shoulder so the scapula cannot move;",
         "一只手向下按住肩顶，不让肩胛骨移动；")
    note(f, 50, 290, "the other forcibly raises the arm.", "另一只手用力把手臂抬起来。")
    sh, el, wr = neer_panel(f, 300)
    f.bi(wr[0] + 40, wr[1] - 6, "Raised passively", "被动抬高", 14, RED)
    f.bi(40, 340, "Presses down on the clavicle and acromion", "向下按住锁骨和肩峰", 14, RED)
    note(f, 50, 872, "Neer test: repeat after a subacromial injection; positive if the pain is gone.",
         "Neer 试验：肩峰下注射后重复这个动作，疼痛消失为阳性。", INK, 14)
    panel_title(f, 750, 192, "Hawkins-Kennedy test (front view)", "Hawkins-Kennedy 试验（前面观）")
    note(f, 750, 252, "Shoulder and elbow are placed at 90° of flexion;",
         "检查者把肩和肘都放到屈曲 90°；")
    note(f, 750, 290, "the examiner then forcibly turns the shoulder inward.", "然后用力把肩向内旋转。")
    rs, hel, start, end = hk_panel(f, 990)
    f.leader(start[0] - 16, start[1] + 26, 836, 410)
    f.bi(740, 380, "Start: forearm points up", "开始：前臂朝上", 14, INK)
    f.bi(1034, 456, "Internal rotation", "内旋", 15, RED)
    f.leader(hel[0] - 6, hel[1] + 20, 860, 700)
    f.bi(740, 720, "Upper arm points toward you", "上臂朝向读者", 14, INK)
    note(f, 740, 768, "That is, the shoulder is flexed to 90°.", "也就是肩前屈 90°。", MUTE, 13)
    f.bi(1170, 312, "Start, seen from the side", "起始体位（侧面观）", 14, INK)
    hk_side_inset(f, 1250, 392)
    f.path("M700,180 L700,800", "#ddd8cc", 1.4, rough=False)
    foot(f.save("Neer与Hawkins-Kennedy试验"), FOOT_EN, FOOT_ZH)


# ------------------------------------------------------------------ 03 external rotation lag sign and hornblower sign
def lag_panel(f, tx, ty, sc=1.35):
    """Seen from above, patient facing the top of the page; the right arm is tested. Drawn at local (0, 0) and
    scaled; returns a function mapping local points to figure points."""
    T = lambda q: (tx + sc * q[0], ty + sc * q[1])
    f.raw(f'<g transform="translate({tx},{ty}) scale({sc})">')
    rs, ls = trunk_top(f, 0, 0)
    el = (rs[0] + 34, rs[1] + 6)                       # elbow slightly away from the side (about 20° elevation)
    L = 128
    placed, lag = -14, -58                             # forward = -90, lateral = 0
    arm(f, [el, P(el, placed, L / 2), P(el, placed, L)], pale=True, hand_ang=placed, r=(13, 11.5, 10))
    b = Body(f, ARM); b.seg(rs, el, 16, 14); b.draw()
    arm(f, [el, P(el, lag, L / 2), P(el, lag, L)], hand_ang=lag, r=(13, 11.5, 10))
    exam_hand(f, el[0] + 14, el[1] + 34, 160, 0.75)                                      # keeps holding the elbow
    exam_hand(f, *P(el, placed, L + 92), placed + 180, 0.75, op=0.45)                     # has let go of the wrist
    r = L + 58
    a0, a1 = P(el, placed - 3, r), P(el, lag + 4, r)
    f.arrow(f"M{a0[0]:.1f},{a0[1]:.1f} A{r},{r} 0 0 0 {a1[0]:.1f},{a1[1]:.1f}", GOLD, 2.6, dash="8 6")
    for a in (placed, lag):
        q0, q1 = P(el, a, L + 40), P(el, a, r + 12)
        f.raw(f'<line x1="{q0[0]:.1f}" y1="{q0[1]:.1f}" x2="{q1[0]:.1f}" y2="{q1[1]:.1f}" stroke="{GOLD}" stroke-width="1.6"/>')
    f.raw("</g>")
    return T, rs, el, L, placed, lag, r


def hornblower_test(f, cx, top):
    """Front view: right arm supported at 90° of abduction, elbow at 90°; the patient tries to turn the forearm up."""
    rs, ls = trunk_front(f, cx, top, 200)
    arm(f, [ls, P(ls, 86, 105), P(ls, 88, 200)], fill=SKIN, hand_ang=88)
    el = (rs[0] - 112, rs[1] - 2)
    stub = P(el, 104, 46)                                                            # forearm pointing toward you
    b = Body(f, PALE, PALE_E); b.seg(el, stub, 12, 14); b.ell(stub[0], stub[1] + 12, 15, 16); b.draw()
    up = P(el, -90, 100)
    arm(f, [rs, el, up], hand_ang=-90, r=(15, 12.5, 10.5))
    exam_hand(f, el[0] + 40, el[1] + 26, 0, 0.8)                                   # supports the arm near the elbow
    exam_hand(f, up[0] - 34, up[1] - 4, 0, 0.8)                                     # resists behind the forearm
    straight(f, (up[0] - 34, up[1] - 92), (up[0] - 34, up[1] - 40), RED)
    straight(f, (up[0] + 40, el[1] - 20), (up[0] + 40, el[1] - 92), BLUE)
    return rs, el, stub, up


def f03():
    f = Fig("03", 1400, 1040, "External rotation lag sign and hornblower sign: the back of the cuff", "外旋滞后征与 Hornblower 征：肩袖后部")
    legend(f, 40, 118)
    panel_title(f, 50, 192, "External rotation lag sign (seen from above)", "外旋滞后征（从上往下看）")
    note(f, 50, 252, "Arm raised 20° in the scapular plane, elbow bent 90°; the examiner turns",
         "上臂在肩胛平面抬高 20°、屈肘 90°，检查者把前臂外旋到")
    note(f, 50, 290, "the forearm out to 5° short of full external rotation, then lets go of the wrist",
         "比最大外旋少 5° 的位置，然后松开手腕，")
    note(f, 50, 328, "but keeps holding the elbow. The patient faces the top of the page.",
         "但仍托住肘部。图中病人面朝上方。")
    T, rs, el, L, placed, lag, r = lag_panel(f, 210, 640)
    q = T(P(el, placed, L - 10)); f.leader(q[0], q[1] + 22, q[0] - 20, 742)
    f.bi(q[0] - 120, 762, "Placed here", "检查者放在这里", 14, INK)
    q = T(P(el, placed, L + 92)); f.leader(q[0], q[1] + 26, q[0] - 6, 690)
    f.bi(q[0] - 40, 710, "Lets go", "松开手腕", 14, MUTE)
    q = T(P(el, lag, L + 16)); f.leader(q[0] - 26, q[1] - 6, 400, 424)
    f.bi(150, 404, "The patient cannot hold it:", "病人保持不住，", 14, INK)
    note(f, 150, 446, "the forearm drifts back toward the belly", "前臂往腹部方向回漂", INK)
    q = T(P(el, (placed + lag) / 2, r + 14)); f.bi(q[0] + 8, q[1] - 6, "Lag", "滞后角度", 15, GOLD)
    q = T((el[0] + 14, el[1] + 34)); f.leader(q[0] - 30, q[1] + 26, 330, 790)
    f.bi(150, 812, "The examiner still holds the elbow", "检查者仍托住肘部", 14, INK)
    panel_title(f, 750, 192, "Hornblower sign (front view)", "Hornblower 征（前面观）")
    note(f, 750, 252, "The examiner supports the arm at 90° of abduction in the scapular plane, elbow bent 90°;",
         "检查者托住手臂：肩胛平面外展 90°、屈肘 90°；")
    note(f, 750, 290, "the patient turns the forearm up (external rotation) against the examiner's hand.",
         "病人对抗检查者的手，把前臂向上转（外旋）。")
    rs, el, stub, up = hornblower_test(f, 1150, 480)
    f.bi(up[0] + 58, el[1] - 70, "Turn up", "向上转", 14, BLUE)
    f.bi(up[0] - 150, up[1] - 70, "Examiner resists", "检查者给阻力", 14, RED)
    f.leader(stub[0] - 14, stub[1] + 20, 820, 600)
    f.bi(750, 622, "Start: the forearm points toward you", "起始：前臂朝向读者", 14, INK)
    f.bi(750, 680, "Positive: cannot turn it up;", "阳性：转不上去，", 14, RED)
    note(f, 750, 720, "the forearm stays pointing toward you", "前臂停在朝前的位置", RED)
    f.bi(750, 790, "Sources word the positive differently:", "各来源对阳性的说法不同：", 14, INK)
    note(f, 750, 832, "• cannot turn it up against resistance (course handout citing Patte 1988)",
         "• 对抗阻力转不上去（引用 Patte 1988 的课程讲义）", INK)
    note(f, 750, 874, "• cannot hold full external rotation and falls forward (Moulton 2016 review)",
         "• 保持不住最大外旋，前臂向前落下（Moulton 2016 综述）", INK)
    note(f, 750, 916, "Walch's 1998 paper itself could not be opened; chapter 1 explains.",
         "Walch 1998 原文没能打开，详见 01 章。")
    f.path("M700,180 L700,960", "#ddd8cc", 1.4, rough=False)
    foot(f.save("外旋滞后征与Hornblower征"), FOOT_EN, FOOT_ZH)


# ------------------------------------------------------------------ 04 belly-press test (subscapularis)
def belly_panel(f, tx, ty, positive, sc=1.5):
    """Seen from above, patient facing the top of the page; the right hand presses on the belly."""
    T = lambda q: (tx + sc * q[0], ty + sc * q[1])
    f.raw(f'<g transform="translate({tx},{ty}) scale({sc})">')
    f.path("M-150,2 L215,2", GREY, 1.4, dash="7 6", rough=False)
    rs, ls = trunk_top(f, 0, 0)
    if not positive:
        el, wr = (148, -26), (44, -50)
        hand_ang = math.degrees(math.atan2(wr[1] - el[1], wr[0] - el[0]))          # wrist straight: hand in line with the forearm
    else:
        el, wr = (138, 44), (56, -46)
        hand_ang = 180                                                              # wrist bent so the palm stays on the belly
    b = Body(f, ARM); b.seg(rs, el, 15, 13); b.seg(el, wr, 12.5, 10); b.draw()
    hc = P(wr, hand_ang, 17); h = Body(f, ARM); h.seg(wr, hc, 10, 12); h.ell(hc[0], hc[1], 20, 12, hand_ang); h.draw()
    f.raw("</g>")
    return T, rs, el, wr, hc


def f04():
    f = Fig("04", 1400, 900, "Belly-press test: subscapularis", "腹压试验：肩胛下肌")
    legend(f, 40, 118)
    note(f, 50, 196, "The patient presses the flat of the hand into the belly and tries to keep the arm fully turned in. Both drawings are seen from above,",
         "病人用手掌平按腹部，尽量让手臂保持最大内旋。两张图都是从上往下看，", INK, 15)
    note(f, 50, 236, "with the patient facing the top of the page; the dashed line joins the two sides of the body.",
         "病人面朝上方；虚线连接身体两侧。", INK, 15)
    for k, pos in enumerate((False, True)):
        ox = 290 + k * 700
        T, rs, el, wr, hc = belly_panel(f, ox, 620, pos)
        ttl = (("Normal: the elbow stays in front", "正常：肘部保持在前方"), ("Positive: the elbow drops back", "阳性：肘部向后落"))[k]
        panel_title(f, ox - 240, 316, *ttl, col=(INK, RED)[k])
        e, w, hcg = T(el), T(wr), T(hc)
        straight(f, (hcg[0] - 4, hcg[1] - 80), (hcg[0] - 4, hcg[1] - 26), BLUE)
        if not pos:
            straight(f, (e[0] + 10, e[1] + 4), (e[0] + 10, e[1] - 66), BLUE)
            f.bi(e[0] - 96, e[1] - 104, "Elbow kept in front of the line", "肘部保持在虚线前方", 14, INK)
            f.leader(w[0] + 2, w[1] - 20, w[0] - 10, 452)
            f.bi(w[0] - 120, 432, "Wrist straight", "手腕伸直", 14, INK)
        else:
            f.leader(e[0] + 22, e[1] + 10, e[0] + 50, e[1] + 56)
            f.bi(e[0] + 10, e[1] + 78, "Elbow behind the line", "肘部落到虚线后方", 14, RED)
            f.leader(w[0] + 2, w[1] - 20, w[0] - 10, 452)
            f.bi(w[0] - 230, 432, "Wrist bends to keep pressing (Tokish 2003)", "靠屈腕才能继续按压（Tokish 2003）", 14, RED)
    f.path("M700,300 L700,840", "#ddd8cc", 1.4, rough=False)
    foot(f.save("腹压试验"), FOOT_EN, FOOT_ZH)


# ------------------------------------------------------------------ 05 sensitivity and specificity quoted in chapter 1
# (test en, test zh, reading en, reading zh, target en, target zh, source, sensitivity %, specificity %)
ACC = [
    ("Empty can", "空罐试验", "read for weakness", "按无力判读", "full-thickness supraspinatus tear on MRI", "MRI 显示的冈上肌腱全层撕裂", "Itoi 1999", 77, 68),
    ("Full can", "满罐试验", "read for weakness", "按无力判读", "full-thickness supraspinatus tear on MRI", "MRI 显示的冈上肌腱全层撕裂", "Itoi 1999", 77, 74),
    ("Neer", "Neer", "", "", "subacromial impingement, pooled studies", "肩峰下撞击，多项研究合并", "Hegedus 2012", 72, 60),
    ("Hawkins-Kennedy", "Hawkins-Kennedy", "", "", "subacromial impingement, pooled studies", "肩峰下撞击，多项研究合并", "Hegedus 2012", 79, 59),
    ("External rotation lag sign", "外旋滞后征", "", "", "isolated full-thickness supraspinatus tear at surgery", "手术证实的单纯冈上肌腱全层撕裂", "Castoldi 2009", 56, 98),
    ("Hornblower sign", "Hornblower 征", "", "", "severe fatty degeneration of teres minor, combined supraspinatus-infraspinatus tears", "冈上肌、冈下肌联合撕裂病人的小圆肌严重脂肪变性", "Walch 1998", 100, 93),
    ("Hornblower sign", "Hornblower 征", "", "", "infraspinatus tear, patients over 45 with shoulder pain", "冈下肌撕裂，45 岁以上肩痛病人", "Jain 2017", 17, 96),
    ("Belly-press", "腹压试验", "", "", "any subscapularis tear at arthroscopy", "关节镜下任何肩胛下肌撕裂", "Barth 2006", 40, 97.9),
]
SENS_C, SPEC_C = BLUE, GOLD


def f05():
    rows = len(ACC)
    h = 330 + rows * 120 + 210
    f = Fig("05", 1400, h, "How accurate are the tests? The numbers quoted in chapter 1", "这些检查有多准：01 章引用的数字")
    x0, x1 = 600, 1300                                                     # 0 % and 100 %
    sx = lambda v: x0 + (x1 - x0) * v / 100
    f.raw(f'<rect x="40" y="112" width="26" height="16" fill="{SENS_C}"/>')
    f.bi(76, 126, "Sensitivity: of people who have the condition, how many test positive", "敏感度：真正有病的人里，检查阳性的比例", 14, INK, weight="400")
    f.raw(f'<rect x="40" y="166" width="26" height="16" fill="{SPEC_C}"/>')
    f.bi(76, 180, "Specificity: of people who do not have it, how many test negative", "特异度：没有这个病的人里，检查阴性的比例", 14, INK, weight="400")
    top = 300
    for v in range(0, 101, 25):
        x = sx(v)
        f.raw(f'<line x1="{x:.0f}" y1="{top - 30}" x2="{x:.0f}" y2="{top + rows * 120 - 10}" stroke="#ddd8cc" stroke-width="1.2"/>')
        f.text(x, top - 40, f"{v}%", 13, MUTE, "middle", "400")
    for i, (en, zh, ren, rzh, ten, tzh, src, se, sp) in enumerate(ACC):
        y = top + i * 120
        f.bi(40, y + 4, f"{en} ({ren})" if ren else en, f"{zh}（{rzh}）" if rzh else zh, 16, INK, gap=24, zsize=14)
        f.bi(40, y + 56, f"{ten} · {src}", f"{tzh} · {src}", 12, MUTE, weight="400", gap=20, zsize=12)
        for k, (val, col) in enumerate(((se, SENS_C), (sp, SPEC_C))):
            yy = y - 14 + k * 34
            f.raw(f'<rect x="{x0}" y="{yy}" width="{sx(val) - x0:.1f}" height="24" rx="3" fill="{col}"/>')
            f.text(sx(val) + 8, yy + 18, f"{val}%", 15, INK, "start", "700")
    yb = top + rows * 120 + 20
    note(f, 40, yb, "Rows from different studies differ in target condition, reference standard and patients.",
         "来自不同研究的行，目标疾病、参考标准和病人都不一样。", INK, 15)
    note(f, 40, yb + 40, "Read a test's sensitivity against its own specificity; do not rank the rows against each other.",
         "看同一行里敏感度和特异度的关系，不要把不同行拿来排名。", INK, 15)
    note(f, 40, yb + 80, "The empty and full can share one study (Itoi 1999), as do Neer and Hawkins-Kennedy (Hegedus 2012).",
         "空罐和满罐同出 Itoi 1999，Neer 和 Hawkins-Kennedy 同出 Hegedus 2012。", INK, 15)
    foot(f.save("检查准确性对比"), "Numbers as reported by the cited studies; chapter 1 gives each study's details.",
         "数字按所引研究的报告；每项研究的细节见 01 章。")


# ------------------------------------------------------------------ 06 the two force couples (redrawn from the chapter's figures 10 and 11)
BONE, BONE_E = "#fbf5e6", "#3a3a3a"
SCAP = ("M85,72 L292,63 Q300,74 308,64 L322,70 Q352,82 372,98 L384,140 L386,200 Q345,280 300,352 L172,598 "
        "Q140,540 118,480 L62,340 Q66,250 76,160 Z")                      # right scapula from behind, as in chapter figure 11
SPINE = "M88,160 L252,118 L396,78 L408,96 L258,140 L92,180 Z"
CLAV = "M392,72 Q470,42 542,56 Q556,72 542,86 Q470,96 406,100 Z"


def gh_couple(f):
    gx, gy = 330, 590                                                   # centre of the glenoid
    hx, hy, hr = gx + 72, gy, 66                                        # humeral head
    f.raw(f'<path d="M{gx - 40},{gy - 150} Q{gx - 20},{gy - 120} {gx - 4},{gy - 96} Q{gx + 12},{gy} {gx - 4},{gy + 96} '
          f'Q{gx - 24},{gy + 130} {gx - 44},{gy + 170}" fill="{BONE}" stroke="{BONE_E}" stroke-width="3"/>')   # lateral part of the scapula
    f.path(f"M{gx - 44},{gy + 170} L{gx - 40},{gy - 150}", GREY, 1.6, dash="6 5", rough=False)          # cut edge
    f.raw(f'<path d="M{gx - 2},{gy - 84} Q{gx + 10},{gy} {gx - 2},{gy + 84}" fill="none" stroke="#5f5a50" stroke-width="9" stroke-linecap="round"/>')
    ang = 68
    shaft_end = P((hx, hy), ang, 300)
    b = Body(f, BONE, BONE_E); b.seg((hx, hy), shaft_end, 30, 24); b.ell(hx, hy, hr, hr); b.draw()
    f.raw(f'<path d="M{gx - 74},{gy - 186} Q{gx + 30},{gy - 222} {gx + 180},{gy - 196} Q{gx + 196},{gy - 180} {gx + 178},{gy - 166} '
          f'Q{gx + 30},{gy - 190} {gx - 66},{gy - 160} Z" fill="{BONE}" stroke="{BONE_E}" stroke-width="3"/>')   # acromion
    tub = P((hx, hy), ang, 200)
    straight(f, (tub[0] + 12, tub[1]), (hx + 92, gy - 150), BLUE, 4.4)                 # deltoid
    straight(f, (hx + 4, hy), (gx + 24, hy), BLUE, 4.4)                                 # supraspinatus compresses
    straight(f, (hx + 4, hy + 12), (hx - 44, hy + 88), BLUE, 4.4)                       # inferomedial pull
    f.arrow(f"M{hx},{hy - 76} L{hx},{hy - 140}", GREY, 3, dash="7 5")                   # deltoid alone
    return gx, gy, hx, hy, tub


def scap_couple(f, tx, ty, sc):
    T = lambda q: (tx + sc * q[0], ty + sc * q[1])
    f.raw(f'<g transform="translate({tx},{ty}) scale({sc})">'
          f'<path d="{SCAP}" fill="{BONE}" stroke="{BONE_E}" stroke-width="{3 / sc:.1f}"/>'
          f'<path d="{SPINE}" fill="{BONE}" stroke="{BONE_E}" stroke-width="{3 / sc:.1f}"/>'
          f'<path d="{CLAV}" fill="{BONE}" stroke="{BONE_E}" stroke-width="{3 / sc:.1f}"/></g>')
    straight(f, T((440, 66)), T((350, 6)), BLUE, 4.4)                                   # upper trapezius
    straight(f, T((96, 180)), T((10, 300)), BLUE, 4.4)                                  # lower trapezius
    straight(f, T((176, 592)), T((340, 606)), BLUE, 4.4)                                # lower serratus anterior
    a, b = T((316, 470)), T((392, 236))
    f.arrow(f"M{a[0]:.0f},{a[1]:.0f} A200,200 0 0 0 {b[0]:.0f},{b[1]:.0f}", RED, 3.6)
    for k, q in enumerate((T((100, 170)), T((400, 88)))):
        f.raw(f'<circle cx="{q[0]:.0f}" cy="{q[1]:.0f}" r="13" fill="#fffaf0" stroke="{RED}" stroke-width="2.6"/>')
        f.text(q[0], q[1] + 5, str(k + 1), 14, RED, "middle", "700")
    return T


def f06():
    f = Fig("06", 1400, 1110, "Two force couples that let the arm rise", "让手臂抬起来的两组力偶")
    f.markers = getattr(f, "markers", set()) | {RED, BLUE, GREY}
    for x, col, en, zh in ((40, BLUE, "Pull of a muscle", "肌肉的拉力方向"), (330, RED, "Resulting movement", "产生的运动")):
        f.raw(f'<line x1="{x}" y1="122" x2="{x + 40}" y2="122" stroke="{col}" stroke-width="3.4" marker-end="url(#{f.id("m" + col.strip("#"))})"/>')
        f.bi(x + 54, 127, en, zh, 14, INK, weight="400")
    f.arrow("M620,122 L660,122", GREY, 3, dash="7 5")
    f.bi(674, 127, "What would happen without the partner muscles", "缺少配合时会发生什么", 14, INK, weight="400")
    panel_title(f, 50, 196, "Shoulder joint: deltoid with the rotator cuff", "盂肱关节：三角肌与肩袖")
    note(f, 50, 256, "Right shoulder from behind, arm partly raised", "从后面看右肩，手臂稍微抬起")
    gx, gy, hx, hy, tub = gh_couple(f)
    f.bi(hx + 104, tub[1] - 70, "Deltoid", "三角肌", 15, BLUE)
    note(f, hx + 104, tub[1] - 28, "pulls the humerus up", "把肱骨往上拉", BLUE, 13)
    f.leader(hx + 6, hy - 120, 470, 340)
    f.bi(400, 318, "Deltoid alone: the head rides up", "三角肌单独作用：肱骨头上移", 14, MUTE)
    f.leader(gx - 50, 402, 190, 380)
    f.bi(60, 366, "Acromion", "肩峰", 14, INK)
    f.leader(gx + 24, gy - 8, 250, 520)
    f.bi(40, 478, "Supraspinatus", "冈上肌", 15, BLUE)
    note(f, 40, 520, "presses the head into the glenoid", "把肱骨头压向关节盂", BLUE, 13)
    f.leader(hx - 40, hy + 82, 260, 804)
    f.bi(40, 822, "Infraspinatus, teres minor, subscapularis", "冈下肌、小圆肌、肩胛下肌", 15, BLUE)
    note(f, 40, 864, "pull the head down and in", "把肱骨头往下、往内拉", BLUE, 13)
    f.raw(f'<rect x="30" y="960" width="610" height="70" rx="10" fill="none" stroke="{RED}" stroke-width="1.6" stroke-dasharray="7 5"/>')
    f.bi(50, 990, "Together: the arm rises and the head stays centred beneath the acromion", "合起来：手臂抬起，肱骨头仍居中，留在肩峰下方", 15, INK)
    panel_title(f, 690, 196, "Scapula: trapezius with serratus anterior", "肩胛骨：斜方肌与前锯肌")
    note(f, 690, 256, "Right scapula from behind. Axis of rotation, as marked in the chapter's figure 11:",
         "从后面看右肩胛骨。旋转轴（按章节图 11 的标注）：")
    note(f, 690, 294, "(1) early, near the root of the spine; (2) later, at the acromioclavicular joint.",
         "(1) 早期在肩胛冈根部附近；(2) 后期在肩锁关节。")
    T = scap_couple(f, 960, 450, 0.74)
    f.bi(1010, 360, "Upper trapezius (accessory nerve)", "上斜方肌（副神经）", 14, BLUE)
    note(f, 1010, 400, "pulls the acromion and lateral clavicle up and in", "把肩峰和锁骨外端往上、往内拉", BLUE, 13)
    f.bi(690, 660, "Lower trapezius (accessory nerve)", "下斜方肌（副神经）", 14, BLUE)
    note(f, 690, 700, "pulls the root of the spine down and in", "把肩胛冈根部往下、往内拉", BLUE, 13)
    f.bi(940, 960, "Lower serratus anterior (long thoracic nerve)", "前锯肌下部（胸长神经）", 14, BLUE)
    note(f, 940, 1000, "pulls the inferior angle out and forward", "把肩胛下角往外、往前拉", BLUE, 13)
    q = T((330, 380)); f.bi(q[0] + 48, q[1] + 30, "Upward rotation", "上旋", 16, RED)
    f.path("M665,180 L665,1040", "#ddd8cc", 1.4, rough=False)
    f.save("两组力偶")


def build(out_dir):
    set_out(out_dir)
    f01(); f02(); f03(); f04(); f05(); f06()
    copy_library_figure("shoulder", "12-0--30--90--180-肩肱节律", out_dir, "07-肩肱节律")


if __name__ == "__main__":
    build(sys.argv[1] if len(sys.argv) > 1 else pathlib.Path(__file__).resolve().parent / "资源")
