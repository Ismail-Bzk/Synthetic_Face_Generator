from math import *
import math
from mathutils import Matrix
from mathutils import *
import bpy
import bpy_extras
from bpy.props import StringProperty, IntProperty, BoolProperty
from bpy_extras.io_utils import ExportHelper
import numpy as np
import random
from pathlib import Path
import os
import csv
import sys


# For eyeblinking


def Init_csv():    
    scene = bpy.context.scene
    D=bpy.data
    obj=D.objects['FBHead']
    cam=D.objects['STFOX']
    bpy.context.scene.camera = cam
    BShapesName= ([i.name for i in bpy.data.shape_keys["Key"].key_blocks])
    #Eye_mouth = [BShapesName[1],BShapesName[2],BShapesName[20],BShapesName[21],BShapesName[31],BShapesName[32]]
    Eye_Blend = BShapesName[1:3]
    row = ["frame"] +Eye_Blend
    return row

def Write_In_Csv(frame,csv_writer):
    BShapesName= ([i.name for i in bpy.data.shape_keys["Key"].key_blocks])
    #Eye_mouth = [BShapesName[1],BShapesName[2],BShapesName[20],BShapesName[21],BShapesName[31],BShapesName[32]]
    #Eye_mouth = BShapesName[1:5]+BShapesName[20:21]
    Eye_Blend = [BShapesName[1],BShapesName[2]]
    #ShapesValue = [bpy.data.shape_keys["Key"].key_blocks[i].value for i in Eye_Blend]
    ShapesValue = [min(1,(bpy.data.shape_keys["Key"].key_blocks[BShapesName[i]].value  +0.3*(bpy.data.shape_keys["Key"].key_blocks[BShapesName[i+2]].value))) for i in range(1,3)]
    rowI = [frame] + ShapesValue
    csv_writer.writerow(rowI)
    
def Write_In_CsvALL(csv_writer):
    res1 =[467, 11774, 4600, 6525, 7531, 5925, 7261, 6732, 9282, 9596, 9533, 9475, 8826, 8050, 4299, 12283, 2070, 76, 462, 2813, 3570, 2853, 1010, 1005, 4110, 575, 3403, 5623, 5400, 5674, 5722, 5077, 5075, 5721, 4723, 4644, 1252, 3437, 3101, 9917, 10120, 10052, 9955, 1067, 3019, 870, 10349, 10297, 6831, 7635, 7831, 8884, 8070, 6418, 9411, 9406, 9478, 9167, 5927, 7902, 7244, 5936, 9178, 9472, 9194, 9446, 9312, 5885]
    BShapesName= ([i.name for i in bpy.data.shape_keys["Key"].key_blocks])
    #Eye_mouth = [BShapesName[1],BShapesName[2],BShapesName[20],BShapesName[21],BShapesName[31],BShapesName[32]]
    #Eye_mouth = BShapesName[1:5]+BShapesName[20:21]
    Eye_Blend = [BShapesName[1],BShapesName[2],BShapesName[20]]
    depsgraph = bpy.context.evaluated_depsgraph_get()
    obj =bpy.data.objects['FBHead']
    obj_eval = obj.evaluated_get(depsgraph)
    mesh = obj_eval.to_mesh()
    matrix = cam.matrix_world.normalized().inverted()
    mesh.transform(obj.matrix_world)
    XX = np.array([v.co[0] for v in mesh.vertices])
    YY = np.array([v.co[1] for v in mesh.vertices])
    ZZ = np.array([v.co[2] for v in mesh.vertices])
    mesh.transform(matrix)
    
    # Getting 2D dlib in camera reference   
    coW = [Vector((XX[i],YY[i],ZZ[i])) for i in res1]
    coords_2d = [bpy_extras.object_utils.world_to_camera_view(scene, cam, coord) for coord in coW]
    # If you want pixel coords
    render_scale = scene.render.resolution_percentage / 100
    render_size = (
        int(scene.render.resolution_x * render_scale),
        int(scene.render.resolution_y * render_scale),
    )
    Pixels = [[(i.x * render_size[0]),(render_size[1] - i.y * render_size[1])] for i in coords_2d]
    Pixels=np.array(Pixels)
    Pix = []
    for i in range(len(Pixels)):
        Pix.append(Pixels[i][0])
        Pix.append(Pixels[i][1])
    
    #ShapesValue = [bpy.data.shape_keys["Key"].key_blocks[i].value for i in Eye_Blend]
    ShapesValue = [min(1,(bpy.data.shape_keys["Key"].key_blocks[BShapesName[i]].value  +0.3*(bpy.data.shape_keys["Key"].key_blocks[BShapesName[i+2]].value))) for i in range(1,3)]
    rowI = Pix+ShapesValue +[bpy.data.shape_keys["Key"].key_blocks[Eye_Blend[-1]].value]
    csv_writer.writerow(rowI)




def Init_csvAll():    
    scene = bpy.context.scene
    D=bpy.data
    obj=D.objects['FBHead']
    cam=D.objects['STFOX']
    bpy.context.scene.camera = cam
    res1 =[467, 11774, 4600, 6525, 7531, 5925, 7261, 6732, 9282, 9596, 9533, 9475, 8826, 8050, 4299, 12283, 2070, 76, 462, 2813, 3570, 2853, 1010, 1005, 4110, 575, 3403, 5623, 5400, 5674, 5722, 5077, 5075, 5721, 4723, 4644, 1252, 3437, 3101, 9917, 10120, 10052, 9955, 1067, 3019, 870, 10349, 10297, 6831, 7635, 7831, 8884, 8070, 6418, 9411, 9406, 9478, 9167, 5927, 7902, 7244, 5936, 9178, 9472, 9194, 9446, 9312, 5885]
    BShapesName= ([i.name for i in bpy.data.shape_keys["Key"].key_blocks])
    #Eye_mouth = [BShapesName[1],BShapesName[2],BShapesName[20],BShapesName[21],BShapesName[31],BShapesName[32]]
    Eye_Blend = BShapesName[1:3] 

    Dlib = ["Dlib%d"% (i+1) for i in range(len(res1))]
    # 1ère colonne contenant les étiquettes

    pix = []
    pix_x = ["Pix%d.x"% (i+1) for i in range(len(res1))]
    pix_y = ["Pix%d.y"% (i+1) for i in range(len(res1))]
    for i in range(len(res1)):
        pix.append(pix_x[i])
        pix.append(pix_y[i])
        

    row =  pix+Eye_Blend
    return row




