"""Explicit owned cargo, one-percent share and town-demand display fixtures."""

import struct
from pathlib import Path

from unicorn.arm_const import UC_ARM_REG_R0

from dk4tool.patch.grand_race_menu_release import sha
from scripts.probe_button_prompt_native import BASE, call, machine
from scripts.verify_village_wrap_v608 import read


def assign(arm, raw, request):
    config = read('translations/market_stock_editorial_release_v1.json')
    assert sha(arm) in (config['source_arm9_sha256'], config['target_arm9_sha256'])
    assert request in ({'mode': 'one'}, {'mode': 'two'}) and len(raw) == 0x400000
    u = machine(arm)
    u.mem_write(BASE, raw)
    def get(f, args=()):
        call(u, f, args)
        return u.reg_read(UC_ARM_REG_R0)
    town = get(0xB6618)
    assert get(0xB65E4) == 22 and get(0xB4A88, (town,)) == 0
    root = get(0xCB160)
    company = get(0x397D8, (root,))
    assert company == 2 and bytes(u.mem_read(town + 0x12, 2)) == bytes((21, 0))
    fleet = get(0xCB1A8) + 4 + 0x84
    model = get(0x36C94, (fleet + 12,))
    assert bytes(u.mem_read(model + 8, 24)).split(b'\0')[0] == b'Vestaros'
    assert get(0x36180, (fleet, 0x02440000)) == 2
    assert bytes(u.mem_read(0x02440000, 24)) == bytes.fromhex('5a03000000000000000000005a0300000000000000000000')
    ids = [103, 103 if request['mode'] == 'one' else 108]
    fields = [(town + 0x12, bytes((company, 1)), 'previously unused company/share pair')]
    names = []
    for i, product in enumerate(ids):
        ob = get(0xCB124) + 4 + product * 16
        vt = struct.unpack('<I', u.mem_read(ob, 4))[0]
        name = get(struct.unpack('<I', u.mem_read(vt + 8, 4))[0] - BASE, (ob,))
        text = bytes(u.mem_read(name, 64)).split(b'\0')[0].decode('ascii')
        assert text == ('North Sea Ambergris' if product == 103 else 'Fire and Ice Rubies')
        names.append(text)
        fields.append((model + 0x50 + i * 12, bytes((product,)), 'existing owned cargo product ID; grade/prices unchanged'))
    for i, product in enumerate(sorted(set(ids))):
        slot = get(0xB30EC, (town, i))
        assert bytes(u.mem_read(slot, 2)) == bytes((125, 0))
        fields.append((slot, bytes((product, 10)), 'original empty town-demand pair'))
    after, changes = bytearray(raw), []
    for address, payload, field in fields:
        for n, value in enumerate(payload):
            at = address + n - BASE
            if after[at] != value:
                changes.append({'address': BASE + at, 'before': after[at], 'after': value, 'field': field})
                after[at] = value
    assert sum(a != b for a, b in zip(raw, after, strict=True)) == len(changes)
    u.mem_write(BASE, bytes(after))
    assert get(0xB4A88, (town,)) == get(0xB4AA8, (town, company)) == 1
    assert get(0x36180, (fleet, 0x02440000)) == 2
    cargos = bytes(u.mem_read(0x02440000, 24))
    assert [cargos[0], cargos[12]] == ids
    assert cargos[1:12] == cargos[13:24] == bytes.fromhex('0300000000000000000000')
    return bytes(after), {'synthetic_Market_stock_display_fixture': True, 'mode': request['mode'],
        'cargo_product_names': names, 'changes': changes, 'town': 22, 'company': company,
        'original_ship': model, 'existing_cargo_hold_count_unchanged_at2': True,
        'all_other_RAM_code_cargo_grades_prices_money_health_location_and_quest_bytes_unchanged': True,
        'earned_inventory_share_demand_or_rewards_not_claimed': True,
        'before_RAM_sha256': sha(raw), 'after_RAM_sha256': sha(after), 'ARM9_sha256': sha(arm),
        'fixture_source_sha256': sha(Path(__file__).read_bytes())}
