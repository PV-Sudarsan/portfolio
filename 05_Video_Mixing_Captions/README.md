# Project 05 — Video mix, noise reduction, effects and captions

## Aim
Video mix, noise reduction, effects and captions.

## Tool / environment
OpenShot for manual editing; FFmpeg for reproducible export

## Files
clip_1.mp4, clip_2.mp4, noisy_audio.wav, cleaned_audio.wav, captions.srt, timeline.json, build_video.py, final_captioned.mp4

## Procedure
In OpenShot create a 960 × 540, 24 fps project. Import both clips and place clip_1 at 0 seconds and clip_2 at 6 seconds on the same video track. Add cleaned_audio.wav at 0 seconds on an audio track. Apply 0.5-second fades at each clip start and end. Create two title overlays using the text and timings in captions.srt; place them near the lower center with a dark outline. Save as video_mix.osp and export H.264 MP4. The supplied build_video.py uses noisy_audio.wav, FFT denoising, fades and burned-in captions to reproduce the provided final video: run python build_video.py with FFmpeg installed.

## Check your output
Play final_captioned.mp4. Check both scenes, the dip-to-black cut at six seconds, readable captions and sound. Compare noisy_audio.wav with cleaned_audio.wav.

## Result and scope
timeline.json is an editable recipe, not a native OpenShot project. The exported sample uses two still-image video clips and synthetic music, not live footage.
