import bpy, math
from pathlib import Path
from mathutils import Vector
BASE=Path(__file__).resolve().parent
bpy.ops.object.select_all(action='SELECT');bpy.ops.object.delete(use_global=False)
s=bpy.context.scene;s.frame_start=1;s.frame_end=120;s.render.fps=24
bpy.ops.mesh.primitive_cube_add(location=(-2,0,1));cube=bpy.context.object;cube.name='Keyframed cube'
mat=bpy.data.materials.new('Blue');mat.diffuse_color=(.05,.25,.8,1);cube.data.materials.append(mat)
for f,x,z,rot in [(1,-2,1,0),(30,-1,3,90),(60,0,1,180),(90,1,2.5,270),(120,2,1,360)]:
 cube.location=(x,0,z);cube.rotation_euler=(0,math.radians(rot),math.radians(rot));cube.keyframe_insert(data_path='location',frame=f);cube.keyframe_insert(data_path='rotation_euler',frame=f)
bpy.ops.object.armature_add(location=(0,2,0));arm=bpy.context.object;arm.name='Two bone IK demonstration';arm.show_in_front=True
bpy.ops.object.mode_set(mode='EDIT');a=arm.data.edit_bones[0];a.name='Upper';a.head=(0,0,0);a.tail=(0,0,1.5);b=arm.data.edit_bones.new('Lower');b.head=a.tail;b.tail=(0,0,3);b.parent=a;b.use_connect=True;bpy.ops.object.mode_set(mode='OBJECT')
bpy.ops.object.empty_add(location=(1,2,2));target=bpy.context.object;target.name='Animated IK target'
con=arm.pose.bones['Lower'].constraints.new('IK');con.target=target;con.chain_count=2
for f,x,z in [(1,1,2),(60,-1,2.5),(120,1,2)]:
 target.location=(x,2,z);target.keyframe_insert(data_path='location',frame=f)
bpy.ops.mesh.primitive_plane_add(size=200);floor=bpy.context.object;floor.name='Ground'
bpy.ops.object.light_add(type='AREA',location=(2,-4,7));bpy.context.object.data.energy=900;bpy.context.object.data.shape='DISK';bpy.context.object.data.size=5
bpy.ops.object.camera_add(location=(7,-11,7));cam=bpy.context.object;cam.rotation_euler=(Vector((0,0,1))-cam.location).to_track_quat('-Z','Y').to_euler();s.camera=cam
s.world.color=(.2,.2,.2);s.render.resolution_x=960;s.render.resolution_y=540;s.render.resolution_percentage=100
s.frame_set(1);bpy.ops.wm.save_as_mainfile(filepath=str(BASE/'keyframes_ik.blend'))
print('Saved keyframes_ik.blend. IK bones/target are visible in the viewport, not rendered.')
