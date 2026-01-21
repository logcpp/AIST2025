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

RF_PAD_PITCH = 125     # RF pad pitch
RF_PAD_SIZE = 110      # RF pad size

# design parameters of CPW
taper_length = 50 # um
SIG_width = 8 # um
GND_width = 35 # um # => ~50 Ohm
gap = 15 # um

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
		TiN_left_corner_botleft[0] + 6,
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
		TiN_right_corner_topright[0] - 6,
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

# top_cell = gdstk.Cell("top_cell")

# CPWL2500_01 = new_CPW_cell(2500, "CPW_L2.5mm")
# CPWL5000_01 = new_CPW_cell(5000, "CPW_L5.0mm")
# Short_01 = new_Short_cell(100, "SHORT_L100um")
# Open_01 = new_Open_cell(100, "OPEN_L100um")
# Load_01 = new_Load_cell(100, "LOAD_L100um")
# Through_01 = new_CPW_cell(100, "THROUGH_L100um")

# CPWL2500_01_origin = [0, 0]
# CPWL5000_01_origin = [-400, -200]
# Short_01_origin = [0, 4500]
# Open_01_origin = [0, 4000]
# Load_01_origin = [0, 3500]
# Through_01_origin = [0, 3000]

# top_cell.add(gdstk.Reference(CPWL2500_01, origin=CPWL2500_01_origin))
# top_cell.add(gdstk.Reference(CPWL5000_01, origin=CPWL5000_01_origin))
# top_cell.add(gdstk.Reference(Short_01, origin=Short_01_origin))
# top_cell.add(gdstk.Reference(Open_01, origin=Open_01_origin))
# top_cell.add(gdstk.Reference(Load_01, origin=Load_01_origin))
# top_cell.add(gdstk.Reference(Through_01, origin=Through_01_origin))

# LIB.add(top_cell, *top_cell.dependencies(True))
# LIB.write_gds("RF_calib_pattern.gds")
