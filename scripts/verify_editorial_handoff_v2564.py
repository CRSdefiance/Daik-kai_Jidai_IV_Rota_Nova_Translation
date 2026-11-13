"""Final withdrawal8 audit plus zero-credit direct-city source packet."""
from pathlib import Path
OLD=Path('scripts/verify_editorial_handoff_v2561.py')
if __name__=='__main__':
 outer=OLD.read_text();a='"\'/COMMON/MESFILE.DK4\':137":"\'/COMMON/MESFILE.DK4\':115"';b='"\'/COMMON/MESFILE.DK4\':137,":"\'/COMMON/MESFILE.DK4\':115,"';assert outer.count(a)==1;outer=outer.replace(a,b)
 needle="\n exec(compile(source,__file__,'exec'),{'__name__':'__main__','__file__':__file__})";assert outer.count(needle)==1
 env={'__name__':'__main__','__file__':__file__};exec(compile(outer.replace(needle,'\n captured_effective_source=source'),__file__,'exec'),env);source=env['captured_effective_source']
 changes={'editorial_handoff_verification_v2561':'editorial_handoff_verification_v2564','V2561-audit-of-V2560':'V2564-audit-of-V2563',
  'work/analysis/aftermath_withdrawal_completion_v2560/completion_receipt.json':'work/analysis/aftermath_city_source_handoff_v2563/handoff_receipt.json',
  "h['fresh_reconciliations']==8":"h['completed_this_goal_turn']==8",'# Current editorial handoff - V2560':'# Current editorial handoff - V2563'}
 for a,b in changes.items():
  assert a in source,a
  source=source.replace(a,b)
 extra=""" assert h['next_packet_records']==8 and h['next_packet_fresh_credit']==0
 packetpath=Path('work/analysis/aftermath_city_context_v2562/all8_clean_current_context_catalog.json');packet=read(packetpath)
 contextpath=Path('work/analysis/aftermath_city_context_v2562/source_context_packet.json');nextcontext=read(contextpath)
 preflight=read('work/analysis/aftermath_city_context_v2562/next8_preflight.json')
 assert packet['selected_IDs']==list(range(2038,2046))and len(packet['neighbors'])==2 and packet['source_prose_or_fresh_pass_credit_added']==0
 assert packet['current_ROM_sha256']==digest and packet['current_ARM9_sha256']==sha(arm)and packet['current_COMMON_sha256']==sha(common)
 assert sha(packetpath.read_bytes())==preflight['packet_sha256']and sha(contextpath.read_bytes())==preflight['source_context_sha256']and preflight['fresh_credit']==0
 assert nextcontext['original_signed_eight_members']==list(range(2038,2046))and len(nextcontext['all208_original_voice_selections'])==208
 assert all(r['message_ID']==2038+r['voice_class']for r in nextcontext['all208_original_voice_selections'])
 assert nextcontext['original_entry']==0x02053F0C and nextcontext['original_parent']==0x02053F40 and nextcontext['original_table_stack_offset']==0x274
 bindings=nextcontext['three_current_original_city_defender_captain_bindings'];assert len(bindings)==3
 for r in bindings:assert r['original_call']['entry']==0x02053F0C and r['original_call']['arguments'][:2]==[r['source_captain_object'],0x021178C0]and r['original_call']['original_return']==0x0206EE30
 assert bindings[-1]['source_fleet_ID']==22 and bindings[-1]['source_captain_actor_ID']==46 and nextcontext['historical_actual_selected_ID']==2043
 for r in nextcontext['original_source_code']:assert sha(arm[r['start']:r['end']])==r['sha256']and r['current_clean_historical_snapshots_exact']
 prior={r['message_id']:r for r in read(preflight['registered_manuscript'])['records']}
 for r in packet['records']:
  n=r['message_ID'];e=entries[n];j=jp[n]
  assert r['source_hex']==j.text.hex()==prior[n]['source_hex']and r['current_hex']==e.text.hex()and compiled(prior[n])==e.text
  assert all(r['source_reference'][k]==v for k,v in dict(block=j.block,offset=j.block_offset,copy_end=j.copy_end,bytes=len(j.text)).items())
  assert all(r['current_reference'][k]==v for k,v in dict(block=e.block,offset=e.block_offset,copy_end=e.copy_end,bytes=len(e.text)).items())
  assert('/COMMON/MESFILE.DK4',f'COMMON_MESSAGE_{n}')not in keys
 previous=read('work/analysis/editorial_handoff_verification_v2561b/verified_handoff.json')
 assert previous['ledger_sha256']==sha(Path('work/analysis/aftermath_city_source_handoff_v2563/editorial_review_current_v1.json.before').read_bytes())
"""
 needle=' ROOT.mkdir(parents=True)';assert source.count(needle)==1;source=source.replace(needle,extra+needle)
 source=source.replace('all8_exact_clean_current_integrated_references_payloads_and_five_gates=True,','next8_direct_city_context_packet=str(packetpath),next8_direct_city_context_packet_sha256=sha(packetpath.read_bytes()),next8_context_only_credit0=True,preserved_bounded_inventory_adapter_successor_sha256=sha(Path("scripts/verify_editorial_handoff_v2561b.py").read_bytes()),all8_exact_clean_current_integrated_references_payloads_and_five_gates=True,')
 source=source.replace('retentions=8,metadata_revisions=0','retentions=8,next8_context_credit=0,metadata_revisions=0')
 exec(compile(source,__file__,'exec'),{'__name__':'__main__','__file__':__file__})
