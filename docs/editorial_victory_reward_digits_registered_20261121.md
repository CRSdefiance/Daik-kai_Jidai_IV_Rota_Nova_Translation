# Victory reward numbers

The three original victory reward notices now use regular-width digits. Captured supplies keep food before water and give both quantities in barrels. Captured gold and the national reward stay separate. The wording and original reward calculations carry forward. Four number-format calls change. [Source and registered review](../releases/all_routes_editorial_20261121_victory_reward_digits_candidate/verification/registered_review.json)

The paired emulator replay showed 109 barrels of food, 103 barrels of water and 6055 gold. Both notices matched their complete native glyph masks, and 19 other frames matched the previous build. The national reward and uncommon amount lengths were checked offline. The replay used the established copied save and 40-byte position fixture. [Gameplay comparison](../releases/all_routes_editorial_20261121_victory_reward_digits_candidate/verification/victory_rewards_live.png)

The captured-gold paragraph wrapped after “from” at the observed amount and split “captured ships” with a one-digit amount. The national-reward stress example could strand “gold.” Both line breaks were corrected in the following release. [Original previews](../releases/all_routes_editorial_20261121_victory_reward_digits_candidate/verification/stored_panels_01.png) · [Registered correction](editorial_victory_reward_wrap_registered_20261121.md)

Startup and the 17 focused tests passed. The clean-input patch reconstructs the ROM byte for byte. [Testing ROM and patch](../releases/all_routes_editorial_20261121_victory_reward_digits_candidate/README.md)

The Drive copy was updated in place at 14:51 UTC on November 21. Its authenticated readback matched the registered SHA-256 `04d953314bf0deaff07f353275707d65a94af84cb0a263d6f2e9cb41f9a98208`. It is the folder’s only `.nds`. [Latest Build on Drive](https://drive.google.com/file/d/1vM8IXRtSIMvFR4F-TR3oPLtcuhFobGwa/view?usp=drivesdk)

Checkpoint cleanup removed 12 verification files totaling 61,092,874 bytes, including the duplicate clean reconstruction, two copied saves, and test scratch files. [Cleanup receipt](../work/victory_reward_digits_20261121/checkpoint_cleanup.json)
