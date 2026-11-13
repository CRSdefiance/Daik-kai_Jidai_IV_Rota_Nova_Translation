"""Qualified Strategist, then one original condition byte for a warning sample."""

import struct
from types import FunctionType
from unicorn.arm_const import UC_ARM_REG_R0, UC_ARM_REG_R4, UC_ARM_REG_R5, UC_ARM_REG_R6, UC_ARM_REG_SP, UC_ARM_REG_LR
from scripts.probe_button_prompt_native import STACK, STOP
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts import native_strategist_fixture_v624 as original
from scripts.native_recruit_shortfall_fixture_v782 import ARMS, BASE
from scripts.native_call_abi_v764 import call
from scripts.native_machine_scoped_v764 import machine


def set_condition(arm, raw, request):
    if sha(arm) not in ARMS or len(raw) != 0x400000 or request not in ({'mode': 'enable-schemes'}, {'mode': 'low-success-warning'}):
        raise ValueError('Exact V780/V782 and declared two-stage warning fixture required')
    clean = NdsImage.open('work/clean.nds').read_file('/__arm9__.bin')
    for lo, hi in ((0x7DCC8, 0x7DE20), (0x7E100, 0x7E108), (0x7E668, 0x7E750),
                   (0xCC9C8, 0xCCA30), (0x567CC, 0x56990), (0x56998, 0x56AE8)):
        assert arm[lo:hi] == clean[lo:hi]
    if request['mode'] == 'enable-schemes':
        after, assignment = FunctionType(original.assign.__code__, {**original.__dict__, 'ARM': sha(arm)})(arm, raw, True)
    else:
        after, assignment = raw, None
    u = machine(arm)
    u.mem_write(BASE, after)
    def get(fn, args=()):
        call(u, fn, args)
        return u.reg_read(UC_ARM_REG_R0)
    actor = get(0xCB184)+4+16*32
    result = bytearray(after)
    fields, owned = [], {r['address']-BASE for r in assignment['changes']} if assignment else set()
    if assignment:
        assert actor == assignment['actor']
        calendar = get(0xCB1B4)
        ticks = struct.unpack('<I', u.mem_read(calendar+8, 4))[0]
        assert ticks+768 < 2**32
        for at, value in ((actor+16, 300000), (calendar+8, ticks+768)):
            before = struct.unpack_from('<I', result, at-BASE)[0]
            result[at-BASE:at-BASE+4] = struct.pack('<I', value)
            owned.update(range(at-BASE, at-BASE+4))
            fields.append({'address': at, 'before': before, 'after': value, 'width': 4})
    else:
        assert get(0x825E4, (get(0xCB1A8)+0x2090, 2)) == 16
        assert get(0x7E670, (actor,)) == 300000 and get(0x7E100, (actor,)) == 0
        assert get(0x7DD38, (actor, 7, 6)) >= 200
        result[actor+6-BASE] = 3
        owned.add(actor+6-BASE)
        fields.append({'address': actor+6, 'before': 0, 'after': 3, 'width': 1})
    u.mem_write(BASE, bytes(result))
    skill, speech = get(0x7DD38, (actor, 7, 6)), get(0x7DCC8, (actor, 8))
    faction = get(0xCB160)+4+9*76
    leader = get(0x3CD2C, (faction,))
    leader_speech = get(0x7DCC8, (leader, 8))
    assert leader_speech == 152
    score = speech-leader_speech//2
    assert (skill >= 200 and speech == 209) if assignment else (get(0x7E100, (actor,)) == 3 and speech == 104 and score == 28)
    gate = None
    if assignment:
        assert get(0xB65E4) == 22
        company = get(0xCB160)+4+get(0x397D8)*76
        assert get(0x3CCC8, (company,)) >= 1000
        u.reg_write(UC_ARM_REG_SP, STACK)
        u.reg_write(UC_ARM_REG_LR, STOP)
        u.reg_write(UC_ARM_REG_R5, 16)
        u.mem_write(STACK+0x4C, bytes(4))
        u.emu_start(BASE+0x5685C, BASE+0x56938, count=100000)
        threshold = u.reg_read(UC_ARM_REG_R4)
        assert u.reg_read(UC_ARM_REG_R6) == speech and speech > threshold
        gate = {'original_native_fragment': [BASE+0x5685C, BASE+0x56938], 'Speech': speech, 'threshold': threshold,
                'sixteen_calendar_days_advanced': True, 'original_predicate_passes': True}
    changed = [i for i, (a, b) in enumerate(zip(raw, result, strict=True)) if a != b]
    assert set(changed) <= owned and len(changed) <= (11 if assignment else 1)
    return bytes(result), {
        'synthetic_warning_prerequisite_fixture': True, 'mode': request['mode'], 'ARM9_sha256': sha(arm),
        'source_assignment': assignment, 'actor': actor, 'declared_fields': fields,
        'original_submenu_skill': skill, 'original_strategist_Speech': speech,
        'unchanged_Pasha_leader_Speech': leader_speech, 'native_score_against_Pasha': score,
        'initial_original_menu_predicate': gate,
        'changes': [{'address': BASE+i, 'before': raw[i], 'after': result[i]} for i in changed],
        'all_other4MiB_bytes_exact': True, 'before_RAM_sha256': sha(raw), 'after_RAM_sha256': sha(result),
        'inventory_cash_location_code_menu_flags_opponents_and_original_saves_unchanged': True,
        'earned_qualifications_experience_time_condition_or_success_not_claimed': True}
