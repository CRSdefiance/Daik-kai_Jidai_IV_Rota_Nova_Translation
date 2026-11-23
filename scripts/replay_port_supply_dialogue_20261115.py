"""Replay the Port supply exchange and the ordinary Riga departure."""

from argparse import ArgumentParser
from inspect import getsource
from pathlib import Path
import sys
from types import FunctionType, SimpleNamespace

from scripts import headless_desmume_v193 as harness
from scripts import native_condition_fixture_v520 as fixture_adapter
from scripts import native_port_fixture_v762 as original_fixture
from scripts import observe_london_riga_towns_20261115 as riga
from scripts import observe_online_gallery_common_v1 as playback
from scripts import observe_setup_save_common_v1 as trace
from scripts import replay_london_stockholm_dialogue_20261115 as startup
from scripts import stage_port_supply_dialogue_20261115 as stage
from scripts.run_battle_cooking_livestock_live_v911 import GrowingCommands
from scripts.source_locked_derivation_v5118 import checked_text


base, ROOT, parent = stage.base, stage.ROOT, stage.parent
STARTUP = ROOT / 'own_startup_verification.json'
WATER = Path('work/emulation_v193/port_services_v762_water_only_762/capture_report.json')
WATER_FRAMES = (3200, 3400, 3800, 4200, 4600, 5000, 5400, 5800, 6200, 6600, 7000, 7200)
RIGA_END = 5860


def low_water(arm, raw, request):
    release = base.load(parent.RELEASE)
    assert stage.digest(arm) == release['target_ARM9_sha256']
    source = base.load(WATER)['synthetic_port_service_fixtures']
    historical = base.NdsImage.open('out/all_routes_combined_v762_candidate.nds').read_file(stage.ARM)
    assert stage.digest(historical) == source[0]['ARM9_sha256']
    # The same original fleet getters and supply assignment back the fixture.
    for start, stop in ((0x60518, 0x6063C), (0x34E60, 0x34FE4), (0x2E58C, 0x2E5A4),
                        (0xCB148, 0xCB15C), (0xCB1A8, 0xCB1B8)):
        assert historical[start:stop] == arm[start:stop]
    code = checked_text(getsource(original_fixture.assign), {
        "    assert sha(arm) in ('6508bf3e43144efc4a9b449564e1acd2a0eecacb7184ed23408ce1856cea1ddf', read('translations/port_services_editorial_release_v1.json')['target_arm9_sha256'])":
            '    assert sha(arm) == REQUIRED_ARM',
    })
    env = vars(original_fixture) | {'REQUIRED_ARM': release['target_ARM9_sha256'], '__file__': __file__}
    exec(compile(code, __file__ + '::locked-water-prerequisite', 'exec'), env)
    after, receipt = env['assign'](arm, raw, request)
    assert receipt['before_water_food'] == [350, 350] and receipt['after_water_food'] == [0, 700]
    assert len(receipt['changes']) == 11
    return after, receipt


def target():
    selection = ROOT / 'candidate_selection.json'
    record = base.load(stage.STORED)
    if not selection.exists():
        base.save(selection, {'candidate': str(stage.ROM), 'candidate_sha256': record['candidate_sha256']})
    assert base.load(selection)['candidate_sha256'] == base.digest(stage.ROM)
    return SimpleNamespace(ROM=stage.ROM, RELEASE=selection)


def water(case):
    selected = parent if case == 'water_before' else target()
    folder = ROOT / case
    folder.mkdir()
    report = base.load(WATER)
    donor = report['battery_save_preloaded']
    assert base.digest(donor['source']) == donor['source_sha256'] and donor['copied_byte_exact_before_cold_boot']
    assert report['cold_boot'] and not report['savestate_loaded'] and report['frames'] == 7201
    inputs, commands = folder / 'inputs.json', folder / 'commands.jsonl'
    base.save(inputs, report['scripted_input_schedule'])
    commands.write_text(
        '{"until": 5200, "condition_fixture": {"mode": "water_only"}}\n{"until": 7200}\n{"stop": true}\n',
        encoding='utf-8',
    )
    argv = [sys.argv[0], '--rom', str(selected.ROM), '--out', str(folder / 'capture'),
            '--frames', '7201', '--inputs-json', str(inputs), '--press-start', '-1',
            '--battery-save', donor['source'], '--touchscreen', '--capture-every', '999999',
            '--capture-at', *map(str, WATER_FRAMES), '--pause-at', '3200',
            '--dump-pause-ram', '--allow-condition-fixtures']
    stream = GrowingCommands(commands)
    old = fixture_adapter.set_condition
    previous_stdin, previous_argv = sys.stdin, sys.argv
    try:
        fixture_adapter.set_condition = low_water
        sys.stdin, sys.argv = stream, argv
        harness.main()
    finally:
        fixture_adapter.set_condition = old
        sys.stdin, sys.argv = previous_stdin, previous_argv
        stream.close()


def schedule(case):
    inputs, frames, _, prior, donor = riga.schedule(case)
    return ([row for row in inputs if row['start'] < RIGA_END],
            [frame for frame in frames if frame < RIGA_END], RIGA_END, prior, donor)


def departure():
    target_spec = target()
    env = vars(playback) | {'ROOT': ROOT, 'parent': target_spec, 'get_schedule': schedule,
                            'observer': trace.scoped_observer, '__file__': __file__, 'FOCUS': set(range(3668))}
    FunctionType(playback.main.__code__, env)('riga')


if __name__ == '__main__':
    parser = ArgumentParser(description=__doc__)
    parser.add_argument('case', choices=('startup', 'riga', 'water_before', 'water_after'))
    case = parser.parse_args().case
    if case == 'startup':
        FunctionType(startup.cold_boot.__code__, startup.cold_boot.__globals__ | {'stage': stage})()
    elif case == 'riga':
        departure()
    else:
        water(case)
