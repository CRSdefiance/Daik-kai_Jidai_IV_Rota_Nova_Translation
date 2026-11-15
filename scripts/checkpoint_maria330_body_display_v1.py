"""Publish completed body-native/visual work while preserving the unfinished full editorial goal."""
from pathlib import Path
from scripts.meaning_maria330_clean_v1 import ROOT
from scripts.audit_story_glyph_consistency import load
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest
from scripts.save_editorial_progress_checkpoint_v9 import checkpoint

def main():
    prose_path=Path('translations/maria_B96_B124_contextual_review_v2.json');names_path=Path('translations/maria_B96_B124_scoped_names_v2.json')
    visual_path=ROOT/'body_visual_review_v1.json';native_path=ROOT/'selected_native_sheets_v2/selected_native_pages.json'
    selection_path=ROOT/'native_final_selection_v2/resume_selection.json';plan_path=ROOT/'plan_continuity_v10/automatic_plans.json'
    release_path=Path('work/maria328_release_v1/registered_release_verification.json')
    prose,names,visual,native,selection,plan,release=map(load,[prose_path,names_path,visual_path,native_path,selection_path,plan_path,release_path])
    assert (prose['source_objects'],prose['proposed_revisions'],prose['justified_retentions'])==(330,249,81)
    assert all(r['review']==dict(source=True,context=True,localization=True,naturalness=True,formatting=False) for r in prose['records'])
    assert len(names['records'])==26 and all(not r['review']['formatting'] for r in names['records'])
    assert visual['all_final_body_pages_bound_to_directly_viewed_exact_native_pixels'] and visual['body_pages']==338
    assert len(visual['records'])==native['records_count']==selection['reused_records']==330
    assert native['pages']==338 and native['selected_completed_alignment_cases']==1320
    assert selection['native_selection_complete'] and selection['remaining_records']==0
    assert len(plan['records'])==330 and not plan['failures']
    assert not any(i['severity'] in ['warning','error'] for r in plan['records'] for i in r['base_QA']['issues'])
    assert digest(plan_path)==visual['selected_plan_sha256'] and digest(native_path)==visual['selected_native_proof_sha256']
    paths=[prose_path,names_path,visual_path,native_path,selection_path,plan_path,
        ROOT/'prose_gates_v2.json',ROOT/'formatting_FE_v2/physical_manuscript.json',ROOT/'formatting_FE_v2/pagination_owners.json',
        ROOT/'continuity_preferences_v10.json',ROOT/'formatting_v1/native_macro_measurements.json',
        ROOT/'native_remaining_inputs_v1/resume_selection.json',ROOT/'native_late_fix_inputs_v1/resume_selection.json',
        ROOT/'native_B116_fix_inputs_v1/resume_selection.json',release_path,Path(__file__)]
    evidence={str(p):digest(p) for p in paths}
    summary=('Maria330 body display is complete offline:249 revisions/81 justified retentions across26 exchanges,26 scoped name prose retentions, '
        '330 physical bodies/338 directly viewed pages and1320 passing native alignments. Three premature pages are reclaimed,seven clause boundaries '
        'andthe orphaned See are repaired; three mixed-font Latin lines andone Japanese grant now show complete English. '
        'Two source-owned FE continuations preserve full paragraphs. Caption/style-object/name/storage/gameplay/release checks remain; fifth gates andcredit are pending. '
        'No live workers. Registered c20375bf,integrated20,689,main andfull scope are unchanged.')
    text='''# Maria330 body display checkpoint — November 9, 2026

**All selected body-native and visual checks pass:330 physical bodies,338 pages and1,320 alignment cases.** The330 original editorial objects retain249 revisions/81 individually justified retentions across26 complete exchanges. There are26 scoped name retentions with prose gates only. Every fifth gate remains false; no new completion credit, ROM or patch.

Use `translations/maria_B96_B124_contextual_review_v2.json`, `translations/maria_B96_B124_scoped_names_v2.json` and `work/Maria_B96_B124_clean_20261109/prose_gates_v2.json`. Reuse [the comparison checkpoint](editorial_Maria330_comparisons_20261109.md) for clean-first source/current decisions and [the earlier prose checkpoint](editorial_Maria330_prose_layout_20261109.md) as history. Its live-worker status is superseded: **all workers have ended**. Do not poll sessions96681/59794/63938/72224/61096. The original native run failed at B116R41 after231 durable completions; preserve its failure and every successful receipt.

Selected physical input is `formatting_FE_v2/physical_manuscript.json`; selected plans are `plan_continuity_v10/automatic_plans.json` with `continuity_preferences_v10.json`. Use `scripts/plan_maria330_FE_v3.py`. All source/current/prose bindings, controls, macros, aliases and native widths pass; plans have no warnings, errors or failures. Two exact grammatical retentions cover the complete question ending for? and an ordinary with/the-map soft boundary. All other guards remain. Regional-name soft breaks and the whole interpretive coda at B123R35 have individual reasons rather than global prohibitions.

**338 final body pages were actually viewed.** `body_visual_review_v1.json` maps every exact source/current/final body to48 viewed sheets, including superseded findings. It verifies each complete selected native preview against its actual viewed sheet tile; no final page borrows a changed preview. `native_final_selection_v2/resume_selection.json` binds all330 final records to durable matching receipts. `selected_native_sheets_v2/selected_native_pages.json` and its42 complete sheets are the final aggregate. These aggregate completed checks; they do not claim a fresh monolithic run. Exact runtime/font/macro/source/current/text/compiled dependencies are verified. All four native alignment cases per body, complete leading/internal/trailing glyphs, canaries, consumption, bounds and pagination pass. Do not replay those cases merely to recreate a combined report.

Layout work reclaims three pages without changing a word: B98R13, B106R16 and B115R4. Seven records now preserve a complete closing thought or core clause across A boundaries: B105R101/R106/R132, B106R13, B110R11 and B116R24/R110. The latter two retain documented source-specific shorter setup rows in order to keep their core characterization/interrupted ideals clause together. The child's figurehead See stays attached. Three mixed-width Latin defects at B105R23, B110R11 and B121R19 now visibly use consistent ASCII I; B118R8's formerly Japanese grant now shows complete English. These are body/text-display fixes, not nameplate or artwork approval.

**Two source owners require one additional FE control each:** B116R41 and B116R51. Their whole logical English remains intact, with two children apiece under the exact original six-byte FE preamble. R41's37-cell guarded opening failed the real native painter; reuse of the validated source-scoped36-cell reserve and a sentence-boundary continuation repairs it at unchanged228-pixel physical width. R51's full battle account exceeded one panel's capacity. `formatting_FE_v2/pagination_owners.json` binds both original references, all four children and exact paragraph reconstruction. Source330 =328 body objects +two captions; physical330 body candidates +two captions =332 formatting objects. **Never credit332 source records.** Source-owned insertion, combined relocation/relative branches, inverse/storage and focused actual A transitions remain required. Use `scripts/prepare_maria330_FE_guard_continuation_v1.py` for the qualified projection; do not reapply an obsolete single-owner physical manuscript.

The first231 durable results were retained. Only99 unproved records were rendered after the stop; subsequent four- and two-record subsets repaired new visual findings. Reuse `scripts/prepare_editorial_native_resume_v2.py` for exact receipt selection and `scripts/render_editorial_selected_native_sheets_v1.py` for assembly. The source-scoped caption, style-object, source/current metadata, term/name and macro proofs are already reference-bound. No font metrics, viewport, native dispatch or runtime substitutions were changed to accommodate prose.

**Next complete the remaining mixed-consumer checks:** two B102 two-choice captions/provider/order/selection/cancel returns; six source4100 style objects and all eight aliases each;26 scoped speaker-name strings/consumers, reusing exact compatible prior planes; original script/storage/allocation/relative commands and both FE insertions; then representative gameplay for distinct FE A transitions, styles, choice outcomes, mixed-letter repairs and ordinary return. Offline body previews are not actual gameplay, header or conditional reachability coverage. Original locations, chronology, rewards, arbitrary custom names and hardware remain unvisited. No guide photos are requested. Once necessary checks pass, integrate through the registered cumulative workflow and exactly reconstructable clean-input patch; main promotion still requires acceptance.

Registered candidate remains `work/maria328_release_v1/all_routes_maria328_candidate.nds`, SHA-256 `c20375bfc50a4d5973bfad203f3c45db9ae4b3dada0d328610c79fa19e908692`,715 manifest entries/114 accepted layers/50 passing checks, own startup and exact clean-input patch. It retains the Market Goods Info fix for both Local/Cargo missing from the user's Rafael2952 build. Preserve that allocation, six-section ARM9, ASCII right-bound correction, source25 v2 and all earlier layers/amendments. Integrated20,689 and remaining native story5,209 (Lil1,805/Maria3,404) remain unchanged. All remaining storylines, earlier unfinished contextual passes, shared shop/town/random dialogue, names and player prose stay in scope. Deferred artwork and the later older-record technical re-audit remain separate. Every ROM, translation, draft, failed producer and proof is preserved; no promotion, cleanup, commit or push.
'''
    checkpoint(mutation=ROOT/'body_display_progress_checkpoint_v1',batch_key='editorial_execution_priority_20261104',
        batch_updates=dict(new_credit=0,current_batch='Maria330:249 revisions/81 retentions;all338 body pages pass native and direct visual review.',
            proposed_revisions=249,justified_retentions=81,current_batch_not_yet_integrated=True,all_current_batch_fifth_gates_pending=True,
            native_job_live=False,native_sessions=[],registered_build_live=False,registered_cumulative_build_live=False,guide_photos=False,
            next_action='Complete two-choice captions, six style objects, scoped names, stored two-owner FE insertion/relative inverses and representative gameplay before registered integration.',current_batch_evidence=evidence),
        additional_updates={'Maria_SC3_B96_B124_clean_20261109':dict(new_credit=0,first_four_individual_prose_gates_pass=True,
            all_fifth_formatting_gates_pending=True,source_objects=330,source_body_objects=328,physical_body_candidates=330,planned_pages=338,
            selected_layout_plan=str(plan_path),selected_layout_plan_sha256=digest(plan_path),body_native_andvisual_complete=True,
            current_selected_body_pages_visually_reviewed=338,selected_native_alignment_cases=1320,source_FE_pagination_owners=2,
            premature_pages_reclaimed=3,closing_clause_boundary_fixes=7,orphan_See_repaired=True,
            B105_three_boundary_fixes_fresh_visual_pending=False,native_checks_live=False,native_sessions=[],
            caption_style_object_name_storage_gameplay_andregistered_integration_pending=True,registered_integration_pending=True,
            current_batch_actual_gameplay_observations=0,progress_evidence=evidence)},
        summary=summary,document='docs/editorial_Maria330_body_display_20261109.md',document_text=text,completed=20689,
        protected={'translations/release_stack.json':release['registry_sha256'],release['candidate']:release['candidate_sha256'],
            release['manifest']:release['manifest_sha256'],release['patch']:release['patch_sha256'],release['canonical_base']:release['canonical_sha256']})
    print('Saved Maria330 body checkpoint:338 viewed pages/1320 native cases;no live workers;all fifth gates andintegration remain pending.')

if __name__=='__main__':main()
