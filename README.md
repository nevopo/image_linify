# image_linify
Need an image "linified"? You've come to the right place!!

What exactly is “Linifier”?
The “Linifier” is a python based package, relying on OPENCV and NUMPY for image processing calculations and manipulations.
It offers unlimited range of “Linifying”, what does it even mean?

You enter an input image you would like to manipulate and receive the output image.

Technical Process
Dependencies -
Linifer’s core is written in python (v3.8) and it uses:
Numpy - used for array based calculations and as a OPENCV dependency.
OPENCV or CV2 - used for image processing and manipluation
OS (default library, comes with python) - to save and move images

import numpy as np
import cv2
import os


Parameters -
*  means that the parameter is required

~  means that the parameter is optional

*source image

* destination folder - for output images, only for manual running

~ blank image base color - default value is white, rgb(255, 255, 255)
~ minimum contour size - used to remove noise, default value is 50 (50 means pixels area)
~ line width - the width of the recreated lines, default is 1 pixel (base image)
~ line spacing- the amount pixels between recreated lines , default is 1 pixel wide (base image)
~ binary image threshold - used to determine which parts of the image will be recreated, default is 130 (0 - 255, means gray)
~ reference image - if is decided to be true, recreates the image in color, not black and white, default is black and white
~ blur amount - used to smooth the image, default value is 13

Work Flow - The process

The package receives and image ->

grayscale is applied to it - used to create the binary image ->

a binary version is created - determines the target output, the sensitivity of this part is determined based on the blank image base color parameter ->

morphological filter is applied - this part removes any object in the binary image smaller than the area threshold of the minimum contour size parameter ->

Gaussian blur is applied - used to smooth out the image, works upon the binary image, uses the binary image threshold parameter to determine aggressiveness ->

linifying - based upon the line width and line spacing parameters, the new linified image is created, if given reference image it will be created with colors of the original image.

