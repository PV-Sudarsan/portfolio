from pathlib import Path
import subprocess
p=Path(__file__).resolve().parent
for args in [ ['-i','source.mp4','-c:v','mpeg4','-q:v','3','-c:a','pcm_s16le','intermediate.avi'], ['-i','intermediate.avi','-vf','scale=640:360','-c:v','libx264','-crf','30','-c:a','aac','-b:a','64k','compressed.mp4'], ['-i','source.mp4','-vf','scale=640:360','-c:v','libvpx-vp9','-crf','36','-b:v','0','-c:a','libopus','converted.webm'] ]:
 subprocess.run(['ffmpeg','-y',*args],cwd=p,check=True)
