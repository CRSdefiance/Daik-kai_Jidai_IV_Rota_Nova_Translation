"""Archive the completed Lil278 research and keep cumulative credit pending."""

import ast
import gzip
from pathlib import Path

from scripts.audit_story_glyph_consistency import load, save
from scripts.checkpoint_lil278_offline_v1 import ARCHIVE as PRIOR_ARCHIVE
from scripts.checkpoint_lil278_prose_and_promotion_v1 import ARCHIVES, BATCH, PACKAGE, PROMOTED, REGISTRY, ROM
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest
from scripts.save_editorial_progress_checkpoint_v10 import checkpoint


ARCHIVE = ARCHIVES / 'Lil278_research_20261110_v1'
FINAL = Path('translations/lil_B299_B311_final_review_v1.json')
NAMES = Path('translations/lil_B299_B311_scoped_names_final_v1.json')
READY = BATCH / 'research_completion_v1/research_completion.json'


def archive_receipts():
    prior = load(PRIOR_ARCHIVE / 'archive_manifest.json')['artifacts']
    artifacts = {}
    for path in sorted(BATCH.rglob('*.json')):
        relative = path.relative_to(BATCH)
        if any(part.endswith('checkpoint_v1') for part in relative.parts):
            continue
        raw = path.read_bytes()
        source_hash = digest(path)
        old = prior.get(str(path))
        if old:
            packed = Path(old['archive'])
            assert source_hash == old['source_sha256'] and digest(packed) == old['archive_sha256']
        else:
            packed = (ARCHIVE / relative).with_suffix('.json.gz')
            packed.parent.mkdir(parents=True, exist_ok=True)
            packed.write_bytes(gzip.compress(raw, compresslevel=9, mtime=0))
        assert gzip.decompress(packed.read_bytes()) == raw
        artifacts[str(path)] = dict(archive=str(packed), source_sha256=source_hash, archive_sha256=digest(packed))
    assert prior.keys() <= artifacts.keys()
    producers = [Path(__file__), *(Path('scripts') / name for name in (
        'rebuild_editorial_exact_scope_v1.py', 'check_editorial_stored_exact_scope_v1.py',
        'select_lil278_gameplay_v1.py', 'analyze_scoped_menu_returns_v1.py',
        'approve_lil278_actual_v1.py', 'finalize_lil278_research_v1.py',
    ))]
    for path in producers:
        ast.parse(path.read_bytes(), filename=str(path))
    manifest = ARCHIVE / 'archive_manifest.json'
    save(manifest, dict(
        artifacts=artifacts, producers={str(path): digest(path) for path in producers},
        exact_previous_artifacts_reused=len(prior), all_selected_artifacts_lossless=True,
        raw_planes_images_RAM_andROMs_preserved_locally=True, all_individual_five_gates_pass=True,
        registered_integration_pending=True, new_credit=0, full_goal_complete=False,
    ))
    return manifest


def main():
    assert not ARCHIVE.exists()
    ready = load(READY)
    assert ready['all_individual_five_gates_pass'] and ready['registered_integration_pending']
    assert (ready['records'], ready['revisions'], ready['retentions'], ready['native_body_pages']) == (278, 170, 108, 280)
    assert (ready['actual_source_body_objects'], ready['actual_pages'], ready['offline_only_source_body_objects']) == (52, 55, 220)
    assert ready['manuscript_sha256'] == digest(FINAL) and ready['names_sha256'] == digest(NAMES)
    assert all(digest(path) == checksum for path, checksum in ready['evidence'].items())
    archive = archive_receipts()

    release = load(PACKAGE / 'verification/registered_release_verification.json')
    protected = {
        str(REGISTRY): release['registry_sha256'], str(PROMOTED): digest(PROMOTED),
        str(ROM): release['candidate_sha256'], release['candidate']: release['candidate_sha256'],
        release['manifest']: release['manifest_sha256'], release['patch']: release['patch_sha256'],
        release['canonical_base']: release['canonical_sha256'], 'work/clean.nds': release['clean_input_sha256'],
        str(FINAL): digest(FINAL), str(NAMES): digest(NAMES),
    }
    summary = ('Lil B299–B311 passed all five review gates for 278 records and ten scoped names. '
               'Stored checks covered all 280 pages, 272 native lookups and 670 relocated branch cases. '
               'A focused cold-boot sample displayed 52 bodies and all six captions. '
               'The batch is ready for registered integration and the ledger still credits 25,105 reviews.')
    notes = f"""# Lil B299–B311 stored and gameplay checkpoint

{summary}

The registered Lil361 candidate is the exact reconstruction parent. All 13 reviewed groups rebuild with their complete clean and current inventories, covering 470 commands and 134 relative sites. Only SC2 changes. The block, archive and serialized ROM inverses are exact. A byte-identical ARM9, COMMON, font, runtime payload and all 13 current blocks qualify reuse of the earlier Lil startup context. The research image is pinned and remains separate from the promotion candidate.

Stored render checks matched the directly viewed native pages, with 67 fresh parity-dependent pages and 213 exact reuses. The native full-buffer lookup found every one of the 272 speech bodies. All 336 SC2 loads and cache hits and 672 original parent handoffs passed, including unchanged neighbors and first instruction reads. These are offline native results.

One 25,121-frame initialized Lil B22 sample exercised the page turns in the Basra spice exchange, including the Market Info instruction and its closing sentence. All eight system alerts returned on ordinary A presses. All three two-choice menus displayed their six complete captions. Both highlights were captured for Fight or Run and for the river crossing. The rest menu capture shows Rest longer selected. The selected options were Run, Rest longer and Cross on foot. The tail reached the original host resupply, steering tutorial and Amsterdam departure alert. Seven sheets were directly viewed and bound to the original captures. This host combines selected native commands from conditional alternatives. The remaining 220 bodies have offline-only coverage. Original optional activation, branch outcomes, rewards, locations, full-route play and hardware remain unvisited.

All 170 revisions and 108 justified retentions retain their source, current and exact planned storage references. Individual rows distinguish observed pages and captions from offline-only evidence. The ten scoped name decisions include actual headers where observed and retain separate catalogue and future role limits. [Final dialogue ledger](../{FINAL.as_posix()}) · [Final name review](../{NAMES.as_posix()})

Next, qualify the pure cumulative successor over the 728-entry Lil361 release, preserve all 114 accepted layers and the Market and ASCII right-bound repairs, and build an exactly reconstructable clean-input patch. Verify the new candidate's own startup and protected getters before crediting the batch once. Lil361 remains available for promotion testing and the full editorial goal remains active. [Lossless research evidence](../{archive.as_posix()})
"""
    evidence = {str(path): digest(path) for path in (READY, archive, FINAL, NAMES)}
    checkpoint(
        mutation=BATCH / 'research_checkpoint_v1', batch_key='editorial_execution_priority_20261104',
        batch_updates=dict(new_credit=0, current_batch='Lil B299–B311 ready for registered integration',
                           current_batch_not_yet_integrated=True, current_batch_registered_andcredited_once=False,
                           all_current_batch_fifth_gates_pending=False, current_batch_evidence=evidence,
                           no_batch_worker_live=True, previous_goal_turn_classification='progress',
                           current_goal_turn_classification='progress', guide_photos=False,
                           next_action='Build, verify and register the cumulative Lil278 successor over Lil361.'),
        additional_updates={'Lil_SC2_B299_B311_clean_20261110': dict(
            new_credit=0, all_fifth_gates_pending=False, all_individual_five_gates_pass=True,
            stored_checks_pending=False, gameplay_pending=False, registered_integration_pending=True,
            observed_body_records=52, offline_only_body_records=220, observed_menu_captions=6,
            no_batch_worker_live=True, evidence=evidence)},
        summary=summary, document=Path('docs/editorial_Lil278_stored_gameplay_20261110.md'),
        document_text=notes, completed=25105, protected=protected,
    )
    print('Archived Lil278 stored and gameplay review with zero new registered credit.')


if __name__ == '__main__':
    main()
