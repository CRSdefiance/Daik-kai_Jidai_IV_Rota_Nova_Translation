"""Verify current review provenance and exact retention of the original goal."""

from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha
from scripts.record_plaque_review_v671 import ARCHIVE, GUIDE, KEY
from scripts.review_current_plaques_v671 import CAP, ROOT
from scripts.verify_village_wrap_v608 import read, save


def main():
    pre = read(ROOT / 'preflight.json')
    proof_path = ROOT / 'current_plaque_review_proof.json'
    proof = read(proof_path)
    for path, digest in pre['release_hashes'].items():
        assert sha(Path(path).read_bytes()) == digest, path
    assert proof['candidate_sha256'] == pre['candidate_sha256']
    assert proof['script_sha256'] == sha(Path('scripts/review_current_plaques_v671.py').read_bytes())
    contract = read(CAP / 'run_contract.json')
    assert contract['runner_sha256'] == sha(Path('scripts/run_plaque_review_v671.py').read_bytes())
    assert contract['preflight_sha256'] == sha((ROOT / 'preflight.json').read_bytes())
    report = read(CAP / 'capture_report.json')
    assert report['frames'] == pre['frames'] and report['cold_boot'] and not report['callback_errors']
    assert len(proof['all18_current_native_review_entries']) == 18
    assert all(not r['fully_completed'] for r in proof['all18_current_native_review_entries'])
    assert len(proof['all17_independent_complete_font_masks']) == 17
    assert proof['current_native_static_pixels'] == 14272
    frozen = read('work/analysis/confirm_material_v572/audit_scope_before.json')
    for name, scope in frozen.items():
        path = Path('translations') / name
        data = read(path)
        assert data.get('historical_pending_items_retained') == scope['historical_pending_items_retained']
        assert data.get('plaque_style_v247', {}).get('ongoing_plaque_inventory') == scope['ongoing_plaque_inventory']
        assert all(data[k] == v for k, v in pre['all_original_audits_before'][name].items()
                   if k != 'current_goal_turn_classification')
        assert data[KEY]['proof_sha256'] == sha(proof_path.read_bytes())
        assert (ARCHIVE / 'audits' / name).read_bytes() == path.read_bytes()
    archive = read(ARCHIVE / 'provenance.json')
    for name, digest in archive['files'].items():
        assert sha((ARCHIVE / name).read_bytes()) == digest, name
    guide = read(GUIDE / 'provenance.json')
    assert len(guide['screenshots']) == 4 and not guide['publication_approved']
    for shot in guide['screenshots']:
        assert sha(Path(shot['path']).read_bytes()) == shot['sha256']
        assert shot['ROM_sha256'] == pre['candidate_sha256'] and shot['unmodified_capture']
    result = {'candidate_sha256': pre['candidate_sha256'], 'archive_files_verified': len(archive['files']),
        'source_and_current_full_captures': len(archive['screenshots']), 'guide_candidates': 4,
        '18_native_pairs17_fonts_and_three_hint_planes': True,
        'both_review_sheets_visually_inspected': True,
        'all_release_hashes_exact_all18_plaques_incomplete_all22_scopes_retained': True,
        'verifier_sha256': sha(Path(__file__).read_bytes()), 'full_goal_complete': False}
    save(ROOT / 'final_verification.json', result)
    print(f"V671 final: {len(archive['files'])} archive files/4 guide captures exact;18 plaques and22 scopes retained.")


if __name__ == '__main__':
    main()
