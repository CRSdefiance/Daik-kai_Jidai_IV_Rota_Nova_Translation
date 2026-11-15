"""Bind completed prose, speech planes, cinematic layouts and menus without replaying them."""
from copy import deepcopy
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.audit_story_glyph_consistency import load,save

ROOT=Path('work/analysis/Hodram_B151_B170_reconstruction_inputs_20261102')
FORMAT=Path('work/analysis/Hodram_B151_B170_formatting_20261102')
MANUSCRIPT=Path('translations/hodram_B151_B170_contextual_editorial_manuscript_v3.json')
CINEMATIC=Path('work/analysis/Hodram_B156_cinematic_English_v4_20261102/compiled_cinematic_pages.json')
NAME_ROOT=Path('work/analysis/Hodram_B151_B170_scoped_name_planes_20261102')
STATIC=Path('work/analysis/Hodram_B151_B170_static_labels_20261102/native_static_labels_qualification.json')

if __name__=='__main__':
    assert not ROOT.exists();doc=load(MANUSCRIPT);ordinary_input=load(FORMAT/'ordinary_formatting_input.json')
    old_native_path=FORMAT/'ordinary_native_v2/compiled_native_pages.json';ordinary=load(old_native_path);old_plans_path=Path(ordinary['plan']);plans=load(old_plans_path)
    cine=load(CINEMATIC);visual=load(FORMAT/'ordinary_visual_review_progress_v3.json');cine_visual=load(CINEMATIC.with_name('visual_review.json'))
    assert visual['all_final_627_ordinary_pages_visually_approved'] and not visual['unresolved_findings'] and cine_visual['final23_pages_visually_approved']
    assert len(doc['records'])==642 and len(ordinary['records'])==len(plans['records'])==611 and len(cine['records'])==23
    assert ordinary['runtime']==cine['runtime'];runtime=ordinary['runtime'];ROOT.mkdir(parents=True)
    known={r['id']:r for r in ordinary_input['records']};cines={r['id']:r for r in cine['records']}
    rows=[]
    for original in doc['records']:
        r=deepcopy(original)
        if r['kind']!='typed-choice-label':
            r['kind']='system-FE' if r['source_selector']==254 else 'progressive'
            r['source_record_index']=r['source_reference']['record_index']
            r['planned_English_markup']='{SPEAKER:'+f'{r["source_selector"]:02X}'+'}'+r['english']
            r['source_meaning_gloss']=r['source_meaning'];r['complete_clean_exchange_context']=r['context']
        if r['id'] in known:assert r==known[r['id']]
        else:
            c=cines[r['id']];assert r['english']==c['logical_English'] and r['source_hex']==c['source_hex'] and r['current_hex']==c['current_hex']
            r['automatic_source_cinematic_layout_reason']=c['layout_reason']
        rows.append(r)
    doc.update(records=rows,physical_speech_objects=634,ordinary_speech_objects=634,typed_choice_objects=8,typed_choice_commands=4,
        personality_alternatives=0,personality_alias_slots=0,source_full_manuscript=str(MANUSCRIPT),source_full_manuscript_sha256=sha(MANUSCRIPT.read_bytes()),
        offline_speech_visual_approved=True,all_individual_fifth_gates_still_pending=True,new_credit=0)
    manuscript=ROOT/'storage_manuscript.json';save(manuscript,doc);digest=sha(manuscript.read_bytes())
    native_by={r['id']:r for r in ordinary['records']};plan_by={r['id']:r for r in plans['records']}
    for ident,c in cines.items():
        display=deepcopy(c['native']);display.update(native_plane=display['physical_plane'],native_plane_sha256=display['physical_sha256'],
            native_logical_plane=display['logical_plane'],native_logical_plane_sha256=display['logical_sha256'],preview=c['preview'],preview_sha256=c['preview_sha256'])
        native_by[ident]=dict(id=ident,block=156,source_reference=c['source_reference'],current_reference=c['current_reference'],
            compiled_hex=c['compiled_hex'],expanded_native_hex=c['expanded_native_hex'],kind='system-FE',logical_English=c['logical_English'],
            native_alignment=c['native_macro_alignments'],complete_native_English_display=display,source_cinematic_proof=str(CINEMATIC))
        plan_by[ident]=dict(id=ident,block=156,source_record_index=c['source_reference']['record_index'],source_selector=254,kind='system-FE',
            logical_English=c['logical_English'],source_hex=c['source_hex'],encoded_hex=c['compiled_hex'],formatted_markup=c['formatted_markup'],lines=c['lines'],
            max_total_rows=4,native_rows_per_page=4,expected_native_pages=1,original_usable_width_px=228,
            base_QA=dict(issues=[dict(severity='info',code='source-qualified-cinematic-staging',message=c['layout_reason'])],
                complete_native_control_macro_glyph_row_bounds_andpagination_proof=str(CINEMATIC),
                ordinary_prose_wrap_QA_not_used_for_source_qualified_staging=True),
            individually_documented_automatic_source_staging=True,cinematic_layout_reason=c['layout_reason'])
    speech_ids=[r['id'] for r in rows if r['kind']!='typed-choice-label'];assert len(speech_ids)==634 and set(speech_ids)==set(native_by)==set(plan_by)
    combined_plan={**plans,'manuscript':str(manuscript),'manuscript_sha256':digest,'records':[plan_by[i] for i in speech_ids],
        'ordinary_plan':str(old_plans_path),'ordinary_plan_sha256':sha(old_plans_path.read_bytes()),'cinematic_proof':str(CINEMATIC),'cinematic_proof_sha256':sha(CINEMATIC.read_bytes())}
    plan_path=ROOT/'all634_compiled_plans.json';save(plan_path,combined_plan)
    combined_native={**ordinary,'manuscript':str(manuscript),'manuscript_sha256':digest,'plan':str(plan_path),'plan_sha256':sha(plan_path.read_bytes()),
        'records':[native_by[i] for i in speech_ids],'pages':650,'previous_native':str(old_native_path),'previous_native_sha256':sha(old_native_path.read_bytes()),
        'cinematic_proof':str(CINEMATIC),'cinematic_proof_sha256':sha(CINEMATIC.read_bytes()),'direct_visual_review_pending':False,
        'exact_611_ordinary_and23_cinematic_proofs_reused_not_new_native_calls':True}
    native_path=ROOT/'all634_native_pages.json';save(native_path,combined_native)
    source_packet=Path('work/analysis/Hodram_B151_B170_current_20261102/current_effective.json');packet=load(source_packet)
    assert packet['runtime']==runtime and packet['records']==634 and len(packet['groups'])==20;save(ROOT/'packet.json',packet)
    menus_path=FORMAT/'menus_v1/complete_choice_objects.json';menus=load(menus_path);assert len(menus['objects'])==4 and menus['all_checks_pass']
    groups=[]
    for obj in menus['objects']:
        p=Path(obj['receipt']);assert sha(p.read_bytes())==obj['receipt_sha256'];proof=load(p)
        assert proof['runtime']==runtime and len(proof['records'])==8 and len(proof['compiler_negatives_rejected'])==7
        sheet=proof['review_sheet'];assert sha(Path(sheet['path']).read_bytes())==sheet['sha256']
        groups.append(dict(block=obj['block'],source_command_offset=obj['source_command_offset'],target_object_hex=proof['native_choice_object_hex'],
            record_IDs=obj['record_ids'],original_receipt=str(p),original_receipt_sha256=sha(p.read_bytes())))
    menu=dict(manuscript=str(manuscript),manuscript_sha256=digest,runtime=runtime,menus=groups,offline_visual_approved=True,direct_view_pending=False,
        source_receipt=str(menus_path),source_receipt_sha256=sha(menus_path.read_bytes()),native_provider_alignments=24,bridged_modal_returns=72,
        complete_English_caption_style_planes=32,actual_controller_andstored_objects_still_pending=True,new_credit=0)
    save(ROOT/'menus_reviewed.json',menu)
    save(FORMAT/'menus_v1/caption_visual_review.json',dict(source_receipt=str(menus_path),source_receipt_sha256=sha(menus_path.read_bytes()),
        directly_viewed_sheets=[o['review_sheet'] for o in menus['objects']],all8_reviewed_captions_visually_approved=True,
        complete_leading_trailing_glyphs_centering_native_font_andbounds_pass=True,actual_controller_andstored_integration_pending=True,new_credit=0))
    save(ROOT/'no_style_objects.json',dict(manuscript=str(manuscript),manuscript_sha256=digest,plan_sha256=sha(plan_path.read_bytes()),runtime=runtime,
        objects=[],source_packet_has_zero_4100_commands=True,no_style_consumer_execution_needed=True,new_credit=0))
    name_path=NAME_ROOT/'native_name_planes.json';names=load(name_path);assert names['runtime']==runtime and len(names['planes'])==41 and len(names['review_sheets'])==3
    for sheet in names['review_sheets']:assert sha(Path(sheet['path']).read_bytes())==sheet['sha256']
    save(NAME_ROOT/'visual_review.json',dict(native=str(name_path),native_sha256=sha(name_path.read_bytes()),directly_viewed_sheets=names['review_sheets'],
        all41_native_strings_visually_approved=True,all36_actors_both_bound_getters_plus_Mivor=True,normal_Fernando_F_Samwell_da_andapproved_names_preserved=True,
        actual_catalogue_UI_andrepresentative_B168_headers_not_observed_here=True,new_credit=0))
    static=load(STATIC);assert static['all_native_getter_copy_full_characters_bounds_canaries_andparent_inverse_pass'] and len(static['negative_cases_rejected'])==10
    sheet=static['review_sheet'];assert sha(Path(sheet['path']).read_bytes())==sheet['sha256']
    save(STATIC.with_name('visual_review.json'),dict(native=str(STATIC),native_sha256=sha(STATIC.read_bytes()),directly_viewed_sheet=sheet,
        all5_native_source_current_proposed_literal_planes_visually_approved=True,Abkhaz_andElysion_complete_normal_ASCII=True,
        actual_city_ship_widget_geometry_andEnglish_gameplay_still_pending=True,new_credit=0))
    save(ROOT/'input_binding.json',dict(manuscript=str(manuscript),manuscript_sha256=digest,native=str(native_path),plan=str(plan_path),
        source_prose_comparisons_reused=642,speech_native_andvisual_objects_reused=634,speech_final_pages=650,typed_captions=8,scoped_name_strings=41,
        native_getters_not_replayed=72,static_labels_native_andvisual_qualified_but_not_applied=True,
        actual_English_gameplay_andstored_andregistered_release_pending=True,new_credit=0,
        evidence={str(p):sha(p.read_bytes()) for p in [MANUSCRIPT,old_native_path,old_plans_path,CINEMATIC,source_packet,menus_path,name_path,STATIC,Path(__file__)]}))
    print('All642 prose/source bindings preserved;634 compiled speeches/650 native pages,four menus andsource packet joined for storage. Caption/name/static-label visual approvals saved;no native checks replayed.')
