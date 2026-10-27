"""Final fire6 audit plus next5 capture contexts with exact two-owner provenance."""
from pathlib import Path
OLD=Path('scripts/verify_editorial_handoff_v2577.py')
if __name__=='__main__':
 source=OLD.read_text()
 changes={
  'editorial_handoff_verification_v2577':'editorial_handoff_verification_v2580','V2577-audit-of-V2576':'V2580-audit-of-V2579',
  'work/analysis/powder_fire_completion_v2576/completion_receipt.json':'work/analysis/flagship_capture_source_handoff_v2579/handoff_receipt.json',
  "receipt['fresh_reconciliations']==6":"receipt['completed_this_goal_turn']==6",'# Current editorial handoff - V2576':'# Current editorial handoff - V2579'}
 for a,b in changes.items():
  assert a in source,a
  source=source.replace(a,b)
 extra=""" assert receipt['next_packet_records']==5 and receipt['next_packet_fresh_credit']==0
 packetpath=Path('work/analysis/flagship_capture_context_v2578/all5_clean_current_context_catalog.json');packet=read(packetpath)
 contextpath=Path('work/analysis/flagship_capture_context_v2578/source_context_packet.json');nextcontext=read(contextpath)
 preflight=read('work/analysis/flagship_capture_context_v2578/next5_preflight.json')
 assert packet['selected_IDs']==list(range(2011,2016))and len(packet['neighbors'])==2 and packet['source_prose_or_fresh_pass_credit_added']==0
 assert packet['current_ROM_sha256']==digest and packet['current_ARM9_sha256']==sha(arm)and packet['current_COMMON_sha256']==sha(common)
 assert sha(packetpath.read_bytes())==preflight['packet_sha256']and sha(contextpath.read_bytes())==preflight['source_context_sha256']and preflight['fresh_credit']==0
 values=nextcontext['original_signed_eight_members'];assert values==[2011,-1,2012,-1,-1,2013,2014,2015]and len(nextcontext['all208_original_voice_selections'])==208
 for r in nextcontext['all208_original_voice_selections']:
  value=values[r['voice_class']];assert r['message_ID']==(value if value!=-1 else 2011)and r['original_negative_member_fallback']==(value==-1)
 assert nextcontext['original_entry']==0x02053D44 and nextcontext['original_parent']==0x02053DB8 and nextcontext['original_table_stack_offset']==0x27C and nextcontext['original_role_selector']==1
 assert nextcontext['actual_logical_member_ID']==16 and nextcontext['actual_physical_FirstMate_object']==0 and nextcontext['actual_voice1_negative_member_falls_back_to2011']
 assert nextcontext['original53D44_call_to82478']['mnemonic']=='bl'and nextcontext['original53D44_call_to82478']['operands']=='#0x2082478'
 assert len(nextcontext['three_current_original72368_outcome_prefixes'])==3
 for r in nextcontext['original_source_code']:assert sha(arm[r['start']:r['end']])==r['sha256']and r['current_clean_historical_snapshot_exact']
 from importlib import import_module
 owners=preflight['registered_prose_owner_bindings'];assert len(owners)==2 and owners==packet['registered_prose_owner_bindings']==nextcontext['registered_prose_owner_bindings']
 rows={};owner_by_ID={};compiler_by_ID={}
 for owner in owners:
  stage=manifest['relocations']['/COMMON/MESFILE.DK4'][owner['stage']];cfgpath=Path(owner['registered_config']);cfg=read(cfgpath);docpath=Path(owner['registered_manuscript'])
  assert sha(cfgpath.read_bytes())==owner['registered_config_sha256']==stage['release_config_sha256']and sha(docpath.read_bytes())==owner['registered_manuscript_sha256']==cfg['dependencies'][str(docpath)]
  module,attribute=owner['compiler'].rsplit('.',1);prose_compiler=getattr(import_module(module),attribute)
  selected={r['message_id']:r for r in read(docpath)['records']if r['message_id']in owner['selected_IDs']};assert set(selected)==set(owner['selected_IDs'])and set(selected)<=set(stage['proof']['native_IDs'])
  rows.update(selected)
  for n in selected:owner_by_ID[n]=owner['stage'];compiler_by_ID[n]=prose_compiler
 assert set(rows)==set(range(2011,2016))and owner_by_ID[2015]=='flagship_capture_precision'and all(owner_by_ID[n]=='battle_aftermath_editorial'for n in range(2011,2015))
 assert rows[2015]['english']=="We've captured the enemy flagship after defeating its entire crew!"
 for r in packet['records']:
  n=r['message_ID'];e=entries[n];j=jp[n]
  assert r['registered_prose_owner']==owner_by_ID[n]and r['source_hex']==j.text.hex()==rows[n]['source_hex']and r['current_hex']==e.text.hex()and compiler_by_ID[n](rows[n])==e.text
  assert all(r['source_reference'][k]==v for k,v in dict(block=j.block,offset=j.block_offset,copy_end=j.copy_end,bytes=len(j.text)).items())
  assert all(r['current_reference'][k]==v for k,v in dict(block=e.block,offset=e.block_offset,copy_end=e.copy_end,bytes=len(e.text)).items())
  assert('/COMMON/MESFILE.DK4',f'COMMON_MESSAGE_{n}')not in keys
 previous=read('work/analysis/editorial_handoff_verification_v2577/verified_handoff.json')
 assert previous['ledger_sha256']==sha(Path('work/analysis/flagship_capture_source_handoff_v2579/editorial_review_current_v1.json.before').read_bytes())
"""
 needle=' ROOT.mkdir(parents=True);save(';assert source.count(needle)==1;source=source.replace(needle,extra+needle)
 source=source.replace('all6_exact_clean_current_integrated_references_payloads_and_five_gates=True,','next5_two_owner_capture_packet=str(packetpath),next5_packet_sha256=sha(packetpath.read_bytes()),next5_context_only_credit0=True,all6_exact_clean_current_integrated_references_payloads_and_five_gates=True,')
 source=source.replace('retentions=6,ROM_and_exact_patch_unchanged=True','retentions=6,next5_context_credit=0,ROM_and_exact_patch_unchanged=True')
 exec(compile(source,__file__,'exec'),{'__name__':'__main__','__file__':__file__})
