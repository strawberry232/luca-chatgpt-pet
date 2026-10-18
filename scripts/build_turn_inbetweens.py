"""Build viewer-only motion-compensated inbetweens from approved look artwork.

Requires numpy, Pillow and OpenCV. The native Pets atlas is never edited.
"""
from pathlib import Path
import json
import cv2
import numpy as np
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
STEPS = 8
WIDTH, HEIGHT = 192, 208
atlas = Image.open(ROOT / 'assets/luca-v2.png').convert('RGBA')
tiles = [np.array(atlas.crop(((i % 8) * WIDTH, (9 + i // 8) * HEIGHT,
                              (i % 8 + 1) * WIDTH, (10 + i // 8) * HEIGHT))) for i in range(16)]
grid = np.stack(np.meshgrid(np.arange(WIDTH, dtype=np.float32),
                           np.arange(HEIGHT, dtype=np.float32)), axis=-1)

def remap(array, coordinates, interpolation=cv2.INTER_LINEAR):
    return cv2.remap(array, coordinates[..., 0], coordinates[..., 1],
                     interpolation, borderMode=cv2.BORDER_CONSTANT)

def flow_image(tile):
    alpha = tile[..., 3:4].astype(np.float32) / 255
    color = tile[..., :3] * alpha + 245 * (1 - alpha)
    gray = cv2.cvtColor(color.astype(np.uint8), cv2.COLOR_RGB2GRAY)
    return cv2.resize(gray, (WIDTH * 2, HEIGHT * 2), interpolation=cv2.INTER_CUBIC)

def premultiply(tile):
    result = tile.astype(np.float32) / 255
    result[..., :3] *= result[..., 3:4]
    return result

def unpremultiply(tile):
    alpha = tile[..., 3:4]
    rgb = np.divide(tile[..., :3], alpha, out=np.zeros_like(tile[..., :3]), where=alpha > 1e-6)
    result = np.rint(np.clip(np.concatenate((rgb, alpha), axis=-1), 0, 1) * 255).astype(np.uint8)
    result[result[..., 3] == 0, :3] = 0
    return Image.fromarray(result)

def inverse_coordinates(flow, fraction):
    # Solve source + fraction * flow(source) = destination.
    coordinates = grid.copy()
    for _ in range(8):
        updated = grid - fraction * remap(flow, coordinates)
        coordinates = coordinates * 0.35 + updated * 0.65
    return coordinates

output = Image.new('RGBA', (16 * WIDTH, STEPS * HEIGHT))
samples = Image.new('RGB', (8 * WIDTH, 3 * HEIGHT), '#f5f4ef')
flow = cv2.DISOpticalFlow_create(cv2.DISOPTICAL_FLOW_PRESET_MEDIUM)
flow.setUseSpatialPropagation(True)
flow.setFinestScale(0)
flow.setPatchStride(3)
flow.setGradientDescentIterations(40)
flow.setVariationalRefinementIterations(12)
for i in range(16):
    first, second = tiles[i], tiles[(i + 1) % 16]
    forward = cv2.resize(flow.calc(flow_image(first), flow_image(second), None), (WIDTH, HEIGHT)) / 2
    backward = cv2.resize(flow.calc(flow_image(second), flow_image(first), None), (WIDTH, HEIGHT)) / 2
    a, b = premultiply(first), premultiply(second)
    for step in range(STEPS):
        position = i * STEPS + step
        if step == 0:
            frame = Image.fromarray(first)
        else:
            t = step / STEPS
            warped_a = remap(a, inverse_coordinates(forward, t), cv2.INTER_CUBIC)
            warped_b = remap(b, inverse_coordinates(backward, 1 - t), cv2.INTER_CUBIC)
            frame = unpremultiply(warped_a * (1 - t) + warped_b * t)
        output.paste(frame, ((position % 16) * WIDTH, (position // 16) * HEIGHT))
        if i in (3, 7, 15):
            row = (3, 7, 15).index(i)
            samples.paste(frame, (step * WIDTH, row * HEIGHT), frame)

destination = ROOT / 'assets/viewer/look-inbetweens.png'
destination.parent.mkdir(parents=True, exist_ok=True)
output.save(destination, optimize=True)
(ROOT / 'build').mkdir(exist_ok=True)
samples.save(ROOT / 'build/turn-inbetween-proof.png')
metadata = {'scope': 'viewer only', 'frames': 16 * STEPS, 'steps_per_original': STEPS,
            'cell': [WIDTH, HEIGHT], 'columns': 16, 'rows': STEPS,
            'method': 'bidirectional optical flow, inverse warping, premultiplied RGBA interpolation',
            'native_atlas_modified': False, 'original_endpoints_exact': True}
(ROOT / 'assets/viewer/look-inbetweens.json').write_text(json.dumps(metadata, indent=2) + '\n', encoding='utf-8', newline='\n')
print(f'Built {destination.relative_to(ROOT)}: {destination.stat().st_size} bytes')
