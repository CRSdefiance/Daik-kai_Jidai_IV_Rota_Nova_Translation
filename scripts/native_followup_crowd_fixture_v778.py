"""Fill ten private-meeting task slots with valid future jobs for refusal testing."""

import struct

from unicorn.arm_const import UC_ARM_REG_R0

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.native_call_abi_v764 import call
from scripts.native_machine_scoped_v764 import machine
from scripts.native_followup_expert_fixture_v778 import assign, assign_expert as qualify
from scripts.probe_button_prompt_native import BASE, STACK


def assign_expert(arm, raw, request):
    qualified, proof = qualify(arm, raw, request)
    clean = NdsImage.open('work/clean.nds').read_file('/__arm9__.bin')
    for a, b in ((0x91464, 0x914D8), (0x93BAC, 0x93C04), (0x572D0, 0x57308)):
        assert arm[a:b] == clean[a:b]
    u = machine(arm)
    u.mem_write(BASE, qualified)
    def get(fn, args=()):
        call(u, fn, args)
        return u.reg_read(UC_ARM_REG_R0)
    pool = get(0xCB130)
    company = get(0x397D8, (get(0xCB160),))
    assert get(0x91480, (pool, 4, 14)) == pool+4+16*4
    result, jobs = bytearray(qualified), []
    for n in range(4, 14):
        obj = pool+4+16*n
        before = bytes(u.mem_read(obj, 16))
        assert before[4] == 11 and get(0x91464, (obj,)) == 0
        u.mem_write(STACK, struct.pack('<4I', 4, 365, 0, 21))
        assert get(0x93BAC, (obj, 9, company, 16)) == 1
        after = bytes(u.mem_read(obj, 16))
        assert after[:4] == before[:4] and after[10:12] == before[10:12]
        assert after[4:10] == bytes((9, company, 16, 4, 0, 21))
        assert get(0x91464, (obj,)) == 1
        for i in range(16):
            if before[i] != after[i]:
                assert i in (4, 5, 6, 7, 8, 9, 12, 13, 14, 15)
                result[obj-BASE+i] = after[i]
                proof['changes'].append({'address': obj+i, 'before': before[i], 'after': after[i]})
        jobs.append({'slot': n, 'object': obj, 'before_hex': before.hex(), 'after_hex': after.hex()})
    assert get(0x91480, (pool, 4, 14)) == 0
    changed = {BASE+i for i, (a, b) in enumerate(zip(raw, result, strict=True)) if a != b}
    assert changed == {r['address'] for r in proof['changes']}
    proof.update({'synthetic_private_meeting_task_capacity_fixture': True, 'future_jobs': jobs,
                  'original_free_slot_getter_after_fixture': 0, 'task_type': 9, 'days_until_due': 365,
                  'only_three_assignment_bytes_one_XP_word_one_calendar_word_owned': False,
                  'only_declared_assignment_XP_calendar_and_ten_task_record_fields_owned': True,
                  'all_other4MiB_bytes_exact': True, 'after_RAM_sha256': sha(result),
                  'normal_busy_Tavern_earned_tasks_or_successful_schemes_not_claimed': True})
    return bytes(result), proof
