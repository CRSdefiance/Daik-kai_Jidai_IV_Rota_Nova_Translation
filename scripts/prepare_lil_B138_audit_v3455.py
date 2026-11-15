"""Prepare an independent44-record completion audit including query/raw-result guards."""
import re
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import save
if __name__=='__main__':
    a=Path('scripts/verify_editorial_handoff_v3421b.py');b=Path('scripts/verify_editorial_handoff_v3455.py');assert not b.exists();t=a.read_text(encoding='utf-8')
    placeholders={'lil_B137_registered_hook_repair_v3415':'__OLDHOOKLEDGER__','B137_registered_hook_repair_v3415':'__OLDHOOKINVENTORY__','work/analysis/lil_B137_build_v3409/build_terminal.json':'__OLDFAILEDBUILD__'}
    for x,y in placeholders.items():assert x in t,x;t=t.replace(x,y)
    t=t.replace("profile['lil_B137_editorial_v2']==owned.CONFIG and 'lil_B137_editorial' not in profile","profile['lil_B138_editorial']==owned.CONFIG and 'lil_B138_editorial_v2' not in profile")
    t=t.replace("newprofile.pop('lil_B137_editorial_v2')","newprofile.pop('lil_B138_editorial')").replace("['lil_B137_editorial_v2']['proof']","['lil_B138_editorial']['proof']")
    t=t.replace('from dk4tool.patch import lil_B137_editorial_v2','from dk4tool.patch import lil_B138_editorial_v1')
    changes=[('editorial_handoff_verification_v3421','editorial_handoff_verification_v3455'),('lil_B137_completion_v3420','lil_B138_completion_v3454'),('lil_B137_registration_v3415','lil_B138_registration_v3449'),('lil_B137_scope_reconciliation_v3399','lil_B138_scope_reconciliation_v3439'),('lil_B137_release_v3417','lil_B138_release_v3451'),('lil_B137_registration_v3408b/registry_before_raw.json','lil_B138_registration_v3449/registry_before_raw.json'),('lil_B137_startup_v3419','lil_B138_startup_v3453'),('lil_B137_build_v3416','lil_B138_build_v3450'),('unfinished_editorial_scope_v3420','unfinished_editorial_scope_v3454'),('unfinished_editorial_scope_v3415','unfinished_editorial_scope_v3447'),('V3420','V3454'),('v3416','__NEWPROFILE__'),('v3372','v3416'),('__NEWPROFILE__','v3450'),('V3372','V3416'),('lil_B137','lil_B138'),('B137','B138'),('[137]','[138]'),('(3224,2988)','(2756,2356)'),("{'revise':22,'retain-wording':26}","{'revise':16,'retain-wording':28}"),('revisions=22,justified_retentions=26','revisions=16,justified_retentions=28'),('{2,9,14,16,17,20,22,23,38,92,198}','{2,14,20,21,22,23,92}'),('all_eleven_static_speaker_selectors_preserved_without_role_assignment','all_seven_static_speaker_selectors_preserved_without_role_assignment'),("len(control['relocated_predicate_pairs'])==12 and control['original_event_queries']==[]","len(control['relocated_predicate_pairs'])==11 and len(control['original_event_queries'])==1 and control['original_event_queries'][0]['event']==137"),('all48_final_planes192_macros_static_dispatches_and12_predicates_bound','all44_final_planes176_macros_static_dispatches10_predicates_and1_query_bound'),("registration['failed_profile_and_old_hook_preserved_exactly']","registration['stage_import_module']==owned.__name__"),('B138_B140_and_all_wider_scope_preserved','B139_B140_and_all_wider_scope_preserved')]
    for x,y in changes:assert x in t,x;t=t.replace(x,y)
    counts={4880:4924,4883:4927,3207:3223,1673:1701,3053:3097,3281:3325,48:44,384:352,192:176,31:23,18:21,117:111,240:225,523:524}
    t=re.sub(r'(?<!\d)('+ '|'.join(map(str,sorted(counts,key=lambda n:-len(str(n)))))+r')(?!\d)',lambda m:str(counts[int(m[0])]),t)
    #31 captured framebuffer pairs remain31; only source-consumer negatives become23.
    t=t.replace("start['paired_frame_count']==23","start['paired_frame_count']==31").replace('paired_current_whole_framebuffers=23','paired_current_whole_framebuffers=31').replace('23 fresh frame pairs','31 fresh frame pairs')
    t=t.replace("sum(len(b['relative_skip_fixups']) for b in mapping['blocks'])==44","sum(len(b['relative_skip_fixups']) for b in mapping['blocks'])==45")
    start=t.index("    shock=next(");end=t.index("    assert sum(bool(r.get('qa_waivers'))",start)
    t=t[:start]+"""    for ident in ['DK4_MES_B138_R0078','DK4_MES_B138_R0253']:
        question=next(r for r in rows if r['id']==ident);assert question['integrated_hex']=='023f20' and question['historical_source_prose_predecessor_fields']['current_hex']=='028148' and question['editorial_decision']=='retain-wording'
        proof=next(c for c in padding['final_target_parity_cases'] if c['id']==ident);assert [(e['code'],e['x'],e['y']) for e in proof['complete_native_glyph_events'] if e['code']!=32]==[(63,0,0)]
"""+t[end:]
    t=t.replace("len(negatives['cases'])==28 and negatives['all_rejected_before_mutation'] and registration['negative_tests_reused_by_exact_validated_compiler_and_config_hash']","len(negatives['cases'])==35 and negatives['all_rejected_before_mutation'] and all(c['rejected_before_mutation'] for c in negatives['cases'])")
    line="    assert (REG/'negative_cases.json').read_bytes()==Path(registration['reused_negative_proof']).read_bytes()\n";assert line in t;t=t.replace(line,'')
    marker="    negatives=read(REG/'negative_cases.json')";assert marker in t
    extra="""    assert control['source_predicate_result_constants']['0080ffff200301a1']==2 and control['portable_source_owned_adapters']['predicate'].startswith('SCOPED_RESULTS=')
    for p in control['relocated_predicate_pairs']:
        left,right=p['cases'];assert left['native_result']==right['native_result'] and left['source_command_hex']==right['source_command_hex']
        if left['source_command_hex']=='0080ffff200301a1':assert left['native_result']==[2,2,0,0,0,0]
    assert mapping['all10_predicates_and1_query_current_relocated_results_and_source_operands_equal'] and len(mapping['original_event_queries'])==1 and mapping['original_event_queries'][0]['event']==137
"""
    t=t.replace(marker,extra+marker).replace('wordless_shock_one_complete_glyph_and_private_thought_parentheses_preserved','two_wordless_questions_complete_and_raw_result2_query_preserved')
    for x,y in placeholders.items():t=t.replace(y,x)
    compile(t,str(b),'exec');b.write_text(t,encoding='utf-8');root=Path('work/analysis/lil_B138_audit_tools_v3455');assert not root.exists();root.mkdir(parents=True)
    save(root/'provenance.json',dict(previous=str(a),previous_sha256=sha(a.read_bytes()),successor=str(b),successor_sha256=sha(b.read_bytes()),producer_sha256=sha(Path(__file__).read_bytes()),all_previous_producers_preserved=True,no_ledger_or_ROM_mutation=True,full_goal_complete=False))
