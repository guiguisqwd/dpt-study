# 肩部 3D 学习

基于 Vanatome 与 Z-Anatomy 的本地肩部空间解剖学习工具。使用真实肌肉、骨骼模型，帮助对照肩袖、骨性标志和穴位定位文字。

## 启动

直接双击本目录的 `启动肩部学习.command`，然后打开 <http://127.0.0.1:5178/>。已构建的页面和模型都在本地，无需联网下载模型。关闭终端窗口即可停止服务。

需要修改源代码时，可使用下面的开发命令。

依赖已安装时，在本目录运行：

```sh
pnpm dev
```

打开终端显示的本地地址。检查并构建、预览构建结果：

```sh
pnpm build
pnpm preview
```

新环境先运行 `pnpm install --frozen-lockfile`。模型已保存在 `public/models`，页面需通过本地服务打开。

## 当前功能与定位状态

- 加载 Vanatome 1.4.0 肌肉及骨骼模型，旋转、缩放并查看肩部结构。
- 在模型三维坐标中放置学习标记，通过透视观察标记与深层解剖的关系。
- 将标记位置及说明保存为本地 JSON 数据，保留供后续核对。
- 内置天宗 Tianzong (SI11)、秉风 Bingfeng (SI12)、肩贞 Jianzhen (SI9)、肩髃 Jianyu (LI15)、肩髎 Jianliao (TE14) 的双侧学习参照，共十个点。
- 英语名称为主，中文释义为辅；支持一键隐藏词卡、模型标签和结构索引中的中文，用于回忆与自测。
- 22 个英语解剖词汇及 5 个穴位拼音名称，提供读音提示、词典来源，以及正常／0.75 倍慢速发音。
- 点击模型结构、标签或词表会联动背词卡；Anatomy / Bone landmarks / Acupoints 切换结构、骨性标志和穴位参照。词表中的八个骨性标志现在直接聚焦对应骨面指示点；Posterior shoulder 单独标明为肩后区域参照。
- 点击阅读笔记中的穴名，聚焦对应标记；手动调整保存在覆盖层，可恢复内置参照。
- Acupoints 模式中，Depth probe · 深浅探针 沿一条几何学习轴线显示所选穴位参照穿过的模型层次；穴位详情的 Depth & surroundings · 深浅与周围结构 列出层次深度、参照点深度及 3 cm 内的周围结构。

**已建立模型中的深部解剖学习参照，尚未经过临床穴位校准。** 天宗依据近似肩胛冈中点与下角比例线推定区域，其余条目按特定骨肌关系建立区域参照。十个点均经过实际 GLB 网格内部检查，不是皮肤表面的贴图。体表定位参考点与深层解剖参考点应分别注明；肌肉中心、一次模型点击或任意向内偏移不能直接确定标准穴位。标记之间的空间关系不应解读为穿刺路径，也不表示进针方向或深度。

标记保存的是原始 GLB 模型坐标。显示时模型与标记共同应用 7 倍缩放及 `[0, -6.1, 0]` 位移。校准数据应绑定当前模型版本，不能直接套用于另一人体、另一姿势或改过比例的模型。

## 校准前需核对的姿势差异

- 肩贞：核对模型上臂位置是否符合定位描述中的内收姿势，以及腋后纹能否辨认。
- 肩髃、肩髎：标准描述涉及上臂外展，肩髎还涉及屈肘；需核对肩峰、肱骨大结节及相应凹陷在当前模型姿势下的关系。
- 天宗、秉风：先辨认肩胛冈、冈上窝、冈下窝与肩胛下角，并核对肩胛骨当前位置。
- 左右侧分别复核骨性标志与模型形态；不能只凭镜像坐标就视为完成校准。

## 来源与许可

上游：[vixotic/Vanatome](https://github.com/vixotic/Vanatome)，固定于提交 [`8185b3fa46a1dbefdd907390918c57954fd9b816`](https://github.com/vixotic/Vanatome/tree/8185b3fa46a1dbefdd907390918c57954fd9b816)。引入文件清单见 [UPSTREAM.json](./UPSTREAM.json)。本项目在上游查看器基础上增加学习标注与中文界面。

查看器代码采用 MIT 许可；解剖资产由 Z-Anatomy 等上游材料衍生，遵循 CC BY-SA 4.0 及原始署名要求。完整说明保留在 [代码许可](./public/licenses/LICENSE)、[资产许可](./public/licenses/ASSET-LICENSE.md) 与 [署名文件](./public/licenses/ATTRIBUTION.txt)。

## 几何核对

### 骨性结构辨认

点击 Humerus 自动展开近端六个骨标：肱骨头、大结节、小结节、结节间沟、解剖颈、外科颈。点击 Scapula 展开肩胛冈、下角、肩峰、冈上窝、冈下窝、肩峰前外侧和后外侧七个骨标。英文在前，中文释义跟随隐藏开关。

骨标使用原模型上的代表性表面点，共 26 个双侧位置；它们没有分割完整结构边界，简化肱骨网格中的沟和颈尤其只能提供区域提示。新增肱骨骨标列在独立骨标面板，现有 27 条词表及语音文件保持不变。

进入骨标模式会隐藏肌肉并单独显示该骨，可关闭 Isolate bone 查看周围骨骼；Whole bone / Close-up 在整骨和局部之间切换。选中骨头保留正常表面阴影。骨标切换复用同一场景，相机平滑移动；同骨切换保留手动观察角度和缩放，跨骨或显式视角按钮使用绕目标的旋转动画。

坐标与证据：`src/humerus-landmarks.json`、`src/scapula-landmarks.json`；骨面投射和检查记录在 `public/*-landmark-evidence.json`，可用 `scripts/calibrate-humerus-landmarks.mjs`、`scripts/calibrate-scapula-landmarks.mjs` 重现。

### 连续切换

肌肉、骨标、穴位、左右侧与全身视图共用同一个三维场景。只有明确的导航操作发送镜头请求；图层、显示模式、语言和标签开关保持观察位置。新请求从当前镜头位置继续，拖动可立即接管动画。前后和侧面按钮围绕当前焦点旋转，保留缩放；同一骨头内切换骨标及同模式切换穴位保留当前观察角度和距离。

骨标工具栏预留固定空间，词卡名称与读音区预留稳定高度，切换条目不会推动画布和词表按钮。来源说明的展开状态在切词时保留。

### 穴位学习参照

运行 `pnpm test:geometry` 可重现十个标记的验证：七方向射线奇偶与三角网格绕数必须一致，点须位于其关联肌肉内部、肩胛骨与肱骨外。此测试只证明模型几何归属。

- 内置位置与可见说明：`src/model-references.json`
- 骨标、局部截面和来源：`public/calibration-evidence.json`
- 本次几何验证结果：`public/geometry-validation.json`

### 深浅与周围结构

`public/acupoint-depth.json` 由 `scripts/compute-acupoint-depth.mjs` 从肌肉与骨骼 GLB 计算；改变参照点或模型后运行 `pnpm depth:compute` 重新生成，`pnpm test:depth` 检查文件是否为最新并核对层次顺序、参照点所在结构、左右对称及轴线经过参照点。该脚本不依赖 `node_modules`，并先重现 `geometry-validation.json` 中由 three.js 得到的全部射线计数与表面距离，以证明读取结果一致。

- 坐标约定经模型标志核对：+y 向上（胸骨柄高于胸骨体，C7 高于骶骨），+z 向前（胸骨体在 T4 前方），右侧 x < 0（`.r` 结构均在 x < 0，且与 +y 向上、+z 向前的右手坐标一致）。
- 探针轴线：先按记录的方向（SI11、SI12、SI9 自后方；LI15、TE14 自外侧）穿过参照点，再取该线首先遇到的模型外表面 2.5 cm 范围内的面积加权外法线，使轴线垂直于模型外表面并准确经过参照点。1.5–3 cm 取样半径的结果另记在 `axis.sensitivity`。
- 深度以厘米表示（原始模型米 × 100），从轴线上第一个建模表面起算。模型不含皮肤、皮下脂肪、筋膜、神经、血管、滑囊，也没有斜方肌、背阔肌、大圆肌和肱三头肌；从皮肤量起的实际深度会更大。
- 周围结构为参照点到其他结构最近表面的距离（3 cm 内），方向按上下、内外、前后及沿探针深浅命名。原始网格在 LI15 等处互相穿插，重叠按模型显示。
- 这是模型学习参照，不是进针路径、进针方向或进针深度。

穴名采用 WHO 文献使用的罗马字名称及国际编号；它们是汉语拼音名称，发音使用普通话。SI11 和 SI12 的 WHO 印刷页码均为 93。

## 英语背词与读音

背词卡位于右侧顶部。`Listen` 播放、`Slow` 慢速播放，`Hide Chinese` 隐藏中文释义；`Word list` 选择词汇，或使用 Previous / Next 顺序练习。

英语采用美式读音参考，IPA 与重音拆读的来源保留在 `src/vocabulary.ts` 和词卡的读音依据中。大写音节表示重音辅助提示，不能代替 IPA；词组标音可能由单词读音组合，Merriam-Webster 条目按其标音转写。Supraspinatus 使用有来源的重音提示，没有补写未核实的完整 IPA。

发音文件保存在 `public/audio`，播放时不依赖在线语音服务。目前 22 个英语词中，10 个已换成 OpenAI 的 Marin：Supraspinatus、Infraspinatus、Teres minor、Subscapularis、Deltoid、Acromial part、Clavicular part、Spinal part、Scapula、Clavicle。其余 12 个英语词暂用原来的 Samantha；5 个穴名保留普通话 Tingting。词卡按当前词的清单显示实际声音。所有音频均为合成发音，词典链接提供读音核对依据。

Marin 文件由 OpenAI.fm 页面生成并下载；本次在第 10 次下载后遇到页面每周下载上限。逐条来源、模型、实际生成参数及音频测量见 `public/audio/manifest.json`，未在页面显示的参数保留为 `null`。新文件名含内容哈希，避免继续使用旧的缓存音频。

补齐剩余 12 词的脚本只使用本机环境变量 `OPENAI_API_KEY`，默认只检查已有文件并列出缺项；加入 `--generate` 才调用官方语音 API。它保留已有 10 个下载文件及其来源，每生成一词即保存进度，全部完成后再导入并构建：

```sh
python3 scripts/generate-openai-pronunciation-audio.py --reuse .voice-staging/marin-downloads.json
python3 scripts/generate-openai-pronunciation-audio.py --reuse .voice-staging/marin-downloads.json --generate
python3 scripts/import-openai-pronunciation-audio.py .voice-staging/marin-complete.json --apply
pnpm build
```

仅在明确接受部分替换时，导入器才使用 `--allow-partial`；默认要求 22 个英语词齐全。旧的 `generate-pronunciation-audio.py` 不会覆盖已经包含 OpenAI 音频的清单。
