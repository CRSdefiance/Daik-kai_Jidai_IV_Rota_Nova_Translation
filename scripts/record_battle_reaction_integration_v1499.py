"""Record V1492 integration and prior-event controls;new32 scenes remain open."""
from copy import deepcopy
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/battle_reaction_integration_v1499')
RELEASE=Path('work/analysis/battle_reaction_release_v1491/registered_release_verification.json')

if __name__=='__main__':
    assert not ROOT.exists()
    release=read(RELEASE);digest=release['candidate_sha256']
    startup_path=RELEASE.parent/'ordinary_startup_verification.json';shop_path=RELEASE.parent/'photographed_shop_formatting.json'
    control_path=Path('work/analysis/battle_reaction_control_verified_v1498/actual_capture_and_return_verification.json')
    startup,shop,control=[read(p) for p in [startup_path,shop_path,control_path]]
    assert sha(Path(release['candidate']).read_bytes())==digest
    assert sha(Path(release['patch']).read_bytes())==release['patch_sha256']
    assert all(p['candidate_sha256']==digest for p in [startup,shop,control])
    assert release['complete_reconstruction_byte_exact'] and release['all471_batches114_accepted_layers_and_prior_profiles_preserved']
    assert release['all32_reaction_paragraphs_and3652_unselected_or_retained_texts_preserved']
    assert startup['all8_complete_startup_title_NewGame_frames_exact'] and startup['no_battery_save_savestate_or_fixtures']
    assert sha(Path(startup['review_sheet']).read_bytes())==startup['review_sheet_sha256']
    assert control['entire4MiB_fixture_input_primary_RAM_and_PNG_hash_audits_pass']
    assert control['later10_whole_reward_cargo_and_sailing_screens_exact_to_V1456']
    assert control['normal_capture_A_dismissal_flagship_victory_rewards_X_cargo_finish_touch_Yes_and_return_to_sailing']
    assert control['source_and_disposable_saves_unchanged'] and control['no_sinking_or_other_unreviewed_family_completion_credit']
    ledger_path=Path('translations/editorial_review_current_v1.json');ledger=read(ledger_path);before=deepcopy(ledger)
    assert (ledger['records_editorially_completed'],ledger['records_with_source_and_prose_pass'],len(ledger['reviewed_but_incomplete_COMMON_IDs']))==(1323,1467,144)
    ROOT.mkdir(parents=True);save(ROOT/'coverage_before_integration_checkpoint.json',before)
    visual=ROOT/'startup_and_prior_capture_visual_review.json'
    save(visual,{'startup_sheet':startup['review_sheet'],'startup_sheet_sha256':startup['review_sheet_sha256'],
        'all8_startup_panels_visually_reviewed':True,'actual_capture10750_and_sailing13200_visually_reviewed':True,
        'scope':'Ordinary startup and the earlier original2082 capture control;no new32 reaction event observed in sampled holds.',
        'full_goal_complete':False})
    proofs={str(p):sha(p.read_bytes()) for p in [RELEASE,startup_path,shop_path,control_path,visual]}
    ledger['latest_registered_battle_reaction_candidate']={**release,
        'status':'experimental-integrated-native-startup-and-prior-capture-control-verified;original32-reaction-scenes-pending',
        'proofs':proofs,'ordinary_startup_pending':False,'new_reaction_original_scenes_pending':True,
        'completed_entries_added':0,'full_goal_complete':False}
    unit=next(u for u in ledger['coverage_units'] if u['id']=='Shared-battle-reactions32-source-prose')
    unit.update(status='registered-integrated-native-startup-approved;original-scenes-pending',candidate=release['candidate'],integration_checkpoint=str(ROOT/'integration_receipt.json'))
    ledger['formatting_watchlist']['battle_reactions32'].update(registered_release_and_original_scene_gates_open=False,
        registered_release_pending=False,original_scene_gates_open=True,registered_candidate=release['candidate'],
        integration_proof=str(RELEASE),startup_visual_review=str(visual),prior_capture_control_proof=str(control_path))
    watch=ledger['formatting_watchlist']
    watch['latest_reference_proof']=str(shop_path)
    watch['latest_photographed_shop_recheck']={'checkpoint':'V1499','candidate':release['candidate'],'candidate_sha256':digest,
        'proof':str(shop_path),'result':'Repaired676/677 exact bytes,native wrapping and full font planes pass;no fresh shop visit claimed.',
        'global_formatting_audit_complete':False}
    watch['latest_user_screenshot_recheck']={'proof':str(shop_path),'candidate':release['candidate'],
        'exact_repaired676_677_bytes_preserved':True,'complete_native_wrapping_and_glyph_planes_rechecked':True,
        'new_actual_shop_activation_claimed':False,'global_formatting_audit_complete':False}
    ledger['active_source_prose_drafts']['note']='V1492 integrates32 source/native-approved reactions plus all V1456 layers,including24 pending loss/surrender reports. Original reaction/loss/surrender scenes remain pending.16 sinking,34 aftermath38 older and broader shared/routes/raw prose remain open.'
    summary=('V1499 records registered V1492 integration of32 source/native-approved battle reactions:16 revised16 retained, '
        'without completion credit. Full471-batch/114-accepted-layer stack and exact clean-input patch reconstruction pass. '
        'Only COMMON23,original native ARM9 offset/directory metadata and the existing188-byte selector span change versus '
        'V1456;the172-byte gate,all3652 other/retained text-copy spans,40 other blocks,routes,graphics,fonts,opaque duel '
        'prefix,earlier helpers,sections/BSS/cache/arena/ITCM and123040 staged bytes are preserved. All8 ordinary startup '
        'controls match V1105 and are visually reviewed;repaired shop676/677 native wrapping/full glyph planes pass '
        'without a fresh shop activation claim. Original previous2082 capture has two complete native/independent/'
        'reference/RGB holds10750/10780 and normal dismissal,flagship,victory,rewards,cargo confirmation and return '
        'to sailing13200/mode000/cleared enemy parties;all10 later whole screens match V1456. The sole40-byte '
        'prebattle own-location fixture,all4MiB,input,RAM,PNG and unchanged source/disposable saves are audited. '
        'Actual capture10750 and sailing13200 are visually reviewed. No new32 reaction buffer lead appears in sampled '
        'holds;the control does not complete setup,surprise or injury families. Counts1323 complete(985 revised338 '
        'retained),1467 source/prose,144 reviewed-incomplete COMMON(32 reactions24 loss/surrender16 sinking34 aftermath'
        '38 older),plus broader shared/routes/raw prose. V1492 is latest registered experimental integration;V1430 '
        'remains completed-native relocation reference. Canonical,V997,separate graphics/all18 plaques and later '
        'older-record re-audit remain unchanged/open;goal active.')
    ledger['latest_checkpoint']=summary
    ledger['research_checkpoints'].append({'id':'V1499-battle-reactions32-registered-integration','proof':str(ROOT/'integration_receipt.json'),
        'candidate':release['candidate'],'completed_entries_added':0,'source_prose_reviews_added':0,'full_goal_complete':False})
    for key in ['records_editorially_completed','records_revised_and_integrated','retained_wordings_editorially_completed',
        'records_with_source_and_prose_pass','reviewed_but_incomplete_COMMON_IDs','completed_editorial_record_counts_by_file',
        'current_integrated_candidate','current_native_relocation_reference','source_pins','unresolved_graphics_work',
        'older_record_reaudit_after_full_editorial_goal','raw_source_coverage_revisit']:
        assert ledger[key]==before[key],key
    save(ledger_path,ledger)
    pins_path=Path('translations/rom_retention_pins.json');pins=read(pins_path)
    pin='E:/Rota Nova translations/Generated/out/all_routes_combined_v1492_candidate.nds'
    assert not any(r['path']==pin for r in pins)
    pins.append({'path':pin,'reason':'Registered native/startup/prior-event-control verified reaction32 integration;original new reaction scene verification remains open.'});save(pins_path,pins)
    document=Path('docs/battle_reactions_v1499_integration_checkpoint.md');assert not document.exists()
    document.write_text('# V1499 battle reaction integration checkpoint\n\n'+summary+'\n\n'
        '## Experimental combined release\n\n'
        '- Candidate: `E:/Rota Nova translations/Generated/out/all_routes_combined_v1492_candidate.nds`;SHA-256 `'+digest+'`.\n'
        '- Canonical base: `'+release['canonical_base']+'`;SHA-256 `'+release['canonical_sha256']+'`.\n'
        '- Profile: `all-routes-unified-v1492`;all471 batches114 accepted layers preserved.\n'
        '- Changed internal files versus V1456: `/COMMON/MESFILE.DK4` and `/__arm9__.bin`,limited to COMMON23/native metadata/existing selector span.\n'
        '- Exact patch: `'+release['patch']+'`;SHA-256 `'+release['patch_sha256']+'`;clean input SHA-256 `'+release['clean_input_sha256']+'`.\n'
        '- Checks: runtime1485,fonts1486,copies1487,escape1488,visual1489,release1493,startup1494,shop1495,original prior capture1498.\n\n'
        '## Remaining gates\n\nActivate representative original battle-setup,surprise and injury reactions through '
        'original game logic,with complete visible text,normal dismissal and following scenes. Preserve original RNG, '
        'actor/role selection,HP/injury flags and combat outcomes. No numerical message injection or during-combat '
        'healing/equipment/location changes. The original24 loss/surrender,16 sinking,34 aftermath38 older reviewed '
        'entries and broader source inventory remain open. Experimental;no canonical promotion or full-goal completion.\n',encoding='utf-8')
    for name in ['translation_progress.md','known_issues.md','todo.md','editorial_review_goal.md']:
        with (Path('docs')/name).open('a',encoding='utf-8',newline='\n') as f:
            f.write('\n\n## V1499 battle reactions32 registered integration\n\n'+summary+'\n\nSee [checkpoint](battle_reactions_v1499_integration_checkpoint.md).\n')
    save(ROOT/'integration_receipt.json',{'candidate':release['candidate'],'candidate_sha256':digest,'proofs':proofs,
        'completed':1323,'source_prose':1467,'reviewed_incomplete_COMMON':144,'completed_entries_added':0,
        'source_prose_reviews_added':0,'new_original_reaction_scenes_pending':True,
        'producer_sha256':sha(Path(__file__).read_bytes()),'full_goal_complete':False})
    print('V1492 integration/startup/prior-event controls recorded;1467 source reviewed/1323 complete/144 reviewed COMMON entries pending;goal active.')
