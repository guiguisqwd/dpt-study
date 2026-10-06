# Topic quality rules · 主题质量标准

These rules preserve the user's established requirements across every new anatomical topic. They are content acceptance criteria, not prompts to display inside a lesson.

这些规则保存用户已确定的学习习惯，适用于每个新解剖主题；它们是制作要求，不应作为 AI 提示词插入正文。

1. **English before Chinese · 英文在前、中文在后** — names, bones, landmarks, nerves, actions, diagram labels, captions, questions, answers and methodology terms use paired `en` and `zh` values. Write complete professional English first and a complete Chinese translation second. The shared renderer guarantees this order.
2. **Six sections · 六部分顺序** — anatomy → innervation → movement → clinical/regional anatomy → review → critical paper reading. New topics use the same `content.json` structure; do not create a new independent application or force unrelated material into the shoulder source.
3. **Attachments and course · 起止点与走行** — each named muscle records origin, insertion, course, actions and innervation. The course is a complete sentence: “The [muscle] originates from [site], passes [direction/relation], and inserts onto [site].” Annotated editable SVGs show actual Origin/起点 and Insertion/止点 labels associated with that muscle. A pathway flowchart alone does not substitute for an anatomical figure.
4. **Nerves and segments · 神经与节段** — explain C = Cervical/颈部, T = Thoracic/胸部, L = Lumbar/腰部 and S = Sacral/骶部, distinguish spinal nerve segments from vertebrae, and include anatomical nerve-course figures. Write root levels and anatomical relationships explicitly after checking sources.
5. **Exact model mapping · 三维结构准确对应** — model IDs come from the bundled renderable skeletal/muscular metadata, with correct anatomy, tissue and side. A missing muscle is named as missing, never linked to another muscle. Optional landmark coordinates remain pending until sourced and reviewed; model naming validation is not proof of spatial calibration.
6. **Complete review answers · 完整复习答案** — retain concise mnemonics alongside complete English explanations and Chinese translations. Answers cannot consist only of arrows, abbreviations or a compressed phrase.
7. **Critical reading · 论文批判性阅读** — cite primary sources; state the research question, design, population, methods, results, limitations and applicability. Explain methodology terms in English then Chinese. Do not invent a paper, result or missing fact. Apply an appropriate installed reading skill when actual paper analysis begins, rather than treating this template as research.
8. **Visual review · 视觉核验** — check the actual pages and SVGs at desktop and narrow widths. Avoid overlapping text/boxes, cropped labels and illegible figures. Check every 3D deep link and preserve viewpoint continuity in shared viewer interactions. Existing audio is preserved unless the user requests a change.
9. **Honest readiness · 如实标记完成状态** — new topics start as drafts. Only a model preview is exposed when the course is incomplete. Draft text is not presented as an established lesson. Sources and eight explicit QA checks, reviewer and date are required before `status: published` passes the build.
10. **Offline outputs · 离线输出** — each published standard topic generates Markdown with relative figure links. A PDF is optional and must be separately rendered and visually reviewed. A declared PDF includes a digest of the content and figures, so a stale PDF blocks publication. Do not advertise a nonexistent or outdated PDF.

## Contracts and commands · 数据约定与命令

- `topic.schema.json`: manifest and viewer mapping shape.
- `content.schema.json`: full structured lesson shape.
- `content-records.example.json`: copyable empty record shapes; no invented medical content.
- `templates/`: empty draft templates.
- `topiclib.py`: discovery, semantic validation and one shared renderer.

```sh
python3 scripts/new-topic.py --id knee --en 'Knee joint' --zh 膝关节
python3 scripts/validate-topics.py --topic knee
python3 scripts/validate-topics.py --topic knee --require-published
python3 scripts/build-topics.py
python3 -m unittest discover -s tests -v
```

The normal validator allows incomplete drafts and rejects invalid identifiers, unsafe assets and incorrect model mappings in every status. `--require-published` checks whether the selected topic is ready. The builder validates the entire catalog before replacing generated topic outputs. No external JSON Schema package is required; the Python validator is authoritative for semantic checks. Automated checks enforce structure, not medical truth or visual quality; a real source and layout review must precede signoff.

普通验证允许草稿缺项，但任何状态都不接受错误模型映射或越界文件路径。发布检查与程序自动检查不能替代真实的医学来源和视觉核验；完成这些核验后再填写签名与日期。
