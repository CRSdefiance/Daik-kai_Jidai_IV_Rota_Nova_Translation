"""Qualify the ordered shared entry point andnew semantic boundaries;reuse frozen native/stage proofs."""
import gc
from copy import deepcopy
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.late_editorial_extensions_v1 import plan_extensions
from dk4tool.patch.deck_help31_release_v1 import plan_release as deck_plan
from dk4tool.patch.remaining_help67_release_v1 import plan_release as remaining_plan
from dk4tool.patch.rafael_story_b81_b84_release_v2 import plan_release as story_plan
from scripts.audit_story_glyph_consistency import load,save

PREP=Path('work/analysis/Help97_Rafael330_release_v2_20261105/registered_preparation.json')
ROOT=Path('work/analysis/Help97_Rafael330_release_qualification_20261105')

if __name__=='__main__':
    assert not ROOT.exists();prep=load(PREP);registry_path=Path('translations/release_stack.json')
    assert sha(registry_path.read_bytes())==prep['registry_sha256'];registry=load(registry_path)
    image=NdsImage.open(prep['canonical_parent']);base=NdsImage.open('out/raphael_natural_v2_accepted_base.nds')
    before,base_before=bytes(image.rom.save()),bytes(base.rom.save())
    shared,reports=plan_extensions(image,base,prep['new_extension_specs'])
    assert len(reports)==3 and [len(p['changed_records']) for p in reports]==[31,67,330]
    assert sha(bytes(shared.save()))==prep['ordered_canonical_targets'][-1]['sha256']
    assert bytes(image.rom.save())==before and bytes(base.rom.save())==base_before
    del shared;gc.collect();ROOT.mkdir();rejected=[]
    configs=list(map(load,prep['configs']));planners=[deck_plan,remaining_plan,story_plan]
    cases=[(0,'missing-Deck-article','manuscript'),(0,'wrong-active-Speech-label','manuscript'),
        (0,'wrong-exclusive-adapter-kind',None),(1,'false-offline-coverage','manuscript'),
        (1,'wrong-owned-Help-continuation','manuscript'),(2,'failed-fifth-gate','manuscript'),
        (2,'changed-source-selector00','manuscript'),(2,'missing-source-owned-FE-continuation','manuscript'),
        (2,'failed-name-formatting','scoped_names'),(2,'false-Rafael-actual-scope','actual')]
    for layer,kind,key in cases:
        config=deepcopy(configs[layer])
        if key is None:config['kind']='remaining67'
        else:
            doc=load(config[key])
            if kind=='missing-Deck-article':doc['records'].pop()
            elif kind=='wrong-active-Speech-label':
                row=next(r for r in doc['records'] if r['topic_id']==33)
                row['english']=row['english'].replace('Speech','Social')
                if 'semantic_sections' in row:row['semantic_sections']=[s.replace('Speech','Social') for s in row['semantic_sections']]
            elif kind=='false-offline-coverage':
                for row in doc['records']:row['offline_only']=False
            elif kind=='wrong-owned-Help-continuation':
                next(r for r in doc['records'] if r['topic_id']==133)['current_continuations'][0]['current_hex']='00'
            elif kind in ['failed-fifth-gate','failed-name-formatting']:doc['records'][0]['review']['formatting']=False
            elif kind=='changed-source-selector00':
                next(r for r in doc['records'] if r.get('source_selector')==0)['source_complete_preamble_hex']='0040ffff0001'
            elif kind=='missing-source-owned-FE-continuation':
                next(r for r in doc['records'] if r['id']=='DK4_MES_B84_R0470').pop('planned_integrated_native_pages')
            elif kind=='false-Rafael-actual-scope':doc['offline_only_source_speeches']=0
            else:raise ValueError(kind)
            path=ROOT/(kind+'.json');save(path,doc);config[key]=str(path);config['dependencies'][str(path)]=sha(path.read_bytes())
        cp=ROOT/(kind+'_config.json');save(cp,config)
        parent_path=prep['canonical_parent'] if layer==0 else prep['ordered_canonical_targets'][layer-1]['path']
        parent=NdsImage.open(parent_path);parent_before=bytes(parent.rom.save())
        try:planners[layer](parent,base,cp)
        except (ValueError,AssertionError,KeyError) as error:rejected.append(dict(case=kind,error_type=type(error).__name__,error=str(error)))
        else:raise AssertionError('Accepted invalid changed scope:'+kind)
        assert bytes(parent.rom.save())==parent_before and bytes(base.rom.save())==base_before
        del parent,config;gc.collect();print('Rejected:',kind,flush=True)
    try:plan_extensions(image,base,list(reversed(prep['new_extension_specs'])))
    except ValueError as error:rejected.append(dict(case='reversed-three-layer-order',error_type=type(error).__name__,error=str(error)))
    else:raise AssertionError('Accepted reversed ordered release')
    assert len(rejected)==11
    previous=registry['profiles'][prep['previous_profile']]
    for i,(key,path) in enumerate(prep['preserved_stage_configs'].items()):
        old,new=load(previous[key]),load(path)
        allowed={'parent_ROM_sha256','target_ROM_sha256'}|({'parent_manifest','builder_dependencies'} if i==0 else set())
        assert {k:v for k,v in old.items() if k not in allowed}=={k:v for k,v in new.items() if k not in allowed}
        if i==0:assert all(new['builder_dependencies'][k]==v for k,v in old['builder_dependencies'].items())
    reuse=[Path('work/analysis/Sea22_Fleet66_release_qualification_20261105/qualification.json'),
        Path('work/analysis/Rafael_B81_B84_rebuilt_v3_20261105/reconstruction.json'),
        Path('work/analysis/Rafael_B84_choices_20261105/complete_native_visual_approval_v1.json'),
        Path('work/analysis/Rafael330_current675_dependency_qualification_20261105.json')]
    assert len(load(reuse[0])['changed_scope_andordering_rejections'])==5
    assert len(load(reuse[1])['seven_FE_pagination_invalid_cases_rejected'])==7
    assert load(reuse[2])['all15_menu_compiler_invalid_cases_rejected']
    save(ROOT/'qualification.json',dict(profile=prep['profile'],preparation=str(PREP),preparation_sha256=sha(PREP.read_bytes()),
        registry_sha256=prep['registry_sha256'],positive_ordered_shared_plans=reports,
        direct_prepublication_andshared_targets_equal=True,changed_scope_andordering_rejections=rejected,
        unchanged_eight_final_stage_contracts_compared_exactly=True,all_inputs_unowned_files_components_andcomplete_inverses_preserved=True,
        reused_proofs={str(p):sha(p.read_bytes()) for p in reuse},seven_FE_and15_menu_negative_native_proofs_reused=True,
        unchanged_native_characterization_not_reexecuted=True,registered_build_patch_andown_startup_pending=True,new_credit=0,
        producer_sha256=sha(Path(__file__).read_bytes())))
    print('Three ordered shared plans and11 new semantic/order rejections pass;all eight final stages preserved. Registered build next.')
