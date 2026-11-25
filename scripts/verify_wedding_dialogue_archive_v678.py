"""Final artifact hashes and unchanged historical scope for V678."""

from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha
from scripts.prepare_wedding_dialogue_v678 import ROOT
from scripts.record_wedding_dialogue_v678 import ARCHIVE, KEY, SCRIPTS
from scripts.verify_village_wrap_v608 import read, save
from scripts.verify_wedding_dialogue_v678 import ROM


def main():
    archive, proof = read(ARCHIVE / 'provenance.json'), read(ROOT / 'proof.json')
    pre = read(ROOT / 'preflight.json')
    assert archive['source_scripts'] == {p: sha(Path(p).read_bytes()) for p in SCRIPTS}
    for path, digest in archive['files'].items():
        assert sha((ARCHIVE / path).read_bytes()) == digest, path
    for path, digest in pre['source_release_hashes'].items():
        if Path(path) != Path('translations/release_stack.json'):
            assert sha(Path(path).read_bytes()) == digest, path
    assert sha(ROM.read_bytes()) == proof['candidate_sha256']
    assert sha(ROM.with_suffix('.xdelta').read_bytes()) == proof['patch_sha256']
    assert sha(ROM.with_suffix('.manifest.json').read_bytes()) == proof['manifest_sha256']
    assert sha(Path('translations/release_stack.json').read_bytes()) == proof['registry_sha256']
    allowed = {'current_goal_turn_classification', 'latest_compiled_experimental_candidate_with_inherited_native_gap'}
    frozen = read('work/analysis/confirm_material_v572/audit_scope_before.json')
    for name, scope in frozen.items():
        path = Path('translations') / name
        data = read(path)
        assert all(data[k] == v for k, v in pre['all_original_audits_before'][name].items() if k not in allowed)
        assert data.get('historical_pending_items_retained') == scope['historical_pending_items_retained']
        assert data.get('plaque_style_v247', {}).get('ongoing_plaque_inventory') == scope['ongoing_plaque_inventory']
        assert data[KEY]['proof_sha256'] == sha((ROOT / 'proof.json').read_bytes())
        assert path.read_bytes() == (ARCHIVE / 'audits' / name).read_bytes()
        assert data['latest_compiled_experimental_candidate_with_inherited_native_gap']['sha256'] == proof['candidate_sha256']
    save(ROOT / 'final_verification.json', {
        'archive_files_verified': len(archive['files']),
        'two_source_faithful_dialogue_repairs_complete_tested_combined_ROM_and_exact_patch': True,
        'all18_plaques_incomplete22_original_requirements_and_older_evidence_retained': True,
        'canonical_and_prior_release_hashes_unchanged': True,
        'verifier_sha256': sha(Path(__file__).read_bytes()), 'full_goal_complete': False})
    print(f"V678 final: {len(archive['files'])} archived files exact; complete two-record repair,full graphics goal still active.", flush=True)


if __name__ == '__main__':
    main()
