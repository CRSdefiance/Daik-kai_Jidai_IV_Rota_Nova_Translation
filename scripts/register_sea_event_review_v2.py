"""Register the native- and live-verified sea-event batch over diplomacy."""

import argparse
from collections import Counter
from hashlib import sha256
import inspect
import json
from pathlib import Path
import shutil
import stat
import subprocess
from types import FunctionType

from dk4tool.dialogue.review import validate_natural_dialogue_batch
from dk4tool.patch.sea_event_static_wrap_v1 import transform
from dk4tool.rom.nds import NdsImage
from dk4tool.script.common_message_table import DIRECTORY_OFFSET, TABLE_OFFSET
from scripts import register_diplomatic_outcomes_v2 as prior
from scripts.audit_story_glyph_consistency import load, save
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest
from scripts.package_ship_command_candidate_v1 import replace_checked
from scripts.review_sea_event_wrap_plan_v1 import PROOF as LAYOUT
from scripts.seal_shared_text_source_v1 import ARM, COMMON, reference
from scripts.source_locked_derivation_v5118 import checked_text
from scripts.stage_sea_event_balanced_wrap_v2 import EVIDENCE, OUTPUT, ROM as RESEARCH
from scripts.stage_shared_notices_storage_v1 import relocate
from scripts.verify_sea_event_bubbles_focused_v2 import PROOF as LIVE_VERIFICATION
from scripts.verify_sea_event_startup_v2 import BOOT as STARTUP_VERIFICATION, CHECKPOINT, OBSERVED


PARENT = prior.RELEASE
PROFILE = 'all-routes-sea-event-editorial-v2-20261110'
FAMILY = 'shared_sea_event_contextual_20261110'
CHECK = 'registered_shared_sea_event_native_live_phrase_and_complete_parent_inverse'
PACKAGE = Path('releases/all_routes_editorial_20261110_sea_events_candidate')
VERIFICATION = PACKAGE / 'verification'
RELEASE = VERIFICATION / 'registered_release_verification.json'
REVIEW = VERIFICATION / 'registered_review.json'
TEST = Path('out/sea_events_registered_20261110_v2')
ROM = TEST / 'Translation_DS_All_Routes_Sea_Events_20261110_candidate.nds'
MANIFEST = ROM.with_suffix('.manifest.json')
PATCH = PACKAGE / 'translation.xdelta'
DOC = Path('docs/editorial_sea_events_registered_20261110.md')
QA = Path('work/SharedText_20261110_v1/sea_event_wrap_plan_v1/repo_qa_sea_v1.xml')
ORDINARY = OUTPUT.with_name('sea_event_replay_scope.json')
PENDING_LEDGER = TEST / 'editorial_review_current.sea_events.pending.json'
MUTATION_PLAN = VERIFICATION / 'registration_mutation_plan.json'
TOTAL, REVISED, RETAINED = 98, 57, 41
PREVIOUS_TOTAL = 25985


def rebuild(parent, evidence, source):
    image = NdsImage.open(parent['candidate'])
    before_arm, before_common = image.read_file(ARM), image.read_file(COMMON)
    wrapped, selector = transform(before_arm)
    assert json.loads(json.dumps(selector)) == evidence['selector']
    directory = sha256(before_arm[DIRECTORY_OFFSET:TABLE_OFFSET]).hexdigest()
    repack = FunctionType(relocate.__code__, {**relocate.__globals__, 'DIRECTORY': directory})
    rows = {row['message_ID']: row for row in source['records']}
    cases = {row['message_ID']: row for row in evidence['cases']}
    assert cases.keys() == rows.keys() and len(cases) == TOTAL
    storage = {n: bytes.fromhex(case['staged_hex']) for n, case in cases.items()}
    assert all(b' '.join(raw.split()) == rows[n]['english'].encode('ascii') for n, raw in storage.items())
    common, arm, rebound, packing = repack(before_common, wrapped, rows, storage)
    assert json.loads(json.dumps(packing)) == evidence['storage']
    for n, case in cases.items():
        assert case['staged_reference'] == reference(rebound[n])
    image.replace_file(ARM, arm)
    image.replace_file(COMMON, common)
    assert bytes(image.rom.save()) == RESEARCH.read_bytes()
    image.replace_file(ARM, before_arm)
    image.replace_file(COMMON, before_common)
    assert bytes(image.rom.save()) == Path(parent['candidate']).read_bytes()
    return arm, common


def verification_scope(approved):
    assert approved['live_messages'] == OBSERVED
    assert approved['stored_cases'] == TOTAL
    assert approved['fresh_viewed_pages'] + approved['reused_exact_viewed_pages'] == TOTAL
    return dict(observed_notice_IDs=OBSERVED, stored_cases=TOTAL,
        fresh_viewed_pages=approved['fresh_viewed_pages'],
        reused_exact_viewed_pages=approved['reused_exact_viewed_pages'],
        native_selector_cases=approved['native_selector_cases'], crew_voice_choices=approved['crew_voice_choices'],
        fixture_scope='One temporary selector instruction in an isolated emulator voyage',
        original_bubbles_exchange_and_sailing_return=True, natural_random_selection=False, hardware=False)


def final_review(source, evidence, scope):
    cases = {row['message_ID']: row for row in evidence['cases']}
    layout = {row['message_ID']: row for row in load(LAYOUT)['records']}
    records = []
    for row in source['records']:
        n = row['message_ID']
        assert row['review'] == dict(source=True, context=True, localization=True, naturalness=True, formatting=False)
        case = cases[n]
        assert row['source_reference'] == case['source_reference'] and row['current_reference'] == case['current_reference']
        records.append(row | dict(review=row['review'] | {'formatting': True},
            registered_reference=case['staged_reference'] | {'exact_stored_hex': case['staged_hex'],
                'ROM_sha256': evidence['research_ROM_sha256']},
            native_display_hex=case['display_hex'], exact_viewed_ink_sha256=case['exact_viewed_ink_sha256'],
            protected_phrases=layout[n]['protected_phrases'] if n in layout else [],
            ordinary_boundary_rationale=evidence['ordinary_boundaries_retained'].get(str(n)),
            gameplay_observed=n in OBSERVED, new_credit=1))
    assert len(records) == TOTAL and Counter(r['decision'] for r in records) == {
        'revision': REVISED, 'retention': RETAINED}
    review = dict(translation_policy='natural-dialogue-v2', target_locale='en-US',
        encoder='dialogue-relocatable-v1', review_gates=source['review_gates'],
        records=records, actual_verification_scope=scope, full_goal_complete=False)
    validate_natural_dialogue_batch(review)
    return review


def preserve_compression(path, original):
    attributes = getattr(original.stat(), 'st_file_attributes', 0)
    if attributes & stat.FILE_ATTRIBUTE_COMPRESSED:
        if not path.exists():
            path.touch(exist_ok=False)
            subprocess.run(['compact.exe', '/C', '/Q', str(path)], check=True, capture_output=True)
        assert path.stat().st_file_attributes & stat.FILE_ATTRIBUTE_COMPRESSED


def verify_prepared():
    release = load(RELEASE)
    assert release['profile'] == PROFILE and release['clean_input_patch_byte_exact']
    assert release['candidate'] == str(ROM) and release['patch'] == str(PATCH)
    assert digest(ROM) == release['candidate_sha256'] == digest(RESEARCH)
    assert digest(PATCH) == release['patch_sha256']
    assert digest(prior.REGISTRY) == release['predecessor']['registry_sha256']
    assert not DOC.exists()
    return release


def publish_prepared():
    release = verify_prepared()
    plan = load(MUTATION_PLAN)
    registry, ledger = prior.REGISTRY, prior.LEDGER
    pending_registry = registry.with_name('release_stack.sea_events.pending.json')
    local_ledger = ledger.with_name(PENDING_LEDGER.name)
    assert digest(registry) == plan['registry_before']
    assert digest(ledger) == plan['ledger_before']
    assert digest(pending_registry) == plan['registry_after'] == release['registry_sha256']
    assert digest(PENDING_LEDGER) == plan['ledger_after']
    preserve_compression(local_ledger, ledger)
    with PENDING_LEDGER.open('rb') as source, local_ledger.open('wb') as target:
        shutil.copyfileobj(source, target, length=1024 * 1024)
    assert digest(local_ledger) == plan['ledger_after']
    before_registry, promoted = registry.read_bytes(), digest(prior.PROMOTED)
    assert sha256(before_registry).hexdigest() == plan['registry_before']
    assert digest(ledger) == plan['ledger_before']
    pending_registry.replace(registry)
    try:
        local_ledger.replace(ledger)
    except OSError:
        replace_checked(registry, before_registry)
        raise
    assert digest(registry) == plan['registry_after'] and digest(prior.PROMOTED) == promoted
    publish(release)


def publish(release):
    summary = 'The 98 shared sea-event messages are registered. The ledger now credits 26,083 reviews.'
    notes = f"""# Cumulative sea-event testing candidate

Use `{ROM.as_posix()}` beside its build manifest. The [clean-input patch](translation.xdelta) applies to clean Japanese SHA-256 `{release['clean_input_sha256']}` and reconstructs candidate SHA-256 `{release['candidate_sha256']}` byte for byte. Patch SHA-256 is `{release['patch_sha256']}`.

{summary} This batch includes 57 revisions, 41 justified retentions, 26 phrase-wrap refinements and ordinary ASCII glyphs in seven templates. All 98 stored displays, 71 cumulative release checks and 27 targeted tests pass. Main V4701 awaits acceptance.

The focused bubbles replay displayed five original pages, including Hodram's complete order, and returned to sailing. One temporary selector instruction provided the event input. Two separate ordinary voyages reached other events. The 31,000-frame startup and both protected getters for 12 actors pass. [Live verification](verification/sea_event_focused_bubbles_verification.json) · [Registered review](verification/registered_review.json)
"""
    (PACKAGE / 'README.md').write_text(notes, encoding='utf-8', newline='\n')
    save(PACKAGE / 'checksums.json', {p.relative_to(PACKAGE).as_posix(): digest(p)
        for p in sorted(PACKAGE.rglob('*')) if p.is_file()})
    pin_path = Path('translations/rom_retention_pins.json')
    pins = load(pin_path)
    assert any(row['path'] == str(RESEARCH.resolve()) for row in pins)
    assert not any(row['path'] == str(ROM.resolve()) for row in pins)
    pins.append(dict(path=str(ROM.resolve()), reason='Preserve registered sea-event ROM. SHA256 ' + release['candidate_sha256']))
    replace_checked(pin_path, (json.dumps(pins, ensure_ascii=False, indent=2) + '\n').replace('\n', '\r\n').encode('utf-8'))
    document = f"""# Shared sea-event dialogue registered

{summary} The build preserves the diplomacy release, 114 accepted layers, the Market Trade-screen correction and the ASCII right-bound fix. The cumulative patch reconstructs the exact build. [Release package](../{PACKAGE.as_posix()}/README.md) · [Final record references](../{REVIEW.as_posix()})

The stored checks cover the 16 original groups and all 98 pages. Twenty-six refined layouts preserve complete phrases, including the captain's order and a young sailor's plea about their food. The focused bubbles replay verified five live pages and a return to sailing. The ordinary voyages sampled other scenes. [Reviewed scenes and fixture scope](editorial_sea_events_stored_20261110.md)

Continue the remaining shared town, random and player-facing text, including the generic sailing condition reports and the floating level-up notice exposed by this replay. The unmapped Market replies remain in scope. Deferred artwork and the older-record technical re-audit remain separate.
"""
    replace_checked(DOC, document.encode('utf-8'))
    lead = f'# Current editorial checkpoint - 2026-11-10\n\n{summary}\n\nContinue from [the registered sea-event checkpoint]({DOC.name}).\n\n'.encode('utf-8')
    for name in ('editorial_handoff_current.md', 'editorial_efficiency_workflow.md', 'translation_progress.md'):
        path = Path('docs') / name
        replace_checked(path, lead + path.read_bytes())
    print('Registered 736 entries and credited 98 sea-event reviews once.')


def register(resume_prepared=False):
    if resume_prepared:
        verify_prepared()
    manifest = load(load(PARENT)['manifest'])
    previous_driver = manifest['diplomatic_outcomes_registered_successor_pipeline']
    assert digest(prior.__file__) == previous_driver['driver_sha256']
    # The previous transaction retains its original ancestry, inverse, patch,
    # backup and publication checks. Bind only this batch's different inputs.
    env = {**vars(prior), **globals(), 'resume_prepared': resume_prepared}
    ledger = checked_text(inspect.getsource(prior.update_ledger), {
        "'diplomatic-and-scheme-outcome-notices'": "'shared-sea-event-dialogue'",
        'Thirty-four diplomacy and scheme outcomes are registered.': 'Ninety-eight shared sea-event reviews are registered.',
        '== 25985': '== 26083', '== 15438': '== 15495', '== 10547': '== 10588',
    })
    scope = """    scope = dict(observed_notice_IDs=approved['live_messages'], stored_cases=176, fresh_viewed_pages=31,
        reused_exact_viewed_pages=145, fixture_scope='One incoming letter in a previously empty isolated RAM slot',
        original_no_preserved_war=True, natural_letter_generation=False, hardware=False)"""
    registration = checked_text(inspect.getsource(prior.register), {
        '    assert not any(path.exists() for path in (TEST, PACKAGE, DOC))':
            '    if not resume_prepared:\n        assert not any(path.exists() for path in (TEST, PACKAGE, DOC))',
        '    TEST.mkdir()\n    VERIFICATION.mkdir(parents=True)\n    make_xdelta(CLEAN, RESEARCH, PATCH)\n    apply_xdelta(CLEAN, PATCH, ROM)':
            '    if not resume_prepared:\n        TEST.mkdir()\n        VERIFICATION.mkdir(parents=True)\n        make_xdelta(CLEAN, RESEARCH, PATCH)\n        apply_xdelta(CLEAN, PATCH, ROM)',
        "approved['live_messages'] == [349, 356, 352]": "approved['live_messages'] == OBSERVED",
        "len(manifest['batches']) == 734 and len(manifest['checks']) == 69":
            "len(manifest['batches']) == 735 and len(manifest['checks']) == 70",
        scope: '    scope = verification_scope(approved)',
        'LIVE_VERIFICATION, STARTUP_VERIFICATION, QA):': 'LIVE_VERIFICATION, STARTUP_VERIFICATION, QA, LAYOUT, ORDINARY):',
        'release_stack_before_diplomacy.json': 'release_stack_before_sea_events.json',
        'verified_crew_notice_predecessor=predecessor, diplomatic_outcome_release=str(REVIEW)':
            'verified_diplomacy_predecessor=predecessor, shared_sea_event_release=str(REVIEW)',
        'Reviewed diplomacy and scheme outcomes with scoped native phrase wrapping.':
            'Reviewed shared sea events with verified voice selection and phrase wrapping.',
        'release_stack.diplomacy.pending.json': 'release_stack.sea_events.pending.json',
        "LEDGER.with_name('editorial_review_current.diplomacy.pending.json')": 'PENDING_LEDGER',
        '    assert not pending_registry.exists() and not pending_ledger.exists()':
            '    if not resume_prepared:\n        assert not pending_registry.exists() and not pending_ledger.exists()',
        '    save(pending_registry, registry)':
            '    preserve_compression(pending_registry, REGISTRY)\n    save(pending_registry, registry)',
        "evidence['wrapper']": "evidence['selector']",
        'COMMON_DIPLOMATIC_OUTCOMES_MODAL_AND_PHRASE_WRAP': 'COMMON_SEA_EVENT_SCOPED_PHRASE_WRAP',
        "manifest['diplomatic_outcomes_registered_successor_pipeline']":
            "manifest['shared_sea_events_registered_successor_pipeline']",
        "len(manifest['batches']) == 735 and len(manifest['checks']) == 70":
            "len(manifest['batches']) == 736 and len(manifest['checks']) == 71",
        'registered_manifest_entries=735, accepted_layers=114, passing_release_checks=70':
            'registered_manifest_entries=736, accepted_layers=114, passing_release_checks=71',
        '    pending_registry.replace(REGISTRY)\n    try:\n        pending_ledger.replace(LEDGER)\n    except OSError:\n        replace_checked(REGISTRY, before_registry)\n        raise\n    assert digest(REGISTRY) == release[\'registry_sha256\'] and digest(PROMOTED) == promoted\n    publish(release)':
            '    assert digest(PROMOTED) == promoted\n    print(\'Sea-event registration staged and ready to publish.\')',
    })
    exec(compile(ledger + '\n\n' + registration, __file__ + '::sea-event-registration', 'exec'), env)
    env['register']()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    action = parser.add_mutually_exclusive_group(required=True)
    action.add_argument('--register', action='store_true')
    action.add_argument('--publish-prepared', action='store_true')
    parser.add_argument('--resume-prepared', action='store_true')
    args = parser.parse_args()
    if args.publish_prepared:
        publish_prepared()
    else:
        register(args.resume_prepared)
