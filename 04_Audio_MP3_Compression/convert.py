from pathlib import Path
import subprocess
p=Path(__file__).resolve().parent
subprocess.run(['ffmpeg','-y','-i',str(p/'source.wav'),'-codec:a','libmp3lame','-b:a','128k',str(p/'compressed_128k.mp3')],check=True)
