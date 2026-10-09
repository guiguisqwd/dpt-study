# Topic quality rules · 主题质量标准

The content rules now live in [`standards/`](../../../standards/README.md), the single source for what a piece must contain and how it is checked. This file keeps the topic data contracts and commands.

内容规则已统一到 [`standards/`](../../../standards/README.md)（2026-10-08），每条规则只写在那里一处。原来的十条对应如下：

| 原条目 | 现在的位置 |
| --- | --- |
| 1 English before Chinese | G-01、AN-01 |
| 2 Six sections | CH-01（主模板）、CH-02（短版） |
| 3 Attachments and course | AN-02、AN-03、AN-13、AN-14 |
| 4 Nerves and segments | AN-04、AN-12 |
| 5 Exact model mapping | AN-40 至 AN-43 |
| 6 Complete review answers | AN-06 |
| 7 Critical reading | AN-30 至 AN-35 |
| 8 Visual review | AN-16、QC-21、QC-24、QC-25、G-09 |
| 9 Honest readiness | G-03、`standards/library/checklist.md` |
| 10 Offline outputs | 本文件下方命令与 `library/README.md` §5 |

## Contracts and commands · 数据约定与命令

- `topic.schema.json`: manifest and viewer mapping shape.
- `content.schema.json`: full structured lesson shape.
- `content-records.example.json`: copyable empty record shapes; no invented medical content.
- `templates/`: empty draft templates.
- `topiclib.py`: discovery, semantic validation and one shared renderer.

```sh
python3 site/build/new-topic.py --id knee --en 'Knee joint' --zh 膝关节
python3 site/build/validate-topics.py --topic knee
python3 site/build/validate-topics.py --topic knee --require-published
python3 site/build/build-topics.py
python3 -m unittest discover -s tests -v
```

The normal validator allows incomplete drafts and rejects invalid identifiers, unsafe assets and incorrect model mappings in every status. `--require-published` checks whether the selected topic is ready. The builder validates the entire catalog before replacing generated topic outputs. No external JSON Schema package is required; the Python validator is authoritative for semantic checks. Automated checks enforce structure, not medical truth or visual quality; a real source and layout review must precede signoff.

普通验证允许草稿缺项，但任何状态都不接受错误模型映射或越界文件路径。发布检查与程序自动检查不能替代真实的医学来源和视觉核验；完成这些核验后再填写签名与日期。
