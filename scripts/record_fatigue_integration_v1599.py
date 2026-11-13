"""Record native/registered/positive fatigue verification;recovery stays open."""
from copy import deepcopy
from pathlib import Path
from shutil import copy2
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/fatigue_status_integration_v1599')
RELEASE=Path('work/analysis/fatigue_status_release_v1593/registered_release_verification.json')
ACTUAL=Path('work/analysis/fatigue_increase_verified_v1598/fixture_free_Search_failure_original_plus3_verified.json')
PILOTS=Path('work/analysis/fatigue_shore_pilots_verified_v1597d/both_terminal_shore_pilots_audited.json')
if __name__=='__main__':
    assert not ROOT.exists()
    release,actual,pilots=read(RELEASE),read(ACTUAL),read(PILOTS);digest=release['candidate_sha256']
    assert sha(Path(release['candidate']).read_bytes())==digest==actual['candidate_sha256']
    assert release['complete_reconstruction_byte_exact'] and release['all471_batches114_accepted_layers_and_prior_profiles_preserved']
    assert release['all2_fatigue_statuses_and3666_unselected_texts_preserved'] and release['only_COMMON4_and_original_native_metadata_changed']
    assert actual['no_fixture_or_RNG_state_event_or_message_injection'] and actual['source_disposable_saves_unchanged']
    assert actual['revised308_full_F_amount_period_and_source_shadow_RGB_verified'] and actual['recovery309_still_pending']
    assert [(h['fatigue_before'],h['fatigue_after']) for h in actual['holds']]==[(6,9),(6,9)]
    changed=[r for r in actual['whole_frame_comparisons'] if 'changed_pixels' in r]
    assert [(r['frame'],r['changed_pixels']) for r in changed]==[(5600,276),(5700,276),(5730,276)]
    assert len(actual['whole_frame_comparisons'])-len(changed)==15
    startup_path=RELEASE.parent/'ordinary_startup_verification.json';shop_path=RELEASE.parent/'photographed_shop_formatting.json'
    startup,shop=read(startup_path),read(shop_path)
    assert startup['candidate_sha256']==shop['candidate_sha256']==digest and startup['all8_complete_startup_title_NewGame_frames_exact']
    assert startup['no_battery_save_savestate_or_fixtures'] and all(r['no_authored_indent_internal_gap_or_stray_Discover'] for r in shop['entries'])
    fonts=read('work/analysis/fatigue_status_fonts_v1590/native_font_proof.json')
    assert len(fonts['cases'])==202 and len(fonts['invalid_compiler_inputs_rejected'])==15 and fonts['source_actual_amount_cases']==5
    ledger_path=Path('translations/editorial_review_current_v1.json');ledger=read(ledger_path);before=deepcopy(ledger)
    assert (ledger['records_editorially_completed'],ledger['records_with_source_and_prose_pass'],len(ledger['reviewed_but_incomplete_COMMON_IDs']))==(1348,1494,146)
    ROOT.mkdir(parents=True);save(ROOT/'coverage_before_checkpoint.json',before)
    visual=ROOT/'startup_numeric_panels_and_actual_plus3_visual_review.json'
    save(visual,{'all8_ordinary_startup_panels_actually_viewed':True,'all13_source_and_boundary_numeric_panels_actually_viewed':True,
        'actual_complete_revised308_5730_and_normal_Sea_View5900_actually_viewed':True,
        'recovery_pilot7000_stopped_at_original_disease_result_actually_viewed':True,
        'no_recovery309_or_family_completion_approval':True,'full_goal_complete':False})
    proofs={str(p):sha(p.read_bytes()) for p in [RELEASE,ACTUAL,PILOTS,startup_path,shop_path,visual]}
    ledger['latest_registered_fatigue_status_candidate']={**release,'status':'experimental-native-startup-original308-plus3-verified;original309-recovery-context-pending',
        'proofs':proofs,'completed_entries_added':0,'source_prose_reviews_added':0,'full_goal_complete':False}
    unit=next(u for u in ledger['coverage_units'] if u['id']=='Shared-fatigue-status2-source-prose')
    unit.update(status='registered-native-startup-original308-verified;309-recovery-pending',candidate=release['candidate'],integration_checkpoint=str(ROOT/'integration_receipt.json'))
    ledger['formatting_watchlist']['fatigue_status2'].update(registered_candidate=release['candidate'],native_font_and_registered_release_pending=False,
        original308_live_plus3_complete_F_digits_period_ink_shadow_and_return_verified=True,original309_recovery_pending=True,
        actual_increase_proof=str(ACTUAL),shore_research_proof=str(PILOTS))
    ledger['formatting_watchlist']['latest_reference_proof']=str(shop_path)
    ledger['formatting_watchlist']['latest_photographed_shop_recheck']={'checkpoint':'V1599','candidate':release['candidate'],'candidate_sha256':digest,
        'proof':str(shop_path),'result':'676/677 exact repaired bytes,native wrapping and full font planes pass;no fresh shop visit.','global_formatting_audit_complete':False}
    ledger['active_source_prose_drafts']['note']='Fatigue statuses308/309 have source/native/registered integration,202 font cases and original fixture-free308+3 gameplay. Recovery309 still needs actual-context verification;both entries remain pending with the older144 reviewed COMMON and broader prose/graphics.'
    summary=('V1599 records registered V1594 fatigue status2 integration,both revised,without completion credit. Natural Fatigue increased/decreased by one original%s replaces the unrelated308 fragment and telegraphic309. '
        'Original79728 signed delta/34540 clamp/ABF50 full-width digits/546B8 loader-varargs-macro pipeline and five source amount cases3/5/10/15 are mapped. All202 native/independent full glyph planes for0..100,complete F/full-width digits/period,literal x0 margins,bounds and15 compiler negatives pass;13 source/boundary panels viewed. Zero helper exits without a status;zero formatting probes are synthetic only. '
        '7336 complete native copies180 cache cases pass. Only COMMON4 and original native metadata change versus V1578;3666 other copies,40 blocks,all native code,188 selector172 gate123040 staged bytes and earlier routes/graphics/fonts/helpers are exact.471 batches114 accepted layers,exact clean-input patch,all8 viewed fixture-free startup controls and shop676/677 preservation pass. '
        'Original fixture-free Search finds nothing,then308 naturally reports+3,actual fatigue6 to9. Complete5700/5730 native-independent/source-palette RGB ink-and-shadow holds pass;three changed full screens5600/5700/5730 differ only276 predicted colored glyph pixels each,15 other full screens exact. Normal A returns to Sea View5900 and donors unchanged. '
        'The first binary RGB audit counted CP932 shadow as black;1587g/1598 verify original foreground15/gray14 palette colors exactly without masking or game changes. Two separate shore pilots are audited through5800/7000,with only40 position bytes atdeclaredpre-event frames and all other4MiB,inputs,RAM/PNG and saves checked. They show another failed search and two original beast/crew-loss/disease outcomes;no recovery309 is observed. '
        'Original fleet virtual position2C1C4 reads cached34/38,while36A24 is a mobile getter;the exploratory fleet-call output is discarded. Source offline region/shore queries are not live hot-spring reachability proof. Reconcile actual Search context and cached/mobile positions before predicting recovery;do not force event,RNG,health or numeric messages. '
        'Counts1348 complete(1007 revised341 retained),1494 source/prose reviewed,146 reviewed-incomplete COMMON(2 fatigue plus earlier144),plus broader shared/routes/raw prose. V1594 experimental,V1492 promoted,V1578 completed-native reference;canonical/V997 unchanged. Separate graphics/all18 plaques and later older-record re-audit stay open;goal active.')
    ledger['latest_checkpoint']=summary;ledger['research_checkpoints'].append({'id':'V1599-fatigue2-integrated-native-and-natural-plus3','proof':str(ROOT/'integration_receipt.json'),
        'candidate':release['candidate'],'completed_entries_added':0,'source_prose_reviews_added':0,'full_goal_complete':False})
    for key in ['records_editorially_completed','records_revised_and_integrated','retained_wordings_editorially_completed','records_with_source_and_prose_pass','records_with_source_prose_drafts',
        'reviewed_but_incomplete_COMMON_IDs','completed_editorial_record_counts_by_file','current_integrated_candidate','current_native_relocation_reference',
        'source_pins','unresolved_graphics_work','older_record_reaudit_after_full_editorial_goal','raw_source_coverage_revisit']:assert ledger[key]==before[key],key
    save(ledger_path,ledger)
    pins_path=Path('translations/rom_retention_pins.json');pins=read(pins_path);pin='E:/Rota Nova translations/Generated/out/all_routes_combined_v1594_candidate.nds'
    assert not any(p['path']==pin for p in pins);pins.append({'path':pin,'reason':'Registered fatigue2 integration and original fixture-free308 verified;original recovery309 remains open.'});save(pins_path,pins)
    guide=Path('E:/Rota Nova translations/Guide screenshots/V1594 fatigue increase verified');assert not guide.exists();guide.mkdir(parents=True)
    cap=Path('E:/Rota Nova translations/Generated/work/emulation_v193/fatigue_increase_actual_v1597_1594');screenshots=[]
    for frame,label in [(5730,'Natural_fatigue_increased_by3'),(5900,'Sea_View_after_normal_close')]:
        source=cap/f'frame_{frame:06d}_navigation.png';target=guide/(label+'.png');copy2(source,target);assert sha(source.read_bytes())==sha(target.read_bytes())
        screenshots.append({'source':str(source),'guide':str(target),'sha256':sha(target.read_bytes())})
    save(guide/'provenance.json',{'candidate_sha256':digest,'actual_proof':str(ACTUAL),'screenshots':screenshots,'fixture_free_original_Search_and_natural_plus3':True,
        'no_recovery309_or_full_route_hardware_claim':True,'full_goal_complete':False})
    document=Path('docs/fatigue_status_v1599_integration_checkpoint.md');assert not document.exists()
    document.write_text('# V1599 fatigue status integration checkpoint\n\n'+summary+'\n\n## Experimental release\n\n'
        '- Candidate: `E:/Rota Nova translations/Generated/out/all_routes_combined_v1594_candidate.nds`;SHA-256 `'+digest+'`.\n'
        '- Canonical construction base: `'+release['canonical_base']+'`;SHA-256 `'+release['canonical_sha256']+'`.\n'
        '- Profile: `all-routes-unified-v1594`;471 batches114 accepted layers;V1492 remains promoted.\n'
        '- Changed files versus V1578: `/COMMON/MESFILE.DK4` and `/__arm9__.bin`;COMMON4/original metadata only.\n'
        '- Patch: `'+release['patch']+'`;SHA-256 `'+release['patch_sha256']+'`;clean input `'+release['clean_input_sha256']+'`.\n'
        '- Checks: source1587/prose1588/plan1589/fonts1590/copies1591/native approval1592/release1595/startup1596/shop1596b/positive actual1598/pilots1597d.\n\n'
        '## Next work\n\nResolve original recovery309 gameplay through the source expedition context. The live pilot ended at an original disease result after beast attacks;no normal final return or recovery is claimed for that pilot. A future coherent location fixture may need both original cached fleet point34/38 and mobile positions16/20;prove ownership and preserve all other bytes. The current native region model does not explain all observed results,so do not label an artificially chosen outcome natural. Current positive308 is verified;both family entries stay open until remaining scene gates are resolved.\n',encoding='utf-8')
    for name in ['translation_progress.md','known_issues.md','todo.md','editorial_review_goal.md']:
        with (Path('docs')/name).open('a',encoding='utf-8') as f:f.write('\n\n## V1599 fatigue2 integration and original increase\n\n'+summary+'\n\nSee [checkpoint](fatigue_status_v1599_integration_checkpoint.md).\n')
    Path('docs/editorial_handoff_current.md').write_text('# Current editorial handoff - V1599\n\n'+summary+'\n\n'
        'Read AGENTS.md,build_continuity_protocol.md,release_stack.json,relevant known_issues.md,natural_dialogue_workflow.md and dialogue_delegation_protocol.md. Sources are read-only;executed producers/manuscripts/proofs receive successors. No subagents authorized. All current jobs terminal.\n\n'
        '## Authoritative current evidence\n\n- Ledger: translations/editorial_review_current_v1.json.\n- Latest compiled: registered all-routes-unified-v1594;parser dk4tool.patch.fatigue_status_editorial.current_entries.\n'
        '- Release: work/analysis/fatigue_status_release_v1593/registered_release_verification.json.\n- Current checkpoint: work/analysis/fatigue_status_integration_v1599/integration_receipt.json.\n'
        '- Positive: work/analysis/fatigue_increase_verified_v1598/fixture_free_Search_failure_original_plus3_verified.json.\n- Shore pilot audit: work/analysis/fatigue_shore_pilots_verified_v1597d/both_terminal_shore_pilots_audited.json.\n'
        '- Source: work/analysis/fatigue_status_source_v1587/source_amounts_and_original_expedition_context.json.\n- Source/native manuscript: translations/fatigue_status_editorial_manuscript_v2.json.\n'
        '- V1578 remains completed-native reference;V1594 target hashes require the fatigue parser. V1492 remains promoted;immutable construction baseline stays fixed.\n\n'
        '## Continue\n\nComplete the original recovery309 context and visual/dismissal/transition test. Existing fixture-free308+3 is already fully verified;do not redo it without a concrete risk. Current pilot1597c is terminal at7000 in disease-after-beasts;donors unchanged. Existing40-byte fixtures affect mobiles only;original Search uses fleet cached point via2C1C4. The earlier36A24 fleet ABI attempt is invalid. Reconcile source terrain/cache/region/action context and consider a coherent original-coordinate fixture rather than forcing event/RNG/text. No309 original gameplay completion claim yet.\n\n'
        'Preserve all unowned4MiB,actor identities,health/fatigue and original outcomes. User permits isolated locations and useful testing cheats,but do not label fixture setup earned progress. Full graphics/all18 plaques and later older-record re-audit stay unfinished. ROMs/captures stay under E:/Rota Nova translations;retention preview only. Python C:/Python314/python.exe with PYTHONUTF8=1,PYTHONPATH=.;.deps. Task-specific escalation works around P-drive launcher errors. Builder stdout is huge;redirect logs and use bounded tails. Archive lexical paths through junctions without resolve().\n',encoding='utf-8')
    save(ROOT/'integration_receipt.json',{'candidate':release['candidate'],'candidate_sha256':digest,'proofs':proofs,'guide':str(guide),
        'completed':1348,'source_prose':1494,'reviewed_incomplete_COMMON':146,'source_prose_reviews_added':0,'completed_entries_added':0,
        'original308_positive_verified_original309_recovery_pending':True,'all_current_runs_terminal':True,'producer_sha256':sha(Path(__file__).read_bytes()),'full_goal_complete':False})
    print('V1594 native/release/startup/original+3 recorded;1348 complete/1494 source-prose/146 pending.309 recovery and full goal remain open.')
