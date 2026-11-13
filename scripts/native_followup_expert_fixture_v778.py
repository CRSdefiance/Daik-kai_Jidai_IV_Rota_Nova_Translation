"""The previously bounded room/XP/date fixture on exact V776/V778 ARM9 images."""

from types import FunctionType

from dk4tool.patch.grand_race_menu_release import sha
from scripts import native_strategist_fixture_v624 as room
from scripts import native_scheme_expert_fixture_v776_v2 as expert
from scripts.verify_village_wrap_v608 import read


def assign(arm, raw, request):
    expected = read('work/analysis/scheme_followup_integration_v778/prospective_common_repack.json')['target_ARM9_sha256']
    if sha(arm) not in ('f54d9d10c96edbebffbbab4d184550b2df1157827fe41ac9ffb1a60565c7f523', expected) or len(raw) != 0x400000 or request is not True:
        raise ValueError('Exact V776/V778 and explicit mapped fixture required')
    after, proof = FunctionType(room.assign.__code__, {**room.__dict__, 'ARM': sha(arm)})(arm, raw, True)
    changed = {i for i, (a, b) in enumerate(zip(raw, after, strict=True)) if a != b}
    assert changed == {r['address']-0x02000000 for r in proof['changes']} and len(changed) == 3
    proof['all_other4MiB_bytes_exact'] = True
    proof['stats_XP_money_location_calendar_unchanged'] = True
    return after, proof


def assign_expert(arm, raw, request):
    return FunctionType(expert.assign_expert.__code__, {**expert.__dict__, 'assign': assign})(arm, raw, request)
