# 第 3 层 · 生理解剖检查清单

ST-5 核验时逐条过。自动项由脚本检查；人工项要留截图或记录作证据，未做的不能勾为通过（G-03）。

## 自动检查

| 编号 | 检查 | 对应规则 | 现在由谁检查 |
| --- | --- | --- | --- |
| QC-01 | 六章齐全、顺序正确 | CH-01/CH-02 | `build-reading.py`、`topiclib.py`、`daily/engine/schema.py` |
| QC-02 | 图示占位符都有对应 SVG，SVG 是有效 XML，页面 id 唯一 | AN-10、AN-17 | `build-reading.py`、`daily` 构建 |
| QC-03 | Markdown 图片路径有效 | G-08 | `build-reading.py` |
| QC-04 | 每个 3D term / point 在模型词库中存在；缺项为 `null` | AN-40、AN-41 | `build-reading.py`、`topiclib.py` |
| QC-05 | 英文在前；肌肉 O/I/N/A 和句式齐全；穴位字段齐全 | AN-01 至 AN-03、AN-20 | `daily/engine/schema.py`（主题包尚未覆盖） |
| QC-06 | 读音覆盖所有英文关键术语 | AN-07 | `daily/engine/qa/qa.js`（主题包尚未覆盖） |
| QC-07 | SVG 文字出界、重叠；手机宽度显示 | AN-16 | `daily/engine/qa/qa.js` |
| QC-08 | ST-1 结构清单存在；每一项在它所列的章节正文里出现；3D ID 真实存在；正文里每条肌肉记录都在清单里 | ST-1、AN-40、AN-41 | `site/build/platform/topiclib.py`（草稿记为待办，`published` 时报错） |

## 人工检查

| 编号 | 检查 | 对应规则 |
| --- | --- | --- |
| QC-20 | 每项解剖事实都能对上来源，简化图与真实结构的差别已说明 | G-02、AN-50 |
| QC-21 | 逐张看截图：标签不压结构、引线不交叉且指向正确、穴位点位置正确、没有被裁掉的内容、图文一致 | AN-16、AN-17、AN-21 |
| QC-22 | 每段英文后面都有对应中文；问答展开后答案完整 | AN-01、AN-06 |
| QC-23 | 论文数值、单位、时间点与核对记录一致；核对层级已写明 | AN-31 至 AN-33 |
| QC-24 | 点开代表性 3D 链接，确认选中结构、侧别正确；旋转、缩放、切换、后退无跳跃 | AN-40、AN-42 |
| QC-25 | 宽屏、分屏、窄屏下无遮挡和溢出 | AN-16 |
| QC-26 | 制作记录列出所有未核验项 | G-03 |

新主题从 `draft` 改为 `published` 前，以上各项和 `library/README.md` §4 的 8 项签核都要完成，并记录审核人和日期。
