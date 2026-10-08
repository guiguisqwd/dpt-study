# -*- coding: utf-8 -*-
"""Strict checks for a day's content.json. validate(content) -> list of problems ([] = OK).

These checks enforce the user's standing rules (see daily/README.md):
English first then Chinese; complete O/I/N/A + the full "originates … inserts" sentence;
every acupoint has location, layers, safety, related muscles and a way to find it; every
English key term has pronunciation; figures exist for every muscle and the meridian; sources;
archive tags; no public-health framing; the day's points/muscles match the study plan.
"""
import json, re
from .paths import day_dir, build_dir
from .render import load_pron
from . import plan

CJK = re.compile(r"[一-鿿]")
LATIN = re.compile(r"[A-Za-z]")
CH_ORDER = ["muscles", "nerve", "motion", "acupoints", "review", "english"]
BANNED = ["公共卫生", "公卫", "public health", "Public health"]
MUSCLE_KEYS = ["id", "en", "zh", "letter", "color", "figure", "o", "i", "n", "a", "sentence", "acu", "acu_en", "o_short", "i_short", "n_short", "a_short", "source"]
ACU_KEYS = ["name", "pinyin", "code", "loc", "loc_short", "layers", "safety", "muscles", "find"]
BLOCK_TYPES = {"p", "h3", "fig", "html", "levels", "pitfall", "song", "muscle_cards", "acu_cards", "summary_tables", "pron_table", "flashcards", "sources"}


def _pair(v, where, errs, need_zh=True):
    if not (isinstance(v, (list, tuple)) and len(v) == 2 and all(isinstance(x, str) and x.strip() for x in v)):
        errs.append(f"{where}: needs [English, 中文] (two non-empty strings)")
        return
    en, zh = v
    if not LATIN.search(en):
        errs.append(f"{where}: first item should be English: {en[:40]!r}")
    if need_zh and not CJK.search(zh):
        errs.append(f"{where}: second item should be Chinese: {zh[:40]!r}")


def validate(c, check_plan=True, check_figures=True):
    errs = []
    for k in ["schema", "date", "kind", "slug_zh", "title", "description", "today_line", "tags", "chapters"]:
        if k not in c:
            errs.append(f"missing top-level field: {k}")
    if errs:
        return errs
    date = c["date"]
    if c["schema"] != "dpt-daily-pack/1":
        errs.append("schema must be dpt-daily-pack/1")
    tags = c.get("tags", {})
    if not tags.get("vertical") or not tags.get("horizontal"):
        errs.append("tags.vertical and tags.horizontal (archive tags for later agents) are required")
    text = json.dumps(c, ensure_ascii=False)
    for w in BANNED:
        if w in text:
            errs.append(f"banned framing found: {w!r} (user: no public-health content)")
    if c["kind"] != "learning":
        return errs + _validate_chapters(c, check_figures)

    # ---- plan match
    if check_plan:
        info = plan.day_info(date)
        if info.get("kind") != "learning":
            errs.append(f"{date} is not a learning day in plan/schedule.json")
        else:
            if c.get("day") != info["day"]:
                errs.append(f"day number {c.get('day')} != plan {info['day']}")
            want_a = [a["name"] for a in info["acupoints"]]
            got_a = [a.get("name") for a in c.get("acupoints", [])]
            if want_a != got_a:
                errs.append(f"acupoints {got_a} != plan {want_a} (same order)")
            want_m = [m["zh"] for m in info["muscles"]]
            got_m = [m.get("zh") for m in c.get("muscles", [])]
            if want_m != got_m:
                errs.append(f"muscles {got_m} != plan {want_m} (same order)")
    # ---- muscles
    figs = c.get("figures", {})
    for i, m in enumerate(c.get("muscles", [])):
        w = f"muscles[{i}] {m.get('en', '?')}"
        for k in MUSCLE_KEYS:
            if k not in m or m[k] in ("", None, []):
                errs.append(f"{w}: missing {k}")
        for k in ["o", "i", "n", "a", "sentence", "o_short", "i_short", "n_short", "a_short"]:
            if k in m:
                _pair(m[k], f"{w}.{k}", errs)
        s = (m.get("sentence") or ["", ""])[0]
        if not re.search(r"originates? from .+ inserts? (onto|into|on)", s):
            errs.append(f"{w}.sentence must follow 'The X originates from …, passes …, and inserts onto …'")
        if m.get("figure") and m["figure"] not in figs:
            errs.append(f"{w}: figure {m['figure']} not declared in content.figures")
        if m.get("source") and not str(m["source"]).startswith("http"):
            errs.append(f"{w}: source must be a URL")
        if not re.search(r"\b[CTLS]\d", (m.get("n") or [""])[0]):
            errs.append(f"{w}.n: give spinal segments, e.g. (C5–C7)")
    # ---- acupoints
    for i, a in enumerate(c.get("acupoints", [])):
        w = f"acupoints[{i}] {a.get('name', '?')}"
        for k in ACU_KEYS:
            if not a.get(k):
                errs.append(f"{w}: missing {k}")
        if a.get("pinyin") and not re.search(r"[āáǎàēéěèīíǐìōóǒòūúǔùǖǘǚǜ]", a["pinyin"]):
            errs.append(f"{w}: pinyin needs tone marks")
        if a.get("layers") and "→" not in a["layers"]:
            errs.append(f"{w}: layers should read skin → … → deep with arrows")
    if not c.get("sources"):
        errs.append("sources: at least one [url, label]")
    return errs + _validate_chapters(c, check_figures)


def _validate_chapters(c, check_figures):
    errs = []
    chs = c["chapters"]
    ids = [ch.get("id") for ch in chs]
    if c["kind"] == "learning" and ids != CH_ORDER:
        errs.append(f"chapters must be {CH_ORDER}, got {ids}")
    pron = load_pron(c.get("pronunciation"))
    used_figs = set()
    for k, ch in enumerate(chs):
        w = f"chapter {ch.get('id')}"
        if ch.get("num") != k + 1:
            errs.append(f"{w}: num should be {k + 1}")
        _pair(ch.get("title"), f"{w}.title", errs)
        _pair(ch.get("toc"), f"{w}.toc", errs)
        if not ch.get("goals"):
            errs.append(f"{w}: goals required")
        for g in ch.get("goals", []):
            _pair(g, f"{w}.goal", errs)
        if c["kind"] == "learning" and not ch.get("terms"):
            errs.append(f"{w}: key terms required")
        for t in ch.get("terms", []):
            if len(t) == 3 and t[2] == "zh":
                continue
            _pair(t[:2], f"{w}.term", errs)
            if t[0] not in pron:
                errs.append(f"{w}: no pronunciation for key term {t[0]!r} (add to content.pronunciation or engine/data/pronunciation.json)")
        for b in ch.get("blocks", []):
            if b.get("t") not in BLOCK_TYPES:
                errs.append(f"{w}: unknown block type {b.get('t')}")
            if b.get("t") in ("p", "h3", "fig"):
                _pair([b.get("en", ""), b.get("zh", "")], f"{w}.{b['t']}", errs)
            if b.get("t") == "fig":
                used_figs.add(b.get("n"))
            if b.get("t") == "pron_table":
                for t in b.get("terms", []):
                    if t not in pron:
                        errs.append(f"{w}: pron_table term without pronunciation: {t}")
                    if t not in b.get("zh_map", {}):
                        errs.append(f"{w}: pron_table term without Chinese: {t}")
        if c["kind"] == "learning" and ch.get("id") != "review" and not ch.get("check"):
            errs.append(f"{w}: self-check questions required")
        for q in ch.get("check", []):
            if len(q) != 4:
                errs.append(f"{w}: check items are [question_en, question_zh, answer_en, answer_zh]")
        if k < len(chs) - 1 and not ch.get("bridge"):
            errs.append(f"{w}: bridge to the next chapter required")
    used_figs |= {m.get("figure") for m in c.get("muscles", [])}
    declared = set(c.get("figures", {}))
    if declared - used_figs:
        errs.append(f"figures declared but never shown: {sorted(declared - used_figs)}")
    if used_figs - declared - {None}:
        errs.append(f"figures shown but not declared: {sorted(used_figs - declared - {None})}")
    if check_figures:
        res = build_dir(c["date"]) / "资源"
        have = {p.name[:2] for p in res.glob("*.svg")} if res.exists() else set()
        if declared - have:
            errs.append(f"figure files missing in build/资源: {sorted(declared - have)} (run the figures step)")
    return errs
