# Authoring brief · 2026-10-14 周三

Week 1 · chapter `shoulder` (肩袖 Rotator cuff) · rules: `standards/daily/README.md`

## Today's chapters (one per plan entry, same order; content/items/forms copied exactly from plan/weeks.json)

1. **N-4 临床案例** (新)
   - items: ["Supraspinatus tendinopathy 冈上肌腱病案例"]
   - forms: F-3 实际案例（SOAP） → block `case`; F-4 口语实操：英文问诊、给病人解释、向同事汇报；附示范对话和读音 → block `dialogue`
2. **O-4 神经分布：节段、走行、皮节和肌节、卡压点** (旧的夯实)
   - items: ["Suprascapular nerve", "Axillary nerve"]
   - forms: F-8 听音辨词：听英文读音，写出结构名 → block `listen`; F-11 手敲笔记：给提示，凭记忆打出来，再对照原文 → block `notes`

## What to write

1. `daily/days/2026-10-14/content.json` — schema `dpt-daily-pack/2`, kind `supplement`, `week` 1, `chapter` `shoulder`, `chapter_name` `肩袖 Rotator cuff`. Each chapter carries `content`, `items`, `forms` as above plus the usual title/toc/goals/terms/blocks/bridge. Field and block definitions: `daily/CONTENT_SCHEMA.md` (v2 section); the last weekly pack is `daily/days/2026-10-13/content.json`.
2. `daily/days/2026-10-14/figures.py` — `build(out_dir)` drawing every figure in `content.figures` with `engine.figlib` (an empty build is fine when no figure is needed). To reuse a chapter figure (DL-03) call `copy_library_figure(chapter, name, out_dir, out_name)`; it strips the displacement filter the figure check rejects.
3. Consolidation (O-x): take the facts from the chapter `library/shoulder/content.json` (DL-01), do not rewrite them differently.
   New content: N-1 acupoints in `content.acupoints` with `meridian` (AN-20 to AN-24); N-5 papers come from `daily/papers/<id>.json` (block `paper`);
   N-2/N-3/N-4/N-6/N-7 need sources you actually opened (G-02); N-4 cases are teaching cases.
4. Rules: English first then Chinese; pronunciation for every English key term (content.pronunciation or engine/data/pronunciation.json); no public-health framing; archive tags (tags.vertical with fixed top levels, tags.horizontal).
5. Then run `python3 daily/pipeline.py evening --date 2026-10-14` again.
