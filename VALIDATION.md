# Validation and remaining application checks

## Verified here
- All SVG/XML and JSON sources parse, and Python generators pass syntax parsing.
- Audio/video media can be read by FFprobe with positive durations; generated media streams decode through FFmpeg.
- Browser checks passed: mobile horizontal overflow on both website variants, search result and empty states, quiz correct/incorrect feedback, sprite pause and mobile UI action.
- Local HTML links resolve. Captions and recorded-lesson frames were visually inspected.
- The real browser recording and edited MP4 are included in project 11.

## Not verified here
- Blender is unavailable: no .blend files are included. The generators are editable sources that must be run and checked in Blender. They clear the current scene, so use a new file.
- Audacity and OpenShot are unavailable: no native .aup3 or .osp sessions are included. Import the supplied assets using each folder's guide and save in the application.
- The Lottie JSON was structurally checked but was not played in a Lottie application.
- SCORM was not tested in a real LMS. The standalone lesson was browser-tested.
- WebXR/3D GPU rendering and immersive VR/AR were not tested: this runtime has no usable GPU, headset or AR camera. Device testing remains necessary.

See validation_browser.json and validation_media.json for the checks performed. A null browser-test result means not tested, not passed.
