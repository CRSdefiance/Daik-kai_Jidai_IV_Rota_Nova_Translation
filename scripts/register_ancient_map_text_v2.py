"""Register the Ancient Map documents and artifact rumors with native wrap proof."""

import argparse
from collections import Counter
from inspect import getsource
from json import dumps, loads
from pathlib import Path
from shutil import copyfile
from types import SimpleNamespace

from dk4tool.dialogue.review import validate_natural_dialogue_batch
from scripts import register_golden_route_exchanges_v1 as predecessor
from scripts import verify_ancient_map_text_v2 as verification
from scripts.prepare_all_routes_promotion_20261111 import package_checksums, verify_runtime
from scripts.source_locked_derivation_v5118 import checked_text


parent, transaction, base = predecessor.parent, predecessor.transaction, predecessor.base
stage = verification.stage
PARENT = stage.parent.RELEASE
PROFILE = 'all-routes-ancient-map-text-editorial-v2-20261111'
FAMILY = 'ancient_map_text_contextual_20261111'
CHECK = 'registered_ancient_map_native_text_and_complete_parent_inverse'
PACKAGE = Path('releases/all_routes_editorial_20261111_ancient_map_text_candidate')
VERIFICATION = PACKAGE / 'verification'
RELEASE = VERIFICATION / 'registered_release_verification.json'
REVIEW = VERIFICATION / 'registered_review.json'
TEST = Path('out/ancient_map_text_registered_20261111_v2')
ROM = TEST / 'Translation_DS_All_Routes_Ancient_Map_20261111_candidate.nds'
MANIFEST = ROM.with_suffix('.manifest.json')
PATCH = PACKAGE / 'translation.xdelta'
DOC = Path('docs/editorial_ancient_map_text_registered_20261111.md')
PENDING_LEDGER = TEST / 'editorial_review_current.ancient_map_text.pending.json'
OUTPUT, EVIDENCE, RESEARCH = verification.OUTPUT, stage.PROOF, stage.ROM
STARTUP_VERIFICATION, CHECKPOINT = verification.BOOT, verification.CHECKPOINT
LIVE_VERIFICATION, QA = verification.LIVE, verification.QA
PREVIOUS_TOTAL, TOTAL, REVISED, RETAINED = 27597, 61, 15, 46


def rebuild(release, evidence, source):
    image = base.NdsImage.open(release['candidate'])
    old_arm, old_common = (image.read_file(path) for path in (stage.ARM, stage.COMMON))
    runtime = SimpleNamespace(arm=old_arm, common=old_common)
    rows = {row['message_ID']: row for row in source['records']}
    assert source['source_manuscript_sha256'] == evidence['manuscript_sha256']
    assert all(base.digest(path) == sha for path, sha in evidence['manuscript_sha256'].items())
    arm, common, storage, entries, allocation = stage.stage(runtime, release, rows)
    assert loads(dumps(allocation)) == evidence['allocation']
    assert evidence['original_runtime_code_preserved'] and evidence['complete_parent_inverse_exact']
    for row in evidence['records']:
        n = row['message_ID']
        assert row['staged_reference'] == stage.prior.document.reference(entries[n])
        assert row['staged_hex'] == storage[n].hex()
    verify_runtime(arm, release)
    image.replace_file(stage.ARM, arm)
    image.replace_file(stage.COMMON, common)
    assert bytes(image.rom.save()) == RESEARCH.read_bytes()
    image.replace_file(stage.ARM, old_arm)
    image.replace_file(stage.COMMON, old_common)
    assert bytes(image.rom.save()) == Path(release['candidate']).read_bytes()
    return arm, common


def verification_scope(approved, live):
    assert approved['live_messages'] == live['observed_ids'] == list(verification.OBSERVED_IDS)
    assert approved['stored_cases'] == TOTAL and approved['viewed_pages'] == 30
    assert live['actual_emulator'] and not live['hardware']
    assert live['original_map_title_marker_buttons_and_returns_exact'] and live['exact_document_ink'] > 0
    assert live['exact_other_framebuffers'] == [9900, 10300, 10700, 11500, 11900]
    return dict(observed_notice_IDs=live['observed_ids'], stored_cases=TOTAL, viewed_pages=30,
        original_map_title_marker_buttons_and_returns_exact=True, actual_emulator=True, hardware=False,
        artifact_rumor_portraits_offline=10, native_document_fields=51, fixture_scope=live['fixture_scope'])


def final_review(source, evidence, scope):
    records = []
    for row, stored in zip(source['records'], evidence['records'], strict=True):
        n = stored['message_ID']
        assert row['id'] == f'COMMON_MESSAGE_{n}' and row['source_reference'] == stored['source_reference']
        assert row['current_reference'] == stored['previous_reference'] and row['original_substitution_count'] == 0
        records.append(row | dict(review=row['review'] | {'formatting': True}, new_credit=1,
            registered_reference=stored['staged_reference'] | {'exact_stored_hex': stored['staged_hex'],
                'ROM_sha256': evidence['research_ROM_sha256']}, native_lines=stored['visible_lines'],
            native_consumer=stored['original_consumer'], gameplay_observed=n in scope['observed_notice_IDs']))
    assert len(records) == TOTAL and Counter(row['decision'] for row in records) == {
        'revision': REVISED, 'retention': RETAINED}
    review = dict(translation_policy='natural-dialogue-v2', target_locale='en-US', encoder='dialogue-relocatable-v1',
        review_gates=['source', 'context', 'localization', 'naturalness', 'formatting'],
        records=records, actual_verification_scope=scope, region_direction_pairs=source['region_direction_pairs'],
        native_fields=source['native_fields'], source_manuscript_sha256=source['source_manuscript_sha256'],
        full_goal_complete=False)
    validate_natural_dialogue_batch(review)
    return review


def publish(release):
    pin_path = Path('translations/rom_retention_pins.json')
    pins = base.load(pin_path)
    for path in (stage.parent.ROM, stage.prior.ROM, RESEARCH, ROM):
        resolved = str(path.resolve())
        assert path.is_file()
        if not any(row['path'] == resolved for row in pins):
            pins.append(dict(path=resolved, reason=f'Preserve the Ancient Map text build. SHA256 {base.digest(path)}'))
    base.replace_checked(pin_path, (dumps(pins, ensure_ascii=False, indent=2) + '\n').replace('\n', '\r\n').encode())
    native = verification.NATIVE
    assert base.digest(native) == base.load(CHECKPOINT)['evidence'][str(native)]
    copyfile(native, VERIFICATION / native.name)
    summary = 'All 61 Ancient Map records are registered. The ledger now credits 27,658 reviews.'
    readme = f"""# All Routes Ancient Map candidate

Use [{ROM.name}](../../{ROM.as_posix()}) with its build manifest. The [clean-input patch](translation.xdelta) reconstructs the ROM byte for byte from Japanese SHA-256 `{release['clean_input_sha256']}`. Candidate SHA-256 `{release['candidate_sha256']}`. Patch SHA-256 `{release['patch_sha256']}`.

{summary} The 15 revisions and 46 justified retentions preserve the 20 region and direction pairs, the independently selected artifact inscriptions and the spoken rumors. All 51 document fields match complete native glyph masks. Twenty complete map previews and ten rumor portraits received visual review. The Old Dagger replay verifies the four clue fields and original navigation using four temporary clue bits in a copied Syracuse save. Cold startup, 24 protected name getters, 34 targeted tests and 111 release checks passed. [Gameplay](verification/{LIVE_VERIFICATION.name}) · [Exact records](verification/registered_review.json)
"""
    (PACKAGE / 'README.md').write_text(readme, encoding='utf-8', newline='\n')
    base.save(PACKAGE / 'checksums.json', package_checksums(PACKAGE))
    doc = f"""# Ancient Map text registered

{summary} COMMON 3607–3667 covers four fields on the Hint screen and ten spoken artifact rumors. The [review ledger](../{REVIEW.as_posix()}) binds the clean source, prior English, individual decisions and all five gates. The [registered ROM and clean-input patch](../{PACKAGE.as_posix()}/README.md) preserve the Market and ASCII right-bound fixes and all 114 accepted layers.

The static painter pairs ASCII glyphs across LF. The formatter inserts an invisible empty cell at the end of an odd nonfinal row. The 36-cell text column, logical prose, original line pitch and runtime code stay intact. The native verification reproduces the prior “driveo” migration from exact old bytes and verifies every corrected map field against an independent complete glyph plane. The focused Old Dagger replay verified the map, title, marker, clue text and both returns to the previous screens. Other map variants and all rumor portraits were checked offline.

318 native shared keys remain to review or classify. The Y button's Japanese Hint label has separate display ownership to establish. Continue with the music, Online and scene-label consumers and the legacy menu keys. Other player-facing UI, speaker labels, earlier wraps and glyphs, and representative town and random-scene testing remain in scope. Deferred artwork and the older-record technical re-audit remain separate.
"""
    base.replace_checked(DOC, doc.encode('utf-8'))
    lead = f'# Current editorial checkpoint - 2026-11-11\n\n{summary}\n\nContinue from [the registered Ancient Map text]({DOC.name}).\n\n'
    for name in ('editorial_handoff_current.md', 'editorial_efficiency_workflow.md', 'translation_progress.md'):
        path = Path('docs') / name
        base.replace_checked(path, lead.encode('utf-8') + path.read_bytes())
    continuity = Path('docs/build_continuity_protocol.md')
    protocol = ('Ancient Map text is registered with 776 entries, 114 accepted layers and 111 checks. '
                'Use scripts/register_ancient_map_text_v2.py with --register and --publish-prepared. '
                f'Exact patch, native masks, Old Dagger and startup pass. [Checkpoint]({DOC.name})\n\n')
    base.replace_checked(continuity, protocol.encode('utf-8') + continuity.read_bytes())
    print('Registered 776 entries and credited the 61 Ancient Map records once.')


def environment():
    return predecessor.environment() | globals()


def register():
    source = checked_text(getsource(parent.register), {
        'price-info-trade-good-descriptions': 'ancient-map-text',
        'All 124 Price Info trade-good descriptions are registered.': 'All 61 Ancient Map records are registered.',
        "'== 27093'": "'== 27658'", "'== 16230'": "'== 16587'", "'== 10863'": "'== 11071'",
        "== 763 and len(manifest['checks']) == 98": "== 775 and len(manifest['checks']) == 110",
        "== 764 and len(manifest['checks']) == 99": "== 776 and len(manifest['checks']) == 111",
        'registered_manifest_entries=764, accepted_layers=114, passing_release_checks=99':
            'registered_manifest_entries=776, accepted_layers=114, passing_release_checks=111',
        'verified_proof_and_relic_advice_predecessor=predecessor, trade_good_descriptions_release=str(REVIEW)':
            'verified_arrival_month_labels_predecessor=predecessor, ancient_map_text_release=str(REVIEW)',
        'Reviewed the native Price Info descriptions with word wrapping and pagination.':
            'Reviewed Ancient Map documents and rumors with the original painter and bounded word wraps.',
        'release_stack_before_trade_good_descriptions': 'release_stack_before_ancient_map_text',
        'release_stack.trade_good_descriptions.pending': 'release_stack.ancient_map_text.pending',
        'COMMON_PRICE_INFO_DESCRIPTION_DIRECTORY_AND_POINTERS': 'COMMON_ANCIENT_MAP_TEXT_DIRECTORY_AND_POINTERS',
        'trade_good_descriptions_registered_successor_pipeline': 'ancient_map_text_registered_successor_pipeline',
        'Price Info registration staged and ready to publish.': 'Ancient Map registration staged and ready to publish.',
    })
    env = environment()
    exec(compile(source, __file__ + '::registered-ancient-map', 'exec'), env)
    env['register']()


def publish_prepared():
    source = checked_text(getsource(parent.publish_prepared), {
        'release_stack.trade_good_descriptions.pending': 'release_stack.ancient_map_text.pending',
    })
    env = environment()
    exec(compile(source, __file__ + '::atomic-publication', 'exec'), env)
    env['publish_prepared']()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    action = parser.add_mutually_exclusive_group(required=True)
    action.add_argument('--register', action='store_true')
    action.add_argument('--publish-prepared', action='store_true')
    (publish_prepared if parser.parse_args().publish_prepared else register)()
