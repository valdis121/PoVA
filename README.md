# Project Name

This project consists of three scripts: `geo.py`, `new.py`, and `nn.py`.

## geo.py

The `geo.py` script utilizes the Geopy library to create a map and calculate the km/pix distance for a GPS location of a road or crossroad.

## new.py

The `new.py` script calculates the homographic matrix and stores it into `h.npy`. This matrix is used to transform frames in the video to a view similar to an image from Geopy.

## nn.py

The `nn.py` script uses the YOLOv8 model to estimate the speed of cars in a video. It utilizes the homographic matrix from `h.npy` to transform each frame and create a view similar to an image from Geopy.

Please refer to the individual script files for more detailed information on their usage and dependencies.

## Installation

To run this project, you will need to install the following dependencies:

- Geopy
- YOLOv8

You can install these dependencies using pip:
```bash
pip install geopy
pip install yolov8