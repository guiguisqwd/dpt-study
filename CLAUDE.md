# Anatomy study · 解剖学习 — Claude collaboration rules

本文件记录用户对本项目的长期协作要求。Claude 在开始工作前应读取本文件；用户在当前对话中的明确指示优先于本文件。

用户要求将本仓库作为独立的“解剖学习工作台”项目维护，范围覆盖整个多主题学习工作台。项目职责、入口和接手说明见 [docs/MAINTENANCE.md](./docs/MAINTENANCE.md)；项目注册不由这些文档自动完成。

## 0. 多主题产品，肩袖是第一个主题

用户要求这个软件覆盖多个解剖主题；后续加入 Hip joint（髋关节）等内容时，应沿用已经确认的内容、图示、英语表达、模型联动与质量检查规范，避免重复修正同一类问题。

- 产品名为 **Anatomy study（解剖学习）**。GitHub 仓库于 2026-10-08 按用户要求由 `shoulder-study` 改名为 **`dpt-study`**（站点 `https://guiguisqwd.github.io/dpt-study/`），以涵盖解剖、经穴、3D、每日学习包和文献阅读。GitHub 会把旧仓库地址重定向到新仓库，但 Pages 旧站点路径不会自动跳转。本地“肩袖”和“肩部3D学习”目录仍是兼容路径，不表示产品只能有一个主题；未经明确迁移安排，不要重命名这些目录。
- 新主题放在 `topics/<slug>/`，由 `topic.json` 注册；用共享脚本发现、校验并构建。先读 [docs/ADDING_A_TOPIC.md](./docs/ADDING_A_TOPIC.md)，不要复制整个应用另建一套。
- 保持“共享界面与渲染逻辑”和“主题内容与模型映射”分离。一般新增关节应修改主题数据、图示和资料；如果确需扩展共享能力，扩展一次并检查已有主题。
- 肩袖使用兼容适配方式保留现有成熟阅读稿、3D 行为、语音和 Claude 独立版。不要为统一目录破坏已经完成的内容。
- `draft` 表示内容未完成，`published` 表示主题已完成相应核验。Hip joint 的起始目录是结构化草稿，不等于已完成的髋关节课程。不得把占位数据、未核对图示或未知模型当作已就绪学习材料。
- 自动检查可以发现结构和链接问题，不能证明解剖事实正确；发布前仍须核验资料和实际图文显示。

## 1. GitHub 是共同维护的项目来源

用户的原话：

> 直接存在 github 上，然后每次更新和修改都存在 github 上；写个 md 给 Claude，让他记录这个规则。

执行规则：**每次完成用户授权的内容或代码修改，都要在适当检查通过后提交到 Git，并推送到同一个 GitHub 仓库。只修改本地文件不算完成同步。** 不必为已经授权的正常提交和推送重复征求确认。

共同仓库：[guiguisqwd/dpt-study](https://github.com/guiguisqwd/dpt-study)；远端地址：`https://github.com/guiguisqwd/dpt-study.git`。该仓库为公开仓库，只放本项目可公开的学习内容、代码及必要资源。

- 本仓库根目录是解剖学习项目，包含主题数据、阅读源稿、配图、3D 应用和维护文档；本地目录仍沿用“肩袖”这一历史名称。不要把上级“知识工作台”中的其他项目一起加入版本控制。
- 用 `git remote get-url origin` 确认实际 GitHub 地址；用当前分支及其 upstream 确认推送目标。不要猜测仓库名称、分支或部署地址。
- 多台电脑、Codex 和 Claude 使用同一仓库；开始新工作前先同步远端，完成后推送。不要长期保留互不关联的“最终版”副本。
- 生成文件用于阅读和发布；可维护的源文件也必须进入仓库，不能只上传 `dist/`。

## 2. 每次修改的 Git 流程

1. 读取本文件、根目录 `README.md` 和相关子项目说明；运行 `git status --short --branch`、`git remote -v`，确认仓库、分支和未提交修改。
2. 运行 `git fetch origin`，检查本地与 upstream 的差异。工作区干净且能快进时，运行 `git pull --ff-only`。若存在用户或另一代理的未提交修改，先辨认归属、保留原文件，避免直接拉取造成覆盖。存在分叉时检查双方改动并整合，不要强行重置。
3. 修改源文件，再生成相应输出。先完成必要检查，检查 diff，只暂存此次任务需要的文件。不要把不相关修改、账户资料、API key、访问令牌、`.env`、语音暂存目录或依赖目录一并提交。
4. 使用描述实际变化的提交说明。正常完成任务时执行 `git commit` 和 `git push`，推送到已确认的当前工作分支及其 upstream。若用户要求 PR，按该流程提交 PR，不能把尚未合并的分支称为已上线。
5. 推送后核对远端目标分支的 commit 与本地 `HEAD`，报告提交号和推送结果。若存在发布工作流，再核对运行结果和线上入口；“已推送”与“已部署成功”分别报告。

不得自动 `push --force`、`reset --hard`、删除他人分支或覆盖他人工作。遇到权限、网络、合并冲突或发布失败，应保留已完成的文件和提交，说明准确阻碍；不能声称“已同步 GitHub”或“已上线”。推送被拒绝时，先获取远端新提交并检查差异，保护双方工作。

## 3. 文件与构建边界

| 需要修改的内容 | 应编辑的位置 |
| --- | --- |
| 主题目录、状态、标题与入口 | `topics/<slug>/topic.json` |
| 新主题内容、资料及模型映射 | 对应 `topics/<slug>/`；创建方式与校验见 `docs/ADDING_A_TOPIC.md` |
| 主题生成与校验规则 | 根目录 `scripts/` 中共享脚本 |
| 共享主题内容规范、页面渲染和主题库样式 | `platform/` |
| 肩袖六章阅读正文 | `reading-source/sections/` 中对应的 `.html` 与 `.md`，两者同步维护 |
| 肩袖阅读版式与目录 | `reading-source/reading.css`、`reading-source/templates/` |
| 肩袖可编辑解剖配图 | `2026-10-06-肩袖-阅读优化版-资源/` 中的 SVG |
| 肩袖肌肉、模型跳转及资料依据 | `reading-source/data/` |
| 共享 3D 页面、状态与交互 | `肩部3D学习/src/` |
| 模型、音频、许可等公开资源 | `肩部3D学习/public/` |
| Claude 独立阅读版 | `肩部3D学习/public/reading-claude.html` |
| 每日学习包（内容、配图、流水线、运行记录） | `daily/`：每天的 `days/<date>/content.json` 与 `figures.py`；共用引擎在 `daily/engine/`；说明见 `daily/README.md`。`肩部3D学习/public/daily/` 是生成输出 |

`reading-claude.html` 是独立维护的版本，必须保留。标准阅读构建不得覆盖它；修改该版时以 `public/reading-claude.html` 为源，不要只改 `dist/` 中的副本。

新主题正文只维护一份 `content.json`，共同生成 HTML 和 Markdown。主题校验与生成在仓库根目录运行：

```sh
python3 scripts/validate-topics.py
python3 scripts/build-platform.py
```

`肩部3D学习/public/topics.json` 和 `public/topics/` 是主题构建输出，不能只在其中修改正文。新主题先保持 `draft`，按 `docs/ADDING_A_TOPIC.md` 完成内容与验证后再改为 `published`。

`python3 scripts/build-platform.py` 生成主题页和自动发现主题的 `study.html` 学习首页；应用的 `prebuild` / `predev` 会调用它，因此正常的 `pnpm build` / `pnpm dev` 会同步主题库。

仅在修改肩袖标准阅读源稿时运行 `python3 reading-source/build-reading.py`，更新原有 HTML / Markdown 输出，再构建应用；这项兼容流程不需要复制到新主题。

3D 应用构建：

```sh
cd 肩部3D学习
pnpm install --frozen-lockfile
pnpm build
```

依赖已安装且锁文件未变时，无须重复安装。`pnpm build` 包含 TypeScript 检查；改变穴位参照或几何逻辑时另运行 `pnpm test:geometry`。对阅读版式、图示、模型链接及交互的修改，要在浏览器中检查实际效果，不能仅以编译通过替代视觉检查。

发布材料由根目录的 `reading-source/prepare-web-release.py` 生成到 `website-release/`。正式发布传入 `--site-url` 和实际 HTTPS 根地址（包括 GitHub Pages 项目子路径），使 HTML、Markdown 和 PDF 中的 3D 链接指向线上站点。

GitHub Pages 的 Source 已设为 GitHub Actions。`.github/workflows/pages.yml` 在推送 `main` 时执行检查、构建和发布；PR 仅检查与构建。它使用 Node.js 24、pnpm 11.19.0、Python 3.13，以及 `reading-source/requirements-publish.txt` 固定的 `pypdf==6.10.0`。本地保存不会自动上线；每次修改完成后提交并推送到 `main`，且工作流发布成功，才会更新网站。必须核对 Actions 和站点结果。

线上入口如下；首次部署已于 2026-10-06 通过 GitHub Actions，并验证阅读、3D 和下载入口返回 HTTP 200。以后每次部署仍需检查运行结果：

- 学习首页：`https://guiguisqwd.github.io/dpt-study/study.html`
- 标准阅读：`https://guiguisqwd.github.io/dpt-study/reading.html`
- Claude 阅读版：`https://guiguisqwd.github.io/dpt-study/reading-claude.html`
- 3D：`https://guiguisqwd.github.io/dpt-study/?term=humerus`

PDF 和 Markdown 离线输出位于 `output/pdf/`。目前发布使用已核验的 38 页 PDF，仅用 `pypdf` 更新其中的线上链接，不重新排版。PDF 重新导出目前依赖 Mac 字体和本地渲染环境；正文或配图变化后，按 `制作流程-肩袖双语学习.md` 重新导出并检查，再提交更新。不要把旧 PDF 标为已同步，也不要假设 Ubuntu 发布工作流会自动重建 PDF。

## 4. 所有主题共同遵守的内容与界面规则

- 所有解剖专业词汇、骨性结构、神经、动作、图标及答案：**英文在前，中文在后**。完整英文描述后给出完整中文翻译。
- 肌肉需提供 Origin（起点）、Insertion（止点）、走行及相关解剖关系；图上标出起止点，并与正文对应。使用完整句式，例如：`The [muscle] originates from [origin], passes [direction or relation], and inserts onto [insertion].` 句式是表达模板，填入的解剖内容仍须核验，不能按肩袖数据套用其他关节。
- 神经需要实际解剖位置图，并标出起源、走行及支配对象；流程图只能作为补充。区分 `C = Cervical（颈部）`、`T = Thoracic（胸部）`、`L = Lumbar（腰部）`、`S = Sacral（骶部）`，明确数字指神经节段还是椎骨，不能混写。
- 沿用六阶段顺序：Anatomy（解剖）→ Innervation（神经支配）→ Movement（动作）→ Clinical anatomy（临床解剖）→ Review（复习）→ Paper reading（论文阅读）。动作部分也需关联参与肌肉的起止点及具体走行。正文不放 AI 提示词、制作过程或空泛学习引导，维护记录放文档。
- Review 保留简记，同时提供完整专业英文描述、中文翻译和完整问答；不能只给压缩口诀。Paper reading 采用英文在前的双语方法学术语，说明研究问题、设计、人群、干预/比较、结局、结果与局限，区分原文结论和解读。
- 结构链接必须带正确的主题和实际存在的 `?term=` / `?point=`，并与模型映射中的真实 ID 核对。不存在的模型要明确缺项，不能猜 ID 或链接到另一块肌肉代替；旧肩袖链接仍需可用。
- 保持旋转、缩放、切换结构和主题时的连续性；检查宽屏、分屏与窄屏下的字图遮挡、标签换行及重叠。图示可读性和交互要在浏览器中手动验证，不能仅靠构建通过。
- **保留现有语音、音频文件、读音操作与来源记录。未经用户新指示，不更换声音或重新生成语音。**
- 穴位是模型中的解剖学习参照；保留其校准状态和证据范围，不把任意深部坐标称为标准穴位或进针路径。
- 保留研究来源、证据不足与模型许可说明，不虚构验证结果。
- 创建新主题时即按以上要求收集、编排和核验内容，不等用户再次指出英文顺序、缺图、起止点或答案不完整才补。

## 5. Claude 的权限与协作方式

公开网站或公开 GitHub 地址允许读取资料，**不会自动赋予 Claude 写入权限**。Claude 必须通过用户已经授权的本地仓库、Claude Code 或支持写入的 GitHub 集成，才能提交和推送。不要在聊天、网页或仓库中索取或保存令牌。

本文件是可版本化的项目规则，不代表已经修改了 Claude 账户的永久记忆或已授予账户权限。支持自动读取 `CLAUDE.md` 的工具应在仓库根目录工作；其他 Claude 界面应先读取或附加本文件，再开始修改。

最终交付说明应包含：改了什么、完成了哪些检查、commit、实际推送分支，以及部署状态（若此次涉及部署）。
