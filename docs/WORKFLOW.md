# Workflow and evidence boundaries

[中文](WORKFLOW.zh-CN.md) | [Home](../README.md)

## Reference video: observation versus inference

The supplied MP4 is approximately 82.37 seconds, 1920 × 1080 at 30 fps. The review used 81 sampled frames plus key full-resolution views. The original video, model and source project are not redistributed here.

| Evidence level | Finding |
|---|---|
| Directly visible | Head tilt and turn, eyelid and mouth changes, expressions and effects, glasses/bread/ears, keyboard/mouse-area hand motion, expression lists, event/settings menus. |
| Author captions and UI | Live2DViewerEX and BongoCat are named; captions describe accessory switches, independent animation buttons and audio-volume-driven mouth opening. These are the author's claims, not inspected source code. |
| Inferred architecture | Layered Cubism artwork, parameters, expression/motion assets and host input mappings are a plausible implementation. No original parameter IDs or source code were inspected. |
| Not established by the video | AI conversation, semantic understanding, desktop walking, speech synthesis, exact input-to-action timings or audio-mouth synchronization. |

The initial desktop Live2D route changed when the goal became a pet inside ChatGPT. The delivered project uses the Pets v2 sprite layout rather than a Cubism runtime.

## Actual production pipeline

1. Approve a canonical idle image: brown hair, asymmetric button eyes, gray/charcoal striped outfit, knee-length shorts, ankle wraps and black boots.
2. Produce the standard states and sixteen look poses. Preserve the approved rows when revising one motion.
3. Generate one pair of true 90° side-profile anchors using the idle reference. Calibrate hair, skin, cloth and eye material colors once against the idle image. The calibrated anchors are included in `assets/source/`.
4. With the user's explicit authorization for layered animation, split the anchors into head, collar, torso, upper/lower arms, thighs, shins and boots. Fill narrow hidden garment areas with nearby source-material colors.
5. Render eight poses per direction using hierarchical shoulder/elbow and hip/knee/ankle transforms. Keep the bandage on the anatomical arm. Use fixed texture colors and layer occlusion for depth. Register support feet and flight phases.
6. Replace only atlas rows 1 and 2. Keep idle, wave, jump, disappointed, waiting, working, review and sixteen look poses unchanged.
7. Validate atlas geometry, alpha, occupied cells, key-color edges and continuity; inspect native-size GIFs, run keyframes and idle/run comparisons. Record results in `qa/`.
8. In a supported Pets environment, validate, upload and update the intended pet, preserving its identity. Activation is a separate choice; account-specific IDs and upload URLs are excluded from this repository.

## Tools and plugin roles

| Tool | Role and limits |
|---|---|
| ChatGPT | Analyze references, describe character consistency, plan states and review previews. |
| Codex + Python/Pillow/NumPy | Cut layers, animate joints, assemble the atlas, verify unchanged rows and package bilingual documentation. |
| Image generation | Create canonical art and missing profile views. Generating every frame independently tends to drift in color and costume; the final running build reuses fixed anchors. |
| Pets plugin (`work-pets`) | Create/update, validate and preview pets in supported ChatGPT Work environments. It does not import a Live2D model or implement arbitrary trigger commands. |
| GitHub plugin / official GitHub CLI | Store versioned assets, source and documentation. It does not control animation playback. |
| Live2D Cubism / Live2DViewerEX / BongoCat | Relevant only if making a separate desktop Live2D edition later. They are not dependencies of this delivered atlas. |

Rebuild instructions are in the README. Broader original-art changes still need drawing and visual review; this rig is fitted to the supplied anchors and is not an automatic rig for arbitrary characters.
