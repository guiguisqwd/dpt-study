# Authoring brief · 2026-10-17 周六

Week 1 · chapter `shoulder` (肩袖 Rotator cuff) · rules: `standards/daily/README.md`

## Today's chapters (one per plan entry, same order; content/items/forms copied exactly from plan/weeks.json)

1. **quiz 本周小测** (旧的夯实)
   - items: ["本周新旧混合小测"]
   - forms: F-6 自测题（选择、填空、看图标注） → block `quiz`
2. **review 跨周间隔复习** (旧的夯实)
   - items: ["跨周间隔复习"]
   - forms: F-10 间隔复习（DL-15） → block `due_cards`

## What to write

1. `daily/days/2026-10-17/content.json` — schema `dpt-daily-pack/2`, kind `supplement`, `week` 1, `chapter` `shoulder`, `chapter_name` `肩袖 Rotator cuff`. Each chapter carries `content`, `items`, `forms` as above plus the usual title/toc/goals/terms/blocks/bridge. Field and block definitions: `daily/CONTENT_SCHEMA.md` (v2 section); the last weekly pack is `daily/days/2026-10-16/content.json`.
2. `daily/days/2026-10-17/figures.py` — `build(out_dir)` drawing every figure in `content.figures` with `engine.figlib` (an empty build is fine when no figure is needed). To reuse a chapter figure (DL-03) call `copy_library_figure(chapter, name, out_dir, out_name)`; it strips the displacement filter the figure check rejects.
3. Consolidation (O-x): take the facts from the chapter `library/shoulder/content.json` (DL-01), do not rewrite them differently.
   New content: N-1 acupoints in `content.acupoints` with `meridian` (AN-20 to AN-24); N-5 papers come from `daily/papers/<id>.json` (block `paper`);
   N-2/N-3/N-4/N-6/N-7 need sources you actually opened (G-02); N-4 cases are teaching cases.
4. Rules: English first then Chinese; pronunciation for every English key term (content.pronunciation or engine/data/pronunciation.json); no public-health framing; archive tags (tags.vertical with fixed top levels, tags.horizontal).
5. Then run `python3 daily/pipeline.py evening --date 2026-10-17` again.
