# Project 09 — 2D sprite animation

## Aim
2D sprite animation.

## Tool / environment
Blender; browser preview

## Files
sprite.svg, sprite.png, create_blender_project.py, preview.html

## Procedure
Preview motion in preview.html. For Blender, open the Scripting workspace, choose Open and select create_blender_project.py, then Run Script. The script clears the current scene, creates a textured sprite plane, inserts position keyframes and saves sprite_animation.blend beside itself. Use a new Blender file so existing work is not overwritten. Press Space in the timeline to play. The sprite texture is packed into the saved file.

## Check your output
The robot moves across the scene and bounces at intermediate keyframes. The browser preview illustrates the motion but is not a Blender render.

## Result and scope
The editable vector sprite becomes a transparent image plane animated with position keyframes.

Additional output: sprite_preview.mp4 is a rendered FFmpeg motion preview. Rebuild it with python render_preview.py. It is not a Blender render.
