"""Register the reviewed weapon and armor advice with the verified release transaction."""

import argparse
from inspect import getsource
import json
from pathlib import Path
from types import FunctionType, SimpleNamespace

from scripts import register_item_production_advice_v1 as previous
from scripts import stage_weapon_armor_advice_v2 as layout
from scripts import verify_weapon_armor_advice_v1 as verification
from scripts.source_locked_derivation_v5118 import checked_text


base = previous.base
stage = SimpleNamespace(**(vars(verification.stage) | vars(layout.first) | vars(layout) | {
    'stage': FunctionType(layout.first.stage_build.__code__, vars(layout.first) | vars(layout)),
}))
PARENT = previous.RELEASE
PROFILE = 'all-routes-weapon-armor-advice-editorial-v1-20261111'
FAMILY = 'weapon_armor_advice_contextual_20261111'
CHECK = 'registered_weapon_armor_advice_native_live_and_complete_parent_inverse'
PACKAGE = Path('releases/all_routes_editorial_20261111_weapon_armor_advice_candidate')
VERIFICATION = PACKAGE / 'verification'
RELEASE = VERIFICATION / 'registered_release_verification.json'
REVIEW = VERIFICATION / 'registered_review.json'
MUTATION_PLAN = VERIFICATION / 'registration_mutation_plan.json'
TEST = Path('out/weapon_armor_advice_registered_20261111_v1')
ROM = TEST / 'Translation_DS_All_Routes_Weapon_Armor_Advice_20261111_candidate.nds'
MANIFEST = ROM.with_suffix('.manifest.json')
PATCH = PACKAGE / 'translation.xdelta'
DOC = Path('docs/editorial_weapon_armor_advice_registered_20261111.md')
PENDING_LEDGER = TEST / 'editorial_review_current.weapon_armor_advice.pending.json'
OUTPUT, EVIDENCE, RESEARCH = stage.OUTPUT, stage.PROOF, stage.ROM
STARTUP_VERIFICATION, CHECKPOINT = verification.BOOT, verification.CHECKPOINT
LIVE_VERIFICATION, QA = verification.LIVE, verification.QA
PREVIOUS_TOTAL, TOTAL, REVISED, RETAINED = 26775, 50, 30, 20


def verification_scope(approved, live):
    assert approved['live_messages'] == live['observed_ids'] == list(verification.OBSERVED)
    assert approved['stored_cases'] == approved['viewed_pages'] == TOTAL
    assert live['original_Advice_button'] and live['original_item_view_restored'] and live['original_town_return']
    assert live['complete_dialogue_ink_and_blank_cells_exact']
    assert all(row['header']['text'] == 'Hans Letzel' for row in live['observed'])
    assert [len(row['body_rows']) for row in live['observed']] == [1, 4]
    return dict(observed_notice_IDs=live['observed_ids'], stored_cases=TOTAL, viewed_pages=TOTAL,
        offline_actor_and_screen_cases=300, offline_native_portrait_cases=100,
        original_Advice_button_item_and_Lisbon_return=True, natural_advice_unlock=False, hardware=False,
        fixture_scope='The original transfer supplied Black Rapier and Charles Martel Armor to a copy '
                      'of the Lisbon save. The original flag setter enabled Advice. Normal controller '
                      'and stylus inputs opened Items, requested and dismissed both Hans portraits, '
                      'switched items and returned to Lisbon.')


def publish(release):
    summary = 'The 50 weapon and armor advice replies are registered. The ledger now credits 26,825 reviews.'
    notes = f"""# All Routes Weapon and Armor Advice candidate

Use [{ROM.name}](../../{ROM.as_posix()}) with its build manifest. The [clean-input patch](translation.xdelta) reconstructs it byte for byte from the clean Japanese ROM with SHA-256 '{release['clean_input_sha256']}'. Expected ROM SHA-256 is '{release['candidate_sha256']}'. Patch SHA-256 is '{release['patch_sha256']}'.

{summary} Thirty revisions and twenty justified retentions cover the full weapon and armor advice categories. The dialogue uses the game’s Boarding Leader title, preserves the legendary character of Lohengrin’s story, distinguishes Gentian from its item title, and restores the adviser’s shifts between practical recommendations and delight at a rare find. Common replies retain the same wording where the source repeats it.

All 50 final native pages passed visual review. All 100 portrait cases and 300 original caller-fragment cases passed offline. A focused replay showed Hans’s one-row Black Rapier and four-row Charles Martel Armor replies, returned to the same Items view after each, then returned to Lisbon. The copied save used isolated inventory and Advice flag fixtures. The other replies and Mikhail’s branch were checked offline. All 95 release checks, 34 targeted tests, the 31,000-frame cold boot and 24 protected name getters passed. [Gameplay proof](verification/weapon_armor_advice_gameplay_verification.json) · [Exact record review](verification/registered_review.json)
"""
    (PACKAGE / 'README.md').write_text(notes, encoding='utf-8', newline='\n')
    base.save(PACKAGE / 'checksums.json', {p.relative_to(PACKAGE).as_posix(): base.digest(p)
        for p in sorted(PACKAGE.rglob('*')) if p.is_file() and p.name != 'checksums.json'})
    pin_path = Path('translations/rom_retention_pins.json')
    pins = base.load(pin_path)
    for path in (layout.first.ROM, RESEARCH, ROM):
        resolved = str(path.resolve())
        assert not any(row['path'] == resolved for row in pins)
        pins.append(dict(path=resolved, reason=f'Preserve the weapon and armor advice build. SHA256 {base.digest(path)}'))
    base.replace_checked(pin_path, (json.dumps(pins, ensure_ascii=False, indent=2) + '\n').replace('\n', '\r\n').encode('utf-8'))
    doc = f"""# Weapon and armor advice registered

{summary} COMMON 3057–3106 covers all 25 weapons and 25 armor pieces. The Gallery, compact item screen and regular Items continue selecting the original actor and message by index. The role name Boarding Leader matches the item and crew interfaces. [Registered review](../{REVIEW.as_posix()}) · [Release and patch](../{PACKAGE.as_posix()}/README.md)

Only COMMON block 34 and the guarded portrait selector changed. All other selected COMMON spans and the 123,264-byte copied allocation remain exact. Both native actors produce the same body for each item. The Lisbon replay verifies the first and last glyphs on one- and four-row portraits and shows the normal transition after each.

Continue at COMMON 3107 with crew equipment, then figureheads, gifts, Proofs and map advice. Reuse the verified original caller and portrait behavior where dependencies match. Test all changed text and use focused gameplay for distinct display behavior or concrete remaining risks. Graphics artwork and the older-record technical re-audit remain separate.
"""
    base.replace_checked(DOC, doc.encode('utf-8'))
    lead = f'# Current editorial checkpoint - 2026-11-11\n\n{summary}\n\nContinue from [the registered weapon and armor advice]({DOC.name}).\n\n'
    for name in ('editorial_handoff_current.md', 'editorial_efficiency_workflow.md', 'translation_progress.md'):
        path = Path('docs') / name
        base.replace_checked(path, lead.encode('utf-8') + path.read_bytes())
    continuity = Path('docs/build_continuity_protocol.md')
    protocol = (
        'The 50 weapon and armor replies are registered over Item Production Advice with '
        '760 entries, 114 accepted layers and 95 checks. Use scripts/register_weapon_armor_advice_v1.py '
        f'with --register and --publish-prepared. Exact reconstruction, the two Lisbon Advice portraits '
        f'and cold startup pass. [Registered checkpoint]({DOC.name})\n\n')
    base.replace_checked(continuity, protocol.encode('utf-8') + continuity.read_bytes())
    print('Registered 760 entries and credited 50 weapon and armor advice reviews once.')


def environment():
    env = vars(previous) | globals()
    env['rebuild'] = FunctionType(previous.rebuild.__code__, env)
    env['final_review'] = FunctionType(previous.final_review.__code__, env)
    return env


def register():
    code = checked_text(getsource(previous.register), {
        "'item-production-and-voyage-advice'": "'weapon-and-armor-advice'",
        'Twenty-four item advice replies are registered.': 'Fifty weapon and armor advice replies are registered.',
        '== 26775': '== 26825', '== 16001': '== 16031', '== 10774': '== 10794',
        "== 758 and len(manifest['checks']) == 93": "== 759 and len(manifest['checks']) == 94",
        'release_stack_before_item_production_advice.json': 'release_stack_before_weapon_armor_advice.json',
        'verified_promotional_item_cards_predecessor=predecessor, item_production_advice_release=str(REVIEW)':
            'verified_item_production_advice_predecessor=predecessor, weapon_armor_advice_release=str(REVIEW)',
        'Reviewed item production and voyage-supply advice with scoped portrait wraps.':
            'Reviewed weapon and armor advice with scoped portrait wraps.',
        'release_stack.item_production_advice.pending.json': 'release_stack.weapon_armor_advice.pending.json',
        'COMMON_ITEM_PRODUCTION_ADVICE_PORTRAIT_WRAP': 'COMMON_WEAPON_ARMOR_ADVICE_PORTRAIT_WRAP',
        "manifest['item_production_advice_registered_successor_pipeline']":
            "manifest['weapon_armor_advice_registered_successor_pipeline']",
        "== 759 and len(manifest['checks']) == 94": "== 760 and len(manifest['checks']) == 95",
        'registered_manifest_entries=759, accepted_layers=114, passing_release_checks=94, repository_tests=34':
            'registered_manifest_entries=760, accepted_layers=114, passing_release_checks=95, repository_tests=34',
        'Item advice registration staged and ready to publish.':
            'Weapon and armor advice registration staged and ready to publish.',
        'live_check.verified.VISUAL': 'verification.VISUAL',
    })
    env = environment()
    exec(compile(code, __file__ + '::registered-weapon-armor-transaction', 'exec'), env)
    env['register']()


def publish_prepared():
    code = checked_text(getsource(previous.publish_prepared), {
        'release_stack.item_production_advice.pending.json': 'release_stack.weapon_armor_advice.pending.json',
    })
    env = environment()
    exec(compile(code, __file__ + '::atomic-weapon-armor-publication', 'exec'), env)
    env['publish_prepared']()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    action = parser.add_mutually_exclusive_group(required=True)
    action.add_argument('--register', action='store_true')
    action.add_argument('--publish-prepared', action='store_true')
    (publish_prepared if parser.parse_args().publish_prepared else register)()
