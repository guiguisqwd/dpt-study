# Shoulder adapter · 肩袖兼容层

`topic.json` registers the rotator cuff chapter in the shared topic library. Like every chapter, its six
sections live in one source, `content.json` (with `pronunciation.json` and the SVGs in `figures/`); the shared
renderer in `site/build/platform/reading.py` writes both the HTML page and the Markdown from it, and
`text/build-reading.py` writes them to the historical paths (`text/2026-10-06-肩袖-阅读优化版.html` / `.md`
and `3d/public/reading.html`). The PDF is in `pdf/`, the 3D site in `3d/`, and the independent Claude
edition in `3d/public/reading-claude.html`.
`adapter: shoulder` only keeps the historical addresses working (reading.html, `?term=` links without
`?topic=`); the content is validated exactly like a standard chapter. It is reserved for this topic.

本章和其他章一样只维护一份 `content.json`（另有 `pronunciation.json` 与 `figures/` 里的 SVG），网页和
Markdown 由共用渲染器同时生成；`text/build-reading.py` 把结果写到旧地址。`shoulder` 适配方式只负责保留旧网址，
不放宽任何内容检查；Claude 阅读版 `3d/public/reading-claude.html` 独立维护，构建不会覆盖它。

发布前的 8 项核验（`library/README.md` §4）记录在 [`发布签核.md`](./发布签核.md)：每项的结果、证据、检查人、日期，以及仍待处理的问题（目前 PDF 尚未随正文重新导出）。
