"""Seal directly viewed native pages and bridge unchanged storage metadata."""
from copy import deepcopy
from pathlib import Path
from scripts.audit_story_glyph_consistency import load,save
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest

ROOT=Path('work/Hodram_B0_B41_clean_20261107')
DOC=ROOT/'formatting_v1/formatting_input_v3.json'
PLAN=ROOT/'automatic_plans_v4/automatic_plans.json'
NATIVE=ROOT/'native_joined_v2/compiled_native_pages.json'
STYLES=ROOT/'native_objects_styles_v2/compiled_style_objects.json'
VIEW=ROOT/'offline_visual_approval_v1.json'
OUT=ROOT/'storage_inputs_v1'

def main():
    assert not VIEW.exists() and not OUT.exists()
    doc,plan,native,styles=map(load,(DOC,PLAN,NATIVE,STYLES))
    initialpath=ROOT/'body_initial_visual_review_v1.json';initial=load(initialpath)
    followpath=ROOT/'body_followup_contact_v1/contact_manifest.json';follow=load(followpath)
    assert initial['all389_initial_pages_directly_viewed'] and len(initial['sheets'])==22
    assert len(follow['pages'])==6 and len(follow['sheets'])==1
    for p in initial['sheets']+follow['sheets']:assert digest(p['path'])==p['sha256']
    assert len(doc['records'])==394 and len(native['records'])==len(plan['records'])==388 and native['pages']==389
    assert native['manuscript_sha256']==styles['manuscript_sha256']==plan['manuscript_sha256']==digest(DOC)
    assert native['plan_sha256']==styles['plan_sha256']==digest(PLAN)
    assert native['all_first_internal_final_glyph_codes_pixels_input_canaries_andbounds_pass'] and native['complete_consumption_andpagination_exact']
    assert not plan['failures'] and not any(i['severity'] in ['warning','error'] for r in plan['records'] for i in r['base_QA']['issues'])
    assert native['origins_counts']=={str(ROOT/'native_visual_followup_v1/compiled_native_pages.json'):5,str(ROOT/'native_joined_v1/compiled_native_pages.json'):383}
    after={r['id']:r for r in plan['records']}
    for obj in styles['objects']:
        assert digest(obj['target_path'])==obj['target_sha256']
        for slot in obj['native_slots']:
            assert slot['target_hex']==bytes.fromhex(after[slot['record_id']]['encoded_hex'])[1:].hex()
            assert slot['complete_original_getter_pointer_body_terminator_stream_owner_andall_unowned4MiB_exact']
    assert (len(styles['objects']),styles['physical_alternatives'],styles['native_target_slot_cases'])==(7,47,56)
    menu_path=ROOT/'native_objects_v2/complete_choice_objects.json';menus=load(menu_path)
    assert menus['all_checks_pass'] and len(menus['objects'])==3 and menus['physical_caption_records']==6
    groups=[];menu_sheets=[]
    source={r['id']:r for r in doc['records']}
    for obj in menus['objects']:
        p=Path(obj['receipt']);assert digest(p)==obj['receipt_sha256'];proof=load(p)
        assert proof['runtime']==native['runtime'] and proof['complete_caption_glyphs_centering_bounds_guards_andconsumption_pass']
        assert digest(obj['compiled_path'])==obj['compiled_sha256']
        value=Path(obj['compiled_path']).read_bytes().hex();assert value==proof['native_choice_object_hex']
        for row in proof['records']:
            assert source[row['id']]['english']==row['english']
        sheet=obj['review_sheet'];assert digest(sheet['path'])==sheet['sha256'];menu_sheets.append(sheet)
        groups.append(dict(block=obj['block'],source_command_offset=obj['source_command_offset'],target_object_hex=value,
            record_IDs=obj['record_ids'],original_receipt=str(p),original_receipt_sha256=digest(p)))
    name_path=ROOT/'scoped_names_formatting_review_v1.json';names=load(name_path)
    assert names['all42_planned_progressive_names_native_andvisually_checked']
    assert load(ROOT/'name_field_visual_approval_v1.json')['all12_current_andproposed_planes_directly_viewed']
    assert load(ROOT/'retained_name_visual_approval_v1.json')['all38_retained_progressive_strings_directly_viewed']
    initial_native=load(ROOT/'native_joined_v1/compiled_native_pages.json')
    changed={r['id'] for r in native['records'] if r['compiled_hex']!=next(a['compiled_hex'] for a in initial_native['records'] if a['id']==r['id'])}
    assert len(changed)==5
    prefs=load(ROOT/'formatting_v1/preferences_v4.json')['records']
    pages=load(ROOT/'body_contact_sheets_v1/contact_manifest.json')['pages']
    by_page={}
    for page in pages:by_page.setdefault(page['id'],[]).append(page)
    fresh={}
    for page in follow['pages']:fresh.setdefault(page['id'],[]).append(page)
    findings=[]
    for row in native['records']:
        ident=row['id'];reason=prefs.get(ident,{}).get('reason',initial['retention_reason'])
        if ident=='DK4_MES_B30_R0013':
            reason='Reinspection confirms the original native row already ends the man. The source-bound phrase preference changes no bytes; retain the already natural layout.'
        if ident=='DK4_MES_B3_R0006':reason=source[ident]['editorial_finding']
        findings.append(dict(id=ident,source_reference=source[ident]['source_reference'],current_reference=source[ident]['current_reference'],
            disposition='revised-prose-and-layout' if ident=='DK4_MES_B3_R0006' else 'revised-layout' if ident in changed else 'retained-checked-layout',
            reason=reason,pages=fresh.get(ident,by_page[ident]),compiled_hex=row['compiled_hex'],all_final_pages_directly_viewed=True))
    evidence={str(p):digest(p) for p in [DOC,PLAN,NATIVE,STYLES,initialpath,followpath,menu_path,name_path,Path(__file__)]}
    save(VIEW,dict(manuscript=str(DOC),manuscript_sha256=digest(DOC),plan=str(PLAN),plan_sha256=digest(PLAN),
        native=str(NATIVE),native_sha256=digest(NATIVE),final_native_pages=389,records=388,
        initial_all389_pages_directly_viewed=True,final_six_changed_pages_directly_viewed=True,
        final_all389_pages_directly_viewed_or_exact_reused=True,initial_body_sheets=initial['sheets'],followup_sheets=follow['sheets'],
        three_menus_six_captions_directly_viewed=True,menu_sheets=menu_sheets,all42_scoped_planned_names_native_andvisually_checked=True,
        visual_wrap_corrections=4,one_substitution_prose_correction=True,one_retained_layout_candidate='DK4_MES_B30_R0013',
        earlier_FE_blank_row_correction='DK4_MES_B29_R0112',earlier_contrast_phrase_correction='DK4_MES_B3_R0036',
        eighteen_body_glyph_targets_native_checked=True,findings=findings,all_fifth_gates_still_pending=True,
        representative_gameplay_stored_checks_andregistered_integration_pending=True,actual_gameplay=False,new_credit=0,evidence=evidence))
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
    for document,path,original in [(native,OUT/'native_pages.json',NATIVE),(styles,OUT/'styles.json',STYLES)]:
        document.update(manuscript=str(manuscript),manuscript_sha256=digest(manuscript),plan=str(planpath),plan_sha256=digest(planpath),
            metadata_only_storage_bridge=True,original_receipt=str(original),original_receipt_sha256=digest(original),direct_visual_review_pending=False,
            final_visual_approval=str(VIEW),final_visual_approval_sha256=digest(VIEW))
        save(path,document)
    packet=load(ROOT/'current_v1/current_effective.json');assert packet['runtime']==native['runtime']==styles['runtime']
    save(OUT/'packet.json',packet)
    save(OUT/'menus.json',dict(manuscript=str(manuscript),manuscript_sha256=digest(manuscript),runtime=native['runtime'],menus=groups,
        offline_visual_approved=True,direct_view_pending=False,actual_controller_andstored_objects_still_pending=True,
        complete_caption_glyphs_centering_bounds_guards_andconsumption_pass=True,new_credit=0))
    print('All389 final pages, six captions and42 scoped names approved offline; exact storage bridge ready. No integration credit.')

if __name__=='__main__':main()
