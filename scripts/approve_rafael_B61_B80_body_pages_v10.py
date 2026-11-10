"""Bind all545 final native pages to directly viewed exact contact-sheet pixels."""
from copy import deepcopy
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.audit_story_glyph_consistency import load,save

ROOT=Path('work/analysis/Rafael_B61_B80_formatting_20261104')

if __name__=='__main__':
    combined=ROOT/'combined_native_v10.json';approval=ROOT/'body_display_approval_v10.json'
    assert not combined.exists() and not approval.exists()
    base_path=ROOT/'combined_native_v8.json';delta_path=ROOT/'speech_native_delta_v10/compiled_native_pages.json'
    plan_path=ROOT/'automatic_v10/automatic_plans.json'
    base,delta,plan=map(load,[base_path,delta_path,plan_path])
    assert delta['runtime']==base['runtime'] and len(delta['records'])==1 and delta['pages']==1
    assert delta['complete_consumption_andpagination_exact'] and delta['all_first_internal_final_glyph_codes_pixels_input_canaries_andbounds_pass']
    rows={r['id']:deepcopy(r) for r in base['records']};fresh=delta['records'][0]
    assert fresh['id']=='DK4_MES_B69_R0143' and fresh['compiled_hex']!=rows[fresh['id']]['compiled_hex']
    rows[fresh['id']]=deepcopy(fresh)
    folders=['contact_B61_B66_v1','contact_B67_B68_v1','contact_delta_v4','contact_ASCII_ellipsis_v2',
        'contact_delta_v8','contact_fresh250_v3','contact_delta_v10']
    manifests=[ROOT/folder/'contact_manifest.json' for folder in folders]
    views={};sheets=[];all_viewed_pages=0
    for path in manifests:
        data=load(path)
        for sheet in data['sheets']:
            assert sha(Path(sheet['path']).read_bytes())==sheet['sha256']
            sheets.append(sheet)
        for page in data['pages']:
            assert sha(Path(page['source']).read_bytes())==page['source_sha256']
            views.setdefault((page['id'],page['page'],page['source_sha256']),[]).append(dict(
                manifest=str(path),manifest_sha256=sha(path.read_bytes()),source=page['source']))
            all_viewed_pages+=1
    assert len(sheets)==35 and all_viewed_pages==563
    assert len(rows)==len(plan['records'])==539 and not plan['failures']
    bindings=[]
    for target in plan['records']:
        row=rows[target['id']]
        assert row['compiled_hex']==target['encoded_hex'] and row['logical_English']==target['logical_English']
        assert not any(i['severity'] in ['warning','error'] for i in target['base_QA']['issues'])
        rendered=row['complete_native_English_display']
        pages=[dict(page=1,preview=rendered['preview'],preview_sha256=rendered['preview_sha256'])] if row['kind']=='system-FE' else rendered['pages']
        assert len(pages)==target['expected_native_pages']
        for page in pages:
            path=Path(page['preview']);digest=sha(path.read_bytes());assert digest==page['preview_sha256']
            key=row['id'],page['page'],digest
            assert key in views,key
            bindings.append(dict(id=row['id'],page=page['page'],preview=str(path),preview_sha256=digest,
                exact_direct_visual_evidence=views[key]))
    assert len(bindings)==545
    special=next(r for r in plan['records'] if r['id']=='DK4_MES_B69_R0143')
    assert special['lines']==["...{MACRO:FI}, thank you so much. It's",'all thanks to you that the','villagers are smiling again.']
    warning=[i for i in special['unmodified_base_QA']['issues'] if i['severity']=='warning']
    assert len(warning)==1 and warning[0]['code']=='weak-line-ending'
    assert any(i.get('reviewed_retention_reason') for i in special['base_QA']['issues'])
    result=deepcopy(base);result.update(records=[rows[r['id']] for r in plan['records']],
        plan=str(plan_path),plan_sha256=sha(plan_path.read_bytes()),
        previous_native=str(base_path),previous_native_sha256=sha(base_path.read_bytes()),
        final_delta=str(delta_path),final_delta_sha256=sha(delta_path.read_bytes()),
        direct_visual_review_pending=False,all545_final_body_pages_directly_viewed=True,
        layout_refinements=14,ellipsis_glyph_refinements=14,
        changed_compiled_record_IDs_since_initial547_page_plan=base['changed_compiled_record_IDs_since_initial547_page_plan']+[fresh['id']],
        exact_grammatical_line_ending_retention=dict(id=fresh['id'],line_index=1,exact_line='all thanks to you that the',
            reason='One complete-word article soft wrap uses three readable native-width rows instead of four shorter rows. Source/current/English bindings, original QA warning and all native glyph/bounds/control checks are preserved.'),
        all_individual_fifth_gates_still_false=True,new_credit=0,producer_sha256=sha(Path(__file__).read_bytes()))
    assert len(result['changed_compiled_record_IDs_since_initial547_page_plan'])==28
    save(combined,result)
    save(approval,dict(final_native=str(combined),final_native_sha256=sha(combined.read_bytes()),
        final_plan=str(plan_path),final_plan_sha256=sha(plan_path.read_bytes()),
        final_manuscript=base['manuscript'],final_manuscript_sha256=base['manuscript_sha256'],
        body_records=539,body_pages=545,all_final_pages_directly_viewed=True,exact_page_bindings=bindings,
        viewed_sheets=sheets,viewed_candidate_pages=563,retired_orreplaced_candidate_pages_also_reviewed=18,
        dialogue_revisions=210,justified_retentions=329,fullwidth_I_corrections=16,ellipsis_glyph_corrections=14,
        scoped_copied_fullwidth_punctuation_characters_normalized=19,layout_refinements=14,
        unnecessary_pages_removed=2,all_prose_preserved_across_layout_refinements=True,
        complete_native_glyphs_macros_controls_canaries_bounds_andpagination_pass=True,
        progressive_width216_FE_width228_four_native_rows_font_andaccepted_runtime_unchanged=True,
        all_five_Charlotte_FE_andone_funds_notice_native_row_memberships_exact=True,
        concrete_FE_single_letter_wrap_fixed_without_runtime_orfont_change=True,
        one_exact_grammatical_soft_boundary_retention=result['exact_grammatical_line_ending_retention'],
        reviewed_native_two_page_retentions=[
            dict(id='DK4_MES_B65_R0035',reason='The full unchanged paragraph cannot occupy four native rows with the short question tag intact. First page keeps the complete question, second the complete workload explanation; no text is shortened or viewport widened.'),
            dict(id='DK4_MES_B75_R0238',reason='No full-word four-row fit exists. The first page ends a complete sentence; the second is the complete contempt sentence, preserving deliberate character emphasis.')],
        ordinary_soft_boundary_retention=dict(id='DK4_MES_B67_R0088',
            reason='Following/through is an ordinary complete-word soft boundary in a single page; the alternatives create a sparse opening line. All words and glyphs are present. No manual spacing or narrower viewport is introduced.'),
        source_header_name_planes_storage_representative_CG_transitions_andregistered_integration_pending=True,
        actual_gameplay=False,all539_new_scene_gameplay_unvisited=True,
        all_individual_fifth_gates_remain_false_until_remaining_checks_pass=True,
        evidence={str(p):sha(p.read_bytes()) for p in [base_path,delta_path,plan_path,*manifests,Path(__file__)]},
        new_credit=0,guide_photos=False,full_goal_complete=False))
    print('All545 final body pages visually approved on35 readable sheets;14 layout refinements/16 I/14 ellipsis fixes.539 records retain pending full display/storage/gameplay/integration gates;zero credit.',flush=True)
