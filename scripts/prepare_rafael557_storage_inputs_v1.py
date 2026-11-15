"""Bind completed native/visual evidence to the exact 557-object storage input."""
from collections import Counter
from copy import deepcopy
from pathlib import Path
from scripts.audit_story_glyph_consistency import load,save
from dk4tool.patch.grand_race_menu_release import sha

ROOT=Path('work/analysis/Rafael557_storage_inputs_v1_20261105')
DOC=Path('translations/rafael_B141_B160_formatting_manuscript_v3.json')
PLAN=Path('work/analysis/Rafael557_automatic_plans_v10_20261105/automatic_plans.json')
NATIVE=Path('work/analysis/Rafael557_native_final_v1_20261105/compiled_native_pages.json')
BODY=Path('work/analysis/Rafael557_body_visual_review_v1_20261105/body_visual_review.json')
FRESH=Path('work/analysis/Rafael557_remaining_native_v1_20261105/compiled_native_pages.json')
MENUS=Path('work/analysis/Rafael557_two_choice_v1_20261105/complete_choice_objects.json')
CAPTIONS=Path('work/analysis/Rafael557_all_caption_styles_v1_20261105/receipt.json')
NAMES=Path('work/analysis/Rafael557_name_planes_v1_20261105/native_name_planes.json')
IDENTITY=Path('work/analysis/Rafael557_macros_inputs_v1_20261105/qualified_identity_andmacros.json')
CURRENT=Path('work/analysis/Rafael_B141_B160_current867_20261105/current_effective.json')

if __name__=='__main__':
    assert not ROOT.exists()
    doc,plan,native,body,fresh,menu,captions,names,identity,current=map(load,[DOC,PLAN,NATIVE,BODY,FRESH,MENUS,CAPTIONS,NAMES,IDENTITY,CURRENT])
    assert len(doc['records'])==557 and len(native['records'])==len(plan['records'])==549 and native['pages']==558
    assert native['manuscript_sha256']==plan['manuscript_sha256']==sha(DOC.read_bytes())
    assert native['plan_sha256']==body['final_plan_sha256']==sha(PLAN.read_bytes()) and not plan['failures']
    assert body['native_sha256']==sha(NATIVE.read_bytes()) and body['all558_final_body_pages_directly_viewed']
    assert len(body['records'])==549 and len(body['directly_opened_readable_sheets'])==42
    assert all(d['runtime']==current['runtime'] for d in [native,fresh,names,identity])
    assert identity['complete_ARM9_COMMON_font_andactor0_macro_dependencies_qualified']
    assert identity['macro_ascii_lengths']['FU']==13 and identity['macro_widths']['FU']==78 and not identity['dynamic_roles']
    assert menu['all_checks_pass'] and menu['physical_caption_records']==8 and len(menu['objects'])==4
    assert names['scoped_actors']==names['distinct_strings']==20 and names['fresh_name_planes']==11 and names['exact_reused_name_planes']==9
    assert captions['planes']==32
    assert all(r['review']==dict(source=True,context=True,localization=True,naturalness=True,formatting=False) for r in doc['records'])
    counts=Counter(c['word'] for g in current['groups'] for c in g['all_source_commands'])
    assert counts==Counter(c['word'] for g in current['groups'] for c in g['all_current_commands'])
    assert (counts[0x4000],counts[0x4100],counts[0x2100],counts[0x2200],counts[0x2000])==(549,0,4,0,5)
    sheets=[];proofs=[];menu_rows=[];planes=[]
    for obj in menu['objects']:
        path=Path(obj['receipt']);proof=load(path);proofs.append(path)
        assert sha(path.read_bytes())==obj['receipt_sha256'] and proof['runtime']==current['runtime']
        original_path=Path(proof['manuscript']);original=load(original_path)
        assert proof['manuscript_sha256']==sha(original_path.read_bytes())
        selected=[r for r in doc['records'] if r['id'] in obj['record_ids']]
        assert len(selected)==2 and original['records']==selected
        assert proof['complete_caption_glyphs_centering_bounds_guards_andconsumption_pass'] and len(proof['compiler_negatives_rejected'])==7
        assert proof['native_provider_alignments']==6 and proof['bridged_modal_returns']==18 and len(proof['records'])==8
        assert bytes.fromhex(proof['native_choice_object_hex'])==Path(obj['compiled_path']).read_bytes()
        sheets.append(proof['review_sheet']);planes.extend(proof['records'])
        menu_rows.append(dict(block=obj['block'],source_command_offset=obj['source_command_offset'],record_IDs=obj['record_ids'],
            versions=proof['versions'],target_object_hex=proof['native_choice_object_hex'],native_proof=str(path),native_proof_sha256=sha(path.read_bytes())))
    sheets.append(dict(path=captions['sheet'],sha256=captions['sheet_sha256']))
    sheets+=names['review_sheets'];assert len(sheets)==7
    for s in [*sheets,*body['directly_opened_readable_sheets']]:assert sha(Path(s['path']).read_bytes())==s['sha256']
    for key in ['source_owned_target_page_adapter','source_owned_progressive_macro_adapter','source_owned_FE_expected_value_adapter','FE_factory_calibration']:
        native[key]=deepcopy(fresh[key])
    native['dynamic_role_bindings']={}
    ROOT.mkdir(parents=True)
    approval=ROOT/'complete_offline_visual_andinventory_review.json'
    save(approval,dict(body_review=str(BODY),body_review_sha256=sha(BODY.read_bytes()),all558_body_pages_directly_viewed=True,
        four_menu_sheets_all32_caption_states_andtwo_public_name_sheets_directly_viewed=True,menu_andname_sheets=sheets,
        source_visual_review_completed_in_preceding_checkpoint=True,public_names_only_not_two_fullcatalogue_particle_fixes=True,
        command_kind_counts={f'{k:04x}':v for k,v in sorted(counts.items())},
        complete_source_object_census=dict(ordinary=549,physical_style=0,alias_slots=0,choice_labels=8,style_objects=0,choice_objects=4,label_free_2000_controls=5),
        stored_actual_andregistered_release_pending=True,all_fifth_gates_still_false=True,actual_gameplay=False,new_credit=0))
    planpath=ROOT/'plans.json';save(planpath,plan)
    native.update(plan=str(planpath),plan_sha256=sha(planpath.read_bytes()),direct_visual_review_pending=False,
        all549_body_layouts_approved=True,all558_complete_pages_directly_viewed=True,review_sheets=body['directly_opened_readable_sheets'],
        native_adapters_reused_from=str(FRESH),native_adapters_reused_from_sha256=sha(FRESH.read_bytes()),
        source_visual_approval=str(approval),source_visual_approval_sha256=sha(approval.read_bytes()),
        no_repeated_body_rendering_ornew_gameplay_claim=True)
    save(ROOT/'native.json',native)
    save(ROOT/'styles.json',dict(manuscript=str(DOC),manuscript_sha256=sha(DOC.read_bytes()),plan=str(planpath),plan_sha256=sha(planpath.read_bytes()),
        runtime=current['runtime'],objects=[],native_target_slot_cases=0,physical_alternatives=0,
        complete_clean_current_census_proves_no4100_objects=True,no_style_native_execution_claim=True,source_visual_approval=str(approval),new_credit=0))
    save(ROOT/'menu.json',dict(manuscript=str(DOC),manuscript_sha256=sha(DOC.read_bytes()),runtime=current['runtime'],menus=menu_rows,records=planes,
        native_provider_alignments=24,bridged_modal_returns=72,complete_English_caption_style_planes=32,
        complete_caption_glyphs_centering_bounds_guards_andconsumption_pass=True,direct_view_pending=False,offline_visual_approved=True,
        review_sheets=sheets[:5],source_visual_approval=str(approval),source_visual_approval_sha256=sha(approval.read_bytes()),actual_gameplay=False,new_credit=0,
        evidence={str(p):sha(p.read_bytes()) for p in [MENUS,CAPTIONS,*proofs,approval,Path(__file__)]}))
    save(ROOT/'qualified_public_names.json',{**names,'direct_visual_review_pending':False,'offline_visual_approved':True,
        'source_visual_approval':str(approval),'source_visual_approval_sha256':sha(approval.read_bytes())})
    save(ROOT/'input_qualification.json',dict(manuscript=str(DOC),manuscript_sha256=sha(DOC.read_bytes()),all557_four_prose_gates_andcomplete_offline_display=True,
        stored_actual_fullcatalogue_particles_andregistered_work_still_pending=True,new_credit=0,
        evidence={str(p):sha(p.read_bytes()) for p in [DOC,PLAN,NATIVE,BODY,FRESH,MENUS,CAPTIONS,NAMES,IDENTITY,CURRENT,approval,Path(__file__)]}))
    print('Qualified557 objects:549 bodies/558 viewed pages,8 captions/four menus,20 public names;no4100 objects. Stored/gameplay/release remain.')
