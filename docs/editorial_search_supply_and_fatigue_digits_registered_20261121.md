# Shore Search counts and fatigue

Regular-width digits now appear in both fatigue notices and all five foraging voices. The original signed fatigue logic, capped stored fatigue, and reported adjustment carry forward. The foraging report and supply update both receive water first and food second. The original unit is barrels for both. The battle capture notice uses the reverse order. [Exact source and release decisions](../releases/all_routes_editorial_20261121_search_supply_and_fatigue_digits_candidate/verification/registered_review.json)

The same copied save and original Search inputs showed a requested fatigue reduction of 15 at a hot spring and an increase of 3 after a failed search. Continued Search produced Charles Rochefort’s report of 175 barrels of water and 140 of food. The paired runs matched the relevant fleet state and return to sailing. The replay used fleet-position setups at the original shoreline. Forty native pages and 1,920 formatter checks passed. [Fatigue comparison](../releases/all_routes_editorial_20261121_search_supply_and_fatigue_digits_candidate/verification/search_counts_live.png) · [Foraging comparison](../releases/all_routes_editorial_20261121_search_supply_and_fatigue_digits_candidate/verification/search_forage_live.png)

The foraging paragraph split the water quantity from “of water” in this build. The next registered build keeps both resource phrases whole. [Native previews](../releases/all_routes_editorial_20261121_search_supply_and_fatigue_digits_candidate/verification/portrait_sheet_01.png) · [Registered follow-up](editorial_search_forage_wrap_registered_20261121.md)

Startup and 17 focused tests passed. The clean-input patch reconstructs the ROM byte for byte. [Testing ROM and patch](../releases/all_routes_editorial_20261121_search_supply_and_fatigue_digits_candidate/README.md)

The sole Drive `.nds` was updated in place on November 21 at 15:30 UTC. Its authenticated readback matched the registered SHA-256 `d97eabf0d3aab25581820f90280495639000c490a864632b89e9c1a7a4e65d2a`. [Latest Build on Drive](https://drive.google.com/file/d/1vM8IXRtSIMvFR4F-TR3oPLtcuhFobGwa/view?usp=drivesdk)

Checkpoint cleanup removed 23 verification files totaling 95,434,660 bytes. The cleanup included the duplicate reconstruction, copied saves, test scratch files and RAM snapshots unused by the final comparisons. [Cleanup receipt](../work/search_supply_and_fatigue_digits_20261121/checkpoint_cleanup.json)
