"""Current208 method selections and15 original numeric call bindings;not prose approval."""
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.duel_special_layout_v1216 import compiled,IDS
from scripts.duel_special_dispatch_v1217 import helper,front
from scripts.verify_village_wrap_v608 import read,save
OLD=Path('scripts/research_duel_special_context_v1215.py')
ROOT=Path('work/analysis/duel_special_context_v2530')
if __name__=='__main__':
 source=OLD.read_text()
 changes={'dk4tool.patch.duel_bark_editorial':'dk4tool.patch.refit_contextual_spritsail_v1',
  'work/analysis/duel_special_context_v1215':'work/analysis/duel_special_context_v2530',
  "ROM=Path('out/all_routes_combined_v1206_candidate.nds')":"ROM=Path('out/all_routes_combined_v2284_candidate.nds')",
  "assert sha(ROM.read_bytes())=='3ab79feca6d89fbb3cb4495b378f0a8d70cdeb15ecaf3085713940fc799dcd57'":"assert sha(ROM.read_bytes())=='7c6d025ef0d12c6dd7cc58095802a27bb49dafc830f33851e73e734b4f8bdfe1'",
  '(15,0xF2D4,1987)':'(15,0xF2D4,1988)','(20,0xF2D4,1988)':'(20,0xF2D4,1987)',
  'raw=RAW.read_bytes();widget,nested,header,h=actual_widget(raw)':"raw=RAW.read_bytes();report=read(RAW.parent/'capture_report.json');assert report['ROM_sha256']==sha(Path('out/all_routes_combined_v1206_candidate.nds').read_bytes());assert sha(raw)==next(r['sha256']for r in report['read_only_capture_RAM_snapshots']+report['read_only_pause_RAM_snapshots']if r['frame']==6113);widget,nested,header,h=actual_widget(raw)",
  "'no_new_prose_or_completion_credit':True":"'snapshot_historical_V1206_not_current_gameplay':True,'historical_model_labels_do_not_replace_current_approved_names':True,'no_new_prose_or_completion_credit':True",
 }
 for a,b in changes.items():assert a in source,a;source=source.replace(a,b)
 exec(compile(source,__file__,'exec'),{'__name__':'__main__','__file__':__file__})
 rom=NdsImage.open('out/all_routes_combined_v2284_candidate.nds');arm=rom.read_file('/__arm9__.bin')
 assert arm[0x535E8:0x53628]==helper()[0]and arm[0xDAF0:0xDB5C]==front(1480)[0]
 packetpath=Path('work/analysis/duel_special_context_source_v2529/all15_clean_current_context_catalog.json');packet=read(packetpath)
 contextpath=ROOT/'source_context_packet.json';context=read(contextpath)
 assert context['current_ARM9_sha256']==sha(arm)and len(context['all208_original_native_special_method_selections'])==208 and len(context['all15_original_message_call_bindings'])==15
 assert all(r['side']==0 and r['duration']==120 for r in context['all15_original_message_call_bindings'])
 assert {r['actor_ID']:r['message_ID']for r in context['all15_original_message_call_bindings']}[15]==1988
 assert {r['actor_ID']:r['message_ID']for r in context['all15_original_message_call_bindings']}[20]==1987
 manifest=read('out/all_routes_combined_v2284_candidate.manifest.json');stage=manifest['relocations']['/COMMON/MESFILE.DK4']['duel_special_editorial']
 configpath=Path(stage['release_config']);config=read(configpath);docpath=Path(config['manuscript']);prior={r['message_id']:r for r in read(docpath)['records']}
 assert sha(configpath.read_bytes())==stage['release_config_sha256']
 expected=config.get('manuscript_sha256')or config['dependencies'][str(docpath)]
 assert sha(docpath.read_bytes())==expected
 registered_ids=stage['proof'].get('native_IDs',stage['proof'].get('reviewed_native_IDs'))
 assert sorted(prior)==packet['selected_IDs']==registered_ids==list(IDS)
 for r in packet['records']:n=r['message_ID'];assert r['source_hex']==prior[n]['source_hex']and bytes.fromhex(r['current_hex'])==compiled(prior[n])
 ledger=read('translations/editorial_review_current_v1.json');fresh=ledger['contextual_story_natural_dialogue_pass_v1871']
 assert fresh['fresh_pass_records_integrated']==1984 and not{('/COMMON/MESFILE.DK4',f'COMMON_MESSAGE_{n}')for n in IDS}&{(r['file_path'],r['id'])for r in fresh['record_keys']}
 save(ROOT/'next15_preflight.json',dict(packet=str(packetpath),packet_sha256=sha(packetpath.read_bytes()),source_context=str(contextpath),source_context_sha256=sha(contextpath.read_bytes()),
  registered_config=str(configpath),registered_config_sha256=sha(configpath.read_bytes()),registered_manuscript=str(docpath),registered_manuscript_sha256=sha(docpath.read_bytes()),
  all15_clean_current_registered_compilations_match=True,all208_original_method_choices_and15_side0_duration120_calls_bound=True,
  current_extended_front_and_helper_bytes_exact=True,original_Angelo1988_and_Fernando1987_pairing_retained=True,
  no_current_emulator_or_actual_animation_activation=True,fresh_credit=0,all_editorial_current_native_historical_and_registered_reconciliation_pending=True,
  original=str(OLD),original_sha256=sha(OLD.read_bytes()),effective_source_sha256=sha(source.encode()),producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
 print('Next15 exact paragraphs;208 current original method choices and15 side0/duration120 calls pass. Zero editorial credit.')
