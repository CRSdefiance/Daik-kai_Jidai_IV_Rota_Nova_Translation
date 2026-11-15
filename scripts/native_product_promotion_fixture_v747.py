"""Three declared event/product bytes for the original Square demonstration."""

import struct
from pathlib import Path

from unicorn.arm_const import UC_ARM_REG_R0

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.probe_button_prompt_native import BASE, call, machine
from scripts.verify_village_wrap_v608 import read


def assign(arm, raw, request):
    config = read('translations/product_pitches_editorial_release_v1.json')
    assert sha(arm) in (config['source_arm9_sha256'], config['target_arm9_sha256'])
    assert len(raw) == 4194304 and request == {'product': 14}
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
    after = bytearray(raw)
    for row in changes:
        assert after[row['address'] - BASE] == row['before']
        after[row['address'] - BASE] = row['after']
    assert sum(a != b for a, b in zip(raw, after, strict=True)) == 3
    return bytes(after), {
        'synthetic_product_promotion_event_fixture': True, 'changes': changes,
        'before_RAM_sha256': sha(raw), 'after_RAM_sha256': sha(after), 'ARM9_sha256': sha(arm),
        'original_town_index': city, 'product_index': 14, 'product_name': 'Olive Oil', 'product_category': category,
        'original_stock_parameter_unchanged_at0': True,
        'expected_original_intro675_then_category676': True,
        'only_three_event_tracking_and_town_stock_bytes_changed': True,
        'all_other_RAM_code_inventory_money_health_quests_and_location_bytes_unchanged': True,
        'ordinary_event_acquisition_or_progress_not_claimed': True,
        'fixture_source_sha256': sha(Path(__file__).read_bytes())}
