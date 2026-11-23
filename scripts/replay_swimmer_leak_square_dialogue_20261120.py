"""Replay the revised scenes with the original game inputs and disclosed fixtures."""

import argparse
import json
from pathlib import Path
import sys
from types import FunctionType, SimpleNamespace

from scripts import headless_desmume_v193 as harness
from scripts import native_condition_fixture_v520 as adapter
from scripts import replay_fleet_encounter_dialogue_20261119 as fleet
from scripts import replay_square_samples_wraps_20261115 as square
from scripts import run_ship_emergency_replays_v1 as leak
from scripts import stage_swimmer_leak_square_dialogue_20261120 as stage
from scripts.run_battle_cooking_livestock_live_v911 import GrowingCommands
from scripts.verify_personal_gameplay_v841 import get_machine


TOWN = {'square-war': (0, 682), 'square-sunk': (5, 687)}
CASES = ('mermaid', 'leak', *TOWN)


def town_condition(arm, ram, request):
    case = request['mode']
    condition, message = TOWN[case]
    clean_arm = stage.NdsImage.open(stage.CLEAN).read_file(stage.ARM)
    assert all(arm[lo:hi] == clean_arm[lo:hi] for lo, hi in ((0xB2E04, 0xB2E30), (0x5FA98, 0x5FB54)))
    _, get = get_machine(arm, ram)
    assert get(0xB65E4) == 22
    town = get(0xB6618)
    assert town == get(0xCB178) + 4 + 22 * 108 and get(0xB2E04, town) == 12
    offset = town + 0x6A - 0x02000000
    replacement = bytes((condition, 30))
    changed = ram[:offset] + replacement + ram[offset + len(replacement):]
    _, get = get_machine(arm, changed)
    assert get(0xB2E04, town) == condition and get(0x5FA98, 0, town) == message
    changes = [dict(address=0x02000000 + index, before=ram[index], after=changed[index])
               for index in range(offset, offset + 2) if ram[index] != changed[index]]
    assert len(changes) == 2
    return changed, dict(mode=case, town_ID=22, original_status=12, supplied_status=condition,
                         original_shop_selection=message, changes=changes)


def anchor_ship(setter, source_report, *, source_frame=8927):
    source, = [row for row in source_report['read_only_pause_RAM_snapshots'] if row['frame'] == source_frame]
    donor = Path(source['path']).read_bytes()
    assert len(donor) == 0x400000 and source['read_only_export'] and stage.digest(donor) == source['sha256']

    def apply(arm, raw, request):
        changed, receipt = setter(arm, raw, request)
        if request['mode'] not in ('choose', 'select-leak'):
            return changed, receipt

        def ship(memory):
            _, get = get_machine(arm, memory)
            assert get(0x7F244) == 1
            fleet_addr = get(0xCB1A8) + 4 + get(0x2E58C) * 0x84
            return get(0x36C70, fleet_addr + 0xC)

        pos = ship(raw) + 0x10 - 0x02000000
        assert pos == ship(donor) + 0x10 - 0x02000000
        assert 0 < pos < len(raw) - 8 and raw[pos:pos+8] != donor[pos:pos+8]
        # The last header byte carries transient voyage state. Bind the ship
        # by the stable fields on each side and leave the state byte intact.
        assert raw[pos-16:pos-1] == donor[pos-16:pos-1]
        assert raw[pos+8:pos+48] == donor[pos+8:pos+48]
        actual = changed[:pos] + donor[pos:pos+8] + changed[pos+8:]
        coords = [dict(address=0x02000000 + index, before=changed[index], after=actual[index])
                  for index in range(pos, pos + 8) if changed[index] != actual[index]]
        return actual, receipt | dict(voyage_coordinate_anchor_only=True, coordinate_source=source,
                                      changes=receipt['changes'] + coords)

    return apply


def plan(case, anchored=False, *, rom=stage.ROM):
    if case in TOWN:
        prior, report, donor, frames = square.history('epidemic')
        end = report['frames']
        return prior, donor, 3200, end, report['scripted_input_schedule'], (
            dict(until=end, condition_fixture={'mode': case}), dict(stop=True),
        ), frames, town_condition
    if case == 'mermaid':
        earlier = fleet.earlier.OUT
        terminal = stage.load(earlier / 'terminal.json')
        prefix = earlier / 'original_input_prefix.json'
        assert stage.digest(prefix.read_bytes()) == terminal['original_input_prefix_sha256']
        end, commands = fleet.schedule(case)
        setter = FunctionType(fleet.set_condition.__code__, vars(fleet) |
                              {'build': SimpleNamespace(ROM=rom, CLEAN=stage.CLEAN, ARM=stage.ARM)})
        pause = fleet.PAUSE
    else:
        earlier = leak.DONOR
        terminal = stage.load(earlier / 'terminal.json')
        prefix, journal = earlier / 'inputs.json', Path(terminal['commands'])
        assert stage.digest(prefix.read_bytes()) == terminal['input_prefix_sha256']
        assert stage.digest(journal.read_bytes()) == terminal['commands_sha256']
        commands = [json.loads(line) for line in journal.read_text(encoding='utf-8').splitlines()][:4]
        commands += [{'stop': True}]
        commands[0]['condition_fixture'] = {'mode': 'select-leak'}
        commands[3]['condition_fixture'] = {'mode': 'restore-leak-selection'}
        setter = FunctionType(leak.set_condition.__code__, vars(leak) | {'ROM': rom})
        pause, end = leak.PAUSE, commands[3]['until']
    path = Path(terminal['report'])
    assert stage.digest(path.read_bytes()) == terminal['report_sha256']
    report = stage.load(path)
    donor = Path(report['battery_save_preloaded']['source'])
    assert stage.digest(donor.read_bytes()) == report['battery_save_preloaded']['source_sha256']
    if anchored:
        setter = anchor_ship(setter, report)
    return path, donor, pause, end, stage.load(prefix), commands, (), setter


def main(case, destination, anchored=False):
    staged = stage.load(stage.ROOT / 'staging.json')
    assert stage.digest(stage.ROM.read_bytes()) == staged['candidate_sha256']
    source, donor, pause, end, inputs, commands, frames, setter = plan(case, anchored)
    donor_sha = stage.digest(donor.read_bytes())
    output = Path(destination) / case
    output.mkdir(parents=True)
    inputs_path, journal = output / 'inputs.json', output / 'commands.jsonl'
    stage.write(inputs_path, inputs)
    journal.write_text(''.join(json.dumps(row) + '\n' for row in commands), encoding='utf-8')
    argv = [harness.__file__, '--rom', str(stage.ROM), '--out', str(output / 'capture'),
            '--frames', str(end + 1), '--inputs-json', str(inputs_path), '--battery-save', str(donor),
            '--touchscreen', '--capture-every', '999999', '--pause-at', str(pause), '--allow-condition-fixtures',
            '--dump-pause-ram', '--dump-ram']
    if frames:
        argv += ['--press-start', '-1', '--capture-at', *map(str, frames)]
    original = adapter.set_condition, sys.stdin, sys.argv
    cursor = GrowingCommands(journal)
    try:
        adapter.set_condition, sys.stdin, sys.argv = setter, cursor, argv
        harness.main()
    finally:
        adapter.set_condition, sys.stdin, sys.argv = original
        cursor.close()
    report_path = output / 'capture/capture_report.json'
    report = stage.load(report_path)
    assert report['frames'] == end and report['ROM_sha256'] == staged['candidate_sha256']
    assert report['cold_boot'] and not report['savestate_loaded'] and not report['callback_errors']
    assert stage.digest(donor.read_bytes()) == donor_sha
    assert len(report['synthetic_condition_fixtures']) == (1 if case in TOWN else 2)
    stage.write(output / 'terminal.json', dict(case=case, candidate_sha256=staged['candidate_sha256'],
        capture=str(report_path), capture_sha256=stage.digest(report_path.read_bytes()),
        prior_capture=str(source), prior_capture_sha256=stage.digest(source.read_bytes()),
        save_sha256=donor_sha, ordinary_inputs_after_fixture=True, natural_condition_selection=False))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('case', choices=CASES)
    parser.add_argument('--output', required=True, type=Path)
    parser.add_argument('--voyage-anchor', action='store_true')
    args = parser.parse_args()
    main(args.case, args.output, args.voyage_anchor)
