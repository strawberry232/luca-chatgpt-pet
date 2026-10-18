# Luca — ChatGPT Pet

[中文](README.zh-CN.md) | English

An unofficial Identity V Prisoner / Luca animated pet asset project for ChatGPT Work Pets. Includes nine animation states and sixteen look directions, with complete side-profile running in both directions.

![Side-profile running](assets/previews/side-running.gif)

The final atlas is [assets/luca-v2.png](assets/luca-v2.png): transparent RGBA PNG, 1536 × 2288, eight columns × eleven rows, 192 × 208 per cell. There are 57 animation frames and 16 look poses; 15 unused cells stay transparent. “v2” describes the Pets atlas format; this artwork revision is v6.

## Preview

![All nine states](assets/previews/all-states.gif)

[Idle](assets/previews/idle.gif) · [Left run](assets/previews/running-left.gif) · [Right run](assets/previews/running-right.gif) · [Wave](assets/previews/waving.gif) · [Jump](assets/previews/jumping.gif) · [Disappointed](assets/previews/failed.gif) · [Waiting](assets/previews/waiting.gif) · [Working](assets/previews/running.gif) · [Review](assets/previews/review.gif)

[Idle / run color comparison](assets/previews/idle-running-comparison.gif) · [Sixteen directions](assets/previews/look-directions.png) · [MP4 overview](assets/previews/all-states.mp4)

## Use in ChatGPT

In an environment with the Pets plugin and custom pet upload support, provide `assets/luca-v2.png` and ask the Pets workflow to validate it and create or update a custom pet. Select the pet separately if you want to activate it. This repository is the artwork and build pipeline; it does not add a new import button, client event hooks or keyword commands. Availability depends on the client and account.

The client chooses animations from work activity. **Nine included states do not imply nine user commands.** The exact mapping of the `review` row to the client's Ready state is unconfirmed. See [state meanings and triggers](docs/STATES.md).

## Mouse tracking and blink preview

Open [the interactive viewer](viewer/index.html) locally, or run `python scripts/build_interactive_preview.py` to make `build/luca-preview.html`, a standalone file with the atlas embedded. Pointer tracking inside this page is implemented and tested in all sixteen directions. Choose “Show turning demo” for automatic direction changes.

Direction changes follow the shortest arc through neighboring poses, with acceleration, braking and boundary hysteresis. All sixteen drawings retain their original pixels, colors and costume. These are sprite transitions; first target acquisition, returning to idle and action-mode changes still select a frame directly. See the [turning comparison](assets/previews/turning-comparison.gif): instant switching on the left, gradual turns on the right.

The native ChatGPT client controls its own tracking targets and idle timing. This project cannot enable global mouse tracking or change native frame timing by uploading an atlas. The repaired idle uses one closed frame instead of two half/closed frames; the current client still holds that frame for about 660 ms. The viewer also offers a natural 75 ms blink mode, explicitly separate from native behavior. See [support and limits](docs/MOUSE_TRACKING.md).

## Submit to Petdex

Use a ZIP with an explicit v2 manifest. Petdex's bare-image uploader was observed to generate a manifest without `spriteVersionNumber`, which defaults to v1 and conflicts with this 1536 × 2288 atlas.

```sh
python scripts/package_petdex.py
```

Upload `build/luca-petdex-v2.zip` at [Petdex Submit](https://petdex.dev/submit). The ZIP contains exactly `pet.json` and `spritesheet.png` at its root; the manifest sets numeric `spriteVersionNumber: 2`. The original atlas bytes remain unchanged. Packaging does not publish anything; sign in and review the submission on Petdex yourself. Source manifest: [petdex/pet.json](petdex/pet.json).

## Rebuild

Python 3.12 was used. Run from the repository root:

```sh
python -m pip install -r requirements.txt
python scripts/rebuild.py
python scripts/verify.py
```

The build writes `build/luca-v2.png`, two eight-frame cycles, reusable layer PNGs and motion parameters. It rebuilds the two side-profile running rows, then reuses the canonical idle head and costume to repair idle and disappointment. The latest v6 change preserves all nine other rows from v5. Verification compares the rebuilt image against the shipped image pixel for pixel, checks transparency, occupied cells and asset hashes. It requires no API key or image generation service.

## Reusable skill

The project includes [pet-animation-workflow](.agents/skills/pet-animation-workflow/SKILL.md) in `.agents/skills/`. It captures character consistency, profile artwork, layered animation, preservation of unrelated states, atlas checks and Petdex packaging. Its references separate general guidance from the Luca-specific rig. It complements the Pets plugin; it does not provide upload tools or keyword triggers by itself.

Invoke `$pet-animation-workflow` while working in this repository. A project skill travels with the repository; install the same folder in your Codex user skill directory to use it across projects. If it does not appear in the skill selector, reopen or restart Codex. [Official skill discovery guidance](https://learn.chatgpt.com/docs/build-skills).

The standalone helper requires Pillow. Run `python scripts/test_pet_skill.py` to check v1/v2 detection, the v2 manifest regression, preserved rows and ZIP integrity.

## Production notes

The torso, head, arms, shorts, wraps and boots all face sideways. Arm bandage placement follows anatomical sides. Each run cycle reuses fixed source textures; limb depth uses occlusion instead of alternating dark tints. Edges still change through interpolation. The v6 expression repair changes only idle and disappointment; all nine other rows remain unchanged from v5.

- [Workflow, tools and evidence boundaries](docs/WORKFLOW.md)
- [State layout and trigger limitations](docs/STATES.md)
- [Source art prompt](docs/source-art-prompt.md)
- [Quality checks](qa/README.md)
- [Credits](CREDITS.md)

This is a sprite atlas project. It does not contain the reference video's Cubism model, Live2DViewerEX configuration or BongoCat package.
