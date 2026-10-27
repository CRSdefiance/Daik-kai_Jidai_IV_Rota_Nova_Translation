"""Isolated original Deck cooldown counters; no calendar, crew, text or RNG edits."""

import struct

from unicorn.arm_const import UC_ARM_REG_R0

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.native_call_abi_v764 import call
from scripts.native_machine_scoped_v764 import machine
from scripts.verify_village_wrap_v608 import read

BASE = 0x02000000


def assign(arm, raw, parameters):
    allowed = [read('translations/refit_dialogue_editorial_release_v1.json')['target_arm9_sha256'],
               read('translations/personal_chatter_editorial_release_v1.json')['target_arm9_sha256']]
    if sha(arm) not in allowed or len(raw) != 0x400000:
        raise ValueError('Exact V834/V838 ARM9 and4MiB captured RAM required')
    if parameters != {'elapsed_ticks': 961}:
        raise ValueError('Only the declared961-tick elapsed-counter fixture is allowed')
    clean = NdsImage.open('work/clean.nds').read_file('/__arm9__.bin')
    spans = ((0x13C94, 0x13D80), (0x34674, 0x34688), (0x82B98, 0x82BA0))
    assert all(arm[a:b] == clean[a:b] for a, b in spans)
    cpu = machine(arm)
    cpu.mem_write(BASE, raw)
    def get(at, *args):
        call(cpu, at, args)
        return cpu.reg_read(UC_ARM_REG_R0)
    model = get(0xCB1A8)
    fleet = model + 4 + get(0x2E58C) * 0x84
    if get(0x34674, fleet) != 115:
        raise ValueError('Depart normally before the Deck elapsed-counter fixture')
    calendar = get(0xCB1B4)
    now = struct.unpack_from('<I', raw, calendar + 8 - BASE)[0]
    if now <= 961:
        raise ValueError('Use an established later save;counter wrap fixtures are not allowed')
    controller = model + struct.unpack_from('<I', arm, 0x13D74)[0]
    locations = [struct.unpack_from('<I', arm, 0x13D70)[0], controller + 0x28]
    assert len(set(locations)) == 2 and all(BASE <= p < BASE + len(raw) - 4 for p in locations)
    before = [struct.unpack_from('<I', raw, p - BASE)[0] for p in locations]
    values = [old if (now - old) & 0xFFFFFFFF >= 961 and (index != 0 or old != 0)
              else now - 961 for index, old in enumerate(before)]
    after = bytearray(raw)
    for p, value in zip(locations, values, strict=True):
        struct.pack_into('<I', after, p - BASE, value)
    allowed_bytes = {p - BASE + n for p in locations for n in range(4)}
    changes = [{'address': BASE + n, 'before': raw[n], 'after': after[n]}
               for n in sorted(allowed_bytes) if raw[n] != after[n]]
    assert all(raw[n] == after[n] for n in range(len(raw)) if n not in allowed_bytes)
    return bytes(after), {'synthetic_elapsed_counter_fixture': True, 'calendar_tick_preserved': now,
        'original_counter_addresses': locations, 'before_counter_values': before,
        'fixture_counter_values': values, 'minimum_elapsed_ticks': 961, 'changes': changes,
        'before_RAM_sha256': sha(raw), 'after_RAM_sha256': sha(bytes(after)),
        'all_calendar_crew_roles_food_health_money_RNG_text_code_other_RAM_exact': True,
        'actual_elapsed_days_or_earned_progress_not_verified': True,
        'native_original_scheduler_actor_selection_and_rendering_unmodified': True}
