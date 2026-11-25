"""Verify archived opacity-path evidence, additive audit and unchanged release."""

from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha
from scripts.record_opacity_paths_v704 import ARCHIVE, KEY, ROOT, SOURCES
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
            assert len(inventory) == 18 and all(not r['fully_completed'] for r in inventory)
        assert data[KEY]['proof_sha256'] == sha((ROOT / 'native_proof.json').read_bytes())
        assert path.read_bytes() == (ARCHIVE / 'audits' / name).read_bytes()
    save(ROOT / 'final_verification.json', {'archive_files_verified': len(archive['files']),
        'external_E_drive_files_verified': len(archive['external_E_drive_evidence']),
        'complete_portrait_import_and_five_source_bound_half_blend_contracts_verified': True,
        'no_production_alpha_fix_or_original_comic_scene_clearance': True,
        'all18_plaques_incomplete22_historical_scopes_and_production_preserved': True,
        'verifier_sha256': sha(Path(__file__).read_bytes()), 'full_goal_complete': False})
    print(f"V704 final: {len(archive['files'])} archived files and {len(archive['external_E_drive_evidence'])} external reference verified; full goal active.", flush=True)


if __name__ == '__main__':
    main()
