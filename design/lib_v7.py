# AIST 2025 design library
# created on: 2026/01/13
# last change: 2026/01/30

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

LAYER_SSC    = 53 # ssc box
LAYER_NODMY  = 60 # no dummy area

# constants
wg_width = 0.44        # waveguide width (um)
radius = 10            # waveguide bending radius (um)
dr = 0.1               # straight part length of bent waveguide (um)
dicing_length = 50     # dicing area length, one-side (um)
ssc_width_small = 0.16 # ssc small width (um)
ssc_length = 100       # ssc length (um)
ssc_pitch = 127        # ssc pitch (um)
label_size = 80        # label text size (um)

RF_PAD_PITCH = 125
RF_PAD_GAP = 9
SIG_width = 16
GAP_width = 5
RF_PAD_size = RF_PAD_PITCH - RF_PAD_GAP
RF_GND_taper_length = 45
RF_SIG_taper_length = RF_GND_taper_length - RF_PAD_GAP
RF_PAD_taper_length = 45
RF_PAD_taper_end = 30.5

PIN_distance = 2*RF_PAD_PITCH - GAP_width - SIG_width

def get_cell_size(cell):
	min_xy, max_xy = cell.bounding_box()
	width = max_xy[0] - min_xy[0]
	height = max_xy[1] - min_xy[1]
	return width, height

def horizontal(origin, length, layer, ret_cell):
	assert np.abs(length) >= 1e-3, f"horizontal(): {length=}" # to avoid empty path
	path = gdstk.FlexPath(origin, wg_width, layer=layer, datatype=0, tolerance=1e-3)
	path.horizontal(length, relative=True)
	origin_next = [
		origin[0] + length,
		origin[1],
	]
	ret_cell.add(path)
	return origin_next

def vertical(origin, length, layer, ret_cell):
	assert np.abs(length) >= 1e-3, f"vertical(): {length=}" # to avoid empty path
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

def new_sbend_RUR_cell(start, end, layer, cell_name):
	sbend_width = end[0] - start[0]
	sbend_height = end[1] - start[1]
	assert sbend_width > 0
	assert sbend_height > 0
	ret_cell = gdstk.Cell(cell_name)
	o = start
	o = horizontal(o, sbend_width/2 - (radius + dr), layer, ret_cell)
	o = arc_RU(o, layer, ret_cell)
	o = vertical(o, sbend_height - 2*(radius + dr), layer, ret_cell)
	o = arc_UR(o, layer, ret_cell)
	o = horizontal(o, sbend_width/2 - (radius + dr), layer, ret_cell)
	return ret_cell

def new_sbend_RDR_cell(start, end, layer, cell_name):
	sbend_width = end[0] - start[0]
	sbend_height = end[1] - start[1]
	assert sbend_width > 0
	assert sbend_height < 0
	ret_cell = gdstk.Cell(cell_name)
	o = start
	o = horizontal(o, sbend_width/2 - (radius + dr), layer, ret_cell)
	o = arc_RD(o, layer, ret_cell)
	o = vertical(o, sbend_height + 2*(radius + dr), layer, ret_cell)
	o = arc_DR(o, layer, ret_cell)
	o = horizontal(o, sbend_width/2 - (radius + dr), layer, ret_cell)
	return ret_cell

def new_sbend_LUL_cell(start, end, layer, cell_name):
	sbend_width = end[0] - start[0]
	sbend_height = end[1] - start[1]
	assert sbend_width < 0
	assert sbend_height > 0
	ret_cell = gdstk.Cell(cell_name)
	o = start
	o = horizontal(o, sbend_width/2 + (radius + dr), layer, ret_cell)
	o = arc_LU(o, layer, ret_cell)
	o = vertical(o, sbend_height - 2*(radius + dr), layer, ret_cell)
	o = arc_UL(o, layer, ret_cell)
	o = horizontal(o, sbend_width/2 + (radius + dr), layer, ret_cell)
	return ret_cell

def new_sbend_LDL_cell(start, end, layer, cell_name):
	sbend_width = end[0] - start[0]
	sbend_height = end[1] - start[1]
	assert sbend_width < 0
	assert sbend_height < 0
	ret_cell = gdstk.Cell(cell_name)
	o = start
	o = horizontal(o, sbend_width/2 + (radius + dr), layer, ret_cell)
	o = arc_LD(o, layer, ret_cell)
	o = vertical(o, sbend_height + 2*(radius + dr), layer, ret_cell)
	o = arc_DL(o, layer, ret_cell)
	o = horizontal(o, sbend_width/2 + (radius + dr), layer, ret_cell)
	return ret_cell

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
		# ssc box
		rect = gdstk.rectangle((-dicing_length, -10), (dicing_length, 10), layer=LAYER_SSC, datatype=0)
		ret_cell.add(rect)
		rect = gdstk.rectangle(( dicing_length, -10), (dicing_length+length, 10), layer=LAYER_SSC, datatype=0)
		ret_cell.add(rect)
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
		# ssc box
		rect = gdstk.rectangle((-length-dicing_length, -10), (-dicing_length, 10), layer=LAYER_SSC, datatype=0)
		ret_cell.add(rect)
		rect = gdstk.rectangle((-dicing_length, -10), (dicing_length, 10), layer=LAYER_SSC, datatype=0)
		ret_cell.add(rect)
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
	# constants
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
	# NODMY
	NODMY_size = 30
	no_dummy = gdstk.rectangle((0, -NODMY_size/2), (NODMY_size, NODMY_size/2), layer=LAYER_NODMY, datatype=0)
	ret_cell.add(no_dummy)
	return ret_cell

def new_RF_PAD_cell():
	ret_cell = gdstk.Cell("RF_PAD")
	origin=(0,0)
	# GSGSG pad
	for i in range(5):
		pad_offset = i - 2
		#----- LAYER_MET = 36 (AlCu contact and metal wire) -----#
		layer = LAYER_MET
		MET_MIDDLE_corner_botleft = [
			- pad_offset*RF_PAD_PITCH - RF_PAD_size/2,
			origin[1] - RF_GND_taper_length - RF_PAD_size
		]
		MET_MIDDLE_corner_topright = [
			- pad_offset*RF_PAD_PITCH + RF_PAD_size/2,
			origin[1] - RF_GND_taper_length
		]
		pad_metal = gdstk.rectangle(MET_MIDDLE_corner_botleft, MET_MIDDLE_corner_topright, layer=layer, datatype=0)
		ret_cell.add(pad_metal)
		#----- LAYER_PW = 41 (AlCu contact and metal wire) -----#
		layer = LAYER_PW
		PW_MIDDLE_corner_botleft = [
			MET_MIDDLE_corner_botleft[0] + 5,
			MET_MIDDLE_corner_botleft[1] + 5,
		]
		PW_MIDDLE_corner_topright = [
			MET_MIDDLE_corner_topright[0] - 5,
			MET_MIDDLE_corner_topright[1] - 5,
		]
		assert RF_PAD_PITCH - (PW_MIDDLE_corner_topright[0]-PW_MIDDLE_corner_botleft[0]) > 4 # design rule
		pad_window = gdstk.rectangle(PW_MIDDLE_corner_botleft, PW_MIDDLE_corner_topright, layer=layer, datatype=0)
		ret_cell.add(pad_window)
	# taper
	#----- LAYER_MET = 36 (AlCu contact and metal wire) -----#
	layer = LAYER_MET
	# left SIG
	taper_left_SIG_botleft  = [ -1*RF_PAD_PITCH - RF_PAD_size/2, origin[1] - RF_GND_taper_length ]
	taper_left_SIG_botright = [ -1*RF_PAD_PITCH + RF_PAD_size/2, origin[1] - RF_GND_taper_length ]
	taper_left_SIG_topleft  = [ -1*RF_PAD_PITCH - RF_PAD_size/2, origin[1] + RF_SIG_taper_length - RF_GND_taper_length ]
	taper_left_SIG_topright = [ -1*RF_PAD_PITCH + RF_PAD_size/2, origin[1] + RF_SIG_taper_length - RF_GND_taper_length ]
	taper_left_SIG = gdstk.rectangle(taper_left_SIG_botleft, taper_left_SIG_topright, layer=layer, datatype=0)
	ret_cell.add(taper_left_SIG) # large pad
	taper_left_SIG_topleft[0]  = -1*RF_PAD_PITCH - SIG_width/2
	taper_left_SIG_topright[0] = -1*RF_PAD_PITCH + SIG_width/2
	taper_left_SIG_botleft  = taper_left_SIG_topleft.copy()
	taper_left_SIG_botright = taper_left_SIG_topright.copy()
	taper_left_SIG_topleft[1]  = origin[1] # returned value
	taper_left_SIG_topright[1] = origin[1] # returned value
	taper_left_SIG = gdstk.rectangle(taper_left_SIG_botleft, taper_left_SIG_topright, layer=layer, datatype=0)
	ret_cell.add(taper_left_SIG) # small pad
	# left GND
	taper_left_GND_botleft  = [ -2*RF_PAD_PITCH - RF_PAD_size/2, origin[1] - RF_GND_taper_length ]
	taper_left_GND_botright = [ -2*RF_PAD_PITCH + RF_PAD_size/2, origin[1] - RF_GND_taper_length ]
	taper_left_GND_topleft  = [ -2*RF_PAD_PITCH - RF_PAD_size/2, origin[1] ]
	taper_left_GND_topright = [ -2*RF_PAD_PITCH + RF_PAD_size/2, origin[1] ]
	taper_left_GND = gdstk.rectangle(taper_left_GND_botleft, taper_left_GND_topright, layer=layer, datatype=0)
	ret_cell.add(taper_left_GND)
	taper_left_GND_topleft[0]  = -2*RF_PAD_PITCH - RF_PAD_size/2 # returned value
	taper_left_GND_topright[0] = taper_left_SIG_topleft[0] - GAP_width # returned value
	# right SIG
	taper_right_SIG_botleft  = [ +1*RF_PAD_PITCH - RF_PAD_size/2, origin[1] - RF_GND_taper_length ]
	taper_right_SIG_botright = [ +1*RF_PAD_PITCH + RF_PAD_size/2, origin[1] - RF_GND_taper_length ]
	taper_right_SIG_topleft  = [ +1*RF_PAD_PITCH - RF_PAD_size/2, origin[1] + RF_SIG_taper_length - RF_GND_taper_length]
	taper_right_SIG_topright = [ +1*RF_PAD_PITCH + RF_PAD_size/2, origin[1] + RF_SIG_taper_length - RF_GND_taper_length]
	taper_right_SIG = gdstk.rectangle(taper_right_SIG_botleft, taper_right_SIG_topright, layer=layer, datatype=0)
	ret_cell.add(taper_right_SIG)
	taper_right_SIG_topleft[0]  = +1*RF_PAD_PITCH - SIG_width/2
	taper_right_SIG_topright[0] = +1*RF_PAD_PITCH + SIG_width/2
	taper_right_SIG_botleft  = taper_right_SIG_topleft.copy()
	taper_right_SIG_botright = taper_right_SIG_topright.copy()
	taper_right_SIG_topleft[1]  = origin[1] # returned value
	taper_right_SIG_topright[1] = origin[1] # returned value
	taper_right_SIG = gdstk.rectangle(taper_right_SIG_botleft, taper_right_SIG_topright, layer=layer, datatype=0)
	ret_cell.add(taper_right_SIG) # small pad
	# right GND
	taper_right_GND_botleft  = [ +2*RF_PAD_PITCH - RF_PAD_size/2, origin[1] - RF_GND_taper_length ]
	taper_right_GND_botright = [ +2*RF_PAD_PITCH + RF_PAD_size/2, origin[1] - RF_GND_taper_length ]
	taper_right_GND_topleft  = [ +2*RF_PAD_PITCH - RF_PAD_size/2, origin[1] ]
	taper_right_GND_topright = [ +2*RF_PAD_PITCH + RF_PAD_size/2, origin[1] ]
	taper_right_GND = gdstk.rectangle(taper_right_GND_botleft, taper_right_GND_topright, layer=layer, datatype=0)
	ret_cell.add(taper_right_GND)
	taper_right_GND_topleft[0]  = taper_right_SIG_topright[0] + GAP_width # returned value
	taper_right_GND_topright[0] = +2*RF_PAD_PITCH + RF_PAD_size/2 # returned value
	# middle GND
	taper_middle_GND_botleft  = [ -RF_PAD_size/2, origin[1] - RF_GND_taper_length ]
	taper_middle_GND_botright = [ +RF_PAD_size/2, origin[1] - RF_GND_taper_length ]
	taper_middle_GND_topleft  = [ -RF_PAD_size/2, origin[1]]
	taper_middle_GND_topright = [ +RF_PAD_size/2, origin[1]]
	taper_middle_GND = gdstk.rectangle(taper_middle_GND_botleft, taper_middle_GND_topright, layer=layer, datatype=0)
	ret_cell.add(taper_middle_GND)
	taper_middle_GND_topleft[0]  = taper_left_SIG_topright[0] + GAP_width # returned value
	taper_middle_GND_topright[0] = taper_right_SIG_topleft[0] - GAP_width # returned value
	# return point
	ret_points = [
		taper_left_GND_topleft, taper_left_GND_topright,
		taper_left_SIG_topleft, taper_left_SIG_topright,
		taper_middle_GND_topleft, taper_middle_GND_topright,
		taper_right_SIG_topleft, taper_right_SIG_topright,
		taper_right_GND_topleft, taper_right_GND_topright,
	]
	return ret_cell, ret_points
RF_PAD_cell, RF_PAD_cell_points = new_RF_PAD_cell()

# => 18Ω based on sheet resistance = 27 Ω/sq + contact 5.56*2=11.1Ω => 29.1Ω
def new_TIN_SERIES_TERM_cell(TIN_width=36, TIN_length=24):
	# top pads
	cell_name = "TIN_SERIES_TERM_30Ohm"
	ret_cell = gdstk.Cell(cell_name)
	pad_origin = (0, 0)
	# CPW pad #
	taper_left_GND_topleft    = RF_PAD_cell_points[0].copy()
	taper_left_GND_topright   = RF_PAD_cell_points[1].copy()
	taper_left_SIG_topleft    = RF_PAD_cell_points[2].copy()
	taper_left_SIG_topright   = RF_PAD_cell_points[3].copy()
	taper_middle_GND_topleft  = RF_PAD_cell_points[4].copy()
	taper_middle_GND_topright = RF_PAD_cell_points[5].copy()
	taper_right_SIG_topleft   = RF_PAD_cell_points[6].copy()
	taper_right_SIG_topright  = RF_PAD_cell_points[7].copy()
	taper_right_GND_topleft   = RF_PAD_cell_points[8].copy()
	taper_right_GND_topright  = RF_PAD_cell_points[9].copy()
	## TiN (left)
	contact_width = 12
	contact_length = 12 # => contact resistance = 8e-6Ωcm^2 / 12e-4 / 12e-4 = 5.56Ω/contact
	gap = 2
	# TIN resistor
	TIN_corner_botleft = [
		-0.5 * TIN_width,
		0,
	]
	TIN_corner_topright = [
		+0.5 * TIN_width,
		TIN_length + contact_length + 2*gap,
	]
	ret_cell.add( gdstk.rectangle(TIN_corner_botleft, TIN_corner_topright, layer=LAYER_TIN, datatype=0))
	# bottom contact
	contact_bot_corner_botleft = [
		- 0.5 * contact_width,
		gap,
	]
	contact_bot_corner_topright = [
		+ 0.5 * contact_width,
		gap + contact_length,
	]
	ret_cell.add( gdstk.rectangle(contact_bot_corner_botleft, contact_bot_corner_topright, layer=LAYER_CT2TIN, datatype=0))
	# top contact
	contact_top_corner_botleft = [
		- 0.5 * contact_width,
		TIN_length + gap,
	]
	contact_top_corner_topright = [
		+ 0.5 * contact_width,
		TIN_length + gap + contact_length,
	]
	ret_cell.add(
		gdstk.rectangle(contact_top_corner_botleft, contact_top_corner_topright, layer=LAYER_CT2TIN, datatype=0)
	)
	ret_size = [TIN_width, TIN_length + contact_length + 2*gap]
	return ret_cell, ret_size
TIN_SERIES_TERM_30Ohm, TIN_SERIES_TERM_30Ohm_size = new_TIN_SERIES_TERM_cell()

def new_CPW_TERM_cell(CPW_length, thermal_isolation_length, cell_name, with_end_pad=False):
	ret_cell = gdstk.Cell(cell_name)
	# RF pad
	ret_cell.add(gdstk.Reference(RF_PAD_cell, origin=(0,0)))
	# CPW pad #
	taper_left_GND_topleft    = RF_PAD_cell_points[0].copy()
	taper_left_GND_topright   = RF_PAD_cell_points[1].copy()
	taper_left_SIG_topleft    = RF_PAD_cell_points[2].copy()
	taper_left_SIG_topright   = RF_PAD_cell_points[3].copy()
	taper_middle_GND_topleft  = RF_PAD_cell_points[4].copy()
	taper_middle_GND_topright = RF_PAD_cell_points[5].copy()
	taper_right_SIG_topleft   = RF_PAD_cell_points[6].copy()
	taper_right_SIG_topright  = RF_PAD_cell_points[7].copy()
	taper_right_GND_topleft   = RF_PAD_cell_points[8].copy()
	taper_right_GND_topright  = RF_PAD_cell_points[9].copy()
	# TIN cell
	TIN_cell, TIN_size = new_TIN_SERIES_TERM_cell()
	ret_cell.add(
		# left TIN
		gdstk.Reference( TIN_cell, origin=[ (taper_left_SIG_topleft[0] + taper_left_SIG_topright[0]) / 2, 0]),
		# right TIN
		gdstk.Reference( TIN_cell, origin=[ (taper_right_SIG_topleft[0] + taper_right_SIG_topright[0]) / 2, 0]),
	)
	# TIN part
	sig_length = SIG_width
	## left GND
	gnd_line_left_corner_botleft  = [ taper_left_GND_topleft[0], taper_left_GND_topleft[1] ]
	gnd_line_left_corner_topright = [ taper_left_GND_topright[0], TIN_size[1] + taper_left_GND_topright[1] ]
	gnd_line_left = gdstk.rectangle(gnd_line_left_corner_botleft, gnd_line_left_corner_topright, layer=LAYER_MET, datatype=0)
	ret_cell.add(gnd_line_left)
	## left SIG
	sig_line_left_corner_botleft  = [ taper_left_SIG_topleft[0], taper_left_SIG_topleft[1] ]
	sig_line_left_corner_topright = [ taper_left_SIG_topright[0], sig_length ]
	sig_line_left = gdstk.rectangle(sig_line_left_corner_botleft, sig_line_left_corner_topright, layer=LAYER_MET, datatype=0)
	ret_cell.add(sig_line_left)
	sig_line_left_corner_botleft  = [ taper_left_SIG_topleft[0], TIN_size[1] - sig_length ]
	sig_line_left_corner_topright = [ taper_left_SIG_topright[0], TIN_size[1] ]
	sig_line_left = gdstk.rectangle(sig_line_left_corner_botleft, sig_line_left_corner_topright, layer=LAYER_MET, datatype=0)
	ret_cell.add(sig_line_left)
	## middle GND
	gnd_line_middle_corner_botleft  = [ taper_middle_GND_topleft[0], taper_middle_GND_topleft[1] ]
	gnd_line_middle_corner_topright = [ taper_middle_GND_topright[0], TIN_size[1] + taper_middle_GND_topright[1] ]
	gnd_line_middle = gdstk.rectangle(gnd_line_middle_corner_botleft, gnd_line_middle_corner_topright, layer=LAYER_MET, datatype=0)
	ret_cell.add(gnd_line_middle)
	## right SIG
	sig_line_right_corner_botleft  = [ taper_right_SIG_topleft[0], taper_right_SIG_topleft[1] ]
	sig_line_right_corner_topright = [ taper_right_SIG_topright[0], sig_length ]
	sig_line_right = gdstk.rectangle(sig_line_right_corner_botleft, sig_line_right_corner_topright, layer=LAYER_MET, datatype=0)
	ret_cell.add(sig_line_right)
	sig_line_right_corner_botleft  = [ taper_right_SIG_topleft[0], TIN_size[1] - sig_length ]
	sig_line_right_corner_topright = [ taper_right_SIG_topright[0], TIN_size[1] ]
	sig_line_right = gdstk.rectangle(sig_line_right_corner_botleft, sig_line_right_corner_topright, layer=LAYER_MET, datatype=0)
	ret_cell.add(sig_line_right)
	## right GND
	gnd_line_right_corner_botleft  = [ taper_right_GND_topleft[0], taper_right_GND_topleft[1] ]
	gnd_line_right_corner_topright = [ taper_right_GND_topright[0], TIN_size[1] ]
	gnd_line_right = gdstk.rectangle(gnd_line_right_corner_botleft, gnd_line_right_corner_topright, layer=LAYER_MET, datatype=0)
	ret_cell.add(gnd_line_right)
	# CPW pad #
	taper_left_GND_topleft[1]    += TIN_size[1]
	taper_left_GND_topright[1]   += TIN_size[1]
	taper_left_SIG_topleft[1]    += TIN_size[1]
	taper_left_SIG_topright[1]   += TIN_size[1]
	taper_middle_GND_topleft[1]  += TIN_size[1]
	taper_middle_GND_topright[1] += TIN_size[1]
	taper_right_SIG_topleft[1]   += TIN_size[1]
	taper_right_SIG_topright[1]  += TIN_size[1]
	taper_right_GND_topleft[1]   += TIN_size[1]
	taper_right_GND_topright[1]  += TIN_size[1]
	# thermal isolation CPW
	## left GND
	gnd_line_left_corner_botleft  = [ taper_left_GND_topleft[0], taper_left_GND_topleft[1] ]
	gnd_line_left_corner_topright = [ taper_left_GND_topright[0], thermal_isolation_length + taper_left_GND_topright[1] ]
	gnd_line_left = gdstk.rectangle(gnd_line_left_corner_botleft, gnd_line_left_corner_topright, layer=LAYER_MET, datatype=0)
	ret_cell.add(gnd_line_left)
	## left SIG
	sig_line_left_corner_botleft  = [ taper_left_SIG_topleft[0], taper_left_SIG_topleft[1] ]
	sig_line_left_corner_topright = [ taper_left_SIG_topright[0], thermal_isolation_length + taper_left_SIG_topright[1] ]
	sig_line_left = gdstk.rectangle(sig_line_left_corner_botleft, sig_line_left_corner_topright, layer=LAYER_MET, datatype=0)
	ret_cell.add(sig_line_left)
	## middle GND
	gnd_line_middle_corner_botleft  = [ taper_middle_GND_topleft[0], taper_middle_GND_topleft[1] ]
	gnd_line_middle_corner_topright = [ taper_middle_GND_topright[0], thermal_isolation_length + taper_middle_GND_topright[1] ]
	gnd_line_middle = gdstk.rectangle(gnd_line_middle_corner_botleft, gnd_line_middle_corner_topright, layer=LAYER_MET, datatype=0)
	ret_cell.add(gnd_line_middle)
	## right SIG
	sig_line_right_corner_botleft  = [ taper_right_SIG_topleft[0], taper_right_SIG_topleft[1] ]
	sig_line_right_corner_topright = [ taper_right_SIG_topright[0], thermal_isolation_length + taper_right_SIG_topright[1] ]
	sig_line_right = gdstk.rectangle(sig_line_right_corner_botleft, sig_line_right_corner_topright, layer=LAYER_MET, datatype=0)
	ret_cell.add(sig_line_right)
	## right GND
	gnd_line_right_corner_botleft  = [ taper_right_GND_topleft[0], taper_right_GND_topleft[1] ]
	gnd_line_right_corner_topright = [ taper_right_GND_topright[0], thermal_isolation_length + taper_right_GND_topright[1] ]
	gnd_line_right = gdstk.rectangle(gnd_line_right_corner_botleft, gnd_line_right_corner_topright, layer=LAYER_MET, datatype=0)
	ret_cell.add(gnd_line_right)
	# CPW pad #
	taper_left_GND_topleft[1]    += thermal_isolation_length
	taper_left_GND_topright[1]   += thermal_isolation_length
	taper_left_SIG_topleft[1]    += thermal_isolation_length
	taper_left_SIG_topright[1]   += thermal_isolation_length
	taper_middle_GND_topleft[1]  += thermal_isolation_length
	taper_middle_GND_topright[1] += thermal_isolation_length
	taper_right_SIG_topleft[1]   += thermal_isolation_length
	taper_right_SIG_topright[1]  += thermal_isolation_length
	taper_right_GND_topleft[1]   += thermal_isolation_length
	taper_right_GND_topright[1]  += thermal_isolation_length
	# CPW waveguide
	## left GND
	gnd_line_left_corner_botleft  = [ taper_left_GND_topleft[0], taper_left_GND_topleft[1] ]
	gnd_line_left_corner_topright = [ taper_left_GND_topright[0], CPW_length + taper_left_GND_topright[1] ]
	gnd_line_left = gdstk.rectangle(gnd_line_left_corner_botleft, gnd_line_left_corner_topright, layer=LAYER_MET, datatype=0)
	ret_cell.add(gnd_line_left)
	## left SIG
	sig_line_left_corner_botleft  = [ taper_left_SIG_topleft[0], taper_left_SIG_topleft[1] ]
	sig_line_left_corner_topright = [ taper_left_SIG_topright[0], CPW_length + taper_left_SIG_topright[1] ]
	sig_line_left = gdstk.rectangle(sig_line_left_corner_botleft, sig_line_left_corner_topright, layer=LAYER_MET, datatype=0)
	ret_cell.add(sig_line_left)
	## middle GND
	gnd_line_middle_corner_botleft  = [ taper_middle_GND_topleft[0], taper_middle_GND_topleft[1] ]
	gnd_line_middle_corner_topright = [ taper_middle_GND_topright[0], CPW_length + taper_middle_GND_topright[1] ]
	gnd_line_middle = gdstk.rectangle(gnd_line_middle_corner_botleft, gnd_line_middle_corner_topright, layer=LAYER_MET, datatype=0)
	ret_cell.add(gnd_line_middle)
	## right SIG
	sig_line_right_corner_botleft  = [ taper_right_SIG_topleft[0], taper_right_SIG_topleft[1] ]
	sig_line_right_corner_topright = [ taper_right_SIG_topright[0], CPW_length + taper_right_SIG_topright[1] ]
	sig_line_right = gdstk.rectangle(sig_line_right_corner_botleft, sig_line_right_corner_topright, layer=LAYER_MET, datatype=0)
	ret_cell.add(sig_line_right)
	## right GND
	gnd_line_right_corner_botleft  = [ taper_right_GND_topleft[0], taper_right_GND_topleft[1] ]
	gnd_line_right_corner_topright = [ taper_right_GND_topright[0], CPW_length + taper_right_GND_topright[1] ]
	gnd_line_right = gdstk.rectangle(gnd_line_right_corner_botleft, gnd_line_right_corner_topright, layer=LAYER_MET, datatype=0)
	ret_cell.add(gnd_line_right)
	# CPW pad #
	if with_end_pad:
		ret_cell.add(gdstk.Reference(RF_PAD_cell, origin=(0, CPW_length + taper_right_GND_topright[1]), x_reflection=True))
	ret_o = [0, TIN_size[1] + thermal_isolation_length]
	return ret_cell, ret_o
def new_PIN_AMZM_GC_cell(PIN_length, cell_name, with_TERM=False, with_end_pad=False):
	ret_cell = gdstk.Cell(cell_name)
	if with_TERM:
		thermal_isolation_length = 100
		CPW_TERM_cell, CPW_TERM_end_o = new_CPW_TERM_cell(PIN_length+1, thermal_isolation_length, cell_name+"_CPW_TERM", with_end_pad=with_end_pad)
		ret_cell.add(gdstk.Reference(CPW_TERM_cell, origin=(0, -CPW_TERM_end_o[1])))
	else:
		CPW_cell = new_CPW_cell(PIN_length+1, cell_name+"_CPW", with_end_pad=with_end_pad)
		ret_cell.add(gdstk.Reference(CPW_cell, origin=(0, 0)))
	PIN, end_o = PIN_structure(PIN_length, [0, -RF_PAD_taper_end], f"PIN_L{PIN_length}")
	## left PIN
	PIN_origin = [-1*RF_PAD_PITCH + SIG_width/2 + GAP_width/2, 0]
	ret_cell.add( gdstk.Reference(PIN, origin=PIN_origin))
	PIN_left_o = PIN_origin.copy()
	## right PIN
	PIN_origin = [+1*RF_PAD_PITCH - SIG_width/2 - GAP_width/2, 0]
	ret_cell.add( gdstk.Reference(PIN, origin=PIN_origin))
	PIN_right_o = PIN_origin.copy()
	## dummy waveguides
	layer = LAYER_SiWG
	MMI2x2_BOTLEFT_CENTER  = [-0.55, 0.0]
	MMI2x2_BOTRIGHT_CENTER = [+0.55, 0.0]
	MMI2x2_TOPLEFT_CENTER  = [-0.55, 41.016]
	MMI2x2_TOPRIGHT_CENTER = [+0.55, 41.016]
	## bot left
	o = [PIN_left_o[0], PIN_left_o[1] - RF_PAD_taper_end]
	o = arc_DR(o, layer, ret_cell)
	h = MMI2x2_TOPLEFT_CENTER[0] - o[0] - (radius+dr)
	o = horizontal(o, h, layer, ret_cell)
	o = arc_RD(o, layer, ret_cell)
	## bot right
	o = [PIN_right_o[0], PIN_right_o[1] - RF_PAD_taper_end]
	o = arc_DL(o, layer, ret_cell)
	h = MMI2x2_TOPRIGHT_CENTER[0] - o[0] + (radius+dr)
	o = horizontal(o, h, layer, ret_cell)
	o = arc_LD(o, layer, ret_cell)
	## bot 2x2 MMI
	ret_cell.add(gdstk.Reference(AIST_PDK["AIST_MMI_2x2"], origin=[o[0]-MMI2x2_BOTRIGHT_CENTER[0], o[1]], x_reflection=True)); o[1] -= MMI2x2_TOPLEFT_CENTER[1]
	MMI_bot_point = o.copy()
	# left end
	o = [MMI_bot_point[0] + 2*MMI2x2_BOTLEFT_CENTER[0], MMI_bot_point[1]]
	o = arc_DL(o, layer, ret_cell)
	h = -RF_PAD_PITCH/2 - o[0] + (radius+dr)
	o = horizontal(o, h, layer, ret_cell)
	o = arc_LD(o, layer, ret_cell)
	# right end
	o = [MMI_bot_point[0], MMI_bot_point[1]]
	o = arc_DR(o, layer, ret_cell)
	h = +RF_PAD_PITCH/2 - o[0] - (radius+dr)
	o = horizontal(o, h, layer, ret_cell)
	o = arc_RD(o, layer, ret_cell)
	## top left
	o = [PIN_left_o[0], PIN_left_o[1] + end_o[1]]
	o = arc_UR(o, layer, ret_cell)
	h = MMI2x2_TOPLEFT_CENTER[0] - o[0] - (radius+dr)
	o = horizontal(o, h, layer, ret_cell)
	o = arc_RU(o, layer, ret_cell)
	## top right
	o = [PIN_right_o[0], PIN_right_o[1] + end_o[1]]
	o = arc_UL(o, layer, ret_cell)
	h = MMI2x2_TOPRIGHT_CENTER[0] - o[0] + (radius+dr)
	o = horizontal(o, h, layer, ret_cell)
	o = arc_LU(o, layer, ret_cell)
	## top 2x2 MMI
	ret_cell.add(gdstk.Reference(AIST_PDK["AIST_MMI_2x2"], origin=[o[0]-MMI2x2_TOPRIGHT_CENTER[0], o[1]])); o[1] += MMI2x2_TOPLEFT_CENTER[1]
	MMI_top_point = o.copy()
	# left end
	o = [MMI_top_point[0] - 2*MMI2x2_TOPRIGHT_CENTER[0], MMI_top_point[1]]
	o = arc_UL(o, layer, ret_cell)
	h = -RF_PAD_PITCH/2 - o[0] + (radius+dr)
	o = horizontal(o, h, layer, ret_cell)
	o = arc_LU(o, layer, ret_cell)
	# right end
	o = [MMI_top_point[0], MMI_top_point[1]]
	o = arc_UR(o, layer, ret_cell)
	h = +RF_PAD_PITCH/2 - o[0] - (radius+dr)
	o = horizontal(o, h, layer, ret_cell)
	o = arc_RU(o, layer, ret_cell)
	ret_o = o.copy()
	# # label
	# label_cell = new_label_cell(f"{PIN_length:.0f}", cell_name+"_label", layer=LAYER_MET)
	# w, h = get_cell_size(label_cell)
	# ret_cell.add(gdstk.Reference(label_cell, origin=(525-h/2, 40+PIN_length/2-w/2), rotation=np.pi/2))
	return ret_cell, ret_o
def new_PIN_AMZM_cell(PIN_length, cell_name):
	# connection points for use
	MZM_BOTLEFT_CENTER = [0.0, +0.55]
	MZM_BOTRIGHT_CENTER = [0.0, -0.55]
	# constants
	MMI2x2_BOTLEFT_CENTER  = [-0.55, 0.0]
	MMI2x2_BOTRIGHT_CENTER = [+0.55, 0.0]
	MMI2x2_TOPLEFT_CENTER  = [-0.55, 41.016]
	MMI2x2_TOPRIGHT_CENTER = [+0.55, 41.016]
	AMZM_total_delay_length = 100 # um, total optical path difference
	AMZM_delayloop_length = AMZM_total_delay_length # delay on one side, total delay is doubled to match AMZM_total_delay_length
	assert AMZM_delayloop_length > 0
	routing_waveguide_pitch = 5
	# PIN cell
	PIN_cell, PIN_end_o = PIN_structure(PIN_length, [0,0], cell_name+"_PIN")
	ret_cell = gdstk.Cell(cell_name)
	# SiWG layer = 30
	layer = LAYER_SiWG
	## 2x2 MMI (bottom)
	o = [0, 0]
	ret_cell.add(gdstk.Reference(AIST_PDK["AIST_MMI_2x2"], origin=o, rotation=-np.pi/2)); o[0] += MMI2x2_TOPLEFT_CENTER[1]
	MMI_top_point = o.copy()
	## 2x2 MMI (bottom) left ports
	o = [MMI_top_point[0], -MMI2x2_BOTLEFT_CENTER[0]]
	o = arc_RU(o, layer, ret_cell)
	TAPER_BOT_LEFT = o.copy() # savepoint for taper (bottom left)
	ret_cell.add(gdstk.Reference(PIN_cell, origin=o))
	o[0] += PIN_end_o[0]
	o[1] += PIN_end_o[1]
	TAPER_TOP_LEFT = o.copy() # savepoint for taper (top left)
	## 2x2 MMI (bottom) right ports
	o = [MMI_top_point[0], -MMI2x2_BOTRIGHT_CENTER[0]]
	o = horizontal(o, RF_PAD_PITCH, layer, ret_cell) # go pad pitch first, then delay loop
	o = arc_RU(o, layer, ret_cell)
	v = np.abs(MMI2x2_BOTLEFT_CENTER[0] - MMI2x2_BOTRIGHT_CENTER[0])
	o = vertical(o, v, layer, ret_cell)
	TAPER_BOT_RIGHT = o.copy() # savepoint for taper (bottom right)
	ret_cell.add(gdstk.Reference(PIN_cell, origin=o, rotation=np.pi, x_reflection=True))
	o[0] += PIN_end_o[0]
	o[1] += PIN_end_o[1]
	TAPER_TOP_RIGHT = o.copy() # savepoint for taper (top right)
	# connect to top MMI
	## 2x2 MMI (top) left ports
	o = TAPER_TOP_LEFT.copy()
	v = np.abs(MMI2x2_BOTLEFT_CENTER[0] - MMI2x2_BOTRIGHT_CENTER[0])
	o = vertical(o, v, layer, ret_cell)
	o = arc_UL(o, layer, ret_cell)
	o = arc_LD(o, layer, ret_cell)
	o = arc_DL(o, layer, ret_cell)
	h = -1 * AMZM_delayloop_length / 2
	o = horizontal(o, h, layer, ret_cell)
	o = arc_LU(o, layer, ret_cell)
	o = vertical(o, routing_waveguide_pitch, layer, ret_cell) # spacing for top MMI and loops
	o = arc_UR(o, layer, ret_cell)
	h = AMZM_delayloop_length / 2
	o = horizontal(o, h, layer, ret_cell)
	o = horizontal(o, RF_PAD_PITCH, layer, ret_cell) # go pad pitch at last
	MMI_bot_point_left = o.copy() # savepoint for top MMI (left port)
	## 2x2 MMI (top) right ports
	o = TAPER_TOP_RIGHT.copy()
	o = arc_UL(o, layer, ret_cell)
	o = arc_LD(o, layer, ret_cell)
	o = arc_DL(o, layer, ret_cell)
	o = arc_LU(o, layer, ret_cell)
	o = vertical(o, routing_waveguide_pitch, layer, ret_cell) # spacing for top MMI and loops
	o = arc_UR(o, layer, ret_cell)
	MMI_bot_point_right = o.copy() # savepoint for top MMI (right port)
	## 2x2 MMI (top)
	o = [
		MMI_bot_point_right[0],
		(MMI_bot_point_left[1] + MMI_bot_point_right[1]) / 2
	]
	ret_cell.add(gdstk.Reference(AIST_PDK["AIST_MMI_2x2"], origin=o, rotation=-np.pi/2)); o[0] += MMI2x2_TOPLEFT_CENTER[1]
	ret_o = o.copy()
	## PIN pad ##
	#----- LAYER_MET = 36 (AlCu contact and metal wire) -----#
	layer = LAYER_MET
	MET_MIDDLE_corner_botleft = [
		TAPER_BOT_LEFT[0] + RF_PAD_GAP/2,
		TAPER_BOT_LEFT[1] + 10 + 20
	]
	MET_MIDDLE_corner_topright = [
		TAPER_BOT_RIGHT[0] - RF_PAD_GAP/2,
		TAPER_BOT_RIGHT[1] + 10 + 20 + PIN_length + 2
	]
	pad_metal = gdstk.rectangle(MET_MIDDLE_corner_botleft, MET_MIDDLE_corner_topright, layer=layer, datatype=0)
	#----- LAYER_PW = 41 (AlCu contact and metal wire) -----#
	layer = LAYER_PW
	PW_MIDDLE_corner_botleft = [
		MET_MIDDLE_corner_botleft[0] + 5,
		MET_MIDDLE_corner_botleft[1] + 5,
	]
	PW_MIDDLE_corner_topright = [
		MET_MIDDLE_corner_topright[0] - 5,
		MET_MIDDLE_corner_topright[1] - 5,
	]
	assert RF_PAD_PITCH - (PW_MIDDLE_corner_topright[0]-PW_MIDDLE_corner_botleft[0]) > 4 # design rule
	pad_window = gdstk.rectangle(PW_MIDDLE_corner_botleft, PW_MIDDLE_corner_topright, layer=layer, datatype=0)
	### create pad cell
	pad_cell = gdstk.Cell(cell_name+"_PIN_PAD")
	pad_cell.add(pad_metal, pad_window)
	### add to ret_cell
	ret_cell.add(
		gdstk.Reference(pad_cell, origin=(-RF_PAD_PITCH*2, 0), columns=5, rows=1, spacing=(RF_PAD_PITCH, 0))
	)
	# label
	label_cell = new_label_cell(f"{PIN_length:.0f}", cell_name+"_label", layer=LAYER_MET)
	w, h = get_cell_size(label_cell)
	ret_cell.add(gdstk.Reference(label_cell, origin=(-250-h/2, 175+PIN_length/2-w/2), rotation=-np.pi/2))
	return ret_cell, ret_o

def new_PIN_AMZM_TERM_cell(PIN_length, cell_name, with_TERM=True, with_end_pad=False):
	# connection points for use
	MZM_BOTLEFT_CENTER = [0.0, +0.55]
	MZM_BOTRIGHT_CENTER = [0.0, -0.55]
	# constants
	MMI2x2_BOTLEFT_CENTER  = [-0.55, 0.0]
	MMI2x2_BOTRIGHT_CENTER = [+0.55, 0.0]
	MMI2x2_TOPLEFT_CENTER  = [-0.55, 41.016]
	MMI2x2_TOPRIGHT_CENTER = [+0.55, 41.016]
	AMZM_total_delay_length = 100 # um, total optical path difference
	AMZM_delayloop_length = AMZM_total_delay_length # delay on one side, total delay is doubled to match AMZM_total_delay_length
	assert AMZM_delayloop_length > 0
	routing_waveguide_pitch = 5
	# PIN cell
	PIN_cell, PIN_end_o = PIN_structure(PIN_length, [0,0], cell_name+"_PIN")
	ret_cell = gdstk.Cell(cell_name)
	# SiWG layer = 30
	layer = LAYER_SiWG
	## 2x2 MMI (bottom)
	o = [0, 0]
	ret_cell.add(gdstk.Reference(AIST_PDK["AIST_MMI_2x2"], origin=o, rotation=-np.pi/2)); o[0] += MMI2x2_TOPLEFT_CENTER[1]
	MMI_top_point = o.copy()
	## 2x2 MMI (bottom) left ports
	o = [MMI_top_point[0], -MMI2x2_BOTLEFT_CENTER[0]]
	o = arc_RU(o, layer, ret_cell)
	TAPER_BOT_LEFT = o.copy() # savepoint for taper (bottom left)
	ret_cell.add(gdstk.Reference(PIN_cell, origin=o))
	o[0] += PIN_end_o[0]
	o[1] += PIN_end_o[1]
	TAPER_TOP_LEFT = o.copy() # savepoint for taper (top left)
	## 2x2 MMI (bottom) right ports
	o = [MMI_top_point[0], -MMI2x2_BOTRIGHT_CENTER[0]]
	o = horizontal(o, PIN_distance, layer, ret_cell) # go PIN distance first, then delay loop
	o = arc_RU(o, layer, ret_cell)
	v = np.abs(MMI2x2_BOTLEFT_CENTER[0] - MMI2x2_BOTRIGHT_CENTER[0])
	o = vertical(o, v, layer, ret_cell)
	TAPER_BOT_RIGHT = o.copy() # savepoint for taper (bottom right)
	ret_cell.add(gdstk.Reference(PIN_cell, origin=o, rotation=np.pi, x_reflection=True))
	o[0] += PIN_end_o[0]
	o[1] += PIN_end_o[1]
	TAPER_TOP_RIGHT = o.copy() # savepoint for taper (top right)
	# connect to top MMI
	## 2x2 MMI (top) left ports
	o = TAPER_TOP_LEFT.copy()
	v = np.abs(MMI2x2_BOTLEFT_CENTER[0] - MMI2x2_BOTRIGHT_CENTER[0])
	o = vertical(o, v, layer, ret_cell)
	o = arc_UL(o, layer, ret_cell)
	o = arc_LD(o, layer, ret_cell)
	o = arc_DL(o, layer, ret_cell)
	h = -1 * AMZM_delayloop_length / 2
	o = horizontal(o, h, layer, ret_cell)
	o = arc_LU(o, layer, ret_cell)
	o = vertical(o, routing_waveguide_pitch, layer, ret_cell) # spacing for top MMI and loops
	o = arc_UR(o, layer, ret_cell)
	h = AMZM_delayloop_length / 2
	o = horizontal(o, h, layer, ret_cell)
	o = horizontal(o, PIN_distance, layer, ret_cell) # go PIN distance at last
	MMI_bot_point_left = o.copy() # savepoint for top MMI (left port)
	## 2x2 MMI (top) right ports
	o = TAPER_TOP_RIGHT.copy()
	o = arc_UL(o, layer, ret_cell)
	o = arc_LD(o, layer, ret_cell)
	o = arc_DL(o, layer, ret_cell)
	o = arc_LU(o, layer, ret_cell)
	o = vertical(o, routing_waveguide_pitch, layer, ret_cell) # spacing for top MMI and loops
	o = arc_UR(o, layer, ret_cell)
	MMI_bot_point_right = o.copy() # savepoint for top MMI (right port)
	## 2x2 MMI (top)
	o = [
		MMI_bot_point_right[0],
		(MMI_bot_point_left[1] + MMI_bot_point_right[1]) / 2
	]
	ret_cell.add(gdstk.Reference(AIST_PDK["AIST_MMI_2x2"], origin=o, rotation=-np.pi/2)); o[0] += MMI2x2_TOPLEFT_CENTER[1]
	ret_o = o.copy()
	## PAD cell
	SIG_GND_line_length = PIN_length + 1
	if with_TERM:
		thermal_isolation_length = 100
		PAD_cell, PAD_end_o = new_CPW_TERM_cell(SIG_GND_line_length, thermal_isolation_length, cell_name+"_PAD", with_end_pad=with_end_pad)
		PAD_origin = [
			(TAPER_BOT_LEFT[0]+TAPER_BOT_RIGHT[0])/2,
			(TAPER_BOT_LEFT[1]+TAPER_BOT_RIGHT[1])/2 + RF_PAD_taper_end - PAD_end_o[1]
		]
		ret_cell.add(gdstk.Reference(PAD_cell, origin=PAD_origin))
	else:
		PAD_cell = new_CPW_cell(SIG_GND_line_length, cell_name+"_PAD", with_end_pad=with_end_pad)
		PAD_origin = [
			(TAPER_BOT_LEFT[0]+TAPER_BOT_RIGHT[0])/2,
			(TAPER_BOT_LEFT[1]+TAPER_BOT_RIGHT[1])/2 + RF_PAD_taper_end
		]
		ret_cell.add(gdstk.Reference(PAD_cell, origin=PAD_origin))
	# # label
	# label_cell = new_label_cell(f"{PIN_length:.0f}", cell_name+"_label", layer=LAYER_MET)
	# w, h = get_cell_size(label_cell)
	# ret_cell.add(gdstk.Reference(label_cell, origin=(420-h/2, 40+PIN_length/2-w/2), rotation=np.pi/2))
	return ret_cell, ret_o

def new_PIN_AMZM_GC_cell(PIN_length, cell_name, with_TERM=False, with_end_pad=False):
	# connection points for use
	MZM_BOTLEFT_CENTER = [0, 0]
	MZM_BOTRIGHT_CENTER = [0.0, -0.55]
	# constants
	MMI1x2_BOT_CENTER  = [0, 0]
	MMI1x2_TOPLEFT_CENTER  = [-0.55, 15.704]
	MMI1x2_TOPRIGHT_CENTER = [+0.55, 15.704]
	AMZM_total_delay_length = 100 # um, total optical path difference
	AMZM_delayloop_length = AMZM_total_delay_length # delay on one side, total delay is doubled to match AMZM_total_delay_length
	assert AMZM_delayloop_length > 0
	routing_waveguide_pitch = 5
	# PIN cell
	PIN_cell, PIN_end_o = PIN_structure(PIN_length, [0,0], cell_name+"_PIN")
	ret_cell = gdstk.Cell(cell_name)
	# SiWG layer = 30
	layer = LAYER_SiWG
	## 1x2 MMI (bottom)
	o = [0, 0]
	ret_cell.add(gdstk.Reference(AIST_PDK["AIST_MMI_1x2"], origin=o, rotation=-np.pi/2)); o[0] += MMI1x2_TOPLEFT_CENTER[1]
	MMI_top_point = o.copy()
	## 1x2 MMI (bottom) left ports
	o = [MMI_top_point[0], -MMI1x2_TOPLEFT_CENTER[0]]
	o = arc_RU(o, layer, ret_cell)
	TAPER_BOT_LEFT = o.copy() # savepoint for taper (bottom left)
	ret_cell.add(gdstk.Reference(PIN_cell, origin=o))
	o[0] += PIN_end_o[0]
	o[1] += PIN_end_o[1]
	TAPER_TOP_LEFT = o.copy() # savepoint for taper (top left)
	## 1x2 MMI (bottom) right ports
	o = [MMI_top_point[0], -MMI1x2_TOPRIGHT_CENTER[0]]
	o = horizontal(o, PIN_distance, layer, ret_cell) # go PIN distance at last
	o = arc_RU(o, layer, ret_cell)
	v = np.abs(MMI1x2_TOPLEFT_CENTER[0] - MMI1x2_TOPRIGHT_CENTER[0])
	o = vertical(o, v, layer, ret_cell)
	TAPER_BOT_RIGHT = o.copy() # savepoint for taper (bottom right)
	ret_cell.add(gdstk.Reference(PIN_cell, origin=o, rotation=np.pi, x_reflection=True))
	o[0] += PIN_end_o[0]
	o[1] += PIN_end_o[1]
	TAPER_TOP_RIGHT = o.copy() # savepoint for taper (top right)
	# connect to top MMI
	## 1x2 MMI (top) left ports
	o = TAPER_TOP_LEFT.copy()
	v = np.abs(MMI1x2_TOPLEFT_CENTER[0] - MMI1x2_TOPRIGHT_CENTER[0])
	o = vertical(o, v, layer, ret_cell)
	o = arc_UL(o, layer, ret_cell)
	o = arc_LD(o, layer, ret_cell)
	o = arc_DL(o, layer, ret_cell)
	h = -1 * AMZM_delayloop_length / 2
	o = horizontal(o, h, layer, ret_cell)
	o = arc_LU(o, layer, ret_cell)
	o = vertical(o, routing_waveguide_pitch, layer, ret_cell) # spacing for top MMI and loops
	o = arc_UR(o, layer, ret_cell)
	h = AMZM_delayloop_length / 2
	o = horizontal(o, h, layer, ret_cell)
	o = horizontal(o, PIN_distance, layer, ret_cell) # go PIN distance at last
	MMI_bot_point_left = o.copy() # savepoint for top MMI (left port)
	## 1x2 MMI (top) right ports
	o = TAPER_TOP_RIGHT.copy()
	o = arc_UL(o, layer, ret_cell)
	o = arc_LD(o, layer, ret_cell)
	o = arc_DL(o, layer, ret_cell)
	o = arc_LU(o, layer, ret_cell)
	o = vertical(o, routing_waveguide_pitch, layer, ret_cell) # spacing for top MMI and loops
	o = arc_UR(o, layer, ret_cell)
	MMI_bot_point_right = o.copy() # savepoint for top MMI (right port)
	## 1x2 MMI (top)
	o = [
		MMI_bot_point_right[0] + MMI1x2_TOPLEFT_CENTER[1],
		(MMI_bot_point_left[1] + MMI_bot_point_right[1]) / 2
	]
	ret_cell.add(gdstk.Reference(AIST_PDK["AIST_MMI_1x2"], origin=o, rotation=np.pi/2))
	ret_o = o.copy()
	## PAD cell
	SIG_GND_line_length = PIN_length + 1
	PAD_cell = new_CPW_cell(SIG_GND_line_length, cell_name+"PAD", with_end_pad=with_end_pad)
	PAD_origin = [
		(TAPER_BOT_LEFT[0]+TAPER_BOT_RIGHT[0])/2,
		(TAPER_BOT_LEFT[1]+TAPER_BOT_RIGHT[1])/2 + RF_PAD_taper_end
	]
	ret_cell.add(gdstk.Reference(PAD_cell, origin=PAD_origin))
	## TIN TERM
	if with_TERM:
		TIN_contact_length = 16 * 2
		TIN_length = 90
		TIN_TERM_origin = [
			PAD_origin[0],
			PAD_origin[1] - RF_PAD_size - TIN_length + TIN_contact_length
		]
		ret_cell.add(gdstk.Reference(TIN_SERIES_TERM_30Ohm, origin=TIN_TERM_origin))
	# # label
	# label_cell = new_label_cell(f"{PIN_length:.0f}", cell_name+"_label", layer=LAYER_MET)
	# w, h = get_cell_size(label_cell)
	# ret_cell.add(gdstk.Reference(label_cell, origin=(560-h/2, 40+PIN_length/2-w/2), rotation=np.pi/2))
	return ret_cell, ret_o

def PIN_structure(PIN_length, start_point, cell_name):
	# LAYER_SiWG   = 30
	# LAYER_RIB    = 40
	# LAYER_NP     = 31 # N+
	# LAYER_PP     = 32 # P+
	# LAYER_NPP    = 33 # N++
	# LAYER_PPP    = 34 # P++
	# LAYER_TIN    = 38 <------ not used here
	# LAYER_CT2PN  = 35 # contact to P++/N++
	# LAYER_CT2TIN = 39 # contact to TiN <------ not used here
	# LAYER_MET    = 36 # AlCu contact and metal wire
	# LAYER_PW     = 41 # probe window
	# LAYER_DW     = 42 # deep window (trench) <------ not used here
	ret_cell = gdstk.Cell(cell_name)
	#----- LAYER_SiWG = 30 -----#
	layer = LAYER_SiWG
	o = start_point.copy()
	# taper (bottom)
	path = gdstk.FlexPath(o, wg_width, layer=layer, datatype=0, tolerance=1e-3)
	path.vertical(10, 0.51, relative=True); o[1] += 10
	ret_cell.add(path)
	path = gdstk.FlexPath(o, 0.51, layer=layer, datatype=0, tolerance=1e-3)
	path.vertical(20, 2.00, relative=True); o[1] += 20
	ret_cell.add(path)
	# rectangle
	path = gdstk.FlexPath(o, 30, layer=layer, datatype=0, tolerance=1e-3)
	path.vertical(PIN_length + 2, relative=True); o[1] += PIN_length + 2
	ret_cell.add(path)
	# taper (top)
	path = gdstk.FlexPath(o, 2.00, layer=layer, datatype=0, tolerance=1e-3)
	path.vertical(20, 0.51, relative=True); o[1] += 20
	ret_cell.add(path)
	path = gdstk.FlexPath(o, 0.51, layer=layer, datatype=0, tolerance=1e-3)
	path.vertical(10, wg_width, relative=True); o[1] += 10
	ret_cell.add(path)
	ret_o = o.copy() # <--- return value of taper end of Si waveguide
	#----- LAYER_RIB = 40 -----#
	layer = LAYER_RIB
	o = start_point.copy()
	rib_start_point = o.copy()
	rib_paths = []
	# taper (rib): 2um wider than waveguide rib
	path = gdstk.FlexPath(o, 2.44, layer=layer, datatype=0, tolerance=1e-3)
	path.vertical(10, 2.51, relative=True); o[1] += 10
	path.vertical(19, 4.00, relative=True); o[1] += 19
	rib_paths.append(path)
	# rectangle (rib)
	path = gdstk.FlexPath(o, 32, layer=layer, datatype=0, tolerance=1e-3)
	path.vertical(PIN_length + 4, relative=True); o[1] += PIN_length + 4
	rib_paths.append(path)
	# taper (rib)
	path = gdstk.FlexPath(o, 4.00, layer=layer, datatype=0, tolerance=1e-3)
	path.vertical(19, 2.51, relative=True); o[1] += 19
	path.vertical(10, 2.44, relative=True); o[1] += 10
	rib_paths.append(path)
	rib_end_point = o.copy()
	# NOT region
	not_path = gdstk.FlexPath(rib_start_point, 0.51, layer=layer, datatype=0, tolerance=1e-3)
	not_path.vertical(np.abs(rib_end_point[1]-rib_start_point[1]), relative=True)
	# Boolean
	rib = gdstk.boolean(rib_paths, not_path, "not", precision=1e-3, layer=layer, datatype=0)
	ret_cell.add(*rib)
	# TODO: N+,N++ should be on the right, and P+,P++ should be on the left -> gdstk.Reference(x_reflection=True, rotation=np.pi)
	#----- LAYER_NP = 31 (N+) -----#
	layer = LAYER_NP
	o = start_point.copy()
	NP_corner_botright = [
		o[0] - 0.5,
		o[1] + 10 + 19 + 1.0 + 0.5
	]
	NP_corner_topleft = [
		NP_corner_botright[0] - 14,
		NP_corner_botright[1] + PIN_length + 1,
	]
	NP_rectangle = gdstk.rectangle(NP_corner_botright, NP_corner_topleft, layer=layer, datatype=0)
	ret_cell.add(NP_rectangle)
	#----- LAYER_PP = 32 (P+) -----#
	layer = LAYER_PP
	o = start_point.copy()
	PP_corner_botleft = [
		o[0] + 0.5,
		o[1] + 10 + 19 + 1.0 + 0.5
	]
	PP_corner_topright = [
		PP_corner_botleft[0] + 14,
		PP_corner_botleft[1] + PIN_length + 1,
	]
	PP_rectangle = gdstk.rectangle(PP_corner_botleft, PP_corner_topright, layer=layer, datatype=0)
	ret_cell.add(PP_rectangle)
	#----- LAYER_NPP = 33 (N++) -----#
	layer = LAYER_NPP
	o = start_point.copy()
	NPP_corner_botright = [
		NP_corner_botright[0] - 0.65,
		NP_corner_botright[1] + 0.5
	]
	NPP_corner_topleft = [
		NP_corner_topleft[0],
		NP_corner_topleft[1] - 0.5,
	]
	assert NPP_corner_topleft[1] - NPP_corner_botright[1] == PIN_length
	NPP_rectangle = gdstk.rectangle(NPP_corner_botright, NPP_corner_topleft, layer=layer, datatype=0)
	ret_cell.add(NPP_rectangle)
	#----- LAYER_PPP = 34 (P++) -----#
	layer = LAYER_PPP
	o = start_point.copy()
	PPP_corner_botleft = [
		PP_corner_botleft[0] + 0.65,
		PP_corner_botleft[1] + 0.5
	]
	PPP_corner_topright = [
		PP_corner_topright[0],
		PP_corner_topright[1] - 0.5,
	]
	assert PPP_corner_topright[1] - PPP_corner_botleft[1] == PIN_length
	PPP_rectangle = gdstk.rectangle(PPP_corner_botleft, PPP_corner_topright, layer=layer, datatype=0)
	ret_cell.add(PPP_rectangle)
	#----- LAYER_CT2PN = 35 (contact to P++/N++) -----#
	layer = LAYER_CT2PN
	o = start_point.copy()
	CT2PN_LEFT_corner_botright = [
		NP_corner_botright[0] - 5.5,
		NP_corner_botright[1] + 0.5 + 1
	]
	CT2PN_LEFT_corner_topleft = [
		NP_corner_topleft[0] + 1.5,
		NP_corner_topleft[1] - 0.5 - 1
	]
	assert np.abs(CT2PN_LEFT_corner_topleft[0] - CT2PN_LEFT_corner_botright[0]) == 7
	assert np.abs(CT2PN_LEFT_corner_topleft[1] - CT2PN_LEFT_corner_botright[1]) == PIN_length - 2
	CT2PN_LEFT_rectangle = gdstk.rectangle(CT2PN_LEFT_corner_botright, CT2PN_LEFT_corner_topleft, layer=layer, datatype=0)
	ret_cell.add(CT2PN_LEFT_rectangle)
	#----- LAYER_CT2PN = 35 (contact to P++/N++) -----#
	layer = LAYER_CT2PN
	o = start_point.copy()
	CT2PN_RIGHT_corner_botleft = [
		PP_corner_botleft[0] + 5.5,
		PP_corner_botleft[1] + 0.5 + 1
	]
	CT2PN_RIGHT_corner_topright = [
		PP_corner_topright[0] - 1.5,
		PP_corner_topright[1] - 0.5 - 1,
	]
	assert np.abs(CT2PN_RIGHT_corner_botleft[0] - CT2PN_RIGHT_corner_topright[0]) == 7
	assert np.abs(CT2PN_RIGHT_corner_botleft[1] - CT2PN_RIGHT_corner_topright[1]) == PIN_length - 2
	CT2PN_RIGHT_rectangle = gdstk.rectangle(CT2PN_RIGHT_corner_botleft, CT2PN_RIGHT_corner_topright, layer=layer, datatype=0)
	ret_cell.add(CT2PN_RIGHT_rectangle)
	return ret_cell, ret_o

# coplanar waveguide for RF probe calibration
def new_CPW_cell(length, cell_name, with_end_pad=True):
	ret_cell = gdstk.Cell(cell_name)
	# CPW pad #
	ret_cell.add(gdstk.Reference(RF_PAD_cell, origin=(0,0)))
	taper_left_GND_topleft    = RF_PAD_cell_points[0].copy()
	taper_left_GND_topright   = RF_PAD_cell_points[1].copy()
	taper_left_SIG_topleft    = RF_PAD_cell_points[2].copy()
	taper_left_SIG_topright   = RF_PAD_cell_points[3].copy()
	taper_middle_GND_topleft  = RF_PAD_cell_points[4].copy()
	taper_middle_GND_topright = RF_PAD_cell_points[5].copy()
	taper_right_SIG_topleft   = RF_PAD_cell_points[6].copy()
	taper_right_SIG_topright  = RF_PAD_cell_points[7].copy()
	taper_right_GND_topleft   = RF_PAD_cell_points[8].copy()
	taper_right_GND_topright  = RF_PAD_cell_points[9].copy()
	# CPW waveguide
	## left GND
	gnd_line_left_corner_botleft  = [ taper_left_GND_topleft[0], taper_left_GND_topleft[1] ]
	gnd_line_left_corner_topright = [ taper_left_GND_topright[0], length + taper_left_GND_topright[1] ]
	gnd_line_left = gdstk.rectangle(gnd_line_left_corner_botleft, gnd_line_left_corner_topright, layer=LAYER_MET, datatype=0)
	ret_cell.add(gnd_line_left)
	## left SIG
	sig_line_left_corner_botleft  = [ taper_left_SIG_topleft[0], taper_left_SIG_topleft[1] ]
	sig_line_left_corner_topright = [ taper_left_SIG_topright[0], length + taper_left_SIG_topright[1] ]
	sig_line_left = gdstk.rectangle(sig_line_left_corner_botleft, sig_line_left_corner_topright, layer=LAYER_MET, datatype=0)
	ret_cell.add(sig_line_left)
	## middle GND
	gnd_line_middle_corner_botleft  = [ taper_middle_GND_topleft[0], taper_middle_GND_topleft[1] ]
	gnd_line_middle_corner_topright = [ taper_middle_GND_topright[0], length + taper_middle_GND_topright[1] ]
	gnd_line_middle = gdstk.rectangle(gnd_line_middle_corner_botleft, gnd_line_middle_corner_topright, layer=LAYER_MET, datatype=0)
	ret_cell.add(gnd_line_middle)
	## right SIG
	sig_line_right_corner_botleft  = [ taper_right_SIG_topleft[0], taper_right_SIG_topleft[1] ]
	sig_line_right_corner_topright = [ taper_right_SIG_topright[0], length + taper_right_SIG_topright[1] ]
	sig_line_right = gdstk.rectangle(sig_line_right_corner_botleft, sig_line_right_corner_topright, layer=LAYER_MET, datatype=0)
	ret_cell.add(sig_line_right)
	## right GND
	gnd_line_right_corner_botleft  = [ taper_right_GND_topleft[0], taper_right_GND_topleft[1] ]
	gnd_line_right_corner_topright = [ taper_right_GND_topright[0], length + taper_right_GND_topright[1] ]
	gnd_line_right = gdstk.rectangle(gnd_line_right_corner_botleft, gnd_line_right_corner_topright, layer=LAYER_MET, datatype=0)
	ret_cell.add(gnd_line_right)
	# CPW pad #
	if with_end_pad:
		ret_cell.add(gdstk.Reference(RF_PAD_cell, origin=(0, length), x_reflection=True))
	return ret_cell

def new_label_cell(text, cell_name, size=label_size, layer=LAYER_MET):
	ret_cell = gdstk.Cell(cell_name)
	# replace error characters
	text = text.replace('0', 'O')
	# replace error characters
	text = gdstk.text(text, size, (0,0), layer=layer, datatype=0)
	ret_cell.add(*text)
	return ret_cell

#-------------------- Routing functions --------------------#

# port position of 2x2 MMI of AMZM
MMI2x2_BOTLEFT_CENTER  = [-0.55, 0.0]
MMI2x2_BOTRIGHT_CENTER = [+0.55, 0.0]

routing_wg_pitch = 5
MZM_routing_height_max = 3500 + 875
MZM_routing_width_max = 1066
MZM_routing_MZM_height_max = 120

GC_routing_width_min = 160 + 50 + (radius+dr)
GC_routing_width_max = 900 + (radius+dr)
GC_routing_height_ssc_min = 3500 + ssc_length + dicing_length + routing_wg_pitch + 2
GC_routing_height_GC_min = 10000 - 1325
GC_routing_height_GC_max = 3500 + 1500

def S_shape_routing(o, layer, ret_cell, ssc_point, wg_offset, dh=0, skip=0):
	h = dh
	if wg_offset > 2 and skip < 1:
		h += ssc_pitch * 4 - 2*(2*radius+dr)
		o = horizontal(o, h, layer, ret_cell)
		o = arc_RD(o, layer, ret_cell)
		o = arc_DR(o, layer, ret_cell)
	if wg_offset > 6 and skip < 2:
		h = ssc_pitch * 4 - 2*(2*radius+dr)
		o = horizontal(o, h, layer, ret_cell)
		o = arc_RD(o, layer, ret_cell)
		o = arc_DR(o, layer, ret_cell)
	if wg_offset > 10 and skip < 3:
		h = ssc_pitch * 4 - 2*(2*radius+dr)
		o = horizontal(o, h, layer, ret_cell)
		o = arc_RD(o, layer, ret_cell)
		o = arc_DR(o, layer, ret_cell)
	if wg_offset > 14 and skip < 4:
		h = ssc_pitch * 4 - 2*(2*radius+dr)
		o = horizontal(o, h, layer, ret_cell)
		o = arc_RD(o, layer, ret_cell)
		o = arc_DR(o, layer, ret_cell)
	if wg_offset > 18 and skip < 5:
		h = ssc_pitch * 4 - 2*(2*radius+dr)
		o = horizontal(o, h, layer, ret_cell)
		o = arc_RD(o, layer, ret_cell)
		o = arc_DR(o, layer, ret_cell)
	if wg_offset > 22 and skip < 6:
		h = ssc_pitch * 6 - 2*(2*radius+dr)
		o = horizontal(o, h, layer, ret_cell)
		o = arc_RD(o, layer, ret_cell)
		o = arc_DR(o, layer, ret_cell)
	return o

# bot left
def PINL500_01_route_cell(origin, end_o, ssc_point, layer, cell_name, right_end):
	ret_cell = gdstk.Cell(cell_name)
	# bot left port
	wg_offset = 0
	o = [
		origin[0] + MMI2x2_BOTLEFT_CENTER[0],
		origin[1],
	]
	o = arc_DL(o, layer, ret_cell)
	o = arc_LD(o, layer, ret_cell)
	v = GC_routing_height_ssc_min - o[1] + (20+wg_offset)*routing_wg_pitch + 2*(radius+dr)
	o = vertical(o, v, layer, ret_cell)
	o = arc_DR(o, layer, ret_cell)
	### bend at SSC for better space efficiency
	dh = 90 - 4.45 + GC_routing_width_min - origin[0] + wg_offset*routing_wg_pitch
	o = S_shape_routing(o, layer, ret_cell, ssc_point, wg_offset+20, dh=dh)
	### bend at SSC for better space efficiency
	h = ssc_point[0] - o[0] - (radius+dr) - (13-wg_offset)*ssc_pitch
	o = horizontal(o, h, layer, ret_cell)
	o = arc_RD(o, layer, ret_cell)
	v = ssc_point[1] - o[1]
	o = vertical(o, v, layer, ret_cell)
	# bot right port
	wg_offset += 1
	o = [
		origin[0] + MMI2x2_BOTRIGHT_CENTER[0],
		origin[1],
	]
	v = GC_routing_height_ssc_min - o[1] + (20+wg_offset)*routing_wg_pitch + 2*(radius+dr)
	o = vertical(o, v, layer, ret_cell)
	o = arc_DR(o, layer, ret_cell)
	### bend at SSC for better space efficiency
	dh = 90 - 4.45 + GC_routing_width_min - origin[0] - 2*(radius+dr) + wg_offset*routing_wg_pitch
	dh -= np.abs(MMI2x2_BOTRIGHT_CENTER[0] - MMI2x2_BOTLEFT_CENTER[0])
	o = S_shape_routing(o, layer, ret_cell, ssc_point, wg_offset+20, dh=dh)
	### bend at SSC for better space efficiency
	h = ssc_point[0] - o[0] - (radius+dr) - (13-wg_offset)*ssc_pitch
	o = horizontal(o, h, layer, ret_cell)
	o = arc_RD(o, layer, ret_cell)
	v = ssc_point[1] - o[1]
	o = vertical(o, v, layer, ret_cell)
	# top right port
	wg_offset += 1
	o = [
		origin[0] - end_o[1] + MMI2x2_BOTRIGHT_CENTER[0],
		origin[1] + end_o[0],
	]
	o = arc_UR(o, layer, ret_cell)
	h_1 = 15 # arbitrary value
	o = horizontal(o, h_1, layer, ret_cell)
	o = arc_RU(o, layer, ret_cell)
	v = 80 # arbitrary value
	o = vertical(o, v, layer, ret_cell)
	o = arc_UR(o, layer, ret_cell)
	h = end_o[1] - 4*(radius+dr) + routing_wg_pitch - h_1
	o = horizontal(o, h, layer, ret_cell)
	o = arc_RD(o, layer, ret_cell)
	v = GC_routing_height_ssc_min - o[1] + (20+wg_offset)*routing_wg_pitch + 2*(radius+dr)
	o = vertical(o, v, layer, ret_cell)
	o = arc_DR(o, layer, ret_cell)
	### bend at SSC for better space efficiency
	dh = 90 - 4.45 + GC_routing_width_min - origin[0] - 2*(radius+dr) + (wg_offset-1)*routing_wg_pitch
	dh -= np.abs(MMI2x2_BOTRIGHT_CENTER[0] - MMI2x2_BOTLEFT_CENTER[0])
	o = S_shape_routing(o, layer, ret_cell, ssc_point, wg_offset+20, dh=dh)
	### bend at SSC for better space efficiency
	h = ssc_point[0] - o[0] - (radius+dr) - (13-wg_offset)*ssc_pitch
	o = horizontal(o, h, layer, ret_cell)
	o = arc_RD(o, layer, ret_cell)
	v = ssc_point[1] - o[1]
	o = vertical(o, v, layer, ret_cell)
	return ret_cell

# bot right
def PINL200_01_route_cell(origin, end_o, ssc_point, layer, cell_name, right_end):
	ret_cell = gdstk.Cell(cell_name)
	# bot left port
	wg_offset = 3
	o = [
		origin[0] + MMI2x2_BOTLEFT_CENTER[0],
		origin[1],
	]
	o = arc_DL(o, layer, ret_cell)
	o = arc_LD(o, layer, ret_cell)
	v = GC_routing_height_ssc_min - o[1] + (20-4+wg_offset)*routing_wg_pitch + 2*(radius+dr)
	o = vertical(o, v, layer, ret_cell)
	o = arc_DR(o, layer, ret_cell)
	### bend at SSC for better space efficiency
	h = 240 - 13.2
	o = horizontal(o, h, layer, ret_cell)
	o = arc_RD(o, layer, ret_cell)
	o = arc_DR(o, layer, ret_cell)
	dh = 0
	o = S_shape_routing(o, layer, ret_cell, ssc_point, wg_offset+24, dh=dh, skip=2)
	### bend at SSC for better space efficiency
	h = ssc_point[0] - o[0] - (radius+dr) - (13-wg_offset)*ssc_pitch
	o = horizontal(o, h, layer, ret_cell)
	o = arc_RD(o, layer, ret_cell)
	v = ssc_point[1] - o[1] # note: v=0 here!!!
	o = vertical(o, v, layer, ret_cell)
	# bot right port
	wg_offset += 1
	o = [
		origin[0] + MMI2x2_BOTRIGHT_CENTER[0],
		origin[1],
	]
	v = GC_routing_height_ssc_min - o[1] + (20-4+wg_offset)*routing_wg_pitch + 2*(radius+dr)
	o = vertical(o, v, layer, ret_cell)
	o = arc_DR(o, layer, ret_cell)
	### bend at SSC for better space efficiency
	h = 240 - 13.2 - 16.1 - 2*(radius+dr) + wg_offset*routing_wg_pitch
	o = horizontal(o, h, layer, ret_cell)
	o = arc_RD(o, layer, ret_cell)
	o = arc_DR(o, layer, ret_cell)
	dh = 0
	o = S_shape_routing(o, layer, ret_cell, ssc_point, wg_offset+24, dh=dh, skip=2)
	### bend at SSC for better space efficiency
	h = ssc_point[0] - o[0] - (radius+dr) - (13-wg_offset)*ssc_pitch
	o = horizontal(o, h, layer, ret_cell)
	o = arc_RD(o, layer, ret_cell)
	v = ssc_point[1] - o[1]
	o = vertical(o, v, layer, ret_cell)
	# top right port
	wg_offset += 1
	o = [
		origin[0] - end_o[1] + MMI2x2_BOTRIGHT_CENTER[0],
		origin[1] + end_o[0],
	]
	o = arc_UR(o, layer, ret_cell)
	o = arc_RU(o, layer, ret_cell)
	v = 80 # arbitrary value
	o = vertical(o, v, layer, ret_cell)
	o = arc_UR(o, layer, ret_cell)
	h = end_o[1] - 4*(radius+dr) + routing_wg_pitch
	o = horizontal(o, h, layer, ret_cell)
	o = arc_RD(o, layer, ret_cell)
	v = GC_routing_height_ssc_min - o[1] + (20-4+wg_offset)*routing_wg_pitch + 2*(radius+dr)
	o = vertical(o, v, layer, ret_cell)
	o = arc_DR(o, layer, ret_cell)
	### bend at SSC for better space efficiency
	h = 240 - 13.2 - 16.1 - 2*(radius+dr) + (wg_offset-1)*routing_wg_pitch
	o = horizontal(o, h, layer, ret_cell)
	o = arc_RD(o, layer, ret_cell)
	o = arc_DR(o, layer, ret_cell)
	dh = 0
	o = S_shape_routing(o, layer, ret_cell, ssc_point, wg_offset+24, dh=dh, skip=2)
	### bend at SSC for better space efficiency
	h = ssc_point[0] - o[0] - (radius+dr) - (13-wg_offset)*ssc_pitch
	o = horizontal(o, h, layer, ret_cell)
	o = arc_RD(o, layer, ret_cell)
	v = ssc_point[1] - o[1]
	o = vertical(o, v, layer, ret_cell)
	return ret_cell

# top left
def PINL100TERM_02_route_cell(origin, end_o, ssc_point, layer, cell_name):
	ret_cell = gdstk.Cell(cell_name)
	# top right port
	wg_offset = 6
	o = [
		origin[0] + end_o[1] - MMI2x2_BOTRIGHT_CENTER[0],
		origin[1] - end_o[0],
	]
	o = arc_DL(o, layer, ret_cell)
	o = arc_LD(o, layer, ret_cell)
	v = MZM_routing_height_max - o[1] + (-6+wg_offset)*routing_wg_pitch + 1*(radius+dr)
	o = vertical(o, v, layer, ret_cell)
	o = arc_DR(o, layer, ret_cell)
	h = MZM_routing_width_max - o[0] + (-8+wg_offset)*routing_wg_pitch
	o = horizontal(o, h, layer, ret_cell)
	o = arc_RD(o, layer, ret_cell)
	v = GC_routing_height_ssc_min - o[1] + (20-4+wg_offset)*routing_wg_pitch + 2*(radius+dr)
	o = vertical(o, v, layer, ret_cell)
	o = arc_DR(o, layer, ret_cell)
	### bend at SSC for better space efficiency
	h = 240 - 35.4
	o = horizontal(o, h, layer, ret_cell)
	o = arc_RD(o, layer, ret_cell)
	o = arc_DR(o, layer, ret_cell)
	dh = 0
	o = S_shape_routing(o, layer, ret_cell, ssc_point, wg_offset+24, dh=dh, skip=2)
	### bend at SSC for better space efficiency
	h = ssc_point[0] - o[0] - (radius+dr) - (13-wg_offset)*ssc_pitch
	o = horizontal(o, h, layer, ret_cell)
	o = arc_RD(o, layer, ret_cell)
	v = ssc_point[1] - o[1]
	o = vertical(o, v, layer, ret_cell)
	# top left port
	wg_offset += 1
	o = [
		origin[0] + end_o[1] + MMI2x2_BOTRIGHT_CENTER[0],
		origin[1] - end_o[0],
	]
	v = MZM_routing_height_max - o[1] + (-6+wg_offset)*routing_wg_pitch + 1*(radius+dr)
	o = vertical(o, v, layer, ret_cell)
	o = arc_DR(o, layer, ret_cell)
	h = MZM_routing_width_max - o[0] + (-8+wg_offset)*routing_wg_pitch
	o = horizontal(o, h, layer, ret_cell)
	o = arc_RD(o, layer, ret_cell)
	v = GC_routing_height_ssc_min - o[1] + (20-4+wg_offset)*routing_wg_pitch + 2*(radius+dr)
	o = vertical(o, v, layer, ret_cell)
	o = arc_DR(o, layer, ret_cell)
	### bend at SSC for better space efficiency
	h = 240 - 35.4 - 14.8 - 2*(radius+dr) + wg_offset*routing_wg_pitch
	o = horizontal(o, h, layer, ret_cell)
	o = arc_RD(o, layer, ret_cell)
	o = arc_DR(o, layer, ret_cell)
	dh = 0
	o = S_shape_routing(o, layer, ret_cell, ssc_point, wg_offset+24, dh=dh, skip=2)
	### bend at SSC for better space efficiency
	h = ssc_point[0] - o[0] - (radius+dr) - (13-wg_offset)*ssc_pitch
	o = horizontal(o, h, layer, ret_cell)
	o = arc_RD(o, layer, ret_cell)
	v = ssc_point[1] - o[1]
	o = vertical(o, v, layer, ret_cell)
	# bot left port
	wg_offset += 1
	o = [
		origin[0] - MMI2x2_BOTLEFT_CENTER[0],
		origin[1],
	]
	o = arc_UR(o, layer, ret_cell)
	h_1 = 15 # arbitrary value
	o = horizontal(o, h_1, layer, ret_cell)
	o = arc_RU(o, layer, ret_cell)
	v = 40 # arbitrary value
	o = vertical(o, v, layer, ret_cell)
	o = arc_UR(o, layer, ret_cell)
	h = end_o[1] - 4*(radius+dr) + routing_wg_pitch - h_1
	o = horizontal(o, h, layer, ret_cell)
	o = arc_RD(o, layer, ret_cell)
	v = MZM_routing_height_max - o[1] + (-6+wg_offset)*routing_wg_pitch + 1*(radius+dr)
	o = vertical(o, v, layer, ret_cell)
	o = arc_DR(o, layer, ret_cell)
	h = MZM_routing_width_max - o[0] + (-8+wg_offset)*routing_wg_pitch
	o = horizontal(o, h, layer, ret_cell)
	o = arc_RD(o, layer, ret_cell)
	v = GC_routing_height_ssc_min - o[1] + (20-4+wg_offset)*routing_wg_pitch + 2*(radius+dr)
	o = vertical(o, v, layer, ret_cell)
	o = arc_DR(o, layer, ret_cell)
	### bend at SSC for better space efficiency
	h = 240 - 35.4 - 14.8 - 2*(radius+dr) + (wg_offset-1)*routing_wg_pitch
	o = horizontal(o, h, layer, ret_cell)
	o = arc_RD(o, layer, ret_cell)
	o = arc_DR(o, layer, ret_cell)
	dh = 0
	o = S_shape_routing(o, layer, ret_cell, ssc_point, wg_offset+24, dh=dh, skip=2)
	### bend at SSC for better space efficiency
	h = ssc_point[0] - o[0] - (radius+dr) - (13-wg_offset)*ssc_pitch
	o = horizontal(o, h, layer, ret_cell)
	o = arc_RD(o, layer, ret_cell)
	v = ssc_point[1] - o[1]
	o = vertical(o, v, layer, ret_cell)
	return ret_cell

# top right
def PINL200TERM_02_route_cell(origin, end_o, ssc_point, layer, cell_name):
	ret_cell = gdstk.Cell(cell_name)
	# top right port
	wg_offset = 9
	o = [
		origin[0] + end_o[1] - MMI2x2_BOTRIGHT_CENTER[0],
		origin[1] - end_o[0],
	]
	o = arc_DL(o, layer, ret_cell)
	o = arc_LD(o, layer, ret_cell)
	v = MZM_routing_height_max - o[1] + (11-wg_offset)*routing_wg_pitch + 1*(radius+dr)
	o = vertical(o, v, layer, ret_cell)
	o = arc_DL(o, layer, ret_cell)
	h = MZM_routing_width_max - o[0] + (-4+wg_offset)*routing_wg_pitch + 2*dr
	o = horizontal(o, h, layer, ret_cell)
	o = arc_LD(o, layer, ret_cell)
	v = GC_routing_height_ssc_min - o[1] + (20-4+wg_offset)*routing_wg_pitch + 2*(radius+dr)
	o = vertical(o, v, layer, ret_cell)
	o = arc_DR(o, layer, ret_cell)
	### bend at SSC for better space efficiency
	h = 220 - 15.4
	o = horizontal(o, h, layer, ret_cell)
	o = arc_RD(o, layer, ret_cell)
	o = arc_DR(o, layer, ret_cell)
	dh = 0
	o = S_shape_routing(o, layer, ret_cell, ssc_point, wg_offset+24, dh=dh, skip=2)
	### bend at SSC for better space efficiency
	h = ssc_point[0] - o[0] - (radius+dr) - (13-wg_offset)*ssc_pitch
	o = horizontal(o, h, layer, ret_cell)
	o = arc_RD(o, layer, ret_cell)
	v = ssc_point[1] - o[1]
	o = vertical(o, v, layer, ret_cell)
	# top left port
	wg_offset += 1
	o = [
		origin[0] + end_o[1] + MMI2x2_BOTRIGHT_CENTER[0],
		origin[1] - end_o[0],
	]
	v = MZM_routing_height_max - o[1] + (11-wg_offset)*routing_wg_pitch + 1*(radius+dr)
	o = vertical(o, v, layer, ret_cell)
	o = arc_DL(o, layer, ret_cell)
	h = MZM_routing_width_max - o[0] + (-4+wg_offset)*routing_wg_pitch + 2*dr
	o = horizontal(o, h, layer, ret_cell)
	o = arc_LD(o, layer, ret_cell)
	v = GC_routing_height_ssc_min - o[1] + (20-4+wg_offset)*routing_wg_pitch + 2*(radius+dr)
	o = vertical(o, v, layer, ret_cell)
	o = arc_DR(o, layer, ret_cell)
	### bend at SSC for better space efficiency
	h = 220 - 15.4 - 29.8 - 2*(radius+dr) + wg_offset*routing_wg_pitch
	o = horizontal(o, h, layer, ret_cell)
	o = arc_RD(o, layer, ret_cell)
	o = arc_DR(o, layer, ret_cell)
	dh = 0
	o = S_shape_routing(o, layer, ret_cell, ssc_point, wg_offset+24, dh=dh, skip=2)
	### bend at SSC for better space efficiency
	h = ssc_point[0] - o[0] - (radius+dr) - (13-wg_offset)*ssc_pitch
	o = horizontal(o, h, layer, ret_cell)
	o = arc_RD(o, layer, ret_cell)
	v = ssc_point[1] - o[1]
	o = vertical(o, v, layer, ret_cell)
	# bot left port
	wg_offset += 1
	o = [
		origin[0] - MMI2x2_BOTLEFT_CENTER[0],
		origin[1],
	]
	o = arc_UR(o, layer, ret_cell)
	o = arc_RU(o, layer, ret_cell)
	v = 40 # arbitrary value
	o = vertical(o, v, layer, ret_cell)
	o = arc_UR(o, layer, ret_cell)
	h = end_o[1] - 4*(radius+dr) + routing_wg_pitch
	o = horizontal(o, h, layer, ret_cell)
	o = arc_RD(o, layer, ret_cell)
	v = MZM_routing_height_max - o[1] + (11-wg_offset)*routing_wg_pitch + 1*(radius+dr)
	o = vertical(o, v, layer, ret_cell)
	o = arc_DL(o, layer, ret_cell)
	h = MZM_routing_width_max - o[0] + (-4+wg_offset)*routing_wg_pitch + 2*dr
	o = horizontal(o, h, layer, ret_cell)
	o = arc_LD(o, layer, ret_cell)
	v = GC_routing_height_ssc_min - o[1] + (20-4+wg_offset)*routing_wg_pitch + 2*(radius+dr)
	o = vertical(o, v, layer, ret_cell)
	o = arc_DR(o, layer, ret_cell)
	### bend at SSC for better space efficiency
	h = 220 - 15.4 - 29.8 - 2*(radius+dr) + (wg_offset-1)*routing_wg_pitch
	o = horizontal(o, h, layer, ret_cell)
	o = arc_RD(o, layer, ret_cell)
	o = arc_DR(o, layer, ret_cell)
	dh = 0
	o = S_shape_routing(o, layer, ret_cell, ssc_point, wg_offset+24, dh=dh, skip=2)
	### bend at SSC for better space efficiency
	h = ssc_point[0] - o[0] - (radius+dr) - (13-wg_offset)*ssc_pitch
	o = horizontal(o, h, layer, ret_cell)
	o = arc_RD(o, layer, ret_cell)
	v = ssc_point[1] - o[1]
	o = vertical(o, v, layer, ret_cell)
	return ret_cell

# bot right right
def PINL50GC_03_route_cell(origin, end_o, layer, cell_name):
	ret_cell = gdstk.Cell(cell_name)
	GC_length = 217
	# top port
	o = [
		origin[0] + end_o[1],
		origin[1] - end_o[0],
	]
	o = arc_DR(o, layer, ret_cell)
	o = arc_RU(o, layer, ret_cell)
	v = 80
	o = vertical(o, v, layer, ret_cell)
	o = arc_UR(o, layer, ret_cell)
	o = arc_RD(o, layer, ret_cell)
	ret_cell.add(gdstk.Reference(AIST_PDK["AIST_GC"], origin=[o[0], o[1]-GC_length], rotation=np.pi/2))
	# bot port
	o = [
		origin[0],
		origin[1],
	]
	v = 60
	o = vertical(o, v, layer, ret_cell)
	o = arc_UR(o, layer, ret_cell)
	h = 130 + 8.3
	o = horizontal(o, h, layer, ret_cell)
	o = arc_RD(o, layer, ret_cell)
	v = -180
	o = vertical(o, v, layer, ret_cell)
	o = arc_DR(o, layer, ret_cell)
	o = arc_RU(o, layer, ret_cell)
	ret_cell.add(gdstk.Reference(AIST_PDK["AIST_GC"], origin=[o[0], o[1]+GC_length], rotation=-np.pi/2))
	return ret_cell


# GC 4x4 routing
def GC4x4_route_cell(origin, GC_pitch, ssc_point, layer, cell_name):
	ret_cell = gdstk.Cell(cell_name)
	for i in range(4): # row
		for j in range(4): # column
			wg_offset = i*4 + j
			o = [
				origin[0] + (3-j) * GC_pitch,
				origin[1] + (3-i) * GC_pitch,
			]
			o = arc_LU(o, layer, ret_cell)
			v = + 10 + (3-j)*routing_wg_pitch
			o = vertical(o, v, layer, ret_cell)
			o = arc_UL(o, layer, ret_cell)
			h = GC_routing_width_min - o[0] + wg_offset*routing_wg_pitch
			o = horizontal(o, h, layer, ret_cell)
			o = arc_LD(o, layer, ret_cell)
			### bend in Sherry region for better space efficiency
			v = (3500+1500) - o[1] - wg_offset*routing_wg_pitch
			o = vertical(o, v, layer, ret_cell)
			o = arc_DL(o, layer, ret_cell)
			h = -(GC_routing_width_min - 50 - routing_wg_pitch - 3*(radius+dr)) # 5 um from dicing line
			o = horizontal(o, h, layer, ret_cell)
			o = arc_LD(o, layer, ret_cell)
			### bend in Sherry region for better space efficiency
			v = GC_routing_height_ssc_min - o[1] + wg_offset*routing_wg_pitch + 2*(radius+dr)
			o = vertical(o, v, layer, ret_cell)
			o = arc_DR(o, layer, ret_cell)
			### bend at SSC for better space efficiency
			dh = 350 - GC_routing_width_min
			o = S_shape_routing(o, layer, ret_cell, ssc_point, wg_offset, dh=dh)
			### bend at SSC for better space efficiency
			h = ssc_point[0] - o[0] - (radius+dr) + (2+wg_offset)*ssc_pitch
			o = horizontal(o, h, layer, ret_cell)
			o = arc_RD(o, layer, ret_cell)
			v = ssc_point[1] - o[1]
			o = vertical(o, v, layer, ret_cell)
	return ret_cell

# GC 4x1 routing
def GC4x1output_route_cell(origin, GC_pitch, ssc_point, layer, cell_name):
	ret_cell = gdstk.Cell(cell_name)
	for i in range(4): # row
		wg_offset = i + 16
		o = [
			origin[0],
			origin[1] + (3-i) * GC_pitch,
		]
		o = arc_DL(o, layer, ret_cell)
		h = GC_routing_width_min - o[0] + wg_offset*routing_wg_pitch
		o = horizontal(o, h, layer, ret_cell)
		o = arc_LD(o, layer, ret_cell)
		### bend in Sherry region for better space efficiency
		v = (3500+1500) - o[1] - wg_offset*routing_wg_pitch
		o = vertical(o, v, layer, ret_cell)
		o = arc_DL(o, layer, ret_cell)
		h = -(GC_routing_width_min - 50 - routing_wg_pitch - 3*(radius+dr)) # 5 um from dicing line
		o = horizontal(o, h, layer, ret_cell)
		o = arc_LD(o, layer, ret_cell)
		### bend in Sherry region for better space efficiency
		v = GC_routing_height_ssc_min - o[1] + wg_offset*routing_wg_pitch + 2*(radius+dr)
		o = vertical(o, v, layer, ret_cell)
		o = arc_DR(o, layer, ret_cell)
		### bend at SSC for better space efficiency
		dh = 350 - GC_routing_width_min
		o = S_shape_routing(o, layer, ret_cell, ssc_point, wg_offset, dh=dh)
		### bend at SSC for better space efficiency
		h = ssc_point[0] - o[0] - (radius+dr) + (2+wg_offset)*ssc_pitch
		o = horizontal(o, h, layer, ret_cell)
		o = arc_RD(o, layer, ret_cell)
		v = ssc_point[1] - o[1]
		o = vertical(o, v, layer, ret_cell)
	return ret_cell

# GC 1x4 routing
def GC1x4input_route_cell(origin, GC_pitch, layer, cell_name,
						PINL500_01_origin, PINL200_01_origin, PINL100TERM_02_origin, PINL200TERM_02_origin,
						pin_mzm_L500_end_o, pin_mzm_L200_end_o, pin_mzm_L100_TERM_end_o, pin_mzm_L200_TERM_end_o):
	ret_cell = gdstk.Cell(cell_name)
	top_ends = []
	for j in range(4): # col
		wg_offset = j + 16 + 4
		o = [
			origin[0] + j * GC_pitch,
			origin[1],
		]
		o = arc_LD(o, layer, ret_cell)
		v = - 20 + (wg_offset-20)*routing_wg_pitch # note: v=0 here!!!
		o = vertical(o, v, layer, ret_cell)
		o = arc_DR(o, layer, ret_cell)
		h = GC_routing_width_max - o[0] + (wg_offset-20)*routing_wg_pitch
		o = horizontal(o, h, layer, ret_cell)
		o = arc_RD(o, layer, ret_cell)
		v = GC_routing_height_GC_min - o[1] - (wg_offset-20)*routing_wg_pitch
		o = vertical(o, v, layer, ret_cell)
		o = arc_DL(o, layer, ret_cell)
		h = GC_routing_width_min - o[0] + wg_offset*routing_wg_pitch
		o = horizontal(o, h, layer, ret_cell)
		o = arc_LD(o, layer, ret_cell)
		if j >= 2:
			v = (3500+1500+20) - o[1]
			o = vertical(o, v, layer, ret_cell)
		else:
			### bend in Sherry region for better space efficiency
			v = (3500+1500) - o[1] - wg_offset*routing_wg_pitch
			o = vertical(o, v, layer, ret_cell)
			o = arc_DL(o, layer, ret_cell)
			h = -(GC_routing_width_min - 50 - routing_wg_pitch - 3*(radius+dr)) # 5 um from dicing line
			o = horizontal(o, h, layer, ret_cell)
			o = arc_LD(o, layer, ret_cell)
			### bend in Sherry region for better space efficiency
		top_ends.append(o.copy())
	v_3 = -97 # arbitrary value
	v_1 = -607 # arbitrary value
	# PINL200TERM_02_origin
	o = top_ends[3]
	right_end = PINL200TERM_02_origin.copy()
	right_end[0] -= np.abs(MMI2x2_BOTLEFT_CENTER[0])
	o = arc_DR(o, layer, ret_cell)
	h = right_end[0] - o[0] - 1*(radius+dr)
	o = horizontal(o, h, layer, ret_cell)
	o = arc_RD(o, layer, ret_cell)
	v = right_end[1] - o[1]
	o = vertical(o, v, layer, ret_cell)
	# PINL100TERM_02_origin
	o = top_ends[2]
	right_end = PINL100TERM_02_origin.copy()
	right_end[0] -= np.abs(MMI2x2_BOTLEFT_CENTER[0])
	v = - routing_wg_pitch
	o = vertical(o, v, layer, ret_cell)
	o = arc_DR(o, layer, ret_cell)
	h = right_end[0] - o[0] - 1*(radius+dr)
	o = horizontal(o, h, layer, ret_cell)
	o = arc_RD(o, layer, ret_cell)
	v = right_end[1] - o[1]
	o = vertical(o, v, layer, ret_cell)
	# PINL200_01_origin
	o = top_ends[1]
	right_end = PINL200_01_origin.copy()
	right_end[0] -= pin_mzm_L200_end_o[1]
	right_end[0] -= np.abs(MMI2x2_BOTLEFT_CENTER[0])
	right_end[1] += pin_mzm_L200_end_o[0]
	v = v_1 # arbitrary value
	o = vertical(o, v, layer, ret_cell)
	o = arc_DR(o, layer, ret_cell)
	h = right_end[0] - o[0] - 1*(radius+dr)
	o = horizontal(o, h, layer, ret_cell)
	o = arc_RD(o, layer, ret_cell)
	v = right_end[1] - o[1]
	o = vertical(o, v, layer, ret_cell)
	# PINL500_01_origin
	o = top_ends[0]
	right_end = PINL500_01_origin.copy()
	right_end[0] -= pin_mzm_L500_end_o[1]
	right_end[0] -= np.abs(MMI2x2_BOTLEFT_CENTER[0])
	right_end[1] += pin_mzm_L500_end_o[0]
	v = -1*(radius+dr-dr) # here only radius is enough
	v += v_1 # arbitrary value
	o = vertical(o, v, layer, ret_cell)
	o = arc_DR(o, layer, ret_cell)
	h = 12 # arbitrary value
	o = horizontal(o, h, layer, ret_cell)
	o = arc_RD(o, layer, ret_cell)
	o = arc_DL(o, layer, ret_cell)
	h = right_end[0] - o[0] + 1*(radius+dr)
	assert h < 0
	o = horizontal(o, h, layer, ret_cell)
	o = arc_LD(o, layer, ret_cell)
	v = right_end[1] - o[1]
	o = vertical(o, v, layer, ret_cell)
	return ret_cell

#-------------------- Passive test patterns  --------------------#

def passive_test_patterns(origin, ssc_right, loop_right, GC_cell, cell_name):
	ret_cell = gdstk.Cell(cell_name)
	# constants
	MMI1x2_BOT_CENTER  = [0, 0]
	MMI1x2_TOPLEFT_CENTER  = [-0.55, 15.704]
	MMI1x2_TOPRIGHT_CENTER = [+0.55, 15.704]
	GC_length = 217
	ssc_minor_pitch = 40
	minor_origin = [origin[0], origin[1] - 50]
	#----- ssc and loops -----#
	# ssc
	ret_cell.add(
		gdstk.Reference(
			ssc_right,
			origin=[origin[0], origin[1] + 1*ssc_pitch],
			columns=1, rows=7, spacing=(0, ssc_pitch)
		),
		gdstk.Reference(
			ssc_right,
			origin=[minor_origin[0], minor_origin[1] + ssc_minor_pitch],
			columns=1, rows=3, spacing=(0, ssc_minor_pitch)
		),
	)
	# loop
	ret_cell.add(
		gdstk.Reference(
			loop_right, rotation=np.pi,
			origin=[ origin[0] - ssc_length - dicing_length, origin[1] + 7*ssc_pitch ],
			columns=1, rows=2, spacing=(0, 5*ssc_pitch)
		),
	)
	#----- 1x2 MMI -----#
	layer = LAYER_SiWG
	o = [
		origin[0] - ssc_length - dicing_length,
		origin[1] + 3*ssc_pitch
	]
	h = -10
	o = horizontal(o, h, layer, ret_cell)
	o = arc_LU(o, layer, ret_cell)
	v = 30
	o = vertical(o, v, layer, ret_cell)
	ret_cell.add(gdstk.Reference(AIST_PDK["AIST_MMI_1x2"], origin=o)); o[1] += MMI1x2_TOPLEFT_CENTER[1]
	MMI_top_point = o.copy()
	# top left port
	o = [MMI_top_point[0] + MMI1x2_TOPLEFT_CENTER[0], MMI_top_point[1]]
	end_point = [origin[0] - ssc_length - dicing_length, origin[1] + 5*ssc_pitch]
	o = arc_UL(o, layer, ret_cell)
	o = arc_LU(o, layer, ret_cell)
	v = end_point[1] - o[1] - (radius+dr)
	o = vertical(o, v, layer, ret_cell)
	o = arc_UR(o, layer, ret_cell)
	h = end_point[0] - o[0]
	o = horizontal(o, h, layer, ret_cell)
	# top right port
	o = [MMI_top_point[0] + MMI1x2_TOPRIGHT_CENTER[0], MMI_top_point[1]]
	end_point = [origin[0] - ssc_length - dicing_length, origin[1] + 4*ssc_pitch]
	v = end_point[1] - o[1] - (radius+dr)
	o = vertical(o, v, layer, ret_cell)
	o = arc_UR(o, layer, ret_cell)
	h = end_point[0] - o[0]
	o = horizontal(o, h, layer, ret_cell)
	#----- GC test ports -----#
	# AIST GC
	o = [
		minor_origin[0] - ssc_length - dicing_length,
		minor_origin[1] + 3*ssc_minor_pitch
	]
	h = -10
	o = horizontal(o, h, layer, ret_cell)
	ret_cell.add(gdstk.Reference(AIST_PDK["AIST_GC"], origin=[o[0]-GC_length, o[1]]))
	# Ren GC w/ NODMY
	o = [
		minor_origin[0] - ssc_length - dicing_length,
		minor_origin[1] + 2*ssc_minor_pitch
	]
	h = -100
	o = horizontal(o, h, layer, ret_cell)
	ret_cell.add(gdstk.Reference(GC_cell, origin=o, rotation=-np.pi))
	# Ren GC w/o NODMY
	GC_cell_woNODMY = GC_cell.copy(GC_cell.name+"_woNODMY")
	remove_layer = 60 # NODMY
	for poly in list(GC_cell_woNODMY.polygons):
		if poly.layer == remove_layer:
			GC_cell_woNODMY.remove(poly)
	for path in list(GC_cell_woNODMY.paths):
		if path.layers == remove_layer:
			GC_cell_woNODMY.remove(path)
	for label in list(GC_cell_woNODMY.labels):
		if label.layer == remove_layer:
			GC_cell_woNODMY.remove(label)
	o = [
		minor_origin[0] - ssc_length - dicing_length,
		minor_origin[1] + 1*ssc_minor_pitch
	]
	h = -100
	o = horizontal(o, h, layer, ret_cell)
	ret_cell.add(gdstk.Reference(GC_cell_woNODMY, origin=o, rotation=-np.pi))
	#----- LAYER_MET = 36 -----#
	# label
	size = label_size
	label_index = 0
	o = [
		origin[0],
		origin[1] + 1*ssc_pitch
	]
	# loop back
	for i in range(2):
		pos = [
			o[0] - dicing_length - ssc_length,
			o[1] + 10 + label_index*ssc_pitch
		]
		text = f"{label_index}"
		text = text.replace('0', 'O')
		text = gdstk.text(text, size, pos, layer=LAYER_MET)
		ret_cell.add(*text)
		label_index += 1
	# 1x2 MMI
	for j in range(3):
		pos = [
			o[0] - dicing_length - ssc_length,
			o[1] + 10 + label_index*ssc_pitch
		]
		# if   j == 0: text = f"{label_index}o"
		# elif j == 1: text = f"{label_index}iR"
		# elif j == 2: text = f"{label_index}iL"
		text = f"{label_index}"
		text = text.replace('0', 'O')
		text = gdstk.text(text, size, pos, layer=LAYER_MET)
		ret_cell.add(*text)
		label_index += 1
	# loop back
	for i in range(2):
		pos = [
			o[0] - dicing_length - ssc_length,
			o[1] + 10 + label_index*ssc_pitch
		]
		text = f"{label_index}"
		text = text.replace('0', 'O')
		text = gdstk.text(text, size, pos, layer=LAYER_MET)
		ret_cell.add(*text)
		label_index += 1
	return ret_cell

#---------- SSC labels ----------#
def port_number(n):
	binary = f"{n:06b}"
	binary = binary.replace('0', '-')
	binary = binary.replace('1', 'X')
	return binary

def new_ssc_labels_cell(ssc_right_origin, cell_name):
	ret_cell = gdstk.Cell(cell_name)
	o = [
		ssc_right_origin[0] + 10,
		ssc_right_origin[1] + dicing_length + ssc_length
	]
	size = label_size
	#----- LAYER_MET = 36 -----#
	label_index = 0
	# loop back
	for i in range(2):
		pos = [
			o[0] - label_index*ssc_pitch,
			o[1]
		]
		label_cell = new_label_cell(f"{label_index}", cell_name+f"_{label_index}", size=size, layer=LAYER_MET)
		# number = gdstk.text(port_number(label_index), size, (0,size), layer=LAYER_MET)
		# label_cell.add(*number)
		ret_cell.add(gdstk.Reference(label_cell, origin=pos, rotation=-np.pi/2))
		label_index += 1
	# AMZM-L200-TERM (top right)
	for j in range(3):
		pos = [
			o[0] - label_index*ssc_pitch,
			o[1]
		]
		text = f"{label_index}"
		# if   j == 0: text = f"{label_index}TRo"
		# elif j == 1: text = f"{label_index}TRiR"
		# elif j == 2: text = f"{label_index}TRiL"
		label_cell = new_label_cell(text, cell_name+f"_{label_index}", size=size, layer=LAYER_MET)
		# number = gdstk.text(port_number(label_index), size, (0,size), layer=LAYER_MET)
		# label_cell.add(*number)
		ret_cell.add(gdstk.Reference(label_cell, origin=pos, rotation=-np.pi/2))
		label_index += 1
	# AMZM-L100-TERM (top left)
	for j in range(3):
		pos = [
			o[0] - label_index*ssc_pitch,
			o[1]
		]
		text = f"{label_index}"
		# if   j == 0: text = f"{label_index}TLo"
		# elif j == 1: text = f"{label_index}TLiR"
		# elif j == 2: text = f"{label_index}TLiL"
		label_cell = new_label_cell(text, cell_name+f"_{label_index}", size=size, layer=LAYER_MET)
		# number = gdstk.text(port_number(label_index), size, (0,size), layer=LAYER_MET)
		# label_cell.add(*number)
		ret_cell.add(gdstk.Reference(label_cell, origin=pos, rotation=-np.pi/2))
		label_index += 1
	# AMZM-L200 (bot right)
	for j in range(3):
		pos = [
			o[0] - label_index*ssc_pitch,
			o[1]
		]
		text = f"{label_index}"
		# if   j == 0: text = f"{label_index}BRo"
		# elif j == 1: text = f"{label_index}BRiR"
		# elif j == 2: text = f"{label_index}BRiL"
		label_cell = new_label_cell(text, cell_name+f"_{label_index}", size=size, layer=LAYER_MET)
		# number = gdstk.text(port_number(label_index), size, (0,size), layer=LAYER_MET)
		# label_cell.add(*number)
		ret_cell.add(gdstk.Reference(label_cell, origin=pos, rotation=-np.pi/2))
		label_index += 1
	# AMZM-L100 (bot left)
	for j in range(3):
		pos = [
			o[0] - label_index*ssc_pitch,
			o[1]
		]
		text = f"{label_index}"
		# if   j == 0: text = f"{label_index}BLo"
		# elif j == 1: text = f"{label_index}BLiR"
		# elif j == 2: text = f"{label_index}BLiL"
		label_cell = new_label_cell(text, cell_name+f"_{label_index}", size=size, layer=LAYER_MET)
		# number = gdstk.text(port_number(label_index), size, (0,size), layer=LAYER_MET)
		# label_cell.add(*number)
		ret_cell.add(gdstk.Reference(label_cell, origin=pos, rotation=-np.pi/2))
		label_index += 1
	# loop back
	for i in range(2):
		pos = [
			o[0] - label_index*ssc_pitch,
			o[1]
		]
		label_cell = new_label_cell(f"{label_index}", cell_name+f"_{label_index}", size=size, layer=LAYER_MET)
		# number = gdstk.text(port_number(label_index), size, (0,size), layer=LAYER_MET)
		# label_cell.add(*number)
		ret_cell.add(gdstk.Reference(label_cell, origin=pos, rotation=-np.pi/2))
		label_index += 1
	# GC 4x1 output
	for i in range(4):
		pos = [
			o[0] - label_index*ssc_pitch,
			o[1]
		]
		text = f"{label_index}"
		label_origin = pos
		number_origin = (0, size)
		# if i == 0:
			# text += "B" # bottom
		if i == 3:
			label_index += 1
			continue
			# text += "T" # top
			# label_origin = [pos[0] - 70 + 2.5, pos[1]] # to avoid dicing line
			# number_origin = (0, size - 9)
		label_cell = new_label_cell(text, cell_name+f"_{label_index}", size=size, layer=LAYER_MET)
		# number = gdstk.text(port_number(label_index), size, number_origin, layer=LAYER_MET)
		# label_cell.add(*number)
		ret_cell.add(gdstk.Reference(label_cell, origin=label_origin, rotation=-np.pi/2))
		label_index += 1
	# GC 4x4 array
	for i in range(4): # row (bottom to top in GC array)
		for j in range(4): # column (left to right in GC array)
			pos = [
				o[0] - label_index*ssc_pitch,
				o[1]
			]
			text = f"{label_index}"
			label_origin = pos
			# if j == 0:
				# text += "L" # left
			# if j == 3:
				# text += "R" # right
			label_cell = new_label_cell(text, cell_name+f"_{label_index}", size=size, layer=LAYER_MET)
			# number = gdstk.text(port_number(label_index), size, (0,size), layer=LAYER_MET)
			# label_cell.add(*number)
			ret_cell.add(gdstk.Reference(label_cell, origin=label_origin, rotation=-np.pi/2))
			label_index += 1
	# loop back
	for i in range(2):
		pos = [
			o[0] - label_index*ssc_pitch,
			o[1]
		]
		label_cell = new_label_cell(f"{label_index}", cell_name+f"_{label_index}", size=size, layer=LAYER_MET)
		# number = gdstk.text(port_number(label_index), size, (0,size), layer=LAYER_MET)
		# label_cell.add(*number)
		ret_cell.add(gdstk.Reference(label_cell, origin=pos, rotation=-np.pi/2))
		label_index += 1
	return ret_cell
