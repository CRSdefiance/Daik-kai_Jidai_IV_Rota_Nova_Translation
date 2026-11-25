"""Register the proven49-line opening after the complete immutable V1676 stack."""
from copy import deepcopy
import json
import os
from pathlib import Path
from dk4tool.patch import lil_opening_editorial as owned
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/lil_opening_release_v1710')
PROFILE='all-routes-unified-v1711'


if __name__=='__main__':
    assert not ROOT.exists() and not Path(owned.CONFIG).exists()
    parent=Path('out/all_routes_combined_v1676_candidate.nds');baseline=Path('out/raphael_natural_v2_accepted_base.nds')
    assert sha(parent.read_bytes())=='337edf22ab6ee96536aadb15fb461652149b157e8d9bd1ef60db998f97608510'
    assert sha(baseline.read_bytes())=='3cb827e4c52ab2086fb5a626835d72192085a958581279d3c79b0200bbf405fe'
    image=NdsImage.open(parent);base=NdsImage.open(baseline);clean=NdsImage.open('work/clean.nds')
    manuscript=Path('translations/lil_opening_editorial_manuscript_v2.json');doc=read(manuscript)
    research=read('work/analysis/lil_opening_research_v1704/research_image_receipt.json')
    map_path=Path('translations/lil_opening_editorial_relocation_map_v1.json');mapping=read(map_path)
    assert mapping['external_references_complete']
    files={str(manuscript),str(map_path),'dk4tool/patch/lil_opening_editorial.py','dk4tool/dialogue/profiles.py','dk4tool/dialogue/layout.py',
        'dk4tool/dialogue/encoder.py','dk4tool/dialogue/codec.py','tests/test_lil_editorial_literal_guard.py',__file__,
        'translations/search_reports_editorial_release_v1.json',doc['source_context'],doc['native_macro_proof'],doc['native_font_proof'],doc['visual_review']}
    files.update(mapping['evidence']);files.update(r['path'] for r in read(doc['native_font_proof'])['review_sheets'])
    files.update(r['preview'] for r in read(doc['native_font_proof'])['cases'])
    files.add('work/analysis/lil_opening_references_v1709/actual_visual_review.json')
    config={'format':'dk4-lil-opening-editorial-release-v1','manuscript':str(manuscript),'reference_map':str(map_path),
        'source_SC2_sha256':sha(image.read_file(owned.PATH)),'target_SC2_sha256':research['SC2_sha256'],
        'canonical_SC2_sha256':sha(base.read_file(owned.PATH)),'clean_ROM':'work/clean.nds',
        'clean_ROM_sha256':sha(Path('work/clean.nds').read_bytes()),'clean_SC2_sha256':sha(clean.read_file(owned.PATH)),
        'required_runtime_arm9_sha256':sha(image.read_file('/__arm9__.bin')),
        'dependencies':{name:sha(Path(name).read_bytes()) for name in sorted(files)}}
    rp,builder=Path('translations/release_stack.json'),Path('scripts/build_integrated_release.py')
    registry_raw,before=rp.read_bytes(),builder.read_bytes();registry=read(rp)
    assert PROFILE not in registry['profiles'] and len(registry['accepted_layers'])==114
    assert registry['latest_promoted_build']['profile']=='all-routes-unified-v1492'
    assert b"profile_config.get('lil_opening_editorial')" not in before
    stage=b'''    lil_opening_editorial = profile_config.get('lil_opening_editorial')
    if lil_opening_editorial:
        from dk4tool.patch.lil_opening_editorial import apply_release as apply_lil_opening_editorial

        opening_report = apply_lil_opening_editorial(candidate, baseline, lil_opening_editorial)
        file_path = '/data/SC2.DK4'
        grouped.setdefault(file_path, [])
        changed_records.setdefault(file_path, []).extend(row['id'] for row in opening_report['changed_records'])
        relocation_checks.setdefault(file_path, {})['lil_opening_editorial'] = {
            'release_config': lil_opening_editorial,
            'release_config_sha256': sha256(Path(lil_opening_editorial).read_bytes()),
            'proof': opening_report}
        opening_batch = Path(opening_report['manuscript'])
        if opening_batch in release_batches:
            raise ValueError('Lil opening must run only after the frozen cumulative stages')
        release_batches.append(opening_batch)

'''
    anchor=b'    # Lexically valid "% o"';assert before.count(anchor)==1
    at=before.index(anchor);after=before[:at]+stage+before[at:];compile(after,str(builder),'exec')
    ROOT.mkdir(parents=True)
    (ROOT/'registry_before_raw.json').write_bytes(registry_raw);(ROOT/'builder_before.py').write_bytes(before)
    (ROOT/'builder_added_optional_stage.bin').write_bytes(stage)
    save(owned.CONFIG,config)
    plan=owned.apply_release(image,base,owned.CONFIG)
    assert sha(image.read_file(owned.PATH))==research['SC2_sha256'] and plan['block_growth_bytes']==292
    negatives=[]
    try:owned.apply_release(image,base,owned.CONFIG)
    except ValueError as error:
        assert 'current/canonical source' in str(error);negatives.append('repeat_application_rejected')
    else:raise AssertionError('Repeat application accepted')
    wrong=NdsImage.open(parent);arm=bytearray(wrong.read_file('/__arm9__.bin'));arm[0x100]^=1;wrong.replace_file('/__arm9__.bin',bytes(arm))
    try:owned.apply_release(wrong,base,owned.CONFIG)
    except ValueError as error:
        assert 'proven native literal/cursor runtime' in str(error);negatives.append('wrong_runtime_rejected')
    else:raise AssertionError('Unproven runtime accepted')
    bad_map=deepcopy(mapping);bad_map['external_references_complete']=False
    bad_map_path=ROOT/'incomplete_map_negative.json';save(bad_map_path,bad_map)
    bad=deepcopy(config);bad['reference_map']=str(bad_map_path);bad['dependencies'][str(bad_map_path)]=sha(bad_map_path.read_bytes())
    bad_config=ROOT/'incomplete_reference_negative_config.json';save(bad_config,bad)
    try:owned.apply_release(NdsImage.open(parent),base,bad_config)
    except ValueError as error:
        assert 'complete source reference map' in str(error);negatives.append('incomplete_reference_map_rejected')
    else:raise AssertionError('Incomplete reference map accepted')
    save(ROOT/'native_source_release_plan.json',plan)
    profile=deepcopy(registry['profiles']['all-routes-unified-v1676'])
    profile.update(lil_opening_editorial=owned.CONFIG,status='experimental',
        description='Complete V1676 stack plus49 fully reviewed Lil Amsterdam opening lines.',
        note='SC2 B22 only,+292 bytes;all49 source speakers/macros,all41 other commands and original entry/VM paths proven.98 actual text holds and all90 command returns pass on byte-locked research image. Registered patch/startup/research-equivalence and next-scene terminal audit pending. V1492 remains promoted.')
    registry['profiles'][PROFILE]=profile
    assert rp.read_bytes()==registry_raw and builder.read_bytes()==before
    temporary=rp.with_name('release_stack_v1710_pending.json');assert not temporary.exists()
    save(temporary,registry);assert read(temporary)==registry and rp.read_bytes()==registry_raw
    builder.write_bytes(after);os.replace(temporary,rp)
    restored=deepcopy(read(rp));restored['profiles'].pop(PROFILE)
    assert restored==read(ROOT/'registry_before_raw.json') and builder.read_bytes().replace(stage,b'',1)==before
    save(ROOT/'registration_provenance.json',{'profile':PROFILE,'source_profile':'all-routes-unified-v1676',
        'source_and_runtime_bound_post_layer':True,'full_prior_accepted_layers_profiles_batches_and_promotion_preserved':True,
        'builder_before_sha256':sha(before),'builder_after_sha256':sha(after),'registry_before_sha256':sha(registry_raw),
        'registry_after_sha256':sha(rp.read_bytes()),'negative_cases_rejected':negatives,
        'producer_sha256':sha(Path(__file__).read_bytes()),'full_goal_complete':False})
    print('Experimental V1711 registered after all V1676 stages;only SC2 B22 changes. Three source/runtime/reference negatives rejected. Build/patch/startup/next-scene audit pending.')
