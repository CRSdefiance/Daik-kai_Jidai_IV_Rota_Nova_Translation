"""Exercise original sea inspection using the Monster Fish or Ghost Ship model."""

from argparse import ArgumentParser
from inspect import getsource
from json import dumps
from pathlib import Path
import sys

from scripts import headless_desmume_v193 as harness
from scripts import native_condition_fixture_v520 as adapter
from scripts import native_inspection_status_lookout_fixture_v1581 as previous
from scripts import register_aziza_mutiny_dialogue_20261115 as parent
from scripts.run_battle_cooking_livestock_live_v911 import GrowingCommands
from scripts.source_locked_derivation_v5118 import checked_text

base = parent.base
ROOT = Path('work/special_target_labels_20261115_v2')
HISTORICAL = Path('work/emulation_v193/inspection_status_lookout_v1582_1578/capture_report.json')
FRAMES = (4800, 5400, 5600, 5700, 5800, 5830, 5900, 6040, 6100, 6200, 6300)


def special_target(rom, expected, model, arm, raw, request):
    assert model in (149, 153) and request == previous.REQUEST
    code = checked_text(getsource(previous.apply_fixture), {
        "    assert sha(arm)==read('work/analysis/inspection_status_release_v1577/registered_release_verification.json')['ARM9_sha256']":
            '    assert sha(arm) == EXACT_ARM',
        '    beforemodel=bytes(cpu.mem_read(model,140))': '''    assert bytes(cpu.mem_read(fleet + 16, 1)) == bytes([149])
    if SELECTED_MODEL != 149:
        cpu.mem_write(fleet + 16, bytes([SELECTED_MODEL]))
    model = models + 4 + SELECTED_MODEL * 140
    assert get(MODEL_GETTER, fleet + 12) == model
    assert bytes(cpu.mem_read(model + 8, 24)).split(bytes(1))[0] == EXPECTED_LABEL
    beforemodel=bytes(cpu.mem_read(model,140))''',
        '    assert get(0xAB128,mobile)==34': '    assert get(0xAB128,mobile)==SELECTED_CLASS',
        '    owned={at+i for label,at,n in regions for i in range(n)}':
            '''    if SELECTED_MODEL != 149:
        regions.append(('explicit_existing_ship_model_link', fleet + 16, 1))
    owned={at+i for label,at,n in regions for i in range(n)}''',
        "'context':'original_registered_Monster_Fish_inspection'": "'context':'original_registered_special_target_inspection'",
        "'original_existing_model_ID':149,'original_class_ID':34":
            "'original_existing_model_ID':SELECTED_MODEL,'original_class_ID':SELECTED_CLASS",
        "'no_message_ID_renderer_target_type_actor_identity_or_result_injected':True":
            "'no_message_ID_renderer_actor_identity_or_result_injected':True, 'target_model_link_fixture': SELECTED_MODEL != 149",
    })
    env = vars(previous) | {'EXACT_ARM': expected, 'SELECTED_MODEL': model, 'SELECTED_CLASS': 34 if model == 149 else 38,
                            'MODEL_GETTER': 0x36C94,
                            'EXPECTED_LABEL': '化魚'.encode('cp932') if model == 149 else b'Ghost',
                            'ROM': rom, '__file__': __file__}
    exec(compile(code, __file__ + '::declared-special-target-fixture', 'exec'), env)
    return env['apply_fixture'](arm, raw, request)


def replay(case, candidate=None, settled=False):
    parent_receipt = base.load(parent.RELEASE)
    rom = parent.ROM if candidate is None else Path(candidate)
    assert base.digest(parent.ROM) == parent_receipt['candidate_sha256']
    if candidate:
        from scripts import stage_special_target_labels_20261115 as stage
        data = base.load(stage.STORED)
        assert rom == stage.ROM and base.digest(rom) == data['candidate_sha256']
        assert data['previous_sha256'] == parent_receipt['candidate_sha256']
        expected_arm = data['target_ARM9_sha256']
    else:
        expected_arm = parent_receipt['target_ARM9_sha256']
    model = 149 if case == 'monster' else 153
    history = base.load(HISTORICAL)
    assert history['cold_boot'] and not history['savestate_loaded'] and not history['callback_errors']
    donor = history['battery_save_preloaded']
    assert donor['copied_byte_exact_before_cold_boot'] and base.digest(donor['source']) == donor['source_sha256']
    folder = ROOT / (case + '_settled' if settled else case)
    folder.mkdir(parents=True)
    inputs, commands = folder / 'inputs.json', folder / 'commands.jsonl'
    schedule = history['scripted_input_schedule']
    frames, end = FRAMES, 6300
    if settled:
        assert model == 153
        # Two separated confirmations allow each native panel to settle.
        schedule = [row for row in schedule if row['start'] <= 5701]
        schedule.extend({'start': n, 'duration': 6, 'buttons': ['A']} for n in (6051, 6451))
        frames, end = (4800, 5400, 5600, 5700, 5950, 6300, 6750), 6750
    base.save(inputs, schedule)
    commands.write_text(''.join(dumps(row) + '\n' for row in (
        {'until': 5700, 'condition_fixture': previous.REQUEST}, {'until': end}, {'stop': True})), encoding='utf-8')
    argv = [harness.__file__, '--rom', str(rom), '--out', str(folder / 'capture'),
            '--frames', str(end + 1), '--inputs-json', str(inputs), '--press-start', '-1', '--touchscreen',
            '--battery-save', donor['source'], '--capture-every', '999999', '--capture-at', *map(str, frames),
            '--pause-at', '4800', '--dump-pause-ram', '--allow-condition-fixtures']
    stdin, original, old = sys.stdin, sys.argv, adapter.set_condition
    stream = GrowingCommands(commands)
    try:
        adapter.set_condition = lambda arm, raw, request: special_target(rom, expected_arm, model, arm, raw, request)
        sys.stdin, sys.argv = stream, argv
        harness.main()
    finally:
        sys.stdin, sys.argv, adapter.set_condition = stdin, original, old
        stream.close()
    path = folder / 'capture/capture_report.json'
    report = base.load(path)
    assert report['ROM_sha256'] == base.digest(rom) and report['scripted_input_schedule'] == schedule
    assert report['frames'] == end and report['cold_boot'] and not report['savestate_loaded'] and not report['callback_errors']
    assert report['battery_save_preloaded']['source_sha256'] == donor['source_sha256']
    fixture, = report['synthetic_condition_fixtures']
    assert fixture['frame'] == 4800 and fixture['original_existing_model_ID'] == model and fixture['all_other4MiB_bytes_exact']
    base.save(folder / 'terminal.json', {'case': case, 'candidate_sha256': report['ROM_sha256'],
                                        'capture': str(path), 'capture_sha256': base.digest(path),
                                        'original_model': model, 'fixture': fixture,
                                        'historical_replay': str(HISTORICAL), 'settled_controller_schedule': settled,
                                        'natural_spawn': False})


if __name__ == '__main__':
    parser = ArgumentParser(description=__doc__)
    parser.add_argument('case', choices=('monster', 'ghost_before', 'ghost_after'))
    parser.add_argument('--candidate')
    parser.add_argument('--settled', action='store_true')
    args = parser.parse_args()
    replay(args.case, args.candidate, args.settled)
