"""Reconstruct the cumulative test ROM and audit remaining editorial coverage."""

from collections import Counter
import filecmp
import gzip
from hashlib import sha256
from json import dumps, loads
from pathlib import Path
from shutil import copyfile
from struct import unpack_from

from ndspy.code import MainCodeFile

from dk4tool.patch.duel_editorial import owned_entries
from dk4tool.patch.market_goods_info_terminator_v1 import BASE, FIELDS, NEW_FORMAT, PAYLOAD
from dk4tool.patch.xdelta import apply_xdelta
from dk4tool.rom.nds import NdsImage
from dk4tool.script.common_message_table import DIRECTORY_OFFSET, TABLE_OFFSET, common_message_entries
from scripts.audit_item_advice_promotion_scope_v1 import (
    ARM, COMMON, HELP, JAPANESE, SOURCE_PACKET, check_story,
)
from scripts import register_sailing_reactions_v1 as current
from scripts.verify_release_baseline import REQUIRED_MENU_TEXT, REQUIRED_OPTIONS_TEXT, files


base = current.base
read, digest, save = base.load, base.digest, base.save
NAMES = ('figurehead_navigation_gift_advice', 'proof_and_relic_advice', 'trade_good_descriptions',
         'sailing_reactions')
PROMOTION = Path('out/promotion_ready_20261111_trade_and_sailing')
ROM = PROMOTION / 'Translation_DS_All_Routes_Trade_and_Sailing_20261111_candidate.nds'
ADJACENT = ROM.with_suffix('.manifest.json')
VERIFICATION = current.VERIFICATION


def package_checksums(package):
    return {path.relative_to(package).as_posix(): digest(path) for path in sorted(package.rglob('*'))
            if path.is_file() and path.name != 'checksums.json'}


def checked_release_chain():
    previous = None
    checksums = {}
    for index, name in enumerate(NAMES):
        package = Path('releases') / f'all_routes_editorial_20261111_{name}_candidate'
        inventory = package_checksums(package)
        assert inventory == read(package / 'checksums.json')
        checksums[package.as_posix()] = len(inventory)
        release = read(package / 'verification/registered_release_verification.json')
        manifest_raw = gzip.decompress((package / 'build_manifest.json.gz').read_bytes())
        registry_raw = gzip.decompress((package / 'build_release_stack.json.gz').read_bytes())
        assert sha256(manifest_raw).hexdigest() == release['manifest_sha256']
        assert sha256(registry_raw).hexdigest() == release['registry_sha256']
        manifest, registry = loads(manifest_raw), loads(registry_raw)
        assert manifest['candidate_sha256'] == release['candidate_sha256']
        assert len(manifest['batches']) == release['registered_manifest_entries'] == 762 + index
        assert len(manifest['checks']) == release['passing_release_checks'] == 97 + index
        assert all(result is True for result in manifest['checks'].values())
        if previous:
            old_manifest, old_registry = previous
            assert manifest['batches'][:-1] == old_manifest['batches']
            assert manifest['checks'] | old_manifest['checks'] == manifest['checks']
            assert release['predecessor']['candidate_sha256'] == old_manifest['candidate_sha256']
            for key in ('canonical_baseline', 'accepted_layers'):
                assert registry[key] == old_registry[key]
            assert registry['profiles'] | old_registry['profiles'] == registry['profiles']
        else:
            first_release = release
        previous = manifest, registry
    return first_release, release, manifest, registry, checksums


def audit_remaining(clean, candidate, ledger, release):
    keys = Counter((row['file_path'], row['id'])
                   for row in ledger[base.CONTEXT]['integrated_record_keys'])
    assert len(keys) == ledger['records_editorially_completed'] == 27146 and set(keys.values()) == {1}
    assert ledger['current_integrated_candidate']['sha256'] == release['candidate_sha256']
    story = check_story(read, digest, clean, keys)
    story_count = sum(row['source_objects'] for row in story)
    assert story_count == 24092
    assert {record for path, record in keys if path == HELP} == {f'HELP_TOPIC_{n}' for n in range(202)}
    source = common_message_entries(clean.read_file(COMMON), clean.read_file(ARM))
    arm = candidate.read_file(ARM)
    latest = owned_entries(candidate.read_file(COMMON), arm, sha256(arm[DIRECTORY_OFFSET:TABLE_OFFSET]).hexdigest())
    assert len(source) == len(latest) == 3668
    assert all(row.message_id == other.message_id == n for n, (row, other) in enumerate(zip(source, latest, strict=True)))
    credited = {record for path, record in keys if path == COMMON}
    assert credited <= {f'COMMON_MESSAGE_{row.message_id}' for row in source}
    pending = [row.message_id for row in source if f'COMMON_MESSAGE_{row.message_id}' not in credited]
    assert len(credited) == 2838 and len(pending) == 830
    assert not set(pending) & (set(range(137, 261)) | set(range(2359, 2366)) | set(range(2454, 2500)))
    pending_japanese = [n for n in pending if JAPANESE.search(latest[n].text.decode('cp932', errors='replace'))]
    return dict(candidate_sha256=release['candidate_sha256'], coverage_ledger=base.LEDGER.as_posix(),
        ledger_sha256=digest(base.LEDGER), completed_reviews=len(keys),
        revised_records=ledger['records_revised_and_integrated'],
        justified_retentions=ledger['retained_wordings_editorially_completed'],
        source_census_packet=SOURCE_PACKET.as_posix(), source_census_packet_sha256=digest(SOURCE_PACKET),
        story_archives=story, typed_story_positions_reviewed=story_count, source_help_topics_credited=202,
        shared_native_COMMON=dict(total=len(source), credited=len(credited), pending=len(pending), pending_ids=pending,
            pending_by_block=dict(sorted(Counter(source[n].block for n in pending).items())),
            pending_with_Japanese_characters_ids=pending_japanese,
            pending_with_Japanese_characters_in_current_storage=len(pending_japanese),
            scope='Includes conditional, legacy and potentially non-player-facing keys. Japanese storage is a lead.'),
        remaining_unquantified='Other player-facing UI prose, retrospective names, roles, wrapping and glyphs, '
                               'and representative town and random-scene coverage.',
        separate_work='Deferred graphics artwork and older-record technical re-audit.',
        whole_game_percent_established=False, full_goal_complete=False)


def verify_runtime(arm, release):
    assert all(text in arm for text in REQUIRED_MENU_TEXT)
    assert any(text in arm for text in REQUIRED_OPTIONS_TEXT)
    sections = {section.ramAddress: section.data for section in MainCodeFile(arm, BASE).sections}
    assert len(sections) == 6 and sections[NEW_FORMAT][:len(PAYLOAD)] == PAYLOAD
    assert all(unpack_from('<I', arm, offset)[0] == NEW_FORMAT for offset in FIELDS)
    assert sections[0x01FFC000][0x6AC:0x6B0] == bytes.fromhex('0c209fe5')
    patches = read(release['right_bound_configuration'])['proof']['patches']
    original_itcm = patches[0]['offset'] - 0x21C
    for patch in patches:
        offset = patch['offset']
        expected = bytes.fromhex(patch['after_hex'])
        if original_itcm <= offset < original_itcm + 4096:
            offset -= original_itcm
            assert sections[0x01FFC000][offset:offset + len(expected)] == expected
        else:
            assert arm[offset:offset + len(expected)] == expected


def main():
    prior, release, manifest, registry, packages = checked_release_chain()
    assert not PROMOTION.exists()
    assert read(base.REGISTRY) == registry and digest(base.REGISTRY) == manifest['release_stack_sha256']
    canonical = registry['canonical_baseline']
    batches = {name.replace('\\', '/') for name in manifest['batches']}
    accepted = registry['accepted_layers']
    assert len(accepted) == release['accepted_layers'] == 114
    assert all(layer['status'] == 'accepted' and (layer.get('baked_into_baseline') is True or
               layer['batch'].replace('\\', '/') in batches) for layer in accepted)
    assert digest(canonical['path']) == canonical['sha256'] == manifest['base_sha256'] == release['canonical_sha256']
    assert manifest['profile'] == release['profile'] == current.PROFILE
    assert registry['profiles'][current.PROFILE]['status'] == 'experimental'
    assert manifest['changed_paths'] and manifest['changed_records']
    assert manifest['checks']['registered_market_goods_info_terminated_format_and_complete_parent_inverse']
    assert manifest['checks']['registered_runtime_bounds_and_complete_parent_target_inverse']
    assert release['clean_input_patch_byte_exact'] and release['whole_parent_inverse_exact']
    assert release['experimental_not_promoted'] and not release['own_registered_startup_pending']
    clean_path = current.stage.CLEAN
    assert digest(clean_path) == release['clean_input_sha256']
    assert digest(current.ROM) == manifest['candidate_sha256'] == release['candidate_sha256']
    assert digest(current.MANIFEST) == release['manifest_sha256']
    assert digest(current.PATCH) == release['patch_sha256']
    boot_path = Path(release['own_registered_startup'])
    assert digest(boot_path) == release['own_registered_startup_sha256']
    boot = read(boot_path)
    assert boot['candidate_sha256'] == release['candidate_sha256']
    assert boot['cold_boot'] and not boot['savestate'] and boot['complete_deployed_payload_exact']
    assert len(boot['original_protected_name_getters']) == release['original_protected_name_getters_count'] == 24
    main_build = read(base.PROMOTED)
    assert main_build['profile'] == 'all-routes-unified-v4701' and main_build['main_build']

    PROMOTION.mkdir()
    apply_xdelta(clean_path, current.PATCH, ROM)
    assert digest(ROM) == release['candidate_sha256'] and filecmp.cmp(ROM, current.ROM, shallow=False)
    copyfile(current.MANIFEST, ADJACENT)
    assert digest(ADJACENT) == release['manifest_sha256']
    clean, candidate = NdsImage.open(clean_path), NdsImage.open(ROM)
    assert digest(prior['candidate']) == prior['candidate_sha256']
    before, after = files(NdsImage.open(prior['candidate'])), files(candidate)
    assert sorted(path for path in before.keys() | after.keys() if before.get(path) != after.get(path)) == [COMMON, ARM]
    assert sha256(after[ARM]).hexdigest() == release['target_ARM9_sha256']
    assert sha256(after[COMMON]).hexdigest() == release['target_COMMON_sha256']
    verify_runtime(after[ARM], release)
    scope = audit_remaining(clean, candidate, read(base.LEDGER), release)
    save(VERIFICATION / 'editorial_remaining_scope.json', scope)
    receipt = dict(candidate=ROM.as_posix(), candidate_sha256=digest(ROM), manifest=ADJACENT.as_posix(),
        manifest_sha256=digest(ADJACENT), registry_sha256=digest(base.REGISTRY),
        release=current.RELEASE.as_posix(), release_sha256=digest(current.RELEASE), profile=current.PROFILE,
        patch=current.PATCH.as_posix(), patch_sha256=digest(current.PATCH), clean_sha256=digest(clean_path),
        verified_package_checksums=packages, accepted_layers=114, release_entries=765, release_checks=100,
        tests=release['repository_tests'], protected_name_getters=24, byte_exact_reconstruction=True,
        previous_candidate_sha256=prior['candidate_sha256'], additional_editorial_records=247,
        changed_paths=[COMMON, ARM], main_profile=main_build['profile'], user_acceptance_pending=True,
        new_hardware_coverage=False)
    for folder in (VERIFICATION, PROMOTION):
        save(folder / 'promotion_reconstruction.json', receipt)

    readme = current.PACKAGE / 'README.md'
    details = readme.read_text(encoding='utf-8').split('\n\n', 2)[2]
    readme.write_text(
        '# All Routes Trade and Sailing promotion candidate\n\n'
        f'Cold-boot the [local candidate ROM](../../{ROM.as_posix()}) with its '
        f'[build manifest](../../{ADJACENT.as_posix()}). The [clean-input patch](translation.xdelta) '
        f'reconstructs the ROM byte for byte from Japanese ROM SHA-256 `{release["clean_input_sha256"]}`. '
        f'Expected ROM SHA-256 `{release["candidate_sha256"]}`. '
        f'Patch SHA-256 `{release["patch_sha256"]}`.\n\n'
        'This build adds 247 reviews since Item Advice, including the last 70 item-advice replies, '
        '124 Price Info descriptions and 53 sailing reactions. It includes Rafael’s tutorials, '
        'the Market Goods Info fix and the ASCII right-bound correction. V4701 remains main pending '
        'cold-boot acceptance. [Reconstruction](verification/promotion_reconstruction.json) · '
        '[Remaining work](verification/editorial_remaining_scope.json)\n\n' + details,
        encoding='utf-8', newline='\n')
    save(current.PACKAGE / 'checksums.json', package_checksums(current.PACKAGE))
    pin_path = Path('translations/rom_retention_pins.json')
    pins = read(pin_path)
    assert not any(Path(pin['path']) == ROM.resolve() for pin in pins)
    pins.append(dict(path=str(ROM.resolve()), reason=f'Preserve promotion test copy. SHA256 {digest(ROM)}'))
    base.replace_checked(pin_path, (dumps(pins, ensure_ascii=False, indent=2) + '\n').replace('\n', '\r\n').encode())
    handoff = Path('docs/editorial_handoff_current.md')
    intro = (f'The [All Routes Trade and Sailing promotion candidate](../{ROM.as_posix()}) is ready for cold-boot testing. '
             f'The [release package and clean-input patch](../{current.PACKAGE.as_posix()}/README.md) reconstruct it '
             'byte for byte. The ledger has 27,146 credited reviews and 830 native shared keys still to review '
             'or classify. V4701 remains main pending acceptance.\n\n')
    marker = b'Continue from [the registered sailing reactions]'
    before = handoff.read_bytes()
    assert before.startswith(b'# Current editorial checkpoint') and before.count(marker) == 1
    base.replace_checked(handoff, before.replace(marker, intro.encode() + marker, 1))
    print(f'{ROM} | {digest(ROM)} | {scope["completed_reviews"]} reviews | 830 shared keys pending')


if __name__ == '__main__':
    main()
