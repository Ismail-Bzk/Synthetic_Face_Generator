import os
import sys

import bpy


def parse_args(argv):
    if "--" in argv:
        args = argv[argv.index("--") + 1:]
    else:
        args = []
    output_dir = "ci_output"
    resolution = (128, 128)
    num_samples = 4

    i = 0
    while i < len(args):
        if args[i] == "--output_dir":
            output_dir = args[i + 1]
            i += 2
        elif args[i] == "--resolution":
            res = args[i + 1]
            if "x" in res:
                width, height = res.split("x", 1)
                resolution = (int(width), int(height))
            else:
                size = int(res)
                resolution = (size, size)
            i += 2
        elif args[i] == "--num_samples":
            num_samples = int(args[i + 1])
            i += 2
        else:
            i += 1
    return output_dir, resolution, num_samples


def main():
    output_dir, resolution, num_samples = parse_args(sys.argv)
    if not os.path.isabs(output_dir):
        output_dir = os.path.join(os.path.dirname(__file__), output_dir)
    os.makedirs(output_dir, exist_ok=True)

    scene = bpy.context.scene
    scene.render.engine = "CYCLES"
    scene.cycles.samples = num_samples
    scene.render.resolution_x, scene.render.resolution_y = resolution
    scene.render.resolution_percentage = 100
    scene.render.image_settings.file_format = "PNG"
    scene.render.image_settings.color_mode = "RGB"
    scene.render.filepath = os.path.join(output_dir, "smoke.png")

    bpy.ops.object.select_all(action="SELECT")
    bpy.ops.object.delete()

    bpy.ops.mesh.primitive_cube_add(size=2, location=(0, 0, 0))
    bpy.ops.object.light_add(type="AREA", location=(4, -4, 4))
    bpy.ops.object.camera_add(location=(4, -4, 3), rotation=(1.1, 0, 0.78))
    scene.camera = bpy.context.object

    bpy.ops.render.render(write_still=True)


if __name__ == "__main__":
    main()
