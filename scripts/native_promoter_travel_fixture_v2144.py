"""Explicit original-event inputs for promoter travel request and arrival testing."""

import struct
from pathlib import Path

from unicorn.arm_const import UC_ARM_REG_R0

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.probe_button_prompt_native import BASE, call, machine
from scripts.verify_village_wrap_v608 import read


def assign(arm, raw, request):
    config = read('translations/town_events_editorial_release_v1.json')
    assert sha(arm)=='29da98540c4366e83cca21102d4440bd8ccda3dac27f0a67cd10fa8c0d319ca5'
    assert len(raw) == 4194304 and request in ({'product': 14, 'level': 25}, {'arrival': True})
    clean = NdsImage.open('work/clean.nds').read_file('/__arm9__.bin')
    for lo, hi in ((0x5E458, 0x5E680), (0xB30EC, 0xB3134), (0xB65E4, 0xB6640), (0xCB124, 0xCB190)):
        assert arm[lo:hi] == clean[lo:hi]
    cpu = machine(arm)
    cpu.mem_write(BASE, raw)

    def get(fn, args=()):
        call(cpu, fn, args)
        return cpu.reg_read(UC_ARM_REG_R0)

    state, player, town = get(0xCB178), get(0xCB184), get(0xB6618)
    city = get(0xB65E4)
    assert city == 22
    assert struct.unpack('<I', cpu.mem_read(player + 0x1A4C, 4))[0] & 4 == 0
    slot = get(0xB30EC, (town, 1))
    assert bytes(cpu.mem_read(slot, 2)) == bytes((125, 0))
    product = get(0xCB124) + 4 + 14 * 16
    vt = struct.unpack('<I', cpu.mem_read(product, 4))[0]
    name = get(struct.unpack('<I', cpu.mem_read(vt + 8, 4))[0] - BASE, (product,))
    assert bytes(cpu.mem_read(name, 10)) == b'Olive Oil\0'
    category = bytes(cpu.mem_read(product + 12, 1))[0]
    assert category < 4
    changes = [
        {'address': state + 0x3020, 'before': raw[state + 0x3020 - BASE], 'after': city, 'field': 'promotion tracked city'},
        {'address': state + 0x3021, 'before': raw[state + 0x3021 - BASE], 'after': 14, 'field': 'promotion tracked product'},
        {'address': slot, 'before': 125, 'after': 14, 'field': 'temporary first trade slot product'}]
    assert [r['before'] for r in changes] == [74, 33, 125]
    if request.get('arrival'):
        flag = struct.unpack('<I', cpu.mem_read(player + 0x1A4C, 4))[0]
        assert flag & 4 == 0
        changes = [{'address': player + 0x1A4C, 'before': raw[player + 0x1A4C - BASE],
            'after': raw[player + 0x1A4C - BASE] | 4, 'field': 'explicit promoter travel flag for original different-town arrival'}]
    else:
        changes.append({'address': slot + 1, 'before': 0, 'after': 25,
            'field': 'native stock/promotion parameter reaches original travel-request threshold'})
    after = bytearray(raw)
    for row in changes:
        assert after[row['address'] - BASE] == row['before']
        after[row['address'] - BASE] = row['after']
    assert sum(a != b for a, b in zip(raw, after, strict=True)) == (1 if request.get('arrival') else 4)
    return bytes(after), {
        'synthetic_promoter_travel_fixture': True, 'changes': changes,
        'before_RAM_sha256': sha(raw), 'after_RAM_sha256': sha(after), 'ARM9_sha256': sha(arm),
        'original_town_index': city, 'product_index': 14, 'product_name': 'Olive Oil', 'product_category': category,
        'mode': 'arrival' if request.get('arrival') else 'request',
        'expected_original_messages': [738] if request.get('arrival') else [675, 676, 739],
        'only_declared_event_and_stock_data_bytes_changed': True,
        'all_other_RAM_code_inventory_money_health_quests_and_location_bytes_unchanged': True,
        'ordinary_event_acquisition_or_progress_not_claimed': True,
        'fixture_source_sha256': sha(Path(__file__).read_bytes())}
