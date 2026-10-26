"""Final city8 audit plus zero-credit six-alert powder-fire source handoff."""
from pathlib import Path
OLD=Path('scripts/verify_editorial_handoff_v2569.py')
if __name__=='__main__':
 outer=OLD.read_text();needle="\n exec(compile(source,__file__,'exec'),{'__name__':'__main__','__file__':__file__})";assert outer.count(needle)==1
 env={'__name__':'__main__','__file__':__file__};exec(compile(outer.replace(needle,'\n captured_effective_source=source'),__file__,'exec'),env);source=env['captured_effective_source']
 changes={'editorial_handoff_verification_v2569':'editorial_handoff_verification_v2572','V2569-audit-of-V2568':'V2572-audit-of-V2571',
  'work/analysis/aftermath_city_completion_v2568/completion_receipt.json':'work/analysis/powder_fire_source_handoff_v2571/handoff_receipt.json',"h['fresh_reconciliations']==8":"h['completed_this_goal_turn']==8",'# Current editorial handoff - V2568':'# Current editorial handoff - V2571'}
 for a,b in changes.items():
  assert a in source,a
  source=source.replace(a,b)
 extra=""" assert h['next_packet_records']==6 and h['next_packet_fresh_credit']==0
 packetpath=Path('work/analysis/powder_fire_context_v2570/all6_clean_current_context_catalog.json');packet=read(packetpath)
 contextpath=Path('work/analysis/powder_fire_context_v2570/source_context_packet.json');nextcontext=read(contextpath)
 preflight=read('work/analysis/powder_fire_context_v2570/next6_preflight.json')
 assert packet['selected_IDs']==list(range(2052,2058))and len(packet['neighbors'])==2 and len(packet['extinguished_followup_candidates_context_only'])==2 and packet['source_prose_or_fresh_pass_credit_added']==0
 assert packet['current_ROM_sha256']==digest and packet['current_ARM9_sha256']==sha(arm)and packet['current_COMMON_sha256']==sha(common)
 assert sha(packetpath.read_bytes())==preflight['packet_sha256']and sha(contextpath.read_bytes())==preflight['source_context_sha256']and preflight['fresh_credit']==0
 values=nextcontext['original_signed_eight_members'];assert values==[2052,2053,-1,-1,2054,2055,2056,2057]and len(nextcontext['all208_original_voice_selections'])==208
 for r in nextcontext['all208_original_voice_selections']:
  value=values[r['voice_class']];assert r['message_ID']==(value if value!=-1 else 2052)and r['original_negative_member_fallback']==(value==-1)
 assert nextcontext['original_entry']==0x02053F0C and nextcontext['original_parent']==0x02053F40 and nextcontext['original_table_stack_offset']==0x274 and nextcontext['actual_source_selected_ID']==2053
 bindings=nextcontext['four_current_original_gun_position_speaker_prefixes'];assert len(bindings)==4 and[r['original_battery_slot']for r in bindings]==[0,1,2,3]
 for r in bindings:
  assert r['original_call']['entry']==0x02053F0C and r['original_call']['arguments'][:2]==[r['original_gunner_object'],0x02117980]and r['original_call']['original_return']==0x02075614
  assert r['all_executed_section_code_current_exact']and r['actor_model_bytes_unchanged']and r['CPU_stack_slot_argument_only_no_new_fire_or_eligibility_claim']and r['executed_current_instruction_addresses']>0
 for r in nextcontext['original_source_code']:assert sha(arm[r['start']:r['end']])==r['sha256']and r['current_clean_historical_snapshot_exact']
 from scripts.powder_fire_native_plan_v1309 import compiled as powder_compiled
 prior={r['message_id']:r for r in read(preflight['registered_manuscript'])['records']}
 for r in packet['records']:
  n=r['message_ID'];e=entries[n];j=jp[n]
  assert r['source_hex']==j.text.hex()==prior[n]['source_hex']and r['current_hex']==e.text.hex()and powder_compiled(prior[n])==e.text
  assert all(r['source_reference'][k]==v for k,v in dict(block=j.block,offset=j.block_offset,copy_end=j.copy_end,bytes=len(j.text)).items())
  assert all(r['current_reference'][k]==v for k,v in dict(block=e.block,offset=e.block_offset,copy_end=e.copy_end,bytes=len(e.text)).items())
  assert('/COMMON/MESFILE.DK4',f'COMMON_MESSAGE_{n}')not in keys
 for r in packet['extinguished_followup_candidates_context_only']:
  n=r['message_ID'];assert r['source_hex']==jp[n].text.hex()and r['current_hex']==entries[n].text.hex()and not r['selected']
 assert packet['followup585_586_identical_current_payload']==(entries[585].text==entries[586].text)
 stage=manifest['relocations']['/COMMON/MESFILE.DK4']['powder_fire_editorial'];cfg=read(preflight['registered_config'])
 assert sha(Path(preflight['registered_config']).read_bytes())==stage['release_config_sha256']and stage['proof']['native_IDs']==list(range(2052,2058))
 assert sha(Path(cfg['manuscript']).read_bytes())==cfg['dependencies'][cfg['manuscript']]
 previous=read('work/analysis/editorial_handoff_verification_v2569/verified_handoff.json')
 assert previous['ledger_sha256']==sha(Path('work/analysis/powder_fire_source_handoff_v2571/editorial_review_current_v1.json.before').read_bytes())
"""
 needle=' ROOT.mkdir(parents=True)';assert source.count(needle)==1;source=source.replace(needle,extra+needle)
 source=source.replace('all8_exact_clean_current_integrated_references_payloads_and_five_gates=True,','next6_powder_fire_context_packet=str(packetpath),next6_powder_fire_context_packet_sha256=sha(packetpath.read_bytes()),next6_context_only_credit0=True,all8_exact_clean_current_integrated_references_payloads_and_five_gates=True,')
 source=source.replace('retentions=8,metadata_revisions=0','retentions=8,next6_context_credit=0,metadata_revisions=0')
 exec(compile(source,__file__,'exec'),{'__name__':'__main__','__file__':__file__})
