# '''
# Created on 24 mar. 2022
#
# @author: pedrogil
# '''
#
# '''
# Created on 4 mar. 2022
#
# @author: pedrogil
# '''
#
# # NOTE: To include the other project as a external library:
# # - Project/Properties:
# #   - PyDev - PYTHONPATH
# #     - tAB External Libraries -> Add source folder
#
# import sys
# from openpyxl import Workbook
#
#
# from simulator.simulator import Simulator
# from physics.stairs import Stair
# from structure import base
# from simulator.time import compute_time
# import readXML
# from optimize.mesh import generate_mesh_abc
#
# # from optimize.compute_time import ComputeTime
#
#
# def check_max_size(size, wheels):
#     """Check maximum allowed size for the structure.
#
#     """
#     if size['a'] + size['b'] + size['c'] > 150.0:
#         raise ValueError
#
#
# # Open and check settings file.
# try:
#     settings_name = sys.argv[1]
# except Exception:
#     settings_name = "settings.xml"
#
# # Read stairs data and create physical stairs object.
# stairs_data, landing = readXML.read_stairs(settings_name)
# stairs_list = [Stair([stair], landing) for stair in stairs_data]
# # Read simulator data.
# dynamics_data, sample_data = readXML.read_dynamics(settings_name)
# simulator = Simulator(dynamics_data, sample_data)
#
# # Read structure dimensions and create structure.
# structure_size, radius = readXML.read_structure(settings_name)
#
# # self.structure_size = structure_size
# #
# # compute = ComputeTime(stairs_list, simulator,
# #                       structure_size, radius, check_max_size)
#
# wb = Workbook()
# ws = wb.active
#
# d = 50.0
# n = 0
# header_list = []
# result_list = []
#
# for a, b, c, s, cs, ca in generate_mesh_abc(
#         radius, 90.0, 100.0, 2.0, 5.0, 10.0):
#     print(n, "(", a, b, c, ")->", s)
#     n += 1
#     if cs:
#         if len(header_list) == 0:
#             header_list = [s]
#         header_list.append(b)
#     elif len(header_list) > 1:
#         ws.append([])
#         ws.append(header_list)
#         header_list = []
#     if ca:
#         ws.append(result_list)
#         result_list = [a]
#     try:
#         structure_size['a'] = a
#         structure_size['b'] = b
#         structure_size['c'] = c
#         total_time = 0.0
#         for stair in stairs_list:
#             structure = base.Base(structure_size, radius, stair)
#             total_time += compute_time(structure, simulator)
#         result_list.append(total_time)
#     except RuntimeError:
#         result_list.append("Err")
#     except Exception:
#         result_list.append(0.0)
# ws.append(result_list)
#
# wb.save("/home/pedrogil/Escritorio/data.xlsx")
# print("fin")
# #
# #
# # min_value = scipy.optimize.minimize(
# #     compute.compute_time, dimensions, method='Nelder-Mead')
# #
# # print(min_value)
#
# # a_list = []
# # c_list = []
# # t_list = []
# #
# # for a, b, c, s, cs, ca in generate_mesh_abc(
# #         radius, 110.0, 110.0, 1.0, 5.0, 20.0):
# #     print(n, "(", a, b, c, ")->", s)
# #     n += 1
# #     try:
# #         structure_size['a'] = a
# #         structure_size['b'] = b
# #         structure_size['c'] = c
# #         total_time = 0.0
# #         for stair in stairs_list:
# #             structure = base.Base(structure_size, radius, stair)
# #             total_time += compute_time(structure, simulator)
# #         t_list.append(total_time)
# #         a_list.append(a)
# #         c_list.append(c)
# #     except Exception:
# #         pass
# #
# # ax = plt.figure().add_subplot(projection='3d')
# #
# # ax.plot_trisurf(a_list, c_list, t_list, linewidth=0.2, antialiased=True)
# # plt.show(block=True)
# # print("fin")
# #
# #
# # min_value = scipy.optimize.minimize(
# #     compute.compute_time, dimensions, method='Nelder-Mead')
# #
# print(min_value)
#
#
# '''
# Created on 21 mar. 2022
#
# @author: pedrogil
# '''
#
# import numpy
#
#
# def sample_generator(val_min, val_max, resolution):
#     total = int((val_max - val_min) / resolution) + 1
#     for ind in range(total):
#         yield val_min + ind * resolution
#
#
# def generate_mesh_abc(radius, min_size, max_size, resolution, min_gap, gap_b):
#     """Generate a mesh os values varying distances a and c.
#
#     Arguments:
#     radius -- Dictionary with the radius of the wheels (keys: r1, r2, r3, r4).
#     min_size, max_size -- Size of the complete structure (size = a + b + c)
#     resolution -- step of the mesh.
#     min_gap -- Minimum value for the gap between wheels 1-2 and 3-4
#     gap_b -- Minimum value for the gap between wheels 2 and 3.
#
#     """
#     if min_size > max_size:
#         raise ValueError("Minimum sixe must be greater than maximum size.")
#     if min_size < 0:
#         raise ValueError("Sizes must be positive.")
#
#     # Complete distance that occupied by the wheel radius.
#     r_abc = radius['r1'] + 2 * radius['r2'] + 2 * radius['r3'] + radius['r4']
#
#     for size in sample_generator(min_size, max_size, resolution):
#         gaps = size - r_abc - min_gap - gap_b
#         a = gaps + radius['r1'] + radius['r2']
#         c = gaps + radius['r3'] + radius['r4']
#         A, C = numpy.meshgrid(a, c)
#         B = size - A - C
#     # min_size = r_abc + 3 * min_gap + resolution
#         for gap_a in sample_generator(min_gap, max_gap_a, resolution):
#             change_a = True
#             max_gap_c = size - r_abc - gap_a - gap_b
#             for gap_c in sample_generator(min_gap, max_gap_c, resolution):
#                 gap_b = size - r_abc - gap_a - gap_c
#                 a = radius['r1'] + radius['r2'] + gap_a
#                 b = radius['r2'] + radius['r3'] + gap_b
#                 c = radius['r3'] + radius['r4'] + gap_c
#                 yield a, b, c, size, change_size, change_a
#                 change_a = False
#             change_size = False

# '''
# Created on 18 mar. 2022
#
# @author: pedrogil
# '''
#
# import numpy


# def sample_generator(val_min, val_max, resolution):
#     total = int((val_max - val_min) / resolution) + 1
#     for ind in range(total):
#         yield val_min + ind * resolution


# def generate_mesh_abc(radius, max_dim, resolution, gap):
#     a_min = radius['r1'] + radius['r2'] + gap
#     b_min = radius['r2'] + radius['r3'] + gap
#
#     s_max = max_dim
#     s_min = radius['r1'] + radius['r4'] + 2 * (radius['r2'] + radius['r3'])
#     s_min += 3 * gap
#     for s in sample_generator(s_min, s_max, resolution):
#         a_max = s - radius['r4'] - 2 * radius['r3'] - radius['r2'] - gap
#         for a in sample_generator(a_min, a_max, resolution):
#             b_max = s - a - radius['r4'] - radius['r3'] - gap
#             for b in sample_generator(b_min, b_max, resolution):
#                 c = s - a - b
#                 yield a, b, c, s
#


# def generate_mesh_abc(radius, max_dim, resolution, d_value):
#     a_min = radius['r1'] + radius['r2']
#     a_max = max_dim - radius['r4'] - 2 * radius['r3'] - radius['r2']
#     a_tot = int((a_max - a_min) / resolution) + 1
#     for a_ind in range(a_tot):
#         a = resolution * a_ind + a_min
#         b_min = radius['r2'] + radius['r3']
#         b_max = max_dim - a - radius['r4'] - radius['r3']
#         b_tot = int((b_max - b_min) / resolution) + 1
#         for b_ind in range(b_tot):
#             b = resolution * b_ind + b_min
#             c_min = radius['r3'] + radius['r4']
#             c_max = max_dim - a - b
#             c_tot = int((c_max - c_min) / resolution) + 1
#             for c_ind in range(c_tot):
#                 c = resolution * c_ind + c_min
#                 yield a, b, c, d_value


# def generate_mesh_abc(radius, min_size, max_size, resolution, min_gap, gap_b):
#     """Generate a mesh os values varying distances a and c.
#
#     Arguments:
#     radius -- Dictionary with the radius of the wheels (keys: r1, r2, r3, r4).
#     min_size, max_size -- Size of the complete structure (size = a + b + c)
#     resolution -- step of the mesh.
#     min_gap -- Minimum value for the gap between wheels 1-2 and 3-4
#     gap_b -- Minimum value for the gap between wheels 2 and 3.
#
#     """
#     if min_size > max_size:
#         raise ValueError("Minimum sixe must be greater than maximum size.")
#     if min_size < 0:
#         raise ValueError("Sizes must be positive.")
#
#     # Complete distance that occupied by the wheel radius.
#     r_abc = radius['r1'] + 2 * radius['r2'] + 2 * radius['r3'] + radius['r4']
#     # min_size = r_abc + 3 * min_gap + resolution
#     for size in sample_generator(min_size, max_size, resolution):
#         change_size = True
#         max_gap_a = size - r_abc - min_gap - gap_b
#         for gap_a in sample_generator(min_gap, max_gap_a, resolution):
#             change_a = True
#             max_gap_c = size - r_abc - gap_a - gap_b
#             for gap_c in sample_generator(min_gap, max_gap_c, resolution):
#                 gap_b = size - r_abc - gap_a - gap_c
#                 a = radius['r1'] + radius['r2'] + gap_a
#                 b = radius['r2'] + radius['r3'] + gap_b
#                 c = radius['r3'] + radius['r4'] + gap_c
#                 yield a, b, c, size, change_size, change_a
#                 change_a = False
#             change_size = False
