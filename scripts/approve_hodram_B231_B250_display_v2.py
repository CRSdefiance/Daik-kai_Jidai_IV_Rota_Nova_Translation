"""Seal direct offline page review and bridge exact objects to complete-block storage."""
from copy import deepcopy
from pathlib import Path
from scripts.audit_story_glyph_consistency import load,save
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest
from scripts.refine_hodram_B231_B250_visual_v1 import ROOT,DOC,INITIAL,VIEW as INITIAL_VIEW
from scripts.review_hodram_B231_B250_contextual_v1 import CURRENT

PLAN=ROOT/'formatting_v1/visual_trial_v2/automatic_plans.json'
NATIVE=ROOT/'final_native_v2/compiled_native_pages.json'
STYLES=ROOT/'native_objects_v1/styles/compiled_style_objects.json'
VIEW=ROOT/'final_visual_approval_v2.json'
OUT=ROOT/'storage_inputs_v2'

def main():
    assert not VIEW.exists() and not OUT.exists()
    doc,plan,native,styles,initial,delta,sheets,names,retentions=map(load,(DOC,PLAN,NATIVE,STYLES,INITIAL_VIEW,
        ROOT/'layout_delta_v2/delta.json',ROOT/'changed_body_sheets_v2/sheet_index.json',
        ROOT/'name_planes_v1/native_name_planes.json',ROOT/'layout_trial_retentions_v2.json'))
    assert len(doc['records'])==225 and len(plan['records'])==len(native['records'])==223 and native['pages']==228
    assert native['all_first_internal_final_glyph_codes_pixels_input_canaries_andbounds_pass'] and native['complete_consumption_andpagination_exact']
    assert not plan['failures'] and not any(i['severity'] in ('error','warning') for r in plan['records'] for i in r['base_QA']['issues'])
    assert initial['all230_initial_body_pages_directly_viewed'] and initial['all_initial_name_andmenu_sheets_directly_viewed']
    assert len(delta['changed_record_IDs'])==13 and delta['fresh_pages']==17
    assert len(sheets['sheets'])==1 and sum(len(s['included']) for s in sheets['sheets'])==17
    for sheet in initial['body_sheets']+sheets['sheets']: assert digest(sheet['path'])==sheet['sha256']
    before={r['id']:r for r in load(INITIAL)['records']};after={r['id']:r for r in plan['records']}
    # Plan metadata changes, but not a single style alternative or native slot input.
    assert styles['manuscript_sha256']==digest(DOC) and styles['physical_alternatives']==14 and styles['native_target_slot_cases']==16
    for obj in styles['objects']:
        assert digest(obj['target_path'])==obj['target_sha256']
        for key in obj['physical_record_IDs']: assert before[key]['encoded_hex']==after[key]['encoded_hex']
    retained={r['id']:r for r in retentions['records']}
    assert {r['id'] for r in initial['observed_layout_candidates']}==set(delta['changed_record_IDs'])|set(retained)
    for key,row in retained.items():assert after[key]['encoded_hex']==row['retained_encoded_hex']
    source={r['id']:r for r in doc['records']}
    findings=[dict(id=r['id'],source_reference=source[r['id']]['source_reference'],current_reference=source[r['id']]['current_reference'],
        original_finding=r['reason'],disposition='retained-layout' if r['id'] in retained else 'revised-layout',
        reason=retained[r['id']]['reason'] if r['id'] in retained else r['reason'],compiled_hex=after[r['id']]['encoded_hex'])
        for r in initial['observed_layout_candidates']]
    save(VIEW,dict(manuscript=str(DOC),manuscript_sha256=digest(DOC),plan=str(PLAN),plan_sha256=digest(PLAN),
        native=str(NATIVE),native_sha256=digest(NATIVE),initial_review=str(INITIAL_VIEW),changed_review_sheets=sheets['sheets'],
        all17_new_native_pages_directly_viewed=True,all230_initial_body_pages_directly_viewed=True,
        final_speech_pages_visually_approved=True,final_pages=228,visual_layout_revisions=13,visual_candidate_retentions=9,
        findings=findings,scoped_actors=19,scoped_name_strings=19,all_name_andmenu_sheets_directly_viewed=True,
        all_words_andnative_controls_unchanged_by_layout=True,no_QA_waiver=True,offline_only=True,
        actual_new_batch_gameplay=False,all_fifth_gates_still_pending=True,new_credit=0,
        evidence={str(p):digest(p) for p in (DOC,PLAN,NATIVE,STYLES,INITIAL_VIEW,ROOT/'layout_trial_retentions_v2.json',Path(__file__))}))
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
        metadata_only_storage_bridge=True,all14_style_inputs_andcompiled_bytes_exact_to_original_proof=True,
        original_style_receipt=str(STYLES),original_style_receipt_sha256=digest(STYLES))
    save(OUT/'styles.json',styles)
    packet=load(CURRENT);assert packet['runtime']==native['runtime']==styles['runtime']==names['runtime'];save(OUT/'packet.json',packet)
    two=load(ROOT/'native_objects_v1/menu/complete_choice_objects.json');assert two['all_checks_pass']
    groups=[]
    for obj in two['objects']:
        path=Path(obj['receipt']);assert digest(path)==obj['receipt_sha256']
        proof=load(path);assert proof['runtime']==native['runtime'] and proof['complete_caption_glyphs_centering_bounds_guards_andconsumption_pass']
        value=Path(obj['compiled_path']).read_bytes().hex();assert value==proof['native_choice_object_hex']
        groups.append(dict(block=obj['block'],source_command_offset=obj['source_command_offset'],target_object_hex=value,
            record_IDs=obj['record_ids'],original_receipt=str(path),original_receipt_sha256=digest(path)))
    assert len(groups)==1 and sum(len(g['record_IDs']) for g in groups)==2
    save(OUT/'menus.json',dict(manuscript=str(manuscript),manuscript_sha256=digest(manuscript),runtime=native['runtime'],menus=groups,
        offline_visual_approved=True,direct_view_pending=False,actual_controller_andstored_objects_still_pending=True,
        complete_caption_glyphs_centering_bounds_guards_andconsumption_pass=True,new_credit=0))
    print('228 final native pages approved; 13 wrap revisions, nine layout retentions. Storage metadata bridged; fifth gates pending.')

if __name__=='__main__':main()
