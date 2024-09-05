import bpy
import bpy_extras
import bmesh
import numpy as np
import os
import math
from mathutils import *
from math import *
from bpy.props import StringProperty, IntProperty, BoolProperty
from bpy_extras.io_utils import ExportHelper



def VertexCoordinates(a,obj):
    depsgraph = bpy.context.evaluated_depsgraph_get()
    obj_eval = obj.evaluated_get(depsgraph)
    mesh = obj_eval.to_mesh()
    mesh.transform(obj_eval.matrix_world)
    XX = np.array([v.co[0] for v in mesh.vertices])
    YY = np.array([v.co[1] for v in mesh.vertices])
    ZZ = np.array([v.co[2] for v in mesh.vertices])
    return Vector((XX[a],YY[a],ZZ[a]))

def LeftEyeP():
    obj = bpy.data.objects['FBHead']
    depsgraph = bpy.context.evaluated_depsgraph_get()
    obj_eval = obj.evaluated_get(depsgraph)
    mesh = obj_eval.to_mesh()
    mesh.transform(obj_eval.matrix_world)
    XX = np.array([v.co[0] for v in mesh.vertices])
    YY = np.array([v.co[1] for v in mesh.vertices])
    ZZ = np.array([v.co[2] for v in mesh.vertices])
    return [XX[17866],YY[17866],ZZ[17866]]

def RightEyeP():
    obj = bpy.data.objects['FBHead']
    depsgraph = bpy.context.evaluated_depsgraph_get()
    obj_eval = obj.evaluated_get(depsgraph)
    mesh = obj_eval.to_mesh()
    mesh.transform(obj_eval.matrix_world)
    XX = np.array([v.co[0] for v in mesh.vertices])
    YY = np.array([v.co[1] for v in mesh.vertices])
    ZZ = np.array([v.co[2] for v in mesh.vertices])
    index = [9900,9915,10155,10177,17952,17959]
    return np.mean([XX[index],YY[index],ZZ[index]],axis=1)
    

def MapPointToMesh(a,obj):
    depsgraph = bpy.context.evaluated_depsgraph_get()
    obj_eval = obj.evaluated_get(depsgraph)
    mesh = obj_eval.to_mesh()
    mesh.transform(obj_eval.matrix_world)
    XX = np.array([v.co[0] for v in mesh.vertices])
    YY = np.array([v.co[1] for v in mesh.vertices])
    ZZ = np.array([v.co[2] for v in mesh.vertices])
    
    Index = np.array([i.index for i in obj.data.vertices ])
    Index_filtered = (Index[3300:4800]).tolist()
    Verts = [Vector((XX[i],YY[i],ZZ[i])) for i in range(len(XX))]
    Verts_filtered = (Verts[3300:4800])
    distance = [ dist(a[1:],i[1:]) for i in Verts_filtered ]
    return  Index_filtered[distance.index(min(distance))],Verts_filtered[distance.index(min(distance))]
    
        
def Writetxt(R_eye_index,L_eye_index):
    if(0):
        R_eye= RightEyeP()
        R_eye_index,R_eye_co = MapPointToMesh(R_eye,bpy.data.objects['Right Eye'])
        L_eye= LeftEyeP()
        L_eye_index,L_eye_co = MapPointToMesh(L_eye,bpy.data.objects['Left Eye'])
        
    scene = bpy.context.scene
    D=bpy.data
    cam=D.objects['STFOX']
    bpy.context.scene.camera = cam
    
    R_eye_co = VertexCoordinates(R_eye_index,bpy.data.objects['Right Eye'])
    L_eye_co= VertexCoordinates(L_eye_index,bpy.data.objects['Left Eye'])
    coW = [R_eye_co,L_eye_co]
    coords_2d = [bpy_extras.object_utils.world_to_camera_view(scene, cam, coord) for coord in coW]
    #Pixel
    render_scale = scene.render.resolution_percentage / 100
    render_size = (
        int(scene.render.resolution_x * render_scale),
        int(scene.render.resolution_y * render_scale),
    )
    Pixels = np.array([[(i.x * render_size[0]),(render_size[1] - i.y * render_size[1])] for i in coords_2d])
    visibility = np.zeros(len(coW))
    depsgraph = bpy.context.evaluated_depsgraph_get()
    for index in range(len(coW)):
        end=coW[index]
        start = cam.location
        dir = end-start
        dir.normalize()
        hit, loc, normal, ind, ob, m = bpy.context.scene.ray_cast(depsgraph,start,dir)
        visible = hit & ((loc-end).length<10e-3)
        visibility[index]=visible
        
    return Pixels,visibility
    
    
    
if __name__ == "__main__":
    scene = bpy.context.scene
    D=bpy.data
    cam=D.objects['STFOX']
    bpy.context.scene.camera = cam
    R_eye= RightEyeP()
    R_eye_index,R_eye_co = MapPointToMesh(R_eye,bpy.data.objects['Right Eye'])
    L_eye= LeftEyeP()
    L_eye_index,L_eye_co = MapPointToMesh(L_eye,bpy.data.objects['Left Eye'])
    print("index ",R_eye_index,L_eye_index)
    
    Pupils_pixel_x,Pupils_visibility = Writetxt(R_eye_index,L_eye_index)
    for (i) in range(len(Pupils_pixel_x)):
        print(Pupils_pixel_x[i],Pupils_visibility[i])
        

"""
a= RightEyeP()
index = MapPointToMesh(a,bpy.data.objects['Right Eye'])
print("Right Eye index: ",index)

b= LeftEyeP()
index = MapPointToMesh(b,bpy.data.objects['Left Eye'])
print("Left Eye index: ",index)
"""