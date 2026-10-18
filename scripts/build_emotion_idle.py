"""User-authorized original-pixel layering: same idle head/body in idle and failure."""
from pathlib import Path
import json, argparse
import numpy as np
from PIL import Image, ImageDraw, ImageFilter

root=Path(__file__).resolve().parents[1]
parser=argparse.ArgumentParser(description=__doc__)
parser.add_argument('--base', type=Path, default=root/'assets/source/pre-face-repair.png')
args=parser.parse_args()
run=root/'build/emotion-idle'
for folder in ['qa','final']: (run/folder).mkdir(parents=True,exist_ok=True)
refs=root/'assets/source'
base=Image.open(args.base).convert('RGBA')
idle=base.crop((0,0,192,208))
half=Image.open(refs/'expression-half-blink.png').convert('RGBA')
closed=Image.open(refs/'expression-closed-blink.png').convert('RGBA')
sad=Image.open(refs/'expression-disappointed.png').convert('RGBA')

def clean(im):
    a=np.array(im);a[a[:,:,3]==0,:3]=0
    return Image.fromarray(a)

def eye_patch(original, expression):
    # Change eyelids only. All hair, face outline, body and costume stay canonical.
    out=original.copy()
    mask=Image.new('L',(192,208));d=ImageDraw.Draw(mask)
    d.ellipse((63,72,87,100),fill=255)
    d.ellipse((105,73,129,101),fill=255)
    # Keep the central hair lock and hair pixels even inside an eye ellipse.
    a=np.array(original);m=np.array(mask)
    hair=(a[:,:,0]>a[:,:,1]*1.18)&(a[:,:,0]<150)&(a[:,:,1]<105)&(a[:,:,3]>0)
    m[hair]=0
    mask=Image.fromarray(m).filter(ImageFilter.GaussianBlur(.35))
    protected=np.array(mask);protected[hair]=0
    mask=Image.fromarray(protected)
    out.paste(expression,(0,0),mask)
    return out

def sad_mouth(original):
    # Preserve the generated mouth's anti-aliased curve instead of thresholding
    # its lighter central pixels into disconnected dashes.
    out=original.copy();mask=Image.new('L',(192,208))
    ImageDraw.Draw(mask).rounded_rectangle((88,99,105,108),radius=2,fill=255)
    out.paste(sad,(0,0),mask.filter(ImageFilter.GaussianBlur(.5)))
    return out

open_sad=sad_mouth(idle)
closed_idle=eye_patch(idle,closed)
half_sad=eye_patch(open_sad,half)
closed_sad=eye_patch(open_sad,closed)

def pose(source, head_dy, body_dy=0):
    # No head scaling or resampling. The complete idle head is translated only.
    head=source.crop((0,0,192,116))
    torso=idle.crop((0,116,192,162))
    feet=idle.crop((0,162,192,208))
    out=Image.new('RGBA',(192,208))
    out.alpha_composite(feet,(0,162))
    out.alpha_composite(torso,(0,116+body_dy))
    out.alpha_composite(head,(0,head_dy))
    return clean(out)

frames={
 'idle':[pose(idle,0),pose(closed_idle,0),pose(idle,0),pose(idle,-1),pose(idle,-1),pose(idle,0)],
 'failed':[pose(idle,0),pose(open_sad,1),pose(half_sad,3,1),pose(closed_sad,5,1),pose(closed_sad,5,1),pose(half_sad,3,1),pose(open_sad,1),pose(idle,0)],
}
final=base.copy()
for state,row in [('idle',0),('failed',5)]:
    target=run/'frames'/state;target.mkdir(parents=True,exist_ok=True)
    final.paste((0,0,0,0),(0,row*208,1536,(row+1)*208))
    for i,frame in enumerate(frames[state]):
        frame.save(target/f'{i:02d}.png');final.paste(frame,(i*192,row*208))
        if state=='idle' and i==0:assert frame.tobytes()==idle.tobytes()
for row,count in enumerate([6,8,8,4,5,8,6,6,6]):
    state=['idle','running-right','running-left','waving','jumping','failed','waiting','running','review'][row]
    dst=run/'frames'/state;dst.mkdir(parents=True,exist_ok=True)
    if state in frames:continue
    for col in range(count):base.crop((col*192,row*208,(col+1)*192,(row+1)*208)).save(dst/f'{col:02d}.png')
final=clean(final);(run/'final').mkdir(exist_ok=True);final.save(run/'final/spritesheet-extended.png')
unchanged={str(r):base.crop((0,r*208,1536,(r+1)*208)).tobytes()==final.crop((0,r*208,1536,(r+1)*208)).tobytes() for r in range(11) if r not in [0,5]}
assert all(unchanged.values())
head_box=idle.crop((0,0,192,116)).getbbox()
records=[]
for state,items in frames.items():
    for i,frame in enumerate(items):
        a=np.array(frame);original=np.array(idle)
        # Hair in the upper head is untouched by the small eyelid/mouth patches.
        dy=([0,0,0,-1,-1,0] if state=='idle' else [0,1,3,5,5,3,1,0])[i]
        src=original[4:70,30:170];dst=a[4+dy:70+dy,30:170]
        hair_same=np.array_equal(src,dst)
        assert hair_same
        records.append({'state':state,'frame':i,'head_translation_y':dy,'head_scale':1.0,'upper_hair_exact_rgba':bool(hair_same),'head_reference_bounds':head_box})
report={'ok':True,'changed_rows':[0,5],'unchanged_rows_exact_rgba':unchanged,'identity_method':'Unscaled canonical idle head and costume pixels; only small eyelid and mouth patches are generated; head/body translated at integer pixels','frames':records,'blink':{'closed_frame_indices':[1],'old_reduced_idle_closed_or_half_ms':1500,'new_reduced_idle_closed_ms':660,'client_idle_durations_ms':[1680,660,660,840,840,1920],'natural_preview_durations_ms':[3200,75,85,900,900,1000],'limitation':'Client timing is hardcoded; spritesheet changes cannot implement a true 75ms native blink'}}
(run/'qa/identity-and-timing.json').write_text(json.dumps(report,indent=2),encoding='utf8')
(run/'frames/frames-manifest.json').write_text(json.dumps({'ok':True,'rows':[{'state':s,'method':'user-authorized-canonical-layer-repair' if s in frames else 'preserved-approved-atlas','frames':[(Path('frames')/s/f'{i:02d}.png').as_posix() for i in range(len(list((run/'frames'/s).glob('*.png'))))]} for s in ['idle','running-right','running-left','waving','jumping','failed','waiting','running','review']]},indent=2),encoding='utf8')
print(json.dumps({'ok':True,'changed_rows':[0,5],'other_rows_preserved':all(unchanged.values()),'head_scale':1.0}))
