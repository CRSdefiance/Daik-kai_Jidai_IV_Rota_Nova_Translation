"""Isolated original-method financial prerequisite for Tavern refusal testing."""

from pathlib import Path
import struct

from unicorn.arm_const import UC_ARM_REG_R0

from dk4tool.patch.grand_race_menu_release import sha
from scripts.probe_button_prompt_native import BASE, call, machine
from scripts.verify_village_wrap_v608 import read


def assign(arm, raw, request):
    assert request in ({'mode': 'no_money'}, {'mode': 'water_only'}) and len(raw) == 4194304
    assert sha(arm) in ('6508bf3e43144efc4a9b449564e1acd2a0eecacb7184ed23408ce1856cea1ddf', read('translations/port_services_editorial_release_v1.json')['target_arm9_sha256'])
    u = machine(arm); u.mem_write(BASE, raw)
    def get(fn, args=()):
        call(u, fn, args); return u.reg_read(UC_ARM_REG_R0)
    if request['mode'] == 'water_only':
        fleet = get(0xCB1A8) + 4 + get(0x2E58C) * 0x84
        capacity = get(0x34E60, (fleet,)); assert capacity > 0
        get(0x34EB0, (fleet, 0x02450000))
        before_totals = list(struct.unpack('<2I', u.mem_read(0x02450000, 8)))
        root = get(0xCB148)
        ids = [u.mem_read(fleet + 0x10 + 8 * i, 1)[0] for i in range(5)]
        assert all(i != 155 for i in ids)
        ships = [root + 4 + i * 0x8C for i in ids]
        get(0x60518, (0, 0, capacity))
        get(0x34EB0, (fleet, 0x02450000))
        after_totals = list(struct.unpack('<2I', u.mem_read(0x02450000, 8)))
        assert after_totals == [0, capacity]
        after = bytes(u.mem_read(BASE, 4194304))
        changes = [{'address': BASE + i, 'before': x, 'after': y} for i, (x, y) in enumerate(zip(raw, after, strict=True)) if x != y]
        assert changes and all(any(p + 0x3E <= r['address'] < p + 0x42 for p in ships) for r in changes)
        return after, {'mode': 'water_only', 'native_fleet': fleet, 'member_ships': ships,
            'capacity': capacity, 'original_totals_getter': 0x02034EB0, 'before_water_food': before_totals,
            'after_water_food': after_totals, 'original_native_supply_assignment': 0x02060518,
            'changes': changes, 'all_other4MiB_RAM_exact': True, 'before_RAM_sha256': sha(raw), 'after_RAM_sha256': sha(after),
            'ARM9_sha256': sha(arm), 'fixture_source_sha256': sha(Path(__file__).read_bytes()),
            'no_earned_resupply_or_financial_state_claim': True}
    root = get(0xCB160); company = get(0x397D8, (root,)); assert company < 40
    force = root + 4 + company * 0x4C
    before = get(0x3CCC8, (force,)); assert before in (8371, 25975)
    get(0x3CC80, (force, -before)); assert get(0x3CCC8, (force,)) == 0
    after = bytes(u.mem_read(BASE, 4194304))
    changes = [{'address': BASE + i, 'before': x, 'after': y} for i, (x, y) in enumerate(zip(raw, after, strict=True)) if x != y]
    assert changes and all(force + 12 <= r['address'] < force + 16 for r in changes)
    return after, {'mode': 'no_money', 'company_index': company, 'native_company': force, 'before_funds': before,
        'after_funds': 0, 'original_CForce_money_method': 0x0203CC80, 'changes': changes,
        'all_other4MiB_RAM_exact': True, 'before_RAM_sha256': sha(raw), 'after_RAM_sha256': sha(after),
        'ARM9_sha256': sha(arm), 'fixture_source_sha256': sha(Path(__file__).read_bytes()),
        'no_earned_financial_state_claim': True}
