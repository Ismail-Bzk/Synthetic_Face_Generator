import bpy
import bpy_extras
from bpy.props import StringProperty, IntProperty, BoolProperty
from bpy_extras.io_utils import ExportHelper
from mathutils import Matrix, Vector, Euler
import numpy as np
import random
from pathlib import Path
import os
import math
import csv
import sys
import json

from utils import *
current_dir = os.getcwd()
parent_dir = os.getcwd()

class GenGazeP:
    def __init__(self, R_pupil, L_pupil,directoy_name = "Gaze_PillarA_test",frame_end=2,
                 clothes_choice="random",hat_choice="random",mask_choice="random",
                 hair_choice="random"):
        
        self.dumpImage = True
        self.enableDebug = True
        self.fpath = os.path.join(os.path.dirname(__file__), directoy_name)
        self.IMAGE_Back = [str(f) for f in (Path(os.path.join(os.path.dirname(__file__),"HDRI"))).glob("*")]
        bpy.context.scene.frame_end = int(frame_end)
        self.frame_range = range(0, bpy.context.scene.frame_end + 1)
        self.hair = None
        self.clothes = None
        self.mask = None
        self.LeftPupil = L_pupil
        self.RightPupil = R_pupil
        self.data_json= self.read_json(os.path.join(os.path.dirname(__file__), "utils","utils.json"))
        self.clothes_choice = str(clothes_choice)
        self.hat_choice = str(hat_choice)
        self.mask_choice = mask_choice
        self.hair_choice = hair_choice
        
    def read_json(self,file_path):
        with open(file_path, 'r') as json_file:
            data = json.load(json_file)
        
        # Access the stored variable
        return data


    
    def setup_render_nodes(self):
        """Setup rendering nodes for glare and lens distortion."""
        tree = bpy.context.scene.node_tree
        tree.nodes.clear()

        render_layers = tree.nodes.new('CompositorNodeRLayers')
        render_layers.location = -300, 300

        glare = tree.nodes.new('CompositorNodeGlare')
        glare.location = 100, 300
        glare.glare_type = 'FOG_GLOW'
        glare.quality = 'HIGH'
        glare.threshold = 0.85

        lens_distortion = tree.nodes.new('CompositorNodeLensdist')
        lens_distortion.location = 300, 300
        lens_distortion.use_fit = True
        lens_distortion.inputs[2].default_value = 0.025

        composite = tree.nodes.new('CompositorNodeComposite')
        composite.location = 500, 300

        tree.links.new(render_layers.outputs[0], glare.inputs[0])
        tree.links.new(glare.outputs[0], lens_distortion.inputs[0])
        tree.links.new(lens_distortion.outputs[0], composite.inputs[0])

    def setup_background(self, background_path, brightness=0.0, contrast=0, b_M=0, c_M=0):
        """Setup background image and compositing nodes."""
        cam = bpy.data.objects['STFOX']
        img = bpy.data.images.load(background_path)
        cam.data.show_background_images = True
        bg = cam.data.background_images.new()
        bg.image = img
        bpy.context.scene.render.film_transparent = True
        bpy.context.scene.use_nodes = True
        tree = bpy.context.scene.node_tree
        tree.nodes.clear()

        render_layers = tree.nodes.new('CompositorNodeRLayers')
        render_layers.location = -300, 300

        brightness_node_model = tree.nodes.new('CompositorNodeBrightContrast')
        brightness_node_model.location = 50, 200
        brightness_node_model.name = "Model_B/C"
        brightness_node_model.inputs[1].default_value = b_M
        brightness_node_model.inputs[2].default_value = c_M

        composite = tree.nodes.new('CompositorNodeComposite')
        composite.location = 500, 300

        alpha_over = tree.nodes.new(type="CompositorNodeAlphaOver")
        alpha_over.location = 250, 450

        scale = tree.nodes.new(type="CompositorNodeScale")
        scale.space = 'RENDER_SIZE'
        scale.frame_method = 'CROP'
        scale.location = -100, 500

        image_node = tree.nodes.new(type="CompositorNodeImage")
        image_node.image = img
        image_node.location = -550, 500

        brightness_node = tree.nodes.new(type="CompositorNodeBrightContrast")
        brightness_node.location = -300, 500
        brightness_node.inputs[1].default_value = brightness
        brightness_node.inputs[2].default_value = contrast

        blur_type_options = ['FLAT', 'TENT', 'QUAD', 'CUBIC', 'GAUSS', 'FAST_GAUSS', 'CATROM', 'MITCH']
        background_blur = tree.nodes.new(type="CompositorNodeBlur")
        background_blur.location = 100, 700
        background_blur.filter_type = random.choice(blur_type_options)
        background_blur.size_x = random.randint(0, 20)
        background_blur.size_y = random.randint(0, 20)

        links = tree.links
        links.new(render_layers.outputs[0], brightness_node_model.inputs[0])
        links.new(brightness_node_model.outputs[0], alpha_over.inputs[2])
        links.new(alpha_over.outputs[0], composite.inputs[0])
        links.new(image_node.outputs[0], brightness_node.inputs[0])
        links.new(brightness_node.outputs[0], background_blur.inputs[0])
        links.new(background_blur.outputs[0], scale.inputs[0])
        links.new(scale.outputs[0], alpha_over.inputs[1])

    def apply_environment_texture(self, background_path):
        """Apply HDRI environment texture."""
        node_tree = bpy.context.scene.world.node_tree
        node_tree.nodes.clear()

        node_background = node_tree.nodes.new(type='ShaderNodeBackground')
        node_background.location = 500, 300

        node_environment = node_tree.nodes.new('ShaderNodeTexEnvironment')
        node_environment.image = bpy.data.images.load(background_path)
        node_environment.location = -300, 0

        node_output = node_tree.nodes.new(type='ShaderNodeOutputWorld')
        node_output.location = 200, 0

        node_mapping = node_tree.nodes.new(type='ShaderNodeMapping')
        node_mapping.location = 0, 300

        node_tex_coord = node_tree.nodes.new(type='ShaderNodeTexCoord')
        node_tex_coord.location = -200, 300

        links = node_tree.links
        links.new(node_tex_coord.outputs[0], node_mapping.inputs[0])
        links.new(node_mapping.outputs[0], node_environment.inputs[0])
        links.new(node_environment.outputs["Color"], node_background.inputs[0])
        links.new(node_background.outputs[0], node_output.inputs["Surface"])

        node_mapping.inputs[2].default_value[2] = math.radians(random.randint(0, 360))
        node_background.inputs[1].default_value = random.uniform(0.3, 0.5)

    def apply_eye_head_noise(self):
        """Apply random textures and parameters to eyes and head materials."""
        eye_texture_path = str(random.choice(list((Path(os.path.join(os.path.dirname(__file__),"EyeTextures"))).glob("*"))))
        bpy.data.materials['texture_Eye'].node_tree.nodes['Image Texture'].image = bpy.data.images.load(eye_texture_path)
        bpy.data.materials["FBHead_preview_mat"].node_tree.nodes["Mix Shader"].inputs[0].default_value = random.uniform(0.1, 0.7)
        bpy.data.materials["texture_Eye"].node_tree.nodes["Mix Shader"].inputs[0].default_value = random.uniform(0.3, 0.8)

    def capture_image(self, f):
        """Capture and save the rendered image for the given frame."""
        directory = os.path.join(self.fpath, '%d' % f)
        bpy.context.scene.render.filepath = os.path.join(directory, 'image%d.jpg' % f)
        bpy.ops.render.render(write_still=True)

    def cleanup(self):
        """Clean up objects and materials used during the render process."""
        for obj in [self.hair, self.clothes, self.mask]:
            if obj and obj.name in bpy.data.objects:
                for mat in obj.data.materials:
                    bpy.data.materials.remove(mat)
                bpy.data.objects.remove(obj)
        
    def remove_objects_and_materials(self, *objects):
        """Remove the given objects and their associated materials from the scene."""
        for obj in objects:
            if obj in [ i for i in bpy.data.objects]:
                for mat in obj.data.materials:
                    bpy.data.materials.remove(mat)
                bpy.data.objects.remove(obj)




    def write_csv_data(self, f, csv_writer):
        """Write metadata to CSV."""
        Write_In_Csv(f, csv_writer)


    def process_frame(self, f, csv_writer):
        bpy.context.scene.frame_set(f)
        
        BShapesName = [i.name for i in bpy.data.shape_keys["Key"].key_blocks]
        Eye_Blend = [BShapesName[1], BShapesName[2]]

    	# Randomly adjust eye blend shapes
        for k in Eye_Blend:
            bpy.data.shape_keys["Key"].key_blocks[k].value = random.uniform(0, 0)

    	# Apply random facial expressions
        if not random.randint(1, 5):
            rand = random.choices(BShapesName[15:20], k=random.randint(1, 3))
            for m in rand:
                bpy.data.shape_keys["Key"].key_blocks[m].value = random.uniform(0, 0.5)

    	# Camera setup
        cam = bpy.data.objects['STFOX']
        cam.data.background_images.clear()
        cam.data.background_images.update()

    	# Object evaluation for vertex data
        scene = bpy.context.scene
        depsgraph = bpy.context.evaluated_depsgraph_get()
        obj = bpy.data.objects['FBHead']
        obj_eval = obj.evaluated_get(depsgraph)
        mesh = obj_eval.to_mesh()
        matrix = cam.matrix_world.normalized().inverted()
        mesh.transform(obj.matrix_world)

    	# Get vertex coordinates
        XX = np.array([v.co[0] for v in mesh.vertices])
        YY = np.array([v.co[1] for v in mesh.vertices])
        ZZ = np.array([v.co[2] for v in mesh.vertices])
        mesh.transform(matrix)

    	# List of important vertices (from your previous landmarks or other key vertices)
        res1 = self.data_json.get("res1", [])    
        coW = [Vector((XX[i], YY[i], ZZ[i])) for i in res1]
        coW_all = [Vector((XX[i], YY[i], ZZ[i])) for i in range(len(XX))]
        coords_2d = [bpy_extras.object_utils.world_to_camera_view(scene, cam, coord) for coord in coW]
        coords_2d_all = [bpy_extras.object_utils.world_to_camera_view(scene, cam, coord) for coord in coW_all]

    	# Convert to pixel coordinates
        render_scale = scene.render.resolution_percentage / 100
        render_size = (
        int(scene.render.resolution_x * render_scale),
        int(scene.render.resolution_y * render_scale),
    	)
        Pixels = [[(i.x * render_size[0]), (render_size[1] - i.y * render_size[1])] for i in coords_2d]
        all_pix = [[(i.x * render_size[0]), (render_size[1] - i.y * render_size[1])] for i in coords_2d_all]
        Pixels = np.array(Pixels)
        all_pix = np.array(all_pix)

    	# Create output directory for the frame
        directory = os.path.join(self.fpath, '%d' % f)
        os.mkdir(directory)

    	# If debugging is enabled, compute visibility for each vertex
        if self.enableDebug:
            visibility = np.zeros(len(XX))
            for index in range(len(XX)):
                end = Vector([XX[index], YY[index], ZZ[index]])
                start = cam.location
                dir = end - start
                dir.normalize()
                hit, loc, normal, ind, ob, m = bpy.context.scene.ray_cast(depsgraph, start, dir)
                visible = hit & ((loc - end).length < 10e-3)
                visibility[index] = visible
            with open(os.path.join(directory, 'DlibpointCloud.txt'), 'wt') as fp:
                fp.write("Landmark,Pixel_x,Pixel_y,Visibility\n")
                for landmark, v in enumerate(res1, 1):
                    fp.write(f"{landmark},{Pixels[landmark-1][0]},{Pixels[landmark-1][1]},{visibility[v]}\n")
                
                Pupils_pixel_x, Pupils_visibility = Writetxt(self.RightPupil, self.LeftPupil)
                for i in range(len(Pupils_pixel_x)):
                    fp.write(f"{landmark},{Pupils_pixel_x[i][0]},{Pupils_pixel_x[i][1]},{visibility[i]}\n")
                    landmark += 1

    	# Bounding boxes
        ears = range(10394, 13002)
        idx_without_ears = np.array([i for i in range(len(XX)) if i not in ears])
        scalp = self.data_json.get("scalp", [])
        idx_without_ears_scalp = np.array([i for i in idx_without_ears if i not in scalp])
        
        bboxH = [
        	[min(all_pix[idx_without_ears_scalp][:, 0]), min(all_pix[idx_without_ears][:, 1])],
        	[max(all_pix[idx_without_ears_scalp][:, 0]), max(all_pix[idx_without_ears][:, 1])]
    	]
        bboxF = [
        	[min(all_pix[res1][:, 0]), min(all_pix[res1][:, 1])],
        	[max(all_pix[res1][:, 0]), max(all_pix[res1][:, 1])]
    	]

    	# Write bounding boxes to files
        with open(os.path.join(directory, 'Hbox.txt'), 'wt') as fp:
            fp.write("Pixel_x,Pixel_y\n")
            fp.write(f"{bboxH[0][0]},{bboxH[0][1]}\n")
            fp.write(f"{bboxH[1][0]},{bboxH[1][1]}\n")
        
        
        with open(os.path.join(directory, 'Fbox.txt'), 'wt') as fp:
            fp.write("Pixel_x,Pixel_y\n")
            fp.write(f"{bboxF[0][0]},{bboxF[0][1]}\n")
            fp.write(f"{bboxF[1][0]},{bboxF[1][1]}\n")

    	# Head rotation in user reference
        user_rot = Vector(bpy.data.objects['FBHead'].matrix_world.to_euler())
        with open(os.path.join(directory, 'HeadRot_Use.txt'), 'wt') as fu:
            fu.write("Rot_X,Rot_Y,Rot_Z\n")
            fu.write(f"{user_rot[0]},{user_rot[1]},{user_rot[2]}\n")

    	# Head rotation in camera reference
        rotation_vector = (cam.rotation_euler[0] - 1.5707963705062866, 0.0, cam.rotation_euler[2] + 1.5707963705062866)
        euler_rotation = Euler(rotation_vector, 'XYZ')
        rotation_matrix = euler_rotation.to_matrix()
        mat = rotation_matrix.normalized().inverted() @ bpy.data.objects['FBHead'].matrix_world.to_euler().to_matrix()
        Rotation_Vect = Vector(mat.to_euler())
        with open(os.path.join(directory, 'HeadRot_Cam.txt'), 'wt') as fp:
            fp.write("Rot_X,Rot_Y,Rot_Z\n")
            fp.write(f"{Rotation_Vect[0]},{Rotation_Vect[1]},{Rotation_Vect[2]}\n")

    	# Eye rotation in user reference
        Eyeuser_rot = Vector(bpy.data.objects['Right Eye'].matrix_world.to_euler())
        with open(os.path.join(directory, 'EyeRot_Use.txt'), 'wt') as fE:
            fE.write("Rot_X,Rot_Y,Rot_Z\n")
            fE.write(f"{Eyeuser_rot[0]},{Eyeuser_rot[1]},{Eyeuser_rot[2]}\n")

		# Eye rotation in camera reference
        Eye_C = rotation_matrix.normalized().inverted() @ bpy.data.objects['Right Eye'].matrix_world.to_euler().to_matrix()
        Rotation_Vect_E = Vector(Eye_C.to_euler())
        with open(os.path.join(directory, 'EyeRot_Cam.txt'), 'wt') as fp:
            fp.write("Rot_X,Rot_Y,Rot_Z\n")
            fp.write(f"{Rotation_Vect_E[0]},{Rotation_Vect_E[1]},{Rotation_Vect_E[2]}\n")

    	# Write data to CSV
        Write_In_Csv(f, csv_writer)
        if self.dumpImage:
            # Set background image or environment texture
            # self.setup_background(self.IMAGE_Back[random.randint(0, len(self.IMAGE_Back) - 1)], 0, random.randint(0, 30), 0)
            bpy.data.objects['Spot'].data.energy = random.uniform(1, 15)
            bpy.data.worlds["World"].node_tree.nodes['Environment Texture'].image = bpy.data.images.load(random.choice(self.IMAGE_Back))
            bpy.data.worlds["World"].node_tree.nodes["Background"].inputs[1].default_value = random.uniform(0.2, 0.5)
            bpy.data.worlds["World"].node_tree.nodes["Mapping"].inputs[2].default_value[2] = math.radians(random.uniform(0, 360))

        	# Randomize depth of field
            #bpy.data.objects['STFOX'].data.dof.aperture_fstop = random.uniform(0.4, 15)
            
            self.apply_eye_head_noise()
            
            
        	# Add random hair, clothes, or accessories  
            if self.clothes_choice != "empty":
                self.clothes = Clothes_Model(self.clothes_choice)
                
            if self.hair_choice != "empty":
                self.hair = hair_Model(self.hair_choice)
                
            if self.hat_choice != "empty":
                self.hair = Hat(self.hat_choice)
                
            if self.mask_choice != "empty":
                self.mask = Maskk(self.mask_choice)
                
            
                
            """    
            if random.randint(0, 3):
                if random.randint(0, 2):
                    self.hair = hair_Model()
                else:
                    self.hair = Hat()
            
            if not random.randint(0, 8):
                if random.randint(1, 2):
                    self.mask = Maskk()
                else:
                    self.mask = beard()
            """
        	# Render and save image
            bpy.context.scene.render.filepath = os.path.join(directory, f'image{f}.jpg')
            bpy.ops.render.render(write_still=True)

        	# Clean up
            
            """_summary_
        
            if self.hair in [ i for i in bpy.data.objects]:
                for mat in self.hair.data.materials:
                        bpy.data.materials.remove(mat)
                bpy.data.objects.remove(self.hair)

            if self.clothes in [ i for i in bpy.data.objects]:
               for mat in self.clothes.data.materials:
                  bpy.data.materials.remove(mat)
               bpy.data.objects.remove(self.clothes)

            if self.mask in [ i for i in bpy.data.objects]:
                for mat in self.mask.data.materials:
                    bpy.data.materials.remove(mat)
                bpy.data.objects.remove(self.mask)
            """
            # Usage
            self.remove_objects_and_materials(self.hair, self.clothes, self.mask)

        	# Reset blend shapes
            #for m in BShapesName:
            #   bpy.data.shape_keys["Key"].key_blocks[m].value = 0

        

    def start(self, nameRep):
        """Main function to start the generation process."""
        self.fpath = os.path.join(self.fpath, sys.argv[18], nameRep)
        os.makedirs(self.fpath, exist_ok=True)

        prev_output_format = bpy.context.scene.render.image_settings.file_format
        bpy.context.scene.render.image_settings.file_format = 'JPEG'
        bpy.context.scene.render.image_settings.color_mode = 'RGB'
        bpy.context.scene.render.engine = 'CYCLES'
        prefs = bpy.context.preferences.addons['cycles'].preferences
        prefs.compute_device_type = 'CUDA'
        for device in prefs.devices:
            device.use = True
            
        

        csv_path = os.path.join(Path(self.fpath).parent, f'Dlib_Blenshapes_ME_2d{sys.argv[18]}.csv')
        with open(csv_path, 'w', newline='') as csv_file:
            csv_writer = csv.writer(csv_file)
            row = Init_csv()
            csv_writer.writerow(row)

            for f in self.frame_range:
                self.process_frame(f, csv_writer)

        bpy.context.scene.render.image_settings.file_format = prev_output_format
        
        csv_file.close()

