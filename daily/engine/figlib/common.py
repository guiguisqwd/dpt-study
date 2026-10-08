#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Generic figure helpers shared by all days."""
from .fig import *

# ------------------------------------------------------------------ 08 layers
def stack(f, x, y, w, title_en, title_zh, layers, foot_en, foot_zh):
    f.bi(x, y, title_en, title_zh, 17, INK)
    yy = y + 36
    for name_en, name_zh, h, fill, edge, note in layers:
        f.raw(f'<rect x="{x}" y="{yy}" width="{w}" height="{h}" fill="{fill}" stroke="{edge}" stroke-width="1.2"/>')
        f.text(x + 14, yy + h / 2 + 5, f"{name_en} {name_zh}", 14, INK, lang="zh-CN")
        if note: f.text(x + w - 12, yy + h / 2 + 5, note, 13, RED, "end", "700", "zh-CN")
        yy += h
    f.bi(x, yy + 30, foot_en, foot_zh, 13, RED)


def stack2(f, x, y, w, title_en, title_zh, layers, foot_en, foot_zh, h_min=48):
    """Layer stack with English on the first line and Chinese on the second inside every box.
    layers: [(en, zh, height, fill, edge, note)] — note (short Chinese) is drawn on the right."""
    f.bi(x, y, title_en, title_zh, 17, INK)
    yy = y + 40
    for en, zh, h, fill, edge, note in layers:
        h = max(h, h_min)
        f.raw(f'<rect x="{x}" y="{yy}" width="{w}" height="{h}" fill="{fill}" stroke="{edge}" stroke-width="1.2"/>')
        f.bi(x + 14, yy + h / 2 - 3, en, zh, 14, INK, weight="400", gap=18, zsize=13)
        if note:
            f.raw(f'<rect x="{x + w - 78}" y="{yy + h / 2 - 13}" width="68" height="24" rx="12" fill="#fff" stroke="{RED}" stroke-width="1.2"/>')
            f.text(x + w - 44, yy + h / 2 + 4, note, 13, RED, "middle", "700", "zh-CN")
        yy += h
    f.bi(x, yy + 30, foot_en, foot_zh, 14, RED)
    return yy
