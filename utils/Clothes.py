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


def hair_Model():
        def add_texture(texture_path, obj):
            mat = bpy.data.materials.new(name='HairMaterial')
            mat.use_nodes = True
            nodes = mat.node_tree.nodes
            
            texImage = nodes.new('ShaderNodeTexImage')
            texImage.image = bpy.data.images.load(texture_path)
            
            
            mixRGB = nodes.new('ShaderNodeMixRGB')
            mixRGB.inputs[0].default_value = 0.4
            mixRGB.inputs[1].default_value = (random.random(), random.random(), random.random(), 1)
            mixRGB.inputs[2].default_value = (random.random(), random.random(), random.random(), 1)


            principled = nodes['Principled BSDF']
            principled.inputs[9].default_value = 1
            principled.inputs[0].default_value=(random.random(), random.random(), random.random(), 1)
            
            Transparent = nodes.new('ShaderNodeBsdfTransparent')
            Transparent.inputs[0].default_value = (0, 0, 0, 1)
            
            MixShader = nodes.new('ShaderNodeMixShader')
            MixShader.inputs[0].default_value = bpy.data.materials["FBHead_preview_mat"].node_tree.nodes["Mix Shader"].inputs[0].default_value 

            Output =  nodes['Material Output']
            
            # What to link here? 
            mat.node_tree.links.new( principled.outputs[0], MixShader.inputs[1] )
            mat.node_tree.links.new( Transparent.outputs[0], MixShader.inputs[2] )
            mat.node_tree.links.new( MixShader.outputs[0], Output.inputs[0] )
            mat.node_tree.links.new( mixRGB.outputs[0], principled.inputs[0] )
            # Assign it to object
            if obj.data.materials:
                obj.data.materials[0] = mat
            else:
                obj.data.materials.append(mat)
                
                
        l=[]
        # Chemin vers le fichier CSV   x=z_t, y=x_t , z=y_t
        
        csv_path = os.path.join(parent_dir,"txt/HairGaze.txt")
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
        # Loading hair model
        path = os.path.join(parent_dir,"Hair2/makehuman_system_assets_cc0/hair/")
        filepath = str(path) + "/"+chosen_File + "/" + Hair_name+".obj"
        bpy.ops.wm.obj_import(filepath=filepath)
        a = bpy.data.objects[Hair_name]
        bpy.context.view_layer.objects.active = a
        bpy.ops.object.modifier_add(type='SUBSURF')
        #bpy.context.object.modifiers["Subdivision"].levels = 4
        bpy.context.object.modifiers["Subdivision"].render_levels = 4
        bpy.ops.object.origin_set(type='GEOMETRY_ORIGIN', center='MEDIAN')
        a.location = localisation
        a.scale = scale
        a.rotation_euler[2] = math.radians(-90)
        bpy.context.view_layer.objects.active = a
        bpy.ops.object.transform_apply(location=False, rotation=True, scale=False)
        a.rotation_euler = bpy.data.objects['FBHead'].rotation_euler
        bpy.ops.object.constraint_add(type='CHILD_OF')
        bpy.context.object.constraints["Child Of"].target = bpy.data.objects["FBHead"]
        bpy.ops.object.constraint_add(type='COPY_ROTATION')
        bpy.context.object.constraints["Copy Rotation"].target = bpy.data.objects["FBHead"]
        bpy.data.objects['FBHead'].rotation_euler = rotation

        if(random.randint(0,0)):
            file_path = os.path.join(parent_dir,"WithoutTracking/HairMat_Node.blend")
            inner_path = 'Material'
            object_name = 'HairMaterial'
            bpy.ops.wm.append(
                filepath=os.path.join(file_path, inner_path, object_name),
                directory=os.path.join(file_path, inner_path),
                filename=object_name
                )
            a.data.materials.append( bpy.data.materials['HairMaterial'])
            bpy.data.materials["HairMaterial"].node_tree.nodes["ColorRamp"].color_ramp.elements[1].color = (random.random(), random.random(), random.random(), 1)
        else:
            if(0):
                l=Path(os.path.join(parent_dir,"Hair2/hair02_ccby/texture"))
                l= [str(f) for f in l.glob("*")]
                add_texture(l[random.randint(0,len(l)-1)], a)
            else:
                path = Path(os.path.join(parent_dir,"Hair2/makehuman_system_assets_cc0/hair/"))
        
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
            mixRGB.inputs[0].default_value = random.uniform(0.95,1)
            mixRGB.inputs[1].default_value = (random.random(), random.random(), random.random(), 1)

            principled = nodes['Principled BSDF']
            principled.inputs[9].default_value = 0.9
            
            texImagenorm = nodes.new('ShaderNodeTexImage')
            texImagenorm.image = bpy.data.images.load(texturenorm_path)
            bpy.data.images[ Path(texturenorm_path).name].colorspace_settings.name = 'Non-Color'
            
            NormalMap = nodes.new('ShaderNodeNormalMap')
            BumpMap = nodes.new('ShaderNodeBump')
            
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
        return a
    

def Clothes_Model():
        l=[]
        csv_path = os.path.join(parent_dir,"txt/clothes.txt")
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
        path = os.path.join(parent_dir,"Hair2/makehuman_system_assets_cc0/clothes/")
        filepath = str(path) + "/"+chosen_File + "/" + Hair_name+".obj"
        bpy.ops.wm.obj_import(filepath=filepath)
        a = bpy.data.objects[Hair_name]
        bpy.context.view_layer.objects.active = a
        bpy.ops.object.modifier_add(type='SUBSURF')
        bpy.context.object.modifiers["Subdivision"].render_levels = 3
        a.location = localisation
        a.scale = scale
        a.rotation_euler[2] = math.radians(-90)
        bpy.ops.object.transform_apply(location=False, rotation=True, scale=False)
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
        mixRGB.inputs[0].default_value = random.uniform(0.8,1)
        mixRGB.inputs[1].default_value = (random.random(), random.random(), random.random(), 1)

        principled = nodes['Principled BSDF']
        principled.inputs[9].default_value = 0.9
        
        texImagenorm = nodes.new('ShaderNodeTexImage')
        texImagenorm.image = bpy.data.images.load(texturenorm_path)
        bpy.data.images[ Path(texturenorm_path).name].colorspace_settings.name = 'Non-Color'
        
        NormalMap = nodes.new('ShaderNodeNormalMap')
        BumpMap = nodes.new('ShaderNodeBump')
        
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
    
def Mask():
        path = os.path.join(parent_dir,"WithoutTracking")
        filepath = str(path) +"/Mask.obj"
        bpy.ops.wm.obj_import(filepath=filepath)
        
        rotation = bpy.data.objects['FBHead'].rotation_euler.copy()
        bpy.data.objects['FBHead'].rotation_euler = (0,0,0)

        bpy.data.objects['Mask'].location = Vector((1.36, -0.3416078984737396, 1.00064218044281))
        bpy.data.objects['Mask'].scale = Vector((0.11020000278949738, 0.12020000070333481, 0.115020000070333481))
        bpy.data.objects['Mask'].rotation_euler[2] = math.radians(-90)
        bpy.ops.object.transform_apply(location=False, rotation=True, scale=False)
        bpy.data.objects['Mask'].rotation_euler = bpy.data.objects['FBHead'].rotation_euler
        bpy.ops.object.constraint_add(type='CHILD_OF')
        bpy.context.object.constraints["Child Of"].target = bpy.data.objects["FBHead"]
        bpy.ops.object.constraint_add(type='COPY_ROTATION')
        bpy.context.object.constraints["Copy Rotation"].target = bpy.data.objects["FBHead"]
        bpy.data.objects['FBHead'].rotation_euler = rotation
        
        #bpy.data.materials["Material.001"].node_tree.nodes["Principled BSDF"].inputs[0].default_value = (random.random(), random.random(), random.random(), 1)
        bpy.data.materials["Material"].node_tree.nodes["Principled BSDF"].inputs[9].default_value = 1
        bpy.data.materials["Material"].node_tree.nodes["Principled BSDF"].inputs[0].default_value = (random.random(), random.random(), random.random(), 1)
        
        
        mat =  bpy.data.materials["Material.001"]
        mat.use_nodes = True
        nodes = mat.node_tree.nodes
        
        principled = nodes['Principled BSDF']
        principled.inputs[9].default_value = 1
        principled.inputs[0].default_value=(random.random(), random.random(), random.random(), 1)
        
        Transparent = nodes.new('ShaderNodeBsdfTransparent')
        Transparent.inputs[0].default_value = (0, 0, 0, 1)
        
        MixShader = nodes.new('ShaderNodeMixShader')
        MixShader.inputs[0].default_value = random.random()
        Output =  nodes['Material Output']
        
        mat.node_tree.links.new( principled.outputs[0], MixShader.inputs[1] )
        mat.node_tree.links.new( Transparent.outputs[0], MixShader.inputs[2] )
        mat.node_tree.links.new( MixShader.outputs[0], Output.inputs[0] )

        
        return bpy.data.objects['Mask']
    

if __name__ == "__main__":
    #hair_Model()
    Clothes_Model()
