"""Preserve completed offline work and the separate unresolved FE exchange with zero credit."""
from pathlib import Path
from scripts.audit_story_glyph_consistency import load
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest
from scripts.save_editorial_progress_checkpoint_v8 import checkpoint

ROOT=Path('work/Maria_B37_B50_clean_20261109')

def main():
    approval_path=ROOT/'offline270_display_approval_v2.json';approval=load(approval_path)
    assert (approval['records'],approval['final_body_pages'],approval['accepted_layout_changes_count'])==(270,272,26)
    assert approval['all272_selected_body_pages_directly_viewed'] and approval['all_fifth_review_gates_still_false']
    native=load(approval['final_native'])
    assert digest(approval['final_native'])==approval['final_native_sha256']
    assert native['fresh_compiled_alignments']+native['reused_compiled_alignments']==4*266
    release=load('work/maria301_release_v1/registered_release_verification.json')
    assert native['runtime']['candidate_sha256']==release['candidate_sha256']
    evidence={str(p):digest(p) for p in [approval_path,Path(approval['final_native']),Path(approval['final_plan']),
        ROOT/'complete_B37_B49_projection_v1/projection_qualification.json',ROOT/'FE_row_diagnostic_v1.json',Path(__file__)]}
    summary=('Maria B37–B49 now has 270 contextual reviews (161 revisions/109 retentions), 272 directly viewed passing '
        'native body pages, 28 names/42 strings and four captions. Twenty-six wrap improvements reclaim four pages '
        'without changing prose; six layouts are justified retentions. Stored checks, representative gameplay and '
        'registration remain. Complete B50/16 records retains its source/prose work but is held for a concrete long-FE '
        'guard/bounds issue. Integrated 19,462, registered c9b583a6/main and full scope are unchanged; zero new credit.')
    text='''# Maria B37–B49 offline checkpoint — November 9, 2026

**270 reviews in 13 complete exchanges: 161 proposed dialogue revisions and 109 justified retentions.** All 266 body records pass current native checks; all 272 selected pages were directly reviewed. Four captions in two menus and 28 scoped names/42 distinct strings also pass offline/native checks and direct review. All fifth review gates remain false pending stored-script and representative gameplay checks. Nothing new is integrated or promoted.

Continue with these exact artifacts under `work/Maria_B37_B50_clean_20261109`:

- `complete_B37_B49_projection_v1/formatting_input.json` and `contextual_review.json`: exact whole-exchange subset of the sealed 286-record source-first manuscript, with 18 live macro occurrences.
- `final270_plan_v2/automatic_plans.json` and `final270_native_v2/compiled_native_pages.json`: selected full-width plans and native planes, preserving every word, native header and substitution.
- `offline270_display_approval_v2.json`: 26 accepted wrap changes, six justified layout retentions, four unnecessary pages reclaimed and exact visual/native evidence.
- `scoped28_name_editorial_review_v1.json`, `name_planes_v1/native_name_planes.json`, `scoped_terms_v1.json` and `menu_planes_v1/group_verification.json`: names, terms, native caption providers/normal/highlight glyphs and exact references.

The 26 layout improvements include joined North Sea/Zheng He names, complete short idioms and the wasn’t-it question tag, coherent closing clauses on second pages and four same-prose one-page successes. Six reviewed layout retentions avoid worse sparse rows or preserve an already coherent two-page threat. Rafael’s proposed `I had no` lead-in was rejected in favor of the original `I had no idea`; both generated versions were directly viewed. Retentions and wrapping add no duplicate dialogue credit.

The initial native run completed all 13 B37–B49 blocks before a later B50 failure. Its per-block records preserve 266 bodies/276 pages/1,064 alignment cases. All 30 initial sheets were directly viewed. `qualify_maria270_completed_native_blocks_v1.py` binds and reuses only these completed source/current/compiled records, current runtime/font and pixel/canary proofs; it does not claim the full failed run passed. Only 27 layout candidates were freshly rendered (32 pages/108 cases), and all three new sheets were viewed. One trial is rejected; final selected proofs use 26 fresh bodies/104 cases plus 240 exact earlier bodies/960 cases, totaling 266 bodies/272 pages. No completed native blocks were replayed. Metadata v2 distinguishes the four rejected trial cases from selected coverage; v1 remains evidence.

Both two-choice objects pass their source/current/reviewed native provider cases (12 alignments, 36 bridged modal returns and 14 compiler rejections). Every reviewed caption passes normal/highlight complete-glyph, centering, bounds and guard checks. The old B38 choice contains `、greed.`: its current provider bytes are tested, while the ASCII-only old-caption raster oracle is explicitly omitted for that malformed non-ASCII caption. The corrected target captions are fully checked. Bridged returns are offline evidence, not observed controller gameplay.

**Complete B50 is held separately, with all 16 source meanings/drafts and nine proposed revisions/seven retentions preserved.** The full 286-record contextual manuscript remains unchanged. `FE_row_diagnostic_v1.json` proves B50R36’s generic 38-cell guarded plan inserts an unintended blank native row, while B50R43’s full 139-character counterfactual fails the original native painter’s glyph/bounds assertion. Scoped existing FE36/FE37 plans cannot fit the complete R43 prose. Failed plans and the failed native run are preserved; no guard is relaxed, prose shortened, viewport/font changed or incomplete B50 shipped. This is an unresolved text-display issue inside the goal, not deferred graphics artwork. The seven initially generated B50 pages were also directly viewed. Resolve B50 with focused consumer/layout evidence later; do not repeat the completed 13-block work or restart its source pass.

Next reconstruct and check the selected 13 complete blocks through the existing native archive/catalogue/allocation/loader workflow; use exact final v2 plans/planes. Run representative initialized gameplay for the one FE unseen-voice entrance, six remaining two-page bodies, both two-choice commands/highlights/returns and transitions. Reuse the current registered Maria3 startup and inherited system-only unlock with its stated limits. Do not count the old Hangzhou startup or offline sheets as B37–B49 gameplay. Integrate the 270 reviews once necessary checks pass using the registered cumulative pipeline and exact clean-input patch, preserving every accepted layer and the ASCII right-bound correction. Do not promote main without required acceptance.

Current registered candidate remains [Maria301](editorial_Maria301_registered_20261109.md), SHA-256 `c9b583a629a327e7e4893e3d10d57c5e7a4c591f724354ac9561937cba6cfa01`, with 709 entries/114 accepted layers/44 checks and its exact clean-input patch. Main/canonical and all ROMs are preserved. Integrated totals stay **19,462 = 11,710 revisions + 7,752 retentions**; **6,436 native story objects remain**, including this unintegrated work. Shared town/shop/random and remaining player prose are tracked separately. All four storylines, unfinished earlier contextual passes, speaker names, wrap/glyph work and full editorial scope stay active. No guide photos; deferred artwork and the later older-record technical re-audit remain separate. No process is live at this checkpoint.
'''
    checkpoint(mutation=ROOT/'offline270_checkpoint_v1',batch_key='editorial_execution_priority_20261104',
        batch_updates=dict(new_credit=0,current_batch='Maria270 B37-B49:offline/native/visual complete;stored andrepresentative checks next. B50/16 held forlong-FE risk.',
            proposed_revisions=161,justified_retentions=109,all_current_batch_fifth_gates_pending=True,
            current_batch_not_yet_integrated=True,native_job_live=False,registered_build_live=False,
            next_action='Stored reconstruct/check270 reviewed records in13 complete blocks,representative FE/menu/pagination gameplay,thenregistered cumulative integration. Preserve B50 source/prose andrisk separately.',guide_photos=False),
        additional_updates={'Maria_SC3_B37_B50_clean_20261109':dict(new_credit=0,source_objects=286,
            contextual_comparisons_preserved=286,active_complete_exchange_subset=270,withheld_complete_exchange=50,
            withheld_records=16,withheld_revisions=9,withheld_retentions=7,
            withheld_reason='B50R43 full prose doesnotfit validated guarded FE36/37;generic38 causes native failure. No shortening orscope loss.',
            subset_offline_approval=str(approval_path),subset_offline_approval_sha256=digest(approval_path),
            all_fifth_formatting_gates_pending=True,registered_integration_pending=True)},
        new_entries={'Maria_SC3_B37_B49_display_20261109':dict(new_credit=0,source_objects=270,complete_exchanges=13,
            proposed_revisions=161,justified_retentions=109,body_records=266,selected_native_pages=272,
            wrap_improvements=26,layout_retentions=6,pages_reclaimed_without_prose_changes=4,
            scoped_name_retentions=28,distinct_name_strings=42,typed_captions=4,menu_commands=2,
            offline_native_visual_pass=True,actual_current_batch_gameplay_observations=0,
            all_fifth_formatting_gates_pending=True,stored_andrepresentative_checks_pending=True,
            registered_integration_pending=True,evidence=evidence)},
        summary=summary,document='docs/editorial_Maria270_offline_20261109.md',document_text=text,
        completed=19462,protected={'translations/release_stack.json':release['registry_sha256'],
            release['canonical_base']:release['canonical_sha256'],release['candidate']:release['candidate_sha256'],
            release['manifest']:release['manifest_sha256'],release['patch']:release['patch_sha256']})
    print('Savedoffline270 checkpoint andseparate B50 risk;integrated19462 andregistered/main unchanged;zero credit.')

if __name__=='__main__':main()
