"""Register the verified leak, fire, and supply reports over the mutiny candidate."""

import argparse
from collections import Counter
from hashlib import sha256
import inspect
import json
from pathlib import Path
from types import FunctionType

from dk4tool.dialogue.review import validate_natural_dialogue_batch
from dk4tool.patch import ship_emergency_wrap_v1 as wrap
from dk4tool.rom.nds import NdsImage
from dk4tool.script.common_message_table import DIRECTORY_OFFSET, TABLE_OFFSET
from scripts import register_diplomatic_outcomes_v2 as base
from scripts import register_mutiny_review_v1 as previous
from scripts import register_sea_event_review_v2 as transaction
from scripts.audit_story_glyph_consistency import load, save
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest
from scripts.package_ship_command_candidate_v1 import replace_checked
from scripts.seal_shared_text_source_v1 import ARM, COMMON, reference
from scripts.source_locked_derivation_v5118 import checked_text
from scripts.stage_ship_emergency_balanced_v2 import DYNAMIC, STATIC, OUTPUT, PROOF as EVIDENCE, ROM as RESEARCH, first
from scripts.stage_shared_notices_storage_v1 import relocate
from scripts.verify_ship_emergency_release_inputs_v1 import BOOT as STARTUP_VERIFICATION, CHECKPOINT, LIVE as LIVE_VERIFICATION, QA


PARENT = previous.RELEASE
PROFILE = 'all-routes-ship-emergency-editorial-v1-20261111'
FAMILY = 'shared_ship_emergencies_and_supplies_20261111'
CHECK = 'registered_ship_emergency_display_live_and_complete_parent_inverse'
PACKAGE = Path('releases/all_routes_editorial_20261111_ship_emergency_candidate')
VERIFICATION = PACKAGE / 'verification'
RELEASE = VERIFICATION / 'registered_release_verification.json'
REVIEW = VERIFICATION / 'registered_review.json'
TEST = Path('out/ship_emergency_registered_20261111_v1')
ROM = TEST / 'Translation_DS_All_Routes_Ship_Emergency_20261111_candidate.nds'
MANIFEST = ROM.with_suffix('.manifest.json')
PATCH = PACKAGE / 'translation.xdelta'
DOC = Path('docs/editorial_ship_emergency_registered_20261111.md')
PENDING_LEDGER = TEST / 'editorial_review_current.ship_emergency.pending.json'
MUTATION_PLAN = VERIFICATION / 'registration_mutation_plan.json'
ORDINARY = first.PROOF
TOTAL, REVISED, RETAINED = 41, 32, 9
PREVIOUS_TOTAL = 26179


def rebuild(parent, evidence, source):
    image = NdsImage.open(parent['candidate'])
    old_arm, old_common = image.read_file(ARM), image.read_file(COMMON)
    assembly = FunctionType(wrap.assembly.__code__, {**wrap.assembly.__globals__, 'DYNAMIC': DYNAMIC, 'STATIC': STATIC})
    transform = FunctionType(wrap.transform.__code__, {**wrap.transform.__globals__, 'assembly': assembly})
    patched, selector = transform(old_arm)
    assert json.loads(json.dumps(selector)) == evidence['selector']
    directory = sha256(old_arm[DIRECTORY_OFFSET:TABLE_OFFSET]).hexdigest()
    repack = FunctionType(relocate.__code__, {**relocate.__globals__, 'DIRECTORY': directory})
    rows = {row['message_ID']: row for row in source['records']}
    cases = {row['message_ID']: row for row in evidence['stored']}
    assert cases.keys() == rows.keys() and len(cases) == TOTAL
    # The stored report lists lookups by native ID. Repacking records changed
    # IDs in the same static-then-substitution order as the stage compiler.
    ordered_ids = sorted(cases, key=lambda n: bool(rows[n]['original_substitutions']))
    storage = {n: bytes.fromhex(cases[n]['staged_hex']) for n in ordered_ids}
    assert all(b' '.join(raw.split()) == rows[n]['english'].encode('ascii') for n, raw in storage.items())
    common, arm, rebound, packing = repack(old_common, patched, rows, storage)
    assert json.loads(json.dumps(packing)) == evidence['storage']
    assert all(case['staged_reference'] == reference(rebound[n]) for n, case in cases.items())
    image.replace_file(ARM, arm)
    image.replace_file(COMMON, common)
    assert bytes(image.rom.save()) == RESEARCH.read_bytes()
    image.replace_file(ARM, old_arm)
    image.replace_file(COMMON, old_common)
    assert bytes(image.rom.save()) == Path(parent['candidate']).read_bytes()
    return arm, common


def verification_scope(approved):
    observed = approved['live_messages']
    assert len(observed) == 2 and 573 <= observed[0] <= 579 and 601 <= observed[1] <= 608
    assert approved['stored_cases'] == TOTAL and approved['native_expansions'] == 109
    assert approved['fresh_viewed_pages'] + approved['reused_exact_viewed_pages'] == 101
    return dict(observed_notice_IDs=observed, stored_templates=TOTAL, native_expansions=109,
        fresh_viewed_pages=approved['fresh_viewed_pages'], reused_exact_viewed_pages=approved['reused_exact_viewed_pages'],
        native_selector_cases=approved['native_selector_cases'], crew_voice_choices=approved['crew_voice_choices'],
        fixture_scope='One temporary native condition selection per isolated voyage',
        original_flagship_warning_and_dismissal=True, original_food_and_water_depletion=True,
        named_ship_fire_and_automatic_travel_variants_offline_only=True, hardware=False)


def final_review(source, evidence, scope):
    stored = {row['message_ID']: row for row in evidence['stored']}
    records = []
    for row in source['records']:
        n = row['message_ID']
        case = stored[n]
        assert row['source_reference'] == case['source_reference'] and row['current_reference'] == case['current_reference']
        pages = [item for item in evidence['native_cases'] if item['message_ID'] == n]
        assert pages and len(pages) == (5 if 580 <= n <= 584 or 593 <= n <= 600 else
                                        2 if 601 <= n <= 608 else 3 if 610 <= n <= 613 else 1)
        records.append(row | dict(review=row['review'] | {'formatting': True},
            registered_reference=case['staged_reference'] | {'exact_stored_hex': case['staged_hex'],
                'ROM_sha256': evidence['research_ROM_sha256']},
            displayed_variants=[dict(arguments=item['arguments'], display_hex=item['display_hex'],
                protected_phrases=item['protected_phrases'], ink_sha256=item['native_ink_sha256']) for item in pages],
            gameplay_observed=n in scope['observed_notice_IDs'], new_credit=1))
    assert len(records) == TOTAL and Counter(row['decision'] for row in records) == {'revision': REVISED, 'retention': RETAINED}
    review = dict(translation_policy='natural-dialogue-v2', target_locale='en-US',
        encoder='dialogue-relocatable-v1', review_gates=source['review_gates'],
        records=records, actual_verification_scope=scope, full_goal_complete=False)
    validate_natural_dialogue_batch(review)
    return review


def publish(release):
    summary = 'The 41 leak, fire, and supply reports are registered. The ledger now credits 26,220 reviews.'
    notes = f"""# All Routes ship emergency candidate

Use `{ROM.as_posix()}` beside its build manifest. The [clean-input patch](translation.xdelta) applies to clean Japanese SHA-256 `{release['clean_input_sha256']}` and reconstructs candidate SHA-256 `{release['candidate_sha256']}` byte for byte. Patch SHA-256 is `{release['patch_sha256']}`.

{summary} The batch has 32 revisions and nine justified retentions. It restores the flagship and other-ship distinctions, uncertainty about hull damage, and the complete fire and automatic-travel reports. The original ship-name and supply arguments stay in place. All 109 native expansions, 74 cumulative release checks, and 30 targeted tests passed. Promotion awaits acceptance.

Two focused emulator voyages displayed the flagship leak through dismissal and both Food and Water warnings after the original mutiny outcome. Each used one temporary encounter selection. The named-ship, fire, and automatic-travel alternatives passed offline. The candidate passed its own 31,000-frame startup and 24 protected name getters. [Gameplay verification](verification/ship_emergency_gameplay_verification.json) · [Registered review](verification/registered_review.json)
"""
    (PACKAGE / 'README.md').write_text(notes, encoding='utf-8', newline='\n')
    save(PACKAGE / 'checksums.json', {p.relative_to(PACKAGE).as_posix(): digest(p)
        for p in sorted(PACKAGE.rglob('*')) if p.is_file()})
    pins_path = Path('translations/rom_retention_pins.json')
    pins = load(pins_path)
    for path, expected, role in (
        (first.ROM, load(ORDINARY)['research_ROM_sha256'], 'first-pass emergency research ROM'),
        (RESEARCH, release['candidate_sha256'], 'balanced emergency research ROM'),
        (ROM, release['candidate_sha256'], 'registered emergency ROM'),
    ):
        assert digest(path) == expected and not any(row['path'] == str(path.resolve()) for row in pins)
        pins.append(dict(path=str(path.resolve()), reason=f'Preserve {role}. SHA256 {expected}'))
    replace_checked(pins_path, (json.dumps(pins, ensure_ascii=False, indent=2) + '\n').replace('\n', '\r\n').encode('utf-8'))
    doc = f"""# Ship emergency reports registered

{summary} The build includes the mutiny release, 114 accepted layers, the Market correction, and the ASCII right-bound fix. [Release package](../{PACKAGE.as_posix()}/README.md) · [Exact registered review](../{REVIEW.as_posix()})

The source distinguishes damage to the bottom of the hull, a named ship's leak or fire, an exhausted supply, and cancellation of automatic travel. The review preserves the original name getter, both supply labels, and the original order of the two automatic-travel arguments. The native renderer keeps long, Japanese, and macro-like ship names intact. Complete sentences in the automatic-travel reports now occupy separate rows. The fire response keeps “We put the fire out!” together.

All 41 stored templates, 109 native expansions, 101 distinct viewed pages, 1,242 voice choices, 30 targeted tests, 24 protected getters, and the 31,000-frame startup passed. The two focused replays verified the flagship leak and dismissal, and the Food and Water warnings after normal resource depletion in the initialized mutiny voyage. The fire, named-ship, and automatic-travel displays are offline coverage.

Continue with the fleet encounters beginning at 614. The Market replies, remaining town and random scenes, and remaining player-facing text stay in scope. Deferred artwork and the older-record technical re-audit stay separate.
"""
    replace_checked(DOC, doc.encode('utf-8'))
    lead = f'# Current editorial checkpoint - 2026-11-11\n\n{summary}\n\nContinue from [the registered emergency checkpoint]({DOC.name}).\n\n'.encode('utf-8')
    for name in ('editorial_handoff_current.md', 'editorial_efficiency_workflow.md', 'translation_progress.md'):
        path = Path('docs') / name
        replace_checked(path, lead + path.read_bytes())
    print('Registered 739 entries and credited 41 emergency reports once.')


def register():
    manifest = load(load(PARENT)['manifest'])
    driver = manifest['mutiny_registered_successor_pipeline']
    assert digest(previous.__file__) == driver['driver_sha256']
    env = {**vars(base), **globals(), 'preserve_compression': transaction.preserve_compression}
    ledger = checked_text(inspect.getsource(base.update_ledger), {
        "'diplomatic-and-scheme-outcome-notices'": "'shared-ship-emergencies-and-supplies'",
        'Thirty-four diplomacy and scheme outcomes are registered.': 'Forty-one leak, fire, and supply reports are registered.',
        '== 25985': '== 26220', '== 15438': '== 15605', '== 10547': '== 10615',
    })
    old_scope = """    scope = dict(observed_notice_IDs=approved['live_messages'], stored_cases=176, fresh_viewed_pages=31,
        reused_exact_viewed_pages=145, fixture_scope='One incoming letter in a previously empty isolated RAM slot',
        original_no_preserved_war=True, natural_letter_generation=False, hardware=False)"""
    registration = checked_text(inspect.getsource(base.register), {
        "approved['live_messages'] == [349, 356, 352]": "approved['live_messages'] == live['observed_notice_IDs']",
        "sum(int(s.get('tests', 0)) for s in tests) == 27": "sum(int(s.get('tests', 0)) for s in tests) == 30",
        "len(manifest['batches']) == 734 and len(manifest['checks']) == 69":
            "len(manifest['batches']) == 738 and len(manifest['checks']) == 73",
        old_scope: '    scope = verification_scope(approved)',
        'LIVE_VERIFICATION, STARTUP_VERIFICATION, QA):': 'LIVE_VERIFICATION, STARTUP_VERIFICATION, QA, ORDINARY):',
        'release_stack_before_diplomacy.json': 'release_stack_before_ship_emergency.json',
        'verified_crew_notice_predecessor=predecessor, diplomatic_outcome_release=str(REVIEW)':
            'verified_mutiny_predecessor=predecessor, ship_emergency_release=str(REVIEW)',
        'Reviewed diplomacy and scheme outcomes with scoped native phrase wrapping.':
            'Reviewed shared ship emergency and supply notices and their original arguments.',
        'release_stack.diplomacy.pending.json': 'release_stack.ship_emergency.pending.json',
        "LEDGER.with_name('editorial_review_current.diplomacy.pending.json')": 'PENDING_LEDGER',
        '    save(pending_registry, registry)':
            '    preserve_compression(pending_registry, REGISTRY)\n    save(pending_registry, registry)',
        "evidence['wrapper']": "evidence['selector']",
        'COMMON_DIPLOMATIC_OUTCOMES_MODAL_AND_PHRASE_WRAP': 'COMMON_SHIP_EMERGENCY_SCOPED_PHRASE_WRAP',
        "manifest['diplomatic_outcomes_registered_successor_pipeline']":
            "manifest['ship_emergency_registered_successor_pipeline']",
        "len(manifest['batches']) == 735 and len(manifest['checks']) == 70":
            "len(manifest['batches']) == 739 and len(manifest['checks']) == 74",
        'registered_manifest_entries=735, accepted_layers=114, passing_release_checks=70, repository_tests=27':
            'registered_manifest_entries=739, accepted_layers=114, passing_release_checks=74, repository_tests=30',
        '    pending_registry.replace(REGISTRY)\n    try:\n        pending_ledger.replace(LEDGER)\n    except OSError:\n        replace_checked(REGISTRY, before_registry)\n        raise\n    assert digest(REGISTRY) == release[\'registry_sha256\'] and digest(PROMOTED) == promoted\n    publish(release)':
            '    assert digest(PROMOTED) == promoted\n    print(\'Emergency registration staged and ready to publish.\')',
    })
    exec(compile(ledger + '\n\n' + registration, __file__ + '::ship-emergency-registration', 'exec'), env)
    env['register']()


def publish_prepared():
    env = {**vars(transaction), **globals(), 'prior': base}
    env['verify_prepared'] = FunctionType(transaction.verify_prepared.__code__, env)
    code = checked_text(inspect.getsource(transaction.publish_prepared), {
        'release_stack.sea_events.pending.json': 'release_stack.ship_emergency.pending.json',
    })
    exec(compile(code, __file__ + '::ship-emergency-publication', 'exec'), env)
    env['publish_prepared']()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    action = parser.add_mutually_exclusive_group(required=True)
    action.add_argument('--register', action='store_true')
    action.add_argument('--publish-prepared', action='store_true')
    if parser.parse_args().publish_prepared:
        publish_prepared()
    else:
        register()
