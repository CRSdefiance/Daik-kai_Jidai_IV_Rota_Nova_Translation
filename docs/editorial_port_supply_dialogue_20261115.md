# Port resupply and departure dialogue

The November 19 [Copenhagen replays](editorial_port_resupply_options_20261119.md) verified both prompts that had offline coverage in this checkpoint.

The [registered review](../releases/all_routes_editorial_20261115_port_supply_dialogue_candidate/verification/registered_review.json) covers eight Port Worker lines. The worker now explains that extra food will be thrown out, offers a smaller refill when the player is short of gold, and asks about changing the mix of water and food. The low-water question and inn suggestion keep their prior wording with complete questions on the second line. The rest of the exchange retains the water-disposal warning, the empty-cargo reply and the price quote.

Two Copenhagen cold boots used the original refill and disposal controls. A fixture set the copied fleet’s supplies to zero water and 700 food before the player chose resupply. Both runs finished with 350 water, 350 food and 25,975 gold. The ordinary Riga departure showed the complete inn suggestion. The four revised panels match the native font masks. The small refill offer and supply mix prompt were checked offline. [Gameplay comparison](../releases/all_routes_editorial_20261115_port_supply_dialogue_candidate/verification/gameplay_comparison.png)

The [registered ROM and clean-input patch](../releases/all_routes_editorial_20261115_port_supply_dialogue_candidate/README.md) maintain the 114 accepted layers and ASCII right-bound correction. Six startup frames matched, 24 protected name getters and 42 targeted tests passed, and the patch reproduced every ROM byte. Two repository tests for older optional mapper fixtures were outside the focused run. Physical hardware and the remaining shared-text scope are open.
