# Shoulder study · 肩袖学习

英文在前、中文在后的肩部学习项目：六章解剖与论文阅读、可编辑 SVG 配图、可旋转的 3D 肌肉与骨骼、骨性标志及穴位学习参照，并提供 PDF 和 Markdown 离线版本。

**GitHub 是共同维护的项目来源。每次授权修改均需在检查后提交并推送。** 共同仓库：[guiguisqwd/shoulder-study](https://github.com/guiguisqwd/shoulder-study)。Claude 与其他协作者先读 [CLAUDE.md](./CLAUDE.md)；工作前用 `git remote get-url origin` 核对远端。提交成功与网站部署成功应分别验证。

```sh
git clone https://github.com/guiguisqwd/shoulder-study.git
cd shoulder-study
```

## 文件结构

| 路径 | 用途 |
| --- | --- |
| `reading-source/` | 六章 HTML / Markdown 源稿、样式、构建脚本与来源数据 |
| `2026-10-06-肩袖-阅读优化版-资源/` | 可编辑解剖 SVG 图示 |
| `2026-10-06-肩袖-阅读优化版.html` / `.md` | 标准阅读构建输出 |
| `肩部3D学习/` | React、TypeScript、Three.js、Vite 应用 |
| `肩部3D学习/public/reading-claude.html` | 独立维护的 Claude 阅读版，保留其学习模式与功能 |
| `output/pdf/` | 完整双语 PDF 与 Markdown 配图包 |
| `website-release/` | 发布脚本生成的网站包，不作为源稿编辑位置 |
| [制作流程-肩袖双语学习.md](./制作流程-肩袖双语学习.md) | 内容规范、图示、模型链接、核验与离线导出流程 |

## 本地构建与阅读

使用 Node.js 24、pnpm 11.19.0、Python 3.13，与发布工作流保持一致。从仓库根目录执行：

```sh
python3 reading-source/build-reading.py
cd 肩部3D学习
pnpm install --frozen-lockfile
pnpm build
```

Mac 可双击 `肩部3D学习/启动肩部学习.command`。也可在应用目录运行：

```sh
python3 -m http.server 5178 --bind 127.0.0.1 --directory dist
```

浏览器打开：

- 3D：[http://127.0.0.1:5178/?term=humerus](http://127.0.0.1:5178/?term=humerus)
- 标准阅读：[http://127.0.0.1:5178/reading.html](http://127.0.0.1:5178/reading.html)
- Claude 阅读版：[http://127.0.0.1:5178/reading-claude.html](http://127.0.0.1:5178/reading-claude.html)

`127.0.0.1` 指打开浏览器的这台电脑，本地服务停止后地址就无法访问。分享学习材料应使用完成部署的线上地址。开发时在应用目录运行 `pnpm dev`，打开终端输出的地址。

## 更新与发布

先同步 GitHub，再改源文件，生成输出，检查效果，提交并推送。具体 Git 步骤和多人协作约束见 [CLAUDE.md](./CLAUDE.md)。阅读正文的 HTML 和 Markdown 源稿需要同步修改；不能只改最终输出。Claude 阅读版独立保存，不由标准阅读构建覆盖。

`pnpm build` 检查 TypeScript 并生成应用。修改几何参照时运行 `pnpm test:geometry`；涉及图文版式和交互时，另检查浏览器中的实际显示。

GitHub Pages 的发布来源已设置为 **GitHub Actions**。[发布工作流](./.github/workflows/pages.yml) 在推送到 `main` 后依次检查阅读内容、几何参照及 TypeScript，构建并发布网站；PR 只检查和构建。**本地保存不会更新网站；提交并推送到 `main`，且发布任务成功后，网站才会更新。**

预定线上入口（首次部署目前待验证）：

- [学习首页](https://guiguisqwd.github.io/shoulder-study/study.html)
- [标准阅读](https://guiguisqwd.github.io/shoulder-study/reading.html)
- [Claude 阅读版](https://guiguisqwd.github.io/shoulder-study/reading-claude.html)
- [3D 肱骨入口](https://guiguisqwd.github.io/shoulder-study/?term=humerus)

根目录运行以下命令可生成与线上地址匹配的静态发布包：

```sh
python3 -m pip install -r reading-source/requirements-publish.txt
python3 reading-source/prepare-web-release.py --site-url https://guiguisqwd.github.io/shoulder-study/
```

输出入口是 `website-release/dist/study.html`，3D 入口是 `index.html`。发布依赖固定为 `pypdf==6.10.0`，用于更新 PDF 的线上链接；工作流使用 GitHub 返回的实际站点地址。发布包包含两种阅读版、模型、音频、配图、下载文件和许可。

目前 PDF 发布输入是已核验的 38 页版本。发布不会重新排版 PDF；重新导出目前依赖 Mac 字体及本地渲染环境，正文或图示变化后需按制作流程更新并检查 PDF，再提交。

浏览器学习进度及本地标注保存在 `localStorage`，不会随 GitHub 提交跨设备同步。公开网站允许阅读；修改源码和推送仍需用户授权的 GitHub 写入权限。

## 交给 Claude

让 Claude 使用同一仓库，并先读根目录 `CLAUDE.md`。可直接复制：

> 请先读取这个仓库的 CLAUDE.md 和 README.md，再处理我的修改。GitHub 是项目共同来源；开始前检查并同步远端，保留已有修改；完成必要检查后提交并推送，告诉我实际 commit、分支和部署结果。请遵守英文在前、中文在后，保留现有语音及 Claude 独立阅读版。

## 来源与许可

3D 查看器基于 [Vanatome](https://github.com/vixotic/Vanatome)，引入版本与文件记录在 [UPSTREAM.json](./肩部3D学习/UPSTREAM.json)。上游查看器代码采用 MIT；Z-Anatomy 等解剖资产遵循 CC BY-SA 4.0 及署名要求。分发时保留 [代码许可](./肩部3D学习/public/licenses/LICENSE)、[资产许可](./肩部3D学习/public/licenses/ASSET-LICENSE.md) 和 [署名文件](./肩部3D学习/public/licenses/ATTRIBUTION.txt)。这些许可说明不自动替未明确授权的第三方材料授予新许可。

学习内容的来源和证据范围保留在阅读正文及 `reading-source/data/`。穴位标记为模型解剖学习参照，尚不代表经过临床校准的标准定位；详细状态见 [3D 应用说明](./肩部3D学习/README.md)。
