"""Replace one directly viewed FE page and preserve all544 unchanged visual bindings."""
from copy import deepcopy
from pathlib import Path
from scripts.audit_story_glyph_consistency import load,save
from dk4tool.patch.grand_race_menu_release import sha

ROOT=Path('work/analysis/Rafael_B61_B80_formatting_20261104')
if __name__=='__main__':
    prior=ROOT/'combined_native_v10.json';approval=ROOT/'body_display_approval_v10.json'
    delta=ROOT/'speech_native_reassurance_v13/compiled_native_pages.json'
    manuscript=ROOT/'formatting_input_v5.json';plan=ROOT/'automatic_v12/automatic_plans.json'
    output=ROOT/'combined_native_v12.json';visual=ROOT/'body_display_approval_v12.json'
    assert not output.exists() and not visual.exists()
    before,old_visual,fresh,doc,plans=map(load,[prior,approval,delta,manuscript,plan])
    assert before['runtime']==fresh['runtime'] and before['font_sha256']==fresh['font_sha256']
    assert fresh['complete_consumption_andpagination_exact'] and fresh['all_first_internal_final_glyph_codes_pixels_input_canaries_andbounds_pass']
    assert len(fresh['records'])==fresh['pages']==1 and old_visual['all_final_pages_directly_viewed']
    changed=fresh['records'][0];assert changed['id']=='DK4_MES_B69_R0069'
    assert changed['logical_English']=='Does it look bad on me?'
    rows={r['id']:deepcopy(r) for r in before['records']};assert rows[changed['id']]['compiled_hex']!=changed['compiled_hex']
    rows[changed['id']]=deepcopy(changed)
    for target in plans['records']:
        row=rows[target['id']]
        assert row['compiled_hex']==target['encoded_hex'] and row['logical_English']==target['logical_English']
        assert not any(i['severity'] in ['warning','error'] for i in target['base_QA']['issues'])
    rendered=changed['complete_native_English_display']
    assert rendered['planned_native_row_comparison']['actual_rows']==['Does it look bad on me?']
    assert sha(Path(rendered['preview']).read_bytes())==rendered['preview_sha256']
    assert sha(Path(rendered['native_plane']).read_bytes())==rendered['native_plane_sha256']
    bindings=[deepcopy(r) for r in old_visual['exact_page_bindings'] if r['id']!=changed['id']]
    assert len(bindings)==544
    direct=dict(id=changed['id'],page=1,preview=rendered['preview'],preview_sha256=rendered['preview_sha256'],
        exact_direct_visual_evidence=[dict(kind='individual_native_page_directly_viewed',
            source=rendered['preview'],source_sha256=rendered['preview_sha256'],reason='Full negative concern clearly answered by the retained reassuring Not at all!')])
    bindings.append(direct)
    result=deepcopy(before);result.update(manuscript=str(manuscript),manuscript_sha256=sha(manuscript.read_bytes()),
        plan=str(plan),plan_sha256=sha(plan.read_bytes()),records=[rows[r['id']] for r in doc['records']],
        previous_native=str(prior),previous_native_sha256=sha(prior.read_bytes()),
        source_owned_target_page_adapter=fresh['source_owned_target_page_adapter'],
        final_delta=str(delta),final_delta_sha256=sha(delta.read_bytes()),
        direct_visual_review_pending=False,all545_final_body_pages_directly_viewed=True,
        reassurance_revision='Does it look bad on me? / Not at all!',
        fresh_reassurance_records=1,exact_native_records_reused=538,new_credit=0,
        evidence={str(p):sha(p.read_bytes()) for p in [prior,approval,delta,manuscript,plan,Path(__file__)]})
    save(output,result)
    result_visual=deepcopy(old_visual);result_visual.update(final_native=str(output),final_native_sha256=sha(output.read_bytes()),
        final_plan=str(plan),final_plan_sha256=sha(plan.read_bytes()),final_manuscript=str(manuscript),final_manuscript_sha256=sha(manuscript.read_bytes()),
        exact_page_bindings=bindings,viewed_candidate_pages=564,retired_orreplaced_candidate_pages_also_reviewed=19,
        additional_individual_page_directly_viewed=direct,unchanged_final_page_bindings_reused=544,
        previous_approval=str(approval),previous_approval_sha256=sha(approval.read_bytes()),new_credit=0,
        producer_sha256=sha(Path(__file__).read_bytes()))
    save(visual,result_visual)
    for kind in ['menu','style']:
        old=ROOT/('no_'+kind+'_objects.json');target=ROOT/('no_'+kind+'_objects_v12.json')
        assert not target.exists();value=deepcopy(load(old))
        assert not value['menus' if kind=='menu' else 'objects']
        value.update(manuscript_sha256=sha(manuscript.read_bytes()),plan_sha256=sha(plan.read_bytes()),
            previous_absence_proof=str(old),previous_absence_proof_sha256=sha(old.read_bytes()),
            same_exact_clean_andcurrent_command_inventory_no_compound_objects=True)
        save(target,value)
    print('539 final records/545 pages:one fresh directly viewed FE page,538 native records/544 visual bindings reused. No new credit.')
