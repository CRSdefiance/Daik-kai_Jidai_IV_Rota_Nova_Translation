"""Preserve complete539 research gates and honest scene coverage before registration."""
from pathlib import Path
from scripts.audit_story_glyph_consistency import load
from dk4tool.patch.grand_race_menu_release import sha
from scripts.save_editorial_progress_checkpoint_v3 import checkpoint

ROOT=Path('work/analysis/Rafael_B61_B80_checked_20261104')
FORMAT=Path('work/analysis/Rafael_B61_B80_formatting_20261104')
if __name__=='__main__':
    final=Path('translations/rafael_B61_B80_contextual_final_review_v1.json')
    status=load(ROOT/'formatting_checkpoint.json');actual=load(ROOT/'actual_review.json')
    release=load('work/analysis/Rafael_B51_B60_release_verified_20261104/registered_release_verification.json')
    rebuilt_path=Path('work/analysis/Rafael_B61_B80_rebuilt_v12_20261104/reconstruction.json');rebuilt=load(rebuilt_path)
    assert status['prose_reviews']==539 and status['all_individual_five_gates_pass_in_research']
    assert all(all(r['review'].values()) for r in load(final)['records'])
    assert (actual['actual_utterances'],actual['actual_body_pages'],actual['offline_only_utterances'])==(95,101,444)
    summary=('Rafael early story and all tutorials remain first. B61–B80 now has539 five-gate research reviews:210 revisions/329 retentions,545 reviewed native/stored pages,22 scoped names,14 layout refinements/16 I fixes/14 ellipsis fixes. '
        'Final initialized tests observe95 utterances/101 pages/all22 headers,all six two-page passages andthe complete66-speech Charlotte CG/action/return scene;444 utterances remain offline-only. '
        'A negative-question/reassurance mismatch is corrected;the brief Here page was a capture gap andis intact. '
        'Registered eight-stage integration/patch remain;zero new credit,10774 integrated completions,verified eb62870b/main unchanged. Full scope/all ROMs preserved;no live jobs or guide photos.')
    document=Path('docs/editorial_rafael_539_research_ready_20261104.md')
    text=f'''# Rafael539: research checks complete — 2026-11-04

Rafael early story and all tutorial work remain first. Keep the full all-story/earlier-translation/shared town-shop/random/name-role/player-prose objective active. Preserve all translations, retentions, credit, ROMs and evidence. No main promotion, pruning, commit/push or guide photographs. Graphics artwork and the later older-record technical re-audit stay separate.

## Verified release remains unchanged

Candidate `{release['candidate']}`, SHA256 `{release['candidate_sha256']}`, profile `{release['profile']}`. Its669 entries/114 accepted layers/eight stages/26 checks, exact clean-input patch, own startup andboth Fernan getters remain verified. Registry SHA256 `{release['registry_sha256']}`. Reuse the release proof under `work/analysis/Rafael_B51_B60_release_verified_20261104`; do not repeat completed checks. Main `{release['canonical_base']}`, SHA256 `{release['canonical_sha256']}` is unchanged.

Integrated totals remain10774 complete/6356 revisions/4418 retentions; this checkpoint adds zero credit. The539 receive completion credit once only after registered cumulative verification.

## Current final review and display

Final individual review `{final}`, SHA256 `{sha(final.read_bytes())}`:539 records,210 revisions/329 justified retentions, all five individual gates true in research. Names: `translations/rafael_B61_B80_scoped_names_actual_final_v1.json`,22 individually retained public names/role labels. Exact clean/current references, original independent drafts and prior versions remain preserved. See `docs/editorial_rafael_539_prose545_body_20261104.md` for the earlier complete prose/context findings; do not restart them.

Latest contextual manuscript `translations/rafael_B61_B80_contextual_editorial_manuscript_v5.json`; formatting input `{FORMAT/'formatting_input_v5.json'}`; plan `{FORMAT/'automatic_v12/automatic_plans.json'}`; final native `{FORMAT/'combined_native_v12.json'}`; approval `{FORMAT/'body_display_approval_v12.json'}`. All539 formatting checks/545 pages pass. Fourteen layout refinements remove two unnecessary pages;16 full-width I letters,14 inconsistent ellipses and19 specifically scoped copied punctuation characters are corrected. Original216px progressive/228px FE geometry, native controls, four rows andregistered ASCII right bounds are preserved. Logical paragraphs remain, with no shortened prose or authored ordinary breaks.

Source539 comprise533 progressive speeches/five Charlotte FE speeches/one funds notice. B68 is an unchanged control-only block. No2100/2200/4100 compound objects occur. The earlier measured R87 FE extra-row/single-letter defect remains fixed. The exact R143 grammatical article-boundary retention remains scoped and documented; no global QA rule is relaxed.

Actual whole-exchange review caught one additional issue: clean 似合わない？ / そんなことないよ！ expresses insecurity/reassurance, while proposed Doesn't it suit me? / Not at all! can imply an insult. R69 now asks Does it look bad on me? andR73 retains Not at all! with a contextual reason. The original sealed draft is retained as historical, not rewritten. Revision/retention totals remain210/329. Only one native FE page changed: fresh four-alignment/glyph/row/bounds checks and direct visual review pass;538 native records/544 visual bindings are exact reuses. The latest stored check takes seconds using exact record-scoped reuse.

## Stored research image and checks

Research ROM `{rebuilt['research_ROM']}`, SHA256 `{rebuilt['research_ROM_sha256']}`. It is pinned and preserved, is not a registered playable release, and must not be handed off as cumulative. Parent is verified eb62870b. Only SC0 changes; all other files/components/code/fonts/names/runtime fixes andserialized parent inverse are exact. Reconstruction `{rebuilt_path}` covers20 reviewed blocks/19 changed blocks,539 speeches,860 commands/97 relative sites, withB68 unchanged.

Stored proof: `work/analysis/Rafael_B61_B80_stored_native_v12_20261104/stored_native_verification.json`:539 records/545 pages,538 exact previous stored-record reuses/one fresh parity-dependent page,485 fresh native branch cases. Catalogue proof: `work/analysis/Rafael_B61_B80_stored_catalogue_v12_20261104/all539_stored_effective_body_bindings.json`:all539 bodies survive original lookup byte-for-byte. Loader proof: `work/analysis/Rafael_B61_B80_loaders_v12_20261104/verification.json`:343 fresh loads/cache hits,two fresh/684 exact reused parent modes,344 unchanged EV0 actions.

The first storage run reached all blocks but failed saving final evidence because of a local variable collision; it is not called a whole-run pass. Version2 saved every block andpassed;version3 reuses538 exact records andchecks the changed page andall485 branches. The failed formatting diagnostic caught stale proposed-markup metadata after the question revision;version5 input/automatic_v12/native subset_v13 pass. Preserve these artifacts; do not repeat their completed checks.

## Honest gameplay and visual coverage

`{ROOT/'actual_review.json'}` and`{ROOT/'actual_visual_approval.json'}` bind95 observed utterances/101 distinct body pages,216 complete body-plane samples/204 complete header-plane samples, all22 actors/all six FE speeches/all six two-page cases.444 utterances remain offline-only. All17 final QA sheets are directly viewed or exact sheet-pixel reuse:11 fresh final CG sheets were viewed;the six final name sheets exactly match the six already viewed predecessor sheets.

Final qualifying runs: `work/analysis/Rafael_B69_complete_scene_run_v12_20261104/terminal.json` (24001 frames) and`work/analysis/Rafael_B61_B80_names_pagination_run_v12_20261104/terminal.json` (15001 frames). Final pixels: `work/analysis/Rafael_B69_complete_scene_pixels_v12_20261104/focused_actual_pixels.json` and`work/analysis/Rafael_B61_B80_names_pagination_pixels_v12_20261104/focused_actual_pixels.json`. Both are ordinary-input coldboots with disclosed initialized fixtures, no savestate/battery/RAM/condition override. All five preserved runs total102005 frames; only the latest two/39002 frames qualify current revision. No natural activation, original location, earned chronology, full route or hardware claim.

The full B69 fixture preserves all92 commands/66 speeches andoriginal CG/actions/return. The kiss is now visually confirmed at `work/rf69finalcap_20261104/frame_015840_cold_boot.png`; no action or relationship is invented in English. The R100 Here page appears at9495..9535, between the first run's120-frame samples. Dense exact-frame captures show it intact; this was a capture gap, not a missing-letter ROM defect. All66 final pages andthe corrected question/reassurance are pixel-bound andvisually checked. The shorter fixture is a synthetic name/pagination sample, not a complete story exchange. Full catalogue UI/global207 names andactor40 full-middle フォン/current Ｆong remain open.

## Continue with registered integration

Register andqualify this complete539 batch, preserving all114 accepted layers andall eight final stages fromprofile `{release['profile']}`. Use `scripts/build_integrated_release_with_Fernan_field.py`; the exclusive actor35 Fernan F correction remains mandatory. Rebase only whole-ROM identities ofthe eight stage configurations andthe first-stage parent manifest/builder dependency contract. Preserve earlier profile/configs/drivers/data ownership exactly. Reconcile current registry before building; current registry remains unchanged atthis checkpoint.

The previous batch's pure module/registration/qualification scripts are `dk4tool/patch/rafael_B51_B60_release_v1.py`, `scripts/prepare_rafael_B51_B60_release.py` and`scripts/qualify_rafael_B51_B60_release_v2.py`. New scope hasno menus,19 changed blocks plusunchanged68,539 records/545 pages/485 native branch cases,22 names and95 observed utterances/444 offline-only. Its final research identity is `{rebuilt['research_ROM_sha256']}`. Adapt structural/semantic guards without changing native addresses. Keep the existing reviewed_scene_rebuild_v3 complete source/control/inverse algorithm. Do not conflate reviewed_blocks20 withchanged_blocks19. Preserve the exact R143 info-level wrap retention.

Run meaningful production rejection checks, direct/shared plan equality, the full registered build, exact clean-input patch reconstruction andown cumulative startup bindings. Then credit539 exactly once:expected totals11313 complete/6566 revisions/4747 retentions. Do not use those future counts until verification actuallypasses. Do not promote main without required acceptance. After integration, continue remaining early tutorials/help andRafael priority work; all broader scope stays active. No jobs fromthis checkpoint are live.
'''
    checkpoint(mutation=ROOT/'539_research_ready_checkpoint_mutation_v1',batch_key='Rafael_SC0_B61_B80_clean_20261104',
        batch_updates=dict(new_credit=0,comparison='translations/rafael_B61_B80_contextual_editorial_manuscript_v5.json',
            comparison_sha256=sha(Path('translations/rafael_B61_B80_contextual_editorial_manuscript_v5.json').read_bytes()),
            contextual_prose_comparisons=539,remaining_contextual_comparisons=0,proposed_revisions=210,justified_retentions=329,
            final_five_gate_research_review=str(final),final_five_gate_research_review_sha256=sha(final.read_bytes()),
            individual_five_gates_passed=539,all_individual_fifth_gates_pending=False,
            final_formatting_input=str(FORMAT/'formatting_input_v5.json'),final_body_plan=str(FORMAT/'automatic_v12/automatic_plans.json'),
            final_native_body=str(FORMAT/'combined_native_v12.json'),body_display_approval=str(FORMAT/'body_display_approval_v12.json'),
            final_body_pages=545,actual_gameplay_records=95,actual_gameplay_body_pages=101,offline_only_utterances=444,
            scoped_names_approved=22,source_control_commands=860,relative_sites=97,native_relative_cases=485,
            reconstruction=str(rebuilt_path),reconstruction_sha256=sha(rebuilt_path.read_bytes()),
            research_ROM=rebuilt['research_ROM'],research_ROM_sha256=rebuilt['research_ROM_sha256'],
            CG_gesture_unconfirmed=False,CG_gesture_andEstado_final_wording_pending=False,
            scoped_header_name_planes_storage_actual_CG_transitions_andregistered_integration_pending=False,
            fresh_formatting_stored_visual_gameplay_andregistered_integration_pending=False,
            all_research_checks_passed_registered_integration_pending=True,
            negative_question_reassurance_mismatch_corrected=True,brief_Here_page_intact_sampling_gap_resolved=True,
            no_live_jobs=True,next_action='Register/qualify539 andall eight preserved stages;build cumulative ROM/exact clean patch;own startup;credit once.Then remaining early tutorials/help andRafael.'),
        additional_updates={'editorial_execution_priority_20261104':dict(new_credit=0,
            Rafael_early_story_andall_tutorials_first=True,current_batch='Rafael_SC0_B61_B80_clean_20261104',
            current539_five_gate_research_ready=True,registered_cumulative_integration_next=True,
            registered_cumulative_build_live=False,current_batch_not_yet_integrated=True,
            full_editorial_scope_preserved=True,guide_photos=False)},
        summary=summary,document=document,document_text=text,completed=10774,
        protected={'translations/release_stack.json':release['registry_sha256'],release['candidate']:release['candidate_sha256'],
            release['patch']:release['patch_sha256'],release['canonical_base']:release['canonical_sha256']})
    print('Checkpointed539 complete research reviews;registered integration next.10774 completions/main unchanged;full scope/all ROMs preserved.')
