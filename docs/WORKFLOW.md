# Maintaining the final assets

[中文](WORKFLOW.zh-CN.md)

Use `assets/luca-v2.png` as the release baseline. Eleven final row strips live in `assets/source/rows/`. Older atlases, before/after comparisons, stage reports and pointer-tracking code are excluded.

Before an animation repair, save the current atlas and lock the head, hair color, stripes, shorts, wraps, boots and anatomical sides. Modify only the intended rows. Draw a missing profile before animating it; reuse fixed textures and joint layers when that method is authorized. Compare RGBA rows, then inspect the actual loop at native size.

Rebuild, package and verify v2 geometry, transparent cells, hashes, canonical failure hair and a numeric version 2 ZIP. Update the same pet, read it back and use the downloaded atlas as the release. Platforms may re-encode PNGs, so distinguish byte equality from decoded RGBA equality.

The native client controls frame timing; a faster GIF does not speed up the installed pet. Half-blink artwork must not be described as a timing override. Export final previews with `scripts/render_previews.py`; MP4 export optionally uses OpenCV via `--mp4`.

Use `$pet-animation-workflow` for detailed production guidance. Public submission and changing the active selection follow the user's explicit intent.
