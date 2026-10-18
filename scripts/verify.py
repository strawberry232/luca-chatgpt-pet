"""Verify atlas geometry, occupied cells, transparency and optional rebuild parity."""
from pathlib import Path
import hashlib, json
import numpy as np
from PIL import Image

root = Path(__file__).resolve().parents[1]
path = root / 'assets/luca-v2.png'
atlas = Image.open(path)
assert atlas.mode == 'RGBA' and atlas.size == (1536, 2288), 'Invalid v2 atlas geometry'
pixels = np.asarray(atlas)
assert not np.any(pixels[pixels[:, :, 3] == 0, :3]), 'Hidden RGB under transparent pixels'
counts = [6, 8, 8, 4, 5, 8, 6, 6, 6, 8, 8]
for row, count in enumerate(counts):
    for col in range(8):
        tile = pixels[row*208:(row+1)*208, col*192:(col+1)*192]
        assert bool(np.any(tile[:, :, 3])) == (col < count), f'Invalid cell {row},{col}'
base = np.asarray(Image.open(root/'assets/source/base-spritesheet.png').convert('RGBA'))
for row in range(11):
    if row not in (0, 1, 2, 5):
        assert np.array_equal(base[row*208:(row+1)*208], pixels[row*208:(row+1)*208]), f'Unexpected change in row {row}'
previous = np.asarray(Image.open(root/'assets/source/pre-face-repair.png').convert('RGBA'))
for row in range(11):
    if row not in (0, 5):
        assert np.array_equal(previous[row*208:(row+1)*208], pixels[row*208:(row+1)*208]), f'Unexpected v6 change in row {row}'
assert np.array_equal(previous[:208,:192], pixels[:208,:192]), 'Canonical idle frame changed'
manifest = json.loads((root/'manifest.json').read_text(encoding='utf8'))
for item in manifest['files']:
    file = root/item['path']
    assert hashlib.sha256(file.read_bytes()).hexdigest() == item['sha256'], f'Changed asset: {item["path"]}'
rebuilt = root / 'build/luca-v2.png'
if rebuilt.exists():
    assert np.array_equal(np.asarray(Image.open(rebuilt).convert('RGBA')), pixels), 'Rebuild differs from shipped atlas'
    print('Rebuild: exact RGBA pixel match')
print('PASS: 73 occupied cells, 15 empty cells, clean transparent pixels; nine rows preserved since v5; canonical idle unchanged; asset hashes match')
