"""Register the verified battle commands, ram strikes and defeat reports."""

import argparse
from inspect import getsource
import json
from pathlib import Path
from types import FunctionType, SimpleNamespace

from scripts import register_pirate_and_retreat_reports_v1 as predecessor
from scripts import verify_battle_commands_and_outcomes_v1 as verified
from scripts.source_locked_derivation_v5118 import checked_text


parent, transaction, base = predecessor.parent, predecessor.transaction, predecessor.base
v1 = verified.stage.first
stage = SimpleNamespace(**(vars(v1.first) | vars(v1) | vars(verified.stage)))
verification = SimpleNamespace(VISUAL=verified.VISUAL)
PARENT = predecessor.RELEASE
PROFILE = 'all-routes-battle-commands-and-outcomes-editorial-v1-20261111'
FAMILY = 'battle_commands_and_outcomes_contextual_20261111'
CHECK = 'registered_battle_commands_and_outcomes_native_live_and_complete_parent_inverse'
PACKAGE = Path('releases/all_routes_editorial_20261111_battle_commands_and_outcomes_candidate')
VERIFICATION = PACKAGE / 'verification'
RELEASE = VERIFICATION / 'registered_release_verification.json'
REVIEW = VERIFICATION / 'registered_review.json'
MUTATION_PLAN = VERIFICATION / 'registration_mutation_plan.json'
TEST = Path('out/battle_commands_and_outcomes_registered_20261111_v1')
ROM = TEST / 'Translation_DS_All_Routes_Battle_Commands_and_Outcomes_20261111_candidate.nds'
MANIFEST = ROM.with_suffix('.manifest.json')
PATCH = PACKAGE / 'translation.xdelta'
DOC = Path('docs/editorial_battle_commands_and_outcomes_registered_20261111.md')
PENDING_LEDGER = TEST / 'editorial_review_current.battle_commands_and_outcomes.pending.json'
OUTPUT, EVIDENCE, RESEARCH = stage.OUTPUT, stage.PROOF, stage.ROM
STARTUP_VERIFICATION, CHECKPOINT = verified.BOOT, verified.CHECKPOINT
LIVE_VERIFICATION, QA = verified.LIVE, verified.QA
PREVIOUS_TOTAL, TOTAL, REVISED, RETAINED = 27309, 29, 18, 11


def verification_scope(approved, live):
    assert approved['live_messages'] == live['observed_ids'] == [2123]
    assert approved['stored_cases'] == TOTAL and approved['viewed_pages'] == 65
    assert live['actual_emulator'] and not live['hardware'] and live['native_accept_and_cancel']
    assert live['ram_and_defeat_messages_offline']
    assert [row['action'] for row in live['observations']] == ['accept', 'cancel']
    return dict(observed_notice_IDs=live['observed_ids'], stored_cases=TOTAL, viewed_pages=65,
        actual_emulator_holds=len(live['observations']), native_accept_and_cancel=True,
        setup_fixture='Original Sao Tome approach and two duty bytes to assign the existing officer',
        ram_and_defeat_messages_offline=True, hardware=False)


def publish(release):
    summary = 'All 29 battle commands and outcomes are registered. The ledger now credits 27,338 reviews.'
    readme = f"""# All Routes Battle Commands and Outcomes candidate

Use [{ROM.name}](../../{ROM.as_posix()}) with its build manifest. The [clean-input patch](translation.xdelta) reconstructs the ROM byte for byte from Japanese SHA-256 `{release['clean_input_sha256']}`. Candidate SHA-256 `{release['candidate_sha256']}`. Patch SHA-256 `{release['patch_sha256']}`.

{summary} The batch includes 18 revisions and 11 justified retentions across ram strikes, town attack confirmations, flagship defeats and special-target victories. The tested town names and questions stay together. The special victory call renders Monster Fish, Giant Squid, Shark, White Whale and Ghost Ship in English, including inherited Japanese or abbreviated strings from loaded models.

Two focused Sao Tome replays displayed “Attack Sao Tome?” and exercised the original Yes and No transitions. A location and crew fixture set up the prompt. Ram and defeat reports received offline native tests. All 65 pages, cold boot, 24 protected name getters, 34 targeted tests and 105 release checks passed. [Gameplay](verification/{LIVE_VERIFICATION.name}) · [Exact records](verification/registered_review.json)
"""
    (PACKAGE / 'README.md').write_text(readme, encoding='utf-8', newline='\n')
    base.save(PACKAGE / 'checksums.json', {p.relative_to(PACKAGE).as_posix(): base.digest(p)
        for p in sorted(PACKAGE.rglob('*')) if p.is_file() and p.name != 'checksums.json'})
    pin_path = Path('translations/rom_retention_pins.json')
    pins = base.load(pin_path)
    for path in (v1.ROM, RESEARCH, ROM):
        resolved = str(path.resolve())
        assert path.is_file() and not any(row['path'] == resolved for row in pins)
        pins.append(dict(path=resolved, reason=f'Preserve the battle commands and outcomes build. SHA256 {base.digest(path)}'))
    base.replace_checked(pin_path, (json.dumps(pins, ensure_ascii=False, indent=2) + '\n')
        .replace('\n', '\r\n').encode('utf-8'))
    document = f"""# Battle commands and outcomes registered

{summary} COMMON 2106–2113, 2122–2129 and 2179–2191 cover four original voice tables. The [review ledger](../{REVIEW.as_posix()}) records clean Japanese, prior English, per-record decisions, native substitutions and all five gates. COMMON 2192 stays linked as previously credited context. The [registered ROM and patch](../{PACKAGE.as_posix()}/README.md) retain earlier runtime fixes.

The Sao Tome fixture changed the approach and assigned the existing officer Gerhard through the original roster setter. Both emulator runs displayed 2123 with the full name. Yes entered town combat and No returned to target selection. Ram and defeat alternatives passed offline native checks. The special-target victory caller resolves four inherited Japanese names and “Ghost,” with controls for the clean Ghost Ship name and unmatched values. Its new alias is scoped to this report. The corresponding fixed model strings remain a lead for any other player-facing consumer. The original Monster Fish name getter was exercised offline using a read-only historical snapshot of an active target.

638 native shared keys remain to review or classify. Continue with the complete crew reprimand exchange at COMMON 2193–2200 and the next shore-party reports, including COMMON 2222–2228 and 2234–2274. Preserve already credited context from adjacent native tables. Legacy New Game 104–107, Market 750–752, other player-facing prose, earlier wraps and glyphs, names and roles, and practical town and random-scene coverage remain in scope. Deferred artwork and the later older-record technical re-audit remain separate.
"""
    base.replace_checked(DOC, document.encode('utf-8'))
    lead = f'# Current editorial checkpoint - 2026-11-11\n\n{summary}\n\nContinue from [the registered battle commands and outcomes]({DOC.name}).\n\n'
    for name in ('editorial_handoff_current.md', 'editorial_efficiency_workflow.md', 'translation_progress.md'):
        path = Path('docs') / name
        base.replace_checked(path, lead.encode('utf-8') + path.read_bytes())
    continuity = Path('docs/build_continuity_protocol.md')
    protocol = ('The 29 battle commands and outcomes are registered with 770 entries, 114 accepted layers and 105 checks. '
                'Use scripts/register_battle_commands_and_outcomes_v1.py with --register and --publish-prepared. '
                f'Exact reconstruction, both town confirmation branches and cold startup pass. [Checkpoint]({DOC.name})\n\n')
    base.replace_checked(continuity, protocol.encode('utf-8') + continuity.read_bytes())
    print('Registered 770 entries and credited 29 battle commands and outcomes once.')


def environment():
    env = predecessor.environment() | globals()
    for name in ('rebuild', 'final_review'):
        env[name] = FunctionType(env[name].__code__, env)
    return env


def register():
    source = checked_text(getsource(parent.register), {
        'price-info-trade-good-descriptions': 'battle-commands-and-outcomes',
        'All 124 Price Info trade-good descriptions are registered.': 'All 29 battle commands and outcomes are registered.',
        "'== 27093'": "'== 27338'", "'== 16230'": "'== 16399'", "'== 10863'": "'== 10939'",
        "== 763 and len(manifest['checks']) == 98": "== 769 and len(manifest['checks']) == 104",
        "== 764 and len(manifest['checks']) == 99": "== 770 and len(manifest['checks']) == 105",
        'registered_manifest_entries=764, accepted_layers=114, passing_release_checks=99':
            'registered_manifest_entries=770, accepted_layers=114, passing_release_checks=105',
        'verified_proof_and_relic_advice_predecessor=predecessor, trade_good_descriptions_release=str(REVIEW)':
            'verified_pirate_and_retreat_reports_predecessor=predecessor, battle_commands_and_outcomes_release=str(REVIEW)',
        'Reviewed the native Price Info descriptions with word wrapping and pagination.':
            'Reviewed battle commands and outcomes with town confirmations and special target names.',
        'release_stack_before_trade_good_descriptions': 'release_stack_before_battle_commands_and_outcomes',
        'release_stack.trade_good_descriptions.pending': 'release_stack.battle_commands_and_outcomes.pending',
        'COMMON_PRICE_INFO_DESCRIPTION_DIRECTORY_AND_POINTERS': 'COMMON_BATTLE_COMMANDS_OUTCOMES_WRAP_AND_NAMES',
        '"dict(native_directory_and_pointer_updates_only=True, runtime_code_changed=False)"':
            r'''"evidence[\'ownership\']"''',
        'trade_good_descriptions_registered_successor_pipeline': 'battle_commands_and_outcomes_registered_successor_pipeline',
        'Price Info registration staged and ready to publish.': 'Battle commands and outcomes registration staged and ready to publish.',
    })
    env = environment()
    exec(compile(source, __file__ + '::derive-registration', 'exec'), env)
    env['register']()


def publish_prepared():
    source = checked_text(getsource(parent.publish_prepared), {
        'release_stack.trade_good_descriptions.pending': 'release_stack.battle_commands_and_outcomes.pending',
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
