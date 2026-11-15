"""Register the two source-bound hostess labels and reconstruct the exact candidate."""

from copy import deepcopy
from hashlib import sha256
from json import dumps
from pathlib import Path
from shutil import copyfile
from xml.etree import ElementTree

from dk4tool.dialogue.review import validate_natural_dialogue_batch
from dk4tool.patch.owned_name_fields_v2 import plan_arm9_name_fields
from dk4tool.patch.xdelta import apply_xdelta, make_xdelta
from dk4tool.script.format_safety_relocated_v2 import bind_registered_story_percent_guard
from scripts import stage_barmaid_town_labels_20261115 as stage
from scripts.editorial_ledger_storage_v1 import encode_ledger
from scripts.prepare_all_routes_promotion_20261111 import package_checksums, verify_runtime
from scripts.register_lil_ceramics_wrap_20261111 import archive_file, write_pending
from scripts.verify_release_baseline import files


base, parent = stage.base, stage.parent
PROFILE = 'all-routes-barmaid-town-labels-v1-20261115'
CHECK = 'registered_barmaid_town_labels_and_complete_parent_inverse'
ROOT = Path('out/barmaid_town_labels_registered_20261115_v1')
ROM = ROOT / 'Translation_DS_All_Routes_Barmaid_Town_Labels_20261115_candidate.nds'
MANIFEST = ROM.with_suffix('.manifest.json')
PACKAGE = Path('releases/all_routes_editorial_20261115_barmaid_town_labels_candidate')
PATCH, VERIFY = PACKAGE / 'translation.xdelta', PACKAGE / 'verification'
REVIEW, RELEASE = VERIFY / 'registered_review.json', VERIFY / 'registered_release_verification.json'
DOC = Path('docs/editorial_barmaid_town_labels_registered_20261115.md')
BOOT = stage.ROOT / 'own_startup_verification.json'
QA = stage.ROOT / 'repository_qa_verified.xml'
VIEWED = '2483f7069fc15c853e6541a86e224e05d1c6539b4c5bff3d8e50a29ab3d6a765'
LABELS = {195: 'Nelly Alexandria', 204: 'Verisa Sao Jorge'}


def verify(prior, guard):
    staged, boot, deployed = map(base.load, (stage.STORED, BOOT, stage.DEPLOYED))
    sha = base.digest(stage.ROM)
    assert sha == staged['candidate_sha256'] == boot['candidate_sha256'] == deployed['candidate_sha256']
    assert base.digest(parent.ROM) == prior['candidate_sha256'] == staged['previous_sha256']
    assert base.digest(stage.CLEAN) == prior['clean_input_sha256']
    assert boot['cold_boot'] and not boot['savestate'] and boot['complete_deployed_payload_exact']
    assert len(boot['exact_matching_frames']) == 6 and len(boot['original_protected_name_getters']) == 24
    assert {row['actor']: row['complete_joined_name'] for row in deployed['full_name_runtime_values']} == LABELS
    for bundle in boot, deployed:
        assert all(base.digest(path) == value for path, value in bundle['evidence'].items())
    assert Path(staged['sheet']) == stage.SHEET and base.digest(stage.SHEET) == staged['sheet_sha256'] == VIEWED
    panels = staged['native_D5404_cases']
    assert len(panels) == 8 and all(r['bitmap_header_and_neighbor_guards_exact'] and r['original_draw_return_verified'] for r in panels)
    rendered = {(r['actor'], r['supplied_width']): r['complete_name'] for r in panels if r['exact_independent_font_match']}
    assert rendered == {(n, w): label for n, label in LABELS.items() for w in stage.WIDTHS}
    tests, = ElementTree.parse(QA).iter('testsuite')
    assert (int(tests.get('tests')), *(int(tests.get(k, 0)) for k in ('failures', 'errors', 'skipped'))) == (70, 0, 0, 0)

    before, after, clean = map(base.NdsImage.open, (parent.ROM, stage.ROM, stage.CLEAN))
    original, result = map(files, (before, after))
    assert original.keys() == result.keys() and {p for p in original if original[p] != result[p]} == {stage.ARM}
    assert base.digest(staged['initial_review']) == staged['review_sha256']
    reviewed = base.load(staged['initial_review'])
    a, b = original[stage.ARM], result[stage.ARM]
    expected, ownership = plan_arm9_name_fields(a, dict(format='dk4-owned-name-fields-proposal-v2',
        runtime=reviewed['native_fixture'], fields=reviewed['proposal']), clean.read_file(stage.ARM))
    assert expected == b and ownership == staged['plan'] and ownership['target_ARM9_sha256'] == staged['target_ARM9_sha256']
    verify_runtime(b, prior)
    checked = bind_registered_story_percent_guard(guard)(files(clean), result)
    assert checked['total_exact_source_bound_relocated_leading25_count'] == 7
    assert not any(checked['source_bound_new_command_counts'].values())
    after.replace_file(stage.ARM, a)
    assert bytes(after.rom.save()) == parent.ROM.read_bytes()
    slots = {field['actor']: field for field in ownership['fields']}
    rows = []
    for row in reviewed['records']:
        n = row['actor']
        row['review']['formatting'] = True
        row['id'] = f'ACTOR_{n}_TOWN_LABEL'
        row['english'] = row['English_city_label']
        row['file_path'] = stage.ARM
        row['context'] = 'Town field in the original hostess catalogue and complete-name drawer.'
        row['speaker'] = row['current_primary']
        row['source_meaning'] = f'The original town or regional label for {row["speaker"]} is {row["english"]}.'
        row['localization_note'] = row['reason']
        row['registered_reference'] = dict(candidate_sha256=sha, table_field=row['current_ALIGNED_field'], pointer=row['current_pointer'],
            exact_stored_hex=slots[n]['new_hex'] if n in slots else row['current_hex'])
        rows.append(row)
    assert len(rows) == 21 and {r['actor'] for r in rows if r['decision'] == 'revision'} == set(LABELS)
    payload = reviewed | dict(records=rows, candidate_sha256=sha, previous_candidate_sha256=prior['candidate_sha256'],
        encoder='dialogue-relocatable-v1', storage_transform='plan_arm9_name_fields', native_name_line_cases=panels,
        reviewed_native_sheet_sha256=VIEWED,
        exact_postboot_label_getters=deployed, checked_story_format_guard=checked,
        visual_scope='Original name-line draws on controlled bitmaps. Full name panel unvisited during ordinary gameplay.')
    validate_natural_dialogue_batch(payload)
    return staged, payload


def main():
    before_registry, before_ledger = base.REGISTRY.read_bytes(), base.LEDGER.read_bytes()
    registry, ledger, manifest, prior = map(base.load, (base.REGISTRY, base.LEDGER, parent.MANIFEST, parent.RELEASE))
    assert base.digest(base.REGISTRY) == prior['registry_sha256'] and base.digest(parent.MANIFEST) == prior['manifest_sha256']
    assert ledger['current_integrated_candidate']['sha256'] == prior['candidate_sha256']
    assert ledger['records_editorially_completed'] == 27700 and not ledger['full_goal_complete']
    assert len(registry['accepted_layers']) == 114 and PROFILE not in registry['profiles']
    assert len(manifest['batches']) == 820 and len(manifest['checks']) == 155 and all(manifest['checks'].values())
    profile = deepcopy(registry['profiles'][prior['profile']])
    staged, review = verify(prior, profile['source25_multiarchive_guard'])
    reg_tmp = base.REGISTRY.with_name('release_stack.barmaid_town_labels.pending.json')
    ledger_tmp = base.LEDGER.with_name('editorial_review_current.barmaid_town_labels.pending.json')
    assert not any(path.exists() for path in (ROOT, PACKAGE, DOC, reg_tmp, ledger_tmp))
    main_sha = base.digest(base.PROMOTED)
    ROOT.mkdir()
    VERIFY.mkdir(parents=True)
    make_xdelta(stage.CLEAN, stage.ROM, PATCH)
    apply_xdelta(stage.CLEAN, PATCH, ROM)
    sha = base.digest(ROM)
    assert sha == review['candidate_sha256'] and ROM.read_bytes() == stage.ROM.read_bytes()
    for path in (stage.STORED, stage.DEPLOYED, BOOT, QA, stage.SHEET):
        copyfile(path, VERIFY / path.name)
        assert base.digest(path) == base.digest(VERIFY / path.name)
    base.save(REVIEW, review)

    backup = ROOT / 'release_stack_before_barmaid_town_labels.json'
    backup.write_bytes(before_registry)
    lineage = {key: prior[key] for key in ('profile', 'candidate', 'candidate_sha256', 'manifest', 'manifest_sha256', 'registry_sha256')}
    lineage['registry'] = str(backup)
    profile.update(verified_square_rumors_predecessor=lineage, barmaid_town_label_release=str(REVIEW))
    registry['profiles'][PROFILE] = profile
    base.save(reg_tmp, registry)
    manifest.update(profile=PROFILE, candidate_rom=str(ROM), candidate_sha256=sha, release_stack_sha256=base.digest(reg_tmp))
    manifest['batches'].append(str(REVIEW))
    manifest['checks'][CHECK] = True
    assert stage.ARM in manifest['changed_paths']
    manifest['changed_records'][stage.ARM].extend(f'ACTOR_{n}_TOWN_LABEL' for n in LABELS)
    manifest['barmaid_town_label_pipeline'] = dict(predecessor=lineage, registered_review=str(REVIEW),
        review_sha256=base.digest(REVIEW), producer=stage.__file__, producer_sha256=base.digest(stage.__file__),
        registered_driver=__file__, registered_driver_sha256=base.digest(__file__), complete_parent_inverse=True,
        owned_ARM9_fields=staged['plan']['fields'])
    base.save(MANIFEST, manifest)
    boot = VERIFY / BOOT.name
    release = prior | dict(profile=PROFILE, candidate=str(ROM), candidate_sha256=sha, patch=str(PATCH), patch_sha256=base.digest(PATCH),
        manifest=str(MANIFEST), manifest_sha256=base.digest(MANIFEST), registry_sha256=base.digest(reg_tmp), predecessor=lineage,
        target_ARM9_sha256=staged['target_ARM9_sha256'], registered_manifest_entries=821, passing_release_checks=156,
        own_registered_startup=str(boot), own_registered_startup_sha256=base.digest(boot), changed_components=[stage.ARM],
        changed_internal_files=[], repository_tests=70, new_contextual_records=0, prose_revisions=0, name_label_revisions=2,
        justified_retentions=19, reviewed_UI_labels=21, actual_verification_scope=dict(actual_emulator=True, own_startup_only=True,
            offline_complete_changed_name_planes=4, ordinary_name_panel_gameplay=False, hardware=False))
    base.save(RELEASE, release)
    base.save(PACKAGE / 'release_manifest.json', release | {'user_acceptance_pending': True})
    archive_file(MANIFEST.read_bytes(), PACKAGE / 'build_manifest.json.gz')
    archive_file(reg_tmp.read_bytes(), PACKAGE / 'build_release_stack.json.gz')
    archive_file(before_ledger, ROOT / 'editorial_ledger_before.json.gz')
    pending = ledger['pending_shared_consumer_checkpoint_20261114']
    assert pending['remaining_total'] == 276 and pending['candidate_sha256'] == prior['candidate_sha256']
    pending['candidate_sha256'] = sha
    checkpoint = 'Nelly’s Alexandria and Verisa’s Sao Jorge town labels are registered.'
    ledger['current_integrated_candidate'].update(path=str(ROM), sha256=sha, profile=PROFILE, patch=str(PATCH),
        patch_sha256=release['patch_sha256'], manifest=str(MANIFEST), manifest_sha256=release['manifest_sha256'],
        ARM9_sha256=release['target_ARM9_sha256'], registered_release_verification=str(RELEASE))
    ledger['barmaid_town_labels_20261115'].update(registered_candidate_sha256=sha, registered_review=str(REVIEW),
        registered_release=str(RELEASE), ordinary_name_panel_gameplay_unvisited=[195, 204])
    ledger['latest_checkpoint'] = checkpoint
    write_pending(ledger_tmp, encode_ledger(ledger))

    receipt = dict(registry_before=sha256(before_registry).hexdigest(), registry_after=base.digest(reg_tmp),
        ledger_before=sha256(before_ledger).hexdigest(), ledger_after=base.digest(ledger_tmp), main_sha256=main_sha)
    base.save(VERIFY / 'registration_mutation_plan.json', receipt)
    (PACKAGE / 'README.md').write_text(f"""# Hostess Town Labels test candidate

The [local ROM](../../{ROM.as_posix()}) localizes the town fields attached to Nelly and Verisa.
The [clean-input patch](translation.xdelta) reconstructs SHA-256 `{sha}` byte for byte. It awaits hardware testing and acceptance for main.
""", encoding='utf-8', newline='\n')
    base.save(PACKAGE / 'checksums.json', package_checksums(PACKAGE))
    assert base.digest(base.REGISTRY) == receipt['registry_before'] and base.digest(base.LEDGER) == receipt['ledger_before']
    assert base.digest(base.PROMOTED) == main_sha
    reg_tmp.replace(base.REGISTRY)
    try:
        ledger_tmp.replace(base.LEDGER)
    except OSError:
        base.replace_checked(base.REGISTRY, before_registry)
        raise
    assert base.digest(base.REGISTRY) == receipt['registry_after'] and base.digest(base.LEDGER) == receipt['ledger_after']
    pins = Path('translations/rom_retention_pins.json')
    existing = base.load(pins)
    for path in (ROM, stage.ROM):
        absolute = str(path.resolve())
        assert not any(row['path'] == absolute for row in existing)
        existing.append(dict(path=absolute, reason=f'Preserve the verified hostess town labels candidate. SHA256 {sha}'))
    base.replace_checked(pins, (dumps(existing, ensure_ascii=False, indent=2) + '\n').replace('\n', '\r\n').encode())
    base.replace_checked(DOC, f"""# Registered hostess town labels

**Nelly Alexandria** and **Verisa Sao Jorge** pass both original name drawers. The initialized offline test uses the original actor getters, source branch logic and renderer. All four revised bitmap masks match the complete ASCII lettering and blank pixels. All eight current and revised samples received visual review. [Renderer comparison](../{(VERIFY / stage.SHEET.name).as_posix()})

The candidate cold boot matched six startup frames and 24 protected name getters. The resulting emulator snapshot contains both revised strings. Five original name getters per hostess return the expected town, joined name and personal name. Ordinary activation of the complete name panels and hardware remain unvisited. Seventy focused tests passed. Ten historical fleet-name cases in the initial run required an unavailable V148 ROM fixture.

The [registered ROM and exact clean-input patch](../{PACKAGE.as_posix()}/README.md) preserve all 114 accepted layers. Only two fixed ARM9 name slots changed. The [review ledger](../{REVIEW.as_posix()}) includes 19 justified retentions. The count remains 27,700 credited reviews and 276 mapped shared records to review or classify.
""".encode())
    prefix = f"# Current editorial checkpoint - 2026-11-15\n\n{checkpoint} [Checkpoint]({DOC.name})\n\n".encode()
    for name in ('editorial_handoff_current.md', 'translation_progress.md', 'build_continuity_protocol.md'):
        path = Path('docs') / name
        base.replace_checked(path, prefix + path.read_bytes())
    print(f'Registered {sha}. 821 entries, 114 accepted layers, 156 checks.')


if __name__ == '__main__':
    main()
