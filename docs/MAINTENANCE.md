# Anatomy study workbench · 解剖学习工作台

用户要求将解剖学习作为独立项目，主要维护整个 Anatomy study 工作台：多主题课程、主题库、3D 查看器、阅读与离线导出、共享质量规则，以及 GitHub 构建和网站发布。肩袖是第一个课程，维护范围覆盖后续解剖主题和共用能力。

独立 Codex 项目拟命名为 **解剖学习工作台**。添加项目时选择现有仓库目录，无须复制或搬动文件；本文档本身不完成项目注册：

```text
/Users/guigui/Documents/ChatGPT/知识工作台/阅读输出/肩袖
```

本地“肩袖”“肩部3D学习”目录及 `shoulder-study` 仓库名保留兼容旧路径，不限制产品范围。上级“知识工作台”的其他项目不属于此仓库的维护范围。

## 入口与当前内容

- [GitHub 共同仓库](https://github.com/guiguisqwd/shoulder-study)
- [学习首页与主题库](https://guiguisqwd.github.io/shoulder-study/study.html)
- [肩袖主题](https://guiguisqwd.github.io/shoulder-study/topics/shoulder/index.html) · [标准阅读](https://guiguisqwd.github.io/shoulder-study/reading.html) · [Claude 阅读版](https://guiguisqwd.github.io/shoulder-study/reading-claude.html)
- [肩袖 3D 旧入口](https://guiguisqwd.github.io/shoulder-study/?term=humerus)
- [髋关节草稿](https://guiguisqwd.github.io/shoulder-study/topics/hip/index.html) · [骨骼模型预览](https://guiguisqwd.github.io/shoulder-study/?topic=hip&term=femur)

截至 2026-10-07，Shoulder / Rotator cuff（肩部／肩袖）为 `published`，Hip joint（髋关节）为 `draft`，已接入骨骼预览，完整课程尚未编写。后续以各主题的 `topic.json` 为准，不把草稿或模型预览称为完成课程。

## 维护位置

| 范围 | 源文件与入口 |
| --- | --- |
| 主题注册、课程与模型绑定 | `topics/<id>/topic.json`、`content.json`、`assets/`；新主题共用一份正文生成 HTML / Markdown |
| 主题库、共享阅读渲染与内容校验 | `platform/`、`scripts/build-platform.py`、`scripts/build-topics.py`、`scripts/validate-topics.py` |
| 3D 查看器、选择与相机交互 | `肩部3D学习/src/`；模型、既有语音及许可在 `肩部3D学习/public/` |
| 肩袖标准阅读与配图 | `reading-source/`、`2026-10-06-肩袖-阅读优化版-资源/`；沿用已有兼容构建 |
| Claude 独立阅读版 | `肩部3D学习/public/reading-claude.html`，独立维护，标准构建不得覆盖 |
| 离线导出与发布包 | `output/pdf/`、`reading-source/export-pdf.py`、`reading-source/prepare-web-release.py`；`website-release/` 是生成输出 |
| 自动检查与 GitHub Pages | `tests/`、`.github/workflows/pages.yml` |

构建和编辑边界见 [README](../README.md)；协作、提交与推送规则见 [CLAUDE.md](../CLAUDE.md)。新增主题按 [ADDING_A_TOPIC.md](./ADDING_A_TOPIC.md) 操作，内容和人工核验要求见 [QUALITY_RULES.md](../platform/QUALITY_RULES.md)，无需在每次新建关节课程时重新约定。

## 接手与交付

先读取规则并安全同步 GitHub，再修改源文件、执行适当检查，完成后提交并推送。维护共用能力时检查已有课程，保留旧链接、现有语音、Claude 独立阅读版和资产署名。内容质量、PDF 同步及发布核验沿用上述文档，不重复另设一套规则。

交付说明包括改动范围、核验结果、未完成项、commit、分支和部署状态，使下次任务从同一仓库继续。此文档记录维护职责，不自动安排定时任务，也不代表已授权尚未提出的课程制作。
