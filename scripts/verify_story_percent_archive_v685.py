"""Final independent archive hashes, release identity and all original scope."""

from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha
from scripts.prepare_story_percent_v685 import ROOT
from scripts.record_story_percent_v685 import ARCHIVE, KEY, POINTER, SOURCES
from scripts.verify_story_percent_v685 import ROM
from scripts.verify_village_wrap_v608 import read, save


def main():
    pre, proof = read(ROOT / 'preflight.json'), read(ROOT / 'proof.json')
    archive = read(ARCHIVE / 'provenance.json')
    assert archive['source_files'] == {p: sha(Path(p).read_bytes()) for p in SOURCES}
    for path, digest in archive['files'].items():
        assert sha((ARCHIVE / path).read_bytes()) == digest, path
    assert proof['candidate_sha256'] == sha(ROM.read_bytes())
    assert proof['manifest_sha256'] == sha(ROM.with_suffix('.manifest.json').read_bytes())
    assert proof['patch_sha256'] == sha(ROM.with_suffix('.xdelta').read_bytes())
    assert proof['registry_sha256'] == sha(Path('translations/release_stack.json').read_bytes())
    assert sha(Path(pre['canonical_baseline']['path']).read_bytes()) == pre['canonical_baseline']['sha256']
    assert proof['verifier_sha256'] == sha(Path('scripts/finish_story_percent_v685.py').read_bytes())
    frozen = read('work/analysis/confirm_material_v572/audit_scope_before.json')
    for name, scope in frozen.items():
        path = Path('translations') / name
        data = read(path)
        assert all(data[k] == v for k, v in pre['all_original_audits_before'][name].items()
                   if k not in ('current_goal_turn_classification', POINTER))
        old_pointer = pre['all_original_audits_before'][name][POINTER]
        assert {k: v for k, v in data[POINTER].items() if k not in ('candidate', 'sha256', 'profile')} == {
            k: v for k, v in old_pointer.items() if k not in ('candidate', 'sha256', 'profile')}
        assert data[POINTER]['sha256'] == proof['candidate_sha256']
        assert data.get('historical_pending_items_retained') == scope['historical_pending_items_retained']
        assert data.get('plaque_style_v247', {}).get('ongoing_plaque_inventory') == scope['ongoing_plaque_inventory']
        assert data[KEY]['proof_sha256'] == sha((ROOT / 'proof.json').read_bytes())
        assert path.read_bytes() == (ARCHIVE / 'audits' / name).read_bytes()
    save(ROOT / 'final_verification.json', {'archive_files_verified': len(archive['files']),
        'candidate_sha256': proof['candidate_sha256'], 'four_repairs_native_actual_scene_and_format_gate_verified': True,
        'canonical_V610_pointers18_incomplete_plaques22_original_scopes_and_prior_evidence_preserved': True,
        'latest_experimental_pointer_V685_only': True,
        'source_older_wording_blank_hold_and_other_graphics_contexts_remain_open': True,
        'verifier_sha256': sha(Path(__file__).read_bytes()), 'full_goal_complete': False})
    print(f"V685 final: {len(archive['files'])} archived files exact; four defects repaired; graphics goal active.", flush=True)


if __name__ == '__main__':
    main()
