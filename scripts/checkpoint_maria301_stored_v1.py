"""Save the checked Maria storage transaction without adding release credit."""
from pathlib import Path
from scripts.audit_story_glyph_consistency import load
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest
from scripts.save_editorial_progress_checkpoint_v8 import checkpoint

ROOT = Path('work/Maria_B0_B32_clean_20261109')


def main():
    paths = dict(reconstruction=ROOT/'stored_reconstruction_v1/reconstruction.json',
        stored=ROOT/'stored_v1/stored_native_verification.json',
        catalogue=ROOT/'stored_catalogue_all_v1/all299_stored_effective_body_bindings.json',
        loaders=ROOT/'loaders_v1/verification.json',
        visual=ROOT/'offline_display_approval_v1.json',
        manuscript=ROOT/'storage_inputs_v1/storage_manuscript.json')
    d = {k: load(p) for k, p in paths.items()}
    rebuilt, stored, catalogue, loaders = [d[k] for k in ['reconstruction', 'stored', 'catalogue', 'loaders']]
    assert (rebuilt['speech_count'], rebuilt['style_physical_speech_count'], rebuilt['typed_choice_count']) == (292, 7, 2)
    assert len(rebuilt['changed_blocks']) == 32 and rebuilt['command_count'] == 606 and rebuilt['relative_sites'] == 127
    assert rebuilt['full_clean_current_block_archive_andserialized_NDS_inverses_exact']
    assert rebuilt['all_other_files_components_exact']
    assert digest(rebuilt['research_ROM']) == rebuilt['research_ROM_sha256']
    assert (stored['complete_stored_pages'], stored['fresh_parity_dependent_pages'], stored['exact_compiled_pages_reused'], stored['fresh_relocated_native_relative_cases']) == (303, 148, 155, 635)
    assert stored['every_byte_consumed_andall_first_internal_final_glyphs_bounds_canaries_andpagination_pass']
    assert stored['all_stored_planes_equal_directly_viewed_compiled_planes']
    assert len(stored['records']) == 292 and len(stored['style_records']) == 7 and stored['typed_labels_checked'] == 2
    assert catalogue['all299_ordinary_and_style_bodies_checked'] and len(catalogue['records']) == 299
    assert (loaders['fresh_whole_archive_loads_andcache_hits'], loaders['fresh_parent_cases']) == (303, 606)
    for key in ['stored', 'loaders']:
        assert d[key]['reconstruction_sha256'] == digest(paths['reconstruction'])
    assert catalogue['stored_sha256'] == digest(paths['stored'])
    assert d['visual']['every_final_page_directly_viewed_in_readable_sheets']
    assert all(r['review'] == dict(source=True, context=True, localization=True, naturalness=True, formatting=False) for r in d['manuscript']['records'])
    release = load('work/hodram_residual_release_v1/registered_release_verification.json')
    summary = ('Maria301 now passes stored-script checks: 32 SC3 blocks, 303 final pages, '
        '635 native branch cases, all 299 catalogue lookups and 303 complete loads/606 parent handoffs. '
        'The 178 prose revisions, 123 retentions, 35 wrap improvements and glyph correction are preserved. '
        'Representative gameplay and registered integration remain; fifth gates are still false. '
        'Integrated coverage stays 19,161; registered f166991f and main are unchanged.')
    text = '''# Maria301 stored-script checkpoint — November 9, 2026

The source-first editorial and direct visual review are complete offline. Reuse
[the offline checkpoint](editorial_Maria301_offline_display_20261109.md): 178
revisions, 123 justified retentions, 35 wrap improvements, two layout retentions,
one reclaimed page, all 303 final body pages, 44 names and two captions viewed.

The source-qualified transaction in
`work/Maria_B0_B32_clean_20261109/stored_reconstruction_v1/reconstruction.json`
passes all 32 reviewed SC3 blocks, 606 commands and 127 relative sites. Only SC3
changes; the complete archive and serialized parent ROM restore byte for byte.
The registered ASCII right-bound runtime, names, other routes, artwork and all
other components remain exact. The research ROM is not a release or test handoff:
`stored_reconstruction_v1/reviewed_RESEARCH_ONLY.nds`, SHA-256
`c9b583a629a327e7e4893e3d10d57c5e7a4c591f724354ac9561937cba6cfa01`.

`stored_v1/stored_native_verification.json` checks 292 ordinary speeches, seven
physical alternatives/eight native style slots and the two menu captions. All
303 final pages pass: 148 alignment-dependent pages are freshly rendered and
match the directly viewed planes; 155 reuse exact compiled buffers, runtime,
font and planes. All 635 native relative-branch cases pass. Substitutions use
the current Maria context, FI5/FA2/FO7/FU15, not historical name assumptions.
No unrelated FE characterization was repeated or FE approval inferred.

`stored_catalogue_all_v1/all299_stored_effective_body_bindings.json` verifies
every body through the original pre-macro catalogue lookup, complete buffers,
stack and four-MiB unowned-memory guards. `loaders_v1/verification.json` verifies
303 whole SC3 loads/cache hits and 606 original parent handoffs/first reads.
These are controlled native checks, not naturally activated events. Other
unchanged routes were not replayed.

Next use focused cold-boot QA for the four two-page speeches (B4R9, B8R5,
B18R36, B30R20), B24R11's new four-row page, the B14R5 glyph, B29 menu/ordinary
controller return and representative names/voice styles/transitions. Copy
complete native commands and disclose synthetic sequence versus natural story
activation. The existing Maria opening-to-Hangzhou run is context evidence,
not this changed dialogue's gameplay coverage. Do not rerun completed offline
checks absent changed dependencies or failures.

All 301 fifth gates remain false pending necessary representative tests and
registered integration. Credit stays 19,161; 6,737 native story objects remain,
including this pending batch. Register a cumulative successor and exactly
reconstructable clean-input patch before credit. Main remains unchanged and
requires user acceptance for promotion. Preserve all ROMs, translations and
evidence. No guide photos. Full editorial scope remains active; deferred artwork
and the later older-record technical re-audit remain separate.
'''
    checkpoint(mutation='work/Maria301_stored_checkpoint_20261109',
        batch_key='editorial_execution_priority_20261104',
        batch_updates=dict(new_credit=0, current_batch='Maria301 stored checks passed; representative gameplay next.',
            current_batch_not_yet_integrated=True, all_current_batch_fifth_gates_pending=True,
            next_action='Representative pagination, glyph, menu/return and style gameplay; then registered cumulative integration.', guide_photos=False),
        additional_updates={'Maria_SC3_B0_B32_clean_20261109':dict(
            stored_checks_pass=True, stored_evidence={str(p):digest(p) for p in paths.values()},
            stored_pages=303, stored_branch_cases=635, stored_catalogue_bodies=299,
            whole_native_archive_loads=303, native_parent_handoffs=606,
            stored_andrepresentative_gameplay_pending=True, representative_gameplay_pending=True,
            all_fifth_formatting_gates_pending=True, registered_integration_pending=True, new_credit=0)},
        summary=summary, document='docs/editorial_Maria301_stored_20261109.md', document_text=text,
        completed=19161, protected={'translations/release_stack.json':release['registry_sha256'],
            release['candidate']:release['candidate_sha256'], release['manifest']:release['manifest_sha256'],
            release['patch']:release['patch_sha256'],
            'out/raphael_natural_v2_accepted_base.nds':'3cb827e4c52ab2086fb5a626835d72192085a958581279d3c79b0200bbf405fe'})
    print('Saved303-page stored checkpoint; zero new credit; current registered candidate and main unchanged.')


if __name__ == '__main__':
    main()
