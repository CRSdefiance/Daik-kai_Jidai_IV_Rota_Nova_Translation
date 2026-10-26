"""Final five-capture audit plus next eight victory contexts,with no new credit."""
from pathlib import Path
if __name__=='__main__':
 source=Path('scripts/verify_editorial_handoff_v2585.py').read_text()
 changes={
  'editorial_handoff_verification_v2585':'editorial_handoff_verification_v2588','V2585-audit-of-V2584':'V2588-audit-of-V2587',
  'work/analysis/flagship_capture_completion_v2584/completion_receipt.json':'work/analysis/battle_victory_source_handoff_v2587/handoff_receipt.json',
  "receipt['fresh_reconciliations']==5":"receipt['completed_this_goal_turn']==5",'# Current editorial handoff - V2584':'# Current editorial handoff - V2587',
 }
 for a,b in changes.items():assert a in source,a;source=source.replace(a,b)
 extra=""" assert receipt['next_packet_records']==8 and receipt['next_packet_fresh_credit']==0
 packetpath=Path('work/analysis/battle_victory_context_v2586b/all8_clean_current_context_catalog.json');packet=read(packetpath)
 contextpath=packetpath.parent/'source_context_packet.json';context=read(contextpath);preflight=read(packetpath.parent/'next8_preflight.json')
 assert packet['selected_IDs']==list(range(2130,2138))and len(packet['neighbors'])==2 and packet['source_prose_or_fresh_pass_credit_added']==0
 assert packet['current_ROM_sha256']==digest and packet['current_ARM9_sha256']==sha(arm)and packet['current_COMMON_sha256']==sha(common)
 assert sha(packetpath.read_bytes())==preflight['packet_sha256']and sha(contextpath.read_bytes())==preflight['source_context_sha256']and preflight['fresh_credit']==0
 assert context['original_signed_eight_members']==list(range(2130,2138))and len(context['all208_original_voice_selections'])==208
 assert all(r['message_ID']==2130+r['voice_class']for r in context['all208_original_voice_selections'])
 assert context['actual_logical_member_ID']==16 and context['actual_physical_FirstMate_object']==0 and context['actual_voice1_selects2131']and context['no_actor_ID_roster_or_result_changes']
 assert context['original_entry']==0x02053D44 and context['original_parent']==0x02053DB8 and context['original_role_selector']==1 and context['original_table_stack_offset']==0x27C and context['original_table']==0x02117EE0
 prefix=context['one_current_original72168_victory_prefix'];assert len(prefix)==1 and prefix[0]['entry']==0x02053D44 and prefix[0]['arguments'][:2]==[1,0x02117EE0]
 for row in context['original_source_code']:assert sha(arm[row['start']:row['end']])==row['sha256']and row['current_clean_historical_snapshot_exact']
 assert context['compiler_emits_no_leading_cell_native_legacy_formatter_adds_one']and context['source2132_genuine_IC_plural_localized_as_we']and '2129 attack confirmation' in context['context']
 from scripts.battle_victory_native_plan_v1396 import compiled as victory_compiled
 nextowners=preflight['registered_prose_owner_bindings'];assert len(nextowners)==1 and nextowners==packet['registered_prose_owner_bindings']==context['registered_prose_owner_bindings']
 owner=nextowners[0];stage=manifest['relocations']['/COMMON/MESFILE.DK4'][owner['stage']];cfgpath=Path(owner['registered_config']);cfg=read(cfgpath);mp=Path(owner['registered_manuscript']);priorrows={r['message_id']:r for r in read(mp)['records']}
 assert owner['stage']=='battle_victory_editorial'and owner['compiler']=='scripts.battle_victory_native_plan_v1396.compiled'and stage['proof']['native_IDs']==owner['selected_IDs']==list(range(2130,2138))
 assert sha(cfgpath.read_bytes())==owner['registered_config_sha256']==stage['release_config_sha256']and sha(mp.read_bytes())==owner['registered_manuscript_sha256']==cfg['dependencies'][str(mp)]
 assert priorrows[2132]['source_native_macros']==['IC first-person plus plural tachi localized grammatically as we']and jp[2132].text.count(b'IC')==1
 for row in packet['records']:
  n=row['message_ID'];e,j=entries[n],jp[n]
  assert row['source_hex']==j.text.hex()==priorrows[n]['source_hex']and row['current_hex']==e.text.hex()and victory_compiled(priorrows[n])==e.text and not e.text.startswith(b' ')
  assert all(row['source_reference'][k]==v for k,v in dict(block=j.block,offset=j.block_offset,copy_end=j.copy_end,bytes=len(j.text)).items())and all(row['current_reference'][k]==v for k,v in dict(block=e.block,offset=e.block_offset,copy_end=e.copy_end,bytes=len(e.text)).items())
  assert('/COMMON/MESFILE.DK4',f'COMMON_MESSAGE_{n}')not in keys
 previous=read('work/analysis/editorial_handoff_verification_v2585/verified_handoff.json');assert previous['ledger_sha256']==sha(Path('work/analysis/battle_victory_source_handoff_v2587/editorial_review_current_v1.json.before').read_bytes())
"""
 needle=' ROOT.mkdir(parents=True);save(';assert source.count(needle)==1;source=source.replace(needle,extra+needle)
 source=source.replace('all5_exact_clean_current_integrated_references_payloads_five_gates_and_two_prose_owners_verified=True,','next8_legacy_cell_and_IC_plural_victory_packet=str(packetpath),next8_packet_sha256=sha(packetpath.read_bytes()),next8_context_only_credit0=True,all5_exact_clean_current_integrated_references_payloads_five_gates_and_two_prose_owners_verified=True,')
 source=source.replace('retentions=5,ROM_and_exact_patch_unchanged=True','retentions=5,next8_context_credit=0,ROM_and_exact_patch_unchanged=True')
 exec(compile(source,__file__,'exec'),{'__name__':'__main__','__file__':__file__})
