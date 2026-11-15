"""Final scoped audit of this turn's61 retentions and zero-credit next packet."""
from pathlib import Path
from collections import Counter
from dk4tool.dialogue.review import validate_natural_dialogue_batch
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.refit_contextual_spritsail_v1 import current_entries
from dk4tool.rom.nds import NdsImage
from dk4tool.script.common_message_table import common_message_entries
from scripts.verify_village_wrap_v608 import read,save
from scripts.work_comments_layout_v843 import compiled as cook_compiled
from scripts.livestock_prayer_layout_v854 import compiled as livestock_compiled
from scripts.planning_finance_layout_v860 import compiled as planning_compiled
ROOT=Path('work/analysis/editorial_handoff_verification_v2342')
if __name__=='__main__':
 assert not ROOT.exists();ledgerpath=Path('translations/editorial_review_current_v1.json');l=read(ledgerpath);f=l['contextual_story_natural_dialogue_pass_v1871'];keys={(r['file_path'],r['id'])for r in f['record_keys']}
 assert len(keys)==len(f['record_keys'])==len(f['record_IDs'])==1495 and(f['fresh_pass_records_explicitly_reread'],f['fresh_pass_records_integrated'],f['fresh_pass_records_pending_native_actual_release'])==(1495,1495,0)
 assert Counter(p for p,n in keys)=={'/COMMON/MESFILE.DK4':839,'/data/SC2.DK4':428,'/data/SC0.DK4':117,'/data/SC1.DK4':73,'/data/SC3.DK4':38}
 assert l['records_editorially_completed']==2143 and l['records_revised_and_integrated']==1498 and l['retained_wordings_editorially_completed']==645 and sum(l['source_prose_reviewed_counts_by_file'].values())==2259 and len(l['reviewed_but_incomplete_COMMON_IDs'])==116 and l['goal_status']=='active'and not l['full_goal_complete']
 release=read('work/analysis/refit_spritsail_release_v2285b/registered_release_verification.json');rompath=Path(l['current_integrated_candidate']['path']);digest=sha(rompath.read_bytes());assert digest==release['candidate_sha256']==l['current_integrated_candidate']['sha256']and sha(Path(release['patch']).read_bytes())==release['patch_sha256']and release['whole_ROM_reconstruction_byte_exact']
 rom,clean=NdsImage.open(rompath),NdsImage.open('work/clean.nds');entries=current_entries(rom.read_file('/COMMON/MESFILE.DK4'),rom.read_file('/__arm9__.bin'));jp=common_message_entries(clean.read_file('/COMMON/MESFILE.DK4'),clean.read_file('/__arm9__.bin'));seen=set();metadata=[];batches=[]
 for family,compiler,ids in[('cooking',cook_compiled,range(1410,1423)),('livestock_prayer',livestock_compiled,range(1423,1447)),('planning_finance',planning_compiled,range(1447,1471))]:
  path=Path('translations')/(family+'_contextual_final_review_v1.json');final=read(path);notespath=Path('translations')/(family+'_contextual_editorial_manuscript_v2.json');notes=read(notespath);validate_natural_dialogue_batch(notes)
  assert final['candidate_sha256']==digest and final['revised_count']==0 and final['retained_count']==len(ids)and final['no_ROM_profile_registry_manifest_or_patch_change']and final['whole_clean_input_reconstruction_exact']and not final['full_goal_complete'];assert final['records']==notes['records']and final['native_message_IDs']==list(ids)
  for p,h in final['evidence'].items():assert sha(Path(p).read_bytes())==h,p
  for row in notes['records']:
   n=row['message_id'];k=(row['file_path'],row['id']);assert k in keys and n not in seen and row['source_hex']==jp[n].text.hex()and row['current_hex']==row['integrated_hex']==entries[n].text.hex()and compiler(row)==entries[n].text and all(row['review'].values())and row['fresh_retained_wording_justification'];seen.add(n)
   assert row['integrated_reference']==dict(block=entries[n].block,offset=entries[n].block_offset,copy_end=entries[n].copy_end,bytes=len(entries[n].text))
   if row['speaker_metadata_corrected']:assert row['speaker']=='Hodram (native captain1)'and row['prior_speaker_metadata']=='Joakim (native captain1)';metadata.append(n)
  batches.append(dict(final_review=str(path),sha256=sha(path.read_bytes()),records=len(ids),all_five_individual_review_gates=True,exact_clean_current_integrated_references=True))
 assert seen==set(range(1410,1471))and metadata==[1419,1432,1444,1456,1468]
 handoff=Path('work/analysis/bridge_duties_handoff_v2341/handoff_receipt.json');h=read(handoff)
 for p,d in h['updated_files'].items():assert sha(Path(p).read_bytes())==d,p
 for p,d in h['evidence'].items():assert sha(Path(p).read_bytes())==d,p
 assert h['fresh_integrated']==1495 and h['completed_this_turn']==61 and h['new_credit_for_packet']==0 and h['all_jobs_terminal']
 inv=read('work/analysis/planning_finance_completion_v2339/remaining_historical_fresh_review_inventory.json');assert inv['remaining']==648 and Counter(r['file_path']for r in inv['records'])=={'/COMMON/MESFILE.DK4':647,'/data/SC2.DK4':1}
 ROOT.mkdir(parents=True);save(ROOT/'verified_handoff.json',dict(checkpoint='V2342-audit-of-V2341',ledger=str(ledgerpath),ledger_sha256=sha(ledgerpath.read_bytes()),fresh_records=1495,completed_this_turn=61,retained=61,new_prose_revisions=0,speaker_metadata_corrections=metadata,batches=batches,all61_exact_clean_current_integrated_payloads_and_per_record_five_gates=True,all_final_review_evidence_hashes_current=True,handoff_receipt=str(handoff),handoff_receipt_sha256=sha(handoff.read_bytes()),all_handoff_updated_file_hashes_current=True,next28_packet_credit=0,remaining_historical_fresh_reviews=648,historical_complete_unchanged=2143,source_prose_unchanged=2259,incomplete_COMMON_unchanged=116,candidate=str(rompath),candidate_sha256=digest,patch=release['patch'],patch_sha256=release['patch_sha256'],prior_clean_input_reconstruction_proof_still_bound=True,no_ROM_registry_profile_manifest_or_patch_change=True,all_jobs_terminal=True,full_objective_and_separate_graphics_and_later_technical_reaudit_preserved=True,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False));print(dict(all61_reviews_and_evidence_pass=True,fresh_integrated=1495,next28_credit=0,ROM_and_exact_patch_unchanged=True,goal='active'))
