"""Register the verified item-action and crew-management replies."""

import argparse
from collections import Counter
from inspect import getsource
import json
from pathlib import Path
from types import SimpleNamespace

from dk4tool.dialogue.review import validate_natural_dialogue_batch
from dk4tool.rom.nds import NdsImage
from scripts import register_sailing_reactions_v1 as predecessor
from scripts import verify_crew_item_actions_live_v1 as verified
from scripts.source_locked_derivation_v5118 import checked_text


transaction, parent, base = predecessor.transaction, predecessor.parent, predecessor.base
verification = SimpleNamespace(**(vars(verified) | {'VISUAL': verified.checked.VISUAL}))
stage = SimpleNamespace(**verification.stage.stage_environment())
PARENT = predecessor.RELEASE
PROFILE = 'all-routes-crew-item-actions-editorial-v1-20261111'
FAMILY = 'crew_item_actions_contextual_20261111'
CHECK = 'registered_crew_item_actions_native_live_and_complete_parent_inverse'
PACKAGE = Path('releases/all_routes_editorial_20261111_crew_item_actions_candidate')
VERIFICATION = PACKAGE / 'verification'
RELEASE = VERIFICATION / 'registered_release_verification.json'
REVIEW = VERIFICATION / 'registered_review.json'
MUTATION_PLAN = VERIFICATION / 'registration_mutation_plan.json'
TEST = Path('out/crew_item_actions_registered_20261111_v1')
ROM = TEST / 'Translation_DS_All_Routes_Crew_Item_Actions_20261111_candidate.nds'
MANIFEST = ROM.with_suffix('.manifest.json')
PATCH = PACKAGE / 'translation.xdelta'
DOC = Path('docs/editorial_crew_item_actions_registered_20261111.md')
PENDING_LEDGER = TEST / 'editorial_review_current.crew_item_actions.pending.json'
OUTPUT, EVIDENCE, RESEARCH = verification.stage.OUTPUT, stage.PROOF, stage.ROM
STARTUP_VERIFICATION, CHECKPOINT = verification.checked.BOOT, verification.CHECKPOINT
LIVE_VERIFICATION, QA, VISUAL = verification.LIVE, verification.checked.QA, verification.checked.VISUAL
PREVIOUS_TOTAL, TOTAL, REVISED, RETAINED = 27146, 33, 24, 9


def rebuild(parent_release, evidence, draft):
    image = NdsImage.open(parent_release['candidate'])
    old_arm, old_common = image.read_file(stage.ARM), image.read_file(stage.COMMON)
    rows = {row['message_ID']: row for row in draft['records']}
    arm, common, storage, rebound, allocation, ownership = stage.stage(
        SimpleNamespace(arm=old_arm, common=old_common), parent_release, rows, draft['native_context'])
    assert json.loads(json.dumps(allocation)) == evidence['allocation']
    assert json.loads(json.dumps(ownership)) == evidence['ownership']
    assert evidence['parent_inverse_exact'] and len(evidence['records']) == TOTAL
    for case in evidence['records']:
        number = case['message_ID']
        assert case['staged_reference'] == verification.base.reference(rebound[number])
        assert storage[number].hex() == case['staged_hex']
    image.replace_file(stage.ARM, arm)
    image.replace_file(stage.COMMON, common)
    assert bytes(image.rom.save()) == RESEARCH.read_bytes()
    image.replace_file(stage.ARM, old_arm)
    image.replace_file(stage.COMMON, old_common)
    assert bytes(image.rom.save()) == Path(parent_release['candidate']).read_bytes()
    return arm, common


def verification_scope(approved, live):
    assert approved['live_messages'] == live['observed_ids'] == [2505, 2512, 2509]
    assert approved['stored_cases'] == TOTAL and approved['viewed_pages'] == 40
    assert live['actual_emulator'] and not live['hardware']
    assert live['original_item_use_and_return'] and live['successful_long_name_substitution']
    assert live['no_need_and_unavailable_replies']
    return dict(observed_notice_IDs=live['observed_ids'], stored_cases=TOTAL, viewed_pages=40,
        native_cases=46, actual_pages=len(live['observed']), original_item_use_and_return=True,
        successful_long_name_substitution=True, fixture_scope='Supplied item, fleet condition and one crew reassignment',
        normal_item_acquisition_verified=False, natural_event_selection=False, hardware=False)


def final_review(draft, evidence, scope):
    records = []
    for row, case in zip(draft['records'], evidence['records'], strict=True):
        number = case['message_ID']
        assert row['id'] == f'COMMON_MESSAGE_{number}' and row['message_ID'] == number
        assert case['source_reference'] == row['source_reference'] and case['previous_reference'] == row['current_reference']
        records.append(row | dict(review=row['review'] | {'formatting': True}, new_credit=1,
            registered_reference=case['staged_reference'] | {'exact_stored_hex': case['staged_hex'],
                'ROM_sha256': evidence['research_ROM_sha256']},
            native_displays=case['displays'], gameplay_observed=number in scope['observed_notice_IDs']))
    assert len(records) == TOTAL and Counter(row['decision'] for row in records) == {
        'revision': REVISED, 'retention': RETAINED}
    result = dict(translation_policy='natural-dialogue-v2', target_locale='en-US', encoder='dialogue-relocatable-v1',
        review_gates=['source', 'context', 'localization', 'naturalness', 'formatting'], records=records,
        native_context=draft['native_context'], actual_verification_scope=scope, full_goal_complete=False)
    validate_natural_dialogue_batch(result)
    return result


def publish(release):
    summary = 'All 33 crew item-action replies are registered. The ledger now credits 27,179 reviews.'
    notes = f"""# All Routes Crew Item Actions candidate

Use [{ROM.name}](../../{ROM.as_posix()}) with its adjacent manifest. The [clean-input patch](translation.xdelta) reconstructs it byte for byte from clean Japanese SHA-256 `{release['clean_input_sha256']}`. Candidate SHA-256 `{release['candidate_sha256']}`. Patch SHA-256 `{release['patch_sha256']}`.

{summary} The batch includes 24 revisions and nine justified retentions. It covers remedy use, required equipment, crew dismissals, Hermes’ Prayer and the Golden Cat. The native word wrapper keeps both substituted item names intact.

All 40 distinct native portrait pages received visual review. Two Items-menu replays on a copied save confirmed both refusal branches, successful use with the full Hua Tuo’s Tonic name, and the original returns. The replays supplied the item and condition, and moved one existing crew member for the successful use. Other variants received offline checks. Cold startup, 24 protected name getters, 34 targeted tests and 101 release checks passed. [Gameplay](verification/{LIVE_VERIFICATION.name}) · [Exact records](verification/registered_review.json)
"""
    (PACKAGE / 'README.md').write_text(notes, encoding='utf-8', newline='\n')
    base.save(PACKAGE / 'checksums.json', {p.relative_to(PACKAGE).as_posix(): base.digest(p)
        for p in sorted(PACKAGE.rglob('*')) if p.is_file() and p.name != 'checksums.json'})
    pin_path = Path('translations/rom_retention_pins.json')
    pins = base.load(pin_path)
    for path in (verification.stage.first.ROM, RESEARCH, ROM):
        resolved = str(path.resolve())
        assert path.is_file() and not any(row['path'] == resolved for row in pins)
        pins.append(dict(path=resolved, reason=f'Preserve the crew item-action build. SHA256 {base.digest(path)}'))
    base.replace_checked(pin_path, (json.dumps(pins, ensure_ascii=False, indent=2) + '\n')
        .replace('\n', '\r\n').encode('utf-8'))
    document = f"""# Crew item-action replies registered

{summary} COMMON 2500–2532 covers eight original tables and 18 caller sites. The three shared portrait wrappers passed 46 native display cases and 33 original stored lookups. The longer remedy name originally overflowed in one variant and broke across rows in two variants. Both approved item names now remain intact through the direct and queued paths. [Exact records](../{REVIEW.as_posix()}) · [Release and patch](../{PACKAGE.as_posix()}/README.md)

The emulator observed the no-need reply, the unavailable-specialist reply and the successful use of Hua Tuo’s Tonic through the original Items menu. The test used a copied save and supplied the item, condition and one crew reassignment for the success branch. The other replies have offline coverage.

797 shared native keys remain to review or classify. Start with COMMON 2533–2579, the fleet engagement, outcome and financial reports. Check the exact name and amount substitutions and the earlier battle-aftermath evidence before deciding which tests carry forward. Legacy New Game 104–107 and Market 750–752 still need consumer classification. Retrospective names, roles, wrapping and glyphs, other player-facing UI and representative town and random-scene coverage remain in scope. Deferred artwork and the later older-record technical re-audit remain separate.
"""
    base.replace_checked(DOC, document.encode('utf-8'))
    lead = f'# Current editorial checkpoint - 2026-11-11\n\n{summary}\n\nContinue from [the registered crew item actions]({DOC.name}).\n\n'
    for name in ('editorial_handoff_current.md', 'editorial_efficiency_workflow.md', 'translation_progress.md'):
        path = Path('docs') / name
        base.replace_checked(path, lead.encode('utf-8') + path.read_bytes())
    continuity = Path('docs/build_continuity_protocol.md')
    protocol = ('The 33 crew item-action replies are registered with 766 entries, 114 accepted layers and 101 checks. '
                'Use scripts/register_crew_item_actions_v1.py with --register and --publish-prepared. '
                f'Exact reconstruction, original Items transitions and cold startup pass. [Checkpoint]({DOC.name})\n\n')
    base.replace_checked(continuity, protocol.encode('utf-8') + continuity.read_bytes())
    print('Registered 766 entries and credited 33 crew item-action replies once.')


def environment():
    return predecessor.environment() | globals()


def register():
    source = checked_text(getsource(predecessor.register), {
        '"\'sailing-reactions\'"': '"\'crew-item-actions\'"',
        'Fifty-three sailing reactions are registered.': 'All 33 crew item-action replies are registered.',
        "'== 27146'": "'== 27179'", "'== 16265'": "'== 16289'", "'== 10881'": "'== 10890'",
        r"': '== 764 and len(manifest[\'checks\']) == 99',": r"': '== 765 and len(manifest[\'checks\']) == 100',",
        r"': '== 765 and len(manifest[\'checks\']) == 100',": r"': '== 766 and len(manifest[\'checks\']) == 101',",
        'registered_manifest_entries=765, accepted_layers=114, passing_release_checks=100':
            'registered_manifest_entries=766, accepted_layers=114, passing_release_checks=101',
        'verified_trade_good_descriptions_predecessor=predecessor, sailing_reactions_release=str(REVIEW)':
            'verified_sailing_reactions_predecessor=predecessor, crew_item_actions_release=str(REVIEW)',
        'Reviewed sailing reactions with scoped native phrase wrapping.':
            'Reviewed item-action replies with scoped native phrase wrapping and remedy names.',
        'release_stack_before_sailing_reactions': 'release_stack_before_crew_item_actions',
        'release_stack.sailing_reactions.pending': 'release_stack.crew_item_actions.pending',
        'COMMON_SAILING_REACTIONS_PORTRAIT_WRAP': 'COMMON_CREW_ITEM_ACTIONS_PORTRAIT_WRAP',
        'sailing_reactions_registered_successor_pipeline': 'crew_item_actions_registered_successor_pipeline',
        'Sailing reaction registration staged and ready to publish.': 'Crew item-action registration staged and ready to publish.',
    })
    env = environment()
    exec(compile(source, __file__ + '::derive-registration', 'exec'), env)
    env['register']()


def publish_prepared():
    source = checked_text(getsource(predecessor.publish_prepared), {
        'release_stack.sailing_reactions.pending': 'release_stack.crew_item_actions.pending',
    })
    env = environment()
    exec(compile(source, __file__ + '::derive-publication', 'exec'), env)
    env['publish_prepared']()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    action = parser.add_mutually_exclusive_group(required=True)
    action.add_argument('--register', action='store_true')
    action.add_argument('--publish-prepared', action='store_true')
    (publish_prepared if parser.parse_args().publish_prepared else register)()
