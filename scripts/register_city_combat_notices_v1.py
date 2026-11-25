"""Register city and combat notices over the verified fleet-report release."""

import argparse
from inspect import getsource
import json
from pathlib import Path
from types import FunctionType, SimpleNamespace

from scripts import register_fleet_reports_v1 as predecessor
from scripts import verify_city_combat_notices_live_v1 as verified
from scripts.source_locked_derivation_v5118 import checked_text


parent, transaction, base = predecessor.parent, predecessor.transaction, predecessor.base
stage = SimpleNamespace(**(vars(verified.stage.first.first) | vars(verified.stage.first) | vars(verified.stage)))
verification = SimpleNamespace(VISUAL=verified.checked.VISUAL)
PARENT = predecessor.RELEASE
PROFILE = 'all-routes-city-combat-notices-editorial-v1-20261111'
FAMILY = 'city_combat_notices_contextual_20261111'
CHECK = 'registered_city_combat_notices_native_live_and_complete_parent_inverse'
PACKAGE = Path('releases/all_routes_editorial_20261111_city_combat_notices_candidate')
VERIFICATION = PACKAGE / 'verification'
RELEASE = VERIFICATION / 'registered_release_verification.json'
REVIEW = VERIFICATION / 'registered_review.json'
MUTATION_PLAN = VERIFICATION / 'registration_mutation_plan.json'
TEST = Path('out/city_combat_notices_registered_20261111_v1')
ROM = TEST / 'Translation_DS_All_Routes_City_Combat_Notices_20261111_candidate.nds'
MANIFEST = ROM.with_suffix('.manifest.json')
PATCH = PACKAGE / 'translation.xdelta'
DOC = Path('docs/editorial_city_combat_notices_registered_20261111.md')
PENDING_LEDGER = TEST / 'editorial_review_current.city_combat_notices.pending.json'
OUTPUT, EVIDENCE, RESEARCH = stage.OUTPUT, stage.PROOF, stage.ROM
STARTUP_VERIFICATION, CHECKPOINT = verified.checked.BOOT, verified.CHECKPOINT
LIVE_VERIFICATION, QA = verified.LIVE, verified.checked.QA
PREVIOUS_TOTAL, TOTAL, REVISED, RETAINED = 27226, 35, 21, 14


def verification_scope(approved, live):
    assert approved['live_messages'] == live['observed_ids'] and live['observed_ids']
    assert set(live['observed_ids']) <= set(range(2580, 2615))
    assert any(2607 <= number <= 2614 for number in live['observed_ids'])
    assert approved['stored_cases'] == TOTAL and approved['viewed_pages'] == 80
    assert live['actual_emulator'] and not live['hardware']
    assert live['original_attack_order_and_report'] and live['original_A_advance_and_return_to_sailing']
    return dict(observed_notice_IDs=live['observed_ids'], stored_cases=TOTAL, viewed_pages=80,
        actual_emulator_holds=len(live['observations']), ordinary_regional_order=True,
        original_A_advance_and_return_to_sailing=True, hardware=False)


def publish(release):
    scope = release['actual_verification_scope']
    ids = ', '.join(str(number) for number in scope['observed_notice_IDs'])
    summary = 'All 35 city and combat notices are registered. The ledger now credits 27,261 reviews.'
    readme = f"""# All Routes City and Combat Notices candidate

Use [{ROM.name}](../../{ROM.as_posix()}) with its adjacent manifest. The [clean-input patch](translation.xdelta) reconstructs it byte for byte from clean Japanese SHA-256 `{release['clean_input_sha256']}`. Candidate SHA-256 `{release['candidate_sha256']}`. Patch SHA-256 `{release['patch_sha256']}`.

{summary} The batch includes 21 revisions and 14 justified retentions. It covers city attacks and surrender, ship losses and captures, and the gold value of spoils. City and ship names stay together in the tested layouts. The spoils amount uses the same scoped digit rendering as the monthly fleet reports.

The original Attack Town order and sailing controls produced the Hamburg report. The live replay observed COMMON {ids} and an original return to sailing. Other variants received offline native checks. All 80 portrait pages received visual review. Cold startup, 24 protected name getters, 34 targeted tests and 103 release checks passed. [Gameplay](verification/{LIVE_VERIFICATION.name}) · [Exact records](verification/registered_review.json)
"""
    (PACKAGE / 'README.md').write_text(readme, encoding='utf-8', newline='\n')
    base.save(PACKAGE / 'checksums.json', {p.relative_to(PACKAGE).as_posix(): base.digest(p)
        for p in sorted(PACKAGE.rglob('*')) if p.is_file() and p.name != 'checksums.json'})
    pin_path = Path('translations/rom_retention_pins.json')
    pins = base.load(pin_path)
    for path in (verified.stage.first.ROM, RESEARCH, ROM):
        resolved = str(path.resolve())
        assert path.is_file() and not any(row['path'] == resolved for row in pins)
        pins.append(dict(path=resolved, reason=f'Preserve the city and combat notice build. SHA256 {base.digest(path)}'))
    base.replace_checked(pin_path, (json.dumps(pins, ensure_ascii=False, indent=2) + '\n')
        .replace('\n', '\r\n').encode('utf-8'))
    document = f"""# City and combat notices registered

{summary} COMMON 2580–2614 covers eight original battle tables. All 35 templates passed the native loader checks. The 80 native portraits preserve the tested city and ship names, including the 18-byte ship-name boundary input, and render the original spoils values in the dialogue font. Nine controls verify the amount conversion and fallback. [Exact records](../{REVIEW.as_posix()}) · [Release and patch](../{PACKAGE.as_posix()}/README.md)

The emulator used the existing regional fleet save and the original controls to order the attack on Hamburg. It observed COMMON {ids} and the return to sailing. The replay adds coverage for those displayed records. Other variants have offline proof.

715 shared native keys remain to review or classify. Continue with the connected pirate notices, outcomes and nearby-port orders at COMMON 2615–2662. At the shared original call at `02077C80`, the first field is the location and the second is the pirate. Current 2627–2628 put the pirate first in their English template. The Hamburg replay also captured the follow-up retreat and nearby-port replies at frames 25100 and 25500. The latter visibly splits “await” inside the word. Verify these exact contexts before assigning credit. Legacy New Game 104–107 and Market 750–752, other UI prose, earlier wraps and glyphs, names and roles, and practical town and random-scene coverage remain in scope. Deferred artwork and the later older-record technical re-audit remain separate.
"""
    base.replace_checked(DOC, document.encode('utf-8'))
    lead = f'# Current editorial checkpoint - 2026-11-11\n\n{summary}\n\nContinue from [the registered city and combat notices]({DOC.name}).\n\n'
    for name in ('editorial_handoff_current.md', 'editorial_efficiency_workflow.md', 'translation_progress.md'):
        path = Path('docs') / name
        base.replace_checked(path, lead.encode('utf-8') + path.read_bytes())
    continuity = Path('docs/build_continuity_protocol.md')
    protocol = ('The 35 city and combat notices are registered with 768 entries, 114 accepted layers and 103 checks. '
                'Use scripts/register_city_combat_notices_v1.py with --register and --publish-prepared. '
                f'Exact reconstruction, original regional attack replay and cold startup pass. [Checkpoint]({DOC.name})\n\n')
    base.replace_checked(continuity, protocol.encode('utf-8') + continuity.read_bytes())
    print('Registered 768 entries and credited 35 city and combat notices once.')


def environment():
    env = predecessor.environment() | globals()
    for function in (predecessor.rebuild, predecessor.final_review):
        env[function.__name__] = FunctionType(function.__code__, env)
    return env


def register():
    source = checked_text(getsource(parent.register), {
        'price-info-trade-good-descriptions': 'city-combat-notices',
        'All 124 Price Info trade-good descriptions are registered.': 'All 35 city and combat notices are registered.',
        "'== 27093'": "'== 27261'", "'== 16230'": "'== 16351'", "'== 10863'": "'== 10910'",
        "== 763 and len(manifest['checks']) == 98": "== 767 and len(manifest['checks']) == 102",
        "== 764 and len(manifest['checks']) == 99": "== 768 and len(manifest['checks']) == 103",
        'registered_manifest_entries=764, accepted_layers=114, passing_release_checks=99':
            'registered_manifest_entries=768, accepted_layers=114, passing_release_checks=103',
        'verified_proof_and_relic_advice_predecessor=predecessor, trade_good_descriptions_release=str(REVIEW)':
            'verified_fleet_reports_predecessor=predecessor, city_combat_notices_release=str(REVIEW)',
        'Reviewed the native Price Info descriptions with word wrapping and pagination.':
            'Reviewed city and combat notices with native name and amount rendering.',
        'release_stack_before_trade_good_descriptions': 'release_stack_before_city_combat_notices',
        'release_stack.trade_good_descriptions.pending': 'release_stack.city_combat_notices.pending',
        'COMMON_PRICE_INFO_DESCRIPTION_DIRECTORY_AND_POINTERS': 'COMMON_CITY_COMBAT_NOTICES_WRAP_AND_AMOUNT_GLYPHS',
        '"dict(native_directory_and_pointer_updates_only=True, runtime_code_changed=False)"':
            r'''"evidence[\'ownership\']"''',
        'trade_good_descriptions_registered_successor_pipeline': 'city_combat_notices_registered_successor_pipeline',
        'Price Info registration staged and ready to publish.': 'City and combat registration staged and ready to publish.',
    })
    env = environment()
    exec(compile(source, __file__ + '::derive-registration', 'exec'), env)
    env['register']()


def publish_prepared():
    source = checked_text(getsource(parent.publish_prepared), {
        'release_stack.trade_good_descriptions.pending': 'release_stack.city_combat_notices.pending',
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
