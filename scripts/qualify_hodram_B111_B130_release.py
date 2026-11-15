"""Prove mixed production, preserved name stages and fail-closed semantic guards."""
from copy import deepcopy
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.reviewed_scene_batch_v5 import plan_release
from dk4tool.patch.late_editorial_extensions_v1 import plan_extensions
from dk4tool.patch.registered_owned_name_glyph_v1 import plan_release as emilio_plan
from dk4tool.patch.registered_owned_name_fields_v2 import plan_release as prior_plan
from dk4tool.patch.registered_owned_name_fields_v3 import plan_release as next_plan
from scripts.audit_story_glyph_consistency import load,save

ROOT=Path('work/analysis/Hodram_B111_B130_release_qualification_20261102')
PREPARATION=Path('work/analysis/Hodram_B111_B130_release_20261102/registered_preparation.json')
PROFILE='all-routes-hodram-b111-b130-names-20261102'

def main():
    assert not ROOT.exists();ROOT.mkdir(parents=True)
    prepared=load(PREPARATION);conf_path=Path(prepared['config']);conf=load(conf_path)
    image=NdsImage.open(prepared['canonical_parent']);base=NdsImage.open('out/raphael_natural_v2_accepted_base.nds')
    before,base_before=bytes(image.rom.save()),bytes(base.rom.save())
    target,report=plan_release(image,base,conf_path)
    assert sha(bytes(target.save()))==prepared['pre_runtime_ROM_sha256'] and len(report['changed_records'])==323
    assert bytes(image.rom.save())==before and bytes(base.rom.save())==base_before
    rejected=[]
    for kind in ['missing-choice','wrong-third-index','failed-style-review','changed-style-alias','changed-choice-prose','changed-speech','wrong-speaker-plan','bad-style-prefix','false-changed-scope','false-FE-membership']:
        config=deepcopy(conf)
        if kind=='false-changed-scope':config['blocks'].append(128)
        elif kind=='false-FE-membership':config['FE_count']+=1
        else:
            field='plan' if kind in ['wrong-speaker-plan','bad-style-prefix'] else 'manuscript';doc=load(conf[field])
            if field=='plan':
                row=next(r for r in doc['records'] if ('STYLE' in r['id'])==(kind=='bad-style-prefix'))
                raw=bytes.fromhex(row['encoded_hex']);row['encoded_hex']=(bytes([raw[0]^1])+raw[1:]).hex()
            else:
                choices=[r for r in doc['records'] if r['kind']=='typed-choice-label'];styles=[r for r in doc['records'] if r.get('native_object_kind')=='4100-style-alternative']
                if kind=='missing-choice':doc['records'].remove(choices[-1])
                elif kind=='wrong-third-index':choices[2]['source_index']=1
                elif kind=='failed-style-review':styles[0]['review']['formatting']=False
                elif kind=='changed-style-alias':styles[0]['source_style_indices']=[]
                elif kind=='changed-choice-prose':choices[0]['english']='Unreviewed answer.'
                else:doc['records'][0]['english']+=' Unexpected addition.'
            path=ROOT/(kind+'.json');save(path,doc);config[field]=str(path);config['dependencies'][str(path)]=sha(path.read_bytes())
        path=ROOT/(kind+'_config.json');save(path,config)
        try:plan_release(image,base,path)
        except (ValueError,AssertionError,KeyError) as error:rejected.append(dict(case=kind,error=type(error).__name__+': '+str(error)))
        else:raise AssertionError(kind)
        assert bytes(image.rom.save())==before and bytes(base.rom.save())==base_before
        print('Rejected',kind,flush=True)
    spec=load('translations/release_stack.json')['profiles'][PROFILE]['late_editorial_extensions'][-1]
    staged,shared=plan_extensions(image,base,[spec]);assert bytes(staged.save())==bytes(target.save())
    try:plan_extensions(image,base,[{**spec,'target_ROM_sha256':'0'*64}])
    except ValueError as error:rejected.append(dict(case='shared-late-target',error=str(error)))
    else:raise AssertionError('shared-late-target')
    metadata=[]
    for source_key,config_key,planner,target_key in [('post_bounds_ROM','emilio_config',emilio_plan,'post_Emilio_ROM_sha256'),
        ('post_Emilio_ROM','prior_fields_config',prior_plan,'post_prior_fields_ROM_sha256'),('post_prior_fields_ROM','next_fields_config',next_plan,'target_ROM_sha256')]:
        source=NdsImage.open(prepared[source_key]);original=bytes(source.rom.save());arm,proof=planner(source,prepared[config_key]);result=deepcopy(source);result.replace_file('/__arm9__.bin',arm)
        assert sha(bytes(result.rom.save()))==prepared[target_key] and bytes(source.rom.save())==original
        metadata.append(dict(config=prepared[config_key],proof=proof,target=prepared[target_key]))
    source=NdsImage.open(prepared['post_prior_fields_ROM']);original=bytes(source.rom.save());fields=load(prepared['next_fields_config'])
    for kind in ['name-failed-review','name-false-owner','name-changed-full-spelling','name-false-consumer-policy','name-stale-parent']:
        config=deepcopy(fields)
        if kind=='name-stale-parent':config['parent_ROM_sha256']='0'*64
        elif kind=='name-false-consumer-policy':config['actual_policy'][1]['kind']='changed-progressive-name';config['actual_policy'][1].update(complete_header_key='normal_F_andall_name_glyphs_andblank_guards_exact',minimum_headers=1)
        else:
            field='proposal' if kind=='name-false-owner' else 'manuscript';doc=load(config[field])
            if kind=='name-failed-review':doc['records'][0]['review']['formatting']=False
            elif kind=='name-changed-full-spelling':doc['records'][1]['english']='Lord Diogo Escante'
            else:doc['fields'][0]['owners']=[]
            path=ROOT/(kind+'.json');save(path,doc);config[field]=str(path);config['dependencies'][str(path)]=sha(path.read_bytes())
        path=ROOT/(kind+'_config.json');save(path,config)
        try:next_plan(source,path)
        except (ValueError,AssertionError,KeyError) as error:rejected.append(dict(case=kind,error=type(error).__name__+': '+str(error)))
        else:raise AssertionError(kind)
        assert bytes(source.rom.save())==original
    assert len(rejected)==16 and bytes(image.rom.save())==before and bytes(base.rom.save())==base_before
    save(ROOT/'qualification.json',dict(config=str(conf_path),config_sha256=sha(conf_path.read_bytes()),positive_scene_plan=report,ordered_metadata_plans=metadata,
        semantic_rejections=rejected,direct_andshared_scene_planners_equal_exact_tested_target=True,ordered_metadata_stages_equal_exact_tested_final=True,
        all_caller_images_baseline_andunowned_bytes_preserved=True,all_prior_builders_unchanged=True,registered_build_patch_andown_startup_pending=True,new_credit=0,
        producer_sha256=sha(Path(__file__).read_bytes())))
    print('PASS323-record direct/shared production andall preserved metadata stages;16 semantic/ownership/consumer/late-target rejections.',flush=True)

if __name__=='__main__':main()
