"""Record the registered Lil261 package, display evidence and completed source census."""

import gzip
from pathlib import Path

from scripts.audit_story_glyph_consistency import load, save
from scripts.build_registered_lil261_v1 import OUT, RELEASE, REGISTRY, ROOT
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest
from scripts.save_editorial_progress_checkpoint_v10 import checkpoint


ARCHIVE = Path('translations/editorial_checkpoints/Lil261_registered_20261110_v1')
PRIOR = Path('translations/editorial_checkpoints/Lil261_stored_20261110_v1/archive_manifest.json')
PACKAGE = Path('releases/all_routes_editorial_20261110_lil261_candidate')
CENSUS = Path('work/story_source_coverage_20261110_SC2_v8/coverage.json')
DOCUMENT = Path('docs/editorial_Lil261_registered_20261110.md')
FINAL = Path('translations/lil261_B323_B335_integrated_final_review_v1.json')


def main():
    assert not ARCHIVE.exists() and not DOCUMENT.exists()
    release, census, final = map(load, (RELEASE, CENSUS, FINAL))
    complete = load(OUT / 'completion_checkpoint.json')
    assert complete['new_credit'] == census['new_exact_bindings'] == len(final['records']) == 261
    assert complete['counts'] == dict(completed=25898, revised=15401, retained=10497)
    assert (release['registered_manifest_entries'], release['accepted_layers'], release['passing_release_checks']) == (731, 114, 66)
    assert all(all(row['review'].values()) for row in final['records'])
    assert len(census['records']) == 6720 and all(r['covered'] for r in census['records'])
    assert not any(census[key] for key in ['missing', 'inventory_failures', 'legacy_source_bindings_not_exact'])
    checksums = load(PACKAGE / 'checksums.json')
    assert set(checksums) == {p.relative_to(PACKAGE).as_posix() for p in PACKAGE.rglob('*')
                             if p.is_file() and p.name != 'checksums.json'}
    assert all(digest(PACKAGE / name) == checksum for name, checksum in checksums.items())
    package_receipt = load(PACKAGE / 'verification/promotion_reconstruction.json')
    test = Path(package_receipt['candidate'])
    patch = PACKAGE / 'translation.xdelta'
    assert digest(test) == package_receipt['candidate_sha256'] == release['candidate_sha256']
    assert digest(patch) == package_receipt['patch_sha256'] == release['patch_sha256']
    assert digest(test.with_suffix('.manifest.json')) == release['manifest_sha256']
    assert package_receipt['exact_registered_candidate_reconstructed_from_clean_input'] and not package_receipt['main_promoted']
    actual = load(ROOT / 'gameplay_review_v1.json')
    assert actual['all_actual_body_menu_andtransition_sheets_directly_viewed']
    assert actual['all_thirteen_FE_returns_observed'] and actual['all_three_menus_and_following_A_returns_observed']

    paths = [
        CENSUS, CENSUS.with_name('residual_clean_source_packet.json'),
        OUT / 'exact_integrated_record_bindings.json', OUT / 'completion_mutation_plan.json',
        OUT / 'own_startup_run_v1/run_plan.json',
        ROOT / 'actual_run0_v1/terminal.json', ROOT / 'actual_sheets0_v1/sheets.json',
        ROOT / 'display_pixels0_v1/focused_actual_pixels.json',
        ROOT / 'actual_menus_returns0_v1/menu_actual_pixels.json', ROOT / 'transition_review_v1/receipt.json',
        ROOT / 'research_completion_v1/research_completion.json',
        ROOT / 'research_completion_v1/source255_release_plans.json',
        ROOT / 'registered_preparation_v1/qualification.json', ROOT / 'registered_preparation_v1/sealed_research_inputs.json',
    ]
    artifacts = {}
    for path in sorted(paths):
        raw = path.read_bytes()
        packed = ARCHIVE / path.relative_to('work')
        packed = packed.with_suffix(packed.suffix + '.gz')
        packed.parent.mkdir(parents=True, exist_ok=True)
        packed.write_bytes(gzip.compress(raw, compresslevel=9, mtime=0))
        assert gzip.decompress(packed.read_bytes()) == raw
        artifacts[path.as_posix()] = dict(archive=packed.as_posix(), source_sha256=digest(path), archive_sha256=digest(packed))
    archive = ARCHIVE / 'archive_manifest.json'
    save(archive, dict(artifacts=artifacts, prior_stored_archive=PRIOR.as_posix(),
        prior_stored_archive_sha256=digest(PRIOR), packaged_verification=PACKAGE.as_posix(),
        packaged_checksums_sha256=digest(PACKAGE / 'checksums.json'),
        all_selected_artifacts_lossless=True, registered_andcredited_once=True, new_credit=0, full_goal_complete=False))

    summary = ('Lil B323–B335 is registered and credited once. Lil261 adds 261 contextual reviews, '
               'including 198 revisions and 63 retentions. The clean-input patch reconstructs it exactly. '
               'The exact native Lil census covers 6,720 of 6,720 positions. The ledger credits 25,898 reviews.')
    notes = f"""# Lil261 registered cumulative candidate

{summary}

The [testing ROM](../{test.as_posix()}) and adjacent manifest match the registered candidate with SHA-256 `{release['candidate_sha256']}`. The [clean-input patch](../{patch.as_posix()}) has SHA-256 `{release['patch_sha256']}`. The successor preserves the 730-entry predecessor and 114 accepted layers, including Rafael's tutorials, the Market Trade-screen fix and the ASCII right-bound correction. All new bytes belong to 13 SC2 blocks. Main V4701 awaits user cold-boot acceptance. [Package notes](../{PACKAGE.as_posix()}/README.md)

Offline and stored checks cover all 258 dialogue pages, six captions and 12 strings for nine scoped name reviews. Thirty revised layouts improve phrase continuity and pagination. The initialized Lil emulator sample displayed 58 bodies and 61 pages, exercised three page turns, 13 system-alert returns and all three menu returns, and continued into the original resupply and steering tutorial. The other 197 bodies have offline and stored coverage. Original optional activation, branch outcomes, full-route play and hardware remain unvisited.

The exact candidate separately passed a 31,000-frame Maria startup with the existing isolated system unlock, six visually checked captures, both getters for 12 protected actors, 66 release checks and 27 repository tests. The census covers dialogue, captions and personality variants. Wider story, shared town and random exchanges, other player-facing prose and name work remain in scope. Deferred artwork and the older-record technical re-audit stay separate. [Integrated review](../{FINAL.as_posix()}) · [Lossless evidence](../{archive.as_posix()})
"""
    protocol = Path('docs/build_continuity_protocol.md')
    before = protocol.read_bytes()
    assert before.startswith(b'Lil254 B312')
    (OUT / 'continuity_before.txt').write_bytes(before)
    lead = ('Lil261 B323–B335 is registered over Lil254 with 731 entries, 114 accepted layers and 66 checks. '
            'Use `scripts/build_registered_lil261_v1.py` and `dk4tool/patch/lil261_release_v1.py`. '
            'Preserve the Market fix and both pointers, six-section ARM9, ASCII right bounds, source25v2 and B164R99. '
            'The exact clean-input patch, own startup and 24 protected getters pass. '
            'The native Lil story census is complete. [Registered checkpoint](' + DOCUMENT.name + ')\n\n')
    staged = protocol.with_name(protocol.name + '.Lil261.pending')
    assert not staged.exists()
    staged.write_bytes(lead.encode('utf-8') + before)
    assert protocol.read_bytes() == before
    staged.replace(protocol)

    evidence = {str(p): digest(p) for p in (RELEASE, CENSUS, FINAL, archive)}
    checkpoint(mutation=OUT / 'registered_checkpoint_v1', batch_key='editorial_execution_priority_20261104',
        batch_updates=dict(new_credit=0, current_batch='Lil B323–B335 registered and credited once',
            current_batch_not_yet_integrated=False, current_batch_registered_andcredited_once=True,
            all_current_batch_fifth_gates_pending=False, current_batch_evidence=evidence,
            previous_goal_turn_classification='progress', current_goal_turn_classification='progress',
            no_batch_worker_live=True, guide_photos=False,
            next_action='Continue the outstanding storyline, shared town, random, name and other player-facing reviews.'),
        summary=summary, document=DOCUMENT, document_text=notes, completed=25898,
        protected={str(REGISTRY): release['registry_sha256'],
            'translations/promoted_build.json': digest('translations/promoted_build.json'),
            str(test): release['candidate_sha256'], str(patch): release['patch_sha256'],
            release['manifest']: release['manifest_sha256'], release['candidate']: release['candidate_sha256']})
    print('Verified and archived the Lil261 package and complete native Lil census.')


if __name__ == '__main__':
    main()
