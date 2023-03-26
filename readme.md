# 3D Mesh Renderer

This project is a 3D mesh renderer implemented in C++, which takes Wavefront OBJ files as input and renders the 3D mesh using OpenGL. The renderer supports different shading models, including Phong and Gouraud shading, and also includes camera controls for better visualization of the 3D objects.

![Mesh Renderer Sample Image](sample_image.png)

## Features

- Load and parse Wavefront OBJ files
- Render 3D meshes using OpenGL
- Support for Phong and Gouraud shading models
- Camera controls for object visualization
- User-friendly interface

## Installation

1. Download and install [OpenGL](https://www.opengl.org/) and [GLUT](https://www.opengl.org/resources/libraries/glut/) libraries for your platform.
2. Clone this repository or download the source code.
3. Build the project using your preferred C++ compiler and development environment.

## Usage

1. Run the compiled executable.
2. The program will open a window displaying the 3D mesh along with a simple user interface.
3. Load a Wavefront OBJ file to render the mesh in the window.
4. Use the interface to switch between shading models (Phong or Gouraud) and control the camera for better visualization.

For more information on modifying the renderer, refer to the source code comments.

## License

This project is licensed under the [MIT License](LICENSE).
