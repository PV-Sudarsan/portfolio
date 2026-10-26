import bpy, os
from pathlib import Path
BASE=Path(__file__).resolve().parent
bpy.ops.object.select_all(action='SELECT');bpy.ops.object.delete(use_global=False)
scene=bpy.context.scene;scene.frame_start=1;scene.frame_end=96;scene.render.fps=24
bpy.ops.mesh.primitive_plane_add(size=2);obj=bpy.context.object;obj.name='Robot sprite'
mat=bpy.data.materials.new('Sprite texture');mat.use_nodes=True
n=mat.node_tree.nodes;n.clear();tex=n.new('ShaderNodeTexImage');tex.image=bpy.data.images.load(str(BASE/'sprite.png'));tex.image.pack()
em=n.new('ShaderNodeEmission');tr=n.new('ShaderNodeBsdfTransparent');mix=n.new('ShaderNodeMixShader');out=n.new('ShaderNodeOutputMaterial')
l=mat.node_tree.links;l.new(tex.outputs['Color'],em.inputs[0]);l.new(tex.outputs['Alpha'],mix.inputs[0]);l.new(tr.outputs[0],mix.inputs[1]);l.new(em.outputs[0],mix.inputs[2]);l.new(mix.outputs[0],out.inputs[0]);obj.data.materials.append(mat)
for frame,x,y in [(1,-3,0),(24,-1.5,1),(48,0,0),(72,1.5,1),(96,3,0)]:
 obj.location=(x,y,0);obj.keyframe_insert(data_path='location',frame=frame)
bpy.ops.object.camera_add(location=(0,1,12));cam=bpy.context.object;cam.data.type='ORTHO';cam.data.ortho_scale=10;scene.camera=cam
scene.world.color=(.18,.24,.35);scene.render.resolution_x=960;scene.render.resolution_y=540;scene.render.resolution_percentage=100
scene.frame_set(1);bpy.ops.wm.save_as_mainfile(filepath=str(BASE/'sprite_animation.blend'))
print('Saved sprite_animation.blend. Press Space in the timeline to play; render with Ctrl+F12.')
