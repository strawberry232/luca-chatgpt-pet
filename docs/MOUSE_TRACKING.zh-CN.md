# 鼠标跟随与眨眼时长

[English](MOUSE_TRACKING.md)

四个正方向能提供基本跟随，八方向包含斜向，十六方向能更细地转向。本项目已有十六张注视姿态，符合原生 v2 布局：每档 22.5°，第 9 行为 0°–157.5°，第 10 行为 180°–337.5°，0° 朝上。这个格式不需要再补画一套方向图。

## 已实现的部分

`viewer/gaze.js` 把鼠标相对宠物的位置映射到十六个格子，`viewer/player.js` 处理浏览器鼠标事件、动作切换、离开窗口恢复待机及减少动态效果偏好。页面可离线使用，提供中英文，也可用 `scripts/build_interactive_preview.py` 导出单个 HTML。

这是真实运行在独立预览中的交互，不是注入 ChatGPT 的功能。本项目没有新增系统全局鼠标监听器。

## 转向过渡

当前预览将方向控制和画面过渡分开处理。方向采用阻尼响应，最大速度 360°/秒、加速度 2600°/秒²；反向时保留速度并先刹停，不再立即清零。后台暂停后最多按 50 毫秒推进。状态文字的十六方向索引仍有 3° 稳定区，但实际画面使用连续角度。

画面从十六张原图生成 128 帧预览素材，存于 `assets/viewer/look-inbetweens.png`，每 2.8125° 一张。相邻原图之间使用双向光流匹配、逆向变形和预乘透明度混合；原始十六个端点逐像素保留。播放器按连续角度再混合邻近补帧，因此同一个 22.5° 扇区内也会有实际画面变化。它不是直接把两张差异很大的脸透明叠加，也没有旋转整张角色图。

这是原图形变近似，不是完整 Live2D 的体积、遮挡或骨骼模型。源图差异较大的发丝和脸部仍可能略软或出现局部形变，需要人工补画才能进一步提高。首次获得目标、鼠标离开后的待机和动作模式切换仍直接选帧。原生图集、九种状态和原有十六方向均未修改，预览补帧不能直接塞入固定尺寸的 v2 图集；上述改进不会改变 ChatGPT 原生浮窗。

点击“演示转向”可自动播放。[左右对比 GIF](../assets/previews/turning-comparison.gif)中，两边使用相同角度轨迹，左侧按十六姿态切换，右侧采用补帧与混合。重建预览素材需要额外的 OpenCV，日常打开页面无需安装：

```sh
python -m pip install -r requirements-viewer.txt
python scripts/build_turn_inbetweens.py
python scripts/verify_turn_inbetweens.py
node scripts/test_gaze.cjs
node scripts/export_turn_trace.cjs build/turn-trace.json
python scripts/render_turn_preview.py build/turn-trace.json
```

实际浏览器检查使用 `node scripts/test_turn_viewer.cjs`，需要 Playwright 及 Chromium，并先导出独立 HTML。可通过 `PLAYWRIGHT_MODULE` 和 `PLAYWRIGHT_EXECUTABLE` 指定现有安装；结果记录在 `qa/turn-transition-browser-check.json`。

## 当前原生客户端的情况

只读检查本机 Windows 客户端 26.1013.4894.0，确认已有 v2 十六方向选择逻辑。检查到的浮窗会传入输入光标位置和 Computer Use 光标目标；这不能证明它会跟随每一次普通系统鼠标移动。未找到可用来开启该行为的受支持开关，本次没有修改客户端二进制或设置。

同一版本的待机时长为 `[280,110,110,140,140,320]` 乘以六，即 `[1680,660,660,840,840,1920]` 毫秒。因此，单独导出快 GIF 不能让安装后的宠物变快。修订图集将闭眼减至最短槽位的一帧（660 毫秒）；预览的自然模式使用 `[3200,75,85,900,900,1000]` 毫秒。75 毫秒只在该预览页生效，不是修改了原生客户端。

上述结论只针对检查到的版本，不保证其他版本行为相同。[Pets 官方帮助](https://learn.chatgpt.com/docs/pets)说明产品使用范围，具体支持以客户端为准。
