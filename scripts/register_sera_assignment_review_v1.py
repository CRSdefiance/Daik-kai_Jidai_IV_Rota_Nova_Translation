"""Register Sera's four verified responses over the sea and village build."""

import argparse
from collections import Counter
import inspect
import json
from pathlib import Path
from types import FunctionType

from dk4tool.dialogue.review import validate_natural_dialogue_batch
from dk4tool.rom.nds import NdsImage
from scripts import register_diplomatic_outcomes_v2 as base
from scripts import register_sea_approach_village_review_v1 as previous
from scripts import register_sea_event_review_v2 as transaction
from scripts.audit_story_glyph_consistency import load, save
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest
from scripts.package_ship_command_candidate_v1 import replace_checked
from scripts.seal_shared_text_source_v1 import ARM, COMMON, reference
from scripts.source_locked_derivation_v5118 import checked_text
from scripts.stage_sera_assignment_review_v1 import OUTPUT, PROOF as EVIDENCE, ROM as RESEARCH, rebuild_components
from scripts.verify_sera_assignment_release_inputs_v1 import BOOT as STARTUP_VERIFICATION
from scripts.verify_sera_assignment_release_inputs_v1 import CHECKPOINT, LIVE as LIVE_VERIFICATION, QA


PARENT = previous.RELEASE
PROFILE = 'all-routes-sera-assignment-editorial-v1-20261111'
FAMILY = 'shared_sera_room_assignment_20261111'
CHECK = 'registered_sera_assignment_display_live_and_complete_parent_inverse'
PACKAGE = Path('releases/all_routes_editorial_20261111_sera_assignment_candidate')
VERIFICATION = PACKAGE / 'verification'
RELEASE = VERIFICATION / 'registered_release_verification.json'
REVIEW = VERIFICATION / 'registered_review.json'
TEST = Path('out/sera_assignment_registered_20261111_v1')
ROM = TEST / 'Translation_DS_All_Routes_Sera_Assignment_20261111_candidate.nds'
MANIFEST = ROM.with_suffix('.manifest.json')
PATCH = PACKAGE / 'translation.xdelta'
DOC = Path('docs/editorial_sera_assignment_registered_20261111.md')
PENDING_LEDGER = TEST / 'editorial_review_current.sera_assignment.pending.json'
MUTATION_PLAN = VERIFICATION / 'registration_mutation_plan.json'
TOTAL, REVISED, RETAINED = 4, 3, 1
PREVIOUS_TOTAL = 26311


def rebuild(parent, evidence, source):
    image = NdsImage.open(parent['candidate'])
    old_arm, old_common = image.read_file(ARM), image.read_file(COMMON)
    rows = {row['message_ID']: row for row in source['records']}
    cases = {row['message_ID']: row for row in evidence['stored']}
    assert cases.keys() == rows.keys() and len(cases) == TOTAL
    storage = {n: bytes.fromhex(case['staged_hex']) for n, case in cases.items()}
    assert all(b' '.join(raw.split()) == rows[n]['english'].encode('ascii') for n, raw in storage.items())
    arm, common, rebound, packing = rebuild_components(old_arm, old_common, rows, storage)
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
    assert approved['live_messages'] == [1357, 1360] and approved['stored_cases'] == approved['viewed_pages'] == 4
    return dict(observed_notice_IDs=approved['live_messages'], stored_templates=4, viewed_pages=4,
        original_assignment_and_refusal_paths=4, original_portrait_and_assignment_code_unchanged=True,
        live_Galley_acceptance=True, live_language_refusal=True,
        fixture_scope='Selected actor, room type and language bit set in isolated Deck UI',
        cabin_and_other_refusal_offline_only=True, hardware=False)


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
                ink_sha256=page['native_ink_sha256'])],
            gameplay_observed=n in scope['observed_notice_IDs'], new_credit=1))
    assert len(records) == TOTAL and Counter(row['decision'] for row in records) == {'revision': REVISED, 'retention': RETAINED}
    review = dict(translation_policy='natural-dialogue-v2', target_locale='en-US',
        encoder='dialogue-relocatable-v1', review_gates=source['review_gates'], records=records,
        native_context=source['native_context'], actual_verification_scope=scope, full_goal_complete=False)
    validate_natural_dialogue_batch(review)
    return review


def publish(release):
    summary = 'Sera’s four room-assignment reactions are registered. The ledger now credits 26,315 reviews.'
    notes = f"""# All Routes Sera assignment candidate

Use `{ROM.as_posix()}` beside its build manifest. The [clean-input patch](translation.xdelta) applies to clean Japanese SHA-256 `{release['clean_input_sha256']}` and reconstructs SHA-256 `{release['candidate_sha256']}` byte for byte. Patch SHA-256 is `{release['patch_sha256']}`.

{summary} Three revisions keep Sera’s plain voice, restore the ordinary ASCII I, and preserve her different reactions to the Galley, Cabin, and language barrier. The existing “Can’t do that... Sorry.” is retained. The original game code handles the wraps and room decisions.

All four stored records, native pages and assignment outcomes passed. Two focused Deck replays verified the Galley acceptance and the language refusal through A dismissal. Each staged the selected actor, room type and language bit in its own emulator session. The Cabin and other refusal passed offline. The candidate passed 77 release checks, 30 repository tests, its own startup, and 24 protected name getters. Main promotion awaits acceptance. [Gameplay proof](verification/sera_assignment_gameplay_verification.json) · [Registered review](verification/registered_review.json)
"""
    (PACKAGE / 'README.md').write_text(notes, encoding='utf-8', newline='\n')
    save(PACKAGE / 'checksums.json', {p.relative_to(PACKAGE).as_posix(): digest(p)
        for p in sorted(PACKAGE.rglob('*')) if p.is_file()})
    pins_path = Path('translations/rom_retention_pins.json')
    pins = load(pins_path)
    for path, role in ((RESEARCH, 'Sera assignment research ROM'), (ROM, 'registered Sera assignment ROM')):
        expected = release['candidate_sha256']
        assert digest(path) == expected and not any(row['path'] == str(path.resolve()) for row in pins)
        pins.append(dict(path=str(path.resolve()), reason=f'Preserve {role}. SHA256 {expected}'))
    replace_checked(pins_path, (json.dumps(pins, ensure_ascii=False, indent=2) + '\n').replace('\n', '\r\n').encode('utf-8'))
    doc = f"""# Sera’s room-assignment responses registered

{summary} The build preserves all 114 accepted layers, the Market correction, and the ASCII right-bound fix. [Release package](../{PACKAGE.as_posix()}/README.md) · [Exact registered review](../{REVIEW.as_posix()})

The original Deck personnel handler selects 1357 for the Galley, 1358 for the Cabin, 1359 for an ineligible room after the language flag, and 1360 before that flag. Sera’s reluctance and language difficulty stay distinct. Three revisions and one justified retention passed the five gates. The native code and portrait controls are byte-exact. The only ARM9 changes are COMMON storage offsets.

The focused Galley and language-refusal replays match the complete native glyph planes and original assignment or refusal after dismissal. The Cabin and other refusal were executed offline. The tests staged the relevant UI fields and language bit in isolated sessions. Recruitment, the story event that teaches the language, and hardware testing were outside the replay.

Continue with the early shared setup and save notices, including the remaining consumer bindings. The unmapped Market replies, town and random scenes, and other player-facing text stay in scope. Deferred artwork and the older-record technical re-audit stay separate.
"""
    replace_checked(DOC, doc.encode('utf-8'))
    lead = f'# Current editorial checkpoint - 2026-11-11\n\n{summary}\n\nContinue from [the registered Sera assignment checkpoint]({DOC.name}).\n\n'.encode('utf-8')
    for name in ('editorial_handoff_current.md', 'editorial_efficiency_workflow.md', 'translation_progress.md'):
        path = Path('docs') / name
        replace_checked(path, lead + path.read_bytes())
    print('Registered 742 entries and credited Sera’s four room responses once.')


def register():
    manifest = load(load(PARENT)['manifest'])
    driver = manifest['sea_approach_village_registered_successor_pipeline']
    assert digest(previous.__file__) == driver['driver_sha256']
    env = {**vars(base), **globals(), 'preserve_compression': transaction.preserve_compression}
    ledger = checked_text(inspect.getsource(base.update_ledger), {
        "'diplomatic-and-scheme-outcome-notices'": "'shared-sera-room-assignment-reactions'",
        'Thirty-four diplomacy and scheme outcomes are registered.': 'Four Sera room-assignment reactions are registered.',
        '== 25985': '== 26315', '== 15438': '== 15687', '== 10547': '== 10628',
    })
    old_scope = """    scope = dict(observed_notice_IDs=approved['live_messages'], stored_cases=176, fresh_viewed_pages=31,
        reused_exact_viewed_pages=145, fixture_scope='One incoming letter in a previously empty isolated RAM slot',
        original_no_preserved_war=True, natural_letter_generation=False, hardware=False)"""
    registration = checked_text(inspect.getsource(base.register), {
        "approved['live_messages'] == [349, 356, 352]": "approved['live_messages'] == live['observed_notice_IDs']",
        "sum(int(s.get('tests', 0)) for s in tests) == 27": "sum(int(s.get('tests', 0)) for s in tests) == 30",
        "len(manifest['batches']) == 734 and len(manifest['checks']) == 69":
            "len(manifest['batches']) == 741 and len(manifest['checks']) == 76",
        old_scope: '    scope = verification_scope(approved)',
        'release_stack_before_diplomacy.json': 'release_stack_before_sera_assignment.json',
        'verified_crew_notice_predecessor=predecessor, diplomatic_outcome_release=str(REVIEW)':
            'verified_sea_approach_village_predecessor=predecessor, sera_assignment_release=str(REVIEW)',
        'Reviewed diplomacy and scheme outcomes with scoped native phrase wrapping.':
            'Reviewed the four native Sera room responses with the original renderer.',
        'release_stack.diplomacy.pending.json': 'release_stack.sera_assignment.pending.json',
        "LEDGER.with_name('editorial_review_current.diplomacy.pending.json')": 'PENDING_LEDGER',
        '    save(pending_registry, registry)':
            '    preserve_compression(pending_registry, REGISTRY)\n    save(pending_registry, registry)',
        "evidence['wrapper']": "evidence['selector']",
        'COMMON_DIPLOMATIC_OUTCOMES_MODAL_AND_PHRASE_WRAP': 'COMMON_SERA_ASSIGNMENT_STORAGE_OFFSETS',
        "manifest['diplomatic_outcomes_registered_successor_pipeline']":
            "manifest['sera_assignment_registered_successor_pipeline']",
        "len(manifest['batches']) == 735 and len(manifest['checks']) == 70":
            "len(manifest['batches']) == 742 and len(manifest['checks']) == 77",
        'registered_manifest_entries=735, accepted_layers=114, passing_release_checks=70, repository_tests=27':
            'registered_manifest_entries=742, accepted_layers=114, passing_release_checks=77, repository_tests=30',
        '    pending_registry.replace(REGISTRY)\n    try:\n        pending_ledger.replace(LEDGER)\n    except OSError:\n        replace_checked(REGISTRY, before_registry)\n        raise\n    assert digest(REGISTRY) == release[\'registry_sha256\'] and digest(PROMOTED) == promoted\n    publish(release)':
            '    assert digest(PROMOTED) == promoted\n    print(\'Sera assignment registration staged and ready to publish.\')',
    })
    exec(compile(ledger + '\n\n' + registration, __file__ + '::sera-assignment-registration', 'exec'), env)
    env['register']()


def publish_prepared():
    env = {**vars(transaction), **globals(), 'prior': base}
    env['verify_prepared'] = FunctionType(transaction.verify_prepared.__code__, env)
    code = checked_text(inspect.getsource(transaction.publish_prepared), {
        'release_stack.sea_events.pending.json': 'release_stack.sera_assignment.pending.json',
    })
    exec(compile(code, __file__ + '::sera-assignment-publication', 'exec'), env)
    env['publish_prepared']()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    action = parser.add_mutually_exclusive_group(required=True)
    action.add_argument('--register', action='store_true')
    action.add_argument('--publish-prepared', action='store_true')
    (publish_prepared if parser.parse_args().publish_prepared else register)()
