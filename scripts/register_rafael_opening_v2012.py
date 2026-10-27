"""Register complete reviewed B44 after V1986; preserve every older profile."""
from copy import deepcopy
import os
from pathlib import Path
from dk4tool.patch import rafael_opening_editorial as owned
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.verify_village_wrap_v608 import read,save

DOC=Path('translations/rafael_opening_contextual_editorial_manuscript_v3.json')
CHOICES=Path('translations/rafael_opening_contextual_choices_editorial_draft_v2.json')
MAP=Path('translations/rafael_opening_editorial_relocation_map_v1.json')
ACTUAL0=Path('work/analysis/rafael_guided_actual_v2009/guided_preparation_repaired_outer_skip_and_Lisbon_return.json')
ACTUAL1=Path('work/analysis/rafael_independent_actual_v2007e/independent_preparation_and_normal_Lisbon_return.json')
ROOT=Path('work/analysis/rafael_opening_release_v2012')
PROFILE='all-routes-unified-v2013'
CONFIG='translations/rafael_opening_editorial_release_v1.json'
PARENT=Path('out/all_routes_combined_v1986_candidate.nds')
RESEARCH=Path('work/analysis/rafael_opening_relocation_v2001b/rafael_opening_V1986_derived_RESEARCH_ONLY.nds')

if __name__=='__main__':
    assert not ROOT.exists()and not Path(CONFIG).exists()
    assert sha(PARENT.read_bytes())=='f2dcb4cc4d688e1cd40a22367180841d27d06e540edbd16927f784b2cfcb50ca'
    assert sha(RESEARCH.read_bytes())=='29d9de4bdd46231b865cbe39a0592dd65a0c55378dfdbb7d8c10aa6104ca7d55'
    base_path=Path('out/raphael_natural_v2_accepted_base.nds')
    assert sha(base_path.read_bytes())=='3cb827e4c52ab2086fb5a626835d72192085a958581279d3c79b0200bbf405fe'
    image,baseline,clean=map(NdsImage.open,(PARENT,base_path,'work/clean.nds'))
    doc,menu,mapping=map(read,(DOC,CHOICES,MAP))
    files={str(p)for p in(DOC,CHOICES,MAP,ACTUAL0,ACTUAL1,Path(__file__),
        Path('scripts/approve_rafael_opening_v2010.py'),Path('scripts/approve_rafael_opening_v2010b.py'),
        Path('work/analysis/rafael_opening_approval_v2010b/approval_receipt.json'),
        Path('dk4tool/dialogue/rafael_opening_profile.py'),Path('dk4tool/patch/rafael_opening_editorial.py'))}
    files.update(mapping['evidence'])
    config=dict(format='dk4-rafael-opening-editorial-release-v1',manuscript=str(DOC),choices=str(CHOICES),reference_map=str(MAP),
        source_SC0_sha256=sha(image.read_file(owned.PATH)),target_SC0_sha256=sha(NdsImage.open(RESEARCH).read_file(owned.PATH)),
        canonical_SC0_sha256=sha(baseline.read_file(owned.PATH)),clean_ROM='work/clean.nds',clean_ROM_sha256=sha(Path('work/clean.nds').read_bytes()),
        clean_SC0_sha256=sha(clean.read_file(owned.PATH)),required_runtime_ARM9_sha256=sha(image.read_file('/__arm9__.bin')),
        tested_research_ROM_sha256=sha(RESEARCH.read_bytes()),dependencies={p:sha(Path(p).read_bytes())for p in sorted(files)})
    registry_path,builder=Path('translations/release_stack.json'),Path('scripts/build_integrated_release.py')
    raw,before=registry_path.read_bytes(),builder.read_bytes();registry=read(registry_path)
    assert PROFILE not in registry['profiles']and len(registry['accepted_layers'])==114
    assert registry['latest_promoted_build']['profile']=='all-routes-unified-v1492'
    assert b"profile_config.get('rafael_opening_editorial')"not in before
    stage=b'''    rafael_opening_editorial = profile_config.get('rafael_opening_editorial')
    if rafael_opening_editorial:
        from dk4tool.patch.rafael_opening_editorial import apply_release as apply_rafael_opening_editorial

        rafael_report = apply_rafael_opening_editorial(candidate, baseline, rafael_opening_editorial)
        file_path = '/data/SC0.DK4'
        grouped.setdefault(file_path, [])
        changed_records.setdefault(file_path, []).extend(row['id'] for row in rafael_report['changed_records'])
        relocation_checks.setdefault(file_path, {})['rafael_opening_editorial'] = {
            'release_config': rafael_opening_editorial,
            'release_config_sha256': sha256(Path(rafael_opening_editorial).read_bytes()),
            'proof': rafael_report}
        for batch_name in ('manuscript', 'choices'):
            rafael_batch = Path(rafael_report[batch_name])
            if rafael_batch in release_batches:
                raise ValueError('Rafael opening must run after the complete frozen cumulative stages')
            release_batches.append(rafael_batch)

'''
    anchor=b'    # Lexically valid "% o"';assert before.count(anchor)==1
    at=before.index(anchor);after=before[:at]+stage+before[at:];compile(after,str(builder),'exec')
    ROOT.mkdir(parents=True)
    (ROOT/'registry_before_raw.json').write_bytes(raw);(ROOT/'builder_before.py').write_bytes(before);(ROOT/'builder_added_optional_stage.bin').write_bytes(stage)
    save(CONFIG,config)
    report=owned.apply_release(image,baseline)
    assert image.read_file(owned.PATH)==NdsImage.open(RESEARCH).read_file(owned.PATH)
    assert report['typed_commands']==182 and report['relative_sites']==4 and len(report['explicit_inherited_relative_repairs'])==2
    assert report['blocks'][0]['growth_bytes']==60 and report['compiled_progressive_records']==114
    save(ROOT/'native_source_release_plan.json',report)
    negatives=[]
    def reject(label,target,cfgpath=CONFIG,base=baseline):
        previous=target.read_file(owned.PATH)
        try:owned.apply_release(target,base,cfgpath)
        except ValueError as exc:
            assert target.read_file(owned.PATH)==previous
            negatives.append(dict(case=label,error=str(exc),no_partial_SC0_mutation=True))
        else:raise AssertionError('Invalid Rafael release accepted: '+label)
    reject('repeat-application',image)
    for label,path in(('wrong-runtime','/__arm9__.bin'),('wrong-source',owned.PATH)):
        target=NdsImage.open(PARENT);data=bytearray(target.read_file(path));data[0x100]^=1;target.replace_file(path,bytes(data));reject(label,target)
    wrong_base=NdsImage.open(base_path);data=bytearray(wrong_base.read_file(owned.PATH));data[0x100]^=1;wrong_base.replace_file(owned.PATH,bytes(data))
    reject('wrong-canonical',NdsImage.open(PARENT),base=wrong_base)
    tests=('incomplete-map','missing-command','wrong-command-target','wrong-relative-span','wrong-relative-target','missing-relative-site','undeclared-old-repair',
        'unreviewed-formatting','changed-prose','changed-speaker','authored-padding','wrong-source-index','wrong-current-index','wrong-target-index',
        'wrong-Japanese-hex','wrong-Japanese-prose','invented-macro','changed-FE','changed-choice','unreviewed-choice','false-actual')
    for label in tests:
        kind='reference_map'if label in tests[:7]else'choices'if label in('changed-choice','unreviewed-choice')else'manuscript'
        value=deepcopy(mapping if kind=='reference_map'else menu if kind=='choices'else doc);bad=deepcopy(config)
        if label=='incomplete-map':value['external_references_complete']=False
        elif label=='missing-command':value['mapped_native_commands'].pop()
        elif label=='wrong-command-target':value['mapped_native_commands'][3]['new_offset']+=2
        elif label=='wrong-relative-span':value['relative_skip_fixups'][0]['target_span']+=2
        elif label=='wrong-relative-target':value['relative_skip_fixups'][0]['new_matched_skip_target']+=2
        elif label=='missing-relative-site':value['relative_skip_fixups'].pop()
        elif label=='undeclared-old-repair':value['relative_skip_fixups'][1]['inherited_stale_span_explicitly_repaired']=False
        elif label=='unreviewed-formatting':value['records'][0]['review']['formatting']=False
        elif label=='changed-prose':value['records'][0]['english']+=' Extra words.'
        elif label=='changed-speaker':value['records'][0]['english']=value['records'][0]['english'].replace('SPEAKER:05','SPEAKER:04')
        elif label=='authored-padding':value['records'][0]['english']+='{PAD}'
        elif label=='wrong-source-index':value['records'][0]['source_record_index']+=1
        elif label=='wrong-current-index':value['records'][0]['record_index']+=1
        elif label=='wrong-target-index':value['records'][0]['target_record_index']+=1
        elif label=='wrong-Japanese-hex':value['records'][0]['source_hex']=value['records'][0]['source_hex'][:-2]+'20'
        elif label=='wrong-Japanese-prose':value['records'][0]['source_Japanese']+='違う'
        elif label=='invented-macro':value['records'][0]['english']+='{MACRO:FI}'
        elif label=='changed-FE':next(r for r in value['records']if r['source_presentation_prefix_hex']=='fe')['english']='{SPEAKER:FE}Received 300 gold!'
        elif label=='changed-choice':value['records'][0]['english']='Ask her.{PAD}'
        elif label=='unreviewed-choice':value['records'][0]['review']['formatting']=False
        else:
            proof=deepcopy(read(ACTUAL0));proof['actual_repaired_outer0100_length72_and_cleanup6742']=False
            proof_path=ROOT/'false_actual.json';save(proof_path,proof);value['actual_choice0_proof']=str(proof_path);bad['dependencies'][str(proof_path)]=sha(proof_path.read_bytes())
        path=ROOT/(label+'.json');save(path,value);bad[kind]=str(path);bad['dependencies'][str(path)]=sha(path.read_bytes())
        cfgpath=ROOT/(label+'_config.json');save(cfgpath,bad);reject(label,NdsImage.open(PARENT),cfgpath)
    assert len(negatives)==25
    profile=deepcopy(registry['profiles']['all-routes-unified-v1986'])
    profile.update(rafael_opening_editorial=CONFIG,status='experimental',
        description='Complete V1986 stack plus the full117-entry fresh Rafael Lisbon opening review andtwo clean-derived tutorial skip repairs.',
        note='33prose revisions84retentions.115speeches/twochoices reviewed;114progressive native planes,916macro calls,separate money FE andnative labels,both ordinary gameplay choices andnormal Lisbon returns pass.OnlySC0B44 grows60bytes;342otherblocks andallotherfiles/components exact.487batches114acceptedlayers expected;cleanpatch/startup pending,V1492 promoted.')
    registry['profiles'][PROFILE]=profile
    assert registry_path.read_bytes()==raw and builder.read_bytes()==before
    pending=registry_path.with_name('release_stack_v2012_pending.json');assert not pending.exists();save(pending,registry)
    builder.write_bytes(after);os.replace(pending,registry_path)
    restored=deepcopy(read(registry_path));restored['profiles'].pop(PROFILE)
    assert restored==read(ROOT/'registry_before_raw.json')and builder.read_bytes().replace(stage,b'',1)==before
    save(ROOT/'registration_provenance.json',dict(profile=PROFILE,source_profile='all-routes-unified-v1986',source_parent=str(PARENT),source_parent_sha256=sha(PARENT.read_bytes()),
        all_previous_profiles_accepted_layers_and_promotion_preserved=True,registry_before_sha256=sha(raw),registry_after_sha256=sha(registry_path.read_bytes()),
        builder_before_sha256=sha(before),builder_after_sha256=sha(after),release_config_sha256=sha(Path(CONFIG).read_bytes()),
        negative_cases=negatives,source_compiler_exact_to_research_SC0=True,new_registered_candidate_not_yet_built=True,
        producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    print(dict(profile=PROFILE,negative_cases=25,compiler_exact_research=True,accepted_layers=114,changed_speech_commands=len(report['changed_records'])))
