"""Save the completed offline display/storage pass without gameplay or integration credit."""
from pathlib import Path
from scripts.audit_story_glyph_consistency import load
from scripts.prepare_hodram_B281_B300_formatting_v1 import ROOT,PROSE
from scripts.build_registered_hodram_B251_B280_v1 import RELEASE,REGISTRY
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest
from scripts.save_editorial_progress_checkpoint_v7 import checkpoint
from scripts.save_rafael3222_weekend_checkpoint_v1 import PACKAGE

def main():
    visual=ROOT/'final_visual_approval_v5.json'
    reconstruction=ROOT/'rebuilt_v1/reconstruction.json'
    stored=ROOT/'stored_v1/stored_native_verification.json'
    loaders=ROOT/'loaders_v1/verification.json'
    catalogue=ROOT/'stored_catalogue_all_v1/all373_stored_effective_body_bindings.json'
    names=Path('translations/hodram_B281_B300_scoped_names_review_v1.json')
    terms=ROOT/'scoped_terms_v1.json'
    prose,view,rebuilt,storage,loader,lookup=map(load,(PROSE,visual,reconstruction,stored,loaders,catalogue))
    assert prose['counts']==dict(revision=181,retention=203) and len(prose['records'])==384
    assert all(r['review']==dict(source=True,context=True,localization=True,naturalness=True,formatting=False) for r in prose['records'])
    assert view['final_speech_pages_visually_approved'] and view['final_pages']==374
    assert (view['visual_layout_revisions'],view['visual_candidate_retentions'],view['corrected_FE_blank_rows'],view['scoped_punctuation_glyph_fixes'])==(28,2,1,5)
    assert rebuilt['changed_blocks']==list(range(281,301)) and rebuilt['compound_objects']==23
    assert (rebuilt['command_count'],rebuilt['relative_sites'])==(934,283)
    assert (storage['complete_stored_pages'],storage['typed_labels_checked'],storage['fresh_relocated_native_relative_cases'])==(374,11,1415)
    assert (storage['fresh_parity_dependent_pages'],storage['exact_compiled_pages_reused'])==(108,266)
    assert storage['every_byte_consumed_andall_first_internal_final_glyphs_bounds_canaries_andpagination_pass']
    assert (loader['fresh_whole_archive_loads_andcache_hits'],loader['fresh_parent_cases'],loader['exact_reused_parent_cases'])==(325,40,610)
    assert lookup['all373_ordinary_and_style_bodies_checked'] and len(lookup['records'])==373
    for proof in [storage,loader]:assert proof['reconstruction_sha256']==digest(reconstruction)
    assert lookup['stored_sha256']==digest(stored) and digest(rebuilt['research_ROM'])==rebuilt['research_ROM_sha256']
    release,package=map(load,(RELEASE,PACKAGE))
    summary=('Hodram B281–B300 has 384 contextual decisions: 181 proposed revisions and 203 justified retentions. '
        'All 374 final pages, 18 scoped actors/17 name strings and five menus pass offline native/visual checks. '
        'Twenty-eight wraps, one native FE blank row and five punctuation glyph targets are corrected; two layouts are retained with reasons. '
        'Stored checks pass for all 374 pages, 11 captions, 1,415 branch cases and 373 catalogue lookups; archive loading passes. '
        'Representative scene gameplay, individual fifth-gate sealing and registered integration remain. Integrated coverage stays 17,749; main is unchanged.')
    evidence_paths=(PROSE,names,terms,visual,reconstruction,stored,loaders,catalogue,
        ROOT/'native_styles_v5/compiled_style_objects.json',ROOT/'scoped_names_visual_approval_v1.json',Path(__file__))
    evidence={str(p):digest(p) for p in evidence_paths}
    document=f'''# Hodram B281–B300: offline display and storage checkpoint

{summary}

The [contextual manuscript](../{PROSE.as_posix()}) preserves all 384 source-first decisions and exact source/current references; no prose was changed in this display pass. See the [earlier contextual checkpoint](editorial_Hodram_B281_B300_contextual_20261107.md) for exchange-level findings. The scope is 242 ordinary speeches, 131 physical voice alternatives/144 source slots in 18 objects, and 11 captions in five menus. All first four individual gates remain true; all 384 fifth gates remain false until the required gameplay and final qualification pass.

The [name review](../{names.as_posix()}) retains all 18 actors with individual reasons. Thirty-six fresh original getters and all 17 distinct progressive name strings pass. Clean fields, full-name references and source relationships are bound; opaque metadata is not used to invent identity. The [term bindings](../{terms.as_posix()}) verify Ancient City Map, Saltpeter, Sulfur, Timber and city aliases, preserving nonname metadata. These are scoped bindings and compatible earlier proofs, not new full-catalogue UI, ownership or older-record technical-audit claims.

The [visual approval](../{visual.as_posix()}) binds all 375 initial pages and 29 newly generated pages, each directly viewed in readable sheets, plus all name and menu sheets. Final coverage is 373 bodies/374 pages. Twenty-eight layouts improve phrase and page continuity; two retain the better originals with individual reasons. B287 R125 now fits one page without shortening prose. B282 R19 still needs two pages, but keeps Iscal Yasar and the complete final sentence together. The retained balanced bear reaction avoids a sparse We tried opening or an orphaned run. The gunpowder phrase a great deal already worked and retains identical bytes. No manual ordinary breaks, QA waivers, font/engine changes or shortened prose are introduced.

The actual native FE defect at B290 R148 inserted an unintended blank row when a guarded 36-character first line wrapped before its LF. A source-bound 35-cell planning budget for that record alone fixes the two intended rows while native 228-pixel geometry remains unchanged. Failed artifacts and the row diagnostic remain preserved. Five source-qualified mixed-font punctuation targets pass fresh checks: B283 R100, B290 R179 and B296 R33 use ASCII periods; B287 R65 uses an ASCII question mark; B290 R92 uses ASCII exclamation marks. No global normalization was applied.

All complete leading/internal/trailing glyphs, native controls, runtime substitutions, guard bytes, bounds, consumption and pagination pass. Only the 28 byte-changed layouts were freshly rendered; 345 identical bodies reuse exact proofs. Eleven changed voice objects pass 88 fresh original target-slot cases and 99 negative cases; seven unchanged objects reuse exact inputs/compiled bytes, yielding all 144 slots/162 semantic rejection cases. Five menu providers and complete caption/highlight planes pass. These checks do not imply actual conditional character participation.

The [research reconstruction](../{reconstruction.as_posix()}) changes only the 20 reviewed SC1 blocks over registered B251–B280, preserving every other file/component, all runtime/name/artwork layers and exact source/current/archive/serialized parent inverses. Its SHA-256 is `{rebuilt['research_ROM_sha256']}`. This research ROM is not a registered handoff or main build; every generated ROM remains preserved.

The [stored verification](../{stored.as_posix()}) covers 374 pages: 108 fresh parity-dependent checks and 266 exact native-page reuses. All 11 captions and 1,415 native branch cases pass. The [catalogue verification](../{catalogue.as_posix()}) checks all 373 original pre-macro lookups with complete buffers, guards and unowned RAM unchanged. The [archive proof](../{loaders.as_posix()}) covers 325 complete loads/cache hits, 40 fresh parent cases and 610 compatible exact reuses. All are offline checks, not controller gameplay or proof of naturally earned rewards, branches or locations.

Next sample representative emulator scenes for the corrected injury FE rows, the two-page royal conclusion, the one-page map response, all distinct menu behavior, dynamic headers/voice fallbacks, substitutions, gunpowder exchange and transitions. Reuse compatible proofs instead of activating every conditional speech. Current B281–B300 gameplay remains unvisited. Then seal individual fifth gates, register a cumulative successor, reconstruct its clean-input patch exactly and verify its own startup before adding the 384 records once. No test/build process remains live at this checkpoint.

Integrated totals remain 17,749: 10,828 revisions and 6,921 retentions; historical source/prose counters remain 17,752. Main, current registered candidate, clean/canonical inputs and weekend package are unchanged. The full goal stays active, including every storyline, shared town/shop/random exchange, unfinished earlier contextual pass, names and remaining player-facing prose, with Rafael/tutorial priority. Deferred graphics artwork and the later older-record technical re-audit stay separate. No guide photos.
'''
    checkpoint(mutation=ROOT/'stored_checkpoint_v1',batch_key='Hodram_B281_B300_clean_next_20261107',
        batch_updates=dict(new_credit=0,scoped_names_pending=False,scoped_terms_pending=False,fresh_native_body_pages_pending=False,
            scoped_name_actors_reviewed=18,scoped_name_strings_checked=17,fresh_original_name_getters=36,
            stored_reconstruction_pending=False,final_native_pages=374,visual_layout_revisions=28,justified_layout_retentions=2,
            FE_blank_row_wrap_fixes=1,glyph_targets_corrected=5,stored_pages_passed=374,typed_captions_checked=11,
            native_relative_cases_passed=1415,stored_catalogue_lookups_passed=373,archive_loading_pass=True,
            current_story_gameplay_utterances=0,representative_gameplay_pending=True,registered_integration_pending=True,
            all_five_review_gates_pending=True,all_formatting_gates_pending=True,native_job_live=False,registered_build_live=False,
            contextual_manuscript=str(PROSE),contextual_manuscript_sha256=digest(PROSE),evidence=evidence),
        additional_updates={'editorial_execution_priority_20261104':dict(new_credit=0,
            current_batch='Hodram B281–B300: all384 contextual decisions and all374 offline display/stored pages pass.',
            next_action='Representative scene gameplay, individual fifth gates and registered cumulative integration with exact clean patch and own startup.',
            current_batch_not_yet_integrated=True,all_current_batch_fifth_gates_pending=True,registered_integration_pending=True,
            native_job_live=False,registered_build_live=False,registered_cumulative_build_live=False,guide_photos=False)},
        summary=summary,document='docs/editorial_Hodram_B281_B300_stored_20261107.md',document_text=document,completed=17749,
        protected={str(REGISTRY):release['registry_sha256'],release['canonical_base']:release['canonical_sha256'],
            release['candidate']:release['candidate_sha256'],release['patch']:release['patch_sha256'],package['zip']:package['zip_sha256']})
    print('Saved all384 prose decisions and374 offline pages; 17,749 integrated records unchanged. Gameplay/integration remain; full goal active.')

if __name__=='__main__':main()
