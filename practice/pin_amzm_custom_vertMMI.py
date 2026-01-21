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

def new_PIN_AMZM_cell(PIN_length, cell_name):
	# connection points for use
	MZM_BOTLEFT_CENTER = [0.0, +0.55]
	MZM_BOTRIGHT_CENTER = [0.0, -0.55]
	# constants
	MMI2x2_BOTLEFT_CENTER  = [-0.55, 0.0]
	MMI2x2_BOTRIGHT_CENTER = [+0.55, 0.0]
	MMI2x2_TOPLEFT_CENTER  = [-0.55, 41.016]
	MMI2x2_TOPRIGHT_CENTER = [+0.55, 41.016]
	RF_PAD_PITCH = 125
	AMZM_total_delay_length = 100 # um, total optical path difference
	AMZM_refloop_length = 20
	AMZM_delayloop_length = AMZM_total_delay_length + AMZM_refloop_length # delay on one side, total delay is doubled to match AMZM_total_delay_length
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
	ret_cell.add(gdstk.Reference(PIN_cell, origin=o))
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
	h = -1 * AMZM_refloop_length / 2
	o = horizontal(o, h, layer, ret_cell)
	o = arc_LU(o, layer, ret_cell)
	o = vertical(o, routing_waveguide_pitch, layer, ret_cell) # spacing for top MMI and loops
	o = arc_UR(o, layer, ret_cell)
	h = AMZM_refloop_length / 2
	o = horizontal(o, h, layer, ret_cell)
	o = horizontal(o, RF_PAD_PITCH, layer, ret_cell) # go pad pitch at last
	MMI_bot_point_left = o.copy() # savepoint for top MMI (left port)
	## 2x2 MMI (top) right ports
	o = TAPER_TOP_RIGHT.copy()
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
	MMI_bot_point_right = o.copy() # savepoint for top MMI (right port)
	## 2x2 MMI (top)
	o = [
		MMI_bot_point_left[0],
		(MMI_bot_point_left[1] + MMI_bot_point_right[1]) / 2
	]
	ret_cell.add(gdstk.Reference(AIST_PDK["AIST_MMI_2x2"], origin=o, rotation=-np.pi/2)); o[0] += MMI2x2_TOPLEFT_CENTER[1]
	ret_o = o.copy()
	## PIN pad ##
	#----- LAYER_MET = 36 (AlCu contact and metal wire) -----#
	layer = LAYER_MET
	MET_MIDDLE_corner_botleft = [
		TAPER_BOT_LEFT[0] + 0.5 + 4,
		TAPER_BOT_LEFT[1] + 10 + 20
	]
	MET_MIDDLE_corner_topright = [
		TAPER_BOT_RIGHT[0] - 0.5 - 4,
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
	pad_cell = gdstk.Cell(cell_name+"_TIN_PAD")
	pad_cell.add(pad_metal, pad_window)
	### add to ret_cell
	ret_cell.add(
		gdstk.Reference(pad_cell, origin=(-RF_PAD_PITCH*2, 0), columns=5, rows=1, spacing=(RF_PAD_PITCH, 0))
	)
	return ret_cell

def new_PIN_AMZM_cell_deprecated(PIN_length, cell_name):
	# connection points for use
	MZM_BOTLEFT_CENTER = [-50, 0.0]
	MZM_BOTRIGHT_CENTER = [+50, 0.0]
	# constants
	MMI2x2_BOTLEFT_CENTER  = [-0.55, 0.0]
	MMI2x2_BOTRIGHT_CENTER = [+0.55, 0.0]
	MMI2x2_TOPLEFT_CENTER  = [-0.55, 41.016]
	MMI2x2_TOPRIGHT_CENTER = [+0.55, 41.016]
	RF_PAD_PITCH = 125
	TIN_length = 100
	TIN_width = 5
	PIN_TIN_distance = 14.4
	AMZM_delay_length = 100 # um
	AMZM_ref_length = 30 # um
	# PIN and TIN cells
	PIN_cell, PIN_end_o = PIN_structure(PIN_length, [0,0], cell_name+"_PIN")
	# TIN_cell, TIN_end_o = TIN_structure(TIN_length, TIN_width, [0,0], cell_name+"_TIN")
	ret_cell = gdstk.Cell(cell_name)
	# SiWG layer = 30
	layer = LAYER_SiWG
	## 2x2 MMI (bottom) bottom left port
	start_point = [MZM_BOTLEFT_CENTER[0], 0]
	end_point = [MMI2x2_BOTLEFT_CENTER[0], 2*(radius+dr)]
	o = start_point
	o = arc_UR(o, layer, ret_cell)
	o = horizontal(o, np.abs(start_point[0]-end_point[0]) - 2*(radius+dr), layer, ret_cell)
	o = arc_RU(o, layer, ret_cell)
	## 2x2 MMI (bottom) bottom right port
	start_point = [MZM_BOTRIGHT_CENTER[0], 0]
	end_point = [MMI2x2_BOTRIGHT_CENTER[0], 2*(radius+dr)] # 2x2 MMI left port
	o = start_point
	o = arc_UL(o, layer, ret_cell)
	o = horizontal(o, -( np.abs(start_point[0]-end_point[0]) - 2*(radius+dr) ), layer, ret_cell)
	o = arc_LU(o, layer, ret_cell)
	## 2x2 MMI (bottom)
	start_point = [0, end_point[1]]
	ret_cell.add(gdstk.Reference(AIST_PDK["AIST_MMI_2x2"], origin=start_point)); o[1] += start_point[1]
	MMI_top_point = start_point
	## 2x2 MMI (bottom) top left port
	start_point = [
		MMI2x2_TOPLEFT_CENTER[0],
		MMI_top_point[1] + MMI2x2_TOPLEFT_CENTER[1] - MMI2x2_BOTLEFT_CENTER[1]
	]
	end_point = [
		- RF_PAD_PITCH/2,
		start_point[1] + 2*(radius+dr)
	]
	o = start_point
	o = arc_UL(o, layer, ret_cell)
	o = horizontal(o, -( np.abs(start_point[0]-end_point[0]) - 2*(radius+dr) ), layer, ret_cell)
	o = arc_LU(o, layer, ret_cell)
	### savepoint for taper (bottom left) ###
	TAPER_BOT_LEFT = o.copy()
	ret_cell.add(gdstk.Reference(PIN_cell, origin=o))
	o[0] += PIN_end_o[0]
	o[1] += PIN_end_o[1]
	### savepoint for taper (bottom left) ###
	o = vertical(o, PIN_TIN_distance, layer, ret_cell)
	# # TIN heater
	# TIN_BOT_LEFT = o.copy()
	# ret_cell.add(gdstk.Reference(TIN_cell, origin=o))
	# o[0] += TIN_end_o[0]
	# o[1] += TIN_end_o[1]
	# add delay (reference)
	o = arc_UL(o, layer, ret_cell)
	o = arc_LD(o, layer, ret_cell)
	o = arc_DL(o, layer, ret_cell)
	o = arc_LU(o, layer, ret_cell)
	o = vertical(o, AMZM_ref_length, layer, ret_cell)
	o = arc_UR(o, layer, ret_cell)
	o = arc_RD(o, layer, ret_cell)
	o = arc_DR(o, layer, ret_cell)
	o = arc_RU(o, layer, ret_cell)
	# connect to top MMI
	start_point = o
	end_point = [
		MMI2x2_BOTLEFT_CENTER[0],
		start_point[1] + 2*(radius+dr)
	]
	o = arc_UR(o, layer, ret_cell)
	o = horizontal(o, np.abs(start_point[0]-end_point[0]) - 2*(radius+dr), layer, ret_cell)
	o = arc_RU(o, layer, ret_cell)
	## 2x2 MMI (bottom) top right port
	start_point = [
		MMI2x2_TOPRIGHT_CENTER[0],
		MMI_top_point[1] + MMI2x2_TOPRIGHT_CENTER[1] - MMI2x2_BOTLEFT_CENTER[1]
	]
	end_point = [
		RF_PAD_PITCH/2,
		start_point[1] + 2*(radius+dr)
	]
	o = start_point
	o = arc_UR(o, layer, ret_cell)
	o = horizontal(o, np.abs(start_point[0]-end_point[0]) - 2*(radius+dr), layer, ret_cell)
	o = arc_RU(o, layer, ret_cell)
	### savepoint for taper (bottom right) ###
	TAPER_BOT_RIGHT = o.copy()
	ret_cell.add(gdstk.Reference(PIN_cell, origin=o, x_reflection=True, rotation=np.pi))
	o[0] += PIN_end_o[0]
	o[1] += PIN_end_o[1]
	### savepoint for taper (bottom right) ###
	o = vertical(o, PIN_TIN_distance, layer, ret_cell)
	# # TIN heater
	# TIN_BOT_RIGHT = o.copy()
	# ret_cell.add(gdstk.Reference(TIN_cell, origin=o, x_reflection=True, rotation=np.pi))
	# o[0] += TIN_end_o[0]
	# o[1] += TIN_end_o[1]
	# add delay (delay line)
	o = arc_UR(o, layer, ret_cell)
	o = arc_RD(o, layer, ret_cell)
	o = arc_DR(o, layer, ret_cell)
	o = arc_RU(o, layer, ret_cell)
	o = vertical(o, AMZM_ref_length + AMZM_delay_length/2, layer, ret_cell)
	o = arc_UL(o, layer, ret_cell)
	o = arc_LD(o, layer, ret_cell)
	o = vertical(o, -AMZM_delay_length/2, layer, ret_cell)
	o = arc_DL(o, layer, ret_cell)
	o = arc_LU(o, layer, ret_cell)
	# connect to top MMI
	start_point = o
	end_point = [
		MMI2x2_BOTRIGHT_CENTER[0],
		start_point[1] + 2*(radius+dr)
	]
	o = arc_UL(o, layer, ret_cell)
	o = horizontal(o, -( np.abs(start_point[0]-end_point[0]) - 2*(radius+dr) ), layer, ret_cell)
	o = arc_LU(o, layer, ret_cell)
	## 2x2 MMI (top)
	end_point = o
	start_point = [0, end_point[1]]
	ret_cell.add(gdstk.Reference(AIST_PDK["AIST_MMI_2x2"], origin=start_point))
	MMI_top_point = start_point
	## 2x2 MMI (top) top left port
	start_point = [
		MMI2x2_TOPLEFT_CENTER[0],
		MMI_top_point[1] + MMI2x2_TOPLEFT_CENTER[1] - MMI2x2_BOTLEFT_CENTER[1]
	]
	end_point = [
		MZM_BOTLEFT_CENTER[0],
		start_point[1] + 2*(radius+dr)
	]
	o = start_point
	o = arc_UL(o, layer, ret_cell)
	o = horizontal(o, -( np.abs(start_point[0]-end_point[0]) - 2*(radius+dr) ), layer, ret_cell)
	o = arc_LU(o, layer, ret_cell)
	## 2x2 MMI (top) top right port
	start_point = [
		MMI2x2_TOPRIGHT_CENTER[0],
		MMI_top_point[1] + MMI2x2_TOPRIGHT_CENTER[1] - MMI2x2_BOTLEFT_CENTER[1]
	]
	end_point = [
		MZM_BOTRIGHT_CENTER[0],
		start_point[1] + 2*(radius+dr)
	]
	o = start_point
	o = arc_UR(o, layer, ret_cell)
	o = horizontal(o, np.abs(start_point[0]-end_point[0]) - 2*(radius+dr), layer, ret_cell)
	o = arc_RU(o, layer, ret_cell)
	## PIN pad ##
	#----- LAYER_MET = 36 (AlCu contact and metal wire) -----#
	layer = LAYER_MET
	MET_MIDDLE_corner_botleft = [
		TAPER_BOT_LEFT[0] + 0.5 + 4,
		TAPER_BOT_LEFT[1] + 10 + 20
	]
	MET_MIDDLE_corner_topright = [
		TAPER_BOT_RIGHT[0] - 0.5 - 4,
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
	# ## TIN pad ##
	# #----- LAYER_MET = 36 (AlCu contact and metal wire) -----#
	# layer = LAYER_MET
	# MET_MIDDLE_corner_botleft = [
		# TIN_BOT_LEFT[0] + 5,
		# TIN_BOT_LEFT[1]
	# ]
	# MET_MIDDLE_corner_topright = [
		# TIN_BOT_RIGHT[0] - 5,
		# TIN_BOT_RIGHT[1] + TIN_length
	# ]
	# pad_metal = gdstk.rectangle(MET_MIDDLE_corner_botleft, MET_MIDDLE_corner_topright, layer=layer, datatype=0)
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
	pad_cell = gdstk.Cell(cell_name+"_TIN_PAD")
	pad_cell.add(pad_metal, pad_window)
	### add to ret_cell
	ret_cell.add(
		gdstk.Reference(pad_cell, origin=(-RF_PAD_PITCH*2, 0), columns=5, rows=1, spacing=(RF_PAD_PITCH, 0))
	)
	return ret_cell

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

def TIN_structure(TIN_length, TIN_width, start_point, cell_name):
	# LAYER_SiWG   = 30
	# LAYER_TIN    = 38
	# LAYER_CT2TIN = 39 # contact to TiN
	# LAYER_DW     = 42 # deep window (trench)
	ret_cell = gdstk.Cell(cell_name)
	#----- LAYER_SiWG = 30 -----#
	layer = LAYER_SiWG
	o = start_point.copy()
	o = vertical(o, TIN_length, layer, ret_cell)
	ret_o = o # <--- return value of taper end of Si waveguide
	#----- LAYER_TIN = 38 -----#
	layer = LAYER_TIN
	o = start_point.copy()
	# rectangle
	path = gdstk.FlexPath(o, TIN_width, layer=layer, datatype=0, tolerance=1e-3)
	path.vertical(TIN_length, relative=True); o[1] += TIN_length
	ret_cell.add(path)
	TIN_pad_botleft_corner_botleft = [
		start_point[0] - TIN_width/2 - 20,
		start_point[1]
	]
	TIN_pad_botleft_corner_topright = [
		start_point[0] - TIN_width/2,
		start_point[1] + 20
	]
	TIN_pad_botleft = gdstk.rectangle(TIN_pad_botleft_corner_botleft, TIN_pad_botleft_corner_topright, layer=layer, datatype=0)
	ret_cell.add(TIN_pad_botleft)
	TIN_pad_topright_corner_botleft = [
		start_point[0] + TIN_width/2,
		start_point[1] + TIN_length - 20
	]
	TIN_pad_topright_corner_topright = [
		start_point[0] + TIN_width/2 + 20,
		start_point[1] + TIN_length
	]
	TIN_pad_topright = gdstk.rectangle(TIN_pad_topright_corner_botleft, TIN_pad_topright_corner_topright, layer=layer, datatype=0)
	ret_cell.add(TIN_pad_topright)
	#----- LAYER_CT2TIN = 39 -----#
	layer = LAYER_CT2TIN
	# rectangle
	TIN_contact_botleft_corner_botleft = [
		TIN_pad_botleft_corner_botleft[0] + 3,
		TIN_pad_botleft_corner_botleft[1] + 3,
	]
	TIN_contact_botleft_corner_topright = [
		TIN_pad_botleft_corner_topright[0] - 3,
		TIN_pad_botleft_corner_topright[1] - 3,
	]
	TIN_contact_botleft = gdstk.rectangle(TIN_contact_botleft_corner_botleft, TIN_contact_botleft_corner_topright, layer=layer, datatype=0)
	ret_cell.add(TIN_contact_botleft)
	TIN_contact_topright_corner_botleft = [
		TIN_pad_topright_corner_botleft[0] + 3,
		TIN_pad_topright_corner_botleft[1] + 3,
	]
	TIN_contact_topright_corner_topright = [
		TIN_pad_topright_corner_topright[0] - 3,
		TIN_pad_topright_corner_topright[1] - 3,
	]
	TIN_contact_topright = gdstk.rectangle(TIN_contact_topright_corner_botleft, TIN_contact_topright_corner_topright, layer=layer, datatype=0)
	ret_cell.add(TIN_contact_topright)
	#----- LAYER_MET = 36 (AlCu contact and metal wire) -----#
	layer = LAYER_MET
	MET_botleft_corner_botleft = TIN_pad_botleft_corner_botleft
	MET_botleft_corner_topright = TIN_pad_botleft_corner_topright
	pad_metal_botleft = gdstk.rectangle(MET_botleft_corner_botleft, MET_botleft_corner_topright, layer=layer, datatype=0)
	ret_cell.add(pad_metal_botleft)
	MET_topright_corner_botleft = TIN_pad_topright_corner_botleft
	MET_topright_corner_topright = TIN_pad_topright_corner_topright
	pad_metal_topright = gdstk.rectangle(MET_topright_corner_botleft, MET_topright_corner_topright, layer=layer, datatype=0)
	ret_cell.add(pad_metal_topright)
	return ret_cell, ret_o

def PINL100_01_route_cell(pos, end_point, layer, cell_name):
	ret_cell = gdstk.Cell(cell_name)
	# top right port
	o = [
		pos[0] + 50,
		pos[1] + 492.916,
	]
	path = gdstk.FlexPath(o, wg_width, layer=layer, datatype=0, tolerance=1e-3)
	o = vertical(o, 10, layer, ret_cell)
	o = arc_UR(o, layer, ret_cell)
	o = horizontal(o, 50, layer, ret_cell)
	o = arc_RD(o, layer, ret_cell)
	vertical_length = o[1] - end_point[1] - radius - dr
	o = vertical(o, -vertical_length, layer, ret_cell)
	o = arc_DR(o, layer, ret_cell)
	horizontal_length = end_point[0] - o[0]
	o = horizontal(o, horizontal_length, layer, ret_cell)
	ret_cell.add(path)
	return ret_cell

top_cell = gdstk.Cell("top_cell")

pin_mzm_L100 = new_PIN_AMZM_cell(100, "CR_PINL100AMZ")
pin_mzm_L100_deprecated = new_PIN_AMZM_cell_deprecated(100, "CR_PINL100AMZ_deprecated")
pin_mzm_L200 = new_PIN_AMZM_cell(200, "CR_PINL200AMZ")
pin_mzm_L200_deprecated = new_PIN_AMZM_cell_deprecated(200, "CR_PINL200AMZ_deprecated")
pin_mzm_L500 = new_PIN_AMZM_cell(500, "CR_PINL500AMZ")
pin_mzm_L500_deprecated = new_PIN_AMZM_cell_deprecated(500, "CR_PINL500AMZ_deprecated")

PINL100_01_origin = [0, 0]
PINL100_deprecated_01_origin = [750, 0]
PINL200_01_origin = [0, 750]
PINL200_deprecated_01_origin = [750, 750]
PINL500_01_origin = [0, 1500]
PINL500_deprecated_01_origin = [750, 1500]

# PINL100_01_origin = [750, 1000]
# PINL100_02_origin = [250, 1000]
# PINL250_01_origin = [750,   50]
# PINL500_01_origin = [250,   50]

top_cell.add(gdstk.Reference(pin_mzm_L100, origin=PINL100_01_origin))
top_cell.add(gdstk.Reference(pin_mzm_L100_deprecated, origin=PINL100_deprecated_01_origin))
top_cell.add(gdstk.Reference(pin_mzm_L200, origin=PINL200_01_origin))
top_cell.add(gdstk.Reference(pin_mzm_L200_deprecated, origin=PINL200_deprecated_01_origin))
top_cell.add(gdstk.Reference(pin_mzm_L500, origin=PINL500_01_origin))
top_cell.add(gdstk.Reference(pin_mzm_L500_deprecated, origin=PINL500_deprecated_01_origin))

LIB.add(top_cell, *top_cell.dependencies(True))
LIB.write_gds("pin_amzm_custom_vertMMI.gds")
