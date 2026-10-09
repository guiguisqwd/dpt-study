# 制作规范变更记录

| 日期 | 编号 | 改动 | 依据 |
| --- | --- | --- | --- |
| 2026-10-08 | 全部 | 建立四层结构。规则从 CLAUDE.md §4、platform/QUALITY_RULES.md、docs/ADDING_A_TOPIC.md、制作流程-肩袖双语学习.md、dpt-reading-pack 技能和每日生成任务的提示里提取、去重并编号；只收内容制作规则，推送、发布、存档规则不收 | gui：“需要从推送中提取出目前制作内容的要求和标准……需要清晰结构，即方便更改 也方便 调整。也为后续其它方向的内容制作提供清晰的路径” |
| 2026-10-08 | CH-01、CH-02 | 主题包六章（Clinical anatomy + Paper reading）定为主模板，每日包六章作为短版变体 | gui 确认 |
| 2026-10-08 | AN-07 | 读音（IPA + 重音 + 词典链接，穴位声调拼音）定为必做 | gui：“一定” |
| 2026-10-08 | 结构 | 内容分成两大块：`standards/anatomy/` 改名 `standards/library/`（知识库章节规则）；新建 `standards/daily/README.md`（取材规程 DL-01 至 DL-06，DL-01 至 DL-04 为目标、尚未落实）；CH-02 从 chapters.md 移到 daily/README.md | gui：“每日学习的目的 是从我们生成好的大内容下 按照规程生成 今日该学习的东西。现在的肩袖 应当属于大的解剖知识下的 一个章节。” |
| 2026-10-08 | ST-7 | 新增“本章 3D”步骤：生成、修改 3D 网站是每一章都有的部分，放 `library/<id>/3d/`；文件落点改为 `library/<id>/` 下 text / figures / pdf / 3d | gui：“生成 修改这个网站的过程 需要加入在每一个大的部分当中例如hip也应当有这么一部分” |
