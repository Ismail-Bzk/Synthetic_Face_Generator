import os
import bpy
from bpy.props import StringProperty, IntProperty, BoolProperty
from bpy_extras.io_utils import ExportHelper


def write_anim(filepath, frame_start, frame_end):
    fw = open(filepath, 'w').write
    fw("object,frame,posx,posy,posz,scalex,scaley,scalez,roll,pitch,yaw\n")
    frame_range = range(frame_start, frame_end + 1)
    for obj in bpy.context.selected_objects:
        for f in frame_range:
            bpy.context.scene.frame_set(f)
            matrix = obj.matrix_world.copy()
            posx, posy, posz = matrix.to_translation()[:]
            scalex, scaley, scalez = matrix.to_scale()[:]
            roll, pitch, yaw = matrix.to_euler()[:]
            fw("%s, %d, %r, %r, %r, %r, %r, %r, %r, %r, %r\n"
                % (obj.name, f, posx,posy,posz, scalex,scaley,scalez, roll,pitch,yaw))


#filepath = "/home/renault/Documents/Apprenticeship/blender/fw.csv"
filepath = '/home/renault/Téléchargements/WithoutTracking/WithoutTracking.cvs' 

frame_start = 1
frame_end = 185

write_anim( filepath, frame_start, frame_end)