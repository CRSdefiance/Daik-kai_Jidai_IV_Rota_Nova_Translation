"""Register the verified pirate portraits, battle results and port orders."""

import argparse
from inspect import getsource
import json
from pathlib import Path
from types import FunctionType, SimpleNamespace

from scripts import register_city_combat_notices_v1 as predecessor
from scripts import verify_pirate_and_retreat_reports_v1 as verified
from scripts.source_locked_derivation_v5118 import checked_text


parent, transaction, base = predecessor.parent, predecessor.transaction, predecessor.base
v1 = verified.stage.first
stage = SimpleNamespace(**(vars(v1.first) | vars(v1) | vars(verified.stage)))
stage.stage = FunctionType(v1.stage.__code__, vars(v1) | {'PHRASES': stage.PHRASES}, argdefs=v1.stage.__defaults__)
verification = SimpleNamespace(VISUAL=verified.VISUAL)
PARENT = predecessor.RELEASE
PROFILE = 'all-routes-pirate-and-retreat-reports-editorial-v1-20261111'
FAMILY = 'pirate_and_retreat_reports_contextual_20261111'
CHECK = 'registered_pirate_and_retreat_reports_native_live_and_complete_parent_inverse'
PACKAGE = Path('releases/all_routes_editorial_20261111_pirate_and_retreat_reports_candidate')
VERIFICATION = PACKAGE / 'verification'
RELEASE = VERIFICATION / 'registered_release_verification.json'
REVIEW = VERIFICATION / 'registered_review.json'
MUTATION_PLAN = VERIFICATION / 'registration_mutation_plan.json'
TEST = Path('out/pirate_and_retreat_reports_registered_20261111_v1')
ROM = TEST / 'Translation_DS_All_Routes_Pirate_and_Retreat_Reports_20261111_candidate.nds'
MANIFEST = ROM.with_suffix('.manifest.json')
PATCH = PACKAGE / 'translation.xdelta'
DOC = Path('docs/editorial_pirate_and_retreat_reports_registered_20261111.md')
PENDING_LEDGER = TEST / 'editorial_review_current.pirate_and_retreat_reports.pending.json'
OUTPUT, EVIDENCE, RESEARCH = stage.OUTPUT, stage.PROOF, stage.ROM
STARTUP_VERIFICATION, CHECKPOINT = verified.BOOT, verified.CHECKPOINT
LIVE_VERIFICATION, QA = verified.LIVE, verified.QA
PREVIOUS_TOTAL, TOTAL, REVISED, RETAINED = 27261, 48, 30, 18


def verification_scope(approved, live):
    assert approved['live_messages'] == live['observed_ids'] == [2651, 2657]
    assert approved['stored_cases'] == TOTAL and approved['viewed_pages'] == 71
    assert live['actual_emulator'] and not live['hardware']
    assert live['original_attack_order_and_report'] and live['original_A_advance_and_return_to_sailing']
    assert live['pirate_bearing_display_verified_offline'] and not live['live_pirate_activation']
    layout = base.load(verified.VISUAL)
    assert len(layout['offline_original_queued_portraits']) == 20
    return dict(observed_notice_IDs=live['observed_ids'], stored_cases=TOTAL, viewed_pages=71,
        actual_emulator_holds=len(live['observations']), original_A_advance_and_return_to_sailing=True,
        focused_queued_portraits_offline=20, live_pirate_activation=False, hardware=False)


def publish(release):
    summary = 'All 48 pirate and retreat reports are registered. The ledger now credits 27,309 reviews.'
    readme = f"""# All Routes Pirate and Retreat Reports candidate

Use [{ROM.name}](../../{ROM.as_posix()}) with its build manifest. The [clean-input patch](translation.xdelta) reconstructs the ROM byte for byte from Japanese SHA-256 `{release['clean_input_sha256']}`. Candidate SHA-256 `{release['candidate_sha256']}`. Patch SHA-256 `{release['patch_sha256']}`.

{summary} The batch includes 30 revisions and 18 justified retentions. The two pirate alert tables keep the original bearing and given-name fields in order. The scoped caller renders all nine bearings as ordinary English without changing other uses of the compass abbreviations.

The original Hamburg sequence displayed the retreat and the revised port order, then returned to sailing. The pirate sighting and attack alerts passed focused offline native tests. All 71 portrait pages, cold boot, 24 protected name getters, 34 targeted tests and 104 release checks passed. [Gameplay](verification/{LIVE_VERIFICATION.name}) · [Exact records](verification/registered_review.json)
"""
    (PACKAGE / 'README.md').write_text(readme, encoding='utf-8', newline='\n')
    base.save(PACKAGE / 'checksums.json', {p.relative_to(PACKAGE).as_posix(): base.digest(p)
        for p in sorted(PACKAGE.rglob('*')) if p.is_file() and p.name != 'checksums.json'})
    pin_path = Path('translations/rom_retention_pins.json')
    pins = base.load(pin_path)
    for path in (v1.ROM, RESEARCH, ROM):
        resolved = str(path.resolve())
        assert path.is_file() and not any(row['path'] == resolved for row in pins)
        pins.append(dict(path=resolved, reason=f'Preserve the pirate and retreat report build. SHA256 {base.digest(path)}'))
    base.replace_checked(pin_path, (json.dumps(pins, ensure_ascii=False, indent=2) + '\n')
        .replace('\n', '\r\n').encode('utf-8'))
    document = f"""# Pirate and retreat reports registered

{summary} COMMON 2615–2662 covers eight original voice tables and ten caller sites. The clean Japanese and prior English references, five gates, exact stored forms and individual rationales are recorded in the [review ledger](../{REVIEW.as_posix()}). The [release and clean-input patch](../{PACKAGE.as_posix()}/README.md) retain the earlier Market and right-bound corrections.

The Hamburg replay displayed 2651 and 2657, including the revised two-line port order, and then returned to sailing through the original input. The nine bearing mappings pass on both alert tables with four fallback controls. Another 20 focused offline cases run from the scoped call through original selection, expansion and formatting. All 71 staged pages were visually reviewed. The pirate sightings and attacks were unvisited in gameplay.

667 native shared keys remain to review or classify. Use the remaining-scope audit linked from the Combat and Fleet release and remove the now-credited range 2615–2662 when identifying the next connected family. Legacy New Game 104–107 and Market 750–752 still need consumer classification. Other player-facing prose, earlier wraps and glyphs, names and roles, and practical town and random-scene coverage remain in scope. Deferred artwork and the later older-record technical re-audit remain separate.
"""
    base.replace_checked(DOC, document.encode('utf-8'))
    lead = f'# Current editorial checkpoint - 2026-11-11\n\n{summary}\n\nContinue from [the registered pirate and retreat reports]({DOC.name}).\n\n'
    for name in ('editorial_handoff_current.md', 'editorial_efficiency_workflow.md', 'translation_progress.md'):
        path = Path('docs') / name
        base.replace_checked(path, lead.encode('utf-8') + path.read_bytes())
    continuity = Path('docs/build_continuity_protocol.md')
    protocol = ('The 48 pirate and retreat reports are registered with 769 entries, 114 accepted layers and 104 checks. '
                'Use scripts/register_pirate_and_retreat_reports_v1.py with --register and --publish-prepared. '
                f'Exact reconstruction, Hamburg retreat and cold startup pass. [Checkpoint]({DOC.name})\n\n')
    base.replace_checked(continuity, protocol.encode('utf-8') + continuity.read_bytes())
    print('Registered 769 entries and credited 48 pirate and retreat reports once.')


def environment():
    env = predecessor.environment() | globals()
    for function in (predecessor.predecessor.rebuild, predecessor.predecessor.final_review):
        env[function.__name__] = FunctionType(function.__code__, env)
    return env


def register():
    source = checked_text(getsource(parent.register), {
        'price-info-trade-good-descriptions': 'pirate-and-retreat-reports',
        'All 124 Price Info trade-good descriptions are registered.': 'All 48 pirate and retreat reports are registered.',
        "'== 27093'": "'== 27309'", "'== 16230'": "'== 16381'", "'== 10863'": "'== 10928'",
        "== 763 and len(manifest['checks']) == 98": "== 768 and len(manifest['checks']) == 103",
        "== 764 and len(manifest['checks']) == 99": "== 769 and len(manifest['checks']) == 104",
        'registered_manifest_entries=764, accepted_layers=114, passing_release_checks=99':
            'registered_manifest_entries=769, accepted_layers=114, passing_release_checks=104',
        'verified_proof_and_relic_advice_predecessor=predecessor, trade_good_descriptions_release=str(REVIEW)':
            'verified_city_combat_notices_predecessor=predecessor, pirate_and_retreat_reports_release=str(REVIEW)',
        'Reviewed the native Price Info descriptions with word wrapping and pagination.':
            'Reviewed pirate alerts and retreat reports with scoped bearing localization and native wrapping.',
        'release_stack_before_trade_good_descriptions': 'release_stack_before_pirate_and_retreat_reports',
        'release_stack.trade_good_descriptions.pending': 'release_stack.pirate_and_retreat_reports.pending',
        'COMMON_PRICE_INFO_DESCRIPTION_DIRECTORY_AND_POINTERS': 'COMMON_PIRATE_AND_RETREAT_REPORTS_WRAP_AND_BEARINGS',
        '"dict(native_directory_and_pointer_updates_only=True, runtime_code_changed=False)"':
            r'''"evidence[\'ownership\']"''',
        'trade_good_descriptions_registered_successor_pipeline': 'pirate_and_retreat_reports_registered_successor_pipeline',
        'Price Info registration staged and ready to publish.': 'Pirate and retreat registration staged and ready to publish.',
    })
    env = environment()
    exec(compile(source, __file__ + '::derive-registration', 'exec'), env)
    env['register']()


def publish_prepared():
    source = checked_text(getsource(parent.publish_prepared), {
        'release_stack.trade_good_descriptions.pending': 'release_stack.pirate_and_retreat_reports.pending',
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
