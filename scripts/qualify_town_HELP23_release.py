"""Qualify changed partial-coverage guards;reuse the already checked source/parser/eight-stage contracts."""
from copy import deepcopy
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.town_help23_release_v1 import plan_release
from dk4tool.patch.late_editorial_extensions_v1 import plan_extensions
from scripts.audit_story_glyph_consistency import load,save

ROOT=Path('work/analysis/Town_HELP23_release_qualification_20261104')
PREP=Path('work/analysis/Town_HELP23_release_20261104/registered_preparation.json')
if __name__=='__main__':
    assert not ROOT.exists();prep=load(PREP);conf_path=Path(prep['config']);conf=load(conf_path)
    registry_path=Path('translations/release_stack.json');registry=load(registry_path);assert sha(registry_path.read_bytes())==prep['registry_sha256']
    image=NdsImage.open(prep['canonical_parent']);base=NdsImage.open('out/raphael_natural_v2_accepted_base.nds')
    before,base_before=bytes(image.rom.save()),bytes(base.rom.save())
    planned,proof=plan_release(image,base,conf_path);assert len(proof['changed_records'])==23 and sha(bytes(planned.save()))==conf['target_ROM_sha256']
    spec=registry['profiles'][prep['profile']]['late_editorial_extensions'][-1]
    shared,shared_proof=plan_extensions(image,base,[spec]);assert bytes(shared.save())==bytes(planned.save())
    ROOT.mkdir();rejected=[]
    for kind,key in [('false-offline-article-scope','manuscript'),('invented-offline-page-observation','manuscript'),
        ('missing-offline-native-page','native'),('missing-observed-page','actual')]:
        config=deepcopy(conf);doc=load(config[key])
        if kind=='false-offline-article-scope':next(r for r in doc['records'] if r['offline_only'])['offline_only']=False
        elif kind=='invented-offline-page-observation':next(r for r in doc['records'] if r['offline_only'])['planned_stored_pages'][0]['actual_frame']=12345
        elif kind=='missing-offline-native-page':doc['records']=[r for r in doc['records'] if r['topic_id']!=23]
        else:doc['actual_HELP_cases'].pop()
        changed=ROOT/(kind+'.json');save(changed,doc);config[key]=str(changed);config['dependencies'][str(changed)]=sha(changed.read_bytes())
        if key=='actual':
            approved=load(config['actual_visual']);approved['actual_proof']=str(changed);approved['actual_proof_sha256']=sha(changed.read_bytes())
            path=ROOT/(kind+'_visual.json');save(path,approved);config['actual_visual']=str(path);config['dependencies'][str(path)]=sha(path.read_bytes())
        path=ROOT/(kind+'_config.json');save(path,config)
        try:plan_release(image,base,path)
        except (ValueError,AssertionError,KeyError) as error:rejected.append(dict(case=kind,error_type=type(error).__name__,error=str(error)))
        else:raise AssertionError('Accepted invalid partial-coverage case:'+kind)
        assert bytes(image.rom.save())==before and bytes(base.rom.save())==base_before
    assert len(rejected)==4
    old=registry['profiles'][prep['previous_profile']]
    for i,(key,path) in enumerate(prep['preserved_stage_configs'].items()):
        prior,new=load(old[key]),load(path);allowed={'parent_ROM_sha256','target_ROM_sha256'}|({'parent_manifest','builder_dependencies'} if i==0 else set())
        assert {k:v for k,v in prior.items() if k not in allowed}=={k:v for k,v in new.items() if k not in allowed}
        if i==0:assert all(new['builder_dependencies'][k]==v for k,v in prior['builder_dependencies'].items())
    previous=Path('work/analysis/Early_HELP23_release_qualification_20261104/qualification.json')
    formatter=Path('work/analysis/Shared_HELP_T21_T43_formatting_20261104/preview_qualification_v2/qualification.json')
    assert len(load(previous)['semantic_rejections'])==10 and len(load(formatter)['new_semantic_rejections'])==4
    save(ROOT/'qualification.json',dict(profile=prep['profile'],preparation=str(PREP),preparation_sha256=sha(PREP.read_bytes()),
        registry_sha256=prep['registry_sha256'],positive_Help_plan=proof,direct_andshared_Help_targets_equal=True,shared_extension_proof=shared_proof,
        changed_partial_coverage_rejections=rejected,unchanged_eight_final_stage_contracts_compared_exactly=True,
        previous_unchanged_source_gates_andruntime_name_stage_proofs=str(previous),previous_unchanged_proofs_sha256=sha(previous.read_bytes()),
        new_formatter_semantic_guards=str(formatter),new_formatter_semantic_guards_sha256=sha(formatter.read_bytes()),
        unchanged_native_characterization_not_reexecuted=True,all_inputs_unowned_bytes_andcomplete_inverses_preserved=True,
        registered_build_patch_andown_startup_pending=True,new_credit=0,producer_sha256=sha(Path(__file__).read_bytes())))
    print('Town23 direct/shared plans/four changed coverage guards pass;four formatter guards andten unchanged guards reused;all eight stages preserved.')
