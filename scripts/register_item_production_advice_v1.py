"""Register the reviewed item-production and voyage-supply advice."""

import argparse
from collections import Counter
import inspect
import json
from pathlib import Path
from types import FunctionType, SimpleNamespace

from dk4tool.dialogue.review import validate_natural_dialogue_batch
from scripts import register_promotional_item_cards_v1 as previous
from scripts import register_sea_event_review_v2 as transaction
from scripts import stage_item_production_advice_v3 as layout
from scripts import verify_item_production_advice_live_v1 as live_check
from scripts.source_locked_derivation_v5118 import checked_text


base, stage = previous.base, live_check.stage
PARENT = previous.RELEASE
PROFILE = 'all-routes-item-production-advice-editorial-v1-20261111'
FAMILY = 'item_production_advice_contextual_20261111'
CHECK = 'registered_item_production_advice_native_live_and_complete_parent_inverse'
PACKAGE = Path('releases/all_routes_editorial_20261111_item_production_advice_candidate')
VERIFICATION = PACKAGE / 'verification'
RELEASE = VERIFICATION / 'registered_release_verification.json'
REVIEW = VERIFICATION / 'registered_review.json'
MUTATION_PLAN = VERIFICATION / 'registration_mutation_plan.json'
TEST = Path('out/item_production_advice_registered_20261111_v1')
ROM = TEST / 'Translation_DS_All_Routes_Item_Production_Advice_20261111_candidate.nds'
MANIFEST = ROM.with_suffix('.manifest.json')
PATCH = PACKAGE / 'translation.xdelta'
DOC = Path('docs/editorial_item_production_advice_registered_20261111.md')
PENDING_LEDGER = TEST / 'editorial_review_current.item_production_advice.pending.json'
OUTPUT, EVIDENCE, RESEARCH = stage.OUTPUT, stage.PROOF, stage.ROM
STARTUP_VERIFICATION, CHECKPOINT = live_check.verified.BOOT, live_check.CHECKPOINT
LIVE_VERIFICATION, QA = live_check.LIVE, live_check.verified.QA
PREVIOUS_TOTAL, TOTAL, REVISED, RETAINED = 26751, 24, 15, 9


def rebuild(parent, evidence, source):
    image = stage.NdsImage.open(parent['candidate'])
    arm, common = image.read_file(stage.ARM), image.read_file(stage.review.COMMON)
    runtime = SimpleNamespace(arm=arm, common=common)
    rows = {row['message_ID']: row for row in source['records']}
    rebuild_stage = FunctionType(stage.stage.__code__, vars(stage) | {'PHRASES': layout.PHRASES})
    target_arm, target_common, storage, entries, allocation, selector = rebuild_stage(parent, runtime, rows)
    assert json.loads(json.dumps(allocation)) == evidence['allocation']
    assert json.loads(json.dumps(selector)) == evidence['ownership']
    assert len(evidence['native_original_copies']) == TOTAL
    for row in evidence['native_original_copies']:
        n = row['message_ID']
        assert row['staged_reference'] == stage.review.reference(entries[n])
        assert bytes.fromhex(next(case['display_hex'] for case in evidence['native_display_cases']
                                 if case['message_ID'] == n)) == storage[n]
    image.replace_file(stage.ARM, target_arm)
    image.replace_file(stage.review.COMMON, target_common)
    assert bytes(image.rom.save()) == RESEARCH.read_bytes()
    image.replace_file(stage.ARM, arm)
    image.replace_file(stage.review.COMMON, common)
    assert bytes(image.rom.save()) == Path(parent['candidate']).read_bytes()
    return target_arm, target_common


def verification_scope(approved, live):
    assert approved['live_messages'] == live['observed_ids'] == [live_check.MESSAGE]
    assert approved['stored_cases'] == approved['viewed_pages'] == TOTAL
    assert live['original_Advice_button'] and live['original_item_view_restored'] and live['original_town_return']
    assert live['complete_dialogue_ink_and_blank_cells_exact'] and live['header']['text'] == 'Hans Letzel'
    return dict(observed_notice_IDs=live['observed_ids'], stored_cases=TOTAL, viewed_pages=TOTAL,
        offline_actor_and_screen_cases=144, offline_native_portrait_cases=48,
        original_Advice_button_item_and_Lisbon_return=True, natural_advice_unlock=False, hardware=False,
        fixture_scope='The original transfer supplied Baby Shark to a copy of the Lisbon save. '
                      'The original flag setter enabled Advice. Controller and stylus inputs opened '
                      'Items, requested Advice, dismissed the complete Hans portrait and returned to town.')


def final_review(source, evidence, scope):
    stored = {row['message_ID']: row for row in evidence['native_original_copies']}
    pages = evidence['native_display_cases']
    records = []
    for row in source['records']:
        n = row['message_ID']
        case = stored[n]
        assert row['source_reference'] == case['source_reference'] and row['current_reference'] == case['previous_reference']
        variants = [page for page in pages if page['message_ID'] == n]
        assert [page['actor_ID'] for page in variants] == [75, 76]
        assert len({page['display_hex'] for page in variants}) == 1
        records.append(row | dict(review=row['review'] | {'formatting': True},
            registered_reference=case['staged_reference'] | {'exact_stored_hex': variants[0]['display_hex'],
                'ROM_sha256': evidence['research_ROM_sha256']},
            displayed_variants=[{key: page[key] for key in
                ('actor_ID', 'display_hex', 'visible_lines', 'native_ink_sha256')} for page in variants],
            gameplay_observed=n in scope['observed_notice_IDs'], new_credit=1))
    assert len(records) == TOTAL and Counter(row['decision'] for row in records) == {
        'revision': REVISED, 'retention': RETAINED}
    review = dict(translation_policy='natural-dialogue-v2', target_locale='en-US',
        encoder='dialogue-relocatable-v1', review_gates=source['review_gates'], records=records,
        native_context=source['native_context'], actual_verification_scope=scope, full_goal_complete=False)
    validate_natural_dialogue_batch(review)
    return review


def publish(release):
    summary = 'The 24 item production and voyage-supply replies are registered. The ledger now credits 26,775 reviews.'
    notes = f"""# All Routes Item Production Advice candidate

Use the local ROM [{ROM.name}](../../{ROM.as_posix()}) with its build manifest. The [clean-input patch](translation.xdelta) reconstructs it byte for byte from Japanese ROM SHA-256 '{release['clean_input_sha256']}'. Expected ROM SHA-256 is '{release['candidate_sha256']}'. Patch SHA-256 is '{release['patch_sha256']}'.

{summary} Fifteen revisions and nine justified retentions preserve Hans and Mikhail's shared advice, including the tropical banana clue, the Black Sea food custom and the dye made from mangosteen peel. The original item and actor selectors remain exact. The wraps use the native width with complete ASCII letters and one portrait per reply.

All 24 native pages passed visual review, and all 48 portrait cases and 144 caller-fragment cases passed offline. A focused emulator replay opened Hans's Baby Shark reply through the original Advice button and returned to Items and Lisbon. It used a copied save with an isolated item transfer and Advice flag. The other replies and the Mikhail branch were checked offline. All 94 release checks, 34 targeted tests, the 31,000-frame cold boot and 24 protected name getters passed. [Gameplay proof](verification/item_advice_gameplay_verification.json) · [Exact record review](verification/registered_review.json)
"""
    (PACKAGE / 'README.md').write_text(notes, encoding='utf-8', newline='\n')
    base.save(PACKAGE / 'checksums.json', {p.relative_to(PACKAGE).as_posix(): base.digest(p)
        for p in sorted(PACKAGE.rglob('*')) if p.is_file() and p.name != 'checksums.json'})
    pin_path = Path('translations/rom_retention_pins.json')
    pins = base.load(pin_path)
    for path in (layout.previous.previous.ROM, layout.previous.ROM, RESEARCH, ROM):
        resolved = str(path.resolve())
        assert not any(row['path'] == resolved for row in pins)
        pins.append(dict(path=resolved, reason=f'Preserve the item advice review build. SHA256 {base.digest(path)}'))
    base.replace_checked(pin_path, (json.dumps(pins, ensure_ascii=False, indent=2) + '\n').replace('\n', '\r\n').encode('utf-8'))
    doc = f"""# Item production and voyage-supply advice registered

{summary} COMMON 3033–3056 covers 20 Local Product hints and four voyage supplies. Gallery, the compact item screen and regular Items select the same message by item index. Each original branch still selects Hans or Mikhail from the game state. [Registered review](../{REVIEW.as_posix()}) · [Release and patch](../{PACKAGE.as_posix()}/README.md)

The final native pages preserve complete text within two or three rows. The guarded layout applies to these 24 IDs through the original portrait wrapper. All other selected COMMON spans and the 123,264-byte copied allocation remain exact. The focused Lisbon replay binds Hans's displayed name and all three Baby Shark rows, then returns to the same Items screen and town.

Continue at COMMON 3057 with weapons, then armor, crew equipment, figureheads, gifts, Proofs and map advice. Reuse the exact actor and item-index caller proof where the code matches. Check new text in the same native portrait consumer. Continue the rest of the player-facing prose and speaker labels. Graphics artwork and the later older-record technical re-audit remain separate.
"""
    base.replace_checked(DOC, doc.encode('utf-8'))
    lead = f'# Current editorial checkpoint - 2026-11-11\n\n{summary}\n\nContinue from [the registered item production advice]({DOC.name}).\n\n'
    for name in ('editorial_handoff_current.md', 'editorial_efficiency_workflow.md', 'translation_progress.md'):
        path = Path('docs') / name
        base.replace_checked(path, lead.encode('utf-8') + path.read_bytes())
    continuity = Path('docs/build_continuity_protocol.md')
    protocol = (
        'The 24 item production and voyage-supply replies are registered over Promotional Item Cards with '
        '759 entries, 114 accepted layers and 94 checks. Use scripts/register_item_production_advice_v1.py '
        f'with --register and --publish-prepared. Preserve the original item index and both advisers. '
        f'Exact reconstruction, Lisbon Advice and cold startup pass. [Registered checkpoint]({DOC.name})\n\n')
    base.replace_checked(continuity, protocol.encode('utf-8') + continuity.read_bytes())
    print('Registered 759 entries and credited 24 item advice reviews once.')


def register():
    ledger = checked_text(inspect.getsource(base.update_ledger), {
        "'diplomatic-and-scheme-outcome-notices'": "'item-production-and-voyage-advice'",
        'Thirty-four diplomacy and scheme outcomes are registered.': 'Twenty-four item advice replies are registered.',
        '== 25985': '== 26775', '== 15438': '== 16001', '== 10547': '== 10774',
    })
    old_scope = """    scope = dict(observed_notice_IDs=approved['live_messages'], stored_cases=176, fresh_viewed_pages=31,
        reused_exact_viewed_pages=145, fixture_scope='One incoming letter in a previously empty isolated RAM slot',
        original_no_preserved_war=True, natural_letter_generation=False, hardware=False)"""
    src = checked_text(inspect.getsource(base.register), {
        "approved['live_messages'] == [349, 356, 352]": "approved['live_messages'] == live['observed_ids']",
        "sum(int(s.get('tests', 0)) for s in tests) == 27": "sum(int(s.get('tests', 0)) for s in tests) == 34",
        "len(manifest['batches']) == 734 and len(manifest['checks']) == 69":
            "len(manifest['batches']) == 758 and len(manifest['checks']) == 93",
        "evidence['target_ARM9_sha256']": "evidence['research_ARM9_sha256']",
        "evidence['target_COMMON_sha256']": "evidence['research_COMMON_sha256']",
        old_scope: '    scope = verification_scope(approved, live)',
        'release_stack_before_diplomacy.json': 'release_stack_before_item_production_advice.json',
        'verified_crew_notice_predecessor=predecessor, diplomatic_outcome_release=str(REVIEW)':
            'verified_promotional_item_cards_predecessor=predecessor, item_production_advice_release=str(REVIEW)',
        'Reviewed diplomacy and scheme outcomes with scoped native phrase wrapping.':
            'Reviewed item production and voyage-supply advice with scoped portrait wraps.',
        'release_stack.diplomacy.pending.json': 'release_stack.item_production_advice.pending.json',
        "LEDGER.with_name('editorial_review_current.diplomacy.pending.json')": 'PENDING_LEDGER',
        '    save(pending_registry, registry)':
            '    preserve_compression(pending_registry, REGISTRY)\n    save(pending_registry, registry)',
        '(EVIDENCE, CHECKPOINT, LIVE_VERIFICATION, STARTUP_VERIFICATION, QA)':
            '(EVIDENCE, CHECKPOINT, LIVE_VERIFICATION, STARTUP_VERIFICATION, QA, VISUAL)',
        "evidence['wrapper']": "evidence['ownership']",
        "evidence['storage']": "evidence['allocation']",
        'COMMON_DIPLOMATIC_OUTCOMES_MODAL_AND_PHRASE_WRAP': 'COMMON_ITEM_PRODUCTION_ADVICE_PORTRAIT_WRAP',
        "manifest['diplomatic_outcomes_registered_successor_pipeline']":
            "manifest['item_production_advice_registered_successor_pipeline']",
        "len(manifest['batches']) == 735 and len(manifest['checks']) == 70":
            "len(manifest['batches']) == 759 and len(manifest['checks']) == 94",
        'registered_manifest_entries=735, accepted_layers=114, passing_release_checks=70, repository_tests=27':
            'registered_manifest_entries=759, accepted_layers=114, passing_release_checks=94, repository_tests=34',
        '    pending_registry.replace(REGISTRY)\n    try:\n        pending_ledger.replace(LEDGER)\n    except OSError:\n        replace_checked(REGISTRY, before_registry)\n        raise\n    assert digest(REGISTRY) == release[\'registry_sha256\'] and digest(PROMOTED) == promoted\n    publish(release)':
            '    assert digest(PROMOTED) == promoted\n    print("Item advice registration staged and ready to publish.")',
    })
    env = vars(base) | globals() | {
        'preserve_compression': transaction.preserve_compression,
        'VISUAL': live_check.verified.VISUAL,
    }
    exec(compile(ledger + '\n\n' + src, __file__ + '::registered-item-advice-transaction', 'exec'), env)
    env['register']()


def publish_prepared():
    env = vars(transaction) | globals() | {'prior': base}
    env['verify_prepared'] = FunctionType(transaction.verify_prepared.__code__, env)
    code = checked_text(inspect.getsource(transaction.publish_prepared), {
        'release_stack.sea_events.pending.json': 'release_stack.item_production_advice.pending.json',
    })
    exec(compile(code, __file__ + '::atomic-item-advice-publication', 'exec'), env)
    env['publish_prepared']()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    action = parser.add_mutually_exclusive_group(required=True)
    action.add_argument('--register', action='store_true')
    action.add_argument('--publish-prepared', action='store_true')
    (publish_prepared if parser.parse_args().publish_prepared else register)()
