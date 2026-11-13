"""Save the completed residual SC0 review before registered integration."""
from pathlib import Path
from scripts.audit_story_glyph_consistency import load
from scripts.build_registered_rafael4903_v1 import RELEASE, REGISTRY
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest
from scripts.plan_rafael_B0_B34_v1 import ROOT
from scripts.prepare_rafael_B0_B34_registered_v1 import QUALIFICATION
from scripts.save_editorial_progress_checkpoint_v6 import checkpoint
from scripts.save_rafael3222_weekend_checkpoint_v1 import PACKAGE


def main():
    ready_path=ROOT/'research_final_v1/research_completion.json'
    ready,release,package=map(load,(ready_path,RELEASE,PACKAGE))
    assert ready['all_individual_five_gates_pass'] and ready['records']==283
    assert load(QUALIFICATION)['dialogue_rebuilt_and_exact_283_stored_bindings_verified']
    summary=('Rafael B0–B34 passed all five review gates for 283 records: 162 revisions and 121 justified '
        'retentions. All 284 stored pages and 675 branch cases passed. Nineteen wraps improved; one '
        'candidate was retained with a reason. The emulator sample displayed 96 pages across 95 '
        'utterances and all 39 scoped headers. Registration and candidate-owned startup remain. '
        'Integrated coverage stays 16,748 in Rafael4903.')
    doc=f'''# Rafael B0–B34 completed research

{summary}

The [sealed completion](../{ready_path.as_posix()}) binds all individual clean/current/target references and five review gates. The final manuscript contains 162 revisions and 121 justified retentions. Previously completed decisions and every earlier batch retain their coverage. See the [earlier source and editorial findings](editorial_Rafael_B0_B34_native_20261106.md).

The final 283 speeches produce 284 pages. Every final offline page and scoped name plane was directly inspected, including the 15 latest wrap refinements; 268 exact earlier native proofs were reused. Together with the four earlier refinements, 19 layouts improved. B21 R5 keeps its existing layout because the proposed constraint produced a sparse modal split. The unshortened poem retains two pages and a complete memory phrase on page two. Both earlier glyph defects and all 16 substitution-bearing speeches pass. [Complete visual proof](../work/Rafael_B0_B34_clean_20261106/complete_visual_review_v1.json).

The [stored proof](../work/Rafael_B0_B34_clean_20261106/stored_v1/stored_native_verification.json) checks 284 pages, complete glyphs and pagination, 675 relative cases and all 283 pre-macro body bindings. Whole archive/cache checking covers 343 blocks and 686 modes, reusing exact unchanged dependencies. The qualified source-bound production transaction reproduces all 283 stored references and the whole Rafael4903 inverse.

The [initialized emulator sequence](../work/Rafael_B0_B34_clean_20261106/research_final_v1/actual_review.json) observed 95 utterances, 96 pages and all 39 scoped speaker headers in 28,001 frames. All 16 capture sheets were directly reviewed. The poem's page turn, two corrected leading glyphs, combined FI/FA substitutions, battle reminder, complete selected poem exchange and Aziza's final recruitment exchange passed. The other 188 utterances are offline-only. This uses retained Lisbon display initializers, not natural quest activation, original locations or chronology. Battle/tavern event transitions, a full route and hardware remain unvisited.

The three exclusive middle-field repairs use nine changed ARM9 data bytes: Dinis de Albuquerque, Antony von Kuhn and Garcia de Oviedo. Progressive labels remain unchanged. Original getters, native glyphs, ownership, allocation and inverse checks passed. Full catalogue UI remains unvisited. These are text defects, separate from graphics artwork. Both research ROMs remain preserved; neither is a registered test candidate.

Continue with the separately qualified owned-name stage, cumulative registration, exact clean-input patch, candidate-owned startup and original getters, then credit the 283 records once. Preserve the accepted ASCII right-bound correction, all prior layers, promoted main and weekend package. All storylines, shared/town/random dialogue and remaining player-facing prose remain in scope. Artwork and the later older-record re-audit stay separate. No guide photos are collected.
'''
    checkpoint(mutation=ROOT/'research_checkpoint_v1',batch_key='Rafael_SC0_B0_B34_clean_20261106',
        batch_updates=dict(new_credit=0,five_gate_research_records=283,prose_revisions=162,
            justified_retentions=121,formatting_pending=False,remaining_display_checks=0,
            remaining_wrap_candidates=0,refined_layouts_checked=19,justified_layout_retentions=1,
            representative_gameplay_pending=False,representative_utterances=95,representative_pages=96,
            representative_name_headers=39,offline_only_speech_variants=188,scoped_names_reviewed=39,
            stored_pages=284,relative_cases=675,registered_integration_pending=True,native_job_live=False,
            guide_photos=False,evidence={str(p):digest(p) for p in (ready_path,QUALIFICATION,Path(__file__))}),
        summary=summary,document='docs/editorial_Rafael_B0_B34_research_20261106.md',document_text=doc,
        completed=16748,protected={str(REGISTRY):release['registry_sha256'],
            release['canonical_base']:release['canonical_sha256'],release['candidate']:release['candidate_sha256'],
            release['patch']:release['patch_sha256'],package['zip']:package['zip_sha256']})
    print('Saved completed residual SC0 research; registration pending, integrated credit unchanged.')


if __name__=='__main__':main()
