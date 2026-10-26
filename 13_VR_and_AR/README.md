# Project 13 — Simple VR and AR applications

## Aim
Simple VR and AR applications.

## Tool / environment
WebXR-compatible browser/device (alternative to the example tools)

## Files
index.html, xr.js

## Procedure
For desktop preview run python serve.py from the pack root and browse to this folder. For immersive VR use a compatible headset browser. For AR host this folder on HTTPS and open it on a compatible phone; grant camera/XR permissions when prompted. Enter AR, move the camera slowly until the small cube marks a detected plane, then tap to place the larger cube. Tap another detected surface to reposition it. End session exits immersive mode.

## Check your output
Unsupported browsers keep the desktop preview and disable unavailable immersive modes. Actual VR/AR must be tested on compatible hardware. The desktop preview is not proof of device tracking.

## Result and scope
This is a real WebXR API example with stereo VR views and AR hit testing. It is not a Google Cardboard SDK or OpenSpace3D project; ordinary phone viewers without WebXR support cannot run its immersive mode.
