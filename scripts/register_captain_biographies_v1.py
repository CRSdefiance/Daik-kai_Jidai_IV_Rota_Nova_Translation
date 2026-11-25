"""Register the verified chooser biographies as an ARM9-only successor."""

import argparse
import inspect
import json
from pathlib import Path
from types import FunctionType

from scripts import register_diplomatic_outcomes_v2 as base
from scripts import register_sea_event_review_v2 as transaction
from scripts import stage_captain_biographies_v2 as stage
from scripts.register_sera_assignment_review_v1 import RELEASE as PARENT
from scripts.source_locked_derivation_v5118 import checked_text
from scripts.verify_captain_biographies_v1 import BOOT as STARTUP_VERIFICATION
from scripts.verify_captain_biographies_v1 import CHECKPOINT, LIVE as LIVE_VERIFICATION


PROFILE = 'all-routes-captain-biographies-editorial-v1-20261111'
FAMILY = 'captain_chooser_biographies_contextual_20261111'
CHECK = 'registered_captain_biography_display_and_complete_parent_inverse'
PACKAGE = Path('releases/all_routes_editorial_20261111_captain_biographies_candidate')
VERIFICATION = PACKAGE / 'verification'
RELEASE = VERIFICATION / 'registered_release_verification.json'
REVIEW = VERIFICATION / 'registered_review.json'
MUTATION_PLAN = VERIFICATION / 'registration_mutation_plan.json'
TEST = Path('out/captain_biographies_registered_20261111_v1')
ROM = TEST / 'Translation_DS_All_Routes_Captain_Biographies_20261111_candidate.nds'
MANIFEST = ROM.with_suffix('.manifest.json')
PATCH = PACKAGE / 'translation.xdelta'
DOC = Path('docs/editorial_captain_biographies_registered_20261111.md')
PENDING_LEDGER = TEST / 'editorial_review_current.captain_biographies.pending.json'
QA = Path('work/captain_biographies_repo_qa_exact_20261111.xml')
OUTPUT = EVIDENCE = stage.PROOF
RESEARCH = stage.ROM
PREVIOUS_TOTAL, TOTAL, REVISED, RETAINED = 26315, 4, 4, 0


def rebuild(parent, evidence, source):
    assert source == evidence
    assert base.digest(stage.__file__) == evidence['producer_sha256']
    assert base.digest(stage.previous.INVENTORY) == evidence['inventory_sha256']
    assert base.digest(base.PROMOTED) == evidence['promoted_sha256']
    env = {**vars(stage.previous), 'DECISIONS': stage.DECISIONS, 'encode_rows': stage.encode_rows}
    compiler = checked_text(inspect.getsource(stage.previous.rebuild), {
        "payload = '\\n'.join(lines).encode('ascii') + b'\\0'": 'payload = encode_rows(lines)',
    })
    exec(compile(compiler, __file__ + '::verified-biography-storage', 'exec'), env)
    image, clean = base.NdsImage.open(parent['candidate']), base.NdsImage.open(base.CLEAN)
    before = image.read_file(base.ARM)
    arm, rows, pointers, asset_matches = env['rebuild'](image, clean, base.load(stage.previous.INVENTORY))
    assert json.loads(json.dumps(rows)) == evidence['records']
    assert pointers == evidence['old_direct_pointer_owners']
    assert asset_matches == evidence['unchanged_asset_payload_matches']
    common = image.read_file(base.COMMON)
    assert base.sha256(common).hexdigest() == parent['target_COMMON_sha256']
    image.replace_file(base.ARM, arm)
    assert bytes(image.rom.save()) == RESEARCH.read_bytes()
    image.replace_file(base.ARM, before)
    assert bytes(image.rom.save()) == Path(parent['candidate']).read_bytes()
    return arm, common


def verification_scope(approved, live):
    assert approved['live_captains'] == live['live_captains'] == ['Rafael', 'Hodram', 'Lil', 'Maria']
    assert approved['stored_cases'] == approved['viewed_pages'] == 4
    assert len(live['live_cases']) == 7 and live['reverse_switch_verified']
    return dict(observed_captains=live['live_captains'], stored_biographies=4, viewed_pages=4,
                native_selector_cases=4, emulator_chooser_selections=7, original_back_return=True,
                existing_system_unlock_fixture=True, new_unlock_earned=False, hardware=False)


def final_review(source, evidence, scope):
    assert source == evidence
    records = []
    for row in source['records']:
        assert row['review']['formatting'] is False
        assert row['actor'] in scope['observed_captains']
        records.append(row | dict(review=row['review'] | {'formatting': True},
            registered_reference=row['staged_reference'] | {'ROM_sha256': evidence['research_ROM_sha256']},
            gameplay_observed=True, new_credit=1))
    assert len(records) == TOTAL and all(row['decision'] == 'revision' for row in records)
    review = dict(translation_policy='natural-dialogue-v2', target_locale='en-US',
        encoder='dialogue-relocatable-v1', review_gates=sorted(records[0]['review']),
        records=records, actual_verification_scope=scope, full_goal_complete=False)
    base.validate_natural_dialogue_batch(review)
    return review


def publish(release):
    summary = 'The four New Game biographies are registered. The ledger now credits 26,319 reviews.'
    notes = f"""# All Routes Captain Biographies candidate

Use the local ROM \x60{ROM.as_posix()}\x60 beside its build manifest. The [clean-input patch](translation.xdelta) applies to clean Japanese SHA-256 \x60{release['clean_input_sha256']}\x60 and reconstructs SHA-256 \x60{release['candidate_sha256']}\x60 byte for byte. Patch SHA-256 is \x60{release['patch_sha256']}\x60.

{summary} The revisions preserve Rafael's first-time recommendation, Hodram's privateer fleet and renewed Swedish independence, Lil's partnership with Camille, and Maria's defense against wokou raids. The original chooser still uses three rows. The compiler places a blank before an LF when needed to keep the next row's first letter in place.

All four biographies passed complete native glyph and bounds checks. Seven emulator selections covered forward and reverse switching and the original Back transition with the existing system unlock fixture. The candidate passed its own cold boot through Maria's startup, 24 protected name getters, 78 release checks and 30 targeted repository tests. The release carries forward the Market fix and ASCII right bounds. [Gameplay verification](verification/captain_chooser_gameplay_verification.json) · [Registered review](verification/registered_review.json)
"""
    (PACKAGE / 'README.md').write_text(notes, encoding='utf-8', newline='\n')
    base.save(PACKAGE / 'checksums.json', {p.relative_to(PACKAGE).as_posix(): base.digest(p)
        for p in sorted(PACKAGE.rglob('*')) if p.is_file() and p.name != 'checksums.json'})
    pins_path = Path('translations/rom_retention_pins.json')
    pins = base.load(pins_path)
    for path, role in ((stage.previous.ROM, 'bare-LF chooser research ROM'),
                       (RESEARCH, 'pair-safe chooser research ROM'), (ROM, 'registered chooser ROM')):
        assert not any(row['path'] == str(path.resolve()) for row in pins)
        pins.append(dict(path=str(path.resolve()), reason=f'Preserve {role}. SHA256 {base.digest(path)}'))
    base.replace_checked(pins_path, (json.dumps(pins, ensure_ascii=False, indent=2) + '\n').replace('\n', '\r\n').encode('utf-8'))
    doc = f"""# New Game biographies registered

{summary} The original chooser's four ARM9 pointers and 424-byte allocation bind the reviewed English. The compiler keeps complete words and restores left alignment with an invisible blank before LF on odd-length ASCII rows. The font, chooser code, name fields, button prompts and every archive remain byte-exact. All four complete live text bands passed, including Lil's 39-character row. [Release package](../{PACKAGE.as_posix()}/README.md) · [Exact source, previous and registered references](../{REVIEW.as_posix()})

The original menu was observed on both registered predecessor and candidate with the same existing system unlock. Seven selections verified all four biographies, repeated selections in reverse order, and Back to the prior menu. The cloned selector separately resolved all four pointers. The 31,000-frame Maria startup matched the five unaffected frames and the complete revised biography at the chooser. All 24 protected name getters passed. Hardware coverage remains pending.

Continue with the unmapped Market replies, the legacy COMMON 104–107 consumer classification and remaining shared player-facing text. The separate graphics work and older-record technical re-audit remain open. Sera Assignment remains the build prepared for user promotion testing.
"""
    base.replace_checked(DOC, doc.encode('utf-8'))
    lead = f'# Current editorial checkpoint - 2026-11-11\n\n{summary}\n\nContinue from [the registered New Game biographies]({DOC.name}).\n\n'.encode('utf-8')
    for name in ('editorial_handoff_current.md', 'editorial_efficiency_workflow.md', 'translation_progress.md'):
        path = Path('docs') / name
        base.replace_checked(path, lead + path.read_bytes())
    continuity = Path('docs/build_continuity_protocol.md')
    protocol = f"""The four New Game biographies are registered over Sera Assignment with 743 entries, 114 accepted layers and 78 checks. Use \x60scripts/register_captain_biographies_v1.py --register\x60 to stage and \x60--publish-prepared\x60 to publish. Keep the original chooser code, four selection pointers and complete biography allocation. The compiler pads an odd ASCII row before LF and preserves the original NUL terminator. The exact clean-input reconstruction, all four live chooser views and 24 protected name getters pass. [Registered checkpoint]({DOC.name})

"""
    base.replace_checked(continuity, protocol.encode('utf-8') + continuity.read_bytes())
    print('Registered 743 entries and credited the four chooser biographies once.')


def register():
    env = {**vars(base), **globals(), 'preserve_compression': transaction.preserve_compression}
    ledger = checked_text(inspect.getsource(base.update_ledger), {
        "'diplomatic-and-scheme-outcome-notices'": "'captain-chooser-biographies'",
        'Thirty-four diplomacy and scheme outcomes are registered.': 'The four New Game biographies are registered.',
        '== 25985': '== 26319', '== 15438': '== 15691', '== 10547': '== 10628',
    })
    old_scope = """    scope = dict(observed_notice_IDs=approved['live_messages'], stored_cases=176, fresh_viewed_pages=31,
        reused_exact_viewed_pages=145, fixture_scope='One incoming letter in a previously empty isolated RAM slot',
        original_no_preserved_war=True, natural_letter_generation=False, hardware=False)"""
    old_manifest_ownership = """    manifest['relocations'][ARM][FAMILY] = evidence['wrapper']
    manifest['relocations'][COMMON][FAMILY] = evidence['storage']
    for path, ids in ((ARM, ('COMMON_DIPLOMATIC_OUTCOMES_MODAL_AND_PHRASE_WRAP',)),
                      (COMMON, [f'COMMON_MESSAGE_{n}' for n in evidence['storage']['changed_visible_templates']])):
        manifest['changed_records'][path].extend(n for n in ids if n not in manifest['changed_records'][path])"""
    new_manifest_ownership = """    manifest['relocations'][ARM][FAMILY] = dict(owned_ARM9_offsets=evidence['owned_ARM9_offsets'],
        exact_pointer_fields=evidence['old_direct_pointer_owners'], stored_count=4)
    ids = [row['id'] for row in review['records']]
    assert all(n not in manifest['changed_records'][ARM] for n in ids)
    manifest['changed_records'][ARM].extend(ids)"""
    registration = checked_text(inspect.getsource(base.register), {
        "approved['live_messages'] == [349, 356, 352]": "approved['live_captains'] == live['live_captains']",
        "sum(int(s.get('tests', 0)) for s in tests) == 27": "sum(int(s.get('tests', 0)) for s in tests) == 30",
        "len(manifest['batches']) == 734 and len(manifest['checks']) == 69":
            "len(manifest['batches']) == 742 and len(manifest['checks']) == 77",
        "evidence['target_ARM9_sha256']": "evidence['candidate_ARM9_sha256']",
        "evidence['target_COMMON_sha256']": "parent['target_COMMON_sha256']",
        old_scope: '    scope = verification_scope(approved, live)',
        'release_stack_before_diplomacy.json': 'release_stack_before_captain_biographies.json',
        'verified_crew_notice_predecessor=predecessor, diplomatic_outcome_release=str(REVIEW)':
            'verified_sera_assignment_predecessor=predecessor, captain_biographies_release=str(REVIEW)',
        'Reviewed diplomacy and scheme outcomes with scoped native phrase wrapping.':
            'Reviewed the four original chooser biographies with pair-safe native row boundaries.',
        'release_stack.diplomacy.pending.json': 'release_stack.captain_biographies.pending.json',
        "LEDGER.with_name('editorial_review_current.diplomacy.pending.json')": 'PENDING_LEDGER',
        '    save(pending_registry, registry)':
            '    preserve_compression(pending_registry, REGISTRY)\n    save(pending_registry, registry)',
        old_manifest_ownership: new_manifest_ownership,
        "manifest['diplomatic_outcomes_registered_successor_pipeline']":
            "manifest['captain_biographies_registered_successor_pipeline']",
        "len(manifest['batches']) == 735 and len(manifest['checks']) == 70":
            "len(manifest['batches']) == 743 and len(manifest['checks']) == 78",
        'registered_manifest_entries=735, accepted_layers=114, passing_release_checks=70, repository_tests=27':
            'registered_manifest_entries=743, accepted_layers=114, passing_release_checks=78, repository_tests=30',
        'changed_components=[ARM], changed_internal_files=[COMMON]':
            'changed_components=[ARM], changed_internal_files=[]',
        '    pending_registry.replace(REGISTRY)\n    try:\n        pending_ledger.replace(LEDGER)\n    except OSError:\n        replace_checked(REGISTRY, before_registry)\n        raise\n    assert digest(REGISTRY) == release[\'registry_sha256\'] and digest(PROMOTED) == promoted\n    publish(release)':
            '    assert digest(PROMOTED) == promoted\n    print(\'Captain biography registration staged and ready to publish.\')',
    })
    exec(compile(ledger + '\n\n' + registration, __file__ + '::captain-biographies-registration', 'exec'), env)
    env['register']()


def publish_prepared():
    env = {**vars(transaction), **globals(), 'prior': base}
    env['verify_prepared'] = FunctionType(transaction.verify_prepared.__code__, env)
    code = checked_text(inspect.getsource(transaction.publish_prepared), {
        'release_stack.sea_events.pending.json': 'release_stack.captain_biographies.pending.json',
    })
    exec(compile(code, __file__ + '::captain-biographies-publication', 'exec'), env)
    env['publish_prepared']()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    action = parser.add_mutually_exclusive_group(required=True)
    action.add_argument('--register', action='store_true')
    action.add_argument('--publish-prepared', action='store_true')
    (publish_prepared if parser.parse_args().publish_prepared else register)()
