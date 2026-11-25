"""Register the oasis, discovery, shark and white-whale exchanges."""

import argparse
from inspect import getsource
import json
from pathlib import Path
from types import FunctionType, SimpleNamespace

from scripts import register_crew_and_shore_reports_v1 as predecessor
from scripts import verify_oasis_and_whale_reports_v1 as verified
from scripts.source_locked_derivation_v5118 import checked_text


parent, transaction, base = predecessor.parent, predecessor.transaction, predecessor.base
v1 = verified.replay.candidate
stage = SimpleNamespace(**(vars(v1.first) | vars(v1)))
verification = SimpleNamespace(VISUAL=verified.VISUAL)
PARENT = predecessor.RELEASE
PROFILE = 'all-routes-oasis-and-whale-reports-editorial-v1-20261111'
FAMILY = 'oasis_and_whale_reports_contextual_20261111'
CHECK = 'registered_oasis_and_whale_reports_native_live_and_complete_parent_inverse'
PACKAGE = Path('releases/all_routes_editorial_20261111_oasis_and_whale_reports_candidate')
VERIFICATION = PACKAGE / 'verification'
RELEASE = VERIFICATION / 'registered_release_verification.json'
REVIEW = VERIFICATION / 'registered_review.json'
MUTATION_PLAN = VERIFICATION / 'registration_mutation_plan.json'
TEST = Path('out/oasis_and_whale_reports_registered_20261111_v1')
ROM = TEST / 'Translation_DS_All_Routes_Oasis_and_Whale_Reports_20261111_candidate.nds'
MANIFEST = ROM.with_suffix('.manifest.json')
PATCH = PACKAGE / 'translation.xdelta'
DOC = Path('docs/editorial_oasis_and_whale_reports_registered_20261111.md')
PENDING_LEDGER = TEST / 'editorial_review_current.oasis_and_whale_reports.pending.json'
OUTPUT, EVIDENCE, RESEARCH = stage.OUTPUT, stage.PROOF, stage.ROM
STARTUP_VERIFICATION, CHECKPOINT = verified.BOOT, verified.CHECKPOINT
LIVE_VERIFICATION, QA = verified.LIVE, verified.QA
PREVIOUS_TOTAL, TOTAL, REVISED, RETAINED = 27394, 71, 51, 20


def verification_scope(approved, live):
    ids = live['observed_ids']
    assert approved['live_messages'] == ids == [2351, 2352]
    assert approved['stored_cases'] == TOTAL and approved['viewed_pages'] == 125
    assert live['actual_emulator'] and not live['hardware'] and live['original_item_follow_up_and_return']
    assert live['oasis_proof_shark_and_other_whale_alternatives_offline']
    return dict(observed_notice_IDs=ids, stored_cases=TOTAL, viewed_pages=125,
        actual_emulator_holds=len(live['observations']), original_item_follow_up_and_return=True,
        fixture_scope=live['fixture_scope'], oasis_proof_shark_and_other_whale_alternatives_offline=True,
        hardware=False)


def publish(release):
    summary = 'All 71 oasis, discovery, shark and white-whale reports are registered. The ledger now credits 27,465 reviews.'
    readme = f"""# All Routes Oasis and Whale Reports candidate

Use [{ROM.name}](../../{ROM.as_posix()}) with its build manifest. The [clean-input patch](translation.xdelta) reconstructs the ROM byte for byte from Japanese SHA-256 `{release['clean_input_sha256']}`. Candidate SHA-256 `{release['candidate_sha256']}`. Patch SHA-256 `{release['patch_sha256']}`.

{summary} The batch includes 51 revisions and 20 justified retentions. The original Proof reports now display full region names and preserve the matching artifact names. Shark reports refer to the equipped figurehead. The whale reports preserve each speaker’s certainty, urgency and reaction to its escape.

All 125 pages received native and visual review. The focused emulator replays observed the whale warning, escape, item presentation, sympathy and return to sailing. The oasis, Proof, shark and other whale alternatives received offline checks. Cold boot, 24 protected name getters, 34 targeted tests and 107 release checks passed. [Gameplay](verification/{LIVE_VERIFICATION.name}) · [Exact records](verification/registered_review.json)
"""
    (PACKAGE / 'README.md').write_text(readme, encoding='utf-8', newline='\n')
    base.save(PACKAGE / 'checksums.json', {p.relative_to(PACKAGE).as_posix(): base.digest(p)
        for p in sorted(PACKAGE.rglob('*')) if p.is_file() and p.name != 'checksums.json'})
    pin_path = Path('translations/rom_retention_pins.json')
    pins = base.load(pin_path)
    for path in (RESEARCH, ROM):
        resolved = str(path.resolve())
        assert path.is_file() and not any(row['path'] == resolved for row in pins)
        pins.append(dict(path=resolved, reason=f'Preserve the oasis and whale report build. SHA256 {base.digest(path)}'))
    base.replace_checked(pin_path, (json.dumps(pins, ensure_ascii=False, indent=2) + '\n')
        .replace('\n', '\r\n').encode('utf-8'))
    document = f"""# Oasis and whale reports registered

{summary} COMMON 2288–2358 covers ten native tables. The [review ledger](../{REVIEW.as_posix()}) records exact Japanese and prior English, context, individual decisions and all five gates. Fourteen linked whale records keep their previous credit. The [registered ROM and patch](../{PACKAGE.as_posix()}/README.md) preserve the previous accepted layers and runtime fixes.

The original Proof report caller now requests the registered full dialogue region name while retaining the matching item-name getter. The compact selector reuses the registered break guard and leaves previous selector behavior in place. Offline checks exercised all seven original region and artifact pairs and both ends of the figurehead width range. The emulator replay observed COMMON 2351 and 2352 with a disclosed condition setup, plus the original item presentation and sympathy follow-up before the return to sailing.

511 native shared keys remain to review or classify. Continue with the connected reports at COMMON 2366–2424. Legacy New Game 104–107, Market 750–752, other player-facing prose, earlier wraps and glyphs, names and roles, and practical town and random-scene coverage remain in scope. Deferred artwork and the later older-record technical re-audit remain separate.
"""
    base.replace_checked(DOC, document.encode('utf-8'))
    lead = f'# Current editorial checkpoint - 2026-11-11\n\n{summary}\n\nContinue from [the registered oasis and whale reports]({DOC.name}).\n\n'
    for name in ('editorial_handoff_current.md', 'editorial_efficiency_workflow.md', 'translation_progress.md'):
        path = Path('docs') / name
        base.replace_checked(path, lead.encode('utf-8') + path.read_bytes())
    continuity = Path('docs/build_continuity_protocol.md')
    protocol = ('The 71 oasis and whale reports are registered with 772 entries, 114 accepted layers and 107 checks. '
                'Use scripts/register_oasis_and_whale_reports_v1.py with --register and --publish-prepared. '
                f'Exact reconstruction, the whale replays and cold startup pass. [Checkpoint]({DOC.name})\n\n')
    base.replace_checked(continuity, protocol.encode('utf-8') + continuity.read_bytes())
    print('Registered 772 entries and credited 71 oasis and whale reports once.')


def environment():
    env = predecessor.environment() | globals()
    for name in ('rebuild', 'final_review'):
        env[name] = FunctionType(env[name].__code__, env)
    return env


def register():
    source = checked_text(getsource(parent.register), {
        'price-info-trade-good-descriptions': 'oasis-and-whale-reports',
        'All 124 Price Info trade-good descriptions are registered.':
            'All 71 oasis, discovery, shark and white-whale reports are registered.',
        "'== 27093'": "'== 27465'", "'== 16230'": "'== 16487'", "'== 10863'": "'== 10978'",
        "== 763 and len(manifest['checks']) == 98": "== 771 and len(manifest['checks']) == 106",
        "== 764 and len(manifest['checks']) == 99": "== 772 and len(manifest['checks']) == 107",
        'registered_manifest_entries=764, accepted_layers=114, passing_release_checks=99':
            'registered_manifest_entries=772, accepted_layers=114, passing_release_checks=107',
        'verified_proof_and_relic_advice_predecessor=predecessor, trade_good_descriptions_release=str(REVIEW)':
            'verified_crew_and_shore_reports_predecessor=predecessor, oasis_and_whale_reports_release=str(REVIEW)',
        'Reviewed the native Price Info descriptions with word wrapping and pagination.':
            'Reviewed oasis, Proof, shark and whale reports with native portrait wrapping.',
        'release_stack_before_trade_good_descriptions': 'release_stack_before_oasis_and_whale_reports',
        'release_stack.trade_good_descriptions.pending': 'release_stack.oasis_and_whale_reports.pending',
        'COMMON_PRICE_INFO_DESCRIPTION_DIRECTORY_AND_POINTERS': 'COMMON_OASIS_AND_WHALE_REPORTS_WRAP_AND_PROOF_REGION',
        '"dict(native_directory_and_pointer_updates_only=True, runtime_code_changed=False)"':
            r'''"evidence[\'ownership\']"''',
        'trade_good_descriptions_registered_successor_pipeline': 'oasis_and_whale_reports_registered_successor_pipeline',
        'Price Info registration staged and ready to publish.': 'Oasis and whale report registration staged and ready to publish.',
    })
    env = environment()
    exec(compile(source, __file__ + '::derive-registration', 'exec'), env)
    env['register']()


def publish_prepared():
    source = checked_text(getsource(parent.publish_prepared), {
        'release_stack.trade_good_descriptions.pending': 'release_stack.oasis_and_whale_reports.pending',
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
