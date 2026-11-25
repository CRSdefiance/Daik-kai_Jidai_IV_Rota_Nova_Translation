"""Close only308/309 after original increase/recovery and native/release gates."""
from copy import deepcopy
from dataclasses import asdict
from pathlib import Path
from shutil import copy2
from dk4tool.rom.nds import NdsImage
from dk4tool.script.common_message_table import common_message_entries
from dk4tool.patch.fatigue_status_editorial import current_entries
from dk4tool.patch.grand_race_menu_release import sha
from scripts.fatigue_status_native_plan_v1589 import compiled
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/fatigue_status_completion_v1609')
FINAL=Path('translations/fatigue_status_final_review_v1.json')
GUIDE=Path('E:/Rota Nova translations/Guide screenshots/V1594 fatigue recovery verified')
RELEASE=Path('work/analysis/fatigue_status_release_v1593/registered_release_verification.json')
INCREASE=Path('work/analysis/fatigue_increase_verified_v1598/fixture_free_Search_failure_original_plus3_verified.json')
RECOVERY=Path('work/analysis/fatigue_recovery_verified_v1608/original_friendly_village_recovery10_verified.json')
STACK=Path('work/analysis/fatigue_search_stack_v1601/actual_Search_region3_swamp_callstack_proof.json')

if __name__=='__main__':
    assert not ROOT.exists() and not FINAL.exists() and not GUIDE.exists()
    release,increase,recovery,stack=[read(p) for p in [RELEASE,INCREASE,RECOVERY,STACK]]
    rom_path=Path(release['candidate']);digest=sha(rom_path.read_bytes())
    assert digest==release['candidate_sha256']==increase['candidate_sha256']==recovery['candidate_sha256']==stack['candidate_sha256']
    assert release['complete_reconstruction_byte_exact'] and release['all471_batches114_accepted_layers_and_prior_profiles_preserved']
    assert release['all2_fatigue_statuses_and3666_unselected_texts_preserved'] and release['only_COMMON4_and_original_native_metadata_changed']
    assert release['actual_changed_message_IDs']==[308,309]
    assert sha(Path(release['patch']).read_bytes())==release['patch_sha256']
    assert increase['revised308_full_F_amount_period_and_source_shadow_RGB_verified'] and increase['no_fixture_or_RNG_state_event_or_message_injection']
    assert recovery['actual_original_friendly_village_success_and_signed_helper_minus10_observed'] and recovery['recovery6080_and_normal_Sea_View6200_actually_viewed']
    assert recovery['no_health_fatigue_RNG_actor_or_event_result_writes'] and recovery['preservation_audit']['all48_coordinate_byte_changes_and_other4MiB_bytes_audited']
    startup_path=RELEASE.parent/'ordinary_startup_verification.json';shop_path=RELEASE.parent/'photographed_shop_formatting.json'
    startup,shop=read(startup_path),read(shop_path)
    assert startup['candidate_sha256']==shop['candidate_sha256']==digest
    assert startup['all8_complete_startup_title_NewGame_frames_exact'] and startup['no_battery_save_savestate_or_fixtures']
    assert all(r['no_authored_indent_internal_gap_or_stray_Discover'] for r in shop['entries'])
    manuscript=Path('translations/fatigue_status_editorial_manuscript_v2.json');doc=read(manuscript)
    fonts_path=Path(doc['native_font_proof']);fonts=read(fonts_path)
    assert len(fonts['cases'])==202 and len(fonts['invalid_compiler_inputs_rejected'])==15 and fonts['source_actual_amount_cases']==5
    assert fonts['zero_helper_skips_status_and_preserves_all4MiB']
    rom=NdsImage.open(rom_path);arm,common=rom.read_file('/__arm9__.bin'),rom.read_file('/COMMON/MESFILE.DK4')
    assert sha(arm)==fonts['ARM9_sha256']==release['ARM9_sha256'] and sha(common)==fonts['COMMON_sha256']==release['COMMON_sha256']
    entries=current_entries(common,arm);clean=NdsImage.open('work/clean.nds');jp=common_message_entries(clean.read_file('/COMMON/MESFILE.DK4'),clean.read_file('/__arm9__.bin'))
    ledger_path=Path('translations/editorial_review_current_v1.json');ledger=read(ledger_path);before=deepcopy(ledger)
    assert (ledger['records_editorially_completed'],ledger['records_with_source_and_prose_pass'],len(ledger['reviewed_but_incomplete_COMMON_IDs']))==(1348,1494,146)
    assert not any({308,309}&set(f.get('native_message_IDs',[])) for f in ledger['completed_editorial_families'])
    rows=[]
    for record in doc['records']:
        row=deepcopy(record);n=row['message_id'];assert n in [308,309] and row['source_hex']==jp[n].text.hex() and all(row['review'].values())
        assert entries[n].text==compiled(row)
        proof=increase if n==308 else recovery;holds=proof['holds'];assert len(holds)==2
        assert all(h['full_native_independent_actual_ink_and_shadow_RGB_equal'] for h in holds)
        row.update(manuscript=str(manuscript),previous_current_text_hex=row['current_text_hex'],
            current_reference={k:v for k,v in asdict(entries[n]).items() if k!='text'},current_text_hex=entries[n].text.hex(),current_English=row['english'],
            decision='revised-and-integrated',status='complete-source-native-and-original-gameplay',completed_candidate_reference=str(rom_path),completed_candidate_sha256=digest,
            complete_native_font_proof=str(fonts_path),complete_native_font_proof_sha256=sha(fonts_path.read_bytes()),actual_holds=holds,
            actual_proof=str(INCREASE if n==308 else RECOVERY),
            actual_scope='308 +3 fixture-free Search failure;309 -10 original friendly-village success with isolated location only. Other source amounts5/15 have native numeric and representative-family coverage,not individual actual activation.')
        rows.append(row)
    ROOT.mkdir(parents=True);save(ROOT/'coverage_before_completion.json',before)
    scope=('Both fatigue templates308/309 are source-faithful natural English,with one original%s and complete F,full-width amounts and final period. '
        'Original308+3 was fixture-free Search failure,6 to9. Original309-10 was a normal successful friendly-village Search,6 to0 through the original clamp. '
        'The displayed10 is the requested reduction,not a measured post-clamp difference. Two stable full native/independent/actual palette ink-and-shadow holds pass for each message. '
        'Normal A returns to Sea View5900/6200,both viewed.309 uses only declared48-byte own-fleet/mobile location fixtures;all other4MiB,actor identities,health,fatigue,RNG,event choices,inputs and saves are audited. '
        '202 numeric/font cases include all five original amount cases;5/15 are not individually activated in gameplay.7336 native copies180 cache sequences,15 compiler negatives,exact clean-input patch,all8 startup controls and shop676/677 preservation pass. '
        'The two earlier beast holds are proven region3 swamp793FC by saved region3 and speech LR79430;no region/formatter/game fix was needed. '
        'This closes only308/309. Remaining144 reviewed COMMON and broader shared/routes/raw prose,separate graphics/all18 plaques and later older-record checks remain open. '
        'V1594 remains experimental,V1492 promoted;the later optional screenshot-text-repairs-20261022 profile remains preserved and separately unverified in its changed scenes. No full route or hardware claim.')
    proofs={str(p):sha(p.read_bytes()) for p in [RELEASE,INCREASE,RECOVERY,STACK,startup_path,shop_path,fonts_path,manuscript]}
    save(FINAL,{'format':'dk4-editorial-family-final-review-v1','native_message_IDs':[308,309],'records':rows,'manuscript':str(manuscript),
        'candidate':str(rom_path),'candidate_sha256':digest,'proofs':proofs,'actual_verification_scope':scope,
        'completed_entries':2,'revised':2,'retained':0,'full_goal_complete':False})
    family='Shared-fatigue-status2'
    ledger['completed_editorial_families'].append({'id':family,'native_message_IDs':[308,309],'records':rows,'final_review':str(FINAL),
        'documentation':'docs/fatigue_status_v1609_completion.md','actual_verification_scope':scope})
    unit=next(u for u in ledger['coverage_units'] if u['id']=='Shared-fatigue-status2-source-prose');unit.update(status='superseded-by-complete-family',completed_family=family,final_review=str(FINAL))
    ledger['coverage_units'].append({'id':family,'status':'complete-source-native-and-original-gameplay-scope-documented','native_message_IDs':[308,309],
        'final_review':str(FINAL),'actual_proofs':[str(INCREASE),str(RECOVERY)],'full_goal_complete':False})
    ledger['records_editorially_completed']+=2;ledger['records_revised_and_integrated']+=2;ledger['completed_editorial_record_counts_by_file']['/COMMON/MESFILE.DK4']+=2
    ledger['reviewed_but_incomplete_COMMON_IDs']=[n for n in ledger['reviewed_but_incomplete_COMMON_IDs'] if n not in [308,309]]
    drafts=ledger['active_source_prose_drafts'];drafts['native_message_IDs']=[n for n in drafts['native_message_IDs'] if n not in [308,309]]
    for key in drafts['manuscript_record_subsets_pending']:
        if 'fatigue_status_editorial_manuscript' in key:drafts['manuscript_record_subsets_pending'][key]=[]
    drafts.update(status='earlier144-reviewed-COMMON-and-broader-prose-open',note='Fatigue308/309 complete-source-native-original-gameplay. Earlier144 reviewed COMMON and broader shared/routes/raw prose still open.')
    ledger['current_native_relocation_reference'].update(candidate=str(rom_path),candidate_sha256=digest,COMMON_sha256=release['COMMON_sha256'],ARM9_sha256=release['ARM9_sha256'],
        parser='dk4tool.patch.fatigue_status_editorial.current_entries',release_config='translations/fatigue_status_editorial_release_v1.json',fatigue_status2_complete=True)
    ledger['latest_registered_fatigue_status_candidate']={**release,'status':'experimental-source-native-and-original-gameplay-scope-complete','final_review':str(FINAL),'actual_proofs':[str(INCREASE),str(RECOVERY)],'full_goal_complete':False}
    ledger['formatting_watchlist']['fatigue_status2'].update(status='completed-in-V1594',final_review=str(FINAL),
        native_font_release_and_original_increase_recovery_pending=False,original309_recovery_pending=False,
        actual_recovery_proof=str(RECOVERY),original309_live_minus10_complete_F_digits_period_ink_shadow_and_return_verified=True,callstack_erratum=str(STACK))
    defect=ledger['newly_observed_sea_inspection_modal_defects'];defect.update(status='306307308-corrected-and-complete;global-audit-open',
        resolved_IDs=sorted(set(defect.get('resolved_IDs',[]))|{308}),open_IDs=[n for n in defect.get('open_IDs',[]) if n!=308])
    summary=('V1609 closes fatigue308/309 in registered V1594:1350 complete(1009 revised341 retained),1494 source/prose reviewed,144 reviewed-incomplete COMMON plus broader prose. '+scope)
    ledger['latest_checkpoint']=summary;ledger['research_checkpoints'].append({'id':'V1609-fatigue2-complete','proof':str(ROOT/'completion_receipt.json'),
        'final_review':str(FINAL),'completed_entries_added':2,'source_prose_reviews_added':0,'full_goal_complete':False})
    complete=[n for f in ledger['completed_editorial_families'] for n in f.get('native_message_IDs',[])];pending=ledger['reviewed_but_incomplete_COMMON_IDs']
    assert len(complete)==len(set(complete))==1349 and len(pending)==len(set(pending))==len(drafts['native_message_IDs'])==144
    assert not set(complete)&set(pending) and len(set(complete)|set(pending))==1493
    assert ledger['records_editorially_completed']==ledger['records_revised_and_integrated']+ledger['retained_wordings_editorially_completed']==1350
    assert sum(ledger['completed_editorial_record_counts_by_file'].values())==1350
    for k in ['records_with_source_and_prose_pass','records_with_source_prose_drafts','source_prose_reviewed_counts_by_file','current_integrated_candidate',
        'source_pins','unresolved_graphics_work','older_record_reaudit_after_full_editorial_goal','raw_source_coverage_revisit']:assert ledger[k]==before[k],k
    save(ledger_path,ledger)
    GUIDE.mkdir(parents=True);screenshots=[]
    for frame,label in [(5900,'Original_friendly_village_dialogue'),(6080,'Fatigue_decreased_by10'),(6200,'Sea_View_after_normal_close')]:
        source=Path('E:/Rota Nova translations/Generated/work/emulation_v193/fatigue_recovery_live_v1606_1594')/f'frame_{frame:06d}_navigation.png';target=GUIDE/(label+'.png')
        copy2(source,target);assert sha(source.read_bytes())==sha(target.read_bytes());screenshots.append({'source':str(source),'guide':str(target),'sha256':sha(target.read_bytes())})
    save(GUIDE/'provenance.json',{'candidate_sha256':digest,'actual_proof':str(RECOVERY),'screenshots':screenshots,
        'artificial_location_only_original_Search_event_RNG_and_outcome':True,'not_earned_travel_or_full_playthrough':True,'full_goal_complete':False})
    document=Path('docs/fatigue_status_v1609_completion.md');assert not document.exists()
    document.write_text('# V1609 fatigue status2 complete\n\n'+summary+'\n\n## Exact experimental release\n\n'
        '- Candidate: `'+str(rom_path)+'`; SHA-256 `'+digest+'`.\n'
        '- Construction base: `'+release['canonical_base']+'`; SHA-256 `'+release['canonical_sha256']+'`.\n'
        '- Profile: `all-routes-unified-v1594`;471 batches114 accepted layers. V1492 remains promoted.\n'
        '- Changed files versus V1578: `/COMMON/MESFILE.DK4`, `/__arm9__.bin`;COMMON4/original metadata only. All native code/selector188/gate172/staged123040 unchanged.\n'
        '- Patch: `'+release['patch']+'`; SHA-256 `'+release['patch_sha256']+'`;clean input `'+release['clean_input_sha256']+'`.\n\n'
        '## Scope and follow-up\n\nBoth IDs are individually observed. Other source amounts5/15 have native numeric/family coverage. Full source,proof and current-build references are in `translations/fatigue_status_final_review_v1.json`. '
        'The later screenshot repair profile remains experimental,with Alexandria/rumor/nameplate scenes pending. Future releases must preserve it while validating its changed scenes. '
        'Earlier144 pending COMMON records and all remaining route/prose coverage require further work. Graphics/all18 plaque audit remains separate.\n',encoding='utf-8')
    for name in ['translation_progress.md','known_issues.md','todo.md','editorial_review_goal.md']:
        with (Path('docs')/name).open('a',encoding='utf-8') as f:f.write('\n\n## V1609 fatigue2 complete\n\n'+summary+'\n\nSee [completion](fatigue_status_v1609_completion.md).\n')
    Path('docs/editorial_handoff_current.md').write_text('# Current editorial handoff - V1609\n\n'+summary+'\n\n'
        'Read required AGENTS/build continuity/natural dialogue/delegation/known issues and release_stack documents. Sources read-only;executed producers and evidence get successors. No subagents authorized. All current jobs terminal.\n\n'
        '## Current evidence\n\n- Ledger: translations/editorial_review_current_v1.json.\n- Completion: work/analysis/fatigue_status_completion_v1609/completion_receipt.json.\n'
        '- Final review: translations/fatigue_status_final_review_v1.json.\n- Parser: dk4tool.patch.fatigue_status_editorial.current_entries;completed native parent V1594.\n'
        '- Source original recovery: work/analysis/fatigue_recovery_verified_v1608/original_friendly_village_recovery10_verified.json.\n'
        '- Region callstack correction: work/analysis/fatigue_search_stack_v1601/actual_Search_region3_swamp_callstack_proof.json.\n'
        '- New later optional profile: screenshot-text-repairs-20261022,documented docs/screenshot_text_repairs_20261022.md;do not overwrite or omit those changes in a successor. It has no published exact patch and changed scenes remain unverified.\n\n'
        '## Continue\n\nProceed with the earlier144 pending COMMON scene gates or unreviewed shared/route prose. Do not redo completed fatigue testing without a concrete risk. '
        'The old region3 beast-dialogue discrepancy is resolved:the source callback was swamp793FC,not beast79224. No engine/formatter correction is indicated. '
        'Keep global goal active,graphics/all18 plaques unfinished,and older-record checks queued. Preserve approved Rafael/Joakim/Maria/Camille.\n\n'
        'Use Python C:/Python314/python.exe,PYTHONUTF8=1,PYTHONPATH=.;.deps. Task-specific escalations work around P-drive launcher errors. out/work-analysis are E-drive junctions;archive lexical paths without resolve(). '
        'E:/Rota Nova translations holds ROMs/screenshots. Retention preview only;no ROM deletions. Selector188/gate172/staged123040 and immutable construction baseline preserved;V1492 remains promoted.\n',encoding='utf-8')
    save(ROOT/'completion_receipt.json',{'candidate':str(rom_path),'candidate_sha256':digest,'completed':1350,'revised':1009,'retained':341,'source_prose':1494,
        'newly_completed':2,'unique_complete_COMMON':1349,'reviewed_incomplete_COMMON':144,'final_review':str(FINAL),'proofs':proofs,
        'guide':str(GUIDE),'screenshots':screenshots,'V1492_promoted_canonical_and_V997_preserved':True,'later_screenshot_repair_profile_preserved':True,
        'producer_sha256':sha(Path(__file__).read_bytes()),'full_goal_complete':False})
    print('Fatigue308/309 complete:1350 total(1009 revised341 retained),1494 source/prose reviewed,144 pending COMMON plus broader prose;graphics separate,full goal active.')
