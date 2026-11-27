# Lumbar 3D · 背部与腰椎三维部分

按 `standards/library/steps.md` 的 ST-7，每一章都有自己的 3D 部分。

现状（2026-11-27）：

- 网页借用肩部章节的 3D 程序（`library/shoulder/3d/`，`?topic=lumbar&term=vertebra-l4`）。结构映射写在 `../topic.json` 的 `viewer` 里：T12 和 L1–L5 椎骨、骶骨、尾骨、髋骨、第 12 肋，自带模型里已有的腰方肌，以及附加模型的 9 块肌肉。
- 自带模型缺的 9 块肌肉（腰髂肋肌、胸最长肌、胸棘肌、多裂肌、回旋肌、棘间肌、横突间肌、腰大肌、下后锯肌）由共用导出脚本生成附加模型。gui 2026-11-27 同意补（AN-43）。清单是本目录的 `atlas-addon.json`，产物在 `library/shoulder/3d/public/models/` 的 `z-anatomy-1.4.0-lumbar-addon.glb`、`lumbar-addon.metadata.json`、`lumbar-addon.provenance.json`。
- 重新导出：见 `site/build/atlas/README.md`，命令是 `python3 site/build/atlas/build-addon.py lumbar --blender-python <能 import bpy 的 Python>`，检查是 `python3 site/build/atlas/check-addon.py lumbar`。
- 3D 程序按 `topics.json` 的 `viewer.addons` 载入附加模型（构建时只要本目录有 `atlas-addon.json` 就自动加上）。

模型和正文不完全一样的地方（清单的 `mappingNotes` 有实测数字）：

- **多裂肌**：Z-Anatomy 把多裂肌分成颈、胸、腰三段，本章只导出腰段，词条叫 `multifidus-lumborum`（Multifidus lumborum 腰多裂肌）。正文里 multifidus 的链接打开它。网格下端停在骶骨上缘上方约 1 cm，正文写的骶骨起点模型里没有。
- **棘间肌**：只导出腰段，词条 `interspinales-lumborum`。
- **横突间肌**：Z-Anatomy 只有腰外侧横突间肌，每侧分背侧部和腹侧部两块网格，所以是两个词条（`lateral-intertransversarii-dorsal`、`lateral-intertransversarii-ventral`），和髋部股二头肌长头、短头的做法一样；腰内侧横突间肌没有网格，是模型缺项（AN-41）。
- **回旋肌**：每侧一块网格，贯穿整条脊柱，看不出正文写的“胸段最发达、腰段常不恒定”。
- **腰大肌**：和髋部附加模型里的腰大肌是同一块源网格。附加模型的 ID 只能由它所属的章节使用（QC-09），所以本章用 `lumbar-psoas-major-muscles` 这个组名再导出一次，ID 不重复。
- 肌肉卡片上，多裂肌、棘间肌、横突间肌因为词条名和肌肉名不同，不显示“Explore in 3D”按钮，改成一句说明，句子里的英文肌名带链接。
