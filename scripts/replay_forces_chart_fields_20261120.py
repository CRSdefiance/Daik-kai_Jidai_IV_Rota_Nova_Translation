"""Exercise the original chart and its no-home branch in isolated replays."""

from argparse import ArgumentParser
from io import StringIO
from json import dumps
from pathlib import Path
import sys

from scripts import headless_desmume_v193 as harness
from scripts import native_condition_fixture_v520 as fixtures
from scripts import replay_forces_relationships_20261115 as history
from scripts import stage_forces_chart_fields_20261120 as stage
from scripts.verify_inn_numerals_native_20261119 import read_cstring


BASE = stage.runtime.BASE
FRAMES = (13000, 13280, 13580, 13600, 13980, 14480, 14980)
PAUSES = (13600, 14000)
ACTIONS = ((13601, 'LEFT'), (14101, 'RIGHT'), (14261, 'LEFT'), (14601, 'B'))


def home_fixture(expected, clean, original_home):
    def apply(arm, raw, request):
        assert arm == expected and len(raw) == 0x400000
        assert arm[0x3CD24:0x3CD2C] == clean[0x3CD24:0x3CD2C] == raw[0x3CD24:0x3CD2C]
        cpu, get = history.get_machine(arm, raw)
        pool = get(0xCB160)
        assert get(0x397D8, pool) == 0 and get(0x7F244) == 0
        company = pool + 4
        assert read_cstring(cpu, get(0x3CF9C, company)) == b'Castor Co.'
        field = company + 11 - BASE
        assert get(0x3CD24, company) == raw[field]
        mode = request['mode']
        if mode == 'show-no-home':
            assert get(0xB65E4) == raw[field] and len(original_home) == 0
            original_home.append(raw[field])
            before, after = raw[field], 0x73
        else:
            assert mode == 'restore-home' and raw[field] == 0x73
            before, after = 0x73, original_home[0]
        assert before != after
        updated = raw[:field] + bytes([after]) + raw[field + 1:]
        return updated, dict(mode=mode, company=company, original_HOME_getter=0x0203CD24,
            locale='chart-only setup', changes=[dict(address=field + BASE, before=before, after=after)])
    return apply


def main(side, folder):
    assert not folder.exists()
    proof = stage.batch.load(stage.PROOF)
    rom = stage.parent.ROM if side == 'current' else stage.ROM
    assert stage.parent.base.digest(rom) == proof['parent_sha256' if side == 'current' else 'candidate_sha256']
    report = stage.batch.load(history.REFERENCE)
    donor = report['battery_save_preloaded']
    assert stage.parent.base.digest(donor['source']) == donor['source_sha256']
    events = [row for row in report['scripted_input_schedule'] if row['start'] <= 13301]
    events.extend(dict(start=f, duration=8, buttons=[key]) for f, key in ACTIONS)
    folder.mkdir(parents=True)
    inputs = folder / 'inputs.json'
    stage.batch.write(inputs, events)
    clean, arm = [stage.batch.NdsImage.open(path).read_file(stage.batch.ARM) for path in (stage.batch.CLEAN, rom)]
    schedule = [dict(until=14000, condition_fixture=dict(mode='show-no-home')),
                dict(until=14980, condition_fixture=dict(mode='restore-home')), dict(stop=True)]
    original = fixtures.set_condition, sys.stdin, sys.argv
    try:
        fixtures.set_condition = home_fixture(arm, clean, [])
        sys.stdin = StringIO(''.join(dumps(row) + '\n' for row in schedule))
        sys.argv = [harness.__file__, '--rom', str(rom), '--out', str(folder/'capture'), '--frames', '15000',
                    '--inputs-json', str(inputs), '--battery-save', donor['source'], '--touchscreen',
                    '--press-start', '-1', '--capture-every', '999999', '--capture-at', *map(str, FRAMES),
                    '--pause-at', str(PAUSES[0]), '--allow-condition-fixtures', '--dump-capture-ram']
        harness.main()
    finally:
        fixtures.set_condition, sys.stdin, sys.argv = original


if __name__ == '__main__':
    parser = ArgumentParser(description=__doc__)
    parser.add_argument('side', choices=('current', 'revised'))
    parser.add_argument('--out', type=Path, required=True)
    args = parser.parse_args()
    main(args.side, args.out)
