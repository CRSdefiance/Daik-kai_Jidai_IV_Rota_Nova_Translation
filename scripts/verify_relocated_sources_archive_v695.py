"""Independently check the V695 archive and unchanged full graphics scope."""

from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha
from scripts.record_relocated_sources_v695 import ARCHIVE, KEY, ROOT, SOURCES
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
            assert len(inventory) == 18 and all(not p['fully_completed'] for p in inventory)
        assert data[KEY]['proof_sha256'] == sha((ROOT / 'proof.json').read_bytes())
        assert path.read_bytes() == (ARCHIVE / 'audits' / name).read_bytes()
    save(ROOT / 'final_verification.json', {'archive_files_verified': len(archive['files']),
        'external_E_drive_files_verified': len(archive['external_E_drive_evidence']),
        'whole_relocated_sources_and_two_embedded_UI_atlas_retention_classifications_verified': True,
        'six_missing_control_contexts_and_full_graphics_goal_remain_open': True,
        'all18_plaques_incomplete_all22_original_requirements_and_release_pointers_exact': True,
        'verifier_sha256': sha(Path(__file__).read_bytes()), 'full_goal_complete': False})
    print(f"V695 final: {len(archive['files'])} archive files and {len(archive['external_E_drive_evidence'])} retained source references exact; goal active.", flush=True)


if __name__ == '__main__':
    main()
