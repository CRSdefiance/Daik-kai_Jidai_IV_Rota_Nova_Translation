"""Save the verified research checkpoint without promoting a playable release."""

import json
from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha
from scripts.prepare_reviewed_names_v297 import DIGEST, ROM, ROOT


def read(path):
    return json.loads(Path(path).read_text(encoding='utf-8'))


def main():
    prep = read(ROOT / 'preparation.json')
    plan = read(ROOT / 'catalog_plan.json')
    lookup = read(ROOT / 'native_lookup_proof.json')
    fixed = read(ROOT / 'fixed_transform_proof.json')
    native = read(ROOT / 'full_native_proof.json')
    assert sha(ROM.read_bytes()) == DIGEST
    assert native['all444_complete_body_glyphs_pass'] and not native['failures']
    assert fixed['original_native_actors_checked'] == 19254
    assert len(lookup['all_key_four_alignment_three_caller_cases']) == 5604
    assert len(native['native_full_catalog_copies']) == 5604
    checkpoint = {
        'documentation': 'docs/reviewed_name_integration_v297.md',
        'latest_playable_unchanged': str(ROM), 'latest_playable_sha256': DIGEST,
        'source_reviewed_and_compiled_records': len(prep['records']),
        'fixed_records': prep['fixed_records'], 'catalog_records': prep['catalog_records'],
        'complete_catalog_keys': plan['unique_route_scoped_keys'],
        'owned_payload_bytes': plan['pool_payload_bytes'],
        'remaining_before_stage': plan['remaining_before_stage'],
        'all_full_strings_first_final_letters_and_NUL_retained': True,
        'all_original_native_actor_fields_preserved': fixed['original_native_actors_checked'],
        'all_fixed_archive_block_and_command_addresses_preserved': True,
        'route_segments_scanned': plan['route_segments_scanned'],
        'unintended_active_catalog_matches': len(plan['unintended_matches']),
        'foreign_route_matches_rejected': len(plan['foreign_route_matches_rejected']),
        'native_aligned_caller_lookup_cases': 5604,
        'native_route_mask_cases': len(lookup['all_key_four_route_mask_cases']),
        'native_fallback_and_near_miss_cases': lookup['foreign_caller_invalid_route_and_exact_NUL_near_miss_cases'],
        'native_complete_catalog_copy_cases': len(native['native_full_catalog_copies']),
        'complete_native_macro_and_glyph_bodies': len(native['cases']),
        'native_failures': len(native['failures']), 'native_function_bridges': [],
        'controlled_current_code_with_prior_captured_route_data': True,
        'new_gameplay_run_claimed': False,
        'Maria_capture_test_selection_not_legitimate_unlock': True,
        'native_preview_sheets': len(native['sheets']),
        'sheets_inspected_this_checkpoint': [0, 30, 55],
        'full_new_sheet_visual_review_pending': True,
        'full_registered_route_COMMON_HELP_art_integration_pending': True,
        'all18_plaque_hint_entries_and_variants_incomplete': True,
        'low_resolution_Online_translation_exemption_preserved': True,
        'playable_ROM_modified': False, 'full_goal_complete': False,
        'evidence_sha256': {str(ROOT / name): sha((ROOT / name).read_bytes()) for name in
                            ('preparation.json', 'catalog_plan.json', 'native_lookup_proof.json',
                             'fixed_transform_proof.json', 'full_native_proof.json')},
    }
    for filename in ('graphics_completion_campaign_v1.json', 'graphics_visual_audit_v150.json'):
        path = Path('translations') / filename
        data = read(path)
        assert not data['user_scope_exceptions']['low_resolution_online_images']['translation_required']
        plaques = data['plaque_style_v247']['ongoing_plaque_inventory']
        assert len(plaques) == 18 and all(not p['fully_completed'] for p in plaques)
        data['reviewed_name_integration_v297'] = checkpoint
        data['latest_candidate'] = str(ROM)
        data['latest_candidate_sha256'] = DIGEST
        path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    section = '''## V297 research: complete reviewed naming packet passes native checks

All 444 reviewed paragraphs compile without shortening: 197 fixed allocations
and 247 full catalog records, using 467 route-scoped keys. All 19,254 original
speaker fields and fixed command addresses remain intact. 5,604 lookup cases,
1,868 route checks, 1,401 fallbacks/near misses, 5,604 native expanded copies and
444 complete native glyph bodies pass with zero failures. The 119,520-byte owned
payload leaves 9,472 bytes before staging. These are controlled current-code
tests using prior captured route data, not new gameplay runs. Full release,
COMMON/HELP/artwork integration, full new-sheet visual review and all 18 plaque
audits remain open. Low-resolution Online images remain exempt. V296 stays the
latest playable candidate. See [V297 evidence](reviewed_name_integration_v297.md).

'''
    for filename in ('translation_progress.md', 'known_issues.md', 'todo.md'):
        path = Path('docs') / filename
        text = path.read_text(encoding='utf-8')
        if '## V297 research:' not in text:
            title, rest = text.split('\n\n', 1)
            path.write_text(title + '\n\n' + section + rest, encoding='utf-8')
    print('V297 native research recorded; V296 remains latest playable; Online exemption and all18 open plaques preserved.')


if __name__ == '__main__':
    main()
