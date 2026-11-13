"""Re-audit the updated handoff plus next six context records with no credit."""
from pathlib import Path
OLD=Path('scripts/verify_editorial_handoff_v2537.py')
if __name__=='__main__':
 source=OLD.read_text()
 changes={
 'editorial_handoff_verification_v2537':'editorial_handoff_verification_v2540',
 'V2537-audit-of-V2536':'V2540-audit-of-V2539',
 'work/analysis/duel_special_completion_v2536/completion_receipt.json':'work/analysis/aftermath_fled_source_handoff_v2539/handoff_receipt.json',
 "h['fresh_reconciliations']==15":"h['completed_this_goal_turn']==15",
 '# Current editorial handoff - V2536':'# Current editorial handoff - V2539',
 }
 for a,b in changes.items():assert a in source,a;source=source.replace(a,b)
 needle=' ROOT.mkdir(parents=True)'
 extra=""" assert h['next_packet_records']==6 and h['next_packet_fresh_credit']==0
 packetpath=Path('work/analysis/aftermath_fled_context_v2538/all6_clean_current_context_catalog.json');packet=read(packetpath)
 contextpath=Path('work/analysis/aftermath_fled_context_v2538/source_context_packet.json');nextcontext=read(contextpath)
 preflight=read('work/analysis/aftermath_fled_context_v2538/next6_preflight.json')
 assert packet['selected_IDs']==list(range(2046,2052))and len(packet['neighbors'])==2 and packet['source_prose_or_fresh_pass_credit_added']==0
 assert packet['current_ROM_sha256']==digest and packet['current_ARM9_sha256']==sha(arm)and packet['current_COMMON_sha256']==sha(common)
 assert sha(packetpath.read_bytes())==preflight['packet_sha256']and sha(contextpath.read_bytes())==preflight['source_context_sha256']and preflight['fresh_credit']==0
 assert len(nextcontext['all208_original_voice_selections'])==208 and len(nextcontext['original_three_outcome_prefixes'])==3
 values=nextcontext['original_signed_eight_members'];assert values==[2046,2047,-1,-1,2048,2049,2050,2051]
 for case in nextcontext['all208_original_voice_selections']:
  member=values[case['voice_class']];assert case['message_ID']==(2046 if member==-1 else member)and case['original_negative_member_fallback']==(member==-1)
 assert nextcontext['source_role_actor_ID_in_snapshot']==18 and nextcontext['source_role1_unassigned_original_fallback_is_Charles18']and nextcontext['unmodified_actor_IDs_and_no_CPU_roster_assignment']
 from scripts.battle_aftermath_native_plan_v1255 import compiled as aftermath_compiled
 prior={r['message_id']:r for r in read(preflight['registered_manuscript'])['records']}
 for r in packet['records']:
  n=r['message_ID'];e=entries[n];j=jp[n]
  assert r['source_hex']==j.text.hex()==prior[n]['source_hex']and r['current_hex']==e.text.hex()and aftermath_compiled(prior[n])==e.text
  assert all(r['source_reference'][k]==v for k,v in dict(block=j.block,offset=j.block_offset,copy_end=j.copy_end,bytes=len(j.text)).items())
  assert all(r['current_reference'][k]==v for k,v in dict(block=e.block,offset=e.block_offset,copy_end=e.copy_end,bytes=len(e.text)).items())
  assert('/COMMON/MESFILE.DK4',f'COMMON_MESSAGE_{n}')not in keys
 previous=read('work/analysis/editorial_handoff_verification_v2537/verified_handoff.json')
 assert previous['ledger_sha256']==sha(Path('work/analysis/aftermath_fled_source_handoff_v2539/editorial_review_current_v1.json.before').read_bytes())
"""
 assert source.count(needle)==1;source=source.replace(needle,extra+needle)
 source=source.replace('all15_exact_clean_current_integrated_references_payloads_and_five_gates=True,','next6_context_packet=str(packetpath),next6_context_packet_sha256=sha(packetpath.read_bytes()),next6_context_only_credit0=True,all15_exact_clean_current_integrated_references_payloads_and_five_gates=True,')
 source=source.replace('retentions=15,Fernando_metadata_normalizations=1','retentions=15,next6_context_credit=0,Fernando_metadata_normalizations=1')
 exec(compile(source,__file__,'exec'),{'__name__':'__main__','__file__':__file__})
