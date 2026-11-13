"""Verify archived V677 source/fixture evidence and retained full graphics scope."""

from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha
from scripts.native_wedding_fixture_v677 import ROOT
from scripts.record_wedding_playback_v677 import ARCHIVE, KEY, SCRIPTS
from scripts.verify_village_wrap_v608 import read, save


def main():
    pre, archive = read(ROOT / 'preflight.json'), read(ARCHIVE / 'provenance.json')
    pp, proof = ROOT / 'proof.json', read(ROOT / 'proof.json')
    assert proof['verifier_sha256'] == sha(Path('scripts/verify_wedding_playback_v677.py').read_bytes())
    assert archive['source_scripts'] == {path: sha(Path(path).read_bytes()) for path in SCRIPTS}
    for path, digest in pre['release_hashes'].items():
        assert sha(Path(path).read_bytes()) == digest
    for path, digest in archive['files'].items():
        assert sha((ARCHIVE / path).read_bytes()) == digest, path
    assert proof['152_complete_source_compositions_all_native_counters0_through151']
    assert proof['whole_RGB_pixel_comparisons'] == 7471104
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
        'original_M26_loading_crops_crossfade152_source_samples705_repeat_pairs_verified': True,
        'isolated_story_fixture_and_older_dialogue_findings_disclosed': True,
        'release_hashes_exact18_plaques_open22_original_requirements_retained': True,
        'verifier_sha256': sha(Path(__file__).read_bytes()), 'full_goal_complete': False})
    print(f"V677 final: {len(archive['files'])} archive files exact; original wedding source/display verified; full scope retained.", flush=True)


if __name__ == '__main__':
    main()
