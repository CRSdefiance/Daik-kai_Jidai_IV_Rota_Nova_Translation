"""Audit final14-report completion plus next8 withdrawal source-only handoff."""
from pathlib import Path
OLD=Path('scripts/verify_editorial_handoff_v2553.py')
if __name__=='__main__':
 outer=OLD.read_text();needle="\n exec(compile(source,__file__,'exec'),{'__name__':'__main__','__file__':__file__})";assert outer.count(needle)==1
 env={'__name__':'__main__','__file__':__file__};exec(compile(outer.replace(needle,'\n captured_effective_source=source'),__file__,'exec'),env);source=env['captured_effective_source']
 changes={'editorial_handoff_verification_v2553':'editorial_handoff_verification_v2556','V2553-audit-of-V2552':'V2556-audit-of-V2555',
  'work/analysis/aftermath_defeat_completion_v2552/completion_receipt.json':'work/analysis/aftermath_withdrawal_source_handoff_v2555b/handoff_receipt.json',
  "h['fresh_reconciliations']==14":"h['completed_this_goal_turn']==14",'# Current editorial handoff - V2552':'# Current editorial handoff - V2555'}
 for a,b in changes.items():assert a in source,a;source=source.replace(a,b)
 extra=""" assert h['next_packet_records']==8 and h['next_packet_fresh_credit']==0
 packetpath=Path('work/analysis/aftermath_withdrawal_context_v2554/all8_clean_current_context_catalog.json');packet=read(packetpath)
 contextpath=Path('work/analysis/aftermath_withdrawal_context_v2554/source_context_packet.json');nextcontext=read(contextpath)
 preflight=read('work/analysis/aftermath_withdrawal_context_v2554/next8_preflight.json')
 assert packet['selected_IDs']==list(range(2114,2122))and len(packet['neighbors'])==2 and packet['source_prose_or_fresh_pass_credit_added']==0
 assert packet['current_ROM_sha256']==digest and packet['current_ARM9_sha256']==sha(arm)and packet['current_COMMON_sha256']==sha(common)
 assert sha(packetpath.read_bytes())==preflight['packet_sha256']and sha(contextpath.read_bytes())==preflight['source_context_sha256']and preflight['fresh_credit']==0
 assert nextcontext['original_signed_eight_members']==list(range(2114,2122))and len(nextcontext['all208_original_voice_selections'])==208
 assert all(r['message_ID']==2114+r['voice_class']for r in nextcontext['all208_original_voice_selections'])
 assert len(nextcontext['original_mode2_withdrawal_prefix'])==1 and nextcontext['original_mode2_withdrawal_prefix'][0]['arguments'][:2]==[1,0x02117D00]
 assert len(nextcontext['three_original7251C_mode2_callsites'])==3 and all(r['source_mode']==2 for r in nextcontext['three_original7251C_mode2_callsites'])
 samples=nextcontext['current_original513D0_on9_historical_town_ship_positions'];assert len(samples)==9 and {r['current_original513D0_result']for r in samples}>={0,1,2}
 assert all(r['current_original513D0_result']==r['original_result']and r['CPU_scratch_point_copies_only_no_emulator_position_change']for r in samples)
 for r in nextcontext['original_source_code']:assert sha(arm[r['start']:r['end']])==r['sha256']and r['current_clean_snapshot_exact']
 prior={r['message_id']:r for r in read(preflight['registered_manuscript'])['records']}
 for r in packet['records']:
  n=r['message_ID'];e=entries[n];j=jp[n]
  assert r['source_hex']==j.text.hex()==prior[n]['source_hex']and r['current_hex']==e.text.hex()and compiled(prior[n])==e.text
  assert all(r['source_reference'][k]==v for k,v in dict(block=j.block,offset=j.block_offset,copy_end=j.copy_end,bytes=len(j.text)).items())
  assert all(r['current_reference'][k]==v for k,v in dict(block=e.block,offset=e.block_offset,copy_end=e.copy_end,bytes=len(e.text)).items())
  assert('/COMMON/MESFILE.DK4',f'COMMON_MESSAGE_{n}')not in keys
 previous=read('work/analysis/editorial_handoff_verification_v2553/verified_handoff.json')
 assert previous['ledger_sha256']==sha(Path('work/analysis/aftermath_withdrawal_source_handoff_v2555b/editorial_review_current_v1.json.before').read_bytes())
 assert not Path('work/analysis/aftermath_withdrawal_source_handoff_v2555').exists()
"""
 needle=' ROOT.mkdir(parents=True)';assert source.count(needle)==1;source=source.replace(needle,extra+needle)
 source=source.replace('all14_exact_clean_current_integrated_references_payloads_and_five_gates=True,','next8_context_packet=str(packetpath),next8_context_packet_sha256=sha(packetpath.read_bytes()),next8_context_only_credit0=True,preserved_handoff_prewrite_adapter_failure_sha256=sha(Path("scripts/record_aftermath_withdrawal_handoff_v2555.py").read_bytes()),all14_exact_clean_current_integrated_references_payloads_and_five_gates=True,')
 source=source.replace('retentions=14,metadata_revisions=0','retentions=14,next8_context_credit=0,metadata_revisions=0')
 exec(compile(source,__file__,'exec'),{'__name__':'__main__','__file__':__file__})
