# Shoulder study — Claude collaboration rules

本文件记录用户对本项目的长期协作要求。Claude 在开始工作前应读取本文件；用户在当前对话中的明确指示优先于本文件。

## 1. GitHub 是共同维护的项目来源

用户的原话：

> 直接存在 github 上，然后每次更新和修改都存在 github 上；写个 md 给 Claude，让他记录这个规则。

执行规则：**每次完成用户授权的内容或代码修改，都要在适当检查通过后提交到 Git，并推送到同一个 GitHub 仓库。只修改本地文件不算完成同步。** 不必为已经授权的正常提交和推送重复征求确认。

共同仓库：[guiguisqwd/shoulder-study](https://github.com/guiguisqwd/shoulder-study)；远端地址：`https://github.com/guiguisqwd/shoulder-study.git`。该仓库为公开仓库，只放本项目可公开的学习内容、代码及必要资源。

- 本仓库根目录是“肩袖”项目，包含阅读源稿、配图、3D 应用和维护文档。不要把上级“知识工作台”中的其他项目一起加入版本控制。
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
| 六章阅读正文 | `reading-source/sections/` 中对应的 `.html` 与 `.md`，两者同步维护 |
| 阅读版式与目录 | `reading-source/reading.css`、`reading-source/templates/` |
| 可编辑解剖配图 | `2026-10-06-肩袖-阅读优化版-资源/` 中的 SVG |
| 肌肉、模型跳转及资料依据 | `reading-source/data/` |
| 3D 页面、状态与交互 | `肩部3D学习/src/` |
| 模型、音频、许可等公开资源 | `肩部3D学习/public/` |
| Claude 独立阅读版 | `肩部3D学习/public/reading-claude.html` |

`reading-claude.html` 是独立维护的版本，必须保留。标准阅读构建不得覆盖它；修改该版时以 `public/reading-claude.html` 为源，不要只改 `dist/` 中的副本。

在仓库根目录重新生成标准阅读页及 Markdown：

```sh
python3 reading-source/build-reading.py
```

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

- 学习首页：`https://guiguisqwd.github.io/shoulder-study/study.html`
- 标准阅读：`https://guiguisqwd.github.io/shoulder-study/reading.html`
- Claude 阅读版：`https://guiguisqwd.github.io/shoulder-study/reading-claude.html`
- 3D：`https://guiguisqwd.github.io/shoulder-study/?term=humerus`

PDF 和 Markdown 离线输出位于 `output/pdf/`。目前发布使用已核验的 38 页 PDF，仅用 `pypdf` 更新其中的线上链接，不重新排版。PDF 重新导出目前依赖 Mac 字体和本地渲染环境；正文或配图变化后，按 `制作流程-肩袖双语学习.md` 重新导出并检查，再提交更新。不要把旧 PDF 标为已同步，也不要假设 Ubuntu 发布工作流会自动重建 PDF。

## 4. 用户确定的内容与界面规则

- 所有解剖专业词汇、骨性结构、神经、动作、图标及答案：**英文在前，中文在后**。完整英文描述后给出完整中文翻译。
- 肌肉需描述 Origin（起点）、Insertion（止点）、走行及相关解剖关系。使用完整句式，例如：`The [muscle] originates from [origin], passes [direction or relation], and inserts onto [insertion].`
- 区分 `C = Cervical（颈部）` 与 `T = Thoracic（胸部）`，区分椎骨和神经节段。图示与说明应能直接对应，避免只给抽象流程让读者记忆。
- 保持先解剖、后文章阅读的六章顺序；正文不放 AI 提示词、制作过程或空泛学习引导。维护记录放文档。
- 05 节保留简记，也保留完整专业英文叙述、中文翻译和完整答案；06 节论文方法学术语采用英文在前的双语说明。
- 结构链接必须匹配实际 `?term=` / `?point=`。不存在的模型应说明缺项，不能链接到另一块肌肉代替。
- 保持旋转、缩放、切换结构时的连续性，检查窄屏下的字图遮挡和重叠。
- **保留现有语音、音频文件、读音操作与来源记录。未经用户新指示，不更换声音或重新生成语音。**
- 穴位是模型中的解剖学习参照；保留其校准状态和证据范围，不把任意深部坐标称为标准穴位或进针路径。
- 保留研究来源、证据不足与模型许可说明，不虚构验证结果。

## 5. Claude 的权限与协作方式

公开网站或公开 GitHub 地址允许读取资料，**不会自动赋予 Claude 写入权限**。Claude 必须通过用户已经授权的本地仓库、Claude Code 或支持写入的 GitHub 集成，才能提交和推送。不要在聊天、网页或仓库中索取或保存令牌。

本文件是可版本化的项目规则，不代表已经修改了 Claude 账户的永久记忆或已授予账户权限。支持自动读取 `CLAUDE.md` 的工具应在仓库根目录工作；其他 Claude 界面应先读取或附加本文件，再开始修改。

最终交付说明应包含：改了什么、完成了哪些检查、commit、实际推送分支，以及部署状态（若此次涉及部署）。
