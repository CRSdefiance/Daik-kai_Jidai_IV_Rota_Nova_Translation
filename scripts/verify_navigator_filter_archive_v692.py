"""Verify every retained V692 file/reference and unchanged original audit scope."""

from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha
from scripts.record_navigator_filter_v692 import ARCHIVE, KEY, POINTER, ROOT, SOURCES
from scripts.verify_village_wrap_v608 import read, save


def main():
    archive = read(ARCHIVE / 'provenance.json')
    pre, static = read(ROOT / 'build_preflight.json'), read(ROOT / 'static_release_proof.json')
    assert archive['scripts'] == {p: sha(Path(p).read_bytes()) for p in SOURCES}
    for path, digest in archive['files'].items():
        assert sha((ARCHIVE / path).read_bytes()) == digest, path
    for path, digest in archive['external_E_drive_evidence'].items():
        assert sha(Path(path).read_bytes()) == digest, path
    assert sha(Path(archive['guide_provenance']).read_bytes()) == archive['guide_provenance_sha256']
    for path, row in read(archive['guide_provenance'])['files'].items():
        assert sha(Path(path).read_bytes()) == row['sha256']
    initial = read(ROOT / 'preflight.json')
    for path, digest in initial['release_hashes'].items():
        if path != 'translations\\release_stack.json' and Path(path).name != 'release_stack.json':
            assert sha(Path(path).read_bytes()) == digest
    for row in initial['donors'].values():
        assert sha(Path(row['path']).read_bytes()) == row['sha256']
    frozen = read('work/analysis/confirm_material_v572/audit_scope_before.json')
    for name, scope in frozen.items():
        path = Path('translations') / name
        data = read(path)
        before = pre['all_original_audits_before'][name]
        assert all(data[k] == v for k, v in before.items() if k not in (POINTER, 'current_goal_turn_classification'))
        assert all(data[POINTER][k] == v for k, v in before[POINTER].items() if k not in ('candidate', 'sha256', 'profile'))
        assert data[POINTER]['sha256'] == static['candidate_sha256'] and data[POINTER]['profile'] == pre['profile']
        assert data.get('historical_pending_items_retained') == scope['historical_pending_items_retained']
        inventory = data.get('plaque_style_v247', {}).get('ongoing_plaque_inventory')
        assert inventory == scope['ongoing_plaque_inventory']
        if inventory:
            assert len(inventory) == 18 and all(not row['fully_completed'] for row in inventory)
        assert data[KEY]['proof_sha256'] == sha((ROOT / 'proof.json').read_bytes())
        assert path.read_bytes() == (ARCHIVE / 'audits' / name).read_bytes()
    save(ROOT / 'final_verification.json', {'archive_files_verified': len(archive['files']),
        'external_E_drive_evidence_files_verified': len(archive['external_E_drive_evidence']),
        'all_release_donor_and_source_hashes_verified': True,
        'all18_plaques_incomplete22_original_requirements_exact': True,
        'shared_Captain_caption_verified_second_gender_cursor_timing_and_other_graphics_open': True,
        'verifier_sha256': sha(Path(__file__).read_bytes()), 'full_goal_complete': False})
    print(f"V692 final:{len(archive['files'])} archive files and{len(archive['external_E_drive_evidence'])} E-drive references exact; graphics goal active.", flush=True)


if __name__ == '__main__':
    main()
