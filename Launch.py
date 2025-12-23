import os
import bpy
import sys
from types import SimpleNamespace
from pathlib import Path

# Add directories to the Python path so that custom modules can be imported
sys.path.insert(0, os.path.dirname(__file__))

# Import custom modules
from MyScene import MyScene
from model import SyntheticFaceGenerator
from AnimGaze import MyAnimGaze
from GenPupils import GenGazeP


def parse_args(argv):
    expected_count = 13
    if "--" in argv:
        args = argv[argv.index("--") + 1:]
    else:
        args = argv[1:]
    if len(args) > expected_count:
        args = args[-expected_count:]
    if len(args) < expected_count:
        raise SystemExit(f"Expected {expected_count} args, got {len(args)}: {args}")

    (
        head_texture,
        camera_mode,
        directory_name,
        light_power,
        gaze_yaw_range,
        gaze_pitch_range,
        images_nb,
        head_fixed,
        clothes_choice,
        hat_choice,
        mask_choice,
        hair_choice,
        run_id,
    ) = args

    try:
        light_power = float(light_power)
    except ValueError as exc:
        raise SystemExit(f"Invalid light_power: {light_power}") from exc
    try:
        images_nb = int(images_nb)
    except ValueError as exc:
        raise SystemExit(f"Invalid images_nb: {images_nb}") from exc

    return SimpleNamespace(
        head_texture=head_texture,
        camera_mode=camera_mode,
        directory_name=directory_name,
        light_power=light_power,
        gaze_yaw_range=gaze_yaw_range,
        gaze_pitch_range=gaze_pitch_range,
        images_nb=images_nb,
        head_fixed=head_fixed,
        clothes_choice=clothes_choice,
        hat_choice=hat_choice,
        mask_choice=mask_choice,
        hair_choice=hair_choice,
        run_id=run_id,
    )


args = parse_args(sys.argv)

# Set the device to GPU
bpy.context.scene.render.engine = "CYCLES"
bpy.context.scene.cycles.device = "GPU"
bpy.context.scene.cycles.samples = 128  # Number of samples
bpy.context.scene.cycles.use_adaptive_sampling = True  # Adaptive sampling for faster renders
try:
    bpy.context.scene.cycles.use_denoising = True  # Enable denoising
except AttributeError:
    bpy.context.view_layer.cycles.use_denoising = True

# Initialize and run the model setup
Model = SyntheticFaceGenerator()
Model.start(args.head_texture)


# Initialize and set up the scene
Scene = MyScene("STFOX", power=args.light_power, mode=args.camera_mode)
Scene.start()

# Animate the gaze
anim = MyAnimGaze(
    fixed=args.head_fixed,
    gaze_yaw_range=tuple(map(int, args.gaze_yaw_range.split(","))),
    gaze_pitch_range=tuple(map(int, args.gaze_pitch_range.split(","))),
    num_frames=args.images_nb,
)

# Generate the synthetic data by rendering the scene
Gen = GenGazeP(
    R_pupil=Model.RightPupil,
    L_pupil=Model.LeftPupil,
    directoy_name=args.directory_name,
    frame_end=args.images_nb,
    clothes_choice=args.clothes_choice,
    hat_choice=args.hat_choice,
    mask_choice=args.mask_choice,
    hair_choice=args.hair_choice,
    run_id=args.run_id,
).start(f"Rendu_{args.run_id}")
