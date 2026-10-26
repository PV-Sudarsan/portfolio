# Project 10 — 3D keyframes, inverse kinematics and mobile UI motion

## Aim
3D keyframes, inverse kinematics and mobile UI motion.

## Tool / environment
Blender plus Lottie-compatible tools/browser

## Files
create_blender_project.py, mobile_pulse.lottie.json, mobile_ui.html

## Procedure
Use a new Blender scene. In Scripting, open and run create_blender_project.py. It saves keyframes_ik.blend. Play frames 1–120 to see the cube translate and rotate. Inspect the two-bone armature and animated IK target in the viewport; the skeleton is intentionally not renderable. Open mobile_ui.html and press Start lesson to see a separate UI confirmation animation. Import mobile_pulse.lottie.json into a Lottie-compatible player/editor for a simple scale pulse.

## Check your output
Confirm the cube changes both position and rotation, and the armature follows its target. The mobile UI and Lottie pulse are separate 2D UI examples; Lottie is not a 3D scene format.

## Result and scope
The folder separates true 3D/keyframe/IK work from the mobile UI animation exercise.

Additional preview: cube_preview.html shows a CSS 3D cube translating and rotating; it is an illustrative browser preview, not a Blender render or IK preview.
