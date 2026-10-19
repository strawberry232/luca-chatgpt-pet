"""Render final-only GIF/still previews; --mp4 additionally requires OpenCV."""
from pathlib import Path
import argparse
import json
from PIL import Image,ImageDraw,ImageFont

ROOT=Path(__file__).resolve().parents[1]
STATES=[('idle','待机 / Idle',6),('running-right','向右跑 / Run right',8),
        ('running-left','向左跑 / Run left',8),('waving','挥手 / Wave',4),
        ('jumping','跳跃 / Jump',5),('failed','失落 / Disappointed',8),
        ('waiting','等待 / Waiting',6),('running','工作 / Working',6),('review','检查 / Review',6)]
TIMES=[[1680,660,660,840,840,1920],[90]*8,[90]*8,[180]*4,
       [120,100,140,100,220],[140]*7+[240],[220]*6,[150]*6,[180]*6]


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--mp4',action='store_true')
    args=parser.parse_args()
    atlas=Image.open(ROOT/'assets/luca-v2.png').convert('RGBA')
    target=ROOT/'assets/previews';target.mkdir(parents=True,exist_ok=True)
    font_path=Path('C:/Windows/Fonts/msyh.ttc')
    font=ImageFont.truetype(str(font_path),18) if font_path.exists() else ImageFont.load_default(size=16)
    def cell(row,col):return atlas.crop((col*192,row*208,(col+1)*192,(row+1)*208))
    def panel(sprite,label):
        image=Image.new('RGB',(384,464),'#f1f4f8')
        scaled=sprite.resize((384,416),Image.Resampling.NEAREST)
        image.paste(scaled,(0,40),scaled)
        ImageDraw.Draw(image).text((12,10),label,font=font,fill='#334155')
        return image
    def gif(path,frames,durations):
        frames[0].save(path,save_all=True,append_images=frames[1:],duration=durations,loop=0,disposal=2)
    all_frames=[];all_times=[]
    contact=Image.new('RGB',(384*3,464*3),'#f1f4f8')
    for row,(state,label,count) in enumerate(STATES):
        if not font_path.exists():label=label.split(' / ')[-1]
        frames=[panel(cell(row,i),label) for i in range(count)]
        gif(target/f'{state}.gif',frames,TIMES[row])
        all_frames.extend(frames);all_times.extend(TIMES[row])
        key=3 if row==5 else 2 if row==4 else 0
        contact.paste(frames[key],((row%3)*384,(row//3)*464))
    gif(target/'all-states.gif',all_frames,all_times)
    contact.save(target/'contact-sheet.png')
    sequence=[panel(cell(0,0),'Idle')]+[panel(cell(4,i),'Jump') for i in range(5)]+[panel(cell(0,0),'Idle')]
    gif(target/'idle-jump-idle.gif',sequence,[700]+TIMES[4]+[700])
    comparison=Image.new('RGB',(768,464),'#f1f4f8')
    comparison.paste(panel(cell(0,0),'Idle'),(0,0));comparison.paste(panel(cell(5,3),'Disappointed'),(384,0))
    comparison.save(target/'idle-failed-still.png')
    look_frames=[panel(cell(9+i//8,i%8),f'{i*22.5:g} degrees') for i in range(16)]
    gif(target/'look-loop.gif',look_frames,[180]*16)
    directions=Image.new('RGB',(192*8,238*3),'#f1f4f8')
    directions.paste(cell(0,0),(0,25),cell(0,0))
    ImageDraw.Draw(directions).text((4,3),'Idle reference',font=font,fill='#334155')
    for i in range(16):
        left=(i%8)*192;top=(1+i//8)*238
        directions.paste(cell(9+i//8,i%8),(left,top+25),cell(9+i//8,i%8))
        ImageDraw.Draw(directions).text((left+4,top+3),f'{i*22.5:g} degrees',font=font,fill='#334155')
    directions.save(target/'look-directions.png')
    if args.mp4:
        import cv2
        import numpy as np
        video=cv2.VideoWriter(str(target/'all-states.mp4'),cv2.VideoWriter_fourcc(*'mp4v'),50,(384,464))
        if not video.isOpened():raise RuntimeError('MP4 writer failed to open')
        try:
            for frame,duration in zip(all_frames,all_times):
                bgr=cv2.cvtColor(np.array(frame),cv2.COLOR_RGB2BGR)
                for _ in range(max(1,round(duration/20))):video.write(bgr)
        finally:video.release()
    print(json.dumps({'states':9,'look_poses':16,'source':'assets/luca-v2.png','native_idle_timing_reference_ms':TIMES[0],'mp4':args.mp4}))


if __name__=='__main__':main()
