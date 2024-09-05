import os
import bpy
import sys
from pathlib import Path

# Add directories to the Python path so that custom modules can be imported
sys.path.insert(0, os.path.dirname(__file__))

# Import custom modules
from MyScene import MyScene
from model import SyntheticFaceGenerator
from AnimGaze import MyAnimGaze
from GenPupils import GenGazeP


# Set the device to GPU
bpy.context.scene.cycles.device = 'GPU'
bpy.context.scene.cycles.samples = 128  # Number of samples
bpy.context.scene.cycles.use_adaptive_sampling = True  # Adaptive sampling for faster renders
bpy.context.scene.cycles.use_denoising = True  # Enable denoising

# Initialize and run the model setup
Model = SyntheticFaceGenerator()
Model.start()


# Initialize and set up the scene
Scene = MyScene("STFOX",power=sys.argv[9], mode=sys.argv[7])
Scene.start()

# Animate the gaze
anim = MyAnimGaze(fixed=sys.argv[13],
                  gaze_yaw_range=tuple(map(int, (sys.argv[10]).split(','))), 
                  gaze_pitch_range=tuple(map(int, (sys.argv[11]).split(','))), 
                  num_frames=sys.argv[12]
                  )  

# Generate the synthetic data by rendering the scene
Gen = GenGazeP(R_pupil= Model.RightPupil, 
               L_pupil= Model.LeftPupil,
               directoy_name= sys.argv[8],
               frame_end =sys.argv[12],
               clothes_choice =  sys.argv[14],
               hat_choice =  sys.argv[15],
               mask_choice = sys.argv[16],  
               hair_choice =  sys.argv[17],  
               ).start("Rendu_" + sys.argv[18])

