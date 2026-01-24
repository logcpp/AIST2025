# AIST 2025 design script
# created on: 2026/01/18
# last change: 2026/01/18

import gdstk
import numpy as np
import lib_v4 as lib
import lib_v4_RF as lib_RF

top_cell = gdstk.Cell("TOP_Ren")

#---------- total chip area ----------#
CHIP_WIDTH = 5000
CHIP_HEIGHT = 10000
JIANG_HEIGHT = 3500
SHERRY_HEIGHT = 1500
chip_area_JIANG = gdstk.rectangle([0, 0], [CHIP_WIDTH, JIANG_HEIGHT], layer=0, datatype=0)
chip_area_SHERRY_REN = gdstk.rectangle([0, JIANG_HEIGHT], [CHIP_WIDTH, JIANG_HEIGHT+SHERRY_HEIGHT], layer=0, datatype=0)
chip_area_SUGANUMA_LEFT = gdstk.rectangle([0, JIANG_HEIGHT+SHERRY_HEIGHT], [CHIP_WIDTH/2, CHIP_HEIGHT], layer=0, datatype=0)
chip_area_SUGANUMA_RIGHT = gdstk.rectangle([CHIP_WIDTH/2, JIANG_HEIGHT+SHERRY_HEIGHT], [CHIP_WIDTH, CHIP_HEIGHT], layer=0, datatype=0)
top_cell.add(
	chip_area_JIANG,
	chip_area_SHERRY_REN,
	chip_area_SUGANUMA_LEFT,
	chip_area_SUGANUMA_RIGHT,
)

#---------- GC test patterns ----------#
GC_pitch = 120 # <-- based on simulation
GC_io_distance = 500 # distance between array **centers**
GC_input_origin = [
	550,
	CHIP_HEIGHT - 1000,
]
GC_output_origin = [
	GC_input_origin[0],
	GC_input_origin[1] + GC_io_distance - GC_pitch*1.5,
]
GC4x1_output_origin = [
	GC_input_origin[0] + 1.5*GC_pitch + 15,
	GC_input_origin[1] - 1.5*GC_pitch - 15
]
GC_grating_num = 20
GC_grating_pitch = 0.6
GC_grating_angle_deg = 35
GC_taper_length = 10
GC_T20P0_6A35L10 = lib.new_GC_cell(GC_grating_num, GC_grating_pitch, GC_grating_angle_deg, GC_taper_length, "GC_T20P0.6A35L10")
top_cell.add(
	# input 1x4 GC array
	gdstk.Reference(
		GC_T20P0_6A35L10,
		# rotation=np.pi/2,
		origin=GC_input_origin,
		columns=4,
		rows=1,
		spacing=(GC_pitch, GC_pitch)
	),
	# output 4x1 GC array (optional)
	gdstk.Reference(
		GC_T20P0_6A35L10,
		rotation=np.pi/2,
		origin=GC4x1_output_origin,
		columns=4,
		rows=1,
		spacing=(GC_pitch, GC_pitch)
	),
	# output 4x4 GC array
	gdstk.Reference(
		GC_T20P0_6A35L10,
		# rotation=-np.pi/2,
		origin=GC_output_origin,
		columns=4,
		rows=4,
		spacing=(GC_pitch, GC_pitch)
	)
)
# markers for µ-Manipulator
Mani_marker_size = 200
Mani_marker_pitch = 500
Mani_marker_cell = gdstk.Cell("Mani_marker")
Mani_marker_cell.add(
	gdstk.rectangle((-100,-100),(100,100), layer=lib.LAYER_MET, datatype=0),
	# gdstk.rectangle((-150,-150),(150,150), layer=lib.LAYER_NODMY, datatype=0),
)
top_cell.add(
	gdstk.Reference(
		Mani_marker_cell,
		origin=[
			GC_input_origin[0] - 0.5*Mani_marker_pitch,
			GC_input_origin[1] - 1.0*Mani_marker_size,
		],
		columns=1,
		rows=2,
		spacing=(500+3*GC_pitch, Mani_marker_pitch - 100)
	),
	gdstk.Reference(
		Mani_marker_cell,
		origin=[
			GC_input_origin[0] - 0.5*Mani_marker_pitch,
			GC_input_origin[1] + 4.0*Mani_marker_size,
		],
		columns=1,
		rows=1,
		spacing=(500+3*GC_pitch, Mani_marker_pitch)
	)
)

#---------- MZM test patterns ----------#
o = [745-0.35, JIANG_HEIGHT+457-0.616]
PINL200_01_origin = [o[0]+ 305, o[1],]
PINL500_01_origin = [o[0]+   0, o[1],]
pin_mzm_L200, pin_mzm_L200_end_o = lib.new_PIN_AMZM_cell(200, "CR_PINL200AMZ")
pin_mzm_L500, pin_mzm_L500_end_o = lib.new_PIN_AMZM_cell(500, "CR_PINL500AMZ")
top_cell.add(gdstk.Reference(pin_mzm_L200, origin=PINL200_01_origin, rotation=np.pi/2))
top_cell.add(gdstk.Reference(pin_mzm_L500, origin=PINL500_01_origin, rotation=np.pi/2))
PINL100TERM_02_origin = [o[0]- 250 + 1.2, o[1]+ 850,]
PINL200TERM_02_origin = [o[0]+ 390 + 1.2, o[1]+ 850,]
pin_mzm_L100_TERM, pin_mzm_L100_TERM_end_o = lib.new_PIN_AMZM_TERM_cell(100, "CR_PINL100AMZ_TERM")
pin_mzm_L200_TERM, pin_mzm_L200_TERM_end_o = lib.new_PIN_AMZM_TERM_cell(200, "CR_PINL200AMZ_TERM")
top_cell.add(gdstk.Reference(pin_mzm_L100_TERM, origin=PINL100TERM_02_origin, rotation=-np.pi/2))
top_cell.add(gdstk.Reference(pin_mzm_L200_TERM, origin=PINL200TERM_02_origin, rotation=-np.pi/2))

#---------- right ssc region ----------#
ssc_right_origin = [CHIP_WIDTH-150, JIANG_HEIGHT]
ssc_right = lib.new_ssc_cell(lib.LAYER_SiWG, "ssc_right", position='right')
top_cell.add(
	# ssc for MZM
	gdstk.Reference(
		ssc_right, rotation=-np.pi/2, x_reflection=True,
		origin=[
			ssc_right_origin[0],
			ssc_right_origin[1]
		],
		columns=1,
		rows=16,
		spacing=(0, lib.ssc_pitch)
	),
	# ssc for GC array
	gdstk.Reference(
		ssc_right, rotation=-np.pi/2, x_reflection=True,
		origin=[
			ssc_right_origin[0]-16*lib.ssc_pitch,
			ssc_right_origin[1]
		],
		columns=1,
		rows=22,
		spacing=(0, lib.ssc_pitch)
	),
)
loop_straight_length = 0 # um
loop_right = lib.new_loopback_cell(loop_straight_length, lib.LAYER_SiWG, "loopback_right")
top_cell.add(
	# loopbacks of ssc for MZM
	gdstk.Reference(
		loop_right, rotation=np.pi/2, x_reflection=True,
		origin=[
			ssc_right_origin[0] - lib.ssc_pitch,
			ssc_right_origin[1] + lib.ssc_length + lib.dicing_length,
		]
	),
	gdstk.Reference(
		loop_right, rotation=np.pi/2,
		origin=[
			ssc_right_origin[0] - lib.ssc_pitch*14,
			ssc_right_origin[1] + lib.ssc_length + lib.dicing_length,
		]
	),
	# loopbacks of ssc for GC array
	gdstk.Reference(
		loop_right, rotation=np.pi/2, x_reflection=True,
		origin=[
			ssc_right_origin[0] - lib.ssc_pitch*(16+21),
			ssc_right_origin[1] + lib.ssc_length + lib.dicing_length,
		]
	),
)

#---------- PIN MZM routing ----------#
ssc_point = [
	ssc_right_origin[0],
	ssc_right_origin[1] + lib.ssc_length + lib.dicing_length,
]
PINL500_01_route = lib.PINL500_01_route_cell(PINL500_01_origin, pin_mzm_L500_end_o, ssc_point, lib.LAYER_SiWG, "PINL500_01_route", right_end=PINL200TERM_02_origin)
PINL200_01_route = lib.PINL200_01_route_cell(PINL200_01_origin, pin_mzm_L200_end_o, ssc_point, lib.LAYER_SiWG, "PINL200_01_route", right_end=PINL200TERM_02_origin)
PINL100TERM_02_route = lib.PINL100TERM_02_route_cell(PINL100TERM_02_origin, pin_mzm_L100_TERM_end_o, ssc_point, lib.LAYER_SiWG, "PINL100TERM_02_route")
PINL200TERM_02_route = lib.PINL200TERM_02_route_cell(PINL200TERM_02_origin, pin_mzm_L200_TERM_end_o, ssc_point, lib.LAYER_SiWG, "PINL200TERM_02_route")
top_cell.add(gdstk.Reference(PINL500_01_route, origin=(0,0)))
top_cell.add(gdstk.Reference(PINL200_01_route, origin=(0,0)))
top_cell.add(gdstk.Reference(PINL100TERM_02_route, origin=(0,0)))
top_cell.add(gdstk.Reference(PINL200TERM_02_route, origin=(0,0)))

#---------- GC array routing ----------#
# GC 4x4 array
ssc_point = [
	ssc_right_origin[0] - lib.ssc_pitch*(16+21),
	ssc_right_origin[1] + lib.ssc_length + lib.dicing_length,
]
GC4x4_route = lib.GC4x4_route_cell(GC_output_origin, GC_pitch, ssc_point, lib.LAYER_SiWG, "GC4x4_route")
top_cell.add(gdstk.Reference(GC4x4_route, origin=(0,0)))
# GC 4x1 output
ssc_point = [
	ssc_right_origin[0] - lib.ssc_pitch*(16+21),
	ssc_right_origin[1] + lib.ssc_length + lib.dicing_length,
]
GC4x1output_route = lib.GC4x1output_route_cell(GC4x1_output_origin, GC_pitch, ssc_point, lib.LAYER_SiWG, "GC4x1output_route")
top_cell.add(gdstk.Reference(GC4x1output_route, origin=(0,0)))
# GC 1x4 input
GC1x4input_route = lib.GC1x4input_route_cell(GC_input_origin, GC_pitch, lib.LAYER_SiWG, "GC1x4input_route", PINL500_01_origin, PINL200_01_origin, PINL100TERM_02_origin, PINL200TERM_02_origin, pin_mzm_L500_end_o, pin_mzm_L200_end_o, pin_mzm_L100_TERM_end_o, pin_mzm_L200_TERM_end_o)
top_cell.add(gdstk.Reference(GC1x4input_route, origin=(0,0)))


#---------- RF calibration pattern ----------#

CPW2L_01 = lib_RF.new_CPW_cell(2000, "CPW_L3.0mm")
CPW1L_01 = lib_RF.new_CPW_cell(1000, "CPW_L1.5mm")
Short_01 = lib_RF.new_Short_cell(100, "SHORT_L100um")
Open_01 = lib_RF.new_Open_cell(100, "OPEN_L100um")
Load_01 = lib_RF.new_Load_cell(100, "LOAD_L100um")
Through_01 = lib_RF.new_CPW_cell(100, "THROUGH_L100um")

CPW_o = [300, 3500+1500+10]

CPW1L_01_origin   = [CPW_o[0]+1000, CPW_o[1]+3800 - 46]
CPW2L_01_origin   = [CPW_o[0]+ 170, CPW_o[1]+ 170]
Short_01_origin   = [CPW_o[0]+ 170, CPW_o[1]+3360]
Open_01_origin    = [CPW_o[0]+ 170, CPW_o[1]+2930]
Load_01_origin    = [CPW_o[0]+ 170, CPW_o[1]+2500]
Through_01_origin = [CPW_o[0]+1100 - 22, CPW_o[1]-1000 + 50 + 8.616]

top_cell.add(gdstk.Reference(CPW2L_01, origin=CPW2L_01_origin))
top_cell.add(gdstk.Reference(CPW1L_01, origin=CPW1L_01_origin))
top_cell.add(gdstk.Reference(Short_01, origin=Short_01_origin))
top_cell.add(gdstk.Reference(Open_01, origin=Open_01_origin))
top_cell.add(gdstk.Reference(Load_01, origin=Load_01_origin))
top_cell.add(gdstk.Reference(Through_01, origin=Through_01_origin, rotation=np.pi/2))

lib.LIB.add(top_cell, *top_cell.dependencies(True))
lib.LIB.write_gds("AIST2025_CR_v4.gds")
