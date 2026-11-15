"""Verify the corrected evidence record and unchanged full graphics scope."""

from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha
from scripts.prepare_maria_opening_v674 import ROOT
from scripts.record_maria_dispatch_v674 import ARCHIVE, KEY, SCRIPTS
from scripts.verify_village_wrap_v608 import read, save


def main():
    pre, archive = read(ROOT / 'preflight.json'), read(ARCHIVE / 'provenance.json')
    pp, proof = ROOT / 'proof.json', read(ROOT / 'proof.json')
    assert proof['verifier_sha256'] == sha(Path('scripts/verify_maria_dispatch_v674.py').read_bytes())
    assert archive['source_scripts'] == {p: sha(Path(p).read_bytes()) for p in SCRIPTS}
    for path, digest in pre['release_hashes'].items():
        assert sha(Path(path).read_bytes()) == digest
    for path, digest in archive['files'].items():
        assert sha((ARCHIVE / path).read_bytes()) == digest, path
    assert proof['initial_Maria_M26_mapping_retracted_not_used_as_evidence']
    assert proof['separate_incomplete_reveal_transition']['original_reveal_painter_and_timing_not_yet_proven']
    frozen = read('work/analysis/confirm_material_v572/audit_scope_before.json')
    for name, scope in frozen.items():
        path = Path('translations') / name
        data = read(path)
        assert data.get('historical_pending_items_retained') == scope['historical_pending_items_retained']
        assert data.get('plaque_style_v247', {}).get('ongoing_plaque_inventory') == scope['ongoing_plaque_inventory']
        assert all(data[k] == v for k, v in pre['all_original_audits_before'][name].items()
                   if k != 'current_goal_turn_classification')
        assert data[KEY]['proof_sha256'] == sha(pp.read_bytes())
        assert path.read_bytes() == (ARCHIVE / 'audits' / name).read_bytes()
    save(ROOT / 'final_verification.json', {'archive_files_verified': len(archive['files']),
        'three_runs_terminal14_baseline11_pilot_states_and_two_stable_courts': True,
        'incorrect_movie_assignment_retracted_reveal_painter_still_open': True,
        'release_hashes_exact18_plaques_open22_requirements_retained': True,
        'verifier_sha256': sha(Path(__file__).read_bytes()), 'full_goal_complete': False})
    print(f"V674 final: {len(archive['files'])} archive files exact; corrected mapping/reveal gap explicit;18/22 scopes unchanged.")


if __name__ == '__main__':
    main()
