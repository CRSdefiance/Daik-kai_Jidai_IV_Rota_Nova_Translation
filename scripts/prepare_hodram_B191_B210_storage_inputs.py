"""Bind the approved speech/menu/name evidence to complete-block reconstruction inputs."""
from copy import deepcopy
from pathlib import Path
from scripts.audit_story_glyph_consistency import load, save
from dk4tool.patch.grand_race_menu_release import sha

ROOT = Path('work/analysis/Hodram_B191_B210_storage_inputs_20261104')
FORMAT = Path('work/analysis/Hodram_B191_B210_formatting_20261104')
DISPLAY = FORMAT / 'speech_display_approved_20261104'
CURRENT = Path('work/analysis/Hodram_B191_B210_current_20261104/current_effective.json')
MENUS = Path('work/analysis/Hodram_B191_B210_menus_20261104/complete_choice_objects.json')
NAMES = Path('work/analysis/Hodram_B191_B210_scoped_name_planes_20261104/native_name_planes.json')


if __name__ == '__main__':
    assert not ROOT.exists()
    doc = load(FORMAT / 'formatting_input.json')
    plans, native, visual, packet, menus, names = map(load, [DISPLAY / 'all352_compiled_plans.json',
        DISPLAY / 'all352_native_pages.json', DISPLAY / 'visual_approval.json', CURRENT, MENUS, NAMES])
    assert visual['final_speech_pages_visually_approved'] and visual['all21_caption_visual_checks_pass']
    assert len(doc['records']) == 373 and packet['records'] == 352 and len(packet['groups']) == 20
    assert packet['runtime'] == native['runtime'] == names['runtime']
    assert names['actors'] == 43 and names['distinct_current_strings'] == 36
    assert names['fresh_planes'] == 7 and names['exact_reused_planes'] == 29
    for sheet in names['review_sheets']:
        assert sha(Path(sheet['path']).read_bytes()) == sheet['sha256']
    assert len(names['review_sheets']) == 3
    ROOT.mkdir()
    save(ROOT / 'scoped_name_visual_approval.json', dict(native=str(NAMES), native_sha256=sha(NAMES.read_bytes()),
        review_sheets=names['review_sheets'], all_three_sheets_directly_viewed=True,
        actors=43, consumer_bindings=86, complete_native_name_strings=36, fresh_planes=7, exact_reused_planes=29,
        complete_leading_internal_trailing_characters_style11_font_and216px_bounds_pass=True,
        full_name_literal_proof_not_actual_catalogue_UI_layout_observation=True,
        representative_headers_andfull_catalogue_UI_unvisited_in_this_batch=True,
        no_new_name_table_edit_or_global207_approval=True, new_credit=0))
    storage = deepcopy(doc)
    for row in storage['records']:
        if row['kind'] == 'typed-choice-label':
            row['original_exact_source_reference'] = deepcopy(row['source_reference'])
            row['source_reference'].update(command_offset=row['source_command_offset'], source_index=row['source_index'])
    storage.update(offline_speech_visual_approved=True, offline_caption_visual_approved=True,
        scoped_name_native_andvisual_approved=True, all_individual_fifth_gates_still_pending=True,
        source_full_manuscript=str(FORMAT / 'formatting_input.json'),
        source_full_manuscript_sha256=sha((FORMAT / 'formatting_input.json').read_bytes()))
    manuscript = ROOT / 'storage_manuscript.json'
    save(manuscript, storage)
    plans.update(manuscript=str(manuscript), manuscript_sha256=sha(manuscript.read_bytes()))
    plan_path = ROOT / 'all352_compiled_plans.json'
    save(plan_path, plans)
    native.update(manuscript=str(manuscript), manuscript_sha256=sha(manuscript.read_bytes()), plan=str(plan_path), plan_sha256=sha(plan_path.read_bytes()))
    save(ROOT / 'all352_native_pages.json', native)
    save(ROOT / 'packet.json', packet)
    groups = []
    for obj in menus['objects']:
        path = Path(obj['receipt'])
        assert sha(path.read_bytes()) == obj['receipt_sha256']
        proof = load(path)
        assert proof['runtime'] == native['runtime'] and proof['complete_caption_glyphs_centering_bounds_guards_andconsumption_pass']
        assert Path(obj['compiled_path']).read_bytes().hex() == obj['target_object_hex']
        groups.append(dict(block=obj['block'], source_command_offset=obj['source_command_offset'],
            target_object_hex=obj['target_object_hex'], record_IDs=obj['record_ids'],
            source_count=obj['count'], exact_complete_object_reused=obj['exact_complete_object_andcode_dependencies_reused'],
            original_receipt=str(path), original_receipt_sha256=sha(path.read_bytes())))
    assert len(groups) == 10 and sum(g['source_count'] for g in groups) == 21
    save(ROOT / 'menus_reviewed.json', dict(manuscript=str(manuscript), manuscript_sha256=sha(manuscript.read_bytes()),
        runtime=native['runtime'], menus=groups, offline_visual_approved=True, direct_view_pending=False,
        complete_caption_glyphs_centering_bounds_guards_andconsumption_pass=True,
        fresh_distinct_menus=4, exact_reused_menus=6, native_provider_alignments=menus['fresh_native_provider_alignments'],
        bridged_modal_returns=menus['fresh_bridged_modal_returns'], complete_English_caption_style_planes=menus['fresh_complete_caption_style_planes'],
        source_receipt=str(MENUS), source_receipt_sha256=sha(MENUS.read_bytes()),
        actual_controller_andstored_objects_still_pending=True, new_credit=0))
    save(ROOT / 'no_style_objects.json', dict(manuscript=str(manuscript), manuscript_sha256=sha(manuscript.read_bytes()),
        plan_sha256=sha(plan_path.read_bytes()), runtime=native['runtime'], objects=[],
        source_packet_has_zero_4100_commands=True, native_target_slot_cases=0, source_alias_equivalence_exact=True, new_credit=0))
    save(ROOT / 'input_binding.json', dict(manuscript=str(manuscript), manuscript_sha256=sha(manuscript.read_bytes()),
        prose_reviews_reused=373, speech_native_andvisual_objects_reused=352, speech_pages=355, typed_captions=21,
        scoped_name_planes_reused_without_replay=36, native_orvisual_checks_replayed=0,
        all_fifth_gates_still_false=True, new_credit=0, new_ROMs=0,
        evidence={str(p): sha(p.read_bytes()) for p in [FORMAT / 'formatting_input.json', DISPLAY / 'visual_approval.json', CURRENT, MENUS, NAMES, Path(__file__)]}))
    print('373 exact prose objects / 355 viewed pages / 21 captions / 36 approved name strings bound for storage; no checks replayed.')
