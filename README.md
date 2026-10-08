# Anatomy study · 解剖学习

面向多个解剖主题的双语学习网站。每个主题沿用同一套学习顺序、英文表达、解剖图示、3D 联动和核验标准；肩袖是第一个主题，Hip joint（髋关节）作为后续主题草稿保留扩展位置。

**GitHub 是共同维护的项目来源：每次授权修改，检查后提交并推送。** 仓库 [guiguisqwd/dpt-study](https://github.com/guiguisqwd/dpt-study)（2026-10-08 由 shoulder-study 改名）。Claude 与其他协作者先读 [CLAUDE.md](./CLAUDE.md)。

- [学习首页](https://guiguisqwd.github.io/dpt-study/study.html)
- [解剖学习工作台：维护范围与接手说明](./docs/MAINTENANCE.md)
- [内容制作规范（唯一规则来源）](./standards/README.md)
- [新增主题流程](./docs/ADDING_A_TOPIC.md)
- [肩袖阅读](https://guiguisqwd.github.io/dpt-study/reading.html) · [Claude 阅读版](https://guiguisqwd.github.io/dpt-study/reading-claude.html) · [肩袖 3D](https://guiguisqwd.github.io/dpt-study/?term=humerus)

## 新增主题

从仓库根目录创建主题骨架：

```sh
python3 scripts/new-topic.py --id knee --en 'Knee joint' --zh 膝关节
python3 scripts/validate-topics.py
python3 scripts/build-platform.py
```

主题由 `topics/<id>/topic.json` 自动发现，具体双语内容保存在同目录的 `content.json`，图示放入 `assets/`。**新主题以同一个 `content.json` 生成 HTML 和 Markdown，无须维护两份正文。** 新主题默认为 `draft`；填写六阶段内容、核对解剖与来源、验证模型绑定并完成视觉检查后，才能标为 `published`。创建目录并不等于已完成课程。

学习顺序固定为 **Anatomy → Innervation → Movement → Clinical anatomy → Review → Paper reading**，即解剖 → 神经支配 → 动作 → 临床解剖 → 复习 → 论文阅读。新增主题复用渲染器和检查规则；英文在前、中文在后，起止点配图、完整英文走行、专业答案等标准不必重新约定。详细步骤见 [ADDING_A_TOPIC.md](./docs/ADDING_A_TOPIC.md)。

## 文件结构

| 路径 | 用途 |
| --- | --- |
| `topics/<id>/topic.json` | 主题注册、状态、适配方式与模型映射 |
| `topics/<id>/content.json`、`assets/` | 新主题双语正文、资料依据与图示 |
| `scripts/` | 新主题创建、校验及共享页面构建 |
| `platform/` | 共享内容规范、校验、主题页面渲染及主题库样式 |
| `肩部3D学习/` | 共享 React / TypeScript / Three.js / Vite 应用；保留历史路径 |
| `肩部3D学习/public/topics.json`、`public/topics/` | 生成的主题目录与页面，不在这里编辑源稿 |
| `reading-source/` | 肩袖现有六章 HTML / Markdown 源稿、样式及构建脚本 |
| `2026-10-06-肩袖-阅读优化版-资源/` | 肩袖可编辑 SVG 图示 |
| `肩部3D学习/public/reading-claude.html` | 独立维护的 Claude 肩袖阅读版，构建时保留 |
| `output/pdf/` | 肩袖 PDF 与 Markdown 配图包 |
| `website-release/` | 发布脚本生成的网站包，不是源稿位置 |

肩袖通过兼容适配保留现有课程、语音与模型交互。不要为了新增髋关节重写肩袖，也不要把肩袖事实或模型 ID 直接套入新主题。[肩袖制作流程](./制作流程-肩袖双语学习.md) 保留该课程的具体维护和离线导出方法。

## 本地构建

使用 Node.js 24、pnpm 11.19.0、Python 3.13，与发布工作流保持一致：

```sh
git clone https://github.com/guiguisqwd/dpt-study.git
cd dpt-study
python3 scripts/validate-topics.py
cd 肩部3D学习
pnpm install --frozen-lockfile
pnpm build
```

依赖和锁文件未变时可省略安装。`pnpm build` 包含 TypeScript 检查；改变几何参照时另运行 `pnpm test:geometry` 和 `pnpm test:depth`。修改内容、图示或交互后，还需在浏览器中检查实际效果。

`pnpm build` 和 `pnpm dev` 都会先调用 `scripts/build-platform.py`，自动生成主题页与 `study.html` 主题库。单独运行 `build-topics.py` 只生成主题内容，不生成学习首页。

在应用目录运行：

```sh
python3 -m http.server 5178 --bind 127.0.0.1 --directory dist
```

打开 [肩袖 3D](http://127.0.0.1:5178/?term=humerus)、[肩袖阅读](http://127.0.0.1:5178/reading.html) 或 `/topics/<id>/index.html`。Mac 也可双击 `肩部3D学习/启动肩部学习.command`；开发时运行 `pnpm dev`。`127.0.0.1` 仅指当前电脑，本地服务停止后不可访问；分享使用线上地址。

## 更新与发布

先同步 GitHub，再修改源文件，校验并构建，检查效果，提交并推送。保留其他协作者的修改；不强推、不覆盖。具体协作规则见 [CLAUDE.md](./CLAUDE.md)。肩袖正文的 HTML 和 Markdown 源稿同步维护，Claude 阅读版单独维护；新主题以结构化源文件生成页面与 Markdown。

仅在修改肩袖标准阅读稿时，于仓库根目录运行 `python3 reading-source/build-reading.py`，再构建应用。新增主题直接维护自己的 `content.json`。

[GitHub Actions 工作流](./.github/workflows/pages.yml) 在推送 `main` 后检查、构建并发布，PR 只检查和构建。**本地保存、推送成功、部署成功是不同状态，分别核实后再报告。**

根目录运行以下命令生成静态发布包：

```sh
python3 -m pip install -r reading-source/requirements-publish.txt
python3 reading-source/prepare-web-release.py --site-url https://guiguisqwd.github.io/dpt-study/
```

网站入口为 `website-release/dist/study.html`；3D 入口仍是 `index.html`。发布保留主题内容、肩袖两种阅读版、模型、现有音频、配图、下载及许可，并转换线上链接。

肩袖 PDF 目前使用已核验的 38 页输入文件，发布仅更新其中的链接，不重新排版。正文或图示改动后，按肩袖制作流程重新导出并检查，不能把旧 PDF 称为已同步。新主题只有在实际生成、核验并登记后才提供 PDF 下载；自动生成的 Markdown 不代表 PDF 也已完成。

学习进度及本地标注保存在浏览器 `localStorage`，不随 GitHub 提交跨设备同步。公开站点允许阅读；Claude 修改和推送仍须用户授予 GitHub 写入权限，`CLAUDE.md` 本身不会授予账户权限。

## 交给 Claude

> 请先读本仓库的 CLAUDE.md 和 README.md。这是多主题 Anatomy study 项目，肩袖是第一个主题。新增主题请按 docs/ADDING_A_TOPIC.md 创建并填写主题数据，复用既有引擎和全部内容规范。开始前同步 GitHub 并保留已有修改；检查后提交并推送，报告实际 commit、分支和部署结果。保留现有语音和 Claude 独立阅读版。

## 来源与许可

3D 查看器基于 [Vanatome](https://github.com/vixotic/Vanatome)，版本记录在 [UPSTREAM.json](./肩部3D学习/UPSTREAM.json)。上游查看器代码采用 MIT；Z-Anatomy 等资产遵循 CC BY-SA 4.0 及署名要求。分发时保留 [代码许可](./肩部3D学习/public/licenses/LICENSE)、[资产许可](./肩部3D学习/public/licenses/ASSET-LICENSE.md) 和 [署名](./肩部3D学习/public/licenses/ATTRIBUTION.txt)。这些说明不替未授权第三方材料授予新许可。

解剖与研究内容须保留各自来源、证据范围及未解决缺项。校验器检查结构、完整性和链接，不能代替专业内容核验。肩袖穴位为模型学习参照，其状态见 [3D 应用说明](./肩部3D学习/README.md)。
