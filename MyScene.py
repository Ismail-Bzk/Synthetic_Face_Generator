import bpy
import numpy as np
from math import radians
from mathutils import Vector, Euler

class MyScene:
    def __init__(self, camera_name,power=20, mode="front"):
        """
        Initializes the scene setup with a camera and lighting configuration.
        
        :param camera_name: Name for the camera object.
        :param mode: Camera positioning mode ('front' or 'Pillar').
        :param power: Power level of the light.
        
        """
        self.camera_name = camera_name
        self.mode = mode
        self.power = float(power)
        
    def setup_camera(self, location=(0, 0, 0), rotation=(radians(90), 0, 0), resolution=(720, 720), fov_angle=0.88174):
        """
        Sets up a camera in the scene.
        
        :param location: Camera location in the scene.
        :param rotation: Camera rotation in Euler angles.
        :param resolution: Resolution of the render output (width, height).
        :param fov_angle: Field of view angle for the camera.
        """
        # Create and position the camera
        bpy.ops.object.camera_add(enter_editmode=False, align='VIEW', location=location, rotation=rotation)
        camera = bpy.context.object
        camera.name = self.camera_name
        
        # Position camera based on mode
        if self.mode == "Pillar":
            camera.location = Vector((0.697774, -0.594165, 0.995036))
            camera.rotation_euler[2] = radians(-70)
        else:
            median_eyes = 0.5 * (bpy.data.objects['Right Eye'].location + bpy.data.objects['Left Eye'].location)
            camera.location = median_eyes
            camera.location[0] = 0.481137
            camera.rotation_euler[2] = radians(-90)

        # Set render resolution
        bpy.context.scene.render.resolution_x, bpy.context.scene.render.resolution_y = resolution
        
        # Configure lens and sensor settings
        camera.data.lens_unit = 'FOV'
        camera.data.sensor_fit = 'VERTICAL'
        camera.data.sensor_width = 24
        camera.data.sensor_height = 11
        camera.data.angle = fov_angle

        # Set render settings
        bpy.context.scene.render.image_settings.color_mode = 'RGB'
        bpy.context.scene.render.image_settings.file_format = 'JPEG'
        bpy.context.scene.render.use_compositing = True
        
    def setup_light(self,):
        """
        Sets up a spotlight in the scene with tracking constraints.
        
        """
        camera_location = bpy.data.objects[self.camera_name].location
        bpy.ops.object.light_add(type='SPOT', align='WORLD', location=camera_location)
        light = bpy.context.object
        light.name = "Spot"
        light.data.type = 'AREA'
        light.data.shape = 'ELLIPSE'
        light.data.energy = self.power
        
        # Add tracking constraint to the light
        constraint = light.constraints.new(type='TRACK_TO')
        constraint.target = bpy.data.objects["FBHead"]
        constraint.track_axis = 'TRACK_NEGATIVE_Z'
        constraint.up_axis = 'UP_Y'

    def setup_dof(self):
        """
        Sets up Depth of Field (DoF) focusing on the midpoint between the eyes.
        """
        bpy.ops.object.empty_add(type='PLAIN_AXES', align='WORLD', location=(0, 0, 0))
        focus_empty = bpy.context.object
        focus_empty.name = "FocusEmpty"
        focus_empty.location = (bpy.data.objects['Left Eye'].location + bpy.data.objects['Right Eye'].location) / 2

        # Add child-of constraint to the empty
        constraint = focus_empty.constraints.new(type='CHILD_OF')
        constraint.target = bpy.data.objects["FBHead"]

        # Enable DoF on the camera
        camera = bpy.data.objects[self.camera_name]
        camera.data.dof.use_dof = True
        camera.data.dof.focus_object = focus_empty

    def start(self):
        """
        Initializes the scene by setting up the background, camera, light, and DoF.
        """
        # Set background to black
        world = bpy.context.scene.world
        if world is None:
            world = bpy.data.worlds.new("World")
            bpy.context.scene.world = world
        world.use_nodes = True
        nodes = world.node_tree.nodes
        background = nodes.get("Background") or nodes.new(type="ShaderNodeBackground")
        output = nodes.get("World Output") or nodes.new(type="ShaderNodeOutputWorld")
        if not background.outputs[0].is_linked:
            world.node_tree.links.new(background.outputs[0], output.inputs["Surface"])
        background.inputs[0].default_value = (0, 0, 0, 1)
        
        # Setup camera, light, and DoF
        self.setup_camera()
        self.setup_light()
        self.setup_dof()

if __name__ == "__main__":
    scene = MyScene("STFOX")
    scene.start()
