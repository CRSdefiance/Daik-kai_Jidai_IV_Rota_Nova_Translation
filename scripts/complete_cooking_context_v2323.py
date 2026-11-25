"""Reconcile thirteen fresh Cook retentions against registered cumulative V2284."""
from pathlib import Path
from collections import Counter
from copy import deepcopy
from shutil import copy2
from dk4tool.dialogue.review import validate_natural_dialogue_batch
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.refit_contextual_spritsail_v1 import current_entries
from dk4tool.rom.nds import NdsImage
from dk4tool.script.common_message_table import common_message_entries
from scripts.work_comments_layout_v843 import compiled
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/cooking_completion_v2323')
LEDGER=Path('translations/editorial_review_current_v1.json')
DOC=Path('translations/cooking_contextual_editorial_manuscript_v1.json')
NOTES=Path('translations/cooking_contextual_editorial_manuscript_v2.json')
FINAL=Path('translations/cooking_contextual_final_review_v1.json')
FONTS=Path('work/analysis/cooking_fonts_v2318/all13_current_native_fonts.json')
ACTUAL=Path('work/analysis/cooking_current_verification_v2321/ordinary_current_Cook_actual.json')
HISTORY=Path('work/analysis/cooking_history_v2322/historical8_current_binding.json')
RELEASE=Path('work/analysis/refit_spritsail_release_v2285b/registered_release_verification.json')
GUIDE=Path('E:/Rota Nova translations/Guide screenshots/V2284 Cook13 contextual retentions verified')
IDS=list(range(1410,1423));FAMILY='Shared-Cook13-contextual-retentions'
SUMMARY=(
 'V2323 reconciles thirteen historical COMMON Cook comments 1410-1422 as fresh, individually justified retentions. Every clean Japanese entry was reread with its native role, voice class, protagonist and actor context. These are independent flavor comments, rather than a sequential conversation. The English preserves nutrition, preparation, confidence, humming, the salt/sugar mistake, the masculine cooking joke, the missing-food question, seasoning, Rafael\'s mild criticism, Hodram\'s apprenticeship recollection, Lil\'s complaint, Maria\'s fried-rice plan and Sera\'s simple pleasure in good food. No recipe, ingredient, rank, relationship, culprit or mechanical reward is invented. Each entry has a new source gloss and retention reason. Speaker metadata for 1419 is corrected from Joakim to the native actor1 given name Hodram. Joakim remains approved within Hodram Joakim Bergstrom; the historical JoakimCook case label and all older manuscripts remain preserved. English and native names are unchanged. '
 'Clean-exact source code and 25 current native helper selections establish the eight NPC voice classes, four protagonists and Sera actor24\'s separate 1422 override. The four protagonist states are previously captured states, without fresh captain-ID substitution or new current four-hero visits. All thirteen full current native selectors, macro expanders, clears, fonts, glyphs, bounds, canaries and ABI checks pass under declared CPU role/assignment and initialized-widget controls. Actor health, mood and captain records are not replaced. Twenty-six cold/warm COMMON copies pass with explicit host file-I/O contracts. All complete authored words, first/final letters and independent pixels fit the native 252x96 canvas and the unchanged 216x36 body crop from native (0,60) to screen (16,112). One current initialized-parent projection binds the shared crop; thirteen GPU visits or parent reinitializations are not claimed. The work-v843 compiler supplies generated pair-safe 36-column, three-row wrapping. The odd nineteen-character first rows of 1416 and 1419 retain their full continuations. All thirteen font previews were viewed on two sheets. '
 'One new ordinary V2284 Copenhagen cold boot runs 5401 frames using the inherited five-ship test battery. Gerhard moves through the original UI from Survey slot7 to Galley slot21, native role15; two complete 1411 holds match the full bitmap and actual RGB foreground/blank-ink plane. Only the two assignment bytes change during preview, and cancel restores all31. Funds, calendar, owned actor records, flagship and full ship models stay equal across four checkpoints. There is no new RAM, code, text, health, role, location, timing or RNG fixture or savestate. The inherited battery is not earned recruitment, statistics, fleet acquisition or campaign progress. Eight selection/return frames were viewed on one sheet. The earlier wrong-touch V2319 run selected equipment slot29 and has zero Cook coverage credit; both runs and the source-bound button geometry proof are preserved. '
 'Eight historical V850 holds across 1411, 1416, 1419 and 1422 are freshly rebound to current complete payloads, independent bitmaps and actual RGB ink, covering Gerhard, Emilio, Hodram and Sera. One clearly labeled historical sheet was viewed. Their disclosed two/three-byte room/occupant fixtures remain historical; Emilio and Sera remain foreign faction21, with no earned recruitment claim. The four historical normal-return controls remain historical. Other twelve entries have no new current individual visit claim. '
 'No English, ROM, runtime, geometry, registry, profile, manifest or patch change is required. All thirteen reconcile through the existing cooking_comments_editorial stage; its ten historical revisions are not new revisions. Registered cumulative experimental V2284 remains 493 batches and114 accepted layers with its exact clean-input patch. V1492 stays promoted, canonical/clean inputs are unchanged, and every ROM and earlier translation is preserved. '
 'Fresh coverage is 1447 reread /1447 integrated-reconciled /zero pending. Historical completion remains2143 (1498 revised,645 retained), source/prose review2259 and incomplete COMMON116. Another696 historical completions require fresh review:695 COMMON plus SC2B294R73. All never-reviewed storylines, shared town/shop dialogue, random scenes and remaining player-facing prose remain in scope. Separate graphics/all18 plaques, SC3B109 classification and the later older-record technical re-audit remain open. The full objective is active. All jobs are terminal.'
)

def historical_key(row):
 path=row.get('file_path','/COMMON/MESFILE.DK4');n=row.get('message_id')
 return path,f'COMMON_MESSAGE_{n}'if n is not None and path=='/COMMON/MESFILE.DK4'else row['id']

if __name__=='__main__':
 assert not any(p.exists()for p in(ROOT,NOTES,FINAL,GUIDE))
 l,d,fonts,actual,history,release=[read(p)for p in(LEDGER,DOC,FONTS,ACTUAL,HISTORY,RELEASE)]
 f=l['contextual_story_natural_dialogue_pass_v1871']
 assert(f['fresh_pass_records_explicitly_reread'],f['fresh_pass_records_integrated'],f['fresh_pass_records_pending_native_actual_release'])==(1434,1434,0)
 assert len(d['records'])==d['retained_count']==13 and d['revised_IDs']==[] and d['speaker_metadata_corrections']==[1419]
 contextpath=Path(d['native_context_proof']);metadata=Path(d['captain1_metadata_correction'])
 assert sha(contextpath.read_bytes())==d['native_context_proof_sha256']and sha(metadata.read_bytes())==d['captain1_metadata_correction_sha256']
 context=read(contextpath)
 assert len(context['all25_current_native_role_helper_selections'])==25 and context['actor_records_and_captain_IDs_not_replaced']
 assert len(fonts['all13_complete_native_cases'])==13 and len(fonts['all26_native_cold_warm_copies'])==26 and len(fonts['review_sheets'])==2
 assert fonts['current_parent_projection_controls']==1 and fonts['all_original_numeric_selections_macro_expanders_clears_fonts_glyphs_guards_and_ABI_pass']and fonts['Sera_actor24_original1422_override_executed']
 assert len(actual['actual_complete_holds'])==2 and actual['current_message_IDs']==[1411]and actual['all31_assignment_bytes_restored_after_cancel']and actual['all_other_scoped_fields_unchanged_across4_checkpoints']
 assert actual['ordinary_input_selection_moves_Gerhard_from_slot7_to21_only']and actual['no_RAM_code_text_health_location_timing_role_or_RNG_fixture_or_savestate']
 assert len(history['historical_holds'])==8 and history['historical_IDs']==[1411,1416,1419,1422]
 for scope in history['historical_reports_and_fixture_scopes']:
  fix=scope['historical_room_occupant_fixture'];assert fix['role_type']==15 and len(fix['changes'])in(2,3)
  if fix['actor_ID']in(14,24):assert fix['original_actor_faction']==21 and fix['foreign_actor_not_claimed_as_normally_recruited']
 rompath=Path(l['current_integrated_candidate']['path']);digest=sha(rompath.read_bytes());mp=rompath.with_suffix('.manifest.json');manifest=read(mp)
 registry_path=Path('translations/release_stack.json');registry=read(registry_path)
 assert digest==d['current_ROM_sha256']==fonts['candidate_sha256']==actual['candidate_sha256']==history['candidate_sha256']==release['candidate_sha256']==manifest['candidate_sha256']
 assert sha(mp.read_bytes())==release['manifest_sha256']and manifest['release_stack_sha256']==sha(registry_path.read_bytes())and all(manifest['checks'].values())
 assert len(manifest['batches'])==493 and len(registry['accepted_layers'])==114 and registry['latest_promoted_build']['profile']=='all-routes-unified-v1492'
 assert release['whole_ROM_reconstruction_byte_exact']and sha(Path(release['patch']).read_bytes())==release['patch_sha256']and sha(Path('work/clean.nds').read_bytes())==release['clean_input_sha256']and sha(Path(manifest['base_rom']).read_bytes())==manifest['base_sha256']
 stage=manifest['relocations']['/COMMON/MESFILE.DK4']['cooking_comments_editorial'];configpath=Path(stage['release_config']);config=read(configpath);oldman=Path(config['manuscript'])
 assert sha(configpath.read_bytes())==stage['release_config_sha256']and sha(oldman.read_bytes())==config['manuscript_sha256']and stage['proof']['reviewed_native_IDs']==IDS
 changed=stage['proof']['changed_records'];assert len(changed)==10
 binding=dict(stage='cooking_comments_editorial',release_config=str(configpath),release_config_sha256=sha(configpath.read_bytes()),registered_manuscript=str(oldman),registered_manuscript_sha256=sha(oldman.read_bytes()),reviewed_native_IDs=IDS,historical_changed_records=changed,new_revisions=0)
 rom,clean=NdsImage.open(rompath),NdsImage.open('work/clean.nds');arm,common=rom.read_file('/__arm9__.bin'),rom.read_file('/COMMON/MESFILE.DK4');entries=current_entries(common,arm)
 jp=common_message_entries(clean.read_file('/COMMON/MESFILE.DK4'),clean.read_file('/__arm9__.bin'))
 assert sha(arm)==d['current_ARM9_sha256']==fonts['ARM9_sha256']==release['ARM9_sha256']and sha(common)==d['current_COMMON_sha256']==fonts['COMMON_sha256']==release['COMMON_sha256']
 oldhistory={historical_key(r):g['id']for g in l['completed_editorial_families']for r in g['records']};keys={(r['file_path'],r['id'])for r in f['record_keys']};selected={('/COMMON/MESFILE.DK4',f'COMMON_MESSAGE_{n}')for n in IDS}
 assert len(oldhistory)==2143 and not keys&selected and selected<=set(oldhistory)
 notes=deepcopy(d);notes.update(status='complete-fresh-contextual-retentions-reconciled-registered-V2284',formatting_review_pending=False,current_native_and_actual_family_reconciliation_pending=False,final_review=str(FINAL),registered_stage_binding=binding,current_native_fonts=str(FONTS),current_actual=str(ACTUAL),historical_current_binding=str(HISTORY))
 for r in notes['records']:
  n=r['message_id'];assert r['source_hex']==jp[n].text.hex()and r['current_hex']==entries[n].text.hex()and entries[n].text==compiled(r)
  r['review']['formatting']=True
  r.update(status='complete-fresh-source-native-display-actual-family-and-registered-retention-reconciliation',original_historical_family=oldhistory[(r['file_path'],r['id'])],integrated_hex=entries[n].text.hex(),integrated_reference=dict(block=entries[n].block,offset=entries[n].block_offset,copy_end=entries[n].copy_end,bytes=len(entries[n].text)),current_V2284_actual_holds=actual['actual_complete_holds']if n==1411 else[],new_current_visit=n==1411,historical_V850_current_bound_holds=[h for h in history['historical_holds']if h['message_ID']==n],all13_native_proof=str(FONTS),consumer='252x96 canvas,body y60;216x36 parent crop at screen16,112;work-v843 generated36-column3row pair-safe paragraph')
 validate_natural_dialogue_batch(notes)
 docs=[Path('docs')/p for p in('editorial_handoff_current.md','translation_progress.md','editorial_review_goal.md','todo.md','known_issues.md')]
 assert docs[0].read_text().startswith('# Current editorial handoff - V2315')
 ROOT.mkdir(parents=True)
 for p in[LEDGER,*docs]:(ROOT/(p.name+'.before')).write_bytes(p.read_bytes())
 save(NOTES,notes);visual=ROOT/'visual_review.json'
 save(visual,dict(all13_full_native_previews_on2_sheets_viewed=True,current8_selection_and_return_frames_on1_sheet_viewed=True,historical8_holds_on1_labeled_sheet_viewed=True,all4_review_sheets_viewed=True,odd19_character1416_and1419_complete_continuations=True,Gerhard_two_current_holds_original_selector_bitmap_RGB_and_normal_return_verified=True,historical_case_JoakimCook_correctly_shows_Hodram_Joakim_Bergstrom=True,no_new_current_four_hero_Emilio_or_Sera_visits_claim=True,full_goal_complete=False))
 paths=[DOC,NOTES,FONTS,ACTUAL,HISTORY,RELEASE,visual,contextpath,metadata,mp,registry_path,configpath,oldman,Path(d['source_context_packet']),Path('work/analysis/cooking_editorial_v2317/fresh_source_review.json'),Path('work/analysis/cooking_history_v2322/historical_label_metadata.json'),Path('work/analysis/cooking_button_geometry_v2320/source_bound_Galley_touch.json'),Path('work/analysis/cooking_current_verification_v2321/producer_binding.json'),Path(__file__)]
 evidence={str(p):sha(p.read_bytes())for p in paths}
 save(FINAL,dict(format='dk4-editorial-family-final-review-v1',family=FAMILY,file_path='/COMMON/MESFILE.DK4',native_message_IDs=IDS,revised_count=0,retained_count=13,speaker_metadata_corrections=[1419],historical_reconciliation_only=True,new_completed_records=0,records=notes['records'],summary=SUMMARY,evidence=evidence,registered_stage_binding=binding,candidate=str(rompath),candidate_sha256=digest,profile=manifest['profile'],patch=release['patch'],patch_sha256=release['patch_sha256'],whole_clean_input_reconstruction_exact=True,no_ROM_profile_registry_manifest_or_patch_change=True,current_native_fonts=13,current_parent_draw_controls=1,current_native_copies=26,current_actual_IDs=[1411],current_actual_holds=2,historical_actual_IDs=history['historical_IDs'],historical_actual_holds=8,all4_review_sheets_viewed=True,full_goal_complete=False))
 f['record_keys'].extend(dict(file_path=r['file_path'],id=r['id'])for r in notes['records']);f['record_IDs'].extend(r['id']for r in notes['records'])
 f.update(fresh_pass_records_explicitly_reread=1447,fresh_pass_records_integrated=1447,fresh_pass_records_pending_native_actual_release=0,historical_completed_records_outside_reconciled_fresh_pass=696,latest_contextual_manuscript=str(NOTES),latest_completed_family=FAMILY,latest_reconciled_historical_family=FAMILY,latest_contextual_retention_review=str(FINAL),latest_final_review=str(FINAL),latest_pending_contextual_family=None,coverage_note='1447 file-qualified fresh rereads integrated/reconciled;696 other historical completions,116 incomplete COMMON and all never-reviewed storylines/shared town/shop/random/player prose remain in scope.')
 f['reconciled_families'].append(dict(id=FAMILY,records=13,final_review=str(FINAL),new_revisions=0,justified_retentions=13,speaker_metadata_corrections=1,historical_reconciliation_only=True,new_completed_records=0,all_source_native_representative_family_registered_reconciliation_complete=True,new_current_ID_visits=[1411],new_current_actual_holds=2,historical_actual_IDs=4,historical_current_pixel_rechecks=8,new_emulator_runs=2,wrong_touch_run_has_zero_Cook_credit=True))
 l['active_source_prose_drafts']['note']=f['coverage_note'];l['next_cooking_contextual_source_packet_v2315']['resolved_in_v2323']=str(FINAL)
 l['cooking_contextual_v2323']=dict(summary=SUMMARY,final_review=str(FINAL),evidence=evidence,goal_turn_classification='progress',full_goal_complete=False)
 l['latest_checkpoint']=SUMMARY;l['current_integrated_candidate']['details']+=' V2323 reconciles13 unchanged Cook comments and corrects1419 speaker metadata only;binary and exact patch remain V2284.'
 l['formatting_watchlist']['cooking_contextual_v2323']=dict(status='13complete-current-V2284-retentions-original-registered216x36-crop',final_review=str(FINAL),native_fonts=13,native_copies=26,current_actual_IDs=[1411],historical_current_bound_IDs=4,no_runtime_font_or_geometry_change=True)
 keys={(r['file_path'],r['id'])for r in f['record_keys']}
 assert len(keys)==len(f['record_keys'])==len(f['record_IDs'])==1447 and Counter(p for p,i in keys)=={'/COMMON/MESFILE.DK4':791,'/data/SC2.DK4':428,'/data/SC0.DK4':117,'/data/SC1.DK4':73,'/data/SC3.DK4':38}
 assert l['records_editorially_completed']==2143 and l['records_revised_and_integrated']==1498 and l['retained_wordings_editorially_completed']==645 and sum(l['source_prose_reviewed_counts_by_file'].values())==2259 and len(l['reviewed_but_incomplete_COMMON_IDs'])==116 and l['goal_status']=='active'and not l['full_goal_complete']
 remaining=[dict(file_path=p,id=i,historical_family=g)for(p,i),g in oldhistory.items()if(p,i)not in keys]
 assert len(remaining)==696 and Counter(r['file_path']for r in remaining)=={'/COMMON/MESFILE.DK4':695,'/data/SC2.DK4':1}
 inv=ROOT/'remaining_historical_fresh_review_inventory.json';save(inv,dict(remaining=696,records=remaining,counts_by_file=dict(Counter(r['file_path']for r in remaining)),counts_by_family=dict(Counter(r['historical_family']for r in remaining)),full_goal_complete=False))
 l['next_remaining_historical_inventory_v2323']=dict(path=str(inv),sha256=sha(inv.read_bytes()),records=696);save(LEDGER,l)
 section='## V2323: Cook13 contextual retentions reconciled\n\n'+SUMMARY+'\n\nIndividual reviews: '+FINAL.as_posix()+'. Current native fonts: '+FONTS.as_posix()+'. Current ordinary gameplay: '+ACTUAL.as_posix()+'. Historical-only binding: '+HISTORY.as_posix()+'. Remaining inventory: '+inv.as_posix()+'. Current parser: dk4tool.patch.refit_contextual_spritsail_v1.current_entries. Guide: '+GUIDE.as_posix()+'.\n\n'
 first,rest=docs[0].read_text().split('\n',1);docs[0].write_text('# Current editorial handoff - V2323\n\n'+section+rest,newline='\n')
 for p in docs[1:]:first,rest=p.read_text().split('\n',1);p.write_text(first+'\n\n'+section+rest,newline='\n')
 GUIDE.mkdir(parents=True);images=[]
 for scope,items in[('offline-current-native-font',fonts['review_sheets']),('actual-current-V2284',[dict(path=actual['review_sheet'],sha256=actual['review_sheet_sha256'])]),('historical-only-V850',[dict(path=history['review_sheet'],sha256=history['review_sheet_sha256'])])]:
  for item in items:
   source=Path(item['path']);assert sha(source.read_bytes())==item['sha256'];target=GUIDE/(scope+'_'+source.name);copy2(source,target);images.append(dict(path=str(target),sha256=item['sha256'],kind=scope))
 assert len(images)==4
 save(GUIDE/'scope.json',dict(candidate=str(rompath),candidate_sha256=digest,final_review=str(FINAL),images=images,actual_offline_and_historical_scopes_distinct=True,current_actual_IDs=[1411],historical_actual_IDs=history['historical_IDs'],full_goal_complete=False))
 save(ROOT/'completion_receipt.json',dict(checkpoint='V2323',summary=SUMMARY,fresh_reconciliations=13,new_revisions=0,justified_retentions=13,speaker_metadata_corrections=1,fresh_integrated=1447,historical_complete=2143,source_prose_reviewed=2259,COMMON_incomplete=116,other_historical_fresh_reviews=696,candidate_sha256=digest,patch_sha256=release['patch_sha256'],guide=str(GUIDE),guide_images=4,evidence=evidence,updated_files={str(p):sha(p.read_bytes())for p in[LEDGER,*docs,NOTES,FINAL]},goal_turn_classification='progress',full_goal_complete=False))
 print(dict(checkpoint='V2323',fresh_integrated=1447,retained=13,speaker_metadata_corrected=1,ROM='unchanged-registered-V2284',other_historical_fresh_reviews=696,full_goal_complete=False))
