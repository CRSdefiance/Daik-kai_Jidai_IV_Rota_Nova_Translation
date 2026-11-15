"""Register the reviewed sea approaches, battle prompts and village reports."""

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
from scripts import register_navigation_prerequisite_review_v1 as previous
from scripts import register_sea_event_review_v2 as transaction
from scripts.audit_story_glyph_consistency import load, save
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest
from scripts.package_ship_command_candidate_v1 import replace_checked
from scripts.seal_shared_text_source_v1 import ARM, COMMON, reference
from scripts.source_locked_derivation_v5118 import checked_text
from scripts.stage_sea_approach_village_balanced_v2 import OUTPUT, PROOF as EVIDENCE, ROM as RESEARCH, first
from scripts.stage_sea_approach_village_review_v1 import rebuild_components
from scripts.verify_sea_approach_village_release_inputs_v1 import BOOT as STARTUP_VERIFICATION
from scripts.verify_sea_approach_village_release_inputs_v1 import CHECKPOINT, CHOICES, LIVE as LIVE_VERIFICATION, QA


PARENT = previous.RELEASE
PROFILE = 'all-routes-sea-approach-village-editorial-v1-20261111'
FAMILY = 'shared_sea_approach_and_village_20261111'
CHECK = 'registered_sea_approach_village_display_live_and_complete_parent_inverse'
PACKAGE = Path('releases/all_routes_editorial_20261111_sea_approach_village_candidate')
VERIFICATION = PACKAGE / 'verification'
RELEASE = VERIFICATION / 'registered_release_verification.json'
REVIEW = VERIFICATION / 'registered_review.json'
TEST = Path('out/sea_approach_village_registered_20261111_v1')
ROM = TEST / 'Translation_DS_All_Routes_Sea_And_Village_20261111_candidate.nds'
MANIFEST = ROM.with_suffix('.manifest.json')
PATCH = PACKAGE / 'translation.xdelta'
DOC = Path('docs/editorial_sea_approach_village_registered_20261111.md')
PENDING_LEDGER = TEST / 'editorial_review_current.sea_approach_village.pending.json'
MUTATION_PLAN = VERIFICATION / 'registration_mutation_plan.json'
ORDINARY = first.PROOF
TOTAL, REVISED, RETAINED = 67, 56, 11
PREVIOUS_TOTAL = 26244


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
    observed = approved['live_messages']
    assert len(observed) == 2 and 1313 <= observed[0] <= 1320 and 1321 <= observed[1] <= 1328
    assert approved['stored_cases'] == TOTAL and approved['layout_cases'] == 1024
    assert approved['fresh_viewed_pages'] == 16 and approved['reused_exact_viewed_pages'] == 74
    assert approved['crew_voice_choices'] == 1863
    choices = load(CHOICES)
    assert choices['candidate_sha256'] == approved['candidate_sha256']
    assert choices['native_accept_and_decline_paths_preserved'] and len(choices['original_caller_choice_cases']) == 32
    return dict(observed_notice_IDs=observed, stored_templates=TOTAL, checked_layouts=1024,
        fresh_viewed_pages=approved['fresh_viewed_pages'], reused_exact_viewed_pages=approved['reused_exact_viewed_pages'],
        native_selector_cases=approved['native_selector_cases'], crew_voice_choices=approved['crew_voice_choices'],
        offline_battle_choice_cases=32, fixture_scope='One temporary eight-byte ship coordinate placement',
        original_village_discovery_docking_resupply_and_return=True,
        original_faction_and_town_name_arguments=True, original_decimal_arguments=True,
        natural_travel=False, port_attacks_fleet_choices_and_other_village_outcomes_offline=True, hardware=False)


def final_review(source, evidence, scope):
    stored = {row['message_ID']: row for row in evidence['stored']}
    pages = {}
    for page in evidence['native_cases']:
        pages.setdefault(page['message_ID'], []).append(page)
    assert len(stored) == len(pages) == TOTAL
    records = []
    for row in source['records']:
        n = row['message_ID']
        case = stored[n]
        assert row['source_reference'] == case['source_reference'] and row['current_reference'] == case['current_reference']
        records.append(row | dict(review=row['review'] | {'formatting': True},
            registered_reference=case['staged_reference'] | {'exact_stored_hex': case['staged_hex'],
                'ROM_sha256': evidence['research_ROM_sha256']},
            displayed_variants=[dict(display_hex=page['display_hex'], lines=page['visible_lines'],
                argument=page['argument'], ink_sha256=page['native_ink_sha256']) for page in pages[n]],
            gameplay_observed=n in scope['observed_notice_IDs'], new_credit=1))
    assert len(records) == TOTAL and Counter(row['decision'] for row in records) == {'revision': REVISED, 'retention': RETAINED}
    review = dict(translation_policy='natural-dialogue-v2', target_locale='en-US',
        encoder='dialogue-relocatable-v1', review_gates=source['review_gates'], records=records,
        actual_verification_scope=scope, full_goal_complete=False)
    validate_natural_dialogue_batch(review)
    return review


def publish(release):
    summary = 'The 67 sea approach, battle and village records are registered. The ledger now credits 26,311 reviews.'
    notes = f"""# All Routes Sea and Village candidate

Use `{ROM.as_posix()}` beside its build manifest. The [clean-input patch](translation.xdelta) applies to clean Japanese SHA-256 `{release['clean_input_sha256']}` and reconstructs SHA-256 `{release['candidate_sha256']}` byte for byte. Patch SHA-256 is `{release['patch_sha256']}`.

{summary} The batch includes 56 revisions and 11 justified retentions. It preserves the faction names, hostile port names, original decimal arguments and choice outcomes. The revised text works when one villager comes forward, uses ordinary ASCII letters, and keeps the complete help questions together with native faction labels.

The focused Inuvik emulator replay matched the native sighting and resupply lettering through docking and the original return to the village menu. It used one temporary ship-coordinate placement. The battle choices, port attacks and remaining village outcomes passed offline. All 67 stored records, 1,024 layouts, 76 release checks, 30 repository tests, the candidate's own startup, and 24 protected name getters passed. Main promotion awaits acceptance. [Gameplay proof](verification/village_gameplay_verification.json) · [Registered review](verification/registered_review.json)
"""
    (PACKAGE / 'README.md').write_text(notes, encoding='utf-8', newline='\n')
    save(PACKAGE / 'checksums.json', {p.relative_to(PACKAGE).as_posix(): digest(p)
        for p in sorted(PACKAGE.rglob('*')) if p.is_file()})
    pins_path = Path('translations/rom_retention_pins.json')
    pins = load(pins_path)
    for path, expected, role in (
        (first.ROM, load(ORDINARY)['research_ROM_sha256'], 'first-pass sea and village research ROM'),
        (RESEARCH, release['candidate_sha256'], 'balanced sea and village research ROM'),
        (ROM, release['candidate_sha256'], 'registered sea and village ROM'),
    ):
        assert digest(path) == expected and not any(row['path'] == str(path.resolve()) for row in pins)
        pins.append(dict(path=str(path.resolve()), reason=f'Preserve {role}. SHA256 {expected}'))
    replace_checked(pins_path, (json.dumps(pins, ensure_ascii=False, indent=2) + '\n').replace('\n', '\r\n').encode('utf-8'))
    doc = f"""# Sea approaches, fleet encounters and village visits registered

{summary} The build preserves all 114 accepted layers, the Market correction, and the ASCII right-bound fix. [Release package](../{PACKAGE.as_posix()}/README.md) · [Exact registered review](../{REVIEW.as_posix()})

Records 1290–1356 cover nine original voice tables and ten callers. Battle assistance names the fleet's faction. The separate attack warning names the hostile port. The revision restores full spoken questions, replaces stray full-width I with the ordinary ASCII glyph, and keeps the exact count and gold value. The revised counts work at one, and the repair reports cover one or several ships. The original decimal getter continues to use its native numeral glyphs.

All 1,024 layouts passed complete substitution and bounds checks. Sixteen revised pages and 74 exact matching earlier views cover the final display sample. All actual faction names and help questions stay intact on individual lines. The longer synthetic faction label still allows an ordinary word break. The Inuvik replay used a location fixture and observed discovery, docking, resupply, and return to the original menu with Resupply consumed. Both battle callers passed 32 focused accept and decline checks. Battle-choice gameplay, port attacks, the remaining village outcomes, and hardware remain unvisited.

Continue with the individual crew reactions beginning at 1357. Keep the unmapped 750–752 replies, remaining town and random scenes, and other player-facing text in scope. Deferred artwork and the older-record technical re-audit stay separate.
"""
    replace_checked(DOC, doc.encode('utf-8'))
    lead = f'# Current editorial checkpoint - 2026-11-11\n\n{summary}\n\nContinue from [the registered sea and village checkpoint]({DOC.name}).\n\n'.encode('utf-8')
    for name in ('editorial_handoff_current.md', 'editorial_efficiency_workflow.md', 'translation_progress.md'):
        path = Path('docs') / name
        replace_checked(path, lead + path.read_bytes())
    print('Registered 741 entries and credited the 67 sea and village records once.')


def register():
    manifest = load(load(PARENT)['manifest'])
    driver = manifest['navigation_prerequisite_registered_successor_pipeline']
    assert digest(previous.__file__) == driver['driver_sha256']
    env = {**vars(base), **globals(), 'preserve_compression': transaction.preserve_compression}
    ledger = checked_text(inspect.getsource(base.update_ledger), {
        "'diplomatic-and-scheme-outcome-notices'": "'shared-sea-approach-fleet-and-village-reports'",
        'Thirty-four diplomacy and scheme outcomes are registered.': 'Sixty-seven sea and village reports are registered.',
        '== 25985': '== 26311', '== 15438': '== 15684', '== 10547': '== 10627',
    })
    old_scope = """    scope = dict(observed_notice_IDs=approved['live_messages'], stored_cases=176, fresh_viewed_pages=31,
        reused_exact_viewed_pages=145, fixture_scope='One incoming letter in a previously empty isolated RAM slot',
        original_no_preserved_war=True, natural_letter_generation=False, hardware=False)"""
    registration = checked_text(inspect.getsource(base.register), {
        "approved['live_messages'] == [349, 356, 352]": "approved['live_messages'] == live['observed_notice_IDs']",
        "sum(int(s.get('tests', 0)) for s in tests) == 27": "sum(int(s.get('tests', 0)) for s in tests) == 30",
        "len(manifest['batches']) == 734 and len(manifest['checks']) == 69":
            "len(manifest['batches']) == 740 and len(manifest['checks']) == 75",
        old_scope: '    scope = verification_scope(approved)',
        'LIVE_VERIFICATION, STARTUP_VERIFICATION, QA):': 'LIVE_VERIFICATION, STARTUP_VERIFICATION, QA, CHOICES, ORDINARY):',
        'release_stack_before_diplomacy.json': 'release_stack_before_sea_approach_village.json',
        'verified_crew_notice_predecessor=predecessor, diplomatic_outcome_release=str(REVIEW)':
            'verified_navigation_predecessor=predecessor, sea_approach_village_release=str(REVIEW)',
        'Reviewed diplomacy and scheme outcomes with scoped native phrase wrapping.':
            'Reviewed sea approaches, battle-assistance choices, hostile ports, and village results.',
        'release_stack.diplomacy.pending.json': 'release_stack.sea_approach_village.pending.json',
        "LEDGER.with_name('editorial_review_current.diplomacy.pending.json')": 'PENDING_LEDGER',
        '    save(pending_registry, registry)':
            '    preserve_compression(pending_registry, REGISTRY)\n    save(pending_registry, registry)',
        "evidence['wrapper']": "evidence['selector']",
        'COMMON_DIPLOMATIC_OUTCOMES_MODAL_AND_PHRASE_WRAP': 'COMMON_SEA_APPROACH_VILLAGE_SCOPED_PHRASE_WRAP',
        "manifest['diplomatic_outcomes_registered_successor_pipeline']":
            "manifest['sea_approach_village_registered_successor_pipeline']",
        "len(manifest['batches']) == 735 and len(manifest['checks']) == 70":
            "len(manifest['batches']) == 741 and len(manifest['checks']) == 76",
        'registered_manifest_entries=735, accepted_layers=114, passing_release_checks=70, repository_tests=27':
            'registered_manifest_entries=741, accepted_layers=114, passing_release_checks=76, repository_tests=30',
        '    pending_registry.replace(REGISTRY)\n    try:\n        pending_ledger.replace(LEDGER)\n    except OSError:\n        replace_checked(REGISTRY, before_registry)\n        raise\n    assert digest(REGISTRY) == release[\'registry_sha256\'] and digest(PROMOTED) == promoted\n    publish(release)':
            '    assert digest(PROMOTED) == promoted\n    print(\'Sea and village registration staged and ready to publish.\')',
    })
    exec(compile(ledger + '\n\n' + registration, __file__ + '::sea-and-village-registration', 'exec'), env)
    env['register']()


def publish_prepared():
    env = {**vars(transaction), **globals(), 'prior': base}
    env['verify_prepared'] = FunctionType(transaction.verify_prepared.__code__, env)
    code = checked_text(inspect.getsource(transaction.publish_prepared), {
        'release_stack.sea_events.pending.json': 'release_stack.sea_approach_village.pending.json',
    })
    exec(compile(code, __file__ + '::sea-and-village-publication', 'exec'), env)
    env['publish_prepared']()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    action = parser.add_mutually_exclusive_group(required=True)
    action.add_argument('--register', action='store_true')
    action.add_argument('--publish-prepared', action='store_true')
    (publish_prepared if parser.parse_args().publish_prepared else register)()
