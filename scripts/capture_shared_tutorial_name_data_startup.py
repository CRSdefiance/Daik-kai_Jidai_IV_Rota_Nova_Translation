"""Cold boot the exact planned identity while the canonical stack is reconstructed."""
import os
import sys
from pathlib import Path
from scripts import headless_desmume_v193 as harness
from dk4tool.patch.grand_race_menu_release import sha
from scripts.audit_story_glyph_consistency import load, save

ROOT = Path('work/analysis/Shared_tutorial_name_data_identity_coldboot_20261104')
PREP = Path('work/analysis/Shared_tutorial_name_data_release_v4_20261104/registered_preparation.json')
PARENT = Path('work/analysis/Rafael_B36_B41_release_verified_20261104/own_registered_startup_verification.json')

if __name__ == '__main__':
    assert not ROOT.exists()
    prep, parent = map(load, [PREP, PARENT])
    rom = Path(prep['reference_ROM'])
    assert sha(rom.read_bytes()) == prep['target_ROM_sha256']
    capture_path = Path(parent['capture_report'])
    assert sha(capture_path.read_bytes()) == parent['capture_report_sha256']
    prior = load(capture_path)
    assert prior['frames'] == 4001 and parent['actual_captain_getter'] == parent['actual_route_word'] == 0
    ROOT.mkdir(); inputs = ROOT / 'ordinary_NewGame_inputs.json'
    save(inputs, prior['scripted_input_schedule'])
    save(ROOT / 'run_plan.json', dict(reference_ROM=str(rom), target_ROM_sha256=prep['target_ROM_sha256'],
        parent_startup=str(PARENT), parent_startup_sha256=sha(PARENT.read_bytes()),
        prior_capture=str(capture_path), prior_capture_sha256=sha(capture_path.read_bytes()),
        inputs=str(inputs), inputs_sha256=sha(inputs.read_bytes()),
        frames=4001, own_identity_no_battery_savestate_orRAM_override=True, registered_identity_equality_pending=True,
        expected_captain=0, PID=os.getpid(), producer_sha256=sha(Path(__file__).read_bytes())))
    sys.argv = ['headless_desmume_v193.py', '--rom', str(rom), '--out', str(ROOT), '--frames', '4001',
        '--inputs-json', str(inputs), '--capture-every', '999999', '--capture-at',
        *map(str, prior['exact_requested_capture_frames']), '--dump-ram']
    harness.main()
    report = load(ROOT / 'capture_report.json')
    assert report['ROM_sha256'] == prep['target_ROM_sha256'] and report['cold_boot'] and not report['savestate_loaded']
    assert report['frames'] == 4001 and not report['callback_errors']
    save(ROOT / 'terminal.json', dict(frames=4001, target_ROM_sha256=prep['target_ROM_sha256'],
        own_RAM_andregistered_release_binding_pending=True, full_route_orhardware=False))
