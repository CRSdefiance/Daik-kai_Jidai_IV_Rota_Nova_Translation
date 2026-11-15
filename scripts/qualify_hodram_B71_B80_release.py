"""One exact release plan and meaningful rejection cases; caller images stay unchanged."""
from copy import deepcopy
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.late_editorial_extensions_v1 import plan_extensions
from dk4tool.patch.reviewed_scene_batch_v2 import plan_release
from dk4tool.rom.nds import NdsImage
from scripts.audit_story_glyph_consistency import load,save

ROOT=Path('work/analysis/Hodram_B71_B80_release_qualification_20261101')
CONF=Path('translations/hodram_B71_B80_editorial_release_v1.json')

if __name__=='__main__':
    assert not ROOT.exists();ROOT.mkdir(parents=True)
    config=load(CONF)
    current=load('out/all_routes_combined_hodram_julio_20261101_candidate.manifest.json')
    image=NdsImage.open(current['production_pipeline']['canonical_stage'])
    baseline=NdsImage.open('out/raphael_natural_v2_accepted_base.nds')
    before,base_before=bytes(image.rom.save()),bytes(baseline.rom.save())
    target,report=plan_release(image,baseline,CONF)
    assert sha(bytes(target.save()))==config['target_ROM_sha256'] and len(report['changed_records'])==144
    assert bytes(image.rom.save())==before and bytes(baseline.rom.save())==base_before
    rejected=[]
    for case in ['missing-record','failed-context-gate','changed-prose','wrong-speaker-plan']:
        temporary=deepcopy(config)
        kind='plan' if case=='wrong-speaker-plan' else 'manuscript'
        document=load(config[kind])
        if case=='missing-record':document['records'].pop()
        if case=='failed-context-gate':document['records'][0]['review']['context']=False
        if case=='changed-prose':document['records'][0]['english']+=' Unexpected addition.'
        if case=='wrong-speaker-plan':
            row=document['records'][0];raw=bytes.fromhex(row['encoded_hex'])
            row['encoded_hex']=(bytes([1])+raw[1:]).hex()
            assert raw[0]!=1
        path=ROOT/(case+'.json');save(path,document)
        temporary[kind]=str(path);temporary['dependencies'][str(path)]=sha(path.read_bytes())
        conf=ROOT/(case+'_config.json');save(conf,temporary)
        try:plan_release(image,baseline,conf)
        except (ValueError,AssertionError,KeyError) as error:
            rejected.append(dict(case=case,error_type=type(error).__name__,message=str(error)))
        else:raise AssertionError(case+' was not rejected')
        assert bytes(image.rom.save())==before and bytes(baseline.rom.save())==base_before
    wrong=deepcopy(image);bad=bytearray(wrong.read_file('/data/SC1.DK4'));bad[-1]^=1
    wrong.replace_file('/data/SC1.DK4',bytes(bad));wrong_before=bytes(wrong.rom.save())
    try:plan_release(wrong,baseline,CONF)
    except ValueError as error:rejected.append(dict(case='wrong-parent',message=str(error)))
    else:raise AssertionError('wrong-parent was not rejected')
    assert bytes(wrong.rom.save())==wrong_before and bytes(baseline.rom.save())==base_before
    registry=load('translations/release_stack.json')
    spec=registry['profiles']['all-routes-hodram-b71-b80-20261101']['late_editorial_extensions'][-1]
    staged,reports=plan_extensions(image,baseline,[spec])
    assert bytes(staged.save())==bytes(target.save()) and len(reports)==1
    broken={**spec,'target_ROM_sha256':'0'*64}
    try:plan_extensions(image,baseline,[broken])
    except ValueError as error:rejected.append(dict(case='shared-late-target',message=str(error)))
    else:raise AssertionError('shared target mismatch was not rejected')
    assert bytes(image.rom.save())==before and bytes(baseline.rom.save())==base_before
    save(ROOT/'qualification.json',dict(config=str(CONF),config_sha256=sha(CONF.read_bytes()),
        complete_pre_runtime_target_sha256=config['target_ROM_sha256'],positive_plan=report,
        all_six_negative_cases_rejected_before_caller_mutation=rejected,
        direct_andshared_pure_planners_produce_exact_same_target=True,
        canonical_baseline_andall_caller_objects_preserved=True,
        old_renderer_engine_orframework_investigation_not_repeated=True,
        new_credit=0,producer_sha256=sha(Path(__file__).read_bytes())))
    print('Exact direct/shared target;6 meaningful stale/semantic/late-target rejections;caller images unchanged.')
