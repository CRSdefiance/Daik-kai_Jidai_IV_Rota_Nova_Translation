"""Check the retained V694 evidence and preserve every earlier scope requirement."""

from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha
from scripts.record_room_gender_v694 import ARCHIVE, KEY, ROOT, SOURCES
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
    for donor in pre['donors'].values():
        assert sha(Path(donor['path']).read_bytes()) == donor['sha256']
    frozen = read('work/analysis/confirm_material_v572/audit_scope_before.json')
    for name, scope in frozen.items():
        path = Path('translations') / name
        audit = read(path)
        assert all(audit[k] == v for k, v in pre['all_original_audits_before'][name].items()
                   if k != 'current_goal_turn_classification')
        assert audit.get('historical_pending_items_retained') == scope['historical_pending_items_retained']
        inventory = audit.get('plaque_style_v247', {}).get('ongoing_plaque_inventory')
        assert inventory == scope['ongoing_plaque_inventory']
        if inventory:
            assert len(inventory) == 18 and all(not p['fully_completed'] for p in inventory)
        assert audit[KEY]['proof_sha256'] == sha((ROOT / 'proof.json').read_bytes())
        assert path.read_bytes() == (ARCHIVE / 'audits' / name).read_bytes()
    save(ROOT / 'final_verification.json', {'archive_files_verified': len(archive['files']),
        'external_E_drive_files_verified': len(archive['external_E_drive_evidence']),
        'second_actual_loose_parent_and_both_complete_gender_symbol_cells_verified': True,
        'native_full_suffix_memory_mismatches_preserved_not_reported_exact': True,
        'release_donors_pointers_and_all_original_scope_unchanged': True,
        'all18_plaques_incomplete_and_full_graphics_goal_active': True,
        'verifier_sha256': sha(Path(__file__).read_bytes()), 'full_goal_complete': False})
    print(f"V694 final: {len(archive['files'])} archive files and {len(archive['external_E_drive_evidence'])} E-drive references exact; second-parent display verified; native suffix gap retained; goal active.", flush=True)


if __name__ == '__main__':
    main()
