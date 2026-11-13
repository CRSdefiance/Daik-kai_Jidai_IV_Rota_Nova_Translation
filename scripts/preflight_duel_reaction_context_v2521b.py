"""Finish the saved source packet without rerunning its completed416 selections."""
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.duel_bark_layout_v1200 import compiled
from scripts.duel_special_dispatch_v1217 import helper,front
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/duel_reaction_context_v2521')
if __name__=='__main__':
 assert (ROOT/'source_context_packet.json').exists()and not(ROOT/'next16_preflight.json').exists()
 arm=NdsImage.open('out/all_routes_combined_v2284_candidate.nds').read_file('/__arm9__.bin')
 assert arm[0x535E8:0x53628]==helper()[0]and arm[0xDAF0:0xDB5C]==front(1480)[0]
 packetpath=Path('work/analysis/duel_reaction_context_source_v2520/all16_clean_current_context_catalog.json');packet=read(packetpath)
 manifest=read('out/all_routes_combined_v2284_candidate.manifest.json');stage=manifest['relocations']['/COMMON/MESFILE.DK4']['duel_bark_editorial']
 configpath=Path(stage['release_config']);config=read(configpath);docpath=Path(config['manuscript']);rows={r['message_id']:r for r in read(docpath)['records']}
 assert sha(configpath.read_bytes())==stage['release_config_sha256']and sha(docpath.read_bytes())==config['manuscript_sha256']
 assert sorted(rows)==packet['selected_IDs']==stage['proof']['reviewed_native_IDs']==list(range(1957,1973))
 for row in packet['records']:n=row['message_ID'];assert row['source_hex']==rows[n]['source_hex']and bytes.fromhex(row['current_hex'])==compiled(rows[n])
 contextpath=ROOT/'source_context_packet.json';context=read(contextpath)
 assert context['current_ARM9_sha256']==sha(arm)and len(context['all416_unchanged_native_voice_selections'])==416 and len(context['two_original_voice_call_bindings'])==2
 assert context['current_front_includes_both_source_tables_registered_helper_checked_separately']and context['snapshot_is_historical_V1189_not_current_gameplay']
 ledger=read('translations/editorial_review_current_v1.json');fresh=ledger['contextual_story_natural_dialogue_pass_v1871']
 assert fresh['fresh_pass_records_integrated']==1968 and not{('/COMMON/MESFILE.DK4',f'COMMON_MESSAGE_{n}')for n in rows}&{(r['file_path'],r['id'])for r in fresh['record_keys']}
 save(ROOT/'next16_preflight.json',dict(packet=str(packetpath),packet_sha256=sha(packetpath.read_bytes()),source_context=str(contextpath),source_context_sha256=sha(contextpath.read_bytes()),
  registered_config=str(configpath),registered_config_sha256=sha(configpath.read_bytes()),registered_manuscript=str(docpath),registered_manuscript_sha256=sha(docpath.read_bytes()),
  all16_clean_current_registered_compilations_match=True,all416_current_original_voice_choices_and2_timed_calls_pass=True,
  current_registered_five_table_and_numeric_special_front_and64byte_helper_exact=True,
  prior_producer='scripts/preflight_duel_reaction_context_v2521.py',prior_producer_sha256=sha(Path('scripts/preflight_duel_reaction_context_v2521.py').read_bytes()),
  prior_failure_after_successful_source_packet='KeyError b:original main local variable was not available in outer execution namespace',
  completed_source_selections_not_needlessly_repeated=True,fresh_credit=0,all_editorial_current_native_historical_and_registered_reconciliation_pending=True,
  producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
 print('Saved416 selections reused;16 registered templates,current extended front and source calls verified. Zero fresh credit.')
