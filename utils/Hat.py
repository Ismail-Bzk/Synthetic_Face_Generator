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
import os
import sys
import math
import csv


current_dir = os.path.dirname(__file__)
parent_dir = os.path.dirname(current_dir)



def Hat():
        l=[]
        csv_path = os.path.join(parent_dir,"txt/hat.txt")
        # Ouvrir le fichier CSV
        with open(csv_path, newline='') as csvfile:
            reader =csv.reader(csvfile, delimiter=',', quotechar='"')
            # Parcourir chaque ligne du fichier CSV
            for row in reader:
                # Récupérer les données de chaque colonne
                l.append(row)
        # Chemin vers le fichier CSV   x=z_t, y=x_t , z=y_t
        l= l[1:]
        l= np.array(l)
        chosen_Param = random.choice(l)
        chosen_File = chosen_Param[0]
        Hair_name = chosen_Param[1]
        localisation = (float(chosen_Param[2]),float(chosen_Param[3]),float(chosen_Param[4]))
        scale = (float(chosen_Param[5]),float(chosen_Param[6]),float(chosen_Param[7]))
        
        rotation = bpy.data.objects['FBHead'].rotation_euler.copy()
        bpy.data.objects['FBHead'].rotation_euler = (0,0,0)
        path = Path(os.path.join(parent_dir,"Hair2/makehuman_system_assets_cc0/clothes/"))
        filepath = str(path) + "/"+chosen_File + "/" + Hair_name+".obj"
        bpy.ops.wm.obj_import(filepath=filepath)
        a = bpy.data.objects[Hair_name]
        bpy.context.view_layer.objects.active = a
        bpy.ops.object.origin_set(type='GEOMETRY_ORIGIN', center='MEDIAN')
        a.rotation_euler[2] = math.radians(-90)
        bpy.ops.object.transform_apply(location=False, rotation=True, scale=False)
        bpy.ops.object.modifier_add(type='SUBSURF')
        bpy.context.object.modifiers["Subdivision"].render_levels = 3
        a.location = localisation
        a.scale = scale
        
        a.rotation_euler = bpy.data.objects['FBHead'].rotation_euler
        bpy.ops.object.constraint_add(type='CHILD_OF')
        bpy.context.object.constraints["Child Of"].target = bpy.data.objects["FBHead"]
        bpy.ops.object.constraint_add(type='COPY_ROTATION')
        bpy.context.object.constraints["Copy Rotation"].target = bpy.data.objects["FBHead"]
        bpy.data.objects['FBHead'].rotation_euler = rotation
        
        
        #path = Path.home() / "Documents/Synthetic_data/Hair2/makehuman_system_assets_cc0/clothes/"
        
        texturenorm_path = str(path) + "/" + chosen_File + "/" + Hair_name + "_normal.png"
        texturediff_path = str(path) + "/" + chosen_File + "/" + Hair_name + "_diffuse.png" 
        
        obj  = a 
        mat = bpy.data.materials.new(name='texture_'+obj.name)
        mat.use_nodes = True
        nodes = mat.node_tree.nodes
        #
        texImagediff = nodes.new('ShaderNodeTexImage')
        texImagediff.image = bpy.data.images.load(texturediff_path)
        #
        
        mixRGB = nodes.new('ShaderNodeMixRGB')
        mixRGB.inputs[0].default_value = random.uniform(0.75,1)
        mixRGB.inputs[1].default_value = (random.random(), random.random(), random.random(), 1)

        principled = nodes['Principled BSDF']
        principled.inputs[9].default_value = 0.9
        
        texImagenorm = nodes.new('ShaderNodeTexImage')
        texImagenorm.image = bpy.data.images.load(texturenorm_path)
        bpy.data.images[ Path(texturenorm_path).name].colorspace_settings.name = 'Non-Color'
        
        NormalMap = nodes.new('ShaderNodeNormalMap')
        BumpMap = nodes.new('ShaderNodeBump')
        NormalMap.inputs[0].default_value = random.uniform(0.8,1)

        
        # What to link here? 
        mat.node_tree.links.new( texImagediff.outputs[0], mixRGB.inputs[2] )
        mat.node_tree.links.new( texImagediff.outputs[1], principled.inputs[21] )
        mat.node_tree.links.new( mixRGB.outputs[0], principled.inputs[0] )
        
        mat.node_tree.links.new( texImagenorm.outputs[0], NormalMap.inputs[1])
        mat.node_tree.links.new( NormalMap.outputs[0], BumpMap.inputs[3])
        mat.node_tree.links.new( BumpMap.outputs[0], principled.inputs[22])
        # Assign it to object
        if obj.data.materials:
            obj.data.materials[0] = mat
        else:
            obj.data.materials.append(mat)
        
        return obj

def Maskk():
        l=[]
        csv_path = os.path.join(parent_dir,"txt/mask.txt")
        # Ouvrir le fichier CSV
        with open(csv_path, newline='') as csvfile:
            reader =csv.reader(csvfile, delimiter=',', quotechar='"')
            # Parcourir chaque ligne du fichier CSV
            for row in reader:
                # Récupérer les données de chaque colonne
                l.append(row)
        l= l[1:]
        l= np.array(l)
        chosen_Param = random.choice(l)
        chosen_File = chosen_Param[0]
        Hair_name = chosen_Param[1]
        localisation = (float(chosen_Param[2]),float(chosen_Param[3]),float(chosen_Param[4]))
        scale = (float(chosen_Param[5]),float(chosen_Param[6]),float(chosen_Param[7]))
        
        rotation = bpy.data.objects['FBHead'].rotation_euler.copy()
        bpy.data.objects['FBHead'].rotation_euler = (0,0,0)
        path = Path(os.path.join(parent_dir,"Hair2/makehuman_system_assets_cc0/mask/"))
        filepath = str(path) + "/"+chosen_File + "/" + Hair_name+".obj"
        bpy.ops.wm.obj_import(filepath=filepath)
        a = bpy.data.objects[Hair_name]
        bpy.context.view_layer.objects.active = a
        bpy.ops.object.origin_set(type='GEOMETRY_ORIGIN', center='MEDIAN')
        a.rotation_euler[2] = math.radians(-90)
        bpy.ops.object.transform_apply(location=False, rotation=True, scale=False)
        bpy.ops.object.modifier_add(type='SUBSURF')
        bpy.context.object.modifiers["Subdivision"].render_levels = 3
        a.location = localisation
        a.scale = scale
        
        a.rotation_euler = bpy.data.objects['FBHead'].rotation_euler
        bpy.ops.object.constraint_add(type='CHILD_OF')
        bpy.context.object.constraints["Child Of"].target = bpy.data.objects["FBHead"]
        bpy.ops.object.constraint_add(type='COPY_ROTATION')
        bpy.context.object.constraints["Copy Rotation"].target = bpy.data.objects["FBHead"]
        bpy.data.objects['FBHead'].rotation_euler = rotation
        
        
        #path = Path.home() / "Documents/Synthetic_data/Hair2/makehuman_system_assets_cc0/mask/"
        
        texturenorm_path = str(path) + "/" + chosen_File + "/" + Hair_name + "_normal.png"
        texturediff_path = str(path) + "/" + chosen_File + "/" + Hair_name + "_diffuse.png" 
        
        obj  = a 
        mat = bpy.data.materials.new(name='texture_'+obj.name)
        mat.use_nodes = True
        nodes = mat.node_tree.nodes
        #
        texImagediff = nodes.new('ShaderNodeTexImage')
        texImagediff.image = bpy.data.images.load(texturediff_path)
        #
        
        mixRGB = nodes.new('ShaderNodeMixRGB')
        mixRGB.inputs[0].default_value = random.uniform(0.79,1)
        mixRGB.inputs[1].default_value = (random.random(), random.random(), random.random(), 1)

        principled = nodes['Principled BSDF']
        principled.inputs[9].default_value = 0.9
        
        texImagenorm = nodes.new('ShaderNodeTexImage')
        texImagenorm.image = bpy.data.images.load(texturenorm_path)
        bpy.data.images[ Path(texturenorm_path).name].colorspace_settings.name = 'Non-Color'
        
        NormalMap = nodes.new('ShaderNodeNormalMap')
        BumpMap = nodes.new('ShaderNodeBump')
        NormalMap.inputs[0].default_value = random.uniform(0.8,1)
        
        # What to link here? 
        mat.node_tree.links.new( texImagediff.outputs[0], mixRGB.inputs[2] )
        mat.node_tree.links.new( texImagediff.outputs[1], principled.inputs[21] )
        mat.node_tree.links.new( mixRGB.outputs[0], principled.inputs[0] )
        
        mat.node_tree.links.new( texImagenorm.outputs[0], NormalMap.inputs[1])
        mat.node_tree.links.new( NormalMap.outputs[0], BumpMap.inputs[3])
        mat.node_tree.links.new( BumpMap.outputs[0], principled.inputs[22])
        # Assign it to object
        if obj.data.materials:
            obj.data.materials[0] = mat
        else:
            obj.data.materials.append(mat)
        
        return obj


def SunGlasses():
        l=[]
        csv_path = os.path.join(parent_dir,"txt/SunGlasses.txt")
        # Ouvrir le fichier CSV
        with open(csv_path, newline='') as csvfile:
            reader =csv.reader(csvfile, delimiter=',', quotechar='"')
            # Parcourir chaque ligne du fichier CSV
            for row in reader:
                # Récupérer les données de chaque colonne
                l.append(row)
        l= l[1:]
        l= np.array(l)
        chosen_Param = random.choice(l)
        chosen_File = chosen_Param[0]
        Hair_name = chosen_Param[1]
        localisation = (float(chosen_Param[2]),float(chosen_Param[3]),float(chosen_Param[4]))
        scale = (float(chosen_Param[5]),float(chosen_Param[6]),float(chosen_Param[7]))
        
        rotation = bpy.data.objects['FBHead'].rotation_euler.copy()
        bpy.data.objects['FBHead'].rotation_euler = (0,0,0)
        path = Path(os.path.join(parent_dir,"Hair2/makehuman_system_assets_cc0/mask/"))
        filepath = str(path) + "/"+chosen_File + "/" + Hair_name+".obj"
        bpy.ops.wm.obj_import(filepath=filepath)
        a = bpy.data.objects[Hair_name]
        bpy.context.view_layer.objects.active = a
        bpy.ops.object.origin_set(type='GEOMETRY_ORIGIN', center='MEDIAN')
        a.rotation_euler[2] = math.radians(-90)
        bpy.ops.object.transform_apply(location=False, rotation=True, scale=False)
        bpy.ops.object.modifier_add(type='SUBSURF')
        bpy.context.object.modifiers["Subdivision"].render_levels = 3
        a.location = localisation
        a.scale = scale
        
        a.rotation_euler = bpy.data.objects['FBHead'].rotation_euler
        bpy.ops.object.constraint_add(type='CHILD_OF')
        bpy.context.object.constraints["Child Of"].target = bpy.data.objects["FBHead"]
        bpy.ops.object.constraint_add(type='COPY_ROTATION')
        bpy.context.object.constraints["Copy Rotation"].target = bpy.data.objects["FBHead"]
        bpy.data.objects['FBHead'].rotation_euler = rotation
        
        
        #path = Path.home() / "Documents/Synthetic_data/Hair2/makehuman_system_assets_cc0/mask/"
        
        
        texturediff_path = str(path) + "/" + chosen_File + "/" + Hair_name + "_diffuse.png" 
        
        obj  = a 
        mat = bpy.data.materials.new(name='texture_'+obj.name)
        mat.use_nodes = True
        nodes = mat.node_tree.nodes
        #
        texImagediff = nodes.new('ShaderNodeTexImage')
        texImagediff.image = bpy.data.images.load(texturediff_path)
        #
        
        mixRGB = nodes.new('ShaderNodeMixRGB')
        mixRGB.inputs[0].default_value = random.uniform(0.75,0.95)
        mixRGB.inputs[1].default_value = (random.random(), random.random(), random.random(), 1)

        principled = nodes['Principled BSDF']
        principled.inputs[9].default_value = 0.9

        
        # What to link here? 
        mat.node_tree.links.new( texImagediff.outputs[0], mixRGB.inputs[2] )
        mat.node_tree.links.new( texImagediff.outputs[1], principled.inputs[21] )
        mat.node_tree.links.new( mixRGB.outputs[0], principled.inputs[0] )
        
        # Assign it to object
        if obj.data.materials:
            obj.data.materials[0] = mat
        else:
            obj.data.materials.append(mat)
        
        return obj
    
    
def beard():
        l=[]
        csv_path = os.path.join(parent_dir,"txt/beard.txt")
        # Ouvrir le fichier CSV
        with open(csv_path, newline='') as csvfile:
            reader =csv.reader(csvfile, delimiter=',', quotechar='"')
            # Parcourir chaque ligne du fichier CSV
            for row in reader:
                # Récupérer les données de chaque colonne
                l.append(row)
        l= l[1:]
        l= np.array(l)
        chosen_Param = random.choice(l)
        chosen_File = chosen_Param[0]
        Hair_name = chosen_Param[1]
        localisation = (float(chosen_Param[2]),float(chosen_Param[3]),float(chosen_Param[4]))
        scale = (float(chosen_Param[5]),float(chosen_Param[6]),float(chosen_Param[7]))
        
        rotation = bpy.data.objects['FBHead'].rotation_euler.copy()
        bpy.data.objects['FBHead'].rotation_euler = (0,0,0)
        path = Path(os.path.join(parent_dir,"Hair2/makehuman_system_assets_cc0/beard/"))
        filepath = str(path) + "/"+chosen_File + "/" + Hair_name+".obj"
        bpy.ops.wm.obj_import(filepath=filepath)
        a = bpy.data.objects[Hair_name]
        bpy.context.view_layer.objects.active = a
        bpy.ops.object.origin_set(type='GEOMETRY_ORIGIN', center='MEDIAN')
        a.rotation_euler[2] = math.radians(-90)
        bpy.ops.object.transform_apply(location=False, rotation=True, scale=False)
        bpy.ops.object.modifier_add(type='SUBSURF')
        bpy.context.object.modifiers["Subdivision"].render_levels = 3
        a.location = localisation
        a.scale = scale
        
        a.rotation_euler = bpy.data.objects['FBHead'].rotation_euler
        bpy.ops.object.constraint_add(type='CHILD_OF')
        bpy.context.object.constraints["Child Of"].target = bpy.data.objects["FBHead"]
        bpy.ops.object.constraint_add(type='COPY_ROTATION')
        bpy.context.object.constraints["Copy Rotation"].target = bpy.data.objects["FBHead"]
        bpy.data.objects['FBHead'].rotation_euler = rotation
        
        
        #path = Path.home() / "Documents/Synthetic_data/Hair2/makehuman_system_assets_cc0/beard/"
        
        texturenorm_path = str(path) + "/" + chosen_File + "/" + Hair_name + "_normal.png"
        texturediff_path = str(path) + "/" + chosen_File + "/" + Hair_name + "_diffuse.png" 
        
        obj  = a 
        mat = bpy.data.materials.new(name='texture_'+obj.name)
        mat.use_nodes = True
        nodes = mat.node_tree.nodes
        #
        texImagediff = nodes.new('ShaderNodeTexImage')
        texImagediff.image = bpy.data.images.load(texturediff_path)
        #
        
        mixRGB = nodes.new('ShaderNodeMixRGB')
        mixRGB.inputs[0].default_value = random.uniform(0.8,1)
        mixRGB.inputs[1].default_value = (random.random(), random.random(), random.random(), 1)

        principled = nodes['Principled BSDF']
        principled.inputs[9].default_value = 0.9
        
        texImagenorm = nodes.new('ShaderNodeTexImage')
        texImagenorm.image = bpy.data.images.load(texturenorm_path)
        bpy.data.images[ Path(texturenorm_path).name].colorspace_settings.name = 'Non-Color'
        
        NormalMap = nodes.new('ShaderNodeNormalMap')
        BumpMap = nodes.new('ShaderNodeBump')
        NormalMap.inputs[0].default_value = random.uniform(0.8,1)
        
        # What to link here? 
        mat.node_tree.links.new( texImagediff.outputs[0], mixRGB.inputs[2] )
        mat.node_tree.links.new( texImagediff.outputs[1], principled.inputs[21] )
        mat.node_tree.links.new( mixRGB.outputs[0], principled.inputs[0] )
        
        mat.node_tree.links.new( texImagenorm.outputs[0], NormalMap.inputs[1])
        mat.node_tree.links.new( NormalMap.outputs[0], BumpMap.inputs[3])
        mat.node_tree.links.new( BumpMap.outputs[0], principled.inputs[22])
        # Assign it to object
        if obj.data.materials:
            obj.data.materials[0] = mat
        else:
            obj.data.materials.append(mat)
        
        return obj


if __name__ == "__main__":
    #SunGlasses()    
    #beard()    
    Hat()
    #Maskk()
    
