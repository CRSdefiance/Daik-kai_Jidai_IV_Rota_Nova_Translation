"""Replay the original Lisbon Square navigation on both cumulative ROMs."""

from argparse import ArgumentParser
from io import StringIO
from json import dumps
from pathlib import Path
from types import FunctionType
import sys

from scripts import headless_desmume_v193 as harness
from scripts import native_condition_fixture_v520 as fixture
from scripts import observe_lisbon_voyage_and_osaka_20261115 as lisbon
from scripts import replay_kurushima_encounter_20261115 as startup_checks
from scripts import stage_square_shop_captions_20261115 as stage
from scripts.verify_personal_gameplay_v841 import get_machine


base = stage.base
PAUSE = 3720
FRAMES = (3200, PAUSE, 3950, 4350, 4750, 5150, 5550, 5950, 6350, 6750, 7150)
END = 7151
FOCUSED = {'town': 11, 'products': [76, 95]}
TREND_SUFFIX = '_trend_v2'


def trend(arm, raw, request):
    assert request == FOCUSED
    clean = base.NdsImage.open(stage.CLEAN).read_file(stage.ARM)
    assert arm[0x5F1EC:0x5F630] == clean[0x5F1EC:0x5F630]
    cpu, get = get_machine(arm, raw)
    assert get(0xB65E4) == 11
    town = get(0xB6618)
    growth = get(0xB3FD4, town, 0)
    assert growth == 6469
    slots = [get(0xB30EC, town, i) for i in (0, 1)]
    assert [bytes(cpu.mem_read(pointer, 2)) for pointer in slots] == [b'\x7D\0'] * 2
    assert [get(0x5F1EC, row, growth) for row in range(4)] == [13, 31, 50, 41]
    after = bytearray(raw)
    changes = []
    for pointer, product in zip(slots, request['products'], strict=True):
        at = pointer - stage.BASE
        before = bytes(after[at:at + 2])
        value = bytes((product, 8))
        after[at:at + 2] = value
        changes.extend(dict(address=pointer + index, before=a, after=b)
                       for index, (a, b) in enumerate(zip(before, value, strict=True)) if a != b)
    assert sum(a != b for a, b in zip(raw, after, strict=True)) == 4
    cpu, get = get_machine(arm, bytes(after))
    product_base = get(0xCB124) + 4
    products = [get(0x5F1EC, row, growth) for row in range(4)]
    categories = [cpu.mem_read(product_base + index * 16 + 12, 1)[0] for index in products]
    assert products == [13, 76, 95, 95] and categories == [1, 13, 17, 17]
    return bytes(after), dict(changes=changes, original_product_order=products,
                              original_category_order=categories, earned_trend=False)


def replay(which, focused):
    rom, receipt = (stage.parent.ROM, stage.parent.RELEASE) if which == 'parent' else (stage.ROM, stage.STORED)
    assert base.digest(rom) == base.load(receipt)['candidate_sha256']
    events, _, _, _, donor = lisbon.schedule('lisbon')
    assert base.digest(donor['source']) == donor['source_sha256']
    root = stage.ROOT / (which + (TREND_SUFFIX if focused else '_ordinary'))
    root.mkdir(parents=True)
    inputs = root / 'inputs.json'
    base.save(inputs, [row for row in events if row['start'] < END])
    previous_stdin, previous_argv, previous_fixture = sys.stdin, sys.argv, fixture.set_condition
    advance = {'until': END}
    if focused:
        advance['condition_fixture'] = FOCUSED
    sys.stdin = StringIO(''.join(dumps(item) + '\n' for item in (advance, {'stop': True})))
    sys.argv = [harness.__file__, '--rom', str(rom), '--out', str(root / 'capture'),
                '--frames', str(END), '--inputs-json', str(inputs), '--touchscreen',
                '--battery-save', str(Path(donor['source'])), '--capture-every', '999999',
                '--capture-at', *map(str, FRAMES), '--pause-at', str(PAUSE), '--dump-pause-ram']
    if focused:
        sys.argv.append('--allow-condition-fixtures')
        fixture.set_condition = trend
    try:
        harness.main()
    finally:
        sys.stdin, sys.argv, fixture.set_condition = previous_stdin, previous_argv, previous_fixture
    assert base.digest(donor['source']) == donor['source_sha256']


def startup():
    FunctionType(startup_checks.startup.__code__, vars(startup_checks) | dict(stage=stage))()


if __name__ == '__main__':
    parser = ArgumentParser(description=__doc__)
    parser.add_argument('mode', choices=('parent', 'candidate', 'startup'))
    parser.add_argument('--trend', action='store_true')
    args = parser.parse_args()
    if args.mode == 'startup':
        startup()
    else:
        replay(args.mode, args.trend)
