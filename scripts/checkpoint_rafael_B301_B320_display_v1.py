"""Record the complete visual pass and reconstructed archive with no integration credit."""
from pathlib import Path

from scripts.audit_story_glyph_consistency import load
from scripts.checkpoint_rafael3894_registered_v1 import LEDGER, NEXT, PACKAGE, RELEASE
from scripts.checkpoint_rafael_B168_B169_research_v1 import link
from scripts.check_rafael_B301_B320_name_planes_v1 import RETAINED
from scripts.prepare_rafael_B301_B320_actual_v1 import SELECTION
from scripts.rebuild_rafael_B301_B320_reviewed_v1 import MENU, STYLES, VISUAL
from scripts.refine_rafael_B301_B320_plan_v1 import PROBE, PROSE, ROOT, digest
from scripts.save_editorial_progress_checkpoint_v6 import checkpoint
from scripts.verify_rafael_B301_B320_visual_delta_v1 import FINAL, PLAN
from scripts.write_rafael_B301_B320_contextual_v1 import TERMS


REBUILT = ROOT / 'rebuilt_v1/reconstruction.json'
LOADERS = ROOT / 'loaders_v1/verification.json'
STORED = ROOT / 'stored_v1/stored_native_verification.json'
LOOKUP = ROOT / 'stored_catalogue_all_v1/all442_stored_effective_body_bindings.json'
NEXT_PACKET = Path('work/Rafael_B321_B342_clean_20261106/clean_source_packet.json')
NEXT_STYLES = NEXT_PACKET.with_name('clean_style_objects.json')
NEXT_MENUS = NEXT_PACKET.with_name('clean_choice_objects.json')


def main():
    paths = (PROSE, TERMS, FINAL, PLAN, VISUAL, MENU, STYLES, RETAINED, PROBE,
             REBUILT, LOADERS, STORED, LOOKUP, SELECTION, NEXT_PACKET, NEXT_STYLES, NEXT_MENUS, Path(__file__))
    doc, native, plan, visual, menus, styles, names, rebuilt, loaders = map(load, (
        PROSE, FINAL, PLAN, VISUAL, MENU, STYLES, RETAINED, REBUILT, LOADERS))
    release, ledger, package = map(load, (RELEASE, LEDGER, PACKAGE))
    assert (doc['source_objects'], doc['proposed_revisions'], doc['justified_retentions']) == (453, 397, 56)
    assert native['runtime'] == names['runtime'] == styles['runtime'] == menus['runtime'] == doc['runtime']
    assert doc['current_ROM_sha256'] == release['candidate_sha256'] == ledger['current_integrated_candidate']['sha256']
    assert digest(PLAN) == native['plan_sha256'] == rebuilt['plan_sha256'] and not plan['failures']
    assert all(i['severity'] == 'info' for r in plan['records'] for i in r['base_QA']['issues'])
    assert (len(native['records']), native['pages'], native['fresh_visual_delta_records']) == (442, 444, 38)
    assert native['all_first_internal_final_glyph_codes_pixels_input_canaries_andbounds_pass']
    assert native['complete_consumption_andpagination_exact'] and not native['actual_gameplay']
    assert digest(FINAL) == visual['native_sha256'] == rebuilt['native_sha256']
    assert visual['all_final_body_caption_and_name_sheets_directly_viewed']
    assert all(digest(sheet['path']) == sheet['sha256'] for sheet in visual['sheets'])
    assert (len(menus['menus']), styles['native_target_slot_cases'], names['scoped_actors']) == (5, 152, 19)
    assert rebuilt['full_clean_current_block_archive_andserialized_NDS_inverses_exact']
    assert (sum(len(g['command_map']) for g in rebuilt['groups']), rebuilt['relative_sites']) == (720, 126)
    assert rebuilt['changed_blocks'] == list(range(301, 321))
    assert digest(REBUILT) == loaders['reconstruction_sha256']
    assert (loaders['fresh_whole_archive_loads_andcache_hits'], loaders['fresh_parent_cases'],
            loaders['exact_reused_parent_cases']) == (343, 40, 646)
    stored, lookup = map(load, (STORED, LOOKUP))
    assert stored['reconstruction_sha256'] == digest(REBUILT) and stored['native_sha256'] == digest(FINAL)
    assert stored['every_byte_consumed_andall_first_internal_final_glyphs_bounds_canaries_andpagination_pass']
    assert stored['all_stored_planes_equal_directly_viewed_compiled_planes']
    assert (stored['complete_stored_pages'], stored['fresh_parity_dependent_pages'],
            stored['exact_compiled_pages_reused'], stored['fresh_relocated_native_relative_cases']) == (444, 156, 288, 630)
    assert lookup['stored_sha256'] == digest(STORED) and lookup['all442_ordinary_and_style_bodies_checked']
    assert lookup['all_new_effective_bodies_byte_exact_before_original_macro_expansion']
    p, s, m = map(load, (NEXT_PACKET, NEXT_STYLES, NEXT_MENUS))
    assert p['records'] == 242 and len(s['records']) == 298 and len(m['records']) == 16
    assert p['clean_only_no_prior_English_ornew_editorial_credit']
    assert s['source_packet_sha256'] == m['source_packet_sha256'] == digest(NEXT_PACKET)

    summary = (
        'Rafael B301–B320 has 453 contextual decisions, with 397 revisions and 56 justified retentions. '
        'All 444 final pages and 11 menu captions passed offline native display and visual review. '
        'All 444 stored pages and 630 relocated branch cases passed. Focused gameplay and registration remain pending. '
        'Integrated coverage is 15,739.'
    )
    doc_text = f"""# Rafael B301–B320 editorial and offline display checkpoint

{summary}

The second half restores that the mosque honors the king, that the relic search uses incense and a copy of the Arabian Nights, and that Claudio’s reaction follows a command to wait. The reading keeps the source invocation and the tale’s Ifrit. The medicine recognition now names Hua Tuo’s Tonic as shown in the registered catalogue. Claudio’s bridge cue explicitly tells Janus to cross. The previous source and current bindings, wording, and findings are preserved. {link('Contextual ledger', PROSE)}. {link('Clean and current item labels', TERMS)}.

The automatic plans use the established 216-pixel progressive and 228-pixel FE geometry. The full contact sheets and the 38 refreshed visual pages were inspected. The layout changes keep phrases such as the Indian Ocean’s Proof and the bridge directive together. All 152 style slots, five menu providers, 96 bridged menu returns, 44 caption planes, and 19 scoped speaker or role labels passed their offline checks. {link('Final native pages', FINAL)}. {link('Visual approval and sheets', VISUAL)}. {link('Menu proof bindings', MENU)}.

The rebuild owns 20 SC0 blocks, with 720 commands and 126 relative sites. It preserves other files and components and reverses to the exact preceding ROM. All 343 native archive loads or cache hits and 686 checked parent-mode cases passed. Fresh parity checks covered 156 stored pages, 288 reused exact compiled planes, and all 442 bodies passed original lookup. Run the disclosed initialized emulator sequence for all five menus, the page turns, the fixed glyphs and representative names. Verify the exact clean-input patch through the registered release workflow. {link('Rebuild', REBUILT)}. {link('Loaders', LOADERS)}. {link('Stored page verification', STORED)}. {link('Original lookup', LOOKUP)}. {link('Emulator sequence selection', SELECTION)}.

The next clean-only intake covers B321–B342, with 242 ordinary speeches, 298 alternate voices, and 16 captions. The source also has one label-free command retained separately. The wider storyline and shared prose review, graphics separation, and older-record audit remain in scope. {link('Next clean packet', NEXT_PACKET)}.
"""
    evidence = {str(path): digest(path) for path in paths}
    checkpoint(
        mutation=ROOT/'B301_B320_display_checkpoint_v1', batch_key=NEXT,
        batch_updates=dict(new_credit=0, remaining_current_comparisons=0, contextual_compared_records=453,
            proposed_revisions=397, justified_retentions=56, formatting_pending=True,
            native_offline_pages=444, native_offline_typed_captions=11, native_offline_style_slots=152,
            all_final_dialogue_pages_directly_viewed=True, contextual_review=str(PROSE),
            contextual_review_sha256=digest(PROSE), native_page_receipt=str(FINAL),
            native_page_receipt_sha256=digest(FINAL), stored_checks_pending=False,
            stored_pages=444, stored_lookup_records=442, native_relative_cases=630,
            representative_gameplay_pending=True, registered_integration_pending=True,
            evidence={**ledger[NEXT]['evidence'], **evidence}),
        additional_updates={'editorial_execution_priority_20261104': dict(new_credit=0,
            current_batch='Rafael B301–B320 focused emulator and registered integration.',
            next_action='Verify the selected emulator sequence, then register the batch.',
            registered_build_live=False, guide_photos=False)},
        summary=summary, document='docs/editorial_Rafael_B301_B320_display_20261106.md',
        document_text=doc_text, completed=15739, protected={
            'translations/release_stack.json': release['registry_sha256'],
            release['canonical_base']: release['canonical_sha256'],
            release['candidate']: release['candidate_sha256'], release['patch']: release['patch_sha256'],
            package['zip']: package['zip_sha256'],
        },
    )
    print(summary)


if __name__ == '__main__':
    main()
