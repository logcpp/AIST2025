# AIST 2026 design script
# created on: 2026/01/09
# last change: 2026/01/09

import gdstk
import numpy as np

AIST_PDK = gdstk.read_rawcells("../PDK_Device_Cells_20251112.gds")

lib = gdstk.Library()
top_cell = gdstk.Cell("top_cell")

# design rule
LAYER_Si = 30

# constants
wg_width = 0.44   # waveguide width (um)
radius = 10      # waveguide bending radius (um)
dr = 0.1         # straight part length
dicing_length = 50 # dicing area length, one-side (um)
ssc_width_small = 0.16 # ssc small width (um)
ssc_length = 100 # ssc length (um)
sbend_length = 100   # S-shape length (um)
sbend_offset = 40      # S-shape vertical offset (um)

def get_cell_size(cell):
	min_xy, max_xy = cell.bounding_box()
	width = max_xy[0] - min_xy[0]
	height = max_xy[1] - min_xy[1]
	return width, height

def horizontal(origin, length, layer):
	path = gdstk.FlexPath(origin, wg_width, layer=layer, datatype=0)
	path.horizontal(length, relative=True)
	origin_next = [
		origin[0] + length,
		origin[1],
	]
	return path, origin_next

def vertical(origin, length, layer):
	path = gdstk.FlexPath(origin, wg_width, layer=layer, datatype=0)
	path.vertical(length, relative=True)
	origin_next = [
		origin[0],
		origin[1] + length,
	]
	return path, origin_next

def arc_RU(origin, layer):
	theta_start, theta_end = -np.pi / 2, 0
	path = gdstk.FlexPath(origin, wg_width, layer=layer, datatype=0)
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
	path = gdstk.FlexPath(origin, wg_width, layer=layer, datatype=0)
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
	path = gdstk.FlexPath(origin, wg_width, layer=layer, datatype=0)
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
	path = gdstk.FlexPath(origin, wg_width, layer=layer, datatype=0)
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
	ret_cell = gdstk.Cell(cell_name)
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
	ret_cell = gdstk.Cell(cell_name)
	o = start
	path, o = horizontal(o, sbend_width/2 + (radius + dr), layer); ret_cell.add(path)
	path, o = arc_LU(o, layer); ret_cell.add(path)
	path, o = vertical(o, sbend_height - 2*(radius + dr), layer); ret_cell.add(path)
	path, o = arc_UL(o, layer); ret_cell.add(path)
	path, o = horizontal(o, sbend_width/2 + (radius + dr), layer); ret_cell.add(path)
	return ret_cell

def new_ssc_cell(layer, cell_name, gdstk_lib, position='left'):
	length = ssc_length # um
	width_small = ssc_width_small # um
	width_large = wg_width # um
	ret_cell = gdstk.Cell(cell_name)
	if position == 'left':
		path = gdstk.FlexPath((-dicing_length, 0), width_small, layer=layer, datatype=0)
		path.horizontal(dicing_length, relative=True)
		ret_cell.add(path)
		path = gdstk.FlexPath((0, 0), width_small, layer=layer, datatype=0)
		path.horizontal(dicing_length, relative=True)
		ret_cell.add(path)
		path = gdstk.FlexPath((dicing_length, 0), width_small, layer=layer, datatype=0)
		path.horizontal(length, width=width_large, relative=True)
		ret_cell.add(path)
	else:
		path = gdstk.FlexPath((0, 0), width_large, layer=layer, datatype=0)
		path.horizontal(length, width=width_small, relative=True)
		ret_cell.add(path)
		path = gdstk.FlexPath((length, 0), width_small, layer=layer, datatype=0)
		path.horizontal(dicing_length, relative=True)
		ret_cell.add(path)
		path = gdstk.FlexPath((0, 0), width_small, layer=layer, datatype=0)
		path.horizontal(dicing_length, relative=True)
		ret_cell.add(path)
	return ret_cell

ssc_left = new_ssc_cell(LAYER_Si, 'ssc_left', lib, position='left')
ssc_right = new_ssc_cell(LAYER_Si, 'ssc_right', lib, position='right')
sbend_circle_RUR = new_sbend_RUR_cell([0,0], [sbend_length,sbend_offset], LAYER_Si, 'sbend_circle_RUR', lib)
sbend_circle_LUL = new_sbend_LUL_cell([sbend_length,-sbend_offset], [0,0], LAYER_Si, 'sbend_circle_LUL', lib)

o = [0,0]
top_cell.add(gdstk.Reference(ssc_left, origin=o)); o[0] += dicing_length + ssc_length
top_cell.add(gdstk.Reference(sbend_circle_RUR, origin=o)); o[0] += sbend_length; o[1] += sbend_offset
top_cell.add(gdstk.Reference(AIST_PDK["AIST_MODPNL1000AMZ11HT"], origin=[o[0]-38.696,o[1]], rotation=-np.pi/2)); o[0] += 1691.808
top_cell.add(gdstk.Reference(sbend_circle_LUL, origin=o)); o[0] += sbend_length; o[1] -= sbend_offset
top_cell.add(gdstk.Reference(ssc_right, origin=o)); o[0] += ssc_length + dicing_length

lib.add(top_cell, *top_cell.dependencies(True))
lib.write_gds("pin_mzm.gds")
