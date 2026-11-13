"""Bridge the approved303-object manuscript,299 native bodies andtwo menus to complete-block storage."""
from copy import deepcopy
from pathlib import Path
from scripts.audit_story_glyph_consistency import load,save
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest

ROOT=Path('work/Maria_B58_B70_clean_20261109')

def main():
    out=ROOT/'storage_inputs_v1';assert not out.exists()
    approvalpath=ROOT/'offline_display_approval_v1.json';a=load(approvalpath)
    paths=dict(doc=Path(a['full_formatted_manuscript']),plan=Path(a['final_plan']),native=Path(a['final_native']),
        packet=ROOT/'current_v1/current_effective.json',menu=ROOT/'menu_native_v1/group_verification.json')
    doc,plan,native,packet,menus=[load(p) for p in paths.values()]
    assert (len(doc['records']),len(plan['records']),len(native['records']),native['pages'])==(303,299,299,299)
    assert a['all299_final_pages_directly_viewed_or_exact_visual_dependency_reuse'] and a['all24_names_andfour_captions_directly_viewed']
    assert a['all_fifth_review_gates_still_false'] and not native['direct_visual_review_pending'] and not plan['failures']
    assert digest(paths['doc'])==a['full_formatted_manuscript_sha256']==plan['manuscript_sha256']
    assert digest(paths['plan'])==a['final_plan_sha256'] and digest(paths['native'])==a['final_native_sha256']
    bodydoc=load(native['manuscript']);bodyplan=load(native['plan'])
    assert digest(native['manuscript'])==native['manuscript_sha256']==bodyplan['manuscript_sha256']
    assert digest(native['plan'])==native['plan_sha256']
    assert bodydoc['subset_of_sha256']==digest(paths['doc']) and bodyplan['complete_parent_plan_sha256']==digest(paths['plan'])
    assert bodydoc['records']==[r for r in doc['records'] if r['kind']!='typed-choice-label'] and bodyplan['records']==plan['records']
    assert doc['runtime']==native['runtime']==packet['runtime'] and doc['blocks']==[58,59,60,61,62,64,65,66,68,70]
    assert all(r['review']==dict(source=True,context=True,localization=True,naturalness=True,formatting=False) for r in doc['records'])
    assert all(not r.get('native_object_kind') for r in doc['records'])
    release=load(doc['runtime']['release_proof'])
    assert digest('translations/release_stack.json')==release['registry_sha256']
    assert digest(doc['current_ROM'])==doc['current_ROM_sha256']==release['candidate_sha256']
    assert [g['block'] for g in packet['groups']]==doc['blocks']
    before=deepcopy(doc['records'])
    doc.update(offline_speech_visual_approved=True,offline_caption_visual_approved=True,scoped_name_native_andvisual_approved=True,
        all_individual_fifth_gates_still_pending=True,source_full_manuscript=str(paths['doc']),source_full_manuscript_sha256=digest(paths['doc']),
        final_visual_approval=str(approvalpath),final_visual_approval_sha256=digest(approvalpath))
    assert doc['records']==before
    out.mkdir();manuscript=out/'storage_manuscript.json';save(manuscript,doc)
    plan.update(manuscript=str(manuscript),manuscript_sha256=digest(manuscript));planpath=out/'compiled_plans.json';save(planpath,plan)
    native.update(manuscript=str(manuscript),manuscript_sha256=digest(manuscript),plan=str(planpath),plan_sha256=digest(planpath),
        metadata_only_storage_bridge=True,original_native_receipt=str(paths['native']),original_native_receipt_sha256=digest(paths['native']),
        original_body_manuscript=bodydoc['subset_of'],final_visual_approval=str(approvalpath),final_visual_approval_sha256=digest(approvalpath))
    save(out/'native_pages.json',native);save(out/'packet.json',packet)
    save(out/'styles.json',dict(manuscript=str(manuscript),manuscript_sha256=digest(manuscript),plan=str(planpath),plan_sha256=digest(planpath),
        runtime=native['runtime'],objects=[],physical_alternatives=0,native_target_slot_cases=0,source_has_no_4100_style_objects=True,new_credit=0))
    byid={r['id']:r for r in doc['records']};objects=[]
    for item in menus['objects']:
        proof=load(item['receipt']);assert digest(item['receipt'])==item['receipt_sha256']
        assert proof['runtime']==native['runtime'] and proof['complete_caption_glyphs_centering_bounds_guards_andconsumption_pass']
        rows=sorted([byid[i] for i in item['record_ids']],key=lambda r:r['source_index'])
        assert [r['source_index'] for r in rows]==[0,1] and all(r['block']==item['block'] for r in rows)
        assert all(r['source_word']==0x2100 for r in rows)
        objects.append(dict(block=item['block'],source_command_offset=item['source_command_offset'],target_object_hex=proof['native_choice_object_hex'],
            record_IDs=[r['id'] for r in rows],original_receipt=item['receipt'],original_receipt_sha256=digest(item['receipt'])))
    assert len(objects)==2 and {x['block'] for x in objects}=={60,64}
    save(out/'menus.json',dict(manuscript=str(manuscript),manuscript_sha256=digest(manuscript),runtime=native['runtime'],menus=objects,
        offline_visual_approved=True,direct_view_pending=False,complete_caption_glyphs_centering_bounds_guards_andconsumption_pass=True,
        actual_controller_andstored_objects_still_pending=True,new_credit=0))
    save(out/'metadata_bridge_qualification.json',dict(inputs={str(p):digest(p) for p in [*paths.values(),approvalpath,Path(__file__)]},
        all303_prose_decisions_source_current_controls_and299_compiled_buffers_unchanged=True,
        all299_native_pages_andfour_captions_approved_andexact_receipts_reused=True,
        complete_registered_parent=doc['current_ROM'],complete_registered_parent_sha256=doc['current_ROM_sha256'],
        no_ROM_orregistry_changes=True,all_fifth_gates_false=True,new_credit=0))
    print('Prepared303 storage objects/299 native bodies/two typed menus on exact registered Maria310;no prose orcredit change.')

if __name__=='__main__':main()
