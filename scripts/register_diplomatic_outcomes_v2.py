"""Register the 34 reviewed diplomacy outcomes after storage and gameplay proof."""

import argparse
from collections import Counter
from copy import deepcopy
import gzip
from hashlib import sha256
import json
from pathlib import Path
import shutil
from types import FunctionType
import xml.etree.ElementTree as ET

from dk4tool.dialogue.review import validate_natural_dialogue_batch
from dk4tool.patch.diplomatic_outcome_wrap_v2 import transform
from dk4tool.patch.xdelta import apply_xdelta, make_xdelta
from dk4tool.rom.nds import NdsImage
from dk4tool.script.common_message_table import DIRECTORY_OFFSET, TABLE_OFFSET
from scripts.audit_story_glyph_consistency import load, save
from scripts.checkpoint_diplomatic_outcomes_v1 import OUTPUT
from scripts.editorial_ledger_storage_v1 import encode_ledger
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest
from scripts.package_ship_command_candidate_v1 import replace_checked
from scripts.refine_diplomatic_outcomes_layout_v2 import EVIDENCE, ROM as RESEARCH
from scripts.register_shared_crew_notices_v1 import RELEASE as PARENT
from scripts.register_shared_notices_v1 import CONTEXT, LEDGER, PROMOTED, REGISTRY
from scripts.seal_shared_text_source_v1 import ARM, CLEAN, COMMON, reference
from scripts.stage_shared_notices_storage_v1 import relocate
from scripts.verify_diplomatic_outcome_live_v2 import CHECKPOINT, LIVE_VERIFICATION, STARTUP_VERIFICATION


PROFILE = 'all-routes-diplomatic-outcomes-v2-20261110'
FAMILY = 'diplomatic_and_scheme_outcomes_contextual_20261110'
CHECK = 'registered_diplomatic_outcomes_native_live_phrase_and_complete_parent_inverse'
PACKAGE = Path('releases/all_routes_editorial_20261110_diplomatic_outcomes_candidate')
VERIFICATION = PACKAGE / 'verification'
RELEASE = VERIFICATION / 'registered_release_verification.json'
REVIEW = VERIFICATION / 'registered_review.json'
TEST = Path('out/diplomatic_outcomes_registered_20261110_v2')
ROM = TEST / 'Translation_DS_All_Routes_Diplomacy_20261110_candidate.nds'
MANIFEST = ROM.with_suffix('.manifest.json')
PATCH = PACKAGE / 'translation.xdelta'
DOC = Path('docs/editorial_diplomatic_outcomes_registered_20261110.md')
QA = Path('work/SharedText_20261110_v1/diplomatic_outcomes_wrap_v1/repo_qa_phrase_v2.xml')
TOTAL, REVISED, RETAINED = 34, 17, 17
PREVIOUS_TOTAL = 25951


def rebuild(parent, evidence, source):
    image = NdsImage.open(parent['candidate'])
    before_arm, before_common = image.read_file(ARM), image.read_file(COMMON)
    wrapped, owner = transform(before_arm)
    assert json.loads(json.dumps(owner)) == evidence['wrapper']
    directory = sha256(before_arm[DIRECTORY_OFFSET:TABLE_OFFSET]).hexdigest()
    repack = FunctionType(relocate.__code__, {**relocate.__globals__, 'DIRECTORY': directory})
    rows = {row['message_ID']: row for row in source['records']}
    stored = {n: row['english'].encode('ascii') for n, row in rows.items()}
    common, arm, rebound, packing = repack(before_common, wrapped, rows, stored)
    assert json.loads(json.dumps(packing)) == evidence['storage']
    for item in evidence['records']:
        n = item['message_ID']
        assert item['staged'] == reference(rebound[n]) and item['staged_hex'] == stored[n].hex()
    image.replace_file(ARM, arm)
    image.replace_file(COMMON, common)
    assert bytes(image.rom.save()) == RESEARCH.read_bytes()
    image.replace_file(ARM, before_arm)
    image.replace_file(COMMON, before_common)
    assert bytes(image.rom.save()) == Path(parent['candidate']).read_bytes()
    return arm, common


def final_review(source, evidence, scope):
    references = {row['message_ID']: row for row in evidence['records']}
    records = []
    for row in source['records']:
        n = row['message_ID']
        assert row['review'] == dict(source=True, context=True, localization=True, naturalness=True, formatting=False)
        ref = references[n]
        assert row['source_reference'] == ref['source'] and row['current_reference'] == ref['previous']
        result = {k: v for k, v in row.items() if k != 'native_current_wrapper_expansions'}
        records.append(result | dict(review=row['review'] | {'formatting': True},
            registered_reference=ref['staged'] | {'exact_stored_hex': ref['staged_hex'],
                'ROM_sha256': evidence['research_ROM_sha256']},
            closing_phrase=evidence['wrapper']['closing_phrases'].get(str(n)),
            gameplay_observed=n in scope['observed_notice_IDs'], new_credit=1))
    assert len(records) == TOTAL and Counter(r['decision'] for r in records) == {
        'revision': REVISED, 'retention': RETAINED}
    review = dict(translation_policy='natural-dialogue-v2', target_locale='en-US',
        encoder='dialogue-relocatable-v1', review_gates=source['review_gates'],
        records=records, actual_verification_scope=scope, full_goal_complete=False)
    validate_natural_dialogue_batch(review)
    return review


def update_ledger(ledger, records, release, scope):
    ctx = ledger[CONTEXT]
    keys = [dict(file_path=row['file_path'], id=row['id']) for row in records]
    assert len({(row['file_path'], row['id']) for row in keys}) == len(keys) == TOTAL
    assert FAMILY not in ledger and not any(row['id'] == FAMILY for row in ledger['coverage_units'])
    for field in ('record_keys', 'integrated_record_keys'):
        assert len(ctx[field]) == PREVIOUS_TOTAL and all(key not in ctx[field] for key in keys)
        ctx[field].extend(keys)
    ctx['record_IDs'].extend(row['id'] for row in records)
    for field in ('fresh_pass_records_explicitly_reread', 'fresh_pass_records_integrated'):
        ctx[field] += TOTAL
    ctx.update(latest_completed_family=FAMILY, latest_final_review=str(REVIEW))
    ctx['reconciled_families'].append(dict(id=FAMILY, records=TOTAL, final_review=str(REVIEW),
        new_revisions=REVISED, justified_retentions=RETAINED, new_completed_records=TOTAL,
        historical_reconciliation_only=False, actual_verification_scope=scope))
    family = dict(id=FAMILY, kind='diplomatic-and-scheme-outcome-notices', records=TOTAL,
        record_keys=keys, final_review=str(REVIEW), final_review_sha256=digest(REVIEW),
        revised_count=REVISED, retained_count=RETAINED, fresh_revisions=REVISED,
        fresh_retentions=RETAINED, actual_verification_scope=scope, integrated_record_bindings=str(REVIEW))
    ledger['completed_editorial_families'].append(family)
    ledger['coverage_units'].append(family | dict(status='complete-contextual-native-stored-representative-registered-release',
        completion_credit_added=TOTAL, release_verification=str(RELEASE),
        release_verification_sha256=digest(RELEASE), full_goal_complete=False))
    for field in ('records_editorially_completed', 'records_with_source_and_prose_pass', 'records_with_source_prose_drafts'):
        ledger[field] += TOTAL
    ledger['records_revised_and_integrated'] += REVISED
    ledger['retained_wordings_editorially_completed'] += RETAINED
    ledger['current_integrated_candidate'].update(path=str(ROM), sha256=release['candidate_sha256'], profile=PROFILE,
        MESFILE_sha256=release['target_COMMON_sha256'], ARM9_sha256=release['target_ARM9_sha256'],
        patch=str(PATCH), patch_sha256=release['patch_sha256'], manifest=str(MANIFEST),
        manifest_sha256=release['manifest_sha256'], registered_release_verification=str(RELEASE))
    ledger[FAMILY] = dict(new_credit=TOTAL, final_review=str(REVIEW), release_verification=str(RELEASE),
        actual_verification=str(VERIFICATION / LIVE_VERIFICATION.name), registered_integration_pending=False)
    ledger['latest_checkpoint'] = 'Thirty-four diplomacy and scheme outcomes are registered.'
    assert len(ctx['integrated_record_keys']) == ledger['records_editorially_completed'] == 25985
    assert ledger['records_revised_and_integrated'] == 15438 and ledger['retained_wordings_editorially_completed'] == 10547


def register():
    assert not any(path.exists() for path in (TEST, PACKAGE, DOC))
    parent, evidence, approved, source, startup, live = map(load, (
        PARENT, EVIDENCE, CHECKPOINT, OUTPUT, STARTUP_VERIFICATION, LIVE_VERIFICATION))
    sha = digest(RESEARCH)
    assert sha == evidence['research_ROM_sha256'] == approved['candidate_sha256'] == startup['candidate_sha256'] == live['candidate_sha256']
    assert approved['approved_for_registered_successor'] and approved['live_messages'] == [349, 356, 352]
    assert all(digest(path) == expected for path, expected in approved['evidence'].items())
    assert len(startup['original_protected_name_getters']) == 24 and startup['frames'] == 31000
    tests = list(ET.parse(QA).getroot().iter('testsuite'))
    assert sum(int(s.get('tests', 0)) for s in tests) == 27
    assert not any(int(s.get(k, 0)) for s in tests for k in ('errors', 'failures', 'skipped'))
    assert digest(REGISTRY) == parent['registry_sha256'] and digest(CLEAN) == parent['clean_input_sha256']
    assert digest(parent['candidate']) == parent['candidate_sha256'] == evidence['registered_input']['candidate_sha256']
    assert digest(parent['manifest']) == parent['manifest_sha256']
    registry, ledger, manifest = load(REGISTRY), load(LEDGER), load(parent['manifest'])
    assert len(manifest['batches']) == 734 and len(manifest['checks']) == 69 and all(manifest['checks'].values())
    assert len(registry['accepted_layers']) == 114 and PROFILE not in registry['profiles']
    assert ledger['records_editorially_completed'] == PREVIOUS_TOTAL and not ledger['full_goal_complete']
    assert ledger['current_integrated_candidate']['sha256'] == parent['candidate_sha256']
    before_registry, before_ledger, promoted = REGISTRY.read_bytes(), LEDGER.read_bytes(), digest(PROMOTED)
    arm, common = rebuild(parent, evidence, source)
    assert sha256(arm).hexdigest() == evidence['target_ARM9_sha256']
    assert sha256(common).hexdigest() == evidence['target_COMMON_sha256']
    scope = dict(observed_notice_IDs=approved['live_messages'], stored_cases=176, fresh_viewed_pages=31,
        reused_exact_viewed_pages=145, fixture_scope='One incoming letter in a previously empty isolated RAM slot',
        original_no_preserved_war=True, natural_letter_generation=False, hardware=False)
    review = final_review(source, evidence, scope)
    TEST.mkdir()
    VERIFICATION.mkdir(parents=True)
    make_xdelta(CLEAN, RESEARCH, PATCH)
    apply_xdelta(CLEAN, PATCH, ROM)
    assert digest(ROM) == sha and ROM.read_bytes() == RESEARCH.read_bytes()
    save(REVIEW, review)
    for path in (EVIDENCE, CHECKPOINT, LIVE_VERIFICATION, STARTUP_VERIFICATION, QA):
        shutil.copyfile(path, VERIFICATION / path.name)
        assert digest(path) == digest(VERIFICATION / path.name)
    previous = TEST / 'release_stack_before_diplomacy.json'
    previous.write_bytes(before_registry)
    predecessor = {k: parent[k] for k in ('profile', 'candidate', 'candidate_sha256', 'manifest', 'manifest_sha256', 'registry_sha256')}
    predecessor['registry'] = str(previous)
    profile = deepcopy(registry['profiles'][parent['profile']])
    profile.update(verified_crew_notice_predecessor=predecessor, diplomatic_outcome_release=str(REVIEW),
        note='Reviewed diplomacy and scheme outcomes with scoped native phrase wrapping.')
    assert profile['ascii_glyph_right_bounds'] == parent['right_bound_configuration']
    assert profile['market_goods_info_terminator'] == registry['profiles'][parent['profile']]['market_goods_info_terminator']
    registry['profiles'][PROFILE] = profile
    pending_registry = REGISTRY.with_name('release_stack.diplomacy.pending.json')
    pending_ledger = LEDGER.with_name('editorial_review_current.diplomacy.pending.json')
    assert not pending_registry.exists() and not pending_ledger.exists()
    save(pending_registry, registry)
    manifest.update(profile=PROFILE, candidate_rom=str(ROM), candidate_sha256=sha,
        release_stack_sha256=digest(pending_registry))
    manifest['batches'].append(str(REVIEW))
    manifest['checks'][CHECK] = True
    manifest['relocations'][ARM][FAMILY] = evidence['wrapper']
    manifest['relocations'][COMMON][FAMILY] = evidence['storage']
    for path, ids in ((ARM, ('COMMON_DIPLOMATIC_OUTCOMES_MODAL_AND_PHRASE_WRAP',)),
                      (COMMON, [f'COMMON_MESSAGE_{n}' for n in evidence['storage']['changed_visible_templates']])):
        manifest['changed_records'][path].extend(n for n in ids if n not in manifest['changed_records'][path])
    manifest['diplomatic_outcomes_registered_successor_pipeline'] = dict(predecessor=predecessor,
        driver=str(Path(__file__)), driver_sha256=digest(__file__), review=str(REVIEW), review_sha256=digest(REVIEW),
        exact_rebuild_and_reconstruction=True, scope=scope)
    assert len(manifest['batches']) == 735 and len(manifest['checks']) == 70
    save(MANIFEST, manifest)
    own_startup = VERIFICATION / STARTUP_VERIFICATION.name
    release = dict(profile=PROFILE, candidate=str(ROM), candidate_sha256=sha, patch=str(PATCH),
        patch_sha256=digest(PATCH), clean_input_sha256=parent['clean_input_sha256'],
        clean_input_patch_byte_exact=True, manifest=str(MANIFEST), manifest_sha256=digest(MANIFEST),
        registry_sha256=digest(pending_registry), target_ARM9_sha256=sha256(arm).hexdigest(),
        target_COMMON_sha256=sha256(common).hexdigest(), predecessor=predecessor,
        canonical_base=parent['canonical_base'], canonical_sha256=parent['canonical_sha256'],
        registered_manifest_entries=735, accepted_layers=114, passing_release_checks=70, repository_tests=27,
        whole_parent_inverse_exact=True, experimental_not_promoted=True, own_registered_startup_pending=False,
        own_registered_startup=str(own_startup), own_registered_startup_sha256=digest(own_startup),
        original_protected_name_getters_count=24, right_bound_configuration=profile['ascii_glyph_right_bounds'],
        registered_market_format_andboth_data_pointers_preserved=True, actual_verification_scope=scope,
        changed_components=[ARM], changed_internal_files=[COMMON], new_contextual_records=TOTAL,
        prose_revisions=REVISED, justified_retentions=RETAINED, full_goal_complete=False)
    save(RELEASE, release)
    save(PACKAGE / 'release_manifest.json', release | {'user_acceptance_pending': True})
    for path, target in ((MANIFEST, PACKAGE / 'build_manifest.json.gz'),
                         (pending_registry, PACKAGE / 'build_release_stack.json.gz'),
                         (LEDGER, TEST / 'editorial_ledger_before.json.gz')):
        raw = path.read_bytes()
        target.write_bytes(gzip.compress(raw, compresslevel=1, mtime=0))
        assert gzip.decompress(target.read_bytes()) == raw
    update_ledger(ledger, review['records'], release, scope)
    pending_ledger.write_bytes(encode_ledger(ledger))
    save(VERIFICATION / 'registration_mutation_plan.json', dict(registry_before=sha256(before_registry).hexdigest(),
        registry_after=digest(pending_registry), ledger_before=sha256(before_ledger).hexdigest(),
        ledger_after=digest(pending_ledger)))
    old = json.loads(before_registry)
    assert {k: v for k, v in registry['profiles'].items() if k != PROFILE} == old['profiles']
    assert {k: v for k, v in registry.items() if k != 'profiles'} == {k: v for k, v in old.items() if k != 'profiles'}
    assert REGISTRY.read_bytes() == before_registry and LEDGER.read_bytes() == before_ledger
    pending_registry.replace(REGISTRY)
    try:
        pending_ledger.replace(LEDGER)
    except OSError:
        replace_checked(REGISTRY, before_registry)
        raise
    assert digest(REGISTRY) == release['registry_sha256'] and digest(PROMOTED) == promoted
    publish(release)


def publish(release):
    title = 'Diplomacy and scheme outcomes registered'
    summary = 'The 34 diplomacy and scheme notices are registered. The ledger now credits 25,985 reviews.'
    notes = f"""# Cumulative diplomacy and scheme notices

Use the local ROM `{ROM.as_posix()}` beside its build manifest. The [clean-input patch](translation.xdelta) applies to clean Japanese SHA-256 `{release['clean_input_sha256']}` and reconstructs candidate SHA-256 `{release['candidate_sha256']}` byte for byte. Patch SHA-256 is `{release['patch_sha256']}`.

{summary} The batch includes 17 prose revisions, 17 justified retentions, an ASCII glyph correction, and improved phrase wrapping. There are 735 entries, 114 accepted layers, 70 release checks and 27 passing repository tests. Main V4701 awaits user acceptance.

The isolated Istanbul emulator replay presented the incoming letter, the Yes/No truce choice, and the refusal. Choosing No preserved the existing war and returned to the inn menu. The replay seeded one incoming letter and left the original world and UI logic in control. Ordinary generation of the letter and hardware testing remain unvisited. [Live verification](verification/live_verification.json) · [Registered review](verification/registered_review.json)
"""
    (PACKAGE / 'README.md').write_text(notes, encoding='utf-8', newline='\n')
    save(PACKAGE / 'checksums.json', {p.relative_to(PACKAGE).as_posix(): digest(p)
        for p in sorted(PACKAGE.rglob('*')) if p.is_file()})
    pin_path = Path('translations/rom_retention_pins.json')
    pins = load(pin_path)
    for artifact in (ROM, RESEARCH):
        path = str(artifact.resolve())
        assert not any(row['path'] == path for row in pins)
        pins.append(dict(path=path, reason='Preserve exact diplomacy outcome ROM. SHA256 ' + release['candidate_sha256']))
    replace_checked(pin_path, (json.dumps(pins, ensure_ascii=False, indent=2) + '\n').replace('\n', '\r\n').encode('utf-8'))
    document = f"""# {title}

{summary} The native formatter keeps eight closing phrases together. All 176 stored samples pass, including 31 newly viewed pages and 145 exact reused visual results. The original letter notice, truce question and refusal match the complete emulator glyph masks. The 31,000-frame Maria cold boot and 24 protected name getters pass. [Release package](../{PACKAGE.as_posix()}/README.md) · [Final record references](../{REVIEW.as_posix()})

Continue shared town, random and player-facing prose. The pending Market replies, deferred artwork and older-record technical re-audit remain separate. Keep the registered Market and ASCII right-bound fixes in successors.
"""
    replace_checked(DOC, document.encode('utf-8'))
    lead = f'# Current editorial checkpoint - 2026-11-10\n\n{summary}\n\nContinue from [the registered diplomacy checkpoint]({DOC.name}).\n\n'.encode('utf-8')
    for name in ('editorial_handoff_current.md', 'editorial_efficiency_workflow.md', 'translation_progress.md'):
        path = Path('docs') / name
        replace_checked(path, lead + path.read_bytes())
    print('Registered 735 entries and credited 34 diplomacy reviews once.')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--register', action='store_true', required=True)
    parser.parse_args()
    register()
