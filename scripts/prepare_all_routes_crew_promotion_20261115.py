"""Prepare and verify the registered All Routes Crew Review test candidate."""

import filecmp
from collections import Counter
from gzip import decompress
from hashlib import sha256
from json import loads
from pathlib import Path
from shutil import copyfile
from xml.etree import ElementTree

from dk4tool.patch.xdelta import apply_xdelta
from scripts import register_barmaid_town_labels_20261115 as current
from scripts import verify_fernando_excited_20261115 as crew
from scripts.audit_item_advice_promotion_scope_v1 import ARM, COMMON, HELP, check_story
from scripts.prepare_all_routes_promotion_20261111 import package_checksums, verify_runtime
from scripts.scan_current_progressive_wrap_leads_20261111 import scan
from scripts.verify_release_baseline import files


base = current.base
OUTPUT = Path('out/promotion_ready_20261115_crew_review')
CANDIDATE = OUTPUT / 'Translation_DS_All_Routes_20261115_Crew_Review_candidate.nds'
REPLAY = Path('work/fernando_crew_candidate_20261115_v1')
TRIAGE = Path('translations/editorial_checkpoints/SharedText_20261110_v1/current_progressive_wrap_triage_v25.json')


def story_wrap_scope(candidate):
    def key(row):
        return tuple(row[field] for field in ('file_path', 'block', 'source_selector',
                     'native_preamble_hex', 'stored_body_hex'))

    triage = base.load(TRIAGE)
    reviewed = Counter(key(row) for row in triage['reviewed_current_heuristic_hits'])
    archives, pending = {}, []
    for path in triage['scanned']:
        raw = candidate.read_file(path)
        stats, hits = scan(path, raw)
        current_hits = Counter(key(row) for row in hits)
        unresolved = [row for row in hits if current_hits[key(row)] != 1 or reviewed[key(row)] != 1]
        archives[path] = dict(stats) | dict(archive_sha256=sha256(raw).hexdigest(),
            flagged_bodies=len(hits), exact_reviewed_matches=len(hits) - len(unresolved))
        pending.extend(unresolved)
    return dict(archives=archives, pending=pending, previous_triage_sha256=base.digest(TRIAGE))


def coverage(clean, candidate, release):
    ledger = base.load(base.LEDGER)
    keys = Counter((row['file_path'], row['id']) for row in ledger[base.CONTEXT]['integrated_record_keys'])
    assert len(keys) == ledger['records_editorially_completed'] and set(keys.values()) == {1}
    assert ledger['current_integrated_candidate']['sha256'] == release['candidate_sha256']
    story = check_story(base.load, base.digest, clean, keys)
    assert {key for path, key in keys if path == HELP} == {f'HELP_TOPIC_{n}' for n in range(202)}
    shared = {key for path, key in keys if path == COMMON}
    shared_catalogue = {f'COMMON_MESSAGE_{n}' for n in range(3668)}
    assert shared <= shared_catalogue
    pending = sorted(int(key.rsplit('_', 1)[1]) for key in shared_catalogue - shared)
    online = [n for n in pending if 3289 <= n <= 3319]
    labels = [n for n in pending if 3393 <= n <= 3606]
    arm = sum(path == ARM for path, _ in keys)
    wrap_scope = story_wrap_scope(candidate)
    return dict(completed_reviews=len(keys), ledger_sha256=base.digest(base.LEDGER), story=story,
        story_objects=sum(row['credited_objects'] for row in story), help_topics=202, ARM9_prose=arm,
        shared_reviewed=len(shared), shared_total=len(shared_catalogue), shared_pending=len(pending),
        legacy_pending=sorted(set(pending) - set(online) - set(labels)), online_stored_copy_pending=online,
        scene_label_pending=labels, scoped_story_wrap_leads_pending=len(wrap_scope['pending']),
        current_story_wrap_scan=wrap_scope, full_goal_complete=False)


def main():
    release = base.load(current.PACKAGE / 'release_manifest.json')
    assert package_checksums(current.PACKAGE) == base.load(current.PACKAGE / 'checksums.json')
    manifest_raw = decompress((current.PACKAGE / 'build_manifest.json.gz').read_bytes())
    registry_raw = decompress((current.PACKAGE / 'build_release_stack.json.gz').read_bytes())
    assert sha256(manifest_raw).hexdigest() == release['manifest_sha256'] == base.digest(current.MANIFEST)
    assert sha256(registry_raw).hexdigest() == release['registry_sha256'] == base.digest(base.REGISTRY)
    manifest, registry = loads(manifest_raw), loads(registry_raw)
    assert manifest['candidate_sha256'] == release['candidate_sha256']
    assert manifest['release_stack_sha256'] == release['registry_sha256']
    assert manifest['profile'] == release['profile'] == current.PROFILE
    assert registry['profiles'][current.PROFILE]['status'] == 'experimental'
    assert all(result is True for result in manifest['checks'].values())
    assert len(manifest['checks']) == release['passing_release_checks']
    assert len(manifest['batches']) == release['registered_manifest_entries']
    assert manifest['checks']['registered_market_goods_info_terminated_format_and_complete_parent_inverse']
    assert manifest['checks']['registered_runtime_bounds_and_complete_parent_target_inverse']
    accepted = registry['accepted_layers']
    batches = {name.replace('\\', '/') for name in manifest['batches']}
    assert len(accepted) == release['accepted_layers'] == 114
    assert all(layer['status'] == 'accepted' and (layer.get('baked_into_baseline') is True or
        layer['batch'].replace('\\', '/') in batches) for layer in accepted)
    assert base.digest(registry['canonical_baseline']['path']) == manifest['base_sha256'] == release['canonical_sha256']

    promoted = base.load(base.PROMOTED)
    before_manifest_raw = decompress((Path(promoted['release_directory']) / 'build_manifest.json.gz').read_bytes())
    assert sha256(before_manifest_raw).hexdigest() == promoted['build_manifest_sha256']
    before_manifest = loads(before_manifest_raw)
    assert manifest['batches'][:len(before_manifest['batches'])] == before_manifest['batches']
    assert manifest['checks'] | before_manifest['checks'] == manifest['checks']
    assert base.digest(promoted['rom']) == promoted['rom_sha256']
    assert base.digest(current.stage.CLEAN) == release['clean_input_sha256']
    assert base.digest(current.PATCH) == release['patch_sha256']
    assert base.digest(current.ROM) == release['candidate_sha256']
    assert release['clean_input_patch_byte_exact'] and release['whole_parent_inverse_exact']
    boot = base.load(release['own_registered_startup'])
    assert base.digest(release['own_registered_startup']) == release['own_registered_startup_sha256']
    assert boot['candidate_sha256'] == release['candidate_sha256'] and boot['cold_boot'] and not boot['savestate']
    assert boot['complete_deployed_payload_exact'] and len(boot['original_protected_name_getters']) == 24
    suite, = ElementTree.parse(current.VERIFY / 'repository_qa_verified.xml').iter('testsuite')
    assert int(suite.get('tests')) == release['repository_tests']
    assert not any(int(suite.get(key, 0)) for key in ('errors', 'failures', 'skipped'))

    OUTPUT.mkdir(exist_ok=True)
    adjacent = CANDIDATE.with_suffix('.manifest.json')
    if not CANDIDATE.exists():
        apply_xdelta(current.stage.CLEAN, current.PATCH, CANDIDATE)
    if not adjacent.exists():
        copyfile(current.MANIFEST, adjacent)
    assert filecmp.cmp(CANDIDATE, current.ROM, shallow=False)
    assert base.digest(CANDIDATE) == release['candidate_sha256']
    assert base.digest(adjacent) == release['manifest_sha256']
    clean, candidate, before = map(base.NdsImage.open, (current.stage.CLEAN, CANDIDATE, promoted['rom']))
    old_files, new_files = files(before), files(candidate)
    changed = sorted(path for path in old_files.keys() | new_files.keys() if old_files.get(path) != new_files.get(path))
    assert sha256(new_files[ARM]).hexdigest() == release['target_ARM9_sha256']
    assert sha256(new_files[COMMON]).hexdigest() == release['target_COMMON_sha256']
    assert sha256(new_files[crew.stats.stage.ART]).hexdigest() == release['target_PersonInfo_PXL_sha256']
    verify_runtime(new_files[ARM], release)
    scope = coverage(clean, candidate, release)

    replay_path = REPLAY / 'verification.json'
    replay = base.load(replay_path)
    assert replay['candidate_sha256'] == release['candidate_sha256']
    assert replay['full_stat_plaque_masks'] == 36 and replay['complete_skill_row_masks'] == 120
    assert len(replay['cases']) == 6 and len(replay['title_transition_sample_frames']) == 34
    assert all(base.digest(path) == digest for path, digest in replay['evidence'].items())
    assert base.digest(replay['sheet']) == replay['sheet_sha256']
    receipt = dict(candidate=CANDIDATE.as_posix(), candidate_sha256=release['candidate_sha256'],
        manifest=adjacent.as_posix(), manifest_sha256=release['manifest_sha256'],
        registry_sha256=release['registry_sha256'], profile=current.PROFILE,
        patch=current.PATCH.as_posix(), patch_sha256=release['patch_sha256'], clean_sha256=release['clean_input_sha256'],
        byte_exact_reconstruction=True, market_goods_info_and_ascii_right_bounds_verified=True,
        accepted_layers=len(accepted), registered_manifest_entries=len(manifest['batches']),
        passing_release_checks=len(manifest['checks']), repository_tests=release['repository_tests'],
        changed_paths_since_main=changed, main_profile=promoted['profile'], main_sha256=promoted['rom_sha256'],
        user_acceptance_pending=True, hardware_coverage=False)
    for directory in (OUTPUT, current.VERIFY):
        base.save(directory / 'promotion_reconstruction.json', receipt)
    base.save(current.VERIFY / 'editorial_remaining_scope.json', scope)
    copyfile(replay_path, current.VERIFY / 'fernando_deck_replay.json')
    copyfile(replay['sheet'], current.VERIFY / 'fernando_deck_replay.png')
    base.save(current.PACKAGE / 'checksums.json', package_checksums(current.PACKAGE))
    print(f'{CANDIDATE} | {release["candidate_sha256"]} | {scope["completed_reviews"]} reviews, '
          f'{scope["shared_pending"]} mapped shared keys pending | {changed}')


if __name__ == '__main__':
    main()
