"""Register the sailing reactions over the cumulative Price Info release."""

import argparse
from collections import Counter
from inspect import getsource
import json
from pathlib import Path
from types import SimpleNamespace

from dk4tool.dialogue.review import validate_natural_dialogue_batch
from dk4tool.rom.nds import NdsImage
from scripts import register_trade_good_descriptions_v1 as parent
from scripts import verify_sailing_reactions_v1 as verification
from scripts.source_locked_derivation_v5118 import checked_text


transaction = parent.transaction
base, stage = transaction.base, verification.stage
PARENT = parent.RELEASE
PROFILE = 'all-routes-sailing-reactions-editorial-v1-20261111'
FAMILY = 'sailing_reactions_contextual_20261111'
CHECK = 'registered_sailing_reactions_native_live_and_complete_parent_inverse'
PACKAGE = Path('releases/all_routes_editorial_20261111_sailing_reactions_candidate')
VERIFICATION = PACKAGE / 'verification'
RELEASE = VERIFICATION / 'registered_release_verification.json'
REVIEW = VERIFICATION / 'registered_review.json'
MUTATION_PLAN = VERIFICATION / 'registration_mutation_plan.json'
TEST = Path('out/sailing_reactions_registered_20261111_v1')
ROM = TEST / 'Translation_DS_All_Routes_Sailing_Reactions_20261111_candidate.nds'
MANIFEST = ROM.with_suffix('.manifest.json')
PATCH = PACKAGE / 'translation.xdelta'
DOC = Path('docs/editorial_sailing_reactions_registered_20261111.md')
PENDING_LEDGER = TEST / 'editorial_review_current.sailing_reactions.pending.json'
OUTPUT, EVIDENCE, RESEARCH = stage.OUTPUT, stage.PROOF, stage.ROM
STARTUP_VERIFICATION, CHECKPOINT = verification.BOOT, verification.CHECKPOINT
LIVE_VERIFICATION, QA = verification.LIVE, verification.QA
PREVIOUS_TOTAL, TOTAL, REVISED, RETAINED = 27093, 53, 35, 18


def rebuild(parent_release, evidence, draft):
    image = NdsImage.open(parent_release['candidate'])
    old_arm, old_common = image.read_file(stage.ARM), image.read_file(stage.COMMON)
    rows = {row['message_ID']: row for row in draft['records']}
    arm, common, storage, rebound, allocation, ownership = stage.stage(
        SimpleNamespace(arm=old_arm, common=old_common), parent_release, rows)
    assert json.loads(json.dumps(allocation)) == evidence['allocation']
    assert json.loads(json.dumps(ownership)) == evidence['ownership']
    assert evidence['parent_inverse_exact'] and len(evidence['records']) == TOTAL
    for case in evidence['records']:
        n = case['message_ID']
        assert case['staged_reference'] == stage.editorial.previous.reference(rebound[n])
        assert storage[n].hex() == case['staged_hex']
    image.replace_file(stage.ARM, arm)
    image.replace_file(stage.COMMON, common)
    assert bytes(image.rom.save()) == RESEARCH.read_bytes()
    image.replace_file(stage.ARM, old_arm)
    image.replace_file(stage.COMMON, old_common)
    assert bytes(image.rom.save()) == Path(parent_release['candidate']).read_bytes()
    return arm, common


def verification_scope(approved, live):
    assert approved['live_messages'] == live['observed_ids'] and len(live['observed_ids']) == 3
    assert approved['stored_cases'] == approved['viewed_pages'] == TOTAL
    assert live['actual_emulator'] and not live['natural_event_selection'] and not live['hardware']
    assert live['original_wind_return'] and live['complete_white_whale_exchange']
    assert live['original_A_advancement_and_return'] and live['same_lookout_nameplate']
    return dict(observed_notice_IDs=live['observed_ids'], stored_cases=TOTAL, viewed_pages=TOTAL,
        actual_pages=len(live['observed']), original_A_advancement_and_return=True,
        complete_white_whale_exchange=True, fixture_scope='Original fleet condition setter for wind and whale',
        natural_event_selection=False, hardware=False)


def final_review(draft, evidence, scope):
    records = []
    for row, case in zip(draft['records'], evidence['records'], strict=True):
        n = case['message_ID']
        assert row['id'] == f'COMMON_MESSAGE_{n}' and row['message_ID'] == n
        assert case['source_reference'] == row['source_reference']
        assert case['previous_reference'] == row['current_reference']
        records.append(row | dict(
            review=row['review'] | {'formatting': True}, new_credit=1,
            registered_reference=case['staged_reference'] | {'exact_stored_hex': case['staged_hex'],
                'ROM_sha256': evidence['research_ROM_sha256']},
            native_consumer=case['native'], visible_lines=case['visible_lines'],
            gameplay_observed=n in scope['observed_notice_IDs']))
    assert len(records) == TOTAL and Counter(row['decision'] for row in records) == {
        'revision': REVISED, 'retention': RETAINED}
    result = dict(translation_policy='natural-dialogue-v2', target_locale='en-US', encoder='dialogue-relocatable-v1',
        review_gates=['source', 'context', 'localization', 'naturalness', 'formatting'], records=records,
        native_context=draft['native_context'], actual_verification_scope=scope, full_goal_complete=False)
    validate_natural_dialogue_batch(result)
    return result


def publish(release):
    summary = 'Fifty-three sailing reactions are registered. The ledger now credits 27,146 reviews.'
    notes = f"""# All Routes Sailing Reactions candidate

Use [{ROM.name}](../../{ROM.as_posix()}) with its adjacent manifest. The [clean-input patch](translation.xdelta) reconstructs it byte for byte from clean Japanese SHA-256 `{release['clean_input_sha256']}`. Candidate SHA-256 `{release['candidate_sha256']}`. Patch SHA-256 `{release['patch_sha256']}`.

{summary} The batch includes 35 revisions and 18 justified retentions for returning wind, the white whale, a glint on the water, reef armor, the ram breaking drift ice and treasure. The seven source table bindings preserve the original speaker selection.

All 53 pages passed native checks and visual review. A focused Hodram emulator replay supplied the two conditions through the original setter and confirmed the wind line, both whale remarks from the same lookout and the return to sailing. Reef, ram and treasure variants received offline checks. The cold boot, 24 protected name getters, 34 targeted tests and 100 release checks passed. [Gameplay](verification/{LIVE_VERIFICATION.name}) · [Exact records](verification/registered_review.json)
"""
    (PACKAGE / 'README.md').write_text(notes, encoding='utf-8', newline='\n')
    base.save(PACKAGE / 'checksums.json', {p.relative_to(PACKAGE).as_posix(): base.digest(p)
        for p in sorted(PACKAGE.rglob('*')) if p.is_file() and p.name != 'checksums.json'})
    pin_path = Path('translations/rom_retention_pins.json')
    pins = base.load(pin_path)
    for path in (stage.first.ROM, RESEARCH, ROM):
        resolved = str(path.resolve())
        assert path.is_file() and not any(row['path'] == resolved for row in pins)
        pins.append(dict(path=resolved, reason=f'Preserve the sailing reaction build. SHA256 {base.digest(path)}'))
    base.replace_checked(pin_path, (json.dumps(pins, ensure_ascii=False, indent=2) + '\n')
        .replace('\n', '\r\n').encode('utf-8'))
    doc = f"""# Sailing reactions registered

{summary} COMMON 2359–2365 and 2454–2499 cover seven native voice tables. The changes preserve the original speaker selection and pass the original loader and portrait checks. [Exact records](../{REVIEW.as_posix()}) · [Release and patch](../{PACKAGE.as_posix()}/README.md)

The focused emulator replay observed three messages, including both whale remarks from the same lookout, and verified the original return to sailing. It supplied the two conditions and left the original timer, dispatch, button advancement and presentation in use.

830 shared native keys remain to review or classify. Legacy New Game 104–107 and Market 750–752 still need consumer classification. Retrospective names, roles, wraps and glyphs and representative town and random-scene testing remain in scope. Deferred artwork and the older-record technical re-audit remain separate.
"""
    base.replace_checked(DOC, doc.encode('utf-8'))
    lead = f'# Current editorial checkpoint - 2026-11-11\n\n{summary}\n\nContinue from [the registered sailing reactions]({DOC.name}).\n\n'
    for name in ('editorial_handoff_current.md', 'editorial_efficiency_workflow.md', 'translation_progress.md'):
        path = Path('docs') / name
        base.replace_checked(path, lead.encode('utf-8') + path.read_bytes())
    continuity = Path('docs/build_continuity_protocol.md')
    protocol = ('The 53 sailing reactions are registered with 765 entries, 114 accepted layers and 100 checks. '
                'Use scripts/register_sailing_reactions_v1.py with --register and --publish-prepared. '
                f'Exact reconstruction, focused sailing replay and cold startup pass. [Checkpoint]({DOC.name})\n\n')
    base.replace_checked(continuity, protocol.encode('utf-8') + continuity.read_bytes())
    print('Registered 765 entries and credited 53 sailing reactions once.')


def environment():
    return vars(transaction) | vars(parent) | globals()


def register():
    source = checked_text(getsource(parent.register), {
        "'price-info-trade-good-descriptions'": "'sailing-reactions'",
        'All 124 Price Info trade-good descriptions are registered.': 'Fifty-three sailing reactions are registered.',
        "'== 27093'": "'== 27146'", "'== 16230'": "'== 16265'", "'== 10863'": "'== 10881'",
        '== 763 and len(manifest[\'checks\']) == 98': '== 764 and len(manifest[\'checks\']) == 99',
        '== 764 and len(manifest[\'checks\']) == 99': '== 765 and len(manifest[\'checks\']) == 100',
        'registered_manifest_entries=764, accepted_layers=114, passing_release_checks=99':
            'registered_manifest_entries=765, accepted_layers=114, passing_release_checks=100',
        'verified_proof_and_relic_advice_predecessor=predecessor, trade_good_descriptions_release=str(REVIEW)':
            'verified_trade_good_descriptions_predecessor=predecessor, sailing_reactions_release=str(REVIEW)',
        'Reviewed the native Price Info descriptions with word wrapping and pagination.':
            'Reviewed sailing reactions with scoped native phrase wrapping.',
        'release_stack_before_trade_good_descriptions': 'release_stack_before_sailing_reactions',
        'release_stack.trade_good_descriptions.pending': 'release_stack.sailing_reactions.pending',
        'COMMON_PRICE_INFO_DESCRIPTION_DIRECTORY_AND_POINTERS': 'COMMON_SAILING_REACTIONS_PORTRAIT_WRAP',
        '"dict(native_directory_and_pointer_updates_only=True, runtime_code_changed=False)"':
            r'''"evidence[\'ownership\']"''',
        'trade_good_descriptions_registered_successor_pipeline': 'sailing_reactions_registered_successor_pipeline',
        'Price Info registration staged and ready to publish.': 'Sailing reaction registration staged and ready to publish.',
    })
    env = environment()
    exec(compile(source, __file__ + '::derive-registration', 'exec'), env)
    env['register']()


def publish_prepared():
    source = checked_text(getsource(parent.publish_prepared), {
        'release_stack.trade_good_descriptions.pending': 'release_stack.sailing_reactions.pending',
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
