"""Standalone audit of the five-report,two-owner capture checkpoint."""
from pathlib import Path
from collections import Counter
from importlib import import_module
from dk4tool.dialogue.review import validate_natural_dialogue_batch
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.refit_contextual_spritsail_v1 import current_entries
from dk4tool.rom.nds import NdsImage
from dk4tool.script.common_message_table import common_message_entries
from scripts.review_flagship_capture_context_v2581 import compiled
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/editorial_handoff_verification_v2585');IDS=list(range(2011,2016))
if __name__=='__main__':
 assert not ROOT.exists()
 ledgerpath=Path('translations/editorial_review_current_v1.json');ledger=read(ledgerpath);fresh=ledger['contextual_story_natural_dialogue_pass_v1871'];keys={(r['file_path'],r['id'])for r in fresh['record_keys']}
 assert len(keys)==len(fresh['record_keys'])==len(fresh['record_IDs'])==2046 and(fresh['fresh_pass_records_explicitly_reread'],fresh['fresh_pass_records_integrated'],fresh['fresh_pass_records_pending_native_actual_release'])==(2046,2046,0)
 assert Counter(p for p,n in keys)=={'/COMMON/MESFILE.DK4':1390,'/data/SC2.DK4':428,'/data/SC0.DK4':117,'/data/SC1.DK4':73,'/data/SC3.DK4':38}
 assert ledger['records_editorially_completed']==2143 and ledger['records_revised_and_integrated']==1498 and ledger['retained_wordings_editorially_completed']==645 and sum(ledger['source_prose_reviewed_counts_by_file'].values())==2259 and len(ledger['reviewed_but_incomplete_COMMON_IDs'])==116 and ledger['goal_status']=='active'and not ledger['full_goal_complete']
 release=read('work/analysis/refit_spritsail_release_v2285b/registered_release_verification.json');rompath=Path(ledger['current_integrated_candidate']['path']);digest=sha(rompath.read_bytes());manifestpath=rompath.with_suffix('.manifest.json');manifest=read(manifestpath);registrypath=Path('translations/release_stack.json');registry=read(registrypath)
 assert digest==release['candidate_sha256']==ledger['current_integrated_candidate']['sha256']and sha(Path(release['patch']).read_bytes())==release['patch_sha256']and release['whole_ROM_reconstruction_byte_exact']
 assert sha(manifestpath.read_bytes())==release['manifest_sha256']and manifest['release_stack_sha256']==sha(registrypath.read_bytes())and all(manifest['checks'].values())and len(manifest['batches'])==493 and len(registry['accepted_layers'])==114 and registry['latest_promoted_build']['profile']=='all-routes-unified-v1492'
 assert sha(Path('work/clean.nds').read_bytes())==release['clean_input_sha256']and sha(Path(manifest['base_rom']).read_bytes())==manifest['base_sha256']
 rom,clean=map(NdsImage.open,(rompath,'work/clean.nds'));arm=rom.read_file('/__arm9__.bin');common=rom.read_file('/COMMON/MESFILE.DK4');entries=current_entries(common,arm);jp=common_message_entries(clean.read_file('/COMMON/MESFILE.DK4'),clean.read_file('/__arm9__.bin'))
 notespath=Path('translations/flagship_capture_contextual_editorial_manuscript_v2.json');finalpath=Path('translations/flagship_capture_contextual_final_review_v1.json');notes,final=map(read,(notespath,finalpath));validate_natural_dialogue_batch(notes)
 assert final['records']==notes['records']and final['native_message_IDs']==IDS and final['candidate_sha256']==digest and final['revised_count']==0 and final['retained_count']==5 and final['speaker_metadata_corrections']==notes['speaker_metadata_corrections']==[]and final['whole_clean_input_reconstruction_exact']and final['no_ROM_profile_registry_manifest_or_patch_change']
 for path,value in final['evidence'].items():assert sha(Path(path).read_bytes())==value,path
 owners=notes['registered_prose_owner_bindings'];assert len(owners)==2 and final['registered_stage_binding']['registered_prose_owner_bindings']==owners
 prior={};owner_by_ID={}
 for owner in owners:
  stage=manifest['relocations']['/COMMON/MESFILE.DK4'][owner['stage']];cfgpath=Path(stage['release_config']);cfg=read(cfgpath);mp=Path(cfg['manuscript']);module,attribute=owner['compiler'].rsplit('.',1);own=getattr(import_module(module),attribute)
  assert sha(cfgpath.read_bytes())==stage['release_config_sha256']==owner['registered_config_sha256']and sha(mp.read_bytes())==cfg['dependencies'][str(mp)]==owner['registered_manuscript_sha256']and stage['proof']['native_IDs']==owner['registered_stage_native_IDs']and set(owner['selected_IDs'])<=set(stage['proof']['native_IDs'])
  for row in read(mp)['records']:
   n=row['message_id']
   if n in owner['selected_IDs']:assert n not in prior;prior[n]=row;owner_by_ID[n]=owner['stage'];assert own(row)==compiled(row)==entries[n].text
 assert sorted(prior)==IDS and owner_by_ID=={2011:'battle_aftermath_editorial',2012:'battle_aftermath_editorial',2013:'battle_aftermath_editorial',2014:'battle_aftermath_editorial',2015:'flagship_capture_precision'}
 for r in notes['records']:
  n=r['message_id'];e,j=entries[n],jp[n]
  assert(r['file_path'],r['id'])in keys and r['source_hex']==j.text.hex()and r['current_hex']==r['integrated_hex']==e.text.hex()and compiled(r)==e.text and all(r['review'].values())and r['fresh_retained_wording_justification']and not r['speaker_metadata_corrected']and r['registered_prose_owner']==owner_by_ID[n]
  expected=dict(block=e.block,offset=e.block_offset,copy_end=e.copy_end,bytes=len(e.text));assert r['integrated_reference']==expected and all(r['current_reference'][k]==v for k,v in expected.items())
  assert all(r['source_reference'][k]==v for k,v in dict(block=j.block,offset=j.block_offset,copy_end=j.copy_end,bytes=len(j.text)).items())and r['consumer']=='original-53D44-logical-role1-flagship-capture-portrait'
 assert notes['records'][-1]['english']=="We've captured the enemy flagship after defeating its entire crew!"and notes['original_role_selector']==1 and notes['original_parent']==0x02053DB8 and notes['original_table_stack_offset']==0x27C and notes['original_source_table']==0x02117740
 font=read('work/analysis/flagship_capture_fonts_v2582/native_font_proof.json');cases=font['all8_voice_pipeline_full_font_cases'];assert len(cases)==font['complete_native_font_cases']==8 and font['unique_native_reports']==5
 assert[c['source_voice']for c in cases]==list(range(8))and[c['message_ID']for c in cases]==[2011,2011,2012,2011,2011,2013,2014,2015]and[c['message_ID']for c in font['all5_complete_native_cases']]==IDS and len(font['all10_native_cold_warm_copies'])==10 and not font['findings']
 assert len(font['all_seven_CPU_original_single_roster_byte_fixtures'])==7 and all(len(c['only_original_roster_byte_changed'])==1 and c['all_actor_objects_IDs_RNG_and_other4MiB_bytes_exact']for c in font['all_seven_CPU_original_single_roster_byte_fixtures'])
 assert cases[1]['role_fixture']is None and cases[1]['native_pipeline']['source_actor_ID']==16 and cases[1]['native_pipeline']['actual_voice1_logical16_physical0_unchanged']
 assert all(c['native_pipeline']['original_entry']==0x02053D44 and c['native_pipeline']['parent']==0x02053DB8 and c['native_pipeline']['selector_offset']==0x27C and c['native_pipeline']['selector']==0x02117740 and c['native_pipeline']['logical82478_selection_verified']for c in cases)
 assert final['current_native_flagship_capture_font_executions']==8 and final['current_native_copies']==10 and final['historical_actual_holds']==2 and final['historical_capture_rewards_cargo_and_sailing_transitions_current_bound']==9
 history=read('work/analysis/flagship_capture_history_v2583b/historical_flagship_capture_current_binding.json');assert history['historical_IDs']==[2011]and len(history['historical_holds'])==2 and history['only2011_has_individual_historical_activation_other4_use_family_sample']and history['no_new_current_battle_emulator_runs_or_family_visits']and history['no_fixtures_after4800']and history['all_accepted_input_events_reconstructed_at_pause_frame_plus1']
 assert all(c['source_actor_ID']==16 and c['matching_foreground_pixels']==743 for c in history['historical_holds'])and len(history['seven_negative_controls_current_binding_on_offline_clones'])==7 and all(c['rejected']for c in history['seven_negative_controls_current_binding_on_offline_clones'])
 states=history['natural_combat_outcome_and_original_dismissal_states'];assert len(states)==15 and states[-1]['frame']==13200 and states[-1]['mode8_12_16']==[0,0,0]
 flow=history['scoped_historical_cancellation_and_battle_transitions_freshly_rechecked'];assert[f['frame']for f in flow]==[10850,10950,11100,11300,11500,12400,12700,12900,13200]and 'national-coins' in flow[4]['visually_reviewed_state']and 'discard' in flow[6]['visually_reviewed_state']
 receiptpath=Path('work/analysis/flagship_capture_completion_v2584/completion_receipt.json');receipt=read(receiptpath)
 for group in('updated_files','evidence'):
  for path,value in receipt[group].items():assert sha(Path(path).read_bytes())==value,path
 assert receipt['fresh_reconciliations']==5 and receipt['fresh_integrated']==2046 and receipt['all_jobs_terminal']and read('work/analysis/flagship_capture_completion_v2584/visual_review.json')['font_previews']==8
 inv=read('work/analysis/flagship_capture_completion_v2584/remaining_historical_fresh_review_inventory.json');assert inv['remaining']==97 and Counter(r['file_path']for r in inv['records'])=={'/COMMON/MESFILE.DK4':96,'/data/SC2.DK4':1}and Path('docs/editorial_handoff_current.md').read_text().startswith('# Current editorial handoff - V2584')
 ROOT.mkdir(parents=True);save(ROOT/'verified_handoff.json',dict(checkpoint='V2585-audit-of-V2584',ledger=str(ledgerpath),ledger_sha256=sha(ledgerpath.read_bytes()),fresh_records=2046,completed_this_goal_turn=5,retained=5,new_prose_revisions=0,speaker_metadata_corrections=[],final_review=str(finalpath),final_review_sha256=sha(finalpath.read_bytes()),all5_exact_clean_current_integrated_references_payloads_five_gates_and_two_prose_owners_verified=True,all8_current_voice_fonts_and_three_fallbacks_verified=True,all_final_review_evidence_hashes_current=True,historical_two_holds_seven_corruptions_fifteen_states_nine_transitions_and_corrected_reward_labels_verified=True,handoff_receipt=str(receiptpath),handoff_receipt_sha256=sha(receiptpath.read_bytes()),all_handoff_updated_file_and_evidence_hashes_current=True,remaining_historical_fresh_reviews=97,historical_complete_unchanged=2143,source_prose_unchanged=2259,incomplete_COMMON_unchanged=116,candidate=str(rompath),candidate_sha256=digest,patch=release['patch'],patch_sha256=release['patch_sha256'],prior_clean_input_reconstruction_proof_still_bound=True,no_ROM_registry_profile_manifest_or_patch_change=True,all_jobs_terminal=True,full_objective_and_separate_graphics_and_later_technical_reaudit_preserved=True,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
 print(dict(all5_two_owner_capture_reviews_and8_voices_and_historical_flow_pass=True,fresh_integrated=2046,retentions=5,ROM_and_exact_patch_unchanged=True,goal='active'))
