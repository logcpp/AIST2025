# AIST 2025 GDS design
created on: 2026/01/10
last change: 2026/01/31

## Checkpoints
- FlexPath(..., tolerance=1e-3) -> OK (2026/02/01)
- make vertical(), arc_\*() to add to ret_cell by default -> OK (2026/01/31)
- check PIN injection-type P+ and N+ pad orientation -> OK, symmetric in MZM (2026/01/31)
- check PIN MZM pad configuration and RC constants -> for higher modulation speed -> R=24Ω for PPP,NPP,CT2PN patterns, OK (2026/02/01)
- check 4x4 GC array optimized pitch for:
	- 4 inputs -> 4x4 outputs -> OK (2026/01/31)
	- 4x4 inputs -> 4x4 PD arrays (potential) -> splitting OK (2026/01/31)
- place no dummy at SSC area with large MFD -> OK (2026/01/31)
- dicing line 35~50 um width, including polishing length -> OK (2026/01/31)
- remove GC array markers (for Micro-manipulator) of the right column and add to other remaining space -> OK (2026/01/31)
- NODMY area for GC and micromanipulator markers -> added for GC, no need for mani markers (2026/01/31)
- make sure metal pattern are not easily shorted due to Si WG below -> OK (2026/01/31)
- check all resistance are estimated correctly -> OK (2026/02/01)
- check CPW impedance is estimated correctly -> OK, 50~51 Ohm (2026/01/31)

## Test patterns
- 50 Ohm load -> OK (2026/02/01)
- metal coplanar waveguides -> OK (2026/02/01)
	- Short
	- Load
	- Open
	- Through
	- L=1.0mm & 2L=2.0mm of through coplanar waveguides
- PIN doped Si with different lengths -> no enough space (2026/02/01)
- TiN MZM test patterns (w/ and w/o trench) -> can be measured by 1 channel of MZI tree (2026/02/01)
- GC to GC B2B test port -> OK (2026/02/01)
- SSC to GC (Ren) w/o NODMY -> OK (2026/02/01)
- SSC to GC (Ren) w/ NODMY -> OK (2026/02/01)
- SSC to GC (AIST) -> OK (2026/02/01)
- 1x2 MMI test pattern -> OK (2026/02/01)
- PIN loss test pattern (for ring, MZM) -> maybe with GC-GC ports -> OK with MZM (2026/02/01)
- TiN resistors of different sizes -> OK (2026/02/01)

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
