"""Final audit of updated handoff and next14 source-paired report packet."""
from pathlib import Path
OLD=Path('scripts/verify_editorial_handoff_v2545.py')
if __name__=='__main__':
 outer=OLD.read_text();needle=" exec(compile(source,__file__,'exec'),{'__name__':'__main__','__file__':__file__})"
 assert outer.count(needle)==1
 env={'__name__':'__main__','__file__':__file__};exec(compile(outer.replace(needle,' captured_effective_source=source'),__file__,'exec'),env)
 source=env['captured_effective_source']
 changes={'editorial_handoff_verification_v2545':'editorial_handoff_verification_v2548','V2545-audit-of-V2544':'V2548-audit-of-V2547',
  'work/analysis/aftermath_fled_completion_v2544/completion_receipt.json':'work/analysis/aftermath_defeat_source_handoff_v2547/handoff_receipt.json',
  "h['fresh_reconciliations']==6":"h['completed_this_goal_turn']==6",'# Current editorial handoff - V2544':'# Current editorial handoff - V2547'}
 for a,b in changes.items():assert a in source,a;source=source.replace(a,b)
 extra=""" assert h['next_packet_records']==14 and h['next_packet_fresh_credit']==0
 packetpath=Path('work/analysis/aftermath_defeat_context_v2546/all14_clean_current_context_catalog.json');packet=read(packetpath)
 contextpath=Path('work/analysis/aftermath_defeat_context_v2546/source_context_packet.json');nextcontext=read(contextpath)
 preflight=read('work/analysis/aftermath_defeat_context_v2546/next14_preflight.json')
 assert packet['selected_IDs']==[*range(2016,2022),*range(2138,2146)]and len(packet['neighbors'])==4 and len(packet['other_complete_flood_reports_context_only'])==5 and packet['source_prose_or_fresh_pass_credit_added']==0
 assert packet['current_ROM_sha256']==digest and packet['current_ARM9_sha256']==sha(arm)and packet['current_COMMON_sha256']==sha(common)
 assert sha(packetpath.read_bytes())==preflight['packet_sha256']and sha(contextpath.read_bytes())==preflight['source_context_sha256']and preflight['fresh_credit']==0
 assert len(nextcontext['all416_original_selected_voice_choices'])==416 and len(nextcontext['all208_complete_original_voice_report_pairs'])==208 and len(nextcontext['original_three_outcome_prefixes'])==3
 assert nextcontext['unassigned_role1_original_fallback_actor18_pairs2016_2138']and nextcontext['no_actor_ID_or_roster_changes']
 lookup={}
 for t in nextcontext['original_voice_tables']:
  values=t['signed_eight_members'];assert len(t['all208_original_voice_selections'])==208 and len(values)==8
  for r in t['all208_original_voice_selections']:
   value=values[r['voice_class']];assert r['message_ID']==(value if value!=-1 else next(n for n in values if n!=-1))
   lookup[r['actor_slot'],t['table']]=r['message_ID']
 for r in nextcontext['all208_complete_original_voice_report_pairs']:
  assert r['source_mode0_messages']==[lookup[r['actor_slot'],table]for table in(0x02117760,0x02117F00)]and r['source_mode1_messages'][1]==r['source_mode0_messages'][1]
 assert len({tuple(r['source_mode0_messages'])for r in nextcontext['all208_complete_original_voice_report_pairs']})==8
 for r in packet['records']+packet['other_complete_flood_reports_context_only']:
  n=r['message_ID'];e=entries[n];j=jp[n]
  assert r['source_hex']==j.text.hex()and r['current_hex']==e.text.hex()
  assert all(r['source_reference'][k]==v for k,v in dict(block=j.block,offset=j.block_offset,copy_end=j.copy_end,bytes=len(j.text)).items())
  assert all(r['current_reference'][k]==v for k,v in dict(block=e.block,offset=e.block_offset,copy_end=e.copy_end,bytes=len(e.text)).items())
  assert('/COMMON/MESFILE.DK4',f'COMMON_MESSAGE_{n}')not in keys
 previous=read('work/analysis/editorial_handoff_verification_v2545/verified_handoff.json')
 assert previous['ledger_sha256']==sha(Path('work/analysis/aftermath_defeat_source_handoff_v2547/editorial_review_current_v1.json.before').read_bytes())
"""
 needle=' ROOT.mkdir(parents=True)';assert source.count(needle)==1;source=source.replace(needle,extra+needle)
 source=source.replace('all6_exact_clean_current_integrated_references_payloads_and_five_gates=True,','next14_context_packet=str(packetpath),next14_context_packet_sha256=sha(packetpath.read_bytes()),next14_context_only_credit0=True,audit_adapter_sha256=sha(Path("scripts/verify_editorial_handoff_v2545.py").read_bytes()),all6_exact_clean_current_integrated_references_payloads_and_five_gates=True,')
 source=source.replace('retentions=6,metadata_revisions=0','retentions=6,next14_context_credit=0,metadata_revisions=0')
 exec(compile(source,__file__,'exec'),{'__name__':'__main__','__file__':__file__})
