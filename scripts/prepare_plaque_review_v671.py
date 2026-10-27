"""Freeze the original all18 review schedule for the current integrated ROM."""

from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha
from scripts.inspect_graphic_paints_v669 import ROM
from scripts.review_current_plaques_v632 import SOURCE
from scripts.run_village_visits_v664 import CAP as CAP_ROOT
from scripts.verify_village_wrap_v608 import read, save

ROOT = Path('work/analysis/plaque_review_v671')
CAP = CAP_ROOT / 'plaque_review_v671_current'


def main():
    ROOT.mkdir(parents=True, exist_ok=True)
    assert not (ROOT / 'preflight.json').exists() and not CAP.exists()
    report_path = SOURCE / 'capture_report.json'
    original = read(report_path)
    assert original['frames'] == 7100 and original['cold_boot'] and not original['savestate_loaded']
    donor = original['battery_save_preloaded']
    assert sha(Path(donor['source']).read_bytes()) == donor['source_sha256']
    inputs = ROOT / 'inputs.json'
    save(inputs, original['scripted_input_schedule'])
    frozen = read('work/analysis/confirm_material_v572/audit_scope_before.json')
    save(ROOT / 'preflight.json', {'candidate': str(ROM), 'candidate_sha256': sha(ROM.read_bytes()),
        'release_hashes': {str(p): sha(p.read_bytes()) for p in (ROM, ROM.with_suffix('.manifest.json'),
            ROM.with_suffix('.xdelta'), Path('translations/release_stack.json'),
            Path('out/raphael_natural_v2_accepted_base.nds'))},
        'source_report': str(report_path), 'source_report_sha256': sha(report_path.read_bytes()),
        'donor': donor['source'], 'donor_sha256': donor['source_sha256'],
        'inputs': str(inputs), 'inputs_sha256': sha(inputs.read_bytes()),
        'capture_frames': [4300, 6300, 6700, 7100], 'frames': 7100,
        'previous_goal_turn_classification': 'no progress: preceding status reply only; existing V670 results finalized and archived this turn',
        'all_original_audits_before': {n: read(Path('translations') / n) for n in frozen},
        'full_goal_complete': False})
    print('V671 source schedule/donor and current release locked; no graphics or ROM changes.')


if __name__ == '__main__':
    main()
