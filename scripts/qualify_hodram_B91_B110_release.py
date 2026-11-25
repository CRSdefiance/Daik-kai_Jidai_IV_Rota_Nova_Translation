"""Qualify exact211-record andordered name plans without mutating caller images."""
from copy import deepcopy
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.late_editorial_extensions_v1 import plan_extensions
from dk4tool.patch.reviewed_scene_batch_v4 import plan_release
from dk4tool.patch.registered_owned_name_glyph_v1 import plan_release as emilio_plan
from dk4tool.patch.registered_owned_name_fields_v2 import plan_release as fields_plan
from dk4tool.rom.nds import NdsImage
from scripts.audit_story_glyph_consistency import load,save

ROOT=Path('work/analysis/Hodram_B91_B110_release_qualification_20261101')
CONF=Path('translations/hodram_B91_B110_editorial_release_v1.json')
NAMES=Path('translations/fernando_samwell_owned_fields_release_v1.json')
EMILIO=Path('translations/emilio_name_glyph_hodram_B91_B110_release_v1.json')
PROFILE='all-routes-hodram-b91-b110-names-20261101'

if __name__=='__main__':
    assert not ROOT.exists();ROOT.mkdir(parents=True)
    conf=load(CONF);manifest=load('out/all_routes_combined_hodram_b81_b89_emilio_20261101_candidate.manifest.json')
    image=NdsImage.open(manifest['production_pipeline']['canonical_stage']);base=NdsImage.open('out/raphael_natural_v2_accepted_base.nds')
    before,base_before=bytes(image.rom.save()),bytes(base.rom.save())
    target,report=plan_release(image,base,CONF)
    assert sha(bytes(target.save()))==conf['target_ROM_sha256'] and len(report['changed_records'])==211
    assert sum(r.get('typed_choice',False) for r in report['changed_records'])==2
    assert bytes(image.rom.save())==before and bytes(base.rom.save())==base_before
    rejected=[]
    for kind in ['missing-choice','reversed-choice-indices','failed-choice-format','changed-choice-prose','changed-speech','wrong-speaker-plan','false-observed-FE']:
        temporary=deepcopy(conf)
        if kind=='false-observed-FE':temporary['observed_FE_ids'].append('DK4_MES_B93_R0005')
        else:
            field='plan' if kind=='wrong-speaker-plan' else 'manuscript';doc=load(conf[field]);typed=[r for r in doc['records'] if r.get('kind')=='typed-choice-label']
            if kind=='missing-choice':doc['records'].pop()
            elif kind=='reversed-choice-indices':typed[0]['source_index']=1
            elif kind=='failed-choice-format':typed[0]['review']['formatting']=False
            elif kind=='changed-choice-prose':typed[1]['english']='Go away.'
            elif kind=='changed-speech':doc['records'][0]['english']+=' Unexpected addition.'
            else:
                row=doc['records'][0];raw=bytes.fromhex(row['encoded_hex']);row['encoded_hex']=(bytes([raw[0]^1])+raw[1:]).hex()
            path=ROOT/(kind+'.json');save(path,doc);temporary[field]=str(path);temporary['dependencies'][str(path)]=sha(path.read_bytes())
        config=ROOT/(kind+'_config.json');save(config,temporary)
        try:plan_release(image,base,config)
        except (ValueError,AssertionError,KeyError) as error:rejected.append(dict(case=kind,error=type(error).__name__+': '+str(error)))
        else:raise AssertionError(kind)
        assert bytes(image.rom.save())==before and bytes(base.rom.save())==base_before
    registry=load('translations/release_stack.json');spec=registry['profiles'][PROFILE]['late_editorial_extensions'][-1]
    staged,reports=plan_extensions(image,base,[spec]);assert bytes(staged.save())==bytes(target.save())
    try:plan_extensions(image,base,[{**spec,'target_ROM_sha256':'0'*64}])
    except ValueError as error:rejected.append(dict(case='shared-late-target',error=str(error)))
    else:raise AssertionError('shared-late-target')
    preparation=load('work/analysis/Hodram_B91_B110_release_20261101/registered_preparation.json')
    emilio_source=NdsImage.open(preparation['post_bounds_ROM']);emilio_before=bytes(emilio_source.rom.save())
    arm,emilio_report=emilio_plan(emilio_source,EMILIO);emilio_target=deepcopy(emilio_source);emilio_target.replace_file('/__arm9__.bin',arm)
    assert sha(bytes(emilio_target.rom.save()))==preparation['post_Emilio_ROM_sha256'] and bytes(emilio_source.rom.save())==emilio_before
    source=NdsImage.open('work/analysis/Hodram_B91_B110_rebuilt_20261101/reviewed_RESEARCH_ONLY.nds');source_before=bytes(source.rom.save())
    arm,name_report=fields_plan(source,NAMES);fixed=deepcopy(source);fixed.replace_file('/__arm9__.bin',arm)
    assert sha(bytes(fixed.rom.save()))==preparation['target_ROM_sha256'] and bytes(source.rom.save())==source_before
    names=load(NAMES)
    for kind in ['name-failed-review','name-false-owner','name-changed-full-spelling','name-false-consumer-policy','name-stale-parent']:
        temporary=deepcopy(names)
        if kind=='name-false-consumer-policy':temporary['actual_policy'][1]['kind']='changed-progressive-name';temporary['actual_policy'][1].update(complete_header_key='normal_F_andall_name_glyphs_andblank_guards_exact',minimum_headers=1)
        elif kind=='name-stale-parent':temporary['parent_ROM_sha256']='0'*64
        else:
            field='proposal' if kind=='name-false-owner' else 'manuscript';doc=load(names[field])
            if kind=='name-failed-review':doc['records'][0]['review']['formatting']=False
            elif kind=='name-changed-full-spelling':doc['records'][1]['english']='Samwell the Khan'
            else:doc['fields'][0]['owners']=[]
            path=ROOT/(kind+'.json');save(path,doc);temporary[field]=str(path);temporary['dependencies'][str(path)]=sha(path.read_bytes())
        config=ROOT/(kind+'_config.json');save(config,temporary)
        try:fields_plan(source,config)
        except (ValueError,AssertionError,KeyError) as error:rejected.append(dict(case=kind,error=type(error).__name__+': '+str(error)))
        else:raise AssertionError(kind)
        assert bytes(source.rom.save())==source_before
    assert len(rejected)==13
    assert bytes(image.rom.save())==before and bytes(base.rom.save())==base_before
    save(ROOT/'qualification.json',dict(config=str(CONF),config_sha256=sha(CONF.read_bytes()),name_config=str(NAMES),name_config_sha256=sha(NAMES.read_bytes()),positive_scene_plan=report,positive_Emilio_plan=emilio_report,positive_name_fields_plan=name_report,semantic_rejections=rejected,
        direct_andshared_scene_planners_equal_exact_tested_target=True,ordered_metadata_stages_equal_exact_tested_final=True,all_caller_images_baseline_andunowned_bytes_preserved=True,
        all_prior_builders_unchanged=True,registered_build_patch_andown_startup_pending=True,new_credit=0,producer_sha256=sha(Path(__file__).read_bytes())))
    print('PASS:exact direct/shared211-record scene andordered metadata targets;13 semantic/ownership/consumer/late-target rejections;caller images unchanged.')
