"""Standalone final audit of six reviewed alerts,eight voices,and deferred cleanup."""
from pathlib import Path
from collections import Counter
from dk4tool.dialogue.review import validate_natural_dialogue_batch
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.refit_contextual_spritsail_v1 import current_entries
from dk4tool.rom.nds import NdsImage
from dk4tool.script.common_message_table import common_message_entries
from scripts.powder_fire_native_plan_v1309 import compiled
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/editorial_handoff_verification_v2577');IDS=list(range(2052,2058))
if __name__=='__main__':
 assert not ROOT.exists()
 ledgerpath=Path('translations/editorial_review_current_v1.json');ledger=read(ledgerpath);fresh=ledger['contextual_story_natural_dialogue_pass_v1871'];keys={(r['file_path'],r['id']) for r in fresh['record_keys']}
 assert len(keys)==len(fresh['record_keys'])==len(fresh['record_IDs'])==2041 and(fresh['fresh_pass_records_explicitly_reread'],fresh['fresh_pass_records_integrated'],fresh['fresh_pass_records_pending_native_actual_release'])==(2041,2041,0)
 assert Counter(p for p,n in keys)=={'/COMMON/MESFILE.DK4':1385,'/data/SC2.DK4':428,'/data/SC0.DK4':117,'/data/SC1.DK4':73,'/data/SC3.DK4':38}
 assert ledger['records_editorially_completed']==2143 and ledger['records_revised_and_integrated']==1498 and ledger['retained_wordings_editorially_completed']==645 and sum(ledger['source_prose_reviewed_counts_by_file'].values())==2259 and len(ledger['reviewed_but_incomplete_COMMON_IDs'])==116 and ledger['goal_status']=='active' and not ledger['full_goal_complete']
 release=read('work/analysis/refit_spritsail_release_v2285b/registered_release_verification.json');rompath=Path(ledger['current_integrated_candidate']['path']);digest=sha(rompath.read_bytes());manifestpath=rompath.with_suffix('.manifest.json');manifest=read(manifestpath);registrypath=Path('translations/release_stack.json');registry=read(registrypath)
 assert digest==release['candidate_sha256']==ledger['current_integrated_candidate']['sha256'] and sha(Path(release['patch']).read_bytes())==release['patch_sha256'] and release['whole_ROM_reconstruction_byte_exact']
 assert sha(manifestpath.read_bytes())==release['manifest_sha256'] and manifest['release_stack_sha256']==sha(registrypath.read_bytes()) and all(manifest['checks'].values()) and len(manifest['batches'])==493 and len(registry['accepted_layers'])==114 and registry['latest_promoted_build']['profile']=='all-routes-unified-v1492'
 assert sha(Path('work/clean.nds').read_bytes())==release['clean_input_sha256'] and sha(Path(manifest['base_rom']).read_bytes())==manifest['base_sha256']
 rom,clean=map(NdsImage.open,(rompath,'work/clean.nds'));arm=rom.read_file('/__arm9__.bin');common=rom.read_file('/COMMON/MESFILE.DK4');entries=current_entries(common,arm);jp=common_message_entries(clean.read_file('/COMMON/MESFILE.DK4'),clean.read_file('/__arm9__.bin'))
 notespath=Path('translations/powder_fire_contextual_editorial_manuscript_v2.json');finalpath=Path('translations/powder_fire_contextual_final_review_v1.json');notes,final=map(read,(notespath,finalpath));validate_natural_dialogue_batch(notes)
 assert final['records']==notes['records'] and final['native_message_IDs']==IDS and final['candidate_sha256']==digest and final['revised_count']==0 and final['retained_count']==6 and final['speaker_metadata_corrections']==notes['speaker_metadata_corrections']==[] and final['whole_clean_input_reconstruction_exact'] and final['no_ROM_profile_registry_manifest_or_patch_change']
 for path,value in final['evidence'].items():assert sha(Path(path).read_bytes())==value,path
 for r in notes['records']:
  n=r['message_id'];e=entries[n];j=jp[n]
  assert(r['file_path'],r['id']) in keys and r['source_hex']==j.text.hex() and r['current_hex']==r['integrated_hex']==e.text.hex() and compiled(r)==e.text and all(r['review'].values()) and r['fresh_retained_wording_justification'] and not r['speaker_metadata_corrected']
  expected=dict(block=e.block,offset=e.block_offset,copy_end=e.copy_end,bytes=len(e.text));assert r['integrated_reference']==expected and all(r['current_reference'][k]==v for k,v in expected.items())
  assert all(r['source_reference'][k]==v for k,v in dict(block=j.block,offset=j.block_offset,copy_end=j.copy_end,bytes=len(j.text)).items()) and r['consumer']=='original-53F0C-per-battery-gunner-powder-fire-portrait'
 assert notes['original_entry']==0x02053F0C and notes['original_parent']==0x02053F40 and notes['original_table_stack_offset']==0x274 and notes['original_source_table']==0x02117980 and notes['source_speaker_is_original_per_battery_gunner']
 font=read('work/analysis/powder_fire_fonts_v2574/native_font_proof.json');cases=font['all8_voice_pipeline_full_font_cases'];assert len(cases)==font['complete_native_font_cases']==8 and font['unique_native_alerts']==6
 assert [r['source_voice'] for r in cases]==list(range(8)) and [r['message_ID'] for r in cases]==[2052,2053,2052,2052,2054,2055,2056,2057] and [r['message_ID'] for r in font['all6_complete_native_cases']]==IDS
 assert font['no_actor_or_roster_fixture'] and font['all_original_actor_model_bytes_unchanged'] and font['CPU_actor_or_roster_fixtures']==[] and len(font['all12_native_cold_warm_copies'])==12 and not font['findings']
 assert all(r['native_pipeline']['original_entry']==0x02053F0C and r['native_pipeline']['parent']==0x02053F40 and r['native_pipeline']['selector_offset']==0x274 for r in cases) and cases[1]['native_pipeline']['source_actor_ID']==16
 assert final['current_native_powder_fire_font_executions']==8 and final['current_native_copies']==12 and final['historical_actual_holds']==2 and final['historical_fire_followup_cleanup_and_battle_return_transitions_current_bound']==4
 history=read('work/analysis/powder_fire_history_v2575/historical_powder_fire_current_binding.json');assert history['historical_IDs']==[2053] and len(history['historical_holds'])==2 and history['only2053_has_individual_alert_activation_other5_use_family_sample'] and history['no_new_current_battle_emulator_runs_or_family_visits']
 followups=history['context_only_extinguished_followup_holds'];assert len(followups)==2 and all(r['message_ID'] is None and r['matching_cached_template_ID_candidates']==[585,586] and r['followup_individual_ID_not_claimed'] for r in followups) and history['followup585_586_individual_ID_ambiguous_no_extra_credit']
 assert len(history['nine_negative_controls_current_binding_on_offline_clones'])==9 and all(r['rejected'] for r in history['nine_negative_controls_current_binding_on_offline_clones'])
 states=history['eight_original_fire_followup_and_return_states'];assert len(states)==8 and all(r['original_mobile_flag0E']&1 for r in states if r['frame'] in(7350,7390)) and all(not r['original_mobile_flag0E']&1 for r in states if r['frame'] in(7490,7590))
 assert history['original_fire_cleanup_deferred_until_followup_dismissal_in_both_versions'] and [r['flag0E'] for r in history['source1266_cleanup_states_freshly_rechecked']]==[5,5,4]
 for r in history['source_ignition_gun_position_and_deferred_cleanup_code_current_clean_historical_equal']:assert sha(arm[r['start']:r['end']])==r['sha256']
 stage=manifest['relocations']['/COMMON/MESFILE.DK4']['powder_fire_editorial'];cfgpath=Path(stage['release_config']);cfg=read(cfgpath);assert stage['proof']['native_IDs']==IDS and sha(cfgpath.read_bytes())==stage['release_config_sha256'] and sha(Path(cfg['manuscript']).read_bytes())==cfg['dependencies'][cfg['manuscript']]
 receiptpath=Path('work/analysis/powder_fire_completion_v2576/completion_receipt.json');receipt=read(receiptpath)
 for group in('updated_files','evidence'):
  for path,value in receipt[group].items():assert sha(Path(path).read_bytes())==value,path
 assert receipt['fresh_reconciliations']==6 and receipt['fresh_integrated']==2041 and receipt['all_jobs_terminal'] and read('work/analysis/powder_fire_completion_v2576/visual_review.json')['font_previews']==8
 inv=read('work/analysis/powder_fire_completion_v2576/remaining_historical_fresh_review_inventory.json');assert inv['remaining']==102 and Counter(r['file_path'] for r in inv['records'])=={'/COMMON/MESFILE.DK4':101,'/data/SC2.DK4':1} and Path('docs/editorial_handoff_current.md').read_text().startswith('# Current editorial handoff - V2576')
 ROOT.mkdir(parents=True);save(ROOT/'verified_handoff.json',dict(checkpoint='V2577-audit-of-V2576',ledger=str(ledgerpath),ledger_sha256=sha(ledgerpath.read_bytes()),fresh_records=2041,completed_this_goal_turn=6,retained=6,new_prose_revisions=0,speaker_metadata_corrections=[],final_review=str(finalpath),final_review_sha256=sha(finalpath.read_bytes()),all6_exact_clean_current_integrated_references_payloads_and_five_gates=True,all8_current_voice_fonts_and_both_fallbacks_verified=True,all_final_review_evidence_hashes_current=True,context_only_followup_ID_ambiguity_and_deferred_cleanup_verified=True,handoff_receipt=str(receiptpath),handoff_receipt_sha256=sha(receiptpath.read_bytes()),all_handoff_updated_file_and_evidence_hashes_current=True,remaining_historical_fresh_reviews=102,historical_complete_unchanged=2143,source_prose_unchanged=2259,incomplete_COMMON_unchanged=116,candidate=str(rompath),candidate_sha256=digest,patch=release['patch'],patch_sha256=release['patch_sha256'],prior_clean_input_reconstruction_proof_still_bound=True,no_ROM_registry_profile_manifest_or_patch_change=True,all_jobs_terminal=True,full_objective_and_separate_graphics_and_later_technical_reaudit_preserved=True,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
 print(dict(all6_powder_fire_reviews_and8_voices_and_deferred_cleanup_pass=True,fresh_integrated=2041,retentions=6,ROM_and_exact_patch_unchanged=True,goal='active'))
