"""Register the source-bound mutiny dialogue and choice labels."""

import argparse
from collections import Counter
from hashlib import sha256
import inspect
import json
from pathlib import Path
from types import FunctionType

from dk4tool.dialogue.review import validate_natural_dialogue_batch
from dk4tool.patch.mutiny_static_wrap_v1 import transform
from dk4tool.rom.nds import NdsImage
from dk4tool.script.common_message_table import DIRECTORY_OFFSET, TABLE_OFFSET
from scripts import register_diplomatic_outcomes_v2 as base
from scripts import register_sailing_alert_review_v2 as previous
from scripts import register_sea_event_review_v2 as transaction
from scripts.audit_story_glyph_consistency import load, save
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest
from scripts.package_ship_command_candidate_v1 import replace_checked
from scripts.seal_shared_text_source_v1 import ARM, COMMON, reference
from scripts.source_locked_derivation_v5118 import checked_text
from scripts.stage_mutiny_review_v1 import OUTPUT, PROOF as EVIDENCE, ROM as RESEARCH
from scripts.stage_mutiny_review_v1 import BASE
from scripts.stage_shared_notices_storage_v1 import relocate
from scripts.verify_mutiny_release_inputs_v1 import BOOT as STARTUP_VERIFICATION, CHECKPOINT, LIVE as LIVE_VERIFICATION
from scripts.verify_mutiny_release_inputs_v1 import OBSERVED, QA


PARENT = previous.RELEASE
PROFILE = 'all-routes-mutiny-editorial-v1-20261111'
FAMILY = 'shared_unrest_and_mutiny_20261111'
CHECK = 'registered_mutiny_dialogue_menu_live_and_complete_parent_inverse'
PACKAGE = Path('releases/all_routes_editorial_20261111_mutiny_candidate')
VERIFICATION = PACKAGE / 'verification'
RELEASE = VERIFICATION / 'registered_release_verification.json'
REVIEW = VERIFICATION / 'registered_review.json'
TEST = Path('out/mutiny_registered_20261111_v1')
ROM = TEST / 'Translation_DS_All_Routes_Mutiny_20261111_candidate.nds'
MANIFEST = ROM.with_suffix('.manifest.json')
PATCH = PACKAGE / 'translation.xdelta'
DOC = Path('docs/editorial_mutiny_registered_20261111.md')
PENDING_LEDGER = TEST / 'editorial_review_current.mutiny.pending.json'
MUTATION_PLAN = VERIFICATION / 'registration_mutation_plan.json'
TOTAL, REVISED, RETAINED = 68, 54, 14
PREVIOUS_TOTAL = 26111


def rebuild(parent, evidence, source):
    image = NdsImage.open(parent['candidate'])
    old_arm, old_common = image.read_file(ARM), image.read_file(COMMON)
    patched, menu, selector = transform(old_arm, source['original_choice_menu']['records'])
    assert json.loads(json.dumps(menu)) == evidence['menu_allocation']
    assert json.loads(json.dumps(selector)) == evidence['wrap_selector']
    directory = sha256(old_arm[DIRECTORY_OFFSET:TABLE_OFFSET]).hexdigest()
    repack = FunctionType(relocate.__code__, {**relocate.__globals__, 'DIRECTORY': directory})
    rows = {row['message_ID']: row for row in source['records']}
    cases = {row['message_ID']: row for row in evidence['stored']}
    assert cases.keys() == rows.keys() and len(cases) == 65
    storage = {n: bytes.fromhex(case['staged_hex']) for n, case in cases.items()}
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
    assert approved['live_messages'] == OBSERVED
    assert approved['stored_dialogue'] + approved['menu_labels'] == TOTAL
    return dict(observed_dialogue_IDs=OBSERVED, observed_menu_labels=3, stored_dialogue=65, menu_labels=3,
        portrait_pages=approved['portrait_pages'], native_portrait_expansions=approved['native_portrait_expansions'],
        native_caption_planes=approved['native_menu_caption_planes'], native_selector_cases=approved['native_selector_cases'],
        crew_voice_choices=approved['crew_voice_choices'],
        fixture_scope='One temporary native branch selection in an isolated emulator voyage',
        ordinary_appeal_choice_cook_and_sailor_acceptance=True, normal_sailing_return=True,
        other_choices_or_natural_mutiny_prerequisite_observed=False, hardware=False)


def final_review(source, evidence, scope):
    stored = {row['message_ID']: row for row in evidence['stored']}
    records = []
    for row in source['records']:
        n = row['message_ID']
        case = stored[n]
        assert row['source_reference'] == case['source_reference'] and row['current_reference'] == case['current_reference']
        displays = [page for page in evidence['native_portrait_cases'] if page['message_ID'] == n]
        assert len(displays) == (7 if row['source_native_macros'] else 1)
        records.append(row | dict(review=row['review'] | {'formatting': True},
            registered_reference=case['staged_reference'] | {'exact_stored_hex': case['staged_hex'],
                'ROM_sha256': evidence['research_ROM_sha256']},
            verified_display_hex=displays[0]['display_hex'], exact_viewed_ink_sha256=displays[0]['native_ink_sha256'],
            protected_phrases=displays[0]['protected_phrases'], gameplay_observed=n in OBSERVED, new_credit=1))
    for row, allocation, caption in zip(source['original_choice_menu']['records'], evidence['menu_allocation']['changes'],
                                         evidence['native_menu']['research']['options'], strict=True):
        assert row['id'] == allocation['id'] and row['english'] == caption['text']
        assert row['source_hex'] == allocation['source_terminated_hex']
        assert allocation['target_pointer'] == caption['pointer']
        records.append(row | dict(review=row['review'] | {'formatting': True},
            registered_reference=dict(pointer_field=BASE + allocation['field'], literal_address=caption['pointer'],
                exact_stored_hex=caption['terminated_hex'], ROM_sha256=evidence['research_ROM_sha256']),
            native_width_units=caption['width_units'], gameplay_observed=True, new_credit=1))
    assert len(records) == TOTAL and Counter(r['decision'] for r in records) == {'revision': REVISED, 'retention': RETAINED}
    review = dict(translation_policy='natural-dialogue-v2', target_locale='en-US',
        encoder='dialogue-relocatable-v1', review_gates=source['review_gates'], records=records,
        actual_verification_scope=scope, full_goal_complete=False)
    validate_natural_dialogue_batch(review)
    return review


def publish(release):
    summary = 'The unrest and mutiny exchange is registered across 65 dialogue records and three choices. The ledger now credits 26,179 reviews.'
    notes = f"""# All Routes mutiny candidate

Use `{ROM.as_posix()}` beside its build manifest. The [clean-input patch](translation.xdelta) applies to clean Japanese SHA-256 `{release['clean_input_sha256']}` and reconstructs candidate SHA-256 `{release['candidate_sha256']}` byte for byte. Patch SHA-256 is `{release['patch_sha256']}`.

{summary} This batch has 54 revisions and 14 justified retentions. It restores 26 lines that displayed unrelated text and localizes Quell Mutiny, Appease Crew and Do Nothing. All 65 dialogue pages, six caption planes, 73 cumulative release checks, and 30 targeted tests passed. Main V4701 awaits acceptance.

The focused emulator voyage displayed five complete dialogue panels, all three choices and the selection highlight. The original appeal branch showed the cook's agreement and the crew's acceptance, then returned to sailing. One temporary instruction selected the encounter. The candidate passed its own 31,000-frame startup and 24 protected name getters. [Gameplay verification](verification/mutiny_live_verification.json) · [Registered review](verification/registered_review.json)
"""
    (PACKAGE / 'README.md').write_text(notes, encoding='utf-8', newline='\n')
    save(PACKAGE / 'checksums.json', {p.relative_to(PACKAGE).as_posix(): digest(p)
        for p in sorted(PACKAGE.rglob('*')) if p.is_file()})
    pins_path = Path('translations/rom_retention_pins.json')
    pins = load(pins_path)
    for path, role in ((RESEARCH, 'mutiny research ROM'), (ROM, 'registered mutiny ROM')):
        assert digest(path) == release['candidate_sha256']
        assert not any(row['path'] == str(path.resolve()) for row in pins)
        pins.append(dict(path=str(path.resolve()), reason=f"Preserve {role}. SHA256 {release['candidate_sha256']}"))
    replace_checked(pins_path, (json.dumps(pins, ensure_ascii=False, indent=2) + '\n').replace('\n', '\r\n').encode('utf-8'))
    doc = f"""# Unrest and mutiny registered

{summary} The cumulative candidate retains the sailing-alert batch, 114 accepted layers, the Market correction, and the ASCII right-bound fix. [Release package](../{PACKAGE.as_posix()}/README.md) · [Exact registered review](../{REVIEW.as_posix()})

The exchange restores 26 unrelated or fragmented lines, uses the established Boarding Leader title, and distinguishes the options to suppress the mutiny, appease the crew, or do nothing. Both source IC substitutions express the speaker's first person. The established English “me” preserves that meaning in the two voice lines, with the existing parser unchanged. The menu has three fully localized labels.

All 65 stored dialogue pages, 77 native portrait expansions, 1,449 crew voice choices, 6,552 selector cases, 14 source pronoun cases, six native caption planes, and 30 targeted tests passed. The compiler keeps 50 paragraphs within the original viewport, including five full-width opening rows and four four-row bodies. The emulator replay observed five dialogue panels and all three choices, then followed the successful meal branch back to sailing. One temporary instruction selected the encounter. The other choice outcomes and natural prerequisites remain offline-only. The 31,000-frame startup and 24 protected getters passed.

Continue with the leaks and fire families beginning at 573. Remaining town, random and player-facing text stays in scope, including the unmapped Market replies. Deferred artwork and the older-record technical re-audit stay separate.
"""
    replace_checked(DOC, doc.encode('utf-8'))
    lead = f'# Current editorial checkpoint - 2026-11-11\n\n{summary}\n\nContinue from [the registered mutiny checkpoint]({DOC.name}).\n\n'.encode('utf-8')
    for name in ('editorial_handoff_current.md', 'editorial_efficiency_workflow.md', 'translation_progress.md'):
        path = Path('docs') / name
        replace_checked(path, lead + path.read_bytes())
    print('Registered 738 entries and credited 68 mutiny reviews once.')


def register():
    manifest = load(load(PARENT)['manifest'])
    driver = manifest['sailing_alerts_registered_successor_pipeline']
    assert digest(previous.__file__) == driver['driver_sha256']
    env = {**vars(base), **globals(), 'preserve_compression': transaction.preserve_compression}
    ledger = checked_text(inspect.getsource(base.update_ledger), {
        "'diplomatic-and-scheme-outcome-notices'": "'shared-unrest-and-mutiny'",
        'Thirty-four diplomacy and scheme outcomes are registered.': 'Sixty-eight unrest and mutiny records are registered.',
        '== 25985': '== 26179', '== 15438': '== 15573', '== 10547': '== 10606',
    })
    old_scope = """    scope = dict(observed_notice_IDs=approved['live_messages'], stored_cases=176, fresh_viewed_pages=31,
        reused_exact_viewed_pages=145, fixture_scope='One incoming letter in a previously empty isolated RAM slot',
        original_no_preserved_war=True, natural_letter_generation=False, hardware=False)"""
    registration = checked_text(inspect.getsource(base.register), {
        "approved['live_messages'] == [349, 356, 352]": "approved['live_messages'] == OBSERVED",
        "sum(int(s.get('tests', 0)) for s in tests) == 27": "sum(int(s.get('tests', 0)) for s in tests) == 30",
        "len(manifest['batches']) == 734 and len(manifest['checks']) == 69":
            "len(manifest['batches']) == 737 and len(manifest['checks']) == 72",
        old_scope: '    scope = verification_scope(approved)',
        'release_stack_before_diplomacy.json': 'release_stack_before_mutiny.json',
        'verified_crew_notice_predecessor=predecessor, diplomatic_outcome_release=str(REVIEW)':
            'verified_sailing_alert_predecessor=predecessor, mutiny_release=str(REVIEW)',
        'Reviewed diplomacy and scheme outcomes with scoped native phrase wrapping.':
            'Reviewed the unrest and mutiny exchange and its three native choices.',
        'release_stack.diplomacy.pending.json': 'release_stack.mutiny.pending.json',
        "LEDGER.with_name('editorial_review_current.diplomacy.pending.json')": 'PENDING_LEDGER',
        '    save(pending_registry, registry)':
            '    preserve_compression(pending_registry, REGISTRY)\n    save(pending_registry, registry)',
        "evidence['wrapper']": "dict(menu=evidence['menu_allocation'], selector=evidence['wrap_selector'])",
        "('COMMON_DIPLOMATIC_OUTCOMES_MODAL_AND_PHRASE_WRAP',)":
            "('COMMON_MUTINY_SCOPED_PHRASE_WRAP', *(row['id'] for row in source['original_choice_menu']['records']))",
        "manifest['diplomatic_outcomes_registered_successor_pipeline']":
            "manifest['mutiny_registered_successor_pipeline']",
        "len(manifest['batches']) == 735 and len(manifest['checks']) == 70":
            "len(manifest['batches']) == 738 and len(manifest['checks']) == 73",
        'registered_manifest_entries=735, accepted_layers=114, passing_release_checks=70, repository_tests=27':
            'registered_manifest_entries=738, accepted_layers=114, passing_release_checks=73, repository_tests=30',
        '    pending_registry.replace(REGISTRY)\n    try:\n        pending_ledger.replace(LEDGER)\n    except OSError:\n        replace_checked(REGISTRY, before_registry)\n        raise\n    assert digest(REGISTRY) == release[\'registry_sha256\'] and digest(PROMOTED) == promoted\n    publish(release)':
            '    assert digest(PROMOTED) == promoted\n    print(\'Mutiny registration staged and ready to publish.\')',
    })
    exec(compile(ledger + '\n\n' + registration, __file__ + '::mutiny-registration', 'exec'), env)
    env['register']()


def publish_prepared():
    env = {**vars(transaction), **globals(), 'prior': base}
    env['verify_prepared'] = FunctionType(transaction.verify_prepared.__code__, env)
    code = checked_text(inspect.getsource(transaction.publish_prepared), {
        'release_stack.sea_events.pending.json': 'release_stack.mutiny.pending.json',
    })
    exec(compile(code, __file__ + '::mutiny-publication', 'exec'), env)
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
