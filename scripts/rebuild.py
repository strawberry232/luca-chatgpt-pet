"""Rebuild the two profile run rows while preserving all other atlas pixels."""
from pathlib import Path
import runpy
from PIL import Image

root = Path(__file__).resolve().parents[1]
runpy.run_path(str(root / 'scripts/build_profile_run.py'), run_name='__main__')
atlas = Image.open(root / 'assets/source/base-spritesheet.png').convert('RGBA')
for row, state in [(1, 'running-right'), (2, 'running-left')]:
    for column in range(8):
        frame = Image.open(root / f'build/frames/{state}/{column:02d}.png').convert('RGBA')
        atlas.paste(frame, (column * 192, row * 208))
atlas.save(root / 'build/luca-v2.png')
print('Built build/luca-v2.png')
