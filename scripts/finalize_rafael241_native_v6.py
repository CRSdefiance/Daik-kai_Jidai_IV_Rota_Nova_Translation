"""Seal229 reviewed native body layouts/234 pages,retaining exact completed partial checks."""
from copy import deepcopy
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.audit_story_glyph_consistency import load,save

DOC=Path('translations/rafael_B101_B120_contextual_editorial_manuscript_v4.json')
PLAN=Path('work/analysis/Rafael241_layout_v6_20261105/automatic_plans.json')
BASE=Path('work/analysis/Rafael241_native_v1_20261105/partial_complete_blocks_receipt.json')
DELTA=Path('work/analysis/Rafael241_native_delta_v4_20261105/compiled_native_pages.json')
TWO=Path('work/analysis/Rafael241_native_delta_v5_20261105/B114_checked.json')
LAST=Path('work/analysis/Rafael241_native_delta_v6_20261105/compiled_native_pages.json')
NAMES=Path('work/analysis/Rafael241_scoped_name_planes_v1_20261105/native_name_planes.json')
MENU=Path('work/analysis/Rafael241_three_choice_v1_20261105/menu_provider_and_planes.json')
OUT=Path('work/analysis/Rafael241_native_final_v6_20261105')

if __name__=='__main__':
    assert not OUT.exists()
    doc,plan,base,delta,two,last,names,menu=map(load,[DOC,PLAN,BASE,DELTA,TWO,LAST,NAMES,MENU])
    assert plan['manuscript_sha256']==sha(DOC.read_bytes()) and not plan['failures']
    assert delta['runtime']==last['runtime']==names['runtime']==menu['runtime']
    assert len(base['records'])==101 and base['whole_batch_pass'] is False
    assert (len(delta['records']),delta['pages'],len(two['records']),len(last['records']))==(136,141,2,1)
    sources=[LAST,TWO,DELTA,BASE];proofs=[last,two,delta,base]
    maps=[{r['id']:r for r in p['records']} for p in proofs]
    records=[];origins={};counts={str(p):0 for p in sources};approved_pages=[]
    doc_by={r['id']:r for r in doc['records']}
    for planned in plan['records']:
        ident=planned['id']
        matches=[(rows[ident],path) for rows,path in zip(maps,sources,strict=True) if ident in rows and rows[ident]['compiled_hex']==planned['encoded_hex']]
        assert matches,ident
        row,origin=matches[0]
        assert row['logical_English']==planned['logical_English']==doc_by[ident]['english']
        assert row['source_reference']==doc_by[ident]['source_reference'] and row['current_reference']==doc_by[ident]['current_reference']
        assert len(row['native_alignment']['cases'])==4 and all(c['output_hex']==row['expanded_native_hex'] for c in row['native_alignment']['cases'])
        rendered=row['complete_native_English_display']
        if row['kind']=='system-FE':
            assert rendered['all_first_internal_final_ASCII_CP932_codes_andindependent_logical_plane_exact']
            assert rendered['planned_native_row_comparison']['complete_glyph_row_membership_exact']
            pages=[rendered]
        else:
            assert rendered['all_visible_first_internal_final_characters_in_order'] and rendered['no_blank_or_overlap_page']
            assert rendered['complete_consumed_bytes']==len(bytes.fromhex(row['expanded_native_hex']))
            pages=rendered['pages']
        assert len(pages)==planned['expected_native_pages']
        for page in pages:
            for pathkey,hashkey in [('native_plane','native_plane_sha256'),('preview','preview_sha256')]:
                assert sha(Path(page[pathkey]).read_bytes())==page[hashkey]
            approved_pages.append(dict(id=ident,preview=page['preview'],preview_sha256=page['preview_sha256']))
        counts[str(origin)]+=1;records.append(deepcopy(row))
        origins[ident]=dict(native_proof=str(origin),native_proof_sha256=sha(origin.read_bytes()),
            complete_compiled_bytes_logical_prose_control_refs_andnative_pages_qualified=True,
            direct_visual_review_of_exact_page_complete=True,
            prior_completed_block_before_later_failed_FE_run=origin in [BASE,TWO])
    assert counts=={str(BASE):93,str(DELTA):133,str(TWO):2,str(LAST):1}
    assert len(records)==229 and len(approved_pages)==234
    assert all(i['severity'] not in ['error','warning'] for r in plan['records'] for i in r['base_QA']['issues'])
    viewed=[]
    for block in range(101,113):
        for path in sorted(BASE.parent.glob(f'B{block}_part*.png')):
            viewed.append(dict(path=str(path),sha256=sha(path.read_bytes()),scope='Original completed blocks,including later-refined pages;all directly viewed.'))
    for proof in [delta,last]:
        for sheet in proof['review_sheets']:
            assert sha(Path(sheet['path']).read_bytes())==sheet['sha256'];viewed.append(sheet)
    final_two=TWO.parent/'B114_part1.png';assert final_two.exists()
    viewed.append(dict(path=str(final_two),sha256=sha(final_two.read_bytes()),pages=2))
    assert len(viewed)==34
    # Two images written before the first FE failure are exact duplicates of viewed v4 pages.
    duplicate_partial=[]
    for name in ['DK4_MES_B113_R0029_FE.png','DK4_MES_B113_R0033_p1.png']:
        earlier,later=BASE.parent/name,DELTA.parent/name
        assert earlier.read_bytes()==later.read_bytes()
        duplicate_partial.append(dict(path=str(earlier),sha256=sha(earlier.read_bytes()),viewed_identical_page=str(later)))
    for proof in [names,menu]:
        for sheet in proof['review_sheets']:
            assert sha(Path(sheet['path']).read_bytes())==sheet['sha256']
    assert (names['scoped_actors'],names['distinct_strings'],names['fresh_name_planes'],names['exact_reused_name_planes'])==(18,17,7,10)
    assert (len(menu['menus']),len(menu['records']),menu['native_provider_alignments'],menu['bridged_modal_returns'])==(4,48,24,96)
    compared=load(menu['manuscript']);before={r['id']:r for r in compared['records'] if r['kind']=='typed-choice-label'}
    captions=[r for r in doc['records'] if r['kind']=='typed-choice-label']
    assert len(captions)==12
    for row in captions:
        assert all(row[k]==before[row['id']][k] for k in ['english','source_reference','current_reference','source_choice_object_hex','current_choice_object_hex','review'])
    OUT.mkdir();approval=OUT/'direct_visual_approval.json'
    save(approval,dict(approved_pages=approved_pages,body_sheets=viewed,exact_duplicate_partial_pages=duplicate_partial,
        all234_current_body_pages_andall_generated_readable_sheets_directly_viewed=True,
        final_prose_corrections=132,justified_prose_retentions=109,
        ten_approved_wrap_phrase_page_refinements=True,two_source_scoped_FE_guard_budget_fixes=['DK4_MES_B113_R0037','DK4_MES_B118_R0019'],
        rejected_weak_article_ending_andsparse_middle_alternatives_preserved=True,
        B120_R56_original_balanced_rows_andstandalone_hearsay_aside_retained=True,
        B115_R17_idiom_retained_across_ordinary_rows_withno_sparse_opening_orpage_turn=True,
        no_prose_shortened_to_fit_no_font_viewport_orengine_changes=True,
        native_failures_preserved_original_row_andconsumption_assertions_not_waived=True,
        all18_scoped_names_and17_strings_onboth_sheets_directly_viewed=True,
        all12_caption_labels_both_native_styles_andboth_sheets_directly_viewed=True,
        offline_display_review_not_gameplay=True,stored_actual_andregistered_integration_pending=True,new_credit=0))
    merged=deepcopy(delta)
    merged.update(manuscript=str(DOC),manuscript_sha256=sha(DOC.read_bytes()),plan=str(PLAN),plan_sha256=sha(PLAN.read_bytes()),
        records=records,origins=origins,pages=234,final_native_origins=counts,
        fresh_compiled_alignments=4*229,alignment_count_is_composite_not_one_run=True,
        review_sheets=viewed,direct_visual_review_pending=False,all229_body_layouts_approved=True,
        all234_complete_pages_directly_viewed=True,typed_choice_labels_separately_pending=False,
        full241_object_batch_offline_display_complete=True,scoped_names_display_complete=True,
        complete_consumption_andpagination_exact=True,all_first_internal_final_glyph_codes_pixels_input_canaries_andbounds_pass=True,
        formatting_gates_still_false=True,actual_gameplay=False,stored_actual_andregistered_integration_pending=True,
        evidence={str(p):sha(p.read_bytes()) for p in [DOC,PLAN,*sources,NAMES,MENU,approval,Path(__file__)]},new_credit=0)
    save(OUT/'compiled_native_pages.json',merged)
    save(OUT/'qualified_menu.json',{**deepcopy(menu),'manuscript':str(DOC),'manuscript_sha256':sha(DOC.read_bytes()),
        'qualified_previous_proof':str(MENU),'qualified_previous_proof_sha256':sha(MENU.read_bytes()),
        'all12_exact_source_current_complete_objects_prose_review_gates_andnative_dependencies_unchanged':True,
        'direct_view_pending':False,'no_new_menu_execution_claim':True})
    save(OUT/'scoped_names_visual_approval.json',dict(proof=str(NAMES),proof_sha256=sha(NAMES.read_bytes()),
        review_sheets=names['review_sheets'],all18_scoped_actors17_strings_directly_viewed=True,
        no_name_data_changes_actual_headers_unvisited_full_catalogue_UI_andglobal207_still_open=True,new_credit=0))
    print('229 speeches/234 exact native viewed pages,12 captions and18 scoped names approved offline. All fifth gates/stored/actual/integration still pending.')
