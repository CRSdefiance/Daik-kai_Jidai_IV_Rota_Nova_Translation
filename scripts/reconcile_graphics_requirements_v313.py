"""Keep original requirements while separating current evidence from old backlog."""

import json
from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.audit_current_graphics_v313 import ROM, ROOT


def read(path):
    return json.loads(Path(path).read_text(encoding='utf-8'))


def main():
    campaign = read('translations/graphics_completion_campaign_v1.json')
    preservation = read(ROOT / 'preservation_proof.json')
    manifest = read(ROM.with_suffix('.manifest.json'))
    digest = sha(ROM.read_bytes())
    assert campaign['latest_candidate_sha256'] == preservation['candidate_sha256'] == manifest['candidate_sha256'] == digest
    assert len(preservation['entries']) == 921 and preservation['changed_entries'] == 84
    assert manifest['profile'] == 'all-routes-unified-v309' and len(manifest['batches']) == 470
    assert manifest['release_stack_sha256'] == sha(Path('translations/release_stack.json').read_bytes())
    assert all(manifest['checks'].values())
    release = read('work/analysis/sailing_conditions_v309/release_proof.json')
    assert release['candidate_sha256'] == digest and release['exact_clean_patch_reconstruction']
    assert sha(ROM.with_suffix('.xdelta').read_bytes()) == release['patch_sha256']
    assert Path('work/analysis/sailing_conditions_v309/exact_patch_reconstruction.nds').read_bytes() == ROM.read_bytes()
    names = campaign['reviewed_name_release_v299']
    assert names['all444_complete_native_route_bodies_and5604_expanded_copies_pass']
    assert names['all621_getters_18_COMMON_copies_and24_modal_glyph_cases_pass']
    # Later candidates retain the integrated names/text/art implementation.
    old, current = NdsImage.open(names['candidate']), NdsImage.open(ROM)
    for path in ('/COMMON/HELP.DK4', '/COMMON/MESFILE.DK4', '/data/SC0.DK4', '/data/SC1.DK4',
                 '/data/SC2.DK4', '/data/SC3.DK4', '/FLS/M28.fls'):
        assert old.read_file(path) == current.read_file(path)
    assert campaign['title_display_v229']['opening_foreground_and_menu_first_last_letters_bounds_verified']
    assert campaign['alternate_title_display_v238']['title05_complete_display_verified']
    dispositions = {
        1: ('open', 'Brown water-mark interpretation and original raw-comic display remain open; existing translations retained.', ['root_and_retained_source_v304', 'comic_fringe_v251']),
        2: ('open', 'Eleven legacy storage/layout/composition gates remain open; source content reviews are scoped evidence.', ['current_embedded_storage_census_v192', 'FLS_stream_and_cached_descriptors_v310']),
        3: ('partially_verified', 'Six source retain decisions and bounded native selectors/fixtures verified; normal city assignments/background displays remain open.', ['contextual_environment_native_v206', 'contextual_environment_display_v207', 'square_sign_bounds_v254']),
        4: ('partially_verified', 'Image207 mark source preservation verified; exact identity/reading and actual scene remain open.', ['completed_storage_localizations_v179', 'completed_creator_mark_decision_files']),
        5: ('implementation_verified_contexts_open', 'Approved naming/source choices and current text/art implementation verified; deeper/unlocked contexts remain open.', ['confirmed_name_choices_2026_10_06', 'reviewed_name_release_v299']),
        6: ('partially_verified', 'All15 FLS metadata parsers,520 compressed decoder cases and15 source-identical timelines verified. GPU binding/clipping/alpha and legacy usage remain open.', ['FLS_stream_and_cached_descriptors_v310', 'FLS_payload_decode_v311', 'FLS_timeline_geometry_v312']),
        7: ('integration_verified_acceptance_pending', 'Current470-batch combined ROM, manifest, exact patch and progress verified. Canonical promotion still requires user acceptance.', ['sailing_condition_names_v309']),
        8: ('observed_title_rendering_verified', 'Opening/main-menu complete pixels and first/final lettering verified in actual captures; this old observed-title backlog is superseded. Other logo consumers remain item9.', ['title_display_v229', 'genre_native_view_v305', 'FLS_timeline_geometry_v312']),
        9: ('partially_verified', 'title05 actual Extras/About Extras display and Back verified. Standalone logo consumer remains open.', ['alternate_title_display_v238']),
        10: ('open', 'Porto Estado legacy title native consumer/display and masked scenery review remain open.', ['full_resolution_review_v230', 'current_embedded_storage_census_v192']),
        11: ('open', 'Raw recruitment/end caption artwork needs actual display/readability and visual review of restoration under removed source glyphs.', ['completed_storage_localizations_v181']),
        12: ('open', 'Raw chase caption native display/readability and covered scenery review remain open.', ['completed_storage_localizations_v182']),
        13: ('open', 'Raw creature introduction preserves portraits/contours; actual display/crops/readability remain open.', ['completed_storage_localizations_v183']),
        14: ('open', 'Raw Maria heading source edges retained; backing/shadow restoration and actual display/readability remain open.', ['completed_storage_localizations_v184']),
        15: ('open', 'Raw reaction/reveal visual restoration, brown marks and actual display remain open.', ['completed_storage_localizations_v185', 'root_and_retained_source_v304']),
        16: ('superseded_by_verified_name_integration', 'The old Camille/Kamil implementation discrepancy is superseded by V299 and byte-identical current route/shared/art files. Broader deep contexts remain items5/6.', ['reviewed_name_release_v299']),
        17: ('superseded_by_verified_name_integration', 'The old Maria name spelling/field migration is superseded by V299 and preserved current files. Broader deep contexts remain items5/6.', ['reviewed_name_release_v299']),
        18: ('open_by_user_instruction', 'All17 plaques and Equipped Items hint remain in the ongoing audit with completion false.', ['plaque_style_v247', 'plaque_audit_v300', 'occupied_equipment_audit_v308']),
        19: ('partially_verified', 'Empty Weapon/Armor and occupied book contexts verified; actual occupied weapons/armor and alternate health/mood/route/fleet contexts remain open.', ['plaque_audit_v300', 'occupied_equipment_audit_v308']),
        20: ('partially_verified', 'Three Amsterdam sign selections verified. Other city/category contexts and ongoing plaque/equipment requirements remain open.', ['square_sign_bounds_v254', 'occupied_equipment_audit_v308']),
        21: ('partially_verified', 'F/I and left-margin repairs verified in their documented native/current contexts; broad parent/GPU/prose audits remain open.', ['common_literal_prefix_v255', 'dialogue_left_alignment_v258', 'reviewed_name_release_v299']),
        22: ('partially_verified', 'Eight map paintings have no separate Japanese caption and remain source art. Actual map-menu banks/GPU and legacy archive use remain open.', ['map_source_v256', 'whole_preservation_v225']),
    }
    assert len(campaign['additional_pending']) == len(dispositions) == 22
    rows = []
    for number, original in enumerate(campaign['additional_pending'], 1):
        status, note, keys = dispositions[number]
        assert all(key in campaign for key in keys)
        rows.append({'historical_item': number, 'original_requirement': original,
                     'current_disposition': status, 'current_evidence_and_remaining_work': note,
                     'authoritative_campaign_evidence_keys': keys})
    report = {'format': 'dk4-current-graphics-requirements-reconciliation-v1',
              'candidate': str(ROM), 'candidate_sha256': digest, 'original_scope_preserved': campaign['original_scope'],
              'historical_pending_items_retained': rows,
              'Online_exception': campaign['user_scope_exceptions']['low_resolution_online_images'],
              'all18_plaque_entries_fully_completed_false': True,
              'source_preservation_proof': str(ROOT / 'preservation_proof.json'),
              'all921_preservation_invariants_current': True,
              'preservation_proof_sha256': sha((ROOT / 'preservation_proof.json').read_bytes()),
              'all_current_recorded_implementation_and_release_checks_do_not_prove_full_gameplay': True,
              'full_goal_complete': False, 'documentation': 'docs/graphics_requirements_v313.md'}
    report_path = Path('translations/graphics_completion_requirements_v313.json')
    report_path.write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    for filename in ('graphics_completion_campaign_v1.json', 'graphics_visual_audit_v150.json'):
        path = Path('translations') / filename
        data = read(path)
        group = data['plaque_style_v247']
        assert len(group['ongoing_plaque_inventory']) == 18 and not group['full_plaque_audit_complete']
        assert all(not r['fully_completed'] for r in group['ongoing_plaque_inventory'])
        assert not data['user_scope_exceptions']['low_resolution_online_images']['translation_required']
        data['current_requirement_reconciliation_v313'] = {
            'requirements': str(report_path), 'requirements_sha256': sha(report_path.read_bytes()),
            'current_candidate_sha256': digest, 'historical_requirements_retained': 22,
            'preservation_proof': str(ROOT / 'preservation_proof.json'),
            'documentation': 'docs/graphics_requirements_v313.md', 'full_goal_complete': False}
        data['current_goal_turn_classification'] = 'progress-current921-asset-preservation-and22-requirement-reconciliation'
        path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print('All921 current preservation checks, registered470-batch release and22 original requirements reconciled; full goal incomplete.')


if __name__ == '__main__':
    main()
