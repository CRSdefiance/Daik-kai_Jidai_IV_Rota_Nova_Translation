"""Register the original diplomatic letter portraits over Rumor and Cooperation."""

import argparse
import inspect
import json
from pathlib import Path
from types import FunctionType, SimpleNamespace

from scripts import register_rumor_and_cooperation_v1 as prior
from scripts import stage_diplomatic_letter_portraits_v1 as stage_initial
from scripts import stage_diplomatic_letter_portraits_v2 as stage_final
from scripts.source_locked_derivation_v5118 import checked_text
from scripts.verify_diplomatic_letter_portraits_v1 import BOOT as STARTUP_VERIFICATION
from scripts.verify_diplomatic_letter_portraits_v1 import CHECKPOINT, LIVE as LIVE_VERIFICATION, QA


base, PARENT = prior.base, prior.RELEASE
stage = SimpleNamespace(**(vars(stage_final) | {
    'transform': stage_initial.wrapper.transform,
    'relocate': stage_initial.previous.relocate,
    'reference': stage_initial.previous.reference,
}))
PROFILE = 'all-routes-diplomatic-letter-portraits-editorial-v1-20261111'
FAMILY = 'diplomatic_letter_portraits_contextual_20261111'
CHECK = 'registered_diplomatic_letter_portraits_native_live_and_complete_parent_inverse'
PACKAGE = Path('releases/all_routes_editorial_20261111_diplomatic_letter_portraits_candidate')
VERIFICATION = PACKAGE / 'verification'
RELEASE = VERIFICATION / 'registered_release_verification.json'
REVIEW = VERIFICATION / 'registered_review.json'
MUTATION_PLAN = VERIFICATION / 'registration_mutation_plan.json'
TEST = Path('out/diplomatic_letter_portraits_registered_20261111_v1')
ROM = TEST / 'Translation_DS_All_Routes_Diplomatic_Letter_Portraits_20261111_candidate.nds'
MANIFEST = ROM.with_suffix('.manifest.json')
PATCH = PACKAGE / 'translation.xdelta'
DOC = Path('docs/editorial_diplomatic_letter_portraits_registered_20261111.md')
PENDING_LEDGER = TEST / 'editorial_review_current.diplomatic_letter_portraits.pending.json'
OUTPUT, EVIDENCE, RESEARCH = stage.OUTPUT, stage.PROOF, stage.ROM
PREVIOUS_TOTAL, TOTAL, REVISED, RETAINED = 26453, 59, 25, 34
OBSERVED = [2757, 2766]


def rebuild(parent, evidence, source):
    return FunctionType(prior.rebuild.__code__, vars(prior) | globals())(parent, evidence, source)


def verification_scope(approved, live):
    assert approved['observed_ids'] == live['observed_ids'] == OBSERVED
    assert approved['stored_records'] == TOTAL and approved['viewed_pages'] == 95
    assert live['fixture']['only_letter_slot_bytes_changed'] and not live['fixture']['outcome_forced']
    assert live['original_letter_consumed_and_recipient_independent']
    return dict(observed_notice_IDs=OBSERVED, stored_records=TOTAL, portrait_variants=95,
        directly_viewed_portrait_pages=95, original_rejection_and_inn_return=True,
        fixture_scope='One original outgoing submission letter in an isolated Istanbul save. The game selected the response.',
        actual_natural_letter_generation=False, submission_acceptance_and_ignore_unvisited=True,
        offline_only_notice_IDs=[n for n in range(2711, 2770) if n not in OBSERVED], hardware=False)


def final_review(source, evidence, scope):
    review = FunctionType(prior.final_review.__code__, vars(prior) | globals())(source, evidence, scope)
    rationale = {
        347: 'Keep the brief delivery notice before the recipient appears.',
        362: 'Keep the explicit outcome of coming under the player’s authority.',
        363: 'Keep the explicit rejection and the diplomacy menu’s merger terminology.',
        381: 'Keep the distinct no-reply result and the same merger terminology.',
    }
    review['already_credited_context_retentions'] = [
        row | {'localization_note': rationale[row['message_ID']], 'new_credit': 0}
        for row in source['previously_credited_neighbors'] if row['message_ID'] in rationale]
    review['native_pact_break_surnames'] = source['native_pact_break_surnames']
    return review


def publish(release):
    summary = 'The 59 diplomatic letter portraits are registered. The ledger now credits 26,512 reviews.'
    notes = f"""# All Routes Diplomatic Letter Portraits candidate

Use the local ROM {chr(96)}{ROM.as_posix()}{chr(96)} with its adjacent build manifest. The [clean-input patch](translation.xdelta) applies to clean Japanese SHA-256 {chr(96)}{release['clean_input_sha256']}{chr(96)} and reconstructs SHA-256 {chr(96)}{release['candidate_sha256']}{chr(96)} byte for byte. Patch SHA-256 is {chr(96)}{release['patch_sha256']}{chr(96)}.

{summary} Twenty-five revisions and 34 justified retentions cover personal letters, pacts, cease-fires, declarations of war, and submission demands. Fourteen original voice tables select the same speakers and results. Pact-break portraits preserve the original captain surname. The other affected exchanges preserve faction names. All 95 native portrait variants passed stored and visual checks. Fourteen legacy full-width I and F glyphs across 13 templates now use the dialogue font.

The focused Istanbul replay initialized one original deferred letter. Martin Speyer voiced the demand and rejection, the game reported the merger refusal, and play returned to the inn. All 85 release checks, 30 targeted tests, cold startup and 24 protected name getters passed. Hardware acceptance is pending. [Gameplay proof](verification/diplomatic_letter_portraits_gameplay_verification.json) · [Exact record review](verification/registered_review.json)
"""
    (PACKAGE / 'README.md').write_text(notes, encoding='utf-8', newline='\n')
    base.save(PACKAGE / 'checksums.json', {p.relative_to(PACKAGE).as_posix(): base.digest(p)
        for p in sorted(PACKAGE.rglob('*')) if p.is_file() and p.name != 'checksums.json'})
    pin_path = Path('translations/rom_retention_pins.json')
    pins = base.load(pin_path)
    for path, role in ((stage_initial.ROM, 'first diplomatic letter review ROM'),
                       (RESEARCH, 'phrase-refined diplomatic letter review ROM'), (ROM, 'registered diplomatic letter ROM')):
        resolved = str(path.resolve())
        assert not any(row['path'] == resolved for row in pins)
        pins.append(dict(path=resolved, reason=f'Preserve {role}. SHA256 {base.digest(path)}'))
    base.replace_checked(pin_path, (json.dumps(pins, ensure_ascii=False, indent=2) + '\n').replace('\n', '\r\n').encode('utf-8'))
    notes = f"""# Diplomatic letter portraits registered

{summary} The new text covers COMMON 2711–2769 across all 14 original voice tables. Five visual refinements keep a faction name, a closing question or a short reaction together. The earlier delivery and merger-result notices retain their wording and prior credit. [Release and patch](../{PACKAGE.as_posix()}/README.md) · [Registered review](../{REVIEW.as_posix()})

The original deferred-letter fixture observed the demand and voiced rejection, then the native refusal notice and return to the Istanbul inn. The other 57 portraits were checked offline, including alternate acceptance and dismissal. All four pact-break surname substitutions were checked offline.

Continue with the faction defeat, succession and displaced-crew portraits at COMMON 2690–2710 and their original branches. The [source review](../{OUTPUT.as_posix()}) preserves the exact neighboring references. Keep the open item-card prose, Options and Market callers, artwork and older-record technical re-audit in scope.
"""
    base.replace_checked(DOC, notes.encode('utf-8'))
    lead = f'# Current editorial checkpoint - 2026-11-11\n\n{summary}\n\nContinue from [the registered diplomatic letter portraits]({DOC.name}).\n\n'
    for name in ('editorial_handoff_current.md', 'editorial_efficiency_workflow.md', 'translation_progress.md'):
        path = Path('docs') / name
        base.replace_checked(path, lead.encode('utf-8') + path.read_bytes())
    continuity = Path('docs/build_continuity_protocol.md')
    protocol = (
        'The 59 diplomatic letter portraits are registered over Rumor and Cooperation with 750 entries, '
        '114 accepted layers and 85 checks. Use {tick}scripts/register_diplomatic_letter_portraits_v1.py --register{tick} '
        'and {tick}--publish-prepared{tick}. Preserve the fourteen voice tables, original results and distinct faction and '
        'captain-surname getters. Exact reconstruction, native submission rejection and startup pass. '
        f'[Registered checkpoint]({DOC.name})\n\n').format(tick=chr(96))
    base.replace_checked(continuity, protocol.encode('utf-8') + continuity.read_bytes())
    print('Registered 750 entries and credited 59 diplomatic letter portraits once.')


def register():
    source = checked_text(inspect.getsource(prior.register), {
        'rumor-and-cooperation-portraits': 'diplomatic-letter-portraits',
        'Forty-four rumor and cooperation portraits are registered.': 'Fifty-nine diplomatic letter portraits are registered.',
        "'== 25985': '== 26453', '== 15438': '== 15782', '== 10547': '== 10671'":
            "'== 25985': '== 26512', '== 15438': '== 15807', '== 10547': '== 10705'",
        "== 748 and len(manifest[\\'checks\\']) == 83": "== 749 and len(manifest[\\'checks\\']) == 84",
        "== 749 and len(manifest[\\'checks\\']) == 84": "== 750 and len(manifest[\\'checks\\']) == 85",
        'release_stack_before_rumor_and_cooperation.json': 'release_stack_before_diplomatic_letter_portraits.json',
        'verified_shark_encounter_predecessor=predecessor, rumor_and_cooperation_release=str(REVIEW)':
            'verified_rumor_and_cooperation_predecessor=predecessor, diplomatic_letter_portraits_release=str(REVIEW)',
        'Reviewed rumor and cooperation portraits with scoped native paragraph wrapping.':
            'Reviewed diplomatic letters and submission portraits with scoped native paragraph wrapping.',
        'release_stack.rumor_and_cooperation.pending.json': 'release_stack.diplomatic_letter_portraits.pending.json',
        'COMMON_RUMOR_AND_COOPERATION_WORD_WRAP': 'COMMON_DIPLOMATIC_LETTER_PORTRAITS_WORD_WRAP',
        'rumor_and_cooperation_registered_successor_pipeline': 'diplomatic_letter_portraits_registered_successor_pipeline',
        'registered_manifest_entries=749, accepted_layers=114, passing_release_checks=84, repository_tests=30':
            'registered_manifest_entries=750, accepted_layers=114, passing_release_checks=85, repository_tests=30',
        'Rumor and cooperation registration staged and ready to publish.':
            'Diplomatic letter portrait registration staged and ready to publish.',
    })
    env = vars(prior) | globals()
    exec(compile(source, __file__ + '::same-registered-release-transaction', 'exec'), env)
    env['register']()


def publish_prepared():
    source = checked_text(inspect.getsource(prior.publish_prepared), {
        'release_stack.rumor_and_cooperation.pending.json': 'release_stack.diplomatic_letter_portraits.pending.json',
    })
    env = vars(prior) | globals()
    exec(compile(source, __file__ + '::same-registered-publication', 'exec'), env)
    env['publish_prepared']()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    action = parser.add_mutually_exclusive_group(required=True)
    action.add_argument('--register', action='store_true')
    action.add_argument('--publish-prepared', action='store_true')
    (publish_prepared if parser.parse_args().publish_prepared else register)()

