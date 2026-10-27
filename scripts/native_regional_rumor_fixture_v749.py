"""Explicit zero-share regional-rumor selector and RNG fixture; original town retained."""

import struct
from pathlib import Path

from unicorn.arm_const import UC_ARM_REG_R0

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.probe_button_prompt_native import BASE, call, machine
from scripts.verify_village_wrap_v608 import read


def assign(arm, raw, request):
    config = read('translations/regional_rumors_release_v1.json')
    assert sha(arm) in (config['source_arm9_sha256'], config['target_arm9_sha256'])
    assert len(raw) == 4194304 and request in ({'region': 0}, {'region': 20})
    region = request['region']
    clean = NdsImage.open('work/clean.nds').read_file('/__arm9__.bin')
    for lo, hi in ((0x5F9B8, 0x5FB54), (0xB4A88, 0xB4AD4), (0xB51B4, 0xB51CC),
                   (0xB5690, 0xB56A8), (0x519D4, 0x51A28), (0xD9824, 0xD9868)):
        assert arm[lo:hi] == clean[lo:hi]
    cpu = machine(arm)
    cpu.mem_write(BASE, raw)

    def get(fn, args=()):
        call(cpu, fn, args)
        return cpu.reg_read(UC_ARM_REG_R0)

    town = get(0xB6618)
    assert get(0xB65E4) == 22
    company = get(0x397D8, (get(0xCB160),))
    assert company == 2 and bytes(cpu.mem_read(town + 0x10, 6)) == bytes((9, 99, 21, 0, 21, 0))
    assert get(0xB4A88, (town,)) == 0 and get(0xB51B4, (town,)) == 8
    record = get(0xB5690, (town,))
    seed_address = struct.unpack_from('<I', arm, 0xD9830)[0]
    init_flag = struct.unpack_from('<I', arm, 0x51A20)[0]
    assert bytes(cpu.mem_read(init_flag, 4)) == bytes(4)
    values = [(record + 0x15, bytes((region,)), 'temporary native region table byte'),
              (seed_address, struct.pack('<I', 2), 'SDK RNG seed for controlled original rumor selection')]
    after = bytearray(raw)
    changes = []
    for address, data, field in values:
        for n, value in enumerate(data):
            at = address + n - BASE
            if after[at] != value:
                changes.append({'address': BASE + at, 'before': after[at], 'after': value, 'field': field})
                after[at] = value
    assert 1 <= len(changes) <= 5
    assert sum(a != b for a, b in zip(raw, after, strict=True)) == len(changes)
    cpu.mem_write(BASE, bytes(after))
    assert get(0xB4A88, (town,)) == 0 and get(0xB51B4, (town,)) == region
    assert get(0x5FA60, (0, town)) == 709 + region
    draws = [get(0x519D4, (4,)) for _ in range(3)]
    assert draws == [0, 1, 3]
    return bytes(after), {
        'synthetic_regional_rumor_fixture': True, 'changes': changes,
        'before_RAM_sha256': sha(raw), 'after_RAM_sha256': sha(after), 'ARM9_sha256': sha(arm),
        'original_town_index_retained': 22, 'original_company_index': company,
        'original_zero_share_retained': True, 'temporary_region_selector': region,
        'expected_native_rumor_message': 709 + region, 'source_RNG_seed': 2,
        'first_three_original_random4_results': draws,
        'original_native_getters_and_selector_all_verified': True,
        'region_table_byte_is_explicit_RAM_data_fixture_not_ROM_or_travel': True,
        'all_other_code_and_RAM_bytes_unchanged': True,
        'ordinary_regional_travel_and_event_probability_not_claimed': True,
        'fixture_source_sha256': sha(Path(__file__).read_bytes())}
