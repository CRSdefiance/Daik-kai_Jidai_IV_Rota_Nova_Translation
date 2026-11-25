"""Observe the Market Info trend area with and without an active reported item."""

from argparse import ArgumentParser
from hashlib import sha256
from io import StringIO
from json import dumps
from pathlib import Path
import sys

from scripts import headless_desmume_v193 as harness
from scripts import native_condition_fixture_v520 as fixture
from scripts import register_developed_port_menu_20261115 as current
from scripts.stage_price_info_wraps_20261115 import ROOT as PRICE
from scripts.verify_personal_gameplay_v841 import get_machine


base = current.base
ROOT = Path('work/market_info_trends_20261115_v1')
REFERENCE = PRICE / 'revised/capture/capture_report.json'
BASE = 0x02000000
REQUEST = dict(town=11, product=14, counter=22)
PREDICATES = ((0xB30EC, 0xB30F8), (0xB3178, 0xB3194), (0xB31E0, 0xB320C),
              (0xB65E4, 0xB6650), (0xBED18, 0xBED40))


def replay(mode, rom, rom_sha, folder, exit_report):
    assert base.digest(rom) == rom_sha
    history = base.load(REFERENCE)
    donor = history['battery_save_preloaded']
    assert base.digest(donor['source']) == donor['source_sha256']
    folder.mkdir(parents=True)
    events = [row for row in history['scripted_input_schedule'] if row['start'] <= 12301]
    if exit_report:
        events.append(dict(start=12701, duration=8, buttons=['B']))
    inputs = folder / 'inputs.json'
    base.save(inputs, events)
    arm_path = current.stage.ARM
    clean = base.NdsImage.open(current.stage.CLEAN).read_file(arm_path)
    arm = base.NdsImage.open(rom).read_file(arm_path)

    def set_condition(actual_arm, raw, request):
        assert actual_arm == arm and len(raw) == 0x400000 and request == REQUEST
        assert all(arm[lo:hi] == clean[lo:hi] for lo, hi in PREDICATES)
        cpu, get = get_machine(arm, raw)
        assert get(0xB65E4) == request['town']
        town = get(0xB6618)
        slot = get(0xB30EC, town, 0)
        offset = slot - BASE
        assert raw[offset:offset + 2] == bytes((125, 0))
        get(0xB3178, town, 0, request['product'], request['counter'])
        entry = bytes(cpu.mem_read(slot, 2))
        assert entry == bytes((request['product'], request['counter']))
        assert get(0xB31E0, town, request['product']) == request['counter']
        after = raw[:offset] + entry + raw[offset + 2:]
        return after, dict(town=request['town'], municipal_product_slot=slot, goods='Olive Oil',
            product=request['product'], counter=request['counter'], original_setter=BASE + 0xB3178,
            before_RAM_sha256=sha256(raw).hexdigest(), after_RAM_sha256=sha256(after).hexdigest(),
            changes=[dict(address=slot + i, before=raw[offset + i], after=entry[i]) for i in range(2)])

    command = {'until': 12600}
    if mode == 'trend':
        command['condition_fixture'] = REQUEST
    terminal = 13000 if exit_report else 12600
    args = [harness.__file__, '--rom', str(rom), '--out', str(folder / 'capture'),
        '--frames', str(terminal + 1), '--inputs-json', str(inputs), '--battery-save', donor['source'],
        '--touchscreen', '--press-start', '-1', '--capture-every', '999999', '--capture-at', '12280', '12600', str(terminal),
        '--pause-at', '12280', '--dump-pause-ram', '--allow-condition-fixtures']
    old_fixture, old_input, old_args = fixture.set_condition, sys.stdin, sys.argv
    actions = [command]
    if exit_report:
        actions.append(dict(until=terminal))
    actions.append(dict(stop=True))
    commands = StringIO(''.join(dumps(action) + '\n' for action in actions))
    try:
        fixture.set_condition, sys.stdin, sys.argv = set_condition, commands, args
        harness.main()
    finally:
        fixture.set_condition, sys.stdin, sys.argv = old_fixture, old_input, old_args
    path = folder / 'capture/capture_report.json'
    report = base.load(path)
    assert report['cold_boot'] and not report['savestate_loaded'] and not report['callback_errors']
    assert report['ROM_sha256'] == rom_sha and report['frames'] == terminal
    assert report['scripted_input_schedule'] == events
    assert len(report.get('synthetic_condition_fixtures', [])) == int(mode == 'trend')
    assert base.digest(donor['source']) == donor['source_sha256']


if __name__ == '__main__':
    parser = ArgumentParser(description=__doc__)
    parser.add_argument('mode', choices=('control', 'trend'))
    parser.add_argument('--rom', type=Path, default=current.ROM)
    parser.add_argument('--sha256', default=base.load(current.RELEASE)['candidate_sha256'])
    parser.add_argument('--out', type=Path)
    parser.add_argument('--exit-report', action='store_true')
    args = parser.parse_args()
    replay(args.mode, args.rom, args.sha256, args.out or ROOT / args.mode, args.exit_report)
