"""Register the dolphin log exchange and sailing hazard portraits."""

import argparse
from inspect import getsource
import json
from pathlib import Path
from types import FunctionType, SimpleNamespace

from scripts import register_oasis_and_whale_reports_v1 as predecessor
from scripts import verify_sailing_hazards_and_dolphins_v1 as verified
from scripts.source_locked_derivation_v5118 import checked_text


parent, transaction, base = predecessor.parent, predecessor.transaction, predecessor.base
stage = SimpleNamespace(**verified.replay.candidate.stage_environment())
verification = SimpleNamespace(VISUAL=verified.VISUAL)
PARENT = predecessor.RELEASE
PROFILE = 'all-routes-sailing-hazards-and-dolphins-editorial-v1-20261111'
FAMILY = 'sailing_hazards_and_dolphins_contextual_20261111'
CHECK = 'registered_sailing_hazards_and_dolphins_native_live_and_complete_parent_inverse'
PACKAGE = Path('releases/all_routes_editorial_20261111_sailing_hazards_and_dolphins_candidate')
VERIFICATION = PACKAGE / 'verification'
RELEASE = VERIFICATION / 'registered_release_verification.json'
REVIEW = VERIFICATION / 'registered_review.json'
MUTATION_PLAN = VERIFICATION / 'registration_mutation_plan.json'
TEST = Path('out/sailing_hazards_and_dolphins_registered_20261111_v1')
ROM = TEST / 'Translation_DS_All_Routes_Sailing_Hazards_and_Dolphins_20261111_candidate.nds'
MANIFEST = ROM.with_suffix('.manifest.json')
PATCH = PACKAGE / 'translation.xdelta'
DOC = Path('docs/editorial_sailing_hazards_and_dolphins_registered_20261111.md')
PENDING_LEDGER = TEST / 'editorial_review_current.sailing_hazards_and_dolphins.pending.json'
OUTPUT, EVIDENCE, RESEARCH = stage.OUTPUT, stage.PROOF, stage.ROM
STARTUP_VERIFICATION, CHECKPOINT = verified.BOOT, verified.CHECKPOINT
LIVE_VERIFICATION, QA = verified.LIVE, verified.QA
PREVIOUS_TOTAL, TOTAL, REVISED, RETAINED = 27465, 59, 37, 22


def verification_scope(approved, live):
    ids = live['observed_ids']
    assert approved['live_messages'] == ids == [2366, 2374, 2384]
    assert approved['stored_cases'] == TOTAL and approved['viewed_pages'] == TOTAL
    assert live['actual_emulator'] and not live['hardware'] and live['original_log_reply_farewell_and_next_sailing_report']
    assert live['other_captains_and_hazards_offline']
    return dict(observed_notice_IDs=ids, stored_cases=TOTAL, viewed_pages=TOTAL,
        actual_emulator_holds=len(live['observations']), original_log_reply_farewell_and_next_sailing_report=True,
        fixture_scope=live['fixture_scope'], other_captains_and_hazards_offline=True, hardware=False)


def publish(release):
    summary = 'All 59 dolphin and sailing hazard records are registered. The ledger now credits 27,524 reviews.'
    readme = f"""# All Routes Sailing Hazards and Dolphins candidate

Use [{ROM.name}](../../{ROM.as_posix()}) with its build manifest. The [clean-input patch](translation.xdelta) reconstructs the ROM byte for byte from Japanese SHA-256 `{release['clean_input_sha256']}`. Candidate SHA-256 `{release['candidate_sha256']}`. Patch SHA-256 `{release['patch_sha256']}`.

{summary} The 37 revisions and 22 justified retentions preserve the four captains’ distinct replies, standardize “ship’s log,” restore the sailors’ reactions to the Sirens’ voices and retain the danger or humor of each hazard report.

The focused emulator replay observed the request, Hodram’s reply, the farewell and the next sailing report after supplying one fleet condition. Other captains and hazard variants received offline checks. All 59 pages received native and visual review. Cold boot, 24 protected name getters, 34 targeted tests and 108 release checks passed. [Gameplay](verification/{LIVE_VERIFICATION.name}) · [Exact records](verification/registered_review.json)
"""
    (PACKAGE / 'README.md').write_text(readme, encoding='utf-8', newline='\n')
    base.save(PACKAGE / 'checksums.json', {p.relative_to(PACKAGE).as_posix(): base.digest(p)
        for p in sorted(PACKAGE.rglob('*')) if p.is_file() and p.name != 'checksums.json'})
    pin_path = Path('translations/rom_retention_pins.json')
    pins = base.load(pin_path)
    for path in (verified.replay.candidate.previous.ROM, RESEARCH, ROM):
        resolved = str(path.resolve())
        assert path.is_file() and not any(row['path'] == resolved for row in pins)
        pins.append(dict(path=resolved, reason=f'Preserve the sailing hazards and dolphins build. SHA256 {base.digest(path)}'))
    base.replace_checked(pin_path, (json.dumps(pins, ensure_ascii=False, indent=2) + '\n')
        .replace('\n', '\r\n').encode('utf-8'))
    document = f"""# Sailing hazards and dolphins registered

{summary} COMMON 2366–2424 covers eleven native tables. The [review ledger](../{REVIEW.as_posix()}) records exact Japanese and prior English, context, individual decisions and all five gates. The [registered ROM and patch](../{PACKAGE.as_posix()}/README.md) carry forward the previous accepted layers, Market fix and ASCII right-bound correction.

The former portrait wrapper placed one bubbles warning beyond the safe width. The existing compact selector now covers the affected tables using the same break guard and fallback. The verification covers the prior static and dynamic scopes as well as the new ones. All 59 pages received native and visual review. The focused dolphin replay observed 2366, 2374 and 2384, then the next port report. It supplied the fleet condition and used the original game sequence. Other captain replies, Sirens and hazard variants received offline checks.

452 native shared keys remain to review or classify. The [source range map](editorial_remaining_shared_ranges_20261111.md) identifies the next six groups and the other 35 shared keys, including legacy New Game 104–107 and Market 750–752. Other player-facing prose, earlier wraps and glyphs, names and roles, and practical town and random-scene coverage remain in scope. Deferred artwork and the later older-record technical re-audit remain separate.
"""
    base.replace_checked(DOC, document.encode('utf-8'))
    lead = f'# Current editorial checkpoint - 2026-11-11\n\n{summary}\n\nContinue from [the registered sailing hazards and dolphins]({DOC.name}).\n\n'
    for name in ('editorial_handoff_current.md', 'editorial_efficiency_workflow.md', 'translation_progress.md'):
        path = Path('docs') / name
        base.replace_checked(path, lead.encode('utf-8') + path.read_bytes())
    continuity = Path('docs/build_continuity_protocol.md')
    protocol = ('The 59 dolphin and sailing hazard records are registered with 773 entries, 114 accepted layers and 108 checks. '
                'Use scripts/register_sailing_hazards_and_dolphins_v1.py with --register and --publish-prepared. '
                f'Exact reconstruction, the dolphin log exchange and cold startup pass. [Checkpoint]({DOC.name})\n\n')
    base.replace_checked(continuity, protocol.encode('utf-8') + continuity.read_bytes())
    print('Registered 773 entries and credited 59 dolphin and sailing hazard records once.')


def environment():
    env = predecessor.environment() | globals()
    for name in ('rebuild', 'final_review'):
        env[name] = FunctionType(env[name].__code__, env)
    return env


def register():
    source = checked_text(getsource(parent.register), {
        'price-info-trade-good-descriptions': 'sailing-hazards-and-dolphins',
        'All 124 Price Info trade-good descriptions are registered.':
            'All 59 dolphin and sailing hazard records are registered.',
        "'== 27093'": "'== 27524'", "'== 16230'": "'== 16524'", "'== 10863'": "'== 11000'",
        "== 763 and len(manifest['checks']) == 98": "== 772 and len(manifest['checks']) == 107",
        "== 764 and len(manifest['checks']) == 99": "== 773 and len(manifest['checks']) == 108",
        'registered_manifest_entries=764, accepted_layers=114, passing_release_checks=99':
            'registered_manifest_entries=773, accepted_layers=114, passing_release_checks=108',
        'verified_proof_and_relic_advice_predecessor=predecessor, trade_good_descriptions_release=str(REVIEW)':
            'verified_oasis_and_whale_reports_predecessor=predecessor, sailing_hazards_and_dolphins_release=str(REVIEW)',
        'Reviewed the native Price Info descriptions with word wrapping and pagination.':
            'Reviewed the dolphin exchange and sailing hazard reactions with native portrait wrapping.',
        'release_stack_before_trade_good_descriptions': 'release_stack_before_sailing_hazards_and_dolphins',
        'release_stack.trade_good_descriptions.pending': 'release_stack.sailing_hazards_and_dolphins.pending',
        'COMMON_PRICE_INFO_DESCRIPTION_DIRECTORY_AND_POINTERS': 'COMMON_SAILING_HAZARDS_AND_DOLPHINS_WRAP',
        '"dict(native_directory_and_pointer_updates_only=True, runtime_code_changed=False)"':
            r'''"evidence[\'ownership\']"''',
        'trade_good_descriptions_registered_successor_pipeline': 'sailing_hazards_and_dolphins_registered_successor_pipeline',
        'Price Info registration staged and ready to publish.': 'Dolphin and sailing hazard registration staged and ready to publish.',
    })
    env = environment()
    exec(compile(source, __file__ + '::derive-registration', 'exec'), env)
    env['register']()


def publish_prepared():
    source = checked_text(getsource(parent.publish_prepared), {
        'release_stack.trade_good_descriptions.pending': 'release_stack.sailing_hazards_and_dolphins.pending',
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
