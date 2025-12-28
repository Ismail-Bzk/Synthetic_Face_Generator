import sys
import subprocess
import os
import random
import bpy
import bpy_extras
from bpy.props import StringProperty, IntProperty, BoolProperty
from bpy_extras.io_utils import ExportHelper
from mathutils import Matrix
from mathutils import *
import numpy as np
from pathlib import Path
import math
import csv

current_dir = os.path.dirname(__file__)
parent_dir = os.path.dirname(current_dir)

def load_csv(csv_filename):
    l = []
    csv_path = os.path.join(parent_dir, f"txt/{csv_filename}")
    with open(csv_path, newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='"')
        for row in reader:
            l.append(row)
    l = np.array(l[1:])  # Skip the header
    return l

def choose_asset(asset_list,chosen="random"):
    
    if chosen not in ["random","empty"] :
        
        for i, asset in enumerate(asset_list):
            if chosen in asset:
                return asset_list[int(i)]
    else:
        return random.choice(asset_list)

def apply_material(obj, texture_diffuse_path, texture_normal_path=None):
    mat = bpy.data.materials.new(name=f'texture_{obj.name}')
    mat.use_nodes = True
    nodes = mat.node_tree.nodes

    tex_image_diff = nodes.new('ShaderNodeTexImage')
    tex_image_diff.image = bpy.data.images.load(texture_diffuse_path, check_existing=True)

    mix_rgb = nodes.new('ShaderNodeMixRGB')
    mix_rgb.inputs[0].default_value = random.uniform(0.75, 1)
    mix_rgb.inputs[1].default_value = (random.random(), random.random(), random.random(), 1)

    principled = nodes.get('Principled BSDF')
    if principled is None:
        principled = nodes.new('ShaderNodeBsdfPrincipled')
        output = nodes.get('Material Output')
        if output:
            mat.node_tree.links.new(principled.outputs[0], output.inputs[0])
    roughness_input = principled.inputs.get("Roughness")
    if roughness_input:
        roughness_input.default_value = 0.9

    mat.node_tree.links.new(tex_image_diff.outputs[0], mix_rgb.inputs[2])
    if tex_image_diff.outputs.get("Alpha") and principled.inputs.get("Alpha"):
        mat.node_tree.links.new(tex_image_diff.outputs["Alpha"], principled.inputs["Alpha"])
    mat.node_tree.links.new(mix_rgb.outputs[0], principled.inputs[0])

    if texture_normal_path:
        tex_image_norm = nodes.new('ShaderNodeTexImage')
        tex_image_norm.image = bpy.data.images.load(texture_normal_path, check_existing=True)
        bpy.data.images[Path(texture_normal_path).name].colorspace_settings.name = 'Non-Color'

        normal_map = nodes.new('ShaderNodeNormalMap')
        bump_map = nodes.new('ShaderNodeBump')
        normal_map.inputs[0].default_value = random.uniform(0.8, 1)

        mat.node_tree.links.new(tex_image_norm.outputs[0], normal_map.inputs[1])
        mat.node_tree.links.new(normal_map.outputs[0], bump_map.inputs[3])
        if principled.inputs.get("Normal"):
            mat.node_tree.links.new(bump_map.outputs[0], principled.inputs["Normal"])

    if obj.data.materials:
        obj.data.materials[0] = mat
    else:
        obj.data.materials.append(mat)

def import_and_configure_obj(asset_params, asset_type):
    chosen_file = asset_params[0]
    asset_name = asset_params[1]
    localisation = (float(asset_params[2]), float(asset_params[3]), float(asset_params[4]))
    scale = (float(asset_params[5]), float(asset_params[6]), float(asset_params[7]))

    rotation = bpy.data.objects['FBHead'].rotation_euler.copy()
    bpy.data.objects['FBHead'].rotation_euler = (0, 0, 0)
    path = Path(os.path.join(parent_dir, f"Hair2/makehuman_system_assets_cc0/{asset_type}/"))
    filepath = str(path) + "/" + chosen_file + "/" + asset_name + ".obj"
    if hasattr(bpy.ops.wm, "obj_import"):
        bpy.ops.wm.obj_import(filepath=filepath)
    else:
        bpy.ops.import_scene.obj(filepath=filepath)
    a = bpy.data.objects[asset_name]
    bpy.context.view_layer.objects.active = a
    bpy.ops.object.origin_set(type='GEOMETRY_ORIGIN', center='MEDIAN')
    a.rotation_euler[2] = math.radians(-90)
    bpy.ops.object.transform_apply(location=False, rotation=True, scale=False)
    subsurf = a.modifiers.new(name="Subdivision", type='SUBSURF')
    subsurf.render_levels = 3
    a.location = localisation
    a.scale = scale

    a.rotation_euler = bpy.data.objects['FBHead'].rotation_euler
    child = a.constraints.new(type='CHILD_OF')
    child.target = bpy.data.objects["FBHead"]
    copy_rot = a.constraints.new(type='COPY_ROTATION')
    copy_rot.target = bpy.data.objects["FBHead"]
    bpy.data.objects['FBHead'].rotation_euler = rotation

    texture_diffuse_path = str(path) + "/" + chosen_file + "/" + asset_name + "_diffuse.png"
    texture_normal_path = str(path) + "/" + chosen_file + "/" + asset_name + "_normal.png" if asset_type != "SunGlasses" else None

    apply_material(a, texture_diffuse_path, texture_normal_path)

    return a

def Hat(chosen="random"):
    l = load_csv("hat.txt")
    chosen_param = choose_asset(l,chosen)
    return import_and_configure_obj(chosen_param, "clothes")

def Maskk(chosen="random"):
    l = load_csv("mask.txt")
    chosen_param = choose_asset(l,chosen)
    return import_and_configure_obj(chosen_param, "mask")

def SunGlasses(chosen="random"):
    l = load_csv("SunGlasses.txt")
    chosen_param = choose_asset(l,chosen)
    return import_and_configure_obj(chosen_param, "mask")

def Beard(chosen="random"):
    l = load_csv("beard.txt")
    chosen_param = choose_asset(l,chosen)
    return import_and_configure_obj(chosen_param, "beard")

if __name__ == "__main__":
    asset_choice = input("Choose an asset to add (Hat, Maskk, SunGlasses, Beard): ").strip().lower()

    if asset_choice == "hat":
        Hat()
    elif asset_choice == "maskk":
        Maskk()
    elif asset_choice == "sunglasses":
        SunGlasses()
    elif asset_choice == "beard":
        Beard()
    else:
        print("Invalid choice. Please select a valid asset.")
