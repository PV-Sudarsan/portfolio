from pathlib import Path
import subprocess
p=Path(__file__).resolve().parent
filters="[0:v]setsar=1,fade=t=in:st=0:d=0.5,fade=t=out:st=5.5:d=0.5[v0];[1:v]setsar=1,fade=t=in:st=0:d=0.5,fade=t=out:st=5.5:d=0.5[v1];[v0][v1]concat=n=2:v=1:a=0[v];[2:a]afftdn=nf=-32,afade=t=in:st=0:d=1,afade=t=out:st=10:d=2[a]"
subprocess.run(['ffmpeg','-y','-i','clip_1.mp4','-i','clip_2.mp4','-i','noisy_audio.wav','-filter_complex',filters,'-map','[v]','-map','[a]','-c:v','libx264','-crf','20','-pix_fmt','yuv420p','-c:a','aac','-t','12','mix_without_captions.mp4'],cwd=p,check=True)
subprocess.run(['ffmpeg','-y','-i','mix_without_captions.mp4','-vf',"subtitles=captions.srt:force_style='Fontsize=20,Outline=2,MarginV=24'",'-c:v','libx264','-crf','20','-c:a','copy','final_captioned.mp4'],cwd=p,check=True)
