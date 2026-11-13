"""Reconcile106 individually justified retentions against unchanged registered V2171."""
from pathlib import Path
from copy import deepcopy
from collections import Counter
from shutil import copy2
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.town_trade_port_contextual_reference_v1 import current_entries
from dk4tool.script.common_message_table import common_message_entries
from dk4tool.dialogue.review import validate_natural_dialogue_batch
from dk4tool.rom.nds import NdsImage
from scripts.verify_village_wrap_v608 import read, save

ROOT=Path('work/analysis/recruitment_scheme_completion_v2211')
LEDGER=Path('translations/editorial_review_current_v1.json')
DOC=Path('translations/recruitment_schemes_contextual_editorial_manuscript_v1.json')
NOTES=Path('translations/recruitment_schemes_contextual_editorial_manuscript_v2.json')
FINAL=Path('translations/recruitment_schemes_contextual_final_review_v1.json')
MATRIX=Path('work/analysis/recruitment_scheme_layouts_v2203b/all106_current_native_layouts.json')
FONTS=Path('work/analysis/recruitment_scheme_fonts_v2205/all106_native_font_pagination_and_physical_samples.json')
RECRUIT=Path('work/analysis/recruitment_actual_verification_v2208/ordinary_recruitment_foreground_state_transitions.json')
BRIBE=Path('work/analysis/scheme_bribe_actual_verification_v2210b/scheme_bribe_foreground_fixture_state_transitions.json')
CONTRACT=Path('work/analysis/current_scheme_filter_binding_v2200/source_filter_and_current_name_contract.json')
RELEASE=Path('work/analysis/town_trade_port_release_v2172/registered_release_verification.json')
GUIDE=Path('E:/Rota Nova translations/Guide screenshots/V2171 Recruitment schemes106 contextual retentions verified')
FAMILY='Tavern-recruitment-schemes-followup106'
SUMMARY=('V2211 reconciles 106 historical COMMON entries 883-988 as fresh, individually justified retentions. '
 'Clean Japanese and complete functional exchanges cover funds, recruitment offers and calls, the gathered count before assignment, town-condition rumors, scheme selection and targets, confirmations, deferred arrangements, the independent regular-ship rumor, bribe targets and privacy refusals. '
 'All existing English is retained with an individual source gloss and reason. Actual original consumers bind role1 recruitment and role2 schemes, table/voice choices and argument order. '
 '904 reports volunteers gathered before Assign Sailors, not sailors already assigned. 907 is the original reaction NPC, without an invented crowd identity. '
 '905/906 take original read-only UI condition pointers and private grammatical phrases for twelve eligible conditions; seasonings and spices stay distinct and Normal is excluded. '
 '964-971 announce arrangements before the original subsequent charge and deferred outcome, not guaranteed success. 972 is a separate condition-selected regular-ship rumor. 987 says later and 988 explicitly says tomorrow. '
 'All 56,852 current native printf/selector/wrap cases pass with no findings or waivers. These include supplied stress combinations, not claims that every combination can be selected or earned. '
 'The original scheme filters exclude the editable player company and exclude the first target from the second choice. Fixed nonplayer names therefore bound the target-name domain. '
 'The old synthetic 23-byte faction string is outside that domain; its exclusion is not a waiver for general custom-name issues. Current width24 is already registered through later layers; original ordinary selector closure remains inherited evidence. '
 'All 400 selected full native font samples consume one complete page at unchanged logical228x48 bounds and6x12 metrics; all34 sheets were viewed. Physical16pixel pitch is a separate oracle. '
 'An ordinary fixture-free genuine-save current V2171 cold boot runs8801frames: eight complete foreground holds cover890/897/907/904; seven Assign Sailors/unassigned/return frames were viewed; all seven observed font calls return fully. '
 'The original charge1573 takes cash8371 to6798 and gathers34 volunteers, left unassigned in this sample. Eight state/company/fleet/ship/persistent controls match historical identical inputs. Context1042/71 adds no editorial credit. '
 'A separate13200frame focused Bribe cold boot uses the explicitly declared three room/assignment bytes, one XP word to300000 and calendar+528ticks=11days fixture. All other4MiB bytes are exact at application; no earned XP, assignment, time or campaign progress is claimed. '
 'Nine complete foreground holds cover909/915/973/979/965, seven menus/returns were viewed and all six observed font calls return fully. Six paired native state/model/persistent/task controls match historical identical inputs. The original fee1000 takes40659 to39659 after the arrangement response. '
 'Frame6400 is the scheme menu, not a second909 hold; the failed verifier assumption is preserved and corrected in2210b without changing ROM, capture or runtime. '
 'Only nine of the106 IDs have new actual visits; the remaining97 have offline evidence. No full-route or hardware claim. '
 'No English, ROM, profile, registry, manifest or patch changes are needed. Three registered editorial stages and all106 IDs are bound in existing V2171 manifest relocations. '
 'The cumulative492batches/114accepted layers and exact clean-input patch remain intact. Fresh coverage1076 reread/1076 integrated-reconciled/0pending. '
 'Historical2143=1498revised+645retained, source/prose2259 and116 incompleteCOMMON remain unchanged. Another1067 historical completions still require this fresh pass, plus all never-reviewed routes/shared town/shop/random/player prose. '
 'The full objective stays active. Separate graphics/all18 plaques, SC3B109 classification and the later older-record technical re-audit remain open. Every ROM and earlier translation is preserved. V1492 stays promoted; canonical and clean inputs are unchanged.')

def key(row):
    path=row.get('file_path','/COMMON/MESFILE.DK4'); n=row.get('message_id')
    return path,f'COMMON_MESSAGE_{n}' if n is not None and path=='/COMMON/MESFILE.DK4' else row['id']

if __name__=='__main__':
    assert not any(p.exists() for p in(ROOT,NOTES,FINAL,GUIDE))
    l,d,matrix,fonts,recruit,bribe,release=[read(p) for p in(LEDGER,DOC,MATRIX,FONTS,RECRUIT,BRIBE,RELEASE)]
    f=l['contextual_story_natural_dialogue_pass_v1871']
    assert(f['fresh_pass_records_explicitly_reread'],f['fresh_pass_records_integrated'],f['fresh_pass_records_pending_native_actual_release'])==(970,970,0)
    assert len(d['records'])==106 and d['revised_IDs']==[] and d['retained_count']==106
    assert matrix['case_count']==56852 and not matrix['findings']
    assert fonts['font_count']==400 and len(fonts['physical_sheets'])==34 and fonts['all400_single_native_pages_complete']
    assert {r['message_ID']for r in fonts['full_font_samples']}==set(range(883,989))
    assert fonts['production_logical_view']==[228,48]and fonts['production_metrics']==[6,12]
    assert len(recruit['actual_holds'])==8 and len(recruit['transition_frames'])==7 and len(recruit['paired_native_state_model_controls'])==8
    assert recruit['no_savestate_or_any_synthetic_fixture'] and recruit['actual_charge']==1573 and recruit['gathered_before_assignment']==34
    assert len(bribe['actual_holds'])==9 and len(bribe['transition_frames'])==7 and len(bribe['paired_native_state_model_task_controls'])==6
    assert bribe['source_cost_and_actual_charge']==1000 and bribe['fixture_replayed_exactly_against_preinteraction_RAM']
    assert bribe['room_assignment_XP_and11days_synthetic_not_earned_progress']and bribe['all_other_4MiB_fixture_bytes_exact']
    for p,h in d['native_context_proofs'].items():assert sha(Path(p).read_bytes())==h
    rompath=Path(l['current_integrated_candidate']['path']);digest=sha(rompath.read_bytes())
    mp=rompath.with_suffix('.manifest.json');manifest=read(mp)
    registry_path=Path('translations/release_stack.json');registry=read(registry_path)
    assert digest==l['current_integrated_candidate']['sha256']==d['current_ROM_sha256']==recruit['candidate_sha256']==bribe['candidate_sha256']==release['candidate_sha256']==manifest['candidate_sha256']
    assert sha(mp.read_bytes())==release['manifest_sha256']and manifest['release_stack_sha256']==sha(registry_path.read_bytes())and all(manifest['checks'].values())
    assert len(manifest['batches'])==492 and len(registry['accepted_layers'])==114 and registry['latest_promoted_build']['profile']=='all-routes-unified-v1492'
    patch=Path(release['patch'])
    assert release['whole_ROM_reconstruction_byte_exact']and sha(patch.read_bytes())==release['patch_sha256']
    assert sha(Path('work/clean.nds').read_bytes())==release['clean_input_sha256']and sha(Path(manifest['base_rom']).read_bytes())==manifest['base_sha256']
    bindings=[]
    for stage,a,b in(('recruitment_editorial',883,908),('tavern_schemes_editorial',908,964),('scheme_followup_editorial',964,989)):
        row=manifest['relocations']['/COMMON/MESFILE.DK4'][stage]
        p=Path(registry['profiles'][manifest['profile']][stage]);c=read(p)
        assert Path(row['release_config'])==p and row['release_config_sha256']==sha(p.read_bytes())
        assert set(row['proof']['changed_records'])=={f'COMMON_MESSAGE_{n}'for n in range(a,b)}
        man=Path(c['manuscript']);assert c['manuscript_sha256']==sha(man.read_bytes())
        bindings.append(dict(stage=stage,config=str(p),config_sha256=sha(p.read_bytes()),manuscript=str(man),manuscript_sha256=sha(man.read_bytes()),IDs=list(range(a,b))))
    rom,clean=NdsImage.open(rompath),NdsImage.open('work/clean.nds')
    arm,common=rom.read_file('/__arm9__.bin'),rom.read_file('/COMMON/MESFILE.DK4')
    entries=current_entries(common,arm)
    jp=common_message_entries(clean.read_file('/COMMON/MESFILE.DK4'),clean.read_file('/__arm9__.bin'))
    assert sha(arm)==d['current_ARM9_sha256']==fonts['ARM9_sha256']==release['ARM9_sha256']
    assert sha(common)==d['current_COMMON_sha256']==fonts['COMMON_sha256']==release['COMMON_sha256']
    assert arm[0x9145c:0x91464].hex()=='1800a0e31eff2fe1'
    history={key(r):g['id']for g in l['completed_editorial_families']for r in g['records']}
    keys={(r['file_path'],r['id'])for r in f['record_keys']}
    selected={('/COMMON/MESFILE.DK4',f'COMMON_MESSAGE_{n}')for n in range(883,989)}
    assert len(history)==2143 and not keys&selected and selected<=set(history)
    docs=[Path('docs')/p for p in('editorial_handoff_current.md','translation_progress.md','editorial_review_goal.md','todo.md','known_issues.md')]
    ROOT.mkdir(parents=True)
    for p in[LEDGER,*docs]:(ROOT/(p.name+'.before')).write_bytes(p.read_bytes())
    notes=deepcopy(d)
    notes.update(status='complete-fresh-contextual-retention-reconciled-registered-V2171',formatting_review_pending=False,English_identical_to_v1_and_current_ROM=True,no_new_ROM_profile_manifest_or_patch=True,final_review=str(FINAL),current_native_layouts=str(MATRIX),current_native_fonts=str(FONTS),representative_actual_ordinary=str(RECRUIT),representative_actual_declared_fixture=str(BRIBE),registered_native_stage_bindings=bindings)
    for r in notes['records']:
        n=r['message_id']
        assert r['source_hex']==jp[n].text.hex()and entries[n].text==b' '+r['english'].removesuffix('{PAD}').encode('ascii')and r['current_hex']==entries[n].text.hex()
        r['review']['formatting']=True
        r.update(status='complete-fresh-whole-exchange-retention-native-display-representative-actual-registered-reconciliation',original_historical_family=history[(r['file_path'],r['id'])],integrated_hex=entries[n].text.hex(),integrated_reference=dict(block=entries[n].block,offset=entries[n].block_offset,copy_end=entries[n].copy_end,bytes=len(entries[n].text)),integrated_stored_English=entries[n].text.decode('cp932'),formatting_gate_scope='56852 native layout/stress cases;400 full native font pages/34 viewed sheets;logical228x48 at6x12;physical16pitch separate.',actual_gameplay_coverage=[])
        for evidence,mode in((recruit,'ordinary-fixture-free-genuine-save'),(bribe,'declared-room-XP-11day-display-fixture;not-earned-progress')):
            for h in evidence['actual_holds']:
                if h['message_ID']==n:
                    r['actual_gameplay_coverage'].append(dict(mode=mode,ROM_sha256=digest,font_frame=h['font_frame'],hold_frame=h['hold_frame'],capture=h['capture'],capture_sha256=h['capture_sha256']))
        r['actual_gameplay_visited']=bool(r['actual_gameplay_coverage'])
        r['native_display_evidence']=dict(layouts=str(MATRIX),fonts=str(FONTS),ordinary_sample=str(RECRUIT),controlled_sample=str(BRIBE),unvisited_conditions_have_offline_evidence_not_actual_visits=True)
    assert sum(r['actual_gameplay_visited']for r in notes['records'])==9
    validate_natural_dialogue_batch(notes);save(NOTES,notes)
    visual=ROOT/'visual_review.json'
    save(visual,dict(all400_native_font_cases_on34_sheets_viewed=True,all106_IDs_and_all12_conditions_for905_906_covered=True,eight_ordinary_recruitment_holds_seven_transitions_viewed=True,nine_controlled_bribe_holds_seven_transitions_viewed=True,complete_leading_trailing_glyphs_punctuation_names_amounts_and_final_lines_visible=True,all56852_layouts_zero_findings_or_waivers=True,supplied_stress_combinations_not_claimed_all_reachable=True,physical16pitch_separate_from_logical12pitch_capacity=True,ordinary_transition='6600/7000more-recruitment;7400AssignSailors shows34unassigned;7800leave34unassigned confirmation;8200Tavern menu;8600/8800town',controlled_transition='6400/6800scheme menu;8800faction list;10400town list;12400Tavern menu;12800/13200town',frame6400_is_menu_not909_hold=True,no_full_route_or_hardware_claim=True,full_goal_complete=False))
    paths=[DOC,NOTES,MATRIX,FONTS,RECRUIT,BRIBE,CONTRACT,RELEASE,mp,registry_path,visual,Path(__file__),Path('work/analysis/tavern_recruitment_schemes_source_v2195/all106_clean_current_context_catalog.json'),Path('work/analysis/recruitment_scheme_prose_v2201/source_first_whole_exchange_review.json'),Path('work/analysis/current_scheme_input_contract_v2199/input_contract.json'),Path('work/analysis/recruitment_scheme_layouts_v2203b/probe_terminator_correction.json'),Path('work/analysis/scheme_bribe_actual_verification_v2210b/hold_scope_correction.json')]
    paths.extend(Path(p)for p in d['native_context_proofs'])
    for actual in(recruit,bribe):
        paths.extend(Path(actual[k])for k in('source_plan','source_report','source_observer','native_continuation'))
        native=read(actual['native_continuation'])
        assert all(c['complete_native_return']and c['SP_preserved']and c['callee_registers_preserved']and not c['faults']and not c['error']for c in native['cases'])
    evidence={str(p):sha(p.read_bytes())for p in paths}
    save(FINAL,dict(format='dk4-editorial-family-final-review-v1',family=FAMILY,file_path='/COMMON/MESFILE.DK4',native_message_IDs=list(range(883,989)),revised_count=0,retained_count=106,historical_reconciliation_only=True,new_completed_records=0,records=notes['records'],summary=SUMMARY,evidence=evidence,registered_native_stage_bindings=bindings,candidate=str(rompath),candidate_sha256=digest,profile=manifest['profile'],patch=str(patch),patch_sha256=release['patch_sha256'],whole_clean_input_reconstruction_exact=True,no_ROM_profile_registry_manifest_patch_changes=True,actual_scope=dict(ordinary_IDs=[890,897,907,904],ordinary_frames=8801,ordinary_holds=8,ordinary_transition_frames=7,ordinary_native_font_continuations=7,ordinary_paired_controls=8,quoted_cost_and_charge=1573,gathered_before_assignment=34,left_unassigned_in_this_sample=True,context1042_71_no_extra_credit=True,controlled_IDs=[909,915,973,979,965],controlled_frames=13200,controlled_holds=9,controlled_transition_frames=7,controlled_native_font_continuations=6,controlled_paired_controls=6,controlled_fee=1000,controlled_room_XP_calendar_fixture_explicit_not_earned_progress=True,other97_records_offline_only=True),offline_scope=dict(current_original_recruitment_schemes_followup_consumer_and_role_voice_tables_bound=True,original_readonly_typed905_906_status_contract=True,original_first_second_faction_filters_clean_exact=True,current_registered_width24=True,older_400_first_8000_second_filter_cases_inherited_not_freshly_rerun=True,nonplayer_fixed_name_domain_not_arbitrary23byte_stress=True,native_layouts=56852,supplied_stress_cases_not_all_reachable=True,style_findings=0,full_native_font_cases=400,sheets_viewed=34,all_single_pages_original228x48_and6x12=True),full_goal_complete=False))
    f['record_keys'].extend(dict(file_path=r['file_path'],id=r['id'])for r in notes['records'])
    f['record_IDs'].extend(r['id']for r in notes['records'])
    f.update(fresh_pass_records_explicitly_reread=1076,fresh_pass_records_integrated=1076,fresh_pass_records_pending_native_actual_release=0,historical_completed_records_outside_reconciled_fresh_pass=1067,latest_contextual_manuscript=str(NOTES),latest_completed_family=FAMILY,latest_reconciled_historical_family=FAMILY,latest_contextual_retention_review=str(FINAL),latest_final_review=str(FINAL),latest_pending_contextual_family=None,coverage_note='1076 file-qualified fresh rereads integrated/reconciled;1067 other historical completions,116 incomplete COMMON and all never-reviewed route/shared town/shop/random/player prose remain in scope.')
    f['reconciled_families'].append(dict(id=FAMILY,records=106,final_review=str(FINAL),new_revisions=0,justified_retentions=106,historical_reconciliation_only=True,new_completed_records=0,all_source_native_representative_actual_registered_reconciliation_complete=True))
    l['active_source_prose_drafts']['note']=f['coverage_note']
    l['recruitment_schemes_contextual_v2211']=dict(summary=SUMMARY,final_review=str(FINAL),evidence=evidence,goal_turn_classification='progress',full_goal_complete=False)
    l['latest_checkpoint']=SUMMARY
    l['current_integrated_candidate']['details']+=' V2211 freshly reconciles106 unchanged recruitment/scheme/follow-up entries; binary and exact patch remain V2171.'
    l['formatting_watchlist']['recruitment_schemes_contextual_v2211']=dict(status='106complete-current-V2171-retentions-original228x48-four12rows',final_review=str(FINAL),all56852_native_layouts_pass=True,all400_font_samples_and34sheets_viewed=True,actual_current_ordinary_IDs=[890,897,907,904],actual_current_declared_fixture_IDs=[909,915,973,979,965],no_runtime_font_or_geometry_changes=True)
    old_width=l.get('scheme_name_width_finding')
    if old_width:
        l['scheme_name_width_historical_status_before_v2211']=deepcopy(old_width)
        old_width.update(status='current-registered-width24-and-reachable-scheme-input-contract-bound;historical-research-retained',current_input_contract=str(CONTRACT),current_final_review=str(FINAL),original_ordinary_selector_closure_inherited_from_v793=True,no_new_GPU_visit_to_every_selector_or_general_custom_name_waiver=True,no_broad_older_record_reaudit_claim=True)
    keys={(r['file_path'],r['id'])for r in f['record_keys']}
    assert len(keys)==len(f['record_keys'])==len(f['record_IDs'])==1076
    assert Counter(p for p,i in keys)=={'/COMMON/MESFILE.DK4':420,'/data/SC2.DK4':428,'/data/SC0.DK4':117,'/data/SC1.DK4':73,'/data/SC3.DK4':38}
    assert l['records_editorially_completed']==2143 and l['records_revised_and_integrated']==1498 and l['retained_wordings_editorially_completed']==645 and sum(l['source_prose_reviewed_counts_by_file'].values())==2259 and len(l['reviewed_but_incomplete_COMMON_IDs'])==116 and l['goal_status']=='active'and not l['full_goal_complete']
    remaining=[dict(file_path=p,id=i,historical_family=g)for(p,i),g in history.items()if(p,i)not in keys]
    assert len(remaining)==1067 and Counter(r['file_path']for r in remaining)=={'/COMMON/MESFILE.DK4':1066,'/data/SC2.DK4':1}
    inv=ROOT/'remaining_historical_fresh_review_inventory.json'
    save(inv,dict(remaining=1067,records=remaining,counts_by_file=dict(Counter(r['file_path']for r in remaining)),counts_by_family=dict(Counter(r['historical_family']for r in remaining)),full_goal_complete=False))
    l['next_remaining_historical_inventory_v2211']=dict(path=str(inv),sha256=sha(inv.read_bytes()),records=1067)
    save(LEDGER,l)
    section='## V2211: Recruitment and schemes106 reconciled in unchanged V2171\n\n'+SUMMARY+'\n\nExact spans and individual reasons: '+FINAL.as_posix()+'. Native layouts: '+MATRIX.as_posix()+'. Full fonts: '+FONTS.as_posix()+'. Ordinary recruitment: '+RECRUIT.as_posix()+'. Declared-fixture Bribe: '+BRIBE.as_posix()+'.\n\nNotes-only v2 completes formatting/integrated/actual references. All original producers and manuscripts remain frozen. The three existing editorial stages are bound through manifest relocations; no duplicate release layer or rebuild is appropriate for identical wording. Old width-research pending status is now reconciled to current registered width24 and the source-filter domain; this is not the later general older-record technical re-audit.\n\nRemaining file-qualified historical fresh-review inventory: '+inv.as_posix()+'. Continue subsequent shared exchanges and every remaining route/random/player-facing record. Separate graphics/all18 plaques and SC3B109 classification stay open. Current parser remains dk4tool.patch.town_trade_port_contextual_reference_v1.current_entries. All jobs terminal. Guide: '+GUIDE.as_posix()+'.\n\n'
    text=docs[0].read_text()
    assert text.startswith('# Current editorial handoff - V2194')
    text=text.replace('# Current editorial handoff - V2194','# Current editorial handoff - V2211',1).replace('- Fresh contextual pass: **970 reread,970 integrated/reconciled,0 pending.** Another1173 historical completions still require fresh contextual reconciliation.','- Fresh contextual pass: **1076 reread,1076 integrated/reconciled,0 pending.** Another1067 historical completions still require fresh contextual reconciliation.',1)
    first,rest=text.split('\n',1);docs[0].write_text(first+'\n\n'+section+rest,newline='\n')
    for p in docs[1:]:
        first,rest=p.read_text().split('\n',1);p.write_text(first+'\n\n'+section+rest,newline='\n')
    GUIDE.mkdir(parents=True)
    images=[(ROOT.parent/'recruitment_actual_verification_v2208/eight_recruitment_holds.png','actual_ordinary_recruitment_holds.png','actual-current-fixture-free-genuine-save'),(ROOT.parent/'recruitment_actual_verification_v2208/seven_recruitment_transitions.png','actual_ordinary_recruitment_transitions.png','actual-current-fixture-free-genuine-save'),(ROOT.parent/'scheme_bribe_actual_verification_v2210b/nine_scheme_bribe_holds.png','actual_declared_fixture_bribe_holds.png','actual-current-declared-room-XP-11day-fixture;not-earned-progress'),(ROOT.parent/'scheme_bribe_actual_verification_v2210b/seven_scheme_bribe_transitions.png','actual_declared_fixture_bribe_transitions.png','actual-current-declared-room-XP-11day-fixture;not-earned-progress')]
    images.extend((Path(r['path']),f'offline_font_sheet_{i:02d}.png','offline-native-font-physical-oracle;not-an-actual-visit')for i,r in enumerate(fonts['physical_sheets']))
    saved=[]
    for source,name,kind in images:
        target=GUIDE/name;copy2(source,target)
        assert sha(target.read_bytes())==sha(source.read_bytes())
        saved.append(dict(path=str(target),sha256=sha(target.read_bytes()),kind=kind))
    assert len(saved)==38
    save(GUIDE/'scope.json',dict(candidate=str(rompath),candidate_sha256=digest,final_review=str(FINAL),images=saved,ordinary_fixture_and_offline_labels_distinct=True,no_new_ROM_or_geometry_change=True,full_goal_complete=False))
    save(ROOT/'completion_receipt.json',dict(checkpoint='V2211',summary=SUMMARY,fresh_reconciliations=106,new_revisions=0,justified_retentions=106,fresh_integrated=1076,historical_complete=2143,source_prose_reviewed=2259,COMMON_incomplete=116,other_historical_fresh_reviews=1067,candidate_sha256=digest,patch_sha256=release['patch_sha256'],guide=str(GUIDE),guide_images=38,evidence=evidence,updated_files={str(p):sha(p.read_bytes())for p in[LEDGER,*docs,NOTES,FINAL]},goal_turn_classification='progress',full_goal_complete=False))
    print(dict(checkpoint='V2211',fresh_integrated=1076,reconciled106=True,revised=0,retained=106,ROM='unchanged-V2171',other_historical_fresh_reviews=1067,full_goal_complete=False))
