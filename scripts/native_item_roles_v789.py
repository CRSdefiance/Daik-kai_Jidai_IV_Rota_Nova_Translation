"""Authorized three-byte First Mate/Purser prerequisite in a disposable save run."""

import struct

from unicorn.arm_const import UC_ARM_REG_R0

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.native_call_abi_v764 import call
from scripts.native_machine_scoped_v764 import machine

BASE = 0x02000000
ARMS = {'daa9686528955df3e88258c5c3fc1b63adb551b08669f2a33584e3bd9d674c02',
        '4c2e19d9834bfa79a5e90897afe7c3332f4c850077f2db4c5eb57949f57217bd'}


def set_condition(arm, raw, request):
    if sha(arm) not in ARMS or len(raw) != 0x400000 or request != {'mode': 'item-and-letter-roles'}:
        raise ValueError('Exact V783/V788 RAM and declared role prerequisites required')
    clean = NdsImage.open('work/clean.nds').read_file('/__arm9__.bin')
    spans = ((0x7B60, 0x7C34), (0x132C0, 0x132CC), (0x825E4, 0x8261C),
             (0x829C8, 0x82A44), (0x82BC4, 0x82BD0), (0x82E04, 0x82E2C), (0x5B26C, 0x5B324))
    for lo, hi in spans: assert arm[lo:hi] == clean[lo:hi]
    cpu = machine(arm)
    cpu.mem_write(BASE, raw)
    def get(fn, args=()):
        call(cpu, fn, args)
        return cpu.reg_read(UC_ARM_REG_R0)
    controller = get(0xCB1A8)+0x2090
    model, actors = get(0x82E04, (controller,)), get(0xCB184)
    assert get(0xB65E4) == 57 and get(0x7F244) == 3
    assert get(0x825E4, (controller, 1)) == get(0x825E4, (controller, 3)) == 208
    assert get(0x7B60, (1,)) == 6 and get(0x7B60, (3,)) == 20
    assert get(0x132C0, (model, 15)) == 6 and get(0x132C0, (model, 2)) == 24
    assert get(0x82BC4, (controller, 15)) == get(0x82BC4, (controller, 2)) == 208
    prior_rooms = [get(0x82BC4, (controller, i)) for i in range(31)]
    assert 10 not in prior_rooms and 11 not in prior_rooms
    actor_rows = []
    for n, expected in ((10, b'Xien'), (11, b'Jam')):
        obj = actors+4+n*32
        vt = struct.unpack('<I', cpu.mem_read(obj, 4))[0]
        fn = struct.unpack('<I', cpu.mem_read(vt+0x20, 4))[0]
        p = get(fn-BASE, (obj,))
        assert bytes(cpu.mem_read(p, 32)).split(b'\0')[0] == expected
        actor_rows.append({'actor_ID': n, 'object': obj, 'given_name': expected.decode()})
    fields = ((controller+6+15, 208, 10), (model+0x1E+2, 24, 20), (controller+6+2, 208, 11))
    after = bytearray(raw)
    changes = []
    for at, before, value in fields:
        assert after[at-BASE] == before
        after[at-BASE] = value
        changes.append({'address': at, 'before': before, 'after': value})
    cpu.mem_write(BASE, bytes(after))
    assert get(0x825E4, (controller, 1)) == 10 and get(0x825E4, (controller, 3)) == 11
    changed = {i for i, (a, b) in enumerate(zip(raw, after, strict=True)) if a != b}
    assert changed == {r['address']-BASE for r in changes} and len(changed) == 3
    return bytes(after), {'synthetic_item_and_letter_role_prerequisite_fixture': True,
        'ARM9_sha256': sha(arm), 'controller': controller, 'model': model, 'mode': request['mode'],
        'actors': actor_rows, 'First_Mate_room': 15, 'Purser_room': 2, 'original_getters_after': {'1': 10, '3': 11},
        'changes': changes, 'all_other4MiB_bytes_exact': True,
        'original_source_getter_and_menu_spans': [{'range': [lo, hi], 'sha256': sha(clean[lo:hi])} for lo, hi in spans],
        'money_health_stats_inventory_location_calendar_menu_flags_and_outcomes_unchanged': True,
        'earned_assignment_refit_or_diplomatic_progress_not_claimed': True,
        'before_RAM_sha256': sha(raw), 'after_RAM_sha256': sha(after)}
