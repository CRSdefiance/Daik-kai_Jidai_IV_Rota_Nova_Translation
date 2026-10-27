"""Record V1563 integration,actual inspection evidence and unresolved follow-up text."""
from copy import deepcopy
from pathlib import Path
from shutil import copy2
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/sea_responses_integration_v1570')
RELEASE=Path('work/analysis/sea_responses_release_v1562/registered_release_verification.json')
ACTUAL=Path('work/analysis/sea_inspection_verified_v1568b/original_inspection_complete_pixels_and_transition.json')

if __name__=='__main__':
    assert not ROOT.exists()
    release=read(RELEASE);actual=read(ACTUAL);digest=release['candidate_sha256']
    startup_path=RELEASE.parent/'ordinary_startup_verification.json';shop_path=RELEASE.parent/'photographed_shop_formatting.json'
    startup,shop=read(startup_path),read(shop_path)
    assert all(r['candidate_sha256']==digest for r in [actual,startup,shop])
    assert release['complete_reconstruction_byte_exact'] and release['all8_sea_responses_and3663_unselected_or_retained_texts_preserved']
    assert len(actual['holds'])==4 and len(actual['whole_other_RGB_controls'])==17
    assert actual['normal_response_dismissal_following_ID306_and_final_A_close_return_to_Inspect6300']
    assert actual['entire48_owned_byte_fixture_and_all4MiB_inputs_RAM_PNG_and_unchanged_donors_audited']
    assert startup['all8_complete_startup_title_NewGame_frames_exact'] and startup['no_battery_save_savestate_or_fixtures']
    assert sha(Path(startup['review_sheet']).read_bytes())==startup['review_sheet_sha256']
    ledger_path=Path('translations/editorial_review_current_v1.json');ledger=read(ledger_path);before=deepcopy(ledger)
    assert (ledger['records_editorially_completed'],ledger['records_with_source_and_prose_pass'],len(ledger['reviewed_but_incomplete_COMMON_IDs']))==(1338,1490,152)
    ROOT.mkdir(parents=True);save(ROOT/'coverage_before_checkpoint.json',before)
    visual=ROOT/'startup_actual_response_and_Inspect_visual_review.json'
    save(visual,{'all8_fixture_free_startup_title_NewGame_panels_actually_viewed':True,
        'actual_complete2209_at5830_and_return_to_Inspect6300_actually_viewed':True,
        'actual_source_unidentified_target_No_lookout307_and_following306_wrong_text_observed':True,
        'native8_panel_review':'work/analysis/sea_responses_native_review_v1561/all8_native_panels_visual_review.json',
        'no_family_or_full_goal_completion_claimed':True,'full_goal_complete':False})
    proofs={str(p):sha(p.read_bytes()) for p in [RELEASE,ACTUAL,startup_path,shop_path,visual]}
    ledger['latest_registered_sea_responses_candidate']={**release,'status':'experimental-integrated-native-startup-actual2209-and-Inspect-transition-verified;legacy306_307-followup-open',
        'proofs':proofs,'source_prose_reviews_added':0,'completed_entries_added':0,'full_goal_complete':False}
    unit=next(u for u in ledger['coverage_units'] if u['id']=='Shared-sea-inspection-fear-awe8-source-prose')
    unit.update(status='registered-native-startup-actual2209-verified;following306-and-alternative307-text-correction-pending',
        candidate=release['candidate'],integration_checkpoint=str(ROOT/'integration_receipt.json'))
    watch=ledger['formatting_watchlist']['sea_inspection_fear_awe8']
    watch.update(false_war_reference_2209_prose_corrected_not_yet_integrated=False,registered_release_and_original_inspection_pending=False,
        registered_candidate=release['candidate'],actual_inspection_ID2209_and_complete_letters_verified=True,
        original_scene_followup_text_gate_open=True,legacy_modal_IDs_to_correct=[306,307],actual_proof=str(ACTUAL),
        native_font_family_verified_but_editorial_completion_pending=True)
    ledger['formatting_watchlist']['latest_reference_proof']=str(shop_path)
    ledger['formatting_watchlist']['latest_photographed_shop_recheck']={'checkpoint':'V1570','candidate':release['candidate'],'candidate_sha256':digest,
        'proof':str(shop_path),'result':'676/677 exact repaired bytes,original native wrapping and full font planes pass;no fresh shop visit.','global_formatting_audit_complete':False}
    ledger['active_source_prose_drafts']['note']='V1563 integrates sea8(5 revised3 retained);all8 native fonts and original2209 display/normal transition pass. Following306 and alternative307 are confirmed wrong old text,so sea8 completion remains pending their correction. Other144 reviewed COMMON plus broader shared/routes/raw prose and separate graphics remain open.'
    counts='1338 complete(1000 revised338 retained),1490 source/prose reviewed,152 reviewed-incomplete COMMON(8 sea inspection32 reactions24 loss/surrender16 sinking34 aftermath38 older),plus broader shared/routes/raw prose.'
    summary=('V1570 verifies registered V1563 sea inspection8 integration:5 revised3 retained,without completion credit. Full471 batches114 accepted layers and exact clean-input patch pass. Only COMMON23/native metadata/existing188-byte selector change versus V1542;3663 other or retained copies,40 blocks,172-byte gate,123040 staged bytes,all earlier routes/graphics/fonts/helpers preserved. All8 ordinary startup/title/NewGame frames match V1105 and are viewed;shop676/677 preserved. Original creature registration plus target location and existing Charles18 move from station9 to empty lookout3 form one48-owned-byte prebattle fixture. One original RNG initialization is executed naturally,not forced;own five ships,actor objects and all unowned4MiB bytes are exact. Charles18/voice0/role7/2209 has4 full native/independent/reference/actual RGB holds;17 other whole screens exact to V1542. Normal response close,following306 close and return to Info Mode/Inspect6300 are verified. Old306/307 are unrelated split trade-good text;307 is observed in the no-lookout pilot and306 follows the creature reaction. Correct both before closing this family;308 is an additional fatigue-context lead. The original role7 getter can select a fallback actor and does not prove the station is occupied;original8205C/705F8 identify the actual empty lookout. Failed activation hypotheses and wrapper/auditor assumptions are retained with explicit successors. V1568s sailing-interface label is corrected by1568b:6300 is Info Mode over the sea. '+counts+' V1563 experimental,V1492 promoted,V1542 completed-native reference;canonical/V997 unchanged. Separate graphics/all18 plaques and later older-record re-audit remain open;goal active.')
    ledger['latest_checkpoint']=summary
    ledger['research_checkpoints'].append({'id':'V1570-sea8-integrated-original-inspection-and-followup-defects','proof':str(ROOT/'integration_receipt.json'),
        'candidate':release['candidate'],'source_prose_reviews_added':0,'completed_entries_added':0,'full_goal_complete':False})
    for key in ['records_editorially_completed','records_revised_and_integrated','retained_wordings_editorially_completed','records_with_source_and_prose_pass',
        'reviewed_but_incomplete_COMMON_IDs','completed_editorial_record_counts_by_file','current_integrated_candidate','current_native_relocation_reference',
        'source_pins','unresolved_graphics_work','older_record_reaudit_after_full_editorial_goal','raw_source_coverage_revisit']:
        assert ledger[key]==before[key],key
    save(ledger_path,ledger)
    pins_path=Path('translations/rom_retention_pins.json');pins=read(pins_path)
    pin='E:/Rota Nova translations/Generated/out/all_routes_combined_v1563_candidate.nds'
    assert not any(r['path']==pin for r in pins)
    pins.append({'path':pin,'reason':'Registered sea8 integration and actual2209 verified;needed for correction of following306 and alternative307 before family completion.'});save(pins_path,pins)
    guide=Path('E:/Rota Nova translations/Guide screenshots/V1563 sea creature inspection');assert not guide.exists();guide.mkdir(parents=True)
    screenshots=[]
    cap=Path('E:/Rota Nova translations/Generated/work/emulation_v193/sea_inspection_final_v1567d_1563')
    for frame,label in [(5830,'Charles_complete_creature_response'),(6300,'Inspect_Monster_Fish')]:
        src=cap/f'frame_{frame:06d}_navigation.png';dst=guide/(label+'.png');copy2(src,dst)
        assert sha(src.read_bytes())==sha(dst.read_bytes());screenshots.append({'source':str(src),'guide':str(dst),'sha256':sha(src.read_bytes())})
    save(guide/'provenance.json',{'candidate':release['candidate'],'candidate_sha256':digest,'proof':str(ACTUAL),'screenshots':screenshots,
        'artificial_existing_creature_registration_location_and_lookout_assignment_fixture':True,
        'one_original_RNG_initialization_not_forced':True,'not_earned_travel_discovery_or_acquisition':True,
        'legacy306_307_followup_text_not_approved':True,'full_goal_complete':False})
    doc=Path('docs/sea_responses_v1570_integration_checkpoint.md');assert not doc.exists()
    doc.write_text('# V1570 sea inspection integration checkpoint\n\n'+summary+'\n\n## Experimental combined build\n\n'
        '- Candidate: `E:/Rota Nova translations/Generated/out/all_routes_combined_v1563_candidate.nds`; SHA-256 `'+digest+'`.\n'
        '- Canonical construction base: `'+release['canonical_base']+'`; SHA-256 `'+release['canonical_sha256']+'`.\n'
        '- Profile: `all-routes-unified-v1563`;471 batches114 accepted layers. V1492 stays promoted.\n'
        '- Changed files versus V1542: `/COMMON/MESFILE.DK4` and `/__arm9__.bin`;COMMON23/native metadata/existing selector only.\n'
        '- Exact patch: `'+release['patch']+'`; SHA-256 `'+release['patch_sha256']+'`;clean input `'+release['clean_input_sha256']+'`.\n'
        '- Checks: native1557/fonts1558/copies1559/escape1560/visual1561/release1564b/startup1565b/actual1568b/shop1569.\n\n'
        '## Next work\n\nSource/context-review and correct306/307 through a separate registered natural-dialogue-v2 stage. Recheck their complete literal glyphs and actual no-lookout/creature-followup paths,normal close and return to Inspect. The actual creature response and source-loaded model are proven;do not repeat inactive-fleet or missing-renderer hypotheses. Character identities,health,combat outcomes and message selectors were not forced. Source306 means information cannot be viewed;307 means no lookout is assigned.308 requires a separate fatigue consumer review. Keep the8 sea entries pending until their scene is corrected.\n',encoding='utf-8')
    for name in ['translation_progress.md','known_issues.md','todo.md','editorial_review_goal.md']:
        with (Path('docs')/name).open('a',encoding='utf-8',newline='\n') as f:f.write('\n\n## V1570 sea inspection8 integration and follow-up findings\n\n'+summary+'\n\nSee [checkpoint](sea_responses_v1570_integration_checkpoint.md).\n')
    handoff=Path('docs/editorial_handoff_current.md')
    handoff.write_text('# Current editorial handoff - 2026-10-22\n\n'+summary+'\n\n'
        'Read AGENTS.md,build_continuity_protocol.md,release_stack.json,relevant known_issues.md,natural_dialogue_workflow.md and dialogue_delegation_protocol.md before edits. Sources are read-only;executed producers/manuscripts/proofs stay frozen and receive explicit successors. Use registered builder,not a direct clean-ROM release. No subagents authorized.\n\n'
        '## Authoritative current evidence\n\n'
        '- Ledger: translations/editorial_review_current_v1.json.\n'
        '- Latest integration: work/analysis/sea_responses_integration_v1570/integration_receipt.json.\n'
        '- Exact release: work/analysis/sea_responses_release_v1562/registered_release_verification.json.\n'
        '- Actual display/transition: work/analysis/sea_inspection_verified_v1568b/original_inspection_complete_pixels_and_transition.json.\n'
        '- Old modal source lead: work/analysis/sea_registration_pilot_verified_v1552j/source_unidentified_target_and_old_modal_defects.json.\n'
        '- Sea approved manuscript: translations/sea_responses_editorial_manuscript_v2.json.\n'
        '- Current combined parser: dk4tool.patch.sea_responses_editorial.current_entries;do not use older completed-native reference parser on V1563.\n'
        '- All current jobs terminal;no active emulator handle or pending journal input remains.\n\n'
        '## Continue\n\nCorrect306/307 from clean Japanese and mapped original546B8 consumers,verify native full glyphs/bounds/actual paths,and layer after full V1563. Preserve substitutions/control types;no generic parser hacks. Only then close sea8 if complete. Broader full editorial goal and separate graphics remain open. Source308 fatigue suffix also needs context. Keep older record-based re-audit for after full editorial goal.\n\n'
        'Python: C:/Python314/python.exe;set PYTHONUTF8=1 and PYTHONPATH=.;.deps. Normal launcher may fail P drive authentication;task-specific escalation has worked. out/work-analysis are E-drive junctions;archive lexical paths without resolve(). Builder stdout is a huge manifest:redirect logs and print bounded tails. All generated ROMs/guide captures stay under E:/Rota Nova translations. Retention preview only;no deletions. Keep selector188/gate172/staged123040 fixed,all existing fonts/routes/graphics and promotion exact.\n',encoding='utf-8')
    save(ROOT/'integration_receipt.json',{'candidate':release['candidate'],'candidate_sha256':digest,'proofs':proofs,'guide':str(guide),
        'completed':1338,'source_prose':1490,'reviewed_incomplete_COMMON':152,'completed_entries_added':0,'source_prose_reviews_added':0,
        'following306_alternative307_and_separate308_context_still_open':True,'all_current_runs_terminal':True,
        'producer_sha256':sha(Path(__file__).read_bytes()),'full_goal_complete':False})
    print('V1563 registered/patch/startup/actual2209/Inspect transition recorded;1338 complete,1490 source-prose,152 pending.306/307 next;goal active.')
