"""Bind the approved310 ordinary bodies to the existing complete-block storage contract."""
from copy import deepcopy
from scripts.audit_story_glyph_consistency import load,save
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest
from scripts.meaning_maria_B51_B52_clean_v1 import ROOT

def main():
    out=ROOT/'storage_inputs_v1';assert not out.exists()
    approval_path=ROOT/'offline_display_approval_v1.json';a=load(approval_path)
    paths=dict(doc=ROOT/'formatting_v1/formatting_input.json',plan=a['final_plan'],native=a['final_native'],packet=ROOT/'current_v1/current_effective.json')
    doc,plan,native,packet=[load(p) for p in paths.values()]
    assert (len(doc['records']),len(plan['records']),len(native['records']),native['pages'])==(310,310,310,318)
    assert a['all318_final_pages_directly_viewed_or_exact_visual_reuse'] and a['all31_name_strings_directly_viewed'] and a['all_fifth_review_gates_still_false']
    assert not native['direct_visual_review_pending'] and native['all_records_native_checked_once_or_exact_compiled_dependency_reuse']
    assert native['manuscript_sha256']==plan['manuscript_sha256']==digest(paths['doc']) and native['plan_sha256']==digest(paths['plan'])
    assert doc['runtime']==native['runtime']==packet['runtime'] and doc['blocks']==list(range(51,58))
    assert all(r['review']==dict(source=True,context=True,localization=True,naturalness=True,formatting=False) for r in doc['records'])
    assert all(r['kind'] in ['progressive','system-FE'] and not r.get('native_object_kind') for r in doc['records'])
    source=deepcopy(doc['records'])
    doc.update(offline_speech_visual_approved=True,offline_caption_visual_approved=True,source_has_no_typed_captions=True,
        scoped_name_native_andvisual_approved=True,all_individual_fifth_gates_still_pending=True,
        source_full_manuscript=str(paths['doc']),source_full_manuscript_sha256=digest(paths['doc']),
        final_visual_approval=str(approval_path),final_visual_approval_sha256=digest(approval_path))
    assert doc['records']==source
    out.mkdir();manuscript=out/'storage_manuscript.json';save(manuscript,doc)
    plan.update(manuscript=str(manuscript),manuscript_sha256=digest(manuscript));planpath=out/'compiled_plans.json';save(planpath,plan)
    native.update(manuscript=str(manuscript),manuscript_sha256=digest(manuscript),plan=str(planpath),plan_sha256=digest(planpath),
        metadata_only_storage_bridge=True,original_native_receipt=str(paths['native']),original_native_receipt_sha256=digest(paths['native']),
        final_visual_approval=str(approval_path),final_visual_approval_sha256=digest(approval_path))
    save(out/'native_pages.json',native);save(out/'packet.json',packet)
    styles=dict(manuscript=str(manuscript),manuscript_sha256=digest(manuscript),plan=str(planpath),plan_sha256=digest(planpath),
        runtime=native['runtime'],objects=[],physical_alternatives=0,native_target_slot_cases=0,
        source_has_no_4100_style_objects=True,new_credit=0)
    save(out/'styles.json',styles)
    save(out/'menus.json',dict(manuscript=str(manuscript),manuscript_sha256=digest(manuscript),runtime=native['runtime'],
        menus=[],source_has_no_typed_choice_objects=True,offline_visual_approved=True,direct_view_pending=False,
        complete_caption_glyphs_centering_bounds_guards_andconsumption_pass=True,new_credit=0))
    save(out/'metadata_bridge_qualification.json',dict(inputs={str(p):digest(p) for p in paths.values()},
        all310_prose_decisions_source_current_controls_andcompiled_buffers_unchanged=True,
        all318_pages_directly_viewed_or_exact_RGB_reuse=True,empty_style_andmenu_objects_source_qualified=True,
        fifth_gates_still_false=True,new_credit=0))
    print('Prepared310 storage records/seven complete blocks;318 approved native pages reused;no prose orcredit changes.')
if __name__=='__main__':main()
