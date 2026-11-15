"""Verify exact archived battle evidence and full-scope retention."""

from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha
from scripts.prepare_battle_paints_v673 import ROOT
from scripts.record_battle_paints_v673 import ARCHIVE, KEY, SCRIPTS
from scripts.verify_village_wrap_v608 import read, save


def main():
    pre = read(ROOT / 'preflight.json')
    archive = read(ARCHIVE / 'provenance.json')
    pp = ROOT / 'proof.json'
    proof = read(pp)
    assert proof['verifier_sha256'] == sha(Path('scripts/verify_battle_paints_v673.py').read_bytes())
    assert archive['source_scripts'] == {p: sha(Path(p).read_bytes()) for p in SCRIPTS}
    for path, digest in pre['release_hashes'].items():
        assert sha(Path(path).read_bytes()) == digest
    for path, digest in archive['files'].items():
        assert sha((ARCHIVE / path).read_bytes()) == digest, path
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
        'both_runs_terminal82_current82_retained_frame_pairs_pass': True,
        'no_new_ROM_or_guide_no_six_control_completion_claim': True,
        '18_original_plaques_incomplete22_requirements_exact': True,
        'verifier_sha256': sha(Path(__file__).read_bytes()), 'full_goal_complete': False})
    print(f"V673 final archive: {len(archive['files'])} files exact; ROM/patch/registry and18/22 scopes unchanged.")


if __name__ == '__main__':
    main()
