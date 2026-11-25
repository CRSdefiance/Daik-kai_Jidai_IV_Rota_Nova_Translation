"""Register crew-equipment advice after the native and Mikhail replay gates."""

import argparse
from inspect import getsource
import json
from pathlib import Path
from types import FunctionType, SimpleNamespace

from scripts import register_item_production_advice_v1 as transaction
from scripts import register_weapon_armor_advice_v1 as parent
from scripts import stage_crew_equipment_advice_v2 as layout
from scripts import verify_crew_equipment_advice_v1 as verification
from scripts.source_locked_derivation_v5118 import checked_text


base = transaction.base
PARENT = parent.RELEASE
PROFILE = 'all-routes-crew-equipment-advice-editorial-v1-20261111'
FAMILY = 'crew_equipment_advice_contextual_20261111'
CHECK = 'registered_crew_equipment_advice_native_live_and_complete_parent_inverse'
PACKAGE = Path('releases/all_routes_editorial_20261111_crew_equipment_advice_candidate')
VERIFICATION = PACKAGE / 'verification'
RELEASE = VERIFICATION / 'registered_release_verification.json'
REVIEW = VERIFICATION / 'registered_review.json'
MUTATION_PLAN = VERIFICATION / 'registration_mutation_plan.json'
TEST = Path('out/crew_equipment_advice_registered_20261111_v1')
ROM = TEST / 'Translation_DS_All_Routes_Crew_Equipment_Advice_20261111_candidate.nds'
MANIFEST = ROM.with_suffix('.manifest.json')
PATCH = PACKAGE / 'translation.xdelta'
DOC = Path('docs/editorial_crew_equipment_advice_registered_20261111.md')
PENDING_LEDGER = TEST / 'editorial_review_current.crew_equipment_advice.pending.json'
OUTPUT, EVIDENCE, RESEARCH = layout.OUTPUT, layout.PROOF, layout.ROM
STARTUP_VERIFICATION, CHECKPOINT = verification.BOOT, verification.CHECKPOINT
LIVE_VERIFICATION, QA = verification.LIVE, verification.QA
PREVIOUS_TOTAL, TOTAL, REVISED, RETAINED = 26825, 40, 29, 11


def stage_environment():
    first = layout.first
    env = vars(verification.stage) | vars(first.weapon) | vars(first) | vars(layout)
    env['review'] = verification.stage.review
    env['transform'] = FunctionType(first.weapon.transform.__code__, env)
    code = checked_text(getsource(first.base.stage), {
        "packing['touched_blocks'] == [33, 34]": "packing['touched_blocks'] == [34, 35]",
    })
    exec(compile(code, __file__ + '::exact-crew-advice-stage-reproduction', 'exec'), env)
    return SimpleNamespace(**env)


stage = stage_environment()


def verification_scope(approved, live):
    assert approved['live_messages'] == live['observed_ids'] == list(verification.OBSERVED)
    assert approved['stored_cases'] == approved['viewed_pages'] == TOTAL
    assert live['original_Advice_button'] and live['original_item_view_restored'] and live['original_town_return']
    assert live['complete_dialogue_ink_and_blank_cells_exact']
    assert all(row['header']['text'] == verification.NAMEPLATE for row in live['observed'])
    assert [len(row['body_rows']) for row in live['observed']] == [1, 3]
    assert live['inventory_fixture']['original_captain'] == live['inventory_fixture']['original_route_state'] == 3
    return dict(observed_notice_IDs=live['observed_ids'], stored_cases=TOTAL, viewed_pages=TOTAL,
        offline_actor_and_screen_cases=240, offline_native_portrait_cases=80,
        original_Mikhail_branch=True, original_Advice_button_item_and_Nagasaki_return=True,
        natural_advice_unlock=False, hardware=False,
        fixture_scope='The original transfer supplied Illustrated Bible and Gupta Spirit Beast to a copy '
                      'of the Nagasaki Maria save. The original flag setter enabled Advice. Normal inputs '
                      'requested and dismissed both Mikhail portraits and returned to Nagasaki.')


def publish(release):
    summary = 'The 40 crew-equipment advice replies are registered. The ledger now credits 26,865 reviews.'
    notes = f"""# All Routes Crew Equipment Advice candidate

Use [{ROM.name}](../../{ROM.as_posix()}) with its build manifest. The [clean-input patch](translation.xdelta) reconstructs it byte for byte from the clean Japanese ROM with SHA-256 '{release['clean_input_sha256']}'. Expected ROM SHA-256 is '{release['candidate_sha256']}'. Patch SHA-256 is '{release['patch_sha256']}'.

{summary} Twenty-nine revisions and eleven justified retentions cover the complete equipment advice category. The replies match the in-game Sail Handler, First Mate and Boarding Leader titles, preserve the adviser’s speculation about the Gupta Spirit Beast, and restore both sides of the pricing warning on Vezas’ Scales. The final text uses the native portrait width and preserves the original item and speaker selectors.

All 40 final pages passed visual review. All 80 portrait cases and 240 original caller-fragment cases passed offline. A focused emulator replay showed Mikhail Letzel’s Illustrated Bible and Gupta Spirit Beast replies, restored the correct item view after each, then returned to Nagasaki. The copied Maria save used isolated inventory and Advice flag fixtures. The other replies and Hans’s crew-equipment branch were checked offline. All 96 release checks, 34 targeted tests, the 31,000-frame cold boot and 24 protected name getters passed. [Gameplay proof](verification/crew_equipment_advice_gameplay_verification.json) · [Exact record review](verification/registered_review.json)
"""
    (PACKAGE / 'README.md').write_text(notes, encoding='utf-8', newline='\n')
    base.save(PACKAGE / 'checksums.json', {p.relative_to(PACKAGE).as_posix(): base.digest(p)
        for p in sorted(PACKAGE.rglob('*')) if p.is_file() and p.name != 'checksums.json'})
    pin_path = Path('translations/rom_retention_pins.json')
    pins = base.load(pin_path)
    for path in (layout.first.ROM, RESEARCH, ROM):
        resolved = str(path.resolve())
        assert not any(row['path'] == resolved for row in pins)
        pins.append(dict(path=resolved, reason=f'Preserve the crew-equipment advice build. SHA256 {base.digest(path)}'))
    base.replace_checked(pin_path, (json.dumps(pins, ensure_ascii=False, indent=2) + '\n').replace('\n', '\r\n').encode('utf-8'))
    doc = f"""# Crew-equipment advice registered

{summary} COMMON 3107–3146 covers the 40 crew-equipment replies. The Gallery, compact item screen and regular Items continue selecting the original actor and message by item index. The English restores the First Mate’s duties, the Boarding Leader’s command responsibilities, and the adviser’s doubt that anyone could overcharge or underpay the player. [Registered review](../{REVIEW.as_posix()}) · [Release and patch](../{PACKAGE.as_posix()}/README.md)

Only COMMON blocks 34 and 35 and the guarded portrait selector changed. Every other selected COMMON span and the 123,264-byte copied allocation remain exact. The Nagasaki replay verified both Mikhail nameplates, every visible body glyph on the one- and three-row examples, and return to each item and to town. Maria’s saved route selected Mikhail without changing the captain or route.

Continue at COMMON 3147 with figureheads, navigation items and gifts. Preserve the source’s regional gift clues and qualifications. Proof and map advice and all remaining player-facing text and speaker labels stay in scope. Graphics artwork and the later older-record technical re-audit remain separate.
"""
    base.replace_checked(DOC, doc.encode('utf-8'))
    lead = f'# Current editorial checkpoint - 2026-11-11\n\n{summary}\n\nContinue from [the registered crew-equipment advice]({DOC.name}).\n\n'
    for name in ('editorial_handoff_current.md', 'editorial_efficiency_workflow.md', 'translation_progress.md'):
        path = Path('docs') / name
        base.replace_checked(path, lead.encode('utf-8') + path.read_bytes())
    continuity = Path('docs/build_continuity_protocol.md')
    protocol = (
        'The 40 crew-equipment replies are registered over Weapon and Armor Advice with 761 entries, '
        '114 accepted layers and 96 checks. Use scripts/register_crew_equipment_advice_v1.py with '
        f'--register and --publish-prepared. Exact reconstruction, Mikhail’s Nagasaki Advice replay '
        f'and cold startup pass. [Registered checkpoint]({DOC.name})\n\n')
    base.replace_checked(continuity, protocol.encode('utf-8') + continuity.read_bytes())
    print('Registered 761 entries and credited 40 crew-equipment advice reviews once.')


def environment():
    env = vars(transaction) | globals()
    env['rebuild'] = FunctionType(transaction.rebuild.__code__, env)
    env['final_review'] = FunctionType(transaction.final_review.__code__, env)
    return env


def register():
    code = checked_text(getsource(transaction.register), {
        "'item-production-and-voyage-advice'": "'crew-equipment-advice'",
        'Twenty-four item advice replies are registered.': 'Forty crew-equipment replies are registered.',
        '== 26775': '== 26865', '== 16001': '== 16060', '== 10774': '== 10805',
        "== 758 and len(manifest['checks']) == 93": "== 760 and len(manifest['checks']) == 95",
        'release_stack_before_item_production_advice.json': 'release_stack_before_crew_equipment_advice.json',
        'verified_promotional_item_cards_predecessor=predecessor, item_production_advice_release=str(REVIEW)':
            'verified_weapon_armor_advice_predecessor=predecessor, crew_equipment_advice_release=str(REVIEW)',
        'Reviewed item production and voyage-supply advice with scoped portrait wraps.':
            'Reviewed crew-equipment advice with scoped portrait wraps.',
        'release_stack.item_production_advice.pending.json': 'release_stack.crew_equipment_advice.pending.json',
        'COMMON_ITEM_PRODUCTION_ADVICE_PORTRAIT_WRAP': 'COMMON_CREW_EQUIPMENT_ADVICE_PORTRAIT_WRAP',
        "manifest['item_production_advice_registered_successor_pipeline']":
            "manifest['crew_equipment_advice_registered_successor_pipeline']",
        "== 759 and len(manifest['checks']) == 94": "== 761 and len(manifest['checks']) == 96",
        'registered_manifest_entries=759, accepted_layers=114, passing_release_checks=94, repository_tests=34':
            'registered_manifest_entries=761, accepted_layers=114, passing_release_checks=96, repository_tests=34',
        'Item advice registration staged and ready to publish.':
            'Crew-equipment advice registration staged and ready to publish.',
        'live_check.verified.VISUAL': 'verification.VISUAL',
        'transaction.preserve_compression': 'transaction.transaction.preserve_compression',
    })
    env = environment()
    exec(compile(code, __file__ + '::registered-crew-advice-transaction', 'exec'), env)
    env['register']()


def publish_prepared():
    code = checked_text(getsource(transaction.publish_prepared), {
        'release_stack.item_production_advice.pending.json': 'release_stack.crew_equipment_advice.pending.json',
        'vars(transaction)': 'vars(transaction.transaction)',
        'FunctionType(transaction.verify_prepared.__code__, env)':
            'FunctionType(transaction.transaction.verify_prepared.__code__, env)',
        'getsource(transaction.publish_prepared)': 'getsource(transaction.transaction.publish_prepared)',
        'inspect.getsource(transaction.publish_prepared)': 'inspect.getsource(transaction.transaction.publish_prepared)',
    })
    env = environment()
    exec(compile(code, __file__ + '::atomic-crew-advice-publication', 'exec'), env)
    env['publish_prepared']()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    action = parser.add_mutually_exclusive_group(required=True)
    action.add_argument('--register', action='store_true')
    action.add_argument('--publish-prepared', action='store_true')
    (publish_prepared if parser.parse_args().publish_prepared else register)()
