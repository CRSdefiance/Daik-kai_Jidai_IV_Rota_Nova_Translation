"""Prepare an independent exact-source/current/final completion audit."""
import re
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import save
if __name__=='__main__':
    old=Path('scripts/verify_editorial_handoff_v3305.py');new=Path('scripts/verify_editorial_handoff_v3343b.py');assert not new.exists();t=old.read_text(encoding='utf-8')
    changes={
      'editorial_handoff_verification_v3305':'editorial_handoff_verification_v3343b',
      'lil_B122_B127_completion_v3304':'lil_B131_B133_completion_v3342b',
      'lil_B122_B127_registration_v3299b':'lil_B131_B133_registration_v3337b',
      'lil_B122_B127_editorial_v2':'lil_B131_B133_editorial_v1',
      'lil_B122_B127_scope_reconciliation_v3286':'lil_B131_B133_scope_reconciliation_v3327',
      'lil_after_B119_next_clean_source_lead_v3258':'lil_after_B127_next_source_lead_v3310',
      'lil_B122_B127_release_v3301':'lil_B131_B133_release_v3339',
      'all-routes-unified-v3300':'all-routes-unified-v3338',
      'list(range(122,128))':'[131,133]',
      'lil_B122_B127_startup_v3303':'lil_B131_B133_startup_v3341',
      'equal_V3251':'equal_V3300','actual_selected_B122_B127_IDs':'actual_selected_B131_B133_IDs',
      'unfinished_editorial_scope_v3304':'unfinished_editorial_scope_v3342','unfinished_editorial_scope_v3296':'unfinished_editorial_scope_v3327',
      'lil_B122_B127_build_v3300':'lil_B131_B133_build_v3338','V3304':'V3342',
      'all2_final2100_objects_four_labels_and6_selection_cancel_cases_bound':'all1_final2100_object_two_labels_and3_selection_cancel_cases_bound',
      "padding['both_original_pause_resume_words_and20_decoder_cases_bound']":"padding['no_source2000_pause_commands'] and padding['all18_final_source00_speech_prefixes_and_nonempty_bodies_preserved']",
      'all159_exact_source_predecessor_effective_integrated_references_verified':'all63_exact_source_predecessor_effective_integrated_references_verified',
      'all155_speech_planes_four_labels_two_pauses_conditional_returns_and_all_release_gates_verified':'all61_speech_planes_two_labels_source00_and_all_release_gates_verified',
      'all23_native_sheets_and_current6frame_sheet_reviewed':'all10_native_sheets_and_current6frame_sheet_reviewed',
      'canonical_Maria32_Proof_consistency_source00_B133_and_all_wider_scope_preserved':'canonical_Maria32_Proof_consistency_B135_B140_and_all_wider_scope_preserved',
    }
    for a,b in sorted(changes.items(),key=lambda kv:-len(kv[0])):assert a in t,a;t=t.replace(a,b)
    counts={4734:4797,4737:4800,3142:3169,1592:1628,2907:2970,3135:3198,159:63,155:61,55:27,104:36,519:521,312:112,64:24,320:120,1240:488,620:244,68:19}
    t=re.sub(r'(?<!\d)(4734|4737|3142|1592|2907|3135|159|155|55|104|519|312|64|320|1240|620|68)(?!\d)',lambda m:str(counts[int(m[0])]),t)
    t=t.replace("sum(len(b['choice_commands']) for b in mapping['blocks'])==2","sum(len(b['choice_commands']) for b in mapping['blocks'])==1")
    a=t.index('    pauses=');z=t.index('    font,padding,sample=',a)
    t=t[:a]+"    assert not any(b['original2000_pause_and_resume_maps'] for b in mapping['blocks'])\n"+t[z:]
    t=t.replace("len(font['source_consumer_negative_controls'])==23","len(font['source_consumer_negative_controls'])==22").replace("len(font['review_sheets'])==23","len(font['review_sheets'])==10")
    a=t.index('    fe,control,branch=');z=t.index('    assert sample[',a)
    t=t[:a]+"""    fe,control,typed=map(read,[doc['native_FE_font_proof'],doc['relocated_control_proof'],doc['whole_typed_speech_proof']])
    assert len(fe['cases'])==1 and fe['current_original_null_actor_macro_alignment_cases']==8 and not fe['source_leading_vertical_staging_cases']
    assert len(control['relocated_dispatch_cases'])==61 and len(control['relocated_predicate_pairs'])==5 and control['original_event_queries']==[] and control['all18_final_source00_speeches_are_static_Rafael0_without_role_assignment']
    assert len(typed['cases'])==366 and typed['all108_source00_cases_forward_nonempty_body_after_selector_to_original_display']
    zero=[r for r in rows if r.get('source_selector')==0]
    assert len(zero)==18 and all(bytes.fromhex(r['integrated_hex']).count(b'\\0')==1 and bytes.fromhex(r['integrated_hex'])[0]==0 and r['english'].startswith('{SPEAKER:00}') for r in zero)
    assert any(c['case']=='shared-encoder-still-rejects-source00' and c['rejected'] for c in font['source_consumer_negative_controls'])
"""+t[z:]
    t=t[:t.rindex('    print(')]+"    print('IndependentV3342 audit passes:63completed,4797reread/integrated,4800source-prose;521batches/114layers/exactpatch/31freshframepairs. Full widergoal remains active.')\n"
    compile(t,str(new),'exec');new.write_text(t,encoding='utf-8')
    root=Path('work/analysis/lil_B131_B133_audit_tools_v3343');root.mkdir(parents=True)
    save(root/'provenance.json',dict(previous=str(old),previous_sha256=sha(old.read_bytes()),successor=str(new),successor_sha256=sha(new.read_bytes()),producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
