"""Register the verified Auto Move warning exchanges over the emergency candidate."""

import argparse
from collections import Counter
from hashlib import sha256
import inspect
import json
from pathlib import Path
from types import FunctionType

from dk4tool.dialogue.review import validate_natural_dialogue_batch
from dk4tool.rom.nds import NdsImage
from scripts import register_diplomatic_outcomes_v2 as base
from scripts import register_sea_event_review_v2 as transaction
from scripts import register_ship_emergency_review_v1 as previous
from scripts.audit_story_glyph_consistency import load, save
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest
from scripts.package_ship_command_candidate_v1 import replace_checked
from scripts.seal_shared_text_source_v1 import ARM, COMMON, reference
from scripts.source_locked_derivation_v5118 import checked_text
from scripts.stage_navigation_prerequisite_balanced_v2 import PROOF as EVIDENCE, ROM as RESEARCH, first
from scripts.stage_navigation_prerequisite_review_v1 import OUTPUT, rebuild_components
from scripts.verify_navigation_prerequisite_release_inputs_v1 import BOOT as STARTUP_VERIFICATION
from scripts.verify_navigation_prerequisite_release_inputs_v1 import CHECKPOINT, LIVE as LIVE_VERIFICATION, QA


PARENT = previous.RELEASE
PROFILE = 'all-routes-navigation-prerequisites-editorial-v1-20261111'
FAMILY = 'shared_navigation_prerequisites_20261111'
CHECK = 'registered_navigation_prerequisite_display_live_and_complete_parent_inverse'
PACKAGE = Path('releases/all_routes_editorial_20261111_navigation_prerequisites_candidate')
VERIFICATION = PACKAGE / 'verification'
RELEASE = VERIFICATION / 'registered_release_verification.json'
REVIEW = VERIFICATION / 'registered_review.json'
TEST = Path('out/navigation_prerequisites_registered_20261111_v1')
ROM = TEST / 'Translation_DS_All_Routes_Navigation_20261111_candidate.nds'
MANIFEST = ROM.with_suffix('.manifest.json')
PATCH = PACKAGE / 'translation.xdelta'
DOC = Path('docs/editorial_navigation_prerequisites_registered_20261111.md')
PENDING_LEDGER = TEST / 'editorial_review_current.navigation.pending.json'
MUTATION_PLAN = VERIFICATION / 'registration_mutation_plan.json'
ORDINARY = first.PROOF
TOTAL, REVISED, RETAINED = 24, 23, 1
PREVIOUS_TOTAL = 26220


def rebuild(parent, evidence, source):
    image = NdsImage.open(parent['candidate'])
    old_arm, old_common = image.read_file(ARM), image.read_file(COMMON)
    rows = {row['message_ID']: row for row in source['records']}
    cases = {row['message_ID']: row for row in evidence['stored']}
    assert cases.keys() == rows.keys() and len(cases) == TOTAL
    storage = {n: bytes.fromhex(case['staged_hex']) for n, case in cases.items()}
    assert all(b' '.join(raw.split()) == rows[n]['english'].encode('ascii') for n, raw in storage.items())
    arm, common, rebound, packing, selector = rebuild_components(old_arm, old_common, rows, storage)
    assert json.loads(json.dumps(selector)) == evidence['selector']
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
    assert approved['live_messages'] == [633, 646]
    assert approved['stored_cases'] == approved['native_pages'] == TOTAL
    assert approved['crew_voice_choices'] == 621 and approved['route_predicate_cases'] == 32
    assert [n for sheet in approved['viewed_sheets'] for n in sheet['messages']] == list(range(629, 653))
    return dict(observed_notice_IDs=approved['live_messages'], stored_templates=TOTAL,
        native_pages=TOTAL, viewed_pages=TOTAL, native_selector_cases=approved['native_selector_cases'],
        crew_voice_choices=approved['crew_voice_choices'], route_predicate_cases=approved['route_predicate_cases'],
        natural_Ceuta_missing_surveyor=True, focused_Stockholm_Cabin_display=True,
        fixture_scope='One temporary instruction supplies the second assignment failure on the Stockholm replay',
        both_returned_to_original_confirmation=True, route_failure_offline_only=True, hardware=False)


def final_review(source, evidence, scope):
    stored = {row['message_ID']: row for row in evidence['stored']}
    pages = {row['message_ID']: row for row in evidence['native_cases']}
    assert len(stored) == len(pages) == TOTAL
    records = []
    for row in source['records']:
        n = row['message_ID']
        case, page = stored[n], pages[n]
        assert row['source_reference'] == case['source_reference'] and row['current_reference'] == case['current_reference']
        records.append(row | dict(review=row['review'] | {'formatting': True},
            registered_reference=case['staged_reference'] | {'exact_stored_hex': case['staged_hex'],
                'ROM_sha256': evidence['research_ROM_sha256']},
            displayed_variants=[dict(display_hex=page['display_hex'], lines=page['visible_lines'],
                protected_phrases=page['protected_phrases'], ink_sha256=page['native_ink_sha256'])],
            gameplay_observed=n in scope['observed_notice_IDs'], new_credit=1))
    assert len(records) == TOTAL and Counter(row['decision'] for row in records) == {'revision': REVISED, 'retention': RETAINED}
    review = dict(translation_policy='natural-dialogue-v2', target_locale='en-US',
        encoder='dialogue-relocatable-v1', review_gates=source['review_gates'], records=records,
        native_navigation_predicate=source['native_navigation_predicate'],
        actual_verification_scope=scope, full_goal_complete=False)
    validate_natural_dialogue_batch(review)
    return review


def publish(release):
    summary = 'The 24 Auto Move warnings are registered. The ledger now credits 26,244 reviews.'
    notes = f"""# All Routes Auto Move candidate

Use `{ROM.as_posix()}` beside its build manifest. The [clean-input patch](translation.xdelta) applies to clean Japanese SHA-256 `{release['clean_input_sha256']}` and reconstructs SHA-256 `{release['candidate_sha256']}` byte for byte. Patch SHA-256 is `{release['patch_sha256']}`.

{summary} This batch includes 23 revisions and one justified retention. The missing Surveyor and missing route now appear as complete independent warnings. The Captain's Cabin requests preserve the address and use two readable lines. All 24 native pages, 75 cumulative release checks, and 30 targeted tests passed. Promotion awaits acceptance.

The normal Ceuta replay displayed the missing Surveyor warning. The focused Stockholm replay used a temporary instruction to select the Captain's Cabin warning. Both matched the complete native lettering and returned to the original confirmation. Route failure and the other voice alternatives passed offline. The candidate passed its own 31,000-frame startup and 24 protected name getters. [Gameplay verification](verification/navigation_gameplay_verification.json) · [Registered review](verification/registered_review.json)
"""
    (PACKAGE / 'README.md').write_text(notes, encoding='utf-8', newline='\n')
    save(PACKAGE / 'checksums.json', {p.relative_to(PACKAGE).as_posix(): digest(p)
        for p in sorted(PACKAGE.rglob('*')) if p.is_file()})
    pins_path = Path('translations/rom_retention_pins.json')
    pins = load(pins_path)
    for path, expected, role in (
        (first.ROM, load(ORDINARY)['research_ROM_sha256'], 'first-pass navigation research ROM'),
        (RESEARCH, release['candidate_sha256'], 'balanced navigation research ROM'),
        (ROM, release['candidate_sha256'], 'registered navigation ROM'),
    ):
        assert digest(path) == expected and not any(row['path'] == str(path.resolve()) for row in pins)
        pins.append(dict(path=str(path.resolve()), reason=f'Preserve {role}. SHA256 {expected}'))
    replace_checked(pins_path, (json.dumps(pins, ensure_ascii=False, indent=2) + '\n').replace('\n', '\r\n').encode('utf-8'))
    doc = f"""# Auto Move warnings registered

{summary} The build includes all 114 accepted layers, the Market correction, and the ASCII right-bound fix. [Release package](../{PACKAGE.as_posix()}/README.md) · [Exact registered review](../{REVIEW.as_posix()})

Records 629–652 cover the original missing Surveyor, missing route and Captain's Cabin branches. Record 636 stopped mid-word and 637 began with its tail. The revision restores the two separate warnings. The measured route line at 638 remains unchanged in prose because it clearly explains the original route failure. All eight Cabin variants preserve the address. The formatter keeps the room name and its short question tags together. The familiar request in 647 now occupies two rows with the wording intact.

All 24 stored and visually reviewed native pages, 621 voice selections, 32 focused predicate combinations, 30 targeted tests, 24 protected getters and the candidate's startup passed. Actual emulator coverage is the ordinary Ceuta warning and a focused Stockholm warning, both through dismissal to confirmation. The route-failure variants and hardware remain unvisited.

Continue with the sea approaches, fleet encounters and village visits at 1290–1356. The individual crew reactions starting at 1357 follow separately. Keep the unmapped 750–752 replies, remaining town and random scenes, and other player-facing text in scope. Deferred artwork and the older-record technical re-audit stay separate.
"""
    replace_checked(DOC, doc.encode('utf-8'))
    lead = f'# Current editorial checkpoint - 2026-11-11\n\n{summary}\n\nContinue from [the registered Auto Move checkpoint]({DOC.name}).\n\n'.encode('utf-8')
    for name in ('editorial_handoff_current.md', 'editorial_efficiency_workflow.md', 'translation_progress.md'):
        path = Path('docs') / name
        replace_checked(path, lead + path.read_bytes())
    print('Registered 740 entries and credited 24 Auto Move warnings once.')


def register():
    manifest = load(load(PARENT)['manifest'])
    driver = manifest['ship_emergency_registered_successor_pipeline']
    assert digest(previous.__file__) == driver['driver_sha256']
    env = {**vars(base), **globals(), 'preserve_compression': transaction.preserve_compression}
    ledger = checked_text(inspect.getsource(base.update_ledger), {
        "'diplomatic-and-scheme-outcome-notices'": "'shared-navigation-prerequisite-notices'",
        'Thirty-four diplomacy and scheme outcomes are registered.': 'Twenty-four Auto Move warnings are registered.',
        '== 25985': '== 26244', '== 15438': '== 15628', '== 10547': '== 10616',
    })
    old_scope = """    scope = dict(observed_notice_IDs=approved['live_messages'], stored_cases=176, fresh_viewed_pages=31,
        reused_exact_viewed_pages=145, fixture_scope='One incoming letter in a previously empty isolated RAM slot',
        original_no_preserved_war=True, natural_letter_generation=False, hardware=False)"""
    registration = checked_text(inspect.getsource(base.register), {
        "approved['live_messages'] == [349, 356, 352]": "approved['live_messages'] == live['observed_notice_IDs']",
        "sum(int(s.get('tests', 0)) for s in tests) == 27": "sum(int(s.get('tests', 0)) for s in tests) == 30",
        "len(manifest['batches']) == 734 and len(manifest['checks']) == 69":
            "len(manifest['batches']) == 739 and len(manifest['checks']) == 74",
        old_scope: '    scope = verification_scope(approved)',
        'release_stack_before_diplomacy.json': 'release_stack_before_navigation.json',
        'verified_crew_notice_predecessor=predecessor, diplomatic_outcome_release=str(REVIEW)':
            'verified_ship_emergency_predecessor=predecessor, navigation_prerequisite_release=str(REVIEW)',
        'Reviewed diplomacy and scheme outcomes with scoped native phrase wrapping.':
            'Reviewed the original Auto Move prerequisite warnings with scoped native phrase wrapping.',
        'release_stack.diplomacy.pending.json': 'release_stack.navigation.pending.json',
        "LEDGER.with_name('editorial_review_current.diplomacy.pending.json')": 'PENDING_LEDGER',
        '    save(pending_registry, registry)':
            '    preserve_compression(pending_registry, REGISTRY)\n    save(pending_registry, registry)',
        "evidence['wrapper']": "evidence['selector']",
        'COMMON_DIPLOMATIC_OUTCOMES_MODAL_AND_PHRASE_WRAP': 'COMMON_NAVIGATION_PREREQUISITE_SCOPED_PHRASE_WRAP',
        "manifest['diplomatic_outcomes_registered_successor_pipeline']":
            "manifest['navigation_prerequisite_registered_successor_pipeline']",
        "len(manifest['batches']) == 735 and len(manifest['checks']) == 70":
            "len(manifest['batches']) == 740 and len(manifest['checks']) == 75",
        'registered_manifest_entries=735, accepted_layers=114, passing_release_checks=70, repository_tests=27':
            'registered_manifest_entries=740, accepted_layers=114, passing_release_checks=75, repository_tests=30',
        '    pending_registry.replace(REGISTRY)\n    try:\n        pending_ledger.replace(LEDGER)\n    except OSError:\n        replace_checked(REGISTRY, before_registry)\n        raise\n    assert digest(REGISTRY) == release[\'registry_sha256\'] and digest(PROMOTED) == promoted\n    publish(release)':
            '    assert digest(PROMOTED) == promoted\n    print(\'Navigation registration staged and ready to publish.\')',
    })
    exec(compile(ledger + '\n\n' + registration, __file__ + '::navigation-registration', 'exec'), env)
    env['register']()


def publish_prepared():
    env = {**vars(transaction), **globals(), 'prior': base}
    env['verify_prepared'] = FunctionType(transaction.verify_prepared.__code__, env)
    code = checked_text(inspect.getsource(transaction.publish_prepared), {
        'release_stack.sea_events.pending.json': 'release_stack.navigation.pending.json',
    })
    exec(compile(code, __file__ + '::navigation-publication', 'exec'), env)
    env['publish_prepared']()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    action = parser.add_mutually_exclusive_group(required=True)
    action.add_argument('--register', action='store_true')
    action.add_argument('--publish-prepared', action='store_true')
    (publish_prepared if parser.parse_args().publish_prepared else register)()
