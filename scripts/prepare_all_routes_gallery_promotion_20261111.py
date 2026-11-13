"""Reconstruct the registered All Routes candidate and audit its editorial coverage."""

from collections import Counter
from gzip import decompress
from hashlib import sha256
from json import dumps, loads
from pathlib import Path
from shutil import copyfile
from xml.etree import ElementTree

from dk4tool.patch.duel_editorial import owned_entries
from dk4tool.patch.xdelta import apply_xdelta
from dk4tool.rom.nds import NdsImage
from dk4tool.script.common_message_table import DIRECTORY_OFFSET, TABLE_OFFSET, common_message_entries
from scripts.audit_item_advice_promotion_scope_v1 import ARM, COMMON, HELP, JAPANESE, check_story
from scripts.prepare_all_routes_promotion_20261111 import package_checksums, verify_runtime
from scripts.register_visible_gallery_captions_v1 import CLEAN, MANIFEST, PACKAGE, PATCH, PROFILE, RELEASE, ROM, VERIFICATION, base
from scripts.verify_release_baseline import files


RELEASES = Path('releases')
NAMES = ('arrival_month_labels', 'ancient_map_text', 'sound_bgm_titles', 'ancient_map_hint_label',
         'visible_online_captions', 'visible_gallery_captions')
OUTPUT = Path('out/promotion_ready_20261111_gallery_and_map')
CANDIDATE = OUTPUT / 'Translation_DS_All_Routes_Gallery_and_Map_20261111_candidate.nds'


def check_release_chain():
    inventory_counts = {}
    previous = None
    for name in NAMES:
        package = RELEASES / f'all_routes_editorial_20261111_{name}_candidate'
        inventory = package_checksums(package)
        assert inventory == base.load(package / 'checksums.json')
        inventory_counts[package.as_posix()] = len(inventory)
        release = base.load(package / 'release_manifest.json')
        manifest_raw = decompress((package / 'build_manifest.json.gz').read_bytes())
        registry_raw = decompress((package / 'build_release_stack.json.gz').read_bytes())
        assert sha256(manifest_raw).hexdigest() == release['manifest_sha256']
        assert sha256(registry_raw).hexdigest() == release['registry_sha256']
        assert inventory['translation.xdelta'] == release['patch_sha256']
        manifest, registry = loads(manifest_raw), loads(registry_raw)
        assert manifest['candidate_sha256'] == release['candidate_sha256']
        assert manifest['release_stack_sha256'] == release['registry_sha256']
        assert len(manifest['batches']) == release['registered_manifest_entries']
        assert len(manifest['checks']) == release['passing_release_checks']
        assert all(check is True for check in manifest['checks'].values())
        if previous:
            assert release['predecessor']['candidate_sha256'] == previous['candidate_sha256']
            assert release['predecessor']['manifest_sha256'] == previous['manifest_sha256']
            assert release['predecessor']['registry_sha256'] == previous['registry_sha256']
            assert manifest['batches'][:-1] == previous_manifest['batches']
            assert manifest['checks'] | previous_manifest['checks'] == manifest['checks']
            for key in ('canonical_baseline', 'accepted_layers', 'latest_promoted_build'):
                assert registry[key] == previous_registry[key]
            assert registry['profiles'] | previous_registry['profiles'] == registry['profiles']
        else:
            arrival = release
        previous, previous_manifest, previous_registry = release, manifest, registry
    return arrival, release, manifest, registry, inventory_counts


def coverage(clean, current, release):
    ledger = base.load(base.LEDGER)
    keys = Counter((row['file_path'], row['id']) for row in ledger[base.CONTEXT]['integrated_record_keys'])
    assert len(keys) == ledger['records_editorially_completed'] == 27697 and set(keys.values()) == {1}
    assert ledger['current_integrated_candidate']['sha256'] == release['candidate_sha256']
    assert not ledger['full_goal_complete']
    story = check_story(base.load, base.digest, clean, keys)
    story_count = sum(row['credited_objects'] for row in story)
    assert story_count == 24092
    assert {key for path, key in keys if path == HELP} == {f'HELP_TOPIC_{number}' for number in range(202)}

    source = common_message_entries(clean.read_file(COMMON), clean.read_file(ARM))
    arm = current.read_file(ARM)
    stored = owned_entries(current.read_file(COMMON), arm, sha256(arm[DIRECTORY_OFFSET:TABLE_OFFSET]).hexdigest())
    assert len(source) == len(stored) == 3668
    assert all(a.message_id == b.message_id == n for n, (a, b) in enumerate(zip(source, stored, strict=True)))
    common_credits = {key for path, key in keys if path == COMMON}
    assert common_credits <= {f'COMMON_MESSAGE_{row.message_id}' for row in source}
    pending = [row.message_id for row in source if f'COMMON_MESSAGE_{row.message_id}' not in common_credits]
    legacy_path = Path('translations/editorial_checkpoints/SharedText_20261110_v1/legacy_common_35_checkpoint_v1.json')
    legacy_ids = {98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111,
                  113, 114, 115, 116, 117, 119, 124, 284, 287, 296, 300, 304, 318, 330, 331, 332, 333, 750, 751, 752}
    online_ids, scene_ids = set(range(3289, 3320)), set(range(3393, 3607))
    assert set(pending) == legacy_ids | online_ids | scene_ids
    arm9_credits = sorted(key for path, key in keys if path == ARM)
    assert len(arm9_credits) == 14
    assert story_count + len(common_credits) + 202 + len(arm9_credits) == len(keys)
    japanese = [n for n in pending if JAPANESE.search(stored[n].text.decode('cp932', errors='replace'))]
    return dict(candidate_sha256=release['candidate_sha256'], coverage_ledger=base.LEDGER.as_posix(),
        ledger_sha256=base.digest(base.LEDGER), completed_reviews=len(keys),
        revised_records=ledger['records_revised_and_integrated'],
        justified_retentions=ledger['retained_wordings_editorially_completed'],
        story_archives=story, typed_story_positions_reviewed=story_count, source_help_topics_credited=202,
        arm9_prose_credited_ids=arm9_credits,
        shared_native_COMMON=dict(total=len(source), credited=len(common_credits), pending=len(pending),
            pending_ids=pending, pending_with_Japanese_in_current_storage=japanese,
            legacy_keys_pending=len(legacy_ids), legacy_source_comparison=legacy_path.as_posix(),
            online_keys_pending=len(online_ids), scene_and_asset_keys_pending=len(scene_ids),
            scope='These keys need review or consumer classification. Stored Japanese does not establish display.'),
        independently_reviewed_UI=dict(gallery_event_captions=164, online_captions=13),
        remaining_unquantified='Other player-facing UI prose, name and role consistency, retrospective wrapping and '
            'glyph checks, and representative town and random-scene coverage.',
        separate_work='Deferred graphics artwork and later older-record technical re-audit.',
        whole_game_percent_established=False, full_goal_complete=False)


def main():
    arrival, release, manifest, registry, inventory = check_release_chain()
    assert not (VERIFICATION / 'promotion_reconstruction.json').exists()
    assert base.digest(base.REGISTRY) == release['registry_sha256']
    assert manifest['profile'] == release['profile'] == PROFILE
    assert release['registered_manifest_entries'] == 780 and release['passing_release_checks'] == 115
    assert registry['profiles'][PROFILE]['status'] == 'experimental'
    accepted = registry['accepted_layers']
    batches = {name.replace('\\', '/') for name in manifest['batches']}
    assert len(accepted) == release['accepted_layers'] == 114
    assert all(layer['status'] == 'accepted' and (layer.get('baked_into_baseline') is True or
        layer['batch'].replace('\\', '/') in batches) for layer in accepted)
    canonical = registry['canonical_baseline']
    assert base.digest(canonical['path']) == canonical['sha256'] == manifest['base_sha256'] == release['canonical_sha256']
    assert manifest['checks']['registered_market_goods_info_terminated_format_and_complete_parent_inverse']
    assert manifest['checks']['registered_runtime_bounds_and_complete_parent_target_inverse']
    assert release['clean_input_patch_byte_exact'] and release['whole_parent_inverse_exact']
    assert release['experimental_not_promoted'] and not release['own_registered_startup_pending']
    for path, field in ((CLEAN, 'clean_input_sha256'), (ROM, 'candidate_sha256'), (PATCH, 'patch_sha256'),
                        (MANIFEST, 'manifest_sha256'), (release['own_registered_startup'], 'own_registered_startup_sha256')):
        assert base.digest(path) == release[field]
    assert base.load(RELEASE) | {'user_acceptance_pending': True} == release
    boot = base.load(release['own_registered_startup'])
    assert boot['candidate_sha256'] == release['candidate_sha256'] and boot['cold_boot'] and not boot['savestate']
    assert boot['complete_deployed_payload_exact'] and len(boot['original_protected_name_getters']) == 24
    suites = list(ElementTree.parse(VERIFICATION / 'visible_gallery_captions_repo_qa_20261111.xml').iter('testsuite'))
    assert sum(int(row.get('tests', 0)) for row in suites) == release['repository_tests'] == 34
    assert not any(int(row.get(key, 0)) for row in suites for key in ('errors', 'failures', 'skipped'))
    main_build = base.load(base.PROMOTED)
    assert main_build['profile'] == 'all-routes-unified-v4701' and main_build['main_build']

    adjacent = CANDIDATE.with_suffix('.manifest.json')
    if not OUTPUT.exists():
        OUTPUT.mkdir()
        apply_xdelta(CLEAN, PATCH, CANDIDATE)
        copyfile(MANIFEST, adjacent)
    else:
        assert set(OUTPUT.iterdir()) == {CANDIDATE, adjacent}
    assert CANDIDATE.read_bytes() == ROM.read_bytes() and base.digest(CANDIDATE) == release['candidate_sha256']
    assert base.digest(adjacent) == release['manifest_sha256']
    assert base.digest(arrival['candidate']) == arrival['candidate_sha256']
    candidate = NdsImage.open(CANDIDATE)
    before, after = files(NdsImage.open(arrival['candidate'])), files(candidate)
    changed = sorted(path for path in before.keys() | after.keys() if before.get(path) != after.get(path))
    assert changed == [COMMON, ARM]
    assert sha256(after[ARM]).hexdigest() == release['target_ARM9_sha256']
    assert sha256(after[COMMON]).hexdigest() == release['target_COMMON_sha256']
    verify_runtime(after[ARM], release)
    scope = coverage(NdsImage.open(CLEAN), candidate, release)
    base.save(VERIFICATION / 'editorial_remaining_scope.json', scope)
    receipt = dict(candidate=CANDIDATE.as_posix(), candidate_sha256=release['candidate_sha256'],
        manifest=adjacent.as_posix(), manifest_sha256=release['manifest_sha256'], registry_sha256=release['registry_sha256'],
        patch=PATCH.as_posix(), patch_sha256=release['patch_sha256'], clean_sha256=release['clean_input_sha256'],
        profile=PROFILE, byte_exact_reconstruction=True, accepted_layers=114, release_entries=780, release_checks=115,
        tests=34, protected_name_getters=24, verified_package_checksums_before_preparation=inventory,
        previous_candidate_sha256=arrival['candidate_sha256'], changed_paths=changed, additional_editorial_records=100,
        main_profile=main_build['profile'], user_acceptance_pending=True, new_hardware_coverage=False)
    for directory in (VERIFICATION, OUTPUT):
        base.save(directory / 'promotion_reconstruction.json', receipt)
    readme = PACKAGE / 'README.md'
    details = readme.read_text(encoding='utf-8').split('\n\n', 2)[2]
    readme.write_text(
        '# All Routes Gallery and Map promotion candidate\n\n'
        f'Cold-boot the [local ROM](../../{CANDIDATE.as_posix()}) with its [build manifest](../../{adjacent.as_posix()}). '
        f'The [clean-input patch](translation.xdelta) reconstructs this ROM byte for byte from Japanese ROM SHA-256 '
        f'`{release["clean_input_sha256"]}`. ROM SHA-256 `{release["candidate_sha256"]}`. '
        f'Patch SHA-256 `{release["patch_sha256"]}`.\n\n'
        'The cumulative build includes all four story routes, Rafael’s tutorials, the Market Goods Info repair, '
        'the ASCII right-bound correction, Ancient Map text, Sound Setup titles and the Online and Gallery captions. '
        'V4701 remains main pending user acceptance. [Reconstruction](verification/promotion_reconstruction.json) · '
        '[Remaining work](verification/editorial_remaining_scope.json)\n\n' + details,
        encoding='utf-8', newline='\n')
    base.save(PACKAGE / 'checksums.json', package_checksums(PACKAGE))
    pins_path = Path('translations/rom_retention_pins.json')
    pins = base.load(pins_path)
    assert not any(Path(pin['path']) == CANDIDATE.resolve() for pin in pins)
    pins.append(dict(path=str(CANDIDATE.resolve()), reason=f'Preserve promotion test copy. SHA256 {base.digest(CANDIDATE)}'))
    base.replace_checked(pins_path, (dumps(pins, ensure_ascii=False, indent=2) + '\n').replace('\n', '\r\n').encode())
    print(f'{CANDIDATE} | {release["candidate_sha256"]} | {scope["completed_reviews"]} reviews | 279 shared keys pending')


if __name__ == '__main__':
    main()
