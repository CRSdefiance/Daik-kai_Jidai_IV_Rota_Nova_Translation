"""Verify V676 archive, unchanged release hashes and retained full graphics scope."""

from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha
from scripts.record_wedding_source_v676 import ARCHIVE, KEY, SCRIPTS
from scripts.research_wedding_command_v676 import ROOT
from scripts.verify_village_wrap_v608 import read, save


def main():
    pre, archive = read(ROOT / 'preflight.json'), read(ARCHIVE / 'provenance.json')
    pp, proof = ROOT / 'proof.json', read(ROOT / 'proof.json')
    assert proof['verifier_sha256'] == sha(Path('scripts/verify_wedding_source_v676.py').read_bytes())
    assert archive['source_scripts'] == {path: sha(Path(path).read_bytes()) for path in SCRIPTS}
    for path, digest in pre['release_hashes'].items():
        assert sha(Path(path).read_bytes()) == digest
    for path, digest in archive['files'].items():
        assert sha((ARCHIVE / path).read_bytes()) == digest, path
    assert proof['M26_Lil_chapter70_source_consumer_identified_actual_wedding_playback_still_open']
    frozen = read('work/analysis/confirm_material_v572/audit_scope_before.json')
    for name, scope in frozen.items():
        path = Path('translations') / name
        data = read(path)
        assert data.get('historical_pending_items_retained') == scope['historical_pending_items_retained']
        assert data.get('plaque_style_v247', {}).get('ongoing_plaque_inventory') == scope['ongoing_plaque_inventory']
        assert all(data[key] == value for key, value in pre['all_original_audits_before'][name].items()
                   if key != 'current_goal_turn_classification')
        assert data[KEY]['proof_sha256'] == sha(pp.read_bytes())
        assert path.read_bytes() == (ARCHIVE / 'audits' / name).read_bytes()
    save(ROOT / 'final_verification.json', {'archive_files_verified': len(archive['files']),
        'original_Lil_wedding_source_command_and_ordinary_loader_selector_control_verified': True,
        'actual_M26_wedding_playback_still_open': True,
        'release_hashes_exact18_plaques_open22_original_requirements_retained': True,
        'verifier_sha256': sha(Path(__file__).read_bytes()), 'full_goal_complete': False})
    print(f"V676 final: {len(archive['files'])} archive files exact; wedding source identified; playback gate retained.", flush=True)


if __name__ == '__main__':
    main()
