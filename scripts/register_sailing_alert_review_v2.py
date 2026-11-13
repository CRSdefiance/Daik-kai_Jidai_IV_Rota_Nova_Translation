"""Register the verified sailing alerts over the cumulative sea-event candidate."""

import argparse
from collections import Counter
from hashlib import sha256
import inspect
import json
from pathlib import Path
from types import FunctionType

from dk4tool.dialogue.review import validate_natural_dialogue_batch
from dk4tool.patch.sailing_alert_static_wrap_v1 import transform
from dk4tool.rom.nds import NdsImage
from dk4tool.script.common_message_table import DIRECTORY_OFFSET, TABLE_OFFSET
from scripts import register_diplomatic_outcomes_v2 as base
from scripts import register_sea_event_review_v2 as previous
from scripts.audit_story_glyph_consistency import load, save
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest
from scripts.package_ship_command_candidate_v1 import replace_checked
from scripts.seal_shared_text_source_v1 import ARM, COMMON, reference
from scripts.source_locked_derivation_v5118 import checked_text
from scripts.stage_sailing_alert_balanced_v2 import ORDINARY, OUTPUT, PROOF as EVIDENCE, ROM as RESEARCH
from scripts.stage_shared_notices_storage_v1 import relocate
from scripts.verify_sailing_alert_startup_v2 import BOOT as STARTUP_VERIFICATION, CHECKPOINT, LIVE as LIVE_VERIFICATION
from scripts.verify_sailing_alert_startup_v2 import OBSERVED, QA


PARENT = previous.RELEASE
PROFILE = 'all-routes-sailing-alert-editorial-v2-20261111'
FAMILY = 'shared_sailing_alerts_20261111'
CHECK = 'registered_sailing_alert_native_live_phrase_and_complete_parent_inverse'
PACKAGE = Path('releases/all_routes_editorial_20261111_sailing_alerts_candidate')
VERIFICATION = PACKAGE / 'verification'
RELEASE = VERIFICATION / 'registered_release_verification.json'
REVIEW = VERIFICATION / 'registered_review.json'
TEST = Path('out/sailing_alerts_registered_20261111_v2')
ROM = TEST / 'Translation_DS_All_Routes_Sailing_Alerts_20261111_candidate.nds'
MANIFEST = ROM.with_suffix('.manifest.json')
PATCH = PACKAGE / 'translation.xdelta'
DOC = Path('docs/editorial_sailing_alerts_registered_20261111.md')
PENDING_LEDGER = TEST / 'editorial_review_current.sailing_alerts.pending.json'
MUTATION_PLAN = VERIFICATION / 'registration_mutation_plan.json'
TOTAL, REVISED, RETAINED = 28, 24, 4
PREVIOUS_TOTAL = 26083


def rebuild(parent, evidence, source):
    image = NdsImage.open(parent['candidate'])
    old_arm, old_common = image.read_file(ARM), image.read_file(COMMON)
    wrapped, selector = transform(old_arm)
    assert json.loads(json.dumps(selector)) == evidence['selector']
    directory = sha256(old_arm[DIRECTORY_OFFSET:TABLE_OFFSET]).hexdigest()
    repack = FunctionType(relocate.__code__, {**relocate.__globals__, 'DIRECTORY': directory})
    rows = {row['message_ID']: row for row in source['records']}
    cases = {row['message_ID']: row for row in evidence['stored']}
    assert cases.keys() == rows.keys() and len(cases) == TOTAL
    storage = {n: bytes.fromhex(case['staged_hex']) for n, case in cases.items()}
    assert all(b' '.join(raw.split()) == rows[n]['english'].encode('ascii') for n, raw in storage.items())
    common, arm, rebound, packing = repack(old_common, wrapped, rows, storage)
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
    assert approved['stored_cases'] == TOTAL
    assert approved['fresh_viewed_pages'] + approved['reused_exact_viewed_pages'] == approved['portrait_pages'] == 45
    return dict(observed_notice_IDs=OBSERVED, stored_templates=TOTAL, portrait_pages=45,
        fresh_viewed_pages=approved['fresh_viewed_pages'], reused_exact_viewed_pages=approved['reused_exact_viewed_pages'],
        native_selector_cases=approved['native_selector_cases'], crew_voice_choices=approved['crew_voice_choices'],
        floating_name_expansions=approved['floating_expansion_cases'],
        fixture_scope='Two isolated voyages each use one temporary condition-selector instruction',
        floating_notices_with_original_earned_levels=2, original_becalmed_warning_and_dismissal=True,
        ordinary_reef_warning_observed=False, hardware=False)


def final_review(source, evidence, scope):
    stored = {row['message_ID']: row for row in evidence['stored']}
    records = []
    for row in source['records']:
        n = row['message_ID']
        assert row['review'] == dict(source=True, context=True, localization=True, naturalness=True, formatting=False)
        case = stored[n]
        assert row['source_reference'] == case['source_reference'] and row['current_reference'] == case['current_reference']
        portraits = [proof for proof in evidence['crew_cases'] if proof['message_ID'] == n]
        assert len(portraits) == (0 if n == 97 else 4 if row['original_substitutions'] else 1)
        records.append(row | dict(review=row['review'] | {'formatting': True},
            registered_reference=case['staged_reference'] | {'exact_stored_hex': case['staged_hex'],
                'ROM_sha256': evidence['research_ROM_sha256']},
            displayed_variants=[dict(arguments=proof['arguments'], display_hex=proof['native']['formatted_hex'],
                protected_phrases=proof.get('protected_phrases', []), ink_sha256=proof['native_ink_sha256'])
                for proof in portraits],
            native_floating_name_cases=scope['floating_name_expansions'] if n == 97 else None,
            gameplay_observed=n in OBSERVED, new_credit=1))
    assert Counter(r['decision'] for r in records) == {'revision': REVISED, 'retention': RETAINED}
    review = dict(translation_policy='natural-dialogue-v2', target_locale='en-US',
        encoder='dialogue-relocatable-v1', review_gates=source['review_gates'],
        records=records, actual_verification_scope=scope, full_goal_complete=False)
    validate_natural_dialogue_batch(review)
    return review


def publish(release):
    summary = 'The sailing alerts and floating level-up notice are registered across 28 records. The ledger now credits 26,111 reviews.'
    notes = f"""# All Routes sailing-alert candidate

Use `{ROM.as_posix()}` beside its build manifest. The [clean-input patch](translation.xdelta) applies to clean Japanese SHA-256 `{release['clean_input_sha256']}` and reconstructs candidate SHA-256 `{release['candidate_sha256']}` byte for byte. Patch SHA-256 is `{release['patch_sha256']}`.

The batch covers 28 records, with 24 revisions and four justified retentions. It restores 12 warnings that displayed unrelated text, translates the floating level-up notice, and improves 10 wraps. All 45 portrait pages, 207 floating name expansions, 72 cumulative release checks and 30 targeted tests passed. The build retains the Market Trade-screen fix and the ASCII right-bound correction. Main V4701 awaits acceptance.

One focused replay displayed Gerhard's and Manuel's level-up notices after normal level gains. Another displayed the revised becalmed warning and returned to sailing after A. Each used a temporary condition selector. The separate ordinary voyage missed the Reefs warning. The candidate passed its own 31,000-frame startup and 24 protected name getters. [Gameplay and coverage evidence](verification/sailing_alert_gameplay_verification.json) · [Registered review](verification/registered_review.json)
"""
    (PACKAGE / 'README.md').write_text(notes, encoding='utf-8', newline='\n')
    save(PACKAGE / 'checksums.json', {p.relative_to(PACKAGE).as_posix(): digest(p)
        for p in sorted(PACKAGE.rglob('*')) if p.is_file()})
    pins_path = Path('translations/rom_retention_pins.json')
    pins = load(pins_path)
    ordinary = load(ORDINARY)
    for path, expected, name in (
        (Path(ordinary['research_ROM']), ordinary['research_ROM_sha256'], 'first-pass sailing-alert ROM'),
        (RESEARCH, release['candidate_sha256'], 'balanced sailing-alert research ROM'),
        (ROM, release['candidate_sha256'], 'registered sailing-alert ROM'),
    ):
        assert digest(path) == expected and not any(row['path'] == str(path.resolve()) for row in pins)
        pins.append(dict(path=str(path.resolve()), reason=f'Preserve {name}. SHA256 {expected}'))
    replace_checked(pins_path, (json.dumps(pins, ensure_ascii=False, indent=2) + '\n').replace('\n', '\r\n').encode('utf-8'))
    doc = f"""# Sailing alerts registered

{summary} This cumulative candidate preserves the prior sea-event review, 114 accepted layers, the Market fix and the ASCII right-bound correction. [Release package](../{PACKAGE.as_posix()}/README.md) · [Exact registered record references](../{REVIEW.as_posix()})

The clean Japanese distinguishes the epidemic, a dead calm and sharks. Twelve current records displayed unrelated prose or fragments. The revisions restore those events and distinguish the crew's voices. Four retentions keep natural wording. Ten protected wraps keep complete phrases such as “Watch out!” together. The floating notice keeps the original actor name argument and uses “leveled up!”.

All 28 exact stored lookups, 45 complete portrait pages, 828 crew voice choices, 1,512 selector cases, 207 floating name expansions, 30 targeted tests, the 31,000-frame startup, and 24 protected name getters passed. The emulator displayed two complete floating notices and the revised becalmed warning. The condition selectors were temporary and the usual A dismissal and level calculations ran in game. The separate ordinary voyage missed Reefs. [Representative replay details](../{(VERIFICATION / LIVE_VERIFICATION.name).as_posix()})

Continue with the clean unrest and mutiny exchange at messages 508–572, including the native `IC` substitution, then the separate leaks and fire families. The unmapped Market replies, remaining town dialogue and other player-facing text stay in scope. Graphics artwork and the older-record technical re-audit stay separate.
"""
    replace_checked(DOC, doc.encode('utf-8'))
    lead = f'# Current editorial checkpoint - 2026-11-11\n\n{summary}\n\nContinue from [the registered sailing-alert checkpoint]({DOC.name}).\n\n'.encode('utf-8')
    for name in ('editorial_handoff_current.md', 'editorial_efficiency_workflow.md', 'translation_progress.md'):
        path = Path('docs') / name
        replace_checked(path, lead + path.read_bytes())
    print('Registered 737 entries and credited 28 sailing-alert reviews once.')


def register():
    manifest = load(load(PARENT)['manifest'])
    driver = manifest['shared_sea_events_registered_successor_pipeline']
    assert digest(previous.__file__) == driver['driver_sha256']
    env = {**vars(base), **globals(), 'preserve_compression': previous.preserve_compression}
    ledger = checked_text(inspect.getsource(base.update_ledger), {
        "'diplomatic-and-scheme-outcome-notices'": "'shared-sailing-alerts'",
        'Thirty-four diplomacy and scheme outcomes are registered.': 'Twenty-eight shared sailing alerts are registered.',
        '== 25985': '== 26111', '== 15438': '== 15519', '== 10547': '== 10592',
    })
    old_scope = """    scope = dict(observed_notice_IDs=approved['live_messages'], stored_cases=176, fresh_viewed_pages=31,
        reused_exact_viewed_pages=145, fixture_scope='One incoming letter in a previously empty isolated RAM slot',
        original_no_preserved_war=True, natural_letter_generation=False, hardware=False)"""
    registration = checked_text(inspect.getsource(base.register), {
        "approved['live_messages'] == [349, 356, 352]": "approved['live_messages'] == OBSERVED",
        "sum(int(s.get('tests', 0)) for s in tests) == 27": "sum(int(s.get('tests', 0)) for s in tests) == 30",
        "len(manifest['batches']) == 734 and len(manifest['checks']) == 69":
            "len(manifest['batches']) == 736 and len(manifest['checks']) == 71",
        old_scope: '    scope = verification_scope(approved)',
        'LIVE_VERIFICATION, STARTUP_VERIFICATION, QA):': 'LIVE_VERIFICATION, STARTUP_VERIFICATION, QA, ORDINARY):',
        'release_stack_before_diplomacy.json': 'release_stack_before_sailing_alerts.json',
        'verified_crew_notice_predecessor=predecessor, diplomatic_outcome_release=str(REVIEW)':
            'verified_sea_event_predecessor=predecessor, sailing_alert_release=str(REVIEW)',
        'Reviewed diplomacy and scheme outcomes with scoped native phrase wrapping.':
            'Reviewed sailing alerts and floating level-ups with scoped native phrase wrapping.',
        'release_stack.diplomacy.pending.json': 'release_stack.sailing_alerts.pending.json',
        "LEDGER.with_name('editorial_review_current.diplomacy.pending.json')": 'PENDING_LEDGER',
        '    save(pending_registry, registry)':
            '    preserve_compression(pending_registry, REGISTRY)\n    save(pending_registry, registry)',
        "evidence['wrapper']": "evidence['selector']",
        'COMMON_DIPLOMATIC_OUTCOMES_MODAL_AND_PHRASE_WRAP': 'COMMON_SAILING_ALERT_SCOPED_PHRASE_WRAP',
        "manifest['diplomatic_outcomes_registered_successor_pipeline']":
            "manifest['sailing_alerts_registered_successor_pipeline']",
        "len(manifest['batches']) == 735 and len(manifest['checks']) == 70":
            "len(manifest['batches']) == 737 and len(manifest['checks']) == 72",
        'registered_manifest_entries=735, accepted_layers=114, passing_release_checks=70, repository_tests=27':
            'registered_manifest_entries=737, accepted_layers=114, passing_release_checks=72, repository_tests=30',
        '    pending_registry.replace(REGISTRY)\n    try:\n        pending_ledger.replace(LEDGER)\n    except OSError:\n        replace_checked(REGISTRY, before_registry)\n        raise\n    assert digest(REGISTRY) == release[\'registry_sha256\'] and digest(PROMOTED) == promoted\n    publish(release)':
            '    assert digest(PROMOTED) == promoted\n    print(\'Sailing-alert registration staged and ready to publish.\')',
    })
    exec(compile(ledger + '\n\n' + registration, __file__ + '::sailing-alert-registration', 'exec'), env)
    env['register']()


def publish_prepared():
    env = {**vars(previous), **globals(), 'prior': base}
    env['verify_prepared'] = FunctionType(previous.verify_prepared.__code__, env)
    code = checked_text(inspect.getsource(previous.publish_prepared), {
        'release_stack.sea_events.pending.json': 'release_stack.sailing_alerts.pending.json',
    })
    exec(compile(code, __file__ + '::sailing-alert-publication', 'exec'), env)
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
