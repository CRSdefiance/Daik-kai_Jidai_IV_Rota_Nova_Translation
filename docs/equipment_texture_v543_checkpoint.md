# V543 equipment texture checkpoint

The previous goal turn made progress by integrating the 17 screen-plaque source
grain correction in V542. V543 extends that correction to the dynamic equipment
heading and item hints, including the previously delegated widths34/40/88.

The old 1408-byte tile and original helper were verified exactly in the current
staged pool using their resident offsets. Only tile interior colors and three
BEQ instructions change. There is no new helper or allocation, section growth,
heap/startup/cache change, or unrelated instruction/data change.

All 470 controlled painter width/framebuffer cases and nine invalid contracts
pass. Actual cold-boot captured gameplay verifies five occupied names/papers,
5120 exact icon pixels, three short/heading hints, and 50 whole Sailor Info plaque
crops. All 56 regression frames are exact V542. The clean patch reconstructs V543.
All original/source-copy saves remain unchanged; the authorized inventory fixture
is temporary test RAM and is not shipped. Normal acquisition is not claimed.

See [build notes](../work/analysis/equipment_texture_v543/BUILD_NOTES_V543.md)
and [open texture defect](plaque_background_texture_defect.md). All 18 entries
remain incomplete. Continue original bevel comparisons, town/other plaques,
embedded/legacy graphics and remaining contexts; retain all 22 requirements.
