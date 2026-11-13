"""Integrate the source-locked item projection with its scoped native evidence."""

import json
from pathlib import Path

from dk4tool.dialogue.review import validate_natural_dialogue_batch
from dk4tool.patch.generated_item_advice_research import transform as extend_maps
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.item_interface_research import CLEAN, SOURCE
from dk4tool.patch.item_interface_research import transform as item_text
from dk4tool.patch.item_parent_layout_research import transform as parent_layout
from dk4tool.patch.main_pool_cache_visibility import transform as maintain_cache

TARGET = '642177fcd6f6c0ef69c7cf7d89563c9a974183ab00223733016c814c5d8c74cf'
HISTORICAL = {
    'local_proof': 'c55a2530af7816a5f612494c42c16af5911e58791d571d92ad9297b7e87980ee',
    'label_grid': 'c55a2530af7816a5f612494c42c16af5911e58791d571d92ad9297b7e87980ee',
    'advice_proof': 'edb1032dd92bfbe0c73f18ffdcae71f3b78108bab4ed7546f8b8d3fada739663',
    'crew_proof': 'edb1032dd92bfbe0c73f18ffdcae71f3b78108bab4ed7546f8b8d3fada739663',
    'ship_proof': 'edb1032dd92bfbe0c73f18ffdcae71f3b78108bab4ed7546f8b8d3fada739663',
    'parent_proof': 'd5f49394f4bf6dad6647226b6bcf0f505e5a87bff75100ac486f398c857c92fc',
}


def transform(image, clean_image):
    original, plan = item_text(image, clean_image)
    cached, cache = maintain_cache(original)
    repaired, parent = parent_layout(cached)
    saved, complete = extend_maps(repaired, image.read_file('/COMMON/MESFILE.DK4'), plan)
    if sha(saved) != TARGET:
        raise ValueError('Complete item target differs')
    return saved, complete, {'initial': sha(original), 'cached': sha(cached), 'parent': sha(repaired),
                             'cache': cache, 'parent_repair': parent}


def visual(proof, count):
    review = proof.get('visual_review', {})
    if review.get('complete') is not True or review.get('panel_count') != count:
        raise ValueError('Item visual review incomplete')
    sheet = Path(review['sheet'])
    if sha(sheet.read_bytes()) != review['sheet_sha256']:
        raise ValueError('Item reviewed sheet changed')
    for filename, expected in review.get('panel_sha256', {}).items():
        if sha((sheet.parent / filename).read_bytes()) != expected:
            raise ValueError('Item reviewed panel changed')


def validate_manuscript(manuscript, plan):
    if (manuscript.get('translation_policy') != 'natural-dialogue-v2'
            or manuscript['source_arm9_sha256'] != CLEAN or len(manuscript['records']) != 35):
        raise ValueError('Item source and editorial review differs')
    visible = []
    for row, expected in zip(manuscript['records'], plan['records'], strict=True):
        for key in ('id', 'japanese', 'english', 'compiled', 'source_fields', 'kind', 'index'):
            if row.get(key) != expected.get(key):
                raise ValueError('Item complete source/prose/compiled review differs')
        if row['id'] == 'ITEM_USE':
            # The native branch leaves the name null and never draws this heading.
            # Its reference is preserved without claiming a visible translation.
            if (row['review'].get('formatting') is not False
                    or not all(row['review'].get(k) is True for k in ('source', 'context', 'localization', 'naturalness'))):
                raise ValueError('Nonvisible Use branch must retain separate editorial-only review')
        else:
            visible.append(row)
    validate_natural_dialogue_batch({**manuscript, 'records': visible})


def validate_proofs(proofs, plan):
    for key, target in HISTORICAL.items():
        if proofs[key]['target_arm9_sha256'] != target:
            raise ValueError('Historical item evidence scope differs: ' + key)
    local = proofs['local_proof']
    if (len(local['native_pixel_cases']) != 1338 or len(local['actual_static_resource_cases']) != 752
            or not local['visual_review']['complete'] or local['visual_review']['reviewed_panel_count'] != 29
            or not proofs['label_grid']['all_13_categories_and_16_roles_covered']
            or not proofs['label_grid']['visually_reviewed']):
        raise ValueError('Full item category/role/static coverage incomplete')
    for key, cases, panels in (('advice_proof', 12, 6), ('crew_proof', 456, 8), ('ship_proof', 280, 9),
                               ('parent_proof', 8, 8)):
        if len(proofs[key]['cases']) != cases:
            raise ValueError('Item native owner/menu/parent coverage incomplete')
        visual(proofs[key], panels)
    generated, roles, inherited = [proofs[key] for key in ('generated_proof', 'role_proof', 'inherited_proof')]
    if any(p['target_arm9_sha256'] != TARGET for p in (generated, roles, inherited)):
        raise ValueError('Current item target evidence differs')
    for proof in (generated, roles, inherited):
        snapshot = proof.get('verification_script_snapshot_sha256', {})
        if not snapshot or any(sha(Path(path).read_bytes()) != expected for path, expected in snapshot.items()):
            raise ValueError('Current item verification script changed; refresh its evidence')
    if ([len(generated[k]) for k in ('full_native_initializers', 'all_218_native_metadata_initializers',
                                     'generated_rasters', 'static_default_regressions')] != [37, 218, 320, 20]
            or len(generated['lookup_ABI']['cases']) != 257
            or not generated['lookup_ABI']['all_pointers_registers_stack_guards_pass']
            or not generated['original_defect']['extra_non_ASCII_continuations_reproduced']):
        raise ValueError('Generated item coverage incomplete')
    expected = {(seed, index, page, mode) for seed in (0, 1, 0x7FFFFFFF, 2) for index in range(198, 218)
                for page in ('main', 'standalone') for mode in (4, 16)}
    if ({(r['seed'], r['index'], r['page'], r['mode']) for r in generated['generated_rasters']} != expected
            or not all(r['complete_glyphs_pixels_bounds_native_metadata_and_COMMON_pass']
                       and (r['page'] != 'main' or r['native_parent_complete_glyph_pixels_pass'])
                       for r in generated['generated_rasters'])):
        raise ValueError('Generated item complete glyph/parent coverage incomplete')
    from scripts.verify_item_parent_layout import EXPECTED

    parent = generated['parent']
    if ([(r['source_origin'], r['size'], r['destination_origin']) for r in parent['requests']] != EXPECTED
            or not parent['native_parent_and_seven_detail_crop_dispatches_execute']
            or not parent['destination_256x192_fit_at_native_zero_origin']):
        raise ValueError('Complete native item parent crops differ')
    boot = generated['boot']
    if (boot['arm7_source_changed_bytes_after_arm9_autoload']
            or not all(r['matches_original'] for r in boot['arm7_native_loaded_sections'])
            or not all(boot[k] for k in ('repaired_pool_matches_complete_payload', 'repair_returns_with_stack_preserved',
                                        'actual_startup_call_preserves_r0_r3', 'late_copy_reached_caller_continuation'))
            or not all(boot['SDK_staged_code_cache_line_coverage'][k]
                       for k in ('all_instruction_lines_selected', 'all_data_lines_selected'))
            or not boot['late_copy_cache_model']['worst_case_dirty_data_and_stale_instruction_model_visible']):
        raise ValueError('Complete item startup/cache/ARM7 evidence incomplete')
    counter = generated['counter_canvas']
    if (generated['arena']['low'][0] != plan['final_pool_span'][1]
            or generated['resident_arena']['native_arena_low'] != 0x01FFA000
            or generated['resident_arena']['resident_end'] != 0x01FF9FEC
            or counter['header_pointer'] != 0x022BD7D8
            or not counter['native_constructor_and_actual_overlay_clear_execute']
            or not counter['clear_only_view_preserves_adjacent_rows_columns_and_guards']):
        raise ValueError('Item arena/counter ownership incomplete')
    visual(generated, 10)
    from scripts.prepare_item_role_state import STATES

    indices = roles['actual_item_indices']
    expected_roles = {(item, state, 2, mode) for item in indices for state in STATES for mode in (4, 16)}
    expected_roles |= {(item, state, slot, mode) for item in (74, 126) for state in ('matching', 'mismatching')
                       for slot in (3, 4) for mode in (4, 16)}
    if (indices != [74, 75, 76, 77, 80, 81, 83, 84, 85, 86, 87, 90, 93, 95, 96, 97, 98, 99,
                   101, 102, 103, 105, 106, 108, 109, 110, 113, 126]
            or len(roles['cases']) != 408 or roles['actual_required_roles'] != list(range(16))
            or {(r['index'], r['state'], r['equipment_slot'], r['mode']) for r in roles['cases']} != expected_roles
            or not all(r['all_native_assignment_text_pixels_parent_and_style_pass']
                       and r['eligible'] == (r['state'] not in ('mismatching', 'unassigned'))
                       and r['owner_name_color'] == (1 if r['eligible'] else 4) for r in roles['cases'])):
        raise ValueError('Role eligibility/full owner text coverage incomplete')
    visual(roles, 8)
    if (inherited['source_arm9_sha256'] != SOURCE
            or [len(inherited[k]) for k in ('Gallery_pixels', 'duel_pixels', 'movement_callers', 'village_callers',
                                          'monthly_scope_cases', 'ordinary_names', 'shared_name_owners',
                                          'sailing_status_pixels')] != [14, 64, 24, 54, 9, 207, 239, 2]
            or inherited['common_selected_entries_preserved'] != 3668
            or inherited['shared_copy_alignment_cases'] != 704):
        raise ValueError('Inherited native item-release coverage incomplete')


def apply_release(image, clean_image, config_path):
    config = json.loads(Path(config_path).read_text(encoding='utf-8'))
    if config.get('format') != 'dk4-item-interface-release-v1':
        raise ValueError('Wrong item release format')
    saved, plan, chain = transform(image, clean_image)
    if config['source_arm9_sha256'] != SOURCE or config['target_arm9_sha256'] != TARGET:
        raise ValueError('Item release identities differ')

    def locked(key):
        path = Path(config[key])
        if sha(path.read_bytes()) != config[key + '_sha256']:
            raise ValueError('Item evidence changed: ' + key)
        return json.loads(path.read_text(encoding='utf-8'))

    validate_manuscript(locked('manuscript'), plan)
    proofs = {key: locked(key) for key in (*HISTORICAL, 'generated_proof', 'role_proof', 'inherited_proof')}
    validate_proofs(proofs, plan)
    return saved, {'source_arm9_sha256': SOURCE, 'target_arm9_sha256': TARGET, 'transformation_chain': chain,
                   'changed_records': [r['id'] for r in plan['records']]
                   + [f'ITEM_PARAGRAPH_{index}' for index in range(218)]
                   + ['ITEM_PRIVATE_LOOKUPS_AND_PARAGRAPH_DRAW', 'ITEM_DETAIL_COLUMNS_AND_PARENT_ROWS',
                      'ITEM_STAGED_POOL_CACHE_AND_ARENA'],
                   'visible_localized_logical_records': 34, 'nonvisible_source_references': ['ITEM_USE'],
                   'word_preserving_paragraph_presentations': 218,
                   'historical_local_rasters': 2090, 'historical_owner_menu_rasters': 748,
                   'current_generated_rasters_and_regressions': 340, 'current_role_rasters': 408,
                   'current_metadata_initializers': 218, 'current_lookup_ABI_cases': 257,
                   'final_pool_span': plan['final_pool_span'], 'staging_span': plan['staging_span'],
                   'copy_entry': plan['copy_entry'], 'cache_entry': plan['cache_entry'],
                   'pool_payload_bytes': plan['pool_payload_bytes'],
                   'source_common_sha256': plan['source_common_sha256'],
                   'historical_evidence_note': 'Earlier scopes retain their actual hashes. Source-locked transforms preserve '
                                               'their text/helpers while current evidence checks expanded table, parent and cache.',
                   'physical_gameplay_verified': False}
