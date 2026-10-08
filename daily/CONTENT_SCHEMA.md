# content.json · schema `dpt-daily-pack/1`

One file per day in `days/<date>/content.json`. Copy the previous day's file and change the data;
`engine/schema.py` checks it, `engine/render.py` turns it into the six chapters. `days/2026-10-07/`
is the reference day.

## Top level

| Field | Meaning |
| --- | --- |
| `schema` | `"dpt-daily-pack/1"` |
| `date`, `day`, `kind` | `"2026-10-08"`, `2`, `"learning"` (`weekly_review` / `final_review` are generated) |
| `slug_zh` | short Chinese title used in file names: `肺经与胸前肌` → `2026-10-07-第1天-肺经与胸前肌` |
| `title` | `{"zh": …, "en": …}` page title |
| `page_title`, `description`, `brand_sub`, `footer`, `md_prefix` | optional overrides |
| `today_line` | header line: today's new points, new muscles, number of review cards |
| `study_plan` | four `[bold, text]` steps (optional; default 10/20/15/5 minutes) |
| `tags` | `{"vertical": [...], "horizontal": [...]}` archive tags (see README) |
| `muscles` | list, same order as the plan (fields below) |
| `acupoints` | list, same order as the plan (fields below) |
| `memory` | `{"title": [en, zh], "steps": [[en, zh, text_en, text_zh] ×3], "hook": [en, zh]}` — the "how to remember" card |
| `figures` | `{"01": "Chinese file name", …}` every figure figures.py draws; each must be shown somewhere |
| `pronunciation` | extra `{term: [IPA, "STRESS-ed syl-la-bles", dictionary_url]}` (merged over engine/data/pronunciation.json) |
| `sources` | `[[url, label], …]` shown at the end of the English chapter |
| `chapters` | six chapters (below) |

## Muscle

`id`, `en`, `zh`, `letter` (big initial on the card), `color` (CSS colour), `figure` (its O/I figure number),
`o`, `i`, `n`, `a` (each `[English, 中文]`; `n` must include spinal segments, e.g. `(C5–C7)`),
`sentence` (`[“The X originates from …, passes …, and inserts onto ….”, 中文]`), `acu`, `acu_en` (acupoint anchor),
`o_short`, `i_short`, `n_short`, `a_short` (`[en, zh]` for the summary table), `source` (URL),
optional `extra_pairs` (more `[en, zh]` paragraphs on the card: relations, clinical point, palpation),
optional `vertical` / `horizontal` (item-level archive tags).

## Acupoint

`name`, `pinyin` (tone marks), `code`, `meridian`, `loc` (GB/T 12346 wording), optional `loc_en` (WHO 2008),
`loc_short` (short English), `layers` (`皮肤 → 皮下组织 → … → 深层`), `safety`, `muscles`, `find`,
optional `special` (特定穴: 络穴, 原穴, 井穴 …), `sources` (URLs), optional `vertical` / `horizontal`.

## Chapter

```json
{"num": 1, "id": "muscles", "title": ["Muscles: …", "今日肌肉：…"], "toc": ["Muscles", "今日肌肉"],
 "goals": [[en, zh], …], "terms": [[en, zh], …] (acupoint terms: [name, pinyin, "zh"]),
 "blocks": [ … ], "check": [[question_en, question_zh, answer_en, answer_zh], …],
 "take": [en, zh], "bridge": [next_chapter_id, "Next: … 下一章：…", "02 Innervation"]}
```

Learning days use exactly: `muscles`, `nerve`, `motion`, `acupoints`, `review`, `english`.

## Blocks

| `t` | Fields | Renders |
| --- | --- | --- |
| `p` | `en`, `zh` | English paragraph, Chinese translation |
| `h3` | `en`, `zh` | sub-heading |
| `fig` | `n`, `en`, `zh` | figure `n` with caption |
| `muscle_cards` | — | O/I card per muscle (+ the memory card) |
| `acu_cards` | `show_en_loc` (optional) | one card per acupoint |
| `levels` | `title`, `items: [[segments, 中文], …]` | nerve-level key (C = Cervical …) |
| `pitfall` | `zh`, `label` | highlighted note (易混点) |
| `song` | `zh`, `label` | traditional point song |
| `summary_tables` | — | muscle table + acupoint table |
| `pron_table` | `terms`, `zh_map` | stress + IPA + dictionary table |
| `flashcards` | `extra: [[front_en, front_zh, back_en, back_zh], …]` | card deck (points + muscles + extras) |
| `sources` | `note`, `end: true` | sources line (after the self-check) |
| `html` | `html`, `md` | escape hatch for one-off markup |

Any block may carry `"end": true` to render after the chapter's self-check.
