"""Verify the Lil254 handoff package and record the cumulative checkpoint."""

import gzip
from pathlib import Path

from scripts.audit_story_glyph_consistency import load, save
from scripts.build_registered_lil254_v1 import OUT, RELEASE, REGISTRY, ROOT
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest
from scripts.save_editorial_progress_checkpoint_v10 import checkpoint


ARCHIVE = Path('translations/editorial_checkpoints/Lil254_registered_20261110_v1')
RESEARCH = Path('translations/editorial_checkpoints/Lil254_research_20261110_v1/archive_manifest.json')
PACKAGE = Path('releases/all_routes_editorial_20261110_lil254_candidate')
CENSUS = Path('work/story_source_coverage_20261110_SC2_v7/coverage.json')
DOCUMENT = Path('docs/editorial_Lil254_registered_20261110.md')
FINAL = Path('translations/lil254_B312_B319_integrated_final_review_v1.json')


def main():
    assert not ARCHIVE.exists() and not DOCUMENT.exists()
    release, census, final = map(load, (RELEASE, CENSUS, FINAL))
    complete = load(OUT / 'completion_checkpoint.json')
    assert complete['new_credit'] == census['new_exact_bindings'] == len(final['records']) == 254
    assert complete['counts'] == dict(completed=25637, revised=15203, retained=10434)
    assert (release['registered_manifest_entries'], release['accepted_layers'], release['passing_release_checks']) == (730, 114, 65)
    assert all(all(row['review'].values()) for row in final['records'])
    assert len(census['records']) == 6720 and len(census['missing']) == 261
    assert min(row['block'] for row in census['missing']) == 323
    assert not census['inventory_failures'] and not census['legacy_source_bindings_not_exact']
    checksums = load(PACKAGE / 'checksums.json')
    assert set(checksums) == {p.relative_to(PACKAGE).as_posix() for p in PACKAGE.rglob('*')
                             if p.is_file() and p.name != 'checksums.json'}
    assert all(digest(PACKAGE / name) == checksum for name, checksum in checksums.items())
    receipt = load(PACKAGE / 'verification/promotion_reconstruction.json')
    test = Path(receipt['candidate'])
    patch = PACKAGE / 'translation.xdelta'
    assert digest(test) == receipt['candidate_sha256'] == release['candidate_sha256']
    assert digest(patch) == receipt['patch_sha256'] == release['patch_sha256']
    assert digest(test.with_suffix('.manifest.json')) == release['manifest_sha256']
    assert receipt['exact_registered_candidate_reconstructed_from_clean_input'] and not receipt['main_promoted']

    protocol = Path('docs/build_continuity_protocol.md')
    before = protocol.read_bytes()
    assert before.startswith(b'Lil278 B299')
    backup = OUT / 'continuity_before.txt'
    assert not backup.exists()
    backup.write_bytes(before)
    lead = ('Lil254 B312–B319 is registered over Lil278 with 730 entries, 114 accepted layers and 65 checks. '
            'Use `scripts/build_registered_lil254_v1.py` and `dk4tool/patch/lil254_release_v1.py`. '
            'Preserve the Market fix and both pointers, six-section ARM9, ASCII right bounds, source25v2 and B164R99. '
            'The exact clean-input patch, own startup and 24 protected getters pass. '
            'The next remaining native Lil group starts at B323. [Registered checkpoint](' + DOCUMENT.name + ')\n\n')
    pending = protocol.with_name(protocol.name + '.Lil254.pending')
    assert not pending.exists()
    pending.write_bytes(lead.encode('utf-8') + before)
    assert protocol.read_bytes() == before
    pending.replace(protocol)

    paths = [p for p in OUT.rglob('*') if p.is_file() and p.suffix in {'.json', '.txt'}]
    paths += [CENSUS, CENSUS.with_name('residual_clean_source_packet.json'),
              ROOT / 'registered_preparation_v1/qualification.json',
              ROOT / 'registered_preparation_v1/sealed_research_inputs.json',
              ROOT / 'registered_semantic_checks_v1/qualification.json',
              Path('work/lil254_repository_qa_v1_pytest.xml')]
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
    save(archive, dict(artifacts=artifacts, prior_research_archive=RESEARCH.as_posix(),
        prior_research_archive_sha256=digest(RESEARCH), all_selected_artifacts_lossless=True,
        registered_andcredited_once=True, new_credit=0, full_goal_complete=False))

    summary = ('Lil B312–B319 is registered and credited once. The cumulative Lil254 candidate adds 254 reviews, '
               'including 151 revisions and 103 retentions. The clean-input patch reconstructs it exactly. '
               'Own startup, 24 protected getters, 65 release checks and 27 repository tests passed. '
               'The ledger credits 25,637 reviews, with 261 native Lil positions remaining.')
    notes = f"""# Lil254 registered cumulative candidate

{summary}

The [testing ROM](../{test.as_posix()}) and adjacent manifest match the registered image, SHA-256 `{release['candidate_sha256']}`. The [clean-input patch](../{patch.as_posix()}) has SHA-256 `{release['patch_sha256']}`. The successor preserves the 729-entry predecessor and all 114 accepted layers. Changes are confined to eight `/data/SC2.DK4` blocks. The Market fix, both Market pointers, ASCII right bounds and earlier name fields are preserved. Main V4701 awaits user cold-boot acceptance. [Package notes](../{PACKAGE.as_posix()}/README.md)

All 251 pages, eight captions and 13 name strings passed offline review. The focused initialized Lil sample displayed 53 bodies and 58 pages, including the two corrected displays and both selector-00 nameplates. The other 193 bodies have offline and stored coverage. Original optional activation, branch outcomes, full-route play and hardware remain unvisited. The cumulative candidate separately passed its own 31,000-frame Maria startup with the existing isolated system unlock, six visually checked captures and both getters for all 12 protected actors. [Gameplay and editorial evidence](editorial_Lil254_gameplay_20261110.md)

The exact Lil census covers 6,459 of 6,720 native positions. Continue at B323 with the remaining complete exchanges. The wider story, shared, random, player-facing and name scope remains active. Deferred artwork and the later older-record technical re-audit are separate. [Integrated ledger](../{FINAL.as_posix()}) · [Lossless evidence](../{archive.as_posix()})
"""
    evidence = {str(p): digest(p) for p in (RELEASE, CENSUS, FINAL, archive)}
    checkpoint(mutation=OUT / 'registered_checkpoint_v1', batch_key='editorial_execution_priority_20261104',
        batch_updates=dict(new_credit=0, current_batch='Lil B312–B319 registered and credited once',
            current_batch_not_yet_integrated=False, current_batch_registered_andcredited_once=True,
            all_current_batch_fifth_gates_pending=False, current_batch_evidence=evidence,
            previous_goal_turn_classification='progress', current_goal_turn_classification='progress',
            no_batch_worker_live=True, guide_photos=False,
            next_action='Continue the remaining 261 Lil positions from complete group B323 and preserve the wider editorial scope.'),
        summary=summary, document=DOCUMENT, document_text=notes, completed=25637,
        protected={str(REGISTRY): release['registry_sha256'],
            'translations/promoted_build.json': digest('translations/promoted_build.json'),
            str(test): release['candidate_sha256'], str(patch): release['patch_sha256'],
            release['manifest']: release['manifest_sha256'], release['candidate']: release['candidate_sha256']})
    print('Verified and archived the Lil254 cumulative package and exact remaining source census.')


if __name__ == '__main__':
    main()
