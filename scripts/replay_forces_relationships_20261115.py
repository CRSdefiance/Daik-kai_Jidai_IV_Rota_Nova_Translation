"""Exercise the original chart renderer for three isolated faction relationships."""

from argparse import ArgumentParser
from hashlib import sha256
from io import StringIO
from json import dumps
from pathlib import Path
from struct import unpack_from
import sys

from scripts import headless_desmume_v193 as harness
from scripts import native_condition_fixture_v520 as fixture
from scripts import register_market_info_trends_20261115 as current
from scripts.verify_personal_gameplay_v841 import get_machine


base = current.base
ROOT = Path('work/forces_relationships_20261115_v1')
REFERENCE = Path('work/market_info_trends_20261115_v1/faction_chart/capture/capture_report.json')
BASE = 0x02000000
PAUSES = ((13280, 'allied'), (14080, 'war'), (14880, 'subordinate'), (15680, 'restore'))
FRAMES = (13000, 13280, 13580, 14380, 15180, 15980, 16400)
ACTIONS = ((13301, 'RIGHT'), (13701, 'LEFT'), (14101, 'RIGHT'), (14501, 'LEFT'),
           (14901, 'RIGHT'), (15301, 'LEFT'), (15701, 'RIGHT'), (16101, 'B'))
LOCKS = ((0x3C858, 0x3C8F4), (0x3CB30, 0x3CB90), (0x3CBF4, 0x3CBFC),
         (0x8CEBC, 0x8CEF0), (0x8D2F8, 0x8D400))
OWNERS = (0x214BBAC, 0x214BECC)


def set_relationship(arm, raw, request):
    assert len(raw) == 0x400000 and request['mode'] in dict(PAUSES).values()
    cpu, get = get_machine(arm, raw)
    pool = get(0xCB160)
    assert get(0x397D8, pool) == 0 and get(0x7F244) == 0
    # Bind the current chart and selection slots to the exact original producer.
    chart_ptr = [i for i in range(0x180000, 0x1A0000, 4)
                 if unpack_from('<I', raw, i)[0] in OWNERS
                 and unpack_from('<I', raw, i + 0x6940)[0] == 5
                 and unpack_from('<6I', raw, i + 0x68EC) == (9, 7, 10, 8, 6, 0)]
    chart, = chart_ptr
    player, other = pool + 4, pool + 4 + 9 * 0x4C
    assert get(0x3D030, player) == 0 and get(0x3D030, other) == 9
    player_name = get(0x3CF9C, player)
    assert bytes(cpu.mem_read(player_name, 11)) == b'Castor Co.\0'
    assert bytes(cpu.mem_read(get(0x3CF9C, other), 6)) == b'Pasha\0'
    relation_offset, parent_offset = player + 0x1F + 9 - BASE, other + 0x1E - BASE
    orig = (get(0x3CB30, other, 0), get(0x3CBF4, other))
    assert orig == (raw[relation_offset], raw[parent_offset])
    mode = request['mode']
    before, after, selected = {
        'allied': ((0, 21), (1, 21), 2),
        'war': ((1, 21), (2, 21), 3),
        'subordinate': ((2, 21), (0, 0), 4),
        'restore': ((0, 0), (0, 21), 1),
    }[mode]
    assert orig == before
    result = bytearray(raw)
    changes = []
    for offset, value in zip((relation_offset, parent_offset), after, strict=True):
        if value != raw[offset]:
            result[offset] = value
            cpu.mem_write(BASE + offset, bytes((value,)))
            changes.append(dict(address=BASE + offset, before=raw[offset], after=value))
    assert get(0x3C858, other) == selected and get(0x3CB30, other, 0) == after[0]
    assert get(0x3CBF4, other) == after[1]
    return bytes(result), dict(mode=mode, chart=BASE + chart, selected_player_id=0, next_faction_id=9,
        original_relation_getter=0x0203C858, expected_state=selected, changes=changes,
        before_RAM_sha256=sha256(raw).hexdigest(), after_RAM_sha256=sha256(result).hexdigest())


def replay(rom, rom_sha, folder):
    assert base.digest(rom) == rom_sha
    history = base.load(REFERENCE)
    donor = history['battery_save_preloaded']
    assert base.digest(donor['source']) == donor['source_sha256']
    folder.mkdir(parents=True)
    inputs = folder / 'inputs.json'
    events = [row for row in history['scripted_input_schedule'] if row['start'] <= 13001]
    events.extend(dict(start=f, duration=8, buttons=[key]) for f, key in ACTIONS)
    base.save(inputs, events)
    clean, arm = [base.NdsImage.open(p).read_file(current.stage.ARM) for p in (current.stage.CLEAN, rom)]
    assert all(clean[lo:hi] == arm[lo:hi] for lo, hi in LOCKS)

    def supply(actual, raw, request):
        assert actual == arm
        return set_relationship(arm, raw, request)

    commands = [dict(until=next_f, condition_fixture=dict(mode=mode))
                for (_, mode), next_f in zip(PAUSES, (14080, 14880, 15680, 16400), strict=True)]
    commands.append(dict(stop=True))
    args = [harness.__file__, '--rom', str(rom), '--out', str(folder / 'capture'), '--frames', '16401',
        '--inputs-json', str(inputs), '--battery-save', donor['source'], '--touchscreen', '--press-start', '-1',
        '--capture-every', '999999', '--capture-at', *map(str, FRAMES), '--pause-at', '13280',
        '--allow-condition-fixtures', '--dump-capture-ram']
    previous, stdin, argv = fixture.set_condition, sys.stdin, sys.argv
    try:
        fixture.set_condition, sys.stdin, sys.argv = supply, StringIO(''.join(dumps(row) + '\n' for row in commands)), args
        harness.main()
    finally:
        fixture.set_condition, sys.stdin, sys.argv = previous, stdin, argv
    report = base.load(folder / 'capture/capture_report.json')
    assert report['cold_boot'] and not report['savestate_loaded'] and not report['callback_errors']
    assert report['ROM_sha256'] == rom_sha and report['frames'] == 16400
    assert report['scripted_input_schedule'] == events
    assert [(row['frame'], row['mode']) for row in report['synthetic_condition_fixtures']] == list(PAUSES)
    assert base.digest(donor['source']) == donor['source_sha256']


if __name__ == '__main__':
    parser = ArgumentParser(description=__doc__)
    parser.add_argument('--rom', type=Path, default=current.ROM)
    parser.add_argument('--sha256', default=base.load(current.RELEASE)['candidate_sha256'])
    parser.add_argument('--out', type=Path, default=ROOT / 'previous')
    args = parser.parse_args()
    replay(args.rom, args.sha256, args.out)
