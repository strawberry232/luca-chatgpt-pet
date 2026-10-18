"""Render a turn trace with the shipped atlas; no new or altered artwork."""
import argparse,json
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont

parser=argparse.ArgumentParser(description=__doc__)
parser.add_argument('trace',type=Path)
parser.add_argument('--output',type=Path,default=Path('build/turning-comparison.gif'))
args=parser.parse_args()
root=Path(__file__).resolve().parents[1]
atlas=Image.open(root/'assets/luca-v2.png').convert('RGBA')
trace=json.loads(args.trace.read_text(encoding='utf-8-sig'))
font=ImageFont.load_default(size=20)
small=ImageFont.load_default(size=14)
tiles=[]
for index in range(16):
    row=9+index//8;col=index%8
    tiles.append(atlas.crop((col*192,row*208,(col+1)*192,(row+1)*208)).resize((384,416),Image.Resampling.NEAREST))
frames=[];durations=[]
for item in trace['frames']:
    canvas=Image.new('RGB',(768,484),'#f4f3ed');draw=ImageDraw.Draw(canvas)
    for side,key,label in [(0,'target_index','Instant switch'),(1,'displayed_index','Gentle transition')]:
        tile=tiles[item[key]];canvas.paste(tile,(side*384,58),tile)
        draw.text((side*384+20,15),label,font=font,fill='#3d4938')
    draw.text((270,460),f"Pointer target: {item['target_index']*22.5:g} degrees",font=small,fill='#697160')
    frames.append(canvas);durations.append(item['duration_ms'])
args.output.parent.mkdir(parents=True,exist_ok=True)
frames[0].save(args.output,save_all=True,append_images=frames[1:],duration=durations,loop=0,optimize=False,disposal=2)
print(f'Rendered {args.output}')
