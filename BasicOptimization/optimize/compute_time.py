'''
Created on 4 mar. 2022

@author: pedrogil
'''
from structure import base
from simulator.time import compute_time


class ComputeTime:

    def __init__(self, stairs, simulator, structure_size, wheels_radius):
        self.stairs = stairs
        self.simulator = simulator
        self.structure_size = structure_size
        self.wheels_radius = wheels_radius

    def compute_time(self, dimensions):

        print(dimensions)
        self.structure_size['a'] = dimensions[0]
        self.structure_size['b'] = dimensions[1]
        self.structure_size['c'] = dimensions[2]
        self.structure_size['d'] = dimensions[3]

        total = 0.0
        for stair in self.stairs:
            structure = base.Base(self.structure_size,
                                  self.wheels_radius, stair)
            total += compute_time(structure, self.simulator)

        return total
