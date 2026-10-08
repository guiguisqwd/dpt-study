# -*- coding: utf-8 -*-
"""Review days (Sundays, and 12/16–12/23) need no new authoring: this builds content.json and a
figures.py that reuses the week's own figures, so the review pack is generated automatically."""
import json
from pathlib import Path
from .paths import DAYS, build_dir, load_content


def _week_contents(info):
    out = []
    for d in info["days"]:
        p = DAYS / d["date"] / "content.json"
        if p.exists():
            out.append(json.loads(p.read_text(encoding="utf-8")))
    return out


def write(date, info):
    cs = _week_contents(info)
    if info["kind"] == "final_review":
        title_zh, title_en, slug = "总复习", "Final review", f"总复习-{date[5:]}"
    else:
        title_zh, title_en, slug = f"第 {info['week']} 周复习", f"Week {info['week']} review", f"第{info['week']}周复习"
    acu = [a for c in cs for a in c.get("acupoints", [])]
    mus = [m for c in cs for m in c.get("muscles", [])]
    # reuse each day's meridian chart (the figure that the acupoints chapter shows first) and overview figure
    figs, copies, n = {}, [], 1
    for c in cs:
        for ch in c["chapters"]:
            if ch["id"] in ("acupoints", "muscles"):
                f = next((b for b in ch["blocks"] if b["t"] == "fig"), None)
                if f:
                    src = next((p for p in (build_dir(c["date"]) / "资源").glob(f"{f['n']}-*.svg")), None)
                    if src:
                        key = f"{n:02d}"; n += 1
                        figs[key] = f"{c['date']}-{src.stem[3:]}"
                        copies.append([str(src.relative_to(DAYS)), f"{key}-{c['date']}-{src.stem[3:]}.svg", f["en"], f["zh"], ch["id"], c["date"]])
    pron_terms = []
    for c in cs:
        for ch in c["chapters"]:
            for t in ch.get("terms", []):
                if len(t) == 2 and t[0] not in pron_terms:
                    pron_terms.append(t[0])
    zh_map = {t[0]: t[1] for c in cs for ch in c["chapters"] for t in ch.get("terms", []) if len(t) == 2}
    checks = [q for c in cs for ch in c["chapters"] for q in ch.get("check", [])]
    fig_blocks = lambda chap: [{"t": "fig", "n": k, "en": f"{d}: {e}", "zh": f"{d}：{z}"} for k, (src, name, e, z, cid, d) in zip(figs, copies) if cid == chap]
    content = {
        "schema": "dpt-daily-pack/1", "date": date, "day": None, "kind": info["kind"], "slug_zh": slug,
        "title": {"zh": title_zh, "en": title_en}, "page_title": title_zh,
        "description": f"DPT 基础 · {title_zh}：{len(acu)} 个穴位、{len(mus)} 块肌肉。",
        "brand": title_zh, "brand_sub": f"{len(acu)} 穴 · {len(mus)} 肌",
        "today_line": f"复习：{len(acu)} 个穴位（{'、'.join(a['name'] for a in acu)}）· {len(mus)} 块肌肉（{'、'.join(m['zh'] for m in mus)}）",
        "study_plan": [["先自测（15 分钟）", "03 章所有问题，先说再展开"], ["看图找位（15 分钟）", "01 章经络图，在自己身上找一遍"],
                       ["读音（10 分钟）", "04 章读音表跟读两遍"], ["记忆卡（15 分钟）", "05 章记忆卡 + 复习中心"]],
        "tags": {"vertical": sorted({v for c in cs for v in c.get("tags", {}).get("vertical", [])}),
                 "horizontal": sorted({h for c in cs for h in c.get("tags", {}).get("horizontal", [])} | {"记忆法"})},
        "muscles": mus, "acupoints": acu, "figures": figs,
        "sources": [s for c in cs for s in c.get("sources", [])],
        "chapters": [
            {"num": 1, "id": "points", "title": ["This week's acupoints", "本周穴位"], "toc": ["Acupoints", "本周穴位"],
             "goals": [["Locate every point of the week on your own body.", "在自己身上找到本周每一个穴位。"]], "terms": [],
             "blocks": fig_blocks("acupoints") + [{"t": "acu_cards"}], "bridge": ["muscles", "Next: this week's muscles. 下一章：本周肌肉。", "02 Muscles"]},
            {"num": 2, "id": "muscles", "title": ["This week's muscles", "本周肌肉"], "toc": ["Muscles", "本周肌肉"],
             "goals": [["State origin, insertion, nerve and action of each muscle.", "说出每块肌肉的起点、止点、神经和动作。"]], "terms": [],
             "blocks": fig_blocks("muscles") + [{"t": "summary_tables"}], "bridge": ["quiz", "Next: every self-check question of the week. 下一章：本周全部自测题。", "03 Quiz"]},
            {"num": 3, "id": "quiz", "title": ["Self-check", "自测"], "toc": ["Quiz", "自测"],
             "goals": [["Answer aloud before opening each answer.", "先大声回答，再展开答案。"]], "terms": [], "blocks": [], "check": checks,
             "bridge": ["pron", "Next: pronunciation. 下一章：读音。", "04 Pronunciation"]},
            {"num": 4, "id": "pron", "title": ["Pronunciation", "读音"], "toc": ["Pronunciation", "读音"],
             "goals": [["Say every term with the right stress.", "每个术语都读对重音。"]], "terms": [],
             "blocks": ([{"t": "pron_table", "terms": pron_terms, "zh_map": zh_map}] if pron_terms else []),
             "bridge": ["cards", "Next: flashcards. 下一章：记忆卡。", "05 Cards"]},
            {"num": 5, "id": "cards", "title": ["Flashcards", "记忆卡"], "toc": ["Cards", "记忆卡"],
             "goals": [["Go through every card once.", "所有卡片过一遍。"]], "terms": [], "blocks": [{"t": "flashcards", "extra": []}]},
        ],
    }
    d = DAYS / date
    d.mkdir(parents=True, exist_ok=True)
    (d / "content.json").write_text(json.dumps(content, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    (d / "figures.py").write_text(
        "# -*- coding: utf-8 -*-\n\"\"\"Review day: copies the week's figures (generated by engine/review_pack.py).\"\"\"\n"
        "import re, shutil, sys, pathlib\nDAYS = pathlib.Path(__file__).resolve().parents[1]\nCOPIES = " + json.dumps(copies, ensure_ascii=False) + "\n\n"
        "def build(out_dir):\n    out = pathlib.Path(out_dir); out.mkdir(parents=True, exist_ok=True)\n"
        "    for src, name, *_ in COPIES:\n        s = (DAYS / src).read_text(encoding='utf-8')\n"
        "        old = re.search(r'fig(\\d\\d)-', s); new = name[:2]\n"
        "        if old: s = s.replace('fig' + old.group(1) + '-', 'fig' + new + '-')\n"
        "        (out / name).write_text(s, encoding='utf-8')\n\n"
        "if __name__ == '__main__':\n    build(sys.argv[1])\n", encoding="utf-8")
    return d / "content.json"
