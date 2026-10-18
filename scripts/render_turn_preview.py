"""Compare sixteen-pose stepping with motion-compensated viewer transitions."""
import argparse,json
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont

parser=argparse.ArgumentParser(description=__doc__)
parser.add_argument('trace',type=Path)
parser.add_argument('--output',type=Path,default=Path('build/turning-comparison.gif'))
args=parser.parse_args()
root=Path(__file__).resolve().parents[1]
atlas=Image.open(root/'assets/luca-v2.png').convert('RGBA')
inbetweens=Image.open(root/'assets/viewer/look-inbetweens.png').convert('RGBA')
trace=json.loads(args.trace.read_text(encoding='utf-8-sig'))
font=ImageFont.load_default(size=16)
small=ImageFont.load_default(size=12)
tiles=[]
for index in range(16):
    row=9+index//8;col=index%8
    tiles.append(atlas.crop((col*192,row*208,(col+1)*192,(row+1)*208)))
dense=[inbetweens.crop(((i%16)*192,(i//16)*208,(i%16+1)*192,(i//16+1)*208)) for i in range(128)]
frames=[];durations=[]
for number in range(0,len(trace['frames']),2):
    item=trace['frames'][number]
    canvas=Image.new('RGB',(576,366),'#f4f3ed');draw=ImageDraw.Draw(canvas)
    position=item['angle']/360*128
    cell=int(position)%128;mix=position-int(position)
    # Blend premultiplied alpha just like the Canvas lighter pass.
    smooth=Image.blend(dense[cell].convert('RGBa'),dense[(cell+1)%128].convert('RGBa'),mix).convert('RGBA')
    for side,tile,label in [(0,tiles[item['displayed_index']],'Before: 16 pose steps'),(1,smooth,'Now: inbetween motion')]:
        tile=tile.resize((288,312),Image.Resampling.LANCZOS)
        canvas.paste(tile,(side*288,35),tile)
        draw.text((side*288+12,10),label,font=font,fill='#3d4938')
    draw.text((190,347),f"Target: {item['target_index']*22.5:g} degrees",font=small,fill='#697160')
    frames.append(canvas);durations.append(sum(frame['duration_ms'] for frame in trace['frames'][number:number+2]))
args.output.parent.mkdir(parents=True,exist_ok=True)
frames[0].save(args.output,save_all=True,append_images=frames[1:],duration=durations,loop=0,optimize=False,disposal=2)
print(f'Rendered {args.output}')
