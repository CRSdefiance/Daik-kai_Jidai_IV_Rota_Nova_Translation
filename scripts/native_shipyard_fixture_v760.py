"""Isolated native durability setter and qualified repair-helper prerequisites."""

import struct
from pathlib import Path

from unicorn.arm_const import UC_ARM_REG_R0

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.shipyard_editorial import BANKS, SOURCE
from scripts.probe_button_prompt_native import BASE, call, machine
from scripts.verify_village_wrap_v608 import read


def assign(arm, raw, request):
    assert sha(arm) in (SOURCE, read('translations/shipyard_editorial_release_v1.json')['target_arm9_sha256'])
    assert request in ({'mode': 'repair_helper'}, {'mode': 'copy_name', 'name': 'FALCON'},
                       {'mode': 'copy_name', 'name': 'ICARUS'},
                       {'mode': 'copy_name', 'name': 'FALCON', 'preparation': 0},
                       {'mode': 'copy_name', 'name': 'ICARUS', 'preparation': 1},
                       {'mode': 'repair_pair'}, {'mode': 'repair_pair_no_funds'}) and len(raw) == 0x400000
    u = machine(arm)
    u.mem_write(BASE, raw)
    def get(function, args=()):
        call(u, function, args)
        return u.reg_read(UC_ARM_REG_R0)
    root = get(0xCB1A8)
    controller = root + struct.unpack_from('<I', arm, 0xBAB34)[0]
    if request['mode'] in ('repair_pair', 'repair_pair_no_funds'):
        fleet_index = get(0x2E58C)
        assert fleet_index < 40
        fleet = root + 4 + fleet_index * 0x84
        ids = [raw[fleet + 0x10 + i * 8 - BASE] for i in range(5)]
        assert len([i for i in ids if i != 155]) == 5 and get(0x8261C, (controller, 13)) == 208
        ship_root = get(0xCB148)
        ships, allowed = [], []
        for index in ids[:2]:
            ship = ship_root + 4 + index * 0x8C
            table = struct.unpack('<I', u.mem_read(ship, 4))[0]
            getter = struct.unpack('<I', u.mem_read(table + 0x24, 4))[0]
            setter = struct.unpack('<I', u.mem_read(table + 0x34, 4))[0]
            maximum = get(0xAB8F0, (ship,))
            assert get(getter - BASE, (ship,)) == maximum and maximum >= 10
            get(setter - BASE, (ship, maximum - 3))
            assert get(getter - BASE, (ship,)) == maximum - 3
            allowed.append((ship, ship + 0x8C))
            ships.append({'ship_ID': index, 'ship': ship, 'maximum_HP': maximum, 'fixture_HP': maximum - 3,
                          'original_HP_getter': getter, 'original_HP_setter': setter})
        assert get(0x621B4, (0, fleet, 0x02450000)) == 2
        assert list(struct.unpack('<2I', u.mem_read(0x02450000, 8))) == ids[:2]
        company_root = get(0xCB160)
        force = company_root + 4 + get(0x397D8, (company_root,)) * 0x4C
        funds = get(0x3CCC8, (force,))
        assert funds == 25975
        if request['mode'] == 'repair_pair_no_funds':
            get(0x3CC80, (force, -funds))
            assert get(0x3CCC8, (force,)) == 0
            allowed.append((force + 12, force + 16))
        after = bytes(u.mem_read(BASE, 0x400000))
        changes = [{'address': BASE + i, 'before': a, 'after': b} for i, (a, b) in enumerate(zip(raw, after, strict=True)) if a != b]
        assert changes and all(any(lo <= r['address'] < hi for lo, hi in allowed) for r in changes)
        return after, {'synthetic_shipyard_two_ship_fixture': True, 'mode': request['mode'], 'changes': changes,
            'fleet': fleet, 'ships': ships, 'original_eligible_repair_count_after': 2,
            'original_role13_helper': 208, 'before_funds': funds,
            'funds_after': get(0x3CCC8, (force,)), 'original_CForce_money_method': 0x0203CC80,
            'all_other4MiB_RAM_exact': True, 'before_RAM_sha256': sha(raw), 'after_RAM_sha256': sha(after),
            'ARM9_sha256': sha(arm), 'fixture_source_sha256': sha(Path(__file__).read_bytes()),
            'no_earned_damage_or_financial_state_claim': True}
    model = get(0x82E04, (controller,))
    assert bytes(u.mem_read(model + 8, 24)).split(b'\0')[0] == b'Vestaros'
    vt = struct.unpack('<I', u.mem_read(model, 4))[0]
    if request['mode'] == 'copy_name':
        name_getter = struct.unpack('<I', u.mem_read(vt + 4, 4))[0]
        pointer = get(name_getter - BASE, (model,))
        assert pointer == model + 8
        name = request['name'].encode('ascii')
        assert len(name) == 6 < len(b'Vestaros')
        u.mem_write(pointer, name + b'\0')
        assert bytes(u.mem_read(get(name_getter - BASE, (model,)), 24)).split(b'\0')[0] == name
        design_fields = []
        if 'preparation' in request:
            model_type = get(struct.unpack('<I', u.mem_read(vt + 8, 4))[0] - BASE, (model,))
            assert model_type == 11
            default = get(0xCB154) + 4 + model_type * 64
            default_vt = struct.unpack('<I', u.mem_read(default, 4))[0]
            default_sail_getter = struct.unpack('<I', u.mem_read(default_vt + 0x10, 4))[0]
            model_sail_getter = struct.unpack('<I', u.mem_read(vt + 0x10, 4))[0]
            assert model_sail_getter == 0x02062D68
            for slot in range(3):
                old = get(model_sail_getter - BASE, (model, slot))
                value = get(default_sail_getter - BASE, (default, slot))
                if old != value:
                    at = model + 0x1B + slot
                    assert bytes(u.mem_read(at, 1))[0] == old
                    u.mem_write(at, bytes((value,)))
                    design_fields.append({'address': at, 'before': old, 'after': value, 'source': 'original catalogue sail getter', 'slot': slot})
            default_room_getter = struct.unpack('<I', u.mem_read(default_vt + 0x18, 4))[0]
            for slot in range(31):
                value = get(default_room_getter - BASE, (default, slot))
                old = get(0x132C0, (model, slot))
                assert old == bytes(u.mem_read(model + 0x1E + slot, 1))[0]
                if value != old:
                    at = model + 0x1E + slot
                    u.mem_write(at, bytes((value,)))
                    design_fields.append({'address': at, 'before': old, 'after': value, 'source': 'original catalogue room getter', 'slot': slot})
            if request['preparation'] == 0:
                end_getter = struct.unpack('<I', u.mem_read(default_vt + 0x1C, 4))[0]
                value = get(end_getter - BASE, (default,))
                old = bytes(u.mem_read(model + 0x4A, 1))[0]
                u.mem_write(model + 0x4A, bytes((value,)))
                design_fields.append({'address': model + 0x4A, 'before': old, 'after': value, 'source': 'original catalogue last-property getter'})
            # Run the unchanged original preparation algorithm over both real
            # native objects. No computed result or branch is overridden.
            assert get(0x62B8C, (0, model)) == request['preparation']
        company_root = get(0xCB160)
        company = get(0x397D8, (company_root,))
        assert 0 <= company < 40
        force = company_root + 4 + company * 0x4C
        old_funds = get(0x3CCC8, (force,))
        assert old_funds == 8371
        get(0x3CC80, (force, 100000 - old_funds))
        assert get(0x3CCC8, (force,)) == 100000
        after = bytes(u.mem_read(BASE, 0x400000))
        changes = [{'address': BASE + i, 'before': a, 'after': b} for i, (a, b) in enumerate(zip(raw, after, strict=True)) if a != b]
        assert changes and all(pointer <= r['address'] < pointer + len(name) + 1
                               or force + 12 <= r['address'] < force + 16
                               or any(r['address'] == d['address'] for d in design_fields) for r in changes)
        return after, {'synthetic_shipyard_name_fixture': True, 'mode': 'copy_name', 'changes': changes,
            'supplied_name': request['name'], 'native_ship': model, 'native_name_getter': name_getter,
            'original_CForce_money_method': 0x0203CC80, 'company_funds_before': old_funds,
            'supplied_company_funds': 100000, 'original_company_funds_word': force + 12,
            'catalogue_derived_design_fields': design_fields,
            'original_native_preparation_result': get(0x62B8C, (0, model)),
            'name_storage_bound': 'Six ASCII letters and NUL fit inside the existing eight-letter name allocation.',
            'all_other4MiB_RAM_exact': True, 'before_RAM_sha256': sha(raw), 'after_RAM_sha256': sha(after),
            'ARM9_sha256': sha(arm), 'fixture_source_sha256': sha(Path(__file__).read_bytes()),
            'no_earned_design_modification_or_purchase_claim': True}
    getter = struct.unpack('<I', u.mem_read(vt + 0x24, 4))[0]
    setter = struct.unpack('<I', u.mem_read(vt + 0x34, 4))[0]
    maximum, current = get(0xAB8F0, (model,)), get(getter - BASE, (model,))
    assert maximum == current == 60
    actor = get(0xCB184) + 4 + 16 * 32
    actor_vt = struct.unpack('<I', u.mem_read(actor, 4))[0]
    name_pointer = get(struct.unpack('<I', u.mem_read(actor_vt + 0x20, 4))[0] - BASE, (actor,))
    assert bytes(u.mem_read(name_pointer, 24)).split(b'\0')[0] == b'Gerhard'
    assert get(0x8261C, (controller, 13)) == 208
    assert raw[controller + 6 + 21 - BASE] == 16 and raw[controller + 6 + 18 - BASE] == 208
    room_type = get(0x7B60, (13,))
    assert room_type < 256
    # Gerhard is already level39 in this donor; qualification needs no XP edit.
    fields = ((model + 0x1E + 18, bytes((room_type,))),
              (controller + 6 + 21, bytes((208,))), (controller + 6 + 18, bytes((16,))))
    for at, payload in fields:
        u.mem_write(at, payload)
    assert get(0x8261C, (controller, 13)) == 16
    level = get(0x7E728, (actor,))
    assert level >= 25
    get(setter - BASE, (model, maximum - 3))
    assert get(getter - BASE, (model,)) == maximum - 3
    voice = get(0x7E988, (actor,))
    after = bytes(u.mem_read(BASE, 0x400000))
    changes = [{'address': BASE + i, 'before': a, 'after': b} for i, (a, b) in enumerate(zip(raw, after, strict=True)) if a != b]
    allowed = [(model, model + 0x8C), (controller + 6 + 18, controller + 6 + 19),
               (controller + 6 + 21, controller + 6 + 22)]
    assert changes and all(any(lo <= r['address'] < hi for lo, hi in allowed) for r in changes)
    assert all(raw[lo - BASE:hi - BASE] == after[lo - BASE:hi - BASE] for lo, hi in BANKS)
    discount = level // 5
    return after, {'synthetic_shipyard_repair_fixture': True, 'mode': request['mode'], 'changes': changes,
        'native_ship': model, 'native_HP_getter': getter, 'native_HP_setter': setter,
        'current_durability_before': current, 'supplied_durability_after': maximum - 3, 'maximum_durability': maximum,
        'original_role13_helper_after': 16, 'existing_actor_name': 'Gerhard', 'fixture_room_type': room_type,
        'native_existing_level': level, 'actor_experience_bytes_unchanged': True, 'native_voice_index': voice,
        'expected_volunteer_message': 791 if voice in (0, 1) else 790 + voice,
        'native_discount_percent': discount, 'all_other4MiB_RAM_exact': True,
        'const_code_banks_untouched': True, 'before_RAM_sha256': sha(raw), 'after_RAM_sha256': sha(after),
        'ARM9_sha256': sha(arm), 'fixture_source_sha256': sha(Path(__file__).read_bytes()),
        'no_earned_damage_refit_assignment_experience_or_repair_claim': True}
