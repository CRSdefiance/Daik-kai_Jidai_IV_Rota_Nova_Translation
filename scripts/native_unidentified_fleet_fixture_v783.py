"""Authorized isolated NPC-fleet identity/report-state fixture for rumor samples."""

import struct

from unicorn import UC_HOOK_CODE
from unicorn.arm_const import UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_R2, UC_ARM_REG_SP, UC_ARM_REG_LR

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.native_call_abi_v764 import call
from scripts.native_machine_scoped_v764 import machine
from scripts.probe_button_prompt_native import BASE, STACK, STOP

ARMS = {'d2d2670bfbbb8ce1c3433b0c1a6220f385ef8beba5678bea9e9d4bb612b57abb',
        'daa9686528955df3e88258c5c3fc1b63adb551b08669f2a33584e3bd9d674c02'}


def set_condition(arm, raw, request):
    if sha(arm) not in ARMS or len(raw) != 0x400000 or request != {'mode': 'unidentified-fleet-rumors'}:
        raise ValueError('Pinned V780/V782/V783 and the declared unidentified-fleet fixture required')
    clean = NdsImage.open('work/clean.nds').read_file('/__arm9__.bin')
    for a, b in ((0x57A5C, 0x57C74), (0x57C90, 0x57EAC), (0x35320, 0x35400), (0x34674, 0x34688)):
        assert arm[a:b] == clean[a:b]
    u = machine(arm)
    u.mem_write(BASE, raw)

    def get(fn, args=()):
        call(u, fn, args)
        return u.reg_read(UC_ARM_REG_R0)

    def ptr(at): return struct.unpack('<I', u.mem_read(at, 4))[0]

    fleet_store, towns = get(0xCB1A8), get(0xCB178)
    here = get(0xB6618)
    assert get(0xB65E4) == 22
    region = get(0xB2B48, (here,))
    company = get(0xCB160)+4+get(0x397D8)*76
    faction = get(0x3D030, (company,))

    def candidates():
        destination, anchored = [], []
        for i in range(57):
            f = fleet_store+4+i*132
            b = bytes(u.mem_read(f, 132))
            if not get(ptr(ptr(f)+0x10)-BASE, (f,)) or b[0x50] & 2 or get(0x35320, (f,)) == faction:
                continue
            town, dest = get(0x34674, (f,)), b[0x3F]
            if dest < 114 and b[0x3E] != 6 and get(0xB2B48, (towns+4+dest*108,)) == region:
                destination.append(i)
            if town < 114 and get(0xB2B48, (towns+4+town*108,)) == region:
                anchored.append(i)
        return destination, anchored

    before = candidates()
    assert before == ([0, 6, 7, 8, 9, 10, 22, 24, 25, 27, 28, 35], [0, 7, 10, 27, 28, 35])
    owned, reports = set(), []
    for i in sorted(set(before[0]+before[1])-{0, 7}):
        f = fleet_store+4+i*132
        prior = bytes(u.mem_read(f+0x50, 2))
        get(0x353DC, (f, 1))
        after = bytes(u.mem_read(f+0x50, 2))
        assert int.from_bytes(after, 'little') == int.from_bytes(prior, 'little') | 2
        owned.update((f+0x50, f+0x51))
        reports.append(i)
    identities = []
    for i in (0, 7):
        f = fleet_store+4+i*132
        old = bytes(u.mem_read(f+8, 1))[0]
        u.mem_write(f+8, bytes([208]))
        assert get(0x35320, (f,)) == 21 and get(ptr(ptr(f)+0x10)-BASE, (f,))
        owned.add(f+8)
        identities.append({'fleet_index': i, 'prior_captain': old, 'fixture_captain_sentinel': 208, 'native_unknown_faction': 21})
    anchored = fleet_store+4+7*132
    prior_order = bytes(u.mem_read(anchored+0x3E, 1))[0]
    assert prior_order == 1
    u.mem_write(anchored+0x3E, bytes([6]))
    owned.add(anchored+0x3E)
    assert candidates() == ([0], [0, 7])
    result = bytearray(raw)
    for at in owned:
        result[at-BASE] = bytes(u.mem_read(at, 1))[0]
    changes = [{'address': BASE+i, 'before': a, 'after': b}
               for i, (a, b) in enumerate(zip(raw, result, strict=True)) if a != b]
    assert len(changes) == 13 and all(c['address'] in owned for c in changes)
    # Full original destination selection marks0 reported; the remaining original
    # anchorage selector then selects7. Only stop at the real speech wrapper.
    u.mem_write(BASE, bytes(result))
    scratch, events = 0x02479000, []
    u.mem_write(scratch, bytes(20))

    def speech(c, pc, size, unused):
        at = c.reg_read(UC_ARM_REG_R2)
        events.append({'ID': c.reg_read(UC_ARM_REG_R1), 'speaker': c.reg_read(UC_ARM_REG_R0),
                       'town_argument_hex': bytes(c.mem_read(at, 128)).split(b'\0')[0].hex()})
        c.emu_stop()

    h = u.hook_add(UC_HOOK_CODE, speech, begin=BASE+0x53FE4, end=BASE+0x53FE4)
    try:
        for fn, expected in ((0x57C90, 1032), (0x57A5C, 1034)):
            u.reg_write(UC_ARM_REG_SP, STACK)
            u.reg_write(UC_ARM_REG_LR, STOP)
            u.reg_write(UC_ARM_REG_R0, scratch)
            u.reg_write(UC_ARM_REG_R1, 22)
            u.emu_start(BASE+fn, STOP, count=200000)
            assert events[-1]['ID'] == expected
    finally:
        u.hook_del(h)
    return bytes(result), {
        'synthetic_unidentified_fleet_fixture': True, 'mode': request['mode'], 'ARM9_sha256': sha(arm),
        'town_ID': 22, 'current_region': region, 'own_faction': faction,
        'original_destination_candidates': before[0], 'original_anchored_candidates': before[1],
        'other_NPC_fleets_marked_already_reported': reports, 'original_report_setter': BASE+0x353DC,
        'identity_fixtures': identities, 'anchored_fleet7_order_before': prior_order, 'anchored_fleet7_order_after': 6,
        'full_original_selector_CPU_preflight': events,
        'changes': changes, 'all_other4MiB_bytes_exact': True,
        'before_RAM_sha256': sha(raw), 'after_RAM_sha256': sha(result),
        'no_ROM_dialogue_code_menu_player_fleet_cash_location_or_source_save_change': True,
        'no_earned_unidentified_fleet_or_report_history_claim': True,
        'no_rng_result_injection': True}
