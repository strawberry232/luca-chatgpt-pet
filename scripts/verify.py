"""Verify only the final release assets, identity invariant and optional rebuild."""
from pathlib import Path
import hashlib,json,zipfile
import numpy as np
from PIL import Image
root=Path(__file__).resolve().parents[1]
path=root/'assets/luca-v2.png';image=Image.open(path)
assert image.mode=='RGBA' and image.size==(1536,2288)
pixels=np.array(image)
assert not np.any(pixels[pixels[:,:,3]==0,:3])
counts=[6,8,8,4,5,8,6,6,6,8,8]
strips=sorted((root/'assets/source/rows').glob('*.png'))
assert len(strips)==11
for row,count in enumerate(counts):
    assert np.array_equal(np.array(Image.open(strips[row])),pixels[row*208:(row+1)*208])
    for col in range(8):
        assert bool(np.any(pixels[row*208:(row+1)*208,col*192:(col+1)*192,3]))==(col<count)
canonical=pixels[4:70,30:170]
hair=[]
for col,shift in enumerate([0,1,3,5,5,3,1,0]):
    same=np.array_equal(pixels[5*208+4+shift:5*208+70+shift,col*192+30:col*192+170],canonical)
    assert same, f'Failure frame {col}: canonical hair differs'
    hair.append(bool(same))
manifest=json.loads((root/'manifest.json').read_text(encoding='utf8'))
for entry in manifest['files']:
    assert hashlib.sha256((root/entry['path']).read_bytes()).hexdigest()==entry['sha256'],entry['path']
rebuilt=root/'build/luca-v2.png'
if rebuilt.exists():assert np.array_equal(np.array(Image.open(rebuilt).convert('RGBA')),pixels)
package=root/'petdex/luca-final-v2.zip'
with zipfile.ZipFile(package) as archive:
    assert sorted(archive.namelist())==['pet.json','spritesheet.png']
    assert json.loads(archive.read('pet.json'))['spriteVersionNumber']==2
    assert archive.read('spritesheet.png')==path.read_bytes()
report={'ok':True,'atlas_sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'failure_hair_exact_rgba_frames':hair,'head_scale':1.0,'source_rows_exact':11,'used_cells':73,'empty_cells':15,'rebuilt_rgba_equal':rebuilt.exists(),'package_atlas_bytes_equal':True}
(root/'qa/final-identity.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf8')
print(json.dumps(report,indent=2))
