"""Role assignments use the game's eligibility branches and preserve owner text."""

import json
import struct
from pathlib import Path

import pytest

from dk4tool.rom.nds import NdsImage
from scripts.prepare_item_role_state import STATES
from scripts.verify_item_role_eligibility import verify_case


@pytest.fixture(scope='module')
def resources():
    image = NdsImage.open('out/all_routes_combined_v158_candidate.nds')
    return (Path('work/analysis/generated_item_advice_research_arm9.bin').read_bytes(),
            json.loads(Path('work/analysis/generated_item_advice_plan.json').read_text(encoding='utf-8')),
            image.read_file('/COMMON/MESFILE.DK4'), image.read_file('/GRP/KANJI.FNT'))


@pytest.mark.parametrize('state', STATES)
def test_real_assignment_and_fleet_exceptions_keep_complete_owner(resources, state):
    source, plan, common, font = resources
    result = verify_case(source, plan, common, font, 74, state, 16)
    assert result['item_actual_owner_classifications']
    assert result['item_actual_role_eligibility'][0]['eligible'] == (state not in ('mismatching', 'unassigned'))


@pytest.mark.parametrize(('slot', 'mode'), ((3, 4), (4, 16)))
def test_accessory_slot_boundaries_execute_real_search(resources, slot, mode):
    source, plan, common, font = resources
    result = verify_case(source, plan, common, font, 126, 'mismatching', mode, slot)
    assert not result['item_actual_role_eligibility'][0]['eligible']


def test_bypassing_native_eligibility_is_rejected(resources):
    source, plan, common, font = resources
    damaged = bytearray(source)
    # A permissive return would silently hide incorrect role assignments.
    struct.pack_into('<2I', damaged, 0x49A18, 0xE3A00001, 0xE12FFF1E)
    with pytest.raises(ValueError, match='eligibility|native branch'):
        verify_case(bytes(damaged), plan, common, font, 74, 'mismatching', 16)
