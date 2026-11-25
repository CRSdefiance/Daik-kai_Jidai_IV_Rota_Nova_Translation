"""Exact current ARM9 binding of the preserved room/XP/eleven-day display fixture."""
from types import FunctionType
from dk4tool.patch.grand_race_menu_release import sha
from scripts import native_strategist_fixture_v624 as room
from scripts import native_scheme_expert_fixture_v776_v2 as expert

ARM = 'ab7475ec929bd271c54f8b88cdb2fb10fd71ceb5f54b988507d073f0e3466bde'

def assign(arm, raw, request):
    if sha(arm) != ARM or len(raw) != 0x400000 or request is not True:
        raise ValueError('Exact V2171 ARM9, full RAM and explicit fixture request required')
    after, proof = FunctionType(room.assign.__code__, {**room.__dict__, 'ARM': ARM})(arm, raw, True)
    changed = {i for i, (a, b) in enumerate(zip(raw, after, strict=True)) if a != b}
    assert changed == {r['address']-0x02000000 for r in proof['changes']} and len(changed) == 3
    proof['all_other4MiB_bytes_exact'] = True
    proof['stats_XP_money_location_calendar_unchanged'] = True
    return after, proof

def assign_expert(arm, raw, request):
    after, proof = FunctionType(expert.assign_expert.__code__, {**expert.__dict__, 'assign': assign})(arm, raw, request)
    proof['current_binding_producer_sha256'] = sha(__import__('pathlib').Path(__file__).read_bytes())
    proof['room_producer_sha256'] = sha(__import__('pathlib').Path(room.__file__).read_bytes())
    proof['experience_calendar_producer_sha256'] = sha(__import__('pathlib').Path(expert.__file__).read_bytes())
    return after, proof
