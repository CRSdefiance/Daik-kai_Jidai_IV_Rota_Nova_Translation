"""Combine only byte-identical qualified native results for the final539/545 plan."""
from copy import deepcopy
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.audit_story_glyph_consistency import load,save

ROOT=Path('work/analysis/Rafael_B61_B80_formatting_20261104')

if __name__=='__main__':
    output=ROOT/'combined_native_v8.json';assert not output.exists()
    manuscript=ROOT/'formatting_input_v3.json';plan_path=ROOT/'automatic_v8/automatic_plans.json'
    reused_path=ROOT/'native_resume_v3/exact_reused_native_records.json'
    fresh_path=ROOT/'speech_native_resume_v3/compiled_native_pages.json'
    delta_path=ROOT/'speech_native_delta_v8/compiled_native_pages.json'
    doc,plans,reused,fresh,delta=map(load,[manuscript,plan_path,reused_path,fresh_path,delta_path])
    assert reused['runtime']==fresh['runtime']==delta['runtime']
    assert len(reused['records'])==289 and len(fresh['records'])==250 and len(delta['records'])==1
    for proof in [fresh,delta]:
        assert proof['complete_consumption_andpagination_exact']
        assert proof['all_first_internal_final_glyph_codes_pixels_input_canaries_andbounds_pass']
        assert proof['FE_expected_defaults']==dict(FI='Rafael',FA='Castor',FO='Castor Co.')
    targets={r['id']:r for r in plans['records']};manuscript_rows={r['id']:r for r in doc['records']}
    rows={r['id']:deepcopy(r) for r in reused['records']}
    origins={k:dict(kind='qualified-completed-native-reuse',receipt=str(reused_path),
        receipt_sha256=sha(reused_path.read_bytes()),original=v) for k,v in reused['origins'].items()}
    for row in fresh['records']:
        assert row['id'] not in rows
        rows[row['id']]=deepcopy(row)
        origins[row['id']]=dict(kind='fresh-complete-native-run',receipt=str(fresh_path),receipt_sha256=sha(fresh_path.read_bytes()))
    assert len(rows)==539
    changed=delta['records'][0];assert changed['id']=='DK4_MES_B70_R0193'
    assert rows[changed['id']]['compiled_hex']!=changed['compiled_hex']
    rows[changed['id']]=deepcopy(changed)
    origins[changed['id']]=dict(kind='fresh-final-page-boundary',receipt=str(delta_path),receipt_sha256=sha(delta_path.read_bytes()))
    pages=0;FE=0
    for key,row in rows.items():
        target=targets[key];original=manuscript_rows[key]
        assert row['compiled_hex']==target['encoded_hex'] and row['logical_English']==target['logical_English']==original['english']
        assert row['source_reference']==original['source_reference'] and row['current_reference']==original['current_reference']
        assert bytes.fromhex(row['compiled_hex'])[0]==original['source_selector']
        assert len(row['native_alignment']['cases'])==4
        assert all(c['output_hex']==row['expanded_native_hex'] for c in row['native_alignment']['cases'])
        rendered=row['complete_native_English_display']
        if row['kind']=='system-FE':
            FE+=1;count=1
            assert rendered['all_first_internal_final_ASCII_CP932_codes_andindependent_logical_plane_exact']
            comparison=rendered['planned_native_row_comparison'];assert comparison['complete_glyph_row_membership_exact']
            assert comparison['planned_rows']==comparison['actual_rows']
        else:
            assert rendered['all_visible_first_internal_final_characters_in_order'] and rendered['no_blank_or_overlap_page']
            assert rendered['complete_consumed_bytes']==len(bytes.fromhex(row['expanded_native_hex']))
            count=len(rendered['pages'])
        assert count==target['expected_native_pages'];pages+=count
    assert pages==545 and FE==6 and len(targets)==539 and not plans['failures']
    r87=rows['DK4_MES_B69_R0087']['complete_native_English_display']['planned_native_row_comparison']
    assert r87['actual_rows']==['Hee hee, thank you. Come along.','There is plenty of food!']
    before=load(ROOT/'automatic_v2/automatic_plans.json');old={r['id']:r for r in before['records']}
    changed_IDs=[k for k in rows if old[k]['encoded_hex']!=targets[k]['encoded_hex']]
    assert len(changed_IDs)==27
    save(output,dict(manuscript=str(manuscript),manuscript_sha256=sha(manuscript.read_bytes()),
        plan=str(plan_path),plan_sha256=sha(plan_path.read_bytes()),runtime=fresh['runtime'],font_sha256=fresh['font_sha256'],
        records=[rows[r['id']] for r in doc['records']],origins=origins,pages=545,
        final_records=539,progressive_records=533,Charlotte_FE_records=5,military_funds_FE_notices=1,
        final_compatible_reused_records=288,final_compatible_reused_pages=292,
        complete_fresh_remaining_records=250,complete_fresh_remaining_pages=251,final_delta_records=1,final_delta_pages=2,
        source_owned_FE_expected_value_adapter=fresh['source_owned_FE_expected_value_adapter'],
        FE_expected_defaults=fresh['FE_expected_defaults'],FE_R87_actual_rows=r87,
        complete_consumption_andpagination_exact=True,
        all_first_internal_final_glyph_codes_pixels_input_canaries_andbounds_pass=True,
        all_source_selectors_controls_substitution_order_andparagraph_words_exact=True,
        final_all_English_ASCII=True,changed_compiled_record_IDs_since_initial547_page_plan=changed_IDs,
        layout_refinements=13,ellipsis_glyph_refinements=14,fullwidth_I_corrections=16,
        two_unnecessary_pages_removed_without_shortening_prose=True,
        failed_full_runs_preserved_with_only_completed_compatible_block_reuse=True,
        direct_visual_review_pending=True,all_individual_fifth_gates_still_false=True,
        stored_source_control_flow_actual_headers_CG_transitions_andregistered_integration_pending=True,
        actual_gameplay=False,new_credit=0,guide_photos=False,
        evidence={str(p):sha(p.read_bytes()) for p in [manuscript,plan_path,reused_path,fresh_path,delta_path,
            ROOT/'Charlotte_FE_R87_row_finding_v1.json',ROOT/'ellipsis_native_visual_finding_v1.json',Path(__file__)]}))
    print('539 records/545 final native pages pass;all six FE rows/four-alignment substitutions/control/glyph/bounds/pagination checks pass.27 compiled changes:13 layout/14 ellipsis;visual/storage/gameplay/integration remain.',flush=True)
