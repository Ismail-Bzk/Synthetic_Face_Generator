# New animation taking in consideration the new stabilisation for eyes
import bpy
from math import *

bpy.context.scene.frame_start = 0
bpy.context.scene.frame_end = 185


bpy.context.view_layer.objects.active = bpy.data.objects['Right Eye']
ob = bpy.context.active_object
frame_num = 0
positionsR0 = [0, 0.0, radians(-5)]
ob.rotation_euler = positionsR0
ob.keyframe_insert(data_path='rotation_euler', frame= frame_num)

bpy.context.view_layer.objects.active = bpy.data.objects['Left Eye']
ob = bpy.context.active_object
positionsL0 = [radians(0.5), 0.0, radians(5)]
ob.rotation_euler = positionsL0
ob.keyframe_insert(data_path='rotation_euler', frame= frame_num)

#########################################################################################

bpy.context.view_layer.objects.active = bpy.data.objects['Right Eye']
ob = bpy.context.active_object
positionsR1 = positionsR0
positionsR1[2]= positionsR1[2] +radians(15)
ob.rotation_euler = positionsR1
ob.keyframe_insert(data_path='rotation_euler', frame= frame_num+40)
ob.rotation_euler = positionsR1
ob.keyframe_insert(data_path='rotation_euler', frame= frame_num+50)


bpy.context.view_layer.objects.active = bpy.data.objects['Left Eye']
ob = bpy.context.active_object
positionsL1 = positionsL0
positionsL1[2]= positionsL1[2]+radians(20)
positionsL1[0]= positionsL1[0] +radians(2.5)
#positionsL1 =[10.2595 , -19.200000762939453, -0.5219443440437317]
ob.rotation_euler = positionsL1
ob.keyframe_insert(data_path='rotation_euler', frame= frame_num+40)
ob.rotation_euler = positionsL1
ob.keyframe_insert(data_path='rotation_euler', frame= frame_num+50)


###############################################################

bpy.context.view_layer.objects.active = bpy.data.objects['Right Eye']
ob = bpy.context.active_object
#ob.rotation_euler = [-2.1501145362854004, -19.200000762939453, 0.2981676161289215]
ob.rotation_euler  = [0, 0.0, radians(-5)]
ob.keyframe_insert(data_path='rotation_euler', frame= frame_num+80)

bpy.context.view_layer.objects.active = bpy.data.objects['Left Eye']
ob = bpy.context.active_object
#ob.rotation_euler = [1.9857800006866455, -19.200000762939453, 0.318055659532547]
ob.rotation_euler  = [radians(0.5), 0.0, radians(5)]
ob.keyframe_insert(data_path='rotation_euler', frame= frame_num+80)

# setting keyfram for eye rotaion
    # Initial conditions for head
bpy.context.view_layer.objects.active = bpy.data.objects['FBHead']
ob = bpy.context.active_object
ob.rotation_euler = (0.0, 0.0, 0)
ob.keyframe_insert(data_path='rotation_euler', frame= frame_num+90) 


ob.rotation_euler = (0.0, 0.0, radians(16))
ob.keyframe_insert(data_path='rotation_euler', frame= frame_num+120)

ob.rotation_euler = (0.0, 0.0, radians(16))
ob.keyframe_insert(data_path='rotation_euler', frame= frame_num+150) 


ob.rotation_euler = (0.0, 0.0, 0)
ob.keyframe_insert(data_path='rotation_euler', frame= frame_num+170) 
