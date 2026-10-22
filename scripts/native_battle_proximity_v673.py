"""V666-only delegation of the retained coordinate-only encounter fixture."""

from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.village_port_consistency import transform
from dk4tool.rom.nds import NdsImage
from scripts.native_full_fleet_proximity_v653 import ARM
from scripts.native_full_fleet_proximity_v653 import apply_fixture as original_fixture

CURRENT_ARM = 'b92df335942af8db216b149f54c0eac75626ddde2cf573b6f41c20f3e217bda8'


def apply_fixture(arm, raw, action):
    if sha(arm) != CURRENT_ARM or action != 'approach':
        raise ValueError('This fixture permits only V666 coordinate approach, never recovery or outcome changes')
    reference = NdsImage.open('out/all_routes_combined_v653_candidate.nds').read_file('/__arm9__.bin')
    assert sha(reference) == ARM and arm == transform(reference)[0]
    # The delegated body runs the actual captured V666 RAM, including its loaded
    # code. The reference argument preserves the earlier source guards exactly.
    after, receipt = original_fixture(reference, raw, action)
    assert len(receipt['owned_bytes']) == 8
    assert all(c['address'] in receipt['owned_bytes'] for c in receipt['changes'])
    assert receipt['no_enemy_stats_war_outcome_reward_inventory_or_resource_flags_changed']
    receipt.update(current_ARM_sha256=CURRENT_ARM, delegation_reference_ARM_sha256=ARM,
        current_ARM_exact_V666_seven_village_data_repairs=True,
        current_fixture_wrapper_sha256=sha(Path(__file__).read_bytes()))
    return after, receipt
