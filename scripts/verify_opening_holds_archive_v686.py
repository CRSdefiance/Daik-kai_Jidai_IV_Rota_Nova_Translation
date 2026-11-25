"""Independently verify retained wait evidence, release hashes and original scope."""

from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha
from scripts.record_opening_holds_v686 import ARCHIVE, KEY, SCRIPTS
from scripts.run_opening_holds_v686 import ROOT
from scripts.verify_village_wrap_v608 import read, save


def main():
    pre = read(ROOT / 'preflight.json')
    archive = read(ARCHIVE / 'provenance.json')
    actual = read(ROOT / 'actual_wait_proof.json')
    assert archive['source_scripts'] == {p: sha(Path(p).read_bytes()) for p in SCRIPTS}
    assert actual['verifier_sha256'] == sha(Path('scripts/verify_actual_waits_v686.py').read_bytes())
    for path, digest in archive['files'].items():
        assert sha((ARCHIVE / path).read_bytes()) == digest, path
    for path, digest in pre['release_hashes'].items():
        assert sha(Path(path).read_bytes()) == digest, path
    assert sha(Path(pre['clean']).read_bytes()) == pre['clean_sha256']
    assert sha(Path(pre['donor']).read_bytes()) == pre['donor_sha256']
    frozen = read('work/analysis/confirm_material_v572/audit_scope_before.json')
    for name, scope in frozen.items():
        path = Path('translations') / name
        data = read(path)
        assert all(data[k] == v for k, v in pre['all_original_audits_before'][name].items()
                   if k != 'current_goal_turn_classification')
        assert data.get('historical_pending_items_retained') == scope['historical_pending_items_retained']
        assert data.get('plaque_style_v247', {}).get('ongoing_plaque_inventory') == scope['ongoing_plaque_inventory']
        assert data[KEY]['actual_proof_sha256'] == sha((ROOT / 'actual_wait_proof.json').read_bytes())
        assert path.read_bytes() == (ARCHIVE / 'audits' / name).read_bytes()
    save(ROOT / 'final_verification.json', {
        'archive_files_verified': len(archive['files']),
        'three_source_script_waits24_complete_baseline_pairs_actual_entry_return_proof_verified': True,
        'ROM_patch_registry_canonical_and_release_pointers_unchanged': True,
        'all18_plaques_incomplete22_historical_requirements_exact': True,
        'verifier_sha256': sha(Path(__file__).read_bytes()), 'full_goal_complete': False})
    print(f"V686 final: {len(archive['files'])} archive files exact; three original waits resolved; graphics goal active.", flush=True)


if __name__ == '__main__':
    main()
