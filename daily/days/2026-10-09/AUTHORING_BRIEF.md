# Authoring brief · 2026-10-09

Kind: **learning**
Day 3 · meridians: 手阳明大肠经 · regions: 肩带与肩部

## Today's items (must match exactly, same order)

Acupoints: 二间 LI2、三间 LI3、合谷 LI4、阳溪 LI5、偏历 LI6、温溜 LI7

Muscles: 肩胛提肌 Levator scapulae、大菱形肌 Rhomboid major、小菱形肌 Rhomboid minor

## What to write

1. `daily/days/2026-10-09/content.json` — schema `dpt-daily-pack/1`; copy the structure of `daily/days/2026-10-08/content.json` (six chapters muscles → nerve → motion → acupoints → review → english, block types in `daily/CONTENT_SCHEMA.md`).
2. `daily/days/2026-10-09/figures.py` — `build(out_dir)` that draws every figure declared in `content.figures` with `engine.figlib` (reuse region base art: chest.py, arm.py, …; add new base art to engine/figlib/ when a new region appears).
3. Facts: verify from sources you actually open (StatPearls/NCBI, TeachMeAnatomy, Kenhub, Radiopaedia; acupoints: GB/T 12346-2021, WHO 2008, 《针灸学》). Put URLs in muscle.source / acupoint.sources / content.sources. Never invent; mark uncertainty in text.
4. Rules: English first then Chinese; muscle sentence 'The X originates from …, passes …, and inserts onto ….'; nerve with segments (C = Cervical 颈部, T = Thoracic 胸部); nerve figure starts from the spine; movement explained from line of pull with firing order/force couples where relevant; every acupoint: GB/T location, layers skin → deep, safety, related muscles, how to find, shown on a figure with the surrounding muscles; layer figures say 'not needling depth or direction'; pronunciation (IPA + CAPS stress + dictionary URL) for every English key term; no public-health framing; archive tags (tags.vertical with fixed top levels, tags.horizontal from the controlled vocabulary in DPT-每日简报/README.md).
5. Then run `python3 daily/pipeline.py evening --date 2026-10-09` again.
