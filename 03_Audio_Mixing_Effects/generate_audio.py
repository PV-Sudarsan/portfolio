"""Rebuild original educational audio; requires Python 3 and numpy."""
from pathlib import Path
import wave
import numpy as np
p=Path(__file__).resolve().parent
sr=44100
t=np.arange(sr*12)/sr
melody=np.zeros_like(t)
for k,f in enumerate([261.63,329.63,392,523.25,392,329.63]*4):
 mask=(t>=k*.5)&(t<k*.5+.45)
 u=t[mask]-k*.5
 melody[mask]=.24*np.sin(2*np.pi*f*u)*np.minimum(u/.02,1)*np.exp(-4*u)
bass=.12*np.sin(2*np.pi*130.815*t)+.07*np.sin(2*np.pi*80*t)*np.exp(-25*(t%.5))
fade=np.minimum(t/1.5,1)*np.minimum((12-t)/2,1)
for name,data in [('melody.wav',melody),('bass_and_beat.wav',bass),('mixed_fades.wav',(melody+bass)*fade)]:
 with wave.open(str(p/name),'wb') as w:
  w.setnchannels(1);w.setsampwidth(2);w.setframerate(sr)
  w.writeframes((np.clip(data,-1,1)*32767).astype('<i2').tobytes())
print('Created two tracks and a 12-second mix.')
