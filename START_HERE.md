# Multimedia Lab — 13 projects

This collection covers all 13 visible exercises in the supplied image. Each numbered folder has editable sources, a README with aim/procedure/checks, and sample outputs where the runtime can produce them. All example names, music and vector artwork are original educational material. No client assets or paid services are required.

## Start in five steps
1. Extract the whole ZIP. Keep the folder structure intact.
2. Read the README.md in a numbered folder. Markdown files open in any text editor.
3. Open SVG in Inkscape; WAV/MP3 in Audacity; MP4/WebM in a media player or OpenShot; HTML in a browser or Bluefish.
4. For local web serving, install Python 3 and run `python serve.py` from this pack folder. Open http://localhost:8000. This server binds only to your own computer.
5. For Blender projects, open the included .blend if present, or run the generator script in Blender's Scripting workspace. Generators replace the current scene: use a new Blender file.

## Application formats and limits
- Inkscape: editable native SVG files and PNG exports supplied.
- Audacity: separate WAV tracks and .lof import list supplied. Open/import and Save Project to create your own .aup3 session.
- OpenShot: media, captions and a timeline recipe supplied. Import them and save your own .osp session. The repeatable video export uses the provided FFmpeg script.
- Bluefish: editable HTML/CSS/JavaScript supplied; no build tools needed.
- Blender: Python scene generators supplied; any generated .blend files are listed in the validation notes.
- Lottie: an editable JSON pulse animation is supplied, plus a browser UI demonstration.
- E-learning: editable HTML and a SCORM 1.2 ZIP are supplied, not proprietary authoring-app project formats. Test the SCORM package on your chosen LMS before submission.
- VR/AR: a WebXR implementation is supplied as an open browser alternative to the examples in the image, not a native Google Cardboard/OpenSpace3D package. Requires compatible hardware and HTTPS for phone use. Device tracking cannot be verified on a desktop-only runtime.

## What to submit
Use your institution's required formats. These are worked examples, not evidence that you personally performed the exercises. Edit the material, open it in the required application, take your own screenshots and save the native project where required. If the instructor insists on a specific named tool, reproduce/import the supplied assets in that tool.

## Dependencies
Basic previews need only a modern browser and media player. Regeneration uses Python 3 and FFmpeg (with libx264, libmp3lame, libvpx-vp9, libopus and subtitle support). Blender generators need Blender with its bpy API; standalone Python alone cannot execute them unless bpy is installed. Automated screen recording needs Node.js and Playwright plus its Chromium browser.

## Project index
01. Selections and transforms — `01_Image_Selection_Transforms`
02. Logo and homepage banner — `02_Logo_and_Banner`
03. Audio mixing and fades — `03_Audio_Mixing_Effects`
04. MP3 compression — `04_Audio_MP3_Compression`
05. Video mix, noise reduction, effects and captions — `05_Video_Mixing_Captions`
06. Video compression and format conversion — `06_Video_Format_Compression`
07. Homepage with branding, table and quick links — `07_Homepage_Design`
08. Responsive website, navigation and search — `08_Responsive_Search_Navigation`
09. 2D sprite animation — `09_2D_Sprite_Animation`
10. 3D keyframes, inverse kinematics and mobile UI motion — `10_3D_Keyframes_and_Mobile_UI`
11. Screen recording and e-learning editing — `11_Screen_Recording_Lesson`
12. Interactive e-learning module — `12_E_Learning_Module`
13. Simple VR and AR applications — `13_VR_and_AR`
