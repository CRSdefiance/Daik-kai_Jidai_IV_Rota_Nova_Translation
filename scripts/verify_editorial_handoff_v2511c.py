"""Standalone final audit;no nested execution namespace or generated source quoting."""
from pathlib import Path
from collections import Counter
from dk4tool.dialogue.review import validate_natural_dialogue_batch
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.refit_contextual_spritsail_v1 import current_entries
from dk4tool.rom.nds import NdsImage
from dk4tool.script.common_message_table import common_message_entries
from scripts.duel_editorial_layout_v1155 import compiled,ESCAPE_IDS
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/editorial_handoff_verification_v2511c')
if __name__=='__main__':
 assert not ROOT.exists()
 ledgerpath=Path('translations/editorial_review_current_v1.json');l=read(ledgerpath);f=l['contextual_story_natural_dialogue_pass_v1871'];keys={(r['file_path'],r['id'])for r in f['record_keys']}
 assert len(keys)==len(f['record_keys'])==len(f['record_IDs'])==1955
 assert(f['fresh_pass_records_explicitly_reread'],f['fresh_pass_records_integrated'],f['fresh_pass_records_pending_native_actual_release'])==(1955,1955,0)
 assert Counter(p for p,n in keys)=={'/COMMON/MESFILE.DK4':1299,'/data/SC2.DK4':428,'/data/SC0.DK4':117,'/data/SC1.DK4':73,'/data/SC3.DK4':38}
 assert l['records_editorially_completed']==2143 and l['records_revised_and_integrated']==1498 and l['retained_wordings_editorially_completed']==645 and sum(l['source_prose_reviewed_counts_by_file'].values())==2259 and len(l['reviewed_but_incomplete_COMMON_IDs'])==116 and l['goal_status']=='active'and not l['full_goal_complete']
 release=read('work/analysis/refit_spritsail_release_v2285b/registered_release_verification.json');rompath=Path(l['current_integrated_candidate']['path']);digest=sha(rompath.read_bytes());manifestpath=rompath.with_suffix('.manifest.json');manifest=read(manifestpath);registry=read('translations/release_stack.json')
 assert digest==release['candidate_sha256']==l['current_integrated_candidate']['sha256']and sha(Path(release['patch']).read_bytes())==release['patch_sha256']and release['whole_ROM_reconstruction_byte_exact']
 assert sha(manifestpath.read_bytes())==release['manifest_sha256']and manifest['release_stack_sha256']==sha(Path('translations/release_stack.json').read_bytes())and all(manifest['checks'].values())and len(manifest['batches'])==493 and len(registry['accepted_layers'])==114 and registry['latest_promoted_build']['profile']=='all-routes-unified-v1492'
 assert sha(Path('work/clean.nds').read_bytes())==release['clean_input_sha256']and sha(Path(manifest['base_rom']).read_bytes())==manifest['base_sha256']
 rom,clean=NdsImage.open(rompath),NdsImage.open('work/clean.nds');arm=rom.read_file('/__arm9__.bin');entries=current_entries(rom.read_file('/COMMON/MESFILE.DK4'),arm);jp=common_message_entries(clean.read_file('/COMMON/MESFILE.DK4'),clean.read_file('/__arm9__.bin'))
 notespath=Path('translations/static_duel_contextual_editorial_manuscript_v2.json');finalpath=Path('translations/static_duel_contextual_final_review_v1.json');notes,final=map(read,(notespath,finalpath));validate_natural_dialogue_batch(notes)
 assert final['records']==notes['records']and final['native_message_IDs']==list(range(1931,1951))and final['candidate_sha256']==digest and final['revised_count']==0 and final['retained_count']==20 and final['no_ROM_profile_registry_manifest_or_patch_change']and final['whole_clean_input_reconstruction_exact']
 for p,h in final['evidence'].items():assert sha(Path(p).read_bytes())==h,p
 for r in notes['records']:
  n=r['message_id'];assert(r['file_path'],r['id'])in keys and r['source_hex']==jp[n].text.hex()and r['current_hex']==r['integrated_hex']==entries[n].text.hex()and compiled(r)==entries[n].text and all(r['review'].values())and r['fresh_retained_wording_justification']and not r['speaker_metadata_corrected']
  assert r['integrated_reference']==dict(block=entries[n].block,offset=entries[n].block_offset,copy_end=entries[n].copy_end,bytes=len(entries[n].text))
 assert Counter(r['consumer']for r in notes['records'])=={'original-duel-side0-actor-text':8,'original-duel-side1-actor-text':12}
 assert final['current_native_static_duel_font_executions']==36 and final['current_native_copies']==40 and final['current_parent_draw_controls']==0 and final['historical_actual_holds']==6 and final['historical_original_duel_terminal_transitions_current_bound']==1
 history=read('work/analysis/static_duel_history_v2505c/historical_static_duel_current_binding.json');assert history['actual_historical_challenge_name']=='Centurione'and'original_actor_IDs_1_32_and_conditional_Clifford_name_unchanged'not in history
 handoffpath=Path('work/analysis/escape_source_handoff_v2510/handoff_receipt.json');h=read(handoffpath)
 for group in('updated_files','evidence'):
  for p,d in h[group].items():assert sha(Path(p).read_bytes())==d,p
 assert h['completed_this_goal_turn']==20 and h['fresh_integrated']==1955 and h['next_packet_records']==13 and h['next_packet_fresh_or_source_prose_credit']==0 and h['all_jobs_terminal']
 packetpath=Path('work/analysis/escape_source_handoff_v2510/next13_direct_escape_source_packet.json');p=read(packetpath);assert p['selected_native_IDs']==list(ESCAPE_IDS)and p['source_context_only_fresh_credit']==0 and p['all13_prose_current_native_fonts_historical_defeat_path_and_registered_reconciliation_pending'];assert p['correct_original_direct_return_parent']==0x02053F40 and p['correct_original_direct_table_stack_offset']==0x274 and p['incorrect_older_speech53DB8_plus27C_frame_must_not_be_used']
 assert len(p['all416_current_original_voice_selections'])==416 and len(p['all208_original_actor_ID_predicates'])==len(p['all208_original_virtual20_compact_name_getters'])==208 and p['zero_predicate_actor_IDs']==[0,1,2,3]
 assert sha(Path(p['registered_manuscript']).read_bytes())==p['registered_manuscript_sha256']and sha(Path(p['effective_formatter_config']).read_bytes())==p['effective_formatter_config_sha256'];prior={r['message_id']:r for r in read(p['registered_manuscript'])['records']};catalog=read(p['source_catalog'])
 for r in catalog['records']:
  n=r['message_ID'];assert r['source_hex']==jp[n].text.hex()==prior[n]['source_hex']and r['current_hex']==entries[n].text.hex()and compiled(prior[n])==entries[n].text;assert('/COMMON/MESFILE.DK4',f'COMMON_MESSAGE_{n}')not in keys
 assert sha(Path(p['corrected_direct_font_proof']).read_bytes())==p['corrected_direct_font_proof_sha256']and len(read(p['corrected_direct_font_proof'])['cases'])==1417;assert sha(Path(p['corrected_direct_pipeline']).read_bytes())==p['corrected_direct_pipeline_sha256']and len(read(p['corrected_direct_pipeline'])['all13_direct_pipeline_cases'])==13
 inv=read('work/analysis/static_duel_completion_v2506/remaining_historical_fresh_review_inventory.json');assert inv['remaining']==188 and Counter(r['file_path']for r in inv['records'])=={'/COMMON/MESFILE.DK4':187,'/data/SC2.DK4':1};assert Path('docs/editorial_handoff_current.md').read_text().startswith('# Current editorial handoff - V2510')
 ROOT.mkdir(parents=True)
 save(ROOT/'verified_handoff.json',dict(checkpoint='V2511c-audit-of-V2510',ledger=str(ledgerpath),ledger_sha256=sha(ledgerpath.read_bytes()),fresh_records=1955,completed_this_goal_turn=20,retained=20,new_prose_revisions=0,speaker_metadata_corrections=[],final_review=str(finalpath),final_review_sha256=sha(finalpath.read_bytes()),all20_exact_clean_current_integrated_payloads_and_five_gates=True,all_final_review_evidence_hashes_current=True,handoff_receipt=str(handoffpath),handoff_receipt_sha256=sha(handoffpath.read_bytes()),all_handoff_updated_file_and_evidence_hashes_current=True,next_corrected_direct_escape_packet=str(packetpath),next_packet_sha256=sha(packetpath.read_bytes()),next13_source_context_only_credit0_all_editorial_native_historical_reconciliation_pending=True,remaining_historical_fresh_reviews=188,historical_complete_unchanged=2143,source_prose_unchanged=2259,incomplete_COMMON_unchanged=116,candidate=str(rompath),candidate_sha256=digest,patch=release['patch'],patch_sha256=release['patch_sha256'],prior_clean_input_reconstruction_proof_still_bound=True,no_ROM_registry_profile_manifest_or_patch_change=True,all_jobs_terminal=True,full_objective_and_separate_graphics_and_later_technical_reaudit_preserved=True,preserved_failed_audits={str(t):sha(t.read_bytes())for t in map(Path,('scripts/verify_editorial_handoff_v2511.py','scripts/verify_editorial_handoff_v2511b.py'))},producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
 print(dict(all20_reviews_and_next13_source_packet_pass=True,fresh_integrated=1955,next13_credit=0,ROM_and_exact_patch_unchanged=True,goal='active'))
