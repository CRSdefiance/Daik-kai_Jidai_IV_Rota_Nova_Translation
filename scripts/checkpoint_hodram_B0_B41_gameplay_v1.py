"""Save the completed research gates and exact next mixed-release work without integration credit."""
from pathlib import Path
from scripts.audit_story_glyph_consistency import load
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest
from scripts.save_editorial_progress_checkpoint_v7 import checkpoint
from scripts.save_rafael3222_weekend_checkpoint_v1 import PACKAGE

ROOT=Path('work/Hodram_B0_B41_clean_20261107')
RELEASE=Path('work/hodram_B311_B324_release_v1/registered_release_verification.json')
REGISTRY=Path('translations/release_stack.json')
FINAL=Path('translations/hodram_B0_B41_final_review_v2.json')

def main():
    paths=dict(final=FINAL,ready=ROOT/'research_final_v2/research_completion.json',actual=ROOT/'gameplay_review_v1.json',
        visual=ROOT/'offline_visual_approval_v2.json',stored=ROOT/'stored_v2/stored_native_verification.json',
        reconstruction=ROOT/'stored_reconstruction_v3/reconstruction.json',catalogue=ROOT/'stored_catalogue_all_v2/all388_stored_effective_body_bindings.json',
        loaders=ROOT/'loaders_v2/verification.json',mixed=ROOT/'mixed_research_v2/research_reference.json',
        names=Path('translations/hodram_B0_B41_scoped_names_final_v1.json'),fields=Path('translations/hodram_B0_B41_owned_surnames_final_v1.json'),
        native_fields=ROOT/'research_final_v1/owned_surnames_native_approved.json',
        glyph_model=ROOT/'opaque_pixel_model_qualification_v1.json')
    d={k:load(p) for k,p in paths.items()};ready=d['ready'];actual=d['actual'];doc=d['final']
    assert ready['manuscript_sha256']==digest(FINAL) and ready['all_individual_five_gates_pass']
    assert (ready['records'],ready['revisions'],ready['retentions'],ready['body_pages'])==(394,221,173,389)
    assert all(all(r['review'][g] for g in ['source','context','localization','naturalness','formatting']) for r in doc['records'])
    assert (actual['frames'],actual['distinct_source_utterances'],actual['distinct_body_pages'],actual['offline_only_source_utterances'])==(57363,169,170,219)
    assert actual['all_three_native_menus_default_selection_andordinary_A_returns_observed'] and actual['all_three_final_resupply_returns_directly_viewed']
    assert actual['all_three_changed_progressive_names_observed_complete'] and len(actual['reviewed_body_sheets'])==17
    assert d['stored']['complete_stored_pages']==389 and d['stored']['fresh_relocated_native_relative_cases']==685
    assert d['stored']['fresh_parity_dependent_pages']==1 and d['stored']['exact_compiled_pages_reused']==388
    assert d['catalogue']['stored_sha256']==digest(paths['stored']) and d['catalogue']['all388_ordinary_and_style_bodies_checked']
    assert (d['loaders']['fresh_whole_archive_loads_andcache_hits'],d['loaders']['fresh_parent_cases'],d['loaders']['exact_reused_parent_cases'])==(325,2,648)
    assert d['mixed']['complete_registered_parent_inverse_exact'] and digest(d['mixed']['research_ROM'])==d['mixed']['research_ROM_sha256']
    assert len(d['names']['records'])==42 and d['names']['all42_individual_five_gates_pass']
    assert len(d['fields']['records'])==3 and d['fields']['all3_owned_fields_five_gates_pass']
    assert d['glyph_model']['all8_mutations_rejected']
    release,package=map(load,(RELEASE,PACKAGE))
    summary=('All 394 residual Hodram B0–B41 reviews now pass five gates in research: 221 revisions/173 retentions. '
        'All 389 final pages, six captions and 42 names are checked; five visual wrap fixes, the FE blank-row repair and three surname fixes pass. '
        'Three emulator runs observe 169 distinct utterances/170 pages, the corrected headers, all three menus/default A returns and all resupply transitions. '
        'Final stored checks pass, reusing 388 pages and rendering only the additional tutorial wrap. '
        'Mixed registered integration remains; integrated coverage is 18,767 and main is unchanged.')
    document=f'''# Hodram residual review: gameplay complete, mixed integration next

{summary}

- [Final 394 reviews](../{FINAL.as_posix()}) and [research completion](../{paths['ready'].as_posix()}): exact source/current/stored references, individual findings, justified retentions and all five gates. No integration credit has been added. The original 32 tutorial prose decisions remain unchanged.
- [Gameplay evidence and visual approval](../{paths['actual'].as_posix()}): three cold-boot native display sequences, 57,363 frames; 169 distinct source variants/170 final pages. All 15 broad contact sheets, the corrected-name sheet, final wrap sheet, three-menu sheet and three final resupply screens were directly viewed. This is initialized display QA, not natural activation of original story events or hardware coverage. The remaining 219 body variants are offline-only. Original choices, chronology, rewards and future party assignments remain unvisited; all three menus show default option 0 and its ordinary A return. Other choices/cancel retain the offline VM proofs.
- [Final stored checks](../{paths['stored'].as_posix()}): 389 pages, six captions and 685 native branch cases. Gameplay revealed one more All/hands split in B29R59. The final layout keeps “All hands” together. Fresh native checks cover that one page; 340 unchanged ordinary records and all 47 style bodies reuse exact byte/position/prefix/parity/runtime/font/plane proofs. The stored audit renders only one parity-dependent page and reuses the other 388. Five final visual wrap corrections, the earlier contrast-phrase wrap and FE blank-row repair remain; no additional prose changes.
- [Final catalogue](../{paths['catalogue'].as_posix()}) and [archive proof](../{paths['loaders'].as_posix()}): all 388 effective buffers and all 325 loads/cache hits pass. Only B29 needs two fresh parent cases; the other 648 cases match exactly. The incremental verifier distinguishes this one-block delta from the full 39-block registered-parent reconstruction.
- [Names](../{paths['names'].as_posix()}), [three exclusive surname reviews](../{paths['fields'].as_posix()}) and [approved native field proof](../{paths['native_fields'].as_posix()}): David Flahven, Georg Salzgitter and Nagayoshi Kamuro have complete observed corrected headers. Both original getters, all 12 current/proposed planes, eight malformed-field rejections, the original pointers/terminators/adjacency and the exact 28-byte inverse remain qualified. Full catalogue UI is unvisited.
- [Opaque-glyph pixel qualification](../{paths['glyph_model'].as_posix()}): two deliberately opaque source cries use style-1 ink and style-15 shadow. Their independent complete color masks both match actual pixels. Eight missing/extra ink/shadow mutations are rejected. No text, font, ROM or capture changed to satisfy the check. The initial single-ink analyzer rejection and the two failed selector-metadata adapters are preserved.
- [Final mixed research target](../{paths['mixed'].as_posix()}): `{d['mixed']['research_ROM']}`, SHA-256 `{d['mixed']['research_ROM_sha256']}`. It contains the final reviewed SC1 and only the three approved surname spans. The exact story-only and complete registered-parent inverses execute successfully. This is research evidence, not a registered testing candidate or promoted main.

The broad run initially observes the old three headers; the later focused run observes their corrected forms. The final merged evidence selects those corrected samples and the later final tutorial-wrap sample. Every final selected body plane equals the final compiled native plane. Nothing is relabeled as fresh gameplay. Source actor identities come from the qualified controls/role bindings, not portrait similarity. All full-frame originals, earlier native/ROM outputs and failed experiments remain.

The v1 finalizer sealed the 394 valid story rows, then stopped on missing mapped-speaker metadata in the projected name document. V2 independently revalidated every guard and read the saved story document back byte-for-byte, then supplied explicit name IDs, speakers, context and meanings. The final story v2 only reconciles stale intake-stage pending labels; its English, decisions, five gates and exact references are unchanged. Ready evidence is `research_final_v2/research_completion.json`; use its manuscript and release-plan hashes, not the earlier partial producer status.

Next prepare and qualify a registered mixed successor over [B311–B324](editorial_Hodram_B311_B324_registered_20261107.md), using the Rafael5186 mixed workflow. The dialogue transaction owns only the 39 reviewed SC1 blocks; the surname transaction owns only 28 existing ARM9 data bytes. Preserve all 706 predecessor entries, 114 accepted layers and the ASCII right-bound correction. Freeze the exact final review, stored/native/visual/gameplay/field dependencies; run the original transaction/allocation/format/inverse guards and malformed-input checks. Stage the cumulative ROM, reconstruct it exactly from clean input, verify its own startup and original protected-name getters including actors 55/56/57, then register and credit the batch once. Do not promote main without acceptance.

Registered candidate, baseline, patch, main and weekend ZIP remain unchanged. No process is live. Full editorial scope remains active across remaining routes, earlier unfinished passes, town/shop/random dialogue, names and remaining prose. Preserve Rafael/tutorial priority, separate artwork and the later older-record technical re-audit; no guide photos.
'''
    evidence={str(p):digest(p) for p in [*paths.values(),Path(__file__)]}
    checkpoint(mutation=ROOT/'gameplay_checkpoint_v1',batch_key='Hodram_SC1_B0_B41_clean_next_20261107',
        batch_updates=dict(new_credit=0,current_English_comparisons=394,contextual_decisions=394,
            four_prose_gate_records=394,five_gate_research_records=394,proposed_revisions=221,justified_retentions=173,
            offline_final_pages=389,visual_wrap_corrections=5,remaining_offline_display_checks=0,remaining_display_checks=0,
            all_fifth_gates_pending=False,all_five_gates_research_pass=True,
            representative_gameplay_pending=False,actual_initialized_runs=3,actual_frames=57363,actual_distinct_utterances=169,
            actual_distinct_pages=170,offline_only_utterances=219,actual_menus=3,actual_corrected_name_headers=3,
            all_three_resupply_returns_observed=True,stored_pages_passed=389,stored_fresh_parity_pages=1,stored_exact_reused_pages=388,
            native_relative_cases_passed=685,stored_catalogue_lookups_passed=388,archive_loading_pass=True,
            name_actual_headers_andregistered_layer_pending=True,name_actual_headers_pending=False,registered_integration_pending=True,evidence=evidence),
        additional_updates={'editorial_execution_priority_20261104':dict(new_credit=0,
            current_batch='Hodram residual394 five-gate research complete; mixed registered integration next.',
            next_action='Freeze and qualify SC1 plus three owned surnames; preserve706-entry/114-layer prefix, exact clean patch, own startup andprotected getters before registration/credit.',
            current_batch_not_yet_integrated=True,all_current_batch_fifth_gates_pending=False,native_job_live=False,
            registered_build_live=False,registered_cumulative_build_live=False,guide_photos=False)},
        summary=summary,document='docs/editorial_Hodram_B0_B41_gameplay_20261107.md',document_text=document,
        completed=18767,protected={str(REGISTRY):release['registry_sha256'],release['canonical_base']:release['canonical_sha256'],
            release['candidate']:release['candidate_sha256'],release['patch']:release['patch_sha256'],package['zip']:package['zip_sha256']})
    print('Saved394 completed research reviews andmixed release handoff;18767 integrated,no new credit,no main change.')

if __name__=='__main__':main()
