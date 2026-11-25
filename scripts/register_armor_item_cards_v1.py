"""Register the 25 verified armor descriptions and credit each record once."""

import argparse
import inspect
import json
from pathlib import Path
from types import FunctionType

from scripts import register_utility_weapon_item_cards_v1 as previous
from scripts import verify_armor_item_cards_v1 as verify
from scripts.source_locked_derivation_v5118 import checked_text


base, stage, template = previous.base, verify.stage, previous.template
PARENT = previous.RELEASE
PROFILE = 'all-routes-armor-item-cards-editorial-v1-20261111'
FAMILY = 'armor_item_cards_contextual_20261111'
CHECK = 'registered_armor_item_cards_native_live_and_complete_parent_inverse'
PACKAGE = Path('releases/all_routes_editorial_20261111_armor_item_cards_candidate')
VERIFICATION = PACKAGE / 'verification'
RELEASE = VERIFICATION / 'registered_release_verification.json'
REVIEW = VERIFICATION / 'registered_review.json'
MUTATION_PLAN = VERIFICATION / 'registration_mutation_plan.json'
TEST = Path('out/armor_item_cards_registered_20261111_v1')
ROM = TEST / 'Translation_DS_All_Routes_Armor_Item_Cards_20261111_candidate.nds'
MANIFEST = ROM.with_suffix('.manifest.json')
PATCH = PACKAGE / 'translation.xdelta'
DOC = Path('docs/editorial_armor_item_cards_registered_20261111.md')
PENDING_LEDGER = TEST / 'editorial_review_current.armor_item_cards.pending.json'
OUTPUT, EVIDENCE, RESEARCH = stage.OUTPUT, stage.PROOF, stage.ROM
STARTUP_VERIFICATION, CHECKPOINT, LIVE_VERIFICATION, QA = verify.BOOT, verify.CHECKPOINT, verify.LIVE, verify.QA
PREVIOUS_TOTAL, TOTAL, REVISED, RETAINED = 26583, 25, 20, 5


def rebuild(parent, evidence, source):
    return FunctionType(template.rebuild.__code__, vars(template) | globals())(parent, evidence, source)


def final_review(source, evidence, scope):
    return FunctionType(template.final_review.__code__, vars(template) | globals())(source, evidence, scope)


def verification_scope(approved, live):
    assert approved['observed_ids'] == live['observed_ids'] == verify.OBSERVED
    assert approved['stored_records'] == TOTAL and approved['viewed_pages'] == 50
    assert live['original_Items_screen'] and live['returning_to_same_town_screen']
    assert live['complete_description_foreground_and_blank_cells_exact']
    return dict(observed_notice_IDs=verify.OBSERVED, stored_records=TOTAL,
        offline_item_display_modes=100, directly_viewed_pages=50,
        fixture_scope='The native inventory transfer supplied Charles Martel Armor to a copy of the Lisbon save. Original controller and stylus inputs opened and closed Items.',
        original_item_menu_and_town_return=True, actual_resident_description_and_name_fields=True,
        natural_acquisition=False, offline_only_notice_IDs=[n for n in stage.IDS if n not in verify.OBSERVED],
        hardware=False)


def publish(release):
    summary = 'The 25 main armor catalogue descriptions are registered. The ledger now credits 26,608 reviews.'
    tick = chr(96)
    notes = f"""# All Routes Armor Item Cards candidate

Use the local ROM {tick}{ROM.as_posix()}{tick} with its build manifest. The [clean-input patch](translation.xdelta) reconstructs it byte for byte from Japanese ROM SHA-256 {tick}{release['clean_input_sha256']}{tick}. Expected ROM SHA-256 is {tick}{release['candidate_sha256']}{tick}. Patch SHA-256 is {tick}{release['patch_sha256']}{tick}.

{summary} Twenty prose revisions restore details including the Kanem warriors and Minerva's place among the Twelve. Five wordings were retained with individual reasons. Charles Martel Armor now uses an ordinary capital F and keeps the royal comparison without assigning a title to Charles Martel.

Both item views passed all 100 native render cases. All 218 description getters passed, and the original Items menu showed the complete three-row Charles Martel Armor description and returned to Lisbon after an isolated inventory transfer. The other 24 cards in this batch were checked offline. All 89 release checks, 34 targeted tests, cold startup and 24 protected name getters passed. [Gameplay proof](verification/armor_items_gameplay_verification.json) · [Exact record review](verification/registered_review.json)
"""
    (PACKAGE / 'README.md').write_text(notes, encoding='utf-8', newline='\n')
    base.save(PACKAGE / 'checksums.json', {p.relative_to(PACKAGE).as_posix(): base.digest(p)
        for p in sorted(PACKAGE.rglob('*')) if p.is_file() and p.name != 'checksums.json'})
    pin_path = Path('translations/rom_retention_pins.json')
    pins = base.load(pin_path)
    for path, role in ((RESEARCH, 'verified armor-card stage'), (ROM, 'registered armor-card ROM')):
        resolved = str(path.resolve())
        assert not any(row['path'] == resolved for row in pins)
        pins.append(dict(path=resolved, reason=f'Preserve {role}. SHA256 {base.digest(path)}'))
    base.replace_checked(pin_path, (json.dumps(pins, ensure_ascii=False, indent=2) + '\n').replace('\n', '\r\n').encode('utf-8'))
    doc = f"""# Armor item cards registered

{summary} COMMON 2864–2888 agrees with the private descriptions in both Items displays. The review restored source details and fixed the full-width F on Charles Martel Armor. Five wordings were kept with individual reasons. [Registered review](../{REVIEW.as_posix()}) · [Release and patch](../{PACKAGE.as_posix()}/README.md)

The copied allocation stays at 123,264 bytes. Five descriptions fit in a 520-byte extension of the existing resident catalogue. All 218 getters pass, and the other 193 item projections match the predecessor byte for byte. Both item displays passed native and visual checks. A focused emulator replay showed the full Charles Martel Armor card after a one-item inventory transfer and then returned to Lisbon. Cold boot and all 24 protected name getters passed.

Continue with the crew-role equipment beginning at COMMON 2889. The three later armor records at COMMON 3005 and 3010–3011 remain in scope. Confirm item categories against the clean metadata and use the registered item storage and formatter. Options, Market, other player-facing prose and the remaining earlier-name and role-label review stay in scope. Graphics artwork and the older-record technical re-audit remain separate.
"""
    base.replace_checked(DOC, doc.encode('utf-8'))
    lead = f'# Current editorial checkpoint - 2026-11-11\n\n{summary}\n\nContinue from [the registered armor item cards]({DOC.name}).\n\n'
    for name in ('editorial_handoff_current.md', 'editorial_efficiency_workflow.md', 'translation_progress.md'):
        path = Path('docs') / name
        base.replace_checked(path, lead.encode('utf-8') + path.read_bytes())
    continuity = Path('docs/build_continuity_protocol.md')
    protocol = (
        'The 25 armor descriptions are registered over Utility and Weapon Item Cards with 754 entries, '
        f'114 accepted layers and 89 checks. Use {tick}scripts/register_armor_item_cards_v1.py --register{tick} '
        f'and {tick}--publish-prepared{tick}. Preserve the copied allocation and both item-description representations. '
        f'Exact reconstruction, the original Items return and cold startup pass. [Registered checkpoint]({DOC.name})\n\n')
    base.replace_checked(continuity, protocol.encode('utf-8') + continuity.read_bytes())
    print('Registered 754 entries and credited 25 armor reviews once.')


def register():
    ledger = checked_text(inspect.getsource(base.update_ledger), {
        "'diplomatic-and-scheme-outcome-notices'": "'armor-item-cards'",
        'Thirty-four diplomacy and scheme outcomes are registered.': 'Twenty-five armor item descriptions are registered.',
        '== 25985': '== 26608', '== 15438': '== 15877', '== 10547': '== 10731',
    })
    old_scope = """    scope = dict(observed_notice_IDs=approved['live_messages'], stored_cases=176, fresh_viewed_pages=31,
        reused_exact_viewed_pages=145, fixture_scope='One incoming letter in a previously empty isolated RAM slot',
        original_no_preserved_war=True, natural_letter_generation=False, hardware=False)"""
    src = checked_text(inspect.getsource(base.register), {
        "approved['live_messages'] == [349, 356, 352]": "approved['observed_ids'] == live['observed_ids']",
        "sum(int(s.get('tests', 0)) for s in tests) == 27": "sum(int(s.get('tests', 0)) for s in tests) == 34",
        "len(manifest['batches']) == 734 and len(manifest['checks']) == 69":
            "len(manifest['batches']) == 753 and len(manifest['checks']) == 88",
        "evidence['target_ARM9_sha256']": "evidence['research_ARM9_sha256']",
        "evidence['target_COMMON_sha256']": "evidence['research_COMMON_sha256']",
        old_scope: '    scope = verification_scope(approved, live)',
        'release_stack_before_diplomacy.json': 'release_stack_before_armor_item_cards.json',
        'verified_crew_notice_predecessor=predecessor, diplomatic_outcome_release=str(REVIEW)':
            'verified_utility_weapon_item_cards_predecessor=predecessor, armor_item_cards_release=str(REVIEW)',
        'Reviewed diplomacy and scheme outcomes with scoped native phrase wrapping.':
            'Reviewed armor descriptions in both native stores.',
        'release_stack.diplomacy.pending.json': 'release_stack.armor_item_cards.pending.json',
        "LEDGER.with_name('editorial_review_current.diplomacy.pending.json')": 'PENDING_LEDGER',
        '    save(pending_registry, registry)':
            '    preserve_compression(pending_registry, REGISTRY)\n    save(pending_registry, registry)',
        "evidence['wrapper']": "evidence['ownership']",
        'COMMON_DIPLOMATIC_OUTCOMES_MODAL_AND_PHRASE_WRAP': 'ARMOR_ITEM_CARDS_NATIVE_WRAP',
        "manifest['diplomatic_outcomes_registered_successor_pipeline']":
            "manifest['armor_item_cards_registered_successor_pipeline']",
        "len(manifest['batches']) == 735 and len(manifest['checks']) == 70":
            "len(manifest['batches']) == 754 and len(manifest['checks']) == 89",
        'registered_manifest_entries=735, accepted_layers=114, passing_release_checks=70, repository_tests=27':
            'registered_manifest_entries=754, accepted_layers=114, passing_release_checks=89, repository_tests=34',
        '    pending_registry.replace(REGISTRY)\n    try:\n        pending_ledger.replace(LEDGER)\n    except OSError:\n        replace_checked(REGISTRY, before_registry)\n        raise\n    assert digest(REGISTRY) == release[\'registry_sha256\'] and digest(PROMOTED) == promoted\n    publish(release)':
            '    assert digest(PROMOTED) == promoted\n    print("Armor card registration staged and ready to publish.")',
    })
    env = vars(base) | globals() | {
        'preserve_compression': template.template.previous.transaction.preserve_compression,
    }
    exec(compile(ledger + '\n\n' + src, __file__ + '::same-registered-release-transaction', 'exec'), env)
    env['register']()


def publish_prepared():
    source = checked_text(inspect.getsource(previous.publish_prepared), {
        'release_stack.utility_weapon_item_cards.pending.json': 'release_stack.armor_item_cards.pending.json',
    })
    env = vars(previous) | globals()
    exec(compile(source, __file__ + '::same-registered-armor-publication', 'exec'), env)
    env['publish_prepared']()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    action = parser.add_mutually_exclusive_group(required=True)
    action.add_argument('--register', action='store_true')
    action.add_argument('--publish-prepared', action='store_true')
    (publish_prepared if parser.parse_args().publish_prepared else register)()
