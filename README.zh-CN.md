# 囚徒·卢卡 — ChatGPT 小宠物

中文 | [English](README.md)

以《第五人格》囚徒卢卡为形象的非官方 ChatGPT Work Pets 动画素材项目。包含九种状态、十六个注视方向，以及左右两套完整侧身跑步。

![完整侧身跑步](assets/previews/side-running.gif)

最终图集为 [assets/luca-v2.png](assets/luca-v2.png)：透明 RGBA PNG，1536 × 2288，8 列 × 11 行，每格 192 × 208。包括 57 帧状态动画、16 个注视姿态，另外 15 格保持透明。v2 表示 Pets 图集格式，本次美术修订为 v5。

## 动作预览

![九种状态总览](assets/previews/all-states.gif)

[待机](assets/previews/idle.gif) · [向左跑](assets/previews/running-left.gif) · [向右跑](assets/previews/running-right.gif) · [挥手](assets/previews/waving.gif) · [跳跃](assets/previews/jumping.gif) · [失落](assets/previews/failed.gif) · [等待回应](assets/previews/waiting.gif) · [认真工作](assets/previews/running.gif) · [检查成果](assets/previews/review.gif)

[待机与跑步配色对比](assets/previews/idle-running-comparison.gif) · [十六方向](assets/previews/look-directions.png) · [MP4 总览](assets/previews/all-states.mp4)

## 在 ChatGPT 中使用

在支持 Pets 插件及自定义宠物上传的环境中，提供 `assets/luca-v2.png`，让 Pets 工作流验证并创建或更新自定义宠物。需要启用时再单独选中。此仓库提供美术素材和制作流程，不会给客户端增加导入按钮、事件接口或关键词指令；实际可用性取决于客户端和账号。

动画由客户端根据工作状态选择。**有九种动画，不等于有九条手动触发指令。**`review`“检查成果”与客户端 Ready 状态的确切映射尚未确认。详见[状态含义与触发说明](docs/STATES.zh-CN.md)。

## 投稿到 Petdex

使用带有明确 v2 配置的 ZIP。核查时，Petdex 的单张图片上传流程会生成缺少 `spriteVersionNumber` 的配置，默认按 v1 解析，与本图集的 1536 × 2288 尺寸冲突。

```sh
python scripts/package_petdex.py
```

在 [Petdex 投稿页](https://petdex.dev/submit)上传 `build/luca-petdex-v2.zip`。压缩包根目录仅有 `pet.json` 和 `spritesheet.png`，配置中明确填写数字 `spriteVersionNumber: 2`，图集原始字节保持不变。打包不会公开发布；请自行在 Petdex 登录并确认投稿内容。配置源文件：[petdex/pet.json](petdex/pet.json)。

## 重新制作跑步图集

已在 Python 3.12 环境验证。在仓库根目录运行：

```sh
python -m pip install -r requirements.txt
python scripts/rebuild.py
python scripts/verify.py
```

结果输出到 `build/luca-v2.png`，同时生成左右各八帧跑步、可复用图层 PNG 和动作参数。程序使用已经配色校准的两张侧身原画，按关节层级旋转，只替换基准图集中的左右跑步两行。验证会逐像素比较重建结果与最终图集，并检查透明背景、有效格数和素材哈希。重建无需 API 密钥或图像生成服务。

## 制作要点

头、身体、手臂、短裤、绑腿和鞋都采用完整侧面。手臂绷带按角色真实左右侧处理。每帧复用固定原画纹理，通过遮挡表现远近，不交替给腿染暗；旋转插值仍会影响边缘像素。其他九行原有动画与注视姿态逐像素保留。

- [制作流程、工具及证据边界](docs/WORKFLOW.zh-CN.md)
- [状态布局与触发限制](docs/STATES.zh-CN.md)
- [侧身原画提示词](docs/source-art-prompt.md)
- [质量检查](qa/README.md)
- [素材与角色署名](CREDITS.md)

这是序列帧图集项目，不包含参考视频中的 Cubism 模型、Live2DViewerEX 配置或 BongoCat 适配包。
