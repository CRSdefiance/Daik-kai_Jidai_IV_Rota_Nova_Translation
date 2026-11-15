"""Publish the registered315-source checkpoint without narrowing the full editorial goal."""
from pathlib import Path
from scripts.audit_story_glyph_consistency import load, save
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest
from scripts.save_editorial_progress_checkpoint_v10 import checkpoint

ROOT = Path('work/Maria_B286_B302_clean_20261110')
OUT = Path('work/maria315_B286_B302_release_v1')


def main():
    rp, cp = OUT/'registered_release_verification.json', OUT/'completion_checkpoint.json'
    release, complete = map(load, [rp, cp])
    actual = load(ROOT/'gameplay_review_v1.json')
    censuspath = Path('work/story_source_coverage_20261110_SC3_v17/coverage.json')
    census = load(censuspath)
    assert (release['registered_manifest_entries'], release['accepted_layers'], release['passing_release_checks']) == (725, 114, 60)
    assert complete['new_credit'] == 315 and complete['counts'] == dict(completed=24093, revised=14343, retained=9750)
    assert len(census['records']) == 5129 and len(census['missing']) == 0 and census['new_exact_bindings'] == 315
    assert not census['inventory_failures'] and not census['legacy_source_bindings_not_exact']
    assert release['clean_input_patch_byte_exact'] and not release['own_registered_startup_pending']
    assert actual['all_actual_body_menu_andtransition_sheets_directly_viewed']
    assert (actual['distinct_source_body_objects'], actual['distinct_body_pages'], actual['frames']) == (213, 213, 91844)
    assert Path(release['candidate']).read_bytes() == Path(release['exact_clean_reconstruction']).read_bytes()
    registry, prior = map(load, ['translations/release_stack.json', OUT/'release_stack_before_Maria315.json'])
    assert registry['latest_promoted_build'] == prior['latest_promoted_build']
    delta = load(ROOT/'final_layout_delta_v1.json')
    assert delta['final_layout_changes'] == 7 and delta['pages_reclaimed'] == 1
    package = Path('releases/all_routes_editorial_20261110_maria315_candidate/release_manifest.json')
    assert load(package)['candidate_sha256'] == release['candidate_sha256']
    package_root = package.parent
    for p, h in load(package_root/'checksums.json').items():
        assert digest(package_root/p) == h
    visualpath = OUT/'own_startup_visual_v1/receipt.json'
    visual = load(visualpath)
    assert len(visual['selected_captures']) == 6 and digest(visual['sheet']) == visual['sheet_sha256']
    # All six complete captures and this exact composite were directly opened.
    ownview = OUT/'own_startup_visual_v1/direct_visual_review.json'
    assert not ownview.exists()
    save(ownview, dict(original_receipt=str(visualpath), original_receipt_sha256=digest(visualpath),
        all_six_original_captures_andexact_composite_directly_viewed=True,
        current_candidate_sha256=release['candidate_sha256'], original_capture_receipt_preserved=True,
        gameplay_beyond_disclosed_startup_not_claimed=True, new_credit=0))
    evidence = {str(p): digest(p) for p in [rp, cp, censuspath, package,
        Path('translations/maria315_B286_B302_integrated_final_review_v1.json'),
        *[ROOT/p for p in ['research_completion_v1/research_completion.json', 'gameplay_review_v1.json',
            'offline_display_approval_v1.json', 'stored_v1/stored_native_verification.json',
            'stored_catalogue_all_v1/all_stored_effective_body_bindings.json', 'loaders_v1/verification.json',
            'final_layout_delta_v1.json', 'registered_preparation_v1/qualification.json',
            'registered_semantic_checks_v1/qualification.json', 'actor0_scope_negatives_v1/qualification.json']],
        OUT/'own_registered_startup_verification.json', OUT/'own_registered_name_getters_v1.json', visualpath, ownview,
        Path('work/story_source_coverage_20261109_SC2_v2/residual_clean_source_packet.json'), Path(__file__)]}
    summary = ('Maria B286–B302 isregistered andcredited once:315 contextual reviews,162 revisions,153 justified retentions and14 scoped names. '
        'All309 body pages,six captions and18 name strings pass. Seven layouts improve andone page isreclaimed. '
        'Four initialized emulator samples observe213 bodies/pages,allthree menus,13 FE returns andfour sailing returns;96 body variants areoffline-only. '
        'The cumulative725-entry/114-layer candidate passes60 release checks,exact clean-input reconstruction,own startup,24 protected getters and27 repository tests. '
        'Integrated24,093. Native Maria census5129/5129;Lil1,805 andseparate shared/player-facing scope remain. Main awaits acceptance;fullgoalactive,no worker live.')
    document = 'docs/editorial_Maria315_B286_B302_registered_20261110.md'
    text = f'''# Maria B286–B302 registered cumulative candidate — November 10, 2026

{summary}

Use [the cumulative test ROM](../work/maria315_B286_B302_release_v1/all_routes_maria315_B286_B302_candidate.nds) and its adjacent manifest. ROM SHA256: `{release['candidate_sha256']}`. Clean-input patch SHA256: `{release['patch_sha256']}`;clean input SHA256: `{release['clean_input_sha256']}`. [Standalone patch package](../releases/all_routes_editorial_20261110_maria315_candidate/README.md). This is the registered successor to Maria349,prepared for testing andpromotion acceptance. The earlier Maria349 ROM,its promotion-ready reconstruction,package andcommit48072f1c remain preserved. Main stays V4701;canonical construction baseline stays unchanged. All724 predecessor entries and114 accepted layers remain,including early Rafael/tutorial work,Market16-byte format/both pointers,six-section ARM9,ASCII rightbounds,source25v2 andB164R99 padding correction. No graphics artwork change.

The previous goal turn was progress: a fresh byte-exact Maria349 testing copy andallpending315 prose/native work were committed/pushed as48072f1c,with remote identity andclean worktree verified. This turn isprogress: completed every remaining315 display/storage/representative/release gate andadded315 disjoint credits once. Reuse these checks. Earlier documents that call this batch unreviewed,formatting-pending ornot integrated are preserved history.

Seventeen complete SC3 groups B286–B302 contain196 ordinary bodies,113 physical personality alternatives andsix captions. All315 clean meanings/independent drafts were sealed before current-English extraction. Each exact source/current/registered reference,finding,revision andjustified retention isbound in `translations/maria315_B286_B302_integrated_final_review_v1.json`;allfive individual gates pass. Fourteen scoped names/28 getters retain18 exact strings. Escante is aspoken name inthis scope,not anew observed portrait. The broader207-name review andfull catalogue UI layouts remain separate. Exact four item titles,five commodities,three places andthe full Proof convention arebound;do not repeat those lookups.

Source corrections restore first-person references andreported uncertainty,remove unsupported claims,reverse the guardian discovery back to “You've finally found me,” andcorrect the Sextant transaction to handing it over. Charles mentioned the monk's Alchemy Book;he did not write it. Preserve mineral poison in drinking water,the sacrificed medicine,the monk's illness/death andthe villagers' religious praise without inventing a toxin orbiography. Keep uncertainty about Escante/Spain andthe voluntary trust resolution. Retain good short reactions,character voices andXiexie for their individual reasons. B295R4's full-width Latin I andtwo full-width question reactions arecorrected. Alloriginal controls remain,including Rafael0's two B286 replies andLil2's two B302 book-recognition lines,independently ofcaptain Maria3.

Final plan: `plan_v5/automatic_plans.json`,309 bodies/309 pages plus six captions,zero errors/warnings/failures. The complete conqueror warning/question fits one page rather than leaving “into their hands?” on a second page. Six additional phrase wraps keep like this,out of,preach to,ghost ship,the Ancient City Map title andthe short Proofs question tag together. The title's short opening line is justified to keep its exact name intact;no prose is shortened. One additional give up on preference already matched andreceives no byte-change tally. Seven actual final layout changes reduce310 pages to309. All35 initial body sheets,five name/caption sheets andfour fresh changed-layout sheets were directly viewed;303 exact body proofs are reused andonlysix changed records/24 alignments rerendered. Every final page isbound to exact viewed pixels. The historical actor0 helper is preserved separately under v4;two new allowlist negatives reject missing/extra actors before output. No native guard orQA warning iswaived.

Offline native/storage checks pass309 bodies/1236 selected alignments,17 complete style objects/136 slots/153 compiler negatives,three menus/six captions/18 alignments/54 modal returns/24 planes/21 negatives,andall18 name strings. The whole clean/current/command/block/archive/serialized-ROM inverses pass. Storage has97 fresh parity-dependent pages and212 exact reused pages,320 native relative cases,309 effective native lookups,303 archive loads/cache hits and606 handoffs. Allsource controls andruntime substitutions remain intact.

Four initialized emulator samples run91,844 frames andobserve213 distinct bodies/pages,17 effective voice4 alternatives,allthree two-choice menus/both highlight indices,six captions,all13 original FE panels andtheir normal A returns,andfour resupply/departure/sailing returns. All28 actual body/menu/transition/full-scene sheets aredirectly viewed. The96 other physical style alternatives areoffline-only;no source credits areduplicated for variants. Ms. FA,the corrected I,bothFI substitutions,Rafael/Lil headers,the complete one-page warning andSextant handover areobserved. The existing sailing sharks message isalso seen without new editorial credit. These hosts retain original setup/cleanup whileconcatenating conditional samples;they do not prove natural activation,original outcomes/rewards/geography/chronology,fullroutes orhardware. Allchanged paragraphs areone page;none introduces multipage behavior. The observer's inherited Maria359 label names itsrunner version;fixture/ROM/source IDs areMaria315. No guide photos.

The new ROM's own31,000-frame title/NewGame/Maria opening reaches Hangzhou;all six captures andthe composite aredirectly viewed. The unchanged opening/town captures equalprior approved RGB exactly. Its own snapshot verifiescaptain3/route3,123264 staged bytes and24 original getters for12 protected names. Eight production mutations preservecaller/canonical images whilebeing rejected. All27 selected repository tests pass,terminal0. One initial menu analysis incorrectly received the integer-count summary rather than the approved menu-object receipt;it was rejected. The corrected call passes without changing native guards orreplaying gameplay. Allfailed/superseded producers,plans,pages andROMs remain.

Integrated24,093=14,343 revisions+9,750 retentions;historicalsource/prose/draft count24,096. Exact SC3_v17 census bindsall5,129 native source positions withzero missing orduplicate credit. Remaining native story scope isLil1,805,from `work/story_source_coverage_20261109_SC2_v2/residual_clean_source_packet.json` (6,720 totalpositions). Its old census is an intake locator;qualify source/credit/dependency identities against the current ledger/release before selecting a substantial complete-exchange batch. Its schema lacks the newer selector's inventory flag;use a source-qualified projection orversioned adapter,not a blind flag insertion orrerun ofcompleted inventories. Clean meanings/drafts must precede current-English extraction. Preserve coverage credit andall earlier translations. Shared/shop/town/random/player-facing prose,the broader name review,earlier unfinished contextual passes andearlyRafael/tutorial priority remain fully in scope. Keep deferred artwork andthe later older-record technical re-audit separate. Fullgoalactive;no worker islive.
'''
    checkpoint(mutation=ROOT/'registered_progress_checkpoint_v1', batch_key='editorial_execution_priority_20261104',
        batch_updates=dict(new_credit=0, current_batch='Maria315 B286–B302 registered andcredited once;continue Lil residual andfullshared/player-facing scope.',
            current_batch_not_yet_integrated=False, current_batch_registered_andcredited_once=True,
            all_current_batch_fifth_gates_pending=False, proposed_revisions=162, justified_retentions=153,
            qualified_scoped_names=14, current_batch_actual_gameplay_observations=213, current_batch_actual_gameplay_pages=213,
            current_batch_evidence=evidence, native_job_live=False, native_sessions=[], stored_job_live=False, stored_sessions=[],
            registered_build_live=False, registered_cumulative_build_live=False, no_batch_worker_live=True,
            guide_photos=False, previous_goal_turn_classification='progress', current_goal_turn_classification='progress',
            next_action='Continue clean-first Lil residual using exact SC2_v2 census andcurrent credit/release qualification;retain fullscope.'),
        summary=summary, document=document, document_text=text, completed=24093,
        protected={'translations/release_stack.json': release['registry_sha256'], release['candidate']: release['candidate_sha256'],
            release['manifest']: release['manifest_sha256'], release['patch']: release['patch_sha256'],
            release['canonical_base']: release['canonical_sha256']})
    continuity = Path('docs/build_continuity_protocol.md')
    oldtext = continuity.read_text(encoding='utf-8')
    prefix = ('Maria315 B286–B302 isregistered over Maria349:725 entries,114 accepted layers and60 release checks. '
        'Use `scripts/build_registered_maria315_v1.py` and `--register`;pure transaction:`dk4tool/patch/maria315_release_v1.py`. '
        'All315 source reviews,309 body pages,exact clean-input patch,own startup and24 protected getters pass. '
        'Preserve the724-entry prefix,Market format/both pointers,six-section ARM9,ASCII rightbounds,source25v2 andB164R99 correction. '
        'Native Maria census5129/5129;fullgoalactive. Main requires acceptance. Continue from '
        '[the registered checkpoint](editorial_Maria315_B286_B302_registered_20261110.md);older entries arehistory.\n\n')
    assert not oldtext.startswith(prefix)
    continuity.write_text(prefix+oldtext, encoding='utf-8', newline='\n')
    save(OUT/'handoff_checkpoint.json', dict(document=document, summary=summary, evidence=evidence, new_credit=0, full_goal_complete=False))
    print('Published24093 integrated reviews;Maria native censuscomplete,Lil1805 andfullsharedscope remain;main unchanged.')


if __name__ == '__main__':
    main()
