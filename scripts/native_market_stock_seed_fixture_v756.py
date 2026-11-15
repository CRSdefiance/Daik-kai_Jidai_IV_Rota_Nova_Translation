"""Late SDK seed control before the unchanged randomized return cost."""

import struct
from pathlib import Path

from unicorn.arm_const import UC_ARM_REG_R0

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.native_market_stock_fixture_v756 import assign as stock
from scripts.probe_button_prompt_native import BASE, call, machine
from scripts.verify_village_wrap_v608 import read


def assign(arm, raw, request):
    if request == {'mode': 'one'}:
        return stock(arm, raw, request)
    config = read('translations/market_stock_editorial_release_v1.json')
    assert sha(arm) in (config['source_arm9_sha256'], config['target_arm9_sha256'])
    assert request == {'mode': 'rng', 'seed': 3} and len(raw) == 0x400000
    clean = NdsImage.open('work/clean.nds').read_file('/__arm9__.bin')
    assert all(arm[a:b] == clean[a:b] for a, b in ((0x2FDA0, 0x2FDC4), (0x34540, 0x34564), (0x519D4, 0x51A28), (0xD9824, 0xD9870)))
    u = machine(arm)
    u.mem_write(BASE, raw)
    call(u, 0xCB1A8, ())
    fleet = u.reg_read(UC_ARM_REG_R0) + 0x88
    assert bytes(u.mem_read(fleet + 0x3D, 1)) == bytes((24,))
    seed = struct.unpack_from('<I', arm, 0xD9830)[0]
    initialized = struct.unpack_from('<I', arm, 0x51A20)[0]
    assert struct.unpack('<I', u.mem_read(initialized, 4))[0] == 0
    after = bytearray(raw)
    payload = struct.pack('<I', 3)
    changes = []
    for n, value in enumerate(payload):
        at = seed + n - BASE
        if after[at] != value:
            changes.append({'address': BASE + at, 'before': after[at], 'after': value, 'field': 'original SDK RNG seed'})
            after[at] = value
    assert sum(a != b for a, b in zip(raw, after, strict=True)) == len(changes)
    assert 1 <= len(changes) <= 4
    u.mem_write(BASE, bytes(after))
    call(u, 0x519D4, (5,))
    value = u.reg_read(UC_ARM_REG_R0)
    assert 0 <= value < 5
    return bytes(after), {'synthetic_late_Market_seed_control': True, 'changes': changes,
        'before_RAM_sha256': sha(raw), 'after_RAM_sha256': sha(after), 'ARM9_sha256': sha(arm),
        'source_seed_pointer': seed, 'SDK_seed3_first_native_rand5': value,
        'before_fleet_field3D': 24, 'original_cost_formula': 'minus (2 + native rand(5)), clamped to0..100',
        'all_other_RAM_code_money_cargo_share_quests_health_and_model_bytes_unchanged': True,
        'seeded_RNG_is_a_diagnostic_fixture_not_earned_progress': True,
        'fixture_source_sha256': sha(Path(__file__).read_bytes())}
