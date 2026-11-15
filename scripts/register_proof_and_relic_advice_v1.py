"""Register the final item Advice batch over its exact cumulative predecessor."""

import argparse
from inspect import getsource
import json
from pathlib import Path
from types import FunctionType, SimpleNamespace

from scripts import register_figurehead_navigation_gift_advice_v1 as parent
from scripts import register_item_production_advice_v1 as transaction
from scripts import stage_proof_and_relic_advice_v2 as layout
from scripts import verify_proof_and_relic_advice_v1 as verification
from scripts.source_locked_derivation_v5118 import checked_text


base = transaction.base
PARENT = parent.RELEASE
PROFILE = 'all-routes-proof-and-relic-advice-editorial-v1-20261111'
FAMILY = 'proof_and_relic_advice_contextual_20261111'
CHECK = 'registered_proof_and_relic_advice_native_live_and_complete_parent_inverse'
PACKAGE = Path('releases/all_routes_editorial_20261111_proof_and_relic_advice_candidate')
VERIFICATION = PACKAGE / 'verification'
RELEASE = VERIFICATION / 'registered_release_verification.json'
REVIEW = VERIFICATION / 'registered_review.json'
MUTATION_PLAN = VERIFICATION / 'registration_mutation_plan.json'
TEST = Path('out/proof_and_relic_advice_registered_20261111_v1')
ROM = TEST / 'Translation_DS_All_Routes_Proof_and_Relic_Advice_20261111_candidate.nds'
MANIFEST = ROM.with_suffix('.manifest.json')
PATCH = PACKAGE / 'translation.xdelta'
DOC = Path('docs/editorial_proof_and_relic_advice_registered_20261111.md')
PENDING_LEDGER = TEST / 'editorial_review_current.proof_and_relic_advice.pending.json'
OUTPUT, EVIDENCE, RESEARCH = layout.OUTPUT, layout.PROOF, layout.ROM
STARTUP_VERIFICATION, CHECKPOINT = verification.BOOT, verification.CHECKPOINT
LIVE_VERIFICATION, QA = verification.LIVE, verification.QA
PREVIOUS_TOTAL, TOTAL, REVISED, RETAINED = 26899, 70, 50, 20
stage = SimpleNamespace(**layout.stage_environment())
stage.ARM = stage.review.ARM


def verification_scope(approved, live):
    assert approved['live_messages'] == live['observed_ids'] == list(verification.OBSERVED)
    assert approved['stored_cases'] == approved['viewed_pages'] == TOTAL
    assert live['original_Advice_button'] and live['original_item_view_restored'] and live['original_town_return']
    assert live['complete_dialogue_ink_and_blank_cells_exact']
    assert all(row['header']['text'] == 'Hans Letzel' for row in live['observed'])
    assert [len(row['body_rows']) for row in live['observed']] == [4, 1, 2, 1]
    assert [row['text'] for row in live['observed'][2]['item_footer']] == ['Thales Paper Map', 'Advice', 'Use']
    assert [row['item_id'] for row in live['inventory_fixture']['items']] == list(verification.replay.ITEM_IDS)
    return dict(observed_notice_IDs=live['observed_ids'], stored_cases=TOTAL, viewed_pages=TOTAL,
        offline_actor_and_screen_cases=420, offline_native_portrait_cases=140,
        original_Advice_button_item_and_Lisbon_return=True, completed_map_Use_control_verified=True,
        natural_advice_unlock=False, hardware=False,
        fixture_scope='Original transfer code supplied the four items to a copied Lisbon save. The original '
                      'flag setter enabled Advice. Controller and stylus inputs opened and dismissed each reply.')


def publish(release):
    summary = 'The last 70 item-advice replies are registered. The ledger now credits 26,969 reviews.'
    notes = f"""# All Routes Proof and Relic Advice candidate

Use [{ROM.name}](../../{ROM.as_posix()}) with its build manifest. The [clean-input patch](translation.xdelta) reconstructs it byte for byte from the clean Japanese ROM with SHA-256 `{release['clean_input_sha256']}`. Expected ROM SHA-256 is `{release['candidate_sha256']}`. Patch SHA-256 is `{release['patch_sha256']}`.

{summary} Fifty revisions and twenty justified retentions restore the regional Proof of Conquest names, the distinction between Proofs and maps, clues for assembling maps, and the item-specific advice. The 20 treasure-map fragments now explain what the map leads to and that four fragments make a set.

All 70 pages passed visual review, with the last sheet reused byte for byte after the final revisions. All 140 native portraits and 420 original caller-fragment checks passed offline. The focused Lisbon replay opened the Old Parchment, Rigveda, Thales Paper Map and Stone Circle Map replies with the original Advice button and returned to Items and town. It used a copied save with isolated inventory and Advice fixtures. Other replies and Mikhail's branch were checked offline. All 98 release checks, 34 targeted tests, the cold boot and 24 protected name getters passed. [Gameplay verification](verification/proof_and_relic_advice_gameplay_verification.json) · [Exact record review](verification/registered_review.json)
"""
    (PACKAGE / 'README.md').write_text(notes, encoding='utf-8', newline='\n')
    base.save(PACKAGE / 'checksums.json', {p.relative_to(PACKAGE).as_posix(): base.digest(p)
        for p in sorted(PACKAGE.rglob('*')) if p.is_file() and p.name != 'checksums.json'})
    pin_path = Path('translations/rom_retention_pins.json')
    pins = base.load(pin_path)
    for path in (layout.first.ROM, RESEARCH, ROM):
        resolved = str(path.resolve())
        assert not any(row['path'] == resolved for row in pins)
        pins.append(dict(path=resolved, reason=f'Preserve the Proof and relic advice build. SHA256 {base.digest(path)}'))
    base.replace_checked(pin_path, (json.dumps(pins, ensure_ascii=False, indent=2) + '\n').replace('\n', '\r\n').encode('utf-8'))
    doc = f"""# Proof and relic advice registered

{summary} COMMON 3181–3250 finishes contextual review of the 218 item-advice messages. Fifty revisions and twenty justified retentions preserve the regional Proof of Conquest term, the map and assembly clues, crew-role advice and each adviser's degree of certainty. [Registered review](../{REVIEW.as_posix()}) · [Release and patch](../{PACKAGE.as_posix()}/README.md)

Only COMMON blocks 35–36 and the guarded portrait selector changed. The offline checks cover both advisers in Gallery and both Items consumers. The focused Lisbon replay covers one-, two- and four-row Hans replies with exact glyph and return-state checks. Other advice records and Mikhail's branch were checked offline.

The earlier coverage census leaves 1,007 other native shared keys for review or classification. Continue with shared exchanges and other player-facing text. Check older Proof of Conquest variants with their clean source and context, including earlier story uses of Supremacy. Retrospective names, roles, wraps and glyphs and representative town and random-scene testing remain in scope. Deferred artwork and the later older-record technical re-audit remain separate.
"""
    base.replace_checked(DOC, doc.encode('utf-8'))
    lead = f'# Current editorial checkpoint - 2026-11-11\n\n{summary}\n\nContinue from [the registered Proof and relic advice]({DOC.name}).\n\n'
    for name in ('editorial_handoff_current.md', 'editorial_efficiency_workflow.md', 'translation_progress.md'):
        path = Path('docs') / name
        base.replace_checked(path, lead.encode('utf-8') + path.read_bytes())
    continuity = Path('docs/build_continuity_protocol.md')
    protocol = ('The 70 Proof and relic advice replies are registered with 763 entries, 114 accepted layers and '
                '98 checks. Use scripts/register_proof_and_relic_advice_v1.py with --register and --publish-prepared. '
                f'Exact reconstruction, four Lisbon Advice portraits and cold startup pass. [Checkpoint]({DOC.name})\n\n')
    base.replace_checked(continuity, protocol.encode('utf-8') + continuity.read_bytes())
    print('Registered 763 entries and credited the final 70 item-advice reviews once.')


def environment():
    env = vars(transaction) | globals()
    env['rebuild'] = FunctionType(transaction.rebuild.__code__, env)
    env['final_review'] = FunctionType(transaction.final_review.__code__, env)
    return env


def register():
    code = checked_text(getsource(transaction.register), {
        "'item-production-and-voyage-advice'": "'proof-and-relic-advice'",
        'Twenty-four item advice replies are registered.': 'Seventy Proof and relic advice replies are registered.',
        '== 26775': '== 26969', '== 16001': '== 16133', '== 10774': '== 10836',
        "== 758 and len(manifest['checks']) == 93": "== 762 and len(manifest['checks']) == 97",
        'release_stack_before_item_production_advice.json': 'release_stack_before_proof_and_relic_advice.json',
        'verified_promotional_item_cards_predecessor=predecessor, item_production_advice_release=str(REVIEW)':
            'verified_figurehead_navigation_gift_advice_predecessor=predecessor, proof_and_relic_advice_release=str(REVIEW)',
        'Reviewed item production and voyage-supply advice with scoped portrait wraps.':
            'Reviewed regional Proof, map, and promotional relic advice with scoped portrait wraps.',
        'release_stack.item_production_advice.pending.json': 'release_stack.proof_and_relic_advice.pending.json',
        'COMMON_ITEM_PRODUCTION_ADVICE_PORTRAIT_WRAP': 'COMMON_PROOF_AND_RELIC_ADVICE_PORTRAIT_WRAP',
        "manifest['item_production_advice_registered_successor_pipeline']":
            "manifest['proof_and_relic_advice_registered_successor_pipeline']",
        "== 759 and len(manifest['checks']) == 94": "== 763 and len(manifest['checks']) == 98",
        'registered_manifest_entries=759, accepted_layers=114, passing_release_checks=94, repository_tests=34':
            'registered_manifest_entries=763, accepted_layers=114, passing_release_checks=98, repository_tests=34',
        'Item advice registration staged and ready to publish.': 'Proof and relic advice registration staged and ready to publish.',
        'live_check.verified.VISUAL': 'verification.VISUAL',
        'transaction.preserve_compression': 'transaction.transaction.preserve_compression',
    })
    env = environment()
    exec(compile(code, __file__ + '::registered-proof-and-relic-advice-transaction', 'exec'), env)
    env['register']()


def publish_prepared():
    code = checked_text(getsource(transaction.publish_prepared), {
        'release_stack.item_production_advice.pending.json': 'release_stack.proof_and_relic_advice.pending.json',
        'vars(transaction)': 'vars(transaction.transaction)',
        'FunctionType(transaction.verify_prepared.__code__, env)':
            'FunctionType(transaction.transaction.verify_prepared.__code__, env)',
        'inspect.getsource(transaction.publish_prepared)': 'inspect.getsource(transaction.transaction.publish_prepared)',
    })
    env = environment()
    exec(compile(code, __file__ + '::atomic-proof-and-relic-advice-publication', 'exec'), env)
    env['publish_prepared']()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    action = parser.add_mutually_exclusive_group(required=True)
    action.add_argument('--register', action='store_true')
    action.add_argument('--publish-prepared', action='store_true')
    (publish_prepared if parser.parse_args().publish_prepared else register)()
