"""Register the verified developed-port label and exact clean-input patch."""

from copy import deepcopy
from hashlib import sha256
from json import dumps
from pathlib import Path
from shutil import copyfile
from xml.etree import ElementTree

from dk4tool.dialogue.review import validate_natural_dialogue_batch
from dk4tool.patch.xdelta import apply_xdelta, make_xdelta
from dk4tool.script.format_safety_relocated_v2 import bind_registered_story_percent_guard
from scripts import stage_developed_port_menu_20261115 as stage
from scripts import verify_developed_port_menu_20261115 as live
from scripts.editorial_ledger_storage_v1 import encode_ledger
from scripts.prepare_all_routes_promotion_20261111 import package_checksums, verify_runtime
from scripts.register_lil_ceramics_wrap_20261111 import archive_file, write_pending
from scripts.verify_release_baseline import files


base, parent = stage.base, stage.parent
PROFILE = 'all-routes-developed-port-menu-v1-20261115'
CHECK = 'registered_developed_port_menu_slot_and_complete_parent_inverse'
ROOT = Path('out/developed_port_menu_registered_20261115_v1')
ROM = ROOT / 'Translation_DS_All_Routes_Developed_Port_Menu_20261115_candidate.nds'
MANIFEST = ROM.with_suffix('.manifest.json')
PACKAGE = Path('releases/all_routes_editorial_20261115_developed_port_menu_candidate')
PATCH, VERIFY = PACKAGE / 'translation.xdelta', PACKAGE / 'verification'
REVIEW, RELEASE = VERIFY / 'registered_review.json', VERIFY / 'registered_release_verification.json'
DOC = Path('docs/editorial_developed_port_menu_20261115.md')
STARTUP, QA = (stage.ROOT / name for name in ('own_startup_verification.json', 'repository_qa.xml'))
CHECKPOINT = 'The developed Port menu now reads “Back to Town” and returns to the original town screen.'


def verify(prior, guard):
    staged, boot, gameplay = map(base.load, (stage.STORED, STARTUP, live.OUTPUT))
    sha = base.digest(stage.ROM)
    assert sha == staged['candidate_sha256'] == boot['candidate_sha256'] == gameplay['candidate_sha256']
    assert base.digest(parent.ROM) == staged['previous_sha256'] == prior['candidate_sha256']
    assert base.digest(stage.CLEAN) == prior['clean_input_sha256']
    assert boot['cold_boot'] and not boot['savestate'] and boot['complete_deployed_payload_exact']
    assert len(boot['exact_matching_frames']) == 6 and len(boot['original_protected_name_getters']) == 24
    assert all(base.digest(k) == v for evidence in (boot['evidence'], gameplay['evidence']) for k, v in evidence.items())
    assert gameplay['actual_gameplay'] and gameplay['natural_village_development'] and gameplay['position_fixture_only']
    assert gameplay['port_return_frame'] == 14800 and len(gameplay['equal_control_frames']) == 6
    assert [x['selected'] for x in gameplay['cases']] == [False, True]
    assert all(x['complete_english_ink_pixels'] == 136 and x['complete_blank_cells'] for x in gameplay['cases'])
    assert base.digest(live.SHEET) == gameplay['sheet_sha256']
    suite, = ElementTree.parse(QA).iter('testsuite')
    assert [int(suite.get(k, 0)) for k in ('tests', 'failures', 'errors', 'skipped')] == [15, 0, 0, 0]
    clean, old, new = map(base.NdsImage.open, (stage.CLEAN, parent.ROM, stage.ROM))
    before, after = map(files, (old, new))
    assert before.keys() == after.keys() and {p for p in before if before[p] != after[p]} == {stage.ARM}
    arm, field = stage.apply(clean.read_file(stage.ARM), before[stage.ARM])
    assert arm == after[stage.ARM] and field == staged['changed_slot']
    assert sha256(arm).hexdigest() == staged['target_ARM9_sha256']
    assert sha256(after[stage.parent.stage.COMMON]).hexdigest() == prior['target_COMMON_sha256']
    verify_runtime(arm, prior)
    checked = bind_registered_story_percent_guard(guard)(files(clean), after)
    assert checked['total_exact_source_bound_relocated_leading25_count'] == 7
    assert not any(checked['source_bound_new_command_counts'].values())
    new.replace_file(stage.ARM, before[stage.ARM])
    assert bytes(new.rom.save()) == parent.ROM.read_bytes()
    review = dict(translation_policy='natural-dialogue-v2', encoder='dialogue-relocatable-v1', target_locale='en-US',
        storage_transform='fixed ARM9 C-string slot',
        review_gates=['source', 'context', 'localization', 'naturalness', 'formatting'], records=[dict(
        id=stage.RECORD, file_path=stage.ARM, source_Japanese=stage.JAPANESE, speaker='Port menu',
        source_meaning='Leave the port office and return to the town facilities.',
        context='The Port submenu for a developed village. Depart sails away. This option closes the port office.',
        previous_display=stage.JAPANESE, english=stage.ENGLISH, decision='revision',
        localization_note='Back to Town names the screen that returns and leaves Depart available for sailing.',
        review=dict(source=True, context=True, localization=True, naturalness=True, formatting=True),
        source_reference=dict(offset=stage.OFFSET, capacity=stage.SLOT, source_hex=field['clean_hex']),
        current_reference=dict(offset=stage.OFFSET, pointer_field=stage.POINTER, previous_hex=field['previous_hex']),
        registered_reference=dict(offset=stage.OFFSET, target_hex=field['target_hex'], candidate_sha256=sha),
        controls=dict(layout_preserved=True, original_menu_branch_and_pointer_preserved=True,
                      runtime_substitutions=0, allocation=stage.SLOT, complete_ascii_glyphs=True))],
        candidate_sha256=sha, checked_story_format_guard=checked, actual=gameplay, prior_ledger_credit_change=0)
    validate_natural_dialogue_batch(review)
    return staged, review


def main():
    before_registry, before_ledger = base.REGISTRY.read_bytes(), base.LEDGER.read_bytes()
    registry, ledger, manifest, prior = map(base.load, (base.REGISTRY, base.LEDGER, parent.MANIFEST, parent.RELEASE))
    assert base.digest(base.REGISTRY) == prior['registry_sha256'] and base.digest(parent.MANIFEST) == prior['manifest_sha256']
    assert ledger['current_integrated_candidate']['sha256'] == prior['candidate_sha256']
    assert len(registry['accepted_layers']) == 114 and PROFILE not in registry['profiles']
    assert len(manifest['batches']) == 821 and len(manifest['checks']) == 156 and all(manifest['checks'].values())
    profile = deepcopy(registry['profiles'][prior['profile']])
    staged, review = verify(prior, profile['source25_multiarchive_guard'])
    reg_tmp = base.REGISTRY.with_name('release_stack.developed_port_menu.pending.json')
    ledger_tmp = base.LEDGER.with_name('editorial_review_current.developed_port_menu.pending.json')
    assert not any(path.exists() for path in (ROOT, PACKAGE, DOC, reg_tmp, ledger_tmp))
    main_before = base.digest(base.PROMOTED)
    ROOT.mkdir()
    VERIFY.mkdir(parents=True)
    make_xdelta(stage.CLEAN, stage.ROM, PATCH)
    apply_xdelta(stage.CLEAN, PATCH, ROM)
    sha = base.digest(ROM)
    assert sha == staged['candidate_sha256'] and ROM.read_bytes() == stage.ROM.read_bytes()
    for path in (stage.STORED, STARTUP, live.OUTPUT, live.SHEET, QA):
        copyfile(path, VERIFY / path.name)
        assert base.digest(path) == base.digest(VERIFY / path.name)
    base.save(REVIEW, review)

    backup = ROOT / 'release_stack_before_developed_port_menu.json'
    backup.write_bytes(before_registry)
    predecessor = {k: prior[k] for k in ('profile', 'candidate', 'candidate_sha256', 'manifest',
                                         'manifest_sha256', 'registry_sha256')}
    predecessor['registry'] = str(backup)
    profile.update(verified_barmaid_town_labels_predecessor=predecessor, developed_port_menu_release=str(REVIEW))
    registry['profiles'][PROFILE] = profile
    base.save(reg_tmp, registry)
    manifest.update(profile=PROFILE, candidate_rom=str(ROM), candidate_sha256=sha, release_stack_sha256=base.digest(reg_tmp))
    manifest['batches'].append(str(REVIEW))
    manifest['checks'][CHECK] = True
    manifest['changed_records'][stage.ARM].append(stage.RECORD)
    manifest['developed_port_menu_pipeline'] = dict(predecessor=predecessor, registered_review=str(REVIEW),
        registered_review_sha256=base.digest(REVIEW), producer_sha256=base.digest(stage.__file__),
        registration_driver_sha256=base.digest(__file__), owned_ARM9_field=staged['changed_slot'], complete_parent_inverse=True)
    base.save(MANIFEST, manifest)
    boot = VERIFY / STARTUP.name
    release = prior | dict(profile=PROFILE, candidate=str(ROM), candidate_sha256=sha, patch=str(PATCH),
        patch_sha256=base.digest(PATCH), manifest=str(MANIFEST), manifest_sha256=base.digest(MANIFEST),
        registry_sha256=base.digest(reg_tmp), predecessor=predecessor, target_ARM9_sha256=staged['target_ARM9_sha256'],
        registered_manifest_entries=822, passing_release_checks=157, own_registered_startup=str(boot),
        own_registered_startup_sha256=base.digest(boot), changed_components=[stage.ARM], changed_internal_files=[],
        repository_tests=15, legacy_fixture_tests_skipped=0, new_contextual_records=0, prose_revisions=0, name_label_revisions=0,
        text_display_revisions=1, justified_retentions=0, reviewed_UI_labels=1,
        actual_verification_scope=dict(actual_emulator=True, own_startup=True, developed_Narvik_Port=True,
                                       location_fixture_only=True, hardware=False))
    base.save(RELEASE, release)
    base.save(PACKAGE / 'release_manifest.json', release | {'user_acceptance_pending': True})
    archive_file(MANIFEST.read_bytes(), PACKAGE / 'build_manifest.json.gz')
    archive_file(reg_tmp.read_bytes(), PACKAGE / 'build_release_stack.json.gz')
    archive_file(before_ledger, ROOT / 'editorial_ledger_before.json.gz')
    pending = ledger['pending_shared_consumer_checkpoint_20261114']
    assert pending['remaining_total'] == 276 and pending['candidate_sha256'] == prior['candidate_sha256']
    pending['candidate_sha256'] = sha
    assert ledger['records_editorially_completed'] == 27700 and not ledger['full_goal_complete']
    ledger['current_integrated_candidate'].update(path=str(ROM), sha256=sha, profile=PROFILE, patch=str(PATCH),
        patch_sha256=release['patch_sha256'], manifest=str(MANIFEST), manifest_sha256=release['manifest_sha256'],
        ARM9_sha256=release['target_ARM9_sha256'], registered_release_verification=str(RELEASE))
    ledger['developed_port_menu_20261115'] = dict(registered_candidate_sha256=sha,
        registered_review=str(REVIEW), registered_release=str(RELEASE), record=stage.RECORD, text_display_revisions=1)
    ledger['latest_checkpoint'] = CHECKPOINT
    write_pending(ledger_tmp, encode_ledger(ledger))
    receipt = dict(registry_before=sha256(before_registry).hexdigest(), ledger_before=sha256(before_ledger).hexdigest(),
                   registry_after=base.digest(reg_tmp), ledger_after=base.digest(ledger_tmp), main_sha256=main_before)
    base.save(VERIFY / 'registration_mutation_plan.json', receipt)
    (PACKAGE / 'README.md').write_text(f"""# Developed Port Menu test candidate

The [local ROM](../../{ROM.as_posix()}) shows Back to Town in the developed Port menu. The [clean-input patch](translation.xdelta) reconstructs SHA-256 `{sha}` byte for byte. Hardware testing and acceptance for main are pending.
""", encoding='utf-8', newline='\n')
    base.save(PACKAGE / 'checksums.json', package_checksums(PACKAGE))
    assert base.digest(base.REGISTRY) == receipt['registry_before'] and base.digest(base.LEDGER) == receipt['ledger_before']
    assert base.digest(base.PROMOTED) == main_before
    reg_tmp.replace(base.REGISTRY)
    try:
        ledger_tmp.replace(base.LEDGER)
    except OSError:
        base.replace_checked(base.REGISTRY, before_registry)
        raise
    assert base.digest(base.REGISTRY) == receipt['registry_after'] and base.digest(base.LEDGER) == receipt['ledger_after']

    pins_path = Path('translations/rom_retention_pins.json')
    pins = base.load(pins_path)
    for path in (ROM, stage.ROM):
        absolute = str(path.resolve())
        assert all(row['path'] != absolute for row in pins)
        pins.append(dict(path=absolute, reason=f'Preserve developed Port menu candidate {sha}'))
    base.replace_checked(pins_path, (dumps(pins, ensure_ascii=False, indent=2) + '\n').replace('\n', '\r\n').encode())
    base.replace_checked(DOC, f"""# Developed Port menu

The clean DS Port menu contains 出港所を出る, an option that closes the port office and returns to the town facilities. Its original town-ID branch allows the extra choice at developed villages. Ordinary Syracuse showed Depart, Dock and Cargo Setup. Developed Narvik showed Depart and the Japanese return label. The label now reads **Back to Town** within the same 16-byte ARM9 slot. The native branch, pointer and menu commands are preserved. [Exact review](../{REVIEW.as_posix()})

Two cold boots replayed the original password, development, return to Narvik, resupply, Port menu and selection. Each used one source-checked ship-coordinate fixture near Narvik. The password was entered normally and the original game applied development. At both highlighted states all 136 English glyph pixels and the surrounding blank cells passed. All pixels outside the owned line matched, and six whole frames match, including the return to town. A separate startup matched six frames and 24 protected name getters. All 15 focused tests passed. [Menu comparison](../{(VERIFY / live.SHEET.name).as_posix()})

The [registered candidate and exact clean-input patch](../{PACKAGE.as_posix()}/README.md) preserve 114 accepted layers and 157 passing release checks. This is one UI correction outside the dialogue count. The ledger credits 27,700 reviews with 276 mapped shared keys still open. Hardware testing remains open.
""".encode())
    prefix = f'# Current editorial checkpoint - 2026-11-15\n\n{CHECKPOINT} [Checkpoint]({DOC.name})\n\n'.encode()
    for name in ('editorial_handoff_current.md', 'translation_progress.md', 'build_continuity_protocol.md'):
        path = Path('docs') / name
        base.replace_checked(path, prefix + path.read_bytes())
    print(f'Registered {sha} with 822 entries, 114 accepted layers and 157 passing checks.')


if __name__ == '__main__':
    main()
