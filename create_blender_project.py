
import bpy
import math
import random
from pathlib import Path
from mathutils import Vector

# =========================================================
# ANIMATED SPIDER IN AN ENCHANTED FOREST
# Compatible with Blender 4.x and newer animation APIs
# =========================================================

BASE = Path(__file__).resolve().parent
random.seed(42)

# ---------------------------------------------------------
# CLEAR SCENE
# ---------------------------------------------------------

bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)

scene = bpy.context.scene
scene.frame_start = 1
scene.frame_end = 240
scene.render.fps = 24
scene.render.resolution_x = 1920
scene.render.resolution_y = 1080
scene.render.resolution_percentage = 100
scene.render.image_settings.file_format = 'PNG'
scene.render.image_settings.color_mode = 'RGBA'
scene.render.engine = 'CYCLES'
scene.cycles.samples = 32

# ---------------------------------------------------------
# MATERIALS
# ---------------------------------------------------------

def make_material(name, color, metallic=0.0, roughness=0.4,
                  emission_color=None, emission_strength=0.0):
    mat = bpy.data.materials.new(name)
    mat.diffuse_color = (*color, 1.0)

    # Assign through the node tree without setting use_nodes.
    # Modern Blender versions may deprecate use_nodes.
    nodes = mat.node_tree.nodes
    bsdf = nodes.get("Principled BSDF")

    if bsdf is None:
        bsdf = nodes.new("ShaderNodeBsdfPrincipled")
        output = nodes.get("Material Output")
        if output is None:
            output = nodes.new("ShaderNodeOutputMaterial")
        mat.node_tree.links.new(
            bsdf.outputs["BSDF"], output.inputs["Surface"]
        )

    bsdf.inputs["Base Color"].default_value = (*color, 1.0)
    bsdf.inputs["Metallic"].default_value = metallic
    bsdf.inputs["Roughness"].default_value = roughness

    if emission_color:
        emission = bsdf.inputs.get("Emission Color")
        if emission is None:
            emission = bsdf.inputs.get("Emission")

        if emission:
            emission.default_value = (*emission_color, 1.0)

        strength = bsdf.inputs.get("Emission Strength")
        if strength:
            strength.default_value = emission_strength

    return mat


body_mat = make_material(
    "Obsidian blue-black shell",
    (0.018, 0.035, 0.09), 0.72, 0.22
)
abdomen_mat = make_material(
    "Iridescent sapphire abdomen",
    (0.025, 0.12, 0.42), 0.65, 0.2
)
joint_mat = make_material(
    "Brushed steel joints",
    (0.12, 0.19, 0.27), 0.8, 0.25
)
eye_mat = make_material(
    "Glowing cyan eyes",
    (0.01, 0.35, 0.65), 0.2, 0.12,
    (0.02, 0.8, 1.0), 3.0
)
ground_mat = make_material(
    "Forest moss",
    (0.025, 0.11, 0.055), 0.0, 0.9
)
rock_mat = make_material(
    "Mossy stones",
    (0.09, 0.14, 0.105), 0.0, 0.88
)
bark_mat = make_material(
    "Ancient tree bark",
    (0.075, 0.038, 0.022), 0.0, 0.9
)
fern_mat = make_material(
    "Emerald foliage",
    (0.035, 0.25, 0.075), 0.0, 0.7
)
glow_mat = make_material(
    "Magical fireflies",
    (0.2, 0.8, 0.3), 0.0, 0.3,
    (0.1, 1.0, 0.22), 4.0
)

# ---------------------------------------------------------
# HELPERS
# ---------------------------------------------------------

def smooth_mesh(obj):
    if obj.type == 'MESH':
        for poly in obj.data.polygons:
            poly.use_smooth = True


def uv_sphere(name, location, scale, material,
              segments=24, rings=16):
    bpy.ops.mesh.primitive_uv_sphere_add(
        segments=segments,
        ring_count=rings,
        location=location
    )
    obj = bpy.context.object
    obj.name = name
    obj.scale = scale
    obj.data.materials.append(material)
    smooth_mesh(obj)
    return obj


def cylinder_between(name, start, end, radius, material,
                     vertices=12):
    start = Vector(start)
    end = Vector(end)
    delta = end - start
    length = max(delta.length, 0.001)

    bpy.ops.mesh.primitive_cylinder_add(
        vertices=vertices,
        radius=radius,
        depth=length,
        location=(start + end) * 0.5
    )

    obj = bpy.context.object
    obj.name = name
    obj.data.materials.append(material)
    obj.rotation_euler = delta.to_track_quat('Z', 'Y').to_euler()
    smooth_mesh(obj)
    return obj


def set_segment_geometry(obj, start, end):
    """Position and rotate a segment whose original mesh is 1 unit long."""
    start = Vector(start)
    end = Vector(end)
    delta = end - start
    length = max(delta.length, 0.001)

    obj.location = (start + end) * 0.5
    obj.rotation_euler = delta.to_track_quat('Z', 'Y').to_euler()
    obj.scale = (1.0, 1.0, length)


def smooth_animation(obj):
    """
    Legacy Actions expose action.fcurves.
    Newer Blender versions use layered Actions and channel bags.
    If the API differs, leave valid keyframes unchanged.
    """
    anim_data = obj.animation_data
    if not anim_data or not anim_data.action:
        return

    action = anim_data.action

    # Legacy Action API
    if hasattr(action, "fcurves"):
        try:
            for curve in action.fcurves:
                for key in curve.keyframe_points:
                    key.interpolation = 'BEZIER'
            return
        except (AttributeError, RuntimeError, TypeError):
            pass

    # Layered Action API used by newer Blender versions
    try:
        for layer in action.layers:
            for strip in layer.strips:
                if strip.type != 'KEYFRAME':
                    continue

                slot = anim_data.action_slot
                if slot is None:
                    continue

                bag = strip.channelbag(slot, ensure=False)
                if bag is None:
                    continue

                for curve in bag.fcurves:
                    for key in curve.keyframe_points:
                        key.interpolation = 'BEZIER'

    except (AttributeError, RuntimeError, TypeError):
        pass


def key_transform(obj, frame):
    obj.keyframe_insert(data_path="location", frame=frame)
    obj.keyframe_insert(data_path="rotation_euler", frame=frame)
    obj.keyframe_insert(data_path="scale", frame=frame)


# ---------------------------------------------------------
# SPIDER ROOT
# ---------------------------------------------------------

root = bpy.data.objects.new("SPIDER - Animated Root", None)
bpy.context.collection.objects.link(root)
root.empty_display_type = 'SPHERE'
root.empty_display_size = 0.35

# All spider part coordinates are root-local.
# Use a dedicated body controller for body bobbing.
body_control = bpy.data.objects.new("Spider Body Bob", None)
bpy.context.collection.objects.link(body_control)
body_control.parent = root
body_control.location = (0, 0, 0)

# ---------------------------------------------------------
# BODY
# ---------------------------------------------------------

body = uv_sphere(
    "Spider Thorax", (0, 0, 1.05),
    (0.48, 0.42, 0.36), body_mat
)
abdomen = uv_sphere(
    "Sapphire Abdomen", (-0.57, 0, 1.14),
    (0.73, 0.57, 0.48), abdomen_mat
)
head = uv_sphere(
    "Spider Head", (0.43, 0, 1.12),
    (0.35, 0.34, 0.30), body_mat
)

for obj in (body, abdomen, head):
    obj.parent = body_control

# Abdomen markings
for i in range(3):
    spot = uv_sphere(
        f"Abdomen Armor {i+1}",
        (-0.30 - i * 0.22, -0.48, 1.30 - i * 0.035),
        (0.09, 0.035, 0.055), joint_mat, 16, 12
    )
    spot.parent = body_control

# ---------------------------------------------------------
# EYES AND FANGS
# ---------------------------------------------------------

for side in (-1, 1):
    for idx, z in enumerate((1.16, 1.29)):
        eye = uv_sphere(
            f"Glowing Eye {side} {idx}",
            (0.68, side * (0.13 + idx * 0.07), z),
            (0.075, 0.065, 0.075),
            eye_mat, 20, 12
        )
        eye.parent = body_control

    fang = cylinder_between(
        f"Spider Fang {side}",
        (0.59, side * 0.13, 0.97),
        (0.78, side * 0.18, 0.78),
        0.045, joint_mat, 10
    )
    fang.parent = body_control

# ---------------------------------------------------------
# CREATE EIGHT LEGS
# ---------------------------------------------------------

legs = []

for side in (-1, 1):
    for index in range(4):

        hip = Vector((
            0.32 - index * 0.36,
            side * 0.27,
            1.02
        ))

        knee = Vector((
            hip.x + (0.48 if index < 2 else -0.42),
            side * (0.72 + index * 0.04),
            0.84
        ))

        foot = Vector((
            hip.x + (0.72 if index < 2 else -0.72),
            side * (1.12 + index * 0.05),
            0.10
        ))

        # Create segments and normalize their meshes to one unit.
        upper = cylinder_between(
            f"Leg {side} {index+1} Upper",
            hip, knee, 0.075, body_mat
        )
        lower = cylinder_between(
            f"Leg {side} {index+1} Lower",
            knee, foot, 0.045, joint_mat
        )

        upper_length = (knee - hip).length
        lower_length = (foot - knee).length

        # Apply mesh-space length normalization.
        # The segment's scale.z will now represent actual length.
        for obj, length in (
            (upper, upper_length),
            (lower, lower_length)
        ):
            for vertex in obj.data.vertices:
                vertex.co.z /= max(length, 0.001)

            obj.scale = (1.0, 1.0, length)

        # Parenting preserves local coordinates at the root origin.
        upper.parent = root
        lower.parent = root

        knee_joint = uv_sphere(
            f"Leg {side} {index+1} Knee",
            knee, (0.105, 0.105, 0.105),
            abdomen_mat, 16, 12
        )
        knee_joint.parent = root

        hip_joint = uv_sphere(
            f"Leg {side} {index+1} Hip",
            hip, (0.10, 0.10, 0.10),
            joint_mat, 16, 12
        )
        hip_joint.parent = root

        legs.append({
            "side": side,
            "index": index,
            "hip": hip,
            "base_knee": knee.copy(),
            "base_foot": foot.copy(),
            "upper": upper,
            "lower": lower,
            "knee_joint": knee_joint,
            "hip_joint": hip_joint
        })

# ---------------------------------------------------------
# ANIMATE ALL EIGHT LEGS
# ---------------------------------------------------------

for leg in legs:
    side = leg["side"]
    index = leg["index"]

    hip = leg["hip"]
    base_knee = leg["base_knee"]
    base_foot = leg["base_foot"]

    upper = leg["upper"]
    lower = leg["lower"]
    knee_joint = leg["knee_joint"]

    # Four-frame sampling creates a smooth walking cycle.
    for frame in range(1, 241, 4):
        phase = frame * 0.11 + index * math.pi / 2

        if side < 0:
            phase += math.pi

        stride = math.cos(phase) * 0.22
        lift = max(0.0, math.sin(phase)) * 0.24

        knee = base_knee.copy()
        foot = base_foot.copy()

        knee.x += stride * 0.35
        knee.z += lift * 0.25

        foot.x += stride
        foot.z += lift

        # All coordinates are root-local.
        set_segment_geometry(upper, hip, knee)
        key_transform(upper, frame)

        set_segment_geometry(lower, knee, foot)
        key_transform(lower, frame)

        knee_joint.location = knee
        knee_joint.keyframe_insert(
            data_path="location", frame=frame
        )

    smooth_animation(upper)
    smooth_animation(lower)
    smooth_animation(knee_joint)

# ---------------------------------------------------------
# SPIDER ROOT PATH
# ---------------------------------------------------------

root_path = [
    (1, (-3.0, -0.8, 0.0)),
    (60, (-1.4, 0.1, 0.0)),
    (120, (0.4, 0.0, 0.0)),
    (180, (2.0, -0.4, 0.0)),
    (240, (3.0, 0.7, 0.0))
]

for frame, position in root_path:
    root.location = position

    t = (frame - 1) / 239
    root.rotation_euler.z = math.radians(-10 + 18 * t)

    root.keyframe_insert(data_path="location", frame=frame)
    root.keyframe_insert(data_path="rotation_euler", frame=frame)

smooth_animation(root)

# Body bobbing animation
for frame in range(1, 241, 4):
    body_control.location = (
        0, 0, 0.035 * math.sin(frame * 0.22)
    )
    body_control.keyframe_insert(
        data_path="location", frame=frame
    )

smooth_animation(body_control)

# ---------------------------------------------------------
# FOREST FLOOR
# ---------------------------------------------------------

bpy.ops.mesh.primitive_plane_add(
    size=200, location=(0, 0, -0.04)
)
ground = bpy.context.object
ground.name = "Forest Floor"
ground.data.materials.append(ground_mat)

# Procedural moss texture
nodes = ground_mat.node_tree.nodes
links = ground_mat.node_tree.links
bsdf = nodes.get("Principled BSDF")

noise = nodes.new("ShaderNodeTexNoise")
noise.inputs["Scale"].default_value = 18
noise.inputs["Detail"].default_value = 5
noise.inputs["Roughness"].default_value = 0.75

bump = nodes.new("ShaderNodeBump")
bump.inputs["Strength"].default_value = 0.22
bump.inputs["Distance"].default_value = 0.12

links.new(noise.outputs["Fac"], bump.inputs["Height"])
links.new(bump.outputs["Normal"], bsdf.inputs["Normal"])

# Moss mounds
for i in range(90):
    x = random.uniform(-12, 12)
    y = random.uniform(-8, 8)

    if abs(x) < 1.8 and abs(y) < 1.8:
        continue

    uv_sphere(
        "Moss Mound",
        (x, y, 0),
        (
            random.uniform(0.12, 0.42),
            random.uniform(0.12, 0.35),
            random.uniform(0.04, 0.12)
        ),
        ground_mat, 12, 8
    )

# ---------------------------------------------------------
# ANCIENT TREES
# ---------------------------------------------------------

for i in range(42):
    x = random.choice([-1, 1]) * random.uniform(4.5, 13)
    y = random.uniform(-9, 12)

    height = random.uniform(4.5, 9.0)
    radius = random.uniform(0.18, 0.42)

    bpy.ops.mesh.primitive_cone_add(
        vertices=10,
        radius1=radius * 1.5,
        radius2=radius * 0.55,
        depth=height,
        location=(x, y, height / 2 - 0.03)
    )
    trunk = bpy.context.object
    trunk.name = "Ancient Tree Trunk"
    trunk.data.materials.append(bark_mat)

    for tier in range(3):
        tier_z = height * (0.55 + tier * 0.14)
        canopy_radius = random.uniform(1.0, 2.0) * (
            1.0 - tier * 0.17
        )

        bpy.ops.mesh.primitive_cone_add(
            vertices=12,
            radius1=canopy_radius,
            radius2=0.12,
            depth=height * 0.34,
            location=(x, y, tier_z)
        )
        canopy = bpy.context.object
        canopy.name = "Emerald Tree Canopy"
        canopy.data.materials.append(fern_mat)

# ---------------------------------------------------------
# FERNS
# ---------------------------------------------------------

for i in range(100):
    x = random.uniform(-10, 10)
    y = random.uniform(-7, 10)

    if abs(x) < 1.4 and abs(y) < 1.6:
        continue

    base = Vector((x, y, 0.02))

    for leaf_index in range(5):
        angle = leaf_index * math.tau / 5
        length = random.uniform(0.25, 0.55)

        tip = base + Vector((
            math.cos(angle) * length,
            math.sin(angle) * length,
            random.uniform(0.18, 0.42)
        ))

        cylinder_between(
            "Fern Frond", base, tip,
            0.025, fern_mat, 8
        )

# ---------------------------------------------------------
# MOSSY STONES
# ---------------------------------------------------------

for i in range(45):
    x = random.uniform(-11, 11)
    y = random.uniform(-8, 9)

    if abs(x) < 1.8 and abs(y) < 1.6:
        continue

    bpy.ops.mesh.primitive_ico_sphere_add(
        subdivisions=2,
        radius=1,
        location=(x, y, 0.12)
    )
    stone = bpy.context.object
    stone.name = "Moss-Covered Stone"
    stone.scale = (
        random.uniform(0.18, 0.55),
        random.uniform(0.18, 0.48),
        random.uniform(0.12, 0.28)
    )
    stone.data.materials.append(rock_mat)

# ---------------------------------------------------------
# ANIMATED FIREFLIES
# ---------------------------------------------------------

for i in range(65):
    x = random.uniform(-8, 8)
    y = random.uniform(-5, 8)
    z = random.uniform(0.4, 3.2)

    firefly = uv_sphere(
        "Glowing Firefly",
        (x, y, z),
        (0.035, 0.035, 0.035),
        glow_mat, 12, 8
    )

    initial = Vector((x, y, z))

    for frame in (1, 60, 120, 180, 240):
        t = frame / 240 * math.tau

        firefly.location = (
            initial.x + 0.2 * math.sin(t + i),
            initial.y + 0.2 * math.cos(t * 1.3 + i),
            initial.z + 0.18 * math.sin(t * 2 + i)
        )

        firefly.keyframe_insert(
            data_path="location", frame=frame
        )

    smooth_animation(firefly)

# ---------------------------------------------------------
# WORLD AND LIGHTING
# ---------------------------------------------------------

world = bpy.data.worlds.new("Twilight Forest Atmosphere")
scene.world = world
world.use_nodes = True

world.node_tree.nodes["Background"].inputs["Color"].default_value = (
    0.018, 0.035, 0.075, 1
)
world.node_tree.nodes["Background"].inputs["Strength"].default_value = 0.28

# Moonlight
bpy.ops.object.light_add(type='AREA', location=(0, -5, 9))
key_light = bpy.context.object
key_light.name = "Moonlight"
key_light.data.energy = 1800
key_light.data.shape = 'DISK'
key_light.data.size = 8
key_light.data.color = (0.55, 0.72, 1.0)

key_light.rotation_euler = (
    Vector((0, 0, 0)) - key_light.location
).to_track_quat('-Z', 'Y').to_euler()

# Warm rim light
bpy.ops.object.light_add(type='AREA', location=(4, 3, 5))
rim_light = bpy.context.object
rim_light.name = "Golden Rim Light"
rim_light.data.energy = 1400
rim_light.data.shape = 'DISK'
rim_light.data.size = 5
rim_light.data.color = (1.0, 0.55, 0.22)

rim_light.rotation_euler = (
    Vector((0, 0, 1)) - rim_light.location
).to_track_quat('-Z', 'Y').to_euler()

# Blue fill light
bpy.ops.object.light_add(type='AREA', location=(-5, -3, 3.5))
fill_light = bpy.context.object
fill_light.name = "Blue Fill Light"
fill_light.data.energy = 800
fill_light.data.size = 6
fill_light.data.color = (0.22, 0.55, 1.0)

fill_light.rotation_euler = (
    Vector((0, 0, 1)) - fill_light.location
).to_track_quat('-Z', 'Y').to_euler()

# ---------------------------------------------------------
# CAMERA
# ---------------------------------------------------------

bpy.ops.object.camera_add(location=(8.5, -14, 7.0))
camera = bpy.context.object
camera.name = "Cinematic Spider Camera"
camera.data.lens = 42
camera.data.dof.use_dof = True
camera.data.dof.focus_object = head
camera.data.dof.aperture_fstop = 5.6

scene.camera = camera

for frame, location in [
    (1, (8.5, -14, 7.0)),
    (120, (7.5, -13, 6.5)),
    (240, (6.5, -12, 6.0))
]:
    camera.location = location
    camera.rotation_euler = (
        Vector((0, 0, 1.1)) - camera.location
    ).to_track_quat('-Z', 'Y').to_euler()

    camera.keyframe_insert(data_path="location", frame=frame)
    camera.keyframe_insert(data_path="rotation_euler", frame=frame)

smooth_animation(camera)

# ---------------------------------------------------------
# COLOR MANAGEMENT AND OUTPUT
# ---------------------------------------------------------

scene.view_settings.view_transform = 'AgX'

try:
    scene.view_settings.look = 'AgX - Medium High Contrast'
except TypeError:
    pass

scene.render.filepath = str(BASE / "spider_forest_")
scene.frame_set(1)

bpy.ops.object.select_all(action='DESELECT')
root.select_set(True)
bpy.context.view_layer.objects.active = root

# Save .blend project
output_path = BASE / "animated_spider_forest.blend"
bpy.ops.wm.save_as_mainfile(filepath=str(output_path))

print("=" * 55)
print("ANIMATED SPIDER FOREST CREATED")
print("=" * 55)
print(f"Project: {output_path}")
print("Animation: Frames 1-240 at 24 FPS")
print("Spider legs: 8 animated legs")
print("No dimensions keyframes used")
print("Render output: spider_forest_")
print("Open Blender and use Render > Render Animation.")
