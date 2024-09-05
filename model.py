# model.py
import bpy
import bmesh
import numpy as np
import os
import math
from math import radians
from pathlib import Path
from mathutils import *
import random
import sys
import json
from utils.EyePupils import *


current_dir = os.getcwd()
parent_dir = os.getcwd()# os.path.dirname(current_dir)

class SyntheticFaceGenerator:
    def __init__(self):
        
        self.data_json= self.read_json(os.path.join(os.path.dirname(__file__),"utils/utils.json"))
        self.leftI = self.data_json.get("leftI", [])           
        self.rightI = self.data_json.get("rightI", [])   
        self.hdri_path = Path(os.path.join(os.path.dirname(__file__),"HDRI"))
        self.IMAGE_Back = [str(f) for f in self.hdri_path.glob("*")]
        self.init_blendshapes()
        self.LeftPupil = None
        self.RightPupil = None
        
    def read_json(self,file_path):
        with open(file_path, 'r') as json_file:
            data = json.load(json_file)
        
        # Access the stored variable
        return data
        
    def init_blendshapes(self):
        bpy.ops.keentools_fb.create_blendshapes()
        obj = bpy.data.objects.get('FBHead')
        if obj:
            bpy.ops.object.select_all(action='DESELECT')
            obj.select_set(True)
            bpy.context.view_layer.objects.active = obj

    def load_head_texture(self, texture_id):
        
        if(Path(texture_id).is_file()):
            try:
                bpy.ops.keentools_fb.open_single_filebrowser(filepath=str(texture_id), camnum=0)
                bpy.ops.keentools_fb.open_single_filebrowser(filepath=str(texture_id).replace(Path(texture_id).stem,
                                                                                              str(Path(texture_id).stem)+"_mirror"), camnum=1)
            except Exception as e:
                print(f"Error loading head texture: {e}")
                return
        else:
            head_model_dir = Path(os.path.join(os.path.dirname(__file__),"HeadModel/Head"))
            try:
                bpy.ops.keentools_fb.open_single_filebrowser(filepath=str(head_model_dir) + f"{texture_id}.jpeg", camnum=0)
                bpy.ops.keentools_fb.open_single_filebrowser(filepath=str(head_model_dir) + f"{texture_id}_mirror.jpeg", camnum=1)
            except Exception as e:
                print(f"Error loading head texture: {e}")
                return

        bpy.ops.keentools_fb.select_camera(headnum=0, camnum=0)
        bpy.ops.keentools_fb.pickmode_starter(headnum=0, camnum=0)
        bpy.ops.keentools_fb.exit_pinmode()
        bpy.ops.keentools_fb.select_camera(headnum=0, camnum=1)
        bpy.ops.keentools_fb.pickmode_starter(headnum=0, camnum=1)
        bpy.context.scene.keentools_fb_settings.tex_uv_expand_percents = 20 
        bpy.context.scene.keentools_fb_settings.tex_width = 8192
        bpy.context.scene.keentools_fb_settings.tex_height = 8192
        bpy.ops.keentools_fb.tex_selector()
        
        

    def add_environment_texture(self, background_path):
        C = bpy.context
        scn = C.scene
        node_tree = scn.world.node_tree
        tree_nodes = node_tree.nodes
        tree_nodes.clear()

        node_background = tree_nodes.new(type='ShaderNodeBackground')
        node_environment = tree_nodes.new('ShaderNodeTexEnvironment')
        node_environment.image = bpy.data.images.load(background_path)
        node_output = tree_nodes.new(type='ShaderNodeOutputWorld')
        node_mapping = tree_nodes.new(type='ShaderNodeMapping')
        node_tex_coord = tree_nodes.new(type='ShaderNodeTexCoord')

        links = node_tree.links
        links.new(node_tex_coord.outputs[0], node_mapping.inputs[0])
        links.new(node_mapping.outputs[0], node_environment.inputs[0])
        links.new(node_environment.outputs["Color"], node_background.inputs[0])
        links.new(node_background.outputs[0], node_output.inputs["Surface"])

        node_mapping.inputs[2].default_value[2] = math.radians(random.randint(0, 360))
        node_background.inputs[1].default_value = random.uniform(0.2, 0.5)

    def sphere_fit(self, spX, spY, spZ):
        spX, spY, spZ = np.array(spX), np.array(spY), np.array(spZ)
        A = np.column_stack((spX * 2, spY * 2, spZ * 2, np.ones(len(spX))))
        f = spX**2 + spY**2 + spZ**2
        C, _, _, _ = np.linalg.lstsq(A, f[:, np.newaxis], rcond=None)
        radius = math.sqrt(np.sum(C[:3]**2) + C[3])
        return radius, C[0], C[1], C[2]

    def add_texture(self, texture_path, obj):
        mat = bpy.data.materials.new(name='texture_Eye')
        mat.use_nodes = True
        nodes = mat.node_tree.nodes
        tex_image = nodes.new('ShaderNodeTexImage')
        tex_image.image = bpy.data.images.load(texture_path)
        principled = nodes['Principled BSDF']
        principled.inputs[9].default_value = 1
        principled.inputs[7].default_value = 0
        transparent = nodes.new('ShaderNodeBsdfTransparent')
        transparent.inputs[0].default_value = (0, 0, 0, 1)
        mix_shader = nodes.new('ShaderNodeMixShader')
        mix_shader.inputs[0].default_value = 0.1

        mat.node_tree.links.new(tex_image.outputs[0], principled.inputs[0])
        mat.node_tree.links.new(principled.outputs[0], mix_shader.inputs[1])
        mat.node_tree.links.new(transparent.outputs[0], mix_shader.inputs[2])
        mat.node_tree.links.new(mix_shader.outputs[0], nodes['Material Output'].inputs[0])

        obj.data.materials.clear()
        obj.data.materials.append(mat)
        
    def head_texture(self):
        mat =  bpy.data.materials["FBHead_preview_mat"]
        mat.use_nodes = True
        nodes = mat.node_tree.nodes
        principled = nodes['Principled BSDF']
        principled.inputs[9].default_value = 0.9
        principled.inputs[7].default_value = 0
        transparent = nodes.new('ShaderNodeBsdfTransparent')
        transparent.inputs[0].default_value = (0, 0, 0, 1)
        mix_shader = nodes.new('ShaderNodeMixShader')
        mix_shader.inputs[0].default_value = 0.1
        
        mat.node_tree.links.new(principled.outputs[0], mix_shader.inputs[1])
        mat.node_tree.links.new(transparent.outputs[0], mix_shader.inputs[2])
        mat.node_tree.links.new(mix_shader.outputs[0], nodes['Material Output'].inputs[0])

        
        
        

    def apply_transform_rotation(self, obj):
        bpy.ops.object.select_all(action='DESELECT')
        obj.select_set(True)
        bpy.context.view_layer.objects.active = obj
        bpy.ops.object.transform_apply(location=False, rotation=True, scale=False)

    def create_eye_sphere(self, array, name, x, y, z, texture_path):
        rx, ry, rz = x[array], y[array], z[array]
        res = 64
        radius, cxr, cyr, czr = self.sphere_fit(rx, ry, rz)
        bpy.ops.mesh.primitive_uv_sphere_add(segments=res * 2, ring_count=res, radius=radius * 1.04, location=((cxr + cxr) / 2, cyr, (czr + czr) / 2))
        bpy.context.object.name = name
        obj = bpy.context.object
        

    def rotate_eyes(self, obj):
        obj.rotation_euler[2] = radians(-90)
        self.apply_transform_rotation(obj)
        if obj.name == 'Left Eye':
            self.LeftPupil, _ = MapPointToMesh(obj.location, obj)
            obj.rotation_euler = (0.0, radians(-2.2), radians(7))
        else:
            self.RightPupil, _ = MapPointToMesh(obj.location, obj)
            obj.rotation_euler = (0.0, radians(-2.2), radians(-4))
        self.apply_transform_rotation(obj)

    def add_constraint(self, obj_act, target, constraint_type, constraint_name):
        bpy.context.view_layer.objects.active = obj_act
        bpy.ops.object.constraint_add(type=constraint_type)
        bpy.context.object.constraints[constraint_name].target = target

    def start(self):
        for img in bpy.data.images:
            if not img.users:
                bpy.data.images.remove(img)

        self.load_head_texture(sys.argv[6])
        self.head_texture()
        eye_texture_dir = Path(os.path.join(os.path.dirname(__file__),"EyeTextures/"))
        eye_textures = sorted([str(f) for f in eye_texture_dir.glob("*")])
        chosen_eye_texture = eye_textures[4]  # Or random.choice(eye_textures)
        self.add_environment_texture(self.IMAGE_Back[random.randint(0, len(self.IMAGE_Back) - 1)])
        
        fb_head = bpy.data.objects['FBHead']
        fb_head.location = Vector((1.3637299537658691, -0.3416078984737396, 1.00064218044281))
        fb_head.rotation_euler = Euler((0.0, 0.0, radians(-90)), 'XYZ')
        fb_head.scale = Vector((0.1102, 0.1202, 0.1202))
        self.apply_transform_rotation(fb_head)

        obj = bpy.data.objects['FBHead']
        depsgraph = bpy.context.evaluated_depsgraph_get()
        obj_eval = obj.evaluated_get(depsgraph)
        mesh = obj_eval.to_mesh()
        mesh.transform(obj_eval.matrix_world)

        # x, y, z = np.array([v.co[i] for v in mesh.vertices] for i in range(3))
        x = np.array([ v.co[0] for v in mesh.vertices])
        y = np.array([ v.co[1] for v in mesh.vertices])
        z = np.array([ v.co[2] for v in mesh.vertices])
        self.create_eye_sphere(self.leftI, 'Left Eye', x, y, z, chosen_eye_texture)
        self.create_eye_sphere(self.rightI, 'Right Eye', x, y, z, chosen_eye_texture)
        self.rotate_eyes(bpy.data.objects['Left Eye'])
        self.rotate_eyes(bpy.data.objects['Right Eye'])
        self.add_texture(chosen_eye_texture, bpy.data.objects['Left Eye'])
        bpy.data.objects['Right Eye'].data.materials.append(bpy.data.materials['texture_Eye'])
        self.add_constraint(bpy.data.objects['Left Eye'], fb_head, 'CHILD_OF', "Child Of")
        self.add_constraint(bpy.data.objects['Right Eye'], fb_head, 'CHILD_OF', "Child Of")
        self.add_constraint(bpy.data.objects['Left Eye'], bpy.data.objects['Right Eye'], 'COPY_ROTATION', "Copy Rotation")

        print('generator printer',self.RightPupil, self.LeftPupil)


if __name__ == "__main__":
    generator = SyntheticFaceGenerator()
    generator.start()
    print('generator printer',generator.RightPupil, generator.LeftPupil)
