"""Select exact native/visual/menu/name/style proofs; leave stored and gameplay gates open."""
import argparse
from collections import Counter
from copy import deepcopy
from pathlib import Path
from PIL import Image
from dk4tool.dialogue.reviewed_choice_object_v2 import compile_choices
from dk4tool.dialogue.reviewed_actor_style_object_v1 import compile_styles
from scripts.audit_story_glyph_consistency import load,save
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest


def main():
    ap=argparse.ArgumentParser(description=__doc__)
    for key in ['root','plan','latest-native','FE-calibration']:ap.add_argument('--'+key,type=Path,required=True)
    ap.add_argument('--visual',type=Path,nargs='+',required=True)
    ap.add_argument('--expected-records',type=int,required=True);ap.add_argument('--expected-pages',type=int,required=True)
    args=ap.parse_args();root=args.root
    paths=dict(manuscript=root/'formatting_v1/formatting_input.json',plan=args.plan,
        selection=root/'native_final_selection_v1/resume_selection.json',latest=args.latest_native,calibration=args.FE_calibration,
        menu=root/'menu_native_v1/group_verification.json',names=root/'name_planes_v1/native_name_planes.json',
        mixed=root/'mixed_visual_review_v1.json',styles=root/'compiled_styles_v1/compiled_style_objects.json',
        macros=root/'formatting_v1/native_macro_measurements.json',objects=root/'current_objects_v1/current_objects.json')
    data={k:load(p) for k,p in paths.items()}
    doc,plan,selection,latest,calibration,menu,names,mixed,styles,macros,objects=[data[k] for k in paths]
    assert len(doc['records'])==args.expected_records and not plan['failures']
    assert plan['manuscript_sha256']==digest(paths['manuscript'])
    assert not any(i['severity'] in ['error','warning'] for row in plan['records'] for i in row['base_QA']['issues'])
    assert all(d['runtime']==doc['runtime'] for d in [latest,calibration,menu,names,mixed,styles,macros,objects])
    assert calibration['font_sha256']==latest['font_sha256'] and not calibration['FE_factory_calibration'].get('not_executed_no_FE_records')
    assert selection['native_selection_complete'] and selection['remaining_records']==0
    assert selection['final_plan_sha256']==digest(paths['plan']) and selection['final_manuscript_sha256']==digest(paths['manuscript'])
    originals={r['id']:r for r in doc['records'] if r['kind']!='typed-choice-label'}
    plans={r['id']:r for r in plan['records']};assert originals.keys()==plans.keys()
    assert selection['reused_records']==len(originals) and sum(p['expected_native_pages'] for p in plans.values())==args.expected_pages
    candidates={};sheets=[]
    for path in args.visual:
        visual=load(path);assert visual['runtime']==doc['runtime'] and visual['font_sha256']==latest['font_sha256']
        assert visual['all_native_pages_bound_to_directly_viewed_exact_contact_sheet_tiles']
        assert digest(visual['native_proof'])==visual['native_proof_sha256']
        for row in visual['records']:candidates.setdefault(row['id'],[]).append(row)
        for sheet in visual['review_sheets']:
            assert sheet['directly_viewed'] and digest(sheet['path'])==sheet['sha256'];sheets.append(sheet)
    selected=[];views=[];runs={};used=Counter()
    for binding in selection['reused_native_records']:
        assert digest(binding['receipt'])==binding['receipt_sha256'];proof=load(binding['receipt']);row=proof['record'];key=row['id']
        assert proof['four_native_alignment_cases_pass'] and proof['all_original_native_glyph_pixels_consumption_canaries_bounds_androw_assertions_pass']
        assert row['compiled_hex']==binding['compiled_hex']==plans[key]['encoded_hex'] and row['logical_English']==originals[key]['english']
        assert all(row[k]==originals[key][k] for k in ['source_reference','current_reference']) and len(row['native_alignment']['cases'])==4
        runpath=proof['native_run_inputs'];assert digest(runpath)==proof['native_run_inputs_sha256']
        if runpath not in runs:
            run=load(runpath);runs[runpath]=run
            assert run['runtime']==doc['runtime'] and run['font_sha256']==latest['font_sha256'] and run['all_v1_native_assertions_preserved']
            assert run['macro_proof_sha256']==digest(paths['macros'])
            for k in ['source_owned_target_page_adapter','source_owned_progressive_macro_adapter']:assert run[k]==latest[k]
        used[runpath]+=1
        view=next(v for v in candidates[key] if v['compiled_hex']==row['compiled_hex'])
        display=row['complete_native_English_display'];pages=display['pages'] if row['kind']=='progressive' else [display]
        assert len(pages)==len(view['pages'])==plans[key]['expected_native_pages']
        if row['kind']=='progressive':
            assert display['all_visible_first_internal_final_characters_in_order'] and display['no_blank_or_overlap_page']
            assert display['complete_consumed_bytes']==len(bytes.fromhex(row['expanded_native_hex']))
            assert all(p['native_independent_plane_equal'] and p['all_bitmap_header_input_canaries_exact'] for p in pages)
        else:
            assert display['all_first_internal_final_ASCII_CP932_codes_andindependent_logical_plane_exact']
            assert display['input_bitmap_header_view_context_canaries_andcomplete_return_exact'] and display['all_executed_instructions_exact_current_sections_andpayload']
            assert display['planned_native_row_comparison']['complete_glyph_row_membership_exact']
        for viewed,page in zip(view['pages'],pages,strict=True):
            for k in ['native_plane','preview']:assert viewed[k+'_sha256']==page[k+'_sha256']==digest(page[k])
            assert digest(viewed['viewed_sheet'])==viewed['viewed_sheet_sha256'] and viewed['exact_viewed_pixels_equal']
        selected.append(row);views.append(view)
    assert len(selected)==len(originals) and sum(len(v['pages']) for v in views)==args.expected_pages
    assert mixed['all_names_andcaptions_directly_viewed'] and mixed['distinct_name_strings']==len(names['planes'])
    cursor=0
    for sheet in names['review_sheets']:
        assert digest(sheet['path'])==sheet['sha256'];part=names['planes'][cursor:cursor+sheet['strings']]
        with Image.open(sheet['path']) as canvas:
            canvas=canvas.convert('RGB')
            for i,plane in enumerate(part):
                assert plane['complete_first_internal_final_codes_bounds_andindependent_font_pixels_pass']
                assert digest(plane['native_plane'])==plane['native_plane_sha256'] and digest(plane['preview'])==plane['preview_sha256']
                with Image.open(plane['preview']) as preview:expected=preview.convert('RGB').crop((0,0,216,16)).resize((432,32),Image.Resampling.NEAREST)
                x,y=i%2*456,i//2*64+22;assert canvas.crop((x,y,x+432,y+32)).tobytes()==expected.tobytes()
        cursor+=len(part)
    assert cursor==names['distinct_current_strings']
    choices={(r['block'],r['source_command_offset'],r['source_index']):r for r in doc['records'] if r['kind']=='typed-choice-label'}
    approvedmenus=[]
    for item in menu['objects']:
        assert digest(item['proof'])==item['proof_sha256'];proof=load(item['proof'])
        assert proof['runtime']==doc['runtime'] and proof['complete_caption_glyphs_centering_bounds_guards_andconsumption_pass']
        for plane in proof['records']:assert digest(plane['path'])==plane['sha256']
        rows=[choices[(item['block'],item['source_command_offset'],i)] for i in range(item['caption_count'])]
        assert [r['id'] for r in rows]==item['record_ids']
        assert compile_choices(bytes.fromhex(item['source_object_hex']),bytes.fromhex(item['current_object_hex']),rows,require_formatting=False).hex()==item['target_object_hex']
        for sheet in item['review_sheets']:assert digest(sheet['path'])==sheet['sha256']
        approvedmenus.append(item)
    assert sum(m['caption_count'] for m in approvedmenus)==len(choices)==menu['captions']
    style_rows=[r for r in doc['records'] if r.get('native_object_kind')=='4100-style-alternative']
    assert len(style_rows)==styles['physical_alternatives']==len(objects['style_records'])
    assert len(styles['objects'])==len(objects['style_objects']) and styles['native_target_slot_cases']==8*len(styles['objects'])
    for item in styles['objects']:
        rows=sorted([r for r in style_rows if r['block']==item['block'] and r['source_command_offset']==item['source_command_offset']],key=lambda r:r['source_reference']['offset'])
        assert [r['id'] for r in rows]==item['physical_record_IDs']
        assert compile_styles(bytes.fromhex(item['source_object_hex']),bytes.fromhex(item['current_object_hex']),rows,plans,require_formatting=False).hex()==item['target_object_hex']
        assert digest(item['target_path'])==item['target_sha256']
        assert all(bytes.fromhex(plans[s['record_id']]['encoded_hex'])[1:].hex()==s['target_hex'] for s in item['native_slots'])
    assert sum(len(n['rejected']) for n in styles['compiler_negatives'])==9*len(styles['objects'])
    bodypath=root/'body_visual_review_v1.json';finalpath=root/'final_native_v1.json';menupath=root/'menu_native_approved_v1.json'
    stylepath=root/'compiled_styles_v2/compiled_style_objects.json';out=root/'offline_display_approval_v1.json'
    assert not any(p.exists() for p in [bodypath,finalpath,menupath,stylepath.parent,out])
    save(bodypath,dict(records=views,body_records=len(views),body_pages=args.expected_pages,runtime=doc['runtime'],review_sheets=sheets,
        all_final_body_pages_bound_to_directly_viewed_exact_native_pixels=True,selected_plan=str(args.plan),selected_plan_sha256=digest(args.plan),
        historical_visual_proofs_reused_only_for_exact_compiled_bytes_andplanes=True,actual_gameplay=False,new_credit=0))
    final=deepcopy(latest);final.update(records=selected,pages=args.expected_pages,blocks=doc['blocks'],review_sheets=sheets,
        manuscript=str(paths['manuscript']),manuscript_sha256=digest(paths['manuscript']),plan=str(args.plan),plan_sha256=digest(args.plan),
        selected_alignment_cases=4*len(selected),fresh_compiled_alignments=latest['fresh_compiled_alignments'],
        current_version_fresh_records=len(latest['records']),current_version_exact_reused_records=len(selected)-len(latest['records']),
        current_version_fresh_alignment_cases=latest['fresh_compiled_alignments'],current_version_reused_alignment_cases=4*(len(selected)-len(latest['records'])),
        selected_records_by_run=dict(used),FE_factory_calibration=calibration['FE_factory_calibration'],
        FE_calibration_exact_compatible_proof=str(paths['calibration']),FE_calibration_exact_compatible_proof_sha256=digest(paths['calibration']),
        selected_native_receipt_per_record={r['id']:dict(path=r['receipt'],sha256=r['receipt_sha256']) for r in selection['reused_native_records']},
        aggregation_of_completed_exact_receipts_not_fresh_monolithic_run=True,direct_visual_review_pending=False,
        all_final_pages_directly_viewed_or_exact_visual_dependency_reuse=True,formatting_gates_still_false=True,actual_gameplay=False,new_credit=0)
    save(finalpath,final)
    save(menupath,dict(runtime=doc['runtime'],manuscript=str(paths['manuscript']),manuscript_sha256=digest(paths['manuscript']),menus=approvedmenus,
        source_index_andcount_preserved=True,offline_visual_approved=True,direct_view_pending=False,
        complete_caption_glyphs_centering_bounds_guards_andconsumption_pass=True,original_receipt=str(paths['menu']),original_receipt_sha256=digest(paths['menu']),
        visual_receipt=str(paths['mixed']),visual_receipt_sha256=digest(paths['mixed']),actual_gameplay=False,new_credit=0))
    stylepath.parent.mkdir();save(stylepath,{**styles,'manuscript':str(paths['manuscript']),'manuscript_sha256':digest(paths['manuscript']),
        'plan':str(args.plan),'plan_sha256':digest(args.plan),'exact_prior_native_slot_and27_compiler_negative_cases_reused':True,
        'original_proof':str(paths['styles']),'original_proof_sha256':digest(paths['styles']),
        'complete_source_current_alias_target_body_andfinal_plan_recompiled_exact':True,'no_native_slot_ornegative_cases_reexecuted':True})
    evidence={str(p):digest(p) for p in [*paths.values(),*args.visual,bodypath,finalpath,menupath,stylepath,Path(__file__)]}
    save(out,dict(source_objects=len(doc['records']),complete_exchanges=doc['complete_exchanges'],dialogue_revisions=doc['proposed_revisions'],dialogue_retentions=doc['justified_retentions'],
        physical_body_candidates=len(selected),body_pages=args.expected_pages,selected_alignment_cases=4*len(selected),
        all_final_body_pages_directly_viewed=True,source_styles=len(style_rows),source_style_objects=len(styles['objects']),
        style_slot_cases=styles['native_target_slot_cases'],style_compiler_negatives=9*len(styles['objects']),
        choice_menus=menu['menus'],choice_captions=menu['captions'],scoped_names=names['actors'],distinct_name_strings=names['distinct_current_strings'],
        fresh_name_planes=names['fresh_native_name_strings'],reused_name_planes=names['reused_native_name_strings'],names_sha256=digest(paths['names']),
        all_names_andcaptions_directly_viewed=True,menu_native_provider_alignments=menu['native_provider_alignments'],menu_bridged_returns=menu['bridged_modal_returns'],
        menu_normal_highlight_planes=menu['current_andtarget_normal_highlight_planes'],target_menu_normal_highlight_planes=menu['target_normal_highlight_planes'],
        menu_compiler_negatives=menu['compiler_negatives'],final_native_proof=str(finalpath),final_native_proof_sha256=digest(finalpath),
        all_native_controls_substitutions_words_glyphs_bounds_andpagination_pass=True,
        stored_script_allocation_branches_actual_gameplay_andregistration_pending=True,all_fifth_formatting_gates_still_pending=True,
        actual_gameplay=False,new_ROM=False,new_credit=0,full_goal_complete=False,evidence=evidence))
    print(dict(body_records=len(selected),pages=args.expected_pages,source_styles=len(style_rows),captions=menu['captions'],name_strings=names['distinct_current_strings'],offline_display_pass=True,storage_gameplay_release_pending=True,new_credit=0))


if __name__=='__main__':main()
