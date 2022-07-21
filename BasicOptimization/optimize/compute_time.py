'''
Created on 4 mar. 2022

@author: pedrogil
'''

import io
import numpy
import cv2
import matplotlib.pyplot as plt
from xml.etree import ElementTree

from structure import base
from simulator.time import compute_time

import logging


def generate_mesh_abc(size, radius, gap_a, gap_b, gap_c, resolution):
    """Generate a mesh with all possible combination of dimensions

    Arguments:
    size -- Size of the structure, that is s = a + b + c.
    gap_a -- Maximum gap between wheels 1 and 2, that is a = r1 + gap_a + r2
    gap_b -- Maximum gap between wheels 2 and 3, that is b = r2 + gap_b + r3
    gap_c -- Maximum gap between wheels 3 and 4, that is c = r3 + gap_c + r4
    resolution -- Resolution of the mesh.

    Returns a (n x n x 4) multidimensional array, with:
    - (n x n) matrix, corresponding to "a" dimension.
    - (n x n) matrix, corresponding to "b" dimension.
    - (n x n) matrix, corresponding to "c" dimension.
    - (n x n)empty matrix, to store the "t" value.

    """
    # Get the radius of the wheels (they can be different).
    r1 = radius["r1"]
    r2 = radius["r2"]
    r3 = radius["r3"]
    r4 = radius["r4"]
    # This is the total size occupied by the wheels.
    r_abc = r1 + 2 * r2 + 2 * r3 + r4
    # This is the maximum value for the a and c gaps
    max_ac = size - r_abc - gap_a - gap_b - gap_c + resolution
    # Array with all the possible values for dimension "a" and "c".
    a = numpy.arange(0, max_ac, resolution) + gap_a + r1 + r2
    c = numpy.arange(0, max_ac, resolution) + gap_c + r3 + r4
    # Create a meshgrid with all possible combination for "a" and "c".
    A, C = numpy.meshgrid(a, c)
    # Dimension b is equal to the size of the structure minus "a" and "c".
    B = size - A - C
    # However, the dimension "b" can not be smaller that the minimum gap.
    min_b = gap_b + r2 + r3
    # And so, mask all non possible values for dimension "b" with nan.
    B[B < min_b] = numpy.nan
    # Finally, construct an aditional array so that the program can have all
    # the values in only one array.
    T = numpy.zeros(A.shape[0:2], numpy.float)
    ABCT = numpy.dstack((A, B, C, T))
    return ABCT


def compute_mesh_time(size, structure_size, radius, gaps, stairs_list,
                      simulator, resolution):

    gap_a = gaps['a']
    gap_b = gaps['b']
    gap_c = gaps['c']
    mesh = generate_mesh_abc(size, radius, gap_a, gap_b, gap_c, resolution)
    # If the size of the mesh in any direction is lower than five, the computation function
    # raise an error, so, we have to check the size before compute any time.
    if mesh.shape[0] < 5:
        raise ValueError
    if mesh.shape[1] < 5:
        raise ValueError

    N = numpy.count_nonzero(~numpy.isnan(mesh[:, :, 1]))

    # N = mesh.shape[0] * (1 + mesh.shape[1]) / 2
    n = 0
    # Run all the values from the mesh, and compute the time for each.
    for ABCT in mesh:
        for abct in ABCT:
            # Note that for some values of a and c, and for a given size, the
            # structure is not possible to be constructed without violating the
            # structure restrictions. In this case, the value for b is set to
            # NaN, and so, this particular combination must not be evaluated.
            if numpy.isnan(abct[1]):
                # And this is fixed by setting the result to nan.
                total_time = numpy.nan
            else:
                try:
                    structure_size['a'] = abct[0]
                    structure_size['b'] = abct[1]
                    structure_size['c'] = abct[2]
                    n += 1
                    print("%i%% \t(%i /\t%i)" %
                          ((100 * n / N), n, N), end='\r')
                    total_time = 0.0
                    for stair in stairs_list:
                        structure = base.Base(structure_size, radius, stair)
                        total_time += compute_time(structure, simulator)
                except ValueError:
                    total_time = numpy.nan
                    logging.error("s: %.2f (a: %.2f, b: %.2f, c: %.2f)" %
                                  (size, abct[0], abct[1], abct[2]))
            # print(structure_size['a'],
            #       structure_size['b'], structure_size['c'], total_time)
            abct[3] = total_time
    print("\n-----")
    # Extract the matrices corresponding to the a and c dimensions (b is not
    # necessary), and the time.
    A = mesh[:, :, 0]
    C = mesh[:, :, 2]
    T = mesh[:, :, 3]
    return A, C, T


def save_contours(A, C, T, size, size_title,
                  time_title, x_title, y_title, dpi):
    """Save a contour image to a png file.

    """
    # # Fix for instance 10 levels for the contour representation.
    # levels = numpy.linspace(numpy.nanmin(T), numpy.nanmax(T), 10)
    # # Plot the contour.
    fig, ax = plt.subplots(figsize=(size[0] / dpi, size[1] / dpi), dpi=dpi)
    cs = ax.contourf(A, C, T)
    ax.set_title(size_title)
    ax.set_xlabel(x_title)
    ax.set_ylabel(y_title)
    # # And show the colorbar at the figure right.
    bar = fig.colorbar(cs)
    bar.ax.set_ylabel(time_title)

    buf = io.BytesIO()
    plt.savefig(buf, format="png")
    plt.close()
    buf.seek(0)
    img_arr = numpy.frombuffer(buf.getvalue(), dtype=numpy.uint8)
    buf.close()
    img = cv2.imdecode(img_arr, 1)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    return img


def read_optimization_data(xml_file):
    """Read list of stairs.

    Returns a list of dictionaries with all the dimensions as required by the
    constructor of class Stair (see physics.py).

    """
    try:
        'Read data structure from XML file'
        element = ElementTree.parse(xml_file)
    except ElementTree.ParseError:
        raise RuntimeError("XML file " + xml_file + " is incorrect.")

    # Read the list of stairs:
    optimization = element.find('optimization')
    margin = {
        'min': float(optimization.attrib['min']),
        'max': float(optimization.attrib['max']),
        'res': float(optimization.attrib['res']),
        'height': float(optimization.attrib['height']),
        'width': float(optimization.attrib['width']),
        'dir': optimization.attrib['dir']}

    return margin


###############################################################################
###############################################################################
###############################################################################
# from structure import base
# from simulator.time import compute_time
#
#
# class ComputeTime:
#
#     def __init__(self, stairs, simulator, structure_size, radius, check_size):
#         self.stairs = stairs
#         self.simulator = simulator
#         self.structure_size = structure_size
#         self.wheels_radius = radius
#         self.check_size = check_size
#         self.counter = 0
#
#     def compute_time(self, dimensions):
#
#         total = 0.0
#         self.structure_size['a'] = dimensions[0]
#         self.structure_size['b'] = dimensions[1]
#         self.structure_size['c'] = dimensions[2]
#         self.structure_size['d'] = dimensions[3]
#         for stair in self.stairs:
#             structure = base.Base(self.structure_size, self.wheels_radius,
#                                   stair, self.check_size)
#             total += compute_time(structure, self.simulator)
#
#         return total
