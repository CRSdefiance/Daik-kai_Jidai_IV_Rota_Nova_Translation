"""Bind the reviewed Maria pages to the original mixed-object storage contract."""
from copy import deepcopy
from pathlib import Path
from scripts.audit_story_glyph_consistency import load, save
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest

ROOT = Path('work/Maria_B0_B32_clean_20261109')
OUT = ROOT/'storage_inputs_v1'


def main():
    assert not OUT.exists()
    paths = dict(doc=ROOT/'formatting_v1/formatting_input.json',
        plan=ROOT/'refined_plans_v2/automatic_plans.json',
        native=ROOT/'refined_native_v2/compiled_native_pages.json',
        styles=ROOT/'compiled_styles_v1/compiled_style_objects.json',
        qualification=ROOT/'compiled_styles_v1/final_plan_qualification_v1.json',
        menu=ROOT/'menu_planes_v1/menu_provider_and_planes.json',
        packet=ROOT/'current_v1/current_effective.json',
        visual=ROOT/'offline_display_approval_v1.json')
    data = {key: load(path) for key, path in paths.items()}
    doc, plan, native, styles, qualification, menu, packet, visual = [data[k] for k in paths]
    assert (len(doc['records']), len(plan['records']), len(native['records']), native['pages']) == (301, 299, 299, 303)
    assert visual['every_final_page_directly_viewed_in_readable_sheets']
    assert visual['all_native_glyph_consumption_bounds_andpagination_guards_pass']
    assert visual['all36_scoped_actors_and44_distinct_name_strings_native_andvisually_checked']
    for path, expected in visual['evidence'].items():
        assert digest(path) == expected
    assert not plan['failures']
    assert not any(i['severity'] in ('warning', 'error') for r in plan['records'] for i in r['base_QA']['issues'])
    assert native['manuscript_sha256'] == plan['manuscript_sha256'] == styles['manuscript_sha256'] == menu['manuscript_sha256'] == digest(paths['doc'])
    assert native['plan_sha256'] == digest(paths['plan']) == qualification['final_plan_sha256']
    assert qualification['prior_sha256'] == digest(paths['styles'])
    assert qualification['all_seven_complete_style_plan_rows_exact']
    assert qualification['native_context_andall_compiler_inputs_exact']
    assert native['runtime'] == styles['runtime'] == menu['runtime'] == packet['runtime'] == doc['runtime']
    assert menu['complete_caption_glyphs_centering_bounds_guards_andconsumption_pass']
    assert (menu['native_provider_alignments'], menu['bridged_modal_returns'], menu['complete_English_caption_style_planes'], len(menu['compiler_negatives_rejected'])) == (6, 18, 8, 7)
    assert styles['physical_alternatives'] == 7 and styles['native_target_slot_cases'] == 8
    assert all(r['review'] == dict(source=True, context=True, localization=True, naturalness=True, formatting=False) for r in doc['records'])
    source_rows = deepcopy(doc['records'])
    for row in doc['records']:
        if row['kind'] == 'typed-choice-label':
            row['original_exact_source_reference'] = deepcopy(row['source_reference'])
            row['source_reference'].update(command_offset=row['source_command_offset'], source_index=row['source_index'])
    assert all(a['english'] == b['english'] and a['current_hex'] == b['current_hex'] and a['source_hex'] == b['source_hex'] for a, b in zip(source_rows, doc['records'], strict=True))
    doc.update(offline_speech_visual_approved=True, offline_caption_visual_approved=True,
        scoped_name_native_andvisual_approved=True, all_individual_fifth_gates_still_pending=True,
        source_full_manuscript=str(paths['doc']), source_full_manuscript_sha256=digest(paths['doc']),
        final_visual_approval=str(paths['visual']), final_visual_approval_sha256=digest(paths['visual']))
    OUT.mkdir()
    manuscript = OUT/'storage_manuscript.json'
    save(manuscript, doc)
    planned = {r['id']: r for r in plan['records']}
    assert all(r['compiled_hex'] == planned[r['id']]['encoded_hex'] for r in native['records'])
    plan.update(manuscript=str(manuscript), manuscript_sha256=digest(manuscript))
    planpath = OUT/'compiled_plans.json'
    save(planpath, plan)
    native.update(manuscript=str(manuscript), manuscript_sha256=digest(manuscript),
        plan=str(planpath), plan_sha256=digest(planpath), metadata_only_storage_bridge=True,
        original_native_receipt=str(paths['native']), original_native_receipt_sha256=digest(paths['native']),
        direct_visual_review_pending=False, final_visual_approval=str(paths['visual']), final_visual_approval_sha256=digest(paths['visual']))
    save(OUT/'native_pages.json', native)
    for obj in styles['objects']:
        assert digest(obj['target_path']) == obj['target_sha256']
        for slot in obj['native_slots']:
            assert slot['target_hex'] == bytes.fromhex(planned[slot['record_id']]['encoded_hex'])[1:].hex()
            assert slot['complete_original_getter_pointer_body_terminator_stream_owner_andall_unowned4MiB_exact']
    styles.update(manuscript=str(manuscript), manuscript_sha256=digest(manuscript),
        plan=str(planpath), plan_sha256=digest(planpath), metadata_only_storage_bridge=True,
        original_style_receipt=str(paths['styles']), original_style_receipt_sha256=digest(paths['styles']),
        final_plan_qualification=str(paths['qualification']), final_plan_qualification_sha256=digest(paths['qualification']))
    save(OUT/'styles.json', styles)
    save(OUT/'packet.json', packet)
    captions = sorted((r for r in doc['records'] if r['kind'] == 'typed-choice-label'), key=lambda r: r['source_index'])
    assert len(captions) == 2 and captions[0]['block'] == captions[1]['block'] == 29
    assert captions[0]['source_command_offset'] == captions[1]['source_command_offset']
    save(OUT/'menus.json', dict(manuscript=str(manuscript), manuscript_sha256=digest(manuscript), runtime=native['runtime'],
        menus=[dict(block=29, source_command_offset=captions[0]['source_command_offset'],
            target_object_hex=menu['native_choice_object_hex'], record_IDs=[r['id'] for r in captions],
            original_receipt=str(paths['menu']), original_receipt_sha256=digest(paths['menu']))],
        offline_visual_approved=True, direct_view_pending=False,
        actual_controller_andstored_objects_still_pending=True,
        complete_caption_glyphs_centering_bounds_guards_andconsumption_pass=True, new_credit=0))
    save(OUT/'metadata_bridge_qualification.json', dict(
        inputs={str(p): digest(p) for p in paths.values()},
        source_current_English_controls_macros_all301_decisions_and299_compiled_buffers_unchanged=True,
        final_style_rows_exactly_reused=True, selected_final303_pages_directly_viewed=True,
        fifth_gates_still_false=True, new_credit=0, producer_sha256=digest(Path(__file__))))
    print('Storage inputs bound:301 reviews/299 bodies/303 reviewed pages; prose and all fifth gates unchanged.')


if __name__ == '__main__':
    main()
