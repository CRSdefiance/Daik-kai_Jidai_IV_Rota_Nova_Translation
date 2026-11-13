"""Record registered integration/startup/control proof without new event completion."""
from copy import deepcopy
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/ship_loss_surrender_integration_v1473')
RELEASE=Path('work/analysis/ship_loss_surrender_release_v1455/registered_release_verification.json')

def main():
    assert not ROOT.exists()
    release=read(RELEASE)
    startup_path=RELEASE.parent/'ordinary_startup_verification.json'
    shop_path=RELEASE.parent/'photographed_shop_formatting.json'
    control_path=Path('work/analysis/loss_surrender_control_verified_v1465/actual_capture_and_return_verification.json')
    startup,shop,control=[read(p) for p in [startup_path,shop_path,control_path]]
    digest=release['candidate_sha256']
    assert sha(Path(release['candidate']).read_bytes())==digest
    assert sha(Path(release['patch']).read_bytes())==release['patch_sha256']
    assert all(r['candidate_sha256']==digest for r in [startup,shop,control])
    assert release['complete_reconstruction_byte_exact']
    assert release['all471_batches114_accepted_layers_and_prior_profiles_preserved']
    assert release['sections_BSS_cache_arena_ITCM_and123040_staged_payload_exact']
    assert startup['all8_complete_startup_title_NewGame_frames_exact'] and startup['no_battery_save_savestate_or_fixtures']
    assert sha(Path(startup['review_sheet']).read_bytes())==startup['review_sheet_sha256']
    assert control['entire4MiB_fixture_input_primary_RAM_and_PNG_hash_audits_pass']
    assert control['later10_whole_reward_cargo_and_sailing_screens_exact_to_V1430']
    assert control['normal_capture_A_dismissal_flagship_victory_rewards_X_cargo_finish_touch_Yes_and_return_to_sailing']
    assert control['source_and_disposable_saves_unchanged'] and control['no_sinking_or_other_unreviewed_family_completion_credit']
    ledger_path=Path('translations/editorial_review_current_v1.json');ledger=read(ledger_path);before=deepcopy(ledger)
    assert (ledger['records_editorially_completed'],ledger['records_with_source_and_prose_pass'],len(ledger['reviewed_but_incomplete_COMMON_IDs']))==(1323,1435,112)
    ROOT.mkdir(parents=True);save(ROOT/'coverage_before_integration_checkpoint.json',before)
    proofs={str(p):sha(p.read_bytes()) for p in [RELEASE,startup_path,shop_path,control_path,
        Path('work/analysis/approach_pilots_verified_v1470/terminal_approach_audit.json'),
        Path('work/analysis/original_fleet_guns_v1469/original_fleet_census.json')]}
    visual=ROOT/'startup_visual_review.json'
    save(visual,{'review_sheet':startup['review_sheet'],'review_sheet_sha256':startup['review_sheet_sha256'],
        'all8_panels_visually_reviewed':True,'title_NewGame_confirmation_and_opening_text_visible':True,
        'scope':'The eight recorded ordinary startup controls;not a full route or new loss/surrender scene.',
        'full_goal_complete':False})
    summary=('V1473 records registered V1456 integration of24 native-approved loss/surrender revisions, '
        'without editorial completion credit. Full471-batch/114-accepted-layer build and exact clean-input '
        'patch reconstruction pass;3644 other text/copy spans,routes,graphics,fonts,opaque duel prefix '
        'and all earlier scopes remain preserved. Existing188-byte selector and172-byte gate fit; '
        'sections,BSS,cache,arena,ITCM and123040 staged bytes do not grow. All8 ordinary title/New Game '
        'controls match and are visually reviewed. Repaired shop676/677 wrapping and complete font '
        'planes remain exact,with no fresh shop visit claimed. Original previous2082 capture control '
        'has two complete native/reference/independent/RGB holds and normal capture,flagship,victory, '
        'rewards,cargo confirmation and return to mode000 sailing at13200;all10 later whole screens '
        'match V1430. Source/disposable saves and the sole40-byte prebattle location fixture are fully '
        'audited. Two alternate45-byte approach pilots terminate normally at9500 without starting '
        'combat;all input,4MiB fixture,RAM,PNG and save audits pass and no event credit is granted. '
        'Read-only census finds27 existing stronger fleets at sea;cached points need actual loaded '
        'position verification. Own capture,own surrender,enemy surrender and16 sinking original '
        'scene gates remain open. Counts1323 complete(985 revised338 retained),1435 source/prose, '
        '112 reviewed-incomplete COMMON(24 loss/surrender16 sinking34 aftermath38 older),plus broader '
        'shared/routes/raw prose. V1456 is latest experimental integration;V1430 remains completed-native '
        'relocation reference. Canonical,V997,separate graphics/all18 plaques and later older-record '
        're-audit remain unchanged/open;goal active.')
    ledger['latest_checkpoint']=summary
    ledger['latest_registered_loss_surrender_candidate']={**release,'status':'experimental-integrated-startup-and-prior-capture-control-verified;three-original-new-event-families-pending',
        'proofs':proofs,'startup_visual_review':str(visual),'ordinary_startup_pending':False,
        'representative_original_loss_surrender_scenes_pending':True,'completed_entries_added':0,'full_goal_complete':False}
    unit=next(u for u in ledger['coverage_units'] if u['id']=='Shared-ship-loss-surrender24-source-prose')
    unit.update(status='registered-integrated-native-startup-approved;original-events-pending',candidate=release['candidate'],integration_checkpoint=str(ROOT/'integration_receipt.json'))
    watch=ledger['formatting_watchlist']['ship_loss_surrender_research']
    watch.update(registered_ROM_repair_and_original_events_still_pending=False,
        registered_ROM_repair_pending=False,original_events_still_pending=True,registered_candidate=release['candidate'],
        integration_proof=str(RELEASE),startup_visual_review=str(visual),prior_capture_control_proof=str(control_path))
    ledger['active_source_prose_drafts']['note']='Loss/surrender24 is integrated and source/native/startup-approved in registered V1456 with exact patch;three original new report families still need actual display/dismissal/return.16 sinking,34 aftermath38 older reviewed entries and broader shared/routes/raw prose remain open.'
    ledger['research_checkpoints'].append({'id':'V1473-loss-surrender24-registered-integration','proof':str(ROOT/'integration_receipt.json'),
        'candidate':release['candidate'],'completed_entries_added':0,'source_prose_reviews_added':0,'full_goal_complete':False})
    for key in ['records_editorially_completed','records_revised_and_integrated','retained_wordings_editorially_completed',
        'records_with_source_and_prose_pass','reviewed_but_incomplete_COMMON_IDs','completed_editorial_record_counts_by_file',
        'current_integrated_candidate','current_native_relocation_reference','source_pins','unresolved_graphics_work',
        'older_record_reaudit_after_full_editorial_goal','raw_source_coverage_revisit']:
        assert ledger[key]==before[key],key
    save(ledger_path,ledger)
    pins_path=Path('translations/rom_retention_pins.json');pins=read(pins_path)
    pin='E:/Rota Nova translations/Generated/out/all_routes_combined_v1456_candidate.nds'
    assert not any(r['path']==pin for r in pins)
    pins.append({'path':pin,'reason':'Registered source/native/startup-verified loss/surrender24 integration;original event families still under test.'});save(pins_path,pins)
    document=Path('docs/ship_loss_surrender_v1473_integration_checkpoint.md');assert not document.exists()
    document.write_text('# V1473 loss and surrender integration checkpoint\n\n'+summary+'\n\n'
        'Candidate: `'+release['candidate']+'`; SHA-256 `'+digest+'`.\n\n'
        'Patch: `'+release['patch']+'`; SHA-256 `'+release['patch_sha256']+'`. '
        'Clean input SHA-256 `'+release['clean_input_sha256']+'`.\n\n'
        'Canonical base: `'+release['canonical_base']+'`; SHA-256 `'+release['canonical_sha256']+'`. '
        'Internal changes versus V1430: COMMON22/23, native ARM9 offset/directory metadata, '
        'and the existing selector/gate spans. Experimental; no canonical promotion.\n\n'
        '## Remaining scene verification\n\nActivate each original own-capture,own-surrender and enemy-surrender family '
        'through ordinary game controls. Record visible complete text,normal dismissal and following scenes. '
        'Preserve original ship/slot/party selection,health,crew,RNG and outcome logic. CPU font/counterfactual '
        'proofs do not replace original event activation. The new fleet survey changes only own locations before '
        'combat and does not alter NPC equipment or strengths.\n',encoding='utf-8')
    for name in ['translation_progress.md','known_issues.md','todo.md','editorial_review_goal.md']:
        with (Path('docs')/name).open('a',encoding='utf-8',newline='\n') as f:
            f.write('\n\n## V1473 loss/surrender registered integration\n\n'+summary+'\n\nSee [checkpoint](ship_loss_surrender_v1473_integration_checkpoint.md).\n')
    save(ROOT/'integration_receipt.json',{'candidate':release['candidate'],'candidate_sha256':digest,'proofs':proofs,
        'startup_visual_review':str(visual),'completed':1323,'source_prose':1435,'reviewed_incomplete_COMMON':112,
        'completed_entries_added':0,'source_prose_reviews_added':0,'three_original_report_families_pending':True,
        'producer_sha256':sha(Path(__file__).read_bytes()),'full_goal_complete':False})
    print('V1456 registered integration/startup/prior capture control recorded;1323 complete/1435 reviewed/112 incomplete;new scene gates open.')

if __name__=='__main__':main()
