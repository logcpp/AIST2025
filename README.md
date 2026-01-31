# AIST 2025 GDS design
created on: 2026/01/10
last change: 2026/01/31

## Checkpoints
- FlexPath(..., tolerance=1e-3)
- make vertical(), arc_\*() to add to ret_cell by default -> OK (2026/01/31)
- check PIN injection-type P+ and N+ pad orientation -> OK, symmetric in MZM (2026/01/31)
- check PIN MZM pad configuration and RC constants -> for higher modulation speed
- check 4x4 GC array optimized pitch for:
	- 4 inputs -> 4x4 outputs -> OK (2026/01/31)
	- 4x4 inputs -> 4x4 PD arrays (potential) -> splitting OK (2026/01/31)
- place no dummy at SSC area with large MFD -> OK (2026/01/31)
- dicing line 35~50 um width, including polishing length -> OK (2026/01/31)
- remove GC array markers (for Micro-manipulator) of the right column and add to other remaining space -> OK (2026/01/31)
- NODMY area for GC and micromanipulator markers -> added for GC, no need for mani markers (2026/01/31)
- make sure metal pattern are not easily shorted due to Si WG below -> OK (2026/01/31)
- check all resistance are estimated correctly
- check CPW impedance is estimated correctly -> OK, 50~51 Ohm (2026/01/31)

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
- SSC to GC (Ren) w/o NODMY
- SSC to GC (Ren) w/ NODMY
- SSC to GC (AIST)
- 1x2 MMI test pattern
- PIN loss test pattern (for ring, MZM) -> maybe with GC-GC ports
- TiN resistors of different sizes

## Experiments to do
- PIN MZM measurement
	- L=500,200: PIN resistance, DC bias switching, RF bandwidth
	- L=200w/TERM,200w/oTERM: PIN resistance, TIN resistance, DC bias switching, RF bandwidth
- GC 1x4 in -> GC 4x4 out (MVM)
- GC 1x4 in -> GC 4x1 out (MVM)
- GC 4x4 in -> SLM -> PD? (MVM)
- RF SOLT calibration
- RF Thru L/2L (L=1.0mm) de-embedding
- passive test patterns
	- 1x2 MMI
	- 2x2 MMI
	- GC-GC B2B (AIST, Ren)
	- GC-wg-GC propagation loss (AIST)
	- ssc-GC (AIST, Ren, Ren w/o NODMY)
- active test patterns
	- TiN resistance measurement
	- PIN modulation loss 
