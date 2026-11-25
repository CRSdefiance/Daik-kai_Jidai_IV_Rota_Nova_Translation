"""Register the checked scene while retaining all six existing final runtime/data stages."""
import os
from copy import deepcopy
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.audit_story_glyph_consistency import load, save

ROOT = Path('work/analysis/Hodram_B171_B190_release_20261104')
PROFILE = 'all-routes-hodram-b171-b190-static-text-20261104'
OLD = 'all-routes-hodram-b151-b170-static-text-20261102'
CONFIG = Path('translations/hodram_B171_B190_editorial_release_v1.json')
MODULE = Path('dk4tool/patch/reviewed_scene_batch_v8.py')
FINAL = Path('translations/hodram_B171_B190_contextual_final_review_v1.json')
CHECKED = Path('work/analysis/Hodram_B171_B190_checked_20261104')
INPUT = Path('work/analysis/Hodram_B171_B190_storage_inputs_20261104')
REBUILT = Path('work/analysis/Hodram_B171_B190_rebuilt_20261104/reconstruction.json')
PIXELS = Path('work/analysis/Hodram_B171_B190_actual_pixels_v2_20261104/focused_actual_pixels.json')


if __name__ == '__main__':
    assert not ROOT.exists() and not CONFIG.exists()
    registry_path = Path('translations/release_stack.json')
    before = registry_path.read_bytes()
    assert sha(before) == '7e7288fe7920fb601ab96a6bde937793c2c9873dd6a9573be796853d7924d143'
    registry = load(registry_path)
    assert PROFILE not in registry['profiles'] and len(registry['accepted_layers']) == 114
    profile = deepcopy(registry['profiles'][OLD])
    keys = ['ascii_glyph_right_bounds', 'owned_name_glyph', 'owned_name_fields', 'owned_name_fields_next', 'owned_name_fields_grouped', 'owned_static_text']
    old_configs = [load(profile[k]) for k in keys]
    manifest_path = Path('out/all_routes_combined_hodram_b151_b170_static_text_20261102_candidate.manifest.json')
    manifest = load(manifest_path)
    specs = [('production_pipeline', 'canonical_stage'), ('owned_name_production_pipeline', 'post_bounds_stage'),
        ('owned_fields_production_pipeline', 'post_Emilio_stage'), ('next_owned_fields_production_pipeline', 'post_prior_fields_stage'),
        ('grouped_owned_fields_production_pipeline', 'post_next_fields_stage'), ('static_text_production_pipeline', 'post_grouped_fields_stage')]
    stages = [Path(manifest[a][b]) for a, b in specs]
    rebuilt, doc, pixels = map(load, [REBUILT, FINAL, PIXELS])
    assert all(all(r['review'].values()) for r in doc['records']) and len(doc['records']) == 435
    parent = Path(rebuilt['parent'])
    assert sha(parent.read_bytes()) == manifest['candidate_sha256'] == '7774721fdc6da677f56a75a7350785f3cc5e90759c6784527b3c144fa77b0399'
    old_states = stages + [parent]
    for index, conf in enumerate(old_configs):
        assert sha(old_states[index].read_bytes()) == conf['parent_ROM_sha256']
        assert sha(old_states[index + 1].read_bytes()) == conf['target_ROM_sha256']
    target_archive = Path(rebuilt['target_archive']).read_bytes()
    assert sha(target_archive) == rebuilt['target_archive_sha256']
    ROOT.mkdir()
    (ROOT / 'release_stack_before.json').write_bytes(before)
    targets = []
    for index, old in enumerate(stages):
        original = NdsImage.open(old)
        target = NdsImage.open(old)
        target.replace_file(doc['file_path'], target_archive)
        assert [p for _, p, v in original.iter_files() if target.read_file(p) != v] == [doc['file_path']]
        assert all(target.read_file(p) == v for p, v in original.iter_components())
        path = ROOT / f'stage_{index}_RESEARCH_REFERENCE.nds'
        target.save(path)
        restored = NdsImage.open(path)
        restored.replace_file(doc['file_path'], original.read_file(doc['file_path']))
        assert bytes(restored.rom.save()) == old.read_bytes()
        targets.append(path)
    final_target = Path(rebuilt['research_ROM'])
    assert sha(final_target.read_bytes()) == rebuilt['research_ROM_sha256']
    expected_final = NdsImage.open(parent)
    expected_final.replace_file(doc['file_path'], target_archive)
    assert bytes(expected_final.rom.save()) == final_target.read_bytes()
    targets.append(final_target)
    visual_path = ROOT / 'release_visual_review.json'
    save(visual_path, dict(pages=439, all_final_pages_directly_viewed_or_exact_plane_reuse=True,
        approved='work/analysis/Hodram_B171_B190_formatting_20261102/speech_display_approved_20261104/visual_approval.json',
        complete_stored_parity_planes_equal_viewed_pages=True))
    FE_path = ROOT / 'FE_final_layout_check.json'
    save(FE_path, dict(FE_records=28, findings=[], unexpected_blank_rows_orwraps_absent=True,
        means_visible_glyph_rows_andcomplete_pixel_planes=True, four_initial_row_defects_corrected=True,
        exact_owned_terminal_zeroink_case='DK4_MES_B179_R0047',
        source_qualification='work/analysis/Hodram_B171_B190_stored_FE_diagnostic_20261104/diagnostic.json',
        stored_parity_proof='work/analysis/Hodram_B171_B190_stored_qualified_20261104/stored_native_verification.json',
        actual_same_case_observed=True, no_new_rendering_run=True))
    menu_path = ROOT / 'release_menu_proof.json'
    menu = load(INPUT / 'menus_reviewed.json')
    menu.update(actual_controller_andstored_objects_still_pending=False, both_indices_anddistinct_responses_observed=True)
    save(menu_path, menu)
    style_path = ROOT / 'no_style_proof.json'
    save(style_path, load(INPUT / 'no_style_objects.json'))
    evidence = dict(manuscript=FINAL, plan=CHECKED / 'release_plans.json', reconstruction=REBUILT,
        stored_native=Path('work/analysis/Hodram_B171_B190_stored_qualified_20261104/stored_native_verification.json'),
        loaders=Path('work/analysis/Hodram_B171_B190_loaders_20261104/verification.json'), actual=CHECKED / 'actual_review.json',
        visual_review=visual_path, typed_menu=menu_path, native_styles=style_path, focused_pixels=PIXELS, FE_layout=FE_path,
        scoped_names=Path('translations/hodram_B171_B190_scoped_names_final_v1.json'))
    dependencies = [*evidence.values(), CHECKED / 'actual_visual_review.json', Path(rebuilt['packet']), Path(rebuilt['native']), MODULE,
        Path('dk4tool/patch/reviewed_scene_batch_v5.py'), Path('dk4tool/script/reviewed_scene_rebuild_v3.py'),
        Path('dk4tool/dialogue/reviewed_choice_object_v2.py'), Path('dk4tool/dialogue/reviewed_two_choice_object_v1.py'),
        Path('scripts/source_locked_derivation_v5118.py'), Path('scripts/finalize_hodram_B171_B190_review.py'),
        Path('scripts/analyze_hodram_B171_B190_actual.py'), Path('scripts/analyze_hodram_B171_B190_actual_v2.py'),
        Path('scripts/check_hodram_B171_B190_stored_qualified.py'), Path(__file__)]
    runtime_path = Path('translations/ascii_glyph_right_bounds_hodram_B171_B190_v1.json')
    conf = dict(format='dk4-reviewed-scene-release-v8', **{k: str(v) for k, v in evidence.items()},
        record_count=435, speech_count=433, ordinary_count=433, style_count=0, typed_choice_count=2,
        reviewed_blocks=doc['blocks'], blocks=rebuilt['changed_blocks'], native_pages=439, relative_cases=390,
        FE_count=28, menu_alignments=6, menu_returns=18, menu_planes=8, style_slots=0, scoped_name_count=49,
        actual_frames=85005, actual_runs=5, actual_sheets=8,
        focused_pixel_counts={k: len(pixels[k]) for k in ['body_pages', 'name_headers', 'menu_samples']},
        canonical_ROM_sha256=sha(Path('out/raphael_natural_v2_accepted_base.nds').read_bytes()),
        clean_ROM='work/clean.nds', clean_ROM_sha256=sha(Path('work/clean.nds').read_bytes()),
        parent_ROM_sha256=sha(stages[0].read_bytes()), target_ROM_sha256=sha(targets[0].read_bytes()),
        pre_runtime_reference_ROM=str(targets[0]), pre_runtime_ARM9_sha256=sha(NdsImage.open(stages[0]).read_file('/__arm9__.bin')),
        right_bound_configuration=str(runtime_path), dependencies={str(p): sha(p.read_bytes()) for p in dependencies})
    save(CONFIG, conf)
    profile['late_editorial_extensions'].append(dict(id='hodram-b171-b190', module='dk4tool.patch.reviewed_scene_batch_v8',
        module_sha256=sha(MODULE.read_bytes()), config=str(CONFIG), config_sha256=sha(CONFIG.read_bytes()),
        parent_ROM_sha256=conf['parent_ROM_sha256'], target_ROM_sha256=conf['target_ROM_sha256']))
    contract = deepcopy(load(old_configs[0]['parent_manifest']))
    contract['batches'].append(str(FINAL))
    contract.update(expected_candidate_sha256=conf['target_ROM_sha256'], predecessor_manifest=str(manifest_path),
        predecessor_manifest_sha256=sha(manifest_path.read_bytes()), new_extension_configs=[str(CONFIG)])
    contract_path = ROOT / 'expected_canonical_manifest_contract.json'
    save(contract_path, contract)
    paths = [runtime_path, Path('translations/emilio_name_glyph_hodram_B171_B190_release_v1.json'),
        Path('translations/fernando_samwell_hodram_B171_B190_release_v1.json'), Path('translations/follower_diogo_hodram_B171_B190_release_v1.json'),
        Path('translations/geronimo_vasquez_alonso_hodram_B171_B190_release_v1.json'), Path('translations/abkhaz_elysion_hodram_B171_B190_release_v1.json')]
    assert not any(p.exists() for p in paths)
    for index, (old, path) in enumerate(zip(old_configs, paths, strict=True)):
        value = deepcopy(old)
        value.update(parent_ROM_sha256=sha(targets[index].read_bytes()), target_ROM_sha256=sha(targets[index + 1].read_bytes()))
        if index == 0:
            value['parent_manifest'] = str(contract_path)
            value['builder_dependencies'][str(MODULE)] = sha(MODULE.read_bytes())
        save(path, value)
    profile.update(dict(zip(keys, map(str, paths))))
    profile.update(note='Experimental cumulative435-review successor:195 revisions/240 retentions;439 pages/15 layout fixes. Preserve114 accepted layers, all prior profiles and all six runtime/name/static stages. Use build_integrated_release_with_static_text.py;main acceptance required. No guide photos;full objective active.')
    registry['profiles'][PROFILE] = profile
    assert all(registry[k] == v for k, v in load(ROOT / 'release_stack_before.json').items() if k != 'profiles')
    assert all(registry['profiles'][k] == v for k, v in load(ROOT / 'release_stack_before.json')['profiles'].items())
    assert registry_path.read_bytes() == before
    staged = registry_path.with_name('release_stack.pending_B171_B190.json')
    assert not staged.exists()
    save(staged, registry)
    os.replace(staged, registry_path)
    save(ROOT / 'registered_preparation.json', dict(profile=PROFILE, config=str(CONFIG), preserved_stage_configs=dict(zip(keys, map(str, paths))),
        canonical_parent=str(stages[0]), canonical_parent_sha256=conf['parent_ROM_sha256'],
        stage_targets=[dict(path=str(p), sha256=sha(p.read_bytes())) for p in targets],
        pre_runtime_ROM=str(targets[0]), pre_runtime_ROM_sha256=conf['target_ROM_sha256'], post_grouped_ROM=str(targets[5]),
        static_config=str(paths[5]), final_ROM=str(final_target), target_ROM_sha256=sha(final_target.read_bytes()),
        registry_sha256=sha(registry_path.read_bytes()), accepted_layers=114, previous_profiles_preserved=True,
        all_prior_drivers_anddata_qualification_dependencies_unchanged=True, new_credit=0, main_unchanged=True))
    pins_path = Path('translations/rom_retention_pins.json')
    pins_before = pins_path.read_bytes()
    pins = load(pins_path)
    (ROOT / 'pins.before.json').write_bytes(pins_before)
    pins += [dict(path=str(p.resolve()), reason='Preserve exact B171–B190 registered stage reference; no pruning.') for p in targets[:-1]]
    pin_stage = pins_path.with_name('rom_retention_pins.B171_release.pending.json')
    assert not pin_stage.exists()
    save(pin_stage, pins)
    assert pins_path.read_bytes() == pins_before
    os.replace(pin_stage, pins_path)
    print('Registered experimental435-review profile;114 accepted layers/all prior profiles and six final stages preserved. Production qualification/build pending; no credit or promotion.')
