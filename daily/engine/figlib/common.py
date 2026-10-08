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
