# 囚徒·卢卡 — 最终版

中文 | [English](README.md)

《第五人格》囚徒·卢卡的非官方 ChatGPT / Codex 宠物素材。此仓库只展示最终交付，图集以同步后从 Pets 回读的文件为准。

![最终状态动画](assets/previews/all-states.gif)

失落动作与待机共用相同头发颜色和头部比例，保留完整左右侧身跑步。待机采用轻微半眨眼，减少完全闭眼停住的感觉；实际帧时长没有改变。待机播放节奏由原生客户端控制；GIF 只是预览，图集无法设置客户端单帧时长。本项目不包含鼠标位置追踪、跟随网页或额外转向补帧功能。

## 下载与使用

- [最终 PNG 图集](assets/luca-v2.png)
- [Petdex 投稿 ZIP](petdex/luca-final-v2.zip)：根目录包含 `pet.json` 与 `spritesheet.png`，版本明确为数字 `2`。
- [全部动作 MP4](assets/previews/all-states.mp4)

图集为透明 RGBA PNG，1536 × 2288，8 列 × 11 行，每格 192 × 208。九种状态共 57 帧，另有 v2 格式所需的 16 个方向姿态，15 格保持透明。方向姿态是素材，不是本项目提供的鼠标追踪功能。

[待机](assets/previews/idle.gif) · [向右跑](assets/previews/running-right.gif) · [向左跑](assets/previews/running-left.gif) · [挥手](assets/previews/waving.gif) · [跳跃](assets/previews/jumping.gif) · [失落](assets/previews/failed.gif) · [等待](assets/previews/waiting.gif) · [工作](assets/previews/running.gif) · [检查成果](assets/previews/review.gif)

[最终关键画面](assets/previews/contact-sheet.png) · [十六方向](assets/previews/look-directions.png)

在支持自定义 Pets 的环境中使用最终 PNG；Petdex 使用 ZIP。动画由客户端选择，不承诺关键词触发。详见[状态说明](docs/STATES.zh-CN.md)。

## 制作与检查

```sh
python -m pip install -r requirements.txt
python scripts/rebuild.py
python scripts/package_petdex.py
python scripts/verify.py
python scripts/test_pet_skill.py
```

`assets/source/rows/` 只保存最终版的十一张可编辑行图；重建输出到 `build/luca-v2.png`，用于逐像素核对，不包含旧版本重放链。修改动作时先另存本次基准，再按[制作流程](docs/WORKFLOW.zh-CN.md)检查差异。

已附带 [pet-animation-workflow 技能](.agents/skills/pet-animation-workflow/SKILL.md)。[检查记录](qa/README.md) · [署名](CREDITS.md)。
