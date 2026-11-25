# Captured gold and national awards

The captured-gold notice keeps “from captured ships” on one row. Short national awards still fit on one row, and longer amounts move together with “gold.” Both English paragraphs retain their wording, substitutions, and original reward calculations. [Exact source and release decisions](../releases/all_routes_editorial_20261121_victory_reward_wrap_candidate/verification/registered_review.json)

All 44 native previews passed from one to ten decimal digits. Seven unrelated notices retained their exact display bytes. The paired emulator replay verified the revised 6055 gold notice and matched 20 other frames, including the food and water notice. The national award received offline checks. [Gameplay comparison](../releases/all_routes_editorial_20261121_victory_reward_wrap_candidate/verification/captured_gold_live.png)

Startup and 17 focused tests passed. The clean-input patch reconstructs the ROM byte for byte. [Testing ROM and patch](../releases/all_routes_editorial_20261121_victory_reward_wrap_candidate/README.md)

The sole Drive `.nds` was updated in place on November 21 at 15:00 UTC. Its authenticated readback matched the registered SHA-256 `1eb6f499b8c414c95b18d2d035efbd2db7f6ac0c1789e7452815c0ebfe570307`. [Latest Build on Drive](https://drive.google.com/file/d/1vM8IXRtSIMvFR4F-TR3oPLtcuhFobGwa/view?usp=drivesdk)

Checkpoint cleanup removed 12 verification files totaling 61,093,378 bytes, including the duplicate clean reconstruction, two copied saves, and test scratch files. [Cleanup receipt](../work/victory_reward_wrap_20261121/checkpoint_cleanup.json)

The follow-up build fixes the three remaining wide-digit Power callers and the shore Search gold notice. It carries forward the earlier ruins Power correction. [Registered follow-up](editorial_power_and_gold_digits_registered_20261121.md)
