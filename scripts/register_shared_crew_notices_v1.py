"""Register the 22 crew-loss notices after exact native, gameplay and startup checks."""

import argparse
import gzip
import json
import shutil
import xml.etree.ElementTree as ET
from collections import Counter
from copy import deepcopy
from hashlib import sha256
from pathlib import Path
from types import FunctionType

from dk4tool.dialogue.review import validate_natural_dialogue_batch
from dk4tool.patch.crew_loss_portrait_wrap_v1 import transform
from dk4tool.patch.xdelta import apply_xdelta, make_xdelta
from dk4tool.rom.nds import NdsImage
from dk4tool.script.common_message_table import DIRECTORY_OFFSET, TABLE_OFFSET
from scripts.audit_story_glyph_consistency import load, save
from scripts.checkpoint_shared_crew_notices_v1 import ROOT
from scripts.editorial_ledger_storage_v1 import encode_ledger
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest
from scripts.package_ship_command_candidate_v1 import replace_checked
from scripts.preflight_shared_crew_notices_v1 import ARM, COMMON, OUT
from scripts.register_shared_notices_v1 import CONTEXT, LEDGER, PROMOTED, REGISTRY, RELEASE as PARENT
from scripts.review_ship_loss_context_v1 import OUTPUT
from scripts.run_shared_crew_notices_live_v1 import PREFLIGHT
from scripts.seal_shared_text_source_v1 import reference
from scripts.stage_shared_notices_storage_v1 import relocate
from scripts.stage_ship_command_release_v1 import CLEAN


PROFILE = 'all-routes-crew-loss-notices-v1-20261110'
FAMILY = 'shared_crew_loss_notices_contextual_20261110'
CHECK = 'registered_crew_loss_literal_names_portrait_wrap_and_complete_parent_inverse'
TEST = Path('out/promotion_ready_20261110_crew_notices_v1')
ROM = TEST / 'Translation_DS_All_Routes_Crew_Notices_20261110_candidate.nds'
MANIFEST = ROM.with_suffix('.manifest.json')
PACKAGE = Path('releases/all_routes_editorial_20261110_crew_notices_candidate')
EVIDENCE = PACKAGE / 'verification'
RELEASE = EVIDENCE / 'registered_release_verification.json'
PATCH = PACKAGE / 'translation.xdelta'
REVIEW = ROOT / 'registered_review.json'
DOC = Path('docs/editorial_shared_crew_notices_registered_20261110.md')
QA = OUT / 'crew_release_qa.xml'


def rebuild(parent, checked, manuscript):
    image = NdsImage.open(parent)
    original_arm, original_common = image.read_file(ARM), image.read_file(COMMON)
    arm, selector = transform(original_arm)
    assert json.loads(json.dumps(selector)) == checked['selector']
    directory = sha256(original_arm[DIRECTORY_OFFSET:TABLE_OFFSET]).hexdigest()
    repack = FunctionType(relocate.__code__, {**relocate.__globals__, 'DIRECTORY': directory})
    rows = {row['message_ID']: row for row in manuscript['records']}
    text = {n: row['english'].encode('ascii') for n, row in rows.items()}
    common, arm, entries, packing = repack(original_common, arm, rows, text)
    assert json.loads(json.dumps(packing)) == checked['storage']
    for row in checked['exact_record_references']:
        assert reference(entries[row['message_ID']]) == row['proposed']
    image.replace_file(ARM, arm)
    image.replace_file(COMMON, common)
    assert bytes(image.rom.save()) == Path(checked['research_ROM']).read_bytes()
    image.replace_file(ARM, original_arm)
    image.replace_file(COMMON, original_common)
    assert bytes(image.rom.save()) == Path(parent).read_bytes()
    return arm, common


def final_review(manuscript, checked, scope):
    references = {row['message_ID']: row for row in checked['exact_record_references']}
    records = []
    for row in manuscript['records']:
        n = row['message_ID']
        assert row['review'] == dict(source=True, context=True, localization=True, naturalness=True, formatting=False)
        assert row['source_reference'] == references[n]['source'] and row['current_reference'] == references[n]['prior']
        records.append({**row, 'review': {**row['review'], 'formatting': True},
            'registered_reference': {**references[n]['proposed'], 'ROM_sha256': checked['research_ROM_sha256'],
                'exact_stored_hex': row['english'].encode('ascii').hex()},
            'current_gameplay_observed': n in (339, 2680),
            'native_ship_name_substitution_preserved': True, 'new_credit': 1})
    assert len(records) == 22 and Counter(row['decision'] for row in records) == {'revision': 8, 'retention': 14}
    final = dict(format='dk4-reviewed-shared-crew-notices-v1', target_locale='en-US',
        translation_policy='natural-dialogue-v2', encoder='dialogue-relocatable-v1',
        review_gates=['source', 'context', 'localization', 'naturalness', 'formatting'],
        records=records, actual_verification_scope=scope, ROM_sha256=checked['research_ROM_sha256'],
        full_goal_complete=False)
    validate_natural_dialogue_batch(final)
    return final


def update_ledger(ledger, rows, release, scope):
    ctx = ledger[CONTEXT]
    keys = [dict(file_path=row['file_path'], id=row['id']) for row in rows]
    assert len({(row['file_path'], row['id']) for row in keys}) == len(keys) == 22
    assert FAMILY not in ledger and not any(row['id'] == FAMILY for row in ledger['coverage_units'])
    for field in ('record_keys', 'integrated_record_keys'):
        assert len(ctx[field]) == 25929 and all(key not in ctx[field] for key in keys)
        ctx[field].extend(keys)
    ctx['record_IDs'].extend(row['id'] for row in rows)
    for field in ('fresh_pass_records_explicitly_reread', 'fresh_pass_records_integrated'):
        ctx[field] += 22
    ctx.update(latest_completed_family=FAMILY, latest_final_review=str(REVIEW))
    ctx['reconciled_families'].append(dict(id=FAMILY, records=22, final_review=str(REVIEW), new_revisions=8,
        justified_retentions=14, new_completed_records=22, historical_reconciliation_only=False,
        actual_verification_scope=scope))
    family = dict(id=FAMILY, kind='shared-crew-notices-and-confirmation', records=22, record_keys=keys,
        final_review=str(REVIEW), final_review_sha256=digest(REVIEW), revised_count=8, retained_count=14,
        fresh_revisions=8, fresh_retentions=14, actual_verification_scope=scope,
        integrated_record_bindings=str(REVIEW))
    ledger['completed_editorial_families'].append(family)
    ledger['coverage_units'].append(dict(**family, status='complete-contextual-native-stored-representative-registered-release',
        completion_credit_added=22, release_verification=str(RELEASE), release_verification_sha256=digest(RELEASE),
        full_goal_complete=False))
    for field in ('records_editorially_completed', 'records_with_source_and_prose_pass', 'records_with_source_prose_drafts'):
        ledger[field] += 22
    ledger['records_revised_and_integrated'] += 8
    ledger['retained_wordings_editorially_completed'] += 14
    ledger['current_integrated_candidate'].update(path=str(ROM), sha256=release['candidate_sha256'], profile=PROFILE,
        MESFILE_sha256=release['target_COMMON_sha256'], ARM9_sha256=release['target_ARM9_sha256'],
        patch=str(PATCH), patch_sha256=release['patch_sha256'], manifest=str(MANIFEST),
        manifest_sha256=release['manifest_sha256'], registered_release_verification=str(RELEASE))
    ledger[FAMILY] = dict(new_credit=22, final_review=str(REVIEW), release_verification=str(RELEASE),
        actual_verification=str(EVIDENCE / 'live_verification.json'), registered_integration_pending=False)
    ledger['latest_checkpoint'] = 'Twenty-two crew notices and abandonment confirmations are registered.'
    assert len(ctx['integrated_record_keys']) == ledger['records_editorially_completed'] == 25951
    assert ledger['records_revised_and_integrated'] == 15421 and ledger['retained_wordings_editorially_completed'] == 10530
    return ledger


def publish(release, research):
    notes = f"""# Cumulative crew-notice testing candidate

Use `{ROM.as_posix()}` beside its build manifest. The [clean-input patch](translation.xdelta) applies to the clean Japanese ROM SHA-256 `{release['clean_input_sha256']}`. It reproduces SHA-256 `{release['candidate_sha256']}` byte for byte. Patch SHA-256 is `{release['patch_sha256']}`.

The build reviews 22 crew notices and confirmation lines. It keeps literal ship names, wraps portrait dialogue after substitution and preserves the existing Abandon Ship menu and all original voice slots. The focused emulator replay set the secondary ship's crew to zero and assigned it an 18-byte test name. The warning and two-line confirmation displayed the full name. No returned to the same menu and kept the ship. V4701 awaits user acceptance.
"""
    (PACKAGE / 'README.md').write_text(notes, encoding='utf-8', newline='\n')
    save(PACKAGE / 'checksums.json', {p.relative_to(PACKAGE).as_posix(): digest(p)
        for p in PACKAGE.rglob('*') if p.is_file()})
    pin_path = Path('translations/rom_retention_pins.json')
    pins = load(pin_path)
    for path in (ROM, Path(research)):
        absolute = str(path.resolve())
        assert not any(row['path'] == absolute for row in pins)
        pins.append(dict(path=absolute, reason='Preserve exact crew-notice ROM. SHA256 ' + release['candidate_sha256']))
    replace_checked(pin_path, (json.dumps(pins, ensure_ascii=False, indent=2) + '\n').replace('\n', '\r\n').encode('utf-8'))
    summary = 'The 22 crew-loss and abandonment messages are registered. The ledger now credits 25,951 reviews.'
    doc = f"""# Crew-loss and abandonment messages registered

{summary} The batch has eight prose revisions and 14 justified retentions. The clean-input patch reconstructs the exact candidate. It preserves all 733 predecessor entries and 114 accepted layers. All 69 release checks and 27 targeted repository tests pass. V4701 awaits user acceptance. [Test ROM](../{ROM.as_posix()}) · [Patch and verification](../{PACKAGE.as_posix()}/README.md)

The original speakerless path interpreted name bytes as macros. The two scoped notices now copy the complete name literally. The original three portrait voice tables reuse the established word formatter, including the Yes/No confirmation. The 110 stored native samples, 621 original voice selections, 66 reviewed pages and complete selector-scope checks preserve the original controls. The original crew scan produced the warning and confirmation in the 8,500-frame emulator replay using one test crew field and one test name field. Both complete rendered masks matched. No restored the same menu and kept the ship. The 31,000-frame Maria startup and 24 protected name results passed. [Individual review and exact references](../{REVIEW.as_posix()})

The shared-source packet still has unmapped Market replies and remaining town, random, names and other prose. Continue their source and consumer review. Deferred artwork and the older-record technical re-audit remain separate.
"""
    replace_checked(DOC, doc.encode('utf-8'))
    header = f'# Current editorial checkpoint - 2026-11-10\n\n{summary}\n\nContinue from [the registered crew-notice checkpoint]({DOC.name}).\n\n'
    for filename in ('editorial_handoff_current.md', 'editorial_efficiency_workflow.md', 'translation_progress.md'):
        path = Path('docs') / filename
        replace_checked(path, header.encode('utf-8') + path.read_bytes())


def register():
    assert not any(p.exists() for p in (TEST, PACKAGE, REVIEW, DOC))
    parent, checked, checkpoint = map(load, (PARENT, PREFLIGHT, ROOT / 'checkpoint.json'))
    sha = checked['research_ROM_sha256']
    assert digest(checked['research_ROM']) == sha == checkpoint['candidate_sha256']
    assert checkpoint['approved_for_registered_successor'] and checkpoint['live_messages'] == [339, 2680]
    assert checkpoint['verified_native_cases'] == 110 and checkpoint['original_voice_selections'] == 621
    for path, expected in checkpoint['evidence'].items():
        assert digest(path) == expected
    assert gzip.decompress((ROOT / 'native_preflight.json.gz').read_bytes()) == PREFLIGHT.read_bytes()
    boot = load(ROOT / 'own_startup_verification.json')
    assert boot['candidate_sha256'] == sha and len(boot['original_protected_name_getters']) == 24
    assert digest(REGISTRY) == parent['registry_sha256'] and digest(CLEAN) == parent['clean_input_sha256']
    assert digest(parent['candidate']) == parent['candidate_sha256'] == checked['runtime']['candidate_sha256']
    assert digest(parent['manifest']) == parent['manifest_sha256']
    tests = list(ET.parse(QA).getroot().iter('testsuite'))
    assert sum(int(s.get('tests', 0)) for s in tests) == 27
    assert not any(int(s.get(k, 0)) for s in tests for k in ('errors', 'failures', 'skipped'))
    registry, ledger, old = load(REGISTRY), load(LEDGER), load(parent['manifest'])
    assert len(old['batches']) == 733 and len(old['checks']) == 68 and all(old['checks'].values())
    assert len(registry['accepted_layers']) == 114 and PROFILE not in registry['profiles']
    assert ledger['records_editorially_completed'] == 25929 and not ledger['full_goal_complete']
    assert ledger['current_integrated_candidate']['sha256'] == parent['candidate_sha256']
    previous_registry, previous_ledger, promoted = REGISTRY.read_bytes(), LEDGER.read_bytes(), digest(PROMOTED)
    source = load(OUTPUT)
    arm, common = rebuild(parent['candidate'], checked, source)
    scope = dict(observed_notice_IDs=[339, 2680], native_stored_cases=110, voice_selections=621,
        visual_pages=66, fixture_scope='one existing secondary crew field and one 19-byte name field in isolated RAM',
        actual_no_preserved_the_ship=True, earned_crew_loss=False, confirmed_abandonment=False, hardware=False)
    review = final_review(source, checked, scope)
    TEST.mkdir()
    EVIDENCE.mkdir(parents=True)
    make_xdelta(CLEAN, Path(checked['research_ROM']), PATCH)
    apply_xdelta(CLEAN, PATCH, ROM)
    assert ROM.read_bytes() == Path(checked['research_ROM']).read_bytes() and digest(ROM) == sha
    save(REVIEW, review)
    for path in (ROOT / 'checkpoint.json', ROOT / 'live_verification.json', ROOT / 'own_startup_verification.json',
                 ROOT / 'selector_scope.json', QA):
        shutil.copyfile(path, EVIDENCE / path.name)
        assert digest(path) == digest(EVIDENCE / path.name)
    prior = TEST / 'release_stack_before_crew_notices.json'
    prior.write_bytes(previous_registry)
    predecessor = dict(profile=parent['profile'], candidate=parent['candidate'], candidate_sha256=parent['candidate_sha256'],
        manifest=parent['manifest'], manifest_sha256=parent['manifest_sha256'], registry=str(prior),
        registry_sha256=parent['registry_sha256'])
    profile = deepcopy(registry['profiles'][parent['profile']])
    profile.update(verified_shared_notice_predecessor=predecessor, shared_crew_notice_release=str(REVIEW),
        note='Cumulative crew-loss and abandonment notices with literal ship names.')
    assert profile['ascii_glyph_right_bounds'] == parent['right_bound_configuration']
    registry['profiles'][PROFILE] = profile
    pending_registry = REGISTRY.with_name('release_stack.crew_notices.pending.json')
    pending_ledger = LEDGER.with_name('editorial_review_current.crew_notices.pending.json')
    assert not pending_registry.exists() and not pending_ledger.exists()
    save(pending_registry, registry)
    manifest = deepcopy(old)
    manifest.update(profile=PROFILE, candidate_rom=str(ROM), candidate_sha256=sha,
        release_stack_sha256=digest(pending_registry))
    manifest['batches'].append(str(REVIEW))
    manifest['checks'][CHECK] = True
    manifest['relocations'][ARM][FAMILY] = checked['selector']
    manifest['relocations'][COMMON][FAMILY] = checked['storage']
    for path, ids in ((ARM, ('COMMON_CREW_LITERAL_SHIP_NAME_AND_PORTRAIT_WRAP',)),
                      (COMMON, [f'COMMON_MESSAGE_{n}' for n in checked['storage']['changed_visible_templates']])):
        manifest['changed_records'][path].extend(id for id in ids if id not in manifest['changed_records'][path])
    manifest['shared_crew_notices_registered_successor_pipeline'] = dict(predecessor=predecessor,
        driver=str(Path(__file__)), driver_sha256=digest(__file__), review=str(REVIEW), review_sha256=digest(REVIEW),
        exact_rebuild_and_reconstruction=True, scope=scope)
    assert manifest['batches'][:-1] == old['batches'] and len(manifest['checks']) == 69
    save(MANIFEST, manifest)
    startup = EVIDENCE / 'own_startup_verification.json'
    release = dict(profile=PROFILE, candidate=str(ROM), candidate_sha256=sha, patch=str(PATCH), patch_sha256=digest(PATCH),
        clean_input_sha256=parent['clean_input_sha256'], clean_input_patch_byte_exact=True, manifest=str(MANIFEST),
        manifest_sha256=digest(MANIFEST), registry_sha256=digest(pending_registry), target_ARM9_sha256=sha256(arm).hexdigest(),
        target_COMMON_sha256=sha256(common).hexdigest(), predecessor=predecessor, canonical_base=parent['canonical_base'],
        canonical_sha256=parent['canonical_sha256'], registered_manifest_entries=734, accepted_layers=114,
        passing_release_checks=69, repository_tests=27, whole_parent_inverse_exact=True, experimental_not_promoted=True,
        own_registered_startup_pending=False, own_registered_startup=str(startup), own_registered_startup_sha256=digest(startup),
        original_protected_name_getters_count=24, right_bound_configuration=profile['ascii_glyph_right_bounds'],
        registered_market_format_andboth_data_pointers_preserved=True, actual_verification_scope=scope,
        changed_components=[ARM], changed_internal_files=[COMMON], new_contextual_records=22,
        prose_revisions=8, justified_retentions=14, full_goal_complete=False)
    save(RELEASE, release)
    save(PACKAGE / 'release_manifest.json', {**release, 'user_acceptance_pending': True})
    for path, name in ((MANIFEST, 'build_manifest.json.gz'), (pending_registry, 'build_release_stack.json.gz')):
        raw = path.read_bytes()
        archive = PACKAGE / name
        archive.write_bytes(gzip.compress(raw, mtime=0))
        assert gzip.decompress(archive.read_bytes()) == raw
    backup = TEST / 'editorial_ledger_before.json.gz'
    backup.write_bytes(gzip.compress(previous_ledger, compresslevel=1, mtime=0))
    assert gzip.decompress(backup.read_bytes()) == previous_ledger
    pending_ledger.write_bytes(encode_ledger(update_ledger(ledger, review['records'], release, scope)))
    save(EVIDENCE / 'registration_mutation_plan.json', dict(registry_before=sha256(previous_registry).hexdigest(),
        registry_after=digest(pending_registry), ledger_before=sha256(previous_ledger).hexdigest(),
        ledger_after=digest(pending_ledger)))
    earlier = json.loads(previous_registry)
    assert {k: v for k, v in registry['profiles'].items() if k != PROFILE} == earlier['profiles']
    assert {k: v for k, v in registry.items() if k != 'profiles'} == {k: v for k, v in earlier.items() if k != 'profiles'}
    assert REGISTRY.read_bytes() == previous_registry and LEDGER.read_bytes() == previous_ledger
    pending_registry.replace(REGISTRY)
    pending_ledger.replace(LEDGER)
    assert digest(REGISTRY) == release['registry_sha256'] and digest(PROMOTED) == promoted
    publish(release, checked['research_ROM'])
    print('Registered 734 entries and credited 22 crew notices once.')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--register', action='store_true', required=True)
    parser.parse_args()
    register()
