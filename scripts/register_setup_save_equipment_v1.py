"""Register the verified system and equipment notices over Captain Biographies."""

import argparse
import inspect
import json
from pathlib import Path
from types import FunctionType

from dk4tool.script.common_message_table import DIRECTORY_OFFSET, TABLE_OFFSET
from scripts import register_diplomatic_outcomes_v2 as base
from scripts import register_sea_event_review_v2 as transaction
from scripts import stage_setup_save_equipment_v1 as stage
from scripts.register_captain_biographies_v1 import RELEASE as PARENT
from scripts.source_locked_derivation_v5118 import checked_text
from scripts.verify_setup_save_equipment_v1 import BOOT as STARTUP_VERIFICATION
from scripts.verify_setup_save_equipment_v1 import CHECKPOINT, LIVE as LIVE_VERIFICATION, QA


PROFILE = 'all-routes-equipment-system-notices-editorial-v1-20261111'
FAMILY = 'equipment_system_notices_contextual_20261111'
CHECK = 'registered_equipment_system_native_live_and_complete_parent_inverse'
PACKAGE = Path('releases/all_routes_editorial_20261111_equipment_system_candidate')
VERIFICATION = PACKAGE / 'verification'
RELEASE = VERIFICATION / 'registered_release_verification.json'
REVIEW = VERIFICATION / 'registered_review.json'
MUTATION_PLAN = VERIFICATION / 'registration_mutation_plan.json'
TEST = Path('out/equipment_system_registered_20261111_v1')
ROM = TEST / 'Translation_DS_All_Routes_Equipment_System_20261111_candidate.nds'
MANIFEST = ROM.with_suffix('.manifest.json')
PATCH = PACKAGE / 'translation.xdelta'
DOC = Path('docs/editorial_equipment_system_registered_20261111.md')
PENDING_LEDGER = TEST / 'editorial_review_current.equipment_system.pending.json'
OUTPUT, EVIDENCE, RESEARCH = stage.preflight.MANUSCRIPT, stage.PROOF, stage.ROM
PREVIOUS_TOTAL, TOTAL, REVISED, RETAINED = 26319, 14, 8, 6


def rebuild(parent, evidence, source):
    assert all(base.digest(path) == sha for path, sha in evidence['evidence'].items())
    image = base.NdsImage.open(parent['candidate'])
    before, old_common = image.read_file(base.ARM), image.read_file(base.COMMON)
    wrapped, owner = stage.transform(before)
    assert owner == evidence['ownership']
    rows = {row['message_ID']: row for row in source['records'] if row['message_ID'] != 318}
    storage = {row['message_ID']: bytes.fromhex(row['stored_hex']) for row in evidence['records']}
    assert storage.keys() == rows.keys() and len(rows) == TOTAL
    assert all(b' '.join(raw.split()) == rows[n]['english'].encode('ascii') for n, raw in storage.items())
    directory = base.sha256(before[DIRECTORY_OFFSET:TABLE_OFFSET]).hexdigest()
    repack = FunctionType(stage.relocate.__code__, {**stage.relocate.__globals__, 'DIRECTORY': directory})
    common, arm, rebound, packing = repack(old_common, wrapped, rows, storage)
    comparable = json.loads(json.dumps(packing))
    recorded = dict(evidence['storage'])
    for result in (comparable, recorded):
        result['changed_visible_templates'] = sorted(result['changed_visible_templates'])
    assert comparable == recorded
    assert all(stage.reference(rebound[row['message_ID']]) == row['stored'] for row in evidence['records'])
    image.replace_file(base.ARM, arm)
    image.replace_file(base.COMMON, common)
    assert bytes(image.rom.save()) == RESEARCH.read_bytes()
    image.replace_file(base.ARM, before)
    image.replace_file(base.COMMON, old_common)
    assert bytes(image.rom.save()) == Path(parent['candidate']).read_bytes()
    return arm, common


def verification_scope(approved, live):
    assert approved['observed_ids'] == live['observed_ids'] == [320, 321, 329]
    assert approved['stored_records'] == 14 and approved['viewed_pages'] == 21
    assert len(live['selector_positive_and_negative_cases']) == 8
    return dict(observed_notice_IDs=live['observed_ids'], stored_records=14, modal_variants=21,
        directly_viewed_modal_pages=21, direct_original_chooser=True, original_equip_and_remove=True,
        fixture_scope='Existing ordinary battery save, controller and stylus, passive request observation',
        offline_choice_notice_ids=[316, 319, 325], unresolved_exhibition_message=318, hardware=False)


def final_review(source, evidence, scope):
    bound = {row['message_ID']: row for row in evidence['records']}
    records = []
    for row in source['records']:
        number = row['message_ID']
        if number == 318:
            continue
        reference = bound[number]
        assert row['source_reference'] == reference['source'] and row['current_reference'] == reference['previous']
        records.append(row | dict(review=row['review'] | {'formatting': True},
            registered_reference=reference['stored'] | {'exact_stored_hex': reference['stored_hex'],
                'ROM_sha256': evidence['research_ROM_sha256']},
            layout_revised_without_prose_revision=row['decision'] == 'retention'
                and reference['stored_hex'] != row['current_hex'],
            gameplay_observed=number in scope['observed_notice_IDs'], new_credit=1))
    assert len(records) == TOTAL and base.Counter(row['decision'] for row in records) == {'revision': REVISED, 'retention': RETAINED}
    review = dict(translation_policy=source['translation_policy'], target_locale=source['target_locale'],
        encoder=source['encoder'], review_gates=source['review_gates'], records=records,
        actual_verification_scope=scope, full_goal_complete=False)
    base.validate_natural_dialogue_batch(review)
    return review


def publish(release):
    summary = 'The 14 system and equipment notices are registered. The ledger now credits 26,333 reviews.'
    notes = f"""# All Routes Equipment and System candidate

Use the local ROM \x60{ROM.as_posix()}\x60 beside its build manifest. The [clean-input patch](translation.xdelta) applies to clean Japanese SHA-256 \x60{release['clean_input_sha256']}\x60 and reconstructs SHA-256 \x60{release['candidate_sha256']}\x60 byte for byte. Patch SHA-256 is \x60{release['patch_sha256']}\x60.

{summary} The batch includes eight prose revisions and six justified retentions. The equipment prompt uses “Who should equip it?” and the warning and breakage notice use the catalog name Demon Figurehead. Removal results keep the original two substitutions and wrap after the game expands them.

A controller and stylus replay used an existing ordinary save to buy, equip, and remove the Travels of Marco Polo in Lisbon. The chooser, both full notices, dismissal and return passed. All 21 stored modal variants, 79 release checks, 30 targeted tests, cold startup and 24 protected name getters passed. The ending, quit and forced-figurehead decisions passed offline body checks. [Gameplay verification](verification/equipment_gameplay_verification.json) · [Exact record review](verification/registered_review.json)
"""
    (PACKAGE / 'README.md').write_text(notes, encoding='utf-8', newline='\n')
    base.save(PACKAGE / 'checksums.json', {p.relative_to(PACKAGE).as_posix(): base.digest(p)
        for p in sorted(PACKAGE.rglob('*')) if p.is_file() and p.name != 'checksums.json'})
    pins_path = Path('translations/rom_retention_pins.json')
    pins = base.load(pins_path)
    for path, role in ((RESEARCH, 'equipment system research ROM'), (ROM, 'registered equipment system ROM')):
        assert not any(row['path'] == str(path.resolve()) for row in pins)
        pins.append(dict(path=str(path.resolve()), reason=f'Preserve {role}. SHA256 {base.digest(path)}'))
    base.replace_checked(pins_path, (json.dumps(pins, ensure_ascii=False, indent=2) + '\n').replace('\n', '\r\n').encode('utf-8'))
    live_setup = OUTPUT.with_name('setup_save_live_consumer_verification_v1.json')
    setup = base.load(live_setup)
    assert setup['source_current_inventory_sha256'] == base.digest(OUTPUT)
    assert setup['candidate_sha256'] == release['predecessor']['candidate_sha256']
    doc = f"""# System and equipment notices registered

{summary} Eight prose revisions and six justified retentions cover COMMON 315–329 except 318. Exact source, prior and registered references are in the review. The Demon Figurehead's two notices agree with native item 121. Removal record 329 reuses the established equipment paragraph renderer only under the original notice parent. [Release and patch](../{PACKAGE.as_posix()}/README.md) · [Registered review](../{REVIEW.as_posix()})

Three actual notices were observed in the original Lisbon Items flow. The staged selector opens the crew list, equips Travels of Marco Polo on Rafael, removes it, dismisses the result and returns to the town menu. All 21 stored modal variants passed independent pixel checks and were viewed. The three Yes/No bodies passed offline in their original wrapper. Hardware coverage remains pending.

The [setup and save inventory](../{OUTPUT.as_posix()}) binds 27 clean and registered records. Fresh boot reached the name and birthday editor and the Options Reports confirmation. Those sampled paths issued no COMMON lookups at the two traced entry points. The equipment replay supplied positive lookup controls. DS ending-save record 316 is independently bound, and 119 still carries the source's memory-card wording. The sampled menus do not establish global reachability for 98–111, 113–117, 119 or 124. [Observed menu and lookup evidence](../{live_setup.as_posix()})

Continue with the early shipyard and fleet setup notices around COMMON 261–286, using the identified direct callers to bind each exchange. Keep 318's exhibition branch, the three unresolved Market replies and all remaining town, random and player-facing prose open.
"""
    base.replace_checked(DOC, doc.encode('utf-8'))
    lead = f'# Current editorial checkpoint - 2026-11-11\n\n{summary}\n\nContinue from [the registered system and equipment notices]({DOC.name}).\n\n'.encode('utf-8')
    for name in ('editorial_handoff_current.md', 'editorial_efficiency_workflow.md', 'translation_progress.md'):
        path = Path('docs') / name
        base.replace_checked(path, lead + path.read_bytes())
    path = Path('docs/build_continuity_protocol.md')
    protocol = f"""The 14 system and equipment notices are registered over Captain Biographies with 744 entries, 114 accepted layers and 79 checks. Use \x60scripts/register_setup_save_equipment_v1.py --register\x60 to stage and \x60--publish-prepared\x60 to publish. Preserve the original yes/no routes, direct crew-list prompt, paired name/item substitutions and the message-329-only paragraph dispatch. Exact reconstruction, the live equip/remove sequence and startup pass. [Registered checkpoint]({DOC.name})

"""
    base.replace_checked(path, protocol.encode('utf-8') + path.read_bytes())
    print('Registered 744 entries and credited 14 equipment and system notices once.')


def register():
    env = {**vars(base), **globals(), 'preserve_compression': transaction.preserve_compression}
    ledger = checked_text(inspect.getsource(base.update_ledger), {
        "'diplomatic-and-scheme-outcome-notices'": "'equipment-and-system-notices'",
        'Thirty-four diplomacy and scheme outcomes are registered.': 'Fourteen system and equipment notices are registered.',
        '== 25985': '== 26333', '== 15438': '== 15699', '== 10547': '== 10634',
    })
    old_scope = """    scope = dict(observed_notice_IDs=approved['live_messages'], stored_cases=176, fresh_viewed_pages=31,
        reused_exact_viewed_pages=145, fixture_scope='One incoming letter in a previously empty isolated RAM slot',
        original_no_preserved_war=True, natural_letter_generation=False, hardware=False)"""
    registration = checked_text(inspect.getsource(base.register), {
        "approved['live_messages'] == [349, 356, 352]": "approved['observed_ids'] == live['observed_ids']",
        "sum(int(s.get('tests', 0)) for s in tests) == 27": "sum(int(s.get('tests', 0)) for s in tests) == 30",
        "len(manifest['batches']) == 734 and len(manifest['checks']) == 69":
            "len(manifest['batches']) == 743 and len(manifest['checks']) == 78",
        "evidence['target_ARM9_sha256']": "evidence['research_ARM9_sha256']",
        "evidence['target_COMMON_sha256']": "evidence['research_COMMON_sha256']",
        old_scope: '    scope = verification_scope(approved, live)',
        'release_stack_before_diplomacy.json': 'release_stack_before_equipment_system.json',
        'verified_crew_notice_predecessor=predecessor, diplomatic_outcome_release=str(REVIEW)':
            'verified_captain_biographies_predecessor=predecessor, equipment_system_release=str(REVIEW)',
        'Reviewed diplomacy and scheme outcomes with scoped native phrase wrapping.':
            'Reviewed system and equipment notices, including the original removal result.',
        'release_stack.diplomacy.pending.json': 'release_stack.equipment_system.pending.json',
        "LEDGER.with_name('editorial_review_current.diplomacy.pending.json')": 'PENDING_LEDGER',
        '    save(pending_registry, registry)':
            '    preserve_compression(pending_registry, REGISTRY)\n    save(pending_registry, registry)',
        "evidence['wrapper']": "evidence['ownership']",
        'COMMON_DIPLOMATIC_OUTCOMES_MODAL_AND_PHRASE_WRAP': 'COMMON_329_EQUIPMENT_REMOVAL_WORD_WRAP',
        "manifest['diplomatic_outcomes_registered_successor_pipeline']":
            "manifest['equipment_system_registered_successor_pipeline']",
        "len(manifest['batches']) == 735 and len(manifest['checks']) == 70":
            "len(manifest['batches']) == 744 and len(manifest['checks']) == 79",
        'registered_manifest_entries=735, accepted_layers=114, passing_release_checks=70, repository_tests=27':
            'registered_manifest_entries=744, accepted_layers=114, passing_release_checks=79, repository_tests=30',
        '    pending_registry.replace(REGISTRY)\n    try:\n        pending_ledger.replace(LEDGER)\n    except OSError:\n        replace_checked(REGISTRY, before_registry)\n        raise\n    assert digest(REGISTRY) == release[\'registry_sha256\'] and digest(PROMOTED) == promoted\n    publish(release)':
            '    assert digest(PROMOTED) == promoted\n    print(\'Equipment/system registration staged and ready to publish.\')',
    })
    exec(compile(ledger + '\n\n' + registration, __file__ + '::equipment-system-registration', 'exec'), env)
    env['register']()


def publish_prepared():
    env = {**vars(transaction), **globals(), 'prior': base}
    env['verify_prepared'] = FunctionType(transaction.verify_prepared.__code__, env)
    code = checked_text(inspect.getsource(transaction.publish_prepared), {
        'release_stack.sea_events.pending.json': 'release_stack.equipment_system.pending.json',
    })
    exec(compile(code, __file__ + '::equipment-system-publication', 'exec'), env)
    env['publish_prepared']()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    action = parser.add_mutually_exclusive_group(required=True)
    action.add_argument('--register', action='store_true')
    action.add_argument('--publish-prepared', action='store_true')
    (publish_prepared if parser.parse_args().publish_prepared else register)()
