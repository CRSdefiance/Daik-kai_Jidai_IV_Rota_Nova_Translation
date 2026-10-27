"""Register reviewed B24 after the entire immutable V1807 cumulative stack."""
from copy import deepcopy
import os
from pathlib import Path
from dk4tool.patch import lil_trade_routes_editorial as owned
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.prepare_lil_B24_research_v1829 import ROM as RESEARCH
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/lil_B24_release_v1840')
PROFILE='all-routes-unified-v1841'
PARENT=Path('out/all_routes_combined_v1807_candidate.nds')

if __name__=='__main__':
    assert not ROOT.exists()and not Path(owned.CONFIG).exists()
    assert sha(PARENT.read_bytes())=='4851f3c54fba3d4b745a8990002687b943b842e836044ab54285a13ec7648fdc'
    base_path=Path('out/raphael_natural_v2_accepted_base.nds')
    assert sha(base_path.read_bytes())=='3cb827e4c52ab2086fb5a626835d72192085a958581279d3c79b0200bbf405fe'
    image=NdsImage.open(PARENT);base=NdsImage.open(base_path);clean=NdsImage.open('work/clean.nds')
    docpath=Path('translations/lil_trade_routes_officers_editorial_manuscript_v4.json');doc=read(docpath)
    map_path=Path('translations/lil_trade_routes_editorial_relocation_map_v1.json');mapping=read(map_path)
    assert mapping['external_references_complete']
    files={str(docpath),str(map_path),'dk4tool/patch/lil_trade_routes_editorial.py',__file__,
        'dk4tool/dialogue/profiles.py','dk4tool/dialogue/layout.py','dk4tool/dialogue/encoder.py',
        'dk4tool/dialogue/codec.py','dk4tool/dialogue/review.py','translations/reinforcement_faction_prose_release_v1.json',
        doc['source_context'],doc['native_font_proof'],doc['visual_review'],doc['actual_visual_review']}
    files.update(mapping['evidence']);fonts=read(doc['native_font_proof'])
    files.update(r['preview']for r in fonts['cases'])
    files.update(r['path']for r in fonts['review_sheets'])
    for path in list(mapping['evidence']):
        p=read(path)
        files.update(p.get('evidence',{}))
    config={'format':'dk4-lil-trade-routes-editorial-release-v1','manuscript':str(docpath),'reference_map':str(map_path),
        'source_SC2_sha256':sha(image.read_file(owned.PATH)),
        'target_SC2_sha256':sha(NdsImage.open(RESEARCH).read_file(owned.PATH)),
        'canonical_SC2_sha256':sha(base.read_file(owned.PATH)),'clean_ROM':'work/clean.nds',
        'clean_ROM_sha256':sha(Path('work/clean.nds').read_bytes()),'clean_SC2_sha256':sha(clean.read_file(owned.PATH)),
        'required_runtime_arm9_sha256':sha(image.read_file('/__arm9__.bin')),
        'dependencies':{name:sha(Path(name).read_bytes())for name in sorted(files)}}
    rp=Path('translations/release_stack.json');builder=Path('scripts/build_integrated_release.py')
    raw=rp.read_bytes();registry=read(rp);before=builder.read_bytes()
    assert PROFILE not in registry['profiles']and len(registry['accepted_layers'])==114
    assert registry['latest_promoted_build']['profile']=='all-routes-unified-v1492'
    assert b"profile_config.get('lil_trade_routes_editorial')"not in before
    stage=b'''    lil_trade_routes_editorial = profile_config.get('lil_trade_routes_editorial')
    if lil_trade_routes_editorial:
        from dk4tool.patch.lil_trade_routes_editorial import apply_release as apply_lil_trade_routes_editorial

        trade_report = apply_lil_trade_routes_editorial(candidate, baseline, lil_trade_routes_editorial)
        file_path = '/data/SC2.DK4'
        grouped.setdefault(file_path, [])
        changed_records.setdefault(file_path, []).extend(row['id'] for row in trade_report['changed_records'])
        relocation_checks.setdefault(file_path, {})['lil_trade_routes_editorial'] = {
            'release_config': lil_trade_routes_editorial,
            'release_config_sha256': sha256(Path(lil_trade_routes_editorial).read_bytes()),
            'proof': trade_report}
        trade_batch = Path(trade_report['manuscript'])
        if trade_batch in release_batches:
            raise ValueError('Lil trade routes must run only after the frozen cumulative stages')
        release_batches.append(trade_batch)

'''
    anchor=b'    # Lexically valid "% o"';assert before.count(anchor)==1
    at=before.index(anchor);after=before[:at]+stage+before[at:];compile(after,str(builder),'exec')
    ROOT.mkdir(parents=True);(ROOT/'registry_before_raw.json').write_bytes(raw)
    (ROOT/'builder_before.py').write_bytes(before);(ROOT/'builder_added_optional_stage.bin').write_bytes(stage)
    save(owned.CONFIG,config)
    plan=owned.apply_release(image,base);assert plan['block_growth_bytes']==136
    assert image.read_file(owned.PATH)==NdsImage.open(RESEARCH).read_file(owned.PATH)
    save(ROOT/'native_source_release_plan.json',plan)
    negatives=[]
    def reject(label,im,cfgpath=owned.CONFIG):
        previous=im.read_file(owned.PATH)
        try:owned.apply_release(im,base,cfgpath)
        except ValueError as error:
            assert im.read_file(owned.PATH)==previous
            negatives.append({'case':label,'error':str(error),'no_partial_SC2_mutation':True})
        else:raise AssertionError('Invalid B24 release accepted:'+label)
    reject('repeat_application',image)
    wrong=NdsImage.open(PARENT);arm=bytearray(wrong.read_file('/__arm9__.bin'));arm[0x100]^=1
    wrong.replace_file('/__arm9__.bin',bytes(arm));reject('wrong_runtime',wrong)
    wrong=NdsImage.open(PARENT);sc=bytearray(wrong.read_file(owned.PATH));sc[-1]^=1
    wrong.replace_file(owned.PATH,bytes(sc));reject('wrong_source',wrong)
    for label,kind in [('incomplete_map','map'),('wrong_command_destination','map'),
                       ('unreviewed_formatting','doc'),('changed_prose','doc')]:
        bad=deepcopy(config)
        value=deepcopy(mapping if kind=='map'else doc)
        if label=='incomplete_map':value['external_references_complete']=False
        elif label=='wrong_command_destination':value['commands'][3]['new_offset']+=2
        elif label=='unreviewed_formatting':value['records'][0]['review']['formatting']=False
        else:value['records'][0]['english']+=' Extra words.'
        path=ROOT/(label+'.json');save(path,value)
        bad['reference_map'if kind=='map'else'manuscript']=str(path)
        bad['dependencies'][str(path)]=sha(path.read_bytes())
        cfgpath=ROOT/(label+'_config.json');save(cfgpath,bad)
        reject(label,NdsImage.open(PARENT),cfgpath)
    assert len(negatives)==7
    profile=deepcopy(registry['profiles']['all-routes-unified-v1807'])
    profile.update(lil_trade_routes_editorial=owned.CONFIG,status='experimental',
        description='Complete V1807 stack plus13 fully reviewed Lil trade-route/officer scene lines.',
        note='Only SC2B24 +136bytes;all17 original commands,13 individual actual speech visits26 holds andnormal return proven. Registered exact-patch/startup/research identity verification pending. V1492 remains promoted.')
    registry['profiles'][PROFILE]=profile
    assert rp.read_bytes()==raw and builder.read_bytes()==before
    pending=rp.with_name('release_stack_v1840_pending.json');assert not pending.exists()
    save(pending,registry);builder.write_bytes(after);os.replace(pending,rp)
    restored=deepcopy(read(rp));restored['profiles'].pop(PROFILE)
    assert restored==read(ROOT/'registry_before_raw.json')
    assert builder.read_bytes().replace(stage,b'',1)==before
    save(ROOT/'registration_provenance.json',{'profile':PROFILE,'source_profile':'all-routes-unified-v1807',
        'source_parent':str(PARENT),'source_parent_sha256':sha(PARENT.read_bytes()),
        'all_previous_profiles_accepted_layers_and_promotion_preserved':True,
        'builder_before_sha256':sha(before),'builder_after_sha256':sha(after),
        'registry_before_sha256':sha(raw),'registry_after_sha256':sha(rp.read_bytes()),
        'release_config_sha256':sha(Path(owned.CONFIG).read_bytes()),'negative_cases':negatives,
        'new_registered_candidate_not_yet_built':True,'full_goal_complete':False,
        'producer_sha256':sha(Path(__file__).read_bytes())})
    print({'profile':PROFILE,'negative_release_cases':7,'native_source_plan_equals_research':True},flush=True)
