"""Prepare the cumulative question-wrap candidate for user cold-boot testing."""

import filecmp
from gzip import decompress
from hashlib import sha256
from json import dumps, loads
from pathlib import Path
from shutil import copyfile

from dk4tool.patch.xdelta import apply_xdelta
from dk4tool.rom.nds import NdsImage
from scripts import prepare_all_routes_gallery_promotion_20261111 as gallery
from scripts import register_lil_ceramics_wrap_20261111 as ceramics
from scripts import register_story_question_wraps_20261111 as current
from scripts.prepare_all_routes_promotion_20261111 import package_checksums, verify_runtime
from scripts.verify_release_baseline import files


base = current.base
OUTPUT = Path('out/promotion_ready_20261111_question_wraps')
CANDIDATE = OUTPUT / 'Translation_DS_All_Routes_20261111_Wrap_Review_candidate.nds'
MANIFEST = CANDIDATE.with_suffix('.manifest.json')
PINS = Path('translations/rom_retention_pins.json')


def verify_successors():
    _, gallery_release, previous, previous_registry, _ = gallery.check_release_chain()
    for batch, entries, checks in (
        (ceramics, 781, 116),
        (current.prior, 782, 117),
        (current, 783, 118),
    ):
        package = batch.PACKAGE
        assert package_checksums(package) == base.load(package / 'checksums.json')
        release = base.load(batch.RELEASE)
        published = base.load(package / 'release_manifest.json')
        assert published == release | {'user_acceptance_pending': True}
        manifest_raw = decompress((package / 'build_manifest.json.gz').read_bytes())
        registry_raw = decompress((package / 'build_release_stack.json.gz').read_bytes())
        assert sha256(manifest_raw).hexdigest() == release['manifest_sha256'] == base.digest(batch.MANIFEST)
        assert sha256(registry_raw).hexdigest() == release['registry_sha256']
        assert base.digest(batch.PATCH) == release['patch_sha256']
        manifest, registry = loads(manifest_raw), loads(registry_raw)
        for key in ('candidate_sha256', 'profile'):
            assert manifest[key] == release[key]
        assert manifest['release_stack_sha256'] == release['registry_sha256']
        for key in ('candidate_sha256', 'profile'):
            assert release['predecessor'][key] == previous[key]
        assert release['predecessor']['registry_sha256'] == previous['release_stack_sha256']
        assert manifest['batches'][:-1] == previous['batches']
        assert len(manifest['batches']) == release['registered_manifest_entries'] == entries
        assert len(manifest['checks']) == release['passing_release_checks'] == checks
        assert manifest['checks'] | previous['checks'] == manifest['checks']
        assert all(result is True for result in manifest['checks'].values())
        for key in ('canonical_baseline', 'accepted_layers', 'latest_promoted_build'):
            assert registry[key] == previous_registry[key]
        assert registry['profiles'] | previous_registry['profiles'] == registry['profiles']
        assert release['whole_parent_inverse_exact'] and release['clean_input_patch_byte_exact']
        previous, previous_registry = manifest, registry
    return gallery_release, release, manifest, registry


def main():
    gallery_release, release, manifest, registry = verify_successors()
    assert base.digest(base.REGISTRY) == release['registry_sha256']
    assert registry['profiles'][current.PROFILE]['status'] == 'experimental'
    canonical = registry['canonical_baseline']
    assert base.digest(canonical['path']) == canonical['sha256'] == manifest['base_sha256']
    accepted = registry['accepted_layers']
    batches = {path.replace('\\', '/') for path in manifest['batches']}
    assert len(accepted) == release['accepted_layers'] == 114
    assert all(layer['status'] == 'accepted' and (
        layer.get('baked_into_baseline') is True or layer['batch'].replace('\\', '/') in batches
    ) for layer in accepted)
    assert manifest['checks']['registered_market_goods_info_terminated_format_and_complete_parent_inverse']
    assert manifest['checks']['registered_runtime_bounds_and_complete_parent_target_inverse']
    assert base.digest(current.ROM) == release['candidate_sha256']
    assert base.digest(current.parent.CLEAN) == release['clean_input_sha256']
    assert base.digest(gallery_release['candidate']) == gallery_release['candidate_sha256']
    main_build = base.load(base.PROMOTED)
    assert main_build['profile'] == 'all-routes-unified-v4701' and main_build['main_build']
    _, _, _, _, tests = current.verify_inputs()

    OUTPUT.mkdir(exist_ok=True)
    if not CANDIDATE.exists():
        apply_xdelta(current.parent.CLEAN, current.PATCH, CANDIDATE)
    if not MANIFEST.exists():
        copyfile(current.MANIFEST, MANIFEST)
    assert filecmp.cmp(CANDIDATE, current.ROM, shallow=False)
    assert base.digest(CANDIDATE) == release['candidate_sha256']
    assert base.digest(MANIFEST) == release['manifest_sha256']
    candidate = NdsImage.open(CANDIDATE)
    before = files(NdsImage.open(gallery_release['candidate']))
    after = files(candidate)
    assert before.keys() == after.keys()
    changed = sorted(path for path in before if before[path] != after[path])
    assert changed == [f'/data/SC{route}.DK4' for route in range(4)]
    assert sha256(after[gallery.ARM]).hexdigest() == release['target_ARM9_sha256']
    assert sha256(after[gallery.COMMON]).hexdigest() == release['target_COMMON_sha256']
    verify_runtime(after[gallery.ARM], release)

    scope = gallery.coverage(NdsImage.open(current.parent.CLEAN), candidate, release)
    triage = base.load(current.storage.TRIAGE)
    assert triage['candidate_sha256'] == release['candidate_sha256'] and len(triage['records']) == 833
    scope['wrap_triage'] = dict(
        flagged_bodies=len(triage['records']), findings_by_kind=triage['findings_by_kind'],
        triage_sha256=base.digest(current.storage.TRIAGE),
        scope='Heuristic leads in ASCII progressive dialogue, with overlap. Each needs contextual review.',
    )
    receipt = dict(
        candidate=CANDIDATE.as_posix(), candidate_sha256=release['candidate_sha256'],
        manifest=MANIFEST.as_posix(), manifest_sha256=release['manifest_sha256'],
        patch=current.PATCH.as_posix(), patch_sha256=release['patch_sha256'],
        clean_sha256=release['clean_input_sha256'], registry_sha256=release['registry_sha256'],
        byte_exact_reconstruction=True, profile=current.PROFILE, previous_candidate_sha256=gallery_release['candidate_sha256'],
        changed_paths=changed, revised_dialogue_pages_since_previous_candidate=27,
        accepted_layers=len(accepted), registered_manifest_entries=len(manifest['batches']),
        passing_release_checks=len(manifest['checks']), final_layer_targeted_tests=tests,
        market_goods_info_and_ascii_right_bounds_verified=True,
        main_profile=main_build['profile'], user_acceptance_pending=True, hardware_coverage=False,
    )
    for directory in (OUTPUT, current.VERIFICATION):
        base.save(directory / 'promotion_reconstruction.json', receipt)
    base.save(current.VERIFICATION / 'editorial_remaining_scope.json', scope)
    base.save(current.PACKAGE / 'checksums.json', package_checksums(current.PACKAGE))

    pins = base.load(PINS)
    if not any(Path(pin['path']) == CANDIDATE.resolve() for pin in pins):
        pins.append(dict(path=str(CANDIDATE.resolve()),
                         reason=f'Preserve all-routes wrap review test copy. SHA256 {release["candidate_sha256"]}'))
        base.replace_checked(PINS, (dumps(pins, ensure_ascii=False, indent=2) + '\n').replace('\n', '\r\n').encode())
    print(f'{CANDIDATE} | {release["candidate_sha256"]} | 27,697 credited | 279 shared keys and 833 wrap leads open')


if __name__ == '__main__':
    main()
