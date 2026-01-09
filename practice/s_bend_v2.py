# AIST 2026 design script
# created on: 2026/01/09
# last change: 2026/01/09

import gdstk
import numpy as np

lib = gdstk.Library()
top_cell = lib.new_cell("top_cell")

# constants
wg_width = 0.44   # waveguide width (um)
radius = 10      # waveguide bending radius (um)
dr = 0.1         # straight part length
length = 100.0   # S-shape length (um)
offset = 40      # S-shape vertical offset (um)

def horizontal(origin, length, layer):
	path = gdstk.FlexPath((origin), wg_width, layer=layer, datatype=0)
	path.horizontal(length, relative=True)
	origin_next = [
		origin[0] + length,
		origin[1],
	]
	return path, origin_next

def vertical(origin, length, layer):
	path = gdstk.FlexPath((origin), wg_width, layer=layer, datatype=0)
	path.vertical(length, relative=True)
	origin_next = [
		origin[0],
		origin[1] + length,
	]
	return path, origin_next

def arc_RU(origin, layer):
	theta_start, theta_end = -np.pi / 2, 0
	path = gdstk.FlexPath((origin), wg_width, layer=layer, datatype=0)
	path.horizontal(dr, relative=True)
	path.arc(radius, theta_start, theta_end)
	path.vertical(dr, relative=True)
	origin_next = [
		origin[0] + radius + dr,
		origin[1] + radius + dr,
	]
	return path, origin_next

def arc_LU(origin, layer):
	theta_start, theta_end = -np.pi / 2, -np.pi
	path = gdstk.FlexPath((origin), wg_width, layer=layer, datatype=0)
	path.horizontal(-dr, relative=True)
	path.arc(radius, theta_start, theta_end)
	path.vertical(dr, relative=True)
	origin_next = [
		origin[0] - radius - dr,
		origin[1] + radius + dr,
	]
	return path, origin_next

def arc_UR(origin, layer):
	theta_start, theta_end = np.pi, np.pi / 2
	path = gdstk.FlexPath((origin), wg_width, layer=layer, datatype=0)
	path.vertical(dr, relative=True)
	path.arc(radius, theta_start, theta_end)
	path.horizontal(dr, relative=True)
	origin_next = [
		origin[0] + radius + dr,
		origin[1] + radius + dr,
	]
	return path, origin_next

def arc_UL(origin, layer):
	theta_start, theta_end = 0, np.pi / 2
	path = gdstk.FlexPath((origin), wg_width, layer=layer, datatype=0)
	path.vertical(dr, relative=True)
	path.arc(radius, theta_start, theta_end)
	path.horizontal(-dr, relative=True)
	origin_next = [
		origin[0] - radius - dr,
		origin[1] + radius + dr,
	]
	return path, origin_next

def new_sbend_RUR_cell(start, end, layer, cell_name, gdstk_lib):
	sbend_width = end[0] - start[0]
	sbend_height = end[1] - start[1]
	assert sbend_width > 0
	assert sbend_height > 0
	ret_cell = gdstk_lib.new_cell(cell_name)
	o = start
	path, o = horizontal(o, sbend_width/2 - (radius + dr), layer); ret_cell.add(path)
	path, o = arc_RU(o, layer); ret_cell.add(path)
	path, o = vertical(o, sbend_height - 2*(radius + dr), layer); ret_cell.add(path)
	path, o = arc_UR(o, layer); ret_cell.add(path)
	path, o = horizontal(o, sbend_width/2 - (radius + dr), layer); ret_cell.add(path)
	return ret_cell

def new_sbend_LUL_cell(start, end, layer, cell_name, gdstk_lib):
	sbend_width = end[0] - start[0]
	sbend_height = end[1] - start[1]
	assert sbend_width < 0
	assert sbend_height > 0
	ret_cell = gdstk_lib.new_cell(cell_name)
	o = start
	path, o = horizontal(o, sbend_width/2 + (radius + dr), layer); ret_cell.add(path)
	path, o = arc_LU(o, layer); ret_cell.add(path)
	path, o = vertical(o, sbend_height - 2*(radius + dr), layer); ret_cell.add(path)
	path, o = arc_UL(o, layer); ret_cell.add(path)
	path, o = horizontal(o, sbend_width/2 + (radius + dr), layer); ret_cell.add(path)
	return ret_cell

sbend_circle_RUR = new_sbend_RUR_cell([0,0], [length,offset], 1, "sbend_circle_RUR", lib)
sbend_circle_LUL = new_sbend_LUL_cell([length,0], [0,offset], 1, "sbend_circle_LUL", lib)

top_cell.add(gdstk.Reference(sbend_circle_RUR,   origin=(0,   0)))
top_cell.add(gdstk.Reference(sbend_circle_LUL,   origin=(0,-100)))
lib.write_gds("s_bend_v2.gds")
