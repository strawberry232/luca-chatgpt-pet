# Mouse tracking and blink timing

[中文](MOUSE_TRACKING.zh-CN.md)

Four cardinal drawings give basic tracking, eight add diagonals, and sixteen provide smaller direction steps. This project's sixteen existing look poses already match the native v2 layout: 22.5° per step, row 9 for 0°–157.5° and row 10 for 180°–337.5°, with 0° up. No extra pose artwork is needed for this format.

## What was implemented

`viewer/gaze.js` maps pointer position around the pet to one of the sixteen cells. `viewer/player.js` handles browser pointer events, action switching, idle recovery on window leave and reduced-motion preferences. The viewer works offline, has Chinese and English labels, and is also available as a single embedded HTML file through `scripts/build_interactive_preview.py`.

These are real interactions in the standalone viewer. They are not injected into ChatGPT. There is no new global desktop mouse listener in this project.

## Observed native behavior

Read-only inspection of the installed Windows client 26.1013.4894.0 found an existing sixteen-direction selector for v2 assets. The inspected overlay passes typing-caret targets and a computer-use cursor target to it; this does not establish general tracking of every ordinary OS mouse move. No supported switch for that behavior was identified. The app binary and its settings were not patched.

The same build uses idle durations `[280,110,110,140,140,320]` multiplied by six, or `[1680,660,660,840,840,1920]` ms. This is why exporting a faster GIF alone does not speed up the installed pet. The artwork now uses only one closed-eye frame at the shortest slot (660 ms). The viewer's optional natural mode uses `[3200,75,85,900,900,1000]` ms. The 75 ms setting applies to that viewer, not the native app.

These findings describe the inspected build and are not a promise for other client versions. [Official Pets help](https://learn.chatgpt.com/docs/pets) describes product availability; actual client support remains authoritative.
