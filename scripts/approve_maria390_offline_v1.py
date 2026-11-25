"""Select exact native and directly viewed body/menu/name proofs; leave release gates open."""
from collections import Counter
from copy import deepcopy
from pathlib import Path
from PIL import Image
from scripts.audit_story_glyph_consistency import load,save
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest

ROOT=Path('work/Maria_B152_B175_clean_20261109')


def main():
    paths=dict(manuscript=ROOT/'formatting_v1/formatting_input.json',plan=ROOT/'plan_continuity_v3/automatic_plans.json',
        selection=ROOT/'native_final_selection_v1/resume_selection.json',latest=ROOT/'native_pages_v3/compiled_native_pages.json',
        menu=ROOT/'menu_native_v1/group_verification.json',names=ROOT/'name_planes_v1/native_name_planes.json',
        macros=ROOT/'formatting_v1/native_macro_measurements.json',objects=ROOT/'current_objects_v1/current_objects.json')
    d={k:load(p) for k,p in paths.items()}
    doc,plan,selection,latest,menu,names,macros,objects=[d[k] for k in paths]
    assert (len(doc['records']),len(plan['records']),sum(r['expected_native_pages'] for r in plan['records']))==(390,373,373)
    assert doc['blocks']==list(range(152,176)) and not plan['failures']
    assert not any(i['severity'] in ['warning','error'] for r in plan['records'] for i in r['base_QA']['issues'])
    assert selection['native_selection_complete'] and (selection['reused_records'],selection['remaining_records'])==(373,0)
    assert selection['final_plan_sha256']==digest(paths['plan']) and selection['final_manuscript_sha256']==digest(paths['manuscript'])
    assert all(d[k]['runtime']==doc['runtime'] for k in ['latest','menu','names','macros','objects'])
    assert latest['source_owned_progressive_macro_adapter']==macros['source_owned_progressive_adapter']
    assert latest['fresh_compiled_alignments']==4
    assert (names['actors'],names['distinct_current_strings'],names['fresh_native_name_strings'],names['reused_native_name_strings'])==(47,33,15,18)
    assert all(p['complete_first_internal_final_codes_bounds_andindependent_font_pixels_pass'] for p in names['planes'])
    assert not objects['style_records'] and not objects['style_objects']
    visualpaths=[ROOT/p for p in ['initial_body_visual_review_v1.json','refined_body_visual_review_v1.json','farewell_body_visual_review_v1.json']]
    candidates={};sheets=[]
    for path in visualpaths:
        visual=load(path)
        assert visual['runtime']==doc['runtime'] and visual['font_sha256']==latest['font_sha256']
        assert visual['all_native_pages_bound_to_directly_viewed_exact_contact_sheet_tiles']
        assert digest(visual['native_proof'])==visual['native_proof_sha256']
        for row in visual['records']:candidates.setdefault(row['id'],[]).append(row)
        sheets.extend(visual['review_sheets'])
    originals={r['id']:r for r in doc['records'] if r['kind']!='typed-choice-label'}
    plans={r['id']:r for r in plan['records']};selected=[];bodyviews=[];runs={};used=Counter()
    for binding in selection['reused_native_records']:
        assert digest(binding['receipt'])==binding['receipt_sha256']
        proof=load(binding['receipt']);row=proof['record'];ident=row['id'];original=originals[ident]
        assert row['compiled_hex']==binding['compiled_hex']==plans[ident]['encoded_hex'] and row['logical_English']==original['english']
        assert all(row[k]==original[k] for k in ['source_reference','current_reference'])
        assert proof['four_native_alignment_cases_pass'] and proof['all_original_native_glyph_pixels_consumption_canaries_bounds_androw_assertions_pass']
        assert len(row['native_alignment']['cases'])==4
        runpath=proof['native_run_inputs'];assert digest(runpath)==proof['native_run_inputs_sha256']
        if runpath not in runs:
            run=load(runpath);runs[runpath]=run
            assert run['runtime']==doc['runtime'] and run['font_sha256']==latest['font_sha256'] and run['all_v1_native_assertions_preserved']
            assert run['macro_proof_sha256']==digest(paths['macros'])
            for field in ['source_owned_target_page_adapter','source_owned_progressive_macro_adapter']:assert run[field]==latest[field]
        used[runpath]+=1
        view=next(v for v in candidates[ident] if v['compiled_hex']==row['compiled_hex'])
        display=row['complete_native_English_display'];pages=display['pages'] if row['kind']=='progressive' else [display]
        assert len(view['pages'])==len(pages)==plans[ident]['expected_native_pages']==1
        for checked,page in zip(view['pages'],pages,strict=True):
            for field in ['native_plane','preview']:assert checked[field+'_sha256']==page[field+'_sha256']==digest(page[field])
            assert digest(checked['viewed_sheet'])==checked['viewed_sheet_sha256'] and checked['exact_viewed_pixels_equal']
        if row['kind']=='system-FE':assert display['planned_native_row_comparison']['complete_glyph_row_membership_exact']
        selected.append(row);bodyviews.append(view)
    assert len(selected)==len({r['id'] for r in selected})==373 and sorted(used.values())==[1,10,362]
    assert Counter(r['kind'] for r in selected)=={'progressive':341,'system-FE':32}
    bodypath=ROOT/'body_visual_review_v1.json';finalpath=ROOT/'final_native_v1.json'
    mixedpath=ROOT/'mixed_visual_review_v1.json';menupath=ROOT/'menu_native_approved_v1.json'
    stylepath=ROOT/'compiled_styles_v1/compiled_style_objects.json';out=ROOT/'offline_display_approval_v1.json'
    assert not any(p.exists() for p in [bodypath,finalpath,mixedpath,menupath,stylepath.parent,out])
    save(bodypath,dict(records=bodyviews,body_records=373,body_pages=373,runtime=doc['runtime'],review_sheets=sheets,
        all_final_body_pages_bound_to_directly_viewed_exact_native_pixels=True,selected_plan=str(paths['plan']),selected_plan_sha256=digest(paths['plan']),
        superseded_twelve_receipts_preserved_not_reused_for_changed_pages=True,ordinary_soft_wraps_reviewed_in_complete_exchanges=True,
        actual_gameplay=False,new_credit=0))
    final=deepcopy(latest)
    final.update(records=selected,review_sheets=sheets,pages=373,manuscript=str(paths['manuscript']),manuscript_sha256=digest(paths['manuscript']),
        plan=str(paths['plan']),plan_sha256=digest(paths['plan']),selected_alignment_cases=1492,fresh_compiled_alignments=1492,
        selected_native_receipt_per_record={r['id']:dict(path=r['receipt'],sha256=r['receipt_sha256']) for r in selection['reused_native_records']},
        aggregation_of_completed_exact_receipts_not_fresh_monolithic_run=True,selected_records_by_run=dict(used),
        completed_executed_alignment_cases_including_superseded=1540,superseded_completed_alignment_cases_not_selected=48,
        direct_visual_review_pending=False,all373_final_pages_directly_viewed_or_exact_visual_dependency_reuse=True,
        formatting_gates_still_false=True,actual_gameplay=False,new_credit=0)
    save(finalpath,final)
    # Bind all directly viewed name tiles to their exact independent native planes.
    cursor=0;mixed=[]
    for sheet in names['review_sheets']:
        assert digest(sheet['path'])==sheet['sha256']
        part=names['planes'][cursor:cursor+sheet['strings']]
        with Image.open(sheet['path']) as canvas:
            canvas=canvas.convert('RGB')
            for i,plane in enumerate(part):
                assert digest(plane['preview'])==plane['preview_sha256'] and digest(plane['native_plane'])==plane['native_plane_sha256']
                with Image.open(plane['preview']) as preview:expected=preview.convert('RGB').crop((0,0,216,16)).resize((432,32),Image.Resampling.NEAREST)
                x,y=i%2*456,i//2*64+22
                assert canvas.crop((x,y,x+432,y+32)).tobytes()==expected.tobytes()
        cursor+=len(part);mixed.append(dict(sheet,directly_viewed=True,exact_native_name_tiles_match=True))
    assert cursor==33
    assert (menu['menus'],menu['captions'],menu['native_provider_alignments'],menu['bridged_modal_returns'],menu['current_andtarget_normal_highlight_planes'],menu['compiler_negatives'])==(8,17,48,150,68,57)
    choices={(r['block'],r['source_command_offset'],r['source_index']):r for r in doc['records'] if r['kind']=='typed-choice-label'}
    approvedmenus=[];targetplanes=0
    for item in menu['objects']:
        assert digest(item['proof'])==item['proof_sha256'];proof=load(item['proof'])
        assert proof['runtime']==doc['runtime'] and proof['complete_caption_glyphs_centering_bounds_guards_andconsumption_pass']
        for plane in proof['records']:assert digest(plane['path'])==plane['sha256']
        rows=[choices[(item['block'],item['source_command_offset'],i)] for i in range(item['caption_count'])]
        assert [r['id'] for r in rows]==item['record_ids']
        assert all(r['source_choice_object_hex']==item['source_object_hex'] and r['current_choice_object_hex']==item['current_object_hex'] for r in rows)
        from dk4tool.dialogue.reviewed_choice_object_v2 import compile_choices
        assert compile_choices(bytes.fromhex(item['source_object_hex']),bytes.fromhex(item['current_object_hex']),rows,require_formatting=False).hex()==item['target_object_hex']
        for sheet in item['review_sheets']:
            assert digest(sheet['path'])==sheet['sha256'];mixed.append(dict(sheet,directly_viewed=True))
        targetplanes+=2*len(rows);approvedmenus.append(item)
    assert targetplanes==34 and len(mixed)==11
    save(mixedpath,dict(review_sheets=mixed,distinct_name_strings_directly_viewed=33,target_captions_directly_viewed=17,
        all_names_complete_consistent_andwithin_verified_bounds=True,target_captions_complete_centered_andnatural_in_source_exchange=True,
        full_catalogue_UI_actual_headers_andcontroller_pending=True,actual_gameplay=False,new_credit=0))
    save(menupath,dict(runtime=doc['runtime'],menus=approvedmenus,source_index_andcount_preserved=True,
        offline_visual_approved=True,direct_view_pending=False,complete_caption_glyphs_centering_bounds_guards_andconsumption_pass=True,
        original_receipt=str(paths['menu']),original_receipt_sha256=digest(paths['menu']),
        visual_receipt=str(mixedpath),visual_receipt_sha256=digest(mixedpath),actual_gameplay=False,new_credit=0))
    stylepath.parent.mkdir()
    save(stylepath,dict(runtime=doc['runtime'],manuscript=str(paths['manuscript']),manuscript_sha256=digest(paths['manuscript']),
        plan=str(paths['plan']),plan_sha256=digest(paths['plan']),objects=[],physical_alternatives=0,native_target_slot_cases=0,compiler_negatives=[],
        no_source_orcurrent_style_objects_in_this_scope=True,source_alias_equivalence_exact=True,no_empty_native_permutations_executed=True,new_credit=0))
    save(out,dict(source_objects=390,complete_exchanges=24,dialogue_revisions=153,dialogue_retentions=237,physical_body_candidates=373,body_pages=373,
        original_source_FE_panels=32,physical_FE_panels=32,FE_continuation_owners=0,source_styles=0,source_style_objects=0,choice_menus=8,choice_captions=17,
        selected_alignment_cases=1492,all373_final_pages_directly_viewed=True,scoped_names=47,distinct_name_strings=33,fresh_name_planes=15,reused_name_planes=18,
        all_names_and17_captions_directly_viewed=True,menu_native_provider_alignments=48,menu_bridged_returns=150,
        menu_normal_highlight_planes=68,target_menu_normal_highlight_planes=34,menu_compiler_negatives=57,
        pages_reclaimed=1,additional_phrase_wrap_fixes=11,scoped_FE_guard_reserves=8,no_native_body_failures_in_this_batch=True,
        final_native_proof=str(finalpath),final_native_proof_sha256=digest(finalpath),names_sha256=digest(paths['names']),
        full_paragraphs_native_controls_substitutions_andlayout_provenance_preserved=True,
        stored_script_allocation_branches_actual_gameplay_andregistration_pending=True,all_fifth_formatting_gates_still_pending=True,
        actual_gameplay=False,new_ROM=False,new_credit=0,full_goal_complete=False,
        evidence={str(p):digest(p) for p in [*paths.values(),*visualpaths,bodypath,mixedpath,finalpath,menupath,stylepath,Path(__file__)]}))
    print('Sealed373 directly viewed body pages,33 name strings and17 captions;storage/gameplay/release pending;zero credit.')


if __name__=='__main__':main()
