"""Package the existing v2 atlas with an explicit manifest for Petdex submission."""
from pathlib import Path
import hashlib
import io
import json
import zipfile

from PIL import Image


def main():
    root = Path(__file__).resolve().parents[1]
    metadata = (root / 'petdex/pet.json').read_bytes()
    pet = json.loads(metadata)
    assert type(pet.get('spriteVersionNumber')) is int and pet['spriteVersionNumber'] == 2, 'Expected numeric spriteVersionNumber: 2'
    assert pet.get('spritesheetPath') == 'spritesheet.png', 'Manifest must refer to the packaged image'
    sprite = (root / 'assets/luca-v2.png').read_bytes()
    with Image.open(io.BytesIO(sprite)) as image:
        assert image.size == (1536, 2288) and image.mode == 'RGBA', 'Expected v2 RGBA atlas'
    build = root / 'build'
    build.mkdir(exist_ok=True)
    output = build / 'luca-petdex-v2.zip'
    with zipfile.ZipFile(output, 'w', compression=zipfile.ZIP_DEFLATED) as archive:
        archive.writestr('pet.json', metadata)
        archive.writestr('spritesheet.png', sprite)
    with zipfile.ZipFile(output) as archive:
        assert archive.testzip() is None
        assert sorted(archive.namelist()) == ['pet.json', 'spritesheet.png'], 'Files must be at zip root'
        assert json.loads(archive.read('pet.json'))['spriteVersionNumber'] == 2
        assert archive.read('spritesheet.png') == sprite, 'Atlas bytes must remain unchanged'
    print(json.dumps({
        'archive': output.relative_to(root).as_posix(),
        'spriteVersionNumber': 2,
        'atlas_sha256': hashlib.sha256(sprite).hexdigest(),
        'files': ['pet.json', 'spritesheet.png'],
    }, indent=2))


if __name__ == '__main__':
    main()
