"""Verify the exact V675 evidence archive and unchanged release/full audit scope."""

from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha
from scripts.record_still_reveal_v675 import ARCHIVE, KEY, SCRIPTS
from scripts.verify_still_reveal_v675 import ROOT
from scripts.verify_village_wrap_v608 import read, save


def main():
    pre, archive = read(ROOT / 'preflight.json'), read(ARCHIVE / 'provenance.json')
    pp, proof = ROOT / 'proof.json', read(ROOT / 'proof.json')
    assert proof['verifier_sha256'] == sha(Path('scripts/verify_still_reveal_v675.py').read_bytes())
    assert archive['source_scripts'] == {path: sha(Path(path).read_bytes()) for path in SCRIPTS}
    for path, digest in pre['release_hashes'].items():
        assert sha(Path(path).read_bytes()) == digest
    for path, digest in archive['files'].items():
        assert sha((ARCHIVE / path).read_bytes()) == digest, path
    assert proof['specific_V674_blank_and_reveal_comparisons_resolved_without_ROM_change']
    assert len(proof['full_two_screen_pairs']) == 64
    mixed = [case['mixed_source_frame_original_DMA_prediction']
             for case in proof['actual_upper_source_and_display_cases']
             if case['mixed_source_frame_original_DMA_prediction']]
    assert [case['first_observed_upper_DMA_line'] for case in mixed] == [68, 143]
    frozen = read('work/analysis/confirm_material_v572/audit_scope_before.json')
    for name, scope in frozen.items():
        path = Path('translations') / name
        data = read(path)
        assert data.get('historical_pending_items_retained') == scope['historical_pending_items_retained']
        assert data.get('plaque_style_v247', {}).get('ongoing_plaque_inventory') == scope['ongoing_plaque_inventory']
        assert all(data[key] == value for key, value in pre['all_original_audits_before'][name].items()
                   if key != 'current_goal_turn_classification')
        assert data[KEY]['proof_sha256'] == sha(pp.read_bytes())
        assert path.read_bytes() == (ARCHIVE / 'audits' / name).read_bytes()
    save(ROOT / 'final_verification.json', {'archive_files_verified': len(archive['files']),
        'twenty_native_paints22_actual_source_frames64_screen_pairs_and_two_mixed_DMA_states': True,
        'specific_reveal_comparison_resolved_without_ROM_change': True,
        'release_hashes_exact18_plaques_open22_requirements_retained': True,
        'verifier_sha256': sha(Path(__file__).read_bytes()), 'full_goal_complete': False})
    print(f"V675 final: {len(archive['files'])} archive files exact; reveal comparison resolved; full scope retained.", flush=True)


if __name__ == '__main__':
    main()
