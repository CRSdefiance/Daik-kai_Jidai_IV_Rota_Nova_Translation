"""Register the verified rumor and cooperation exchanges over Shark Encounter."""

import argparse
import inspect
import json
from pathlib import Path

from scripts import register_setup_save_equipment_v1 as previous
from scripts import stage_rumor_and_cooperation_v1 as stage
from scripts.register_shark_encounter_v1 import RELEASE as PARENT
from scripts.source_locked_derivation_v5118 import checked_text
from scripts.verify_rumor_and_cooperation_v1 import BOOT as STARTUP_VERIFICATION
from scripts.verify_rumor_and_cooperation_v1 import CHECKPOINT, LIVE as LIVE_VERIFICATION, QA


base = previous.base
PROFILE = 'all-routes-rumor-cooperation-editorial-v1-20261111'
FAMILY = 'rumor_and_cooperation_contextual_20261111'
CHECK = 'registered_rumor_and_cooperation_native_live_and_complete_parent_inverse'
PACKAGE = Path('releases/all_routes_editorial_20261111_rumor_and_cooperation_candidate')
VERIFICATION = PACKAGE / 'verification'
RELEASE = VERIFICATION / 'registered_release_verification.json'
REVIEW = VERIFICATION / 'registered_review.json'
MUTATION_PLAN = VERIFICATION / 'registration_mutation_plan.json'
TEST = Path('out/rumor_and_cooperation_registered_20261111_v1')
ROM = TEST / 'Translation_DS_All_Routes_Rumor_and_Cooperation_20261111_candidate.nds'
MANIFEST = ROM.with_suffix('.manifest.json')
PATCH = PACKAGE / 'translation.xdelta'
DOC = Path('docs/editorial_rumor_and_cooperation_registered_20261111.md')
PENDING_LEDGER = TEST / 'editorial_review_current.rumor_and_cooperation.pending.json'
OUTPUT, EVIDENCE, RESEARCH = stage.OUTPUT, stage.PROOF, stage.ROM
PREVIOUS_TOTAL, TOTAL, REVISED, RETAINED = 26409, 44, 24, 20


def rebuild(parent, evidence, source):
    code = checked_text(inspect.getsource(previous.rebuild), {
        "assert owner == evidence['ownership']": "assert json.loads(json.dumps(owner)) == evidence['ownership']",
        "rows = {row['message_ID']: row for row in source['records'] if row['message_ID'] != 318}":
            "rows = stage.active_rows(source)",
    })
    env = {**vars(previous), **globals()}
    exec(compile(code, __file__ + '::same-owned-payload-and-parent-inverse', 'exec'), env)
    return env['rebuild'](parent, evidence, source)


def verification_scope(approved, live):
    assert approved['observed_ids'] == live['observed_ids'] == [2802, 2803, 2805]
    assert approved['stored_records'] == 44 and approved['viewed_pages'] == 59
    assert live['fee_quote']['gold_fee'] == 9752
    assert live['refusal']['fixture']['only_letter_slot_bytes_changed']
    assert live['fee_quote']['fixture']['initialized_experience'] == 300000
    return dict(observed_notice_IDs=live['observed_ids'], stored_records=44, portrait_variants=59,
        directly_viewed_portrait_pages=59, original_refusal_and_inn_return=True,
        original_mixed_font_fee_and_insufficient_funds_return=True,
        fixture_scope='Two original deferred cooperation letters in isolated copies of an Istanbul save. The quote run also initialized one experience word. The original game decided the result and price.',
        actual_natural_letter_generation=False, payment_acceptance_unvisited=True,
        offline_only_notice_IDs=[n for n in range(2770, 2814) if n not in live['observed_ids']],
        hardware=False)

def final_review(source, evidence, scope):
    assert evidence['editorial_amendments'] == json.loads(json.dumps(stage.AMENDMENTS))
    updated = source | {'records': list(stage.active_rows(source).values())}
    env = {**vars(previous), **globals()}
    exec(compile(inspect.getsource(previous.final_review), __file__ + '::exact-natural-dialogue-review', 'exec'), env)
    result = env['final_review'](updated, evidence, scope)
    by_id = {}
    for variant in evidence['native_portrait_cases']:
        by_id.setdefault(variant['message_ID'], []).append(variant)
    for row in result['records']:
        row['registered_portrait_variants'] = [
            {key: variant[key] for key in ('arguments', 'lines', 'native_ink_sha256', 'native_glyphs')}
            for variant in by_id[row['message_ID']]]
    return result


def publish(release):
    summary = 'The 44 rumor and cooperation records are registered. The ledger now credits 26,453 reviews.'
    notes = f"""# All Routes Rumor and Cooperation candidate

Use the local ROM `{ROM.as_posix()}` beside its build manifest. The [clean-input patch](translation.xdelta) applies to clean Japanese SHA-256 `{release['clean_input_sha256']}` and reconstructs SHA-256 `{release['candidate_sha256']}` byte for byte. Patch SHA-256 is `{release['patch_sha256']}`.

{summary} Twenty-four revisions and 20 justified retentions cover the false reports and forged documents, the trader’s conditional offer and refusals, and all eight counter-rumor voices. The native portrait formatter preserves town, faction and gold arguments, and wraps complete words.

Two focused Istanbul emulator runs verified the original broker notices, a trader refusal, and a 9,752-gold quote with its insufficient-funds reply. Both runs returned to the inn with cash and shares intact. The deferred letters were initialized, and the fee run also initialized one experience word. All 59 stored display variants were visually reviewed. All 84 release checks, 30 targeted tests, cold startup and 24 protected name getters passed. [Gameplay proof](verification/rumor_and_cooperation_gameplay_verification_v2.json) · [Exact record review](verification/registered_review.json)
"""
    (PACKAGE / 'README.md').write_text(notes, encoding='utf-8', newline='\n')
    base.save(PACKAGE / 'checksums.json', {p.relative_to(PACKAGE).as_posix(): base.digest(p)
        for p in sorted(PACKAGE.rglob('*')) if p.is_file() and p.name != 'checksums.json'})
    pin_path = Path('translations/rom_retention_pins.json')
    pins = base.load(pin_path)
    for path, role in ((RESEARCH, 'rumor and cooperation research ROM'), (ROM, 'registered rumor and cooperation ROM')):
        assert not any(row['path'] == str(path.resolve()) for row in pins)
        pins.append(dict(path=str(path.resolve()), reason=f"Preserve {role}. SHA256 {release['candidate_sha256']}"))
    base.replace_checked(pin_path, (json.dumps(pins, ensure_ascii=False, indent=2) + '\n').replace('\n', '\r\n').encode('utf-8'))
    doc = f"""# Rumor and cooperation exchanges registered

{summary} The eight original tables distinguish reactions to reports, false-document responses, and each counter-rumor voice. The ten direct records preserve the original patron, town representative and trader consumers. The trader’s two-argument offer keeps fee before faction. [Release and patch](../{PACKAGE.as_posix()}/README.md) · [Registered review](../{REVIEW.as_posix()})

The two focused emulator runs observed 2802, 2803 and 2805, including the real 9,752-gold string and both returns to the inn. They initialized original deferred-letter slots and used the original handlers. The quote run also initialized one experience word. The other 41 records, including the separate rival-share quote and the counter-rumor variants, were checked offline. Hardware and natural letter activation remain unvisited.

Continue the earlier submission responses around 2757–2769 and their surrounding branches. The [source review](../{OUTPUT.as_posix()}) preserves those neighbors and the already credited notices without duplicating credit. Keep the open item-card prose, Options and Market callers, artwork and older-record technical re-audit in scope as recorded.
"""
    base.replace_checked(DOC, doc.encode('utf-8'))
    lead = f'# Current editorial checkpoint - 2026-11-11\n\n{summary}\n\nContinue from [the registered rumor and cooperation exchanges]({DOC.name}).\n\n'.encode('utf-8')
    for name in ('editorial_handoff_current.md', 'editorial_efficiency_workflow.md', 'translation_progress.md'):
        path = Path('docs') / name
        base.replace_checked(path, lead + path.read_bytes())
    continuity = Path('docs/build_continuity_protocol.md')
    lead = f"""The 44 rumor and cooperation portraits are registered over Shark Encounter with 749 entries, 114 accepted layers and 84 checks. Use `scripts/register_rumor_and_cooperation_v1.py --register` to stage and `--publish-prepared` to publish. Preserve the eight voice tables, the ten direct selectors, and the original portrait expansion and numeric glyphs. The exact reconstruction, the trader refusal and quote replays, and cold startup pass. [Registered checkpoint]({DOC.name})

"""
    base.replace_checked(continuity, lead.encode('utf-8') + continuity.read_bytes())
    print('Registered 749 entries and credited 44 rumor and cooperation portraits once.')

def register():
    source = checked_text(inspect.getsource(previous.register), {
        "'equipment-and-system-notices'": "'rumor-and-cooperation-portraits'",
        'Fourteen system and equipment notices are registered.': 'Forty-four rumor and cooperation portraits are registered.',
        "'== 25985': '== 26333', '== 15438': '== 15699', '== 10547': '== 10634'":
            "'== 25985': '== 26453', '== 15438': '== 15782', '== 10547': '== 10671'",
        '"len(manifest[\'batches\']) == 743 and len(manifest[\'checks\']) == 78"':
            '"len(manifest[\'batches\']) == 748 and len(manifest[\'checks\']) == 83"',
        '"len(manifest[\'batches\']) == 744 and len(manifest[\'checks\']) == 79"':
            '"len(manifest[\'batches\']) == 749 and len(manifest[\'checks\']) == 84"',
        'release_stack_before_equipment_system.json': 'release_stack_before_rumor_and_cooperation.json',
        'verified_captain_biographies_predecessor=predecessor, equipment_system_release=str(REVIEW)':
            'verified_shark_encounter_predecessor=predecessor, rumor_and_cooperation_release=str(REVIEW)',
        'Reviewed system and equipment notices, including the original removal result.':
            'Reviewed rumor and cooperation portraits with scoped native paragraph wrapping.',
        'release_stack.equipment_system.pending.json': 'release_stack.rumor_and_cooperation.pending.json',
        'COMMON_329_EQUIPMENT_REMOVAL_WORD_WRAP': 'COMMON_RUMOR_AND_COOPERATION_WORD_WRAP',
        'equipment_system_registered_successor_pipeline': 'rumor_and_cooperation_registered_successor_pipeline',
        'registered_manifest_entries=744, accepted_layers=114, passing_release_checks=79, repository_tests=30':
            'registered_manifest_entries=749, accepted_layers=114, passing_release_checks=84, repository_tests=30',
        'Equipment/system registration staged and ready to publish.':
            'Rumor and cooperation registration staged and ready to publish.',
    })
    env = {**vars(previous), **globals()}
    exec(compile(source, __file__ + '::same-registered-release-transaction', 'exec'), env)
    env['register']()


def publish_prepared():
    source = checked_text(inspect.getsource(previous.publish_prepared), {
        'release_stack.equipment_system.pending.json': 'release_stack.rumor_and_cooperation.pending.json',
    })
    env = {**vars(previous), **globals()}
    exec(compile(source, __file__ + '::same-registered-publication', 'exec'), env)
    env['publish_prepared']()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    action = parser.add_mutually_exclusive_group(required=True)
    action.add_argument('--register', action='store_true')
    action.add_argument('--publish-prepared', action='store_true')
    (publish_prepared if parser.parse_args().publish_prepared else register)()
