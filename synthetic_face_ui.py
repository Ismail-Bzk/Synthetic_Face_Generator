import tkinter as tk
from tkinter import filedialog, ttk
from PIL import Image, ImageTk
import subprocess
import os

class SyntheticFaceUI:
    def __init__(self, root):
        self.root = root
        root.title("Synthetic Face Data Generator")
        root.configure(bg="#2c3e50") 
        root.geometry("600x950")
        root.resizable(True, True)

        # Set default font
        default_font = ("Arial", 10)

        # Title Label
        title_label = tk.Label(root, text="Synthetic Face Data Generator", font=("Arial", 18, "bold"), bg="#1abc9c", fg="white")
        title_label.pack(pady=10, fill=tk.X)

        # Image Frame
        self.create_image_frame(root)

        # Input Frame
        self.create_input_frame(root, default_font)

        # Instruction Button
        self.instruction_button = tk.Button(root, text="Instructions", command=self.open_instructions_window, bg="#3498db", fg="white", font=("Arial", 12, "bold"))
        self.instruction_button.pack(pady=10, fill=tk.X, padx=20)

        # Assets Info Button
        self.assets_info_button = tk.Button(root, text="Assets Information", command=self.open_assets_info_window, bg="#3498db", fg="white", font=("Arial", 12, "bold"))
        self.assets_info_button.pack(pady=10, fill=tk.X, padx=20)

        # Generate Button
        self.generate_button = tk.Button(root, text="Generate Dataset", command=self.generate_dataset, bg="#e74c3c", fg="white", font=("Arial", 14, "bold"))
        self.generate_button.pack(pady=20, fill=tk.X, padx=20, side=tk.BOTTOM)  # Explicitly packing at the bottom

    def create_image_frame(self, root):
        # Frame for Image
        image_frame = tk.Frame(root, bg="#2c3e50")
        image_frame.pack(pady=10)

        # Load an image using Pillow
        image_path = os.path.join(os.path.dirname(__file__), "utils", "interface.png")  # Replace with the path to your image
        img = Image.open(image_path)

        # Resize the image to fit within the Tkinter window
        img = img.resize((400, 300), Image.ANTIALIAS)

        # Convert the image to a Tkinter-compatible format
        img_tk = ImageTk.PhotoImage(img)

        # Create a label to display the image
        image_label = tk.Label(image_frame, image=img_tk, bg="#2c3e50")
        image_label.image = img_tk  # Keep a reference to avoid garbage collection
        image_label.pack()

    def create_input_frame(self, root, default_font):
        # Frame for Input Fields
        input_frame = tk.Frame(root, bg="#34495e", padx=20, pady=20)
        input_frame.pack(fill=tk.BOTH, expand=True)

        # Head Texture
        tk.Label(input_frame, text="Head Texture:", font=default_font, bg="#34495e", fg="white").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.head_texture_entry = tk.Entry(input_frame, width=40, bg="#ecf0f1")
        self.head_texture_entry.grid(row=0, column=1, padx=10, pady=5)
        tk.Button(input_frame, text="Browse", command=self.browse_head_texture, bg="#2980b9", fg="white").grid(row=0, column=2, padx=10)

        # Head Fixed
        tk.Label(input_frame, text="Head Fixed:", font=default_font, bg="#34495e", fg="white").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.head_fixed_combobox = ttk.Combobox(input_frame, width=39, values=["True", "False"], font=default_font)
        self.head_fixed_combobox.current(0)  # Set default value to "True"
        self.head_fixed_combobox.grid(row=1, column=1, padx=10, pady=5, sticky=tk.W)

        # Light Power
        tk.Label(input_frame, text="Light Power:", font=default_font, bg="#34495e", fg="white").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.light_power_slider = tk.Scale(input_frame, from_=0, to=100, orient=tk.HORIZONTAL, bg="#2c3e50", fg="white", troughcolor="#1abc9c")
        self.light_power_slider.set(20)
        self.light_power_slider.grid(row=2, column=1, padx=10, pady=5, columnspan=2, sticky="we")

        # Gaze Yaw Range
        tk.Label(input_frame, text="Gaze Yaw Range:", font=default_font, bg="#34495e", fg="white").grid(row=3, column=0, sticky=tk.W, pady=5)
        self.gaze_yaw_min = tk.Entry(input_frame, width=10, bg="#ecf0f1")
        self.gaze_yaw_min.insert(0, "-30")
        self.gaze_yaw_min.grid(row=3, column=1, sticky=tk.W, padx=10, pady=5)
        self.gaze_yaw_max = tk.Entry(input_frame, width=10, bg="#ecf0f1")
        self.gaze_yaw_max.insert(0, "30")
        self.gaze_yaw_max.grid(row=3, column=2, sticky=tk.E, padx=10, pady=5)

        # Gaze Pitch Range
        tk.Label(input_frame, text="Gaze Pitch Range:", font=default_font, bg="#34495e", fg="white").grid(row=4, column=0, sticky=tk.W, pady=5)
        self.gaze_pitch_min = tk.Entry(input_frame, width=10, bg="#ecf0f1")
        self.gaze_pitch_min.insert(0, "-20")
        self.gaze_pitch_min.grid(row=4, column=1, sticky=tk.W, padx=10, pady=5)
        self.gaze_pitch_max = tk.Entry(input_frame, width=10, bg="#ecf0f1")
        self.gaze_pitch_max.insert(0, "15")
        self.gaze_pitch_max.grid(row=4, column=2, sticky=tk.E, padx=10, pady=5)

        # Camera Mode
        tk.Label(input_frame, text="Camera Mode:", font=default_font, bg="#34495e", fg="white").grid(row=5, column=0, sticky=tk.W, pady=5)
        self.camera_mode = ttk.Combobox(input_frame, values=["front", "Pillar"], font=default_font)
        self.camera_mode.current(0)
        self.camera_mode.grid(row=5, column=1, padx=10, pady=5, sticky="we", columnspan=2)

        # Number of images  
        tk.Label(input_frame, text="Number of images:", font=default_font, bg="#34495e", fg="white").grid(row=6, column=0, sticky=tk.W, pady=5)
        self.images_nb = tk.Entry(input_frame, width=40, bg="#ecf0f1")
        self.images_nb.insert(0, "143")
        self.images_nb.grid(row=6, column=1, sticky=tk.W, padx=10, pady=5, columnspan=2)

        # Loop Range
        tk.Label(input_frame, text="Loop Range (start,end):", font=default_font, bg="#34495e", fg="white").grid(row=7, column=0, sticky=tk.W, pady=5)
        self.loop_start = tk.Entry(input_frame, width=10, bg="#ecf0f1")
        self.loop_start.grid(row=7, column=1, sticky=tk.W, padx=10, pady=5)
        self.loop_end = tk.Entry(input_frame, width=10, bg="#ecf0f1")
        self.loop_end.grid(row=7, column=2, sticky=tk.E, padx=10, pady=5)
        
        # Clothes Selection
        tk.Label(input_frame, text="Clothes:", font=default_font, bg="#34495e", fg="white").grid(row=8, column=0, sticky=tk.W, pady=5)
        self.clothes_combobox = ttk.Combobox(input_frame, values=["random",
            "male_casualsuit01", "male_casualsuit02", "male_casualsuit03", 
            "male_casualsuit04", "male_casualsuit05", "male_casualsuit06", 
            "male_elegantsuit01", "flapper_dress", "f_kimono", 
            "goddessdress6", "hero_suit_1","empty"
        ], font=default_font)
        self.clothes_combobox.current(0)  # Set default value to the first option
        self.clothes_combobox.grid(row=8, column=1, padx=10, pady=5, sticky="we", columnspan=2)
        
        # Hat Selection
        tk.Label(input_frame, text="Hat:", font=default_font, bg="#34495e", fg="white").grid(row=9, column=0, sticky=tk.W, pady=5)
        self.hat_combobox = ttk.Combobox(input_frame, values=["random",
            "fedora","elvs_slouchy_beanie1","warrior_helmet",
            "elvs_unisex_chef_hat_1","m1951_72", "sherpa_hat","newsboy_cap",
            "maga_hat", "bikehelmet", "Monks_Hood_Down","empty"
        ], font=default_font)
        self.hat_combobox.current(0)  # Set default value to the first option
        self.hat_combobox.grid(row=9, column=1, padx=10, pady=5, sticky="we", columnspan=2)
        
        # Mask Selection
        tk.Label(input_frame, text="Mask:", font=default_font, bg="#34495e", fg="white").grid(row=10, column=0, sticky=tk.W, pady=5)
        self.mask_combobox = ttk.Combobox(input_frame, values=["random",
            "hero_mask_2","hero_mask_3","bandana_mask",
            "sagerfrogs_glasses_01","empty"
        ], font=default_font)
        self.mask_combobox.current(0)  # Set default value to the first option
        self.mask_combobox.grid(row=10, column=1, padx=10, pady=5, sticky="we", columnspan=2)

        # Mask Selection
        tk.Label(input_frame, text="Hair:", font=default_font, bg="#34495e", fg="white").grid(row=11, column=0, sticky=tk.W, pady=5)
        self.hair_combobox = ttk.Combobox(input_frame, values=["random",
            "elv_50supdo1","elvs_ashley_mayhair1","elvs_braid_bun_q1","cornrowsofelv5","elvs_grumphair",
            "maxwell_hair_mh","elvs_mickey_afro","short_messy","mhair02","blondwithheadband","elvs_hazel_hair",
            "empty"
        ], font=default_font)
        self.hair_combobox.current(0)  # Set default value to the first option
        self.hair_combobox.grid(row=11, column=1, padx=10, pady=5, sticky="we", columnspan=2)


        # Directory Name  
        tk.Label(input_frame, text="Directory Name:", font=default_font, bg="#34495e", fg="white").grid(row=12, column=0, sticky=tk.W, pady=5)
        self.directory_name = tk.Entry(input_frame, width=40, bg="#ecf0f1")
        self.directory_name.insert(0, "Gaze_PillarA_test")
        self.directory_name.grid(row=12, column=1, sticky=tk.W, padx=10, pady=5, columnspan=2)

        
    def open_instructions_window(self):
        # Create a new Toplevel window
        instructions_window = tk.Toplevel(self.root)
        instructions_window.title("Instructions & Guide")
        instructions_window.geometry("400x300")
        instructions_window.configure(bg="#2c3e50")

        # Information Label
        info_label = tk.Label(instructions_window, text="Instructions & Guide", font=("Arial", 14), bg="#2c3e50", fg="white")
        info_label.pack(anchor="w", pady=10)

        # Information Text
        info_text = (
            "1. Select the textures for the head using the 'Browse' button or insert a number =(1,242).\n"
            "2. Choose whether the head is fixed using the dropdown menu.\n"
            "3. Adjust the light power using the slider.\n"
            "4. Set the Gaze Yaw and Pitch ranges.\n"
            "5. Choose the camera mode (front or Pillar).\n"
            "6. Specify the loop range for dataset generation.\n"
            "7. Enter the number of images to generate.\n"
            "8. Enter a directory name where the dataset will be saved.\n"
            "9. Choose an asset for clothes from the dropdown menu.\n"
            "10. Click 'Generate Dataset' to start the process.\n"
        )

        # Create a Label to display the information
        info_text_label = tk.Label(instructions_window, text=info_text, font=("Arial", 10), bg="#2c3e50", fg="white", justify="left", wraplength=350)
        info_text_label.pack(anchor="w", padx=10)

    def open_assets_info_window(self):
        # Create a new Toplevel window
        assets_window = tk.Toplevel(self.root)
        assets_window.title("Available Assets Information")
        assets_window.geometry("500x500")
        assets_window.configure(bg="#2c3e50")

        # Information Label
        info_label = tk.Label(assets_window, text="Available Assets Information", font=("Arial", 14), bg="#2c3e50", fg="white")
        info_label.pack(anchor="w", pady=10)

        # Information Text for assets
        assets_info = (
            "Hat\n"
            "1. fedora\n"
            "2. elvs_slouchy_beanie1\n"
            "3. warrior_helmet\n"
            "4. elvs_unisex_chef_hat_1\n"
            "5. m1951_72\n"
            "6. sherpa_hat\n"
            "7. newsboy_cap\n"
            "8. maga_hat\n"
            "9. bikehelmet\n"
            "10. Monks_Hood_Down\n"
            "\n"
            "Mask\n"
            "1. hero_mask_2\n"
            "2. hero_mask_3\n"
            "3. bandana_mask\n"
            "4. sagerfrogs_glasses_01\n"
            "\n"
            "Sunglasses\n"
            "1. ladies_sunglass1\n"
            "2. sagerfrogs_glasses_01\n"
            "\n"
            "Beard\n"
            "1. beard1\n"
            "2. beard2\n"
            "\n"
            "Hair\n"
            "1. elv_50supdo1\n"
            "2. elvs_ashley_mayhair1\n"
            "3. elvs_braid_bun_q1\n"
            "4. cornrowsofelv5\n"
            "5. elvs_grumphair\n"
            "6. maxwell_hair_mh\n"
            "7. elvs_mickey_afro\n"
            "8. short_messy\n"
            "9. mhair02\n"
            "10. blondwithheadband\n"
            "11. elvs_hazel_hair\n"
            "\n"
            "Clothes\n"
            "1. male_casualsuit01\n"
            "2. male_casualsuit02\n"
            "3. male_casualsuit03\n"
            "4. male_casualsuit04\n"
            "5. male_casualsuit05\n"
            "6. male_casualsuit06\n"
            "7. male_elegantsuit01\n"
            "8. flapper_dress\n"
            "9. f_kimono\n"
            "10. goddessdress6\n"
            "11. hero_suit_1\n"
        )

        # Create a Label to display the assets information
        assets_info_label = tk.Label(assets_window, text=assets_info, font=("Arial", 10), bg="#2c3e50", fg="white", justify="left", wraplength=450)
        assets_info_label.pack(anchor="w", padx=10)

    def browse_head_texture(self):
        filename = filedialog.askopenfilename(title="Select Head Texture")
        self.head_texture_entry.delete(0, tk.END)
        self.head_texture_entry.insert(0, filename)

    def generate_dataset(self):
        head_texture = self.head_texture_entry.get()
        head_fixed = str(self.head_fixed_combobox.get())
        light_power = self.light_power_slider.get()
        gaze_yaw_range = f"{self.gaze_yaw_min.get()},{self.gaze_yaw_max.get()}"
        gaze_pitch_range = f"{self.gaze_pitch_min.get()},{self.gaze_pitch_max.get()}"
        camera_mode = self.camera_mode.get()
        images_nb = self.images_nb.get()
        loop_start = int(self.loop_start.get())
        loop_end = int(self.loop_end.get())
        directory_name = self.directory_name.get()
        clothes_choice = str(self.clothes_combobox.get())
        hat_choice=self.hat_combobox.get()
        mask_choice=self.mask_combobox.get()
        hair_choice= self.hair_combobox.get()
        # Construct the command to run Blender with your script and the provided parameters
        for i in range(loop_start, loop_end + 1):
            command = [
                "./blender", os.path.join(os.path.dirname(__file__), "model_v1/Model_Normal.blend"), "--background", "--python",
                os.path.join(os.path.dirname(__file__), "Launch.py"),
                "--",
                str(head_texture),  # sys.argv[6] ,i
                camera_mode,
                directory_name,
                str(light_power),
                gaze_yaw_range,
                gaze_pitch_range,
                images_nb,
                head_fixed,
                clothes_choice,  # Pass the selected clothes asset to the script
                hat_choice,
                mask_choice,
                hair_choice,
                str(i)
            ]

            # Run the Blender process
            subprocess.run(command)

if __name__ == "__main__":
    root = tk.Tk()
    app = SyntheticFaceUI(root)
    root.mainloop()
