"""Regression checks for atlas preservation and the Petdex v2 mismatch fix."""
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
import zipfile

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
HELPER = ROOT / '.agents/skills/pet-animation-workflow/scripts/pet_assets.py'
SPEC = importlib.util.spec_from_file_location('pet_assets', HELPER)
TOOLS = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(TOOLS)


class PetSkillChecks(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.folder = Path(self.temp.name)
        self.atlas = ROOT / 'assets/luca-v2.png'
        self.manifest = ROOT / 'petdex/pet.json'

    def test_v2_cell_occupancy(self):
        report = TOOLS.inspect_atlas(self.atlas)
        self.assertTrue(report['ok'])
        self.assertEqual((report['spriteVersionNumber'], report['used_cells'], report['empty_cells']), (2, 73, 15))

    def test_v1_is_detected_from_dimensions(self):
        path = self.folder/'v1.png'
        with Image.open(self.atlas) as image:
            image.crop((0, 0, 1536, 1872)).save(path)
        report = TOOLS.inspect_atlas(path)
        self.assertTrue(report['ok'])
        self.assertEqual((report['spriteVersionNumber'], report['used_cells']), (1, 57))

    def test_zip_root_manifest_and_unchanged_atlas(self):
        output = self.folder/'pet.zip'
        TOOLS.package_atlas(self.atlas, self.manifest, output)
        with zipfile.ZipFile(output) as archive:
            self.assertEqual(sorted(archive.namelist()), ['pet.json', 'spritesheet.png'])
            self.assertEqual(archive.read('spritesheet.png'), self.atlas.read_bytes())
            self.assertEqual(json.loads(archive.read('pet.json'))['spriteVersionNumber'], 2)

    def test_missing_wrong_and_string_versions_are_rejected(self):
        original = json.loads(self.manifest.read_text(encoding='utf8'))
        path = self.folder/'pet.json'
        for version in (None, 1, '2', True):
            with self.subTest(version=version):
                metadata = original.copy()
                if version is None:
                    metadata.pop('spriteVersionNumber')
                else:
                    metadata['spriteVersionNumber'] = version
                path.write_text(json.dumps(metadata), encoding='utf8')
                with self.assertRaisesRegex(ValueError, 'numeric spriteVersionNumber: 2'):
                    TOOLS.package_atlas(self.atlas, path, self.folder/'bad.zip')
                self.assertFalse((self.folder/'bad.zip').exists())

    def test_unapproved_row_change_is_detected(self):
        before = ROOT/'assets/source/base-spritesheet.png'
        report = TOOLS.compare_atlases(before, self.atlas, [1, 2])
        self.assertTrue(report['ok'])
        self.assertEqual(report['changed_rows'], [1, 2])
        path = self.folder/'changed-idle.png'
        with Image.open(self.atlas) as image:
            image.putpixel((96, 100), (255, 0, 0, 255))
            image.save(path)
        report = TOOLS.compare_atlases(before, path, [1, 2])
        self.assertFalse(report['ok'])
        self.assertEqual(report['unexpected_changed_rows'], [0])

    def test_unused_cell_and_transparent_rgb_are_reported(self):
        path = self.folder/'bad-alpha.png'
        with Image.open(self.atlas) as image:
            image.putpixel((7*192, 0), (255, 0, 0, 255))
            image.putpixel((0, 0), (255, 0, 0, 0))
            image.save(path)
        report = TOOLS.inspect_atlas(path)
        self.assertFalse(report['ok'])
        self.assertEqual(report['transparent_rgb_residue_pixels'], 1)
        self.assertTrue(any('row=0, col=7' in error for error in report['errors']))

    def test_inputs_and_existing_outputs_are_preserved(self):
        original = self.manifest.read_bytes()
        with self.assertRaisesRegex(ValueError, 'must not overwrite'):
            TOOLS.package_atlas(self.atlas, self.manifest, self.manifest)
        self.assertEqual(self.manifest.read_bytes(), original)
        output = self.folder/'existing.zip'
        output.write_bytes(b'existing')
        with self.assertRaisesRegex(ValueError, 'Output exists'):
            TOOLS.package_atlas(self.atlas, self.manifest, output)
        self.assertEqual(output.read_bytes(), b'existing')


if __name__ == '__main__':
    unittest.main(verbosity=2)
