"""Register one cumulative73-entry layer after V2013, with guarded compilation."""
from copy import deepcopy
import os
from pathlib import Path
from dk4tool.patch import hodram_opening_editorial as owned
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/hodram_opening_release_v2029')
DOC=Path('translations/hodram_opening_contextual_editorial_manuscript_v2.json')
MAP=Path('translations/hodram_opening_editorial_relocation_map_v1.json')
CONFIG='translations/hodram_opening_editorial_release_v1.json'
PROFILE='all-routes-unified-v2030'
PARENT=Path('out/all_routes_combined_v2013_candidate.nds')
RESEARCH=Path('work/analysis/hodram_opening_relocation_v2023/hodram_opening_V2013_derived_RESEARCH_ONLY.nds')

if __name__=='__main__':
    assert not ROOT.exists()and not Path(CONFIG).exists()
    assert sha(PARENT.read_bytes())=='29d9de4bdd46231b865cbe39a0592dd65a0c55378dfdbb7d8c10aa6104ca7d55'
    assert sha(RESEARCH.read_bytes())=='4ed991686628ef679ee1d0fc6a00ad98bccafc99c0b83cba9371fa335eb53532'
    base=Path('out/raphael_natural_v2_accepted_base.nds')
    assert sha(base.read_bytes())=='3cb827e4c52ab2086fb5a626835d72192085a958581279d3c79b0200bbf405fe'
    image,baseline,clean=map(NdsImage.open,(PARENT,base,'work/clean.nds'));doc,mapping=map(read,(DOC,MAP))
    files={str(p)for p in(DOC,MAP,Path(__file__),Path('scripts/approve_hodram_opening_v2028.py'),
        Path('work/analysis/hodram_opening_approval_v2028/approval_receipt.json'),
        Path('dk4tool/dialogue/hodram_opening_profile.py'),Path('dk4tool/patch/hodram_opening_editorial.py'))}
    files.update(mapping['evidence'])
    config=dict(format='dk4-hodram-opening-editorial-release-v1',manuscript=str(DOC),reference_map=str(MAP),
        source_SC1_sha256=sha(image.read_file(owned.PATH)),target_SC1_sha256=sha(NdsImage.open(RESEARCH).read_file(owned.PATH)),
        canonical_SC1_sha256=sha(baseline.read_file(owned.PATH)),clean_ROM='work/clean.nds',clean_ROM_sha256=sha(Path('work/clean.nds').read_bytes()),
        clean_SC1_sha256=sha(clean.read_file(owned.PATH)),required_runtime_ARM9_sha256=sha(image.read_file('/__arm9__.bin')),
        tested_research_ROM_sha256=sha(RESEARCH.read_bytes()),dependencies={p:sha(Path(p).read_bytes())for p in sorted(files)})
    registry_path,builder=Path('translations/release_stack.json'),Path('scripts/build_integrated_release.py')
    raw,before=registry_path.read_bytes(),builder.read_bytes();registry=read(registry_path)
    assert PROFILE not in registry['profiles']and len(registry['accepted_layers'])==114
    assert registry['latest_promoted_build']['profile']=='all-routes-unified-v1492'
    assert b"profile_config.get('hodram_opening_editorial')"not in before
    stage=b'''    hodram_opening_editorial = profile_config.get('hodram_opening_editorial')
    if hodram_opening_editorial:
        from dk4tool.patch.hodram_opening_editorial import apply_release as apply_hodram_opening_editorial

        hodram_report = apply_hodram_opening_editorial(candidate, baseline, hodram_opening_editorial)
        file_path = '/data/SC1.DK4'
        grouped.setdefault(file_path, [])
        changed_records.setdefault(file_path, []).extend(row['id'] for row in hodram_report['changed_records'])
        relocation_checks.setdefault(file_path, {})['hodram_opening_editorial'] = {
            'release_config': hodram_opening_editorial,
            'release_config_sha256': sha256(Path(hodram_opening_editorial).read_bytes()),
            'proof': hodram_report}
        hodram_batch = Path(hodram_report['manuscript'])
        if hodram_batch in release_batches:
            raise ValueError('Hodram opening must run after the complete frozen cumulative stages')
        release_batches.append(hodram_batch)

'''
    anchor=b'    # Lexically valid "% o"';assert before.count(anchor)==1
    at=before.index(anchor);after=before[:at]+stage+before[at:];compile(after,str(builder),'exec')
    ROOT.mkdir(parents=True);(ROOT/'registry_before_raw.json').write_bytes(raw);(ROOT/'builder_before.py').write_bytes(before)
    (ROOT/'builder_added_optional_stage.bin').write_bytes(stage);save(CONFIG,config)
    report=owned.apply_release(image,baseline)
    assert image.read_file(owned.PATH)==NdsImage.open(RESEARCH).read_file(owned.PATH)
    assert(report['typed_commands'],report['relative_sites'],report['compiled_progressive_records'],report['separate_FE_records'])==(171,24,67,6)
    save(ROOT/'native_source_release_plan.json',report);negatives=[]
    def reject(label,target,cfgpath=CONFIG,baseimage=baseline):
        previous=target.read_file(owned.PATH)
        try:owned.apply_release(target,baseimage,cfgpath)
        except ValueError as exc:
            assert target.read_file(owned.PATH)==previous;negatives.append(dict(case=label,error=str(exc),no_partial_SC1_mutation=True))
        else:raise AssertionError('Invalid Hodram release accepted: '+label)
    reject('repeat-application',image)
    for label,path in(('wrong-runtime','/__arm9__.bin'),('wrong-source',owned.PATH)):
        badimage=NdsImage.open(PARENT);data=bytearray(badimage.read_file(path));data[0x100]^=1;badimage.replace_file(path,bytes(data));reject(label,badimage)
    wrongbase=NdsImage.open(base);data=bytearray(wrongbase.read_file(owned.PATH));data[0x100]^=1;wrongbase.replace_file(owned.PATH,bytes(data))
    reject('wrong-canonical',NdsImage.open(PARENT),baseimage=wrongbase)
    tests=('incomplete-map','missing-block','missing-command','wrong-command-target','wrong-relative-span','wrong-relative-target','missing-relative-site',
        'wrong-ancestor','wrong-opaque-command','false-parity','false-FE-consumer','unreviewed-formatting','changed-prose','changed-speaker','authored-padding',
        'wrong-source-index','wrong-current-index','wrong-target-index','wrong-Japanese-hex','wrong-Japanese-prose','invented-macro','changed-FE','false-actual')
    for label in tests:
        kind='reference_map'if label in tests[:11]else'manuscript';value=deepcopy(mapping if kind=='reference_map'else doc);bad=deepcopy(config)
        if label=='incomplete-map':value['external_references_complete']=False
        elif label=='missing-block':value['blocks'].pop()
        elif label=='missing-command':value['blocks'][1]['mapped_native_commands'].pop()
        elif label=='wrong-command-target':value['blocks'][0]['mapped_native_commands'][0]['new_offset']+=2
        elif label=='wrong-relative-span':value['blocks'][1]['relative_skip_fixups'][0]['target_span']+=2
        elif label=='wrong-relative-target':value['blocks'][1]['relative_skip_fixups'][0]['new_matched_target']+=2
        elif label=='missing-relative-site':value['blocks'][1]['relative_skip_fixups'].pop()
        elif label=='wrong-ancestor':value['blocks'][0]['mapped_native_commands'][0]['target_0100_ancestors']=[8]
        elif label=='wrong-opaque-command':value['blocks'][0]['mapped_native_commands'][0]['word']^=1
        elif label=='false-parity':value['blocks'][0]['text_records'][0]['final_parity_native_plane_exact']=False
        elif label=='false-FE-consumer':value['blocks'][0]['text_records'][1]['separate_FE_modal']=False
        elif label=='unreviewed-formatting':value['records'][0]['review']['formatting']=False
        elif label=='changed-prose':value['records'][0]['english']+=' Extra words.'
        elif label=='changed-speaker':value['records'][0]['english']=value['records'][0]['english'].replace('SPEAKER:01','SPEAKER:02')
        elif label=='authored-padding':value['records'][0]['english']+='{PAD}'
        elif label=='wrong-source-index':value['records'][0]['source_record_index']+=1
        elif label=='wrong-current-index':value['records'][0]['record_index']+=1
        elif label=='wrong-target-index':value['records'][0]['target_record_index']+=1
        elif label=='wrong-Japanese-hex':value['records'][0]['source_hex']=value['records'][0]['source_hex'][:-2]+'20'
        elif label=='wrong-Japanese-prose':value['records'][0]['source_Japanese']+='違う'
        elif label=='invented-macro':value['records'][0]['english']+='{MACRO:FI}'
        elif label=='changed-FE':next(r for r in value['records']if r['source_presentation_prefix_hex']=='fe')['english']='{SPEAKER:FE}Invented order!'
        else:
            actual=deepcopy(read(value['actual_representative_proof']));actual['all37_opening_speeches93_commands_and_town_return']=False
            path=ROOT/'false_actual.json';save(path,actual);value['actual_representative_proof']=str(path);bad['dependencies'][str(path)]=sha(path.read_bytes())
        path=ROOT/(label+'.json');save(path,value);bad[kind]=str(path);bad['dependencies'][str(path)]=sha(path.read_bytes())
        cfgpath=ROOT/(label+'_config.json');save(cfgpath,bad);reject(label,NdsImage.open(PARENT),cfgpath)
    assert len(negatives)==27
    profile=deepcopy(registry['profiles']['all-routes-unified-v2013'])
    profile.update(hodram_opening_editorial=CONFIG,status='experimental',
        description='Complete V2013 stack plus73 fresh full-exchange Hodram opening/trade/Lil entries:38 revisions35 retentions.',
        note='All73 complete native glyph planes;171commands24relative sites360native cases;325loads650parent modes perROM;37actual revised opening panels andordinary Stockholm return. B43/B44 offline only,no individual visits claimed.488batches114acceptedlayers expected;exact cleanpatch/startup pending. V1492 promoted.')
    registry['profiles'][PROFILE]=profile
    assert registry_path.read_bytes()==raw and builder.read_bytes()==before
    pending=registry_path.with_name('release_stack_v2029_pending.json');assert not pending.exists();save(pending,registry)
    builder.write_bytes(after);os.replace(pending,registry_path)
    restored=deepcopy(read(registry_path));restored['profiles'].pop(PROFILE)
    assert restored==read(ROOT/'registry_before_raw.json')and builder.read_bytes().replace(stage,b'',1)==before
    save(ROOT/'registration_provenance.json',dict(profile=PROFILE,source_profile='all-routes-unified-v2013',source_parent=str(PARENT),source_parent_sha256=sha(PARENT.read_bytes()),
        all_previous_profiles_accepted_layers_and_promotion_preserved=True,registry_before_sha256=sha(raw),registry_after_sha256=sha(registry_path.read_bytes()),
        builder_before_sha256=sha(before),builder_after_sha256=sha(after),release_config_sha256=sha(Path(CONFIG).read_bytes()),
        negative_cases=negatives,source_compiler_exact_to_research_SC1=True,new_registered_candidate_not_yet_built=True,
        producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    print(dict(profile=PROFILE,negative_cases=27,compiler_exact_research=True,accepted_layers=114,changed_speech_commands=len(report['changed_records'])))
