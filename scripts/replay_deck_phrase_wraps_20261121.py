"""Replay Gerhard's revised sail-handling comment with the established assignment fixture."""

import subprocess
import sys
from inspect import getsource
from pathlib import Path
from shutil import copy2
from types import FunctionType

from PIL import Image
from scripts import native_sails_boarding_fixture_v883 as fixture
from scripts import run_sails_boarding_adapter_v883 as adapter
from scripts import stage_deck_phrase_wraps_20261121 as stage
from scripts.finish_refit_display_v712 import load as load_capture
from scripts.source_locked_derivation_v5118 import checked_text
from scripts.verify_personal_gameplay_v841 import hold, model_state


base = stage.base
CASE = 'GerhardSails'
CAPTURE = stage.ROOT / 'gerhard_gameplay'
PROOF = stage.ROOT / 'gerhard_gameplay.json'
HISTORY = Path('work/analysis/sails_boarding_v883/GerhardSails_run_plan.json')


def assign(arm, raw, request):
    assert request == CASE
    assert stage.sha256(arm).hexdigest() == base.load(stage.PROOF)['target_ARM9_sha256']
    source = checked_text(getsource(fixture.assign), {
        "    config=read('translations/sails_boarding_editorial_release_v1.json')\n"
        "    assert sha(arm) in (config['source_arm9_sha256'],config['target_arm9_sha256'])\n": '',
    })
    scope = vars(fixture) | {'__file__': __file__}
    exec(compile(source, __file__ + '::room-fixture', 'exec'), scope)
    return scope['assign'](arm, raw, request)


def worker():
    source = checked_text(getsource(adapter.main), {
        'from scripts.native_sails_boarding_fixture_v883 import assign as assign_missionary':
            'from scripts.replay_deck_phrase_wraps_20261121 import assign as assign_missionary',
    })
    scope = vars(adapter) | {'__file__': __file__}
    exec(compile(source, __file__ + '::replay-adapter', 'exec'), scope)
    sys.argv = sys.argv[1:]
    scope['main']()


def gameplay():
    plan = base.load(HISTORY)
    source, inputs, commands = (Path(plan[k]) for k in ('source_donor', 'inputs', 'recorded_navigation'))
    assert base.digest(source) == plan['source_donor_sha256']
    assert base.digest(inputs) == plan['inputs_sha256']
    assert base.digest(commands) == plan['recorded_navigation_sha256']
    donor = stage.ROOT / 'disposable_gerhard.dsv'
    assert not CAPTURE.exists() and not donor.exists()
    copy2(source, donor)
    args = ['--rom', str(stage.ROM), '--out', str(CAPTURE), '--battery-save', str(donor), '--inputs-json', str(inputs),
            '--touchscreen', '--frames', '4801', '--capture-every', '999999', '--capture-at', '1', '60', '180', '3200',
            '--dump-capture-ram', '--dump-pause-ram', '--dump-ram', '--pause-at', '3200', '--allow-sails-boarding-fixtures']
    subprocess.run([sys.executable, '-m', 'scripts.replay_deck_phrase_wraps_20261121', 'worker', *args],
                   input=commands.read_text(encoding='utf-8'), text=True, check=True)
    assert base.digest(source) == base.digest(donor) == plan['source_donor_sha256']
    verify()


def verify():
    digest = base.digest(stage.ROM)
    report, shots, receipt = load_capture(CAPTURE, digest, 4800)
    plan = base.load(HISTORY)
    previous_report = base.load(Path(plan['folder']) / 'capture_report.json')
    assert previous_report['scripted_input_schedule'] == report['scripted_input_schedule']
    journal = CAPTURE / 'navigation_command_journal.json'
    old_journal = Path(plan['folder']) / journal.name
    assert base.load(journal)['commands_received'] == base.load(old_journal)['commands_received']
    data = {}
    for item in report['read_only_capture_RAM_snapshots'] + report['read_only_pause_RAM_snapshots']:
        path = Path(item['path'])
        raw = path.read_bytes()
        assert item['read_only_export'] and len(raw) == 0x400000 and base.digest(path) == item['sha256']
        assert data.setdefault(item['frame'], raw) == raw
    evidence, = report['synthetic_sails_boarding_assignment_fixtures']
    assert evidence['frame'] == 3200 and evidence['case'] == CASE and len(evidence['changes']) == 3
    assert not any(v for k, v in report.items() if k.startswith('synthetic_') and k != 'synthetic_sails_boarding_assignment_fixtures')
    image = base.NdsImage.open(stage.ROM)
    arm = image.read_file(stage.ARM)
    after, reapplied = assign(arm, data[3200], CASE)
    assert reapplied == {k: v for k, v in evidence.items() if k != 'frame'}
    assert stage.sha256(after).hexdigest() == evidence['after_RAM_sha256']
    row, = (r for r in base.load(stage.PROOF)['records'] if r['message_ID'] == 1524)
    check = FunctionType(hold.__code__, hold.__globals__ | {
        'layout': stage.ordered_layout, 'expected_pixels': stage.current_pixels,
    })
    holds = [check(image, data[frame], shots[frame], row | {'actor_ID': 16, 'message_id': 1524}, 12) | {'frame': frame}
             for frame in (4200, 4400)]
    assert all(item['source_role_type'] == 0 and item['original_parent_activity_state'] == 0 for item in holds)
    assert model_state(arm, data[3400]) == model_state(arm, data[4800])
    assert shots[3400].tobytes() == shots[4800].tobytes()
    path = stage.ROOT / 'gerhard_two_holds_and_return.png'
    sheet = Image.new('RGB', (768, 384))
    for column, frame in enumerate((4200, 4400, 4800)):
        sheet.paste(shots[frame], (256 * column, 0))
    sheet.save(path)
    base.save(PROOF, dict(candidate_sha256=digest, complete_holds=holds, report=receipt,
                          original_room_fixture=evidence, normal_return_frame=4800, hardware=False,
                          actual_emulator=True, inherited_Copenhagen_save=True, natural_assignment=False,
                          sheet={'path': str(path), 'sha256': base.digest(path)},
                          evidence={str(p): base.digest(p) for p in (journal, old_journal, CAPTURE / 'capture_report.json', path)}))
    print('Gerhard’s revised sail comment in two native/RGB holds and a return to Copenhagen.', flush=True)


if __name__ == '__main__':
    if sys.argv[1:2] == ['worker']:
        worker()
    else:
        gameplay()

