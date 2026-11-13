"""Qualify all viewed bodies, menus and public names for the complete mixed-scene rebuild."""
from collections import Counter
from copy import deepcopy
from pathlib import Path
from scripts.audit_story_glyph_consistency import load,save
from dk4tool.patch.grand_race_menu_release import sha

ROOT=Path('work/analysis/Rafael351_storage_inputs_v1_20261105')
DOC=Path('translations/rafael_B121_B140_consumer_manuscript_v5.json')
INPUT=Path('work/analysis/Rafael351_consumer_inputs_v1_20261105')
BODY=Path('work/analysis/Rafael351_body_visual_review_v1_20261105/body_visual_review.json')
FRESH=Path('work/analysis/Rafael351_native_v2_20261105/compiled_native_pages.json')
MENUS=Path('work/analysis/Rafael351_choice_objects_v2_20261105/complete_choice_objects.json')
NAMES=Path('work/analysis/Rafael351_name_planes_v1_20261105/native_name_planes.json')
CURRENT=Path('work/analysis/Rafael_B121_B140_current678_20261105/current_effective.json')

if __name__=='__main__':
    assert not ROOT.exists()
    doc,plan,native,styles,identity,body,fresh,menu,names,current=map(load,[DOC,INPUT/'plans.json',INPUT/'native.json',INPUT/'styles.json',INPUT/'qualified_identity.json',BODY,FRESH,MENUS,NAMES,CURRENT])
    assert len(doc['records'])==351 and len(native['records'])==341 and native['pages']==344
    assert all(d['runtime']==current['runtime'] for d in [native,styles,identity,fresh,names])
    assert body['all344_final_body_pages_directly_viewed'] and len(body['directly_opened_readable_sheets'])==30
    assert body['native_sha256']==sha(Path(body['native']).read_bytes())
    original_body=load(body['native']);assert original_body['records']==native['records']
    assert menu['all_checks_pass'] and menu['physical_caption_records']==10 and len(menu['objects'])==5
    assert names['scoped_actors']==names['distinct_strings']==22 and names['fresh_name_planes']==8 and names['exact_reused_name_planes']==14
    assert len(styles['objects'])==6 and styles['native_target_slot_cases']==48 and styles['physical_alternatives']==34
    assert sum(len(x['rejected']) for x in styles['compiler_negatives'])==54
    sheets=[];proofs=[];menu_rows=[];planes=[]
    for obj in menu['objects']:
        path=Path(obj['receipt']);proof=load(path);proofs.append(path)
        assert sha(path.read_bytes())==obj['receipt_sha256'] and proof['runtime']==current['runtime']
        assert proof['complete_caption_glyphs_centering_bounds_guards_andconsumption_pass'] and len(proof['compiler_negatives_rejected'])==7
        assert proof['native_provider_alignments']==6 and proof['bridged_modal_returns']==18 and len(proof['records'])==8
        assert bytes.fromhex(proof['native_choice_object_hex'])==Path(obj['compiled_path']).read_bytes()
        sheets.append(proof['review_sheet']);planes.extend(proof['records'])
        menu_rows.append(dict(block=obj['block'],source_command_offset=obj['source_command_offset'],record_IDs=obj['record_ids'],
            versions=proof['versions'],target_object_hex=proof['native_choice_object_hex'],native_proof=str(path),native_proof_sha256=sha(path.read_bytes())))
    sheets+=names['review_sheets'];assert len(sheets)==7
    for s in sheets:assert sha(Path(s['path']).read_bytes())==s['sha256']
    counts=Counter(c['word'] for g in current['groups'] for c in g['all_source_commands'])
    assert counts==Counter(c['word'] for g in current['groups'] for c in g['all_current_commands'])
    assert (counts[0x4000],counts[0x4100],counts[0x2100],counts[0x2200])==(307,6,5,0)
    assert all(r['review']==dict(source=True,context=True,localization=True,naturalness=True,formatting=False) for r in doc['records'])
    for key in ['source_owned_target_page_adapter','source_owned_progressive_macro_adapter','source_owned_FE_expected_value_adapter','FE_factory_calibration']:
        assert key in fresh
        native[key]=deepcopy(fresh[key])
    native['dynamic_role_bindings']={str(r['source_selector']):r['resolved_actor_ID'] for r in identity['dynamic_roles']}
    assert set(map(int,native['dynamic_role_bindings']))=={207,208,209,214,215,220}
    ROOT.mkdir(parents=True)
    approval=ROOT/'complete_offline_visual_andinventory_review.json'
    save(approval,dict(body_review=str(BODY),body_review_sha256=sha(BODY.read_bytes()),all344_body_pages_directly_viewed=True,
        all5_menu_sheets_and2_public_name_sheets_directly_viewed=True,menu_andname_sheets=sheets,
        public_names_only_not_two_fullcatalogue_particle_fixes=True,command_kind_counts={f'{k:04x}':v for k,v in sorted(counts.items())},
        complete_source_object_census=dict(ordinary=307,physical_style=34,alias_slots=48,choice_labels=10,style_objects=6,choice_objects=5),
        stored_actual_andregistered_release_pending=True,all_fifth_gates_still_false=True,actual_gameplay=False,new_credit=0))
    planpath=ROOT/'plans.json';save(planpath,plan)
    for d in [native,styles]:d.update(plan=str(planpath),plan_sha256=sha(planpath.read_bytes()))
    native.update(direct_visual_review_pending=False,all341_body_layouts_approved=True,all344_complete_pages_directly_viewed=True,
        full351_object_batch_offline_display_complete=True,review_sheets=body['directly_opened_readable_sheets'],
        native_adapters_reused_from=str(FRESH),native_adapters_reused_from_sha256=sha(FRESH.read_bytes()),
        full_dynamic_role_bindings_from=str(INPUT/'qualified_identity.json'),full_dynamic_role_bindings_from_sha256=sha((INPUT/'qualified_identity.json').read_bytes()),
        source_visual_approval=str(approval),source_visual_approval_sha256=sha(approval.read_bytes()),
        no_repeated_body_rendering_ornew_gameplay_claim=True)
    save(ROOT/'native.json',native);save(ROOT/'styles.json',styles)
    save(ROOT/'menu.json',dict(manuscript=str(DOC),manuscript_sha256=sha(DOC.read_bytes()),runtime=current['runtime'],
        menus=menu_rows,records=planes,native_provider_alignments=30,bridged_modal_returns=90,complete_English_caption_style_planes=40,
        complete_caption_glyphs_centering_bounds_guards_andconsumption_pass=True,
        direct_view_pending=False,offline_visual_approved=True,review_sheets=sheets[:5],source_visual_approval=str(approval),
        source_visual_approval_sha256=sha(approval.read_bytes()),actual_gameplay=False,new_credit=0,
        evidence={str(p):sha(p.read_bytes()) for p in [MENUS,*proofs,approval,Path(__file__)]}))
    save(ROOT/'qualified_public_names.json',{**names,'direct_visual_review_pending':False,'offline_visual_approved':True,
        'source_visual_approval':str(approval),'source_visual_approval_sha256':sha(approval.read_bytes())})
    save(ROOT/'input_qualification.json',dict(manuscript=str(DOC),manuscript_sha256=sha(DOC.read_bytes()),
        all351_source_objects_four_prose_gates_andcomplete_offline_display=True,
        all_storage_actual_fullcatalogue_particles_andregistered_work_still_pending=True,new_credit=0,
        evidence={str(p):sha(p.read_bytes()) for p in [DOC,INPUT/'input_qualification.json',BODY,FRESH,MENUS,NAMES,CURRENT,approval,Path(__file__)]}))
    print('Qualified351 source objects:344 viewed body pages,10 captions/five menus,22 public names,six style objects/48 slots. No repeated body checks;stored/gameplay/release work remains.')
