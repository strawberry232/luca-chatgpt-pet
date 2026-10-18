# 囚徒·卢卡 — ChatGPT 小宠物

中文 | [English](README.md)

以《第五人格》囚徒卢卡为形象的非官方 ChatGPT Work Pets 动画素材项目。包含九种状态、十六个注视方向，以及左右两套完整侧身跑步。

![完整侧身跑步](assets/previews/side-running.gif)

最终图集为 [assets/luca-v2.png](assets/luca-v2.png)：透明 RGBA PNG，1536 × 2288，8 列 × 11 行，每格 192 × 208。包括 57 帧状态动画、16 个注视姿态，另外 15 格保持透明。v2 表示 Pets 图集格式，本次美术修订为 v6。

## 动作预览

![九种状态总览](assets/previews/all-states.gif)

[待机](assets/previews/idle.gif) · [向左跑](assets/previews/running-left.gif) · [向右跑](assets/previews/running-right.gif) · [挥手](assets/previews/waving.gif) · [跳跃](assets/previews/jumping.gif) · [失落](assets/previews/failed.gif) · [等待回应](assets/previews/waiting.gif) · [认真工作](assets/previews/running.gif) · [检查成果](assets/previews/review.gif)

[待机与跑步配色对比](assets/previews/idle-running-comparison.gif) · [十六方向](assets/previews/look-directions.png) · [MP4 总览](assets/previews/all-states.mp4)

## 在 ChatGPT 中使用

在支持 Pets 插件及自定义宠物上传的环境中，提供 `assets/luca-v2.png`，让 Pets 工作流验证并创建或更新自定义宠物。需要启用时再单独选中。此仓库提供美术素材和制作流程，不会给客户端增加导入按钮、事件接口或关键词指令；实际可用性取决于客户端和账号。

动画由客户端根据工作状态选择。**有九种动画，不等于有九条手动触发指令。**`review`“检查成果”与客户端 Ready 状态的确切映射尚未确认。详见[状态含义与触发说明](docs/STATES.zh-CN.md)。

## 鼠标视线与眨眼预览

本地打开[交互预览](viewer/index.html)，或运行 `python scripts/build_interactive_preview.py` 生成内嵌图集的独立文件 `build/luca-preview.html`。此页面已实现窗口内鼠标跟随，十六方向均经浏览器验证。

ChatGPT 原生客户端自行决定视线目标和待机时长，上传图集无法开启全局鼠标跟随或改写客户端帧率。修订后的待机由连续两帧半闭眼/闭眼改为仅一帧闭眼；当前客户端仍会让这一帧停留约 660 毫秒。预览另提供自然节奏，闭眼约 75 毫秒，与原生客户端明确区分。详见[支持范围与限制](docs/MOUSE_TRACKING.zh-CN.md)。

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

结果输出到 `build/luca-v2.png`，同时生成左右各八帧跑步、可复用图层 PNG 和动作参数。程序先重建左右侧身跑步，再复用原待机的头部和衣服修复待机及失落。本轮 v6 修改保留 v5 中其余九行。验证会逐像素比较重建结果与最终图集，并检查透明背景、有效格数和素材哈希。重建无需 API 密钥或图像生成服务。

## 可复用技能

项目包含 [pet-animation-workflow](.agents/skills/pet-animation-workflow/SKILL.md)，放在 `.agents/skills/`。它固定造型一致性、侧身原画、分层动作、保留其他状态、图集检查及 Petdex 打包流程；参考资料分开记录通用方法和卢卡实例。它配合 Pets 插件使用，本身不提供上传工具或关键词触发接口。

在本仓库中可用 `$pet-animation-workflow` 调用。项目级技能随仓库保存；将同一技能文件夹安装到 Codex 个人技能目录则可跨项目使用。若技能列表未显示，可重新打开或重启 Codex。[官方技能发现说明](https://learn.chatgpt.com/docs/build-skills)。

通用检查工具只需 Pillow。运行 `python scripts/test_pet_skill.py` 可检查 v1/v2 识别、版本冲突回归、保留行及 ZIP 完整性。

## 制作要点

头、身体、手臂、短裤、绑腿和鞋都采用完整侧面。手臂绷带按角色真实左右侧处理。每帧复用固定原画纹理，通过遮挡表现远近，不交替给腿染暗；旋转插值仍会影响边缘像素。本轮表情修订只改待机与失落，其余九行相对 v5 逐像素保留。

- [制作流程、工具及证据边界](docs/WORKFLOW.zh-CN.md)
- [状态布局与触发限制](docs/STATES.zh-CN.md)
- [侧身原画提示词](docs/source-art-prompt.md)
- [质量检查](qa/README.md)
- [素材与角色署名](CREDITS.md)

这是序列帧图集项目，不包含参考视频中的 Cubism 模型、Live2DViewerEX 配置或 BongoCat 适配包。
