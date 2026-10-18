"""Inspect Pets atlases, compare allowed row changes and build explicit-version ZIPs.

Requires Python 3.10+ and Pillow. No network or application state.
"""
import argparse
import hashlib
import io
import json
from pathlib import Path
import sys
import zipfile

from PIL import Image

COUNTS = (6, 8, 8, 4, 5, 8, 6, 6, 6)
LAYOUTS = {(1536, 1872): 1, (1536, 2288): 2}


def load_atlas(path):
    with Image.open(path) as source:
        if source.format not in ('PNG', 'WEBP'):
            raise ValueError('Expected a PNG or WebP atlas')
        if source.mode != 'RGBA':
            raise ValueError('Expected RGBA mode with a transparent background')
        if source.size not in LAYOUTS:
            raise ValueError(f'Unsupported atlas dimensions: {source.size}')
        return source.copy(), source.format


def inspect_atlas(path):
    image, image_format = load_atlas(path)
    version = LAYOUTS[image.size]
    counts = COUNTS + ((8, 8) if version == 2 else ())
    errors = []
    used = empty = 0
    for row, count in enumerate(counts):
        for col in range(8):
            tile = image.crop((col*192, row*208, (col+1)*192, (row+1)*208))
            occupied = tile.getchannel('A').getbbox() is not None
            if occupied != (col < count):
                errors.append(f'Cell row={row}, col={col}: expected {"artwork" if col < count else "empty"}')
            used += int(occupied)
            empty += int(not occupied)
    data = image.get_flattened_data() if hasattr(image, 'get_flattened_data') else image.getdata()
    residue = sum(1 for r, g, b, a in data if a == 0 and (r or g or b))
    if residue:
        errors.append(f'{residue} fully transparent pixels contain RGB residue')
    return {'ok': not errors, 'spriteVersionNumber': version,
            'format': image_format, 'size': list(image.size),
            'used_cells': used, 'empty_cells': empty,
            'transparent_rgb_residue_pixels': residue,
            'sha256': hashlib.sha256(Path(path).read_bytes()).hexdigest(), 'errors': errors}


def compare_atlases(before, after, allowed_rows):
    baseline, _ = load_atlas(before)
    candidate, _ = load_atlas(after)
    if baseline.size != candidate.size:
        raise ValueError('Before and after atlas dimensions must match')
    rows = baseline.height // 208
    if any(row < 0 or row >= rows for row in allowed_rows):
        raise ValueError(f'Allowed rows must be between 0 and {rows - 1}')
    changed = []
    for row in range(rows):
        box = (0, row*208, 1536, (row+1)*208)
        if baseline.crop(box).tobytes() != candidate.crop(box).tobytes():
            changed.append(row)
    unexpected = sorted(set(changed) - set(allowed_rows))
    return {'ok': not unexpected, 'changed_rows': changed,
            'allowed_rows': sorted(set(allowed_rows)), 'unexpected_changed_rows': unexpected}


def package_atlas(atlas, manifest, output, overwrite=False):
    report = inspect_atlas(atlas)
    if not report['ok']:
        raise ValueError('Invalid atlas: ' + '; '.join(report['errors']))
    metadata = json.loads(Path(manifest).read_text(encoding='utf-8-sig'))
    if not isinstance(metadata, dict):
        raise ValueError('Manifest must be a JSON object')
    declared = metadata.get('spriteVersionNumber')
    if type(declared) is not int or declared != report['spriteVersionNumber']:
        raise ValueError(f'Manifest needs numeric spriteVersionNumber: {report["spriteVersionNumber"]}')
    for field in ('id', 'displayName'):
        if not isinstance(metadata.get(field), str) or not metadata[field].strip():
            raise ValueError(f'Manifest needs a nonempty {field}')
    if 'description' in metadata and not isinstance(metadata['description'], str):
        raise ValueError('Manifest description must be a string')
    filename = 'spritesheet.png' if report['format'] == 'PNG' else 'spritesheet.webp'
    if metadata.get('spritesheetPath') != filename:
        raise ValueError(f'Manifest spritesheetPath must be {filename!r}')
    destination = Path(output).resolve()
    if destination in (Path(atlas).resolve(), Path(manifest).resolve()):
        raise ValueError('Output must not overwrite the input atlas or manifest')
    if destination.exists() and not overwrite:
        raise ValueError('Output exists; choose a new path or pass --overwrite')
    payload = Path(atlas).read_bytes()
    buffer = io.BytesIO()
    with zipfile.ZipFile(buffer, 'w', compression=zipfile.ZIP_DEFLATED) as archive:
        archive.writestr('pet.json', json.dumps(metadata, ensure_ascii=False, indent=2)+'\n')
        archive.writestr(filename, payload)
    with zipfile.ZipFile(io.BytesIO(buffer.getvalue())) as archive:
        if archive.testzip() is not None or set(archive.namelist()) != {'pet.json', filename}:
            raise ValueError('ZIP verification failed')
        if archive.read(filename) != payload:
            raise ValueError('Atlas bytes changed during packaging')
    destination.parent.mkdir(parents=True, exist_ok=True)
    with destination.open('wb' if overwrite else 'xb') as stream:
        stream.write(buffer.getvalue())
    return {'ok': True, 'output': str(destination), 'spriteVersionNumber': declared,
            'files': ['pet.json', filename], 'atlas_sha256': report['sha256']}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest='command', required=True)
    inspect_parser = commands.add_parser('inspect', help='Check layout, occupied cells and transparent RGB')
    inspect_parser.add_argument('atlas', type=Path)
    compare_parser = commands.add_parser('compare', help='Check that only allowed rows changed')
    compare_parser.add_argument('before', type=Path)
    compare_parser.add_argument('after', type=Path)
    compare_parser.add_argument('--allow-rows', type=int, nargs='*', default=[])
    pack_parser = commands.add_parser('package', help='Build a ZIP with a matching explicit sprite version')
    pack_parser.add_argument('atlas', type=Path)
    pack_parser.add_argument('--manifest', type=Path, required=True)
    pack_parser.add_argument('--output', type=Path, required=True)
    pack_parser.add_argument('--overwrite', action='store_true')
    args = parser.parse_args()
    try:
        if args.command == 'inspect':
            result = inspect_atlas(args.atlas)
        elif args.command == 'compare':
            result = compare_atlases(args.before, args.after, args.allow_rows)
        else:
            result = package_atlas(args.atlas, args.manifest, args.output, args.overwrite)
    except (OSError, ValueError, zipfile.BadZipFile) as error:
        result = {'ok': False, 'errors': [str(error)]}
    print(json.dumps(result, indent=2))
    return 0 if result['ok'] else 1


if __name__ == '__main__':
    sys.exit(main())
