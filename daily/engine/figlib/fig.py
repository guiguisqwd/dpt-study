#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Shared hand-drawn SVG figure kit for the daily packs (English first, Chinese second).

Use set_out(dir) before Fig.save(). Rough look = double pencil stroke (no SVG displacement filter:
it produced seams in Chrome and is unreliable in print)."""
import html, math, os, sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
OUT = Path.cwd() / "资源"
def set_out(path):
    """Directory that Fig.save() writes to (created if needed)."""
    global OUT
    OUT = Path(path); OUT.mkdir(parents=True, exist_ok=True)
    return OUT

RED, BLUE, INK, GREEN, PURP, GOLD, GREY, TEAL = "#b94334", "#365e91", "#253b36", "#4f8a4a", "#7a5aa6", "#c69014", "#9a958a", "#2b6c7c"
ZH = "#68726a"
BONE, BONE_E = "#FBF5E6", "#3A3A3A"
SCAP = "M85,72 L292,63 Q300,74 308,64 L322,70 Q352,82 372,98 L384,140 L386,200 Q345,280 300,352 L172,598 Q140,540 118,480 L62,340 Q66,250 76,160 Z"
SPINE = "M88,160 L252,118 L396,78 L408,96 L258,140 L92,180 Z"
ACROM = "M392,72 Q470,42 542,56 Q556,72 542,86 Q470,96 406,100 Z"
SUPRA = "M95,154 C93,112 97,90 108,80 L288,70 Q340,75 380,87 L420,100 Q480,106 536,116 L539,134 Q480,128 420,116 L396,84 L252,121 Z"
INFRA = "M92,184 L258,144 L404,100 Q440,118 470,128 Q510,136 549,140 L551,163 Q505,168 470,172 Q420,188 386,212 Q345,285 300,302 Q250,335 214,410 Q160,402 120,380 Q85,300 80,240 Z"
TERES = "M388,214 Q430,192 470,182 Q510,176 549,168 L549,192 Q505,196 470,206 Q420,232 332,330 Q312,346 300,350 Q322,298 388,214 Z"
TMAJ = "M300,356 Q262,420 196,560 Q232,585 262,562 Q332,452 484,332 L486,302 Q400,322 300,356 Z"
DELT = "M400,92 Q470,55 548,60 Q612,110 596,210 Q575,330 528,430 Q490,330 452,250 Q430,170 400,92 Z"
SUBSC = "M100,90 L300,80 Q350,95 380,130 Q420,150 462,165 L468,192 Q420,202 380,216 Q330,300 290,350 L180,560 Q140,520 115,470 L70,340 Q72,240 80,160 Z"
HUM = "M478,200 Q470,420 486,640 L528,640 Q520,420 532,205 Z"
MUS = {"supra": (SUPRA, "#e9a596", RED), "infra": (INFRA, "#a9bfdf", BLUE), "teres": (TERES, "#b3d6ab", GREEN), "subsc": (SUBSC, "#cdb8e6", PURP)}
FIB = {"supra": ([(110, 90), (140, 110), (170, 95), (200, 112), (230, 90), (260, 105), (290, 85)], (537, 125)),
       "infra": ([(100, 200), (110, 250), (120, 320), (150, 370), (190, 395), (180, 260), (240, 300), (260, 180), (330, 160)], (550, 152)),
       "teres": ([(310, 340), (330, 310), (355, 270), (380, 230)], (549, 180)),
       "subsc": ([(110, 110), (100, 200), (95, 300), (130, 420), (170, 520), (200, 150), (210, 300), (260, 250), (300, 120)], (468, 180))}

def esc(s): return html.escape(s, quote=True)

class Fig:
    def __init__(s, num, w, h, en, zh, aria_en=None, aria_zh=None):
        s.n, s.w, s.h, s.en, s.zh = num, w, h, en, zh
        s.p = []
        s.pre = f"fig{num}-"
    def id(s, k): return s.pre + k
    def raw(s, x): s.p.append(x)
    def text(s, x, y, txt, size=16, col=INK, anchor="start", weight="400", lang="en"):
        s.p.append(f'<text x="{x:.1f}" y="{y:.1f}" font-size="{size}" fill="{col}" text-anchor="{anchor}" font-weight="{weight}" lang="{lang}">{esc(txt)}</text>')
    def bi(s, x, y, en, zh, size=16, col=INK, anchor="start", weight="600", zcol=None, gap=None, zsize=None):
        """English line with Chinese line beneath."""
        zsize = zsize or max(size - 2, 11); gap = gap or size + 4
        s.p.append(f'<text x="{x:.1f}" y="{y:.1f}" font-size="{size}" fill="{col}" text-anchor="{anchor}" font-weight="{weight}" aria-label="{esc(en)} — {esc(zh)}"><tspan x="{x:.1f}" dy="0" lang="en">{esc(en)}</tspan><tspan x="{x:.1f}" dy="{gap}" lang="zh-CN" font-size="{zsize}" font-weight="400" fill="{zcol or ZH}">{esc(zh)}</tspan></text>')
    def path(s, d, col=INK, w=2, fill="none", dash=None, rough=True, op=None, extra=""):
        """rough=True：手绘感用“双线铅笔描边”实现（主线 + 一条错位的淡线），不用 SVG 位移滤镜——
        位移滤镜在 Chrome 里会出现断口和小刺，打印也不稳定。"""
        dsh = f' stroke-dasharray="{dash}"' if dash else ""
        s.p.append(f'<path d="{d}" fill="{fill}" stroke="{col}" stroke-width="{w}" stroke-linecap="round" stroke-linejoin="round"'
                   + dsh + (f' opacity="{op}"' if op is not None else "") + f' {extra}/>')
        if rough and col != "none" and w and float(w) >= 1.2:
            s.p.append(f'<path d="{d}" fill="none" stroke="{col}" stroke-width="{max(float(w) * 0.5, 0.8):.2f}" stroke-linecap="round" stroke-linejoin="round"'
                       + dsh + f' opacity="{0.32 * (op if op is not None else 1):.2f}" transform="translate(1.4,1.0)"/>')
    def arrow(s, d, col=INK, w=2.4, dash=None, rough=True):
        mk = s.id("m" + col.strip("#"))
        s.markers.add(col) if hasattr(s, "markers") else setattr(s, "markers", {col})
        s.p.append(f'<path d="{d}" fill="none" stroke="{col}" stroke-width="{w}" stroke-linecap="round"' + (f' stroke-dasharray="{dash}"' if dash else "")
                   + f' marker-end="url(#{mk})"/>')
    def box(s, x, y, w, h, col=INK, fill="#fffdf7", dash=None, sw=1.6):
        s.p.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="8" fill="{fill}" stroke="{col}" stroke-width="{sw}"' + (f' stroke-dasharray="{dash}"' if dash else "") + "/>")
    def circle(s, x, y, r, fill, stroke="#fff", sw=2):
        s.p.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>')
    def step(s, x, y, n, col=GOLD):
        s.circle(x, y, 14, col, "#fff", 2.5); s.text(x, y + 5.5, str(n), 15, "#fff", "middle", "700")
    def leader(s, x1, y1, x2, y2, col="#555", dash=None):
        s.path(f"M{x1:.1f},{y1:.1f} L{x2:.1f},{y2:.1f}", col, 1.2, dash=dash, rough=False)
    def g(s, tr): s.p.append(f'<g transform="{tr}">')
    def end(s): s.p.append("</g>")
    def shoulder(s, view="post", op=1.0, muscles=("supra", "infra", "teres"), sw=2.2, tmaj=True, delt=True, fibers=True, clip=True):
        """Draw the right shoulder in base coordinates (current group transform applies)."""
        s.path(SCAP, BONE_E, sw, BONE)
        s.path(HUM, BONE_E, sw, BONE)
        s.raw(f'<circle cx="470" cy="150" r="62" fill="{BONE}" stroke="{BONE_E}" stroke-width="{sw}"/>')
        if view == "post":
            s.raw(f'<ellipse cx="536" cy="152" rx="22" ry="36" fill="{BONE}" stroke="{BONE_E}" stroke-width="{sw-0.2}"/>')
            if tmaj: s.path(TMAJ, "#8a8a8a", 1.6, "#EAE6DD", dash="6 5", op=op)
        else:
            s.raw(f'<ellipse cx="472" cy="180" rx="18" ry="20" fill="{BONE}" stroke="{BONE_E}" stroke-width="{sw-0.2}"/>')
        for m in muscles:
            d, fill, st = MUS[m]
            s.raw(f'<clipPath id="{s.id("c-" + m)}"><path d="{d}"/></clipPath>')
            s.path(d, st, sw, fill, op=op)
            if fibers:
                org, ins = FIB[m]
                for ox, oy in org:
                    cx, cy = (ox + ins[0]) / 2, (oy + ins[1]) / 2 - 8
                    s.raw(f'<path d="M{ox},{oy} Q{cx},{cy} {ins[0]},{ins[1]}" stroke="{st}" stroke-width="1.2" fill="none" opacity="{0.55*op:.2f}" clip-path="url(#{s.id("c-" + m)})"/>')
        if view == "post": s.path(SPINE, BONE_E, sw, BONE)
        else:
            s.path("M318,72 Q330,30 380,18 Q420,14 440,30", BONE_E, 16); s.path("M318,72 Q330,30 380,18 Q420,14 440,30", BONE, 12, rough=False)
            s.path("M540,52 Q400,20 300,30 Q220,40 150,8", BONE_E, 20); s.path("M540,52 Q400,20 300,30 Q220,40 150,8", BONE, 15, rough=False)
        s.path(ACROM, BONE_E, sw, BONE)
        if delt: s.path(DELT, "#999", 1.5, dash="4 6", rough=False)
    def save(s, name):
        defs = ''
        for c in sorted(getattr(s, "markers", set())):
            defs += f'<marker id="{s.id("m" + c.strip("#"))}" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="{c}"/></marker>'
        head = (f'<text class="fig-title" x="38" y="46" fill="{INK}" font-size="27" font-weight="700" aria-label="{esc(s.en)} — {esc(s.zh)}"><tspan x="38" dy="0" lang="en">{esc(s.en)}</tspan>'
                f'<tspan x="38" dy="32" lang="zh-CN" font-size="22" font-weight="400" fill="{ZH}">{esc(s.zh)}</tspan></text>')
        foot = (f'<text class="fig-foot" x="38" y="{s.h-34}" font-size="13" fill="#6b706a"><tspan x="38" dy="0" lang="en">Schematic; pathway and layers are simplified.</tspan>'
                f'<tspan x="38" dy="17" lang="zh-CN">解剖示意；走行与层次经过简化。</tspan></text>')
        svg = (f'<?xml version="1.0" encoding="UTF-8"?><svg xmlns="http://www.w3.org/2000/svg" width="{s.w}" height="{s.h}" viewBox="0 0 {s.w} {s.h}" role="img" aria-label="{esc(s.en)} — {esc(s.zh)}">'
               f'<style>text{{font-family:Arial,"PingFang SC","Microsoft YaHei",sans-serif}}</style><defs>{defs}</defs>'
               f'<rect width="100%" height="100%" fill="#fcfaf4"/>{head}{"".join(s.p)}{foot}</svg>')
        OUT.mkdir(parents=True, exist_ok=True)
        (OUT / f"{s.n}-{name}.svg").write_text(svg, encoding="utf-8")
        return OUT / f"{s.n}-{name}.svg"

def T(tx, ty, sc, x, y, mirror=False):
    return (tx - x * sc, ty + y * sc) if mirror else (tx + x * sc, ty + y * sc)

