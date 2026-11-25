"""Register the Price Info descriptions over the cumulative Proof and Relic release."""

import argparse
from collections import Counter
from inspect import getsource
import json
from pathlib import Path
from types import FunctionType, SimpleNamespace

from dk4tool.dialogue.review import validate_natural_dialogue_batch
from dk4tool.rom.nds import NdsImage
from dk4tool.script.common_message_table import DIRECTORY_OFFSET, TABLE_END
from scripts import register_item_production_advice_v1 as transaction
from scripts import register_proof_and_relic_advice_v1 as parent
from scripts import verify_trade_good_descriptions_v1 as verification
from scripts.source_locked_derivation_v5118 import checked_text


base, stage = transaction.base, verification.stage
PARENT = parent.RELEASE
PROFILE = 'all-routes-trade-good-descriptions-editorial-v1-20261111'
FAMILY = 'trade_good_descriptions_contextual_20261111'
CHECK = 'registered_trade_good_descriptions_native_live_and_complete_parent_inverse'
PACKAGE = Path('releases/all_routes_editorial_20261111_trade_good_descriptions_candidate')
VERIFICATION = PACKAGE / 'verification'
RELEASE = VERIFICATION / 'registered_release_verification.json'
REVIEW = VERIFICATION / 'registered_review.json'
MUTATION_PLAN = VERIFICATION / 'registration_mutation_plan.json'
TEST = Path('out/trade_good_descriptions_registered_20261111_v1')
ROM = TEST / 'Translation_DS_All_Routes_Trade_Good_Descriptions_20261111_candidate.nds'
MANIFEST = ROM.with_suffix('.manifest.json')
PATCH = PACKAGE / 'translation.xdelta'
DOC = Path('docs/editorial_trade_good_descriptions_registered_20261111.md')
PENDING_LEDGER = TEST / 'editorial_review_current.trade_good_descriptions.pending.json'
OUTPUT, EVIDENCE, RESEARCH = stage.OUTPUT, stage.PROOF, stage.ROM
STARTUP_VERIFICATION, CHECKPOINT = verification.BOOT, verification.CHECKPOINT
LIVE_VERIFICATION, QA = verification.LIVE, verification.QA
PREVIOUS_TOTAL, TOTAL, REVISED, RETAINED = 26969, 124, 97, 27


def rebuild(parent_release, evidence, draft):
    image = NdsImage.open(parent_release['candidate'])
    old_arm, old_common = image.read_file(stage.ARM), image.read_file(stage.COMMON)
    rows = {n: row for n, row in enumerate(draft['records'], stage.FIRST)}
    common, arm, rebound, allocation, storage = stage.repack(SimpleNamespace(arm=old_arm, common=old_common), rows)
    assert json.loads(json.dumps(allocation)) == evidence['allocation']
    assert evidence['native_runtime_code_changed'] is False
    assert arm[:DIRECTORY_OFFSET] == old_arm[:DIRECTORY_OFFSET] and arm[TABLE_END:] == old_arm[TABLE_END:]
    assert len(evidence['records']) == TOTAL
    for case in evidence['records']:
        n = case['message_ID']
        assert case['staged_reference'] == stage.previous.reference(rebound[n])
        assert storage[n].hex() == case['display_hex']
    image.replace_file(stage.ARM, arm)
    image.replace_file(stage.COMMON, common)
    assert bytes(image.rom.save()) == RESEARCH.read_bytes()
    image.replace_file(stage.ARM, old_arm)
    image.replace_file(stage.COMMON, old_common)
    assert bytes(image.rom.save()) == Path(parent_release['candidate']).read_bytes()
    return arm, common


def verification_scope(approved, live):
    assert approved['live_messages'] == live['observed_ids'] == [row[0] for row in verification.CASES]
    assert approved['stored_cases'] == TOTAL and approved['viewed_pages'] >= TOTAL
    assert live['ordinary_gameplay'] and not live['fixtures'] and not live['hardware']
    assert live['original_Price_Info_return'] and live['complete_pagination_and_exact_display']
    return dict(observed_notice_IDs=live['observed_ids'], stored_cases=TOTAL, viewed_pages=approved['viewed_pages'],
        actual_pages=sum(len(row['pages']) for row in live['observed']), original_Price_Info_return=True,
        ordinary_gameplay=True, inventory_or_eligibility_fixture=False, hardware=False)


def final_review(draft, evidence, scope):
    records = []
    for row, case in zip(draft['records'], evidence['records'], strict=True):
        n = case['message_ID']
        assert row['id'] == f'COMMON_MESSAGE_{n}'
        assert case['source_reference'] == row['source_reference']
        assert case['previous_reference'] == row['current_reference']
        records.append(row | dict(
            context=f'The Price Info window shows the {row["commodity_name"]} title, icon and price. Selecting '
                    'the commodity opens its separate speakerless description in the original mode-zero popup.',
            review=row['review'] | {'context': True, 'formatting': True}, new_credit=1,
            registered_reference=case['staged_reference'] | {'exact_stored_hex': case['display_hex'],
                'ROM_sha256': evidence['research_ROM_sha256']}, native_pages=case['pages'],
            original_substitutions=case['substitutions'], gameplay_observed=n in scope['observed_notice_IDs']))
    assert len(records) == TOTAL and Counter(row['decision'] for row in records) == {
        'revision': REVISED, 'retention': RETAINED}
    result = dict(translation_policy='natural-dialogue-v2', target_locale='en-US', encoder='dialogue-relocatable-v1',
        review_gates=['source', 'context', 'localization', 'naturalness', 'formatting'], records=records,
        native_selector=draft['native_selector'], actual_verification_scope=scope, full_goal_complete=False)
    validate_natural_dialogue_batch(result)
    return result


def publish(release):
    summary = 'All 124 Price Info trade-good descriptions are registered. The ledger now credits 27,093 reviews.'
    scope = release['actual_verification_scope']
    notes = f"""# All Routes Trade Good Descriptions candidate

Use [{ROM.name}](../../{ROM.as_posix()}) with its build manifest. The [clean-input patch](translation.xdelta) rebuilds it byte for byte from clean Japanese SHA-256 `{release['clean_input_sha256']}`. Candidate SHA-256 `{release['candidate_sha256']}`. Patch SHA-256 `{release['patch_sha256']}`.

{summary} Ninety-seven revisions and 27 justified retentions include replacements for generic placeholders and unrelated save prompts. Only the COMMON archive and its native ARM9 pointer and size table changed. The original modal, ASCII right bounds and Market Goods Info fixes carry forward.

All {scope['viewed_pages']} pages passed native and visual review. The ordinary Lisbon replay used a copied save and the original Price Info controls. It verified {scope['actual_pages']} pages, original advancement and return to the selected commodity. The cold boot, 24 protected name getters, 34 targeted repository tests and all 99 release checks passed. [Gameplay](verification/{LIVE_VERIFICATION.name}) · [Exact records](verification/registered_review.json)
"""
    (PACKAGE / 'README.md').write_text(notes, encoding='utf-8', newline='\n')
    base.save(PACKAGE / 'checksums.json', {p.relative_to(PACKAGE).as_posix(): base.digest(p)
        for p in sorted(PACKAGE.rglob('*')) if p.is_file() and p.name != 'checksums.json'})
    pin_path = Path('translations/rom_retention_pins.json')
    pins = base.load(pin_path)
    retained_roms = [stage.first.ROM, RESEARCH, ROM]
    if stage.third.ROM.is_file():
        retained_roms.append(stage.third.ROM)
    for path in retained_roms:
        resolved = str(path.resolve())
        assert path.is_file() and not any(row['path'] == resolved for row in pins)
        pins.append(dict(path=resolved, reason=f'Preserve the Price Info description build. SHA256 {base.digest(path)}'))
    base.replace_checked(pin_path, (json.dumps(pins, ensure_ascii=False, indent=2) + '\n').replace('\n', '\r\n').encode('utf-8'))
    doc = f"""# Price Info trade-good descriptions registered

{summary} COMMON 137–260 supplies the original modal through the bounded commodity selector. An ordinary Lisbon replay confirmed that the predecessor displayed an unrelated save prompt for Wheat. This release replaces the placeholder and unrelated text with descriptions of the goods. [Exact records](../{REVIEW.as_posix()}) · [Release and patch](../{PACKAGE.as_posix()}/README.md)

All {scope['viewed_pages']} native pages preserve complete glyphs, including the first letter after each break. The compiler protects the existing ASCII pair phase and groups rows for the native four-row pages. The release preserves all other selected COMMON spans and the native layout, controls and price behavior. The original Price Info replay verified {scope['actual_pages']} pages and dismissal with no inventory or eligibility fixture.

There are 883 other native shared keys to review or classify. The next sailing review can start with COMMON 2454–2483. Its four intact source voice tables at `02117180`, `021171C0`, `02117220` and `02117240` cover returning wind, sympathy for the creature, a sighting and reef armor reports. The unresolved Market 750–752 and the legacy New Game records 104–107 still need consumer classification. Shared exchanges, remaining player-facing text, retrospective names, roles, wraps and glyphs, and representative town and random-scene testing stay in scope. Deferred artwork and the later older-record technical re-audit remain separate.
"""
    base.replace_checked(DOC, doc.encode('utf-8'))
    lead = f'# Current editorial checkpoint - 2026-11-11\n\n{summary}\n\nContinue from [the registered Price Info descriptions]({DOC.name}).\n\n'
    for name in ('editorial_handoff_current.md', 'editorial_efficiency_workflow.md', 'translation_progress.md'):
        path = Path('docs') / name
        base.replace_checked(path, lead.encode('utf-8') + path.read_bytes())
    continuity = Path('docs/build_continuity_protocol.md')
    protocol = ('The 124 Price Info descriptions are registered with 764 entries, 114 accepted layers and 99 checks. '
                'Use scripts/register_trade_good_descriptions_v1.py with --register and --publish-prepared. '
                f'Exact reconstruction, ordinary Price Info replay and cold startup pass. [Checkpoint]({DOC.name})\n\n')
    base.replace_checked(continuity, protocol.encode('utf-8') + continuity.read_bytes())
    print('Registered 764 entries and credited all 124 Price Info descriptions once.')


def environment():
    return vars(transaction) | globals()


def register():
    code = checked_text(getsource(transaction.register), {
        "'item-production-and-voyage-advice'": "'price-info-trade-good-descriptions'",
        'Twenty-four item advice replies are registered.': 'All 124 Price Info trade-good descriptions are registered.',
        '== 26775': '== 27093', '== 16001': '== 16230', '== 10774': '== 10863',
        "== 758 and len(manifest['checks']) == 93": "== 763 and len(manifest['checks']) == 98",
        'release_stack_before_item_production_advice.json': 'release_stack_before_trade_good_descriptions.json',
        'verified_promotional_item_cards_predecessor=predecessor, item_production_advice_release=str(REVIEW)':
            'verified_proof_and_relic_advice_predecessor=predecessor, trade_good_descriptions_release=str(REVIEW)',
        'Reviewed item production and voyage-supply advice with scoped portrait wraps.':
            'Reviewed the native Price Info descriptions with word wrapping and pagination.',
        'release_stack.item_production_advice.pending.json': 'release_stack.trade_good_descriptions.pending.json',
        'COMMON_ITEM_PRODUCTION_ADVICE_PORTRAIT_WRAP': 'COMMON_PRICE_INFO_DESCRIPTION_DIRECTORY_AND_POINTERS',
        '"evidence[\'wrapper\']": "evidence[\'ownership\']"':
            '"evidence[\'wrapper\']": "dict(native_directory_and_pointer_updates_only=True, runtime_code_changed=False)"',
        "manifest['item_production_advice_registered_successor_pipeline']":
            "manifest['trade_good_descriptions_registered_successor_pipeline']",
        "== 759 and len(manifest['checks']) == 94": "== 764 and len(manifest['checks']) == 99",
        'registered_manifest_entries=759, accepted_layers=114, passing_release_checks=94, repository_tests=34':
            'registered_manifest_entries=764, accepted_layers=114, passing_release_checks=99, repository_tests=34',
        'Item advice registration staged and ready to publish.': 'Price Info registration staged and ready to publish.',
        'live_check.verified.VISUAL': 'verification.VISUAL',
        'transaction.preserve_compression': 'transaction.transaction.preserve_compression',
    })
    env = environment()
    exec(compile(code, __file__ + '::registered-price-info-transaction', 'exec'), env)
    env['register']()


def publish_prepared():
    code = checked_text(getsource(transaction.publish_prepared), {
        'release_stack.item_production_advice.pending.json': 'release_stack.trade_good_descriptions.pending.json',
        'vars(transaction)': 'vars(transaction.transaction)',
        'FunctionType(transaction.verify_prepared.__code__, env)':
            'FunctionType(transaction.transaction.verify_prepared.__code__, env)',
        'inspect.getsource(transaction.publish_prepared)': 'inspect.getsource(transaction.transaction.publish_prepared)',
    })
    env = environment()
    exec(compile(code, __file__ + '::atomic-price-info-publication', 'exec'), env)
    env['publish_prepared']()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    action = parser.add_mutually_exclusive_group(required=True)
    action.add_argument('--register', action='store_true')
    action.add_argument('--publish-prepared', action='store_true')
    (publish_prepared if parser.parse_args().publish_prepared else register)()
