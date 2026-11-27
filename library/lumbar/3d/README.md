# Back and lumbar spine 3D · 背部与腰椎三维部分

按 `standards/library/steps.md` 的 ST-7，每一章都有自己的 3D 部分。

现状（2026-11-27）：

- 网页借用肩部章节的 3D 程序（`library/shoulder/3d/`，`?topic=lumbar&term=vertebra-l4`）。结构映射写在 `../topic.json` 的 `viewer` 里：T12 和 L1–L5 椎骨、骶骨、尾骨、髋骨、第 12 肋和自带模型里已有的腰方肌。
- 自带模型缺的 9 块肌肉（腰髂肋肌、胸最长肌、胸棘肌、多裂肌、回旋肌、棘间肌、横突间肌、腰大肌、下后锯肌）由共用导出脚本生成附加模型。gui 2026-11-27 同意补（AN-43）。清单是本目录的 `atlas-addon.json`，产物在 `library/shoulder/3d/public/models/` 的 `z-anatomy-1.4.0-lumbar-addon.glb`、`lumbar-addon.metadata.json`、`lumbar-addon.provenance.json`。
- 重新导出：见 `site/build/atlas/README.md`，命令是 `python3 site/build/atlas/build-addon.py lumbar --blender-python <能 import bpy 的 Python>`，检查是 `python3 site/build/atlas/check-addon.py lumbar`。
- 横突间肌在模型里是腰横突间外侧肌的背侧部和腹侧部两块，所以分成两个词条（`intertransversarii-lateral-dorsal`、`intertransversarii-lateral-ventral`），从正文 1.6 节的链接打开。
- 模型和正文不完全一致的地方（多裂肌、棘间肌只有腰段，回旋肌是全长一块，没有横突间内侧肌）见 `atlas-addon.json` 的 `mappingNotes` 和 `../制作记录.md` 第 4 节。
