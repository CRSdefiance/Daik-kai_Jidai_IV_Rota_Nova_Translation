"""Record direct final-page review and bridge exact reviewed objects to storage."""
from copy import deepcopy
from pathlib import Path
from scripts.audit_story_glyph_consistency import load,save
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest
from scripts.prepare_hodram_B211_B230_formatting_v1 import FORMATTING
from scripts.review_hodram_B221_B230_contextual_v1 import ROOT,CURRENT

PLAN=ROOT/'formatting_v1/visual_plan_v6/automatic_plans.json'
NATIVE=ROOT/'final_native_v6/compiled_native_pages.json'
STYLES=ROOT/'final_styles_v6/compiled_style_objects.json'
VIEW=ROOT/'final_visual_approval_v6.json'
OUT=ROOT/'storage_inputs_v1'

def main():
    assert not VIEW.exists() and not OUT.exists()
    doc,plan,native,styles,initial,delta,sheets,names=map(load,(FORMATTING,PLAN,NATIVE,STYLES,
        ROOT/'initial_visual_review_v1.json',ROOT/'visual_delta_inputs_v6/delta.json',
        ROOT/'visual_delta_sheets_v6/sheet_index.json',ROOT/'name_planes_v1/native_name_planes.json'))
    assert len(doc['records'])==277 and len(plan['records'])==len(native['records'])==270 and native['pages']==284
    assert not plan['failures'] and all(not any(i['severity'] in ('error','warning') for i in r['base_QA']['issues']) for r in plan['records'])
    assert native['manuscript_sha256']==styles['manuscript_sha256']==digest(FORMATTING)
    assert native['plan_sha256']==styles['plan_sha256']==digest(PLAN)
    assert native['all_first_internal_final_glyph_codes_pixels_input_canaries_andbounds_pass'] and native['complete_consumption_andpagination_exact']
    assert styles['native_target_slot_cases']==32 and styles['physical_alternatives']==29
    assert initial['all285_initial_body_pages_directly_viewed'] and initial['all_initial_name_andmenu_sheets_directly_viewed']
    assert len(delta['changed_record_IDs'])==27 and delta['fresh_pages']==39
    assert len(sheets['sheets'])==2 and sum(len(s['included']) for s in sheets['sheets'])==39
    for sheet in initial['sheets']+sheets['sheets']:
        assert digest(sheet['path'])==sheet['sha256']
    retained={
        'DK4_MES_B216_R0054': 'Initial contact-sheet reading was mistaken: enlarged native page and row events confirm A Dou already occupies one row. Exact compiled/native proof retained.',
        'DK4_MES_B216_R0058': 'Initial contact-sheet reading was mistaken: enlarged native page and row events confirm Zhao Yun already occupies one row. Exact compiled/native proof retained.',
        'DK4_MES_B217_R0045': 'Keep My clan descends / from: the complete following prepositional phrase reads better than the tested sparse opening or stranded that retainer. All prose intact.',
        'DK4_MES_B213_R0027': 'Keep the existing six-row two-page description. Tested constraints separating bane / of Tokugawa created sparse opening rows, stranded subject/modal phrases or two weak-ending findings. This ordinary complete-word boundary is the better documented tradeoff.'}
    assert set(initial['observed_layout_candidates'])==set(delta['changed_record_IDs'])|set(retained)
    old={r['id']:r for r in load(ROOT/'native_resume_v2/compiled_native_pages.json')['records']}
    final={r['id']:r for r in native['records']}
    for key in retained:assert final[key]==old[key]
    findings=[]
    source={r['id']:r for r in doc['records']}
    for key,finding in initial['observed_layout_candidates'].items():
        row=source[key]
        findings.append(dict(id=key,source_reference=row['source_reference'],current_reference=row['current_reference'],
            finding=finding,disposition='revised-layout' if key not in retained else 'retained-layout',
            reason=retained.get(key,finding['reason']),compiled_hex=final[key]['compiled_hex']))
    prefs=load(ROOT/'formatting_v1/visual_preferences_v6.json')
    save(VIEW,dict(manuscript=str(FORMATTING),manuscript_sha256=digest(FORMATTING),plan=str(PLAN),plan_sha256=digest(PLAN),
        native=str(NATIVE),native_sha256=digest(NATIVE),initial_review=initial,changed_review_sheets=sheets['sheets'],
        all39_new_native_pages_directly_viewed=True,final_speech_pages_visually_approved=True,final_pages=284,
        visual_layout_revisions=27,visual_candidate_retentions=4,findings=findings,
        separate_FE_punctuation_wrap_corrected=1,FE_record='DK4_MES_B215_R0017',
        scoped_name_strings=22,scoped_actors=23,all_name_andmenu_sheets_directly_viewed=True,
        all7_caption_visual_checks_pass=True,all_words_andnative_controls_unchanged_by_layout=True,
        exact_QA_line_ending_retention=dict(id='DK4_MES_B229_R0036',**prefs['records']['DK4_MES_B229_R0036']),
        additional_justified_page_retention=initial['justified_initial_page_retention'],
        offline_only=True,actual_new_batch_gameplay=False,all_fifth_gates_still_pending=True,new_credit=0,
        evidence={str(p):digest(p) for p in (FORMATTING,PLAN,NATIVE,STYLES,ROOT/'initial_visual_review_v1.json',
            ROOT/'visual_delta_sheets_v6/sheet_index.json',ROOT/'formatting_v1/visual_preferences_v6.json',Path(__file__))}))
    storage=deepcopy(doc)
    for row in storage['records']:
        if row['kind']=='typed-choice-label':
            row['original_exact_source_reference']=deepcopy(row['source_reference'])
            row['source_reference'].update(command_offset=row['source_command_offset'],source_index=row['source_index'])
    storage.update(offline_speech_visual_approved=True,offline_caption_visual_approved=True,
        scoped_name_native_andvisual_approved=True,all_individual_fifth_gates_still_pending=True,
        approved_layout_preferences=str(ROOT/'formatting_v1/visual_preferences_v6.json'),
        approved_layout_preferences_sha256=digest(ROOT/'formatting_v1/visual_preferences_v6.json'),
        source_full_manuscript=str(FORMATTING),source_full_manuscript_sha256=digest(FORMATTING),
        final_visual_approval=str(VIEW),final_visual_approval_sha256=digest(VIEW))
    OUT.mkdir()
    manuscript=OUT/'storage_manuscript.json';save(manuscript,storage)
    plan.update(manuscript=str(manuscript),manuscript_sha256=digest(manuscript));planpath=OUT/'compiled_plans.json';save(planpath,plan)
    native.update(manuscript=str(manuscript),manuscript_sha256=digest(manuscript),plan=str(planpath),plan_sha256=digest(planpath))
    native.update(metadata_only_storage_bridge=True,original_native_receipt=str(NATIVE),original_native_receipt_sha256=digest(NATIVE),
        direct_visual_review_pending=False,final_visual_approval=str(VIEW),final_visual_approval_sha256=digest(VIEW))
    save(OUT/'native_pages.json',native)
    styles.update(manuscript=str(manuscript),manuscript_sha256=digest(manuscript),plan=str(planpath),plan_sha256=digest(planpath),
        metadata_only_storage_bridge=True,original_style_receipt=str(STYLES),original_style_receipt_sha256=digest(STYLES))
    save(OUT/'styles.json',styles)
    packet=load(CURRENT);assert packet['runtime']==native['runtime']==styles['runtime']==names['runtime'];save(OUT/'packet.json',packet)
    two=load(ROOT/'native_objects_v1/two/complete_choice_objects.json')
    threepath=ROOT/'native_objects_v1/three/menu_provider_and_planes.json';three=load(threepath)
    assert two['all_checks_pass'] and three['complete_caption_glyphs_centering_bounds_guards_andconsumption_pass']
    groups=[]
    for obj in two['objects']:
        path=Path(obj['receipt']);assert digest(path)==obj['receipt_sha256']
        proof=load(path);assert proof['runtime']==native['runtime'] and proof['complete_caption_glyphs_centering_bounds_guards_andconsumption_pass']
        value=Path(obj['compiled_path']).read_bytes().hex();assert value==proof['native_choice_object_hex']
        groups.append(dict(block=obj['block'],source_command_offset=obj['source_command_offset'],
            target_object_hex=value,record_IDs=obj['record_ids'],original_receipt=str(path),original_receipt_sha256=digest(path)))
    assert three['runtime']==native['runtime'] and len(three['menus'])==1
    for obj in three['menus']:
        groups.append(dict(block=obj['block'],source_command_offset=obj['source_command_offset'],target_object_hex=obj['target_object_hex'],
            record_IDs=obj['record_IDs'],original_receipt=str(threepath),original_receipt_sha256=digest(threepath)))
    assert len(groups)==3 and sum(len(g['record_IDs']) for g in groups)==7
    save(OUT/'menus.json',dict(manuscript=str(manuscript),manuscript_sha256=digest(manuscript),runtime=native['runtime'],
        menus=groups,offline_visual_approved=True,direct_view_pending=False,actual_controller_andstored_objects_still_pending=True,
        complete_caption_glyphs_centering_bounds_guards_andconsumption_pass=True,new_credit=0))
    print('Approved 284 final native pages; 27 improved layouts, four retentions, one FE fix. Exact storage metadata bridge saved; fifth gates pending.')

if __name__=='__main__':main()
