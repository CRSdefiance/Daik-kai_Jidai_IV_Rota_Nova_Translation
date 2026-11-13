"""Reconcile31 fresh contextual retentions; current and historical gameplay stay separate."""
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

ROOT=Path('work/analysis/barmaid_context_completion_v2221')
LEDGER=Path('translations/editorial_review_current_v1.json')
DOC=Path('translations/barmaid_contextual_editorial_manuscript_v1.json')
NOTES=Path('translations/barmaid_contextual_editorial_manuscript_v2.json')
FINAL=Path('translations/barmaid_contextual_final_review_v1.json')
MATRIX=Path('work/analysis/barmaid_context_layouts_v2217/all31_current_native_layouts.json')
FONTS=Path('work/analysis/barmaid_context_fonts_v2218/all31_native_font_pagination_and_physical_samples.json')
ACTUAL=Path('work/analysis/barmaid_context_actual_v2220/current_fallback_and_historical_family_evidence.json')
RELEASE=Path('work/analysis/town_trade_port_release_v2172/registered_release_verification.json')
GUIDE=Path('E:/Rota Nova translations/Guide screenshots/V2171 Barmaid31 contextual retentions verified')
FAMILY='Tavern-barmaid-introductions-gifts-casual31'
SUMMARY=('V2221 reconciles31 historical COMMON entries989-1019 as fresh individually justified retentions. '
 'Source-first Japanese glosses and complete native interaction branches establish ordered introductions, ordinary independent replies, gift reactions and city/personality-specific conversation. '
 'Retained wording preserves fado, Venus, younger siblings, parents, songs, affection, social opinions and character tone without inventing romance, exact ages, family ties, identities or mechanics. '
 '989 supplies barmaid then captain first name;990 supplies captain then barmaid;999 supplies captain first name. Existing827 remains the original fallback, distinct from these alternatives. '
 'Fresh current native context covers114 city lookups,21 initialized barmaids and84 city/name-provider cases. Thirty entries are selected by that catalog. '
 '996 is a separately reviewed latent source branch: catalog city58 has no matching NPC. A fresh whole-unit caller census closes the two original private chains; three typed source scan coincidences and114 guard cases are bound to unchanged source spans from prior evidence. No normal activation is claimed or invented. '
 'The16byte editable first-name capacity and17byte including-NUL serialization contract are source-bound to prior24 keyboard/IO-boundary tests; those tests are inherited, not new physical keyboard or save/load runs. '
 'All273 current native printf/direct-parent/ID-selector/wrap cases pass complete bytes, words, guards, bounds and ABI. Five apparent weak article endings are exactly literal player-name initials, proved by byte origins and a literal-prose negative; no prose or name warning is waived. '
 'All52 selected full native font samples consume one complete page at unchanged logical228x48 bounds and6x12 metrics;all5 sheets were viewed. Physical16pixel pitch is a separate oracle. '
 'A new ordinary fixture-free9201frame London V2171 cold boot selects fallback827, exactly as original city0 dispatch specifies. Two complete foreground holds match native and independent output, all9 observed native font calls return fully and8 speech/menu frames were viewed. '
 'Its cash40659->40654->40644->40644->40639 reflects20gold of ordinary drinks. London barmaid relationship stage advances0to1, requested gift owner/availability stay unchanged, and fleet/ship models stay unchanged. Company hashes include the paid cash. These are within-run source checks, not paired comparisons to the Istanbul schedule donor. '
 'This current run adds zero visits among989-1019. Earlier V780 evidence remains explicitly historical:12complete holds for989/990/991/999/1000/1014, paired state/model/task and relationship/gift outcomes from declared location/inventory fixtures. '
 'All31 complete stored paragraphs are byte-identical between the historical sampled ROM and current V2171. Current273 layouts/52 full fonts and current fallback consumer complement those inherited family samples. No new travel, earned gift acquisition, individual activation, full-route or hardware claim. '
 'No English, ROM, profile, registry, manifest or patch changes are needed. The existing registered barmaid stage and all31 IDs are bound in V2171 manifest relocations. '
 'The492batch/114accepted-layer cumulative ROM and exact clean-input patch remain intact. Fresh coverage1107 reread/1107 integrated-reconciled/0pending. '
 'Historical2143=1498revised+645retained,source/prose2259 and116 incompleteCOMMON remain unchanged. Another1036 historical completions require this fresh pass, plus all never-reviewed routes/shared town/shop/random/player prose. '
 'Full objective active; separate graphics/all18 plaques,SC3B109 classification and the later older-record technical re-audit remain open. All ROMs/earlier translations preserved. V1492 stays promoted;canonical and clean inputs unchanged.')

def key(row):
    path=row.get('file_path','/COMMON/MESFILE.DK4');n=row.get('message_id')
    return path,f'COMMON_MESSAGE_{n}'if n is not None and path=='/COMMON/MESFILE.DK4'else row['id']

if __name__=='__main__':
    assert not any(p.exists()for p in(ROOT,NOTES,FINAL,GUIDE))
    l,d,matrix,fonts,actual,release=[read(p)for p in(LEDGER,DOC,MATRIX,FONTS,ACTUAL,RELEASE)]
    f=l['contextual_story_natural_dialogue_pass_v1871']
    assert(f['fresh_pass_records_explicitly_reread'],f['fresh_pass_records_integrated'],f['fresh_pass_records_pending_native_actual_release'])==(1076,1076,0)
    assert len(d['records'])==31 and d['revised_IDs']==[]and d['retained_count']==31
    assert matrix['case_count']==273 and not matrix['findings']and len(matrix['raw_name_initial_diagnostics'])==5 and matrix['literal_prose_negative_control_rejected']
    assert fonts['font_count']==52 and len(fonts['physical_sheets'])==5 and fonts['all52_single_native_pages_complete']
    assert {r['message_ID']for r in fonts['full_font_samples']}==set(range(989,1020))
    assert len(actual['current_actual_holds'])==2 and len(actual['current_transition_frames'])==8 and actual['current_all9_unstubbed_font_returns_complete']
    assert actual['current31_new_actual_ID_visits']==[]and len(actual['historical_holds'])==12 and actual['historical_all31_complete_encoded_paragraphs_identical_to_current']
    assert actual['current_no_fixture_or_savestate']and actual['current_ordinary_London_uses_source_fallback827_not989']
    for p,h in d['native_context_proofs'].items():assert sha(Path(p).read_bytes())==h
    rompath=Path(l['current_integrated_candidate']['path']);digest=sha(rompath.read_bytes());mp=rompath.with_suffix('.manifest.json')
    manifest=read(mp);registry_path=Path('translations/release_stack.json');registry=read(registry_path)
    assert digest==l['current_integrated_candidate']['sha256']==d['current_ROM_sha256']==actual['candidate_sha256']==release['candidate_sha256']==manifest['candidate_sha256']
    assert sha(mp.read_bytes())==release['manifest_sha256']and manifest['release_stack_sha256']==sha(registry_path.read_bytes())and all(manifest['checks'].values())
    assert len(manifest['batches'])==492 and len(registry['accepted_layers'])==114 and registry['latest_promoted_build']['profile']=='all-routes-unified-v1492'
    patch=Path(release['patch']);assert release['whole_ROM_reconstruction_byte_exact']and sha(patch.read_bytes())==release['patch_sha256']
    assert sha(Path('work/clean.nds').read_bytes())==release['clean_input_sha256']and sha(Path(manifest['base_rom']).read_bytes())==manifest['base_sha256']
    stage='barmaid_editorial';row=manifest['relocations']['/COMMON/MESFILE.DK4'][stage]
    config=Path(registry['profiles'][manifest['profile']][stage]);c=read(config);man=Path(c['manuscript'])
    assert Path(row['release_config'])==config and row['release_config_sha256']==sha(config.read_bytes())and c['manuscript_sha256']==sha(man.read_bytes())
    assert set(row['proof']['changed_records'])=={f'COMMON_MESSAGE_{n}'for n in range(989,1020)}
    binding=dict(stage=stage,config=str(config),config_sha256=sha(config.read_bytes()),manuscript=str(man),manuscript_sha256=sha(man.read_bytes()),IDs=list(range(989,1020)))
    rom,clean=NdsImage.open(rompath),NdsImage.open('work/clean.nds');arm,common=rom.read_file('/__arm9__.bin'),rom.read_file('/COMMON/MESFILE.DK4')
    entries=current_entries(common,arm);jp=common_message_entries(clean.read_file('/COMMON/MESFILE.DK4'),clean.read_file('/__arm9__.bin'))
    assert sha(arm)==d['current_ARM9_sha256']==fonts['ARM9_sha256']==release['ARM9_sha256']and sha(common)==d['current_COMMON_sha256']==fonts['COMMON_sha256']==release['COMMON_sha256']
    history={key(r):g['id']for g in l['completed_editorial_families']for r in g['records']};keys={(r['file_path'],r['id'])for r in f['record_keys']}
    selected={('/COMMON/MESFILE.DK4',f'COMMON_MESSAGE_{n}')for n in range(989,1020)}
    assert len(history)==2143 and not keys&selected and selected<=set(history)
    docs=[Path('docs')/p for p in('editorial_handoff_current.md','translation_progress.md','editorial_review_goal.md','todo.md','known_issues.md')]
    ROOT.mkdir(parents=True)
    for p in[LEDGER,*docs]:(ROOT/(p.name+'.before')).write_bytes(p.read_bytes())
    notes=deepcopy(d)
    notes.update(status='complete-fresh-contextual-retention-reconciled-registered-V2171',formatting_review_pending=False,English_identical_to_v1_and_current_ROM=True,no_new_ROM_profile_manifest_or_patch=True,final_review=str(FINAL),current_native_layouts=str(MATRIX),current_native_fonts=str(FONTS),current_fallback_and_historical_family_sample=str(ACTUAL),registered_native_stage_binding=binding)
    for r in notes['records']:
        n=r['message_id'];assert r['source_hex']==jp[n].text.hex()and entries[n].text==b' '+r['english'].removesuffix('{PAD}').encode('ascii')and r['current_hex']==entries[n].text.hex()
        r['review']['formatting']=True
        r.update(status='complete-fresh-whole-interaction-retention-native-display-representative-family-evidence-registered-reconciliation',original_historical_family=history[(r['file_path'],r['id'])],integrated_hex=entries[n].text.hex(),integrated_reference=dict(block=entries[n].block,offset=entries[n].block_offset,copy_end=entries[n].copy_end,bytes=len(entries[n].text)),integrated_stored_English=entries[n].text.decode('cp932'),formatting_gate_scope='273 current native layouts;five typed literal-name diagnostics/negative control;52 full native font pages/5 viewed sheets;logical228x48 at6x12;physical16pitch separate.',actual_gameplay_coverage=[],actual_gameplay_visited=False,historical_actual_gameplay_coverage=[h for h in actual['historical_holds']if h['message_ID']==n],current_actual_fallback827_is_consumer_family_context_not_this_record_visit=True,native_display_evidence=dict(layouts=str(MATRIX),fonts=str(FONTS),actual_scope=str(ACTUAL),all31_current_offline_not_individually_revisited=True))
    validate_natural_dialogue_batch(notes);save(NOTES,notes)
    visual=ROOT/'visual_review.json'
    save(visual,dict(all52_native_font_samples_on5_sheets_viewed=True,all31_IDs_complete_leading_trailing_names_punctuation_and_final_lines_visible=True,logical4row1004_1007_1010_1011_1015_samples_complete=True,current_fallback827_two_holds_and8_transitions_viewed=True,historical_V780_12holds_for6consumer_families_viewed_and_labeled=True,current31_new_actual_visits=0,latent996_no_normal_activation_claim=True,physical16pitch_separate_from_logical12pitch_capacity=True,no_new_ROM_or_geometry=True,full_goal_complete=False))
    paths=[DOC,NOTES,MATRIX,FONTS,ACTUAL,RELEASE,mp,registry_path,visual,Path(__file__),Path('work/analysis/barmaid_context_source_v2212/all31_clean_current_context_catalog.json'),Path('work/analysis/barmaid_context_prose_v2215/source_first_whole_interaction_review.json')]
    paths.extend(Path(p)for p in d['native_context_proofs'])
    paths.extend(Path(actual[k])for k in('source_plan','source_report','source_observer','native_continuation','historical_family_proof'))
    paths.extend(Path(p['path'])for p in actual['historical_scenario_proofs'])
    evidence={str(p):sha(p.read_bytes())for p in paths}
    save(FINAL,dict(format='dk4-editorial-family-final-review-v1',family=FAMILY,file_path='/COMMON/MESFILE.DK4',native_message_IDs=list(range(989,1020)),revised_count=0,retained_count=31,historical_reconciliation_only=True,new_completed_records=0,records=notes['records'],summary=SUMMARY,evidence=evidence,registered_native_stage_binding=binding,candidate=str(rompath),candidate_sha256=digest,profile=manifest['profile'],patch=str(patch),patch_sha256=release['patch_sha256'],whole_clean_input_reconstruction_exact=True,no_ROM_profile_registry_manifest_patch_changes=True,actual_scope=dict(current_ordinary_frames=9201,current_ordinary_IDs_from_this31=[],current_fallback827_context_holds=2,current_speech_menu_frames=8,current_unstubbed_font_returns=9,current_within_run_state_controls=5,current_cash=[40659,40654,40644,40644,40639],current_barmaid_stage0_to1=True,current_no_fixture_or_savestate=True,historical_ROM='V780',historical_IDs=[989,990,991,999,1000,1014],historical_holds=12,historical_fixtures_location_inventory_not_earned_gifts_or_travel=True,historical_all31_encoded_words_identical_current=True,all31_current_native_offline_checks_not_individual_current_visits=True),offline_scope=dict(fresh_native_city_lookups=114,fresh_initialized_barmaids=21,fresh_original_city_name_cases=84,fresh_private_caller_chains=2,inherited_typed_reference_classifications=3,inherited_town_guard_cases=114,inherited_first_name_bound_cases=24,first_name_bytes16_NUL_serialized17=True,latent996_normal_activation_unclaimed=True,current_native_layouts=273,typed_literal_name_initials=5,literal_prose_negative_rejected=True,unresolved_findings=0,full_native_font_cases=52,sheets_viewed=5,all_single_pages_original228x48_and6x12=True),full_goal_complete=False))
    f['record_keys'].extend(dict(file_path=r['file_path'],id=r['id'])for r in notes['records']);f['record_IDs'].extend(r['id']for r in notes['records'])
    f.update(fresh_pass_records_explicitly_reread=1107,fresh_pass_records_integrated=1107,fresh_pass_records_pending_native_actual_release=0,historical_completed_records_outside_reconciled_fresh_pass=1036,latest_contextual_manuscript=str(NOTES),latest_completed_family=FAMILY,latest_reconciled_historical_family=FAMILY,latest_contextual_retention_review=str(FINAL),latest_final_review=str(FINAL),latest_pending_contextual_family=None,coverage_note='1107 file-qualified fresh rereads integrated/reconciled;1036 other historical completions,116 incomplete COMMON and all never-reviewed route/shared town/shop/random/player prose remain in scope.')
    f['reconciled_families'].append(dict(id=FAMILY,records=31,final_review=str(FINAL),new_revisions=0,justified_retentions=31,historical_reconciliation_only=True,new_completed_records=0,all_source_native_representative_family_registered_reconciliation_complete=True,current_individual_ID_visits=0,historical_sample_IDs=6))
    l['active_source_prose_drafts']['note']=f['coverage_note'];l['barmaid_contextual_v2221']=dict(summary=SUMMARY,final_review=str(FINAL),evidence=evidence,goal_turn_classification='progress',full_goal_complete=False);l['latest_checkpoint']=SUMMARY
    l['current_integrated_candidate']['details']+=' V2221 freshly reconciles31 unchanged barmaid entries; binary and exact patch remain V2171.'
    l['formatting_watchlist']['barmaid_contextual_v2221']=dict(status='31complete-current-V2171-retentions-original228x48-four12rows',final_review=str(FINAL),all273_current_native_layouts_pass=True,five_name_initial_diagnostics_typed_no_prose_waiver=True,all52_full_fonts_and5sheets_viewed=True,current_actual_fallback827_context_only=True,historical6families12holds_explicit=True,no_runtime_font_or_geometry_changes=True)
    keys={(r['file_path'],r['id'])for r in f['record_keys']}
    assert len(keys)==len(f['record_keys'])==len(f['record_IDs'])==1107 and Counter(p for p,i in keys)=={'/COMMON/MESFILE.DK4':451,'/data/SC2.DK4':428,'/data/SC0.DK4':117,'/data/SC1.DK4':73,'/data/SC3.DK4':38}
    assert l['records_editorially_completed']==2143 and l['records_revised_and_integrated']==1498 and l['retained_wordings_editorially_completed']==645 and sum(l['source_prose_reviewed_counts_by_file'].values())==2259 and len(l['reviewed_but_incomplete_COMMON_IDs'])==116 and l['goal_status']=='active'and not l['full_goal_complete']
    remaining=[dict(file_path=p,id=i,historical_family=g)for(p,i),g in history.items()if(p,i)not in keys]
    assert len(remaining)==1036 and Counter(r['file_path']for r in remaining)=={'/COMMON/MESFILE.DK4':1035,'/data/SC2.DK4':1}
    inv=ROOT/'remaining_historical_fresh_review_inventory.json'
    save(inv,dict(remaining=1036,records=remaining,counts_by_file=dict(Counter(r['file_path']for r in remaining)),counts_by_family=dict(Counter(r['historical_family']for r in remaining)),full_goal_complete=False))
    l['next_remaining_historical_inventory_v2221']=dict(path=str(inv),sha256=sha(inv.read_bytes()),records=1036);save(LEDGER,l)
    section='## V2221: Barmaid31 contextual retentions reconciled in unchanged V2171\n\n'+SUMMARY+'\n\nExact source/current spans and individual reasons: '+FINAL.as_posix()+'. Current layouts: '+MATRIX.as_posix()+'. Full fonts: '+FONTS.as_posix()+'. Explicit current/historical gameplay scopes: '+ACTUAL.as_posix()+'.\n\nNotes-only v2 completes formatting and integrated references. The existing registered barmaid stage is in manifest relocations. Current fallback827 is not credited as a visit to989-1019; old V780 gameplay is explicitly inherited and all31 complete stored paragraphs are exact to current. The source city map remains London0/Marie;989 branches are Hamburg5/Margrete,Seville13/Donna andAlexandria25/Nelly. No new location or gift fixture is needed to repeat equivalent historical conditions.\n\nRemaining file-qualified historical fresh-review inventory: '+inv.as_posix()+'. Next: shared warnings,village,fleet recruitment and private barmaid1020-1069, followed by remaining routes/random/player prose. Separate graphics/all18 plaques,SC3B109 classification and later older-record re-audit remain open. Current parser remains dk4tool.patch.town_trade_port_contextual_reference_v1.current_entries. All jobs terminal. Guide: '+GUIDE.as_posix()+'.\n\n'
    text=docs[0].read_text();assert text.startswith('# Current editorial handoff - V2211')
    text=text.replace('# Current editorial handoff - V2211','# Current editorial handoff - V2221',1).replace('- Fresh contextual pass: **1076 reread,1076 integrated/reconciled,0 pending.** Another1067 historical completions still require fresh contextual reconciliation.','- Fresh contextual pass: **1107 reread,1107 integrated/reconciled,0 pending.** Another1036 historical completions still require fresh contextual reconciliation.',1)
    first,rest=text.split('\n',1);docs[0].write_text(first+'\n\n'+section+rest,newline='\n')
    for p in docs[1:]:
        first,rest=p.read_text().split('\n',1);p.write_text(first+'\n\n'+section+rest,newline='\n')
    GUIDE.mkdir(parents=True)
    images=[(Path(r['path']),Path(r['path']).name,r['scope'])for r in actual['review_sheets']]
    images.extend((Path(r['path']),f'offline_font_sheet_{i:02d}.png','offline-current-native-font-physical-oracle;not-actual-gameplay')for i,r in enumerate(fonts['physical_sheets']))
    saved=[]
    for source,name,kind in images:
        target=GUIDE/name;copy2(source,target);assert sha(target.read_bytes())==sha(source.read_bytes())
        saved.append(dict(path=str(target),sha256=sha(target.read_bytes()),kind=kind))
    assert len(saved)==8
    save(GUIDE/'scope.json',dict(candidate=str(rompath),candidate_sha256=digest,final_review=str(FINAL),images=saved,current_fallback_historical_family_and_offline_labels_distinct=True,current31_new_actual_visits=0,no_ROM_or_geometry_change=True,full_goal_complete=False))
    save(ROOT/'completion_receipt.json',dict(checkpoint='V2221',summary=SUMMARY,fresh_reconciliations=31,new_revisions=0,justified_retentions=31,fresh_integrated=1107,historical_complete=2143,source_prose_reviewed=2259,COMMON_incomplete=116,other_historical_fresh_reviews=1036,candidate_sha256=digest,patch_sha256=release['patch_sha256'],guide=str(GUIDE),guide_images=8,evidence=evidence,updated_files={str(p):sha(p.read_bytes())for p in[LEDGER,*docs,NOTES,FINAL]},goal_turn_classification='progress',full_goal_complete=False))
    print(dict(checkpoint='V2221',fresh_integrated=1107,reconciled31=True,revised=0,retained=31,ROM='unchanged-V2171',other_historical_fresh_reviews=1036,full_goal_complete=False))
