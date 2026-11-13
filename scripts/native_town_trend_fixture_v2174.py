"""Bound original town trend fields and SDK seed; no event tracking or travel changes."""

import struct
from pathlib import Path

from unicorn.arm_const import UC_ARM_REG_R0

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.probe_button_prompt_native import BASE, call, machine
from scripts.verify_village_wrap_v608 import read


def assign(arm, raw, request):
    config = read('translations/town_responses_editorial_release_v1.json')
    assert sha(arm)=='ab7475ec929bd271c54f8b88cdb2fb10fd71ceb5f54b988507d073f0e3466bde'
    assert len(raw) == 4194304 and set(request) == {'level', 'seed'}
    assert request['level'] in (50, 150) and type(request['seed']) is int and 0 <= request['seed'] <= 15
    clean = NdsImage.open('work/clean.nds').read_file('/__arm9__.bin')
    for lo, hi in ((0x5F904, 0x5FCA0), (0xB30EC, 0xB3134), (0xB31E0, 0xB320C),
                   (0x519D4, 0x51A28), (0xD9824, 0xD9868), (0xC5B7C, 0xC5BB8)):
        assert arm[lo:hi] == clean[lo:hi]
    cpu = machine(arm)
    cpu.mem_write(BASE, raw)

    def get(fn, args=()):
        call(cpu, fn, args)
        return cpu.reg_read(UC_ARM_REG_R0)

    town = get(0xB6618)
    assert get(0xB65E4) == 22
    slots = [get(0xB30EC, (town, n)) for n in (0, 1)]
    assert [bytes(cpu.mem_read(p, 2)) for p in slots] == [bytes((125, 0)), bytes((125, 0))]
    product = get(0xCB124) + 4 + 14 * 16
    assert get(0xC5B7C, (product,)) == 14
    category = cpu.mem_read(product + 12, 1)[0]
    assert category == 1
    seed_pointer = struct.unpack_from('<I', arm, 0xD9830)[0]
    values = [(slots[1], bytes((14, request['level'])), 'original second town trend pair'),
        (seed_pointer, struct.pack('<I', request['seed']), 'original SDK RNG seed')]
    after = bytearray(raw)
    changes = []
    for address, data, field in values:
        for n, value in enumerate(data):
            at = address + n - BASE
            if after[at] != value:
                changes.append({'address': BASE + at, 'before': after[at], 'after': value, 'field': field})
                after[at] = value
    assert 2 <= len(changes) <= 6 and sum(a != b for a, b in zip(raw, after, strict=True)) == len(changes)
    cpu.mem_write(BASE, bytes(after))
    assert get(0xB31E0, (town, 14)) == request['level']
    assert bytes(cpu.mem_read(slots[0], 2)) == bytes((125, 0))
    return bytes(after), {'synthetic_town_trend_fixture': True, 'changes': changes,
        'before_RAM_sha256': sha(raw), 'after_RAM_sha256': sha(after), 'ARM9_sha256': sha(arm),
        'original_town_index': 22, 'product_index': 14, 'product_name': 'Olive Oil', 'original_product_category': category,
        'source_trend_value': request['level'], 'source_RNG_seed': request['seed'],
        'original_selected_topic_and_UI_RNG_sequence_must_be_verified_from_actual_display': True,
        'all_other_RAM_event_tracking_inventory_money_quests_and_location_bytes_unchanged': True,
        'ordinary_trend_creation_or_progress_not_claimed': True, 'fixture_source_sha256': sha(Path(__file__).read_bytes())}
