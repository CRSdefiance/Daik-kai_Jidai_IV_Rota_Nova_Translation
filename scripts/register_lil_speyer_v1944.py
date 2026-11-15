"""Register Speyer after the complete preserved V1909 stack; no promotion."""
from copy import deepcopy
import os
from pathlib import Path
from dk4tool.patch import lil_speyer_editorial as owned
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.approve_lil_speyer_references_v1942 import DOC,CHOICES,MAP,ACTUAL
from scripts.verify_village_wrap_v608 import read,save

CONFIG='translations/lil_speyer_editorial_release_v1.json'
ROOT=Path('work/analysis/lil_Speyer_release_v1944')
PROFILE='all-routes-unified-v1945'
PARENT=Path('out/all_routes_combined_v1909_candidate.nds')
RESEARCH=Path('work/analysis/lil_Speyer_research_v1929/lil_Speyer_V1909_derived_RESEARCH_ONLY.nds')

if __name__=='__main__':
    assert not ROOT.exists() and not Path(CONFIG).exists()
    assert sha(PARENT.read_bytes())=='fdc6757a13af0a04c4f2355ade3c66163a6382a0a7081efa03a457b1198dd1d1'
    assert sha(RESEARCH.read_bytes())=='c2432768da7e12c6fce7af9e4d887af932de2532a2d3a16eddbbe407067f6caf'
    base_path=Path('out/raphael_natural_v2_accepted_base.nds')
    assert sha(base_path.read_bytes())=='3cb827e4c52ab2086fb5a626835d72192085a958581279d3c79b0200bbf405fe'
    image,base,clean=map(NdsImage.open,(PARENT,base_path,'work/clean.nds'))
    doc,choices,mapping=map(read,(DOC,CHOICES,MAP))
    files={str(p)for p in(DOC,CHOICES,MAP,ACTUAL,Path(__file__),
        Path('dk4tool/patch/lil_speyer_editorial.py'),Path('dk4tool/dialogue/lil_speyer_profile.py'),
        Path('work/analysis/lil_Speyer_approval_v1942/final_source_reference_approval.json'),
        Path('dk4tool/dialogue/profiles.py'),Path('dk4tool/dialogue/layout.py'),
        Path('dk4tool/dialogue/encoder.py'),Path('dk4tool/dialogue/codec.py'),Path('dk4tool/dialogue/review.py'))}
    files.update(str(p)for p in mapping['evidence'])
    config=dict(format='dk4-lil-speyer-editorial-release-v1',manuscript=str(DOC),choices=str(CHOICES),reference_map=str(MAP),
        source_SC2_sha256=sha(image.read_file(owned.PATH)),target_SC2_sha256=sha(NdsImage.open(RESEARCH).read_file(owned.PATH)),
        canonical_SC2_sha256=sha(base.read_file(owned.PATH)),clean_ROM='work/clean.nds',
        clean_ROM_sha256=sha(Path('work/clean.nds').read_bytes()),clean_SC2_sha256=sha(clean.read_file(owned.PATH)),
        required_runtime_arm9_sha256=sha(image.read_file('/__arm9__.bin')),
        dependencies={p:sha(Path(p).read_bytes())for p in sorted(files)})
    rp,builder=Path('translations/release_stack.json'),Path('scripts/build_integrated_release.py')
    raw,before=rp.read_bytes(),builder.read_bytes()
    registry=read(rp)
    assert PROFILE not in registry['profiles']and len(registry['accepted_layers'])==114
    assert registry['latest_promoted_build']['profile']=='all-routes-unified-v1492'
    assert b"profile_config.get('lil_speyer_editorial')"not in before
    stage=b'''    lil_speyer_editorial = profile_config.get('lil_speyer_editorial')
    if lil_speyer_editorial:
        from dk4tool.patch.lil_speyer_editorial import apply_release as apply_lil_speyer_editorial

        speyer_report = apply_lil_speyer_editorial(candidate, baseline, lil_speyer_editorial)
        file_path = '/data/SC2.DK4'
        grouped.setdefault(file_path, [])
        changed_records.setdefault(file_path, []).extend(row['id'] for row in speyer_report['changed_records'])
        relocation_checks.setdefault(file_path, {})['lil_speyer_editorial'] = {
            'release_config': lil_speyer_editorial,
            'release_config_sha256': sha256(Path(lil_speyer_editorial).read_bytes()),
            'proof': speyer_report}
        for batch_name in ('manuscript', 'choices'):
            speyer_batch = Path(speyer_report[batch_name])
            if speyer_batch in release_batches:
                raise ValueError('Speyer must run after the complete frozen cumulative stages')
            release_batches.append(speyer_batch)

'''
    anchor=b'    # Lexically valid "% o"'
    assert before.count(anchor)==1
    at=before.index(anchor)
    after=before[:at]+stage+before[at:]
    compile(after,str(builder),'exec')
    ROOT.mkdir(parents=True)
    (ROOT/'registry_before_raw.json').write_bytes(raw)
    (ROOT/'builder_before.py').write_bytes(before)
    (ROOT/'builder_added_optional_stage.bin').write_bytes(stage)
    save(CONFIG,config)
    plan=owned.apply_release(image,base)
    assert len(plan['changed_records'])==59 and [r['block']for r in plan['blocks']]==[25,128]
    assert sum(r['growth_bytes']for r in plan['blocks'])==108
    assert image.read_file(owned.PATH)==NdsImage.open(RESEARCH).read_file(owned.PATH)
    save(ROOT/'native_source_release_plan.json',plan)
    negatives=[]
    def reject(label,im,cfgpath=CONFIG):
        previous=im.read_file(owned.PATH)
        try:owned.apply_release(im,base,cfgpath)
        except ValueError as error:
            assert im.read_file(owned.PATH)==previous
            negatives.append(dict(case=label,error=str(error),no_partial_SC2_mutation=True))
        else:raise AssertionError('Invalid Speyer release accepted:'+label)
    reject('repeat_application',image)
    for label,path in(('wrong_runtime','/__arm9__.bin'),('wrong_source',owned.PATH)):
        im=NdsImage.open(PARENT)
        data=bytearray(im.read_file(path));data[0x100]^=1
        im.replace_file(path,bytes(data))
        reject(label,im)
    tests=('incomplete_map','wrong_command_destination','wrong_relative_span','wrong_span_target','missing_map_record',
        'unreviewed_formatting','changed_prose','changed_speaker','authored_padding','wrong_consumer',
        'missing_macro','changed_choice_label','duplicate_choice_index','unreviewed_choice','missing_choice')
    for label in tests:
        bad=deepcopy(config)
        kind='reference_map'if label in tests[:5]else'choices'if label in tests[-4:]else'manuscript'
        value=deepcopy(mapping if kind=='reference_map'else choices if kind=='choices'else doc)
        if label=='incomplete_map':value['external_references_complete']=False
        elif label=='wrong_command_destination':value['blocks'][1]['mapped_native_commands'][3]['new_offset']+=2
        elif label=='wrong_relative_span':value['blocks'][1]['relative_skip_fixups'][0]['target_span']+=2
        elif label=='wrong_span_target':value['blocks'][1]['relative_skip_fixups'][0]['matched_skip_target']+=2
        elif label=='missing_map_record':value['blocks'][0]['text_records'].pop()
        elif label=='unreviewed_formatting':value['records'][0]['review']['formatting']=False
        elif label=='changed_prose':value['records'][0]['english']+=' Extra words.'
        elif label=='changed_speaker':value['records'][0]['english']=value['records'][0]['english'].replace('SPEAKER:1D','SPEAKER:98')
        elif label=='authored_padding':value['records'][0]['english']+='{PAD}'
        elif label=='wrong_consumer':value['records'][0]['native_display_consumer']='original_FE_modal_5473C_mode1'
        elif label=='missing_macro':
            row=next(r for r in value['records']if'{MACRO:FI}'in r['english'])
            row['english']=row['english'].replace('{MACRO:FI}','Lil',1)
        elif label=='changed_choice_label':value['records'][0]['english']+=' Extra words.'
        elif label=='duplicate_choice_index':value['records'][0]['option_index']=1
        elif label=='unreviewed_choice':value['records'][0]['review']['formatting']=False
        else:value['records'].pop()
        path=ROOT/(label+'.json')
        save(path,value)
        bad[kind]=str(path)
        bad['dependencies'][str(path)]=sha(path.read_bytes())
        cfgpath=ROOT/(label+'_config.json')
        save(cfgpath,bad)
        reject(label,NdsImage.open(PARENT),cfgpath)
    assert len(negatives)==18
    profile=deepcopy(registry['profiles']['all-routes-unified-v1909'])
    profile.update(lil_speyer_editorial=CONFIG,status='experimental',
        description='Complete V1909 stack plus57 contextually reviewed Speyer speeches and two choice labels.',
        note='Only SC2 B25/B128 grow108bytes total;137commands48typed spans;51actual speeches102holds,two complete visible labels,sixspeech offline. Original Hamburg79 captures remain separate/unreviewed. Identity/patch/startup pending;V1492 stays promoted.')
    registry['profiles'][PROFILE]=profile
    assert rp.read_bytes()==raw and builder.read_bytes()==before
    pending=rp.with_name('release_stack_v1944_pending.json')
    assert not pending.exists()
    save(pending,registry)
    builder.write_bytes(after)
    os.replace(pending,rp)
    restored=deepcopy(read(rp));restored['profiles'].pop(PROFILE)
    assert restored==read(ROOT/'registry_before_raw.json')
    assert builder.read_bytes().replace(stage,b'',1)==before
    save(ROOT/'registration_provenance.json',dict(profile=PROFILE,source_profile='all-routes-unified-v1909',
        source_parent=str(PARENT),source_parent_sha256=sha(PARENT.read_bytes()),
        all_previous_profiles_accepted_layers_and_promotion_preserved=True,
        registry_before_sha256=sha(raw),registry_after_sha256=sha(rp.read_bytes()),
        builder_before_sha256=sha(before),builder_after_sha256=sha(after),
        release_config_sha256=sha(Path(CONFIG).read_bytes()),negative_cases=negatives,
        source_compiler_exact_to_research_SC2=True,new_registered_candidate_not_yet_built=True,
        producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    print(dict(profile=PROFILE,negative_release_cases=len(negatives),source_compiler_equals_research=True))
