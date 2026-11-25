"""Register the source-reviewed Golden Route discovery, report and reward text."""

import argparse
from inspect import getsource
import json
from pathlib import Path
from shutil import copyfile
from types import FunctionType, SimpleNamespace

from scripts import register_sailing_hazards_and_dolphins_v1 as predecessor
from scripts import verify_golden_route_exchanges_v3 as verified
from scripts.source_locked_derivation_v5118 import checked_text


parent, transaction, base = predecessor.parent, predecessor.transaction, predecessor.base
stage = verified.stage
verification = SimpleNamespace(VISUAL=verified.VISUAL)
PARENT = predecessor.RELEASE
PROFILE = 'all-routes-golden-route-exchanges-editorial-v1-20261111'
FAMILY = 'golden_route_exchanges_contextual_20261111'
CHECK = 'registered_golden_route_exchanges_native_live_and_complete_parent_inverse'
PACKAGE = Path('releases/all_routes_editorial_20261111_golden_route_exchanges_candidate')
VERIFICATION = PACKAGE / 'verification'
RELEASE = VERIFICATION / 'registered_release_verification.json'
REVIEW = VERIFICATION / 'registered_review.json'
MUTATION_PLAN = VERIFICATION / 'registration_mutation_plan.json'
TEST = Path('out/golden_route_exchanges_registered_20261111_v1')
ROM = TEST / 'Translation_DS_All_Routes_Golden_Route_Exchanges_20261111_candidate.nds'
MANIFEST = ROM.with_suffix('.manifest.json')
PATCH = PACKAGE / 'translation.xdelta'
DOC = Path('docs/editorial_golden_route_exchanges_registered_20261111.md')
PENDING_LEDGER = TEST / 'editorial_review_current.golden_route_exchanges.pending.json'
OUTPUT, EVIDENCE, RESEARCH = stage.OUTPUT, stage.PROOF, stage.ROM
STARTUP_VERIFICATION, CHECKPOINT = verified.BOOT, verified.CHECKPOINT
LIVE_VERIFICATION, QA = verified.LIVE, verified.QA
PREVIOUS_TOTAL, TOTAL, REVISED, RETAINED = 27524, 73, 48, 25


def verification_scope(approved, live):
    ids = live['observed_ids']
    assert approved['live_messages'] == ids == list(verified.HOLDS.values())
    assert approved['stored_cases'] == TOTAL and approved['viewed_pages'] == 117
    assert live['actual_emulator'] and not live['hardware'] and live['original_sale_guild_report_and_reward_terms']
    assert live['repeat_discovery_plural_report_and_payout_offline']
    return dict(observed_notice_IDs=ids, stored_cases=TOTAL, viewed_pages=117,
        actual_emulator_holds=len(live['observations']), original_sale_guild_report_and_reward_terms=True,
        fixture_scope=live['fixture_scope'], repeat_discovery_plural_report_and_payout_offline=True,
        hardware=False)


def publish(release):
    pin_path = Path('translations/rom_retention_pins.json')
    pins = base.load(pin_path)
    for path in (stage.previous.ROM, RESEARCH, ROM):
        resolved = str(path.resolve())
        assert path.is_file() and not any(row['path'] == resolved for row in pins)
        pins.append(dict(path=resolved, reason=f'Preserve the Golden Route exchanges build. SHA256 {base.digest(path)}'))
    payout = verified.payout.OUTPUT
    assert base.digest(payout) == base.load(verified.VISUAL)['evidence'][str(payout)]
    copyfile(payout, VERIFICATION / payout.name)
    summary = 'All 73 Golden Route records are registered. The ledger now credits 27,597 reviews.'
    readme = f"""# All Routes Golden Route Exchanges candidate

Use [{ROM.name}](../../{ROM.as_posix()}) with its build manifest. The [clean-input patch](translation.xdelta) reconstructs the ROM byte for byte from Japanese SHA-256 `{release['clean_input_sha256']}`. Candidate SHA-256 `{release['candidate_sha256']}`. Patch SHA-256 `{release['patch_sha256']}`.

{summary} Forty-eight revisions and 25 justified retentions cover discovery, reporting and payment. The reviews preserve the four captains’ and officers’ voices, the purchase-town and good argument order, and the two-year reward terms.

The focused Lisbon emulator replay exercised the original sale, Guild report and reward explanation after supplying one temporary purchase-cost word. Other variants and the monthly payout received offline checks. All 117 pages, cold boot, 24 protected name getters, 34 targeted tests and 109 release checks passed. [Gameplay](verification/{LIVE_VERIFICATION.name}) · [Payout](verification/{payout.name}) · [Exact records](verification/registered_review.json)
"""
    (PACKAGE / 'README.md').write_text(readme, encoding='utf-8', newline='\n')
    base.save(PACKAGE / 'checksums.json', {p.relative_to(PACKAGE).as_posix(): base.digest(p)
        for p in sorted(PACKAGE.rglob('*')) if p.is_file() and p.name != 'checksums.json'})
    base.replace_checked(pin_path, (json.dumps(pins, ensure_ascii=False, indent=2) + '\n')
        .replace('\n', '\r\n').encode('utf-8'))
    document = f"""# Golden Route exchanges registered

{summary} COMMON 3320–3392 covers the original discovery, reporting and payment sequence. The [review ledger](../{REVIEW.as_posix()}) records the clean source, prior English, individual decisions and all five gates. The [registered ROM and patch](../{PACKAGE.as_posix()}/README.md) preserve the earlier runtime fixes and accepted layers.

The original getters supply the purchase port, trade good and gold in the documented order. The existing portrait amount formatter preserves all digits in the guild dialogue. The speakerless payout uses three native rows to fit the largest tested amount with its gold label. The payout tests cover eligible and ineligible months, reported state, expiry and aggregate amounts.

The separate Golden Route Found screen displayed two apparent percent-string placeholders beside the arrival-month label at frame 21200. Trace that display consumer separately from the reviewed dialogue. The same replay observed Julio’s “First, you’re the captain, Rafael” at frame 17300 with the corrected capital F and wrapping.

379 native shared keys remain to review or classify. The [source range map](editorial_remaining_shared_ranges_20261111.md) identifies the next groups. Other UI prose, earlier wraps and glyphs, names and roles, and representative town and random scenes remain in scope. Deferred artwork and the older-record technical re-audit remain separate.
"""
    base.replace_checked(DOC, document.encode('utf-8'))
    lead = f'# Current editorial checkpoint - 2026-11-11\n\n{summary}\n\nContinue from [the registered Golden Route exchanges]({DOC.name}).\n\n'
    for name in ('editorial_handoff_current.md', 'editorial_efficiency_workflow.md', 'translation_progress.md'):
        path = Path('docs') / name
        base.replace_checked(path, lead.encode('utf-8') + path.read_bytes())
    continuity = Path('docs/build_continuity_protocol.md')
    protocol = ('The 73 Golden Route records are registered with 774 entries, 114 accepted layers and 109 checks. '
                'Use scripts/register_golden_route_exchanges_v1.py with --register and --publish-prepared. '
                f'Exact reconstruction, focused Lisbon replay and cold startup pass. [Checkpoint]({DOC.name})\n\n')
    base.replace_checked(continuity, protocol.encode('utf-8') + continuity.read_bytes())
    print('Registered 774 entries and credited 73 Golden Route records once.')


def environment():
    env = predecessor.environment() | globals()
    for name in ('rebuild', 'final_review'):
        env[name] = FunctionType(env[name].__code__, env)
    return env


def register():
    source = checked_text(getsource(parent.register), {
        'price-info-trade-good-descriptions': 'golden-route-exchanges',
        'All 124 Price Info trade-good descriptions are registered.': 'All 73 Golden Route records are registered.',
        "'== 27093'": "'== 27597'", "'== 16230'": "'== 16572'", "'== 10863'": "'== 11025'",
        "== 763 and len(manifest['checks']) == 98": "== 773 and len(manifest['checks']) == 108",
        "== 764 and len(manifest['checks']) == 99": "== 774 and len(manifest['checks']) == 109",
        'registered_manifest_entries=764, accepted_layers=114, passing_release_checks=99':
            'registered_manifest_entries=774, accepted_layers=114, passing_release_checks=109',
        'verified_proof_and_relic_advice_predecessor=predecessor, trade_good_descriptions_release=str(REVIEW)':
            'verified_sailing_hazards_and_dolphins_predecessor=predecessor, golden_route_exchanges_release=str(REVIEW)',
        'Reviewed the native Price Info descriptions with word wrapping and pagination.':
            'Reviewed Golden Route discovery, Guild reporting and payment with native portraits and modal layout.',
        'release_stack_before_trade_good_descriptions': 'release_stack_before_golden_route_exchanges',
        'release_stack.trade_good_descriptions.pending': 'release_stack.golden_route_exchanges.pending',
        'COMMON_PRICE_INFO_DESCRIPTION_DIRECTORY_AND_POINTERS': 'COMMON_GOLDEN_ROUTE_EXCHANGES_WRAP',
        '"dict(native_directory_and_pointer_updates_only=True, runtime_code_changed=False)"':
            r'''"evidence[\'ownership\']"''',
        'trade_good_descriptions_registered_successor_pipeline': 'golden_route_exchanges_registered_successor_pipeline',
        'Price Info registration staged and ready to publish.': 'Golden Route registration staged and ready to publish.',
    })
    env = environment()
    exec(compile(source, __file__ + '::derive-registration', 'exec'), env)
    env['register']()


def publish_prepared():
    source = checked_text(getsource(parent.publish_prepared), {
        'release_stack.trade_good_descriptions.pending': 'release_stack.golden_route_exchanges.pending',
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
