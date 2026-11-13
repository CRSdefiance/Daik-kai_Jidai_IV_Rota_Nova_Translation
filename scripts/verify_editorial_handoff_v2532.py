"""Audit16 completed timed reactions and the zero-credit15-special source packet."""
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.refit_contextual_spritsail_v1 import current_entries
from dk4tool.rom.nds import NdsImage
from dk4tool.script.common_message_table import common_message_entries
from scripts.duel_special_layout_v1216 import compiled,IDS
from scripts.duel_special_dispatch_v1217 import helper,front
from scripts.verify_village_wrap_v608 import read,save
OLD=Path('scripts/verify_editorial_handoff_v2528.py')
ROOT=Path('work/analysis/editorial_handoff_verification_v2532')
if __name__=='__main__':
 assert not ROOT.exists()
 packetpath=Path('work/analysis/duel_special_context_source_v2529/all15_clean_current_context_catalog.json')
 contextpath=Path('work/analysis/duel_special_context_v2530/source_context_packet.json');preflightpath=Path('work/analysis/duel_special_context_v2530/next15_preflight.json')
 packet,context,preflight=map(read,(packetpath,contextpath,preflightpath))
 assert packet['selected_IDs']==list(IDS)and preflight['fresh_credit']==0 and preflight['all_editorial_current_native_historical_and_registered_reconciliation_pending']
 assert len(context['all208_original_native_special_method_selections'])==208 and len(context['all15_original_message_call_bindings'])==15
 assert all(r['side']==0 and r['duration']==120 for r in context['all15_original_message_call_bindings'])
 assert sha(packetpath.read_bytes())==preflight['packet_sha256']and sha(contextpath.read_bytes())==preflight['source_context_sha256']
 manuscriptpath=Path(preflight['registered_manuscript']);configpath=Path(preflight['registered_config']);config=read(configpath)
 expected=config.get('manuscript_sha256')or config['dependencies'][str(manuscriptpath)]
 assert sha(manuscriptpath.read_bytes())==preflight['registered_manuscript_sha256']==expected
 rows={r['message_id']:r for r in read(manuscriptpath)['records']}
 ledger=read('translations/editorial_review_current_v1.json');rom=NdsImage.open(ledger['current_integrated_candidate']['path']);clean=NdsImage.open('work/clean.nds')
 arm=rom.read_file('/__arm9__.bin');en=current_entries(rom.read_file('/COMMON/MESFILE.DK4'),arm);jp=common_message_entries(clean.read_file('/COMMON/MESFILE.DK4'),clean.read_file('/__arm9__.bin'))
 assert arm[0x535E8:0x53628]==helper()[0]and arm[0xDAF0:0xDB5C]==front(1480)[0]
 keys={(r['file_path'],r['id'])for r in ledger['contextual_story_natural_dialogue_pass_v1871']['record_keys']}
 for r in packet['records']:
  n=r['message_ID'];assert r['source_hex']==jp[n].text.hex()==rows[n]['source_hex']and r['current_hex']==en[n].text.hex()and compiled(rows[n])==en[n].text
  assert('/COMMON/MESFILE.DK4',f'COMMON_MESSAGE_{n}')not in keys
 source_bindings={r['actor_ID']:r['message_ID']for r in context['all15_original_message_call_bindings']}
 assert source_bindings[15]==1988 and source_bindings[20]==1987 and source_bindings[6]==2146
 wrapper=OLD.read_text();needle=" exec(compile(source,__file__,'exec'),{'__name__':'__main__','__file__':__file__})"
 assert wrapper.count(needle)==1
 addition=""" source=source.replace('editorial_handoff_verification_v2528','editorial_handoff_verification_v2532').replace('V2528-audit-of-V2527','V2532-audit-of-V2531')
 source=source.replace('work/analysis/duel_reaction_completion_v2527/completion_receipt.json','work/analysis/duel_special_source_handoff_v2531/handoff_receipt.json')
 source=source.replace(\"h['fresh_reconciliations']==16\",\"h['completed_this_goal_turn']==16 and h['next_packet_fresh_credit']==0\")
 source=source.replace('# Current editorial handoff - V2527','# Current editorial handoff - V2531')
"""
 wrapper=wrapper.replace(needle,addition+needle)
 exec(compile(wrapper,__file__,'exec'),{'__name__':'__main__','__file__':__file__})
 proofpath=ROOT/'verified_handoff.json'
 save(ROOT/'next15_special_source_packet_audit.json',dict(checkpoint='V2532-final-and-next-packet',verified_handoff=str(proofpath),verified_handoff_sha256=sha(proofpath.read_bytes()),
  next_packet=str(packetpath),next_packet_sha256=sha(packetpath.read_bytes()),source_context=str(contextpath),source_context_sha256=sha(contextpath.read_bytes()),
  preflight=str(preflightpath),preflight_sha256=sha(preflightpath.read_bytes()),all15_exact_clean_current_registered_paragraphs=True,
  all208_original_method_choices_and15_source_side0_duration120_calls_bound=True,correct_Angelo_Fernando_and_nonadjacent_Julio2146_bindings=True,
  current_extended_front_and_helper_byte_exact=True,all15_outside_completed_fresh_ledger_and_no_added_credit=True,
  completed_this_goal_turn=16,fresh_integrated=1984,original_auditor=str(OLD),original_auditor_sha256=sha(OLD.read_bytes()),effective_auditor_wrapper_sha256=sha(wrapper.encode()),
  all_jobs_terminal=True,full_objective_preserved=True,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
 print('V2532:16 completed timed reactions and next15 zero-credit special-call packet verified;1984 integrated;goal active.')
