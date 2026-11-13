"""Reconcile50 source-first retentions into unchanged registered V2171."""
from pathlib import Path
from copy import deepcopy
from collections import Counter
from shutil import copy2
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.town_trade_port_contextual_reference_v1 import current_entries
from dk4tool.script.common_message_table import common_message_entries
from dk4tool.dialogue.review import validate_natural_dialogue_batch
from dk4tool.rom.nds import NdsImage
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/shared_context_completion_v2232')
LEDGER=Path('translations/editorial_review_current_v1.json')
DOC=Path('translations/shared_contextual_editorial_manuscript_v1.json')
NOTES=Path('translations/shared_contextual_editorial_manuscript_v2.json')
FINAL=Path('translations/shared_contextual_final_review_v1.json')
MATRIX=Path('work/analysis/shared_context_layouts_v2229/all50_current_native_layouts.json')
FONTS=Path('work/analysis/shared_context_fonts_v2230/all50_native_font_pagination_and_physical_samples.json')
ACTUAL=Path('work/analysis/shared_context_actual_v2231/current1042_and_historical_shared_family_evidence.json')
RELEASE=Path('work/analysis/town_trade_port_release_v2172/registered_release_verification.json')
GUIDE=Path('E:/Rota Nova translations/Guide screenshots/V2171 Shared50 contextual retentions verified')
FAMILY='Shared-warnings-village-fleet-recruitment-private50'
SUMMARY=('V2232 reconciles50 historical COMMON entries1020-1069 as fresh, individually justified retentions. '
 'Clean Japanese and complete functional exchanges cover missing contract-town information, seven low-success warnings and YesNo continuations, two supply-village coordinate rumors, unidentified-fleet anchorage/destination reports, required-crew shortage and remaining-capacity prompts, and21 independent private barmaid topics. '
 'All wording is retained with an individual source gloss and reason. Speakers, emotional turns, humor, family facts, fantasies and opinions remain source-grounded. Native branch selection, not catalog adjacency, defines the exchanges. '
 'Fresh current context passes624 actor-voice choices,21 private topic providers,48 village-coordinate fragments,570 town-name rumor fragments and20 headcount fragments. '
 'Consumer probes verify114 immutable town-role13 mappings,4 original role bindings,705 direct bindings,21 private bindings and the null-speaker system negative. The loader is supplied from actual current ROM entries; no actual gameplay is claimed for these CPU fragments. '
 'Original branch tests pass616 warning thresholds,8 acceptance/cancellation branches,204 crew/funds conditions,4 relationship stages,30 supplied chance selections,160 fleet filters,3 missing-information branches and150 complete village selectors. Supplied RNG/eligibility/branch inputs are offline tests, not earned world states. '
 'Role1 is freshly verified as First Mate/room6, with strict assignment208 and original speech fallback18/Charles Rochefort in the current Istanbul snapshot.1035-1048 are officer speech, not Barkeep. '
 'Required crew minus gathered crew and total capacity minus gathered crew remain separate meanings; source branch conditions suppress zero or exhausted real cases. Numeric-width boundary inputs in the layout matrix are explicitly stress tests. '
 'All857 current native printf/parent/table-or-ID selector/wrap cases pass complete bytes, words, argument copies, guards, bounds and ABI with no findings or waivers. '
 '1028/1029 preserve their original raw coordinate input buffers, while the selected native formatter produces inline coordinates. All83 selected full native font samples consume one complete page at unchanged logical228x48 bounds and6x12 metrics; all7 sheets were viewed. Physical16pixel pitch remains a separate oracle. '
 'Existing fixture-free V2171 capture2202 supplies the actual1042 sample: two complete foreground holds with51 spare places match native and independent output; its native font call returns fully. Five Assign Sailors/unassigned/menu/town frames were viewed. '
 'The original run gathers34 volunteers for1573gold and leaves them unassigned in this sample; eight paired state/company/fleet/ship/persistent controls are reused from its exact verified proof. No new emulator run or conditional visit is invented. '
 'Earlier V782/V783 evidence remains explicitly historical:17 complete holds across9 IDs1020/1022/1028/1029/1032/1034/1035/1042/1065 in8 scenarios,405 paired state/model/object/task frames,410 strict screen controls and2 blink controls. '
 'All50 complete stored paragraphs are byte-identical between the historical sampled ROMs and current V2171. The fresh current source/consumer/branch/layout/font checks bind the unchanged wording; older condition/identity/inventory fixtures do not become earned unlocks or gift acquisition. '
 'Current actual record coverage in this50 is1042 only; the other49 are offline or historical, not new current visits. No exhaustive conditional, full-route or hardware claim. '
 'No English,ROM,profile,registry,manifest or patch changes are needed. The existing shared editorial stage and all50 IDs are bound in V2171 manifest relocations. '
 'The492batch/114accepted-layer cumulative ROM and exact clean-input patch remain intact. Fresh coverage1157 reread/1157 integrated-reconciled/0pending. '
 'Historical2143=1498revised+645retained, source/prose2259 and116 incompleteCOMMON stay unchanged. Another986 historical completions require this fresh pass:985COMMON plusSC2B294R73. All never-reviewed routes/shared town/shop/random/player prose remain in scope. '
 'Full objective active; separate graphics/all18 plaques,SC3B109 classification and the later older-record technical re-audit remain open. All ROMs and earlier translations preserved. V1492 remains promoted; canonical and clean inputs unchanged.')

def key(row):
    path=row.get('file_path','/COMMON/MESFILE.DK4');n=row.get('message_id')
    return path,f'COMMON_MESSAGE_{n}'if n is not None and path=='/COMMON/MESFILE.DK4'else row['id']

if __name__=='__main__':
    assert not any(p.exists()for p in(ROOT,NOTES,FINAL,GUIDE))
    l,d,matrix,fonts,actual,release=[read(p)for p in(LEDGER,DOC,MATRIX,FONTS,ACTUAL,RELEASE)]
    f=l['contextual_story_natural_dialogue_pass_v1871']
    assert(f['fresh_pass_records_explicitly_reread'],f['fresh_pass_records_integrated'],f['fresh_pass_records_pending_native_actual_release'])==(1107,1107,0)
    assert len(d['records'])==50 and d['revised_IDs']==[]and d['retained_count']==50
    assert matrix['case_count']==857 and not matrix['findings']and matrix['all50_original_parent_table_and_ID_bindings_used']
    assert fonts['font_count']==83 and len(fonts['physical_sheets'])==7 and fonts['all83_single_native_pages_complete']
    assert {r['message_ID']for r in fonts['full_font_samples']}==set(range(1020,1070))
    assert len(actual['current_actual_holds'])==2 and len(actual['current_transition_frames'])==5 and actual['current50_recorded_actual_IDs']==[1042]
    assert len(actual['historical_holds'])==17 and actual['historical_all50_complete_encoded_paragraphs_identical_to_current']and actual['current_no_fixture_or_savestate']
    for p,h in d['native_context_proofs'].items():assert sha(Path(p).read_bytes())==h
    role=read('work/analysis/shared_role1_v2227/role1_speaker_context_correction.json')
    assert role['source_ROLE1_Japanese']=='副官'and role['accepted_ROLE1_English']=='First Mate'and role['role1_room_type']==6 and role['strict_assigned_actor_ID']==208 and role['selected_speech_actor_ID']==18
    rompath=Path(l['current_integrated_candidate']['path']);digest=sha(rompath.read_bytes());mp=rompath.with_suffix('.manifest.json');manifest=read(mp)
    registry_path=Path('translations/release_stack.json');registry=read(registry_path)
    assert digest==l['current_integrated_candidate']['sha256']==d['current_ROM_sha256']==actual['candidate_sha256']==release['candidate_sha256']==manifest['candidate_sha256']
    assert sha(mp.read_bytes())==release['manifest_sha256']and manifest['release_stack_sha256']==sha(registry_path.read_bytes())and all(manifest['checks'].values())
    assert len(manifest['batches'])==492 and len(registry['accepted_layers'])==114 and registry['latest_promoted_build']['profile']=='all-routes-unified-v1492'
    patch=Path(release['patch']);assert release['whole_ROM_reconstruction_byte_exact']and sha(patch.read_bytes())==release['patch_sha256']
    assert sha(Path('work/clean.nds').read_bytes())==release['clean_input_sha256']and sha(Path(manifest['base_rom']).read_bytes())==manifest['base_sha256']
    stage='shared_dialogue_editorial';row=manifest['relocations']['/COMMON/MESFILE.DK4'][stage]
    config=Path(registry['profiles'][manifest['profile']][stage]);c=read(config);man=Path(c['manuscript'])
    assert Path(row['release_config'])==config and row['release_config_sha256']==sha(config.read_bytes())and c['manuscript_sha256']==sha(man.read_bytes())
    assert set(row['proof']['changed_records'])=={f'COMMON_MESSAGE_{n}'for n in range(1020,1070)}
    binding=dict(stage=stage,config=str(config),config_sha256=sha(config.read_bytes()),manuscript=str(man),manuscript_sha256=sha(man.read_bytes()),IDs=list(range(1020,1070)))
    rom,clean=NdsImage.open(rompath),NdsImage.open('work/clean.nds');arm,common=rom.read_file('/__arm9__.bin'),rom.read_file('/COMMON/MESFILE.DK4')
    entries=current_entries(common,arm);jp=common_message_entries(clean.read_file('/COMMON/MESFILE.DK4'),clean.read_file('/__arm9__.bin'))
    assert sha(arm)==d['current_ARM9_sha256']==fonts['ARM9_sha256']==release['ARM9_sha256']and sha(common)==d['current_COMMON_sha256']==fonts['COMMON_sha256']==release['COMMON_sha256']
    history={key(r):g['id']for g in l['completed_editorial_families']for r in g['records']};keys={(r['file_path'],r['id'])for r in f['record_keys']};selected={('/COMMON/MESFILE.DK4',f'COMMON_MESSAGE_{n}')for n in range(1020,1070)}
    assert len(history)==2143 and not keys&selected and selected<=set(history)
    docs=[Path('docs')/p for p in('editorial_handoff_current.md','translation_progress.md','editorial_review_goal.md','todo.md','known_issues.md')]
    ROOT.mkdir(parents=True)
    for p in[LEDGER,*docs]:(ROOT/(p.name+'.before')).write_bytes(p.read_bytes())
    notes=deepcopy(d);notes.update(status='complete-fresh-contextual-retention-reconciled-registered-V2171',formatting_review_pending=False,English_identical_to_v1_and_current_ROM=True,no_new_ROM_profile_manifest_or_patch=True,final_review=str(FINAL),current_native_layouts=str(MATRIX),current_native_fonts=str(FONTS),current_and_historical_family_samples=str(ACTUAL),registered_native_stage_binding=binding)
    for r in notes['records']:
        n=r['message_id'];assert r['source_hex']==jp[n].text.hex()and entries[n].text==b' '+r['english'].removesuffix('{PAD}').encode('ascii')and r['current_hex']==entries[n].text.hex()
        r['review']['formatting']=True
        r.update(status='complete-fresh-whole-exchange-retention-native-display-representative-family-evidence-registered-reconciliation',original_historical_family=history[(r['file_path'],r['id'])],integrated_hex=entries[n].text.hex(),integrated_reference=dict(block=entries[n].block,offset=entries[n].block_offset,copy_end=entries[n].copy_end,bytes=len(entries[n].text)),integrated_stored_English=entries[n].text.decode('cp932'),formatting_gate_scope='857 complete current native layouts;83 full native font pages/7 viewed sheets;logical228x48 at6x12;physical16pitch separate.',actual_gameplay_coverage=[h for h in actual['current_actual_holds']if h['message_ID']==n],actual_gameplay_visited=n==1042,historical_actual_gameplay_coverage=[h for h in actual['historical_holds']if h['message_ID']==n],native_display_evidence=dict(layouts=str(MATRIX),fonts=str(FONTS),actual_scope=str(ACTUAL),only1042_has_recorded_current_V2171_visit=True,other49_offline_or_historical_not_new_current_visits=True))
    assert sum(r['actual_gameplay_visited']for r in notes['records'])==1
    validate_natural_dialogue_batch(notes);save(NOTES,notes)
    visual=ROOT/'visual_review.json'
    save(visual,dict(all83_native_font_samples_on7_sheets_viewed=True,all50_IDs_complete_leading_trailing_glyphs_names_numbers_coordinates_punctuation_and_final_lines_visible=True,all857_layouts_zero_findings_or_waivers=True,current1042_two_holds_and5_AssignSailors_menu_town_transitions_viewed=True,historical_17holds_on2sheets_for9_IDs_viewed_and_explicitly_labeled=True,current1042_native_return_complete=True,source_required_shortfall_spare_capacity_and_role1_voice_distinctions_preserved=True,physical16pitch_separate_from_logical12pitch_capacity=True,no_new_emulator_run_ROM_or_geometry=True,full_goal_complete=False))
    paths=[DOC,NOTES,MATRIX,FONTS,ACTUAL,RELEASE,mp,registry_path,visual,Path(__file__),Path('work/analysis/shared_context_source_v2222/all50_clean_current_context_catalog.json'),Path('work/analysis/shared_context_prose_v2228/source_first_whole_exchange_review.json')]
    paths.extend(Path(p)for p in d['native_context_proofs'])
    paths.extend(Path(actual[k])for k in('source_current_proof','source_report','source_observer','native_continuation','historical_family_proof'))
    paths.extend(Path(p['path'])for p in actual['historical_scenario_proofs'])
    evidence={str(p):sha(p.read_bytes())for p in paths}
    save(FINAL,dict(format='dk4-editorial-family-final-review-v1',family=FAMILY,file_path='/COMMON/MESFILE.DK4',native_message_IDs=list(range(1020,1070)),revised_count=0,retained_count=50,historical_reconciliation_only=True,new_completed_records=0,records=notes['records'],summary=SUMMARY,evidence=evidence,registered_native_stage_binding=binding,candidate=str(rompath),candidate_sha256=digest,profile=manifest['profile'],patch=str(patch),patch_sha256=release['patch_sha256'],whole_clean_input_reconstruction_exact=True,no_ROM_profile_registry_manifest_patch_changes=True,actual_scope=dict(current_reused_capture='recruitment_actual_v2202_V2171',current_run_frames=8801,current_recorded_IDs=[1042],current_holds=2,current_AssignSailors_menu_town_frames=5,current_native_font_return_complete=True,current_exact_paired_state_model_controls_inherited=8,current_no_fixture_or_savestate=True,new_emulator_runs=0,historical_ROMs='V782/V783',historical_IDs=[1020,1022,1028,1029,1032,1034,1035,1042,1065],historical_holds=17,historical_scenarios=8,historical_paired_state_model_task_controls=405,historical_screen_controls=410,historical_blink_controls=2,historical_fixtures_explicit_not_earned_progress=True,historical_all50_encoded_paragraphs_identical_current=True,other49_current_entries_offline_or_historical_not_new_current_visits=True),offline_scope=dict(actor_voice_selections=624,private_barmaid_providers=21,village_coordinate_provider_fragments=48,town_rumor_fragments=570,headcount_fragments=20,immutable_town_NPC_mappings=114,role_bindings=4,direct_bindings=705,private_bindings=21,null_system_negative=True,warning_thresholds=616,warning_confirmations=8,crew_conditions=204,relationship_stages=4,chance_branches=30,fleet_filters=160,missing_information_conditions=3,full_village_selector_cases=150,all_CPU_boundary_inputs_not_gameplay=True,current_FirstMate_fallback_Charles_proven=True,current_native_layouts=857,unresolved_findings=0,full_native_font_cases=83,sheets_viewed=7,all_single_pages_original228x48_and6x12=True),full_goal_complete=False))
    f['record_keys'].extend(dict(file_path=r['file_path'],id=r['id'])for r in notes['records']);f['record_IDs'].extend(r['id']for r in notes['records'])
    f.update(fresh_pass_records_explicitly_reread=1157,fresh_pass_records_integrated=1157,fresh_pass_records_pending_native_actual_release=0,historical_completed_records_outside_reconciled_fresh_pass=986,latest_contextual_manuscript=str(NOTES),latest_completed_family=FAMILY,latest_reconciled_historical_family=FAMILY,latest_contextual_retention_review=str(FINAL),latest_final_review=str(FINAL),latest_pending_contextual_family=None,coverage_note='1157 file-qualified fresh rereads integrated/reconciled;986 other historical completions,116 incomplete COMMON and all never-reviewed route/shared town/shop/random/player prose remain in scope.')
    f['reconciled_families'].append(dict(id=FAMILY,records=50,final_review=str(FINAL),new_revisions=0,justified_retentions=50,historical_reconciliation_only=True,new_completed_records=0,all_source_native_representative_family_registered_reconciliation_complete=True,current_recorded_ID_visits=1,historical_sample_IDs=9,new_emulator_runs=0))
    l['active_source_prose_drafts']['note']=f['coverage_note'];l['next_shared_contextual_source_packet_v2223']['resolved_in_v2232']=str(FINAL);l['shared_contextual_v2232']=dict(summary=SUMMARY,final_review=str(FINAL),evidence=evidence,goal_turn_classification='progress',full_goal_complete=False);l['latest_checkpoint']=SUMMARY
    l['current_integrated_candidate']['details']+=' V2232 freshly reconciles50 unchanged shared entries; binary and exact patch remain V2171.'
    l['formatting_watchlist']['shared_contextual_v2232']=dict(status='50complete-current-V2171-retentions-original228x48-four12rows',final_review=str(FINAL),all857_current_native_layouts_pass=True,all83_full_fonts_and7sheets_viewed=True,source_coordinate_argument_copies_complete=True,current1042_reused_actual_complete=True,historical9_IDs17holds_explicit=True,no_runtime_font_or_geometry_changes=True)
    keys={(r['file_path'],r['id'])for r in f['record_keys']}
    assert len(keys)==len(f['record_keys'])==len(f['record_IDs'])==1157 and Counter(p for p,i in keys)=={'/COMMON/MESFILE.DK4':501,'/data/SC2.DK4':428,'/data/SC0.DK4':117,'/data/SC1.DK4':73,'/data/SC3.DK4':38}
    assert l['records_editorially_completed']==2143 and l['records_revised_and_integrated']==1498 and l['retained_wordings_editorially_completed']==645 and sum(l['source_prose_reviewed_counts_by_file'].values())==2259 and len(l['reviewed_but_incomplete_COMMON_IDs'])==116 and l['goal_status']=='active'and not l['full_goal_complete']
    remaining=[dict(file_path=p,id=i,historical_family=g)for(p,i),g in history.items()if(p,i)not in keys]
    assert len(remaining)==986 and Counter(r['file_path']for r in remaining)=={'/COMMON/MESFILE.DK4':985,'/data/SC2.DK4':1}
    inv=ROOT/'remaining_historical_fresh_review_inventory.json';save(inv,dict(remaining=986,records=remaining,counts_by_file=dict(Counter(r['file_path']for r in remaining)),counts_by_family=dict(Counter(r['historical_family']for r in remaining)),full_goal_complete=False))
    l['next_remaining_historical_inventory_v2232']=dict(path=str(inv),sha256=sha(inv.read_bytes()),records=986);save(LEDGER,l)
    section='## V2232: Shared50 contextual retentions reconciled in unchanged V2171\n\n'+SUMMARY+'\n\nExact source/current spans and individual reasons: '+FINAL.as_posix()+'. Current native layouts: '+MATRIX.as_posix()+'. Full fonts: '+FONTS.as_posix()+'. Explicit current/historical gameplay scopes: '+ACTUAL.as_posix()+'.\n\nNotes-only v2 completes formatting and integrated references. The existing registered shared stage is in manifest relocations. Source label/room/assignment/speech-provider proof confirms First Mate and Charles fallback, preserving the historical metadata correction. No new ROM or duplicate layer is needed for retained wording. Current1042 is reused from2202; historical eight-scenario playback remains historical.\n\nRemaining file-qualified historical fresh-review inventory: '+inv.as_posix()+'. Continue Guild item buying/selling/Purser bargaining1070-1096,courier346-348,diplomatic letters1097-1145 and all remaining routes/random/player prose. Separate graphics/all18 plaques,SC3B109 classification and later older-record re-audit remain open. Current parser remains dk4tool.patch.town_trade_port_contextual_reference_v1.current_entries. All jobs terminal. Guide: '+GUIDE.as_posix()+'.\n\n'
    text=docs[0].read_text();assert text.startswith('# Current editorial handoff - V2223')
    text=text.replace('# Current editorial handoff - V2223','# Current editorial handoff - V2232',1).replace('- Fresh contextual pass: **1107 reread,1107 integrated/reconciled,0 pending.** Another1036 historical completions still require fresh contextual reconciliation.','- Fresh contextual pass: **1157 reread,1157 integrated/reconciled,0 pending.** Another986 historical completions still require fresh contextual reconciliation.',1)
    first,rest=text.split('\n',1);docs[0].write_text(first+'\n\n'+section+rest,newline='\n')
    for p in docs[1:]:
        first,rest=p.read_text().split('\n',1);p.write_text(first+'\n\n'+section+rest,newline='\n')
    GUIDE.mkdir(parents=True)
    images=[(Path(r['path']),Path(r['path']).name,r['scope'])for r in actual['review_sheets']]
    images.extend((Path(r['path']),f'offline_font_sheet_{i:02d}.png','offline-current-native-font-physical-oracle;not-actual-gameplay')for i,r in enumerate(fonts['physical_sheets']))
    saved=[]
    for source,name,kind in images:
        target=GUIDE/name;copy2(source,target);assert sha(target.read_bytes())==sha(source.read_bytes());saved.append(dict(path=str(target),sha256=sha(target.read_bytes()),kind=kind))
    assert len(saved)==11
    save(GUIDE/'scope.json',dict(candidate=str(rompath),candidate_sha256=digest,final_review=str(FINAL),images=saved,current_reused_actual_historical_family_and_offline_labels_distinct=True,current50_recorded_IDs=[1042],new_emulator_runs=0,no_ROM_or_geometry_change=True,full_goal_complete=False))
    save(ROOT/'completion_receipt.json',dict(checkpoint='V2232',summary=SUMMARY,fresh_reconciliations=50,new_revisions=0,justified_retentions=50,fresh_integrated=1157,historical_complete=2143,source_prose_reviewed=2259,COMMON_incomplete=116,other_historical_fresh_reviews=986,candidate_sha256=digest,patch_sha256=release['patch_sha256'],guide=str(GUIDE),guide_images=11,evidence=evidence,updated_files={str(p):sha(p.read_bytes())for p in[LEDGER,*docs,NOTES,FINAL]},goal_turn_classification='progress',full_goal_complete=False))
    print(dict(checkpoint='V2232',fresh_integrated=1157,reconciled50=True,revised=0,retained=50,ROM='unchanged-V2171',other_historical_fresh_reviews=986,full_goal_complete=False))
