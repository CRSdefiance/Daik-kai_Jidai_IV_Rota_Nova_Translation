"""Exact pure scene/name plans and semantic rejection cases before the cumulative build."""
from copy import deepcopy
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.late_editorial_extensions_v1 import plan_extensions
from dk4tool.patch.reviewed_scene_batch_v3 import plan_release
from dk4tool.patch.registered_owned_name_glyph_v1 import plan_release as name_plan
from dk4tool.rom.nds import NdsImage
from scripts.audit_story_glyph_consistency import load,save

ROOT=Path('work/analysis/Hodram_B81_B89_release_qualification_20261101')
CONF=Path('translations/hodram_B81_B89_editorial_release_v1.json')
NAME=Path('translations/emilio_name_glyph_release_v1.json')
PROFILE='all-routes-hodram-b81-b89-emilio-20261101'

if __name__=='__main__':
    assert not ROOT.exists();ROOT.mkdir(parents=True)
    conf=load(CONF);manifest=load('out/all_routes_combined_hodram_b71_b80_20261101_candidate.manifest.json')
    image=NdsImage.open(manifest['production_pipeline']['canonical_stage']);base=NdsImage.open('out/raphael_natural_v2_accepted_base.nds')
    before,base_before=bytes(image.rom.save()),bytes(base.rom.save())
    target,report=plan_release(image,base,CONF)
    assert sha(bytes(target.save()))==conf['target_ROM_sha256'] and len(report['changed_records'])==306
    assert sum(r.get('typed_choice',False) for r in report['changed_records'])==2
    assert bytes(image.rom.save())==before and bytes(base.rom.save())==base_before
    rejected=[]
    for kind in ['missing-choice','reversed-choice-indices','failed-choice-format','changed-choice-prose','changed-speech','wrong-speaker-plan']:
        temporary=deepcopy(conf);field='plan' if kind=='wrong-speaker-plan' else 'manuscript';doc=load(conf[field])
        typed=[r for r in doc['records'] if r.get('kind')=='typed-choice-label']
        if kind=='missing-choice':doc['records'].pop()
        elif kind=='reversed-choice-indices':typed[0]['source_index']=1
        elif kind=='failed-choice-format':typed[0]['review']['formatting']=False
        elif kind=='changed-choice-prose':typed[1]['english']='No money.'
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
    assert bytes(image.rom.save())==before and bytes(base.rom.save())==base_before
    names=load(NAME);name_source=NdsImage.open('work/analysis/Hodram_B81_B89_rebuild_20261101/reviewed_RESEARCH_ONLY.nds')
    name_before=bytes(name_source.rom.save());arm,name_report=name_plan(name_source,NAME)
    fixed=deepcopy(name_source);fixed.replace_file('/__arm9__.bin',arm)
    assert sha(bytes(fixed.rom.save()))==names['target_ROM_sha256']
    assert bytes(name_source.rom.save())==name_before
    for kind in ['name-failed-review','name-false-owner','name-wrong-glyph']:
        temporary=deepcopy(names);field='manuscript' if kind=='name-failed-review' else 'proposal';doc=load(names[field])
        if kind=='name-failed-review':doc['records'][0]['review']['formatting']=False
        elif kind=='name-false-owner':doc['all207_name_fields_interior_oralias_owners']=[]
        else:doc['target_hex']='4665726f67780000'
        path=ROOT/(kind+'.json');save(path,doc);temporary[field]=str(path);temporary['dependencies'][str(path)]=sha(path.read_bytes())
        config=ROOT/(kind+'_config.json');save(config,temporary)
        try:name_plan(name_source,config)
        except (ValueError,AssertionError,KeyError) as error:rejected.append(dict(case=kind,error=type(error).__name__+': '+str(error)))
        else:raise AssertionError(kind)
        assert bytes(name_source.rom.save())==name_before
    assert len(rejected)==10
    save(ROOT/'qualification.json',dict(config=str(CONF),config_sha256=sha(CONF.read_bytes()),name_config=str(NAME),name_config_sha256=sha(NAME.read_bytes()),
        positive_scene_plan=report,positive_name_plan=name_report,semantic_rejections=rejected,
        direct_andshared_scene_planners_equal_exact_tested_target=True,owned_name_stage_equal_exact_tested_final=True,
        all_caller_images_baseline_andunowned_bytes_preserved=True,canonical_builder_unchanged=True,
        registered_build_patch_andown_startup_pending=True,new_credit=0,producer_sha256=sha(Path(__file__).read_bytes())))
    print('PASS:exact direct/shared306-record scene target andowned-name final;10 semantic/late-target rejections;caller images unchanged.')
