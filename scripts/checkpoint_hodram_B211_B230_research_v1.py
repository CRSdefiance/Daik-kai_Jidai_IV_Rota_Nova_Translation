"""Persist completed research gates while preserving release identities and credited totals."""
from pathlib import Path
from scripts.audit_story_glyph_consistency import load
from scripts.build_registered_rafael5186_v1 import RELEASE,REGISTRY
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest
from scripts.review_hodram_B221_B230_contextual_v1 import ROOT
from scripts.save_editorial_progress_checkpoint_v7 import checkpoint
from scripts.save_rafael3222_weekend_checkpoint_v1 import LEDGER,PACKAGE

READY=ROOT/'research_final_v3/research_completion.json'

def main():
    ready,release,ledger,package=map(load,(READY,RELEASE,LEDGER,PACKAGE))
    assert ready['all_individual_five_gates_pass'] and ready['registered_integration_pending']
    assert (ready['records'],ready['revisions'],ready['retentions'])==(277,170,107)
    assert ledger['records_editorially_completed']==17031 and not ledger['full_goal_complete']
    for p,h in ready['evidence'].items():assert digest(p)==h
    summary=('Hodram B211–B230 passed all five research gates for 277 records: 170 revisions and 107 justified retentions. '
        'All 284 final pages passed native, visual and stored checks. Twenty-seven layouts improved plus one FE punctuation wrap; four candidates were retained. '
        'The focused emulator sequence showed 65 utterances/74 pages and both distinct menu types. Registered integration remains; integrated credit stays 17,031 and main is unchanged.')
    document=f'''# Hodram B211–B230: research complete

{summary}

Continue from the [sealed research completion](../{READY.as_posix()}) and [final per-record review](../translations/hodram_B211_B230_final_review_v1.json). All 277 individual source, context, localization, naturalness and formatting gates pass. The first 136 editorial decisions and all earlier drafts remain preserved. The 23 [scoped name decisions](../translations/hodram_B211_B230_scoped_names_final_v1.json) are justified retentions; full catalogue UI and the wider name review remain open. Clean regional metadata is explicitly not a new surname or biography.

The [final visual approval](../work/Hodram_B211_B230_resume_20261106/final_visual_approval_v6.json) resolves the 31 initial candidates: 27 revised layouts and four retained layouts. Enlarged pages and native row events showed A Dou and Zhao Yun were already intact; their initial split reports were false positives. Existing B213 R27 and B217 R45 layouts read better than the tested sparse alternatives. B224 R68 keeps its earlier complete-clause/invitation boundary. The separate B215 R17 FE punctuation wrap is fixed. Every initial page was viewed; all 39 new final-layout pages were freshly checked and viewed. Final total: 270 bodies/284 pages. No prose was shortened, ordinary manual breaks added, or runtime geometry changed.

B229 R36 has one narrow, source/current/prose-bound `weak-line-ending` waiver: the ordinary wrap after “horsemen of” keeps unchanged prose on one page and Western Roman Empires intact. The original warning, exact line and reason are retained in the plan and final record. Glyph, control, width, canary, consumption and pagination checks are not waived.

The [complete reconstruction](../work/Hodram_B211_B230_resume_20261106/research_rebuilt_v1/reconstruction.json) changes only 19 SC1 blocks; B222 is control-only and unchanged. All 348 commands, seven compound objects, clean/current block/archive/serialized ROM inverses and unowned files/components pass. Registered ASCII bounds, font and all prior runtime/name layers are exact to Rafael5186. [Stored verification](../work/Hodram_B211_B230_resume_20261106/stored_v1/stored_native_verification.json) passes all 284 pages: 126 parity-dependent pages freshly rendered, 158 exact planes reused; all 150 relocated branch cases pass. [All 270 original pre-macro lookups](../work/Hodram_B211_B230_resume_20261106/stored_catalogue_all_v1/all270_stored_effective_body_bindings.json) pass. [Archive checks](../work/Hodram_B211_B230_resume_20261106/loaders_v1/verification.json) pass 325 loads/cache hits, 38 fresh handoffs and 612 exact parent reuses.

The [focused emulator proof](../work/Hodram_B211_B230_resume_20261106/actual_pixels_v1/focused_actual_pixels.json) is one 23,441-frame ordinary coldboot of a disclosed native-command fixture: 65 utterances, 74 ordered pages, 156 complete body planes and 148 header planes across 14 selectors. It includes complete B211/B215/B223 exchanges, all four FE panels, the FI expansion, four unchanged eight-slot voice objects and representative revised page turns. All 13 body sheets were directly viewed. The 205 other speech variants remain offline-only.

[Two distinct menu types](../work/Hodram_B211_B230_resume_20261106/actual_menus_representative_v3/menu_actual_pixels.json) pass complete live caption, centering, blank guard and default-highlight checks with exact source keys and ordered surrounding calls. The representative Yes/No and three-name menu sheet was viewed. B224's repeated Yes/No object is byte-identical and independently checked offline. Its later occurrence is not credited with a complete stable highlight plane: the available samples show transition backgrounds. The first matcher incorrectly assigned the earlier identical capture to both source keys; that receipt and the failed strict all-occurrence check are retained as rejected evidence. The corrected representative proof does not repeat that claim. All seven captions and all source menu returns/branches pass offline; nondefault controller choices and cancellation remain unvisited. No new text defect or altered menu behavior was established.

The fixture preserves each copied complete source command and native initializers; it does not preserve original branch routing between the selected display samples. Natural event activation, original locations, earned chronology, battle transitions, full route, catalogue UI and hardware remain unvisited. This is representative gameplay, not exhaustive natural play. No guide photos are collected.

The research ROM and every prior/failed ROM and trial are preserved. Earlier finalizer attempts stopped on missing name-schema metadata and source-null middle components; the successful v3 adds schema/gloss metadata without changing any name decision or prose. The first fixture preparation stopped at an incorrect requested menu offset before saving a ROM; the exact source offset 138 is used in the successful fixture. Do not rerun completed checks.

Next qualify the cumulative SC1 transaction over registered Rafael5186, reject malformed production inputs, register the complete successor, verify its exactly reconstructable clean-input patch and own startup, then credit 277 once. Main and the weekend package remain unchanged. Every remaining route, shared/shop/town/random exchange, earlier translation and player-facing text stays in scope; deferred graphics artwork and the later older-record technical re-audit stay separate.
'''
    checkpoint(mutation=ROOT/'research_checkpoint_v1',batch_key='Hodram_B211_B230_clean_next_20261104',
        batch_updates=dict(new_credit=0,current_English_comparisons=277,proposed_revisions=170,justified_retentions=107,
            remaining_current_English_comparisons=0,all_five_research_gate_records=277,
            final_native_body_objects=270,final_native_pages=284,fresh_final_layout_pages_directly_viewed=39,
            visual_layout_revisions=27,visual_candidate_retentions=4,remaining_visual_layout_candidates=0,
            initial_FE_punctuation_wraps_corrected=1,final_formatting_andvisual_approval_pending=False,
            stored_reconstruction_andnative_checks_pass=True,stored_body_pages=284,fresh_parity_dependent_pages=126,
            exact_compiled_pages_reused=158,fresh_relocated_native_relative_cases=150,native_archive_loads=325,
            fresh_parent_cases=38,exact_reused_parent_cases=612,stored_catalogue_lookups=270,
            actual_frames=23441,current_batch_story_gameplay_utterances=65,actual_body_pages=74,
            offline_only_speech_variants=205,representative_gameplay_pending=False,
            scoped_names_reviewed=23,scoped_name_revisions=0,scoped_name_retentions=23,
            stored_reconstruction_andregistered_release_pending=True,registered_integration_pending=True,
            research_completion=str(READY),research_completion_sha256=digest(READY),
            native_job_live=False,registered_build_live=False,guide_photos=False,
            evidence={str(READY):digest(READY),str(Path(__file__)):digest(Path(__file__))}),
        additional_updates={'editorial_execution_priority_20261104':dict(new_credit=0,
            current_batch='Hodram B211–B230: all five research gates pass; cumulative registration pending.',
            next_action='Qualify and register the cumulative SC1 successor, verify exact clean-input reconstruction and own startup, then credit 277 once.',
            current_batch_not_yet_integrated=True,registered_integration_pending=True,native_job_live=False,
            registered_build_live=False,registered_cumulative_build_live=False,guide_photos=False)},
        summary=summary,document='docs/editorial_Hodram_B211_B230_research_20261107.md',document_text=document,
        completed=17031,protected={str(REGISTRY):release['registry_sha256'],release['canonical_base']:release['canonical_sha256'],
            release['candidate']:release['candidate_sha256'],release['patch']:release['patch_sha256'],package['zip']:package['zip_sha256']})
    print('Saved five-gate research checkpoint; 17,031 integrated credit, main and weekend package preserved.')

if __name__=='__main__':main()
