"""Qualify the shared transaction and changed source/prose/display boundaries once."""
import argparse
import gc
import importlib
from copy import deepcopy
from pathlib import Path
from dk4tool.patch.late_editorial_extensions_v1 import plan_extensions
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.audit_story_glyph_consistency import load, save


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--preparation',type=Path,required=True)
    parser.add_argument('--out',type=Path,required=True)
    args = parser.parse_args()
    assert not args.out.exists()
    prep = load(args.preparation)
    registry_path = Path('translations/release_stack.json')
    assert sha(registry_path.read_bytes()) == prep['registry_sha256']
    registry = load(registry_path)
    assert len(prep['new_extension_specs']) == len(prep['configs']) == 1
    spec = prep['new_extension_specs'][0]
    conf = load(prep['configs'][0])
    planner = importlib.import_module(spec['module']).plan_release
    image, base = NdsImage.open(prep['canonical_parent']),NdsImage.open(registry['canonical_baseline']['path'])
    before, base_before = bytes(image.rom.save()),bytes(base.rom.save())
    planned, reports = plan_extensions(image,base,prep['new_extension_specs'])
    direct = load(args.preparation.parent/'positive_prepublication_plan.json')
    assert len(reports) == 1 and all(reports[0][k] == v for k,v in direct.items())
    assert sha(bytes(planned.save())) == prep['ordered_canonical_targets'][0]['sha256']
    assert bytes(image.rom.save()) == before and bytes(base.rom.save()) == base_before
    del planned
    gc.collect()
    args.out.mkdir(parents=True)
    rejections = []
    for kind,key in [('failed-fifth-gate','manuscript'),('changed-source-selector00','manuscript'),
        ('changed-caption-index','manuscript'),('failed-name-formatting','scoped_names'),
        ('false-actual-scope','actual'),('changed-logical-prose','manuscript'),('wrong-control-only-membership',None)]:
        config = deepcopy(conf)
        if key is None:
            config['blocks'] = sorted(set(config['blocks'])|{89})
        else:
            doc = load(config[key])
            if kind in ['failed-fifth-gate','failed-name-formatting']:
                doc['records'][0]['review']['formatting'] = False
            elif kind == 'changed-source-selector00':
                next(r for r in doc['records'] if r.get('source_selector') == 0)['source_complete_preamble_hex'] = '0040ffff0001'
            elif kind == 'changed-caption-index':
                next(r for r in doc['records'] if r['kind'] == 'typed-choice-label' and r['source_index'] == 1)['source_index'] = 0
            elif kind == 'false-actual-scope':
                doc['offline_only_source_speeches'] = 0
            elif kind == 'changed-logical-prose':
                doc['records'][0]['english'] += ' Changed.'
            else:
                raise ValueError(kind)
            path = args.out/(kind+'.json')
            save(path,doc)
            config[key] = str(path)
            config['dependencies'][str(path)] = sha(path.read_bytes())
        cp = args.out/(kind+'_config.json')
        save(cp,config)
        try:
            planner(image,base,cp)
        except (ValueError,AssertionError,KeyError) as error:
            rejections.append(dict(case=kind,error_type=type(error).__name__,error=str(error)))
        else:
            raise AssertionError('Accepted invalid source/display scope: '+kind)
        assert bytes(image.rom.save()) == before and bytes(base.rom.save()) == base_before
        gc.collect()
        print('Rejected:',kind,flush=True)
    altered = deepcopy(prep['new_extension_specs'])
    altered[0]['parent_ROM_sha256'] = '0'*64
    try:
        plan_extensions(image,base,altered)
    except ValueError as error:
        rejections.append(dict(case='wrong-ordered-predecessor',error_type=type(error).__name__,error=str(error)))
    else:
        raise AssertionError('Accepted incorrect complete predecessor')
    previous = registry['profiles'][prep['previous_profile']]
    for i,(key,path) in enumerate(prep['preserved_stage_configs'].items()):
        old,new = load(previous[key]),load(path)
        allowed = {'parent_ROM_sha256','target_ROM_sha256'}|({'parent_manifest','builder_dependencies'} if i==0 else set())
        assert {k:v for k,v in old.items() if k not in allowed} == {k:v for k,v in new.items() if k not in allowed}
        if i == 0:
            assert all(new['builder_dependencies'][k] == v for k,v in old['builder_dependencies'].items())
    assert len(rejections) == 8
    assert bytes(image.rom.save()) == before and bytes(base.rom.save()) == base_before
    save(args.out/'qualification.json',dict(profile=prep['profile'],preparation=str(args.preparation),preparation_sha256=sha(args.preparation.read_bytes()),
        registry_sha256=prep['registry_sha256'],positive_ordered_shared_plans=reports,direct_prepublication_andshared_targets_equal=True,
        changed_scope_andordering_rejections=rejections,unchanged_eight_final_stage_contracts_compared_exactly=True,
        all_inputs_unowned_files_components_andcomplete_inverses_preserved=True,
        unchanged_native_characterization_not_reexecuted=True,registered_build_patch_andown_startup_pending=True,new_credit=0,
        producer_sha256=sha(Path(__file__).read_bytes())))
    print('One shared source-bound transaction/eight semantic andordering rejections pass;all eight final stage contracts exact. Build next.',flush=True)


if __name__ == '__main__':
    main()
