
# Synthetic Face Data Generator

This project is a graphical user interface (GUI) application built using Python and Tkinter. The application is designed to generate synthetic face datasets by leveraging Blender's 3D modeling capabilities. The user can specify various parameters such as head texture, gaze direction ranges, camera mode, and more. The application allows for generating multiple images with varying conditions by looping through specified ranges.

## Table of Contents

- [Features](#features)
- [Requirements](#requirements)
- [Installation](#installation)
- [Usage](#usage)
- [Configuration](#configuration)
- [File Descriptions](#file-descriptions)

## Features

- **GUI Interface:** Intuitive user interface to configure various parameters for dataset generation.
- **Customizable Parameters:** Allows users to select head textures, set gaze ranges, choose camera modes, and more.
- **Loop Functionality:** Generate datasets over a range of configurations with loop support.
- **Instruction Guide:** A dedicated instruction guide accessible via the UI.

## Requirements

Before running the application, ensure you have the following installed:

- **Python 3.x**
- **Blender 3D software** (version 3.3)
- Python libraries:
  - `tkinter` (Usually included with Python)
  - `PIL` (Pillow)


## Installation

1. **Clone the repository:**

   ```bash
   git clone https://github.com/yourusername/synthetic-face-data-generator.git
   cd synthetic-face-data-generator

## Usage

1. **Run the Application:**
    Start the GUI by running the Python script:
  
   ```bash
   python main.py
   
3. **Configure Parameters:**

   - **Head Texture:** Browse and select a texture file for the head.
   - **Head Fixed:** Choose whether the head remains fixed (True) or not (False).
   - **Light Power:** Adjust the light intensity for the rendered scene.
   - **Gaze Yaw Range:** Set the minimum and maximum yaw angles for the gaze.
   - **Gaze Pitch Range:** Set the minimum and maximum pitch angles for the gaze.
   - **Camera Mode:** Choose the camera mode (front or Pillar).
   - **Number of Images:** Specify how many images to generate per configuration.
   - **Loop Range:** Define the start and end values for looping over configurations.
   - **Directory Name:** Set the output directory name for the generated dataset

4. **Generate Dataset:**

Click the "Generate Dataset" button to start the process. The images will be generated based on the provided configurations and saved in the specified directory.

5. **Instructions:**

Click the "Instructions" button to open a new window with detailed guidance on how to use the application

## Configuration

Ensure that Blender is installed on your system and accessible from the command line. The application uses Blender's --background and --python options to execute Python scripts for rendering the dataset.

## File Descriptions

  - **main.py:** The main Python script containing the Tkinter GUI code.
  - **Launch.py:** The script executed by Blender to generate the dataset.
  - **Model.py:** Handles the core aspects of generating and manipulating the synthetic face model.It loads head textures, creates blend shapes, and sets up the environment (HDRI background, lighting, etc.). It also generates and positions 3D eye spheres and applies textures to them.
  - **MyScene.py:** Sets up the Blender scene, including camera and lighting configurations.
  - **AnimGaze.py:** Handles the animation of the head and gaze. It sets keyframes for head and eye movements over a specified number of frames.
  - **GenPupils.py:** Responsible for rendering the frames and saving the images, along with generating associated metadata like bounding boxes, landmark positions, and rotations.

