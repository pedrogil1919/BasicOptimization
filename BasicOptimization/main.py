'''
Created on 4 mar. 2022

@author: pedrogil
'''
# NOTE: To include the other project as a external library:
# - Project/Properties:
#   - PyDev - PYTHONPATH
#     - tAB External Libraries -> Add source folder

import sys
import os
import numpy
import cv2

# sys.path.append("/home/pedrogil/git/Wheelchair/Structure")
# sys.path.append("/home/pedrogil/workspace/optimization/Structure")

from simulator.simulator import Simulator
from physics.stairs import Stair
import readXML

from optimize.compute_time import compute_mesh_time, \
    read_optimization_data, save_contours

import logging

# Open and check settings file.
try:
    settings_name = sys.argv[1]
except Exception:
    settings_name = "settings.xml"


# Read stairs data and create physical stairs object.
stairs_data, landing = readXML.read_stairs(settings_name)
stairs = [Stair([stair], landing) for stair in stairs_data]
# Read simulator data.
dynamics_data, sample_data = readXML.read_dynamics(settings_name)
simulator = Simulator(dynamics_data, sample_data)

# Read structure dimensions and create structure.
units, structure_size, radius = readXML.read_structure(settings_name)
gaps = {
    "a": structure_size["a"],
    "b": structure_size["b"],
    "c": structure_size["c"]}
# Generate a mesh with all the possible combination for the parameters a, b
# and c, given a structure size.

# Read margins of the grid.
optimization = read_optimization_data(settings_name)
resolution = optimization['res']
min_size = optimization['min']
max_size = optimization['max']
size = (optimization['width'], optimization['height'])
# Create directory
directory = optimization['dir']
try:
    os.makedirs(directory)
except FileExistsError:
    # If the directory already exits, do nothing.
    pass

logging.basicConfig(level=logging.ERROR, filename=directory + '/errors.log')

sizes = numpy.arange(min_size, max_size + resolution, resolution)
counter = 0
time_title = "t (" + sample_data['time_units'] + ")"
x_title = "a (%s)" % units
y_title = "c (%s)" % units
for s in sizes:
    print("Size %.2f / %.2f:" % (s, max_size))

    try:
        A, C, T = compute_mesh_time(
            s, structure_size, radius, gaps, stairs, simulator, resolution)
    except ValueError:
        continue

    size_title = "L = %.2f %s" % (s, units)
    contour_img = save_contours(A, C, T, size, size_title,
                                time_title, x_title, y_title, 100)
    aux_name = "image%05i.png" % counter
    counter += 1
    image_name = os.path.join(directory, aux_name)
    cv2.imwrite(image_name, contour_img)
print("fin")
