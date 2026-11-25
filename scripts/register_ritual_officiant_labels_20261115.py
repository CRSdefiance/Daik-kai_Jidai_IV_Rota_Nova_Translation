"""Register the verified ritual titles on the exact cumulative predecessor."""

from copy import deepcopy
from json import dumps
from pathlib import Path
from shutil import copyfile
from xml.etree import ElementTree

from dk4tool.dialogue.review import validate_natural_dialogue_batch
from dk4tool.script.format_safety_relocated_v2 import bind_registered_story_percent_guard
from scripts import replay_ritual_officiant_labels_20261115 as live
from scripts import review_ritual_officiant_labels_20261115 as review
from scripts import stage_ritual_officiant_labels_20261115 as stage
from scripts.editorial_ledger_storage_v1 import encode_ledger
from scripts.prepare_all_routes_promotion_20261111 import package_checksums
from scripts.register_lil_ceramics_wrap_20261111 import archive_file, write_pending
from scripts.verify_release_baseline import files


base, parent = stage.base, stage.parent
PROFILE = 'all-routes-ritual-officiant-labels-v1-20261115'
ROOT = Path('out/ritual_officiant_labels_registered_20261115_v1')
ROM = ROOT / 'Translation_DS_All_Routes_Ritual_Officiant_Labels_20261115_candidate.nds'
MANIFEST = ROM.with_suffix('.manifest.json')
PACKAGE = Path('releases/all_routes_editorial_20261115_ritual_officiant_labels_candidate')
PATCH, VERIFY = PACKAGE / 'translation.xdelta', PACKAGE / 'verification'
REVIEW, RELEASE = VERIFY / 'registered_review.json', VERIFY / 'registered_release_verification.json'
STARTUP, QA = review.STARTUP, stage.ROOT / 'repository_qa_retry.xml'
DOC = Path('docs/editorial_ruler_and_ritual_nameplates_20261115.md')
CHECK = 'registered_ritual_officiant_labels_and_complete_parent_inverse'


def verify(prior, guard):
    draft, staged, startup, game = map(base.load, (review.FINAL, stage.STORED, STARTUP, live.OUTPUT))
    validate_natural_dialogue_batch(draft)
    candidate = base.digest(stage.ROM)
    assert candidate == draft['runtime']['candidate_sha256'] == staged['candidate_sha256']
    assert candidate == startup['candidate_sha256'] == game['candidate_sha256']
    assert base.digest(parent.ROM) == staged['previous_sha256'] == prior['candidate_sha256']
    assert base.digest(stage.CLEAN) == prior['clean_input_sha256']
    assert startup['cold_boot'] and not startup['savestate'] and startup['complete_deployed_payload_exact']
    assert len(startup['exact_matching_frames']) == 6 and len(startup['original_protected_name_getters']) == 24
    assert all(base.digest(path) == sha for proof in (startup, game) for path, sha in proof['evidence'].items())
    assert draft['changed_nameplates'] == 2 and draft['justified_nameplate_retentions'] == 13
    assert draft['exact_all_getters_checked'] == 414
    assert [x['actor_ID'] for x in game['results']] == list(stage.ACTORS)
    assert all(row['matched_complete_nameplates'] and row['exact_control_frames'] and
               row['all_sampled_image_differences_inside_nameplate'] for row in game['results'])
    for path in (review.NATIVE, live.OUTPUT):
        assert base.digest(path) == draft['native_receipt_sha256' if path == review.NATIVE else 'gameplay_receipt_sha256']
    assert base.digest(live.SHEET) == game['sheet_sha256']
    assert base.digest(draft['native_sheet']['path']) == draft['native_sheet']['sha256']
    suite, = ElementTree.parse(QA).iter('testsuite')
    tests = int(suite.get('tests', 0))
    assert tests and all(int(suite.get(key, 0)) == 0 for key in ('failures', 'errors', 'skipped'))
    clean, old, new = [base.NdsImage.open(path) for path in (stage.CLEAN, parent.ROM, stage.ROM)]
    before, after = map(files, (old, new))
    assert before.keys() == after.keys() and {path for path in before if before[path] != after[path]} == {stage.ARM}
    arm, owned = stage.stage_arm(before[stage.ARM], clean.read_file(stage.ARM), prior)
    assert arm == after[stage.ARM] and all(staged[key] == value for key, value in owned.items())
    checked = bind_registered_story_percent_guard(guard)(files(clean), after)
    assert checked['total_exact_source_bound_relocated_leading25_count'] == 7
    assert not any(checked['source_bound_new_command_counts'].values())
    new.replace_file(stage.ARM, before[stage.ARM])
    assert bytes(new.rom.save()) == parent.ROM.read_bytes()
    assert stage.ROM.read_bytes() == review.REBUILT.read_bytes()
    return staged, draft | dict(checked_story_format_guard=checked), tests


def main():
    registry_before, ledger_before = base.REGISTRY.read_bytes(), base.LEDGER.read_bytes()
    registry, ledger, manifest, prior = map(base.load, (base.REGISTRY, base.LEDGER, parent.MANIFEST, parent.RELEASE))
    assert base.digest(base.REGISTRY) == prior['registry_sha256'] and base.digest(parent.MANIFEST) == prior['manifest_sha256']
    assert ledger['current_integrated_candidate']['sha256'] == prior['candidate_sha256']
    assert len(registry['accepted_layers']) == 114 and PROFILE not in registry['profiles']
    assert len(manifest['batches']) == 824 and len(manifest['checks']) == 159 and all(manifest['checks'].values())
    profile = deepcopy(registry['profiles'][prior['profile']])
    staged, draft, tests = verify(prior, profile['source25_multiarchive_guard'])
    reg_tmp = base.REGISTRY.with_name('release_stack.ritual_officiant.pending.json')
    ledger_tmp = base.LEDGER.with_name('editorial_review_current.ritual_officiant.pending.json')
    assert not any(path.exists() for path in (ROOT, PACKAGE, reg_tmp, ledger_tmp))
    main_before = base.digest(base.PROMOTED)
    ROOT.mkdir()
    VERIFY.mkdir(parents=True)
    copyfile(review.PATCH, PATCH)
    copyfile(review.REBUILT, ROM)
    candidate = base.digest(ROM)
    assert candidate == staged['candidate_sha256'] and base.digest(PATCH) == base.digest(review.PATCH)
    for path in (stage.STORED, STARTUP, live.OUTPUT, live.SHEET, review.NATIVE, Path(draft['native_sheet']['path']), QA):
        copyfile(path, VERIFY / path.name)
        assert base.digest(path) == base.digest(VERIFY / path.name)
    base.save(REVIEW, draft)
    backup = ROOT / 'release_stack_before_ritual_officiant.json'
    backup.write_bytes(registry_before)
    predecessor = {key: prior[key] for key in ('profile', 'candidate', 'candidate_sha256', 'manifest',
                                               'manifest_sha256', 'registry_sha256')}
    predecessor['registry'] = str(backup)
    profile.update(verified_forces_relationships_predecessor=predecessor, ritual_officiant_labels_release=str(REVIEW))
    registry['profiles'][PROFILE] = profile
    base.save(reg_tmp, registry)
    manifest.update(profile=PROFILE, candidate_rom=str(ROM), candidate_sha256=candidate, release_stack_sha256=base.digest(reg_tmp))
    manifest['batches'].append(str(REVIEW))
    manifest['checks'][CHECK] = True
    manifest['changed_records'][stage.ARM].extend(r['id'] for r in draft['records'] if r['decision'] == 'revision')
    manifest['ritual_officiant_pipeline'] = dict(predecessor=predecessor, registered_review=str(REVIEW),
        registered_review_sha256=base.digest(REVIEW), producer_sha256=base.digest(stage.__file__),
        registration_driver_sha256=base.digest(__file__), owned_ARM9_fields=staged['fields'],
        owned_alignment_span=staged['new_label_span'], complete_parent_inverse=True)
    base.save(MANIFEST, manifest)
    boot = VERIFY / STARTUP.name
    release = prior | dict(profile=PROFILE, candidate=str(ROM), candidate_sha256=candidate, patch=str(PATCH),
        patch_sha256=base.digest(PATCH), manifest=str(MANIFEST), manifest_sha256=base.digest(MANIFEST),
        registry_sha256=base.digest(reg_tmp), predecessor=predecessor, target_ARM9_sha256=staged['target_ARM9_sha256'],
        registered_manifest_entries=825, passing_release_checks=160, own_registered_startup=str(boot),
        own_registered_startup_sha256=base.digest(boot), changed_components=[stage.ARM], changed_internal_files=[],
        repository_tests=tests, legacy_fixture_tests_skipped=0, new_contextual_records=0, prose_revisions=0,
        name_label_revisions=2, text_display_revisions=0, justified_retentions=13, reviewed_UI_labels=0,
        actual_verification_scope=dict(actual_emulator=True, own_startup=True, initialized_Rafael_dialogue=True, hardware=False))
    base.save(RELEASE, release)
    base.save(PACKAGE / 'release_manifest.json', release | {'user_acceptance_pending': True})
    archive_file(MANIFEST.read_bytes(), PACKAGE / 'build_manifest.json.gz')
    archive_file(reg_tmp.read_bytes(), PACKAGE / 'build_release_stack.json.gz')
    archive_file(ledger_before, ROOT / 'editorial_ledger_before.json.gz')
    pending = ledger['pending_shared_consumer_checkpoint_20261114']
    assert pending['remaining_total'] == 276 and pending['candidate_sha256'] == prior['candidate_sha256']
    pending['candidate_sha256'] = candidate
    assert ledger['records_editorially_completed'] == 27700 and not ledger['full_goal_complete']
    ledger['current_integrated_candidate'].update(path=str(ROM), sha256=candidate, profile=PROFILE, patch=str(PATCH),
        patch_sha256=release['patch_sha256'], manifest=str(MANIFEST), manifest_sha256=release['manifest_sha256'],
        ARM9_sha256=release['target_ARM9_sha256'], registered_release_verification=str(RELEASE))
    checkpoint = 'The two ritual officials are labeled Officiant, with Priest retained for the Christian role.'
    ledger['ritual_officiant_nameplates_20261115'] = dict(registered_candidate_sha256=candidate,
        registered_review=str(REVIEW), registered_release=str(RELEASE), name_label_revisions=2, justified_retentions=13)
    ledger['latest_checkpoint'] = checkpoint
    write_pending(ledger_tmp, encode_ledger(ledger))
    receipt = dict(registry_before=stage.digest(registry_before), ledger_before=stage.digest(ledger_before),
                   registry_after=base.digest(reg_tmp), ledger_after=base.digest(ledger_tmp), main_sha256=main_before)
    base.save(VERIFY / 'registration_mutation_plan.json', receipt)
    (PACKAGE / 'README.md').write_text(f'''# Ritual Officiant Labels test candidate

The [local ROM](../../{ROM.as_posix()}) distinguishes two ritual officials from the Christian Priest role. The [clean-input patch](translation.xdelta) reconstructs SHA-256 `{candidate}` byte for byte. Hardware and acceptance for main are pending.
''', encoding='utf-8', newline='\n')
    base.save(PACKAGE / 'checksums.json', package_checksums(PACKAGE))
    assert base.digest(base.REGISTRY) == receipt['registry_before'] and base.digest(base.LEDGER) == receipt['ledger_before']
    assert base.digest(base.PROMOTED) == main_before
    reg_tmp.replace(base.REGISTRY)
    try:
        ledger_tmp.replace(base.LEDGER)
    except OSError:
        base.replace_checked(base.REGISTRY, registry_before)
        raise
    assert base.digest(base.REGISTRY) == receipt['registry_after'] and base.digest(base.LEDGER) == receipt['ledger_after']

    pins_path = Path('translations/rom_retention_pins.json')
    pins = base.load(pins_path)
    for path in (ROM, stage.ROM):
        absolute = str(path.resolve())
        assert all(row['path'] != absolute for row in pins)
        pins.append(dict(path=absolute, reason=f'Preserve verified ritual title candidate {candidate}'))
    base.replace_checked(pins_path, (dumps(pins, ensure_ascii=False, indent=2) + '\n').replace('\n', '\r\n').encode())
    base.replace_checked(DOC, f'''# Ruler and religious nameplates

The [registered review](../{REVIEW.as_posix()}) covers 15 officials in 17 complete story exchanges and the original palace and ceremony roles. Both characters called 祭主 now use **Officiant**, including the temple guardian and the man the party helps return to Guam. **Priest** remains for 神父. The other 12 rulership and religious labels have individual retention reasons, including **Daimyo**, **Magistrate**, and **Senior Monk**.

All 414 default getter outputs were compared and the only actor differences are the two intended labels. All ten distinct nameplates passed original progressive renderer, complete glyph, and bounds checks. Paired initialized Rafael replays show both revised actors and confine the differences to their nameplates. Those replays use the original block and controller inputs after initialization. Natural event activation and physical hardware remain open. A separate cumulative boot matched six startup frames and 24 protected name getters. All {tests} targeted tests passed. [Emulator comparison](../{(VERIFY / live.SHEET.name).as_posix()})

The [registered ROM and exact clean-input patch](../{PACKAGE.as_posix()}/README.md) preserve all 114 accepted layers and the ASCII right-bound correction. The main build awaits hardware acceptance of a candidate. These nameplate decisions preserve the existing dialogue credit of 27,700 and the 276 mapped shared keys still open.
'''.encode('utf-8'))
    prefix = f'# Current editorial checkpoint - 2026-11-15\n\n{checkpoint} [Checkpoint]({DOC.name})\n\n'.encode()
    for name in ('editorial_handoff_current.md', 'translation_progress.md', 'build_continuity_protocol.md'):
        path = Path('docs') / name
        base.replace_checked(path, prefix + path.read_bytes())
    print(f'Registered {candidate} with 825 entries, 114 accepted layers and 160 passing checks.')


if __name__ == '__main__':
    main()
