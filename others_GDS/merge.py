# AIST 2025 design merging script
# created on: 2026/01/23
# last change: 2026/01/23

import gdstk
import numpy as np

lib_ALL = gdstk.Library()
top_cell = lib_ALL.new_cell("TOP")

CHIP_WIDTH = 5000
CHIP_HEIGHT = 10000

AIST_MPW_LIB = gdstk.read_gds("../MPW_Cell/MPW_Cell_5x10.gds")
JIANG_LIB = gdstk.read_gds("../others_GDS/Jiang_20260126.gds")
SHERRY_LIB_1 = gdstk.read_gds("../others_GDS/Sherry_20260126_1.gds")
SHERRY_LIB_2 = gdstk.read_gds("../others_GDS/Sherry_20260126_2_2.gds")
SUGANUMA_LIB = gdstk.read_gds("../others_GDS/20260126_SUGANUMA.gds")
REN_LIB = gdstk.read_gds("../design/AIST2025_CR_v6.gds")

AIST_MPW_LIB.rename_cell("MPW_cell", "BASE")
JIANG_LIB.rename_cell("Top_Final_All_Loops", "Jiang")
SHERRY_LIB_1.rename_cell("MAIN_ARRAY", "Sherry_1")
SHERRY_LIB_2.rename_cell("MAIN_ARRAY", "Sherry_2")
SUGANUMA_LIB.rename_cell("TOP", "Suganuma")
REN_LIB.rename_cell("TOP_Ren", "Ren")

# add rectangle regions for each pattern
CHIP_WIDTH = 5000
CHIP_HEIGHT = 10000
JIANG_HEIGHT = 3500
layer = 50 # chip area
chip_area_JIANG = gdstk.rectangle([0, 0], [CHIP_WIDTH, JIANG_HEIGHT], layer=layer, datatype=0)
chip_area_SUGANUMA_LEFT = gdstk.rectangle([0, JIANG_HEIGHT], [CHIP_WIDTH/2, CHIP_HEIGHT], layer=layer, datatype=0)
chip_area_SUGANUMA_RIGHT = gdstk.rectangle([CHIP_WIDTH/2, JIANG_HEIGHT], [CHIP_WIDTH, CHIP_HEIGHT], layer=layer, datatype=0)
top_cell.add(
	chip_area_JIANG,
	chip_area_SUGANUMA_LEFT,
	chip_area_SUGANUMA_RIGHT,
)

# add NODMY region for additional dicing
layer = 60 # NODMY
dicing_width = 50
dicing_JIANG = gdstk.rectangle([dicing_width, JIANG_HEIGHT-dicing_width], [CHIP_WIDTH-dicing_width, JIANG_HEIGHT+dicing_width], layer=layer, datatype=0)
dicing_SUGANUMA = gdstk.rectangle([CHIP_WIDTH/2-dicing_width, JIANG_HEIGHT+dicing_width], [CHIP_WIDTH/2+dicing_width, CHIP_HEIGHT-dicing_width], layer=layer, datatype=0)
top_cell.add(
	dicing_JIANG,
	dicing_SUGANUMA,
)

# remove layer 0
for ext_lib in [AIST_MPW_LIB, JIANG_LIB, SHERRY_LIB_1, SHERRY_LIB_2, SUGANUMA_LIB, REN_LIB]:
	for cell in ext_lib.cells:
		for poly in list(cell.polygons):
			if poly.layer == 0:
				cell.remove(poly)
		for path in list(cell.paths):
			if path.layers == 0:
				cell.remove(path)
		for label in list(cell.labels):
			if label.layer == 0:
				cell.remove(label)

# remove SSCs
def bbox_overlap(b1, b2):
    return not (
        b1[1][0] < b2[0][0] or
        b1[0][0] > b2[1][0] or
        b1[1][1] < b2[0][1] or
        b1[0][1] > b2[1][1]
    )
exclude_bbox_left = ((-500-CHIP_WIDTH/2, 0-CHIP_HEIGHT/2), (500-CHIP_WIDTH/2, 5000-CHIP_HEIGHT/2))
exclude_bbox_right = ((-500+CHIP_WIDTH/2, 0-CHIP_HEIGHT/2), (500+CHIP_WIDTH/2, CHIP_HEIGHT-CHIP_HEIGHT/2))
cell = AIST_MPW_LIB['ssc_array']
for ref in cell.references:
	ref_bbox = ref.bounding_box()
	if bbox_overlap(ref_bbox, exclude_bbox_left) or bbox_overlap(ref_bbox, exclude_bbox_right):
		cell.remove(ref)
for poly in cell.polygons:
	bbox = poly.bounding_box()
	if bbox_overlap(ref_bbox, exclude_bbox_left) or bbox_overlap(ref_bbox, exclude_bbox_right):
		cell.remove(poly)

# merge and avoid same names
for ext_lib in [AIST_MPW_LIB, JIANG_LIB, SHERRY_LIB_1, SHERRY_LIB_2, SUGANUMA_LIB, REN_LIB]:
	cell_map = {cell.name: cell for cell in lib_ALL.cells}
	for cell in ext_lib.cells:
		if cell.name in cell_map:
			ext_cell = cell_map[cell.name]
		else:
			lib_ALL.add(cell)
			cell_map[cell.name] = cell
top_cell.add(
	gdstk.Reference(AIST_MPW_LIB["BASE"], origin=(2500,5000)),
	gdstk.Reference(JIANG_LIB["Jiang"], origin=(450,800)),
	gdstk.Reference(SHERRY_LIB_1["Sherry_1"], origin=(2380, 300+3500), rotation=np.pi/2),
	gdstk.Reference(SHERRY_LIB_2["Sherry_2"], origin=(3350, 300+3500), rotation=np.pi/2),
	gdstk.Reference(SUGANUMA_LIB["Suganuma"], origin=(CHIP_WIDTH/2, CHIP_HEIGHT-5000)),
	gdstk.Reference(REN_LIB["Ren"], origin=(0, 0)),
)

lib_ALL.write_gds("AIST2025_TLab.gds")
