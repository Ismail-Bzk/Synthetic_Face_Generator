#This script gives projected the 2D pixel coordinate from a 3D world-space location.
#The (0, 0) origin is the bottom left of the image
#A negative Z return value means the point is behind the camera:


# Test the function using the active object (which must be a camera)
# and the 3D cursor as the location to find.
import bpy
import bpy_extras

scene = bpy.context.scene
cam = bpy.data.objects['OV2312']
co = bpy.context.scene.cursor.location

co_2d = bpy_extras.object_utils.world_to_camera_view(scene, cam, co)
"""
# use generator expressions () or list comprehensions []
verts = (vert.co for vert in obj.data.vertices)
coords_2d = [world_to_camera_view(scene, cam, coord) for coord in verts]
aa = [i.z for i in coords_2d]
"""
print("2D Coords:", co_2d)

# If you want pixel coords
render_scale = scene.render.resolution_percentage / 100
render_size = (
    int(scene.render.resolution_x * render_scale),
    int(scene.render.resolution_y * render_scale),
)
print("Pixel Coords:", (
      round(co_2d.x * render_size[0]),
      round(render_size[1] - co_2d.y * render_size[1]),
)) # can use round to round the values
