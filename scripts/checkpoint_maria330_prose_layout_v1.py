"""Checkpoint sealed prose and in-progress native layout QA without integration credit."""
from pathlib import Path
from scripts.meaning_maria330_clean_v1 import ROOT
from scripts.audit_story_glyph_consistency import load,save
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest
from scripts.save_editorial_progress_checkpoint_v9 import checkpoint

def main():
    prose_path=Path('translations/maria_B96_B124_contextual_review_v2.json');names_path=Path('translations/maria_B96_B124_scoped_names_v2.json')
    proof_path=ROOT/'prose_gates_v2.json';plan_path=ROOT/'plan_continuity_v4/automatic_plans.json'
    release_path=Path('work/maria328_release_v1/registered_release_verification.json')
    prose,names,proof,plan,release=map(load,[prose_path,names_path,proof_path,plan_path,release_path])
    assert prose['source_objects']==330 and (prose['proposed_revisions'],prose['justified_retentions'])==(249,81)
    assert all(r['review']==dict(source=True,context=True,localization=True,naturalness=True,formatting=False) for r in prose['records'])
    assert len(names['records'])==26 and all(not r['review']['formatting'] for r in names['records'])
    assert proof['structural_projection_pass'] and proof['unformatted_manuscript_rejected_by_release_gate']
    assert len(plan['records'])==329 and not plan['failures'] and sum(r['expected_native_pages'] for r in plan['records'])==339
    assert not any(i['severity'] in ['warning','error'] for r in plan['records'] for i in r['base_QA']['issues'])
    visual=ROOT/'partial_visual_review_v1.json';assert not visual.exists()
    sheets=[ROOT/'native_pages_v1'/name for name in [
        'B96_part1.png','B98_part1.png','B99_part1.png','B99_part2.png','B100_part1.png','B101_part1.png',
        'B102_part1.png','B102_part2.png','B102_part3.png','B102_part4.png','B103_part1.png','B104_part1.png',
        'B105_part1.png','B105_part2.png','B105_part3.png','B105_part4.png']]+[ROOT/'native_B98_fix_v1/B98_part1.png']
    assert all(p.exists() for p in sheets)
    save(visual,dict(directly_viewed_readable_sheets={str(p):digest(p) for p in sheets},sheets_viewed=17,
        blocks_viewed=[96,98,99,100,101,102,103,104,105],current_selected_body_records_andpages_viewed=126,
        historical_B98_two_page_plan_rejected=True,B98_fresh_one_page_four_alignment_check_anddirect_view_pass=True,
        observed_mixed_width_I_repair='DK4_MES_B105_R0023',
        B105_three_sentence_tail_boundaries_rejected_pending_fresh_selected_previews=['DK4_MES_B105_R0101','DK4_MES_B105_R0106','DK4_MES_B105_R0132'],
        figurehead_See_phrase_continuity_pass_with_justified_short_first_row=True,
        complete_question_ending_for_retained_with_specific_grammatical_reason=True,
        all_new_pages_viewed=False,no_global_fifth_gate_oractual_gameplay_approval=True,new_credit=0,producer_sha256=digest(__file__)))
    paths=[prose_path,names_path,proof_path,plan_path,visual,ROOT/'registered_story_terms_reference_v1.json',ROOT/'dynamic_roles_current_v1.json',
        ROOT/'formatting_v1/formatting_input.json',ROOT/'formatting_v1/native_macro_measurements.json',
        ROOT/'formatting_FE_v1/physical_manuscript.json',ROOT/'formatting_FE_v1/pagination_owners.json',ROOT/'continuity_preferences_v4.json',
        ROOT/'native_inputs_v1/manuscript.json',ROOT/'native_inputs_v1/plans.json',ROOT/'native_pages_v1/native_run_inputs.json',
        ROOT/'native_B98_fix_v1/complete_DK4_MES_B98_R0013.json',release_path,Path(__file__)]
    evidence={str(p):digest(p) for p in paths}
    summary=('Maria330 prose is sealed across26 complete exchanges:249 revisions/81 justified retentions and26 scoped name retentions; '
        'all four individual prose gates pass, fifth gates remain false. Full-width plans pass329 physical bodies/339 pages with no warnings. '
        'One full battle paragraph has two source-owned FE children; no extra source credit. Seventeen sheets are viewed; the B98 unchanged paragraph '
        'now passes one-page native/visual checks, while three B105 closing clauses await fresh previews. Native checks are running with durable receipts. '
        'Registered c20375bf, integrated20,689, main and full scope remain unchanged.')
    text='''# Maria330 prose and layout checkpoint — November 9, 2026

**330 four-gate prose reviews:249 revisions/81 justified retentions, plus26 scoped name retentions.** Formatting gates remain false. No new completion credit, ROM or patch. Reuse [the comparison checkpoint](editorial_Maria330_comparisons_20261109.md) for source intake and concrete findings; all earlier drafts and decisions remain preserved.

Final selected prose is `translations/maria_B96_B124_contextual_review_v2.json`, with individual exact references and reasons. Use `translations/maria_B96_B124_scoped_names_v2.json` and `work/Maria_B96_B124_clean_20261109/prose_gates_v2.json`. Fourteen name/term/read-aloud amendments reconcile Guiding Staff, Evergreen Lotus Leaf, Tang Bamboo Craft, Bamboo Assembly Plan, Lotion Jar, Upper/Lower Stone Tablet, Red Dye and Nagarpur. The finalizer reads the selected `proposed_English`, retaining all81 good current paragraphs exactly; independent drafts are unchanged. Its v2 fixes only an incorrect expected amendment count and uses fresh outputs. Earlier partial name output stays evidence.

`registered_story_terms_reference_v1.json` binds Soaring Scarlet Orca and Proofs of Conquest to unchanged registered blocks and two fresh original current catalogue lookups. Use `scripts/bind_maria330_registered_story_terms_v2.py`; v1 stopped on an unnecessarily broad older-ARM9 equality. No dictionary research was repeated or old font proof relabeled. The epithet remains the prior naval-context localization inference, separate from Shachihoko. `dynamic_roles_current_v1.json` binds source207/208/209/214/220 without assigning a future roster:207 resolves captain3; the other startup fallbacks resolve156 with strict208. These are offline roles, not observed conditional speakers.

`formatting_v1/formatting_input.json` marks all23 live FI/FA/FO occurrences; all four default macro proofs are reused only after exact ARM9/COMMON/font/actor-model/getter/default checks. Every changed paragraph still gets fresh layout/native pixels. Ordinary width216 and FE physical width228 remain unchanged. `formatting_FE_v1/physical_manuscript.json` preserves the whole B116R51 battle account in two virtual FE children; its `pagination_owners.json` binds the single source owner. This creates329 body candidates plus two captions, never331 source credits. Use `scripts/prepare_maria330_FE_pages_v3.py`; the earlier syntax/key failures produced no candidate. Source-owned insertion, branch/inverse/storage checks and actual A transitions still remain before integration.

Selected plans are `plan_continuity_v4/automatic_plans.json`:**329 bodies/339 pages, no warnings/errors/failures**. Use `scripts/plan_maria330_FE_v1.py` with `continuity_preferences_v4.json`. The initial generic SC1 planner rejected the route before outputs; it is not a Maria layout proof. The Maria initial plan correctly rejected the overlong FE paragraph. Phrase constraints keep the figurehead child's See attached. A byte-bound specific retention accepts the complete question ending in for?, not a broken preposition. The directly viewed B98 gift paragraph exposed premature five-row/two-page output: its unchanged text now fits one native page with in return intact. All four native alignments and the fresh one-page sheet pass. Three B105 second pages stranded sentence tails; full closing-clause preferences preserve every word and improve the boundary, with fresh previews pending.

**Native work is in progress.** Main process session96681 runs `check_editorial_compiled_pages_explicit_captain_v2` on `native_inputs_v1` into `native_pages_v1`, using the plan_continuity_v1 selection. Keep its append-only `complete_<ID>.json`, `native_run_inputs.json` and completed block receipts; do not replay finished cases. Its compiled text remains selected except B98R13 and B105R101/R106/R132. B98 fresh selection is `native_B98_fix_inputs_v1`/`native_B98_fix_v1` and is complete/viewed. Focused session59794 is rendering the three B105 replacements under `native_B105_fix_inputs_v1` into `native_B105_fix_v1`. Poll confirmed live sessions, then bind each exact final plan to the appropriate receipt. Session handles are this checkpoint's running-process references, not gameplay evidence.

`partial_visual_review_v1.json` records17 directly viewed sheets. There are126 current selected body pages visually reviewed through B105, excluding its three rejected two-page endings. The repaired B105R23 stammer visibly uses consistent ASCII I. The original B98 and B105 rejected pages remain evidence. Open the new B105 sheet and every later generated sheet; update the visual ledger and rerender only changed/unproved layouts. Menu captions/providers, name planes, full style objects, storage/allocation/relative branches, representative gameplay and registered cumulative integration remain. No new gameplay, original-condition activation, rewards or hardware coverage is claimed.

Current registered test ROM remains `work/maria328_release_v1/all_routes_maria328_candidate.nds`, SHA-256 `c20375bfc50a4d5973bfad203f3c45db9ae4b3dada0d328610c79fa19e908692`,715 entries/114 accepted layers/50 checks and exact clean-input patch. It retains the user's old Rafael2952 Market Goods Info fix for both Local/Cargo. Preserve that allocation, all earlier layers, source25 v2, six-section ARM9 and ASCII right-bound correction. Integrated20,689 and remaining native story5,209 (Lil1,805/Maria3,404) remain unchanged. Main is not promoted. All remaining storylines, earlier contextual passes, shared shop/town/random/name/player prose, separate graphics artwork and later older-record technical re-audit remain in scope. No guide photos, cleanup, commit or push.
'''
    checkpoint(mutation=ROOT/'prose_layout_progress_checkpoint_v1',batch_key='editorial_execution_priority_20261104',
        batch_updates=dict(new_credit=0,current_batch='Maria330:249 revisions/81 retentions;four prose gates pass;native/visual layout checks in progress.',
            proposed_revisions=249,justified_retentions=81,current_batch_not_yet_integrated=True,all_current_batch_fifth_gates_pending=True,
            native_job_live=True,native_sessions=[96681,59794],registered_build_live=False,guide_photos=False,
            next_action='Finish durable native checks; view B105 replacements and all later sheets; bind final plan receipts before style/menu/name/storage/gameplay checks.',current_batch_evidence=evidence),
        additional_updates={'Maria_SC3_B96_B124_clean_20261109':dict(new_credit=0,proposed_revisions=249,justified_retentions=81,
            all_five_individual_gates_pending=False,first_four_individual_prose_gates_pass=True,all_fifth_formatting_gates_pending=True,
            selected_prose=str(prose_path),selected_prose_sha256=digest(prose_path),selected_layout_plan=str(plan_path),selected_layout_plan_sha256=digest(plan_path),
            source_objects=330,physical_body_candidates=329,planned_pages=339,scoped_name_retentions=26,
            B98_premature_pagination_fixed_fresh_native_andvisual=True,B105_three_boundary_fixes_fresh_visual_pending=True,
            current_selected_body_pages_visually_reviewed=126,native_checks_live=True,native_sessions=[96681,59794],
            registered_integration_pending=True,current_batch_actual_gameplay_observations=0,progress_evidence=evidence)},
        summary=summary,document='docs/editorial_Maria330_prose_layout_20261109.md',document_text=text,completed=20689,
        protected={'translations/release_stack.json':release['registry_sha256'],release['candidate']:release['candidate_sha256'],
            release['manifest']:release['manifest_sha256'],release['patch']:release['patch_sha256'],release['canonical_base']:release['canonical_sha256']})
    print('Checkpoint saved:330 four-gate reviews/249 revisions/81 retentions;native checks live;no credit or release change.')

if __name__=='__main__':main()
