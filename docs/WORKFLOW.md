# Maintaining the final assets

[中文](WORKFLOW.zh-CN.md)

The general workflow is: establish a character reference → make only missing or requested animation changes → complete necessary checks → synchronize and deliver as requested. Reuse unchanged approved assets instead of rebuilding all animations or creating a demo website for every small fix.

This project currently retains a full blink at native client timing, with no pointer tracking. Keep bilingual documentation and show only final deliverables; follow any newer explicit user request.

Use `assets/luca-v2.png` as the release baseline. Eleven final row strips live in `assets/source/rows/`. Older atlases, before/after comparisons, stage reports and pointer-tracking code are excluded.

Before an animation repair, save the current atlas and lock the head, hair color, stripes, shorts, wraps, boots and anatomical sides. Modify only the intended rows. Draw a missing profile before animating it; reuse fixed textures and joint layers when that method is authorized. Compare RGBA rows, then inspect the actual loop at native size.

Rebuild, package and verify v2 geometry, transparent cells, hashes, canonical failure hair and a numeric version 2 ZIP. Update the same pet, read it back and use the downloaded atlas as the release. Platforms may re-encode PNGs, so distinguish byte equality from decoded RGBA equality.

The native client controls frame timing; a faster GIF does not speed up the installed pet. Faster previews or changes in eyelid amplitude must not be described as native timing overrides. Export final previews with `scripts/render_previews.py`; MP4 export optionally uses OpenCV via `--mp4`.

Use `$pet-animation-workflow` for detailed production guidance. Public submission and changing the active selection follow the user's explicit intent.
