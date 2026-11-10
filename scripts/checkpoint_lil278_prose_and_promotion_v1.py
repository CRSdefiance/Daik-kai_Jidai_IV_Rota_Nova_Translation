"""Save the uncredited prose review and reconstruct the registered promotion candidate."""

import ast
import gzip
import json
from pathlib import Path

from dk4tool.patch.xdelta import apply_xdelta
from scripts.audit_story_glyph_consistency import load, save
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest
from scripts.save_editorial_progress_checkpoint_v10 import checkpoint


BATCH = Path('work/Lil278_B299_B311_clean_20261110')
ARCHIVES = Path('translations/editorial_checkpoints')
ARCHIVE = ARCHIVES / 'Lil278_prose_plan_20261110_v1'
PACKAGE = Path('releases/all_routes_editorial_20261110_lil361_candidate')
TEST = Path('out/promotion_ready_20261110_lil361_v2')
ROM = TEST / 'Translation_DS_All_Routes_Lil361_20261110_promotion_candidate.nds'
REGISTRY = Path('translations/release_stack.json')
PROMOTED = Path('translations/promoted_build.json')
MANUSCRIPT = Path('translations/lil_B299_B311_contextual_review_v1.json')
NAMES = Path('translations/lil_B299_B311_scoped_names_v1.json')


def reconstruct():
    release_path = PACKAGE / 'verification/registered_release_verification.json'
    release = load(release_path)
    assert not release['own_registered_startup_pending']
    assert release['clean_input_patch_byte_exact']
    assert (release['registered_manifest_entries'], release['accepted_layers'],
            release['passing_release_checks']) == (728, 114, 63)
    for relative, expected in load(PACKAGE / 'checksums.json').items():
        assert digest(PACKAGE / relative) == expected, relative
    patch = PACKAGE / 'translation.xdelta'
    clean = Path('work/clean.nds')
    protected = {
        str(REGISTRY): release['registry_sha256'],
        str(PROMOTED): digest(PROMOTED),
        str(patch): release['patch_sha256'],
        str(clean): release['clean_input_sha256'],
        release['canonical_base']: release['canonical_sha256'],
    }
    assert all(digest(path) == expected for path, expected in protected.items())
    registry = load(REGISTRY)
    assert registry['latest_promoted_build']['profile'] == 'all-routes-unified-v4701'
    assert release['profile'] in registry['profiles']
    manifest = gzip.decompress((PACKAGE / 'build_manifest.json.gz').read_bytes())
    assert gzip.decompress((PACKAGE / 'build_release_stack.json.gz').read_bytes()) == REGISTRY.read_bytes()
    parsed = json.loads(manifest)
    assert len(parsed['batches']) == 728 and len(parsed['checks']) == 63
    assert all(value is True for value in parsed['checks'].values())

    TEST.mkdir()
    apply_xdelta(clean, patch, ROM)
    assert digest(ROM) == release['candidate_sha256']
    assert ROM.read_bytes() == Path(release['candidate']).read_bytes()
    adjacent = ROM.with_suffix('.manifest.json')
    adjacent.write_bytes(manifest)
    assert digest(adjacent) == release['manifest_sha256']
    receipt = dict(
        candidate=ROM.as_posix(), candidate_sha256=digest(ROM),
        manifest=adjacent.as_posix(), manifest_sha256=digest(adjacent),
        patch=patch.as_posix(), patch_sha256=digest(patch), clean_input_sha256=digest(clean),
        registered_release=release_path.as_posix(), registered_release_sha256=digest(release_path),
        registry_sha256=digest(REGISTRY), exact_registered_candidate_reconstructed_from_clean_input=True,
        entries=728, accepted_layers=114, passing_release_checks=63, integrated_editorial_records=25105,
        user_acceptance_pending=True, main_promoted=False, new_editorial_credit=0, new_gameplay_claim=False,
    )
    save(TEST / 'promotion_reconstruction.json', receipt)
    protected.update({str(ROM): receipt['candidate_sha256'], str(adjacent): receipt['manifest_sha256']})
    return protected


def review_and_archive():
    prose, names = map(load, (MANUSCRIPT, NAMES))
    assert (prose['source_objects'], prose['complete_exchanges'],
            prose['proposed_revisions'], prose['justified_retentions']) == (278, 13, 170, 108)
    assert len(names['records']) == names['individual_name_retentions'] == 10
    gates = dict(source=True, context=True, localization=True, naturalness=True, formatting=False)
    assert all(row['review'] == gates for row in prose['records'] + names['records'])
    proof = load(BATCH / 'prose_gates_v1.json')
    assert proof['structural_projection_pass'] and proof['all_fifth_gates_false']
    plan = load(BATCH / 'plan_v2/automatic_plans.json')
    diagnostics = load(BATCH / 'plan_v2/diagnostics.json')
    assert len(plan['records']) == 272 and sum(row['expected_native_pages'] for row in plan['records']) == 280
    assert not plan['failures'] and not diagnostics['failures']
    assert not any(row['severity'] in {'error', 'warning'} for row in diagnostics['issues'])
    assert plan['typed_choice_labels_not_formatted_as_speech'] == 6
    assert load(BATCH / 'formatting_v1/native_macro_measurements.json')[
        'fresh20_native_preflight_cases_not_new_renderer_characterization']
    earlier = load(ARCHIVES / 'Lil278_clean_20261110_v1/archive_manifest.json')['artifacts']
    artifacts = {}
    files = sorted(path for path in BATCH.rglob('*.json') if 'contextual_checkpoint_v1' not in path.parts)
    for path in files:
        raw = path.read_bytes()
        previous = earlier.get(str(path))
        if previous:
            packed = Path(previous['archive'])
            assert digest(packed) == previous['archive_sha256']
            assert digest(path) == previous['source_sha256']
        else:
            packed = (ARCHIVE / path.relative_to(BATCH)).with_suffix('.json.gz')
            packed.parent.mkdir(parents=True, exist_ok=True)
            packed.write_bytes(gzip.compress(raw, compresslevel=9, mtime=0))
        assert gzip.decompress(packed.read_bytes()) == raw
        artifacts[str(path)] = dict(archive=str(packed), source_sha256=digest(path), archive_sha256=digest(packed))
    assert earlier.keys() <= artifacts.keys()
    producers = [Path(__file__), Path('scripts/prepare_lil278_layout_v1.py'),
                 Path('scripts/prepare_lil278_prose_v1.py')]
    for path in producers:
        ast.parse(path.read_bytes(), filename=str(path))
    archive = ARCHIVE / 'archive_manifest.json'
    save(archive, dict(artifacts=artifacts, producers={str(path): digest(path) for path in producers},
                       first_four_gates_pass=True, all_fifth_gates_pending=True, new_credit=0))
    return archive


def main():
    assert not TEST.exists() and not ARCHIVE.exists()
    protected = reconstruct()
    archive = review_and_archive()
    receipt = ARCHIVE / 'promotion_reconstruction.json'
    receipt.write_bytes((TEST / receipt.name).read_bytes())
    pins = Path('translations/rom_retention_pins.json')
    before = pins.read_bytes()
    values = load(pins)
    assert all(Path(row['path']).resolve() != ROM.resolve() for row in values)
    values.append(dict(path=str(ROM.resolve()), reason='Preserve the Lil361 promotion-testing copy. SHA256 ' + digest(ROM)))
    staged = pins.with_name('rom_retention_pins.Lil361_promotion.pending.json')
    assert not staged.exists()
    save(staged, values)
    assert pins.read_bytes() == before
    staged.replace(pins)

    evidence = {str(path): digest(path) for path in (MANUSCRIPT, NAMES, archive, receipt)}
    summary = ('The Lil361 promotion candidate was reconstructed from the clean Japanese ROM and matched the '
               'registered image byte for byte. It includes the Market Trade-screen fix and 25,105 integrated reviews. '
               'Lil B299–B311 has 278 contextual prose decisions and a provisional layout plan. Native display, visual, '
               'stored and gameplay checks remain before registration. Main V4701 awaits cold-boot acceptance.')
    notes = f"""# Lil361 promotion candidate and Lil B299–B311 prose checkpoint

{summary}

The [local promotion ROM](../{ROM.as_posix()}) and adjacent manifest match the registered candidate. The [clean-input patch and release evidence](../{PACKAGE.as_posix()}/README.md) cover 728 registered entries, 114 accepted layers, 63 release checks and 27 repository tests. The published patch reconstructs this copy byte for byte. This handoff adds fresh reconstruction evidence and reuses the registered startup and gameplay checks. Physical hardware acceptance is pending. [Reconstruction receipt](../{receipt.as_posix()})

The current build includes the registered fix for the garbled line under Goods Info. The focused Market test reproduced the original Cheese/Food 101 defect and checked the fix in Local and Cargo. Lil361 adds 361 contextual reviews across B283–B298 and preserves the prior Rafael tutorial work and ASCII right-bound correction. [Registered build details](editorial_Lil361_registered_20261110.md)

The next 13 exchanges have 170 proposed revisions, 108 individually justified retentions and 10 scoped name retentions. The four prose gates pass, with source/current references and earlier source-first drafts preserved. Exact name and terminology checks cover Basra, the nine commission spices, Market Info and Proof of Conquest. [Dialogue manuscript](../{MANUSCRIPT.as_posix()}) · [Name decisions](../{NAMES.as_posix()})

Twenty native substitution preflights pass. The provisional plan covers 272 speech bodies and 280 pages, with six separately typed captions and zero plan errors or warnings. The plan keeps Market Info together and moves several page turns to complete thoughts. The first renderer attempts stopped at the captain guard because the entry points defaulted to Hodram. Resume using the explicit Lil captain context and exact registered-block/runtime dependency guards, then complete native and visual review, storage checks and representative gameplay before crediting or shipping the batch. [Lossless checkpoint archive](../{archive.as_posix()})
"""
    progress = dict(new_credit=0, proposed_revisions=170, justified_retentions=108,
                    all_five_gates_pending=False, first_four_individual_gates_pass=True,
                    names_terms_consumers_pending=False, all_fifth_gates_pending=True,
                    provisional_bodies=272, provisional_pages=280, provisional_captions=6,
                    unresolved_plan_warnings=0, native_rendering_pending=True,
                    direct_visual_review_pending=True, stored_checks_pending=True, gameplay_pending=True,
                    registered_integration_pending=True, no_batch_worker_live=True, evidence=evidence)
    checkpoint(
        mutation=BATCH / 'prose_promotion_checkpoint_v1', batch_key='editorial_execution_priority_20261104',
        batch_updates=dict(new_credit=0, current_batch='Lil B299–B311 prose and provisional layout',
                           current_batch_not_yet_integrated=True, current_batch_registered_andcredited_once=False,
                           all_current_batch_fifth_gates_pending=True, current_batch_evidence=evidence,
                           no_batch_worker_live=True, previous_goal_turn_classification='progress',
                           current_goal_turn_classification='progress', guide_photos=False,
                           next_action='Resume native display with explicit Lil captain and qualified scope reuse.'),
        additional_updates={'Lil_SC2_B299_B311_clean_20261110': progress},
        summary=summary, document=Path('docs/editorial_Lil361_promotion_Lil278_prose_20261110.md'),
        document_text=notes, completed=25105, protected=protected,
    )
    print(ROM)
    print(digest(ROM))


if __name__ == '__main__':
    main()
