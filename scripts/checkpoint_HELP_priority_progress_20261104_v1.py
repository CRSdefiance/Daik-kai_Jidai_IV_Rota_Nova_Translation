"""Save tutorial progress and the targeted terminology amendment without new completion credit."""
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.save_editorial_progress_checkpoint_v4 import checkpoint

def digest(path):
    return sha(Path(path).read_bytes())

TOWN = 'work/analysis/Town_HELP23_release_verified_20261104/registered_release_verification.json'
PREP = 'work/analysis/Shipyard_HELP37_release_v2_20261104/registered_preparation.json'
FINAL37 = 'translations/help_shipyard37_contextual_final_review_v3.json'
FINAL22 = 'translations/help_sea22_contextual_final_review_v1.json'
FINAL66 = 'translations/help_fleet66_Command_contextual_amendment_v1.json'
PLAN37 = 'work/analysis/Shared_HELP_T44_T80_formatting_20261104/production_plan_v3.json'
PLAN22 = 'work/analysis/Shared_HELP_T81_T102_formatting_20261104/production_plan_v1.json'
PLAN66 = 'work/analysis/HELP66_Command_amendment_20261104/production_plan_v1.json'
DRAFT30 = 'work/analysis/Shared_HELP_T103_T132_clean_20261104/clean_meanings_andfull_drafts_v1.json'
COMPARE30 = 'work/analysis/Shared_HELP_T103_T132_clean_20261104/whole_article_comparisons_provisional_v1.json'
CONTROLS = 'work/analysis/HELP83_current_sail_controls_20261104/control_binding_v1.json'
SUMMARY = ('Rafael/tutorial priority continues. Town Help23 is registered, verified and credited once: '
    '11359 completions (6601 revisions/4758 retentions), current verified 9c5ca87b; main unchanged. '
    'Shipyard37 build73767/PID104848 remains OS-confirmed live; preserve it, then verify its complete stack/patch/own startup. '
    'A missed Leadership/Command mismatch in Help66 is now corrected in a separate five-gate amendment: two native/viewed/observed pages, '
    'one changed page, unchanged continuation216, two returns. Hold all37 new credits until that correction is cumulatively integrated. '
    'Next22 sailing/battle articles pass all five research gates:17 revisions/5 retentions,22 native/viewed/observed pages, '
    'eight wrap refinements and17 returns. Next30 Deck/crew comparisons have7 proposed revisions/23 word-exact retention candidates; '
    'native localization bindings and all display gates remain. No duplicate credit, promotion or guide photos; full scope/all ROMs preserved.')

DOCUMENT = '''# Rafael and tutorial priority: verified Town23, next Help batches

The user's early-game priority remains active: Rafael's storyline and all tutorials first. Every other storyline, shared/town/random exchange, earlier contextual revisit, names, wrapping and glyph scope remains in the goal. No guide-photo collection, promotion, pruning or commit/push is requested.

## Verified and credited

Town Help23 completed once. Current verified experimental ROM is `out/all_routes_combined_town_help23_20261104_candidate.nds`, SHA-256 `9c5ca87bce5c4ace721ad4ce33c8409374eb412349acf4098098c927f08e7a9f`. Registry profile: `all-routes-town-help23-20261104`. Its exact clean-input patch is beside it, SHA-256 `b28729dc948ae5283d4c229ca64fc244edb7a44cd9cf4adcf278d9bffdb046a3`.

Reuse `work/analysis/Town_HELP23_release_verified_20261104/`: complete registered verification, own startup, both Fernan getters and once-only completion receipt. All672 entries,114 accepted layers,26 checks and eight stages pass. Only Help differs from d61. Town23 contributes19 revisions/4 retentions,28 native/viewed pages,15 observed pages/10 articles and13 offline-only pages/articles; six returns. Integrated total11359 =6601 revisions+4758 retentions; source/prose counters11362 retain the historical three-record offset. Main/canonical base remain unchanged.

## Running Shipyard37 build and targeted amendment

Build73767/PID104848 began22:55:27 Indianapolis and was OS-confirmed live23:40 on November4. Profile `all-routes-shipyard-help37-20261104`; output `out/all_routes_combined_shipyard_help37_20261104_candidate.nds`; work `work/s37`; expected SHA-256 `763ddb2c76842f4b8231b2147762e1f369937c5203f1c29e032806539dbd6be7`. Do not restart a quiet live build or mutate its registry. Current registry SHA-256 `9d4a352f95f67c847a9ae29f7dd7f93a1a209c79720d070d253d5fe202299c35`. Preparation/qualification: `Shipyard_HELP37_release_v2_20261104/registered_preparation.json` and `Shipyard_HELP37_release_qualification_v2_20261104/qualification.json` under work/analysis.

The frozen37 final manuscript is `translations/help_shipyard37_contextual_final_review_v3.json`; production plan `work/analysis/Shared_HELP_T44_T80_formatting_20261104/production_plan_v3.json`. Version3 only normalizes ten retention decision labels to the registered schema. Preserve initial failed preparation receipt in `Shipyard_HELP37_release_20261104/failure_receipt_v1.json`; no registry mutation occurred on that failure. All38 page proofs and original37 prose decisions remain useful, but Help66's old Leadership term is superseded below.

Concrete follow-up: clean Help66 says 統率力150以上; current native stat labels at ARM9 offsets0x131EB4 and0x148324 both say Command. The older Leadership wording was a missed terminology defect. A separate amendment changes only that term, preserving every fleet/funding/policy fact and two source-bound logical paragraphs. `translations/help_fleet66_Command_contextual_amendment_v1.json` and `work/analysis/HELP66_Command_amendment_20261104/production_plan_v1.json` pass all five research gates. Two complete native pages and one native sheet viewed;23481-frame ordinary Help traversal observes both pages, exact full masks/widgets and two history returns; actual sheet viewed. Topic66 alone changes; continuation216 is byte-identical. Rejection checks cover the wrong stat, corrupted continuation and missing localization gate. Its research ROM is pinned. A rejected capture-every0 CLI invocation never started an emulator; the corrected positive interval run completed. Do not edit the frozen original37 manuscript or repeat its unaffected checks.

Let37 finish and preserve it as an experimental intermediate for the corrective successor. Prepared `scripts/verify_shipyard_HELP37_registered_release.py` can verify all673 entries,114 layers,eight stages and exact clean-input patch; then run `verify_registered_shipyard_HELP37_startup.py` on the completed4001-frame capture `work/analysis/Shipyard_HELP37_identity_coldboot_20261104/capture_report.json` and run the own Fernan getter verifier. These are technical checks; they do not approve the known old Help66 term. No37 completion credit until the Command amendment is included and verified in a registered cumulative successor. Prefer combining it with the already reviewed22 below; no new main promotion.

## Next22: all research gates complete

`translations/help_sea22_contextual_final_review_v1.json` covers81–102:17 revisions/5 exact-wording retentions,22 native/viewed pages,all22 observed in31801 ordinary Help frames,zero offline-only,17 history returns. Both sets of six readable sheets were directly viewed. `work/analysis/Shared_HELP_T81_T102_formatting_20261104/production_plan_v1.json` and its bound source/native/actual evidence are ready for registered integration. Eight wrapping refinements keep tip markers, control phrases and tails together without shortening prose or adding pages. Reuse these exact proofs when composing the Command correction; bind unchanged22 page bytes and their runtime dependencies explicitly rather than replaying them.

Substantive corrections include B then A for cancelling Auto Move, the missing A/B sail controls, independent search risks versus failure-only fatigue, categorical At War versus friendship rating, enemy exclusive-contract town attacks, native Swords/Quarters/Boarding Leader/Deckhand terms, Eagle Figurehead and the historical Promised Words/Uncharted Waters Online connection. Do not claim a current online service or new physical Eagle fast-time test.

`work/analysis/HELP83_current_sail_controls_20261104/control_binding_v1.json` separately binds actual B/question/A/manual transition and A/B sail opening/closing through a9101-frame inherited-Riga battery run. Town runtime/COMMON/font are byte-exact to that input. No new RAM/code/location/unlock fixture; original save preserved. It is shared sailing evidence, not Rafael story progression or hardware verification. Fourteen common frames match the initial probe. The old generic82C4C bit getter was mislabeled an automatic-mode flag in the older Riga proof: it is0 during observed Auto Sail and2 during anchored manual sailing. Preserve the old proof, use the independent visual/control evidence, and carry this interpretation defect into the later separate older-record technical re-audit. Do not launch that broad audit now.

## Next30: contextual comparisons saved, bindings/display pending

Clean meanings/logical drafts for103–132 are sealed in `work/analysis/Shared_HELP_T103_T132_clean_20261104/clean_meanings_andfull_drafts_v1.json`, before fresh current body extraction. Earlier glossary/body and heading exposure is disclosed; do not claim all English was unseen. Exact source/current references and seven proposed revisions/23 word-exact retention candidates are in `whole_article_comparisons_provisional_v1.json`. Every record has a specific source/context finding or retention reason. All localization gates remain open for native term/control bindings; all formatting gates remain open. No credit.

Proposed fixes concern town scope, missing map zoom control, auto-assignment access, Trade House versus Market, native Send Letter and Quarters. Current accurate explanations of skill thresholds, fatigue, food/water, roles, automatic sail adjustment and individual-ship capture are retained. Verify the current DS map/assignment controls before finalizing104/106; do not assume the old Choose Auto wording is itself an error. Bind stat/room/role labels, finish localization decisions, then run the validated formatter and fresh native/visual checks. All30 current articles have no existing continuations. The initial draft save failed because the destination directory did not exist; its receipt is preserved and the unchanged producer succeeded after creating it.

## Continue efficiently

1. Poll the existing37 build, then run its prepared final technical verifier/patch/startup/getter checks once terminal. Keep new credit at zero until the66 amendment is cumulatively included.
2. Compose the22 reviewed Help articles and the independently qualified66 amendment through a registered successor preserving all eight runtime/name stages. Reuse the unchanged22 native/actual proofs with exact page/dependency bindings. Verify the cumulative clean-input patch and own final startup. Credit each of the original37 and22 records once, including corrected66 only once.
3. Finish native labels/controls and display for the30 Deck tutorials. Continue remaining Help133–201 excluding already completed181/184, then Rafael progression and the rest of the preserved goal.

Every generated ROM, earlier translation and evidence is preserved. Unresolved graphics artwork and the later older-record technical re-audit remain separate. Canonical base remains3cb827e4c52ab2086fb5a626835d72192085a958581279d3c79b0200bbf405fe. Full editorial objective is active.
'''

if __name__ == '__main__':
    protected = {p:digest(p) for p in [TOWN,PREP,FINAL37,FINAL22,FINAL66,PLAN37,PLAN22,PLAN66,DRAFT30,COMPARE30,CONTROLS]}
    protected.update({
        'translations/release_stack.json':'9d4a352f95f67c847a9ae29f7dd7f93a1a209c79720d070d253d5fe202299c35',
        'out/all_routes_combined_town_help23_20261104_candidate.nds':'9c5ca87bce5c4ace721ad4ce33c8409374eb412349acf4098098c927f08e7a9f',
        'out/raphael_natural_v2_accepted_base.nds':'3cb827e4c52ab2086fb5a626835d72192085a958581279d3c79b0200bbf405fe'})
    checkpoint(mutation='work/analysis/Editorial_checkpoint_Town23_HELP37_22_66_30_20261104',
        batch_key='shared_HELP_T44_T80_contextual_20261104',
        batch_updates=dict(new_credit=0,manuscript=FINAL37,manuscript_sha256=digest(FINAL37),formatting_plan=PLAN37,
            registered_parent_still_pending=False,registered_build_live=True,registered_build_session=73767,registered_build_PID=104848,
            registered_preparation=PREP,registered_preparation_sha256=digest(PREP),registered_integration_pending=True,
            research_checks_complete=True,original37_research_complete_but_one_term_superseded=True,
            term66_amendment=FINAL66,term66_amendment_sha256=digest(FINAL66),
            all37_credit_held_until_Command_amendment_registered_andverified=True,all37_individual_five_gates_pass=True),
        additional_updates={
            'shared_HELP_T81_T102_contextual_20261104':dict(new_credit=0,contextual_comparisons=22,proposed_revisions=17,justified_retentions=5,
                first_four_gates_passed=22,all22_individual_five_gates_pass=True,all_fifth_gates_pending=False,
                manuscript=FINAL22,manuscript_sha256=digest(FINAL22),formatting_plan=PLAN22,
                fresh_native_pages=22,native_andvisually_approved_pages=22,actual_gameplay_pages=22,actual_gameplay_records=22,
                offline_only_pages=0,offline_only_articles=0,ordinary_Help_frames=31801,history_returns=17,eight_wrap_refinements=True,
                all_localization_controls_terms_display_andintegration_pending=False,registered_integration_pending=True,
                shared_physical_control_binding=CONTROLS,shared_physical_control_binding_sha256=digest(CONTROLS),guide_photos=False),
            'editorial_execution_priority_20261104':dict(new_credit=0,current_batch='shared_HELP_T44_T80_contextual_20261104',
                next_batch='shared_HELP_T81_T102_contextual_20261104',next_help_batch='shared_HELP_T103_T132_contextual_20261104',
                previous_town_HELP23_registered_verified_andcredited_once=True,
                registered_build_session=73767,registered_build_PID=104848,registered_cumulative_build_live=True,
                current_body_pages_native_andvisually_reviewed=38,current_batch_not_yet_integrated=True,
                next37_all_five_gates_research_ready=True,next22_all_five_gates_research_ready=True,
                current37_term66_superseded_by_qualified_amendment=True,integrate_amendment_before_new37_credit=True,
                next_source_meanings=30,next_independent_drafts=30,next_source_drafts=30,next_contextual_comparisons=30,
                next30_proposed_revisions=7,next30_word_exact_retention_candidates=23,
                next30_native_localization_andall_display_gates_pending=True,
                later_older_record_reaudit_note='HELP83_current_sail_controls_20261104/control_binding_v1.json: older82C4C bit accessor is not an automatic-mode flag.',
                guide_photos=False,full_editorial_scope_preserved=True)},
        new_entries={
            'shared_HELP66_Command_amendment_20261104':dict(new_credit=0,manuscript=FINAL66,manuscript_sha256=digest(FINAL66),
                formatting_plan=PLAN66,all_individual_five_gates_pass=True,actual_gameplay_pages=2,actual_gameplay_records=1,
                ordinary_Help_frames=23481,history_returns=2,only_one_stored_page_changes=True,continuation216_byte_exact=True,
                registered_integration_pending=True,no_duplicate_original37_credit=True),
            'shared_HELP_T103_T132_contextual_20261104':dict(new_credit=0,source_topics=30,source_topic_IDs=list(range(103,133)),
                source_meanings=30,sealed_source_drafts=30,contextual_comparisons=30,proposed_revisions=7,word_exact_retention_candidates=23,
                draft=DRAFT30,draft_sha256=digest(DRAFT30),comparisons=COMPARE30,comparisons_sha256=digest(COMPARE30),
                first_four_gates_passed=0,all_localization_native_binding_gates_pending=True,all_fifth_gates_pending=True,
                registered_integration_pending=True,full_editorial_scope_preserved=True)},
        coverage_unit_updates={'help-and-other-player-facing-prose':dict(status='in-progress',active_batch='shared_HELP_T103_T132_contextual_20261104',
            progress_evidence=COMPARE30,progress_evidence_sha256=digest(COMPARE30))},
        summary=SUMMARY,document='docs/editorial_town_integrated_help37_build_sea22_fleet66_20261104.md',
        document_text=DOCUMENT,completed=11359,protected=protected)
    print('Priority checkpoint saved:11359 integrated;37/22/66/30 progress exact, no new credit or promotion.')
