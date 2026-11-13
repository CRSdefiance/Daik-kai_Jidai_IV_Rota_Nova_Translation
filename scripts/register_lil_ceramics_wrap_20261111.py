"""Register the verified ceramics exchange as a zero-credit cumulative revision."""

from copy import deepcopy
from gzip import compress
from json import dumps
from pathlib import Path
from shutil import copyfile
from xml.etree import ElementTree

from dk4tool.dialogue.review import validate_natural_dialogue_batch
from dk4tool.patch.xdelta import apply_xdelta, make_xdelta
from scripts import replay_lil_ceramics_wrap_20261111 as replay
from scripts import stage_lil_ceramics_wrap_20261111 as stage
from scripts.editorial_ledger_storage_v1 import encode_ledger
from scripts.prepare_all_routes_promotion_20261111 import package_checksums, verify_runtime
from scripts.verify_release_baseline import files


base, parent = stage.base, stage.parent
PROFILE = 'all-routes-lil-ceramics-wrap-v1-20261111'
CHECK = 'registered_lil_ceramics_contextual_wrap_and_complete_parent_inverse'
ROOT = Path('out/lil_ceramics_wrap_registered_20261111_v1')
ROM = ROOT / 'Translation_DS_All_Routes_Lil_Ceramics_20261111_candidate.nds'
MANIFEST = ROM.with_suffix('.manifest.json')
PACKAGE = Path('releases/all_routes_editorial_20261111_lil_ceramics_wrap_candidate')
PATCH, VERIFICATION = PACKAGE / 'translation.xdelta', PACKAGE / 'verification'
REVIEW, RELEASE = (VERIFICATION / name for name in ('registered_review.json', 'registered_release_verification.json'))
QA = stage.ROOT / 'repository_qa.xml'
DOC = Path('docs/editorial_lil_ceramics_wrap_registered_20261111.md')


def verify_inputs():
    old, proof, setup, live, startup, draft = map(base.load,
        (parent.RELEASE, stage.PROOF, replay.SETUP, replay.LIVE, replay.STARTUP, stage.REVIEW))
    assert stage.sha(stage.ARCHIVE.read_bytes()) == proof['target_archive_sha256']
    assert base.digest(stage.REVIEW) == proof['review_sha256']
    assert base.digest(stage.PROOF) == setup['source_proof_sha256']
    assert base.digest(parent.ROM) == old['candidate_sha256'] == proof['candidate_sha256'] == live['parent_sha256']
    assert base.digest(parent.CLEAN) == old['clean_input_sha256']
    assert base.digest(parent.MANIFEST) == old['manifest_sha256']
    assert base.digest(replay.ROM) == setup['candidate_sha256'] == live['candidate_sha256'] == startup['candidate_sha256']
    assert startup['cold_boot'] and not startup['savestate'] and len(startup['original_protected_name_getters']) == 24
    assert len(startup['exact_matching_frames']) == 6 and startup['complete_deployed_payload_exact']
    assert len(live['revised_pages']) == 5 and len(live['unchanged_scene_frames']) == 12
    assert live['complete_revised_native_masks_match_captures'] and live['differences_confined_to_original_body_rectangle']
    assert proof['sheet_sha256'] == live['reviewed_offline_sheet_sha256'] == base.digest(proof['sheet'])
    for document in (live, startup):
        assert all(base.digest(path) == digest for path, digest in document['evidence'].items())
    suites = list(ElementTree.parse(QA).iter('testsuite'))
    tests = sum(int(row.get('tests', 0)) for row in suites)
    assert tests == 56 and not any(int(row.get(k, 0)) for row in suites for k in ('errors', 'failures', 'skipped'))
    return old, proof, live, draft, tests


def reconstruct(old, proof, draft):
    parent_image = base.NdsImage.open(parent.ROM)
    original = base.NdsImage.open(parent.CLEAN)
    clean = stage.IlnkContainer.parse(original.read_file(stage.FILE)).blocks[stage.BLOCK]
    before = parent_image.read_file(stage.FILE)
    archive = stage.IlnkContainer.parse(before)
    archive.blocks[stage.BLOCK] = stage.reconstruct(archive.blocks[stage.BLOCK], clean, proof['group'],
        proof['current_packet'], draft['records'], [])
    target = archive.to_bytes()
    assert target == stage.ARCHIVE.read_bytes() and stage.sha(target) == proof['target_archive_sha256']
    parent_files = files(parent_image)
    parent_image.replace_file(stage.FILE, target)
    target_files = files(parent_image)
    assert target_files.keys() == parent_files.keys()
    assert [name for name in target_files if target_files[name] != parent_files[name]] == [stage.FILE]
    assert bytes(parent_image.rom.save()) == replay.ROM.read_bytes()
    verify_runtime(target_files[stage.ARM], old)
    parent_image.replace_file(stage.FILE, before)
    assert bytes(parent_image.rom.save()) == parent.ROM.read_bytes()


def archive_file(raw, path):
    path.write_bytes(compress(raw, compresslevel=1, mtime=0))


def write_pending(path, data):
    with path.open('xb') as stream:
        for start in range(0, len(data), 1024 * 1024):
            stream.write(data[start:start+1024*1024])
    assert base.digest(path) == stage.sha(data)


def main():
    registry_pending = base.REGISTRY.with_name('release_stack.lil_ceramics.pending.json')
    ledger_pending = base.LEDGER.with_name('editorial_review_current.lil_ceramics.pending.json')
    assert not any(path.exists() for path in (ROOT, PACKAGE, DOC, registry_pending, ledger_pending))
    old, proof, live, draft, tests = verify_inputs()
    reconstruct(old, proof, draft)
    before_registry, before_ledger = base.REGISTRY.read_bytes(), base.LEDGER.read_bytes()
    assert stage.sha(before_registry) == old['registry_sha256']
    registry, ledger, manifest = map(base.load, (base.REGISTRY, base.LEDGER, parent.MANIFEST))
    assert PROFILE not in registry['profiles'] and len(registry['accepted_layers']) == 114
    assert len(manifest['batches']) == 780 and len(manifest['checks']) == 115 and all(manifest['checks'].values())
    assert ledger['current_integrated_candidate']['sha256'] == old['candidate_sha256']
    assert ledger['records_editorially_completed'] == 27697 and not ledger['full_goal_complete']
    credits = {(r['file_path'], r['id']) for r in ledger[base.CONTEXT]['integrated_record_keys']}
    assert all((row['file_path'], row['id']) in credits for row in draft['records'])
    main_sha = base.digest(base.PROMOTED)
    ROOT.mkdir()
    VERIFICATION.mkdir(parents=True)
    make_xdelta(parent.CLEAN, replay.ROM, PATCH)
    apply_xdelta(parent.CLEAN, PATCH, ROM)
    sha = base.digest(ROM)
    assert ROM.read_bytes() == replay.ROM.read_bytes() and sha == live['candidate_sha256']
    for path in (stage.PROOF, replay.LIVE, replay.STARTUP, QA):
        copyfile(path, VERIFICATION / path.name)
        assert base.digest(VERIFICATION / path.name) == base.digest(path)

    refs = {row['id']: row for row in proof['group']['text_records']}
    records = [row | dict(review=row['review'] | {'formatting': True}, registered_reference=dict(
        block=stage.BLOCK, file_path=stage.FILE, offset=refs[row['id']]['new_offset'],
        bytes=refs[row['id']]['new_length'], candidate_sha256=sha, raw_hex=row['target_hex'])) for row in draft['records']]
    review = draft | dict(records=records, registered_candidate_sha256=sha, native_and_gameplay_proof=str(VERIFICATION / replay.LIVE.name))
    validate_natural_dialogue_batch(review)
    base.save(REVIEW, review)
    previous = ROOT / 'release_stack_before_lil_ceramics.json'
    previous.write_bytes(before_registry)
    archive_file(before_ledger, ROOT / 'editorial_ledger_before.json.gz')
    predecessor = {key: old[key] for key in ('profile', 'candidate', 'candidate_sha256', 'manifest', 'manifest_sha256', 'registry_sha256')}
    predecessor['registry'] = str(previous)
    profile = deepcopy(registry['profiles'][old['profile']])
    profile.update(verified_visible_gallery_captions_predecessor=predecessor, lil_ceramics_wrap_release=str(REVIEW),
                   note='Contextual revision and full-width reflow of the Hamburg ceramics exchange.')
    registry['profiles'][PROFILE] = profile
    base.save(registry_pending, registry)
    manifest.update(profile=PROFILE, candidate_rom=str(ROM), candidate_sha256=sha, release_stack_sha256=base.digest(registry_pending))
    manifest['batches'].append(str(REVIEW))
    manifest['checks'][CHECK] = True
    manifest['changed_records'][stage.FILE].extend(r for r in draft['stored_changes'] if r not in manifest['changed_records'][stage.FILE])
    manifest['lil_ceramics_registered_successor_pipeline'] = dict(predecessor=predecessor, driver=str(Path(__file__)),
        driver_sha256=base.digest(__file__), review=str(REVIEW), review_sha256=base.digest(REVIEW),
        affected_file=stage.FILE, affected_block=stage.BLOCK, reconstructed_archive_sha256=proof['target_archive_sha256'],
        only_five_changed_speeches=True, clean_and_parent_inverses_exact=True, original_20_command_structure_preserved=True)
    assert len(manifest['batches']) == 781 and len(manifest['checks']) == 116
    base.save(MANIFEST, manifest)
    startup_path = VERIFICATION / replay.STARTUP.name
    release = old | dict(profile=PROFILE, candidate=str(ROM), candidate_sha256=sha, patch=str(PATCH), patch_sha256=base.digest(PATCH),
        manifest=str(MANIFEST), manifest_sha256=base.digest(MANIFEST), registry_sha256=base.digest(registry_pending), predecessor=predecessor,
        registered_manifest_entries=781, passing_release_checks=116, repository_tests=tests, own_registered_startup=str(startup_path),
        own_registered_startup_sha256=base.digest(startup_path), changed_components=[], changed_internal_files=[stage.FILE],
        new_contextual_records=0, prose_revisions=2, justified_retentions=15, reviewed_UI_labels=0,
        actual_verification_scope=dict(actual_emulator=True, hardware=False, revised_complete_pages=5, unchanged_scene_panels=12,
                                       initialized_Lil_entry=True, natural_Hamburg_activation=False))
    base.save(RELEASE, release)
    base.save(PACKAGE / 'release_manifest.json', release | {'user_acceptance_pending': True})
    archive_file(MANIFEST.read_bytes(), PACKAGE / 'build_manifest.json.gz')
    archive_file(registry_pending.read_bytes(), PACKAGE / 'build_release_stack.json.gz')
    ledger['current_integrated_candidate'].update(path=str(ROM), sha256=sha, profile=PROFILE, patch=str(PATCH),
        patch_sha256=release['patch_sha256'], manifest=str(MANIFEST), manifest_sha256=release['manifest_sha256'], registered_release_verification=str(RELEASE))
    ledger['latest_checkpoint'] = 'The Hamburg ceramics exchange is registered with five retrospective display revisions.'
    ledger['lil_ceramics_retrospective_20261111'] = dict(review=str(REVIEW), release=str(RELEASE), new_dialogue_credit=0,
        existing_credit_preserved=17, prose_revisions=2, wrap_only_changes=3)
    write_pending(ledger_pending, encode_ledger(ledger))
    plan = dict(registry_before=stage.sha(before_registry), registry_after=base.digest(registry_pending),
                ledger_before=stage.sha(before_ledger), ledger_after=base.digest(ledger_pending), main_sha256=main_sha)
    base.save(VERIFICATION / 'registration_mutation_plan.json', plan)
    (PACKAGE / 'README.md').write_text(f'''# Hamburg ceramics candidate

The [local ROM](../../{ROM.as_posix()}) includes five retrospective dialogue changes in Lil’s Hamburg ceramics exchange. The [clean-input patch](translation.xdelta) reconstructs SHA-256 `{sha}` byte for byte from Japanese SHA-256 `{release['clean_input_sha256']}`. The 20 original commands and the unchanged forecast panel are preserved. Paired emulator fixtures matched the five complete revised masks and 12 unchanged panels. Cold boot, 24 protected name getters and 56 targeted tests passed.
''', encoding='utf-8', newline='\n')
    base.save(PACKAGE / 'checksums.json', package_checksums(PACKAGE))
    assert base.digest(base.REGISTRY) == plan['registry_before'] and base.digest(base.LEDGER) == plan['ledger_before']
    assert base.digest(base.PROMOTED) == main_sha
    registry_pending.replace(base.REGISTRY)
    try:
        ledger_pending.replace(base.LEDGER)
    except OSError:
        base.replace_checked(base.REGISTRY, before_registry)
        raise
    assert base.digest(base.REGISTRY) == plan['registry_after'] and base.digest(base.LEDGER) == plan['ledger_after']

    pin_path = Path('translations/rom_retention_pins.json')
    pins = base.load(pin_path)
    for path in (ROM, replay.ROM, *(Path(row['path']) for row in base.load(replay.SETUP)['fixture_ROMs'].values())):
        resolved = str(path.resolve())
        assert not any(row['path'] == resolved for row in pins)
        pins.append(dict(path=resolved, reason=f'Preserve Hamburg ceramics release and verification. SHA256 {base.digest(path)}'))
    base.replace_checked(pin_path, (dumps(pins, ensure_ascii=False, indent=2) + '\n').replace('\n', '\r\n').encode())
    base.replace_checked(DOC, f'''# Hamburg ceramics exchange registered

All 17 turns in Lil’s Hamburg ceramics scene were reread together. Three earlier wraps changed without rewording. Two lines were localized again to preserve the collector’s irritation and the port worker’s joke and suggestion. Twelve records, including the final forecast, retain their exact stored text. The [registered review](../{REVIEW.as_posix()}) records every decision and the exact clean, previous and final references.

Paired cold boots staged the complete original exchange at Lil’s entry. All five revised pages matched the native ink masks. The 12 retained panels and four sampled frames before and after the scene were identical. The original Hamburg trigger remains unvisited in this test. A separate cumulative cold boot passed six frame checks and 24 protected name getters. All 56 targeted tests passed.

The [candidate and clean-input patch](../{PACKAGE.as_posix()}/README.md) preserve the prior layers. The ledger still credits 27,697 reviews. The 279 shared-text keys and the rest of the retrospective work remain open.

The [older wrap inventory](../translations/editorial_checkpoints/SharedText_20261110_v1/historical_wrap_leads_current_v1.json) rebinds all 13 earlier leads to the parent. The previous Lil B218 repair remains present. Twelve recorded splits still need contextual and consumer review. None of those blocks is the Hamburg ceramics scene.
'''.encode())
    lead = f'# Current editorial checkpoint - 2026-11-11\n\nThe Hamburg ceramics exchange is registered. [Checkpoint]({DOC.name})\n\n'.encode()
    for filename in ('editorial_handoff_current.md', 'translation_progress.md', 'build_continuity_protocol.md'):
        path = Path('docs') / filename
        base.replace_checked(path, lead + path.read_bytes())
    print(f'Registered {ROM} | SHA-256 {sha} | 781 entries, 114 accepted layers, 116 checks, zero duplicate credit.')


if __name__ == '__main__':
    main()
