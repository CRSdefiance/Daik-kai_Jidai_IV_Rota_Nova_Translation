"""Qualify the two new ordered Help adapters and reuse the unchanged native/stage proofs."""
import gc
from copy import deepcopy
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.late_editorial_extensions_v1 import plan_extensions
from dk4tool.patch.sea_help22_release_v1 import plan_release as sea_plan
from dk4tool.patch.fleet_help66_amendment_release_v1 import plan_release as fleet_plan
from scripts.audit_story_glyph_consistency import load,save

ROOT=Path('work/analysis/Sea22_Fleet66_release_qualification_20261105')
PREP=Path('work/analysis/Sea22_Fleet66_release_v2_20261104/registered_preparation.json')

if __name__=='__main__':
    assert not ROOT.exists();prep=load(PREP)
    registry_path=Path('translations/release_stack.json');assert sha(registry_path.read_bytes())==prep['registry_sha256'];registry=load(registry_path)
    image=NdsImage.open(prep['canonical_parent']);base=NdsImage.open('out/raphael_natural_v2_accepted_base.nds')
    before,base_before=bytes(image.rom.save()),bytes(base.rom.save())
    shared,reports=plan_extensions(image,base,prep['new_extension_specs'])
    assert len(reports)==2 and [len(p['changed_records'])for p in reports]==[22,1]
    assert sha(bytes(shared.save()))==sha(Path(prep['final_canonical_target']).read_bytes())
    assert bytes(image.rom.save())==before and bytes(base.rom.save())==base_before
    del shared;gc.collect();ROOT.mkdir();rejected=[]
    configs=list(map(load,prep['configs']))
    for layer,kind,key in [(0,'missing-reviewed-article','manuscript'),(0,'missing-observed-page','actual'),
        (1,'wrong-Command-term','manuscript'),(1,'wrong-owned-continuation','manuscript')]:
        config=deepcopy(configs[layer]);doc=load(config[key])
        if kind=='missing-reviewed-article':doc['records'].pop()
        elif kind=='missing-observed-page':doc['actual_HELP_cases'].pop()
        elif kind=='wrong-Command-term':
            row=doc['records'][0];row['english']=row['english'].replace('Command','Leadership')
            row['semantic_sections']=[s.replace('Command','Leadership')for s in row['semantic_sections']]
        else:doc['records'][0]['current_continuations'][0]['current_hex']='00'
        path=ROOT/(kind+'.json');save(path,doc);config[key]=str(path);config['dependencies'][str(path)]=sha(path.read_bytes())
        if key=='actual':
            visual=load(config['actual_visual']);visual['actual_proof_sha256']=sha(path.read_bytes());visual['actual_proof']=str(path)
            vp=ROOT/(kind+'_visual.json');save(vp,visual);config['actual_visual']=str(vp);config['dependencies'][str(vp)]=sha(vp.read_bytes())
        cp=ROOT/(kind+'_config.json');save(cp,config)
        parent=NdsImage.open(prep['canonical_parent']if layer==0 else prep['intermediate_canonical_parent'])
        parent_before=bytes(parent.rom.save())
        try:[sea_plan,fleet_plan][layer](parent,base,cp)
        except (ValueError,AssertionError,KeyError)as error:rejected.append(dict(case=kind,error_type=type(error).__name__,error=str(error)))
        else:raise AssertionError('Accepted invalid changed scope:'+kind)
        assert bytes(parent.rom.save())==parent_before and bytes(base.rom.save())==base_before
        del parent,doc,config;gc.collect()
    assert len(rejected)==4 and 'Command' in rejected[2]['error'] and 'continuation' in rejected[3]['error']
    try:plan_extensions(image,base,list(reversed(prep['new_extension_specs'])))
    except ValueError as error:rejected.append(dict(case='reversed-two-layer-order',error_type=type(error).__name__,error=str(error)))
    else:raise AssertionError('Accepted reversed Help layer order')
    old=registry['profiles'][prep['previous_profile']]
    for i,(key,path)in enumerate(prep['preserved_stage_configs'].items()):
        a,b=load(old[key]),load(path);allowed={'parent_ROM_sha256','target_ROM_sha256'}|({'parent_manifest','builder_dependencies'}if i==0 else set())
        assert {k:v for k,v in a.items()if k not in allowed}=={k:v for k,v in b.items()if k not in allowed}
        if i==0:assert all(b['builder_dependencies'][k]==v for k,v in a['builder_dependencies'].items())
    previous=Path('work/analysis/Shipyard_HELP37_release_qualification_v2_20261104/qualification.json')
    sea=Path('work/analysis/Shared_HELP_T81_T102_formatting_20261104/preview_qualification_v1/qualification.json')
    fleet=Path('work/analysis/HELP66_Command_amendment_20261104/preview_qualification_v1/qualification.json')
    assert len(load(previous)['changed_partial_coverage_rejections'])==6
    assert len(load(sea)['new_formatter_andindividual_gate_rejections'])==7 and len(load(fleet)['new_formatter_andindividual_gate_rejections'])==3
    save(ROOT/'qualification.json',dict(profile=prep['profile'],preparation=str(PREP),preparation_sha256=sha(PREP.read_bytes()),registry_sha256=prep['registry_sha256'],
        positive_ordered_shared_plans=reports,direct_prepublication_andshared_targets_equal=True,changed_scope_andordering_rejections=rejected,
        unchanged_eight_final_stage_contracts_compared_exactly=True,all_inputs_unowned_files_components_andcomplete_inverses_preserved=True,
        reused_proofs={str(p):sha(p.read_bytes())for p in [previous,sea,fleet]},six_prior_scope_guards_seven_sea_formatter_guards_three_fleet_guards_reused=True,
        unchanged_native_characterization_not_reexecuted=True,registered_build_patch_andown_startup_pending=True,new_credit=0,
        producer_sha256=sha(Path(__file__).read_bytes())))
    print('Two ordered Help layers qualify:direct/shared targets, five new scope/order rejections, all eight stage contracts; unchanged proofs reused.')
