"""Register the verified Sailor Info text-display correction and clean-input patch."""

from gzip import decompress
from json import loads
from pathlib import Path
from xml.etree import ElementTree

from dk4tool.patch.xdelta import apply_xdelta, make_xdelta
from scripts import register_rafael_early_wraps_20261111 as parent
from scripts import stage_sailor_stat_labels_20261114 as stage
from scripts import verify_sailor_stat_labels_20261114 as live
from scripts.prepare_all_routes_promotion_20261111 import package_checksums, verify_runtime
from scripts.verify_release_baseline import files


base = stage.base
ROOT = Path('out/sailor_stat_labels_registered_20261114_v1')
ROM = ROOT / 'Translation_DS_All_Routes_Sailor_Stat_Labels_20261114_candidate.nds'
MANIFEST = ROM.with_suffix('.manifest.json')
PACKAGE = Path('releases/all_routes_editorial_20261114_sailor_stat_labels_candidate')
PATCH, VERIFICATION = PACKAGE / 'translation.xdelta', PACKAGE / 'verification'
RELEASE = VERIFICATION / 'registered_release_verification.json'
PROFILE = 'all-routes-sailor-stat-labels-v1-20261114'
CHECK = 'registered_sailor_stat_label_selection_and_complete_parent_inverse'
STAGED = stage.ROOT / 'stage.json'
STARTUP = stage.ROOT / 'own_startup_verification.json'
QA = live.WORK / 'repository_qa.xml'
VIEWED = '142f8b6fcc9bae68d50ebfdce040c94e660ce2ef7a8bf3a7e37d421b3b977cca'


def verified_inputs():
    previous, staged, gameplay, startup = map(base.load, (parent.RELEASE, STAGED, live.OUTPUT, STARTUP))
    assert base.digest(parent.ROM) == previous['candidate_sha256'] == staged['parent_sha256']
    assert base.digest(stage.ROM) == staged['sha256'] == gameplay['candidate_sha256'] == startup['candidate_sha256']
    assert base.digest(parent.MANIFEST) == previous['manifest_sha256']
    assert base.digest(parent.stage.CLEAN) == previous['clean_input_sha256']
    assert gameplay['complete_plaque_masks'] == 72 and gameplay['all_non_plaque_frame_pixels_exact']
    assert gameplay['all_original_skill_attribute_pairs_exact']
    assert base.digest(gameplay['sheet']) == gameplay['sheet_sha256'] == VIEWED
    assert startup['cold_boot'] and not startup['savestate'] and startup['complete_deployed_payload_exact']
    assert len(startup['exact_matching_frames']) == 6 and len(startup['original_protected_name_getters']) == 24
    for dependencies in (gameplay['dependencies'], startup['evidence']):
        assert all(base.digest(path) == expected for path, expected in dependencies.items())
    suites = list(ElementTree.parse(QA).iter('testsuite'))
    assert sum(int(row.get('tests', '0')) for row in suites) == 22
    assert not any(int(row.get(key, '0')) for row in suites for key in ('errors', 'failures', 'skipped'))
    original, target, clean = map(base.NdsImage.open, (parent.ROM, stage.ROM, parent.stage.CLEAN))
    before, after = files(original), files(target)
    assert before.keys() == after.keys()
    assert {key for key in before if before[key] != after[key]} == {stage.ARM, stage.ART}
    arm, words = stage.change_arm(before[stage.ARM], clean.read_file(stage.ARM))
    art, rows = stage.clear_labels(before[stage.ART])
    assert arm == after[stage.ARM] and words == staged['words']
    assert art == after[stage.ART] and rows == staged['stripped_plaques']
    verify_runtime(arm, previous)
    for path in (stage.ARM, stage.ART):
        target.replace_file(path, before[path])
    assert bytes(target.rom.save()) == parent.ROM.read_bytes()
    return previous, staged


def main():
    import copy
    import json
    from shutil import copyfile

    previous, staged = verified_inputs()
    before_registry, before_ledger = base.REGISTRY.read_bytes(), base.LEDGER.read_bytes()
    registry, ledger, manifest = map(base.load, (base.REGISTRY, base.LEDGER, parent.MANIFEST))
    archived = decompress((parent.PACKAGE / 'build_release_stack.json.gz').read_bytes())
    assert stage.sha256(archived).hexdigest() == previous['registry_sha256']
    build_registry = loads(archived)
    assert build_registry.keys() == registry.keys()
    assert all(build_registry[key] == registry[key] for key in registry if key != 'latest_promoted_build')
    promoted = base.load(base.PROMOTED)
    promotion = registry['latest_promoted_build']
    assert promoted['main_build'] and promotion['main_build']
    assert all(promoted[key] == promotion[key] for key in ('profile', 'rom_sha256', 'git_tag'))
    assert base.digest(promoted['rom']) == promoted['rom_sha256']
    main_sha = base.digest(base.PROMOTED)
    assert len(registry['accepted_layers']) == 114 and PROFILE not in registry['profiles']
    assert len(manifest['batches']) == 784 and len(manifest['checks']) == 119 and all(manifest['checks'].values())
    assert ledger['records_editorially_completed'] == 27697 and not ledger['full_goal_complete']
    assert ledger['current_integrated_candidate']['sha256'] == previous['candidate_sha256']
    pending_registry = base.REGISTRY.with_name('release_stack.sailor_stat_labels.pending.json')
    pending_ledger = base.LEDGER.with_name('editorial_review_current.sailor_stat_labels.pending.json')
    assert not any(path.exists() for path in (ROOT, PACKAGE, pending_registry, pending_ledger))
    ROOT.mkdir()
    VERIFICATION.mkdir(parents=True)
    make_xdelta(parent.stage.CLEAN, stage.ROM, PATCH)
    apply_xdelta(parent.stage.CLEAN, PATCH, ROM)
    sha = base.digest(ROM)
    assert sha == staged['sha256'] and ROM.read_bytes() == stage.ROM.read_bytes()
    for path in (STAGED, live.OUTPUT, STARTUP, QA):
        copyfile(path, VERIFICATION / path.name)
        assert base.digest(path) == base.digest(VERIFICATION / path.name)
    lineage = {key: previous[key] for key in ('profile', 'candidate', 'candidate_sha256', 'manifest', 'manifest_sha256', 'registry_sha256')}
    registry_backup = ROOT / 'release_stack_before_sailor_stat_labels.json'
    registry_backup.write_bytes(before_registry)
    lineage['registry'] = str(parent.PACKAGE / 'build_release_stack.json.gz')
    lineage['registry_compression'] = 'gzip'
    contract = VERIFICATION / STAGED.name
    profile = copy.deepcopy(registry['profiles'][previous['profile']])
    profile.update(verified_rafael_early_wraps_predecessor=lineage, sailor_stat_label_display_contract=str(contract))
    registry['profiles'][PROFILE] = profile
    base.save(pending_registry, registry)
    manifest.update(profile=PROFILE, candidate_rom=str(ROM), candidate_sha256=sha,
                    release_stack_sha256=base.digest(pending_registry))
    manifest['batches'].append(str(contract))
    manifest['checks'][CHECK] = True
    manifest['sailor_stat_label_display_pipeline'] = dict(predecessor=lineage,
        producer=stage.__file__, producer_sha256=base.digest(stage.__file__),
        verification=str(live.OUTPUT), verification_sha256=base.digest(live.OUTPUT),
        whole_parent_inverse_exact=True, changed_paths=[stage.ARM, stage.ART],
        working_predecessor_registry_sha256=base.digest(registry_backup))
    for path in (stage.ARM, stage.ART):
        assert path in manifest['changed_paths']
        manifest['changed_records'][path].append('DK4_SAILOR_STAT_LABEL_SELECTION_20261114')
    assert len(manifest['batches']) == 785 and len(manifest['checks']) == 120
    base.save(MANIFEST, manifest)
    startup = VERIFICATION / STARTUP.name
    release = previous | dict(profile=PROFILE, candidate=str(ROM), candidate_sha256=sha,
        patch=str(PATCH), patch_sha256=base.digest(PATCH), manifest=str(MANIFEST), manifest_sha256=base.digest(MANIFEST),
        registry_sha256=base.digest(pending_registry), predecessor=lineage,
        target_ARM9_sha256=staged['ARM9_sha256'], target_PersonInfo_PXL_sha256=staged['asset_sha256'],
        registered_manifest_entries=785, passing_release_checks=120, repository_tests=22,
        own_registered_startup=str(startup), own_registered_startup_sha256=base.digest(startup),
        changed_components=[stage.ARM], changed_internal_files=[stage.ART], prose_revisions=0,
        justified_retentions=0, reviewed_UI_labels=6, actual_verification_scope=dict(
            actual_emulator=True, hardware=False, complete_plaque_masks=72,
            selected_skills=10, normal_and_restored_states=2, same_pixels_outside_plaques=True))
    base.save(RELEASE, release)
    base.save(PACKAGE / 'release_manifest.json', release | {'user_acceptance_pending': True})
    parent.precedent.prior.prior.archive_file(MANIFEST.read_bytes(), PACKAGE / 'build_manifest.json.gz')
    parent.precedent.prior.prior.archive_file(pending_registry.read_bytes(), PACKAGE / 'build_release_stack.json.gz')
    parent.precedent.prior.prior.archive_file(before_ledger, ROOT / 'editorial_ledger_before.json.gz')
    ledger['current_integrated_candidate'].update(path=str(ROM), sha256=sha, profile=PROFILE, patch=str(PATCH),
        patch_sha256=release['patch_sha256'], manifest=str(MANIFEST), manifest_sha256=release['manifest_sha256'],
        registered_release_verification=str(RELEASE))
    ledger['latest_checkpoint'] = 'Sailor Info stat label selection is registered.'
    ledger['sailor_stat_label_selection_20261114'] = dict(release=str(RELEASE), new_dialogue_credit=0,
        gameplay=str(VERIFICATION / live.OUTPUT.name), existing_labels_preserved=6)
    contract_tools = parent.precedent.prior.prior
    contract_tools.write_pending(pending_ledger, contract_tools.encode_ledger(ledger))
    receipt = dict(registry_before=stage.sha256(before_registry).hexdigest(), registry_after=base.digest(pending_registry),
        ledger_before=stage.sha256(before_ledger).hexdigest(), ledger_after=base.digest(pending_ledger), main_sha256=main_sha)
    base.save(VERIFICATION / 'registration_mutation_plan.json', receipt)
    (PACKAGE / 'README.md').write_text('# Sailor Info stat labels candidate\n\n'
        f'The [local ROM](../../{ROM.as_posix()}) restores clean stat labels while checking skills. '
        f'The [clean-input patch](translation.xdelta) reconstructs SHA-256 `{sha}` byte for byte. '
        'This cumulative candidate awaits hardware testing and acceptance for main.\n', encoding='utf-8')
    base.save(PACKAGE / 'checksums.json', package_checksums(PACKAGE))
    assert base.digest(base.REGISTRY) == receipt['registry_before'] and base.digest(base.LEDGER) == receipt['ledger_before']
    assert base.digest(base.PROMOTED) == main_sha
    pending_registry.replace(base.REGISTRY)
    try:
        pending_ledger.replace(base.LEDGER)
    except OSError:
        base.replace_checked(base.REGISTRY, before_registry)
        raise
    assert base.digest(base.REGISTRY) == receipt['registry_after'] and base.digest(base.LEDGER) == receipt['ledger_after']
    pin_path = Path('translations/rom_retention_pins.json')
    pins = base.load(pin_path)
    for node in (ROM, stage.ROM):
        pins.append(dict(path=str(node.resolve()), reason=f'Preserve Sailor Info label fix. SHA256 {sha}'))
    base.replace_checked(pin_path, (json.dumps(pins, ensure_ascii=False, indent=2) + '\n').replace('\n', '\r\n').encode())
    print(f'Registered {ROM} | SHA-256 {sha} | 785 entries, 114 accepted layers and 120 checks.')


if __name__ == '__main__':
    main()
