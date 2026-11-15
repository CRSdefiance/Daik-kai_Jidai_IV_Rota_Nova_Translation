"""Bind270 reviewed records to storage without replaying unchanged native page proofs."""
from copy import deepcopy
from pathlib import Path
from scripts.audit_story_glyph_consistency import load,save
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest
from scripts.qualify_maria270_market_parent_v1 import qualify,OUT as PARENT_PROOF

ROOT=Path('work/Maria_B37_B50_clean_20261109')
OUT=ROOT/'storage270_inputs_v1'

def main():
    assert not OUT.exists()
    paths=dict(doc=ROOT/'complete_B37_B49_projection_v1/formatting_input.json',
        plan=ROOT/'final270_plan_v2/automatic_plans.json',native=ROOT/'final270_native_v2/compiled_native_pages.json',
        visual=ROOT/'offline270_display_approval_v2.json',menu=ROOT/'menu_planes_v1/group_verification.json',
        packet=ROOT/'current_v1/current_effective.json')
    doc,plan,native,visual,menus,packet=[load(p) for p in paths.values()]
    assert (len(doc['records']),len(plan['records']),len(native['records']),native['pages'])==(270,266,266,272)
    assert visual['all272_selected_body_pages_directly_viewed'] and visual['all42_name_strings_andboth_menu_sheets_directly_viewed']
    assert visual['all_fifth_review_gates_still_false'] and not plan['failures']
    assert native['manuscript_sha256']==plan['manuscript_sha256']==digest(paths['doc'])
    assert native['plan_sha256']==digest(paths['plan'])
    assert all(r['review']==dict(source=True,context=True,localization=True,naturalness=True,formatting=False) for r in doc['records'])
    image,parent=qualify(native['runtime']);assert load(PARENT_PROOF)==parent
    assert doc['runtime']==native['runtime']==packet['runtime']
    before=deepcopy(doc['records'])
    for row in doc['records']:
        if row['kind']=='typed-choice-label':
            row['original_exact_source_reference']=deepcopy(row['source_reference'])
            row['source_reference'].update(command_offset=row['source_command_offset'],source_index=row['source_index'])
    assert all(a['english']==b['english'] and a['current_hex']==b['current_hex'] and a['source_hex']==b['source_hex'] for a,b in zip(before,doc['records'],strict=True))
    doc.update(current_ROM=parent['target_candidate'],current_ROM_sha256=parent['target_candidate_sha256'],
        exact_registered_market_parent_reuse=parent,offline_speech_visual_approved=True,offline_caption_visual_approved=True,
        scoped_name_native_andvisual_approved=True,all_individual_fifth_gates_still_pending=True,
        source_full_manuscript=str(paths['doc']),source_full_manuscript_sha256=digest(paths['doc']),
        final_visual_approval=str(paths['visual']),final_visual_approval_sha256=digest(paths['visual']))
    packet['groups']=[g for g in packet['groups'] if g['block'] in doc['blocks']]
    assert [g['block'] for g in packet['groups']]==list(range(37,50))
    packet.update(current_ROM=parent['target_candidate'],current_ROM_sha256=parent['target_candidate_sha256'],exact_registered_market_parent_reuse=parent)
    assert len(packet['groups'])==13
    OUT.mkdir();manuscript=OUT/'storage_manuscript.json';save(manuscript,doc)
    plan.update(manuscript=str(manuscript),manuscript_sha256=digest(manuscript));planpath=OUT/'compiled_plans.json';save(planpath,plan)
    native.update(manuscript=str(manuscript),manuscript_sha256=digest(manuscript),plan=str(planpath),plan_sha256=digest(planpath),
        metadata_only_storage_bridge=True,original_native_receipt=str(paths['native']),original_native_receipt_sha256=digest(paths['native']),
        exact_registered_market_parent_reuse=parent)
    save(OUT/'native_pages.json',native);save(OUT/'packet.json',packet)
    styles=dict(manuscript=str(manuscript),manuscript_sha256=digest(manuscript),plan=str(planpath),plan_sha256=digest(planpath),
        runtime=native['runtime'],objects=[],physical_alternatives=0,native_target_slot_cases=0,
        source_has_no_4100_style_objects=True,exact_registered_market_parent_reuse=parent,new_credit=0)
    save(OUT/'styles.json',styles)
    byid={r['id']:r for r in doc['records']};objects=[]
    for item in menus['objects']:
        proof=load(item['receipt']);assert digest(item['receipt'])==item['receipt_sha256']
        assert proof['complete_caption_glyphs_centering_bounds_guards_andconsumption_pass']
        rows=sorted([byid[i] for i in item['record_ids']],key=lambda r:r['source_index'])
        assert [r['source_index'] for r in rows]==[0,1] and all(r['block']==item['block'] for r in rows)
        objects.append(dict(block=item['block'],source_command_offset=item['source_command_offset'],
            target_object_hex=proof['native_choice_object_hex'],record_IDs=[r['id'] for r in rows],
            original_receipt=item['receipt'],original_receipt_sha256=digest(item['receipt'])))
    assert len(objects)==2 and {x['block'] for x in objects}=={38,49}
    save(OUT/'menus.json',dict(manuscript=str(manuscript),manuscript_sha256=digest(manuscript),runtime=native['runtime'],
        menus=objects,offline_visual_approved=True,direct_view_pending=False,
        complete_caption_glyphs_centering_bounds_guards_andconsumption_pass=True,
        actual_controller_andstored_objects_still_pending=True,new_credit=0))
    save(OUT/'metadata_bridge_qualification.json',dict(inputs={str(p):digest(p) for p in paths.values()},
        parent_qualification=str(PARENT_PROOF),parent_qualification_sha256=digest(PARENT_PROOF),
        all270_prose_decisions_source_current_controls_and266_compiled_buffers_unchanged=True,
        actual_native_runtime_is_older_own_Maria3_not_relabelled=True,target_market_fix_preserved=True,
        selected272_pages_directly_viewed_andexact_proofs_reused=True,all_fifth_gates_false=True,new_credit=0))
    print('Prepared270 storage inputs onregistered market-fix parent;266 native bodies/272 pages reused;no prose orcredit changes.')

if __name__=='__main__':main()
