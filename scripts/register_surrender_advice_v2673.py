"""Register one guarded optional prose stage;preserve every earlier profile."""
import os
from pathlib import Path
from copy import deepcopy
from dk4tool.patch import surrender_advice_contextual_v1 as owned
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/surrender_advice_registration_v2673')
PROFILE='all-routes-unified-v2674';DOC=Path('translations/aftermath_remaining_contextual_editorial_manuscript_v2.json')
PARENT=Path('out/all_routes_combined_v2284_candidate.nds')

if __name__=='__main__':
    assert not ROOT.exists() and not Path(owned.CONFIG).exists()
    rp=Path('translations/release_stack.json');builder=Path('scripts/build_integrated_release.py')
    raw,before=rp.read_bytes(),builder.read_bytes();registry=read(rp)
    assert PROFILE not in registry['profiles'] and len(registry['accepted_layers'])==114 and registry['latest_promoted_build']['profile']=='all-routes-unified-v1492'
    parent=NdsImage.open(PARENT);base=NdsImage.open('out/raphael_natural_v2_accepted_base.nds')
    planpath=Path('work/analysis/surrender_advice_payload_v2669/payload_plan.json');plan=read(planpath)
    assert sha(PARENT.read_bytes())==plan['source_ROM_sha256']
    font=Path('work/analysis/aftermath_remaining_fonts_v2668/native_layout_and_font_research.json');doc=read(DOC)
    deps={str(DOC),str(Path(owned.__file__)),__file__,str(planpath),str(font),plan['target_ARM9'],plan['target_COMMON'],
        doc['prior_contextual_draft'],doc['source_context_packet'],doc['native_context_proof'],doc['fresh_ordinary_supplement'],
        'scripts/prepare_surrender_advice_payload_v2669.py','scripts/verify_aftermath_remaining_fonts_v2668.py',
        'scripts/battle_aftermath_native_plan_v1255.py','scripts/battle_aftermath_layout_v1250.py',
        'dk4tool/dialogue/review.py','dk4tool/patch/duel_editorial.py'}
    deps.update(s['path'] for s in read(font)['review_sheets'])
    conf=dict(format='dk4-surrender-advice-contextual-v1',manuscript=str(DOC),payload_plan=str(planpath),native_proof=str(font),
        source_ARM9_sha256=plan['source_ARM9_sha256'],source_COMMON_sha256=plan['source_COMMON_sha256'],
        target_ARM9_sha256=plan['target_ARM9_sha256'],target_COMMON_sha256=plan['target_COMMON_sha256'],directory_sha256=plan['directory_sha256'],
        canonical_COMMON_sha256=sha(base.read_file(owned.PATH)),dependencies={p:sha(Path(p).read_bytes()) for p in sorted(deps)})
    ROOT.mkdir(parents=True);positive=ROOT/'positive_config.json';save(positive,conf)
    test=NdsImage.open(PARENT);proof=owned.apply_release(test,base,positive)
    assert test.read_file(owned.PATH)==Path(plan['target_COMMON']).read_bytes() and test.read_file('/__arm9__.bin')==Path(plan['target_ARM9']).read_bytes()
    save(ROOT/'positive_reconstruction.json',proof);negatives=[]
    def reject(label,image,baseline,configpath):
        initial=(image.read_file(owned.PATH),image.read_file('/__arm9__.bin'))
        try:owned.apply_release(image,baseline,configpath)
        except (AssertionError,ValueError):
            assert (image.read_file(owned.PATH),image.read_file('/__arm9__.bin'))==initial;negatives.append(dict(case=label,rejected_before_mutation=True))
        else:raise AssertionError(label)
    reject('repeated_application',test,base,positive)
    for label,path in [('wrong_COMMON',owned.PATH),('wrong_ARM9','/__arm9__.bin')]:
        image=NdsImage.open(PARENT);data=bytearray(image.read_file(path));data[256]^=1;image.replace_file(path,bytes(data));reject(label,image,base,positive)
    wrong=NdsImage.open('out/raphael_natural_v2_accepted_base.nds');data=bytearray(wrong.read_file(owned.PATH));data[32]^=1;wrong.replace_file(owned.PATH,bytes(data));reject('wrong_canonical',NdsImage.open(PARENT),wrong,positive)
    for label,mutate in [('missing_format_review',lambda d:d['records'][0]['review'].update(formatting=False)),
        ('wrong_clean_source',lambda d:d['records'][0].update(source_hex='00')),
        ('changed_retention',lambda d:d['records'][0].update(english='%s won!')),
        ('changed_revision_after_font_proof',lambda d:next(r for r in d['records'] if r['message_id']==2029).update(english='You must surrender immediately!'))]:
        bad=deepcopy(doc);mutate(bad);mp=ROOT/(label+'_manuscript.json');save(mp,bad)
        cfg=deepcopy(conf);cfg['manuscript']=str(mp);cfg['dependencies'][str(mp)]=sha(mp.read_bytes());cp=ROOT/(label+'_config.json');save(cp,cfg)
        reject(label,NdsImage.open(PARENT),base,cp)
    assert len(negatives)==8;save(ROOT/'negative_cases.json',dict(cases=negatives,all_rejected_before_mutation=True))
    stage=b'''    surrender_advice = profile_config.get('surrender_advice_contextual')
    if surrender_advice:
        from dk4tool.patch.surrender_advice_contextual_v1 import apply_release as apply_surrender_advice

        surrender_advice_report = apply_surrender_advice(candidate, baseline, surrender_advice)
        for advice_path in ('/COMMON/MESFILE.DK4', '/__arm9__.bin'):
            grouped.setdefault(advice_path, [])
            relocation_checks.setdefault(advice_path, {})['surrender_advice_contextual'] = {
                'release_config': surrender_advice,
                'release_config_sha256': sha256(Path(surrender_advice).read_bytes()),
                'proof': surrender_advice_report}
        changed_records.setdefault('/COMMON/MESFILE.DK4', []).extend(row['id'] for row in surrender_advice_report['changed_records'])
        changed_records.setdefault('/__arm9__.bin', []).append('SURRENDER_ADVICE_COMMON22_DIRECTORY_AND_OFFSETS')
        advice_batch = Path(surrender_advice_report['manuscript'])
        if advice_batch in release_batches:
            raise ValueError('Surrender advice must run after the complete cumulative stack')
        release_batches.append(advice_batch)

'''
    anchor=b'    # Lexically valid "% o"'
    assert before.count(anchor)==1 and b"profile_config.get('surrender_advice_contextual')" not in before
    after=before.replace(anchor,stage+anchor);compile(after,str(builder),'exec')
    (ROOT/'registry_before_raw.json').write_bytes(raw);(ROOT/'builder_before.py').write_bytes(before);(ROOT/'builder_added_optional_stage.bin').write_bytes(stage)
    save(owned.CONFIG,conf)
    profile=deepcopy(registry['profiles']['all-routes-unified-v2284']);profile.update(surrender_advice_contextual=owned.CONFIG,
        description='Complete V2284 cumulative stack plus the source-bound courteous surrender recommendation in COMMON2029.',
        note='Aftermath34 contextual/native reviewed;33retentions,one tone correction. Registered build,patch,startup andfinal representative reconciliation pending. Experimental;no promotion andpreserve every ROM.')
    registry['profiles'][PROFILE]=profile
    assert rp.read_bytes()==raw and builder.read_bytes()==before
    temporary=rp.with_name('release_stack_v2673_pending.json');assert not temporary.exists();save(temporary,registry)
    builder.write_bytes(after);os.replace(temporary,rp)
    restored=deepcopy(read(rp));restored['profiles'].pop(PROFILE)
    assert restored==read(ROOT/'registry_before_raw.json') and builder.read_bytes().replace(stage,b'',1)==before
    save(ROOT/'registration_receipt.json',dict(profile=PROFILE,parent_profile='all-routes-unified-v2284',config=owned.CONFIG,
        config_sha256=sha(Path(owned.CONFIG).read_bytes()),all114accepted_layers_previous_profiles_and_V1492_promotion_unchanged=True,
        only_one_optional_stage_and_one_experimental_profile_added=True,negative_cases=8,
        release_stack_sha256=sha(rp.read_bytes()),builder_sha256=sha(builder.read_bytes()),
        no_ROM_created_or_promoted=True,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    print('Registered all-routes-unified-v2674:one optional prose-only stage afterV2284;8negative cases reject before mutation;all earlier profiles/accepted layers preserved.')
