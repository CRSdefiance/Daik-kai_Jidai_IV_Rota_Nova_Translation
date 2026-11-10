"""Register the checked scene and grouped names after every preserved cumulative stage."""
from copy import deepcopy
from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.audit_story_glyph_consistency import load, save

ROOT = Path('work/analysis/Hodram_B131_B150_release_20261102')
PROFILE = 'all-routes-hodram-b131-b150-names-20261102'
OLD_PROFILE = 'all-routes-hodram-b111-b130-names-20261102'
CONFIG = Path('translations/hodram_B131_B150_editorial_release_v1.json')
MODULE = Path('dk4tool/patch/reviewed_scene_batch_v6.py')
FINAL = Path('translations/hodram_B131_B150_contextual_final_review_v1.json')


def main():
    assert not ROOT.exists() and not CONFIG.exists()
    registry_path = Path('translations/release_stack.json')
    before = registry_path.read_bytes()
    assert sha(before) == 'd3cf0000ad4d1a3e4f9df5c0880a001f7449744e5251ced6f613a05d438d076a'
    registry = load(registry_path)
    assert PROFILE not in registry['profiles']
    profile = deepcopy(registry['profiles'][OLD_PROFILE])
    stage_keys = ['ascii_glyph_right_bounds', 'owned_name_glyph', 'owned_name_fields', 'owned_name_fields_next']
    old_configs = [load(profile[k]) for k in stage_keys]
    manifest_path = Path('out/all_routes_combined_hodram_b111_b130_names_20261102_candidate.manifest.json')
    manifest = load(manifest_path)
    stages = [Path(manifest[p][k]) for p, k in [
        ('production_pipeline', 'canonical_stage'), ('owned_name_production_pipeline', 'post_bounds_stage'),
        ('owned_fields_production_pipeline', 'post_Emilio_stage'), ('next_owned_fields_production_pipeline', 'post_prior_fields_stage')]]
    rebuilt_path = Path('work/analysis/Hodram_B131_B150_rebuilt_20261102/reconstruction.json')
    reference_path = Path('work/analysis/Hodram_B131_B150_name_research_20261102/research_reference.json')
    rebuilt, reference, doc = map(load, [rebuilt_path, reference_path, FINAL])
    assert sha(Path(rebuilt['parent']).read_bytes()) == manifest['candidate_sha256'] == 'f2f0bf2fd904ead5d539b25d516d53fa70a0175af145be27751e8d9f6f2ccde2'
    assert sha(Path(rebuilt['research_ROM']).read_bytes()) == rebuilt['research_ROM_sha256']
    assert sha(Path(reference['research_ROM']).read_bytes()) == reference['research_ROM_sha256']
    parent, story = [NdsImage.open(p) for p in [rebuilt['parent'], rebuilt['research_ROM']]]
    canonical = NdsImage.open(stages[0])
    inverse = deepcopy(parent)
    inverse.replace_file('/__arm9__.bin', canonical.read_file('/__arm9__.bin'))
    assert bytes(inverse.rom.save()) == stages[0].read_bytes()
    assert sha(stages[0].read_bytes()) == old_configs[0]['parent_ROM_sha256']
    ROOT.mkdir(parents=True)
    (ROOT / 'release_stack_before.json').write_bytes(before)
    targets = []
    for name, stage in zip(['canonical', 'post_bounds', 'post_Emilio', 'post_prior_fields'], stages):
        variant = deepcopy(story)
        variant.replace_file('/__arm9__.bin', NdsImage.open(stage).read_file('/__arm9__.bin'))
        path = ROOT / (name + '_target_RESEARCH_ONLY.nds')
        path.write_bytes(bytes(variant.rom.save()))
        targets.append(path)
    pre = NdsImage.open(targets[0])
    assert [p for _, p, value in canonical.iter_files() if pre.read_file(p) != value] == ['/data/SC1.DK4']
    assert all(pre.read_file(p) == value for p, value in canonical.iter_components())
    display = Path('work/analysis/Hodram_B131_B150_editorial_20261102')
    visual_source = display / 'visual_review_progress_v7.json'
    visual = load(visual_source)
    assert visual['all_final_speech_pages_approved'] and visual['unresolved_speech_layout_findings'] == 0
    visual.update(pages=328, all_final_pages_directly_viewed_or_exact_plane_reuse=True,
                  original_visual=str(visual_source), original_visual_sha256=sha(visual_source.read_bytes()))
    visual_path = ROOT / 'release_visual_review.json'
    save(visual_path, visual)
    FE_path = display / 'FE_native_row_membership_v1.json'
    FE = load(FE_path)
    assert FE['all_pass'] and FE['original_installed_inside_word_wrap_rejected'] and len(FE['records']) == 23
    FE_review = ROOT / 'FE_final_layout_check.json'
    save(FE_review, dict(FE_records=23, findings=[], unexpected_blank_rows_orwraps_absent=True,
        native_row_membership=str(FE_path), native_row_membership_sha256=sha(FE_path.read_bytes()),
        stored_parity_proof='work/analysis/Hodram_B131_B150_stored_20261102/stored_native_verification.json',
        stored_parity_proof_sha256=sha(Path('work/analysis/Hodram_B131_B150_stored_20261102/stored_native_verification.json').read_bytes()),
        no_new_rendering_run=True, new_credit=0))
    evidence_paths = dict(manuscript=FINAL, plan=Path(rebuilt['plan']), reconstruction=rebuilt_path,
        stored_native=Path('work/analysis/Hodram_B131_B150_stored_20261102/stored_native_verification.json'),
        loaders=Path('work/analysis/Hodram_B131_B150_loaders_20261102/verification.json'),
        actual=Path('work/analysis/Hodram_B131_B150_checked_20261102/actual_review.json'), visual_review=visual_path,
        typed_menu=display / 'menus_v1/menu_provider_and_planes_reviewed.json', native_styles=display / 'style_v1/compiled_style_objects.json',
        FE_layout=FE_review, focused_pixels=Path('work/analysis/Hodram_B131_B150_actual_pixels_20261102/focused_actual_pixels.json'),
        source_control=Path('work/analysis/Hodram_B133_source_control_20261102/source_control_result.json'))
    runtime_path = Path('translations/ascii_glyph_right_bounds_hodram_B131_B150_v1.json')
    deps = [*evidence_paths.values(), reference_path, Path(rebuilt['packet']), Path(rebuilt['native']), MODULE,
            Path('dk4tool/patch/reviewed_scene_batch_v5.py'), Path('dk4tool/script/reviewed_scene_rebuild.py'),
            Path('dk4tool/script/reviewed_scene_rebuild_v2.py'), Path('dk4tool/script/reviewed_scene_rebuild_v3.py'),
            Path('dk4tool/dialogue/reviewed_choice_object_v2.py'), Path('dk4tool/dialogue/reviewed_actor_style_object_v1.py'),
            Path('scripts/check_editorial_compiled_pages_v5.py'), Path('scripts/finalize_hodram_B131_B150_review.py'),
            Path('scripts/check_hodram_B131_B150_actual_pixels.py'), Path(__file__)]
    conf = dict(format='dk4-reviewed-scene-release-v6', **{k: str(v) for k, v in evidence_paths.items()},
        record_count=329, speech_count=319, ordinary_count=311, style_count=8, typed_choice_count=10,
        reviewed_blocks=doc['blocks'], blocks=rebuilt['changed_blocks'], native_pages=328, relative_cases=640,
        FE_count=23, menu_alignments=30, menu_returns=90, menu_planes=40, style_slots=8,
        actual_frames=59005, actual_runs=5, actual_sheets=19, focused_pixel_counts=dict(menu_samples=2, name_headers=2, body_pages=83),
        canonical_ROM_sha256=sha(Path('out/raphael_natural_v2_accepted_base.nds').read_bytes()),
        clean_ROM='work/clean.nds', clean_ROM_sha256=sha(Path('work/clean.nds').read_bytes()),
        parent_ROM_sha256=sha(stages[0].read_bytes()), target_ROM_sha256=sha(targets[0].read_bytes()),
        pre_runtime_reference_ROM=str(targets[0]), pre_runtime_ARM9_sha256=sha(canonical.read_file('/__arm9__.bin')),
        right_bound_configuration=str(runtime_path), dependencies={str(p): sha(p.read_bytes()) for p in deps})
    save(CONFIG, conf)
    profile['late_editorial_extensions'].append(dict(id='hodram-b131-b150', module='dk4tool.patch.reviewed_scene_batch_v6',
        module_sha256=sha(MODULE.read_bytes()), config=str(CONFIG), config_sha256=sha(CONFIG.read_bytes()),
        parent_ROM_sha256=conf['parent_ROM_sha256'], target_ROM_sha256=conf['target_ROM_sha256']))
    contract = deepcopy(load(old_configs[0]['parent_manifest']))
    contract['batches'].append(str(FINAL))
    contract.update(expected_candidate_sha256=conf['target_ROM_sha256'], predecessor_manifest=str(manifest_path),
        predecessor_manifest_sha256=sha(manifest_path.read_bytes()), new_extension_configs=[str(CONFIG)])
    contract_path = ROOT / 'expected_canonical_manifest_contract.json'
    save(contract_path, contract)
    config_paths = [runtime_path, Path('translations/emilio_name_glyph_hodram_B131_B150_release_v1.json'),
                    Path('translations/fernando_samwell_hodram_B131_B150_release_v1.json'),
                    Path('translations/follower_diogo_hodram_B131_B150_release_v1.json')]
    assert not any(p.exists() for p in config_paths)
    for index, (old, path) in enumerate(zip(old_configs, config_paths)):
        new = deepcopy(old)
        new.update(parent_ROM_sha256=sha(targets[index].read_bytes()),
            target_ROM_sha256=sha(targets[index + 1].read_bytes()) if index < 3 else rebuilt['research_ROM_sha256'])
        if index == 0:
            new['parent_manifest'] = str(contract_path)
            new['builder_dependencies'][str(MODULE)] = sha(MODULE.read_bytes())
        save(path, new)
    profile.update(dict(zip(stage_keys, map(str, config_paths))))
    grouped_path = Path('translations/geronimo_vasquez_alonso_hodram_B131_B150_release_v1.json')
    assert not grouped_path.exists()
    native_path = Path('work/analysis/Hodram_B131_B150_name_native_20261102/native_name_fields_verification_reviewed.json')
    native = load(native_path)
    field_doc = Path('translations/geronimo_vasquez_alonso_owned_name_review_v1.json')
    grouped_deps = [field_doc, Path(native['proposal']), native_path, evidence_paths['focused_pixels'], evidence_paths['actual'],
        Path('dk4tool/patch/registered_owned_name_fields_v4.py'), Path('dk4tool/patch/owned_name_fields_v2.py'),
        Path('dk4tool/patch/owned_name_fields_v3.py'), Path('scripts/build_integrated_release_with_grouped_fields.py'),
        Path('scripts/build_integrated_release_with_next_owned_fields.py'), Path('scripts/source_locked_derivation_v5118.py')]
    grouped = dict(format='dk4-registered-owned-name-fields-v4', manuscript=str(field_doc), proposal=native['proposal'],
        native=str(native_path), actual=str(evidence_paths['focused_pixels']), clean_ROM=conf['clean_ROM'], clean_ROM_sha256=conf['clean_ROM_sha256'],
        parent_ROM_sha256=rebuilt['research_ROM_sha256'], target_ROM_sha256=reference['research_ROM_sha256'],
        target_ARM9_sha256=native['name_data_plan']['target_ARM9_sha256'], dependencies={str(p): sha(p.read_bytes()) for p in grouped_deps},
        actual_policy=[dict(actor=a, kind='unchanged-progressive-middle-component', full_name=t) for a, t in
            [(36, 'Geronimo de Espinosa'), (49, 'Alonso de Rosa'), (42, 'Vasquez de Maldonado')]])
    save(grouped_path, grouped)
    profile.update(owned_name_fields_grouped=str(grouped_path), note='Cumulative experimental successor:329 five-gate reviews,328 pages,180 revisions/149 retentions;three full-name de corrections in four bytes after all prior runtime/name stages. Use build_integrated_release_with_grouped_fields.py. Preserve114 accepted layers,all prior profiles andASCII right-bound repair. No main promotion orguide photos;full scope/later audit remain.')
    registry['profiles'][PROFILE] = profile
    assert registry_path.read_bytes() == before
    save(registry_path, registry)
    save(ROOT / 'registered_preparation.json', dict(profile=PROFILE, config=str(CONFIG),
        runtime_config=str(config_paths[0]), emilio_config=str(config_paths[1]), prior_fields_config=str(config_paths[2]), next_fields_config=str(config_paths[3]), grouped_fields_config=str(grouped_path),
        canonical_parent=str(stages[0]), canonical_parent_sha256=conf['parent_ROM_sha256'],
        pre_runtime_ROM=str(targets[0]), pre_runtime_ROM_sha256=conf['target_ROM_sha256'],
        post_bounds_ROM=str(targets[1]), post_bounds_ROM_sha256=sha(targets[1].read_bytes()),
        post_Emilio_ROM=str(targets[2]), post_Emilio_ROM_sha256=sha(targets[2].read_bytes()),
        post_prior_fields_ROM=str(targets[3]), post_prior_fields_ROM_sha256=sha(targets[3].read_bytes()),
        post_next_fields_ROM=rebuilt['research_ROM'], post_next_fields_ROM_sha256=rebuilt['research_ROM_sha256'],
        final_ROM=reference['research_ROM'], target_ROM_sha256=reference['research_ROM_sha256'], accepted_layers=len(registry['accepted_layers']),
        previous_profiles_preserved=True, all_prior_drivers_unchanged=True, new_credit=0, main_unchanged=True))
    pins_path = Path('translations/rom_retention_pins.json')
    pins = load(pins_path)
    pins += [dict(path=str(p.resolve()), reason='Preserve exact B131–B150 registered stage reference; no pruning.') for p in targets]
    save(pins_path, pins)
    print(dict(profile=PROFILE, target=reference['research_ROM_sha256'], accepted_layers=len(registry['accepted_layers']), registry_sha256=sha(registry_path.read_bytes())))


if __name__ == '__main__':
    main()
