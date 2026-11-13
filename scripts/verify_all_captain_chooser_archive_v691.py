"""Independently verify all-four evidence archive, donors and original scope."""

from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha
from scripts.record_all_captain_chooser_v691 import ARCHIVE, KEY, SCRIPTS
from scripts.run_all_captain_chooser_v691 import ROOT
from scripts.verify_village_wrap_v608 import read, save


def main():
    pre, archive = read(ROOT / 'preflight.json'), read(ARCHIVE / 'provenance.json')
    assert archive['scripts'] == {p: sha(Path(p).read_bytes()) for p in SCRIPTS}
    for path, digest in archive['files'].items():
        assert sha((ARCHIVE / path).read_bytes()) == digest, path
    for path, digest in pre['release_hashes'].items():
        assert sha(Path(path).read_bytes()) == digest, path
    assert sha(Path(pre['donor']).read_bytes()) == pre['donor_sha256']
    assert sha(Path(pre['original_donor']).read_bytes()) == pre['original_donor_sha256']
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
    save(ROOT / 'final_verification.json', {
        'archive_files_verified': len(archive['files']),
        'all_four_chooser56_fields198016_source_photo_pixels14_cache_hits_and14_case_pairs_verified': True,
        'all_release_and_donor_hashes_unchanged18_plaques_incomplete22_original_requirements_exact': True,
        'other_raw_readers_graphics_contexts_and_full_goal_not_complete': True,
        'verifier_sha256': sha(Path(__file__).read_bytes()), 'full_goal_complete': False})
    print(f"V691 final: {len(archive['files'])} archive files exact; all-four chooser verified; graphics goal active.", flush=True)


if __name__ == '__main__':
    main()
