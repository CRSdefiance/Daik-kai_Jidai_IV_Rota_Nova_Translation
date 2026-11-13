"""Seal the viewed final pages and source-bound voice/menu inputs for storage checks."""
from copy import deepcopy
from pathlib import Path
from scripts.audit_story_glyph_consistency import load,save
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest
from scripts.prepare_hodram_B281_B300_formatting_v1 import ROOT,FORMATTING as DOC
from scripts.review_hodram_B281_B300_contextual_v1 import CURRENT

PLAN=ROOT/'formatting_v1/visual_plan_v5/automatic_plans.json'
NATIVE=ROOT/'final_native_v5/compiled_native_pages.json'
STYLES=ROOT/'native_styles_v5/compiled_style_objects.json'
VIEW=ROOT/'final_visual_approval_v5.json'
OUT=ROOT/'storage_inputs_v5'

def main():
    assert not VIEW.exists() and not OUT.exists()
    initialpath=ROOT/'initial_visual_review_v2.json'
    retentionpath=ROOT/'layout_trial_retentions_v5.json'
    namespath=ROOT/'name_planes_v2/native_name_planes.json'
    doc,plan,native,styles,initial,delta,sheets,names,retentions=map(load,(DOC,PLAN,NATIVE,STYLES,initialpath,
        ROOT/'layout_delta_v5/delta.json',ROOT/'changed_body_sheets_v5/sheet_index.json',namespath,retentionpath))
    assert len(doc['records'])==384 and len(plan['records'])==len(native['records'])==373 and native['pages']==374
    assert plan['manuscript_sha256']==native['manuscript_sha256']==styles['manuscript_sha256']==digest(DOC)
    assert native['plan_sha256']==styles['plan_sha256']==digest(PLAN)
    assert native['all_first_internal_final_glyph_codes_pixels_input_canaries_andbounds_pass'] and native['complete_consumption_andpagination_exact']
    assert native['all_current_placement_alignments']==1492 and native['current_version_fresh_alignments']==112
    assert not plan['failures'] and not any(i['severity'] in ('error','warning') for r in plan['records'] for i in r['base_QA']['issues'])
    assert initial['all375_initial_body_pages_directly_viewed'] and initial['all_five_menu_sheets_directly_viewed']
    nameview=load(ROOT/'scoped_names_visual_approval_v1.json')
    assert nameview['all17_name_strings_directly_viewed'] and nameview['native_sha256']==digest(namespath)
    assert len(delta['changed_record_IDs'])==28 and delta['fresh_pages']==29
    assert len(sheets['sheets'])==2 and sum(len(s['included']) for s in sheets['sheets'])==29
    for sheet in initial['body_sheets']+initial['menu_sheets']+sheets['sheets']+nameview['sheets']:
        assert digest(sheet['path'])==sheet['sha256']
    after={r['id']:r for r in plan['records']}
    assert styles['physical_alternatives']==131 and styles['native_target_slot_cases']==144
    assert styles['changed_voice_objects']==11 and styles['exact_reused_voice_objects']==7
    for obj in styles['objects']:
        assert digest(obj['target_path'])==obj['target_sha256']
        for slot in obj['native_slots']:
            assert slot['target_hex']==bytes.fromhex(after[slot['record_id']]['encoded_hex'])[1:].hex()
            assert slot['complete_original_getter_pointer_body_terminator_stream_owner_andall_unowned4MiB_exact']
    retained={r['id']:r for r in retentions['records']}
    assert set(initial['observed_layout_candidates'])==set(delta['changed_record_IDs'])|set(retained)
    for key,row in retained.items():assert after[key]['encoded_hex']==row['retained_encoded_hex']
    source={r['id']:r for r in doc['records']}
    prefs=load(ROOT/'formatting_v1/visual_preferences_v5.json')['records']
    findings=[dict(id=k,source_reference=source[k]['source_reference'],current_reference=source[k]['current_reference'],
        original_finding=r['reason'],disposition='retained-layout' if k in retained else 'revised-layout',
        reason=retained[k]['reason'] if k in retained else prefs[k]['reason'],compiled_hex=after[k]['encoded_hex'])
        for k,r in initial['observed_layout_candidates'].items()]
    save(VIEW,dict(manuscript=str(DOC),manuscript_sha256=digest(DOC),plan=str(PLAN),plan_sha256=digest(PLAN),
        native=str(NATIVE),native_sha256=digest(NATIVE),initial_review=str(initialpath),changed_review_sheets=sheets['sheets'],
        all29_new_native_pages_directly_viewed=True,all375_initial_body_pages_directly_viewed=True,
        final_speech_pages_visually_approved=True,final_pages=374,visual_layout_revisions=28,visual_candidate_retentions=2,
        corrected_FE_blank_rows=1,FE_record='DK4_MES_B290_R0148',scoped_punctuation_glyph_fixes=5,
        findings=findings,scoped_actors=18,scoped_name_strings=17,all_name_andmenu_sheets_directly_viewed=True,
        all_words_andnative_controls_unchanged_by_layout=True,no_QA_waiver=True,offline_only=True,
        actual_new_batch_gameplay=False,all_fifth_gates_still_pending=True,new_credit=0,
        evidence={str(p):digest(p) for p in (DOC,PLAN,NATIVE,STYLES,initialpath,retentionpath,namespath,ROOT/'scoped_terms_v1.json',Path(__file__))}))
    storage=deepcopy(doc)
    for row in storage['records']:
        if row['kind']=='typed-choice-label':
            row['original_exact_source_reference']=deepcopy(row['source_reference'])
            row['source_reference'].update(command_offset=row['source_command_offset'],source_index=row['source_index'])
    storage.update(offline_speech_visual_approved=True,offline_caption_visual_approved=True,scoped_name_native_andvisual_approved=True,
        all_individual_fifth_gates_still_pending=True,source_full_manuscript=str(DOC),source_full_manuscript_sha256=digest(DOC),
        final_visual_approval=str(VIEW),final_visual_approval_sha256=digest(VIEW))
    OUT.mkdir();manuscript=OUT/'storage_manuscript.json';save(manuscript,storage)
    plan.update(manuscript=str(manuscript),manuscript_sha256=digest(manuscript));planpath=OUT/'compiled_plans.json';save(planpath,plan)
    native.update(manuscript=str(manuscript),manuscript_sha256=digest(manuscript),plan=str(planpath),plan_sha256=digest(planpath),
        metadata_only_storage_bridge=True,original_native_receipt=str(NATIVE),original_native_receipt_sha256=digest(NATIVE),
        direct_visual_review_pending=False,final_visual_approval=str(VIEW),final_visual_approval_sha256=digest(VIEW))
    save(OUT/'native_pages.json',native)
    styles.update(manuscript=str(manuscript),manuscript_sha256=digest(manuscript),plan=str(planpath),plan_sha256=digest(planpath),
        metadata_only_storage_bridge=True,all131_style_inputs_match_final_native_plan=True,
        original_style_receipt=str(STYLES),original_style_receipt_sha256=digest(STYLES))
    save(OUT/'styles.json',styles)
    packet=load(CURRENT);assert packet['runtime']==native['runtime']==styles['runtime']==names['runtime'];save(OUT/'packet.json',packet)
    two=load(ROOT/'native_objects_v1/two/complete_choice_objects.json');assert two['all_checks_pass']
    groups=[]
    for obj in two['objects']:
        path=Path(obj['receipt']);assert digest(path)==obj['receipt_sha256']
        proof=load(path);assert proof['runtime']==native['runtime'] and proof['complete_caption_glyphs_centering_bounds_guards_andconsumption_pass']
        value=Path(obj['compiled_path']).read_bytes().hex();assert value==proof['native_choice_object_hex']
        groups.append(dict(block=obj['block'],source_command_offset=obj['source_command_offset'],target_object_hex=value,
            record_IDs=obj['record_ids'],original_receipt=str(path),original_receipt_sha256=digest(path)))
    path=ROOT/'native_objects_v1/three/menu_provider_and_planes.json';three=load(path)
    assert three['runtime']==native['runtime'] and three['complete_caption_glyphs_centering_bounds_guards_andconsumption_pass']
    for obj in three['menus']:
        groups.append(dict(block=obj['block'],source_command_offset=obj['source_command_offset'],target_object_hex=obj['target_object_hex'],
            record_IDs=obj['record_IDs'],original_receipt=str(path),original_receipt_sha256=digest(path)))
    assert len(groups)==5 and sum(len(g['record_IDs']) for g in groups)==11
    save(OUT/'menus.json',dict(manuscript=str(manuscript),manuscript_sha256=digest(manuscript),runtime=native['runtime'],menus=groups,
        offline_visual_approved=True,direct_view_pending=False,actual_controller_andstored_objects_still_pending=True,
        complete_caption_glyphs_centering_bounds_guards_andconsumption_pass=True,new_credit=0))
    print('374 final native pages approved; 28 wrap revisions, two layout retentions, one FE blank row and five glyph fixes. Storage inputs ready; fifth gates pending.')

if __name__=='__main__':main()
