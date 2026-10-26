"""Audit13 complete retentions and the next16 zero-credit timed-action packet."""
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.refit_contextual_spritsail_v1 import current_entries
from dk4tool.rom.nds import NdsImage
from dk4tool.script.common_message_table import common_message_entries
from scripts.duel_bark_layout_v1200 import compiled
from scripts.duel_special_dispatch_v1217 import helper,front
from scripts.verify_village_wrap_v608 import read,save
OLD=Path('scripts/verify_editorial_handoff_v2519.py')
ROOT=Path('work/analysis/editorial_handoff_verification_v2523')
if __name__=='__main__':
 assert not ROOT.exists()
 packetpath=Path('work/analysis/duel_reaction_context_source_v2520/all16_clean_current_context_catalog.json')
 contextpath=Path('work/analysis/duel_reaction_context_v2521/source_context_packet.json');preflightpath=Path('work/analysis/duel_reaction_context_v2521/next16_preflight.json')
 packet,context,preflight=map(read,(packetpath,contextpath,preflightpath))
 assert packet['selected_IDs']==list(range(1957,1973))and preflight['fresh_credit']==0 and preflight['all_editorial_current_native_historical_and_registered_reconciliation_pending']
 assert len(context['all416_unchanged_native_voice_selections'])==416 and len(context['two_original_voice_call_bindings'])==2
 assert sha(packetpath.read_bytes())==preflight['packet_sha256']and sha(contextpath.read_bytes())==preflight['source_context_sha256']
 manuscriptpath=Path(preflight['registered_manuscript']);configpath=Path(preflight['registered_config']);config=read(configpath)
 assert sha(manuscriptpath.read_bytes())==preflight['registered_manuscript_sha256']==config['dependencies'][str(manuscriptpath)]
 rows={r['message_id']:r for r in read(manuscriptpath)['records']}
 ledger=read('translations/editorial_review_current_v1.json');rom=NdsImage.open(ledger['current_integrated_candidate']['path']);clean=NdsImage.open('work/clean.nds')
 arm=rom.read_file('/__arm9__.bin');en=current_entries(rom.read_file('/COMMON/MESFILE.DK4'),arm);jp=common_message_entries(clean.read_file('/COMMON/MESFILE.DK4'),clean.read_file('/__arm9__.bin'))
 assert arm[0x535E8:0x53628]==helper()[0]and arm[0xDAF0:0xDB5C]==front(1480)[0]
 keys={(r['file_path'],r['id'])for r in ledger['contextual_story_natural_dialogue_pass_v1871']['record_keys']}
 for r in packet['records']:
  n=r['message_ID'];assert r['source_hex']==jp[n].text.hex()==rows[n]['source_hex']and r['current_hex']==en[n].text.hex()and compiled(rows[n])==en[n].text
  assert('/COMMON/MESFILE.DK4',f'COMMON_MESSAGE_{n}')not in keys
 wrapper=OLD.read_text()
 needle=" exec(compile(source,__file__,'exec'),{'__name__':'__main__','__file__':__file__})"
 assert wrapper.count(needle)==1
 addition=""" source=source.replace('editorial_handoff_verification_v2519','editorial_handoff_verification_v2523').replace('V2519-audit-of-V2518','V2523-audit-of-V2522')
 source=source.replace('work/analysis/escape_completion_v2518/completion_receipt.json','work/analysis/duel_reaction_source_handoff_v2522/handoff_receipt.json')
 source=source.replace(\"h['fresh_reconciliations']==13\",\"h['completed_this_goal_turn']==13 and h['next_packet_fresh_credit']==0\")
 source=source.replace('# Current editorial handoff - V2518','# Current editorial handoff - V2522')
"""
 wrapper=wrapper.replace(needle,addition+needle)
 exec(compile(wrapper,__file__,'exec'),{'__name__':'__main__','__file__':__file__})
 proofpath=ROOT/'verified_handoff.json'
 save(ROOT/'next16_source_packet_audit.json',dict(checkpoint='V2523-final-and-next-packet',verified_handoff=str(proofpath),verified_handoff_sha256=sha(proofpath.read_bytes()),
  next_packet=str(packetpath),next_packet_sha256=sha(packetpath.read_bytes()),source_context=str(contextpath),source_context_sha256=sha(contextpath.read_bytes()),
  preflight=str(preflightpath),preflight_sha256=sha(preflightpath.read_bytes()),all16_exact_clean_current_registered_paragraphs=True,
  all416_original_voice_choices_and2_source_side0_duration60_calls_bound=True,current_extended_front_and_helper_byte_exact=True,
  all16_outside_completed_fresh_ledger_and_no_added_credit=True,completed_this_goal_turn=13,fresh_integrated=1968,
  original_auditor=str(OLD),original_auditor_sha256=sha(OLD.read_bytes()),effective_auditor_wrapper_sha256=sha(wrapper.encode()),
  all_jobs_terminal=True,full_objective_preserved=True,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
 print('V2523:13 completed escape retentions and next16 zero-credit source packet verified;1968 integrated;goal active.')
