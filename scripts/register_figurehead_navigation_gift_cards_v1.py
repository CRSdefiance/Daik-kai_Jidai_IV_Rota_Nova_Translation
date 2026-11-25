"""Register the verified figurehead, navigation and gift descriptions."""

import argparse
import inspect
import json
from pathlib import Path
from types import FunctionType

from dk4tool.patch.duel_editorial import owned_entries
from dk4tool.script.common_message_table import DIRECTORY_OFFSET, TABLE_OFFSET
from scripts import register_crew_equipment_item_cards_v1 as previous
from scripts import register_sea_event_review_v2 as transaction
from scripts import verify_figurehead_navigation_gift_cards_v1 as verify
from scripts.source_locked_derivation_v5118 import checked_text

base, template, stage = previous.base, previous.template, verify.stage
PARENT = previous.RELEASE
PROFILE = 'all-routes-figurehead-navigation-gift-cards-editorial-v1-20261111'
FAMILY = 'figurehead_navigation_gift_cards_contextual_20261111'
CHECK = 'registered_figurehead_navigation_gift_cards_native_live_and_complete_parent_inverse'
PACKAGE = Path('releases/all_routes_editorial_20261111_figurehead_navigation_gift_cards_candidate')
VERIFICATION = PACKAGE / 'verification'
RELEASE = VERIFICATION / 'registered_release_verification.json'
REVIEW = VERIFICATION / 'registered_review.json'
MUTATION_PLAN = VERIFICATION / 'registration_mutation_plan.json'
TEST = Path('out/figurehead_navigation_gift_cards_registered_20261111_v1')
ROM = TEST / 'Translation_DS_All_Routes_Figurehead_Navigation_Gift_Cards_20261111_candidate.nds'
MANIFEST = ROM.with_suffix('.manifest.json')
PATCH = PACKAGE / 'translation.xdelta'
DOC = Path('docs/editorial_figurehead_navigation_gift_cards_registered_20261111.md')
PENDING_LEDGER = TEST / 'editorial_review_current.figurehead_navigation_gift_cards.pending.json'
OUTPUT, EVIDENCE, RESEARCH = stage.OUTPUT, stage.PROOF, stage.ROM
STARTUP_VERIFICATION, CHECKPOINT, LIVE_VERIFICATION, QA = verify.BOOT, verify.CHECKPOINT, verify.LIVE, verify.QA
PREVIOUS_TOTAL, TOTAL, REVISED, RETAINED = 26648, 33, 21, 12


def rebuild(parent, evidence, source):
    arm, common = FunctionType(template.rebuild.__code__, vars(template) | globals())(parent, evidence, source)
    original = base.NdsImage.open(parent['candidate'])
    original_arm = original.read_file(base.ARM)
    old, new = (
        owned_entries(data, code, stage.sha256(code[DIRECTORY_OFFSET:TABLE_OFFSET]).hexdigest())[2931].text
        for code, data in ((original_arm, original.read_file(base.COMMON)), (arm, common))
    )
    assert new == old
    assert 2931 not in stage.IDS
    assert evidence['ownership']['preserved_Shachihoko']['message_ID'] == 2931
    return arm, common


def final_review(source, evidence, scope):
    return FunctionType(template.final_review.__code__, vars(template) | globals())(source, evidence, scope)


def verification_scope(approved, live):
    assert approved['observed_ids'] == live['observed_ids'] == verify.OBSERVED
    assert approved['stored_records'] == TOTAL and approved['viewed_pages'] == 66
    assert live['original_Items_screen'] and live['returning_to_same_town_screen']
    assert live['complete_description_foreground_and_blank_cells_exact']
    assert live['original_sextant_already_held'] and len(live['observed']) == 3
    return dict(observed_notice_IDs=verify.OBSERVED, stored_records=TOTAL,
        offline_item_display_modes=132, directly_viewed_pages=66,
        original_item_menu_and_town_return=True, original_sextant_already_held=True,
        fixture_scope='The native inventory transfer supplied Eagle Figurehead and Frozen Rose to a copy of the Lisbon save. The save already held the Sextant. Original controller and stylus inputs navigated Items.',
        original_battery_save_unchanged=True, normal_acquisition_verified=False,
        offline_only_notice_IDs=[n for n in stage.IDS if n not in verify.OBSERVED],
        previous_Shachihoko_review_reused_without_duplicate_credit=True, hardware=False)


def publish(release):
    summary = 'The figurehead, navigation and gift batch is registered. The ledger now credits 26,681 reviews.'
    tick = chr(96)
    notes = f"""# All Routes Figurehead, Navigation and Gift Cards candidate

Use the local ROM {tick}{ROM.as_posix()}{tick} with its build manifest. The [clean-input patch](translation.xdelta) reconstructs it byte for byte from Japanese ROM SHA-256 {tick}{release['clean_input_sha256']}{tick}. Expected ROM SHA-256 is {tick}{release['candidate_sha256']}{tick}. Patch SHA-256 is {tick}{release['patch_sha256']}{tick}.

{summary} The 33 new reviews comprise nine figureheads, three navigation instruments and 21 gifts. Twenty-one descriptions were revised and 12 wordings were retained with individual reasons. The full-width capital I on Shakuntala was corrected. Shachihoko's existing review, pointer and descriptions were preserved.

Both item views passed 132 native render cases, 66 visual previews and all 218 description getters. The original Items replay showed Eagle Figurehead, Sextant and Frozen Rose, then returned to Lisbon. The save already held the Sextant, and an isolated inventory transfer supplied the other two. The other 30 cards were checked offline. All 91 release checks, 34 targeted tests, cold startup and 24 protected name getters passed. [Gameplay proof](verification/figurehead_navigation_gift_gameplay_verification.json) · [Exact record review](verification/registered_review.json)
"""
    (PACKAGE / 'README.md').write_text(notes, encoding='utf-8', newline='\n')
    base.save(PACKAGE / 'checksums.json', {p.relative_to(PACKAGE).as_posix(): base.digest(p)
        for p in sorted(PACKAGE.rglob('*')) if p.is_file() and p.name != 'checksums.json'})
    pin_path = Path('translations/rom_retention_pins.json')
    pins = base.load(pin_path)
    for path, role in ((RESEARCH, 'verified figurehead, navigation and gift stage'),
                       (ROM, 'registered figurehead, navigation and gift ROM')):
        resolved = str(path.resolve())
        assert not any(row['path'] == resolved for row in pins)
        pins.append(dict(path=resolved, reason=f'Preserve {role}. SHA256 {base.digest(path)}'))
    base.replace_checked(pin_path, (json.dumps(pins, ensure_ascii=False, indent=2) + '\n').replace('\n', '\r\n').encode('utf-8'))
    doc = f"""# Figurehead, navigation and gift cards registered

{summary} COMMON 2929–2962 now has contextual review coverage. Shachihoko at COMMON 2931 retained its earlier coverage and both text representations. The new batch adds 21 revisions and 12 individual retentions. [Registered review](../{REVIEW.as_posix()}) · [Release and patch](../{PACKAGE.as_posix()}/README.md)

All 132 native cases, 66 visual previews and 218 description getters passed. The original Items menu showed three complete cards from the three families and returned to Lisbon. The earlier save held the Sextant, and the Eagle Figurehead and Frozen Rose were supplied by an isolated inventory transfer. The main copied allocation stays at 123,264 bytes. Six descriptions use 504 bytes appended to the resident catalogue. The other 185 projections stayed byte-identical.

Continue with relics and other unreviewed item descriptions beginning at COMMON 2963. Later crew-equipment, armor and weapon records stay in scope. Continue the remaining player-facing prose and earlier speaker names and role labels. Graphics artwork and the older-record technical re-audit remain separate.
"""
    base.replace_checked(DOC, doc.encode('utf-8'))
    lead = f'# Current editorial checkpoint - 2026-11-11\n\n{summary}\n\nContinue from [the registered figurehead, navigation and gift cards]({DOC.name}).\n\n'
    for name in ('editorial_handoff_current.md', 'editorial_efficiency_workflow.md', 'translation_progress.md'):
        path = Path('docs') / name
        base.replace_checked(path, lead.encode('utf-8') + path.read_bytes())
    continuity = Path('docs/build_continuity_protocol.md')
    protocol = (
        'The 33 figurehead, navigation and gift descriptions are registered over Crew Equipment with 756 entries, '
        f'114 accepted layers and 91 checks. Use {tick}scripts/register_figurehead_navigation_gift_cards_v1.py --register{tick} '
        f'and {tick}--publish-prepared{tick}. Preserve both item-description representations and Shachihoko. '
        f'Exact reconstruction, the three Items checks and cold startup pass. [Registered checkpoint]({DOC.name})\n\n')
    base.replace_checked(continuity, protocol.encode('utf-8') + continuity.read_bytes())
    print('Registered 756 entries and credited 33 item-card reviews once.')


def register():
    ledger = checked_text(inspect.getsource(base.update_ledger), {
        "'diplomatic-and-scheme-outcome-notices'": "'figurehead-navigation-gift-cards'",
        'Thirty-four diplomacy and scheme outcomes are registered.': 'Thirty-three figurehead, navigation and gift descriptions are registered.',
        '== 25985': '== 26681', '== 15438': '== 15930', '== 10547': '== 10751',
    })
    old_scope = """    scope = dict(observed_notice_IDs=approved['live_messages'], stored_cases=176, fresh_viewed_pages=31,
        reused_exact_viewed_pages=145, fixture_scope='One incoming letter in a previously empty isolated RAM slot',
        original_no_preserved_war=True, natural_letter_generation=False, hardware=False)"""
    src = checked_text(inspect.getsource(base.register), {
        "approved['live_messages'] == [349, 356, 352]": "approved['observed_ids'] == live['observed_ids']",
        "sum(int(s.get('tests', 0)) for s in tests) == 27": "sum(int(s.get('tests', 0)) for s in tests) == 34",
        "len(manifest['batches']) == 734 and len(manifest['checks']) == 69":
            "len(manifest['batches']) == 755 and len(manifest['checks']) == 90",
        "evidence['target_ARM9_sha256']": "evidence['research_ARM9_sha256']",
        "evidence['target_COMMON_sha256']": "evidence['research_COMMON_sha256']",
        old_scope: '    scope = verification_scope(approved, live)',
        'release_stack_before_diplomacy.json': 'release_stack_before_figurehead_navigation_gift_cards.json',
        'verified_crew_notice_predecessor=predecessor, diplomatic_outcome_release=str(REVIEW)':
            'verified_crew_equipment_item_cards_predecessor=predecessor, figurehead_navigation_gift_cards_release=str(REVIEW)',
        'Reviewed diplomacy and scheme outcomes with scoped native phrase wrapping.':
            'Reviewed figurehead, navigation and gift descriptions in both native stores.',
        'release_stack.diplomacy.pending.json': 'release_stack.figurehead_navigation_gift_cards.pending.json',
        "LEDGER.with_name('editorial_review_current.diplomacy.pending.json')": 'PENDING_LEDGER',
        '    save(pending_registry, registry)':
            '    preserve_compression(pending_registry, REGISTRY)\n    save(pending_registry, registry)',
        "evidence['wrapper']": "evidence['ownership']",
        'COMMON_DIPLOMATIC_OUTCOMES_MODAL_AND_PHRASE_WRAP': 'FIGUREHEAD_NAVIGATION_GIFT_CARDS_NATIVE_WRAP',
        "manifest['diplomatic_outcomes_registered_successor_pipeline']":
            "manifest['figurehead_navigation_gift_cards_registered_successor_pipeline']",
        "len(manifest['batches']) == 735 and len(manifest['checks']) == 70":
            "len(manifest['batches']) == 756 and len(manifest['checks']) == 91",
        'registered_manifest_entries=735, accepted_layers=114, passing_release_checks=70, repository_tests=27':
            'registered_manifest_entries=756, accepted_layers=114, passing_release_checks=91, repository_tests=34',
        '    pending_registry.replace(REGISTRY)\n    try:\n        pending_ledger.replace(LEDGER)\n    except OSError:\n        replace_checked(REGISTRY, before_registry)\n        raise\n    assert digest(REGISTRY) == release[\'registry_sha256\'] and digest(PROMOTED) == promoted\n    publish(release)':
            '    assert digest(PROMOTED) == promoted\n    print("Figurehead, navigation and gift registration staged and ready to publish.")',
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
        'release_stack.sea_events.pending.json': 'release_stack.figurehead_navigation_gift_cards.pending.json',
    })
    exec(compile(code, __file__ + '::atomic-figurehead-navigation-gift-publication', 'exec'), env)
    env['publish_prepared']()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    action = parser.add_mutually_exclusive_group(required=True)
    action.add_argument('--register', action='store_true')
    action.add_argument('--publish-prepared', action='store_true')
    (publish_prepared if parser.parse_args().publish_prepared else register)()
