"""Register the verified Source Item cards and coin-game response."""

import argparse
import inspect
import json
from pathlib import Path

from scripts import register_rumor_and_cooperation_v1 as template
from scripts import verify_source_item_cards_and_coin_v1 as verify
from scripts.register_faction_aftermath_portraits_v1 import RELEASE as PARENT
from scripts.source_locked_derivation_v5118 import checked_text


base, stage = template.base, verify.stage
PROFILE = 'all-routes-source-item-cards-and-coin-editorial-v1-20261111'
FAMILY = 'source_item_cards_and_coin_contextual_20261111'
CHECK = 'registered_source_item_cards_and_coin_native_live_and_complete_parent_inverse'
PACKAGE = Path('releases/all_routes_editorial_20261111_source_item_cards_and_coin_candidate')
VERIFICATION = PACKAGE / 'verification'
RELEASE = VERIFICATION / 'registered_release_verification.json'
REVIEW = VERIFICATION / 'registered_review.json'
MUTATION_PLAN = VERIFICATION / 'registration_mutation_plan.json'
TEST = Path('out/source_item_cards_and_coin_registered_20261111_v1')
ROM = TEST / 'Translation_DS_All_Routes_Source_Item_Cards_and_Coin_20261111_candidate.nds'
MANIFEST = ROM.with_suffix('.manifest.json')
PATCH = PACKAGE / 'translation.xdelta'
DOC = Path('docs/editorial_source_item_cards_and_coin_registered_20261111.md')
PENDING_LEDGER = TEST / 'editorial_review_current.source_item_cards_and_coin.pending.json'
OUTPUT, EVIDENCE, RESEARCH = stage.OUTPUT, stage.PROOF, stage.ROM
STARTUP_VERIFICATION, CHECKPOINT, LIVE_VERIFICATION, QA = verify.BOOT, verify.CHECKPOINT, verify.LIVE, verify.QA
PREVIOUS_TOTAL, TOTAL, REVISED, RETAINED = 26533, 21, 17, 4


def rebuild(parent, evidence, source):
    assert all(base.digest(path) == value for path, value in evidence['evidence'].items())
    image = base.NdsImage.open(parent['candidate'])
    before, old_common = image.read_file(base.ARM), image.read_file(base.COMMON)
    rows = stage.active_rows(source)
    arm, common, rebound, allocation, ownership = stage.build(before, old_common, rows)
    assert json.loads(json.dumps(ownership)) == evidence['ownership']
    assert json.loads(json.dumps(allocation, sort_keys=True)) == evidence['storage']
    assert all(stage.reference(rebound[row['message_ID']]) == row['stored'] for row in evidence['records'])
    assert all(rebound[row['message_ID']].text.hex() == row['stored_hex'] for row in evidence['records'])
    image.replace_file(base.ARM, arm)
    image.replace_file(base.COMMON, common)
    assert bytes(image.rom.save()) == RESEARCH.read_bytes()
    image.replace_file(base.ARM, before)
    image.replace_file(base.COMMON, old_common)
    assert bytes(image.rom.save()) == Path(parent['candidate']).read_bytes()
    return arm, common


def verification_scope(approved, live):
    assert approved['observed_ids'] == live['observed_ids'] == verify.OBSERVED
    assert approved['stored_records'] == TOTAL and approved['viewed_pages'] == 41
    assert live['coin_game']['zero_selection_finished_with_X']
    assert live['item_card']['original_ownership_award_and_sailing_return']
    assert live['item_card']['complete_description_foreground_and_blank_cells_exact']
    return dict(observed_notice_IDs=verify.OBSERVED, stored_records=TOTAL,
        offline_item_display_modes=80, offline_coin_portrait_modes=1, directly_viewed_pages=41,
        fixture_scope='The original coin-game command was placed in a disposable opening. The original Baby Shark encounter was initialized in an isolated save. Normal controller inputs advanced both displays.',
        actual_coin_empty_selection_and_board_return=True, actual_standalone_baby_shark_card_and_sailing_return=True,
        all_twenty_main_item_details_checked_offline=True, natural_event_activation=False,
        offline_only_notice_IDs=[n for n in stage.IDS if n not in verify.OBSERVED], hardware=False)


def final_review(source, evidence, scope):
    assert evidence['editorial_amendments'] == json.loads(json.dumps(stage.AMENDMENTS))
    records = stage.active_rows(source)
    proofs = {row['message_ID']: row for row in evidence['records']}
    projections = {row['message_ID']: row for row in evidence['ownership']['item_paragraphs']}
    reviewed = []
    for n, row in records.items():
        proof = proofs[n]
        assert proof['source'] == row['source_reference'] and proof['previous'] == row['current_reference']
        current = row | dict(review=row['review'] | {'formatting': True},
            registered_reference=proof['stored'] | dict(exact_stored_hex=proof['stored_hex'], ROM_sha256=evidence['research_ROM_sha256']),
            gameplay_observed=n in verify.OBSERVED, new_credit=1)
        if n in projections:
            current['registered_private_projection'] = projections[n]
            current['registered_native_item_displays'] = [
                {key: variant[key] for key in ('page', 'mode', 'lines', 'native_ink_sha256', 'native_glyphs')}
                for variant in evidence['item_cases'] if variant['message_ID'] == n]
        else:
            current['registered_coin_portrait'] = evidence['native_portrait_cases'][0]
        reviewed.append(current)
    assert base.Counter(row['decision'] for row in reviewed) == {'revision': REVISED, 'retention': RETAINED}
    result = dict(translation_policy=source['translation_policy'], target_locale=source['target_locale'],
        encoder=source['encoder'], review_gates=source['review_gates'], records=reviewed,
        actual_verification_scope=scope, full_goal_complete=False)
    base.validate_natural_dialogue_batch(result)
    return result


def publish(release):
    summary = 'The coin response and 20 Source Item descriptions are registered. The ledger now credits 26,554 reviews.'
    notes = f"""# All Routes Source Item Cards and Coin candidate

Use the local ROM {chr(96)}{ROM.as_posix()}{chr(96)} beside its build manifest. The [clean-input patch](translation.xdelta) applies to clean Japanese SHA-256 {chr(96)}{release['clean_input_sha256']}{chr(96)} and reconstructs SHA-256 {chr(96)}{release['candidate_sha256']}{chr(96)} byte for byte. Patch SHA-256 is {chr(96)}{release['patch_sha256']}{chr(96)}.

{summary} Seventeen revisions and four justified retentions cover the entire Source Item category and the coin-game response when no coin is selected. Both item screens use the revised descriptions. The registered item allocation stays at 123,264 bytes. The alternate build with a larger payload hit a startup regression and is preserved as research evidence.

The original coin-game command in an isolated opening showed Fernando Dias's prompt and the return to the board. An initialized original encounter awarded Baby Shark, showed its complete card, and returned to sailing. All 80 item render cases and the coin portrait passed native checks. The remaining 19 item cards were checked offline. All 87 cumulative release checks, 34 targeted tests, cold startup and 24 protected name getters passed. [Gameplay proof](verification/source_item_cards_and_coin_gameplay_verification.json) · [Exact record review](verification/registered_review.json)
"""
    (PACKAGE / 'README.md').write_text(notes, encoding='utf-8', newline='\n')
    base.save(PACKAGE / 'checksums.json', {p.relative_to(PACKAGE).as_posix(): base.digest(p)
        for p in sorted(PACKAGE.rglob('*')) if p.is_file() and p.name != 'checksums.json'})
    pin_path = Path('translations/rom_retention_pins.json')
    pins = base.load(pin_path)
    earlier = stage.initial
    artifacts = (
        (earlier.ROM, 'expanded item-text research ROM with startup regression'),
        (earlier.ROOT / 'coin_fixture/coin_RESEARCH_ONLY.nds', 'first coin-game display fixture'),
        (RESEARCH, 'fixed-allocation source-item research ROM'),
        (verify.replay.COIN_ROM, 'verified coin-game display fixture'),
        (ROM, 'registered Source Item and coin-game ROM'),
    )
    for path, role in artifacts:
        resolved = str(path.resolve())
        assert not any(row['path'] == resolved for row in pins)
        pins.append(dict(path=resolved, reason=f'Preserve {role}. SHA256 {base.digest(path)}'))
    base.replace_checked(pin_path, (json.dumps(pins, ensure_ascii=False, indent=2) + '\n').replace('\n', '\r\n').encode('utf-8'))
    doc = f"""# Source Item cards and coin response registered

{summary} COMMON 2814 uses the original fixed Fernando Dias portrait. COMMON 2815–2834 now agrees with the active private projections used in both item screens. All 218 getters were checked. The other 198 projected descriptions remain byte-identical. The registered release retains the original cache-copy size and runtime allocation. [Release and patch](../{PACKAGE.as_posix()}/README.md) · [Registered review](../{REVIEW.as_posix()})

The first staged build reached a startup regression after growing the copied payload to 125,088 bytes. The registered build keeps 123,264 bytes and uses the selected original paragraph span plus space in the unreferenced 198-entry predecessor table. Both builds and the isolated coin fixtures are retained. The final 41 preview pages match the viewed original renders byte for byte, and the cold boot matches the registered predecessor at all six holds.

Continue from the utility items and weapon descriptions beginning at COMMON 2835. Reuse the current item formatter and native fixtures. The active item table, retired storage spans and earlier entry references must be rebound before additional description edits. Keep Options and Market callers, graphics artwork and the older-record technical re-audit in scope.
"""
    base.replace_checked(DOC, doc.encode('utf-8'))
    lead = f'# Current editorial checkpoint - 2026-11-11\n\n{summary}\n\nContinue from [the registered Source Item cards and coin response]({DOC.name}).\n\n'
    for name in ('editorial_handoff_current.md', 'editorial_efficiency_workflow.md', 'translation_progress.md'):
        path = Path('docs') / name
        base.replace_checked(path, lead.encode('utf-8') + path.read_bytes())
    continuity = Path('docs/build_continuity_protocol.md')
    protocol = (
        'The coin response and 20 Source Item descriptions are registered over Faction Aftermath with 752 entries, '
        '114 accepted layers and 87 checks. Use {tick}scripts/register_source_item_cards_and_coin_v1.py --register{tick} '
        'and {tick}--publish-prepared{tick}. Keep the 123,264-byte startup allocation and both item-description representations. '
        f'Exact reconstruction, the native item and coin replays and cold startup pass. [Registered checkpoint]({DOC.name})\n\n').format(tick=chr(96))
    base.replace_checked(continuity, protocol.encode('utf-8') + continuity.read_bytes())
    print('Registered 752 entries and credited 21 Source Item and coin-game reviews once.')


def register():
    ledger = checked_text(inspect.getsource(base.update_ledger), {
        "'diplomatic-and-scheme-outcome-notices'": "'source-item-cards-and-coin-game'",
        'Thirty-four diplomacy and scheme outcomes are registered.': 'Twenty Source Item descriptions and the coin-game response are registered.',
        '== 25985': '== 26554', '== 15438': '== 15836', '== 10547': '== 10718',
    })
    old_scope = """    scope = dict(observed_notice_IDs=approved['live_messages'], stored_cases=176, fresh_viewed_pages=31,
        reused_exact_viewed_pages=145, fixture_scope='One incoming letter in a previously empty isolated RAM slot',
        original_no_preserved_war=True, natural_letter_generation=False, hardware=False)"""
    src = checked_text(inspect.getsource(base.register), {
        "approved['live_messages'] == [349, 356, 352]": "approved['observed_ids'] == live['observed_ids']",
        "sum(int(s.get('tests', 0)) for s in tests) == 27": "sum(int(s.get('tests', 0)) for s in tests) == 34",
        "len(manifest['batches']) == 734 and len(manifest['checks']) == 69":
            "len(manifest['batches']) == 751 and len(manifest['checks']) == 86",
        "evidence['target_ARM9_sha256']": "evidence['research_ARM9_sha256']",
        "evidence['target_COMMON_sha256']": "evidence['research_COMMON_sha256']",
        old_scope: '    scope = verification_scope(approved, live)',
        'release_stack_before_diplomacy.json': 'release_stack_before_source_item_cards_and_coin.json',
        'verified_crew_notice_predecessor=predecessor, diplomatic_outcome_release=str(REVIEW)':
            'verified_faction_aftermath_predecessor=predecessor, source_item_cards_and_coin_release=str(REVIEW)',
        'Reviewed diplomacy and scheme outcomes with scoped native phrase wrapping.':
            'Reviewed Source Item descriptions in both stores and the original coin-game response.',
        'release_stack.diplomacy.pending.json': 'release_stack.source_item_cards_and_coin.pending.json',
        "LEDGER.with_name('editorial_review_current.diplomacy.pending.json')": 'PENDING_LEDGER',
        '    save(pending_registry, registry)':
            '    preserve_compression(pending_registry, REGISTRY)\n    save(pending_registry, registry)',
        "evidence['wrapper']": "evidence['ownership']",
        'COMMON_DIPLOMATIC_OUTCOMES_MODAL_AND_PHRASE_WRAP': 'SOURCE_ITEM_CARDS_AND_COIN_NATIVE_WRAP',
        "manifest['diplomatic_outcomes_registered_successor_pipeline']":
            "manifest['source_item_cards_and_coin_registered_successor_pipeline']",
        "len(manifest['batches']) == 735 and len(manifest['checks']) == 70":
            "len(manifest['batches']) == 752 and len(manifest['checks']) == 87",
        'registered_manifest_entries=735, accepted_layers=114, passing_release_checks=70, repository_tests=27':
            'registered_manifest_entries=752, accepted_layers=114, passing_release_checks=87, repository_tests=34',
        '    pending_registry.replace(REGISTRY)\n    try:\n        pending_ledger.replace(LEDGER)\n    except OSError:\n        replace_checked(REGISTRY, before_registry)\n        raise\n    assert digest(REGISTRY) == release[\'registry_sha256\'] and digest(PROMOTED) == promoted\n    publish(release)':
            '    assert digest(PROMOTED) == promoted\n    print("Source Item and coin registration staged and ready to publish.")',
    })
    env = vars(base) | globals() | {'preserve_compression': template.previous.transaction.preserve_compression}
    exec(compile(ledger + '\n\n' + src, __file__ + '::same-registered-release-transaction', 'exec'), env)
    env['register']()


def publish_prepared():
    source = checked_text(inspect.getsource(template.publish_prepared), {
        'release_stack.rumor_and_cooperation.pending.json': 'release_stack.source_item_cards_and_coin.pending.json',
    })
    env = vars(template) | globals()
    exec(compile(source, __file__ + '::same-registered-publication', 'exec'), env)
    env['publish_prepared']()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    action = parser.add_mutually_exclusive_group(required=True)
    action.add_argument('--register', action='store_true')
    action.add_argument('--publish-prepared', action='store_true')
    (publish_prepared if parser.parse_args().publish_prepared else register)()

