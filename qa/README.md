# Quality evidence / 质量检查

Current artwork revision: v6, with only idle row 0 and failure row 5 changed since v5. The other nine rows, including side-profile running and all sixteen look poses, remain exact RGBA matches. The neutral idle frame is also unchanged.

当前为 v6 修订，仅修改待机第 0 行和失落第 5 行；其余九行，包括侧身跑步和十六方向，逐像素保留。待机第 0 帧仍为原图。

- `atlas-validation.json`: final v2 dimensions, transparency and chroma checks passed. / 最终图集的尺寸、透明度和绿边检查通过。
- `identity-and-timing.json`: unscaled canonical head/hair and costume reused; integer translation only; actual client timing versus preview timing documented. / 复用待机头发、头部和衣服，仅作整数像素位移；记录真实客户端与预览节奏的区别。
- `standard-frame-review.json`: final frame review passed, with expected warnings about authorized manual layering and preserved atlas extraction. / 帧检查通过，包含手工分层及保留原帧的方式提示。
- `chroma-despill.json`: final edges were already clean, so the final preservation pass used strength 0 and changed no pixels. New source art is transparent. / 最终边缘已干净，保色步骤强度为 0，无像素改色；新原画为透明底。
- `pet-quality.json`: final gate passed; the existing non-fatal 157.5° → 180° look-continuity warning is unchanged. / 最终质量检查通过，原有 157.5° → 180° 非致命连续性提示仍保留。
- `viewer-browser-check.json`: all sixteen directions, mode switching, language labels, blink timing and mobile layout passed in an actual headless browser. This verifies the standalone viewer, not ChatGPT global mouse tracking. / 实际浏览器验证十六方向、动作切换、中英文、眨眼节奏和窄屏布局；此结果只针对独立预览页。

`archive-v5/` holds earlier profile-running checks. Reports with machine-local paths have been sanitized. `scripts/verify.py` checks the current asset hashes, occupied cells, preserved rows and optional rebuilt-image parity; it does not judge visual naturalness.

`archive-v5/` 保留上一轮侧身跑步检查；本机路径已清理。验证脚本检查当前素材哈希、有效格、保留行和可选重建一致性，不替代人工观感判断。
