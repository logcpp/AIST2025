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
taper_length = 50 # um
SIG_width = 10 # um
GND_width = 35 # um # => ~50 Ohm
gap = 18 # um

RF_PAD_PITCH = 125     # RF pad pitch
RF_PAD_SIZE = RF_PAD_PITCH - gap # RF pad size

def new_CPW_PAD_cell(taper_length, SIG_width, GND_width, gap, cell_name):
	ret_cell = gdstk.Cell(cell_name)
	## CPW pad ##
	#----- LAYER_MET = 36 (AlCu contact and metal wire) -----#
	layer = LAYER_MET
	MET_MIDDLE_corner_botleft = [
		-RF_PAD_SIZE / 2,
		0
	]
	MET_MIDDLE_corner_topright = [
		RF_PAD_SIZE / 2,
		RF_PAD_SIZE
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
		gdstk.Reference(pad_cell, origin=(-RF_PAD_PITCH*1, 0), columns=3, rows=1, spacing=(RF_PAD_PITCH, 0))
	)
	#----- LAYER_MET = 36 (AlCu contact and metal wire) -----#
	layer = LAYER_MET
	GND_taper_left = gdstk.Polygon([
		[
			MET_MIDDLE_corner_botleft[0] - RF_PAD_PITCH,
			MET_MIDDLE_corner_topright[1],
		],
		[
			- SIG_width/2 - gap - GND_width,
			RF_PAD_SIZE + taper_length,
		],
		[
			- SIG_width/2 - gap,
			RF_PAD_SIZE + taper_length,
		],
		[
			MET_MIDDLE_corner_botleft[0] - RF_PAD_PITCH + RF_PAD_SIZE,
			MET_MIDDLE_corner_topright[1],
		],
	], layer=layer, datatype=0)
	ret_cell.add(GND_taper_left)
	SIG_taper = gdstk.Polygon([
		[
			MET_MIDDLE_corner_botleft[0],
			MET_MIDDLE_corner_topright[1],
		],
		[
			- SIG_width/2,
			RF_PAD_SIZE + taper_length,
		],
		[
			+ SIG_width/2,
			RF_PAD_SIZE + taper_length,
		],
		[
			MET_MIDDLE_corner_botleft[0] + RF_PAD_SIZE,
			MET_MIDDLE_corner_topright[1],
		],
	], layer=layer, datatype=0)
	ret_cell.add(SIG_taper)
	GND_taper_right = gdstk.Polygon([
		[
			MET_MIDDLE_corner_botleft[0] + RF_PAD_PITCH,
			MET_MIDDLE_corner_topright[1],
		],
		[
			+ SIG_width/2 + gap,
			RF_PAD_SIZE + taper_length,
		],
		[
			+ SIG_width/2 + gap + GND_width,
			RF_PAD_SIZE + taper_length,
		],
		[
			MET_MIDDLE_corner_botleft[0] + RF_PAD_PITCH + RF_PAD_SIZE,
			MET_MIDDLE_corner_topright[1],
		],
	], layer=layer, datatype=0)
	ret_cell.add(GND_taper_right)
	return ret_cell
CPW_PAD = new_CPW_PAD_cell(taper_length, SIG_width, GND_width, gap, "CPW_PAD")

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
	ret_cell.add(gdstk.Reference(CPW_PAD, origin=(0,0)))
	# CPW waveguide
	## GND
	gnd_line_left_corner_botleft = [
		-SIG_width / 2 - gap - GND_width,
		RF_PAD_SIZE + taper_length
	]
	gnd_line_left_corner_topright= [
		-SIG_width / 2 - gap,
		RF_PAD_SIZE + taper_length + CPW_length
	]
	gnd_line_left = gdstk.rectangle(gnd_line_left_corner_botleft, gnd_line_left_corner_topright, layer=LAYER_MET, datatype=0)
	ret_cell.add(gnd_line_left)
	## SIG
	sig_line_corner_botleft = [
		-SIG_width / 2,
		RF_PAD_SIZE + taper_length
	]
	sig_line_corner_topright= [
		+SIG_width / 2,
		RF_PAD_SIZE + taper_length + CPW_length
	]
	sig_line = gdstk.rectangle(sig_line_corner_botleft, sig_line_corner_topright, layer=LAYER_MET, datatype=0)
	ret_cell.add(sig_line)
	## GND
	gnd_line_right_corner_botright = [
		+SIG_width / 2 + gap + GND_width,
		RF_PAD_SIZE + taper_length
	]
	gnd_line_right_corner_topright= [
		+SIG_width / 2 + gap,
		RF_PAD_SIZE + taper_length + CPW_length
	]
	gnd_line_right = gdstk.rectangle(gnd_line_right_corner_botright, gnd_line_right_corner_topright, layer=LAYER_MET, datatype=0)
	ret_cell.add(gnd_line_right)
	# CPW pad #
	ret_cell.add(gdstk.Reference(CPW_PAD, origin=(0, 2*(RF_PAD_SIZE + taper_length) + CPW_length), x_reflection=True))
	return ret_cell

def new_Short_cell(length, cell_name):
	ret_cell = gdstk.Cell(cell_name)
	ret_cell.add(gdstk.Reference(CPW_PAD, origin=(0,0)))
	short_line_corner_botleft = [
		-SIG_width / 2 - gap - GND_width,
		RF_PAD_SIZE + taper_length
	]
	short_line_corner_topright= [
		+SIG_width / 2 + gap + GND_width,
		RF_PAD_SIZE + taper_length + length
	]
	ret_cell.add(
		gdstk.rectangle(short_line_corner_botleft, short_line_corner_topright, layer=LAYER_MET, datatype=0)
	)
	ret_cell.add(gdstk.Reference(CPW_PAD, origin=(0, 2*(RF_PAD_SIZE + taper_length) + length), x_reflection=True))
	return ret_cell

def new_Open_cell(length, cell_name):
	ret_cell = gdstk.Cell(cell_name)
	ret_cell.add(gdstk.Reference(CPW_PAD, origin=(0,0)))
	## GND
	gnd_line_left_corner_botleft = [
		-SIG_width / 2 - gap - GND_width,
		RF_PAD_SIZE + taper_length
	]
	gnd_line_left_corner_topright= [
		-SIG_width / 2 - gap,
		RF_PAD_SIZE + taper_length + length
	]
	gnd_line_left = gdstk.rectangle(gnd_line_left_corner_botleft, gnd_line_left_corner_topright, layer=LAYER_MET, datatype=0)
	ret_cell.add(gnd_line_left)
	## GND
	gnd_line_right_corner_botright = [
		+SIG_width / 2 + gap + GND_width,
		RF_PAD_SIZE + taper_length
	]
	gnd_line_right_corner_topright= [
		+SIG_width / 2 + gap,
		RF_PAD_SIZE + taper_length + length
	]
	gnd_line_right = gdstk.rectangle(gnd_line_right_corner_botright, gnd_line_right_corner_topright, layer=LAYER_MET, datatype=0)
	ret_cell.add(gnd_line_right)
	ret_cell.add(gdstk.Reference(CPW_PAD, origin=(0, 2*(RF_PAD_SIZE + taper_length) + length), x_reflection=True))
	return ret_cell

def new_Load_cell(length, cell_name):
	ret_cell = gdstk.Cell(cell_name)
	ret_cell.add(gdstk.Reference(CPW_PAD, origin=(0,0)))
	## GND
	gnd_line_left_corner_botleft = [
		-SIG_width / 2 - gap - GND_width,
		RF_PAD_SIZE + taper_length
	]
	gnd_line_left_corner_topright= [
		-SIG_width / 2 - gap,
		RF_PAD_SIZE + taper_length + length
	]
	gnd_line_left = gdstk.rectangle(gnd_line_left_corner_botleft, gnd_line_left_corner_topright, layer=LAYER_MET, datatype=0)
	ret_cell.add(gnd_line_left)
	## SIG
	short_line_corner_botleft = [
		-SIG_width / 2,
		RF_PAD_SIZE + taper_length
	]
	short_line_corner_topright= [
		+SIG_width / 2,
		RF_PAD_SIZE + taper_length + length
	]
	ret_cell.add(
		gdstk.rectangle(short_line_corner_botleft, short_line_corner_topright, layer=LAYER_MET, datatype=0)
	)
	## TiN (left)
	TiN_width = 10 # um
	TiN_length = 37 # um => ~100 Ohm
	TiN_left_corner_topright = [
		SIG_width / 2,
		RF_PAD_SIZE + taper_length + length/2 - TiN_width*1.5 + TiN_width
	]
	TiN_left_corner_botleft = [
		TiN_left_corner_topright[0] - TiN_length,
		TiN_left_corner_topright[1] - TiN_width
	]
	ret_cell.add(
		gdstk.rectangle(TiN_left_corner_botleft, TiN_left_corner_topright, layer=LAYER_TIN, datatype=0)
	)
	contact_left_corner_topright = [
		SIG_width / 2 - 2,
		TiN_left_corner_topright[1] - 2
	]
	contact_left_corner_botleft = [
		- SIG_width / 2 + 2,
		TiN_left_corner_botleft[1] + 2
	]
	ret_cell.add(
		gdstk.rectangle(contact_left_corner_botleft, contact_left_corner_topright, layer=LAYER_CT2TIN, datatype=0)
	)
	contact_left_corner_topright = [
		TiN_left_corner_botleft[0] + 7,
		TiN_left_corner_topright[1] - 2
	]
	contact_left_corner_botleft = [
		TiN_left_corner_botleft[0] + 2,
		TiN_left_corner_botleft[1] + 2
	]
	ret_cell.add(
		gdstk.rectangle(contact_left_corner_botleft, contact_left_corner_topright, layer=LAYER_CT2TIN, datatype=0)
	)
	## TiN (right)
	TiN_right_corner_botleft = [
		- SIG_width / 2,
		RF_PAD_SIZE + taper_length + length/2 + TiN_width*0.5
	]
	TiN_right_corner_topright = [
		TiN_right_corner_botleft[0] + TiN_length,
		TiN_right_corner_botleft[1] + TiN_width
	]
	ret_cell.add(
		gdstk.rectangle(TiN_right_corner_botleft, TiN_right_corner_topright, layer=LAYER_TIN, datatype=0)
	)
	contact_right_corner_botleft = [
		- SIG_width / 2 + 2,
		TiN_right_corner_botleft[1] + 2
	]
	contact_right_corner_topright = [
		SIG_width / 2 - 2,
		TiN_right_corner_topright[1] - 2
	]
	ret_cell.add(
		gdstk.rectangle(contact_right_corner_botleft, contact_right_corner_topright, layer=LAYER_CT2TIN, datatype=0)
	)
	contact_right_corner_topright = [
		TiN_right_corner_topright[0] - 2,
		TiN_right_corner_topright[1] - 2
	]
	contact_right_corner_botleft = [
		TiN_right_corner_topright[0] - 7,
		TiN_right_corner_botleft[1] + 2
	]
	ret_cell.add(
		gdstk.rectangle(contact_right_corner_botleft, contact_right_corner_topright, layer=LAYER_CT2TIN, datatype=0)
	)
	## GND
	gnd_line_right_corner_botright = [
		+SIG_width / 2 + gap + GND_width,
		RF_PAD_SIZE + taper_length
	]
	gnd_line_right_corner_topright= [
		+SIG_width / 2 + gap,
		RF_PAD_SIZE + taper_length + length
	]
	gnd_line_right = gdstk.rectangle(gnd_line_right_corner_botright, gnd_line_right_corner_topright, layer=LAYER_MET, datatype=0)
	ret_cell.add(gnd_line_right)
	ret_cell.add(gdstk.Reference(CPW_PAD, origin=(0, 2*(RF_PAD_SIZE + taper_length) + length), x_reflection=True))
	return ret_cell

def new_Load_PIN_cell(length, cell_name):
	ret_cell = gdstk.Cell(cell_name)
	ret_cell.add(gdstk.Reference(CPW_PAD, origin=(0,0)))
	## GND
	gnd_line_left_corner_botleft = [
		-SIG_width / 2 - gap - GND_width,
		RF_PAD_SIZE + taper_length
	]
	gnd_line_left_corner_topright= [
		-SIG_width / 2 - gap + 9, # <--- to fit PIN structure within GND line
		RF_PAD_SIZE + taper_length + length
	]
	gnd_line_left = gdstk.rectangle(gnd_line_left_corner_botleft, gnd_line_left_corner_topright, layer=LAYER_MET, datatype=0)
	ret_cell.add(gnd_line_left)
	## SIG
	short_line_corner_botleft = [
		-SIG_width / 2,
		RF_PAD_SIZE + taper_length
	]
	short_line_corner_topright= [
		+SIG_width / 2,
		RF_PAD_SIZE + taper_length + length
	]
	ret_cell.add(
		gdstk.rectangle(short_line_corner_botleft, short_line_corner_topright, layer=LAYER_MET, datatype=0)
	)
	## PIN
	PIN, end_o = PIN_structure(length, [-9.5, -31], f"PIN_L{length}")
	PIN_origin = [
		0,
		RF_PAD_SIZE + taper_length
	]
	ret_cell.add(
		gdstk.Reference(PIN, origin=PIN_origin)
	)
	## GND
	gnd_line_right_corner_botright = [
		+SIG_width / 2 + gap + GND_width,
		RF_PAD_SIZE + taper_length
	]
	gnd_line_right_corner_topleft= [
		+SIG_width / 2 + gap - 9, # <--- to fit PIN structure within GND line
		RF_PAD_SIZE + taper_length + length
	]
	gnd_line_right = gdstk.rectangle(gnd_line_right_corner_botright, gnd_line_right_corner_topleft, layer=LAYER_MET, datatype=0)
	ret_cell.add(gnd_line_right)
	ret_cell.add(gdstk.Reference(CPW_PAD, origin=(0, 2*(RF_PAD_SIZE + taper_length) + length), x_reflection=True))
	return ret_cell

def new_label_cell(text, cell_name, layer=LAYER_MET):
	ret_cell = gdstk.Cell(cell_name)
	text = gdstk.text(text, 150, (0,0), layer=layer, datatype=0)
	ret_cell.add(*text)
	return ret_cell

top_cell = gdstk.Cell("top_cell")

CPWL2500_01 = new_CPW_cell(2500, "CPW_L2.5mm"); CPWL2500_01_label = new_label_cell("L2.5mm", "CPW_L2.5mm_label")
CPWL5000_01 = new_CPW_cell(5000, "CPW_L5.0mm"); CPWL5000_01_label = new_label_cell("L5.0mm", "CPW_L5.0mm_label")
Short_01 = new_Short_cell(100, "Short_L100um"); Short_01_label = new_label_cell("Short", "Short_L100um_label")
Open_01 = new_Open_cell(100, "Open_L100um"); Open_01_label = new_label_cell("Open", "Open_L100um_label")
Load_01 = new_Load_cell(100, "Load_L100um"); Load_01_label = new_label_cell("Load (50 Ohm)", "Load_L100um_label")
Load_02 = new_Load_PIN_cell(100, "Load_PIN_L100um"); Load_02_label = new_label_cell("Load PIN", "Load_PIN_L100um_label")
Thru_01 = new_CPW_cell(100, "Thru_L100um"); Thru_01_label = new_label_cell("Thru", "Thru_L100um_label")

CPWL5000_01_origin			= [1500,    0]
CPWL5000_01_label_origin	= [1750,    0]

CPWL2500_01_origin			= [   0,    0]
CPWL2500_01_label_origin	= [ 250,    0]
Short_01_origin				= [   0, 4900]
Short_01_label_origin		= [ 250, 4900]
Open_01_origin				= [   0, 4400]
Open_01_label_origin		= [ 250, 4400]
Load_01_origin				= [   0, 3900]
Load_01_label_origin		= [ 250, 3900]
Load_02_origin				= [   0, 3400]
Load_02_label_origin		= [ 250, 3400]
Thru_01_origin			    = [   0, 2900]
Thru_01_label_origin		= [ 250, 2900]

top_cell.add(gdstk.Reference(CPWL2500_01, origin=CPWL2500_01_origin))
top_cell.add(gdstk.Reference(CPWL2500_01_label, origin=CPWL2500_01_label_origin))
top_cell.add(gdstk.Reference(CPWL5000_01, origin=CPWL5000_01_origin))
top_cell.add(gdstk.Reference(CPWL5000_01_label, origin=CPWL5000_01_label_origin))
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
LABEL_LAYER36 = new_label_cell("Layer 36: METAL", "LABEL_LAYER36", layer=LAYER_MET)
LABEL_LAYER38 = new_label_cell("Layer 38: TIN", "LABEL_LAYER38", layer=LAYER_TIN)
LABEL_LAYER39 = new_label_cell("Layer 39: CONTACT TO TIN", "LABEL_LAYER39", layer=LAYER_CT2TIN)
LABEL_LAYER41 = new_label_cell("Layer 41: PAD WINDOW", "LABEL_LAYER41", layer=LAYER_PW)
LABEL_LAYER36_origin		= [2000, 2750]
LABEL_LAYER38_origin		= [2000, 2600]
LABEL_LAYER39_origin		= [2000, 2450]
LABEL_LAYER41_origin		= [2000, 2300]
top_cell.add(gdstk.Reference(LABEL_LAYER36, origin=LABEL_LAYER36_origin))
top_cell.add(gdstk.Reference(LABEL_LAYER38, origin=LABEL_LAYER38_origin))
top_cell.add(gdstk.Reference(LABEL_LAYER39, origin=LABEL_LAYER39_origin))
top_cell.add(gdstk.Reference(LABEL_LAYER41, origin=LABEL_LAYER41_origin))

LIB.add(top_cell, *top_cell.dependencies(True))
LIB.write_gds("RF_calib_pattern.gds")
