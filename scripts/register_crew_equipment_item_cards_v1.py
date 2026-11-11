"""Register the 40 verified crew-role equipment descriptions and their coverage."""

import argparse
import inspect
import json
from pathlib import Path
from types import FunctionType, SimpleNamespace

from scripts import register_armor_item_cards_v1 as previous
from scripts import register_sea_event_review_v2 as transaction
from scripts import verify_crew_equipment_item_cards_v1 as verify
from scripts.source_locked_derivation_v5118 import checked_text

base, template = previous.base, previous.template
stage = SimpleNamespace(**(vars(verify.stage) | vars(verify.current)))
PARENT = previous.RELEASE
PROFILE = 'all-routes-crew-equipment-item-cards-editorial-v1-20261111'
FAMILY = 'crew_equipment_item_cards_contextual_20261111'
CHECK = 'registered_crew_equipment_item_cards_native_live_and_complete_parent_inverse'
PACKAGE = Path('releases/all_routes_editorial_20261111_crew_equipment_item_cards_candidate')
VERIFICATION = PACKAGE / 'verification'
RELEASE = VERIFICATION / 'registered_release_verification.json'
REVIEW = VERIFICATION / 'registered_review.json'
MUTATION_PLAN = VERIFICATION / 'registration_mutation_plan.json'
TEST = Path('out/crew_equipment_item_cards_registered_20261111_v1')
ROM = TEST / 'Translation_DS_All_Routes_Crew_Equipment_Item_Cards_20261111_candidate.nds'
MANIFEST = ROM.with_suffix('.manifest.json')
PATCH = PACKAGE / 'translation.xdelta'
DOC = Path('docs/editorial_crew_equipment_item_cards_registered_20261111.md')
PENDING_LEDGER = TEST / 'editorial_review_current.crew_equipment_item_cards.pending.json'
OUTPUT, EVIDENCE, RESEARCH = stage.OUTPUT, stage.PROOF, stage.ROM
STARTUP_VERIFICATION, CHECKPOINT, LIVE_VERIFICATION, QA = verify.BOOT, verify.CHECKPOINT, verify.LIVE, verify.QA
PREVIOUS_TOTAL, TOTAL, REVISED, RETAINED = 26608, 40, 32, 8


def rebuild(parent, evidence, source):
    return FunctionType(template.rebuild.__code__, vars(template) | globals())(parent, evidence, source)


def final_review(source, evidence, scope):
    return FunctionType(template.final_review.__code__, vars(template) | globals())(source, evidence, scope)


def verification_scope(approved, live):
    assert approved['observed_ids'] == live['observed_ids'] == verify.OBSERVED
    assert approved['stored_records'] == TOTAL and approved['viewed_pages'] == 80
    assert live['original_Items_screen'] and live['returning_to_same_town_screen']
    assert live['complete_description_foreground_and_blank_cells_exact']
    assert len(live['role_index_to_rendered_label']) == 16 and not live['inventory_fixture']
    return dict(observed_notice_IDs=verify.OBSERVED, stored_records=TOTAL,
        offline_item_display_modes=160, directly_viewed_pages=80, offline_native_roles=16,
        original_item_menu_and_town_return=True, actual_First_Mate_label_and_description=True,
        original_battery_save_unchanged=True, inventory_fixture=False,
        offline_only_notice_IDs=[n for n in stage.IDS if n not in verify.OBSERVED], hardware=False)


def publish(release):
    summary = 'The 40 crew-role equipment descriptions are registered. The ledger now credits 26,648 reviews.'
    tick = chr(96)
    notes = f"""# All Routes Crew Equipment Item Cards candidate

Use the local ROM {tick}{ROM.as_posix()}{tick} with its build manifest. The [clean-input patch](translation.xdelta) reconstructs it byte for byte from Japanese ROM SHA-256 {tick}{release['clean_input_sha256']}{tick}. Expected ROM SHA-256 is {tick}{release['candidate_sha256']}{tick}. Patch SHA-256 is {tick}{release['patch_sha256']}{tick}.

{summary} Thirty-two revisions restore source details, use the established Livestock Room label and fix the full-width capital I on Da Vinci Anatomy. Eight wordings were retained with individual reasons. Both item views passed 160 native render cases, including all 16 crew-role labels. All 218 description getters passed.

The original Lisbon save already held Travels of Marco Polo. The emulator replay showed the complete revised description and First Mate label, then returned to Lisbon. The other 39 cards were checked offline. All 90 release checks, 34 targeted tests, cold startup and 24 protected name getters passed. [Gameplay proof](verification/crew_equipment_items_gameplay_verification.json) · [Exact record review](verification/registered_review.json)
"""
    (PACKAGE / 'README.md').write_text(notes, encoding='utf-8', newline='\n')
    base.save(PACKAGE / 'checksums.json', {p.relative_to(PACKAGE).as_posix(): base.digest(p)
        for p in sorted(PACKAGE.rglob('*')) if p.is_file() and p.name != 'checksums.json'})
    pin_path = Path('translations/rom_retention_pins.json')
    pins = base.load(pin_path)
    for path, role in ((RESEARCH, 'verified crew-equipment stage'), (ROM, 'registered crew-equipment ROM')):
        resolved = str(path.resolve())
        assert not any(row['path'] == resolved for row in pins)
        pins.append(dict(path=resolved, reason=f'Preserve {role}. SHA256 {base.digest(path)}'))
    base.replace_checked(pin_path, (json.dumps(pins, ensure_ascii=False, indent=2) + '\n').replace('\n', '\r\n').encode('utf-8'))
    doc = f"""# Crew-role equipment cards registered

{summary} COMMON 2889–2928 matches the private item paragraphs in both item views. The review restored details such as what Marco Polo saw and heard, aligned the Livestock Room wording and fixed the full-width I on Da Vinci Anatomy. [Registered review](../{REVIEW.as_posix()}) · [Release and patch](../{PACKAGE.as_posix()}/README.md)

All 160 native cases, 80 visual previews, 16 native crew-role labels and 218 description getters passed. The original Items replay displayed Travels of Marco Polo with its First Mate label and returned to Lisbon using a copy of the original save. The 178 other item projections remain byte-identical. The main copied allocation stays at 123,264 bytes and eight descriptions use 840 bytes appended to the resident catalogue.

Continue with figureheads beginning at COMMON 2929. Reuse the prior credit and exact wording for Shachihoko at COMMON 2931. Later crew-equipment, armor and weapon records remain in scope. Continue the remaining player-facing prose and earlier speaker names and role labels. Graphics artwork and the older-record technical re-audit remain separate.
"""
    base.replace_checked(DOC, doc.encode('utf-8'))
    lead = f'# Current editorial checkpoint - 2026-11-11\n\n{summary}\n\nContinue from [the registered crew-role equipment cards]({DOC.name}).\n\n'
    for name in ('editorial_handoff_current.md', 'editorial_efficiency_workflow.md', 'translation_progress.md'):
        path = Path('docs') / name
        base.replace_checked(path, lead.encode('utf-8') + path.read_bytes())
    continuity = Path('docs/build_continuity_protocol.md')
    protocol = (
        'The 40 crew-role equipment descriptions are registered over Armor Item Cards with 755 entries, '
        f'114 accepted layers and 90 checks. Use {tick}scripts/register_crew_equipment_item_cards_v1.py --register{tick} '
        f'and {tick}--publish-prepared{tick}. Keep the copied allocation and both item-description representations. '
        f'Exact reconstruction, the original Items return and cold startup pass. [Registered checkpoint]({DOC.name})\n\n')
    base.replace_checked(continuity, protocol.encode('utf-8') + continuity.read_bytes())
    print('Registered 755 entries and credited 40 crew-equipment reviews once.')


def register():
    ledger = checked_text(inspect.getsource(base.update_ledger), {
        "'diplomatic-and-scheme-outcome-notices'": "'crew-equipment-item-cards'",
        'Thirty-four diplomacy and scheme outcomes are registered.': 'Forty crew-role equipment descriptions are registered.',
        '== 25985': '== 26648', '== 15438': '== 15909', '== 10547': '== 10739',
    })
    old_scope = """    scope = dict(observed_notice_IDs=approved['live_messages'], stored_cases=176, fresh_viewed_pages=31,
        reused_exact_viewed_pages=145, fixture_scope='One incoming letter in a previously empty isolated RAM slot',
        original_no_preserved_war=True, natural_letter_generation=False, hardware=False)"""
    src = checked_text(inspect.getsource(base.register), {
        "approved['live_messages'] == [349, 356, 352]": "approved['observed_ids'] == live['observed_ids']",
        "sum(int(s.get('tests', 0)) for s in tests) == 27": "sum(int(s.get('tests', 0)) for s in tests) == 34",
        "len(manifest['batches']) == 734 and len(manifest['checks']) == 69":
            "len(manifest['batches']) == 754 and len(manifest['checks']) == 89",
        "evidence['target_ARM9_sha256']": "evidence['research_ARM9_sha256']",
        "evidence['target_COMMON_sha256']": "evidence['research_COMMON_sha256']",
        old_scope: '    scope = verification_scope(approved, live)',
        'release_stack_before_diplomacy.json': 'release_stack_before_crew_equipment_item_cards.json',
        'verified_crew_notice_predecessor=predecessor, diplomatic_outcome_release=str(REVIEW)':
            'verified_armor_item_cards_predecessor=predecessor, crew_equipment_item_cards_release=str(REVIEW)',
        'Reviewed diplomacy and scheme outcomes with scoped native phrase wrapping.':
            'Reviewed crew-role equipment descriptions in both native stores.',
        'release_stack.diplomacy.pending.json': 'release_stack.crew_equipment_item_cards.pending.json',
        "LEDGER.with_name('editorial_review_current.diplomacy.pending.json')": 'PENDING_LEDGER',
        '    save(pending_registry, registry)':
            '    preserve_compression(pending_registry, REGISTRY)\n    save(pending_registry, registry)',
        "evidence['wrapper']": "evidence['ownership']",
        'COMMON_DIPLOMATIC_OUTCOMES_MODAL_AND_PHRASE_WRAP': 'CREW_EQUIPMENT_ITEM_CARDS_NATIVE_WRAP',
        "manifest['diplomatic_outcomes_registered_successor_pipeline']":
            "manifest['crew_equipment_item_cards_registered_successor_pipeline']",
        "len(manifest['batches']) == 735 and len(manifest['checks']) == 70":
            "len(manifest['batches']) == 755 and len(manifest['checks']) == 90",
        'registered_manifest_entries=735, accepted_layers=114, passing_release_checks=70, repository_tests=27':
            'registered_manifest_entries=755, accepted_layers=114, passing_release_checks=90, repository_tests=34',
        '    pending_registry.replace(REGISTRY)\n    try:\n        pending_ledger.replace(LEDGER)\n    except OSError:\n        replace_checked(REGISTRY, before_registry)\n        raise\n    assert digest(REGISTRY) == release[\'registry_sha256\'] and digest(PROMOTED) == promoted\n    publish(release)':
            '    assert digest(PROMOTED) == promoted\n    print("Crew-equipment card registration staged and ready to publish.")',
    })
    env = vars(base) | globals() | {
        'preserve_compression': transaction.preserve_compression,
    }
    exec(compile(ledger + '\n\n' + src, __file__ + '::same-registered-release-transaction', 'exec'), env)
    env['register']()


def publish_prepared():
    env = vars(transaction) | globals() | {'prior': base}
    env['verify_prepared'] = FunctionType(transaction.verify_prepared.__code__, env)
    code = checked_text(inspect.getsource(transaction.publish_prepared), {
        'release_stack.sea_events.pending.json': 'release_stack.crew_equipment_item_cards.pending.json',
    })
    exec(compile(code, __file__ + '::atomic-crew-equipment-publication', 'exec'), env)
    env['publish_prepared']()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    action = parser.add_mutually_exclusive_group(required=True)
    action.add_argument('--register', action='store_true')
    action.add_argument('--publish-prepared', action='store_true')
    (publish_prepared if parser.parse_args().publish_prepared else register)()
