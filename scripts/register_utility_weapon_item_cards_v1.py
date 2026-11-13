"""Register the verified utility item and weapon card descriptions."""

import argparse
import inspect
import json
from pathlib import Path
from types import FunctionType

from scripts import register_source_item_cards_and_coin_v1 as template
from scripts import verify_utility_weapon_item_cards_v1 as verify
from scripts.source_locked_derivation_v5118 import checked_text


base, stage = template.base, verify.stage
PARENT = template.RELEASE
PROFILE = 'all-routes-utility-weapon-item-cards-editorial-v1-20261111'
FAMILY = 'utility_weapon_item_cards_contextual_20261111'
CHECK = 'registered_utility_weapon_item_cards_native_live_and_complete_parent_inverse'
PACKAGE = Path('releases/all_routes_editorial_20261111_utility_weapon_item_cards_candidate')
VERIFICATION = PACKAGE / 'verification'
RELEASE = VERIFICATION / 'registered_release_verification.json'
REVIEW = VERIFICATION / 'registered_review.json'
MUTATION_PLAN = VERIFICATION / 'registration_mutation_plan.json'
TEST = Path('out/utility_weapon_item_cards_registered_20261111_v1')
ROM = TEST / 'Translation_DS_All_Routes_Utility_Weapon_Item_Cards_20261111_candidate.nds'
MANIFEST = ROM.with_suffix('.manifest.json')
PATCH = PACKAGE / 'translation.xdelta'
DOC = Path('docs/editorial_utility_weapon_item_cards_registered_20261111.md')
PENDING_LEDGER = TEST / 'editorial_review_current.utility_weapon_item_cards.pending.json'
OUTPUT, EVIDENCE, RESEARCH = stage.OUTPUT, stage.PROOF, stage.ROM
STARTUP_VERIFICATION, CHECKPOINT, LIVE_VERIFICATION, QA = verify.BOOT, verify.CHECKPOINT, verify.LIVE, verify.QA
PREVIOUS_TOTAL, TOTAL, REVISED, RETAINED = 26554, 29, 21, 8


def rebuild(parent, evidence, source):
    return FunctionType(template.rebuild.__code__, vars(template) | globals())(parent, evidence, source)


def final_review(source, evidence, scope):
    return FunctionType(template.final_review.__code__, vars(template) | globals())(source, evidence, scope)


def verification_scope(approved, live):
    assert approved['observed_ids'] == live['observed_ids'] == verify.OBSERVED
    assert approved['stored_records'] == TOTAL and approved['viewed_pages'] == 58
    assert live['original_Items_screen'] and live['returning_to_same_town_screen']
    assert live['complete_description_foreground_and_blank_cells_exact']
    return dict(observed_notice_IDs=verify.OBSERVED, stored_records=TOTAL,
        offline_item_display_modes=116, directly_viewed_pages=58,
        fixture_scope='The native inventory transfer supplied Black Rapier to a copy of the Lisbon save. Original controller and stylus inputs opened and closed Items.',
        original_item_menu_and_town_return=True, actual_resident_description_and_name_fields=True,
        natural_acquisition=False, offline_only_notice_IDs=[n for n in stage.IDS if n not in verify.OBSERVED],
        hardware=False)


def publish(release):
    summary = 'The four utility item and 25 weapon descriptions are registered. The ledger now credits 26,583 reviews.'
    tick = chr(96)
    notes = f"""# All Routes Utility and Weapon Item Cards candidate

Use the local ROM {tick}{ROM.as_posix()}{tick} with its build manifest. The [clean-input patch](translation.xdelta) reconstructs it byte for byte from Japanese ROM SHA-256 {tick}{release['clean_input_sha256']}{tick}. Expected ROM SHA-256 is {tick}{release['candidate_sha256']}{tick}. Patch SHA-256 is {tick}{release['patch_sha256']}{tick}.

{summary} The 21 prose revisions restore details including Hermes and Ares among the Twelve and Hua Tuo's role in devising the tonic's recipe. Eight wordings were retained with individual reasons. Azure Talwar now uses the ordinary capital I in both stored descriptions. The final visual pass kept phrases such as “no known reason,” “Aztec water god” and “this superb greatsword” together.

All 116 native render cases and 218 description getters passed. The original Items menu showed the complete Black Rapier card and returned to Lisbon after an isolated inventory transfer. The other 28 new cards were checked offline. All 88 release checks, 34 targeted tests, cold startup and 24 protected name getters passed. [Gameplay proof](verification/utility_weapon_items_gameplay_verification.json) · [Exact record review](verification/registered_review.json)
"""
    (PACKAGE / 'README.md').write_text(notes, encoding='utf-8', newline='\n')
    base.save(PACKAGE / 'checksums.json', {p.relative_to(PACKAGE).as_posix(): base.digest(p)
        for p in sorted(PACKAGE.rglob('*')) if p.is_file() and p.name != 'checksums.json'})
    pin_path = Path('translations/rom_retention_pins.json')
    pins = base.load(pin_path)
    for path, role in ((stage.initial.ROM, 'first utility and weapon card layout'),
                       (RESEARCH, 'final utility and weapon card layout'),
                       (ROM, 'registered utility and weapon item candidate')):
        resolved = str(path.resolve())
        assert not any(row['path'] == resolved for row in pins)
        pins.append(dict(path=resolved, reason=f'Preserve {role}. SHA256 {base.digest(path)}'))
    base.replace_checked(pin_path, (json.dumps(pins, ensure_ascii=False, indent=2) + '\n').replace('\n', '\r\n').encode('utf-8'))
    doc = f"""# Utility and weapon item cards registered

{summary} COMMON 2835–2863 matches the private descriptions in the main Items menu and standalone card. Eight wordings were retained. The Azure Talwar's full-width I was corrected. The second visual pass refined seven cards, including the Hua Tuo recipe and the “no known reason” and “Aztec water god” phrase breaks. [Registered review](../{REVIEW.as_posix()}) · [Release and patch](../{PACKAGE.as_posix()}/README.md)

The main copied allocation remains 123,264 bytes. Three descriptions use a 300-byte extension in the existing resident section. The final build passed all 116 native renders, all 218 native lookups and the original Lisbon Items return after a one-item inventory transfer. The 189 other item projections remained byte-identical. Cold boot and 24 name getters passed. The clean-input patch reconstructs the ROM byte for byte.

Continue with the armor descriptions beginning at COMMON 2864. Rebind the item paragraph and free spans to the current pointers. Options, Market, remaining player-facing prose, and earlier names and role labels remain in the editorial scope. Graphics artwork and the older-record technical re-audit remain separate.
"""
    base.replace_checked(DOC, doc.encode('utf-8'))
    lead = f'# Current editorial checkpoint - 2026-11-11\n\n{summary}\n\nContinue from [the registered utility and weapon item cards]({DOC.name}).\n\n'
    for name in ('editorial_handoff_current.md', 'editorial_efficiency_workflow.md', 'translation_progress.md'):
        path = Path('docs') / name
        base.replace_checked(path, lead.encode('utf-8') + path.read_bytes())
    continuity = Path('docs/build_continuity_protocol.md')
    protocol = (
        'The 29 utility and weapon item descriptions are registered over Source Item Cards and Coin with 753 entries, '
        f'114 accepted layers and 88 checks. Use {tick}scripts/register_utility_weapon_item_cards_v1.py --register{tick} '
        f'and {tick}--publish-prepared{tick}. Preserve the copied allocation and both item-description representations. '
        f'Exact reconstruction, the original Items return and cold startup pass. [Registered checkpoint]({DOC.name})\n\n')
    base.replace_checked(continuity, protocol.encode('utf-8') + continuity.read_bytes())
    print('Registered 753 entries and credited 29 utility and weapon card reviews once.')


def register():
    ledger = checked_text(inspect.getsource(base.update_ledger), {
        "'diplomatic-and-scheme-outcome-notices'": "'utility-and-weapon-item-cards'",
        'Thirty-four diplomacy and scheme outcomes are registered.': 'Twenty-nine utility and weapon item descriptions are registered.',
        '== 25985': '== 26583', '== 15438': '== 15857', '== 10547': '== 10726',
    })
    old_scope = """    scope = dict(observed_notice_IDs=approved['live_messages'], stored_cases=176, fresh_viewed_pages=31,
        reused_exact_viewed_pages=145, fixture_scope='One incoming letter in a previously empty isolated RAM slot',
        original_no_preserved_war=True, natural_letter_generation=False, hardware=False)"""
    src = checked_text(inspect.getsource(base.register), {
        "approved['live_messages'] == [349, 356, 352]": "approved['observed_ids'] == live['observed_ids']",
        "sum(int(s.get('tests', 0)) for s in tests) == 27": "sum(int(s.get('tests', 0)) for s in tests) == 34",
        "len(manifest['batches']) == 734 and len(manifest['checks']) == 69":
            "len(manifest['batches']) == 752 and len(manifest['checks']) == 87",
        "evidence['target_ARM9_sha256']": "evidence['research_ARM9_sha256']",
        "evidence['target_COMMON_sha256']": "evidence['research_COMMON_sha256']",
        old_scope: '    scope = verification_scope(approved, live)',
        'release_stack_before_diplomacy.json': 'release_stack_before_utility_weapon_item_cards.json',
        'verified_crew_notice_predecessor=predecessor, diplomatic_outcome_release=str(REVIEW)':
            'verified_source_item_cards_predecessor=predecessor, utility_weapon_item_cards_release=str(REVIEW)',
        'Reviewed diplomacy and scheme outcomes with scoped native phrase wrapping.':
            'Reviewed utility and weapon descriptions in both native stores.',
        'release_stack.diplomacy.pending.json': 'release_stack.utility_weapon_item_cards.pending.json',
        "LEDGER.with_name('editorial_review_current.diplomacy.pending.json')": 'PENDING_LEDGER',
        '    save(pending_registry, registry)':
            '    preserve_compression(pending_registry, REGISTRY)\n    save(pending_registry, registry)',
        "evidence['wrapper']": "evidence['ownership']",
        'COMMON_DIPLOMATIC_OUTCOMES_MODAL_AND_PHRASE_WRAP': 'UTILITY_WEAPON_ITEM_CARDS_NATIVE_WRAP',
        "manifest['diplomatic_outcomes_registered_successor_pipeline']":
            "manifest['utility_weapon_item_cards_registered_successor_pipeline']",
        "len(manifest['batches']) == 735 and len(manifest['checks']) == 70":
            "len(manifest['batches']) == 753 and len(manifest['checks']) == 88",
        'registered_manifest_entries=735, accepted_layers=114, passing_release_checks=70, repository_tests=27':
            'registered_manifest_entries=753, accepted_layers=114, passing_release_checks=88, repository_tests=34',
        '    pending_registry.replace(REGISTRY)\n    try:\n        pending_ledger.replace(LEDGER)\n    except OSError:\n        replace_checked(REGISTRY, before_registry)\n        raise\n    assert digest(REGISTRY) == release[\'registry_sha256\'] and digest(PROMOTED) == promoted\n    publish(release)':
            '    assert digest(PROMOTED) == promoted\n    print("Utility and weapon item registration staged and ready to publish.")',
    })
    env = vars(base) | globals() | {
        'preserve_compression': template.template.previous.transaction.preserve_compression,
    }
    exec(compile(ledger + '\n\n' + src, __file__ + '::same-registered-release-transaction', 'exec'), env)
    env['register']()


def publish_prepared():
    source = checked_text(inspect.getsource(template.template.publish_prepared), {
        'release_stack.rumor_and_cooperation.pending.json': 'release_stack.utility_weapon_item_cards.pending.json',
    })
    env = vars(template.template) | globals()
    exec(compile(source, __file__ + '::same-registered-publication', 'exec'), env)
    env['publish_prepared']()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    action = parser.add_mutually_exclusive_group(required=True)
    action.add_argument('--register', action='store_true')
    action.add_argument('--publish-prepared', action='store_true')
    (publish_prepared if parser.parse_args().publish_prepared else register)()
