# Search foraging reports

All five voices now keep the water amount and unit on one row and the food amount and unit on the next. The existing wording, voice choices, and water-before-food substitutions carry forward. The thirty-five native pages cover zero, short, unequal, and maximum source-bound amounts. [Exact source and registered decisions](../releases/all_routes_editorial_20261121_search_forage_wrap_candidate/verification/registered_review.json)

The paired emulator replay held Charles Rochefort’s report of 175 barrels of water and 140 barrels of food. The full glyph mask, other views, fleet state, and return to sailing passed. The four other voices were checked offline. [Gameplay comparison](../releases/all_routes_editorial_20261121_search_forage_wrap_candidate/verification/search_forage_wrap_live.png)

Startup and 17 focused tests passed. The clean-input patch reconstructs the ROM byte for byte. [Testing ROM and patch](../releases/all_routes_editorial_20261121_search_forage_wrap_candidate/README.md)

The sole Drive `.nds` was updated in place on November 21 at 15:39 UTC. The authenticated readback matched the registered SHA-256 `d45f78b0c00697c030d9f88909801c8a03545860214b35e266a5a73f1d8df516`. [Latest Build on Drive](https://drive.google.com/file/d/1vM8IXRtSIMvFR4F-TR3oPLtcuhFobGwa/view?usp=drivesdk)

Checkpoint cleanup removed 12 files totaling 61,093,374 bytes, including the duplicate clean reconstruction, two copied saves, and test scratch files. [Cleanup receipt](../work/search_forage_wrap_20261121/checkpoint_cleanup.json)
