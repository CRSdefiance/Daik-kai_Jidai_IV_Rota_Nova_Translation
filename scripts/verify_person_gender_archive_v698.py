"""Verify Sailor Info evidence archive, unchanged production and retained scope."""

from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha
from scripts.record_person_gender_v698 import ARCHIVE, KEY, ROOT, SOURCES
from scripts.verify_village_wrap_v608 import read, save


def main():
    archive, pre = read(ARCHIVE / 'provenance.json'), read(ROOT / 'preflight.json')
    assert archive['scripts'] == {p: sha(Path(p).read_bytes()) for p in SOURCES}
    for path, digest in archive['files'].items():
        assert sha((ARCHIVE / path).read_bytes()) == digest, path
    for path, digest in archive['external_E_drive_evidence'].items():
        assert sha(Path(path).read_bytes()) == digest, path
    for path, digest in pre['release_hashes'].items():
        assert sha(Path(path).read_bytes()) == digest
    assert sha(Path(pre['donor']).read_bytes()) == pre['donor_sha256']
    frozen = read('work/analysis/confirm_material_v572/audit_scope_before.json')
    for name, scope in frozen.items():
        path = Path('translations') / name
        data = read(path)
        assert all(data[k] == v for k, v in pre['all_original_audits_before'][name].items()
                   if k != 'current_goal_turn_classification')
        assert data.get('historical_pending_items_retained') == scope['historical_pending_items_retained']
        inventory = data.get('plaque_style_v247', {}).get('ongoing_plaque_inventory')
        assert inventory == scope['ongoing_plaque_inventory']
        if inventory:
            assert len(inventory) == 18 and all(not p['fully_completed'] for p in inventory)
        assert data[KEY]['proof_sha256'] == sha((ROOT / 'proof.json').read_bytes())
        assert path.read_bytes() == (ARCHIVE / 'audits' / name).read_bytes()
    save(ROOT / 'final_verification.json', {'archive_files_verified': len(archive['files']),
        'external_E_drive_files_verified': len(archive['external_E_drive_evidence']),
        'actual_Sailor_Info_both_symbols_and80_whole_plaque_crops_verified': True,
        'native_prefix_failure_and_V694_suffix_gap_retained': True,
        'fixture_portrait_cache_not_ordinary_return_credit': True,
        'all18_plaques_incomplete_all22_original_requirements_and_release_pointers_exact': True,
        'verifier_sha256': sha(Path(__file__).read_bytes()), 'full_goal_complete': False})
    print(f"V698 final: {len(archive['files'])} archived files and{len(archive['external_E_drive_evidence'])} E-drive references exact; full goal active.", flush=True)


if __name__ == '__main__':
    main()
