"""Reuse the exact source-bound map transfer under V820's stat-only repack."""

from dk4tool.patch.grand_race_menu_release import sha
from scripts.native_ceremony_map_fixture_v814 import set_condition as map_transfer
from scripts.native_ceremony_istanbul_fixture_v827 import set_condition as calendar_access
from scripts.native_ceremony_yield_control_v823 import source_arm


def set_condition(arm, raw, request):
    if request.get('mode') == 'ceremony-Istanbul':
        return calendar_access(arm,raw,request)
    assert request == {'mode':'ceremony-Cappadocia-map'}
    mapped = source_arm(arm)
    after, receipt = map_transfer(mapped,raw,request)
    receipt.update(ARM9_sha256=sha(arm),source_equivalent_native_transfer_ARM9_sha256=sha(mapped),
        no_source_code_captain_dialogue_random_state_or_quest_fixture_available=True)
    return after,receipt
