"""Register one qualified SC0 extension while preserving all eight final-stage contracts."""
import argparse
import gc
import importlib
import os
from copy import deepcopy
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.audit_story_glyph_consistency import load, save
from scripts.verify_rafael_B51_B60_registered_release import KEYS, PIPELINES


def identity(path):
    return dict(path=str(path), sha256=sha(path.read_bytes()))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--spec',type=Path,required=True)
    parser.add_argument('--out',type=Path,required=True)
    args = parser.parse_args()
    spec = load(args.spec)
    registry_path = Path('translations/release_stack.json')
    before = registry_path.read_bytes()
    assert sha(before) == spec['expected_registry_sha256']
    registry = load(registry_path)
    assert spec['profile'] not in registry['profiles'] and len(registry['accepted_layers']) == 114
    assert not args.out.exists()
    release = load(spec['parent_release'])
    assert release['profile'] == spec['previous_profile'] and release['clean_input_patch_byte_exact'] and not release['own_registered_startup_pending']
    manifest_path = Path(release['manifest'])
    manifest = load(manifest_path)
    assert sha(manifest_path.read_bytes()) == release['manifest_sha256']
    assert all(manifest['checks'].values()) and len(manifest['checks']) == 26
    oldprofile = registry['profiles'][spec['previous_profile']]
    oldpaths = [Path(oldprofile[k]) for k in KEYS]
    oldconfigs = list(map(load,oldpaths))
    oldstates = [Path(manifest[a][b]) for a,b in PIPELINES]+[Path(release['candidate'])]
    assert len(oldstates) == 9 and sha(oldstates[-1].read_bytes()) == release['candidate_sha256']
    final = Path(spec['evidence']['manuscript'])
    doc = load(final)
    rebuilt_path = Path(spec['evidence']['reconstruction'])
    rebuilt = load(rebuilt_path)
    assert rebuilt['parent_sha256'] == release['candidate_sha256']
    assert len(doc['records']) == spec['counts']['record_count'] and all(all(r['review'].values()) for r in doc['records'])
    resource = Path(rebuilt['target_archive']).read_bytes()
    assert sha(resource) == rebuilt['target_archive_sha256'] and doc['file_path'] == '/data/SC0.DK4'
    for i, c in enumerate(oldconfigs):
        assert sha(oldstates[i].read_bytes()) == c['parent_ROM_sha256'] and sha(oldstates[i+1].read_bytes()) == c['target_ROM_sha256']
    args.out.mkdir(parents=True)
    (args.out/'release_stack_before.json').write_bytes(before)
    targets = []
    for i, state in enumerate(oldstates[:-1]):
        original, target = NdsImage.open(state), NdsImage.open(state)
        assert sha(original.read_file(doc['file_path'])) == rebuilt['source_archive_sha256']
        target.replace_file(doc['file_path'],resource)
        assert [p for _,p,v in original.iter_files() if target.read_file(p) != v] == [doc['file_path']]
        assert all(target.read_file(p) == v for p,v in original.iter_components())
        path = args.out/f'stage_{i}_RESEARCH_REFERENCE.nds'
        target.save(path)
        inverse = NdsImage.open(path)
        inverse.replace_file(doc['file_path'],original.read_file(doc['file_path']))
        assert bytes(inverse.rom.save()) == state.read_bytes()
        targets.append(path)
        del original,target,inverse
        gc.collect()
    final_research = Path(rebuilt['research_ROM'])
    assert sha(final_research.read_bytes()) == rebuilt['research_ROM_sha256']
    expected = NdsImage.open(oldstates[-1])
    expected.replace_file(doc['file_path'],resource)
    assert bytes(expected.rom.save()) == final_research.read_bytes()
    targets.append(final_research)
    del expected
    gc.collect()
    configpath = Path(spec['config'])
    stagepaths = [Path(p) for p in spec['stage_configs']]
    assert len(stagepaths) == 8 and not configpath.exists() and not any(p.exists() for p in stagepaths)
    modulepath = Path(*spec['module'].split('.')).with_suffix('.py')
    deps = {Path(p) for p in spec['dependencies']} | {args.spec,Path(__file__),modulepath}
    deps |= {Path(p) for p in spec['evidence'].values()}
    contract = deepcopy(load(oldconfigs[0]['parent_manifest']))
    contract['batches'].append(str(final))
    contract.update(expected_candidate_sha256=sha(targets[0].read_bytes()),predecessor_manifest=str(manifest_path),
        predecessor_manifest_sha256=sha(manifest_path.read_bytes()),new_extension_configs=[str(configpath)])
    contractpath = args.out/'expected_canonical_manifest_contract.json'
    save(contractpath,contract)
    for i,(old,path) in enumerate(zip(oldconfigs,stagepaths,strict=True)):
        value = deepcopy(old)
        value.update(parent_ROM_sha256=sha(targets[i].read_bytes()),target_ROM_sha256=sha(targets[i+1].read_bytes()))
        if i == 0:
            value['parent_manifest'] = str(contractpath)
            for dep in deps:
                if dep.suffix == '.py':
                    value['builder_dependencies'][str(dep)] = sha(dep.read_bytes())
        allowed = {'parent_ROM_sha256','target_ROM_sha256'} | ({'parent_manifest','builder_dependencies'} if i == 0 else set())
        assert {k:v for k,v in value.items() if k not in allowed} == {k:v for k,v in old.items() if k not in allowed}
        save(path,value)
    config = dict(format='dk4-reviewed-rafael-plain-scene-release-v1',**spec['evidence'],**spec['counts'],
        blocks=rebuilt['changed_blocks'],reviewed_blocks=rebuilt['reviewed_blocks'],
        canonical_ROM_sha256=registry['canonical_baseline']['sha256'],clean_ROM='work/clean.nds',
        clean_ROM_sha256=sha(Path('work/clean.nds').read_bytes()),parent_ROM_sha256=sha(oldstates[0].read_bytes()),
        target_ROM_sha256=sha(targets[0].read_bytes()),pre_runtime_ARM9_sha256=sha(NdsImage.open(oldstates[0]).read_file('/__arm9__.bin')),
        final_runtime_ARM9_sha256=sha(NdsImage.open(oldstates[-1]).read_file('/__arm9__.bin')),
        final_dependency_ROM=release['candidate'],final_dependency_ROM_sha256=release['candidate_sha256'],
        right_bound_configuration=str(stagepaths[0]),dependencies={str(p):sha(p.read_bytes()) for p in sorted(deps)})
    save(configpath,config)
    planner = importlib.import_module(spec['module']).plan_release
    planned, proof = planner(NdsImage.open(oldstates[0]),NdsImage.open(registry['canonical_baseline']['path']),configpath)
    assert sha(bytes(planned.save())) == config['target_ROM_sha256'] and len(proof['changed_records']) == config['record_count']
    assert proof['one_complete_NDS_object_commit_after_all_gates']
    save(args.out/'positive_prepublication_plan.json',proof)
    del planned
    gc.collect()
    stage_proofs = []
    for i,(old,new) in enumerate(zip(oldstates,targets,strict=True)):
        a,b = NdsImage.open(old),NdsImage.open(new)
        assert all(b.read_file(p) == v for p,v in a.iter_components())
        assert [p for _,p,v in a.iter_files() if b.read_file(p) != v] == [doc['file_path']]
        stage_proofs.append(dict(stage=i,old_state=identity(old),new_state=identity(new),
            ARM9_COMMON_font_andall_final_stage_inputs_except_owned_SC0_exact=True))
        del a,b
        gc.collect()
    profile = deepcopy(oldprofile)
    new_spec = dict(id=spec['extension_id'],module=spec['module'],module_sha256=sha(modulepath.read_bytes()),
        config=str(configpath),config_sha256=sha(configpath.read_bytes()),parent_ROM_sha256=config['parent_ROM_sha256'],target_ROM_sha256=config['target_ROM_sha256'])
    assert not any(s['id'] == new_spec['id'] or s['module'] == new_spec['module'] for s in profile['late_editorial_extensions'])
    profile['late_editorial_extensions'].append(new_spec)
    profile.update(dict(zip(KEYS,map(str,stagepaths))))
    profile['note'] = spec['note']
    registry['profiles'][spec['profile']] = profile
    prior = load(args.out/'release_stack_before.json')
    assert all(registry[k] == v for k,v in prior.items() if k != 'profiles') and all(registry['profiles'][k] == v for k,v in prior['profiles'].items())
    assert registry_path.read_bytes() == before
    pending = registry_path.with_name('release_stack.'+args.out.name+'.pending.json')
    assert not pending.exists()
    save(pending,registry)
    os.replace(pending,registry_path)
    save(args.out/'registered_preparation.json',dict(profile=spec['profile'],previous_profile=spec['previous_profile'],
        configs=[str(configpath)],new_extension_specs=[new_spec],canonical_parent=str(oldstates[0]),canonical_parent_sha256=sha(oldstates[0].read_bytes()),
        ordered_canonical_targets=[identity(targets[0])],stage_targets=[identity(p) for p in targets],old_stage_states=[identity(p) for p in oldstates],
        preserved_stage_configs=dict(zip(KEYS,map(str,stagepaths))),final_ROM=str(targets[-1]),target_ROM_sha256=sha(targets[-1].read_bytes()),
        registry_sha256=sha(registry_path.read_bytes()),expected_manifest_entries=len(manifest['batches'])+1,accepted_layers=114,
        previous_profiles_preserved=True,new_source_editorial_objects=config['record_count'],previously_credited_amendments=[],
        exact_unchanged_eight_final_stage_contracts_andinputs_qualified_by_dependency_reuse=stage_proofs,
        new_credit=0,main_unchanged=True,semantic_qualification_andregistered_build_pending=True))
    pins_path = Path('translations/rom_retention_pins.json')
    pin_before = pins_path.read_bytes()
    pins = load(pins_path)
    (args.out/'pins.before.json').write_bytes(pin_before)
    for path in targets[:-1]:
        assert not any(Path(p['path']).resolve() == path.resolve() for p in pins)
        pins.append(dict(path=str(path.resolve()),reason='Preserve ordered registered SC0 successor research reference. SHA256 '+sha(path.read_bytes())))
    temporary = pins_path.with_name('rom_retention_pins.'+args.out.name+'.pending.json')
    assert not temporary.exists()
    save(temporary,pins)
    assert pins_path.read_bytes() == pin_before
    os.replace(temporary,pins_path)
    print(dict(profile=spec['profile'],entries=len(manifest['batches'])+1,records=config['record_count'],target=sha(targets[-1].read_bytes()),
        registered=True,qualification_andbuild_pending=True,new_credit=0),flush=True)


if __name__ == '__main__':
    main()
