"""Final scoped audit of special15; unchanged registered V2284 artifacts."""
from pathlib import Path
from collections import Counter
from dk4tool.dialogue.review import validate_natural_dialogue_batch
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.refit_contextual_spritsail_v1 import current_entries
from dk4tool.rom.nds import NdsImage
from dk4tool.script.common_message_table import common_message_entries
from scripts.duel_special_layout_v1216 import compiled,IDS
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/editorial_handoff_verification_v2537')
if __name__=='__main__':
 assert not ROOT.exists()
 ledgerpath=Path('translations/editorial_review_current_v1.json');l=read(ledgerpath);f=l['contextual_story_natural_dialogue_pass_v1871'];keys={(r['file_path'],r['id'])for r in f['record_keys']}
 assert len(keys)==len(f['record_keys'])==len(f['record_IDs'])==1999
 assert(f['fresh_pass_records_explicitly_reread'],f['fresh_pass_records_integrated'],f['fresh_pass_records_pending_native_actual_release'])==(1999,1999,0)
 assert Counter(p for p,n in keys)=={'/COMMON/MESFILE.DK4':1343,'/data/SC2.DK4':428,'/data/SC0.DK4':117,'/data/SC1.DK4':73,'/data/SC3.DK4':38}
 assert l['records_editorially_completed']==2143 and l['records_revised_and_integrated']==1498 and l['retained_wordings_editorially_completed']==645 and sum(l['source_prose_reviewed_counts_by_file'].values())==2259 and len(l['reviewed_but_incomplete_COMMON_IDs'])==116 and l['goal_status']=='active'and not l['full_goal_complete']
 release=read('work/analysis/refit_spritsail_release_v2285b/registered_release_verification.json');rompath=Path(l['current_integrated_candidate']['path']);digest=sha(rompath.read_bytes());manifestpath=rompath.with_suffix('.manifest.json');manifest=read(manifestpath);registry=read('translations/release_stack.json')
 assert digest==release['candidate_sha256']==l['current_integrated_candidate']['sha256']and sha(Path(release['patch']).read_bytes())==release['patch_sha256']and release['whole_ROM_reconstruction_byte_exact']
 assert sha(manifestpath.read_bytes())==release['manifest_sha256']and manifest['release_stack_sha256']==sha(Path('translations/release_stack.json').read_bytes())and all(manifest['checks'].values())and len(manifest['batches'])==493 and len(registry['accepted_layers'])==114 and registry['latest_promoted_build']['profile']=='all-routes-unified-v1492'
 assert sha(Path('work/clean.nds').read_bytes())==release['clean_input_sha256']and sha(Path(manifest['base_rom']).read_bytes())==manifest['base_sha256']
 rom,clean=NdsImage.open(rompath),NdsImage.open('work/clean.nds');arm=rom.read_file('/__arm9__.bin');common=rom.read_file('/COMMON/MESFILE.DK4');entries=current_entries(common,arm);jp=common_message_entries(clean.read_file('/COMMON/MESFILE.DK4'),clean.read_file('/__arm9__.bin'))
 notespath=Path('translations/duel_special_contextual_editorial_manuscript_v2.json');finalpath=Path('translations/duel_special_contextual_final_review_v1.json');notes,final=map(read,(notespath,finalpath));validate_natural_dialogue_batch(notes)
 assert final['records']==notes['records']and final['native_message_IDs']==list(IDS)and final['candidate_sha256']==digest and final['revised_count']==0 and final['retained_count']==15 and final['no_ROM_profile_registry_manifest_or_patch_change']and final['whole_clean_input_reconstruction_exact']
 for p,h in final['evidence'].items():assert sha(Path(p).read_bytes())==h,p
 for r in notes['records']:
  n=r['message_id'];e=entries[n];j=jp[n]
  assert(r['file_path'],r['id'])in keys and r['source_hex']==j.text.hex()and r['current_hex']==r['integrated_hex']==e.text.hex()and compiled(r)==e.text and all(r['review'].values())and r['fresh_retained_wording_justification']and r['source_meaning']
  assert r['speaker_metadata_corrected']==(n==1987)
  assert r['integrated_reference']==dict(block=e.block,offset=e.block_offset,copy_end=e.copy_end,bytes=len(e.text))
  assert all(r['current_reference'][k]==v for k,v in r['integrated_reference'].items())
  assert all(r['source_reference'][k]==v for k,v in dict(block=j.block,offset=j.block_offset,copy_end=j.copy_end,bytes=len(j.text)).items())
 assert Counter(r['consumer']for r in notes['records'])=={'original-D4D0-static-duel-side0-duration120':15}
 corrections=notes['speaker_metadata_corrections'];assert len(corrections)==1 and final['speaker_metadata_corrections']==corrections
 assert {k:corrections[0][k]for k in('message_id','source_actor_ID','before','after')}==dict(message_id=1987,source_actor_ID=20,before='Ｆernando',after='Fernando')
 fernando=next(r for r in notes['records']if r['message_id']==1987);assert fernando['speaker']=='Fernando'and fernando['prior_speaker_metadata']=='Ｆernando'and fernando['source_actor_ID']==20
 assert final['current_native_special_call_font_executions']==15 and final['current_native_copies']==30 and final['current_parent_draw_controls']==0 and final['historical_actual_holds']==6 and final['historical_special_combat_and_victory_transitions_current_bound']==4
 font=read('work/analysis/duel_special_fonts_v2534/native_font_proof.json');assert font['complete_native_font_cases']==15 and len(font['focused_excluded_prior_numeric_and_escape_controls'])==6 and font['all15_original_D4D0_side0_duration120_source_contract_preserved']
 history=read('work/analysis/duel_special_history_v2535/historical_duel_special_current_binding.json');assert history['historical_IDs']==[1990]and history['only1990_has_individual_actual_special_activation_other14_family_sample']and history['no_new_current_battle_emulator_runs_or_family_visits']
 assert notes['original_special_side']==0 and notes['original_special_duration']==120 and all(r['source_speaker_side']==0 and r['duration']==120 for r in history['historical_holds'])
 assert len(history['six_negative_controls_current_binding_on_offline_clones'])==6 and all(r['rejected']for r in history['six_negative_controls_current_binding_on_offline_clones'])
 context=read(notes['native_context_proof']);assert len(context['all208_original_native_special_method_selections'])==208 and len(context['all15_original_message_call_bindings'])==15
 stage=manifest['relocations']['/COMMON/MESFILE.DK4']['duel_special_editorial'];configpath=Path(stage['release_config']);config=read(configpath)
 assert stage['proof']['native_IDs']==list(IDS)and len(stage['proof']['changed_records'])==15 and sha(configpath.read_bytes())==stage['release_config_sha256']
 assert sha(Path(config['manuscript']).read_bytes())==config['dependencies'][config['manuscript']]
 handoffpath=Path('work/analysis/duel_special_completion_v2536/completion_receipt.json');h=read(handoffpath)
 for group in('updated_files','evidence'):
  for p,d in h[group].items():assert sha(Path(p).read_bytes())==d,p
 assert h['fresh_reconciliations']==15 and h['fresh_integrated']==1999 and h['speaker_metadata_corrections']==1 and h['all_jobs_terminal']
 inv=read('work/analysis/duel_special_completion_v2536/remaining_historical_fresh_review_inventory.json');assert inv['remaining']==144 and Counter(r['file_path']for r in inv['records'])=={'/COMMON/MESFILE.DK4':143,'/data/SC2.DK4':1}
 assert Path('docs/editorial_handoff_current.md').read_text().startswith('# Current editorial handoff - V2536')
 ROOT.mkdir(parents=True)
 save(ROOT/'verified_handoff.json',dict(checkpoint='V2537-audit-of-V2536',ledger=str(ledgerpath),ledger_sha256=sha(ledgerpath.read_bytes()),fresh_records=1999,completed_this_goal_turn=15,retained=15,new_prose_revisions=0,speaker_metadata_corrections=corrections,
  final_review=str(finalpath),final_review_sha256=sha(finalpath.read_bytes()),all15_exact_clean_current_integrated_references_payloads_and_five_gates=True,all_final_review_evidence_hashes_current=True,
  handoff_receipt=str(handoffpath),handoff_receipt_sha256=sha(handoffpath.read_bytes()),all_handoff_updated_file_and_evidence_hashes_current=True,
  remaining_historical_fresh_reviews=144,historical_complete_unchanged=2143,source_prose_unchanged=2259,incomplete_COMMON_unchanged=116,
  candidate=str(rompath),candidate_sha256=digest,patch=release['patch'],patch_sha256=release['patch_sha256'],prior_clean_input_reconstruction_proof_still_bound=True,no_ROM_registry_profile_manifest_or_patch_change=True,
  all_jobs_terminal=True,full_objective_and_separate_graphics_and_later_technical_reaudit_preserved=True,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
 print(dict(all15_special_reviews_and_evidence_pass=True,fresh_integrated=1999,retentions=15,Fernando_metadata_normalizations=1,ROM_and_exact_patch_unchanged=True,goal='active'))
