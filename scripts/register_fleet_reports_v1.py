"""Register fleet encounter, outcome and finance reports over the item-action release."""

import argparse
from collections import Counter
from inspect import getsource
import json
from pathlib import Path
from types import SimpleNamespace

from dk4tool.dialogue.review import validate_natural_dialogue_batch
from dk4tool.rom.nds import NdsImage
from scripts import register_crew_item_actions_v1 as predecessor
from scripts import verify_fleet_reports_live_v1 as verified
from scripts.source_locked_derivation_v5118 import checked_text


parent, transaction, base = predecessor.parent, predecessor.transaction, predecessor.base
stage = SimpleNamespace(**verified.stage.stage_environment())
verification = SimpleNamespace(VISUAL=verified.checked.VISUAL)
PARENT = predecessor.RELEASE
PROFILE = 'all-routes-fleet-reports-editorial-v1-20261111'
FAMILY = 'fleet_reports_contextual_20261111'
CHECK = 'registered_fleet_reports_native_live_and_complete_parent_inverse'
PACKAGE = Path('releases/all_routes_editorial_20261111_fleet_reports_candidate')
VERIFICATION = PACKAGE / 'verification'
RELEASE = VERIFICATION / 'registered_release_verification.json'
REVIEW = VERIFICATION / 'registered_review.json'
MUTATION_PLAN = VERIFICATION / 'registration_mutation_plan.json'
TEST = Path('out/fleet_reports_registered_20261111_v1')
ROM = TEST / 'Translation_DS_All_Routes_Fleet_Reports_20261111_candidate.nds'
MANIFEST = ROM.with_suffix('.manifest.json')
PATCH = PACKAGE / 'translation.xdelta'
DOC = Path('docs/editorial_fleet_reports_registered_20261111.md')
PENDING_LEDGER = TEST / 'editorial_review_current.fleet_reports.pending.json'
OUTPUT, EVIDENCE, RESEARCH = stage.OUTPUT, stage.PROOF, stage.ROM
STARTUP_VERIFICATION, CHECKPOINT = verified.checked.BOOT, verified.CHECKPOINT
LIVE_VERIFICATION, QA = verified.LIVE, verified.checked.QA
PREVIOUS_TOTAL, TOTAL, REVISED, RETAINED = 27179, 47, 41, 6


def rebuild(parent_release, evidence, draft):
    image = NdsImage.open(parent_release['candidate'])
    old_arm, old_common = image.read_file(stage.ARM), image.read_file(stage.COMMON)
    rows = {row['message_ID']: row for row in draft['records']}
    arm, common, storage, rebound, allocation, ownership = stage.stage(
        SimpleNamespace(arm=old_arm, common=old_common), parent_release, rows, draft['native_context'], verified=evidence)
    assert json.loads(json.dumps(allocation)) == evidence['allocation']
    assert json.loads(json.dumps(ownership)) == evidence['ownership']
    assert evidence['parent_inverse_exact'] and len(evidence['records']) == TOTAL
    for case in evidence['records']:
        number = case['message_ID']
        assert case['staged_reference'] == verified.base.reference(rebound[number])
        assert storage[number].hex() == case['staged_hex']
    image.replace_file(stage.ARM, arm)
    image.replace_file(stage.COMMON, common)
    assert bytes(image.rom.save()) == RESEARCH.read_bytes()
    image.replace_file(stage.ARM, old_arm)
    image.replace_file(stage.COMMON, old_common)
    assert bytes(image.rom.save()) == Path(parent_release['candidate']).read_bytes()
    return arm, common


def verification_scope(approved, live):
    assert approved['live_messages'] == live['observed_ids'] == [2565, 2575]
    assert approved['stored_cases'] == TOTAL and approved['viewed_pages'] == 89
    assert live['actual_emulator'] and not live['hardware'] and live['ordinary_loss_and_deduction']
    assert live['focused_shortfall_and_carried_balance'] and live['original_A_advance_and_return_to_sailing']
    return dict(observed_notice_IDs=live['observed_ids'], stored_cases=TOTAL, viewed_pages=89,
        actual_emulator_holds=3, ordinary_loss=691, focused_carryover=591,
        fixture_scope='One company funds field in the shortfall replay', original_A_advance_and_return_to_sailing=True,
        fleet_encounter_and_outcome_variants_offline=True, hardware=False)


def final_review(draft, evidence, scope):
    records = []
    for row, case in zip(draft['records'], evidence['records'], strict=True):
        number = case['message_ID']
        assert row['id'] == f'COMMON_MESSAGE_{number}' and row['message_ID'] == number
        assert case['source_reference'] == row['source_reference'] and case['previous_reference'] == row['current_reference']
        records.append(row | dict(review=row['review'] | {'formatting': True}, new_credit=1,
            registered_reference=case['staged_reference'] | {'exact_stored_hex': case['staged_hex'],
                'ROM_sha256': evidence['research_ROM_sha256']},
            native_displays=case['displays'], gameplay_observed=number in scope['observed_notice_IDs']))
    assert len(records) == TOTAL and Counter(row['decision'] for row in records) == {
        'revision': REVISED, 'retention': RETAINED}
    result = dict(translation_policy='natural-dialogue-v2', target_locale='en-US', encoder='dialogue-relocatable-v1',
        review_gates=['source', 'context', 'localization', 'naturalness', 'formatting'], records=records,
        native_context=draft['native_context'], actual_verification_scope=scope, full_goal_complete=False)
    validate_natural_dialogue_batch(result)
    return result


def publish(release):
    summary = 'All 47 fleet reports are registered. The ledger now credits 27,226 reviews.'
    readme = f"""# All Routes Fleet Reports candidate

Use [{ROM.name}](../../{ROM.as_posix()}) with its adjacent manifest. The [clean-input patch](translation.xdelta) reconstructs it byte for byte from clean Japanese SHA-256 `{release['clean_input_sha256']}`. Candidate SHA-256 `{release['candidate_sha256']}`. Patch SHA-256 `{release['patch_sha256']}`.

{summary} The batch includes 41 revisions and six justified retentions across fleet encounters, combat outcomes and monthly finance. The native wrappers keep the company and captain names intact in the tested variants. The two amount paths display matching ASCII digits while preserving the exact values supplied by the game.

The original month-end sequence displayed a loss of 691 gold. A second replay supplied 100 in company funds and verified that the original settlement carried the unpaid 591 forward. Both replays returned to sailing through the original controls. Fleet encounter and combat outcome variants received offline checks. All 89 portrait pages received visual review. Cold startup, 24 protected name getters, 34 targeted tests and 102 release checks passed. [Gameplay](verification/{LIVE_VERIFICATION.name}) · [Exact records](verification/registered_review.json)
"""
    (PACKAGE / 'README.md').write_text(readme, encoding='utf-8', newline='\n')
    base.save(PACKAGE / 'checksums.json', {p.relative_to(PACKAGE).as_posix(): base.digest(p)
        for p in sorted(PACKAGE.rglob('*')) if p.is_file() and p.name != 'checksums.json'})
    pin_path = Path('translations/rom_retention_pins.json')
    pins = base.load(pin_path)
    for path in (verified.stage.first.ROM, RESEARCH, ROM):
        resolved = str(path.resolve())
        assert path.is_file() and not any(row['path'] == resolved for row in pins)
        pins.append(dict(path=resolved, reason=f'Preserve the fleet-report build. SHA256 {base.digest(path)}'))
    base.replace_checked(pin_path, (json.dumps(pins, ensure_ascii=False, indent=2) + '\n')
        .replace('\n', '\r\n').encode('utf-8'))
    document = f"""# Fleet reports registered

{summary} COMMON 2533–2579 covers nine original tables and caller sites. All 47 templates passed the original loader checks. The 89 native portrait cases check both name fields, company labels, zero, one and the largest signed gold amount. The two finance tables use a bounded copy of the expanded text to display narrow digits. Fifteen scoped controls confirmed fallback for other text and selectors. [Exact records](../{REVIEW.as_posix()}) · [Release and patch](../{PACKAGE.as_posix()}/README.md)

The original month-end prompt, loss report and return to sailing ran without a new fixture. The second replay changed one company funds field to reach the shortfall branch. It verified the 591-gold carryover, warning and return. Fleet encounter and outcome dialogue received offline native and visual checks.

750 shared native keys remain to review or classify. Continue from COMMON 2580 with city surrender and bombardment, then the combat notices. Bind city and ship name substitutions to their actual callers and reuse the relevant native proofs. Legacy New Game 104–107 and Market 750–752 still need consumer classification. Other UI prose, earlier wraps and glyphs, names and roles, and practical town and random-scene coverage remain in scope. Deferred artwork and the later older-record technical re-audit remain separate.
"""
    base.replace_checked(DOC, document.encode('utf-8'))
    lead = f'# Current editorial checkpoint - 2026-11-11\n\n{summary}\n\nContinue from [the registered fleet reports]({DOC.name}).\n\n'
    for name in ('editorial_handoff_current.md', 'editorial_efficiency_workflow.md', 'translation_progress.md'):
        path = Path('docs') / name
        base.replace_checked(path, lead.encode('utf-8') + path.read_bytes())
    continuity = Path('docs/build_continuity_protocol.md')
    protocol = ('The 47 fleet reports are registered with 767 entries, 114 accepted layers and 102 checks. '
                'Use scripts/register_fleet_reports_v1.py with --register and --publish-prepared. '
                f'Exact reconstruction, original month-end transitions and cold startup pass. [Checkpoint]({DOC.name})\n\n')
    base.replace_checked(continuity, protocol.encode('utf-8') + continuity.read_bytes())
    print('Registered 767 entries and credited 47 fleet reports once.')


def environment():
    return vars(transaction) | vars(parent) | globals()


def register():
    source = checked_text(getsource(parent.register), {
        'price-info-trade-good-descriptions': 'fleet-reports',
        'All 124 Price Info trade-good descriptions are registered.': 'All 47 fleet reports are registered.',
        "'== 27093'": "'== 27226'", "'== 16230'": "'== 16330'", "'== 10863'": "'== 10896'",
        "== 763 and len(manifest['checks']) == 98": "== 766 and len(manifest['checks']) == 101",
        "== 764 and len(manifest['checks']) == 99": "== 767 and len(manifest['checks']) == 102",
        'registered_manifest_entries=764, accepted_layers=114, passing_release_checks=99':
            'registered_manifest_entries=767, accepted_layers=114, passing_release_checks=102',
        'verified_proof_and_relic_advice_predecessor=predecessor, trade_good_descriptions_release=str(REVIEW)':
            'verified_crew_item_actions_predecessor=predecessor, fleet_reports_release=str(REVIEW)',
        'Reviewed the native Price Info descriptions with word wrapping and pagination.':
            'Reviewed fleet reports with scoped native wrapping and amount glyphs.',
        'release_stack_before_trade_good_descriptions': 'release_stack_before_fleet_reports',
        'release_stack.trade_good_descriptions.pending': 'release_stack.fleet_reports.pending',
        'COMMON_PRICE_INFO_DESCRIPTION_DIRECTORY_AND_POINTERS': 'COMMON_FLEET_REPORTS_WRAP_AND_AMOUNT_GLYPHS',
        '"dict(native_directory_and_pointer_updates_only=True, runtime_code_changed=False)"':
            r'''"evidence[\'ownership\']"''',
        'trade_good_descriptions_registered_successor_pipeline': 'fleet_reports_registered_successor_pipeline',
        'Price Info registration staged and ready to publish.': 'Fleet report registration staged and ready to publish.',
    })
    env = environment()
    exec(compile(source, __file__ + '::derive-registration', 'exec'), env)
    env['register']()


def publish_prepared():
    source = checked_text(getsource(parent.publish_prepared), {
        'release_stack.trade_good_descriptions.pending': 'release_stack.fleet_reports.pending',
    })
    env = environment()
    exec(compile(source, __file__ + '::derive-publication', 'exec'), env)
    env['publish_prepared']()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    action = parser.add_mutually_exclusive_group(required=True)
    action.add_argument('--register', action='store_true')
    action.add_argument('--publish-prepared', action='store_true')
    (publish_prepared if parser.parse_args().publish_prepared else register)()
