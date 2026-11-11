# Cumulative crew-notice testing candidate

## v7 promotion candidate

The fresh local test copy is `out/promotion_ready_20261110_all_routes_v7/Translation_DS_All_Routes_20261110_v7_candidate.nds`. Use it with the adjacent build manifest. The clean-input patch reconstructs the registered crew-notice ROM byte for byte. [Reconstruction receipt](verification/promotion_v7_reconstruction.json)

This build includes Rafael’s tutorials, the four reviewed storylines, the Market Trade-screen fix, the Abandon Ship menu correction, 30 shared notices and 22 crew notices. The 69 release checks and 27 repository tests apply to these exact bytes. V4701 remains the main build pending cold-boot testing and acceptance of v7.

## Registered release notes

Use `out/promotion_ready_20261110_crew_notices_v1/Translation_DS_All_Routes_Crew_Notices_20261110_candidate.nds` beside its build manifest. The [clean-input patch](translation.xdelta) applies to the clean Japanese ROM SHA-256 `f4f07c975cc293f5b2ba469747693d3dd37f2e6dfc408cf5910adf5e83d9177d`. It reproduces SHA-256 `ba630cd10bfddcc648c62f5b1bd750fe53b405d82f3ab3635adeac66ea6fa9d2` byte for byte. Patch SHA-256 is `f261b75272fb1a1ea01a1b679bcefab1577051cc53e6a9108979bdcc48e60e69`.

The build reviews 22 crew notices and confirmation lines. It keeps literal ship names, wraps portrait dialogue after substitution and preserves the existing Abandon Ship menu and all original voice slots. The focused emulator replay set the secondary ship's crew to zero and assigned it an 18-byte test name. The warning and two-line confirmation displayed the full name. No returned to the same menu and kept the ship.
