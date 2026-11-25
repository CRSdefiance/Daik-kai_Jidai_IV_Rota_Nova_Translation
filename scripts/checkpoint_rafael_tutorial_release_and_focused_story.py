"""Save verified tutorial integration and bounded next-story evidence without duplicate credit."""
from pathlib import Path
from scripts.audit_story_glyph_consistency import load,save
from scripts.save_editorial_progress_checkpoint_v3 import checkpoint
from dk4tool.patch.grand_race_menu_release import sha

ROOT=Path('work/analysis/Rafael_early_tutorial_release_verified_20261104')
NEXT=Path('work/analysis/Rafael_B36_B41_focused_actual_pixels_20261104')
TOOLTIP=Path('work/analysis/First_Mate_shared_tutorial_20261104/contextual_tooltip_review_v1.json')

if __name__=='__main__':
    release=load(ROOT/'registered_release_verification.json');completion=load(ROOT/'completion_checkpoint.json')
    assert completion['new_credit']==40 and completion['counts']['completed']==10346
    assert release['clean_input_patch_byte_exact'] and not release['own_registered_startup_pending']
    pixels_path=NEXT/'focused_actual_pixels.json';pixels=load(pixels_path)
    assert pixels['frames']==10001 and (pixels['selected_utterances'],pixels['selected_pages'],pixels['complete_body_planes'])==(16,18,40)
    assert pixels['all_selected_pages_observed_in_exact_fixture_order'] and len(pixels['review_sheets'])==3
    approval_path=NEXT/'direct_visual_approval.json';assert not approval_path.exists()
    for sheet in pixels['review_sheets']:assert sha(Path(sheet['path']).read_bytes())==sheet['sha256']
    save(approval_path,dict(read_only_pixel_proof=str(pixels_path),read_only_pixel_proof_sha256=sha(pixels_path.read_bytes()),
        all_three_sheets_directly_viewed=True,all18_selected_pages_readable_andcomplete=True,findings=[],
        full_FU_Rafael_Castor_andboth_ASCII_I_andfour_wrap_fixes_viewed=True,
        both_two_page_boundaries_andfollowing_selected_utterances_viewed=True,
        all11_progressive_nameplates_visually_complete_andconsistent_with_bound_getters=True,
        independent_per_string_header_pixel_binding_still_pending=True,
        original_scene_background_not_tested_fixture_uses_opening_art=True,
        actual_utterances=16,offline_only_utterances=159,natural_activation=False,full_route=False,hardware=False,new_credit=0,guide_photos=False))
    rebuilt_path=Path('work/analysis/Rafael_B36_B41_rebuilt_20261104/reconstruction.json')
    loaders_path=Path('work/analysis/Rafael_B36_B41_loaders_20261104/verification.json')
    rebuilt,loaders=map(load,[rebuilt_path,loaders_path])
    assert rebuilt['parent_sha256']==release['candidate_sha256'] and rebuilt['full_clean_current_block_archive_andserialized_NDS_inverses_exact']
    assert (loaders['fresh_whole_archive_loads_andcache_hits'],loaders['fresh_parent_cases'],loaders['exact_reused_parent_cases'])==(343,12,674)
    tooltip=load(TOOLTIP);assert len(tooltip['records'])==1 and not tooltip['records'][0]['review']['formatting']
    summary=('Rafael tutorials B42/B43 integrated andcredited once:40 reviews,19 revisions/21 retentions;10346 complete '
        '(6177 revisions/4169 retentions). Experimental c555f555:665 entries,114 accepted layers,six final stages,exact clean patch andown Rafael startup pass;main unchanged. '
        'Next175 reviews composed on that successor:177 offline pages,343 archive loads and12 fresh/674 reused handoffs pass. '
        'Focused10001-frame test observes16 utterances/18 pages/40 complete body planes;three QA sheets viewed. '
        'Scoped header pixel proof/final gates andregistration remain;159 utterances offline-only. First Mate tooltip revision saved,pending display. '
        'No live jobs;full scope/all prior work/ROMs retained;no guide photos.')
    document=Path('docs/editorial_rafael_tutorial_release_and_focused_story_20261104.md')
    text=f'''# Verified Rafael tutorials and focused story checkpoint

The preceding goal turn made progress: all175 current text bodies passed native catalogue lookup and the full contextual/stored-display checkpoint was saved. This turn completes registered integration of the earlier40 tutorials and advances the175-record successor. The full goal remains active.

## Verified experimental tutorial release

Candidate: `{release['candidate']}`. SHA256 `{release['candidate_sha256']}`. Profile: `{release['profile']}`. Canonical accepted base remains `{release['canonical_base']}`, SHA256 `{release['canonical_sha256']}`. All665 manifest entries,114 accepted layers and24 checks pass; allsix final stages,including ASCII right bounds,remain. Only SC0 B42/B43 differ from experimental88e9984f. Every other file/component,runtime,font,graphic andearlier name isexact.

Patch: `{release['patch']}`, SHA256 `{release['patch_sha256']}`. Clean input SHA256 `{release['clean_input_sha256']}`. Applying the patch reconstructs the complete candidate byte forbyte. Manifest SHA256 `{release['manifest_sha256']}`;registry SHA256 `{release['registry_sha256']}`. Release/startup/exact40 source-current-final bindings/once-only credit receipts are in `{ROOT}`. Build15896 is terminal exit0; the failed4941 long-path tree remains preserved. Do not restart either.

Its4001-frame ordinary Rafael coldboot passes captain0/route0,own fresh complete RAM/payload/native getters andallten exact prior reviewed PNG pairs. This coldboot used the frozen research image with the exact same c555f555 bytes while the registered reconstruction finished; the subsequent manifest andwhole-ROM equality prove the captured image isbyte-identical to the final candidate. No old RAM overlay,savestate,battery orroster/location/RNG override. The capture report retains the research filename honestly. Reused body/gameplay evidence isstill the completed25002-frame two-tutorial fixture coverage:42 ordered pages,92 complete body planes,five headers andtwo reviewed sheets. Natural event activation,original locations,earned chronology,fullroute andhardware remain unvisited. Main promotion still requires user acceptance; this isexperimental.

The40 tutorials arecredited once:19 revisions/21 justified retentions. Coverage is10346 completions,6177 integrated revisions and4169 retentions; historical source/prose/draft counters10349. All earlier keys/record prefixes areexact. No duplicate credit for existing Julio ASCII repair.

## Next six complete exchanges

The175 comparisons (76 revisions/99 retentions),four wrap fixes,two ASCII-I fixes and177 approved offline pages remain as documented in [the stored review](editorial_rafael_B36_B41_stored_review_20261104.md). All source/current/individual findings remain in `translations/rafael_B36_B41_contextual_editorial_manuscript_v1.json`. Numeric adjacency isnot gameplay chronology: B40 isexplicitly a later Hayreddin rematch.

`{rebuilt_path}` now composes the six already-tested blocks on verified c555f555 andpreserves B42/B43. Complete archive andserialized whole-ROM inverses pass. ARM9,COMMON,font,all actor bytes andall six source blocks exactly match the prior research dependencies,so the177 stored-page and400 relative-case proofs are reused explicitly rather than repeated. This research ROM isnot a registered release. Two proposed catalogue-name fields areunapplied andremain separately pending.

`{loaders_path}` passes343 whole native archive loads/cache hits,12 fresh handoff cases for B36–B41 and674 exact tutorial-parent reuses. All original loader instructions match. The fixture producer initially rejected its own too-short terminal-byte comparison before creating output; the corrected source-equivalent check preserves the entire command including native allocation padding. No shipped source byte changed for that host assertion.

The bounded initialized display fixture selects16 exact speech commands: one for each of11 actors plus six concrete wrap/glyph risks (with overlaps). It preserves all selected six-byte preambles andstored bodies,original Rafael opening initializers andfull unowned-file/component/serialized inverse. It deliberately omits scene condition/branch/economic effects and159 other utterances; this is a synthetic QA sequence,not a story exchange. Original opening artwork remains visible. All175 conversations were reviewed offline; no claim of159 additional gameplay observations.

Run91536 isterminal exit0 at10001frames. Its read-only observer restores every host slot andleaves the core exact. All18 ordered selected pages match40 complete body planes,including blank guards. Both page transitions,the complete FU Rafael Castor expansion,two normal ASCII-I glyphs andall four wrap fixes pass. Three readable QA sheets were directly viewed,covering all18 pages andall11 complete progressive nameplates. The selected follow-on utterances verify page-to-next-speech progression. Independent per-string header pixel binding andfinal scoped name/formal fifth-gate review remain before registration. No need to repeat the body run orall175 prose/format checks.

Fixture: `work/analysis/Rafael_B36_B41_focused_actual_fixture_20261104/focused_fixture.json`. Terminal: `work/analysis/Rafael_B36_B41_focused_actual_run_20261104/terminal.json`. Capture: `work/emulation_v193/Rafael_B36_B41_focused_20261104/capture_report.json`. Pixel andvisual approvals: `{NEXT}`. Original source context andfull instructions remain inthe prior evidence. Actual labels look complete; Salid Ajar andArcadius Eudoxios match bound names. The Pedro de/Barbarossa Fazul catalogue-only proposals have no changed full-catalogue UI observation or deployment credit.

## Shared beginner tooltip

`{TOOLTIP}` saves one complete clean-source/current-panel contextual correction: use First Mate rather than adjutant,to match the visible assignment selector andJulio's tutorial. The proposed paragraph is With a First Mate,you can send negotiation documents fromthe guild (ordinary spacing retained inthe JSON). Existing enabled action,document type andguild location were correct andretained. Four prose gates pass; consumer-specific layout,complete native panel glyphs/allocation,representative Deck observation andregistered static-data integration remain. No claim ofunconsulted English intake: the old wording was already known fromthe queued finding. Original four-panel manuscript andearlier translations stay unchanged.

Next finish scoped progressive-name pixel proofs/final gates for175,register andintegrate the complete batch,thencontinue Rafael early story/all tutorials. Preserve245 later source speeches,later Hodram drafts,all ROMs andall broader storyline/shared/town/random/player-text scope. No main promotion,commit/push,pruning orguide photos. Graphics artwork andthe later older-record technical re-audit remain separate.
'''
    checkpoint(mutation=ROOT/'tutorial_release_andfocused_story_checkpoint_mutation_v1',batch_key='Rafael_SC0_B36_B41_contextual_20261104',
        batch_updates=dict(new_credit=0,research_reconstruction=str(rebuilt_path),research_reconstruction_sha256=sha(rebuilt_path.read_bytes()),
            whole_archive_andserialized_ROM_inverses_pass=True,tutorial_successor_preserved=True,archive_loader_verification=str(loaders_path),
            fresh_archive_loads=343,fresh_handoff_cases=12,exact_reused_handoff_cases=674,focused_actual_pixels=str(pixels_path),
            focused_actual_visual_approval=str(approval_path),actual_frames=10001,actual_utterances=16,actual_pages=18,actual_body_planes=40,actual_QA_sheets=3,
            offline_only_utterances=159,independent_header_pixel_binding_pending=True,
            proposed_display_only_dialogue_fix=dict(id='DK4_MES_B37_R0099',current='Ｉ',proposed='I',wording_retained=True,native_formatting_pending=False,actual_display_pass=True),
            remaining=['Scoped progressive-header pixel proof andfinal name/fifth gates','Registered cumulative integration andclean patch/own startup','Once-only credit'],
            all_fifth_gates_pending=True),
        additional_updates={'editorial_execution_priority_20261104':dict(new_credit=0,current_batch='Rafael_SC0_B36_B41_contextual_20261104',
            previous_tutorial_batch_registered_andcredited=True,shared_first_mate_tooltip_followup='shared_First_Mate_tooltip_contextual_20261104')},
        new_entries={'shared_First_Mate_tooltip_contextual_20261104':dict(new_credit=0,review=str(TOOLTIP),review_sha256=sha(TOOLTIP.read_bytes()),
            total_editorial_objects=1,proposed_revisions=1,all_four_prose_gates_pass=True,formatting_andintegration_pending=True,guide_photos=False)},
        completed=10346,summary=summary,document=document,document_text=text,
        protected={'translations/release_stack.json':release['registry_sha256'],release['candidate']:release['candidate_sha256'],
            release['patch']:release['patch_sha256'],'out/raphael_natural_v2_accepted_base.nds':release['canonical_sha256']})
    print('Verified40 tutorial release and16-utterance focused story coverage saved;10346 completions;full goal active.')
