"""Append reviewed scenes, preserve every runtime/name stage, then owned static text."""
from copy import deepcopy
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.audit_story_glyph_consistency import load, save

ROOT = Path('work/analysis/Hodram_B151_B170_release_20261102')
PROFILE = 'all-routes-hodram-b151-b170-static-text-20261102'
OLD = 'all-routes-hodram-b131-b150-names-20261102'
CONFIG = Path('translations/hodram_B151_B170_editorial_release_v1.json')
MODULE = Path('dk4tool/patch/reviewed_scene_batch_v7.py')
FINAL = Path('translations/hodram_B151_B170_contextual_final_review_v1.json')
CHECKED = Path('work/analysis/Hodram_B151_B170_checked_20261102')


def main():
    assert not ROOT.exists() and not CONFIG.exists()
    registry_path = Path('translations/release_stack.json')
    before = registry_path.read_bytes()
    assert sha(before) == 'dde90af7920d7562851e16858cb9fef923d25268691c8d9fa1ced156ecd9265a'
    registry = load(registry_path)
    assert PROFILE not in registry['profiles'] and len(registry['accepted_layers']) == 114
    profile = deepcopy(registry['profiles'][OLD])
    keys = ['ascii_glyph_right_bounds', 'owned_name_glyph', 'owned_name_fields', 'owned_name_fields_next', 'owned_name_fields_grouped']
    configs = [load(profile[k]) for k in keys]
    manifest_path = Path('out/all_routes_combined_hodram_b131_b150_names_20261102_candidate.manifest.json')
    manifest = load(manifest_path)
    stage_specs = [('production_pipeline', 'canonical_stage'), ('owned_name_production_pipeline', 'post_bounds_stage'),
        ('owned_fields_production_pipeline', 'post_Emilio_stage'), ('next_owned_fields_production_pipeline', 'post_prior_fields_stage'),
        ('grouped_owned_fields_production_pipeline', 'post_next_fields_stage')]
    stages = [Path(manifest[k][v]) for k, v in stage_specs]
    rebuilt_path = Path('work/analysis/Hodram_B151_B170_rebuilt_20261102/reconstruction.json')
    reference_path = Path('work/analysis/Hodram_B151_B170_focused_20261102/research_reference.json')
    rebuilt, reference, doc = map(load, [rebuilt_path, reference_path, FINAL])
    assert sha(Path(rebuilt['parent']).read_bytes()) == manifest['candidate_sha256'] == '7fb6f6d78441a705c137003d8bfc92d4f5b43fd56b85178a59224f3b4570bc04'
    assert sha(Path(rebuilt['research_ROM']).read_bytes()) == rebuilt['research_ROM_sha256']
    assert sha(Path(reference['research_ROM']).read_bytes()) == reference['research_ROM_sha256']
    parent, story = [NdsImage.open(p) for p in [rebuilt['parent'], rebuilt['research_ROM']]]
    canonical = NdsImage.open(stages[0])
    inverse = deepcopy(parent)
    inverse.replace_file('/__arm9__.bin', canonical.read_file('/__arm9__.bin'))
    assert bytes(inverse.rom.save()) == stages[0].read_bytes()
    ROOT.mkdir(parents=True)
    (ROOT / 'release_stack_before.json').write_bytes(before)
    targets = []
    for name, stage, conf in zip(['canonical', 'post_bounds', 'post_Emilio', 'post_prior_fields', 'post_next_fields'], stages, configs):
        assert sha(stage.read_bytes()) == conf['parent_ROM_sha256']
        variant = deepcopy(story)
        variant.replace_file('/__arm9__.bin', NdsImage.open(stage).read_file('/__arm9__.bin'))
        path = ROOT / (name + '_target_RESEARCH_ONLY.nds')
        path.write_bytes(bytes(variant.rom.save()))
        targets.append(path)
    pre = NdsImage.open(targets[0])
    assert [p for _, p, value in canonical.iter_files() if pre.read_file(p) != value] == ['/data/SC1.DK4']
    assert all(pre.read_file(p) == value for p, value in canonical.iter_components())
    inp = Path('work/analysis/Hodram_B151_B170_reconstruction_inputs_20261102')
    pixels_path = Path('work/analysis/Hodram_B151_B170_actual_pixels_20261102/focused_actual_pixels.json')
    pixels, actual = load(pixels_path), load(CHECKED / 'actual_review.json')
    visual_path = ROOT / 'release_visual_review.json'
    save(visual_path, dict(pages=650, all_final_pages_directly_viewed_or_exact_plane_reuse=True,
        ordinary='work/analysis/Hodram_B151_B170_formatting_20261102/ordinary_visual_review_progress_v3.json',
        cinematic='work/analysis/Hodram_B156_cinematic_English_v4_20261102/visual_review.json',
        complete_stored_parity_planes_equal_viewed_pages=True))
    FE_path = ROOT / 'FE_final_layout_check.json'
    save(FE_path, dict(FE_records=32, findings=[], unexpected_blank_rows_orwraps_absent=True,
        ordinary_FE_records=9, cinematic_FE_records=23, source_staging_rows_deliberate_with_individual_reasons=True,
        observed_cinematic='work/analysis/Hodram_B156_cinematic_English_actual_20261102/observed_English_panels.json'))
    menu_path = ROOT / 'release_menu_proof.json'
    menu = load(inp / 'menus_reviewed.json')
    assert menu['offline_visual_approved'] and not menu['direct_view_pending']
    menu.update(complete_caption_glyphs_centering_bounds_guards_andconsumption_pass=True,
        actual_controller_andstored_objects_still_pending=False,
        representative_long_menu_both_indices_observed=True, other_three_menus_offline_only=True)
    save(menu_path, menu)
    style_path = ROOT / 'no_style_proof.json'
    style = load(inp / 'no_style_objects.json')
    assert style['source_packet_has_zero_4100_commands'] and not style['objects']
    style.update(native_target_slot_cases=0, source_alias_equivalence_exact=True)
    save(style_path, style)
    evidence = dict(manuscript=FINAL, plan=CHECKED / 'release_plans.json', reconstruction=rebuilt_path,
        stored_native=Path('work/analysis/Hodram_B151_B170_stored_20261102/stored_native_verification.json'),
        loaders=Path('work/analysis/Hodram_B151_B170_loaders_20261102/verification.json'),
        actual=CHECKED / 'actual_review.json', visual_review=visual_path, typed_menu=menu_path,
        native_styles=style_path, FE_layout=FE_path, focused_pixels=pixels_path,
        qualified_compiled_plans=inp / 'all634_compiled_plans.json')
    runtime_path = Path('translations/ascii_glyph_right_bounds_hodram_B151_B170_v1.json')
    deps = [*evidence.values(), reference_path, Path(rebuilt['packet']), Path(rebuilt['native']), MODULE,
        Path('dk4tool/patch/reviewed_scene_batch_v5.py'), Path('dk4tool/script/reviewed_scene_rebuild_v3.py'),
        Path('dk4tool/dialogue/reviewed_choice_object_v2.py'), Path('dk4tool/dialogue/reviewed_two_choice_object_v1.py'),
        Path('scripts/source_locked_derivation_v5118.py'), Path('scripts/finalize_hodram_B151_B170_review.py'), Path(__file__)]
    plans = load(evidence['qualified_compiled_plans'])
    conf = dict(format='dk4-reviewed-scene-release-v7', **{k: str(v) for k, v in evidence.items()},
        record_count=642, speech_count=634, ordinary_count=634, style_count=0, typed_choice_count=8,
        reviewed_blocks=doc['blocks'], blocks=rebuilt['changed_blocks'], native_pages=650, relative_cases=700,
        FE_count=32, menu_alignments=24, menu_returns=72, menu_planes=32, style_slots=0,
        source_qualified_cinematic_records=[r['id'] for r in plans['records'] if r.get('individually_documented_automatic_source_staging')],
        actual_frames=43003, actual_runs=3, actual_sheets=6,
        focused_pixel_counts={k: len(pixels[k]) for k in ['body_pages', 'name_headers', 'menu_samples']},
        canonical_ROM_sha256=sha(Path('out/raphael_natural_v2_accepted_base.nds').read_bytes()),
        clean_ROM='work/clean.nds', clean_ROM_sha256=sha(Path('work/clean.nds').read_bytes()),
        parent_ROM_sha256=sha(stages[0].read_bytes()), target_ROM_sha256=sha(targets[0].read_bytes()),
        pre_runtime_reference_ROM=str(targets[0]), pre_runtime_ARM9_sha256=sha(canonical.read_file('/__arm9__.bin')),
        right_bound_configuration=str(runtime_path), dependencies={str(p): sha(p.read_bytes()) for p in deps})
    save(CONFIG, conf)
    profile['late_editorial_extensions'].append(dict(id='hodram-b151-b170', module='dk4tool.patch.reviewed_scene_batch_v7',
        module_sha256=sha(MODULE.read_bytes()), config=str(CONFIG), config_sha256=sha(CONFIG.read_bytes()),
        parent_ROM_sha256=conf['parent_ROM_sha256'], target_ROM_sha256=conf['target_ROM_sha256']))
    contract = deepcopy(load(configs[0]['parent_manifest']))
    contract['batches'].append(str(FINAL))
    contract.update(expected_candidate_sha256=conf['target_ROM_sha256'], predecessor_manifest=str(manifest_path),
        predecessor_manifest_sha256=sha(manifest_path.read_bytes()), new_extension_configs=[str(CONFIG)])
    contract_path = ROOT / 'expected_canonical_manifest_contract.json'
    save(contract_path, contract)
    paths = [runtime_path, Path('translations/emilio_name_glyph_hodram_B151_B170_release_v1.json'),
        Path('translations/fernando_samwell_hodram_B151_B170_release_v1.json'),
        Path('translations/follower_diogo_hodram_B151_B170_release_v1.json'),
        Path('translations/geronimo_vasquez_alonso_hodram_B151_B170_release_v1.json')]
    assert not any(p.exists() for p in paths)
    for index, (old, path) in enumerate(zip(configs, paths)):
        value = deepcopy(old)
        value.update(parent_ROM_sha256=sha(targets[index].read_bytes()),
            target_ROM_sha256=sha(targets[index + 1].read_bytes()) if index < 4 else rebuilt['research_ROM_sha256'])
        if index == 0:
            value['parent_manifest'] = str(contract_path)
            value['builder_dependencies'][str(MODULE)] = sha(MODULE.read_bytes())
        save(path, value)
    profile.update(dict(zip(keys, map(str, paths))))
    static_path = Path('translations/abkhaz_elysion_hodram_B151_B170_release_v1.json')
    native_path = Path(reference['static_qualification'])
    native = load(native_path)
    static_deps = [Path('translations/hodram_B151_B170_scoped_names_final_v1.json'), native_path,
        Path(native['proposal']), evidence['actual'], CHECKED / 'actual_visual_review.json',
        Path('dk4tool/patch/registered_owned_static_text_v1.py'), Path('dk4tool/patch/hodram_static_labels_v1.py'),
        Path('scripts/build_integrated_release_with_static_text.py'), Path('scripts/build_integrated_release_with_grouped_fields.py'),
        Path('scripts/build_integrated_release_with_owned_fields.py'), Path('scripts/source_locked_derivation_v5118.py')]
    save(static_path, dict(format='dk4-registered-owned-static-text-v1', manuscript=str(static_deps[0]),
        proposal=native['proposal'], native=str(native_path), actual=str(evidence['actual']),
        clean_ROM=conf['clean_ROM'], clean_ROM_sha256=conf['clean_ROM_sha256'],
        parent_ROM_sha256=rebuilt['research_ROM_sha256'], target_ROM_sha256=reference['research_ROM_sha256'],
        dependencies={str(p): sha(p.read_bytes()) for p in static_deps}))
    profile.update(owned_static_text=str(static_path), note='Experimental cumulative642-review successor:269 revisions/373 retentions;650 pages/26 layout fixes. Fixed-slot Abkhaz/Elysion data after unchanged grouped-fields pipeline. Use build_integrated_release_with_static_text.py. Preserve114 accepted layers/all prior profiles/runtime/name fixes;main acceptance required. No guide photos;full goal remains.')
    registry['profiles'][PROFILE] = profile
    assert registry_path.read_bytes() == before
    save(registry_path, registry)
    save(ROOT / 'registered_preparation.json', dict(profile=PROFILE, config=str(CONFIG),
        static_config=str(static_path), preserved_stage_configs=dict(zip(keys, map(str, paths))),
        canonical_parent=str(stages[0]), canonical_parent_sha256=conf['parent_ROM_sha256'],
        stage_targets=[dict(path=str(p), sha256=sha(p.read_bytes())) for p in targets],
        pre_runtime_ROM=str(targets[0]), pre_runtime_ROM_sha256=conf['target_ROM_sha256'],
        post_grouped_ROM=rebuilt['research_ROM'], post_grouped_ROM_sha256=rebuilt['research_ROM_sha256'],
        final_ROM=reference['research_ROM'], target_ROM_sha256=reference['research_ROM_sha256'],
        accepted_layers=114, previous_profiles_preserved=True, all_prior_drivers_unchanged=True, new_credit=0, main_unchanged=True))
    pins_path = Path('translations/rom_retention_pins.json')
    pins = load(pins_path)
    pins += [dict(path=str(p.resolve()), reason='Preserve exact B151–B170 registered stage reference; no pruning.') for p in targets]
    save(pins_path, pins)
    print(dict(profile=PROFILE, target=reference['research_ROM_sha256'], registry_sha256=sha(registry_path.read_bytes())))


if __name__ == '__main__':
    main()
