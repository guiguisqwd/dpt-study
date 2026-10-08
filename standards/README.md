# 内容制作规范 · Content production standards

这里是内容**制作**的唯一规则来源：一份内容必须包含什么、怎么写、怎么画、怎么核验。推送、定时、发送、GitHub Pages 发布和存档不在这里，由推送流程自己维护。

## 四层结构

| 层 | 文件 | 放什么 | 规则编号 |
| --- | --- | --- | --- |
| 0 通用原则 | [00-general.md](./00-general.md) | 任何内容方向都成立的规则 | `G-xx` |
| 1 方向规范 | [anatomy/rules.md](./anatomy/rules.md)、[anatomy/chapters.md](./anatomy/chapters.md) | 生理解剖特有的写法、图示、穴位、论文、3D 规则和章节模板 | `AN-xx`、`CH-xx` |
| 2 主题数据 | `topics/<id>/`（肩袖为兼容路径 `reading-source/data/`） | 只属于一个主题的事实和参数：结构清单、起止点、来源、3D 映射、配色 | — |
| 3 制作步骤 | [anatomy/steps.md](./anatomy/steps.md)、[anatomy/checklist.md](./anatomy/checklist.md) | 步骤顺序、每步的输入/输出/合格标准，以及检查清单 | `ST-x`、`QC-xx` |

上层约束下层，下层只引用上层的编号，不重写规则内容。用户认可的成品见 [anatomy/exemplars.md](./anatomy/exemplars.md)；规则说不清时以样板为准。

## 怎么改

1. 判断新要求属于哪一层，只改那一个文件里的那一条。
2. 新规则取下一个空编号；删除的编号不再复用，在原位置写“已废止”和日期。
3. 想先试一个新做法：加一条标为 `【试用】` 的规则，用一个主题试，用户认可后去掉标记。
4. 在 [CHANGELOG.md](./CHANGELOG.md) 记日期、编号、用户原话和改动原因。
5. 自动检查（`platform/topiclib.py`、`daily/engine/schema.py`）对应某条规则时，在代码注释里写编号；改规则时一并检查代码。

## 新增一个内容方向

生理解剖是第一个按这个结构写的方向，它不需要兼容其他方向。新方向按 [_new-direction/README.md](./_new-direction/README.md) 建自己的第 1、3 层，第 0 层直接继承。

## 给 Claude 和其他代理

制作任何生理解剖内容前，依次读：`00-general.md` → `anatomy/chapters.md` → `anatomy/rules.md` → `anatomy/steps.md`；交付前跑 `anatomy/checklist.md`。技能和定时任务的提示只写“按哪个文件、什么顺序做”，不再各自抄一份规则。
