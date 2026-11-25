"""Registered hot-spring13,startup and two actual discoveries;relaxation stays open."""
from copy import deepcopy
from pathlib import Path
from shutil import copy2
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/hot_spring_integration_v1629')
RELEASE=Path('work/analysis/hot_spring_release_v1621/registered_release_verification.json')
ACTUAL=Path('work/analysis/hot_spring_actual_v1628b/two_original_hot_spring_discovery_and_minus15_visits.json')
NOTICE=Path('work/analysis/hot_spring_notice_source_v1627/optional_hot_spring_Experience_notice310_source.json')
GUIDE=Path('E:/Rota Nova translations/Guide screenshots/V1622 hot spring discovery verified')
if __name__=='__main__':
    assert not ROOT.exists() and not GUIDE.exists()
    release,actual,notice=[read(p) for p in [RELEASE,ACTUAL,NOTICE]];digest=release['candidate_sha256']
    assert digest==actual['candidate_sha256']==notice['candidate_sha256']==sha(Path(release['candidate']).read_bytes())
    assert release['complete_reconstruction_byte_exact'] and release['all473_batches114_accepted_layers_and_prior_profiles_preserved']
    assert actual['all48_coordinate_byte_fixtures_and_other4MiB_inputs_snapshots_PNGs_and_saves_audited']
    assert actual['terminal13600_is_original_rats_notice_not_normal_Sea_View'] and actual['normal_returns_claimed_only_at10000_and11700']
    assert actual['optional_relaxation_and_Experience_notice310_still_pending'] and len(actual['visits'])==2
    assert [v['normal_Sea_View_return_frame_actually_viewed'] for v in actual['visits']]==[10000,11700]
    startup_path=RELEASE.parent/'ordinary_startup_verification.json';shop_path=RELEASE.parent/'photographed_shop_formatting.json'
    startup,shop=read(startup_path),read(shop_path)
    assert startup['candidate_sha256']==shop['candidate_sha256']==digest and startup['all8_complete_startup_title_NewGame_frames_exact']
    assert startup['no_battery_save_savestate_or_fixtures'] and all(r['no_authored_indent_internal_gap_or_stray_Discover'] for r in shop['entries'])
    for visit in actual['visits']:
        assert len(visit['discovery_holds'])==len(visit['recovery_holds'])==2
        assert all(h['full_native_independent_actual_palette_ink_shadow_complete_letters_bounds_and_blank_paper_pass'] for h in visit['discovery_holds']+visit['recovery_holds'])
    lp=Path('translations/editorial_review_current_v1.json');ledger=read(lp);before=deepcopy(ledger)
    assert (ledger['records_editorially_completed'],ledger['records_with_source_and_prose_pass'],len(ledger['reviewed_but_incomplete_COMMON_IDs']))==(1350,1507,157)
    ROOT.mkdir(parents=True);save(ROOT/'coverage_before_integration.json',before)
    visual=ROOT/'startup_and_original_hot_spring_visits_visual_review.json'
    save(visual,{'all8_fixture_free_startup_panels_actually_viewed':True,'native16_panel_sheet_actually_viewed':True,
        'actual2276_9600_and309_9830_and_normal_return10000_actually_viewed':True,
        'second_original_discovery11300_and_return11700_actually_viewed':True,
        'terminal13600_is_a_rats_notice_actually_viewed':True,
        'optional_relaxation_and310_not_observed_no_completion_approval':True,'full_goal_complete':False})
    proofs={str(p):sha(p.read_bytes()) for p in [RELEASE,ACTUAL,NOTICE,startup_path,shop_path,visual]}
    ledger['latest_registered_hot_spring_candidate']={**release,'status':'experimental-native-startup-original-discovery-and-minus15-verified;optional-relaxation-pending',
        'proofs':proofs,'completed_entries_added':0,'source_prose_reviews_added':0,'full_goal_complete':False}
    unit=next(u for u in ledger['coverage_units'] if u['id']=='Shared-hot-spring13-source-prose');unit.update(
        status='registered-native-startup-original-discovery-verified;optional-relaxation-pending',candidate=release['candidate'],integration_checkpoint=str(ROOT/'integration_receipt.json'))
    ledger['formatting_watchlist']['hot_spring13'].update(registered_candidate=release['candidate'],actual_discovery_ID2276_full_native_independent_palette_RGB_verified=True,
        actual_proof=str(ACTUAL),original_minus15_and_normal_returns_verified=True,optional_relaxation_family_actual_pending=True,registered_release_pending=False)
    ledger['formatting_watchlist']['hot_spring_Experience_notice310']={'native_message_ID':310,'source_packet':str(NOTICE),
        'status':'original-optional-caller-and-source-inventoried;prose-native-release-actual-pending','not_in_completed_or_reviewed_counts_yet':True,
        'current_authored_leading_spaces_and_LF_require_native_literal_modal_review':True,'no_runtime_argument_or_invented_party_amount':True}
    ledger['formatting_watchlist']['latest_reference_proof']=str(shop_path)
    ledger['formatting_watchlist']['latest_photographed_shop_recheck']={'checkpoint':'V1629','candidate':release['candidate'],'candidate_sha256':digest,
        'proof':str(shop_path),'result':'676/677 exact repaired bytes,native wrapping and full font planes pass;no fresh shop visit.','global_formatting_audit_complete':False}
    ledger['active_source_prose_drafts']['note']='Hot-spring13 have source/native/registered integration,startup and two original discovery/-15 visits. Optional relaxation6 and following310 still require work;all13 remain pending. Earlier144 and broader prose/graphics remain open.'
    summary=('V1629 integrates source/native-approved hot-spring13 in registered V1622 while preserving all centered screenshot corrections.12 revisions1 retention;1350 complete(1009 revised341 retained),1507 source/prose reviewed,157 reviewed-incomplete COMMON(earlier144 plus hot-spring13),plus broader shared/routes/raw prose. '
        '529481 native selector/ABI cases,7336 complete copies180 cache sequences13 earlier escapes,16 original voice/table native-independent glyph planes including3 minus1 fallbacks,414 actor-table choices,16 compiler negatives and viewed sheet pass. '
        'Two exact source role1 memberships occupy188 selector bytes;gate remains172 bytes with only one pointer-bias immediate changed896 to873,numeric780 and all prior semantics preserved.123040 staged bytes,all section/BSS/cache/ITCM/arena shapes and3656 unselected or retained text/copy spans stay fixed. '
        '473 manifest batches114 accepted layers,exact clean-input patch,all8 viewed fixture-free startup controls and shop676/677 preservation pass. Two original hot-spring visits select Gerhard/voice1/2276 and original79340 fatigue-15/status309. '
        'Four complete actual discovery holds9600/9630/11300/11330 and four recovery holds9800/9830/11500/11530 match full native/independent/source-palette ink and shadows. Actual original requested15 is preserved even when the total clamps to0. '
        'Normal A returns to Sea View10000/11700,both viewed. The run is terminal13600 at an unrelated original Rats notice,not a normal final Sea View;1628b corrects the first receipt label and preserves it as superseded evidence. '
        'All48-byte position fixtures,all other4MiB,original actors/health/fatigue/skills/RNG/outcomes,inputs,snapshots/PNGs and unchanged source/disposable donors are audited. Navigation detours into ship information are disclosed,not counted as Search events. '
        'The optional relaxation branch did not occur;original read-only captain stat5 value51 gives an inclusive0..25 threshold against RNG100. No skill,eligibility or random value is changed. '
        'Only2276 is individually activated among13 lines;relaxation6 remain unverified in gameplay,so all13 stay pending. Original optional Experience notice310 is separately source-inventoried with awkward wording/authored-indent leads and no new review credit. '
        'No full route or hardware claim. V1622 experimental,V1492 promoted;canonical/V997 unchanged,separate graphics/all18 plaques and later older-record re-audit remain open;full goal active.')
    ledger['latest_checkpoint']=summary;ledger['research_checkpoints'].append({'id':'V1629-hot-spring13-integrated-discovery-verified-relaxation-pending',
        'proof':str(ROOT/'integration_receipt.json'),'candidate':release['candidate'],'completed_entries_added':0,'source_prose_reviews_added':0,'full_goal_complete':False})
    for k in ['records_editorially_completed','records_revised_and_integrated','retained_wordings_editorially_completed','records_with_source_and_prose_pass','records_with_source_prose_drafts',
        'reviewed_but_incomplete_COMMON_IDs','completed_editorial_record_counts_by_file','current_integrated_candidate','current_native_relocation_reference',
        'source_pins','unresolved_graphics_work','older_record_reaudit_after_full_editorial_goal','raw_source_coverage_revisit']:assert ledger[k]==before[k],k
    save(lp,ledger)
    pp=Path('translations/rom_retention_pins.json');pins=read(pp);pin='E:/Rota Nova translations/Generated/out/all_routes_combined_v1622_candidate.nds'
    if not any(p['path']==pin for p in pins):pins.append({'path':pin,'reason':'Registered hot-spring13 with complete centered stack;original discovery/-15 verified,optional relaxation and310 still open.'});save(pp,pins)
    GUIDE.mkdir(parents=True);screenshots=[]
    for frame,label in [(9630,'Original_hot_spring_discovery'),(9830,'Original_fatigue_recovery15'),(10000,'Sea_View_after_first_hot_spring_close')]:
        source=Path('E:/Rota Nova translations/Generated/work/emulation_v193/hot_spring_live_v1626_1622')/f'frame_{frame:06d}_navigation.png';target=GUIDE/(label+'.png')
        copy2(source,target);assert sha(source.read_bytes())==sha(target.read_bytes());screenshots.append({'source':str(source),'guide':str(target),'sha256':sha(target.read_bytes())})
    save(GUIDE/'provenance.json',{'candidate_sha256':digest,'actual_proof':str(ACTUAL),'screenshots':screenshots,'location_fixture_only_original_Search_RNG_and_outcomes':True,
        'only_discovery2276_and_recovery15_verified_optional_relaxation_pending':True,'not_earned_travel_or_full_route_hardware_verification':True,'full_goal_complete':False})
    document=Path('docs/hot_spring_v1629_integration_checkpoint.md');assert not document.exists()
    document.write_text('# V1629 hot-spring13 integration checkpoint\n\n'+summary+'\n\n## Exact experimental release\n\n'
        '- Candidate: `'+release['candidate']+'`;SHA-256 `'+digest+'`.\n- Canonical construction base: `'+release['canonical_base']+'`;SHA-256 `'+release['canonical_sha256']+'`.\n'
        '- Profile: `all-routes-unified-v1622`;473 batches114 accepted layers. V1492 remains promoted.\n'
        '- Changes versus the centered screenshot parent: `/COMMON/MESFILE.DK4` block24 and `/__arm9__.bin` original metadata/fixed selector-gate spans. Other files,fonts,palettes,graphics and all four routes preserved.\n'
        '- Patch: `'+release['patch']+'`;SHA-256 `'+release['patch_sha256']+'`;clean input `'+release['clean_input_sha256']+'`.\n\n'
        '## Continue\n\nReview/correct original optional Experience notice310,then verify the original optional relaxation table2116D60 and following notice through normal gameplay. '
        'Exact recorded navigation through13600 can be replayed with a successor producer;the final state is a Rats warning. Do not restart a live handle without checking it;all present jobs are terminal. '
        'The first actual receipt1628 has an incorrect final-return label;use1628b. Discovery/recovery pixel checks and returns10000/11700 remain valid. All13 editorial entries stay open until remaining gates are satisfied.\n',encoding='utf-8')
    for name in ['translation_progress.md','known_issues.md','todo.md','editorial_review_goal.md']:
        with (Path('docs')/name).open('a',encoding='utf-8') as f:f.write('\n\n## V1629 hot-spring13 integrated;optional branch pending\n\n'+summary+'\n\nSee [checkpoint](hot_spring_v1629_integration_checkpoint.md).\n')
    Path('docs/editorial_handoff_current.md').write_text('# Current editorial handoff - V1629\n\n'+summary+'\n\n'
        'Read AGENTS/build continuity/release_stack/known issues/natural-dialogue/delegation instructions. Sources read-only;executed producers and proofs receive successors. No subagents authorized. All present jobs terminal.\n\n'
        '## Authoritative evidence\n\n- Ledger: translations/editorial_review_current_v1.json.\n- Integration: work/analysis/hot_spring_integration_v1629/integration_receipt.json.\n'
        '- Release/patch: work/analysis/hot_spring_release_v1621/registered_release_verification.json.\n- Actual corrected scope: work/analysis/hot_spring_actual_v1628b/two_original_hot_spring_discovery_and_minus15_visits.json.\n'
        '- Current candidate parser: dk4tool.patch.hot_spring_editorial.current_entries. Completed native reference remains V1594 until the hot-spring family is complete.\n'
        '- Native-approved manuscript: translations/hot_spring_editorial_manuscript_v2.json.\n- Next310 source packet: work/analysis/hot_spring_notice_source_v1627/optional_hot_spring_Experience_notice310_source.json.\n\n'
        '## Next work\n\nReview/correct310 prose and its original literal-modal formatting,retaining no arguments and the Experience stat meaning. Complete actual optional relaxation table2116D60 and its subsequent310/normal return. '
        'Original captain stat5 is51;optional branch accepts source RNG100 draws0..25. No stat/eligibility/RNG edit. Two source-hot-spring visits selected the false branch. '
        'The audited original run1626 ends13600 in a Rats notice;do not call that a normal final Sea View. Actual normal returns10000/11700 are viewed. Use1628b,not the old1628 label. '
        'All13 remain pending;earlier144 COMMON and broader shared/routes/raw prose remain. Preserve separate graphics/all18 plaque audit and queued older-record checks.\n\n'
        'V1622 inherits screenshot-text-repairs-centered-20261022;preserve both later screenshot repairs and Yes/No centering in every successor. Use Python C:/Python314/python.exe,PYTHONUTF8=1,PYTHONPATH=.;.deps. '
        'out/work-analysis junctions point to E;archive lexical paths without resolve(). Redirect huge builder output and print bounded tails. Preserve188 selector/172 gate/123040 staged sizes and canonical base. '
        'V1492 promoted;new ROM and patch remain experimental. Retain all ROMs;unsigned PowerShell retention preview was policy-blocked last turn and no bypass or apply was attempted.\n',encoding='utf-8')
    save(ROOT/'integration_receipt.json',{'candidate':release['candidate'],'candidate_sha256':digest,'proofs':proofs,'guide':str(GUIDE),'completed':1350,'source_prose':1507,
        'reviewed_incomplete_COMMON':157,'completed_entries_added':0,'source_prose_reviews_added':0,'original_discovery_and_minus15_verified_optional_relaxation_and310_pending':True,
        'terminal13600_rats_warning_scope_corrected':True,'producer_sha256':sha(Path(__file__).read_bytes()),'full_goal_complete':False})
    print('V1622 integrated/startup/discovery/-15 recorded:1350 complete,1507 reviewed,157 pending. Optional relaxation/310 and full goal remain open;all jobs terminal.')
