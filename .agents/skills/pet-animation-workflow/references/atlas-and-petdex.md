# 图集、检查与 Petdex 投稿包

## 本流程使用的格式

| 格式 | 尺寸 | 网格 |
|---|---|---|
| v1 | 1536 × 1872 | 8 列 × 9 行 |
| v2 | 1536 × 2288 | 8 列 × 11 行 |

每格 192 × 208。前九行是 `idle` 6、`running-right` 8、`running-left` 8、`waving` 4、`jumping` 5、`failed` 8、`waiting` 6、`running` 6、`review` 6 帧。从第 0 列开始，余格透明。v2 最后两行各用满八格，是从朝上 0° 开始、每次顺时针增加 22.5° 的十六个注视姿态，不是两个新增状态。

v2 共 73 个有图格、15 个空格；v1 共 57 个有图格、15 个空格。`running` 指工作中，不是左右奔跑。版本是格式标识，不随美术修订递增。

若当前宿主文档或验证工具与这些约定不同，先确认宿主/版本，不为通过本脚本丢弃姿态。ChatGPT 上传仍需 Pets 自身验证工具；本地工具不替代全部宿主校验或审核。

## 自带工具

`SKILL_DIR` 是实际技能目录，`PROJECT` 是本次素材项目。需 Python 3.10+ 和 Pillow。

```text
python SKILL_DIR/scripts/pet_assets.py inspect PROJECT/assets/luca-v2.png
python SKILL_DIR/scripts/pet_assets.py compare PROJECT/assets/source/base-spritesheet.png PROJECT/assets/luca-v2.png --allow-rows 1 2
python SKILL_DIR/scripts/pet_assets.py package PROJECT/assets/luca-v2.png --manifest PROJECT/petdex/pet.json --output PROJECT/build/petdex.zip
```

`inspect` 检查几何、原始 RGBA 模式、格子占用及完全透明像素中的 RGB 残留，不检测全部绿边或解剖，不判断动画自然度。

`compare` 逐行比较 RGBA，只允许显式列出的行变化。使用本次修改前的基准，不一直沿用多轮之前的旧图集。

`package` 根据实际尺寸检测版本，要求配置提供匹配的数字版本；缺失/错误报错，不降级为 v1。ZIP 根目录只有 `pet.json` 和 `spritesheet.png`（或 `.webp`），保留图集原始字节。输出不能覆盖输入，已有输出需明确 `--overwrite` 才可替换。

## 投稿

2026-10-18 核查的 Petdex 裸 PNG 流程生成的配置缺少版本号，解析时默认 v1，导致 v2 冲突。优先提交显式版本的 ZIP；不要保证网站将来仍有这个问题。

```json
{
  "id": "character-pet",
  "displayName": "角色名称 / Character Name",
  "description": "用户认可的描述。",
  "spriteVersionNumber": 2,
  "spritesheetPath": "spritesheet.png"
}
```

版本必须是数字 `2`，不是字符串 `"2"`。图片名与包内文件一致。包内不放整仓库、账号记录或临时链接。打包不代表发布；按用户发布意图在 [Petdex](https://petdex.dev/submit) 登录确认，审核以网站结果为准，不推定用户的素材授权选项。

复核当前行为时查看维护方源码：[版本解析](https://github.com/crafter-station/petdex/blob/main/src/lib/sprite-version.ts)、[图集识别](https://github.com/crafter-station/petdex/blob/main/src/lib/sprite-atlas.ts)、[上传界面](https://github.com/crafter-station/petdex/blob/main/src/components/submit/pet-submit-form.tsx)。登录失败或限流时保留本地包，不循环重试发布。
