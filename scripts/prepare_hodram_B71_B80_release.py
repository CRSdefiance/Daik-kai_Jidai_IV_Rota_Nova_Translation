"""Register one cumulative successor without altering the canonical builder or main ROM."""
from copy import deepcopy
from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.audit_story_glyph_consistency import load,save
from scripts.source_locked_derivation_v5118 import checked_text

ROOT=Path('work/analysis/Hodram_B71_B80_release_20261101')
CONFIG=Path('translations/hodram_B71_B80_editorial_release_v1.json')
RUNTIME=Path('translations/ascii_glyph_right_bounds_hodram_B71_B80_v1.json')
PROFILE='all-routes-hodram-b71-b80-20261101'
MODULE=Path('dk4tool/patch/reviewed_scene_batch_v2.py')

if __name__=='__main__':
    assert not ROOT.exists() and not CONFIG.exists() and not RUNTIME.exists() and not MODULE.exists()
    old_module=Path('dk4tool/patch/reviewed_scene_batch_v1.py')
    body=old_module.read_text(encoding='utf-8')
    begin=body.index("    require(native['complete_stored_pages']")
    end=body.index("    path = approved['file_path']",begin)
    checks="""    require(native['complete_stored_pages'] == conf['native_pages'] and
            native['every_byte_consumed_andall_first_internal_final_glyphs_bounds_canaries_andpagination_pass'] and
            native['fresh_relocated_native_relative_cases'] == conf['relative_cases'], 'complete stored display/branch checks')
    require(native['all_stored_planes_equal_directly_viewed_compiled_planes'], 'exact visual review inheritance')
    visual = load(conf['visual_review'])
    require(visual['all_final_pages_directly_viewed_or_exact_plane_reuse'] and
            visual['final_pages'] == conf['native_pages'], 'complete readable page review')
    require(loaders['fresh_whole_archive_loads_andcache_hits'] == 325 and
            loaders['fresh_parent_cases'] == 2 * len(conf['blocks']) and
            loaders['exact_reused_parent_cases'] == 650 - 2 * len(conf['blocks']) and
            loaders['prior_executed_parent_instructions_match_current_runtime'], 'native loaders')
    require(actual['total_frames'] == conf['actual_frames'] and
            len(actual['runs']) == conf['actual_runs'] and
            len(actual['all_review_sheets_directly_viewed']) == conf['actual_sheets'] and
            actual['representative_progressive_FE_pagination_andscene_transition_observed'] and
            actual['no_new_blank_box_lost_glyph_orportrait_issue_seen_in_reviewed_samples'] and
            actual['no_natural_event_activation_original_location_earned_chronology_fullroute_orhardware_claim'],
            'representative gameplay and honest coverage')
"""
    body=checked_text(body,{
        "'dk4-reviewed-scene-release-v1'":"'dk4-reviewed-scene-release-v2'",
        "len(approved['records']) == conf['record_count'] == 224":"len(approved['records']) == conf['record_count'] and conf['record_count'] > 0",
        "set(approved['blocks']) == set(conf['blocks']) == set(range(61, 71))":
            "set(approved['blocks']) == set(conf['blocks']) == {g['block'] for g in reconstruction['groups']} and bool(conf['blocks'])",
        body[begin:end]:checks,
        'all224_source_controls_and392_commands60_relatives_preserved=True':
            'all_source_controls_commands_relatives_andunowned_bytes_preserved=True',
        'native_pages=229, fresh_relative_cases=300, native_loads=325':
            "native_pages=conf['native_pages'], fresh_relative_cases=conf['relative_cases'], native_loads=325",
        'parent_modes=dict(fresh=20, exact_reused=630), actual_frames=43003':
            "parent_modes=dict(fresh=2*len(conf['blocks']), exact_reused=650-2*len(conf['blocks'])), actual_frames=conf['actual_frames']",
    })
    MODULE.write_text(body,encoding='utf-8')
    ROOT.mkdir(parents=True)
    registry_path=Path('translations/release_stack.json');registry=load(registry_path)
    (ROOT/'release_stack_before.json').write_bytes(registry_path.read_bytes())
    assert PROFILE not in registry['profiles']
    parent=deepcopy(registry['profiles']['all-routes-hodram-b61-b70-julio-20261101'])
    old_runtime=load(parent['ascii_glyph_right_bounds'])
    rebuilt_path=Path('work/analysis/Hodram_B71_B80_rebuilt_20261101/reconstruction.json');rebuilt=load(rebuilt_path)
    source_manifest=Path('out/all_routes_combined_hodram_julio_20261101_candidate.manifest.json')
    manifest=load(source_manifest)
    canonical_path=Path(manifest['production_pipeline']['canonical_stage'])
    canonical=NdsImage.open(canonical_path)
    assert sha(canonical_path.read_bytes())==manifest['production_pipeline']['canonical_stage_sha256']==old_runtime['parent_ROM_sha256']
    source=NdsImage.open(rebuilt['parent']);target=NdsImage.open(rebuilt['research_ROM'])
    assert sha(Path(rebuilt['parent']).read_bytes())==manifest['candidate_sha256']==old_runtime['target_ROM_sha256']
    assert sha(Path(rebuilt['research_ROM']).read_bytes())==rebuilt['research_ROM_sha256']
    # Exact inverse of the already registered code-only final layer. Every file
    # and all other components must match the canonical ordered predecessor.
    inverse=deepcopy(source);inverse.replace_file('/__arm9__.bin',canonical.read_file('/__arm9__.bin'))
    assert bytes(inverse.rom.save())==canonical_path.read_bytes()
    pre=deepcopy(target);pre.replace_file('/__arm9__.bin',canonical.read_file('/__arm9__.bin'))
    assert source.read_file('/__arm9__.bin')==target.read_file('/__arm9__.bin')
    pre_path=ROOT/'canonical_target_RESEARCH_ONLY.nds';pre_path.write_bytes(bytes(pre.rom.save()))
    assert [p for _,p,data in canonical.iter_files() if pre.read_file(p)!=data]==['/data/SC1.DK4']
    assert all(pre.read_file(p)==data for p,data in canonical.iter_components())
    final=Path('translations/hodram_B71_B80_contextual_final_review_v1.json')
    plan=Path(rebuilt['plan']);native=Path('work/analysis/Hodram_B71_B80_stored_20261101/stored_native_verification.json')
    loaders=Path('work/analysis/Hodram_B71_B80_loaders_20261101/verification.json')
    actual=Path('work/analysis/Hodram_B71_B80_actual_20261101/actual_review.json')
    visual=Path('work/analysis/Hodram_B71_B80_editorial_20261101/visual_review.json')
    config=deepcopy(load('translations/hodram_B61_B70_editorial_release_v1.json'))
    config.update(format='dk4-reviewed-scene-release-v2',manuscript=str(final),plan=str(plan),
        reconstruction=str(rebuilt_path),stored_native=str(native),loaders=str(loaders),actual=str(actual),
        visual_review=str(visual),record_count=144,blocks=list(range(71,81)),native_pages=154,
        relative_cases=420,actual_frames=25002,actual_runs=2,actual_sheets=10,
        parent_ROM_sha256=sha(canonical_path.read_bytes()),target_ROM_sha256=sha(pre_path.read_bytes()),
        pre_runtime_reference_ROM=str(pre_path),pre_runtime_ARM9_sha256=sha(canonical.read_file('/__arm9__.bin')),
        final_runtime_ROM_sha256=rebuilt['research_ROM_sha256'],right_bound_configuration=str(RUNTIME))
    paths=[final,plan,rebuilt_path,native,loaders,actual,visual,MODULE,old_module,Path(__file__),
        Path('translations/hodram_B71_B80_editorial_manuscript_v1.json'),
        Path(rebuilt['packet']),Path(rebuilt['native']),Path('scripts/rebuild_reviewed_editorial_batch.py'),
        Path('scripts/author_hodram_B71_B80_editorial.py'),Path('scripts/plan_hodram_B71_B80.py'),
        Path('scripts/check_editorial_compiled_pages.py'),Path('scripts/refresh_editorial_compiled_pages.py'),
        Path('scripts/check_editorial_stored_batch.py'),Path('scripts/check_hodram_B71_B80_loaders.py'),
        Path('scripts/check_pending_scene_loaders.py'),Path('scripts/create_hodram_B71_B80_fixtures.py'),
        Path('scripts/create_hodram_representative_fixtures.py'),Path('scripts/make_editorial_capture_sheets.py'),
        Path('scripts/finalize_hodram_B71_B80_review.py'),
        Path('work/analysis/Hodram_B71_B80_identity_20261101/native_names.json'),
        Path('work/analysis/Hodram_B71_B80_identity_20261101/clean_names.json'),
        Path('work/analysis/Hodram_B71_B80_fixtures_20261101/fixtures.json')]
    config['dependencies'].update({str(path):sha(path.read_bytes()) for path in paths})
    save(CONFIG,config)
    spec=dict(id='hodram-b71-b80',module='dk4tool.patch.reviewed_scene_batch_v2',
        module_sha256=sha(MODULE.read_bytes()),config=str(CONFIG),config_sha256=sha(CONFIG.read_bytes()),
        parent_ROM_sha256=config['parent_ROM_sha256'],target_ROM_sha256=config['target_ROM_sha256'])
    parent['late_editorial_extensions'].append(spec)
    parent['ascii_glyph_right_bounds']=str(RUNTIME)
    parent['note']='Natural-dialogue-v2 cumulative successor: Hodram B71-B80,144 complete contextual reviews,100 revisions/44 retentions. Preserve all prior accepted and experimental layers, Julio glyph correction and registered ASCII right-bound runtime.154 offline reviewed pages,420 native relative cases,325 loads and representative initialized B72/B76 gameplay pass. Optional natural activation and other batch scenes remain offline; full goal active. Main promotion requires user acceptance. Guide photo collection discontinued.'
    contract=deepcopy(load(old_runtime['parent_manifest']))
    contract['batches'].append(str(final));contract['expected_candidate_sha256']=config['target_ROM_sha256']
    contract.update(predecessor_manifest=str(source_manifest),predecessor_manifest_sha256=sha(source_manifest.read_bytes()),new_extension_configs=[str(CONFIG)])
    contract_path=ROOT/'expected_canonical_manifest_contract.json';save(contract_path,contract)
    runtime=deepcopy(old_runtime)
    runtime.update(parent_ROM_sha256=config['target_ROM_sha256'],target_ROM_sha256=rebuilt['research_ROM_sha256'],parent_manifest=str(contract_path))
    runtime['builder_dependencies'].update({str(MODULE):sha(MODULE.read_bytes())})
    save(RUNTIME,runtime)
    registry['profiles'][PROFILE]=parent
    save(registry_path,registry)
    save(ROOT/'registered_preparation.json',dict(profile=PROFILE,config=str(CONFIG),config_sha256=sha(CONFIG.read_bytes()),
        runtime_config=str(RUNTIME),runtime_config_sha256=sha(RUNTIME.read_bytes()),
        pre_runtime_ROM=str(pre_path),pre_runtime_ROM_sha256=config['target_ROM_sha256'],
        target_ROM_sha256=rebuilt['research_ROM_sha256'],canonical_builder_unchanged=True,
        previous_profiles_preserved=True,accepted_layers=len(registry['accepted_layers']),
        no_new_main_promotion_orcompletion_credit=True,new_credit=0))
    pins_path=Path('translations/rom_retention_pins.json');pins=load(pins_path)
    pins.append(dict(path=str(pre_path.resolve()),reason='Preserve exact pre-runtime target for registered Hodram B71-B80 cumulative release reconstruction.'))
    save(pins_path,pins)
    print(dict(profile=PROFILE,pre_runtime_sha256=config['target_ROM_sha256'],final_sha256=rebuilt['research_ROM_sha256'],accepted_layers=len(registry['accepted_layers'])))
