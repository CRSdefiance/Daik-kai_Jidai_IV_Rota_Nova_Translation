"""Fresh current-code timed-action calls,voice selection and registered16-row preflight."""
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save
from scripts.duel_bark_layout_v1200 import compiled
from scripts.duel_special_dispatch_v1217 import helper,front
OLD=Path('scripts/research_duel_bark_context_v1199.py')
ROOT=Path('work/analysis/duel_reaction_context_v2521')
if __name__=='__main__':
 source=OLD.read_text()
 changes={'dk4tool.patch.escape_direct_entries':'dk4tool.patch.refit_contextual_spritsail_v1',
  'work/analysis/duel_bark_context_v1199':'work/analysis/duel_reaction_context_v2521',
  "ROM=Path('out/all_routes_combined_v1189_candidate.nds')":"ROM=Path('out/all_routes_combined_v2284_candidate.nds')",
  "assert sha(ROM.read_bytes())=='a7b7799052a83703dc5a2bf84e946e43b31d5e1f795f9f3371417412f60c7df4'":"assert sha(ROM.read_bytes())=='7c6d025ef0d12c6dd7cc58095802a27bb49dafc830f33851e73e734b4f8bdfe1'",
  "raw=snapshot.read_bytes();cpu,get=get_machine(b,raw)":"raw=snapshot.read_bytes();report=read(snapshot.parent/'capture_report.json');assert report['ROM_sha256']==sha(Path('out/all_routes_combined_v1189_candidate.nds').read_bytes());assert sha(raw)==next(r['sha256']for r in report['read_only_capture_RAM_snapshots']+report['read_only_pause_RAM_snapshots']if r['frame']==6202);cpu,get=get_machine(b,raw)",
  "'native_front_currently_excludes_both_new_tables':True":"'current_front_includes_both_source_tables_registered_helper_checked_separately':True,'snapshot_is_historical_V1189_not_current_gameplay':True",
  'fourteen_additional_special_move_lines1980_1993_remain_separate_unreviewed_work':'special_moves1980_1993_and2146_remain_separate_fresh_review_work',
 }
 for a,b in changes.items():assert a in source,a;source=source.replace(a,b)
 env={'__name__':'__main__','__file__':__file__};exec(compile(source,__file__,'exec'),env)
 arm=env['b'];assert arm[0x535E8:0x53628]==helper()[0]and arm[0xDAF0:0xDB5C]==front(1480)[0]
 packetpath=Path('work/analysis/duel_reaction_context_source_v2520/all16_clean_current_context_catalog.json');packet=read(packetpath)
 manifest=read('out/all_routes_combined_v2284_candidate.manifest.json');stage=manifest['relocations']['/COMMON/MESFILE.DK4']['duel_bark_editorial'];configpath=Path(stage['release_config']);config=read(configpath);docpath=Path(config['manuscript']);rows={r['message_id']:r for r in read(docpath)['records']}
 assert sha(configpath.read_bytes())==stage['release_config_sha256']and sha(docpath.read_bytes())==config['manuscript_sha256']
 assert sorted(rows)==packet['selected_IDs']==stage['proof']['reviewed_native_IDs']==list(range(1957,1973))
 for row in packet['records']:n=row['message_ID'];assert row['source_hex']==rows[n]['source_hex']and bytes.fromhex(row['current_hex'])==compiled(rows[n])
 contextpath=ROOT/'source_context_packet.json';context=read(contextpath);assert len(context['all416_unchanged_native_voice_selections'])==416 and len(context['two_original_voice_call_bindings'])==2
 ledger=read('translations/editorial_review_current_v1.json');fresh=ledger['contextual_story_natural_dialogue_pass_v1871'];assert fresh['fresh_pass_records_integrated']==1968 and not{('/COMMON/MESFILE.DK4',f'COMMON_MESSAGE_{n}')for n in rows}&{(r['file_path'],r['id'])for r in fresh['record_keys']}
 save(ROOT/'next16_preflight.json',dict(packet=str(packetpath),packet_sha256=sha(packetpath.read_bytes()),source_context=str(contextpath),source_context_sha256=sha(contextpath.read_bytes()),
  registered_config=str(configpath),registered_config_sha256=sha(configpath.read_bytes()),registered_manuscript=str(docpath),registered_manuscript_sha256=sha(docpath.read_bytes()),
  all16_clean_current_registered_compilations_match=True,all416_current_original_voice_choices_and2_timed_calls_pass=True,
  current_registered_five_table_and_numeric_special_front_and64byte_helper_exact=True,
  original=str(OLD),original_sha256=sha(OLD.read_bytes()),effective_source_sha256=sha(source.encode()),
  fresh_credit=0,all_editorial_current_native_historical_and_registered_reconciliation_pending=True,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
 print('Next16 exact templates;416 current voice selections and2 original side0/duration60 calls pass;registered current extended front exact. Zero fresh credit.')
