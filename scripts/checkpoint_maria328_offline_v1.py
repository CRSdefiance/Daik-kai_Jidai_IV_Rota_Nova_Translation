"""Save the completed prose/native/visual stage without crediting or changing releases."""
from pathlib import Path
from scripts.meaning_maria328_clean_v1 import ROOT
from scripts.audit_story_glyph_consistency import load
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest
from scripts.save_editorial_progress_checkpoint_v9 import checkpoint

def main():
    approvalpath=ROOT/'offline_display_approval_v1.json';approval=load(approvalpath)
    finalpath=ROOT/'final_native_v1.json';final=load(finalpath)
    prosepath=Path('translations/maria_B73_B95_contextual_review_v1.json');prose=load(prosepath)
    releasepath=Path('work/maria303_release_v1/registered_release_verification.json');release=load(releasepath)
    assert approval['final_native_proof_sha256']==digest(finalpath)
    assert approval['all321_final_pages_directly_viewed'] and approval['all_fifth_formatting_gates_still_pending']
    assert (approval['source_objects'],approval['dialogue_revisions'],approval['dialogue_retentions'])==(328,143,185)
    assert len(approval['layout_changes'])==12 and approval['pages_reclaimed']==1
    assert final['runtime']['candidate_sha256']==release['candidate_sha256']==prose['current_ROM_sha256']
    assert digest('translations/release_stack.json')==release['registry_sha256']
    paths=[approvalpath,finalpath,prosepath,releasepath,ROOT/'contextual_prose_qualification_v1.json',
        ROOT/'scoped24_names_editorial_review_v1.json',ROOT/'scoped_terms_reference_v1.json',
        ROOT/'dynamic_roles_current_v1.json',ROOT/'formatting_v1/native_macro_measurements.json',
        ROOT/'formatting_FE_v1/physical_manuscript.json',ROOT/'formatting_FE_v1/pagination_owners.json',
        ROOT/'formatting_FE_v1/preferences_visual_v6.json',ROOT/'plan_visual_v6/automatic_plans.json',
        ROOT/'native_final_selection_v2.json',ROOT/'native_final_v2/compiled_native_pages.json',
        ROOT/'telescope_native_v1/compiled_native_pages.json',ROOT/'visual_reviews_v1/names_andmenus.json',Path(__file__)]
    evidence={str(p):digest(p) for p in paths}
    summary=('Maria B73–B95 now has328 complete-exchange decisions (143 revisions/185 justified retentions), '
        'four individual prose gates passed,24 scoped names/roles andbound terms. All321 final body pages,15 captions '
        'and28 name strings pass native/visual checks. Twelve layout improvements reclaim one page;two FE display '
        'defects andall20 non-ASCII targets,includingtwo corrupt rescue styles,are corrected in the reviewed inputs. '
        'Reuse223 exact body proofs;only changed orunfinished layouts were rerendered. Stored-script/allocation/branch '
        'checks,the new riddle continuation transition,representative gameplay andregistered integration remain. '
        'All fifth gates stay false;zero new credit. Integrated20,361,registered d42dcd8e,main andthe full editorial scope are unchanged.')
    text='''# Maria328 offline display checkpoint — November 9, 2026

**328 source objects across21 complete exchanges have143 revisions and185 individually justified retentions.** The first four gates pass for each object. Every final body page, menu caption and scoped name string has completed native and direct visual review. This is offline editorial/display progress: storage, allocation, branches, representative gameplay, registered integration and every fifth gate remain open. No ROM was built and no completion credit was added.

Continue under `work/Maria_B73_B95_clean_20261109`:

- Selected prose: `translations/maria_B73_B95_contextual_review_v1.json`. Exact clean/current references, original controls, paragraph decisions, individual findings and retention reasons remain bound per record. Independent meanings/drafts and earlier comparisons are preserved. Final counts are143/185, superseding the139/189 proposal totals. Three Proof of Conquest corrections and a clearer treasure-record reference account for the four additional revisions; the complete selected prose was reread as21 exchanges. The original comparison checkpoint remains historical evidence.
- `scoped24_names_editorial_review_v1.json`, `scoped_names_macros_reference_v1.json`, `scoped_terms_reference_v1.json` and `dynamic_roles_current_v1.json` qualify24 retained actor/name/role identities,48 original name getters, established item/location labels and38 source-owned dynamic/style bindings. Samwell Khan and Margrete match registered consumers. Proof of Conquest is bound to an accepted full story reference, separately from abbreviated UI labels. Julio's actual grandfather relationship with Cristina is supported; the rescue child's familiar farewell does not invent kinship. Future lookout/rescuer assignments are not inferred from a current role result.
- `offline_display_approval_v1.json` and `final_native_v1.json` bind all314 physical body candidates/321 final pages,15 captions in five menus and28 distinct name strings. The source still has328 objects:289 ordinary speeches,24 physical style alternatives and15 captions. One long FE riddle owner has two physical children; it never earns two source credits. All1256 selected alignment cases pass:892 exact reused cases for223 unchanged bodies and364 fresh cases for91 final layouts. Every final page was directly viewed, with329 viewed page versions including superseded refinements. Names reuse13 exact planes and freshly check15. Caption checks cover30 provider alignments,120 bridged selection/cancel returns,60 normal/highlight planes and40 rejected compiler negatives. Only the displayed caption previews were directly viewed; highlight/controller behavior is not claimed as gameplay.
- Final formatting is `formatting_FE_v1/physical_manuscript.json` with `plan_visual_v6/automatic_plans.json` and source-bound `preferences_visual_v6.json`:314 successful plans/321 pages, zero errors or warnings. Twelve layout changes include nine ordinary wrap/page-continuity improvements and three physical FE layout repairs. Julio's old-man reflection now fits one full panel. Short questions and old man's stay together. Samwell's offer, the telescope report, gunpowder contrast and fatal-journey consequence receive coherent continuation clauses. The Jaguar God's Vest trial was rejected because it left only Let's look on the opening row; its fuller ordinary word-boundary wrap is explicitly retained. No prose, font, runtime code or physical viewport was shortened/changed to fit.
- Fresh native checks exposed a long-riddle input-consumption failure and a bean-tutorial extra-row failure. The existing scoped36-cell FE guard reserve corrects the exact affected inputs while retaining the228px physical view and all native assertions. All20 formerly non-ASCII targets now render complete ASCII English in the selected inputs, including B85's untranslated greeting and `SC3_B95_STYLE_400_18` / `_42`, previously `濡ot it!`. These are verified text-display corrections, not deferred artwork; they are not yet in a newly registered ROM.
- Completed failed-run block receipts and append-only journals are reused only with exact source/current/prose/compiled/native-plane dependencies. Preserve `native_pages_v1`, `native_resume_v1`, `native_final_v1`, `native_final_v2`, `telescope_native_v1`, their logs and all earlier trials. The successful final90-record and focused telescope invocations exited0. The native run receipts and hashes are authoritative; failed invocations are not reported as complete passes. No job is live.

**Next apply and prove the stored transaction, then representative gameplay and registration.** Use the registered Maria303 predecessor. The `formatting_FE_v1/pagination_owners.json` projection splits B87R139's unchanged paragraph at one ordinary space into two source-owned FE panels, both with original `0040ffff00fe` preambles. Apply the qualified `dk4tool/script/reviewed_FE_pagination_v1.py` helper; prove every resulting command/catalogue index, relative branch and full clean/current/block/archive/serialized-ROM inverse. Do not reapply the disjoint B54R507 storage amendment or B62R53 alignment correction. Check allocations/terminators and native catalogue/loader handoffs before closing gates. Exercise the new FE A→continuation→menu transition, the repaired FE row behavior, representative progressive pagination and dynamic/style/glyph behavior. Reuse unchanged engine proofs; exhaustive original conditional activation is unnecessary. All current-batch gameplay observations remain zero, including unvisited original event conditions and hardware.

Registered candidate remains `work/maria303_release_v1/all_routes_maria303_candidate.nds`, SHA-256 `d42dcd8edbd9c04b1f1e26813d1feef06fada22e9c7a5a525ac637931d780679`, with714 entries/114 accepted layers/49 passing checks. Preserve its market read-only literal and both pointers, six-section ARM9, ASCII right-bound correction and v2 source25 guard. Exact clean-input patch reconstruction, own Maria/Hangzhou startup and24 protected name getters precede registration/credit. Main promotion requires user acceptance. All generated ROMs and earlier translations remain preserved.

Integrated totals remain20,361 (12,245 revisions/8,116 retentions). Native story objects remaining remain5,537 (Lil1,805/Maria3,732); this328-object batch has zero credit until registered integration. All unfinished storylines, earlier contextual passes, shared shop/town/random exchanges, speaker labels and remaining player-facing prose remain in scope. Early Rafael/tutorial priority and completed coverage are preserved. No guide photos are required. Unresolved graphics artwork and the later older-record technical re-audit remain separate.
'''
    checkpoint(mutation=ROOT/'offline_progress_checkpoint_v1',batch_key='editorial_execution_priority_20261104',
        batch_updates=dict(new_credit=0,current_batch='Maria B73–B95:328 prose-approved objects;321 native/visually reviewed pages,15 captions,28 name strings.',
            current_batch_not_yet_integrated=True,all_current_batch_fifth_gates_pending=True,
            proposed_revisions=143,justified_retentions=185,new_source_meanings=328,new_independent_drafts=328,new_current_comparisons=328,
            current_batch_four_prose_gates_pass=328,current_body_pages_native_andvisually_reviewed=321,
            current_batch_layout_changes=12,current_batch_pages_reclaimed=1,current_batch_nonASCII_targets_native_corrected=20,
            native_job_live=False,registered_build_live=False,registered_cumulative_build_live=False,guide_photos=False,
            next_action='Prove stored328 transaction andsource-owned B87R139 FE continuation;representative gameplay,then registered cumulative integration.',
            current_batch_evidence=evidence),
        additional_updates={'Maria_SC3_B73_B95_clean_20261109':dict(new_credit=0,proposed_revisions=143,justified_retentions=185,
            selected_final_prose=str(prosepath),selected_final_prose_sha256=digest(prosepath),
            contextual_comparison_proposal_preserved=True,source_context_localization_naturalness_gates_pass=328,
            final_scoped_names_terms_role_consumers_prose_reread_andall_five_gates_pending=False,
            scoped_names_terms_roles_andcomplete_prose_reread_complete=True,all_fifth_formatting_gates_pending=True,
            new_native_pages_oractual_gameplay_approval=True,offline_native_visual_approval=True,
            physical_body_candidates=314,native_final_body_pages=321,choice_captions=15,distinct_name_strings=28,
            selected_native_alignment_cases=1256,native_exact_reused_bodies=223,native_latest_fresh_bodies=91,
            layout_changes=12,pages_reclaimed=1,nonASCII_current_targets_corrected_in_reviewed_inputs=20,
            source_owned_FE_continuation_storage_andactual_transition_pending=True,
            stored_script_allocation_branches_andrepresentative_gameplay_pending=True,
            actual_gameplay_observations=0,current_batch_actual_gameplay_observations=0,registered_integration_pending=True,
            offline_display_approval=str(approvalpath),offline_display_approval_sha256=digest(approvalpath),progress_evidence=evidence)},
        summary=summary,document='docs/editorial_Maria328_offline_20261109.md',document_text=text,completed=20361,
        protected={'translations/release_stack.json':release['registry_sha256'],release['candidate']:release['candidate_sha256'],
            release['manifest']:release['manifest_sha256'],release['patch']:release['patch_sha256'],release['canonical_base']:release['canonical_sha256']})
    print('Saved328 offline checkpoint;all source coverage/release identities preserved;zero new credit;full goal active.')

if __name__=='__main__':main()
