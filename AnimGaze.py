import bpy
import math
from math import radians
from mathutils import Vector
import numpy as np
import random

class MyAnimGaze:
    def __init__(self, fixed=True, head_yaw_range=(-20, 20), head_pitch_range=(-10, 10), gaze_yaw_range=(-30, 30), gaze_pitch_range=(-20, 15), num_frames=142):
        """
        Initializes the animation by setting up keyframes for head and gaze movements.
        
        :param fixed: If True, the head remains fixed while only the gaze moves.
        :param head_yaw_range: Tuple specifying the min and max values for head yaw.
        :param head_pitch_range: Tuple specifying the min and max values for head pitch.
        :param gaze_yaw_range: Tuple specifying the min and max values for gaze yaw.
        :param gaze_pitch_range: Tuple specifying the min and max values for gaze pitch.
        :param num_frames: Number of frames for the animation.
        """
        
        self.frame_number = self.find_closest_factors(int(num_frames))
        self.Head_Yaw = np.linspace(*head_yaw_range, self.frame_number[1])
        self.Head_Pitch = np.linspace(*head_pitch_range, self.frame_number[0])
        self.Gaze_Yaw = np.linspace(*gaze_yaw_range, self.frame_number[1])
        self.Gaze_Pitch = np.linspace(*gaze_pitch_range, self.frame_number[0])

        self.scene = bpy.context.scene
        self.scene.frame_start = 0
        self.scene.frame_end = int(num_frames)

        self.frame = 0

        # Set initial keyframes
        self.set_initial_keyframes()

        # Generate the animation
        self.generate_animation(eval(fixed))

        # Reset to the first frame
        self.scene.frame_set(0)

    def find_closest_factors(self,n):
        # Start from the square root of n
        root = int(math.sqrt(n))
        
        # Check downwards from the square root
        for i in range(root, 0, -1):
            if n % i == 0:
                # i and n//i are factors
                return (i, n // i)
        
        return None

    def set_initial_keyframes(self):
        """
        Set the initial keyframes for the head and gaze.
        """
        # Set initial keyframe for the right eye
        right_eye = bpy.data.objects.get('Right Eye')
        if right_eye:
            right_eye.rotation_euler = Vector((0, 0, 0))
            right_eye.keyframe_insert(data_path='rotation_euler', frame=0)

        # Set initial keyframe for the head
        head = bpy.data.objects.get('FBHead')
        if head:
            head.rotation_euler = Vector((0, 0, 0))
            head.keyframe_insert(data_path='rotation_euler', frame=0)

    def generate_animation(self, fixed):
        """
        Generate the keyframes for the animation.
        
        :param fixed: If True, the head remains fixed while only the gaze moves.
        """
        head = bpy.data.objects.get('FBHead')
        right_eye = bpy.data.objects.get('Right Eye')

        if not head or not right_eye:
            print("Error: 'FBHead' or 'Right Eye' object not found.")
            return

        for pG in self.Gaze_Pitch:
            for yG in self.Gaze_Yaw:
                self.scene.frame_set(self.frame)

                # Animate gaze
                right_eye.rotation_euler[2] = radians(yG)
                right_eye.rotation_euler[1] = radians(pG)
                right_eye.keyframe_insert(data_path='rotation_euler')

                if not fixed:
                    # Animate head if not fixed
                    head.rotation_euler[1:] = (
                        radians(random.uniform(-10, 10)),
                        radians(random.uniform(-20, 25))
                    )
                    head.keyframe_insert(data_path='rotation_euler')

                self.frame += 1

if __name__ == "__main__":
    MyAnimGaze()

