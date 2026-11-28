# TMJ 3D · 头面部与颞下颌关节三维部分

按 `standards/library/steps.md` 的 ST-7，每一章都有自己的 3D 部分。

现状（2026-11-28）：

- 网页借用肩部章节的 3D 程序（`library/shoulder/3d/`，`?topic=tmj&term=mylohyoid`）。结构映射写在 `../topic.json` 的 `viewer` 里。
- 自带模型里已有、已经接上的 11 个词条：下颌舌骨肌、颏舌骨肌、茎突舌骨肌、二腹肌前腹、二腹肌后腹、颧大肌、口轮匝肌、眼轮匝肌眶部、眼轮匝肌睑部、颊肌（模型拼作 Bucinator）、颈阔肌。
- 二腹肌和眼轮匝肌在模型里各分成两块网格，所以各是两个词条，和髋部股二头肌长头、短头的做法一样。肌肉卡片上这两块肌不显示“Explore in 3D”按钮，正文里的 anterior belly、posterior belly、orbital part、palpebral part 带链接。
- 自带模型**没有**：全部颅骨（下颌骨、颞骨、颧骨、蝶骨、上颌骨、额骨、顶骨、枕骨、鼻骨、舌骨）、四块咀嚼肌（咬肌、颞肌、翼内肌、翼外肌）和枕额肌。所以 21 个骨性标志和这 5 块肌肉现在不能在 3D 中打开，正文里已写明（AN-41）。

## 等 gui 同意的事（AN-43）

要不要给本章导出一个头部附加模型。提议清单在本目录的 `atlas-addon.proposed.json`，共 16 组：

- 骨 10 组：下颌骨、颞骨、颧骨、蝶骨、上颌骨、额骨、顶骨、枕骨、鼻骨、舌骨。
- 肌肉 6 组：咬肌（浅部、深部）、颞肌、翼内肌、翼外肌（上头、下头）、枕额肌（额腹、枕腹）、帽状腱膜。

清单里的源网格名已对照 Z-Anatomy 源文件核对过，都存在。文件名带 `.proposed`，构建和 CI 不会把它当成已启用的附加模型。

同意以后要做的：

1. 把 `atlas-addon.proposed.json` 改名为 `atlas-addon.json`。
2. 运行 `python3 site/build/atlas/build-addon.py tmj --blender-python <能 import bpy 的 Python>`，再运行 `python3 site/build/atlas/check-addon.py tmj`。
3. 在 `../topic.json` 的 `viewer.terms` 里加上这些骨和肌肉，把 5 块肌肉和 21 个骨性标志的 `modelTermId` 接上，去掉对应的 `modelUnavailableReason`。
4. 在 3D 页面里逐个打开检查位置和左右。

神经（三叉神经、面神经）在 Z-Anatomy 源文件里是曲线，不是网格，这次不提议导出；配图里的神经走行已经取自这些曲线。
