"""Reassemble the final v2 atlas from its eleven editable final row strips."""
from pathlib import Path
from PIL import Image
root=Path(__file__).resolve().parents[1]
rows=sorted((root/'assets/source/rows').glob('*.png'))
assert len(rows)==11, 'Expected eleven final row strips'
atlas=Image.new('RGBA',(1536,2288))
for index,path in enumerate(rows):
    assert path.name.startswith(f'{index:02d}-')
    with Image.open(path) as strip:
        assert strip.mode=='RGBA' and strip.size==(1536,208)
        atlas.paste(strip,(0,index*208))
output=root/'build/luca-v2.png';output.parent.mkdir(exist_ok=True)
atlas.save(output)
print('Built build/luca-v2.png from final rows')
