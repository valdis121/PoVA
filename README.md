# Traffic analysis with YOLOv8

There are only source files of our latex report without images.
We were not able to upload our documentation because of size restrictions. Our had 17Mb and limit in VUT IS is only 10Mb.
Here is the link to it - https://www.overleaf.com/8985756448kcmwxkvqjxxy#7e30cd
Our prezentation - https://docs.google.com/presentation/d/1GyvNx3bWsOMYYoNqWbjTuuZfVZwnUh0yMxqG3ORn3r8/edit#slide=id.g2a9a0773282_0_29

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
- ultralytics

You can install these dependencies using pip:
```bash
pip install geopy
pip install ultralytics