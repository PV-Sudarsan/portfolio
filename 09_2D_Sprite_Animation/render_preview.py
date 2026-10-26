"""FFmpeg preview of sprite motion; this is not a Blender render."""
from pathlib import Path
import subprocess
p=Path(__file__).resolve().parent
subprocess.run(['ffmpeg','-y','-f','lavfi','-i','color=c=0xeaf2ff:s=960x540:r=24:d=4','-loop','1','-i',str(p/'sprite.png'),'-filter_complex',"[1:v]scale=140:140[s];[0:v][s]overlay=x='40+180*t':y='300-80*sin(PI*t/2)'",'-t','4','-c:v','libx264','-pix_fmt','yuv420p',str(p/'sprite_preview.mp4')],check=True)
