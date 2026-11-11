"""Register the source-bound shark dialogue and choice labels."""

import argparse
from collections import Counter
from hashlib import sha256
import inspect
import json
from pathlib import Path
from types import FunctionType

from dk4tool.dialogue.review import validate_natural_dialogue_batch
from dk4tool.patch.shark_encounter_wrap_v1 import transform
from dk4tool.rom.nds import NdsImage
from dk4tool.script.common_message_table import DIRECTORY_OFFSET, TABLE_OFFSET
from scripts import register_diplomatic_outcomes_v2 as base
from scripts import register_faction_and_epilogue_v1 as previous
from scripts import register_sea_event_review_v2 as transaction
from scripts.audit_story_glyph_consistency import load, save
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest
from scripts.package_ship_command_candidate_v1 import replace_checked
from scripts.seal_shared_text_source_v1 import ARM, COMMON, reference
from scripts.source_locked_derivation_v5118 import checked_text
from scripts.seal_shark_encounter_glosses_v2 import OUTPUT
from scripts.stage_shark_encounter_v1 import AMENDMENTS, active_rows, PROOF as EVIDENCE, ROM as RESEARCH
from scripts.stage_shark_encounter_v1 import BASE
from scripts.stage_shared_notices_storage_v1 import relocate
from scripts.verify_shark_encounter_v1 import BOOT as STARTUP_VERIFICATION, CHECKPOINT, LIVE as LIVE_VERIFICATION
from scripts.verify_shark_encounter_v1 import QA


PARENT = previous.RELEASE
PROFILE = 'all-routes-shark-encounter-editorial-v1-20261111'
FAMILY = 'shared_shark_encounter_20261111'
CHECK = 'registered_shark_dialogue_menu_live_and_complete_parent_inverse'
PACKAGE = Path('releases/all_routes_editorial_20261111_shark_encounter_candidate')
VERIFICATION = PACKAGE / 'verification'
RELEASE = VERIFICATION / 'registered_release_verification.json'
REVIEW = VERIFICATION / 'registered_review.json'
TEST = Path('out/shark_encounter_registered_20261111_v1')
ROM = TEST / 'Translation_DS_All_Routes_Shark_Encounter_20261111_candidate.nds'
MANIFEST = ROM.with_suffix('.manifest.json')
PATCH = PACKAGE / 'translation.xdelta'
DOC = Path('docs/editorial_shark_encounter_registered_20261111.md')
PENDING_LEDGER = TEST / 'editorial_review_current.shark_encounter.pending.json'
MUTATION_PLAN = VERIFICATION / 'registration_mutation_plan.json'
TOTAL, REVISED, RETAINED = 31, 24, 7
PREVIOUS_TOTAL = 26378


def rebuild(parent, evidence, source):
    initial = source['initial_manuscript']
    assert digest(initial) == source['initial_manuscript_sha256'] == evidence['evidence'][initial]
    original_rows = load(initial)['records']
    assert [{k: v for k, v in row.items() if k != 'source_meaning'} for row in source['records']] == original_rows
    image = NdsImage.open(parent['candidate'])
    old_arm, old_common = image.read_file(ARM), image.read_file(COMMON)
    patched, menu, selector = transform(old_arm, source['original_choice_menu']['records'])
    assert json.loads(json.dumps(menu)) == evidence['menu_allocation']
    assert json.loads(json.dumps(selector)) == evidence['wrap_selector']
    directory = sha256(old_arm[DIRECTORY_OFFSET:TABLE_OFFSET]).hexdigest()
    repack = FunctionType(relocate.__code__, {**relocate.__globals__, 'DIRECTORY': directory})
    rows = active_rows(source)
    cases = {row['message_ID']: row for row in evidence['stored']}
    assert cases.keys() == rows.keys() and len(cases) == 29
    storage = {n: bytes.fromhex(case['staged_hex']) for n, case in cases.items()}
    assert all(b' '.join(raw.split()) == rows[n]['english'].encode('ascii') for n, raw in storage.items())
    common, arm, rebound, packing = repack(old_common, patched, rows, storage)
    packed = json.loads(json.dumps(packing))
    recorded = dict(evidence['storage'])
    for proof in (packed, recorded):
        proof['changed_visible_templates'] = sorted(proof['changed_visible_templates'])
    assert packed == recorded
    assert all(case['staged_reference'] == reference(rebound[n]) for n, case in cases.items())
    image.replace_file(ARM, arm)
    image.replace_file(COMMON, common)
    assert bytes(image.rom.save()) == RESEARCH.read_bytes()
    image.replace_file(ARM, old_arm)
    image.replace_file(COMMON, old_common)
    assert bytes(image.rom.save()) == Path(parent['candidate']).read_bytes()
    return arm, common


def verification_scope(approved, live):
    observed = live['observed_ids']
    assert approved['observed_ids'] == observed and len(observed) == 17
    assert approved['stored_records'] == approved['viewed_portrait_pages'] == 29
    assert approved['viewed_choice_styles'] == 4
    assert [row['choice'] for row in live['original_choice_results']] == ['raise', 'kill']
    assert [row['original_item_4_received'] for row in live['original_choice_results']] == [True, False]
    return dict(observed_notice_IDs=observed, observed_menu_labels=2, stored_dialogue=29, menu_labels=2,
        portrait_pages=29, native_caption_planes=4,
        fixture_scope='A temporary daily-update call selected the original encounter with two actor membership bytes initialized on an isolated Hodram save. Both instruction words and memberships were restored.',
        original_both_choices_and_item_outcomes=True, original_return_to_sailing=True,
        alternate_captains_checked_offline=True, natural_shark_battle=False, hardware=False)

def final_review(source, evidence, scope):
    stored = {row['message_ID']: row for row in evidence['stored']}
    records = []
    assert evidence['editorial_amendments'] == json.loads(json.dumps(AMENDMENTS))
    for row in active_rows(source).values():
        n = row['message_ID']
        case = stored[n]
        assert row['source_reference'] == case['source_reference'] and row['current_reference'] == case['current_reference']
        displays = [page for page in evidence['native_portrait_cases'] if page['message_ID'] == n]
        assert len(displays) == 1
        records.append(row | dict(review=row['review'] | {'formatting': True},
            registered_reference=case['staged_reference'] | {'exact_stored_hex': case['staged_hex'],
                'ROM_sha256': evidence['research_ROM_sha256']},
            verified_display_hex=displays[0]['display_hex'], exact_viewed_ink_sha256=displays[0]['native_ink_sha256'],
            protected_phrases=displays[0]['protected_phrases'], gameplay_observed=n in scope['observed_notice_IDs'], new_credit=1))
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
    summary = 'The shark encounter is registered across 29 dialogue records and two choices. The ledger now credits 26,409 reviews.'
    notes = f"""# All Routes Shark Encounter candidate

Use `{ROM.as_posix()}` beside its build manifest. The [clean-input patch](translation.xdelta) applies to clean Japanese SHA-256 `{release['clean_input_sha256']}` and reconstructs candidate SHA-256 `{release['candidate_sha256']}` byte for byte. Patch SHA-256 is `{release['patch_sha256']}`.

{summary} The exchange restores Maria’s standalone “Yes.” and Al’s separate warning. Samwell’s proposal retains his two guesses about eating shark and a possible new trade good. Raise It and Kill It preserve the original choices. Seven wordings earned retention, and the dialogue uses standard ASCII I.

All 29 stored dialogue pages, four menu caption planes, 83 cumulative release checks and 30 targeted tests passed. The two focused Hodram emulator runs exercised both choices and the original item and return-to-sea results. The fixture temporarily selected the original encounter and made its two crew members eligible. The alternate captains passed offline checks. [Gameplay verification](verification/shark_encounter_gameplay_verification.json) · [Exact registered review](verification/registered_review.json)
"""
    (PACKAGE / 'README.md').write_text(notes, encoding='utf-8', newline='\n')
    save(PACKAGE / 'checksums.json', {p.relative_to(PACKAGE).as_posix(): digest(p)
        for p in sorted(PACKAGE.rglob('*')) if p.is_file() and p.name != 'checksums.json'})
    pins_path = Path('translations/rom_retention_pins.json')
    pins = load(pins_path)
    for path, role in ((RESEARCH, 'shark encounter research ROM'), (ROM, 'registered shark encounter ROM')):
        assert digest(path) == release['candidate_sha256']
        assert not any(row['path'] == str(path.resolve()) for row in pins)
        pins.append(dict(path=str(path.resolve()), reason=f"Preserve {role}. SHA256 {release['candidate_sha256']}"))
    replace_checked(pins_path, (json.dumps(pins, ensure_ascii=False, indent=2) + '\n').replace('\n', '\r\n').encode('utf-8'))
    doc = f"""# Shark encounter registered

{summary} The native sequence assigns Samwell the proposal and Al the objection. Maria’s assent and Al’s grumble are complete on their own panels. The four captain tables and two original result indices are preserved. [Release package](../{PACKAGE.as_posix()}/README.md) · [Registered review](../{REVIEW.as_posix()})

Both original choices passed in isolated Hodram emulator replays with temporary encounter and crew eligibility initialization. Seventeen dialogue records were observed. The other twelve captain variants passed stored and visual checks. The initialized fixture scope excludes natural battle activation and hardware coverage. The previous first replay reached the ordinary supply warnings before the target encounter and remains preserved.

Continue with the source-bound rumor and cooperation exchanges around COMMON 2793–2813. Keep the preceding false-document branch and the outcome responses together. The original item card exposed a separate prose lead in COMMON B29 R0057, item 004. Compare “A fierce fish may attack people” with the clean Japanese in the item-description pass. Keep the remaining Options and Market callers, artwork, and older-record technical re-audit open.
"""
    replace_checked(DOC, doc.encode('utf-8'))
    lead = f'# Current editorial checkpoint - 2026-11-11\n\n{summary}\n\nContinue from [the registered shark encounter]({DOC.name}).\n\n'.encode('utf-8')
    for name in ('editorial_handoff_current.md', 'editorial_efficiency_workflow.md', 'translation_progress.md'):
        path = Path('docs') / name
        replace_checked(path, lead + path.read_bytes())
    continuity = Path('docs/build_continuity_protocol.md')
    lead = f"""The shark encounter is registered over Faction and Epilogue with 748 entries, 114 accepted layers and 83 checks. Use `scripts/register_shark_encounter_v1.py --register` to stage and `--publish-prepared` to publish. Preserve the four captain tables, both owned choice pointers, original result indices and scoped portrait selector. The exact reconstruction, both focused choice results and startup pass. [Registered checkpoint]({DOC.name})

"""
    replace_checked(continuity, lead.encode('utf-8') + continuity.read_bytes())
    print('Registered 748 entries and credited 31 shark encounter records once.')

def register():
    manifest = load(load(PARENT)['manifest'])
    driver = manifest['faction_and_epilogue_registered_successor_pipeline']
    assert digest(previous.__file__) == driver['driver_sha256']
    env = {**vars(base), **globals(), 'preserve_compression': transaction.preserve_compression}
    ledger = checked_text(inspect.getsource(base.update_ledger), {
        "'diplomatic-and-scheme-outcome-notices'": "'shared-shark-encounter'",
        'Thirty-four diplomacy and scheme outcomes are registered.': 'Thirty-one shark encounter records are registered.',
        '== 25985': '== 26409', '== 15438': '== 15758', '== 10547': '== 10651',
    })
    old_scope = """    scope = dict(observed_notice_IDs=approved['live_messages'], stored_cases=176, fresh_viewed_pages=31,
        reused_exact_viewed_pages=145, fixture_scope='One incoming letter in a previously empty isolated RAM slot',
        original_no_preserved_war=True, natural_letter_generation=False, hardware=False)"""
    registration = checked_text(inspect.getsource(base.register), {
        "approved['live_messages'] == [349, 356, 352]": "approved['observed_ids'] == live['observed_ids']",
        "sum(int(s.get('tests', 0)) for s in tests) == 27": "sum(int(s.get('tests', 0)) for s in tests) == 30",
        "len(manifest['batches']) == 734 and len(manifest['checks']) == 69":
            "len(manifest['batches']) == 747 and len(manifest['checks']) == 82",
        old_scope: '    scope = verification_scope(approved, live)',
        'release_stack_before_diplomacy.json': 'release_stack_before_shark_encounter.json',
        'verified_crew_notice_predecessor=predecessor, diplomatic_outcome_release=str(REVIEW)':
            'verified_faction_epilogue_predecessor=predecessor, shark_encounter_release=str(REVIEW)',
        'Reviewed diplomacy and scheme outcomes with scoped native phrase wrapping.':
            'Reviewed the shark exchange and its two original choices.',
        'release_stack.diplomacy.pending.json': 'release_stack.shark_encounter.pending.json',
        "LEDGER.with_name('editorial_review_current.diplomacy.pending.json')": 'PENDING_LEDGER',
        '    save(pending_registry, registry)':
            '    preserve_compression(pending_registry, REGISTRY)\n    save(pending_registry, registry)',
        "evidence['wrapper']": "dict(menu=evidence['menu_allocation'], selector=evidence['wrap_selector'])",
        "('COMMON_DIPLOMATIC_OUTCOMES_MODAL_AND_PHRASE_WRAP',)":
            "('COMMON_SHARK_SCOPED_PHRASE_WRAP', *(row['id'] for row in source['original_choice_menu']['records']))",
        "manifest['diplomatic_outcomes_registered_successor_pipeline']":
            "manifest['shark_encounter_registered_successor_pipeline']",
        "len(manifest['batches']) == 735 and len(manifest['checks']) == 70":
            "len(manifest['batches']) == 748 and len(manifest['checks']) == 83",
        'registered_manifest_entries=735, accepted_layers=114, passing_release_checks=70, repository_tests=27':
            'registered_manifest_entries=748, accepted_layers=114, passing_release_checks=83, repository_tests=30',
        '    pending_registry.replace(REGISTRY)\n    try:\n        pending_ledger.replace(LEDGER)\n    except OSError:\n        replace_checked(REGISTRY, before_registry)\n        raise\n    assert digest(REGISTRY) == release[\'registry_sha256\'] and digest(PROMOTED) == promoted\n    publish(release)':
            '    assert digest(PROMOTED) == promoted\n    print(\'Shark encounter registration staged and ready to publish.\')',
    })
    exec(compile(ledger + '\n\n' + registration, __file__ + '::shark-registration', 'exec'), env)
    env['register']()


def publish_prepared():
    env = {**vars(transaction), **globals(), 'prior': base}
    env['verify_prepared'] = FunctionType(transaction.verify_prepared.__code__, env)
    code = checked_text(inspect.getsource(transaction.publish_prepared), {
        'release_stack.sea_events.pending.json': 'release_stack.shark_encounter.pending.json',
    })
    exec(compile(code, __file__ + '::shark-publication', 'exec'), env)
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
