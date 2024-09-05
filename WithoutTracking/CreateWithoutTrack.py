import bpy
import bmesh
import numpy as np
import os
import math
from math import *



def sphereFit(spX,spY,spZ):
    #   Assemble the A matrix
    spX = np.array(spX)
    spY = np.array(spY)
    spZ = np.array(spZ)
    A = np.zeros((len(spX),4))
    A[:,0] = spX*2
    A[:,1] = spY*2
    A[:,2] = spZ*2
    A[:,3] = 1



   #   Assemble the f matrix
    f = np.zeros((len(spX),1))
    f[:,0] = (spX*spX) + (spY*spY) + (spZ*spZ)
    C, residules, rank, singval = np.linalg.lstsq(A,f,rcond=None)



   #   solve for the radius
    t = (C[0]*C[0])+(C[1]*C[1])+(C[2]*C[2])+C[3]
    radius = math.sqrt(t)
    return radius, C[0], C[1], C[2]



def add_texture(texture_path, obj):
    mat = bpy.data.materials.new(name='texture')
    mat.use_nodes = True
    nodes = mat.node_tree.nodes



    texImage = nodes.new('ShaderNodeTexImage')
    texImage.image = bpy.data.images.load(texture_path)



    principled = nodes['Principled BSDF']
    principled.inputs[9].default_value = 0.122727



   # What to link here?
    
    mat.node_tree.links.new( texImage.outputs[0], principled.inputs[0] )



   # Assign it to object
    if obj.data.materials:
        obj.data.materials[0] = mat
    else:
        obj.data.materials.append(mat)


#leftIdx = np.array((10022, 10049, 10087, 10094, 10123, 10187, 10188, 10215, 10261, 10277, 10279, 10282, 10290, 10292, 10311, 10312, 10313, 10341, 10342, 10352, 10375, 17843, 17845, 17846, 17848, 17849, 17855, 17856, 17860, 17863, 17864, 17865, 17866, 17867, 17873, 17875, 17879, 17880, 17882, 17884, 17888, 17892, 17893, 17894, 17899, 17900, 17903, 17904, 17907))
#rightIdx = np.array((9900, 9907, 9910, 9915, 9939, 9961, 9963, 9967, 9968, 10045, 10048, 10060, 10061, 10112, 10118, 10142, 10143, 10153, 10155, 10177, 10181, 17931, 17934, 17941, 17942, 17944, 17945, 17950, 17951, 17952, 17953, 17954, 17959, 17965, 17967, 17971, 17972, 17975, 17977, 17979, 17982, 17983, 17990, 17992, 17994, 17995, 17999, 18003, 18006))

######## for this new head
leftI =np.array((10022, 10049, 10094, 10123, 10188, 10215, 10277, 10279, 10290, 10292, 10311, 10312, 10313, 10341, 10375, 17860, 17864, 17865, 17866, 17873, 17875, 17879, 17882, 17884, 17888, 17894, 17899, 17900, 17903, 17904))
rightI = np.array((9900, 9907, 9915, 9939, 9961, 10045, 10048, 10060, 10061, 10112, 10118, 10142, 10155, 10177, 10181, 17931, 17941, 17944, 17945, 17950, 17951, 17952, 17953, 17954, 17959, 17972, 17975, 17977, 17979, 17983))
###########

obj = bpy.data.objects['FBHead']
depsgraph = bpy.context.evaluated_depsgraph_get()
obj_eval = obj.evaluated_get(depsgraph)
mesh = obj_eval.to_mesh()
mesh.transform(obj_eval.matrix_world)

# selecting all mesh
x = np.array([ v.co[0] for v in mesh.vertices])
y = np.array([ v.co[1] for v in mesh.vertices])
z = np.array([ v.co[2] for v in mesh.vertices])


# filtering eyes mesh
lx = x[leftI]
ly = y[leftI]
lz = z[leftI]


rx = x[rightI]
ry = y[rightI]
rz = z[rightI]



res = 64
rr,cxr,cyr,czr = sphereFit(rx,ry,rz)
print("%f %f %f %f" % (rr,cxr,cyr,czr))

bpy.ops.mesh.primitive_uv_sphere_add(segments=res*2,ring_count=res,radius=rr*1.04,location=((cxr+cxr)/2,cyr,(czr+czr)/2))
bpy.context.object.name = 'Right Eye'
obj = bpy.context.object

add_texture( "/home/renault/Documents/Apprenticeship/blender/EyeTextures/greenEye.png", obj )


rl,cxl,cyl,czl = sphereFit(lx,ly,lz)
print("%f %f %f %f" % (rl,cxl,cyl,czl))
bpy.ops.mesh.primitive_uv_sphere_add(segments=res*2,ring_count=res,radius=rl*1.04,location=((cxl+cxl)/2,cyl,(czl+czl)/2))
bpy.context.object.name = 'Left Eye'
obj = bpy.context.object
add_texture( "/home/renault/Documents/Apprenticeship/blender/EyeTextures/greenEye.png", obj )

bpy.data.objects['Right Eye'].rotation_euler = (0, 0.0, radians(-5))
bpy.data.objects['Left Eye'].rotation_euler = (radians(0.5), 0.0, radians(5))
#bpy.ops.object.constraint_add(type='COPY_ROTATION')
#bpy.context.object.constraints["Copy Rotation"].target = bpy.data.objects["Right Eye"]


bpy.data.objects['Right Eye'].parent = bpy.data.objects['FBHead']
bpy.data.objects['Left Eye'].parent = bpy.data.objects['FBHead']

