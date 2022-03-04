'''
Created on 4 mar. 2022

@author: pedrogil
'''

from simulator.time import ComputeTime

# Imports needed for the testing block.
import sys
from physics.stairs import Stair
import readXML

# Open and check settings file.
try:
    settings_name = sys.argv[1]
except Exception:
    settings_name = "settings.xml"

# Read stairs data and create physical stairs object.
stairs_list, landing = readXML.read_stairs(settings_name)
stair = Stair(stairs_list, landing)

# for st in stairs_list:
#     st['h'] = -st['h']
# stair2 = Stair(stairs_list, landing)
# stair = (stair, stair2)

# Read structure dimensions and create structure.
structure_size, wheels_radius = readXML.read_structure(settings_name)
# Read simulator data.
dynamics_data, sample_data = readXML.read_dynamics(settings_name)
compute_time = ComputeTime(wheels_radius, stair, dynamics_data, sample_data)
total = compute_time.compute(structure_size)
print("Total:", total, sample_data['time_units'])
