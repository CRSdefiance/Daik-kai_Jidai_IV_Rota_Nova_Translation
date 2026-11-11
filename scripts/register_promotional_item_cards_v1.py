"""Register ten promotional relics and twenty generated map-fragment records."""

import argparse
import inspect
import json
from pathlib import Path
from types import FunctionType

from scripts import register_relic_map_item_cards_v1 as previous
from scripts import register_sea_event_review_v2 as transaction
from scripts import verify_promotional_item_cards_v1 as verify
from scripts.source_locked_derivation_v5118 import checked_text

base, template, stage = previous.base, previous.template, verify.stage
PARENT = previous.RELEASE
PROFILE = 'all-routes-promotional-item-cards-editorial-v1-20261111'
FAMILY = 'promotional_item_cards_contextual_20261111'
CHECK = 'registered_promotional_item_cards_native_live_and_complete_parent_inverse'
PACKAGE = Path('releases/all_routes_editorial_20261111_promotional_item_cards_candidate')
VERIFICATION = PACKAGE / 'verification'
RELEASE = VERIFICATION / 'registered_release_verification.json'
REVIEW = VERIFICATION / 'registered_review.json'
MUTATION_PLAN = VERIFICATION / 'registration_mutation_plan.json'
TEST = Path('out/promotional_item_cards_registered_20261111_v1')
ROM = TEST / 'Translation_DS_All_Routes_Promotional_Item_Cards_20261111_candidate.nds'
MANIFEST = ROM.with_suffix('.manifest.json')
PATCH = PACKAGE / 'translation.xdelta'
DOC = Path('docs/editorial_promotional_item_cards_registered_20261111.md')
PENDING_LEDGER = TEST / 'editorial_review_current.promotional_item_cards.pending.json'
OUTPUT, EVIDENCE, RESEARCH = stage.OUTPUT, stage.PROOF, stage.ROM
STARTUP_VERIFICATION, CHECKPOINT, LIVE_VERIFICATION, QA = verify.BOOT, verify.CHECKPOINT, verify.LIVE, verify.QA
PREVIOUS_TOTAL, TOTAL, REVISED, RETAINED = 26721, 30, 28, 2


def rebuild(parent, evidence, source):
    arm, common = FunctionType(template.rebuild.__code__, vars(template) | globals())(parent, evidence, source)
    assert evidence['ownership']['shared_fragment_alias_count'] == 20
    assert evidence['complete_generated_titles_and_all_twenty_initial_fragment_slots']
    assert len(evidence['native_promotional_initializers']) == 3
    return arm, common


def final_review(source, evidence, scope):
    code = checked_text(inspect.getsource(template.final_review), {
        "('page', 'mode', 'lines', 'native_ink_sha256', 'native_glyphs')":
            "('seed', 'page', 'mode', 'lines', 'native_ink_sha256', 'native_glyphs')",
    })
    env = vars(template) | globals()
    exec(compile(code, __file__ + '::registered-promotional-seed-displays', 'exec'), env)
    return env['final_review'](source, evidence, scope)


def verification_scope(approved, live):
    assert approved['observed_ids'] == live['observed_ids'] == verify.OBSERVED
    assert approved['stored_records'] == TOTAL and approved['viewed_pages'] == 100
    assert live['original_Items_screen'] and live['returning_to_same_town_screen']
    assert live['complete_description_foreground_and_blank_cells_exact']
    assert live['observed']['3009']['title'] == 'Witch Idol'
    assert live['observed']['3013']['title'] == 'Twisted Horn Map 1'
    return dict(observed_notice_IDs=verify.OBSERVED, stored_records=TOTAL,
        offline_item_display_modes=200, directly_viewed_pages=100,
        offline_generated_names=40, controlled_native_initializer_seeds=[0, 2, 3],
        original_item_menu_and_town_return=True,
        fixture_scope='An isolated inventory transfer added Witch Idol and the existing generated Twisted Horn Map 1 to a copy of the Lisbon save. Original controller and stylus inputs opened Items, selected both cards and returned to town.',
        original_battery_save_unchanged=True, normal_acquisition_verified=False,
        downloaded_promotion_verified=False,
        offline_only_notice_IDs=[n for n in stage.IDS if n not in verify.OBSERVED], hardware=False)


def publish(release):
    summary = 'The 30 promotional item descriptions are registered. The ledger now credits 26,751 reviews.'
    tick = chr(96)
    notes = f"""# All Routes Promotional Item Cards candidate

Use the local ROM {tick}{ROM.as_posix()}{tick} with its build manifest. The [clean-input patch](translation.xdelta) reconstructs it byte for byte from Japanese ROM SHA-256 {tick}{release['clean_input_sha256']}{tick}. Expected ROM SHA-256 is {tick}{release['candidate_sha256']}{tick}. Patch SHA-256 is {tick}{release['patch_sha256']}{tick}.

{summary} This completes contextual review of the 218 item-description records. The ten promotional relics and twenty generated map-fragment slots add 28 revisions and two justified retentions. All twenty slots still share one active fragment description. The ten initialized relic titles, generated title templates, part numbers and native metadata passed the exact checks across three controlled seeds.

Both item views passed 200 native renders and 100 visual previews. All 218 description getters passed. The original Items replay showed Witch Idol and Twisted Horn Map 1 after an isolated inventory transfer, then returned to Lisbon. The other 28 cards were checked offline. All 93 release checks, 34 targeted tests, cold startup and 24 protected name getters passed. [Gameplay proof](verification/promotional_items_gameplay_verification.json) · [Exact record review](verification/registered_review.json)
"""
    (PACKAGE / 'README.md').write_text(notes, encoding='utf-8', newline='\n')
    base.save(PACKAGE / 'checksums.json', {p.relative_to(PACKAGE).as_posix(): base.digest(p)
        for p in sorted(PACKAGE.rglob('*')) if p.is_file() and p.name != 'checksums.json'})
    pin_path = Path('translations/rom_retention_pins.json')
    pins = base.load(pin_path)
    for path, role in ((RESEARCH, 'verified promotional item stage'), (ROM, 'registered promotional item ROM')):
        resolved = str(path.resolve())
        assert not any(row['path'] == resolved for row in pins)
        pins.append(dict(path=resolved, reason=f'Preserve {role}. SHA256 {base.digest(path)}'))
    base.replace_checked(pin_path, (json.dumps(pins, ensure_ascii=False, indent=2) + '\n').replace('\n', '\r\n').encode('utf-8'))
    doc = f"""# Promotional item cards registered

{summary} COMMON 3003–3032 agrees with both active item views. The descriptions restore details such as the siren’s role in the Witch Idol design and the story that the King’s Shield served as a ship. The twenty map slots use one description that identifies a piece of an ancient map and the four-piece set. [Registered review](../{REVIEW.as_posix()}) · [Release and patch](../{PACKAGE.as_posix()}/README.md)

The original copied allocation stays at 123,264 bytes. Four separate relic paragraphs and the shared map paragraph use 424 bytes of appended resident storage. The other 188 description projections stayed byte-identical. The offline check covered all 30 slots and all 40 generated title variants across the two item views. The emulator replay covered the original Items view and return, using an isolated inventory transfer for Witch Idol and Twisted Horn Map 1.

Continue with item advice at COMMON 3033. These lines are voiced remarks, including older-speaker phrasing and regional production suggestions. Bind the actual speaker and advice consumer, then review each related sequence in context. Continue all remaining player-facing prose and earlier speaker names and role labels. Graphics artwork and the older-record technical re-audit remain separate.
"""
    base.replace_checked(DOC, doc.encode('utf-8'))
    lead = f'# Current editorial checkpoint - 2026-11-11\n\n{summary}\n\nContinue from [the registered promotional item cards]({DOC.name}).\n\n'
    for name in ('editorial_handoff_current.md', 'editorial_efficiency_workflow.md', 'translation_progress.md'):
        path = Path('docs') / name
        base.replace_checked(path, lead.encode('utf-8') + path.read_bytes())
    continuity = Path('docs/build_continuity_protocol.md')
    protocol = (
        'The 30 promotional item descriptions are registered over Relic and Map Item Cards with 758 entries, '
        f'114 accepted layers and 93 checks. Use {tick}scripts/register_promotional_item_cards_v1.py --register{tick} '
        f'and {tick}--publish-prepared{tick}. Preserve the shared fragment description and generated title behavior. '
        f'Exact reconstruction, original Items return and cold startup pass. [Registered checkpoint]({DOC.name})\n\n')
    base.replace_checked(continuity, protocol.encode('utf-8') + continuity.read_bytes())
    print('Registered 758 entries and credited 30 promotional item reviews once.')


def register():
    ledger = checked_text(inspect.getsource(base.update_ledger), {
        "'diplomatic-and-scheme-outcome-notices'": "'promotional-item-cards'",
        'Thirty-four diplomacy and scheme outcomes are registered.': 'Thirty promotional item descriptions are registered.',
        '== 25985': '== 26751', '== 15438': '== 15986', '== 10547': '== 10765',
    })
    old_scope = """    scope = dict(observed_notice_IDs=approved['live_messages'], stored_cases=176, fresh_viewed_pages=31,
        reused_exact_viewed_pages=145, fixture_scope='One incoming letter in a previously empty isolated RAM slot',
        original_no_preserved_war=True, natural_letter_generation=False, hardware=False)"""
    src = checked_text(inspect.getsource(base.register), {
        "approved['live_messages'] == [349, 356, 352]": "approved['observed_ids'] == live['observed_ids']",
        "sum(int(s.get('tests', 0)) for s in tests) == 27": "sum(int(s.get('tests', 0)) for s in tests) == 34",
        "len(manifest['batches']) == 734 and len(manifest['checks']) == 69":
            "len(manifest['batches']) == 757 and len(manifest['checks']) == 92",
        "evidence['target_ARM9_sha256']": "evidence['research_ARM9_sha256']",
        "evidence['target_COMMON_sha256']": "evidence['research_COMMON_sha256']",
        old_scope: '    scope = verification_scope(approved, live)',
        'release_stack_before_diplomacy.json': 'release_stack_before_promotional_item_cards.json',
        'verified_crew_notice_predecessor=predecessor, diplomatic_outcome_release=str(REVIEW)':
            'verified_relic_map_item_cards_predecessor=predecessor, promotional_item_cards_release=str(REVIEW)',
        'Reviewed diplomacy and scheme outcomes with scoped native phrase wrapping.':
            'Reviewed promotional relic and generated map-fragment descriptions in both native stores.',
        'release_stack.diplomacy.pending.json': 'release_stack.promotional_item_cards.pending.json',
        "LEDGER.with_name('editorial_review_current.diplomacy.pending.json')": 'PENDING_LEDGER',
        '    save(pending_registry, registry)':
            '    preserve_compression(pending_registry, REGISTRY)\n    save(pending_registry, registry)',
        "evidence['wrapper']": "evidence['ownership']",
        'COMMON_DIPLOMATIC_OUTCOMES_MODAL_AND_PHRASE_WRAP': 'PROMOTIONAL_ITEM_CARDS_NATIVE_WRAP',
        "manifest['diplomatic_outcomes_registered_successor_pipeline']":
            "manifest['promotional_item_cards_registered_successor_pipeline']",
        "len(manifest['batches']) == 735 and len(manifest['checks']) == 70":
            "len(manifest['batches']) == 758 and len(manifest['checks']) == 93",
        'registered_manifest_entries=735, accepted_layers=114, passing_release_checks=70, repository_tests=27':
            'registered_manifest_entries=758, accepted_layers=114, passing_release_checks=93, repository_tests=34',
        '    pending_registry.replace(REGISTRY)\n    try:\n        pending_ledger.replace(LEDGER)\n    except OSError:\n        replace_checked(REGISTRY, before_registry)\n        raise\n    assert digest(REGISTRY) == release[\'registry_sha256\'] and digest(PROMOTED) == promoted\n    publish(release)':
            '    assert digest(PROMOTED) == promoted\n    print("Promotional item registration staged and ready to publish.")',
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
        'release_stack.sea_events.pending.json': 'release_stack.promotional_item_cards.pending.json',
    })
    exec(compile(code, __file__ + '::atomic-promotional-item-publication', 'exec'), env)
    env['publish_prepared']()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    action = parser.add_mutually_exclusive_group(required=True)
    action.add_argument('--register', action='store_true')
    action.add_argument('--publish-prepared', action='store_true')
    (publish_prepared if parser.parse_args().publish_prepared else register)()
