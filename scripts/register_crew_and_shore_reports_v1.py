"""Register the source-reviewed crew exchanges and shore reports."""

import argparse
from inspect import getsource
import json
from pathlib import Path
from types import FunctionType, SimpleNamespace

from scripts import register_battle_commands_and_outcomes_v1 as predecessor
from scripts import verify_crew_and_shore_reports_v1 as verified
from scripts.source_locked_derivation_v5118 import checked_text


parent, transaction, base = predecessor.parent, predecessor.transaction, predecessor.base
v1 = verified.stage.first
stage = SimpleNamespace(**(vars(v1.first) | vars(v1) | vars(verified.stage)))
verification = SimpleNamespace(VISUAL=verified.VISUAL)
PARENT = predecessor.RELEASE
PROFILE = 'all-routes-crew-and-shore-reports-editorial-v1-20261111'
FAMILY = 'crew_and_shore_reports_contextual_20261111'
CHECK = 'registered_crew_and_shore_reports_native_live_and_complete_parent_inverse'
PACKAGE = Path('releases/all_routes_editorial_20261111_crew_and_shore_reports_candidate')
VERIFICATION = PACKAGE / 'verification'
RELEASE = VERIFICATION / 'registered_release_verification.json'
REVIEW = VERIFICATION / 'registered_review.json'
MUTATION_PLAN = VERIFICATION / 'registration_mutation_plan.json'
TEST = Path('out/crew_and_shore_reports_registered_20261111_v1')
ROM = TEST / 'Translation_DS_All_Routes_Crew_and_Shore_Reports_20261111_candidate.nds'
MANIFEST = ROM.with_suffix('.manifest.json')
PATCH = PACKAGE / 'translation.xdelta'
DOC = Path('docs/editorial_crew_and_shore_reports_registered_20261111.md')
PENDING_LEDGER = TEST / 'editorial_review_current.crew_and_shore_reports.pending.json'
OUTPUT, EVIDENCE, RESEARCH = stage.OUTPUT, stage.PROOF, stage.ROM
STARTUP_VERIFICATION, CHECKPOINT = verified.BOOT, verified.CHECKPOINT
LIVE_VERIFICATION, QA = verified.LIVE, verified.QA
PREVIOUS_TOTAL, TOTAL, REVISED, RETAINED = 27338, 56, 37, 19


def verification_scope(approved, live):
    ids = live['observed_ids']
    assert approved['live_messages'] == ids == [2244]
    assert approved['stored_cases'] == TOTAL and approved['viewed_pages'] == 56
    assert live['actual_emulator'] and not live['hardware'] and live['original_attack_and_sailor_loss_return_to_sailing']
    assert live['captain_reprimand_and_other_shore_events_offline']
    return dict(observed_notice_IDs=ids, stored_cases=TOTAL, viewed_pages=56,
        actual_emulator_holds=len(live['observations']), original_attack_and_sailor_loss_return_to_sailing=True,
        setup_fixture='Previously documented shore coordinates with the original event selection',
        welcome_observed_in_current_gameplay=False,
        captain_reprimand_and_other_shore_events_offline=True, hardware=False)


def publish(release):
    summary = 'All 56 crew and shore reports are registered. The ledger now credits 27,394 reviews.'
    readme = f"""# All Routes Crew and Shore Reports candidate

Use [{ROM.name}](../../{ROM.as_posix()}) with its build manifest. The [clean-input patch](translation.xdelta) reconstructs the ROM byte for byte from Japanese SHA-256 `{release['clean_input_sha256']}`. Candidate SHA-256 `{release['candidate_sha256']}`. Patch SHA-256 `{release['patch_sha256']}`.

{summary} The batch includes 37 revisions and 19 justified retentions. It preserves the four captains’ reprimands and the different voices reporting shore discoveries, welcome or attack, desertion, illness and quicksand. It also removes mixed-width English letters and keeps phrases such as “food and water” and “caught in quicksand” together.

The focused Search replay displayed the attack report and the loss of 11 sailors, then returned to sailing. The original event selection ran with the disclosed location setup. The friendly welcome and food-and-water follow-up received offline display checks. All 56 pages, cold boot, 24 protected name getters, 34 targeted tests and 106 release checks passed. [Gameplay](verification/{LIVE_VERIFICATION.name}) · [Exact records](verification/registered_review.json)
"""
    (PACKAGE / 'README.md').write_text(readme, encoding='utf-8', newline='\n')
    base.save(PACKAGE / 'checksums.json', {p.relative_to(PACKAGE).as_posix(): base.digest(p)
        for p in sorted(PACKAGE.rglob('*')) if p.is_file() and p.name != 'checksums.json'})
    pin_path = Path('translations/rom_retention_pins.json')
    pins = base.load(pin_path)
    for path in (v1.ROM, RESEARCH, ROM):
        resolved = str(path.resolve())
        assert path.is_file() and not any(row['path'] == resolved for row in pins)
        pins.append(dict(path=resolved, reason=f'Preserve the crew and shore report build. SHA256 {base.digest(path)}'))
    base.replace_checked(pin_path, (json.dumps(pins, ensure_ascii=False, indent=2) + '\n')
        .replace('\n', '\r\n').encode('utf-8'))
    document = f"""# Crew and shore reports registered

{summary} COMMON 2193–2200, 2222–2228 and 2234–2274 cover ten native tables. The [review ledger](../{REVIEW.as_posix()}) records exact Japanese and prior English, speaker context, individual decisions and all five gates. Eleven linked context records retain their earlier credit. The [registered ROM and patch](../{PACKAGE.as_posix()}/README.md) preserve the previous accepted layers and runtime fixes.

The replay observed 2244 at frame 14657, the original loss of 11 sailors and the return to sailing. The event occurred earlier in the current build than in the historical replay. The attempted welcome replay diverged before the welcome and its provision precondition failed. The welcome and food-and-water exchange, captain reprimands and other shore alternatives received offline verification. The longer four-row texts fit on one page, with whole phrases and complete glyphs.

582 native shared keys remain to review or classify. Continue with the connected reports at COMMON 2288–2358. Follow the oasis and mirage, bog, shore discoveries, shark and white-whale exchanges in their original contexts. Verify both substitutions in the Conqueror’s Proof reports. Legacy New Game 104–107, Market 750–752, other player-facing prose, earlier wraps and glyphs, names and roles, and practical town and random-scene coverage remain in scope. Deferred artwork and the later older-record technical re-audit remain separate.
"""
    base.replace_checked(DOC, document.encode('utf-8'))
    lead = f'# Current editorial checkpoint - 2026-11-11\n\n{summary}\n\nContinue from [the registered crew and shore reports]({DOC.name}).\n\n'
    for name in ('editorial_handoff_current.md', 'editorial_efficiency_workflow.md', 'translation_progress.md'):
        path = Path('docs') / name
        base.replace_checked(path, lead.encode('utf-8') + path.read_bytes())
    continuity = Path('docs/build_continuity_protocol.md')
    protocol = ('The 56 crew and shore reports are registered with 771 entries, 114 accepted layers and 106 checks. '
                'Use scripts/register_crew_and_shore_reports_v1.py with --register and --publish-prepared. '
                f'Exact reconstruction, the Search attack and cold startup pass. [Checkpoint]({DOC.name})\n\n')
    base.replace_checked(continuity, protocol.encode('utf-8') + continuity.read_bytes())
    print('Registered 771 entries and credited 56 crew and shore reports once.')


def environment():
    env = predecessor.environment() | globals()
    for name in ('rebuild', 'final_review'):
        env[name] = FunctionType(env[name].__code__, env)
    return env


def register():
    source = checked_text(getsource(parent.register), {
        'price-info-trade-good-descriptions': 'crew-and-shore-reports',
        'All 124 Price Info trade-good descriptions are registered.': 'All 56 crew and shore reports are registered.',
        "'== 27093'": "'== 27394'", "'== 16230'": "'== 16436'", "'== 10863'": "'== 10958'",
        "== 763 and len(manifest['checks']) == 98": "== 770 and len(manifest['checks']) == 105",
        "== 764 and len(manifest['checks']) == 99": "== 771 and len(manifest['checks']) == 106",
        'registered_manifest_entries=764, accepted_layers=114, passing_release_checks=99':
            'registered_manifest_entries=771, accepted_layers=114, passing_release_checks=106',
        'verified_proof_and_relic_advice_predecessor=predecessor, trade_good_descriptions_release=str(REVIEW)':
            'verified_battle_commands_and_outcomes_predecessor=predecessor, crew_and_shore_reports_release=str(REVIEW)',
        'Reviewed the native Price Info descriptions with word wrapping and pagination.':
            'Reviewed captain reprimands and shore-party dialogue with native phrase wrapping.',
        'release_stack_before_trade_good_descriptions': 'release_stack_before_crew_and_shore_reports',
        'release_stack.trade_good_descriptions.pending': 'release_stack.crew_and_shore_reports.pending',
        'COMMON_PRICE_INFO_DESCRIPTION_DIRECTORY_AND_POINTERS': 'COMMON_CREW_AND_SHORE_REPORTS_WRAP',
        '"dict(native_directory_and_pointer_updates_only=True, runtime_code_changed=False)"':
            r'''"evidence[\'ownership\']"''',
        'trade_good_descriptions_registered_successor_pipeline': 'crew_and_shore_reports_registered_successor_pipeline',
        'Price Info registration staged and ready to publish.': 'Crew and shore report registration staged and ready to publish.',
    })
    env = environment()
    exec(compile(source, __file__ + '::derive-registration', 'exec'), env)
    env['register']()


def publish_prepared():
    source = checked_text(getsource(parent.publish_prepared), {
        'release_stack.trade_good_descriptions.pending': 'release_stack.crew_and_shore_reports.pending',
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
