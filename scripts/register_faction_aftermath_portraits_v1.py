"""Register the verified faction aftermath portraits over Diplomatic Letters."""

import argparse
import inspect
import json
from pathlib import Path
from types import FunctionType

from scripts import register_rumor_and_cooperation_v1 as template
from scripts import stage_faction_aftermath_portraits_v2 as stage
from scripts.register_diplomatic_letter_portraits_v1 import RELEASE as PARENT
from scripts.source_locked_derivation_v5118 import checked_text
from scripts.verify_faction_aftermath_portraits_v1 import BOOT as STARTUP_VERIFICATION
from scripts.verify_faction_aftermath_portraits_v1 import CHECKPOINT, LIVE as LIVE_VERIFICATION, OBSERVED, QA


base = template.base
PROFILE = 'all-routes-faction-aftermath-portraits-editorial-v1-20261111'
FAMILY = 'faction_aftermath_portraits_contextual_20261111'
CHECK = 'registered_faction_aftermath_portraits_native_live_and_complete_parent_inverse'
PACKAGE = Path('releases/all_routes_editorial_20261111_faction_aftermath_portraits_candidate')
VERIFICATION = PACKAGE / 'verification'
RELEASE = VERIFICATION / 'registered_release_verification.json'
REVIEW = VERIFICATION / 'registered_review.json'
MUTATION_PLAN = VERIFICATION / 'registration_mutation_plan.json'
TEST = Path('out/faction_aftermath_portraits_registered_20261111_v1')
ROM = TEST / 'Translation_DS_All_Routes_Faction_Aftermath_Portraits_20261111_candidate.nds'
MANIFEST = ROM.with_suffix('.manifest.json')
PATCH = PACKAGE / 'translation.xdelta'
DOC = Path('docs/editorial_faction_aftermath_portraits_registered_20261111.md')
PENDING_LEDGER = TEST / 'editorial_review_current.faction_aftermath_portraits.pending.json'
OUTPUT, EVIDENCE, RESEARCH = stage.OUTPUT, stage.PROOF, stage.ROM
PREVIOUS_TOTAL, TOTAL, REVISED, RETAINED = 26512, 21, 12, 9


def rebuild(parent, evidence, source):
    return FunctionType(template.rebuild.__code__, vars(template) | globals())(parent, evidence, source)


def verification_scope(approved, live):
    assert approved['observed_ids'] == live['observed_ids'] == list(OBSERVED)
    assert approved['stored_records'] == approved['viewed_pages'] == TOTAL
    assert all(row['only_temporary_sailing_instructions_changed'] for row in live['fixture'])
    assert live['original_sailing_instructions_restored']
    return dict(observed_notice_IDs=list(OBSERVED), stored_records=TOTAL, portrait_variants=TOTAL,
        directly_viewed_portrait_pages=TOTAL, original_disband_notice_then_two_portraits_then_sailing=True,
        fixture_scope='A temporary sailing update called the original dissolution handler for an existing NPC faction in an isolated save. The original game chose fleet outcomes and speakers.',
        natural_faction_defeat=False, displaced_commander_branch_unvisited=True,
        offline_only_notice_IDs=[n for n in range(2690, 2711) if n not in OBSERVED], hardware=False)


def final_review(source, evidence, scope):
    result = FunctionType(template.final_review.__code__, vars(template) | globals())(source, evidence, scope)
    for row in result['records']:
        n = row['message_ID']
        if n < 2697:
            row['context'] = ('After the faction disband notice, the native handler selects the commander of the '
                              'fleet whose actor ID matches the faction leader. This is the leader’s own response to defeat.')
        elif n < 2704:
            row['context'] = ('The native dissolution handler processes another fleet of the same faction. Its commander '
                              'can speak after the leader’s own reaction in the same sequence. The line expresses a vow '
                              'about the faction commander from the speaker’s perspective.')
        else:
            row['context'] = ('The native dissolution handler changes the speaker’s affiliation. The displaced fleet '
                              'commander considers what to do next, including looking for work in one voice.')
    credited = next(row for row in source['previously_credited_neighbors'] if row['message_ID'] == 337)
    result['already_credited_context_retentions'] = [
        credited | dict(localization_note='Keep the succinct faction-wide disband notice that introduces the fleet reactions.', new_credit=0)]
    return result


def publish(release):
    summary = 'The 21 faction aftermath portraits are registered. The ledger now credits 26,533 reviews.'
    notes = f"""# All Routes Faction Aftermath Portraits candidate

Use the local ROM {chr(96)}{ROM.as_posix()}{chr(96)} with its adjacent build manifest. The [clean-input patch](translation.xdelta) applies to clean Japanese SHA-256 {chr(96)}{release['clean_input_sha256']}{chr(96)} and reconstructs SHA-256 {chr(96)}{release['candidate_sha256']}{chr(96)} byte for byte. Patch SHA-256 is {chr(96)}{release['patch_sha256']}{chr(96)}.

{summary} Twelve revisions and nine justified retentions cover the faction leader’s defeat, the other fleet commanders’ vows, and the displaced commanders weighing their next move. Six refinements improve phrase continuity. Twenty-five full-width capital I glyphs across 18 templates now use the dialogue font.

The sailing replay called the original dissolution handler for the Hayreddin Clan in an isolated save. It displayed the disband notice, Barbarossa Hayreddin’s reaction and Salid Ajar’s vow, then returned to sailing. The other 19 portraits were checked offline. All 21 native portrait layouts, 86 release checks, 30 targeted tests, cold startup and 24 protected name getters passed. Hardware acceptance is pending. [Gameplay proof](verification/faction_aftermath_portraits_gameplay_verification.json) · [Exact record review](verification/registered_review.json)
"""
    (PACKAGE / 'README.md').write_text(notes, encoding='utf-8', newline='\n')
    base.save(PACKAGE / 'checksums.json', {p.relative_to(PACKAGE).as_posix(): base.digest(p)
        for p in sorted(PACKAGE.rglob('*')) if p.is_file() and p.name != 'checksums.json'})
    pins_path = Path('translations/rom_retention_pins.json')
    pins = base.load(pins_path)
    for path, role in ((stage.initial.ROM, 'first faction aftermath review ROM'),
                       (RESEARCH, 'phrase-refined faction aftermath review ROM'), (ROM, 'registered faction aftermath ROM')):
        resolved = str(path.resolve())
        assert not any(row['path'] == resolved for row in pins)
        pins.append(dict(path=resolved, reason=f'Preserve {role}. SHA256 {base.digest(path)}'))
    base.replace_checked(pins_path, (json.dumps(pins, ensure_ascii=False, indent=2) + '\n').replace('\n', '\r\n').encode('utf-8'))
    doc = f"""# Faction aftermath portraits registered

{summary} The new work covers COMMON 2690–2710 across all three original voice tables. The same disbanding sequence can include the faction leader’s reaction and a second commander’s vow. The separate displaced-fleet response keeps the speaker’s concern about what comes next. The earlier faction-wide disband notice retains its wording and credit. [Release and patch](../{PACKAGE.as_posix()}/README.md) · [Registered review](../{REVIEW.as_posix()})

The focused emulator replay displayed the original disband notice, 2691 and 2703, then returned to sailing. The fixture called the original handler for the existing Hayreddin Clan from an isolated sailing session. The game processed both fleets, cleared both commanders’ affiliations and applied the faction outcome. The temporary instruction changes were restored. The other 19 portraits were checked offline.

Continue with the coin-game response at COMMON 2814 and the item-card descriptions beginning at 2815, including Baby Shark at 2819. Preserve the separate Options and Market callers, graphics artwork and older-record technical re-audit.
"""
    base.replace_checked(DOC, doc.encode('utf-8'))
    lead = f'# Current editorial checkpoint - 2026-11-11\n\n{summary}\n\nContinue from [the registered faction aftermath portraits]({DOC.name}).\n\n'
    for name in ('editorial_handoff_current.md', 'editorial_efficiency_workflow.md', 'translation_progress.md'):
        path = Path('docs') / name
        base.replace_checked(path, lead.encode('utf-8') + path.read_bytes())
    continuity = Path('docs/build_continuity_protocol.md')
    protocol = (
        'The 21 faction aftermath portraits are registered over Diplomatic Letters with 751 entries, 114 accepted layers '
        'and 86 checks. Use {tick}scripts/register_faction_aftermath_portraits_v1.py --register{tick} and {tick}--publish-prepared{tick}. '
        'Preserve the three original voice tables, their conditional callers and the separate disband result. '
        f'Exact reconstruction, the sailing replay and startup pass. [Registered checkpoint]({DOC.name})\n\n').format(tick=chr(96))
    base.replace_checked(continuity, protocol.encode('utf-8') + continuity.read_bytes())
    print('Registered 751 entries and credited 21 faction aftermath portraits once.')


def register():
    source = checked_text(inspect.getsource(template.register), {
        'rumor-and-cooperation-portraits': 'faction-aftermath-portraits',
        'Forty-four rumor and cooperation portraits are registered.': 'Twenty-one faction aftermath portraits are registered.',
        "'== 25985': '== 26453', '== 15438': '== 15782', '== 10547': '== 10671'":
            "'== 25985': '== 26533', '== 15438': '== 15819', '== 10547': '== 10714'",
        "== 748 and len(manifest[\\'checks\\']) == 83": "== 750 and len(manifest[\\'checks\\']) == 85",
        "== 749 and len(manifest[\\'checks\\']) == 84": "== 751 and len(manifest[\\'checks\\']) == 86",
        'release_stack_before_rumor_and_cooperation.json': 'release_stack_before_faction_aftermath_portraits.json',
        'verified_shark_encounter_predecessor=predecessor, rumor_and_cooperation_release=str(REVIEW)':
            'verified_diplomatic_letters_predecessor=predecessor, faction_aftermath_portraits_release=str(REVIEW)',
        'Reviewed rumor and cooperation portraits with scoped native paragraph wrapping.':
            'Reviewed faction aftermath portraits with scoped native paragraph wrapping.',
        'release_stack.rumor_and_cooperation.pending.json': 'release_stack.faction_aftermath_portraits.pending.json',
        'COMMON_RUMOR_AND_COOPERATION_WORD_WRAP': 'COMMON_FACTION_AFTERMATH_PORTRAITS_WORD_WRAP',
        'rumor_and_cooperation_registered_successor_pipeline': 'faction_aftermath_portraits_registered_successor_pipeline',
        'registered_manifest_entries=749, accepted_layers=114, passing_release_checks=84, repository_tests=30':
            'registered_manifest_entries=751, accepted_layers=114, passing_release_checks=86, repository_tests=30',
        'Rumor and cooperation registration staged and ready to publish.':
            'Faction aftermath portrait registration staged and ready to publish.',
    })
    env = vars(template) | globals()
    exec(compile(source, __file__ + '::same-registered-release-transaction', 'exec'), env)
    env['register']()


def publish_prepared():
    source = checked_text(inspect.getsource(template.publish_prepared), {
        'release_stack.rumor_and_cooperation.pending.json': 'release_stack.faction_aftermath_portraits.pending.json',
    })
    env = vars(template) | globals()
    exec(compile(source, __file__ + '::same-registered-publication', 'exec'), env)
    env['publish_prepared']()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    action = parser.add_mutually_exclusive_group(required=True)
    action.add_argument('--register', action='store_true')
    action.add_argument('--publish-prepared', action='store_true')
    (publish_prepared if parser.parse_args().publish_prepared else register)()

