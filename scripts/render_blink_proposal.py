"""Render a timing proposal, explicitly separate from native playback."""
from pathlib import Path
import json
from PIL import Image, ImageDraw, ImageFont

ROOT=Path(__file__).resolve().parents[1]
atlas=Image.open(ROOT/'assets/luca-v2.png').convert('RGBA')
opened=atlas.crop((0,0,192,208))
closed=atlas.crop((192,0,384,208))
half=Image.open(ROOT/'assets/source/blink-transition.png').convert('RGBA')
font_path=Path('C:/Windows/Fonts/msyh.ttc')
font=ImageFont.truetype(str(font_path),17) if font_path.exists() else ImageFont.load_default(size=16)
def panel(sprite):
    image=Image.new('RGB',(480,506),'#f1f4f8')
    enlarged=sprite.resize((384,416),Image.Resampling.NEAREST)
    image.paste(enlarged,(48,40),enlarged)
    draw=ImageDraw.Draw(image)
    draw.text((12,10),'Full blink: timing proposal',font=font,fill='#334155')
    draw.text((12,472),'Preview only; native timing is unchanged',font=font,fill='#475569')
    return image
frames=[panel(sprite) for sprite in [opened,half,closed,half,opened,half,closed,half]]
frames[0].save(ROOT/'assets/previews/blink-natural-proposal.gif',save_all=True,append_images=frames[1:],duration=[4000,40,60,80,5200,40,60,80],loop=0,disposal=2)
print(json.dumps({'proposal_blink_ms':180,'native_timing_override':False}))
