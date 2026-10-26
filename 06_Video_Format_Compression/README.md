# Project 06 — Video compression and format conversion

## Aim
Video compression and format conversion.

## Tool / environment
FFmpeg; outputs can be imported into OpenShot

## Files
source.mp4, intermediate.avi, compressed.mp4, converted.webm, convert.py

## Procedure
Play source.mp4 first. Run python convert.py with FFmpeg installed to create an MPEG-4/PCM AVI intermediate, then a smaller 640 × 360 H.264/AAC MP4 and a VP9/Opus WebM. Inspect the exact commands in convert.py.

## Check your output
Compare all durations and file_sizes.json. The compressed MP4 has lower resolution and higher compression, so some fine detail can be lost. Containers and codecs are different: MP4/AVI/WebM are containers.

## Result and scope
The outputs demonstrate a real AVI-to-MP4 conversion and a separate WebM export.
