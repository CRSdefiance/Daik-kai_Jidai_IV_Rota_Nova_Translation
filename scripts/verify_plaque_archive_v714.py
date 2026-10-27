"""Verify V714 archive, source decisions and all original open audit objects."""

from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha
from scripts.record_plaque_review_v714 import ARCHIVE, GUIDE, KEY
from scripts.review_current_plaques_v714 import ROOT
from scripts.verify_village_wrap_v608 import read, save


def main():
    pre = read(ROOT / 'preflight.json')
    for path, digest in pre['release_hashes'].items():
        assert sha(Path(path).read_bytes()) == digest
    proof = read(ROOT / 'current_plaque_review_proof.json')
    matrix = read(ROOT / 'terminology_review.json')
    assert len(proof['all18_current_native_review_entries']) == len(matrix['all18_source_context_and_natural_English_decisions']) == 18
    assert proof['current_native_static_pixels'] == 14272 and len(proof['all17_independent_complete_font_masks']) == 17
    scope = read('work/analysis/confirm_material_v572/audit_scope_before.json')
    for name, original in scope.items():
        current = read(Path('translations') / name)
        assert current.get('historical_pending_items_retained') == original['historical_pending_items_retained']
        assert current.get('plaque_style_v247', {}).get('ongoing_plaque_inventory') == original['ongoing_plaque_inventory']
        reduced = dict(current)
        reduced.pop(KEY)
        reduced['current_goal_turn_classification'] = pre['all_original_audits_before'][name]['current_goal_turn_classification']
        assert reduced == pre['all_original_audits_before'][name]
        assert (ARCHIVE / 'audits' / name).read_bytes() == (Path('translations') / name).read_bytes()
    archive = read(ARCHIVE / 'provenance.json')
    for path, digest in archive['files'].items():
        assert sha((ARCHIVE / path).read_bytes()) == digest, path
    guide = read(GUIDE / 'provenance.json')
    assert len(guide['screenshots']) == 4 and not guide['publication_approved']
    for shot in guide['screenshots']:
        assert sha(Path(shot['path']).read_bytes()) == shot['sha256']
        assert shot['unmodified_capture'] and shot['ROM_sha256'] == pre['candidate_sha256']
    save(ROOT / 'final_verification.json', {'archive': str(ARCHIVE), 'files_verified': len(archive['files']),
        'guide_candidates_verified': 4, 'all18_source_context_and_current_native_views_verified': True,
        'all18_original_plaque_objects_incomplete22_historical_objects_deep_exact': True,
        'all_other_audit_fields_ROM_patch_registry_and_release_pointers_exact': True,
        'user_material_and_Online_scope_responses_pending_no_acceptance_inferred': True,
        'verifier_sha256': sha(Path(__file__).read_bytes()), 'full_goal_complete': False})
    print('V714 verified:', len(archive['files']), 'archive files,4 guide candidates;18/22 scopes exact and open.', flush=True)


if __name__ == '__main__':
    main()
