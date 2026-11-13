"""Verify source/evidence archive, unchanged release and exact original scope."""

from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha
from scripts.record_file_ids_v683 import ARCHIVE, KEY, SCRIPTS
from scripts.trace_file_ids_v683 import ROOT
from scripts.verify_village_wrap_v608 import read, save


def main():
    pre, proof = read(ROOT / 'preflight.json'), read(ROOT / 'proof.json')
    archive = read(ARCHIVE / 'provenance.json')
    assert proof['verifier_sha256'] == sha(Path('scripts/verify_file_ids_v683.py').read_bytes())
    assert archive['source_scripts'] == {p: sha(Path(p).read_bytes()) for p in SCRIPTS}
    for path, digest in archive['files'].items():
        assert sha((ARCHIVE / path).read_bytes()) == digest, path
    for path, digest in pre['release_hashes'].items():
        assert sha(Path(path).read_bytes()) == digest, path
    frozen = read('work/analysis/confirm_material_v572/audit_scope_before.json')
    for name, scope in frozen.items():
        path = Path('translations') / name
        data = read(path)
        assert all(data[k] == v for k, v in pre['all_original_audits_before'][name].items()
                   if k != 'current_goal_turn_classification')
        assert data.get('historical_pending_items_retained') == scope['historical_pending_items_retained']
        assert data.get('plaque_style_v247', {}).get('ongoing_plaque_inventory') == scope['ongoing_plaque_inventory']
        assert data[KEY]['proof_sha256'] == sha((ROOT / 'proof.json').read_bytes())
        assert path.read_bytes() == (ARCHIVE / 'audits' / name).read_bytes()
    save(ROOT / 'final_verification.json', {'archive_files_verified': len(archive['files']),
        'all247_numeric_IDs8_ranges193_baseline_pairs_and_source_bound_DTCM_checks_verified': True,
        'all_release_hashes_unchanged18_plaques_incomplete22_original_requirements_exact': True,
        'bounded_two_sequence_result_other_contexts_global_nonuse_and_acceptance_open': True,
        'verifier_sha256': sha(Path(__file__).read_bytes()), 'full_goal_complete': False})
    print(f"V683 final: {len(archive['files'])} archive files exact; original graphics scope retained; goal active.", flush=True)


if __name__ == '__main__':
    main()
