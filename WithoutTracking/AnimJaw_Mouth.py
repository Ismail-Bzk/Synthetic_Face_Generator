import bpy
from math import *
from mathutils import *
import bpy_extras
from bpy.props import StringProperty, IntProperty, BoolProperty
from bpy_extras.io_utils import ExportHelper
import numpy as np
import random
import os


class MyAnimMouth():
    def __init__(self):
        self.Eye_Right= np.linspace(0.1,1,6)
        self.Eye_Left= np.linspace(0.1,1,6)
        scene = bpy.context.scene
        bpy.context.scene.frame_start = 0
        bpy.context.view_layer.objects.active = bpy.data.objects['FBHead']
        ob = bpy.context.active_object
        ob.active_shape_key_index=1
        bpy.data.shape_keys["Key.001"].key_blocks["eyeBlinkLeft"].value = 0
        ob.active_shape_key_index=2
        bpy.data.shape_keys["Key.001"].key_blocks["eyeBlinkRight"].value = 0
        ob.active_shape_key_index=20
        bpy.data.shape_keys["Key.001"].key_blocks["jawOpen"].value = 0
        ob.active_shape_key_index=21
        bpy.data.shape_keys["Key.001"].key_blocks["jawOpen"].value = 0
        ob.active_shape_key.keyframe_insert(data_path='value', frame=0)
        frame = 0
        BlinkL = self.Eye_Left
        for (BL) in (BlinkL):
            MClouse = np.linspace(0,BL,6)
            for (MC) in (MClouse):
                scene.frame_set(frame)
                bpy.context.view_layer.objects.active = bpy.data.objects['FBHead']
                ob = bpy.context.active_object
                ob.active_shape_key_index=20
                bpy.data.shape_keys["Key.001"].key_blocks["jawOpen"].value = BL
                ob.active_shape_key.keyframe_insert(data_path='value')
                ob.active_shape_key_index=21
                bpy.data.shape_keys["Key.001"].key_blocks["mouthClose"].value = MC
                ob.active_shape_key.keyframe_insert(data_path='value')
                frame = frame +1

        bpy.context.scene.frame_end = frame-1
        scene.frame_set(0)
MyAnimMouth()