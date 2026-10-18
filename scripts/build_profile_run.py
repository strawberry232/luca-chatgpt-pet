"""Complete profile running: calibrated side-view art, then user-authorized cutout rig."""
from pathlib import Path
import math,json
import numpy as np
from PIL import Image,ImageDraw,ImageChops,ImageOps

root=Path(__file__).resolve().parents[1]
p=root/'build'
p.mkdir(exist_ok=True)
(p/'decoded').mkdir(exist_ok=True)
W,H,S=192,208,6
def T(x,y):return np.array([[1.,0,x],[0,1.,y],[0,0,1.]])
def R(angle,point):
    a=math.radians(angle);c,s=math.cos(a),math.sin(a);x,y=point
    return np.array([[c,s,x-c*x-s*y],[-s,c,y+s*x-c*y],[0,0,1.]])
def polygon(points):
    im=Image.new('L',(W*S,H*S));ImageDraw.Draw(im).polygon([(round(x*S),round(y*S)) for x,y in points],fill=255);return im
def cut(src,points):
    result=src.copy();result.putalpha(ImageChops.multiply(src.getchannel('A'),polygon(points)));return result
def transform(im,matrix):
    a=matrix.copy();a[:2,2]*=S;inv=np.linalg.inv(a)
    return im.transform((W*S,H*S),Image.Transform.AFFINE,tuple(inv[:2].reshape(-1)),Image.Resampling.BICUBIC)
def vertical_mask(layer,y0,y1):
    out=layer.copy();mask=Image.new('L',layer.size);ImageDraw.Draw(mask).rectangle((0,y0*S,W*S,y1*S),fill=255)
    out.putalpha(ImageChops.multiply(layer.getchannel('A'),mask));return out

config={
 'running-right':{'direction':1,'hip':(96,154),'shoulder':(91,118),'elbow':(88,135),'sample_x':103,
 'core':[(90,106),(99,106),(106,118),(110,147),(109,158),(82,158),(80,146),(84,120)],
 'arm':[(90,114),(97,116),(98,125),(95,136),(97,145),(100,149),(102,157),(98,162),(91,163),(86,159),(84,151),(79,149),(77,142),(80,132),(82,122)],
 'fill_x':(82,103)},
 'running-left':{'direction':-1,'hip':(99,154),'shoulder':(102,118),'elbow':(103,135),'sample_x':90,
 'core':[(94,106),(103,106),(110,118),(115,146),(113,158),(83,158),(81,146),(87,120)],
 'arm':[(99,114),(108,117),(112,125),(113,136),(113,145),(110,150),(110,158),(106,162),(100,163),(95,159),(93,153),(93,146),(92,142),(94,131),(95,122)],
 'fill_x':(94,114)}
}
rigs={}
for state,cfg in config.items():
    native=Image.open(root/'assets/source'/f"profile-{'right' if state=='running-right' else 'left'}.png").convert('RGBA')
    src=native.resize((W*S,H*S),Image.Resampling.NEAREST)
    core=src.copy();coremask=polygon(cfg['core']);core.putalpha(coremask)
    cp,sp=core.load(),src.load();x0,x1=cfg['fill_x'];sx=cfg['sample_x']
    for yy in range(118*S,158*S):
        for xx in range(x0*S,x1*S):cp[xx,yy]=sp[sx*S,yy]
    core.putalpha(coremask)
    # Cap unseen collar corners with the actual original silhouette.
    for yy in range(0,118*S):
        for xx in range(W*S):
            rgb=cp[xx,yy];cp[xx,yy]=(*rgb[:3],min(rgb[3],sp[xx,yy][3]))
    head=cut(src,[(0,0),(192,0),(192,107),(0,107)])
    collar=vertical_mask(cut(src,[(82,102),(111,102),(114,114),(106,120),(89,117),(82,112)]),101,118)
    whole=cut(src,cfg['arm']);ex,ey=cfg['elbow']
    upper=whole.copy();lower=whole.copy()
    um=Image.new('L',src.size);lm=Image.new('L',src.size)
    du,dl=ImageDraw.Draw(um),ImageDraw.Draw(lm)
    du.rectangle((0,0,W*S,(ey-2)*S),fill=255)
    dl.rectangle((0,(ey+2)*S,W*S,H*S),fill=255)
    bounds=((ex-7)*S,(ey-6)*S,(ex+7)*S,(ey+7)*S)
    du.ellipse(bounds,fill=255);dl.ellipse(bounds,fill=255)
    upper.putalpha(ImageChops.multiply(whole.getchannel('A'),um))
    lower.putalpha(ImageChops.multiply(whole.getchannel('A'),lm))
    rigs[state]={'source':src,'core':core,'head':head,'collar':collar,'upper':upper,'lower':lower}

# Recover one clean complete shorts-leg, calf wrap and boot in profile.
# The original arm hid the upper shorts; continue the same source stripe rows there.
src=rigs['running-right']['source']
legbase=src.copy();lp,sp=legbase.load(),src.load()
for yy in range(151*S,167*S):
    for xx in range(90*S,106*S):lp[xx,yy]=sp[106*S,yy]
thigh=cut(legbase,[(91,151),(109,151),(110,170),(107,176),(91,176),(89,168)])
shin=cut(src,[(92,173),(106,173),(108,186),(90,187)])
boot=cut(src,[(92,182),(106,182),(107,187),(115,190),(119,194),(119,201),(110,203),(88,202),(87,196),(89,187)])
right_leg={'thigh':thigh,'shin':shin,'boot':boot,'hip':(99,154),'knee':(99,174),'ankle':(99,185)}

def leg_layers(state):
    cfg=config[state]
    if cfg['direction']==1:
        shift=T(cfg['hip'][0]-99,0)
        return {key:transform(right_leg[key],shift) for key in ['thigh','shin','boot']},(cfg['hip'][0],174),(cfg['hip'][0],185)
    shift=T(cfg['hip'][0]-(192-99),0)
    return {key:transform(ImageOps.mirror(right_leg[key]),shift) for key in ['thigh','shin','boot']},(cfg['hip'][0],174),(cfg['hip'][0],185)

hip_angles=[30,10,-12,-30,-35,-10,35,50]
knee_flex=[10,50,22,45,75,95,85,50]
foot_angles=[0,-5,-20,-35,-60,-65,-30,0]
framesroot=p/'frames';framesroot.mkdir(exist_ok=True)
layerdir=p/'layers';layerdir.mkdir(exist_ok=True)
report=[]
for state,cfg in config.items():
    direction=cfg['direction'];rig=rigs[state];hx,hy=cfg['hip']
    body=R(-direction*4.5,cfg['hip'])
    leg,knee,ankle=leg_layers(state)
    other='running-left' if state=='running-right' else 'running-right'
    oc=config[other];other_rig=rigs[other]
    mirrored_shoulder=(192-oc['shoulder'][0],oc['shoulder'][1])
    shift=T(cfg['shoulder'][0]-mirrored_shoulder[0]-direction*1,cfg['shoulder'][1]-mirrored_shoulder[1])
    farupper=transform(ImageOps.mirror(other_rig['upper']),shift)
    farlower=transform(ImageOps.mirror(other_rig['lower']),shift)
    far_elbow=(192-oc['elbow'][0]+shift[0,2],oc['elbow'][1]+shift[1,2])
    far_shoulder=(cfg['shoulder'][0]-direction,cfg['shoulder'][1])
    dst=framesroot/state;dst.mkdir(exist_ok=True)
    for key,layer in list(leg.items())+[(k,rig[k]) for k in ['core','head','collar','upper','lower']]:
        layer.resize((W,H),Image.Resampling.LANCZOS).save(layerdir/f'{state}-{key}.png')
    rendered=[];contact_bottom=[]
    for i in range(8):
        output=Image.new('RGBA',src.size);boot_imgs={}
        phase=i*math.tau/8
        def drawleg(index,far):
            hm=R(direction*hip_angles[index],cfg['hip'])
            km=R(-direction*knee_flex[index],knee)
            fm=R(direction*(foot_angles[index]-(hip_angles[index]-knee_flex[index])),ankle)
            depth=T(-direction*1.2,-.3) if far else np.eye(3)
            for key,local in [('thigh',hm),('shin',hm@km),('boot',hm@km@fm)]:
                image=transform(leg[key],body@depth@local)
                output.alpha_composite(image)
                if key=='boot':boot_imgs['far' if far else 'near']=image
        drawleg((i+4)%8,True)
        # Far arm belongs to the opposite anatomical side, so only one arm bandage exists.
        shoulder_angle=direction*25*math.cos(phase)
        far_rot=R(shoulder_angle,far_shoulder)
        flex=direction*(65+7*math.sin(phase))
        output.alpha_composite(transform(farupper,body@far_rot))
        output.alpha_composite(transform(farlower,body@far_rot@R(flex,far_elbow)))
        drawleg(i,False)
        output.alpha_composite(transform(rig['core'],body))
        near_rot=R(-shoulder_angle,cfg['shoulder'])
        output.alpha_composite(transform(rig['upper'],body@near_rot))
        output.alpha_composite(transform(rig['lower'],body@near_rot@R(direction*(65-7*math.sin(phase)),cfg['elbow'])))
        output.alpha_composite(transform(rig['collar'],body))
        output.alpha_composite(transform(rig['head'],body@R(direction*1.7,(96,105))))
        frame=output.resize((W,H),Image.Resampling.LANCZOS)
        support='near' if i<4 else 'far'
        bb=boot_imgs[support].getchannel('A').point(lambda a:255 if a>64 else 0).getbbox()
        contact_bottom.append(bb[3]/S)
        rendered.append(frame)
    shifts=[202-contact_bottom[i] for i in range(8)]
    for i in [3,7]:shifts[i]=(shifts[(i-1)%8]+shifts[(i+1)%8])/2-3
    for i,frame in enumerate(rendered):
        dy=round(shifts[i]);out=Image.new('RGBA',(W,H));out.paste(frame,(0,dy))
        arr=np.array(out);arr[arr[:,:,3]==0,:3]=0
        out=Image.fromarray(arr);out.save(dst/f'{i:02d}.png')
        report.append({'state':state,'frame':i,'near_hip_deg':hip_angles[i],'near_knee_flex_deg':knee_flex[i],'near_foot_deg':foot_angles[i],'far_phase':(i+4)%8,'body_registration_dy':dy,'bbox':out.getbbox()})
    strip=Image.new('RGBA',(1536,208))
    for i in range(8):strip.paste(Image.open(dst/f'{i:02d}.png'),(i*192,0))
    strip.save(p/'decoded'/f'{state}.png')
(p/'rig.json').write_text(json.dumps({'method':'User-authorized manual layered animation of newly drawn true 90-degree side anchors, calibrated to original idle palette','true_profile':True,'source_art':'assets/source/profile-left.png and profile-right.png','pose_order':'Contact, compression, push-off, flight, opposite contact, opposite compression, opposite push-off, opposite flight','depth':'Fixed near/far layer order and occlusion, no alternating leg recolor','anatomy':'Mirrored opposite-arm asset supplies correct near/far bandage identity; legs use same symmetric costume pixels','frames':report},indent=2),encoding='utf8')
(framesroot/'frames-manifest.json').write_text(json.dumps({'ok':True,'rows':[{'state':state,'method':'manual-profile-rig','frames':[(Path('build/frames')/state/f'{i:02d}.png').as_posix() for i in range(8)]} for state in config]},indent=2),encoding='utf8')
print('Full profile running cycles rendered')
