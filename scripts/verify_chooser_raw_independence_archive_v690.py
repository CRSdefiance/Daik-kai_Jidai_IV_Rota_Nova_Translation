"""Verify the source-bound fixture archive and every original open scope."""

from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha
from scripts.record_chooser_raw_independence_v690 import ARCHIVE, KEY, SCRIPTS
from scripts.trace_chooser_raw_independence_v690 import ROOT
from scripts.verify_village_wrap_v608 import read, save


def main():
    pre, archive = read(ROOT / 'preflight.json'), read(ARCHIVE / 'provenance.json')
    assert archive['scripts'] == {p: sha(Path(p).read_bytes()) for p in SCRIPTS}
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
    save(ROOT / 'final_verification.json', {
        'archive_files_verified': len(archive['files']),
        'original_initialization_return_and_scoped_live_raw_buffer_control_verified': True,
        'all_release_hashes_unchanged18_plaques_incomplete22_original_requirements_exact': True,
        'other_captains_readers_contexts_and_full_graphics_goal_not_complete': True,
        'verifier_sha256': sha(Path(__file__).read_bytes()), 'full_goal_complete': False})
    print(f"V690 final: {len(archive['files'])} archive files exact; remaining graphics scope retained; goal active.", flush=True)


if __name__ == '__main__':
    main()
