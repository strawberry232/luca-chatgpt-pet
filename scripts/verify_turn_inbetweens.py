"""Check viewer inbetweens against the approved native atlas endpoints."""
from pathlib import Path
import hashlib
import json
import numpy as np
from PIL import Image

root = Path(__file__).resolve().parents[1]
source = root / 'assets/luca-v2.png'
atlas = np.array(Image.open(source).convert('RGBA'))
sheet = np.array(Image.open(root / 'assets/viewer/look-inbetweens.png').convert('RGBA'))
assert sheet.shape == (1664, 3072, 4)
assert not np.any(sheet[sheet[..., 3] == 0, :3]), 'Hidden RGB under transparent pixels'

def tile(array, index, columns):
    row, col = divmod(index, columns)
    return array[row*208:(row+1)*208, col*192:(col+1)*192]

originals = [tile(atlas, 72 + i, 8) for i in range(16)]
frames = [tile(sheet, i, 16) for i in range(128)]
for i in range(16):
    assert np.array_equal(frames[i*8], originals[i]), f'Endpoint changed: {i}'
    for j in range(1, 8):
        assert not np.array_equal(frames[i*8+j], originals[i]), f'Missing inbetween: {i},{j}'

def composite(frame):
    alpha = frame[..., 3:4].astype(float) / 255
    return frame[..., :3] * alpha + 245 * (1-alpha)

def step_differences(sequence):
    return [float(np.abs(composite(frame)-composite(sequence[(i+1) % len(sequence)])).mean())
            for i, frame in enumerate(sequence)]

old, new = step_differences(originals), step_differences(frames)
report = {'ok': True, 'scope': 'viewer-only interpolation, not a judgment of naturalness',
          'native_atlas_sha256': hashlib.sha256(source.read_bytes()).hexdigest(),
          'original_endpoints_exact': 16, 'additional_frames': 112,
          'mean_adjacent_rgb_difference_original': float(np.mean(old)),
          'mean_adjacent_rgb_difference_inbetweens': float(np.mean(new)),
          'max_adjacent_rgb_difference_original': max(old),
          'max_adjacent_rgb_difference_inbetweens': max(new)}
(root / 'qa/turn-inbetweens.json').write_text(json.dumps(report, indent=2) + '\n', encoding='utf-8')
print(json.dumps(report))
