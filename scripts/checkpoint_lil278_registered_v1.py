"""Record the verified Lil278 cumulative release and remaining source scope."""

import gzip
from pathlib import Path

from scripts.audit_story_glyph_consistency import load, save
from scripts.build_registered_lil278_v1 import OUT, RELEASE
from scripts.checkpoint_lil278_prose_and_promotion_v1 import ARCHIVES, BATCH, PROMOTED, REGISTRY
from scripts.checkpoint_lil278_research_v1 import ARCHIVE as RESEARCH_ARCHIVE
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest
from scripts.save_editorial_progress_checkpoint_v10 import checkpoint


ARCHIVE = ARCHIVES / 'Lil278_registered_20261110_v1'
PACKAGE = Path('releases/all_routes_editorial_20261110_lil278_candidate')
CENSUS = Path('work/story_source_coverage_20261110_SC2_v6/coverage.json')
DOCUMENT = Path('docs/editorial_Lil278_registered_20261110.md')
FINAL = Path('translations/lil278_B299_B311_integrated_final_review_v1.json')
TEST = Path('out/promotion_ready_20261110_lil278_v1/Translation_DS_All_Routes_Lil278_20261110_candidate.nds')


def archive_receipts():
    prior = RESEARCH_ARCHIVE / 'archive_manifest.json'
    files = [path for path in OUT.rglob('*') if path.is_file() and path.suffix in {'.json', '.txt'}]
    files += [
        CENSUS, CENSUS.with_name('residual_clean_source_packet.json'),
        BATCH / 'registered_preparation_v1/qualification.json',
        BATCH / 'registered_preparation_v1/sealed_research_inputs.json',
        BATCH / 'registered_semantic_checks_v1/qualification.json',
        Path('work/lil278_repository_qa_v1_pytest.xml'),
    ]
    artifacts = {}
    for path in sorted(files):
        raw = path.read_bytes()
        packed = ARCHIVE / path.relative_to('work')
        packed = packed.with_suffix(packed.suffix + '.gz')
        packed.parent.mkdir(parents=True, exist_ok=True)
        packed.write_bytes(gzip.compress(raw, compresslevel=9, mtime=0))
        assert gzip.decompress(packed.read_bytes()) == raw
        artifacts[str(path)] = dict(archive=str(packed), source_sha256=digest(path), archive_sha256=digest(packed))
    archive = ARCHIVE / 'archive_manifest.json'
    save(archive, dict(
        artifacts=artifacts, prior_research_archive=str(prior), prior_research_archive_sha256=digest(prior),
        all_selected_artifacts_lossless=True, raw_images_RAM_andROMs_preserved_locally=True,
        registered_andcredited_once=True, new_credit=0, full_goal_complete=False,
    ))
    return archive


def main():
    assert not ARCHIVE.exists() and not DOCUMENT.exists()
    release, census, final = map(load, (RELEASE, CENSUS, FINAL))
    complete = load(OUT / 'completion_checkpoint.json')
    assert complete['new_credit'] == 278
    assert complete['counts'] == dict(completed=25383, revised=15052, retained=10331)
    assert (release['registered_manifest_entries'], release['accepted_layers'],
            release['passing_release_checks']) == (729, 114, 64)
    assert len(census['records']) == 6720 and len(census['missing']) == 515
    assert census['new_exact_bindings'] == len(final['records']) == 278
    assert all(all(row['review'].values()) for row in final['records'])
    assert not census['inventory_failures'] and not census['legacy_source_bindings_not_exact']
    next_block = min(row['block'] for row in census['missing'])
    assert next_block == 312
    ledger = load('translations/editorial_review_current_v1.json')
    assert ledger['Lil_SC2_B299_B311_clean_20261110']['new_credit'] == 278
    assert ledger['current_integrated_candidate']['sha256'] == release['candidate_sha256'] == digest(TEST)
    checksums = load(PACKAGE / 'checksums.json')
    assert {p.relative_to(PACKAGE).as_posix() for p in PACKAGE.rglob('*') if p.is_file()
            and p.name != 'checksums.json'} == set(checksums)
    assert all(digest(PACKAGE / relative) == checksum for relative, checksum in checksums.items())

    protocol = Path('docs/build_continuity_protocol.md')
    before = protocol.read_bytes()
    assert before.startswith(b'Lil361 B283')
    backup = OUT / 'continuity_before.txt'
    assert not backup.exists()
    backup.write_bytes(before)
    lead = (
        'Lil278 B299–B311 is registered over Lil361 with 729 entries, 114 accepted layers and 64 checks. '
        'Use `scripts/build_registered_lil278_v1.py` for staging and registration and '
        '`dk4tool/patch/lil278_release_v1.py` for the pure transaction. Preserve all 728 predecessor entries, '
        'the Market fix and both pointers, six-section ARM9, ASCII right bounds, source25v2 and B164R99. '
        'The exact clean-input patch, own startup and 24 protected getters pass. '
        'The next native Lil source group begins at B312. [Registered checkpoint](' + DOCUMENT.name + ')\n\n'
    )
    staged = protocol.with_name(protocol.name + '.Lil278.pending')
    assert not staged.exists()
    staged.write_bytes(lead.encode('utf-8') + before)
    assert protocol.read_bytes() == before
    staged.replace(protocol)
    assert protocol.read_bytes() == lead.encode('utf-8') + before
    save(OUT / 'continuity_update.json', dict(path=str(protocol), before_sha256=digest(backup),
                                             after_sha256=digest(protocol), prior_contents_preserved_as_exact_suffix=True))
    archive = archive_receipts()

    summary = ('Lil B299–B311 is registered and credited once. The cumulative Lil278 candidate adds 278 reviews, '
               'including 170 revisions and 108 retentions. The clean-input patch reconstructs it exactly. '
               'Own startup, 24 protected getters, 64 release checks and 27 repository tests passed. '
               'The ledger credits 25,383 reviews, with 515 native Lil positions remaining.')
    notes = f"""# Lil278 registered cumulative candidate

{summary}

The [testing ROM](../{TEST.as_posix()}) and adjacent manifest match the registered image, SHA-256 `{release['candidate_sha256']}`. The published patch has SHA-256 `{release['patch_sha256']}`. Both clean-input reconstructions matched byte for byte. This successor preserves all 728 predecessor entries and all 114 accepted layers. Only `/data/SC2.DK4` changes. The Market fix, both Market pointers, ASCII right bounds, approved name fields and prior releases are preserved. Main V4701 awaits cold-boot acceptance. [Patch and test notes](../{PACKAGE.as_posix()}/README.md)

The 13 reviewed groups include 133 ordinary speeches, 139 personality alternatives and six captions. The 25 layout refinements preserve the reviewed prose. All 280 pages and 11 scoped name strings were reviewed offline. The initialized Lil sample displayed 52 bodies, all six captions, three page turns and all eight system-alert returns. It reached resupply and the steering tutorial. The other 220 bodies have offline coverage. Original optional activation, rewards, full-route play and hardware remain unvisited. [Stored and gameplay evidence](editorial_Lil278_stored_gameplay_20261110.md)

The cumulative image separately passed its own 31,000-frame Maria startup with the existing isolated system unlock. Six frames were visually checked. Both getters for all 12 protected actors passed. The first sandboxed emulator invocation stopped at Windows handle error 0xc0000008. The original attempt is preserved locally, and the successful retry used the same staged ROM and frozen input schedule.

The Lil source census now covers 6,205 of 6,720 positions. Continue from the remaining complete source group at B312, preserving any earlier credited context. The full editorial scope remains active, including other story dialogue, shared scenes, random events, player-facing prose and the broader name review. Deferred artwork and the older-record technical re-audit remain separate. [Integrated ledger](../{FINAL.as_posix()}) · [Lossless release evidence](../{archive.as_posix()})
"""
    protected = {
        str(REGISTRY): release['registry_sha256'], str(PROMOTED): digest(PROMOTED),
        release['candidate']: release['candidate_sha256'], str(TEST): release['candidate_sha256'],
        release['manifest']: release['manifest_sha256'], release['patch']: release['patch_sha256'],
        release['canonical_base']: release['canonical_sha256'], 'work/clean.nds': release['clean_input_sha256'],
        str(FINAL): digest(FINAL), str(protocol): digest(protocol),
    }
    evidence = {str(path): digest(path) for path in (RELEASE, CENSUS, archive, FINAL)}
    checkpoint(
        mutation=OUT / 'registered_checkpoint_v1', batch_key='editorial_execution_priority_20261104',
        batch_updates=dict(
            new_credit=0, current_batch='Lil B299–B311 registered and credited once',
            current_batch_not_yet_integrated=False, current_batch_registered_andcredited_once=True,
            all_current_batch_fifth_gates_pending=False, current_batch_evidence=evidence,
            previous_goal_turn_classification='progress', current_goal_turn_classification='progress',
            no_batch_worker_live=True, guide_photos=False,
            next_action='Continue native Lil source review at B312 and preserve full remaining editorial scope.'),
        summary=summary, document=DOCUMENT, document_text=notes, completed=25383, protected=protected,
    )
    print('Verified the Lil278 patch package and archived the registered release and source census.')


if __name__ == '__main__':
    main()
