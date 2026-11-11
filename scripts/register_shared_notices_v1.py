"""Register the live-verified 30-notice cumulative successor and its clean-input patch."""

import argparse
import gzip
import json
import shutil
import xml.etree.ElementTree as ET
from collections import Counter
from copy import deepcopy
from hashlib import sha256
from pathlib import Path

from dk4tool.dialogue.review import validate_natural_dialogue_batch
from dk4tool.patch.shared_notice_wrap_v1 import transform
from dk4tool.patch.xdelta import apply_xdelta, make_xdelta
from dk4tool.rom.nds import NdsImage
from scripts.audit_story_glyph_consistency import load, save
from scripts.checkpoint_shared_notice_storage_v1 import DEST
from scripts.editorial_ledger_storage_v1 import encode_ledger
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest
from scripts.package_ship_command_candidate_v1 import replace_checked
from scripts.register_ship_command_release_v1 import CONTEXT, LEDGER, PROMOTED
from scripts.review_literal_notice_callers_v1 import OUTPUT
from scripts.stage_shared_notices_storage_v1 import ARM, COMMON, ROOT, relocate
from scripts.stage_ship_command_release_v1 import CLEAN, REGISTRY, RELEASE as PARENT
from scripts.verify_shared_notice_boom_v1 import TARGET as BOOM
from scripts.verify_shared_notice_faction_bound_v1 import OUT as BOUND_DIR


PROFILE = 'all-routes-shared-notices-v1-20261110'
FAMILY = 'shared_status_notices_contextual_20261110'
CHECK = 'registered_shared_notices_native_live_and_complete_parent_inverse'
TEST = Path('out/promotion_ready_20261110_shared_notices_v1')
CANDIDATE = TEST / 'Translation_DS_All_Routes_Shared_Notices_20261110_candidate.nds'
MANIFEST = CANDIDATE.with_suffix('.manifest.json')
PACKAGE = Path('releases/all_routes_editorial_20261110_shared_notices_candidate')
PATCH = PACKAGE / 'translation.xdelta'
EVIDENCE = PACKAGE / 'verification'
RELEASE = EVIDENCE / 'registered_release_verification.json'
REVIEW = DEST / 'registered_review.json'
DOC = Path('docs/editorial_shared_notices_registered_20261110.md')
STAGED = ROOT / 'stored_verification.json'
QA = ROOT / 'registration_qa_v2.xml'


def rebuild(parent, staged, source_rows, rows):
    image = NdsImage.open(parent)
    source_arm, source_common = image.read_file(ARM), image.read_file(COMMON)
    arm, wrapper = transform(source_arm)
    storage = {r['message_ID']: bytes.fromhex(r['target_hex']) for r in rows}
    common, arm, _, proof = relocate(source_common, arm, source_rows, storage)
    assert wrapper == staged['runtime_wrapper']
    rebuilt, recorded = json.loads(json.dumps(proof)), dict(staged['storage'])
    for storage_proof in (rebuilt, recorded):
        storage_proof['changed_visible_templates'] = sorted(storage_proof['changed_visible_templates'])
    assert rebuilt == recorded
    assert proof['all_unselected_native_copy_spans_exact'] and proof['all_41_blocks_fit_8KiB']
    image.replace_file(ARM, arm)
    image.replace_file(COMMON, common)
    data = bytes(image.rom.save())
    assert data == Path(staged['target']).read_bytes()
    image.replace_file(ARM, source_arm)
    image.replace_file(COMMON, source_common)
    assert bytes(image.rom.save()) == Path(parent).read_bytes()
    return arm, common


def finalize_rows(rows, source, sha):
    finished = []
    for row in rows:
        n = row['message_ID']
        old = source[n]
        assert row['native_storage_and_display_checks_passed'] and set(row['review'].values()) == {True, False}
        assert row['review'] == dict(source=True, context=True, localization=True, naturalness=True, formatting=False)
        meaning = ('The original requirement check reports that the named skill is insufficient.'
                   if n == 87 else old['source_meaning'])
        finished.append({**row, 'source_meaning': meaning, 'speaker': old['speaker'],
            'context': old['context'], 'localization_note': row['rationale'],
            'manual_break_reason': old['manual_break_reason'],
            'registered_reference': dict(**row['target'], ROM_sha256=sha, exact_stored_hex=row['target_hex']),
            'native_substitution_count': old['native_substitution_count'],
            'observed_in_gameplay': n in (85, 86, 126),
            'review': {**row['review'], 'formatting': True}, 'new_credit': 1})
    batch = dict(format='dk4-reviewed-shared-status-notices-v1', target_locale='en-US',
        translation_policy='natural-dialogue-v2', encoder='dialogue-relocatable-v1',
        review_gates=['source', 'context', 'localization', 'naturalness', 'formatting'],
        records=finished, ROM_sha256=sha, full_goal_complete=False)
    validate_natural_dialogue_batch(batch)
    return batch


def update_ledger(prior, finished, released, scope):
    rows = finished['records']
    keys = [{k: r[k] for k in ('file_path', 'id')} for r in rows]
    selected = {(r['file_path'], r['id']) for r in keys}
    assert len(selected) == len(rows) == 30
    assert FAMILY not in prior and not any(row['id'] == FAMILY for row in prior['coverage_units'])
    context = deepcopy(prior[CONTEXT])
    for name in ('record_keys', 'integrated_record_keys'):
        assert len(context[name]) == 25899
        assert selected.isdisjoint((r['file_path'], r['id']) for r in context[name])
        context[name].extend(keys)
    context['record_IDs'].extend(r['id'] for r in rows)
    for name in ('fresh_pass_records_explicitly_reread', 'fresh_pass_records_integrated'):
        context[name] += len(rows)
    context.update(latest_completed_family=FAMILY, latest_final_review=str(REVIEW))
    context['reconciled_families'].append(dict(id=FAMILY, records=30, final_review=str(REVIEW),
        new_revisions=11, justified_retentions=19, new_completed_records=30,
        historical_reconciliation_only=False, actual_verification_scope=scope))
    prior[CONTEXT] = context
    family = dict(id=FAMILY, kind='shared-system-notices', records=30, record_keys=keys,
        final_review=str(REVIEW), final_review_sha256=digest(REVIEW), revised_count=11, retained_count=19,
        fresh_revisions=11, fresh_retentions=19, actual_verification_scope=scope,
        integrated_record_bindings=str(REVIEW))
    prior['completed_editorial_families'].append(family)
    prior['coverage_units'].append(dict(**family, status='complete-contextual-native-stored-representative-registered-release',
        completion_credit_added=30, release_verification=str(RELEASE), release_verification_sha256=digest(RELEASE),
        full_goal_complete=False))
    for name in ('records_editorially_completed', 'records_with_source_and_prose_pass', 'records_with_source_prose_drafts'):
        prior[name] += 30
    prior['records_revised_and_integrated'] += 11
    prior['retained_wordings_editorially_completed'] += 19
    prior['current_integrated_candidate'].update(path=str(CANDIDATE), sha256=released['candidate_sha256'],
        profile=PROFILE, MESFILE_sha256=released['target_COMMON_sha256'], ARM9_sha256=released['target_ARM9_sha256'],
        patch=str(PATCH), patch_sha256=released['patch_sha256'], manifest=str(MANIFEST),
        manifest_sha256=released['manifest_sha256'], registered_release_verification=str(RELEASE))
    prior[FAMILY] = dict(new_credit=30, final_review=str(REVIEW), release_verification=str(RELEASE),
        actual_verification=str(EVIDENCE / BOOM.name), registered_integration_pending=False)
    prior['latest_checkpoint'] = 'Thirty shared notices are registered. Copenhagen departure and boom transitions pass.'
    assert len(context['integrated_record_keys']) == prior['records_editorially_completed'] == 25929
    assert prior['records_revised_and_integrated'] == 15413 and prior['retained_wordings_editorially_completed'] == 10516
    assert not prior['full_goal_complete']
    return prior


def register():
    assert not any(p.exists() for p in (TEST, PACKAGE, REVIEW, DOC))
    parent, staged, checkpoint, boom, bound = map(load, (
        PARENT, STAGED, DEST / 'checkpoint.json', BOOM, BOUND_DIR / 'verification.json'))
    sha = staged['target_sha256']
    assert checkpoint['research_ROM_sha256'] == boom['candidate_sha256'] == bound['candidate_sha256'] == sha
    assert len(checkpoint['startup']['original_protected_name_getters']) == 24
    assert len(checkpoint['startup']['exact_matching_Maria_frames']) == 6
    assert [r['message_ID'] for r in checkpoint['observed_gameplay']['observed']] == [85, 86]
    assert boom['three_complete_rows_and_blank_margins_exact'] and boom['live_ITCM_selector_and_both_prior_literals_exact']
    assert boom['B_dismissed_dock_prompt_and_A_dismissed_notice_to_normal_sailing']
    assert bound['valid_18_byte_examples_fit_three_rows'] and bound['synthetic_23_byte_name_exceeds_source_editor_limit']
    assert len(bound['native_complete_pages']) == 12
    assert digest(bound['contact_sheet']) == bound['contact_sheet_sha256']
    assert len(staged['stored_cases']) == 59 and len(staged['direct_lookup_cases']) == 1
    assert Counter(r['decision'] for r in checkpoint['records']) == {'revision': 11, 'retention': 19}
    assert digest(REGISTRY) == parent['registry_sha256'] and digest(CLEAN) == parent['clean_input_sha256']
    assert digest(parent['manifest']) == parent['manifest_sha256']
    assert digest(parent['candidate']) == parent['candidate_sha256'] == staged['registered_input']['candidate_sha256']
    assert digest(staged['target']) == sha
    for path in (DEST / 'checkpoint.json', BOOM, BOUND_DIR / 'verification.json'):
        assert path.is_file()
    for archive, entry in checkpoint['exact_proof_archives'].items():
        assert digest(DEST / archive) == entry['archive_sha256']
        assert digest(entry['original']) == entry['original_sha256']
        assert gzip.decompress((DEST / archive).read_bytes()) == Path(entry['original']).read_bytes()

    report = ET.parse(QA).getroot()
    suites = list(report.iter('testsuite'))
    tests = sum(int(s.get('tests', '0')) for s in suites)
    assert tests == 27 and not any(int(s.get(key, '0')) for s in suites for key in ('errors', 'failures', 'skipped'))
    old, registry, ledger = map(load, (Path(parent['manifest']), REGISTRY, LEDGER))
    assert len(old['batches']) == 732 and len(old['checks']) == 67 and all(old['checks'].values())
    assert len(registry['accepted_layers']) == 114 and PROFILE not in registry['profiles']
    assert ledger['current_integrated_candidate']['sha256'] == parent['candidate_sha256']
    assert ledger['records_editorially_completed'] == 25899
    promoted = digest(PROMOTED)
    original_registry = REGISTRY.read_bytes()
    original_ledger = LEDGER.read_bytes()
    source_rows = {r['message_ID']: r for r in load(OUTPUT)['records']}
    arm, common = rebuild(parent['candidate'], staged, source_rows, checkpoint['records'])
    final = finalize_rows(checkpoint['records'], source_rows, sha)

    TEST.mkdir()
    EVIDENCE.mkdir(parents=True)
    prior_registry = TEST / 'release_stack_before_shared_notices.json'
    prior_registry.write_bytes(original_registry)
    predecessor = dict(profile=parent['profile'], candidate=parent['candidate'], candidate_sha256=parent['candidate_sha256'],
        manifest=parent['manifest'], manifest_sha256=parent['manifest_sha256'],
        registry=str(prior_registry), registry_sha256=parent['registry_sha256'])
    make_xdelta(CLEAN, Path(staged['target']), PATCH)
    apply_xdelta(CLEAN, PATCH, CANDIDATE)
    assert digest(CANDIDATE) == sha and CANDIDATE.read_bytes() == Path(staged['target']).read_bytes()
    target = NdsImage.open(CANDIDATE)
    assert target.read_file(ARM) == arm and target.read_file(COMMON) == common
    scope = dict(actual_notice_IDs=[85, 86, 126], offline_stored_cases=59, offline_direct_lookup_cases=1,
        verified_stock_editor_name_bytes=18, source_caller_state_fixture_ID=126,
        fixture_earned_investment=False, full_hardware_testing=False, remaining_individual_branches_offline=True)
    save(REVIEW, {**final, 'actual_verification_scope': scope})
    for source, name in ((BOOM, BOOM.name), (BOUND_DIR / 'verification.json', 'faction_name_bound_verification.json'),
                         (DEST / 'checkpoint.json', 'stored_and_departure_checkpoint.json'), (QA, QA.name),
                         (ROOT / 'registration_qa_v1.xml', 'legacy_supplemental_test_attempt.xml')):
        shutil.copyfile(source, EVIDENCE / name)
        assert digest(source) == digest(EVIDENCE / name)
    profile = deepcopy(registry['profiles'][parent['profile']])
    assert profile['ascii_glyph_right_bounds'] == parent['right_bound_configuration']
    profile.update(verified_ship_command_predecessor=predecessor, shared_notice_release=str(REVIEW),
        note='Cumulative shared status notices with original consumer wrapping and modal transitions.')
    registry['profiles'][PROFILE] = profile
    pending_registry = REGISTRY.with_name('release_stack.shared_notices.pending.json')
    pending_ledger = LEDGER.with_name('editorial_review_current.shared_notices.pending.json')
    assert not pending_registry.exists() and not pending_ledger.exists()
    save(pending_registry, registry)
    manifest = deepcopy(old)
    manifest.update(profile=PROFILE, candidate_rom=str(CANDIDATE), candidate_sha256=sha,
        release_stack_sha256=digest(pending_registry))
    manifest['batches'].append(str(REVIEW))
    manifest['checks'][CHECK] = True
    manifest['relocations'][ARM][FAMILY] = staged['runtime_wrapper']
    manifest['relocations'][COMMON][FAMILY] = staged['storage']
    for path, ids in ((ARM, ('COMMON_SHARED_STATUS_NOTICE_MODAL_WRAP',)),
                      (COMMON, [r['id'] for r in final['records'] if r['message_ID'] in staged['storage']['changed_visible_templates']])):
        manifest['changed_records'][path].extend(id for id in ids if id not in manifest['changed_records'][path])
    manifest['shared_status_notices_registered_successor_pipeline'] = dict(predecessor=predecessor,
        driver=str(Path(__file__)), driver_sha256=digest(__file__), review=str(REVIEW), review_sha256=digest(REVIEW),
        exact_rebuild_and_reconstruction=True, scope=scope)
    assert manifest['batches'][:-1] == old['batches'] and len(manifest['checks']) == 68
    save(MANIFEST, manifest)
    released = dict(profile=PROFILE, candidate=str(CANDIDATE), candidate_sha256=sha, patch=str(PATCH),
        patch_sha256=digest(PATCH), clean_input_sha256=parent['clean_input_sha256'], clean_input_patch_byte_exact=True,
        manifest=str(MANIFEST), manifest_sha256=digest(MANIFEST), registry_sha256=digest(pending_registry),
        target_ARM9_sha256=digest_bytes(arm), target_COMMON_sha256=digest_bytes(common), predecessor=predecessor,
        canonical_base=parent['canonical_base'], canonical_sha256=parent['canonical_sha256'],
        registered_manifest_entries=733, accepted_layers=114, passing_release_checks=68, repository_tests=tests,
        whole_parent_inverse_exact=True, experimental_not_promoted=True, own_registered_startup_pending=False,
        right_bound_configuration=profile['ascii_glyph_right_bounds'],
        registered_market_format_andboth_data_pointers_preserved=True,
        own_registered_startup=str(EVIDENCE / 'stored_and_departure_checkpoint.json'),
        own_registered_startup_sha256=digest(EVIDENCE / 'stored_and_departure_checkpoint.json'),
        actual_verification_scope=scope, changed_components=[ARM], changed_internal_files=[COMMON],
        new_contextual_records=30, prose_revisions=11, justified_retentions=19, full_goal_complete=False)
    save(RELEASE, released)
    save(PACKAGE / 'release_manifest.json', dict(**released, user_acceptance_pending=True))
    for source, name in ((MANIFEST, 'build_manifest.json.gz'), (pending_registry, 'build_release_stack.json.gz')):
        raw = source.read_bytes()
        archived = PACKAGE / name
        archived.write_bytes(gzip.compress(raw, mtime=0))
        assert gzip.decompress(archived.read_bytes()) == raw
    (TEST / 'editorial_ledger_before.json.gz').write_bytes(gzip.compress(original_ledger, compresslevel=1, mtime=0))
    pending_ledger.write_bytes(encode_ledger(update_ledger(ledger, final, released, scope)))
    save(EVIDENCE / 'registration_mutation_plan.json', dict(registry_before=digest_bytes(original_registry),
        registry_after=digest(pending_registry), ledger_before=digest_bytes(original_ledger), ledger_after=digest(pending_ledger)))

    before = load(prior_registry)
    assert {k: v for k, v in registry['profiles'].items() if k != PROFILE} == before['profiles']
    assert {k: v for k, v in registry.items() if k != 'profiles'} == {k: v for k, v in before.items() if k != 'profiles'}
    assert REGISTRY.read_bytes() == original_registry and LEDGER.read_bytes() == original_ledger
    pending_registry.replace(REGISTRY)
    pending_ledger.replace(LEDGER)
    assert digest(REGISTRY) == released['registry_sha256'] and digest(PROMOTED) == promoted
    assert load(LEDGER)['records_editorially_completed'] == 25929
    publish(released, staged['target'])
    print(f'Registered {released["registered_manifest_entries"]} entries and credited 30 notices.')


def digest_bytes(data):
    return sha256(data).hexdigest()


def publish(released, research_rom):
    pins = Path('translations/rom_retention_pins.json')
    kept = load(pins)
    for path in (CANDIDATE, Path(research_rom)):
        absolute = str(path.resolve())
        assert not any(row['path'] == absolute for row in kept)
        kept.append(dict(path=absolute, reason='Preserve exact shared notice ROM. SHA256 ' + released['candidate_sha256']))
    replace_checked(pins, (json.dumps(kept, ensure_ascii=False, indent=2) + '\n').replace('\n', '\r\n').encode('utf-8'))
    readme = f"""# Translation DS cumulative shared-notice candidate

Apply [translation.xdelta](translation.xdelta) to the clean Japanese ROM with SHA-256 `{released['clean_input_sha256']}`. The exact output SHA-256 is `{released['candidate_sha256']}`. The patch SHA-256 is `{released['patch_sha256']}`.

The local test ROM is `{CANDIDATE.as_posix()}`, beside its manifest. This candidate includes 30 reviewed notices, including the revised sailing estimate, distinct defeat and surrender notices, and word wrapping after name substitution. The Copenhagen replay observed the sailing estimate, departure and economic boom. The boom test initialized one existing investment accumulator and the original town update produced the result. V4701 remains main pending user acceptance.
"""
    (PACKAGE / 'README.md').write_text(readme, encoding='utf-8', newline='\n')
    save(PACKAGE / 'checksums.json', {p.relative_to(PACKAGE).as_posix(): digest(p)
        for p in PACKAGE.rglob('*') if p.is_file()})
    line = 'Thirty shared notices are registered and credited once. The ledger now credits 25,929 reviews.'
    text = f"""# Shared status notices registered

{line} The exact clean-input patch reproduces the candidate, which retains all 732 predecessor entries and 114 accepted layers. All 68 release checks and {released['repository_tests']} targeted repository tests pass. V4701 awaits user acceptance. [Local test ROM](../{CANDIDATE.as_posix()}) · [Clean-input patch and verification](../{PACKAGE.as_posix()}/README.md)

The original town update consumed one test investment accumulator and produced the three-row Copenhagen boom notice. The full foreground and blank margins, expanded and wrapped bytes, live ITCM selector, Market format and ship label matched. A dismissed the notice and sailing resumed. The earlier ordinary departure replay observed notices 85 and 86. The same ROM matched six Maria startup frames and all 24 protected name getter results.

The original company editor allows 18 encoded bytes and stores a 19-byte field including the terminator. Four boundary examples, including mixed ASCII and CP932, pass twelve visually reviewed native pages. The earlier 23-byte stress string exceeds the editor limit. Additional condition branches remain covered by offline evidence. [Completed review records](../{REVIEW.as_posix()})

The supplemental legacy tests reported 32 passes and five fixture skips with Windows Unicorn diagnostics. The established 27-test release suite passed separately. The live selector and current native layout checks use the exact candidate.

Continue the 22 source-reviewed crew-loss and confirmation messages with their distinct modal and portrait consumers. The wider shared, town, random, names and remaining prose review remains active. Preserve the separate graphics work and later older-record technical re-audit.
"""
    replace_checked(DOC, text.encode('utf-8'))
    lead = f"""# Current editorial checkpoint - 2026-11-10

{line}

Continue from [the registered shared-notice checkpoint]({DOC.name}).

""".encode('utf-8')
    for filename in ('editorial_handoff_current.md', 'editorial_efficiency_workflow.md', 'translation_progress.md'):
        path = Path('docs') / filename
        replace_checked(path, lead + path.read_bytes())


if __name__ == '__main__':
    cli = argparse.ArgumentParser(description=__doc__)
    cli.add_argument('--register', action='store_true', required=True)
    cli.parse_args()
    register()
