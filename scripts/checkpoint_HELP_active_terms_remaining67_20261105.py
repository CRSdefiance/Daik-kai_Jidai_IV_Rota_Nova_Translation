"""Preserve the corrected active-term review,remaining67 comparisons and exact running-job state."""
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.audit_story_glyph_consistency import load
from scripts.save_editorial_progress_checkpoint_v5 import checkpoint

FINAL='translations/help_deck30_Coerce33_active_terms_final_review_v1.json'
PLAN='work/analysis/HELP31_active_terms_20261105/production_plan_v1.json'
BIND='work/analysis/HELP_active_skill_labels_20261105/active_terms_binding_v2.json'
COMPARISON='work/analysis/Shared_HELP_T133_T201_clean_20261105/whole_article_comparisons_v2.json'
INTAKE='work/analysis/Shared_HELP_T133_T201_clean_20261105/clean_meanings_andall67_drafts_v2.json'
CURRENT='work/analysis/Shared_HELP_T133_T201_clean_20261105/current_full_articles_verified_parent_v1.json'
CONTROLS='work/analysis/Shared_HELP_T133_T201_clean_20261105/remaining_active_terms_andcontrols_v1.json'
NEXTPLAN='work/analysis/Remaining_HELP67_formatting_20261105/refined_v3/automatic_plans_v1.json'
NEXTNATIVE='work/analysis/Remaining_HELP67_formatting_20261105/native_pages_v3/native_help_pages.json'
NEXTQUAL='work/analysis/Remaining_HELP67_formatting_20261105/preview_qualification_v3/qualification.json'
FINAL67='translations/help_remaining67_contextual_final_review_v1.json'
PROD67='work/analysis/Remaining_HELP67_formatting_20261105/production_plan_v1.json'
LOOKUP='work/analysis/ROM_path_lookup_memory_20261105/equivalence_v1.json'
RETRY='work/analysis/Sea22_Fleet66_lookup_retry_20261105'

if __name__=='__main__':
    assert load(FINAL)['all31_individual_five_gates_pass'] and load(COMPARISON)['first_four_gates_passed']==67
    assert load(NEXTNATIVE)['native_pages']==72 and load(NEXTQUAL)['all_native_andvisual_pages_pass']
    assert load(FINAL67)['all67_individual_five_gates_pass']
    request=load(Path(RETRY)/'request.json')
    assert not load(Path(RETRY)/'completion.json')['driver_completed_without_exception']
    assert not load('work/analysis/Sea22_Fleet66_gc_retry_20261105/completion.json')['driver_completed_without_exception']
    summary=('Rafael/tutorial priority preserved. Corrected31 research now has all five gates:30 new-source candidates(10 revisions/20 retentions) pluszero-credit Coerce33 amendment; '
        'active Vigor/Speech/Guile confirmed,earlier Health/Social/Tactics inference superseded. Six fresh native andnine fresh actual pages useexact prior proofs forremaining pages. '
        'All67 remaining Help reviews passfive gates:7 revisions/60 exact-body retentions. All72 native/viewed pages pass,217 topics/five old continuations preserved; '
        '25 actual pages/20 articles,47 offline-only pages/articles and15 returns pass. Registered integration remains. Two ordinary UI probes confirmY equipment,Left/Right,Y Auto,Flagship/Even/Minimum;no consumable/full-playthrough claim. '
        'Allthree675 attempts ended1 beforeoutput;path-lookup optimization passed5 tests/all-file equivalence buthistorical source lock rejected it. Original core restored exactly;no live release build. '
        'No live jobs. All202 Help source topics havefive-gate research decisions;156 remain uncredited pendingintegration. '
        '11359 integrated/current9c5/main unchanged;zero new credit,no guide photos,all ROMs/full scope preserved.')
    document='''# Active tutorial terms and remaining Help — November 5, 2026

Rafael's early story and all tutorials remain first. The full editorial objective, earlier translations, justified retentions, coverage, names, all routes/shared/town/random prose and every ROM/evidence artifact remain preserved. No guide-photo collection, promotion, pruning or commit/push. Continue Rafael's remaining contextual story work after the tutorial queue; choose uncompleted scope from the ledger.

## Corrected active labels and31 complete research reviews

The previous static-string inference was wrong: actual active skills are **Vigor / Speech / Guile**, not Health / Social / Tactics. `HELP_active_skill_labels_20261105/active_terms_binding_v2.json` binds active pointers in the verified37 own RAM, all10 complete actual character-screen font masks, six attributes, moods/conditions and21 active room references. There are three distinct reviewed navigation frames8200/8400/8600; the second final8600 image is a duplicate. Historical strings and the old Help30 manuscript remain preserved but are superseded for the five skill decisions. Physical Health and the Tactics room are distinct valid labels; do not globally rename them. Command remains confirmed active.

`translations/help_deck30_Coerce33_active_terms_final_review_v1.json` and `HELP31_active_terms_20261105/production_plan_v1.json` now pass all five individual gates. Thirty new-source candidates have10 revisions/20 word-exact retentions, plus a zero-new-credit correction of already credited Coerce33 from Persuasion to Speech200. Eleven revised records in the combined31 are not31 new completions. Three restored Deck bodies now count as retentions, so old13/17 totals are superseded.

Six pages33/116/117/118/121/126 received fresh native rendering and two directly viewed sheets;25 exact native/visual proofs were reused. A26361-frame ordinary Help run freshly observed nine pages, including all six changed pages and three unchanged connectors. Three actual sheets were directly viewed. The final disjoint composition uses nine fresh plus22 exact prior actual observations; every encoded page/runtime/COMMON/font/capture binding is checked. This is not a single31-page new playthrough. All31 current pages have observations across the identified research ROMs. Six inactive-name regression cases reject. Registered integration remains; no credit or main change.

## All remaining67 contextual decisions and72 viewed native pages

`Shared_HELP_T133_T201_clean_20261105/clean_meanings_andall67_drafts_v2.json` preserves all clean meanings/drafts. The first failed draft caught a missing150 link before output; its receipt/source are archived. `current_full_articles_verified_parent_v1.json` freshly binds all67 complete current articles from verified37, including all five continuations. Earlier English exposure is disclosed.

`whole_article_comparisons_v2.json` records all67 individual source/context/localization/naturalness decisions: seven proposed revisions and60 justified exact-body retentions. `translations/help_remaining67_contextual_final_review_v1.json` and `Remaining_HELP67_formatting_20261105/production_plan_v1.json` now seal all67 individual five-gate reviews. Corrections restore Y item operations, current crew policy captions, Trade House rather than the separate Market, Coerce rather than Threaten, and the native Product category with a natural Products (Raw Materials) heading. All active skill/attribute/condition terminology is retained where correct. Existing correct strict greater-than500 percent, three basic diplomatic relations plus Subordinate, fleet-count bonus share and food-only conservation are retained. No extra mechanics were invented.

`remaining_active_terms_andcontrols_v1.json` binds nine additional labels through original pointer references to current own RAM: Sextant, Product and seven city statuses. Two focused actual UI runs total15800 frames and24 distinct directly viewed navigation states. The Riga run confirms Left/Right crew adjustment, Y Auto, Flagship/Even/Minimum, Even selection and X/A return. The Istanbul run confirms Y removal, Y equipment selection and re-equipping Golden Cutlass to Hodram, plus three item displays. Both use isolated copies of preserved historical batteries, no new RAM/code/location fixture or savestate. Donors are unchanged. Historical equipment acquisition was not revalidated; consumable use, red-name warning, alternate city conditions and the67 revised Help pages were not newly activated by these UI probes. No new Rafael progression, hardware or full-playthrough claim.

`Remaining_HELP67_formatting_20261105/refined_v2/automatic_plans_v1.json` plans72 pages across67 articles with217 topics. All five existing continuation owners133→209,139→210,150→206,151→207,168→208 are reused; every unowned topic/sentinel and complete parent inverse is exact. The first74-page plan and initial source-guard derivation failure are preserved. The refined plan avoids two unnecessary extra pages without shortening retained prose: Product/raw-material explanation belongs in the heading, and Market Share's prerequisite begins a complete page. Source table entries and source concepts are semantic sections; the formatter owns line breaks. Trade House, menu/range phrases and auxiliary masts remain continuous.

All72 pages received fresh complete native glyph/font/widget/row/bounds/leading-trailing/allocation checks and direct visual review on18 readable sheets. Nine phrase-tail findings were then fixed without wording changes: change their job, Press Left or Right, when attacked, in a crisis, such as sailing, It is, It suits, this faction, better relations. Final v16/refined_v3 keeps72 pages/217 topics and every word/page count/owner. Nine changed pages received fresh native checks and direct review onthree sheets;63 byte-exact native/approved-visual proofs were reused. `preview_qualification_v3/qualification.json` makes a pinned, reversible Help-only research image. The13 control/label/threshold/source/gate/link/foreign-owner rejections are reused under an exact semantic-guard source comparison, not bypassed. All final per-record formatting gates now pass. Registered integration remains. No new completion credit.

Focused ordinary Help capture29904/PID101860 is terminal0, under `Remaining_HELP67_formatting_20261105/focused_navigation_v1/`. Its42361 frames use the existing cold-boot entry schedule, no battery/savestate/fixtures. `focused_navigation_checked_v1/ordinary_gameplay_verification.json` verifies all25 selected complete pages/20 articles, native child targets and15 full title/body history returns across all five continuation forward/back/L/R cases. Seven readable actual sheets were directly viewed and approved. All47 other pages/articles are explicitly offline-only. This is targeted automated emulator evidence, not a full story playthrough or hardware test. Reuse these completed checks; no live jobs remain.

##675 registered cumulative build: three failures preserved, locked core restored

Reuse the technical37 full registry/startup/clean-patch/Fernan proofs and all existing22 sea/66 amendment proofs from [the previous checkpoint](editorial_HELP30_ready_cumulative_build_20261105.md). Hold37 credit until the Command amendment is cumulatively verified. Original session13641/PID68120 failed with Unicorn memory allocation; `Sea22_Fleet66_build_failure_20261105/failure_receipt.json` preserves it. GC-only retry71881/PID79640 also ended1 before a candidate, this time copying unrelated file payloads during path lookup. Its completion, traceback and telemetry remain under `Sea22_Fleet66_gc_retry_20261105/`; all nine registered driver/registry bytes stayed unchanged.

An optimized path lookup avoided unrelated payload copies, passed five targeted/synthetic tests and every-map/every-read equivalence across clean/accepted/planned675 ROMs. The third attempt31586/PID113740 nevertheless correctly stopped at the historical Hodram outcomes exact dependency lock for `dk4tool/rom/nds.py`. All original guards and registry/driver bytes stayed intact. Preserve its terminal completion/traceback under `Sea22_Fleet66_lookup_retry_20261105/`. No final candidate or patch was emitted. Do not rerun this optimization under the same locked pipeline.

The original dependency-locked core is restored byte-for-byte. Optimization source and its tests are archived as `ROM_path_lookup_memory_20261105/nds.payload_free_RESEARCH_ONLY.py` and `test_rom_path_lookup_RESEARCH_ONLY.py`; the normal test suite has no optimization-dependent failing test. `locked_core_restoration.json` records both identities and why the optimization is not adopted. Two ordinary synthetic ROM/CLI tests pass after restoration. No guard or expected digest was rewritten. There is **no live registered release build**. Preserve `work/s22f66`, `work/s22f66g`, `work/s22f66p` and all failure receipts. Any further build attempt must address the concrete memory risk without silently changing this locked dependency, and should not repeat the same failed attempt while other emulator/native jobs are consuming memory.

Registered profile remains `all-routes-sea22-fleet66-20261104`, registry82a17be4, expected81511dde target. All114 accepted layers/eight stages/26 checks remain mandatory, including ASCII bounds and Fernan's F. The earlier4001-frame planned own startup is preserved; final registered equality/own RAM/getters/manifest/patch binding remain. No intermediate image is a handoff candidate.

After terminal0, prepare the two-layer final verifier and once-only completion. Required source credit remains59=37+22 (44 revisions/15 retentions), not60;66 is an amendment. Refresh all integrated archive offsets and bind60 native pages,39 observed pages/38 articles and21 offline-only pages. Final page66/216 observations must come from the Command amendment. Expected totals only after verification:11418 completions=6645 revisions+4773 retentions; source/prose11421. The corrected Deck30/Coerce33 and final67 then require ordered registered successors, reusing exact existing proofs instead of new full playthroughs.

## Authoritative totals and next actions

Integrated total remains **11359=6601 revisions+4758 retentions**, source/prose11362. Editorial current remains Town9c5ca87b; verified37 is technical only with credit held. Accepted main remains3cb827e4. All202 clean Help topics now have five-gate research decisions:46 credited and156 awaiting ordered registered integration (37+22+30+67; amendments add no source credit). This is tutorial scope, not full-goal completion. Preserve unresolved graphics artwork and the later older-record technical re-audit, including the earlier generic-bit/AutoMove interpretation lead. No promotion is authorized by passing automated checks.
'''
    paths=[FINAL,PLAN,BIND,COMPARISON,INTAKE,CURRENT,CONTROLS,NEXTPLAN,NEXTNATIVE,NEXTQUAL,LOOKUP,FINAL67,PROD67]
    protected={p:sha(Path(p).read_bytes()) for p in paths}
    protected.update({'translations/release_stack.json':'82a17be4f7610abef225fa39c2059cd4180511af5683f519aec8171de3df5f4e',
        'out/all_routes_combined_town_help23_20261104_candidate.nds':'9c5ca87bce5c4ace721ad4ce33c8409374eb412349acf4098098c927f08e7a9f',
        'out/raphael_natural_v2_accepted_base.nds':'3cb827e4c52ab2086fb5a626835d72192085a958581279d3c79b0200bbf405fe',
        'dk4tool/rom/nds.py':load(LOOKUP)['prior_sha256']})
    live=dict(new_credit=0,registered_cumulative_build_live=False,registered_build_live=False,build_live=False,
        registered_build_session=31586,registered_build_PID=113740,build_session=31586,build_PID=113740,
        original_build_terminal_exit_code=1,GC_only_retry_terminal_exit_code=1,path_lookup_retry_terminal_exit_code=1,qualified_path_lookup_equivalence=LOOKUP,
        original_locked_ROM_core_restored=True,path_lookup_optimization_research_only=True,
        retry_request=str(Path(RETRY)/'request.json'),registered_integration_pending=True)
    checkpoint(mutation='work/analysis/Editorial_checkpoint_HELP_active_terms_remaining67_20261105',
        batch_key='shared_HELP_T103_T132_contextual_20261104',batch_updates=dict(new_credit=0,manuscript=FINAL,
            manuscript_sha256=sha(Path(FINAL).read_bytes()),formatting_plan=PLAN,proposed_revisions=10,justified_retentions=20,
            word_exact_retention_candidates=20,first_four_gates_passed=30,all30_individual_five_gates_pass=True,
            combined31_with_zero_credit_Coerce33_amendment=True,fresh_native_pages=6,exact_reused_native_pages=25,
            native_andvisually_approved_pages=31,actual_gameplay_pages=31,fresh_actual_pages=9,exact_reused_actual_pages=22,
            distinct_new_source_articles=30,previously_credited_amendments=[33],all_fifth_gates_pending=False,
            previous_static_skill_inference_superseded=True,active_terms_binding=BIND,registered_integration_pending=True),
        additional_updates={
            'shared_HELP_T81_T102_contextual_20261104':live,
            'shared_HELP66_Command_amendment_20261104':live,
            'sea22_fleet66_registered_cumulative_20261105':live,
            'shared_HELP_T133_T201_contextual_20261105':dict(new_credit=0,source_meanings=67,sealed_source_drafts=67,
                remaining_independent_drafts=0,contextual_comparisons=67,first_four_gates_passed=67,proposed_revisions=7,justified_retentions=60,
                draft=INTAKE,draft_sha256=sha(Path(INTAKE).read_bytes()),current_packet=CURRENT,comparisons=COMPARISON,
                comparisons_sha256=sha(Path(COMPARISON).read_bytes()),formatting_plan=NEXTPLAN,native_proof=NEXTNATIVE,preview_qualification=NEXTQUAL,
                fresh_native_pages=72,native_andvisually_approved_pages=72,all18_initial_andthree_refinement_native_sheets_directly_viewed=True,
                final_changed_pages_fresh_native=9,final_exact_reused_native_pages=63,nine_phrase_tail_refinements_resolved=True,
                current_topics_preserved=217,five_existing_continuation_owners_preserved=True,all_fifth_gates_pending=False,all67_individual_five_gates_pass=True,
                manuscript=FINAL67,manuscript_sha256=sha(Path(FINAL67).read_bytes()),production_plan=PROD67,
                all_current_comparisons_native_display_andintegration_pending=False,focused_Help_navigation_andintegration_pending=False,registered_integration_pending=True,
                actual_current_UI_control_binding=CONTROLS,actual_control_frames=15800,actual_Help_pages=25,actual_Help_articles=20,
                offline_only_pages=47,offline_only_articles=47,actual_Help_frames=42361,history_returns=15,
                focused_Help_navigation_live=False,focused_Help_terminal_exit_code=0,focused_Help_session=29904,focused_Help_PID=101860,
                all_seven_actual_sheets_directly_viewed=True,guide_photos=False),
            'editorial_execution_priority_20261104':dict(**live,current_batch='shared_HELP_T133_T201_contextual_20261105',
                next_batch='shared_HELP_T103_T132_contextual_20261104',next30_proposed_revisions=10,next30_word_exact_retention_candidates=20,
                next30_all_five_gates_research_ready=True,next_source_meanings=67,next_independent_drafts=67,next_source_drafts=67,
                next_contextual_comparisons=67,remaining_HELP_independent_drafts=0,remaining_HELP_four_gate_passes=67,
                remaining_HELP_five_gate_passes=67,all202_HELP_source_topics_five_gate_research_ready=True,
                full_editorial_scope_preserved=True,guide_photos=False)},
        new_entries={'shared_HELP33_Speech_amendment_20261105':dict(new_credit=0,previously_credited=True,
            source_article_id=33,manuscript=FINAL,all_five_gates_research_pass=True,registered_integration_pending=True)},
        coverage_unit_updates={'help-and-other-player-facing-prose':dict(status='in-progress',active_batch='shared_HELP_T133_T201_contextual_20261105',
            progress_evidence=COMPARISON,progress_evidence_sha256=sha(Path(COMPARISON).read_bytes()))},
        summary=summary,document='docs/editorial_HELP_active_terms_remaining67_20261105.md',document_text=document,completed=11359,protected=protected)
    print('Checkpoint preserves11359 completions,corrected31 andremaining67 five-gate research,25 actual/47 offline Help pages andthree preserved build failures. No live jobs;full goal remains active.')
