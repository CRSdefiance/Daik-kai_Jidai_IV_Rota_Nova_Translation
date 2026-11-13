"""Isolated role13 prerequisites; no HP,XP,money,price or duration overrides."""

import struct
from pathlib import Path

from unicorn.arm_const import UC_ARM_REG_R0

from dk4tool.patch.grand_race_menu_release import sha
from scripts.probe_button_prompt_native import BASE, call, machine
from scripts.verify_village_wrap_v608 import read


def assign(arm, raw, request):
    assert request == {'mode': 'qualified_helper'}
    config = read('translations/refit_dialogue_editorial_release_v1.json')
    assert sha(arm) in (config['source_arm9_sha256'], config['target_arm9_sha256'])
    assert len(raw) == 0x400000
    cpu = machine(arm)
    cpu.mem_write(BASE, raw)

    def get(fn, args=()):
        call(cpu, fn, args)
        return cpu.reg_read(UC_ARM_REG_R0)

    root = get(0xCB1A8)
    controller = root + struct.unpack_from('<I', arm, 0xBAB34)[0]
    model = get(0x82E04, (controller,))
    assert bytes(cpu.mem_read(model + 8, 24)).split(b'\0')[0] == b'Vestaros'
    actor = get(0xCB184) + 4 + 16 * 32
    table = struct.unpack('<I', cpu.mem_read(actor, 4))[0]
    pointer = get(struct.unpack('<I', cpu.mem_read(table + 0x20, 4))[0] - BASE, (actor,))
    assert bytes(cpu.mem_read(pointer, 24)).split(b'\0')[0] == b'Gerhard'
    assert get(0x8261C, (controller, 13)) == 208
    assignments = list(raw[controller + 6 - BASE:controller + 6 - BASE + 31])
    assert assignments.count(16) == 1 and assignments[18] == 208
    old_slot = assignments.index(16)
    room = get(0x7B60, (13,))
    fields = ((model + 0x1E + 18, room), (controller + 6 + old_slot, 208), (controller + 6 + 18, 16))
    for at, value in fields:
        cpu.mem_write(at, bytes([value]))
    assert get(0x8261C, (controller, 13)) == 16
    ability = get(0x7E728, (actor,))
    assert ability >= 25
    voice = get(0x7E988, (actor,))
    assert 0 <= voice < 8
    selected = get(0x53F4C, (actor, 0x02118680))
    assert selected == (1256 if voice in (0, 1) else 1255 + voice)
    after = bytes(cpu.mem_read(BASE, 0x400000))
    changes = [{'address': BASE + i, 'before': a, 'after': b} for i, (a, b) in enumerate(zip(raw, after, strict=True)) if a != b]
    assert {r['address'] for r in changes} == {at for at, value in fields}
    assert len(changes) == 3
    return after, {'synthetic_refit_helper_prerequisites': True, 'changes': changes,
                   'source_native_ship': model, 'existing_actor_ID': 16, 'existing_actor_name': 'Gerhard',
                   'source_room_type_getter': BASE + 0x7B60, 'room_type': room,
                   'source_role13_helper_after': 16, 'previous_assignment_slot': old_slot, 'native_existing_ability': ability,
                   'native_voice_index': voice, 'expected_original_offer_ID': selected,
                   'source_discount_percent': ability // 5,
                   'all_other4MiB_RAM_including_code_HP_XP_money_price_duration_quest_flags_exact': True,
                   'before_RAM_sha256': sha(raw), 'after_RAM_sha256': sha(after), 'ARM9_sha256': sha(arm),
                   'fixture_source_sha256': sha(Path(__file__).read_bytes()),
                   'no_earned_room_role_assignment_or_qualification_claim': True}
