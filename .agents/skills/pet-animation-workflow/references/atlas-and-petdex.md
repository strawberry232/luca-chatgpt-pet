# 图集与投稿：只保留必要约定

| 格式 | 尺寸 | 网格 | 有图 / 空格 |
|---|---|---|---|
| v1 | 1536 × 1872 | 8 × 9 | 57 / 15 |
| v2 | 1536 × 2288 | 8 × 11 | 73 / 15 |

每格 192 × 208。前九行依次为 `idle` 6、`running-right` 8、`running-left` 8、`waving` 4、`jumping` 5、`failed` 8、`waiting` 6、`running` 6、`review` 6 帧，从最左格开始，余格透明。`running` 指工作中，不是足部跑步。

v2 最后两行各有八个方向姿态，从上方 0° 开始顺时针每次增加 22.5°。它们不是新增动作或鼠标追踪代码。版本标识布局，不随美术修订递增；新建/更新仍以当前宿主技能及验证器要求为准。

## 本地工具（Python 3.10+、Pillow）

在本技能实际目录运行 `python scripts/pet_assets.py --help`。项目路径由本次上下文确定。

- `inspect atlas.png`：检查尺寸、格子占用、RGBA 与透明像素残留，不判断动作自然度或完整绿边。
- `compare before.png after.png --allow-rows 0 5`：只允许指定行改变；基准必须是本次修改前的文件。
- `package atlas.png --manifest pet.json --output pet.zip`：验证版本后打包，保留图集字节；已有输出默认不覆盖，确需替换时传 `--overwrite`。

## Petdex 包

ZIP 根目录只放 `pet.json` 和 `spritesheet.png`（或 `.webp`）。配置中的 `spritesheetPath` 与文件名一致；v2 要明确写数字 `"spriteVersionNumber": 2`，不能写字符串或省略。打包工具缺版本会报错，不默认为 v1。

不要依赖裸 PNG 上传页始终能自动识别版本。需要确认网站现状时查看 [Petdex 文档](https://petdex.dev/docs)；本地包通过不等于已投稿或审核通过。包中不放账号记录、签名链接和本机路径。
