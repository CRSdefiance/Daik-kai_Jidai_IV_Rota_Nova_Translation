"""Save completed offline work and the exact next storage/gameplay actions without credit."""
from pathlib import Path
from scripts.audit_story_glyph_consistency import load
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest
from scripts.save_editorial_progress_checkpoint_v9 import checkpoint
from scripts.meaning_maria_B51_B52_clean_v1 import ROOT

def main():
    approval_path=ROOT/'offline_display_approval_v1.json';a=load(approval_path)
    assert (a['records'],a['final_body_pages'],a['accepted_layout_changes_count'],a['native_FE_row_repairs_count'])==(310,318,15,5)
    assert a['all318_final_pages_directly_viewed_or_exact_visual_reuse'] and a['all_fifth_review_gates_still_false']
    native=load(a['final_native']);assert digest(a['final_native'])==a['final_native_sha256']
    assert native['fresh_compiled_alignments']+native['reused_compiled_alignments']==1240
    assert not native['direct_visual_review_pending'] and not native['actual_gameplay']
    release=load('work/maria_B50_release_v1/registered_release_verification.json')
    assert native['runtime']['candidate_sha256']==release['candidate_sha256']
    assert digest('translations/release_stack.json')==release['registry_sha256']
    evidence={str(p):digest(p) for p in [approval_path,Path(a['final_native']),Path(a['final_plan']),
        ROOT/'initial_complete_native_v1.json',ROOT/'name_planes_v1/native_name_planes.json',
        ROOT/'scoped26_name_editorial_review_v1.json',ROOT/'scoped_terms_v1.json',Path(__file__)]}
    summary=('Maria B51–B57 has 310 contextual reviews (184 revisions/126 retentions) and now passes offline native/visual checks: '
        '318 final pages, 26 names/31 strings, 15 wrap improvements, five FE row repairs and three mixed-width letter corrections. '
        'Every word and native control is preserved. Only 15 changed layouts were rerendered; exact completed proofs were reused. '
        'Stored-script/allocation checks, representative gameplay and registered integration remain; all fifth gates stay false. '
        'Integrated 19,748, registered de2ffce1, main and full editorial scope are unchanged; zero new credit.')
    text='''# Maria310 offline checkpoint — November 9, 2026

**All 310 contextual reviews now pass offline native and visual checks: 184 proposed revisions and 126 justified retentions, with 318 final body pages.** Fifteen wrap improvements, five FE row repairs and three mixed-width letter corrections preserve every word. All 26 scoped names and 31 distinct strings are native-checked and directly viewed. Formatting gates remain false pending stored-script and representative gameplay checks. No new ROM, integration credit or main promotion is claimed.

Continue from these artifacts under `work/Maria_B51_B57_clean_20261109`:

- `formatting_v1/formatting_input.json`: immutable four-prose-gate manuscript for 279 progressive and 31 FE bodies; no menus or personality alternatives.
- `plan_v8_complete_clauses/automatic_plans.json` and `final_native_v1.json`: final source/current-bound plans, compiled buffers, all 318 native pages and their exact visual receipts.
- `offline_display_approval_v1.json`: 15 accepted wrap improvements, five native FE fixes, two justified layout retentions and exact evidence links.
- `name_planes_v1/native_name_planes.json`, `scoped26_name_editorial_review_v1.json`, `scoped_names_macros_reference_v1.json` and `scoped_terms_v1.json`: names, roles, source fields, both native getters, cultural terms and default substitutions.

Reuse the [contextual checkpoint](editorial_Maria310_contextual_20261109.md) for the clean meanings, independent drafts, complete-exchange decisions and substantive corrections. Nothing was shortened to fit. The nine FI/FA occurrences remain live. The two records containing actual mixed-width letters now use normal ASCII I/F: Maria B56R185 and Julio B57R129. All 15 non-ASCII target records receive current native glyph/code/pixel checks; that target count does not mean 15 independent font defects. Complete leading/internal/trailing characters, protected continuation origins, input canaries, physical bounds, consumption and page counts pass.

The native FE check caught real display failures that the host plan missed. B54R499 and B55R91 produced unintended rows; focused original-plan probes also reject B54R507, B55R155 and B55R179. The existing source-scoped guard reserves fix all five: FE36 for four records and FE37 for the unchanged 135-character R507 paragraph. Original failures and all trials remain. Physical 228px geometry, font, controls and engine are unchanged; no new FE commands or child source records were added. Every corrected panel passes fresh native checks and visual review.

The 15 wrapping improvements keep full voyage, national-stability, peace, marriage-refusal and sword-training thoughts together across page turns. The unchanged 131-character life-stake paragraph retains two pages after its one-page trial fails the existing source/QA contract; page two now carries the complete closing phrase. “Come on,” “What's your name?” and Admiral plus the short default full name stay together. The final historical thought uses three readable rows rather than a detached “of history” tail. The initial illness reassurance is retained because forcing “worried about” together adds a weaker fourth row. Total pages remain 318; no page-reclamation claim is made.

`scripts/plan_maria310_complete_clause_v1.py` restores the already-proven exact-clause page-start behavior only for this batch's byte-bound page preferences. All normal QA, full available geometry, source/current checks and parity rules remain. Final plans have zero host errors or warnings. The ordinary complete-word boundaries around “have/the,” “she/and” and “come/to” improve sentence flow without waiving native checks or authoring line breaks.

`initial_complete_native_v1.json` qualifies the exact completed portions of two later-failed runs: 65 whole-block records and 19 append-only individual receipts. The resumed run checks only the remaining 226. An unchanged checker successor now journals every successful record, preserving all original assertions so later failures do not discard completed work. Unjournaled earlier B54 checks are not credited as reused; their 74 generated previews are byte-identical to the selected, viewed pages. The combined initial proof has 1,240 selected alignment cases. Only 15 changed layouts are freshly rerendered (23 pages/60 cases); the final selection reuses 295 records/1,180 cases. All initial and final generated pages are directly viewed or tied to exact previously viewed pixels; 36 duplicate ending pages reuse explicit PNG/native-plane hashes. Readable contact sheets cover all selected pages. These are offline tests, not gameplay.

**Next reconstruct and check the seven complete SC3 blocks (51–57) through the existing storage, allocation, branch, catalogue and loader workflow, using the final plans and native buffers above.** There are 310 source utterances and 310 native commands, eight two-page progressive records and 31 FE panels; no FE insertion transaction is needed. Source/current command inventories and whole block bytes are already in `current_v1/current_effective.json`. Reuse matching native proofs and rerender only storage-dependent behavior that actually changes. Preserve the registered market terminator/data pointers, six-section ARM9, ASCII right-bound correction and v2 multi-archive source25 guard.

Then run representative initialized gameplay for progressive pagination/A returns, FE narration and inline Bianca/Angelo voice identification, FE/progressive transitions, the three normal-font letters and resupply/departure/sailing. Sample distinct headers and preserve the whole exchange context. The existing Maria startup is compatible context, not B51–B57 gameplay. Original late-event conditions, cutscene effects/outcomes, full catalogue UI and hardware remain unvisited. No guide photos or exhaustive natural playthrough are required. Integrate once necessary checks pass through the registered cumulative workflow and produce the exact clean-input patch; do not promote main without user acceptance.

The registered cumulative remains `work/maria_B50_release_v1/all_routes_maria_B50_candidate.nds`, SHA-256 `de2ffce183ec277bcdd853b0b2e13437468dc1e102673c064e1767e2ac9fbfcd`, with 712 entries, 114 accepted layers and 47 release checks. Main, canonical input, all ROMs, earlier translations and evidence are unchanged. Integrated totals remain **19,748 = 11,880 revisions + 7,868 retentions**; native story objects remaining stay **6,150 (Lil 1,805 / Maria 4,345)** until this batch is integrated. Shared town/shop/random/UI and other prose remain separately tracked. All unfinished storylines, earlier contextual passes, names and display work stay in scope. Deferred graphics artwork and the later older-record technical re-audit remain separate. No worker is live at this checkpoint.
'''
    checkpoint(mutation=ROOT/'offline_progress_checkpoint_v1',batch_key='editorial_execution_priority_20261104',
        batch_updates=dict(new_credit=0,current_batch='Maria310 offline/native/visual complete;stored andrepresentative checks next.',
            proposed_revisions=184,justified_retentions=126,all_current_batch_fifth_gates_pending=True,
            current_batch_not_yet_integrated=True,native_job_live=False,registered_build_live=False,guide_photos=False,
            next_action='Reconstruct/check seven SC3 blocks51–57 using final318-page native proof;representative pagination/FE/glyph gameplay,thenregistered integration.'),
        additional_updates={'Maria_SC3_B51_B57_clean_20261109':dict(new_credit=0,
            offline_native_visual_pass=True,selected_native_pages=318,accepted_wrap_improvements=15,
            native_FE_row_repairs=5,corrected_mixed_width_letters=3,distinct_name_strings=31,
            offline_approval=str(approval_path),offline_approval_sha256=digest(approval_path),
            final_native=a['final_native'],final_native_sha256=a['final_native_sha256'],
            final_plan=a['final_plan'],final_plan_sha256=a['final_plan_sha256'],
            actual_current_batch_gameplay_observations=0,all_fifth_formatting_gates_pending=True,
            stored_andrepresentative_checks_pending=True,registered_integration_pending=True,evidence=evidence)},
        summary=summary,document='docs/editorial_Maria310_offline_20261109.md',document_text=text,completed=19748,
        protected={'translations/release_stack.json':release['registry_sha256'],release['candidate']:release['candidate_sha256'],
            release['manifest']:release['manifest_sha256'],release['patch']:release['patch_sha256'],
            release['canonical_base']:release['canonical_sha256']})
    print('Saved offline310 checkpoint:318 viewed native pages,15 wrap improvements,five FE repairs;19,748 integrated unchanged.')
if __name__=='__main__':main()
