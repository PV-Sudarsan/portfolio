# Project 04 — MP3 compression

## Aim
MP3 compression.

## Tool / environment
Audacity or FFmpeg

## Files
source.wav, compressed_128k.mp3, convert.py, file_sizes.json

## Procedure
Import source.wav in Audacity. Choose Export Audio, MP3 and 128 kbps bitrate, then export. Alternatively install Python and FFmpeg and run python convert.py from this folder. Keep source.wav as the lossless source.

## Check your output
Compare durations and the sizes in file_sizes.json. Listen to both. MP3 is smaller but uses lossy compression; decoding it cannot recover the original samples exactly.

## Result and scope
The project demonstrates encoding existing audio into MP3; it does not implement a new codec.
