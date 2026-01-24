# AIST 2025 GDS design
created on: 2026/01/10
last change: 2026/01/18

## Checkpoints
- FlexPath(..., tolerance=1e-3)
- make vertical(), arc_\*() to add to ret_cell by default
- check PIN injection-type P+ and N+ pad orientation

- check PIN MZM pad configuration and RC constants -> for higher modulation speed
- check 4x4 GC array optimized pitch for:
	- 4 inputs -> 4x4 outputs
	- 4x4 inputs -> 4x4 PD arrays (potential)

- place no dummy at SSC area with large MFD
- dicing line 35~50 um width, including polishing length
- remove GC array markers (for Micro-manipulator) of the right column and add to other remaining space

## Test patterns
- 50 Ohm load
- metal coplanar waveguides
	- Short
	- Load
	- Open
	- Through
	- L & 2L of through coplanar waveguides
- PIN doped Si with different lengths
- TiN MZM test patterns (w/ and w/o trench)
- GC to GC B2B test port

## Experiments to do
- PIN MZM measurement
	- L=500,200: PIN resistance, DC bias switching, RF bandwidth
	- L=100,200: PIN resistance, TIN resistance, DC bias switching, RF bandwidth
- GC 1x4 in -> GC 4x4 out (MVM)
- GC 1x4 in -> GC 4x1 out (MVM)
- GC 4x4 in -> SLM -> PD? (MVM)
- RF SOLT calibration
- RF Thru L/2L (L=1.0mm) de-embedding
