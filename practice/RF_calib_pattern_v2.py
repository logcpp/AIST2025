# AIST 2025 design library
# created on: 2026/01/22
# last change: 2026/01/22

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

# design parameters of CPW
RF_PAD_PITCH = 125
RF_PAD_GAP = 9
SIG_width = 10
GND_width = 50
GAP_width = 9
RF_PAD_size = RF_PAD_PITCH - GAP_width
RF_PAD_taper_length = 45
RF_PAD_taper_end = 30.5

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
			origin[1] - RF_PAD_taper_length - RF_PAD_size
		]
		MET_MIDDLE_corner_topright = [
			- pad_offset*RF_PAD_PITCH + RF_PAD_size/2,
			origin[1] - RF_PAD_taper_length
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
	# middle GND
	taper_middle_GND_botleft  = [ -RF_PAD_size/2, origin[1] - RF_PAD_taper_length ]
	taper_middle_GND_botright  = [ +RF_PAD_size/2, origin[1] - RF_PAD_taper_length ]
	taper_middle_GND_topright = [ +RF_PAD_size/2, origin[1] ]
	taper_middle_GND_topleft = [ -RF_PAD_size/2, origin[1] ]
	taper_middle_GND = gdstk.rectangle(taper_middle_GND_botleft, taper_middle_GND_topright, layer=layer, datatype=0)
	ret_cell.add(taper_middle_GND)
	# left SIG
	taper_left_SIG_botleft  = [ -1*RF_PAD_PITCH - RF_PAD_size/2, origin[1] - RF_PAD_taper_length ]
	taper_left_SIG_botright = [ -1*RF_PAD_PITCH + RF_PAD_size/2, origin[1] - RF_PAD_taper_length ]
	taper_left_SIG_topright = [ -RF_PAD_PITCH/2 - 4 - 0.5, origin[1] ]
	taper_left_SIG_topleft  = [ -RF_PAD_PITCH/2 - 4 - 0.5 - SIG_width, origin[1] ]
	points = [taper_left_SIG_botleft, taper_left_SIG_botright, taper_left_SIG_topright, taper_left_SIG_topleft]
	taper_left_SIG = gdstk.Polygon(points, layer=layer, datatype=0)
	ret_cell.add(taper_left_SIG)
	# left GND
	taper_left_GND_botleft  = [ -2*RF_PAD_PITCH - RF_PAD_size/2, origin[1] - RF_PAD_taper_length ]
	taper_left_GND_botright = [ -2*RF_PAD_PITCH + RF_PAD_size/2, origin[1] - RF_PAD_taper_length ]
	taper_left_GND_topright = [ taper_left_SIG_topleft[0] - GAP_width, origin[1] ]
	taper_left_GND_topleft  = [ taper_left_SIG_topleft[0] - GAP_width - GND_width, origin[1] ]
	points = [taper_left_GND_botleft, taper_left_GND_botright, taper_left_GND_topright, taper_left_GND_topleft]
	taper_left_GND = gdstk.Polygon(points, layer=layer, datatype=0)
	ret_cell.add(taper_left_GND)
	# right SIG
	taper_right_SIG_botleft  = [ +1*RF_PAD_PITCH - RF_PAD_size/2, origin[1] - RF_PAD_taper_length ]
	taper_right_SIG_botright = [ +1*RF_PAD_PITCH + RF_PAD_size/2, origin[1] - RF_PAD_taper_length ]
	taper_right_SIG_topright = [ +RF_PAD_PITCH/2 + 4 + 0.5 + SIG_width, origin[1] ]
	taper_right_SIG_topleft  = [ +RF_PAD_PITCH/2 + 4 + 0.5, origin[1] ]
	points = [taper_right_SIG_botleft, taper_right_SIG_botright, taper_right_SIG_topright, taper_right_SIG_topleft]
	taper_right_SIG = gdstk.Polygon(points, layer=layer, datatype=0)
	ret_cell.add(taper_right_SIG)
	# right GND
	taper_right_GND_botleft  = [ +2*RF_PAD_PITCH - RF_PAD_size/2, origin[1] - RF_PAD_taper_length ]
	taper_right_GND_botright = [ +2*RF_PAD_PITCH + RF_PAD_size/2, origin[1] - RF_PAD_taper_length ]
	taper_right_GND_topright = [ taper_right_SIG_topright[0] + GAP_width + GND_width, origin[1] ]
	taper_right_GND_topleft  = [ taper_right_SIG_topright[0] + GAP_width, origin[1] ]
	points = [taper_right_GND_botleft, taper_right_GND_botright, taper_right_GND_topright, taper_right_GND_topleft]
	taper_right_GND = gdstk.Polygon(points, layer=layer, datatype=0)
	ret_cell.add(taper_right_GND)
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
def new_CPW_cell(CPW_length, cell_name):
	ret_cell = gdstk.Cell(cell_name)
	# CPW pad #
	ret_cell.add(gdstk.Reference(RF_PAD_cell, origin=(0,0)))
	taper_left_GND_topleft    = RF_PAD_cell_points[0]
	taper_left_GND_topright   = RF_PAD_cell_points[1]
	taper_left_SIG_topleft    = RF_PAD_cell_points[2]
	taper_left_SIG_topright   = RF_PAD_cell_points[3]
	taper_middle_GND_topleft  = RF_PAD_cell_points[4]
	taper_middle_GND_topright = RF_PAD_cell_points[5]
	taper_right_SIG_topleft   = RF_PAD_cell_points[6]
	taper_right_SIG_topright  = RF_PAD_cell_points[7]
	taper_right_GND_topleft   = RF_PAD_cell_points[8]
	taper_right_GND_topright  = RF_PAD_cell_points[9]
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
	ret_cell.add(gdstk.Reference(RF_PAD_cell, origin=(0, CPW_length), x_reflection=True))
	return ret_cell

def new_Short_cell(length, cell_name):
	ret_cell = gdstk.Cell(cell_name)
	CPW_length = length
	# CPW pad #
	ret_cell.add(gdstk.Reference(RF_PAD_cell, origin=(0,0)))
	taper_left_GND_topleft    = RF_PAD_cell_points[0]
	taper_left_GND_topright   = RF_PAD_cell_points[1]
	taper_left_SIG_topleft    = RF_PAD_cell_points[2]
	taper_left_SIG_topright   = RF_PAD_cell_points[3]
	taper_middle_GND_topleft  = RF_PAD_cell_points[4]
	taper_middle_GND_topright = RF_PAD_cell_points[5]
	taper_right_SIG_topleft   = RF_PAD_cell_points[6]
	taper_right_SIG_topright  = RF_PAD_cell_points[7]
	taper_right_GND_topleft   = RF_PAD_cell_points[8]
	taper_right_GND_topright  = RF_PAD_cell_points[9]
	# CPW pad #
	ret_cell.add(gdstk.Reference(RF_PAD_cell, origin=(0,0)))
	ret_cell.add(
		gdstk.rectangle(taper_left_GND_topleft, [taper_right_GND_topright[0],taper_right_GND_topright[1]+length], layer=LAYER_MET, datatype=0)
	)
	ret_cell.add(gdstk.Reference(RF_PAD_cell, origin=(0,length), x_reflection=True))
	return ret_cell

def new_Open_cell(length, cell_name):
	ret_cell = gdstk.Cell(cell_name)
	CPW_length = length
	# CPW pad #
	ret_cell.add(gdstk.Reference(RF_PAD_cell, origin=(0,0)))
	taper_left_GND_topleft    = RF_PAD_cell_points[0]
	taper_left_GND_topright   = RF_PAD_cell_points[1]
	taper_left_SIG_topleft    = RF_PAD_cell_points[2]
	taper_left_SIG_topright   = RF_PAD_cell_points[3]
	taper_middle_GND_topleft  = RF_PAD_cell_points[4]
	taper_middle_GND_topright = RF_PAD_cell_points[5]
	taper_right_SIG_topleft   = RF_PAD_cell_points[6]
	taper_right_SIG_topright  = RF_PAD_cell_points[7]
	taper_right_GND_topleft   = RF_PAD_cell_points[8]
	taper_right_GND_topright  = RF_PAD_cell_points[9]
	# CPW waveguide
	## left GND
	gnd_line_left_corner_botleft  = [ taper_left_GND_topleft[0], taper_left_GND_topleft[1] ]
	gnd_line_left_corner_topright = [ taper_left_GND_topright[0], CPW_length + taper_left_GND_topright[1] ]
	gnd_line_left = gdstk.rectangle(gnd_line_left_corner_botleft, gnd_line_left_corner_topright, layer=LAYER_MET, datatype=0)
	ret_cell.add(gnd_line_left)
	# ## left SIG
	# sig_line_left_corner_botleft  = [ taper_left_SIG_topleft[0], taper_left_SIG_topleft[1] ]
	# sig_line_left_corner_topright = [ taper_left_SIG_topright[0], CPW_length + taper_left_SIG_topright[1] ]
	# sig_line_left = gdstk.rectangle(sig_line_left_corner_botleft, sig_line_left_corner_topright, layer=LAYER_MET, datatype=0)
	# ret_cell.add(sig_line_left)
	## middle GND
	gnd_line_middle_corner_botleft  = [ taper_middle_GND_topleft[0], taper_middle_GND_topleft[1] ]
	gnd_line_middle_corner_topright = [ taper_middle_GND_topright[0], CPW_length + taper_middle_GND_topright[1] ]
	gnd_line_middle = gdstk.rectangle(gnd_line_middle_corner_botleft, gnd_line_middle_corner_topright, layer=LAYER_MET, datatype=0)
	ret_cell.add(gnd_line_middle)
	# ## right SIG
	# sig_line_right_corner_botleft  = [ taper_right_SIG_topleft[0], taper_right_SIG_topleft[1] ]
	# sig_line_right_corner_topright = [ taper_right_SIG_topright[0], CPW_length + taper_right_SIG_topright[1] ]
	# sig_line_right = gdstk.rectangle(sig_line_right_corner_botleft, sig_line_right_corner_topright, layer=LAYER_MET, datatype=0)
	# ret_cell.add(sig_line_right)
	## right GND
	gnd_line_right_corner_botleft  = [ taper_right_GND_topleft[0], taper_right_GND_topleft[1] ]
	gnd_line_right_corner_topright = [ taper_right_GND_topright[0], CPW_length + taper_right_GND_topright[1] ]
	gnd_line_right = gdstk.rectangle(gnd_line_right_corner_botleft, gnd_line_right_corner_topright, layer=LAYER_MET, datatype=0)
	ret_cell.add(gnd_line_right)
	# CPW pad #
	ret_cell.add(gdstk.Reference(RF_PAD_cell, origin=(0, CPW_length), x_reflection=True))
	return ret_cell

def new_Load_cell(length, cell_name):
	ret_cell = gdstk.Cell(cell_name)
	CPW_cell = new_CPW_cell(length, cell_name+"_CPW")
	ret_cell.add(gdstk.Reference(CPW_cell, origin=(0,0)))
	taper_left_GND_topleft    = RF_PAD_cell_points[0]
	taper_left_GND_topright   = RF_PAD_cell_points[1]
	taper_left_SIG_topleft    = RF_PAD_cell_points[2]
	taper_left_SIG_topright   = RF_PAD_cell_points[3]
	taper_middle_GND_topleft  = RF_PAD_cell_points[4]
	taper_middle_GND_topright = RF_PAD_cell_points[5]
	taper_right_SIG_topleft   = RF_PAD_cell_points[6]
	taper_right_SIG_topright  = RF_PAD_cell_points[7]
	taper_right_GND_topleft   = RF_PAD_cell_points[8]
	taper_right_GND_topright  = RF_PAD_cell_points[9]
	## TiN (left)
	TIN_width = 10 # um
	TIN_length = 37 # um => ~100 Ohm
	contact_width = 5
	contact_length = 5
	gap = (TIN_width - contact_width) / 2
	def TIN_load_cell(cell_name):
		ret_cell = gdstk.Cell(cell_name)
		TIN_corner_botleft = [
			-0.5 * contact_width - gap,
			-0.5 * contact_width - gap,
		]
		TIN_corner_topright = [
			TIN_corner_botleft[0] + TIN_length,
			TIN_corner_botleft[0] + TIN_width,
		]
		ret_cell.add( gdstk.rectangle(TIN_corner_botleft, TIN_corner_topright, layer=LAYER_TIN, datatype=0))
		contact_left_corner_botleft = [
			TIN_corner_botleft[0] + gap,
			TIN_corner_botleft[1] + gap,
		]
		contact_left_corner_topright = [
			TIN_corner_botleft[0] + gap + contact_length,
			TIN_corner_botleft[1] + gap + contact_width
		]
		ret_cell.add( gdstk.rectangle(contact_left_corner_botleft, contact_left_corner_topright, layer=LAYER_CT2TIN, datatype=0))
		contact_right_corner_botleft = [
			TIN_corner_topright[0] - gap,
			TIN_corner_topright[1] - gap
		]
		contact_right_corner_topright = [
			TIN_corner_topright[0] - (gap + contact_length),
			TIN_corner_topright[1] - (gap + contact_width)
		]
		ret_cell.add(
			gdstk.rectangle(contact_right_corner_botleft, contact_right_corner_topright, layer=LAYER_CT2TIN, datatype=0)
		)
		return ret_cell
	TIN_cell = TIN_load_cell(cell_name+"_TIN")
	ret_cell.add(
		# left SIG
		gdstk.Reference( TIN_cell, origin=[ (taper_left_SIG_topleft[0] + taper_left_SIG_topright[0]) / 2, length/2 - TIN_width/2 - 2 ]),
		gdstk.Reference( TIN_cell, origin=[ (taper_left_SIG_topleft[0] + taper_left_SIG_topright[0]) / 2, length/2 + TIN_width/2 + 2 ], rotation=np.pi),
		# right SIG
		gdstk.Reference( TIN_cell, origin=[ (taper_right_SIG_topleft[0] + taper_right_SIG_topright[0]) / 2, length/2 + TIN_width/2 + 2 ]),
		gdstk.Reference( TIN_cell, origin=[ (taper_right_SIG_topleft[0] + taper_right_SIG_topright[0]) / 2, length/2 - TIN_width/2 - 2 ], rotation=np.pi),
	)
	return ret_cell

def new_Load_PIN_cell(length, cell_name):
	ret_cell = gdstk.Cell(cell_name)
	CPW_cell = new_CPW_cell(length+1, cell_name+"_CPW")
	ret_cell.add(gdstk.Reference(CPW_cell, origin=(0,0)))
	## left PIN
	PIN, end_o = PIN_structure(length, [0, -RF_PAD_taper_end], f"PIN_L{length}")
	PIN_origin = [ -RF_PAD_PITCH / 2, 0 ]
	ret_cell.add( gdstk.Reference(PIN, origin=PIN_origin))
	## right PIN
	PIN, end_o = PIN_structure(length, [0, -RF_PAD_taper_end], f"PIN_L{length}")
	PIN_origin = [ +RF_PAD_PITCH / 2, 0 ]
	ret_cell.add( gdstk.Reference(PIN, origin=PIN_origin))
	return ret_cell

def new_label_cell(text, cell_name, layer=LAYER_MET):
	ret_cell = gdstk.Cell(cell_name)
	text = gdstk.text(text, 150, (0,0), layer=layer, datatype=0)
	ret_cell.add(*text)
	return ret_cell

top_cell = gdstk.Cell("top_cell")

CPWL1000_01 = new_CPW_cell(1000, "CPW_L1.0mm"); CPWL1000_01_label = new_label_cell("L1.0mm", "CPW_L1.0mm_label")
CPWL2000_01 = new_CPW_cell(2000, "CPW_L2.0mm"); CPWL2000_01_label = new_label_cell("L2.0mm", "CPW_L2.0mm_label")
Short_01 = new_Short_cell(50, "Short_L50um"); Short_01_label = new_label_cell("Short", "Short_L50um_label")
Open_01 = new_Open_cell(50, "Open_L50um"); Open_01_label = new_label_cell("Open", "Open_L50um_label")
Load_01 = new_Load_cell(50, "Load_L50um"); Load_01_label = new_label_cell("Load 50Ohm", "Load_L50um_label")
Load_02 = new_Load_PIN_cell(50, "Load_PIN_L50um"); Load_02_label = new_label_cell("Load PIN", "Load_PIN_L50um_label")
Thru_01 = new_CPW_cell(50, "Thru_L50um"); Thru_01_label = new_label_cell("Thru", "Thru_L50um_label")

CPWL2000_01_origin			= [1700,    0]
CPWL2000_01_label_origin	= [1950,    0]
CPWL1000_01_origin			= [   0,    0]
CPWL1000_01_label_origin	= [ 250,    0]

Short_01_origin				= [   0, 3500]
Open_01_origin				= [   0, 3000]
Load_01_origin				= [   0, 2500]
Load_02_origin				= [   0, 2000]
Thru_01_origin			    = [   0, 1500]
Short_01_label_origin		= [ Short_01_origin[0]    + 350, Short_01_origin[1]    - 50]
Open_01_label_origin		= [ Open_01_origin[0]     + 350, Open_01_origin[1]     - 50]
Load_01_label_origin		= [ Load_01_origin[0]     + 350, Load_01_origin[1]     - 50]
Load_02_label_origin		= [ Load_02_origin[0]     + 350, Load_02_origin[1]     - 50]
Thru_01_label_origin		= [ Thru_01_origin[0]     + 350, Thru_01_origin[1]     - 50]

top_cell.add(gdstk.Reference(CPWL1000_01, origin=CPWL1000_01_origin))
top_cell.add(gdstk.Reference(CPWL1000_01_label, origin=CPWL1000_01_label_origin))
top_cell.add(gdstk.Reference(CPWL2000_01, origin=CPWL2000_01_origin))
top_cell.add(gdstk.Reference(CPWL2000_01_label, origin=CPWL2000_01_label_origin))
top_cell.add(gdstk.Reference(Short_01, origin=Short_01_origin))
top_cell.add(gdstk.Reference(Short_01_label, origin=Short_01_label_origin))
top_cell.add(gdstk.Reference(Open_01, origin=Open_01_origin))
top_cell.add(gdstk.Reference(Open_01_label, origin=Open_01_label_origin))
top_cell.add(gdstk.Reference(Load_01, origin=Load_01_origin))
top_cell.add(gdstk.Reference(Load_01_label, origin=Load_01_label_origin))
top_cell.add(gdstk.Reference(Load_02, origin=Load_02_origin))
top_cell.add(gdstk.Reference(Load_02_label, origin=Load_02_label_origin))
top_cell.add(gdstk.Reference(Thru_01, origin=Thru_01_origin))
top_cell.add(gdstk.Reference(Thru_01_label, origin=Thru_01_label_origin))

# layer explanations
LABEL_LAYER30 = new_label_cell("Layer 30: Si", "LABEL_LAYER30", layer=LAYER_SiWG)
LABEL_LAYER40 = new_label_cell("Layer 40: RIB", "LABEL_LAYER40", layer=LAYER_RIB)
LABEL_LAYER31 = new_label_cell("Layer 31: N+", "LABEL_LAYER31", layer=LAYER_NP)
LABEL_LAYER32 = new_label_cell("Layer 32: P+", "LABEL_LAYER32", layer=LAYER_PP)
LABEL_LAYER33 = new_label_cell("Layer 33: N++", "LABEL_LAYER33", layer=LAYER_NPP)
LABEL_LAYER34 = new_label_cell("Layer 34: P++", "LABEL_LAYER34", layer=LAYER_PPP)
LABEL_LAYER35 = new_label_cell("Layer 35: CONTACT TO PN", "LABEL_LAYER35", layer=LAYER_CT2PN)
LABEL_LAYER30_origin		= [2200, 3800]
LABEL_LAYER40_origin		= [2200, 3650]
LABEL_LAYER31_origin		= [2200, 3500]
LABEL_LAYER32_origin		= [2200, 3350]
LABEL_LAYER33_origin		= [2200, 3200]
LABEL_LAYER34_origin		= [2200, 3050]
LABEL_LAYER35_origin		= [2200, 2900]
top_cell.add(gdstk.Reference(LABEL_LAYER30, origin=LABEL_LAYER30_origin))
top_cell.add(gdstk.Reference(LABEL_LAYER40, origin=LABEL_LAYER40_origin))
top_cell.add(gdstk.Reference(LABEL_LAYER31, origin=LABEL_LAYER31_origin))
top_cell.add(gdstk.Reference(LABEL_LAYER32, origin=LABEL_LAYER32_origin))
top_cell.add(gdstk.Reference(LABEL_LAYER33, origin=LABEL_LAYER33_origin))
top_cell.add(gdstk.Reference(LABEL_LAYER34, origin=LABEL_LAYER34_origin))
top_cell.add(gdstk.Reference(LABEL_LAYER35, origin=LABEL_LAYER35_origin))

LABEL_LAYER36 = new_label_cell("Layer 36: METAL", "LABEL_LAYER36", layer=LAYER_MET)
LABEL_LAYER38 = new_label_cell("Layer 38: TIN", "LABEL_LAYER38", layer=LAYER_TIN)
LABEL_LAYER39 = new_label_cell("Layer 39: CONTACT TO TIN", "LABEL_LAYER39", layer=LAYER_CT2TIN)
LABEL_LAYER41 = new_label_cell("Layer 41: PAD WINDOW", "LABEL_LAYER41", layer=LAYER_PW)
LABEL_LAYER36_origin		= [2200, 2600]
LABEL_LAYER38_origin		= [2200, 2450]
LABEL_LAYER39_origin		= [2200, 2300]
LABEL_LAYER41_origin		= [2200, 2150]
top_cell.add(gdstk.Reference(LABEL_LAYER36, origin=LABEL_LAYER36_origin))
top_cell.add(gdstk.Reference(LABEL_LAYER38, origin=LABEL_LAYER38_origin))
top_cell.add(gdstk.Reference(LABEL_LAYER39, origin=LABEL_LAYER39_origin))
top_cell.add(gdstk.Reference(LABEL_LAYER41, origin=LABEL_LAYER41_origin))

LIB.add(top_cell, *top_cell.dependencies(True))
LIB.write_gds("RF_calib_pattern_v2.gds")
