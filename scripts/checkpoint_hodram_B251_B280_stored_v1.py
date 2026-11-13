"""Save completed display/storage work without granting gameplay or release credit."""
from pathlib import Path
from scripts.audit_story_glyph_consistency import load
from scripts.bind_hodram_B251_B280_terms_v1 import ROOT, PROSE, TERMS
from scripts.build_registered_hodram_B231_B250_v1 import RELEASE, REGISTRY
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest
from scripts.save_editorial_progress_checkpoint_v7 import checkpoint
from scripts.save_rafael3222_weekend_checkpoint_v1 import PACKAGE


def main():
    visual = ROOT / 'final_visual_approval_v5.json'
    reconstruction = ROOT / 'research_rebuilt_v1/reconstruction.json'
    stored = ROOT / 'stored_v1/stored_native_verification.json'
    loaders = ROOT / 'loaders_v1/verification.json'
    catalogue = ROOT / 'stored_catalogue_all_v1/all209_stored_effective_body_bindings.json'
    prose, view, rebuilt, storage, loader, lookup = map(load, (PROSE, visual, reconstruction, stored, loaders, catalogue))
    assert prose['counts'] == {'revision': 129, 'retention': 87}
    assert len(prose['records']) == 216
    assert all(r['review'] == dict(source=True, context=True, localization=True, naturalness=True, formatting=False)
               for r in prose['records'])
    assert view['final_speech_pages_visually_approved'] and view['final_pages'] == 212
    assert len(rebuilt['changed_blocks']) == 30 and rebuilt['compound_objects'] == 5
    assert storage['complete_stored_pages'] == 212 and storage['typed_labels_checked'] == 7
    assert storage['fresh_relocated_native_relative_cases'] == 660
    assert storage['every_byte_consumed_andall_first_internal_final_glyphs_bounds_canaries_andpagination_pass']
    assert loader['fresh_whole_archive_loads_andcache_hits'] == 325
    assert loader['fresh_parent_cases'] == 60 and loader['exact_reused_parent_cases'] == 590
    assert lookup['all209_ordinary_and_style_bodies_checked']
    for proof in (storage, loader):
        assert proof['reconstruction_sha256'] == digest(reconstruction)
    assert digest(rebuilt['research_ROM']) == rebuilt['research_ROM_sha256']
    release, package = map(load, (RELEASE, PACKAGE))
    summary = ('Hodram B251–B280 has 216 contextual decisions: 129 proposed revisions and 87 justified retentions. '
        'All 212 final pages, 21 scoped names and three menus pass offline native/visual checks. '
        'Thirteen wraps, one FE warning wrap and two glyph targets are corrected; three layout alternatives retain the better originals. '
        'Stored checks pass for 212 pages, seven captions, 660 branch cases and all 209 catalogue lookups; archive loading passes. '
        'Representative scene gameplay and registered integration remain. Integrated coverage stays 17,533; main is unchanged.')
    evidence_paths = (PROSE, TERMS, visual, reconstruction, stored, loaders, catalogue, Path(__file__))
    evidence = {str(p): digest(p) for p in evidence_paths}
    document = f'''# Hodram B251–B280: display and storage checkpoint

{summary}

Continue the complete source/context review saved in [the contextual checkpoint](editorial_Hodram_B251_B280_contextual_20261107.md).
The current [contextual manuscript](../{PROSE.as_posix()}) supersedes v1 only for two source-qualified Sao Jorge spellings, reclassifying one retention as a revision. The other 214 decisions are unchanged. The approved city name is Sao Jorge; the earlier contextual checkpoint's proposed San Jorge reference is superseded. A separate untranslated city alias remains for the later technical audit. Scoped city spans are term bindings, not new C-string ownership or UI proofs.

The [final visual receipt](../{visual.as_posix()}) binds every approved page. All 214 initial body pages and the name/menu sheets were directly viewed. Thirteen refined records generated 14 freshly checked and viewed pages; the final joined scope is 209 bodies/212 pages. Complete leading/internal/trailing glyphs, controls, substitutions, guards, bounds and pagination pass. Names and short question tags stay together where validated. Two avoidable page turns are removed. Three alternatives retain their original layouts because the trials read worse or fail checks; no prose is shortened and no QA waiver is used.

The actual FE failure at B252 R184 split think after thin before a protected LF. The existing scoped FE36 formatting rule fixes it without changing native geometry or the engine. Failed plans and diagnostics are preserved. B252 R116's mixed full-width punctuation becomes ASCII ?! and B274 R15's lowercase l becomes I. These are text-display corrections, separate from graphics artwork. All 16 style bodies remain exactly identical to the original qualified compound proof. Three source-indexed menus contain seven captions; original native providers, cancellation and complete label planes pass.

The [research reconstruction](../{reconstruction.as_posix()}) changes only the reviewed 30 SC1 blocks over registered Hodram B231–B250. It contains 193 ordinary speeches, 16 physical alternatives and seven captions, with complete source/current block/archive/serialized inverses. Research ROM SHA-256: `{rebuilt['research_ROM_sha256']}`. This is not a registered handoff or main build. Every generated ROM is preserved.

The [stored verification](../{stored.as_posix()}) checks 212 pages: 113 fresh parity-dependent checks and 99 exact compiled-page reuses. All seven captions and 660 relocated native branch cases pass. The [original catalogue lookup](../{catalogue.as_posix()}) binds all 209 ordinary/style bodies. The [loader verification](../{loaders.as_posix()}) covers 325 whole archive loads/cache hits, 60 fresh parent cases and 590 exact compatible reuses. These are offline native checks, not optional scene activation or controller gameplay.

Next use representative emulator scenes for distinct FE categories, pagination, headers/substitutions, menu selections and transitions. Reuse unchanged consumer proofs; do not activate every conditional line. All actual B251–B280 scene content remains unvisited so far. Then seal individual fifth gates and use the registered cumulative workflow, exact clean-input patch and candidate-owned startup before credit. No live test/build process remains.

Integrated totals remain 17,533: 10,699 revisions and 6,834 retentions. Historical source/prose counters remain 17,536. All 216 current fifth gates and registered integration remain pending. Main, canonical base, registered candidate, clean input, runtime bounds and weekend package are unchanged. Keep all remaining storylines/shared town/shop/random prose and unfinished earlier contextual passes in scope, with Rafael/tutorial priority. Preserve deferred graphics and later older-record re-audit separately. No guide photos. The full goal remains active.
'''
    checkpoint(mutation=ROOT/'stored_checkpoint_v1', batch_key='Hodram_B251_B280_clean_next_20261107',
        batch_updates=dict(new_credit=0, proposed_revisions=129, justified_retentions=87,
            contextual_manuscript=str(PROSE), contextual_manuscript_sha256=digest(PROSE),
            scoped_terms_pending=False, fresh_native_body_pages_pending=False, stored_reconstruction_pending=False,
            final_native_pages=212, visual_layout_revisions=13, justified_layout_retentions=3, FE_warning_wrap_fixes=1,
            glyph_targets_corrected=2, stored_pages_passed=212, typed_captions_checked=7, native_relative_cases_passed=660,
            stored_catalogue_lookups_passed=209, archive_loading_pass=True, current_story_gameplay_utterances=0,
            representative_gameplay_pending=True, registered_integration_pending=True, all_five_review_gates_pending=True,
            all_formatting_gates_pending=True, native_job_live=False, registered_build_live=False, evidence=evidence),
        additional_updates={'editorial_execution_priority_20261104': dict(new_credit=0,
            current_batch='Hodram B251–B280: contextual, display, storage and loader checks pass.',
            next_action='Representative scene gameplay, individual fifth gates and registered cumulative integration.',
            current_batch_not_yet_integrated=True, all_current_batch_fifth_gates_pending=True,
            registered_integration_pending=True, native_job_live=False, registered_build_live=False,
            registered_cumulative_build_live=False, guide_photos=False)},
        summary=summary, document='docs/editorial_Hodram_B251_B280_stored_20261107.md', document_text=document,
        completed=17533, protected={str(REGISTRY): release['registry_sha256'],
            release['canonical_base']: release['canonical_sha256'], release['candidate']: release['candidate_sha256'],
            release['patch']: release['patch_sha256'], package['zip']: package['zip_sha256']})
    print('Saved display/storage checkpoint; 17,533 integrated records, 216 current fifth gates pending; full goal active.')


if __name__ == '__main__':
    main()
