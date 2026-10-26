from pathlib import Path
import subprocess
p=Path(__file__).resolve().parent
subprocess.run(['ffmpeg','-y','-ss','0.3','-i',str(p/'raw_recording.webm'),'-vf','scale=960:540,fade=t=in:st=0:d=0.4','-c:v','libx264','-crf','22','-pix_fmt','yuv420p','-an',str(p/'edited_lesson.mp4')],check=True)
