"""Export the offline pointer-tracking viewer as one self-contained HTML file."""
from pathlib import Path
import base64,json

root=Path(__file__).resolve().parents[1]
html=(root/'viewer/index.html').read_text(encoding='utf8')
uri='data:image/png;base64,'+base64.b64encode((root/'assets/luca-v2.png').read_bytes()).decode('ascii')
turn_uri='data:image/png;base64,'+base64.b64encode((root/'assets/viewer/look-inbetweens.png').read_bytes()).decode('ascii')
html=html.replace('<script src="gaze.js"></script>','<script>'+(root/'viewer/gaze.js').read_text(encoding='utf8')+'</script>')
html=html.replace('<script src="player.js"></script>','<script>window.LUCA_ATLAS_URL='+json.dumps(uri)+';window.LUCA_TURN_URL='+json.dumps(turn_uri)+';</script><script>'+(root/'viewer/player.js').read_text(encoding='utf8')+'</script>')
out=root/'build/luca-preview.html';out.parent.mkdir(exist_ok=True)
out.write_text(html,encoding='utf8')
print('Built build/luca-preview.html')
