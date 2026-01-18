# AIST 2025 design library
# created on: 2026/01/13
# last change: 2026/01/13

import gdstk
import numpy as np

AIST_PDK = gdstk.read_rawcells("../PDK_Device_Cells_20251112.gds")
LIB = gdstk.Library()

# design rule
LAYER_SiWG   = 30
LAYER_RIB    = 40
LAYER_NP     = 31 # N+
LAYER_PP     = 32 # P+
LAYER_NPP    = 33 # N++
LAYER_PPP    = 34 # P++
LAYER_TIN    = 38
LAYER_CT2PN  = 35 # contact to P++/N++
LAYER_CT2TIN = 39 # contact to TiN
LAYER_MET    = 36 # AlCu contact and metal wire
LAYER_PW     = 41 # probe window
LAYER_DW     = 42 # deep window (trench)

# constants
wg_width = 0.44        # waveguide width (um)
radius = 10            # waveguide bending radius (um)
dr = 0.1               # straight part length of bent waveguide (um)
dicing_length = 50     # dicing area length, one-side (um)
ssc_width_small = 0.16 # ssc small width (um)
ssc_length = 100       # ssc length (um)
ssc_pitch = 50         # ssc pitch (um)

def get_cell_size(cell):
	min_xy, max_xy = cell.bounding_box()
	width = max_xy[0] - min_xy[0]
	height = max_xy[1] - min_xy[1]
	return width, height

def horizontal(origin, length, layer, ret_cell):
	path = gdstk.FlexPath(origin, wg_width, layer=layer, datatype=0, tolerance=1e-3)
	path.horizontal(length, relative=True)
	origin_next = [
		origin[0] + length,
		origin[1],
	]
	ret_cell.add(path)
	return origin_next

def vertical(origin, length, layer, ret_cell):
	path = gdstk.FlexPath(origin, wg_width, layer=layer, datatype=0, tolerance=1e-3)
	path.vertical(length, relative=True)
	origin_next = [
		origin[0],
		origin[1] + length,
	]
	ret_cell.add(path)
	return origin_next

def arc_RU(origin, layer, ret_cell):
	theta_start, theta_end = -np.pi / 2, 0
	path = gdstk.FlexPath(origin, wg_width, layer=layer, datatype=0, tolerance=1e-3)
	path.horizontal(dr, relative=True)
	path.arc(radius, theta_start, theta_end)
	path.vertical(dr, relative=True)
	origin_next = [
		origin[0] + radius + dr,
		origin[1] + radius + dr,
	]
	ret_cell.add(path)
	return origin_next

def arc_RD(origin, layer, ret_cell):
	theta_start, theta_end = np.pi / 2, 0
	path = gdstk.FlexPath(origin, wg_width, layer=layer, datatype=0, tolerance=1e-3)
	path.horizontal(dr, relative=True)
	path.arc(radius, theta_start, theta_end)
	path.vertical(-dr, relative=True)
	origin_next = [
		origin[0] + radius + dr,
		origin[1] - radius - dr,
	]
	ret_cell.add(path)
	return origin_next

def arc_LU(origin, layer, ret_cell):
	theta_start, theta_end = -np.pi / 2, -np.pi
	path = gdstk.FlexPath(origin, wg_width, layer=layer, datatype=0, tolerance=1e-3)
	path.horizontal(-dr, relative=True)
	path.arc(radius, theta_start, theta_end)
	path.vertical(dr, relative=True)
	origin_next = [
		origin[0] - radius - dr,
		origin[1] + radius + dr,
	]
	ret_cell.add(path)
	return origin_next

def arc_LD(origin, layer, ret_cell):
	theta_start, theta_end = np.pi / 2, np.pi
	path = gdstk.FlexPath(origin, wg_width, layer=layer, datatype=0, tolerance=1e-3)
	path.horizontal(-dr, relative=True)
	path.arc(radius, theta_start, theta_end)
	path.vertical(-dr, relative=True)
	origin_next = [
		origin[0] - radius - dr,
		origin[1] - radius - dr,
	]
	ret_cell.add(path)
	return origin_next

def arc_UR(origin, layer, ret_cell):
	theta_start, theta_end = np.pi, np.pi / 2
	path = gdstk.FlexPath(origin, wg_width, layer=layer, datatype=0, tolerance=1e-3)
	path.vertical(dr, relative=True)
	path.arc(radius, theta_start, theta_end)
	path.horizontal(dr, relative=True)
	origin_next = [
		origin[0] + radius + dr,
		origin[1] + radius + dr,
	]
	ret_cell.add(path)
	return origin_next

def arc_DR(origin, layer, ret_cell):
	theta_start, theta_end = -np.pi, -np.pi / 2
	path = gdstk.FlexPath(origin, wg_width, layer=layer, datatype=0, tolerance=1e-3)
	path.vertical(-dr, relative=True)
	path.arc(radius, theta_start, theta_end)
	path.horizontal(dr, relative=True)
	origin_next = [
		origin[0] + radius + dr,
		origin[1] - radius - dr,
	]
	ret_cell.add(path)
	return origin_next

def arc_UL(origin, layer, ret_cell):
	theta_start, theta_end = 0, np.pi / 2
	path = gdstk.FlexPath(origin, wg_width, layer=layer, datatype=0, tolerance=1e-3)
	path.vertical(dr, relative=True)
	path.arc(radius, theta_start, theta_end)
	path.horizontal(-dr, relative=True)
	origin_next = [
		origin[0] - radius - dr,
		origin[1] + radius + dr,
	]
	ret_cell.add(path)
	return origin_next

def arc_DL(origin, layer, ret_cell):
	theta_start, theta_end = 0, -np.pi / 2
	path = gdstk.FlexPath(origin, wg_width, layer=layer, datatype=0, tolerance=1e-3)
	path.vertical(-dr, relative=True)
	path.arc(radius, theta_start, theta_end)
	path.horizontal(-dr, relative=True)
	origin_next = [
		origin[0] - radius - dr,
		origin[1] - radius - dr,
	]
	ret_cell.add(path)
	return origin_next
def new_ssc_cell(layer, cell_name, position='left'):
	length = ssc_length # um
	width_small = ssc_width_small # um
	width_large = wg_width # um
	ret_cell = gdstk.Cell(cell_name)
	if position == 'left':
		path = gdstk.FlexPath((-dicing_length, 0), width_small, layer=layer, datatype=0, tolerance=1e-3)
		path.horizontal(dicing_length, relative=True)
		ret_cell.add(path)
		path = gdstk.FlexPath((0, 0), width_small, layer=layer, datatype=0, tolerance=1e-3)
		path.horizontal(dicing_length, relative=True)
		ret_cell.add(path)
		path = gdstk.FlexPath((dicing_length, 0), width_small, layer=layer, datatype=0, tolerance=1e-3)
		path.horizontal(length, width=width_large, relative=True)
		ret_cell.add(path)
	else:
		path = gdstk.FlexPath((-length-dicing_length, 0), width_large, layer=layer, datatype=0, tolerance=1e-3)
		path.horizontal(length, width=width_small, relative=True)
		ret_cell.add(path)
		path = gdstk.FlexPath((-dicing_length, 0), width_small, layer=layer, datatype=0, tolerance=1e-3)
		path.horizontal(dicing_length, relative=True)
		ret_cell.add(path)
		path = gdstk.FlexPath((0, 0), width_small, layer=layer, datatype=0, tolerance=1e-3)
		path.horizontal(dicing_length, relative=True)
		ret_cell.add(path)
	return ret_cell

def new_loopback_cell(straight_length, layer, cell_name):
	ret_cell = gdstk.Cell(cell_name)
	o = (0, 0)
	o = horizontal(o, straight_length, layer, ret_cell)
	o = arc_RU(o, layer, ret_cell)
	o = vertical(o, ssc_pitch-2*(radius+dr), layer, ret_cell)
	o = arc_UL(o, layer, ret_cell)
	o = horizontal(o, -straight_length, layer, ret_cell)
	return ret_cell

def new_GC_cell(grating_num, grating_pitch, angle_deg, taper_length, cell_name):
	ret_cell = gdstk.Cell(cell_name)
	# Si taper
	layer = LAYER_SiWG
	o = (0, 0)
	# path = gdstk.FlexPath(o, wg_width, layer=layer, datatype=0, tolerance=1e-3)
	# angle_rad = angle_deg / 180 * np.pi
	# taper_end_width = (np.tan(angle_rad / 2) * taper_length) * 2 + wg_width 
	# path.horizontal(taper_length, taper_end_width, relative=True)
	grating_duty = 0.5
	angle_rad = angle_deg / 180 * np.pi
	taper_start = wg_width/2 / np.tan(angle_rad/2)
	radius = taper_start + taper_length + grating_pitch * grating_num
	# curve
	curve = gdstk.Curve((0,0), tolerance=1e-3)
	curve.segment((radius,0), True)
	curve.arc(radius, 0, angle_rad, 0)
	polygon = gdstk.Polygon(curve.points())
	polygon.rotate(-angle_rad/2)
	polygon.translate((-taper_start, 0))
	# region to remove
	path = gdstk.FlexPath((-taper_start, 0), wg_width, layer=layer, datatype=0, tolerance=1e-3)
	path.horizontal(taper_start, relative=True)
	# Si taper
	si_taper = gdstk.boolean(polygon, path, "not", precision=1e-3, layer=layer, datatype=0)
	ret_cell.add(*si_taper)
	# Rib arcs
	layer = LAYER_RIB
	# angle_rad = (angle_deg+10) / 180 * np.pi
	radius = taper_length
	rib_width = grating_pitch * grating_duty
	for i in range(grating_num):
		r = radius + rib_width / 2
		angle_rad_start = angle_rad/2 + 1.5/r
		angle_rad_end = -(angle_rad/2 + 1.5/r)
		start_point = [r*np.cos(angle_rad_start), r*np.sin(angle_rad_start)]
		path = gdstk.FlexPath(start_point, rib_width, layer=layer, datatype=0, tolerance=1e-3)
		path.arc(r, angle_rad_start, angle_rad_end)
		ret_cell.add(path)
		radius += grating_pitch
	return ret_cell

top_cell = gdstk.Cell("top_cell")

GC_T20P0_6A35L10 = new_GC_cell(20, 0.6, 35, 10, "GC_T20P0.6A35L10")

top_cell.add(gdstk.Reference(GC_T20P0_6A35L10, origin=(0,0)))

LIB.add(top_cell, *top_cell.dependencies(True))
LIB.write_gds("GC.gds")
