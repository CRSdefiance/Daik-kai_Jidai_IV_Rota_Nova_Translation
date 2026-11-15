"""Preserve pending Lil361 storage/gameplay evidence and the registered testing handoff."""
import ast
import gzip
import xml.etree.ElementTree as ET
from pathlib import Path

from scripts.audit_story_glyph_consistency import load, save
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest
from scripts.save_editorial_progress_checkpoint_v10 import checkpoint


ROOT = Path('work/Lil361_B283_B298_clean_20261110')
ARCHIVE = Path('translations/editorial_checkpoints/Lil361_stored_actual_partial_20261110_v1')
PACKAGE = Path('releases/all_routes_promotion_20261110_v5')
TEST = Path('out/promotion_ready_20261110_v5')


def main():
    assert not ARCHIVE.exists()
    release_path = Path('work/lil269_B243_B282_release_v1/registered_release_verification.json')
    release = load(release_path)
    receipt_path = PACKAGE / 'verification/fresh_promotion_reconstruction.json'
    receipt = load(receipt_path)
    assert receipt['exact_registered_candidate_reconstructed_from_clean_input']
    assert receipt['byte_identical_to_registered_candidate'] and not receipt['new_internal_ROM_changes']
    assert (receipt['release_entries'], receipt['accepted_layers'], receipt['passing_release_checks'],
            receipt['fresh_repository_tests']) == (727, 114, 62, 27)
    assert receipt['pending_Lil361_not_integrated'] and not receipt['main_promoted']
    for name, h in load(PACKAGE / 'checksums.json').items():
        assert digest(PACKAGE / name) == h, name
    assert digest(receipt['candidate']) == release['candidate_sha256']

    reconstruction_path = ROOT / 'reconstruction_v1/reconstruction.json'
    reconstruction = load(reconstruction_path)
    assert reconstruction['changed_blocks'] == list(range(283, 299))
    assert reconstruction['source_editorial_objects'] == 361
    assert reconstruction['full_clean_current_block_archive_andserialized_NDS_inverses_exact']
    assert reconstruction['all_other_files_components_exact']
    assert digest(reconstruction['research_ROM']) == reconstruction['research_ROM_sha256']
    qualified = load(ROOT / 'credited_context_rebuild_qualification_v1.json')
    assert qualified['actual_clean_current_andtarget_inverses_pass'] and qualified['positive_B294_target_byte_exact']
    assert (qualified['preserved_context_objects'], qualified['new_owned_speeches']) == (1, 15)
    assert len(qualified['rejected_cases']) == 5
    stored = load(ROOT / 'stored_v1/stored_native_verification.json')
    assert (stored['complete_stored_pages'], stored['fresh_parity_dependent_pages'],
            stored['exact_compiled_pages_reused'], stored['fresh_relocated_native_relative_cases']) == (353, 91, 262, 875)
    assert stored['all_stored_planes_equal_directly_viewed_compiled_planes']
    assert stored['every_byte_consumed_andall_first_internal_final_glyphs_bounds_canaries_andpagination_pass']
    catalogue = load(ROOT / 'stored_catalogue_all_v1/all_stored_effective_body_bindings.json')
    assert catalogue['body_count'] == 352
    assert catalogue['all_new_effective_bodies_byte_exact_before_original_macro_expansion']
    loaders = load(ROOT / 'loaders_v1/verification.json')
    assert (loaders['whole_archive_loads_andcache_hits'], loaders['parent_cases']) == (336, 672)
    assert loaders['all_loaded_payloads_cache_metadata_neighbors_andparent_first_reads_exact']
    selection = load(ROOT / 'display_selection_v1.json')
    assert (selection['distinct_body_records'], selection['personality_tables'], selection['menus']) == (199, 24, 4)
    seen, pages, frames, bindings = set(), set(), 0, {}
    for i, expected in enumerate([(42, 42, 15761), (84, 84, 25601), (73, 74, 23201)]):
        terminal_path = ROOT / f'actual_run{i}_v1/terminal.json'
        pixels_path = ROOT / f'display_pixels{i}_v1/focused_actual_pixels.json'
        terminal, pixels = load(terminal_path), load(pixels_path)
        assert terminal['terminal'] is True and terminal['frames'] == expected[2]
        assert digest(terminal['report']) == terminal['report_sha256']
        assert digest(terminal['observer']) == terminal['observer_sha256']
        assert (pixels['selected_utterances'], pixels['selected_pages'], pixels['frames']) == expected
        assert pixels['all_selected_pages_observed_in_exact_fixture_order']
        assert pixels['all_complete_native_body_andheader_planes_andblank_guards_match']
        assert pixels['direct_visual_review_pending']
        assert not any(pixels[k] for k in ['natural_activation', 'original_location', 'earned_chronology', 'full_route', 'hardware'])
        seen.update(row['id'] for row in pixels['body_pages'])
        pages.update((row['id'], row['page']) for row in pixels['body_pages'])
        frames += terminal['frames']
        bindings.update({str(p): digest(p) for p in [terminal_path, pixels_path]})
    assert (len(seen), len(pages), frames) == (199, 200, 64563)
    manuscript = Path('translations/lil_B283_B298_contextual_review_v1.json')
    names = Path('translations/lil_B283_B298_scoped_names_v1.json')
    for row in load(manuscript)['records'] + load(names)['records']:
        assert row['review'] == dict(source=True, context=True, localization=True, naturalness=True, formatting=False)
    status_path = ROOT / 'stored_actual_partial_checkpoint_v1.json'
    save(status_path, dict(source_objects=361, revisions=178, justified_retentions=183,
        stored_pages=353, native_lookup_bodies=352, relative_cases=875, loads=336, parent_handoffs=672,
        initialized_runs=3, initialized_frames=frames, distinct_body_records_pixel_bound=199,
        unique_body_pages_pixel_bound=200, current_personality_tables_selected=24,
        other153_physical_personality_alternatives_offline_only=True,
        actual_direct_visual_review_pending=True, actual_menu_andtransition_approval_pending=True,
        all_fifth_gates_pending=True, registered_integration_pending=True,
        pending_batch_excluded_from_testing_ROM=True, preserved_B294_credited_context_not_recredited=True,
        no_original_optional_event_chronology_rewards_stats_orhardware_claim=True,
        no_batch_worker_live=True, new_credit=0, full_goal_complete=False, evidence=bindings))

    failed_report = Path('work/promotion_20261110_v5_pytest.xml')
    suites = list(ET.parse(failed_report).getroot().iter('testsuite'))
    assert sum(int(s.get('errors', 0)) for s in suites) == 2
    assert all(int(s.get('failures', 0)) == 0 for s in suites)
    (PACKAGE / 'verification/initial_temp_folder_setup_errors.xml').write_bytes(failed_report.read_bytes())
    save(PACKAGE / 'verification/test_environment_note.json', dict(
        initial_exit_code=1, initial_passed=25, initial_setup_errors=2,
        reason='Pytest could not create its numbered temporary directory in the sandbox user Temp path.',
        correction='Used a fresh explicit --basetemp directory inside work; no test or assertion changed.',
        retry_exit_code=0, retry_passed=27, retry_errors=0, retry_failures=0, retry_skipped=0))
    save(PACKAGE / 'checksums.json', {p.relative_to(PACKAGE).as_posix(): digest(p)
        for p in PACKAGE.rglob('*') if p.is_file() and p.name != 'checksums.json'})

    pin_path = Path('translations/rom_retention_pins.json')
    pins = load(pin_path)
    candidate = str(Path(receipt['candidate']).absolute())
    assert not any(p['path'] == candidate for p in pins)
    pins.append(dict(path=candidate, reason='User-requested cumulative testing candidate; preserve until explicit acceptance. SHA256 ' + release['candidate_sha256']))
    save(pin_path, pins)

    prior_manifest = Path('translations/editorial_checkpoints/Lil361_offline_20261110_v1/archive_manifest.json')
    prior = load(prior_manifest)['artifacts']
    ARCHIVE.mkdir(parents=True)
    artifacts, reused = {}, 0
    for p in sorted(ROOT.rglob('*')):
        if not p.is_file() or p.suffix not in ['.json', '.txt']:
            continue
        raw, h = p.read_bytes(), digest(p)
        old = prior.get(str(p))
        if old and old['source_sha256'] == h:
            assert digest(old['archive']) == old['archive_sha256']
            assert gzip.decompress(Path(old['archive']).read_bytes()) == raw
            artifacts[str(p)] = {**old, 'reused_from': str(prior_manifest)}
            reused += 1
            continue
        dest = (ARCHIVE / p.relative_to(ROOT)).with_suffix(p.suffix + '.gz')
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_bytes(gzip.compress(raw, compresslevel=9, mtime=0))
        assert gzip.decompress(dest.read_bytes()) == raw
        artifacts[str(p)] = dict(archive=str(dest), source_sha256=h, archive_sha256=digest(dest))
    producers = sorted(set(Path('scripts').glob('*lil361*.py')) | {
        Path(__file__), Path('scripts/prepare_registered_promotion_candidate_v2.py'),
        Path('scripts/analyze_lil382_display_v1.py'), Path('scripts/run_lil382_display_v1.py')})
    for p in producers:
        ast.parse(p.read_bytes(), filename=str(p))
    archive = ARCHIVE / 'archive_manifest.json'
    save(archive, dict(artifacts=artifacts, producers={str(p): digest(p) for p in producers},
        all_selected_artifacts_lossless=True, prior_archives_preserved=True,
        exact_previous_artifacts_reused=reused, raw_ROM_RAM_images_andplanes_preserved_locally=True,
        stored_checks_approved=True, gameplay_machine_pixel_bindings_pass=True,
        gameplay_visual_menu_transition_andregistered_integration_pending=True,
        new_credit=0, full_goal_complete=False))
    protected = {'translations/release_stack.json': release['registry_sha256'],
        release['candidate']: release['candidate_sha256'], release['manifest']: release['manifest_sha256'],
        release['patch']: release['patch_sha256'], release['canonical_base']: release['canonical_sha256'],
        'work/clean.nds': release['clean_input_sha256'],
        'translations/promoted_build.json': digest('translations/promoted_build.json'),
        receipt['candidate']: receipt['candidate_sha256'], receipt['manifest']: receipt['manifest_sha256'],
        str(manuscript): digest(manuscript), str(names): digest(names)}
    summary = ('Prepared v5 cumulative testing candidate from the exact registered clean-input patch: '
        '727 entries, 114 accepted layers, 62 release checks and 27 fresh tests pass; byte-identical to registered Lil269/v4. '
        'Lil361 stored reconstruction passes all353 pages,352 native lookups,875 branch cases,336 loads and672 handoffs. '
        'Three initialized emulator runs bind199 bodies/200 pages to complete body/header pixels; direct gameplay visual, '
        'menu/transition approval, fifth gates and registration remain pending. Pending361 is preserved and excluded; '
        '24,744 integrated,zero new credit. Main awaits cold-boot acceptance; full goal active,no worker live.')
    document = Path('docs/editorial_promotion_candidate_20261110_v5.md')
    text = f'''# Cumulative testing candidate and Lil361 checkpoint — November 10, 2026

{summary}

Use [Translation_DS_All_Routes_20261110_v5_candidate.nds](../{Path(receipt['candidate']).as_posix()}) with its adjacent manifest. SHA-256: `{release['candidate_sha256']}`. [Clean-input patch and release notes](../{PACKAGE.as_posix()}/README.md). This fresh reconstruction has the same internal ROM bytes as registered Lil269 and v4; it packages the latest fully registered work without importing unfinished proposals. The exact base is `{release['canonical_base']}` (`{release['canonical_sha256']}`). All114 accepted layers and727 manifest entries remain, including Rafael/tutorial work, the Market Trade-screen correction, name/glyph fixes, six-section ARM9, ASCII right bounds, source25v2 and B164R99. Build manifest and registry are preserved losslessly in the package. Main remains V4701 pending the user's cold-boot testing and explicit acceptance.

All27 selected repository tests pass with native exit0, no failures/errors/skips. The first run passed25 tests and encountered two temporary-folder setup errors; the unchanged suite passed using a new explicit workspace-local temporary directory. Both reports and the explanation are packaged. The initial output-directory attempt stopped at the existing E: junction permission boundary before creating output; the authorized elevated rerun succeeded. The registered62 release checks, candidate-owned startup, protected getters and prior gameplay remain applicable to these exact bytes. This packaging adds no new gameplay or hardware coverage. See [registered Lil269](editorial_Lil269_registered_20261110.md) for observed versus offline content. Earlier ROMs and translations are preserved, and the new ROM is explicitly pinned.

The pending Lil361 B283–B298 work remains separate. Its178 revisions,183 justified retentions,15 scoped actors, source-first seals and completed offline review are unchanged. The16 whole-group reconstruction proves actual clean/current/block/archive/serialized-NDS inverses and leaves every other ROM file/component unchanged. B294 retains its earlier credited R73 as context, using a frozen24,744-key preintegration witness; five deliberate malformed-credit/source/macro cases are rejected. Do not recredit that line.

Stored checks verify353 pages:91 fresh parity-dependent pages and262 exact compiled-plane reuses, all875 relocated native relative cases, complete leading/internal/trailing glyphs, consumption, canaries, bounds and pagination. All352 full-buffer native catalogue lookups pass. All336 whole SC2 loads/cache hits and672 parent handoffs pass. These are offline checks, not natural event activation.

Three ordinary-input initialized B22-host emulator runs finish64,563 planned frames. Machine analysis observes199 unique bodies/200 pages in exact fixture order, with complete body/header planes and blank guards matching native expectations. All175 new ordinary bodies and24 current personality-table selections are included; the153 other physical personality alternatives remain offline-only. Four menus were included in the fixtures, but actual menu/cursor/return approval has not been performed. All actual body-sheet visual review, menu checks, FE/page/host-exit transition review and final aggregation remain pending. Do not infer original optional events, geography, chronology, quest outcomes, rewards, stats, free sailing, full-route or hardware coverage. All fifth gates remain false and no pending text is shipped or credited.

[Lossless stored/actual partial archive](../{archive.as_posix()}) preserves all JSON/TXT receipts and exact earlier archive reuses. Raw research ROMs, RAM, captures and planes remain local. Resume from `work/Lil361_B283_B298_clean_20261110`: all three `actual_runN_v1/terminal.json` and `display_pixelsN_v1/focused_actual_pixels.json` exist and pass machine binding. Finish direct visual, menu and transition approval without rerunning these completed captures, then finalize the five gates and registered cumulative successor with its own startup, protected getters and exact clean-input patch. Do not hand off `reviewed_RESEARCH_ONLY.nds` or the QA-host ROMs.

Integrated credit stays24,744 (14,704 revisions/10,040 retentions). Native Lil still has1,154 remaining positions, including this361 batch. The full unfinished contextual storyline/shared/shop/town/random/player-facing/name objective remains active. Guide-photo collection stays discontinued. Deferred graphics artwork and the later older-record technical re-audit remain separate.
'''
    evidence_paths = [receipt_path, archive, status_path, reconstruction_path,
        ROOT / 'stored_v1/stored_native_verification.json',
        ROOT / 'stored_catalogue_all_v1/all_stored_effective_body_bindings.json',
        ROOT / 'loaders_v1/verification.json']
    evidence = {str(p): digest(p) for p in evidence_paths}
    checkpoint(mutation=ROOT / 'promotion_v5_checkpoint_v1', batch_key='editorial_execution_priority_20261104',
        batch_updates=dict(new_credit=0, current_batch='Lil361 stored and actual pixel bindings pass; gameplay approval and registration pending.',
            current_batch_not_yet_integrated=True, current_batch_registered_andcredited_once=False,
            all_current_batch_fifth_gates_pending=True, current_batch_evidence=evidence,
            no_batch_worker_live=True, guide_photos=False,
            next_action='Reuse completed storage and all three actual captures; finish actual visual/menu/transition approval and register Lil361.'),
        additional_updates={'Lil_SC2_B283_B298_clean_20261110': dict(new_credit=0,
            stored_checks_pending=False, stored_pages=353, native_lookup_bodies=352, relative_cases=875,
            initialized_actual_runs=3, initialized_actual_frames=64563,
            machine_bound_actual_bodies=199, machine_bound_actual_pages=200,
            actual_direct_visual_review_pending=True, actual_menu_transition_approval_pending=True,
            gameplay_pending=True, registered_integration_pending=True, all_fifth_gates_pending=True,
            no_batch_worker_live=True, evidence=evidence)},
        summary=summary, document=document, document_text=text, completed=24744, protected=protected)
    for p, item in artifacts.items():
        assert digest(p) == item['source_sha256']
    for name, h in load(PACKAGE / 'checksums.json').items():
        assert digest(PACKAGE / name) == h
    print(dict(lossless_artifacts=len(artifacts), exact_prior_reuses=reused,
        testing_candidate=receipt['candidate'], pending_records_excluded=361, new_credit=0))


if __name__ == '__main__':
    main()
