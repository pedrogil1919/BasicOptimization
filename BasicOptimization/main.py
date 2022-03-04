'''
Created on 4 mar. 2022

@author: pedrogil
'''
# NOTE: To include the other project as a external library:
# - Project/Properties:
#   - PyDev - PYTHONPATH
#     - tAB External Libraries -> Add source folder

import scipy.optimize
import sys


from simulator.simulator import Simulator
from physics.stairs import Stair
import readXML

from optimize.compute_time import ComputeTime

# Open and check settings file.
try:
    settings_name = sys.argv[1]
except Exception:
    settings_name = "settings.xml"

# Read simulator data.
dynamics_data, sample_data = readXML.read_dynamics(settings_name)
simulator = Simulator(dynamics_data, sample_data)
# Read stairs data and create physical stairs object.
stairs_data, landing = readXML.read_stairs(settings_name)
stairs_list = [Stair([stair], landing) for stair in stairs_data]
# Read structure dimensions and create structure.
structure_size, wheels_radius = readXML.read_structure(settings_name)
dimensions = [
    structure_size['a'],
    structure_size['b'],
    structure_size['c'],
    structure_size['d'],
]
print(dimensions)

compute = ComputeTime(stairs_list, simulator, structure_size, wheels_radius)

min = scipy.optimize.minimize(
    compute.compute_time, dimensions, method='Nelder-Mead')

print(min)
