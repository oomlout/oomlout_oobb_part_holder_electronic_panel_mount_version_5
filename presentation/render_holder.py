"""Blender worker: render unchanged STL geometry in millimetres, two views per mesh."""
import json
import math
import sys
from pathlib import Path

import bpy
from mathutils import Matrix, Vector


def linear(v):
    return v / 12.92 if v <= .04045 else ((v + .055) / 1.055) ** 2.4


def material(name, colour, roughness=.4):
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    shader = m.node_tree.nodes.get('Principled BSDF')
    shader.inputs['Base Color'].default_value = (*[linear(v / 255) for v in colour], 1)
    shader.inputs['Roughness'].default_value = roughness
    return m


def aim(obj, point):
    obj.rotation_euler = (Vector(point) - obj.location).to_track_quat('-Z', 'Y').to_euler()


def rear_hardware(scene, job, **kwargs):
    """Use the catalog screw mesh and a nominal across-flats M3 nut."""
    d = job['dimensions']
    bpy.ops.wm.stl_import(filepath=job['back_plate'])
    plate = bpy.context.object
    plate.scale = (.001,) * 3
    plate.rotation_euler.x = math.pi
    plate.location.z = -.001*d['body_depth_mm']
    plate.data.materials.append(material('Rear plate PLA', (0, 177, 183)))
    bpy.ops.import_scene.gltf(filepath=str(Path(__file__).with_name('m3x12_countersunk.glb')))
    screw = next(obj for obj in bpy.context.selected_objects if obj.type == 'MESH')
    screw.data = screw.data.copy()
    screw.data.transform(screw.matrix_world)
    screw.parent = None
    screw.matrix_world = Matrix.Identity(4)
    screw.rotation_mode = 'XYZ'
    screw.rotation_euler.x = math.pi
    bpy.ops.mesh.primitive_cylinder_add(vertices=6, radius=.0055/math.sqrt(3), depth=.0024)
    nut = bpy.context.object
    # Blender cylinders start a hexagon on Y. Put the two bearing flats parallel to X.
    nut.rotation_euler.z = math.pi/2
    bpy.ops.mesh.primitive_cylinder_add(vertices=32, radius=.0015, depth=.004)
    bore = bpy.context.object
    modifier = nut.modifiers.new('M3 bore', 'BOOLEAN')
    modifier.operation, modifier.object = 'DIFFERENCE', bore
    bpy.context.view_layer.objects.active = nut
    bpy.ops.object.modifier_apply(modifier=modifier.name)
    bpy.data.objects.remove(bore, do_unlink=True)
    nut.data.materials.append(material('Steel', (137, 141, 145), .32))
    groups = {'plate': [plate], 'screw': [], 'nut': []}
    for key, original, z in (
        ('screw', screw, d['depth']-d['join_screw_length_mm']),
        ('nut', nut, d['body_depth_mm']-d['join_nut_skin_mm']-d['embedded_nut_depth_mm']/2),
    ):
        for x in (-d['join_x_mm'], d['join_x_mm']):
            item = original.copy()
            scene.collection.objects.link(item)
            item.location = (.001*x, -.001*d['join_y_mm'], -.001*z)
            groups[key].append(item)
        bpy.data.objects.remove(original, do_unlink=True)
    return groups


def render(job):
    bpy.ops.wm.read_factory_settings(use_empty=True)
    scene = bpy.context.scene
    scene.render.engine = 'CYCLES'
    scene.cycles.samples = 24
    scene.cycles.use_denoising = True
    prefs = bpy.context.preferences.addons['cycles'].preferences
    try:
        prefs.compute_device_type = 'OPTIX'
        prefs.get_devices()
        for d in prefs.devices:
            d.use = d.type == 'OPTIX'
        if any(d.use for d in prefs.devices):
            scene.cycles.device = 'GPU'
            # Keep the same studio style; denoise on the GPU during large batches.
            scene.cycles.denoising_use_gpu = True
    except Exception:
        pass
    scene.render.resolution_x = 1000
    scene.render.resolution_y = 1000
    scene.render.resolution_percentage = 100
    scene.render.image_settings.file_format = 'PNG'
    scene.render.image_settings.color_mode = 'RGBA'
    scene.render.film_transparent = True
    scene.view_settings.view_transform = 'AgX'
    scene.world = bpy.data.worlds.new('Studio')
    scene.world.use_nodes = True
    scene.world.node_tree.nodes['Background'].inputs[0].default_value = (.8, .8, .8, 1)
    scene.world.node_tree.nodes['Background'].inputs[1].default_value = .35
    bpy.ops.wm.stl_import(filepath=job['source'])
    part = bpy.context.object
    # STL is in millimetres. Preserve geometry; translate to the floor and centre.
    part.scale = (.001,) * 3
    bpy.context.view_layer.update()
    corners = [part.matrix_world @ Vector(v) for v in part.bound_box]
    lo = Vector([min(v[i] for v in corners) for i in range(3)])
    hi = Vector([max(v[i] for v in corners) for i in range(3)])
    # The production mesh extends inward along +Z. Turn the front towards the camera.
    part.rotation_euler.x = math.pi
    size = hi - lo
    part.data.materials.append(material('Satin teal PLA', (0, 177, 183)))
    # No remeshing, bevel modifier or smoothing of real holes and sharp edges.
    # An open background keeps through-holes legible; floor shadows can resemble hardware.
    span = max(size)
    for name, pos, energy, radius in [
        ('Key', (-2, -3, 5), 22, 4), ('Fill', (3, -1, 3), 12, 3),
        ('Rim', (0, 4, 4), 18, 3), ('Rear fill', (1, 1, -4), 20, 3),
    ]:
        data = bpy.data.lights.new(name, 'AREA')
        data.energy = energy * .07 * (span / .1) ** 2
        data.shape = 'DISK'
        data.size = span * radius
        light = bpy.data.objects.new(name, data)
        scene.collection.objects.link(light)
        light.location = Vector(pos) * span
        aim(light, (0, 0, 0))
    data = bpy.data.cameras.new('Camera')
    data.type = 'ORTHO'
    cam = bpy.data.objects.new('Camera', data)
    scene.collection.objects.link(cam)
    scene.camera = cam
    d = job['dimensions']
    objects = [part]
    if d['variant'] != 'cutout_only':
        # Schematic envelope only. No catalog mesh or clip geometry is available.
        shell = material('Device envelope', (60, 66, 70))
        face = material('Bezel envelope', (34, 39, 43))
        bezel = min(.002, d['depth_mm'] * .0002)
        body_depth = d['depth_mm'] * .001 - bezel
        for name, dims, level, mat in [
            ('Body envelope', (d['width_cutout_mm']*.001, d['height_cutout_mm']*.001, body_depth), -body_depth/2, shell),
            ('Bezel envelope', (d['width_mm']*.001, d['height_mm']*.001, bezel), bezel/2, face),
        ]:
            bpy.ops.mesh.primitive_cube_add(size=1, location=(0, 0, level))
            obj = bpy.context.object
            obj.name, obj.dimensions = name, dims
            obj.data.materials.append(mat)
            objects.append(obj)
    device = objects[1:]
    rear = rear_hardware(scene, job) if d['variant'] == 'box_width_only' else {}
    for group in rear.values():
        objects.extend(group)
    for view in job['views']:
        offset = (d['depth_mm']*.001 + .012) if view == 'aligned' else 0
        for obj in device:
            obj.hide_render = view not in ('aligned', 'seated', 'part_device', 'rear', 'joined')
            obj.location.z += offset
        part.hide_render = view in ('part_device', 'inside_plate', 'outside_plate', 'part_plate', 'part_nut', 'part_screw')
        for key, group in rear.items():
            for i, obj in enumerate(group):
                visible = view in ('rear', 'joined') or (key == 'nut' and view in ('aligned', 'seated'))
                if key == 'plate' and view in ('inside_plate', 'outside_plate'):
                    visible = True
                if view == 'part_' + key:
                    visible = i == 0
                if key == 'nut' and view == 'part_holder':
                    visible = True
                obj.hide_render = not visible
                if key == 'nut' and view == 'part_holder':
                    obj.location.x += math.copysign(.018, obj.location.x)
        pos = (0, 0, 3) if view == 'top' else (.60, -1.45, 1.25)
        if view in ('rear', 'joined', 'outside_plate', 'part_plate', 'part_screw'):
            pos = (.6, 1.3, -2.2)
        cam.location = Vector(pos) * span
        scene.render.resolution_x, scene.render.resolution_y = 960, 740
        center_z = -size.z / 2
        if view in ('aligned', 'seated', 'part_holder'):
            center_z += .014
        aim(cam, (0, 0, center_z))
        if view in ('rear', 'joined', 'outside_plate', 'inside_plate', 'part_plate'):
            # Physical +Y on the installed plate is screen-up, so the wire exit
            # reads as a bottom opening from either side.
            eye = (cam.location - Vector((0, 0, center_z))).normalized()
            right = Vector((0, -1, 0)).cross(eye).normalized()
            cam.rotation_euler = Matrix((right, eye.cross(right), eye)).transposed().to_euler()
        bpy.context.view_layer.update()
        bounds = [cam.matrix_world.inverted() @ (obj.matrix_world @ Vector(v))
                  for obj in objects if not obj.hide_render for v in obj.bound_box]
        x0, x1 = min(v.x for v in bounds), max(v.x for v in bounds)
        y0, y1 = min(v.y for v in bounds), max(v.y for v in bounds)
        cam.location += cam.rotation_euler.to_quaternion() @ Vector(((x0+x1)/2, (y0+y1)/2, 0))
        data.ortho_scale = max(x1-x0, (y1-y0)*960/740)*1.12
        if view in ('aligned', 'seated', 'part_holder'):
            data.ortho_scale = max(data.ortho_scale, span*1.43)
        data.clip_start = .0001
        scene.render.filepath = str(Path(job['directory']) / (view + '.png'))
        bpy.ops.render.render(write_still=True)
        for obj in device:
            obj.location.z -= offset
        if view == 'part_holder':
            for nut in rear.get('nut', []):
                nut.location.x -= math.copysign(.018, nut.location.x)
    print('OOBB rendered ' + job['key'], flush=True)


if __name__ == '__main__':
    jobs = json.loads(Path(sys.argv[sys.argv.index('--') + 1]).read_text())
    for job in jobs:
        render(job)
