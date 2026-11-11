"""Register the verified figurehead, navigation and gift advice batch."""

import argparse
from inspect import getsource
import json
from pathlib import Path
from types import FunctionType, SimpleNamespace

from scripts import register_item_production_advice_v1 as transaction
from scripts import register_crew_equipment_advice_v1 as parent
from scripts import stage_figurehead_navigation_gift_advice_v2 as layout
from scripts import verify_figurehead_navigation_gift_advice_v1 as verification
from scripts.source_locked_derivation_v5118 import checked_text


base = transaction.base
PARENT = parent.RELEASE
PROFILE = 'all-routes-figurehead-navigation-gift-advice-editorial-v1-20261111'
FAMILY = 'figurehead_navigation_gift_advice_contextual_20261111'
CHECK = 'registered_figurehead_navigation_gift_advice_native_live_and_complete_parent_inverse'
PACKAGE = Path('releases/all_routes_editorial_20261111_figurehead_navigation_gift_advice_candidate')
VERIFICATION = PACKAGE / 'verification'
RELEASE = VERIFICATION / 'registered_release_verification.json'
REVIEW = VERIFICATION / 'registered_review.json'
MUTATION_PLAN = VERIFICATION / 'registration_mutation_plan.json'
TEST = Path('out/figurehead_navigation_gift_advice_registered_20261111_v1')
ROM = TEST / 'Translation_DS_All_Routes_Figurehead_Navigation_Gift_Advice_20261111_candidate.nds'
MANIFEST = ROM.with_suffix('.manifest.json')
PATCH = PACKAGE / 'translation.xdelta'
DOC = Path('docs/editorial_figurehead_navigation_gift_advice_registered_20261111.md')
PENDING_LEDGER = TEST / 'editorial_review_current.figurehead_navigation_gift_advice.pending.json'
OUTPUT, EVIDENCE, RESEARCH = layout.OUTPUT, layout.PROOF, layout.ROM
STARTUP_VERIFICATION, CHECKPOINT = verification.BOOT, verification.CHECKPOINT
LIVE_VERIFICATION, QA = verification.LIVE, verification.QA
PREVIOUS_TOTAL, TOTAL, REVISED, RETAINED = 26865, 34, 23, 11


def stage_environment():
    first = layout.first
    env = vars(verification.stage) | vars(first.weapon) | vars(first) | vars(layout)
    env['review'] = verification.stage.review
    env['transform'] = FunctionType(first.weapon.transform.__code__, env)
    code = checked_text(getsource(first.base.stage), {
        "packing['touched_blocks'] == [33, 34]": "packing['touched_blocks'] == [35]",
    })
    exec(compile(code, __file__ + '::exact-advice-stage-reproduction', 'exec'), env)
    return SimpleNamespace(**env)


stage = stage_environment()


def verification_scope(approved, live):
    assert approved['live_messages'] == live['observed_ids'] == list(verification.OBSERVED)
    assert approved['stored_cases'] == approved['viewed_pages'] == TOTAL
    assert live['original_Advice_button'] and live['original_item_view_restored'] and live['original_town_return']
    assert live['complete_dialogue_ink_and_blank_cells_exact']
    assert all(row['header']['text'] == 'Hans Letzel' for row in live['observed'])
    assert [len(row['body_rows']) for row in live['observed']] == [1, 2, 3]
    assert [row['item_id'] for row in live['inventory_fixture']['items']] == [114, 127]
    assert [field['text'] for field in live['observed'][0]['item_footer']] == ['Sextant', 'Advice', 'Remove']
    return dict(observed_notice_IDs=live['observed_ids'], stored_cases=TOTAL, viewed_pages=TOTAL,
        offline_actor_and_screen_cases=204, offline_native_portrait_cases=68,
        original_Advice_button_item_and_Lisbon_return=True, equipped_tool_controls_verified=True,
        natural_advice_unlock=False, hardware=False,
        fixture_scope='The copied Lisbon save already held the equipped Sextant. The original transfer '
                      'supplied Eagle Figurehead and Frozen Rose, and the original flag setter enabled '
                      'Advice. Ordinary inputs displayed and dismissed the three Hans portraits.')


def publish(release):
    summary = 'The 34 figurehead, navigation and gift advice replies are registered. The ledger now credits 26,899 reviews.'
    notes = f"""# All Routes Figurehead, Navigation and Gift Advice candidate

Use [{ROM.name}](../../{ROM.as_posix()}) with its build manifest. The [clean-input patch](translation.xdelta) reconstructs it byte for byte from the clean Japanese ROM with SHA-256 '{release['clean_input_sha256']}'. Expected ROM SHA-256 is '{release['candidate_sha256']}'. Patch SHA-256 is '{release['patch_sha256']}'.

{summary} Twenty-three revisions and eleven justified retentions distinguish effects on a single ship from effects on the whole fleet, restore the adviser’s qualifications, and preserve regional gift clues such as the Frozen Rose and Bread Millstone suggestions.

All 34 final pages passed visual review. All 68 native portraits and 204 original caller-fragment cases passed offline. A focused emulator replay showed Hans Letzel’s Sextant, Eagle Figurehead and Frozen Rose replies, returned to each item with its original controls, then returned to Lisbon. The copied save already held the Sextant and used isolated fixtures for the other two items and the Advice flag. The other replies and Mikhail’s branch were checked offline. All 97 release checks, 34 targeted tests, the 31,000-frame cold boot and 24 protected name getters passed. [Gameplay proof](verification/figurehead_navigation_gift_advice_gameplay_verification.json) · [Exact record review](verification/registered_review.json)
"""
    (PACKAGE / 'README.md').write_text(notes, encoding='utf-8', newline='\n')
    base.save(PACKAGE / 'checksums.json', {p.relative_to(PACKAGE).as_posix(): base.digest(p)
        for p in sorted(PACKAGE.rglob('*')) if p.is_file() and p.name != 'checksums.json'})
    pin_path = Path('translations/rom_retention_pins.json')
    pins = base.load(pin_path)
    for path in (layout.first.ROM, RESEARCH, ROM):
        resolved = str(path.resolve())
        assert not any(row['path'] == resolved for row in pins)
        pins.append(dict(path=resolved, reason=f'Preserve the figurehead, navigation and gift advice build. SHA256 {base.digest(path)}'))
    base.replace_checked(pin_path, (json.dumps(pins, ensure_ascii=False, indent=2) + '\n').replace('\n', '\r\n').encode('utf-8'))
    doc = f"""# Figurehead, navigation and gift advice registered

{summary} COMMON 3147–3180 covers all ten figureheads, three navigation tools and 21 regional gifts. The original Gallery, compact item screen and regular Items continue selecting both advisers and the correct message by item index. [Registered review](../{REVIEW.as_posix()}) · [Release and patch](../{PACKAGE.as_posix()}/README.md)

Only COMMON block 35 and the guarded portrait selector changed. All other selected COMMON spans and the 123,264-byte copied allocation remain exact. The replay verified the full Hans nameplate and complete one-, two- and three-row replies. The equipped Sextant retained the Remove control when Advice closed. Both other item screens and the original Lisbon view returned exactly.

Continue at COMMON 3181 with Proof and map advice. Compare regional Proofs, their completed maps, ruin maps and unfinished map components in related groups. The reviewed Help topic 4 uses Proof of Conquest. Older story variants and remaining player-facing text and speaker labels stay in scope. Graphics artwork and the later older-record technical re-audit remain separate.
"""
    base.replace_checked(DOC, doc.encode('utf-8'))
    lead = f'# Current editorial checkpoint - 2026-11-11\n\n{summary}\n\nContinue from [the registered figurehead, navigation and gift advice]({DOC.name}).\n\n'
    for name in ('editorial_handoff_current.md', 'editorial_efficiency_workflow.md', 'translation_progress.md'):
        path = Path('docs') / name
        base.replace_checked(path, lead.encode('utf-8') + path.read_bytes())
    continuity = Path('docs/build_continuity_protocol.md')
    protocol = (
        'The 34 figurehead, navigation and gift replies are registered over Crew Equipment Advice with '
        '762 entries, 114 accepted layers and 97 checks. Use scripts/register_figurehead_navigation_gift_advice_v1.py with '
        f'--register and --publish-prepared. Exact reconstruction, three Lisbon Advice portraits '
        f'and cold startup pass. [Registered checkpoint]({DOC.name})\n\n')
    base.replace_checked(continuity, protocol.encode('utf-8') + continuity.read_bytes())
    print('Registered 762 entries and credited 34 figurehead, navigation and gift advice reviews once.')


def environment():
    env = vars(transaction) | globals()
    env['rebuild'] = FunctionType(transaction.rebuild.__code__, env)
    env['final_review'] = FunctionType(transaction.final_review.__code__, env)
    return env


def register():
    code = checked_text(getsource(transaction.register), {
        "'item-production-and-voyage-advice'": "'figurehead-navigation-and-gift-advice'",
        'Twenty-four item advice replies are registered.': 'Thirty-four figurehead, navigation and gift replies are registered.',
        '== 26775': '== 26899', '== 16001': '== 16083', '== 10774': '== 10816',
        "== 758 and len(manifest['checks']) == 93": "== 761 and len(manifest['checks']) == 96",
        'release_stack_before_item_production_advice.json': 'release_stack_before_figurehead_navigation_gift_advice.json',
        'verified_promotional_item_cards_predecessor=predecessor, item_production_advice_release=str(REVIEW)':
            'verified_crew_equipment_advice_predecessor=predecessor, figurehead_navigation_gift_advice_release=str(REVIEW)',
        'Reviewed item production and voyage-supply advice with scoped portrait wraps.':
            'Reviewed figurehead, navigation and gift advice with scoped portrait wraps.',
        'release_stack.item_production_advice.pending.json': 'release_stack.figurehead_navigation_gift_advice.pending.json',
        'COMMON_ITEM_PRODUCTION_ADVICE_PORTRAIT_WRAP': 'COMMON_FIGUREHEAD_NAVIGATION_GIFT_ADVICE_PORTRAIT_WRAP',
        "manifest['item_production_advice_registered_successor_pipeline']":
            "manifest['figurehead_navigation_gift_advice_registered_successor_pipeline']",
        "== 759 and len(manifest['checks']) == 94": "== 762 and len(manifest['checks']) == 97",
        'registered_manifest_entries=759, accepted_layers=114, passing_release_checks=94, repository_tests=34':
            'registered_manifest_entries=762, accepted_layers=114, passing_release_checks=97, repository_tests=34',
        'Item advice registration staged and ready to publish.':
            'Figurehead, navigation and gift advice registration staged and ready to publish.',
        'live_check.verified.VISUAL': 'verification.VISUAL',
        'transaction.preserve_compression': 'transaction.transaction.preserve_compression',
    })
    env = environment()
    exec(compile(code, __file__ + '::registered-catalogue-advice-transaction', 'exec'), env)
    env['register']()


def publish_prepared():
    code = checked_text(getsource(transaction.publish_prepared), {
        'release_stack.item_production_advice.pending.json': 'release_stack.figurehead_navigation_gift_advice.pending.json',
        'vars(transaction)': 'vars(transaction.transaction)',
        'FunctionType(transaction.verify_prepared.__code__, env)':
            'FunctionType(transaction.transaction.verify_prepared.__code__, env)',
        'inspect.getsource(transaction.publish_prepared)': 'inspect.getsource(transaction.transaction.publish_prepared)',
    })
    env = environment()
    exec(compile(code, __file__ + '::atomic-catalogue-advice-publication', 'exec'), env)
    env['publish_prepared']()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    action = parser.add_mutually_exclusive_group(required=True)
    action.add_argument('--register', action='store_true')
    action.add_argument('--publish-prepared', action='store_true')
    (publish_prepared if parser.parse_args().publish_prepared else register)()
