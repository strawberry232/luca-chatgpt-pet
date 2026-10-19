# Luca — Final Pet

[中文](README.zh-CN.md) | English

An unofficial Identity V Luca Balsa pet asset for ChatGPT / Codex. This repository presents only the final deliverable. The canonical atlas is the file downloaded after synchronizing the pet through Pets.

![Final animation states](assets/previews/all-states.gif)

Disappointment shares the idle hair color and head proportions. Full side-profile running is retained in both directions. Idle restores fully closed eyes; native frame durations remain unchanged. The [natural full-blink proposal](docs/BLINK.md) demonstrates a 180 ms target rhythm without claiming a native timing override. Native playback timing is controlled by the client; GIFs are previews and cannot override native frame durations. No pointer-tracking page, mouse-position listener or additional turning interpolation is included.

## Download and use

- [Final PNG atlas](assets/luca-v2.png)
- [Petdex ZIP](petdex/luca-final-v2.zip): root-level `pet.json` and `spritesheet.png`, with numeric `spriteVersionNumber: 2`.
- [All-state MP4](assets/previews/all-states.mp4)

Transparent RGBA PNG, 1536 × 2288, eight columns × eleven rows, 192 × 208 per cell. Nine states use 57 frames; the v2 format adds sixteen direction poses, leaving fifteen empty cells. Direction poses are artwork, not a pointer-tracking feature implemented by this project.

[Idle](assets/previews/idle.gif) · [Run right](assets/previews/running-right.gif) · [Run left](assets/previews/running-left.gif) · [Wave](assets/previews/waving.gif) · [Jump](assets/previews/jumping.gif) · [Disappointed](assets/previews/failed.gif) · [Waiting](assets/previews/waiting.gif) · [Working](assets/previews/running.gif) · [Review](assets/previews/review.gif)

[Final contact sheet](assets/previews/contact-sheet.png) · [Sixteen directions](assets/previews/look-directions.png)

Use the PNG in an environment supporting custom Pets and the ZIP for Petdex submission. The client chooses animations; no keyword triggers are promised. See [state meanings](docs/STATES.md).

## Build and verify

```sh
python -m pip install -r requirements.txt
python scripts/rebuild.py
python scripts/package_petdex.py
python scripts/verify.py
python scripts/test_pet_skill.py
```

`assets/source/rows/` contains only the eleven editable final row strips. Rebuilding writes `build/luca-v2.png` for pixel comparison; it does not replay older revisions. Save a new baseline before future edits and follow the [workflow](docs/WORKFLOW.md).

Includes the [pet-animation-workflow skill](.agents/skills/pet-animation-workflow/SKILL.md). [Quality records](qa/README.md) · [Credits](CREDITS.md).
