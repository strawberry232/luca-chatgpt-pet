"""Reproduce profile running, then the canonical idle/failure repair."""
from pathlib import Path
import runpy,subprocess,sys,shutil
from PIL import Image

root=Path(__file__).resolve().parents[1]
runpy.run_path(str(root/'scripts/build_profile_run.py'),run_name='__main__')
atlas=Image.open(root/'assets/source/base-spritesheet.png').convert('RGBA')
for row,state in [(1,'running-right'),(2,'running-left')]:
    for column in range(8):
        frame=Image.open(root/f'build/frames/{state}/{column:02d}.png').convert('RGBA')
        atlas.paste(frame,(column*192,row*208))
baseline=root/'build/luca-profile-v5.png'
atlas.save(baseline)
subprocess.run([sys.executable,str(root/'scripts/build_emotion_idle.py'),'--base',str(baseline)],check=True)
shutil.copy2(root/'build/emotion-idle/final/spritesheet-extended.png',root/'build/luca-v2.png')
print('Built build/luca-v2.png')
