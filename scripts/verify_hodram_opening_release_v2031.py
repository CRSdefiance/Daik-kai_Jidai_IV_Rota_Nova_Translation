"""Whole cumulative identity, unchanged inheritance and exact clean-input patch."""
from copy import deepcopy
from pathlib import Path
from ndspy.code import MainCodeFile
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.xdelta import make_xdelta,apply_xdelta
from dk4tool.rom.nds import NdsImage
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/hodram_opening_release_v2029b')
PROFILE='all-routes-unified-v2030'
CONFIG='translations/hodram_opening_editorial_release_v2.json'
PARENT=Path('out/all_routes_combined_v2013_candidate.nds')
ROM=Path('out/all_routes_combined_v2030_candidate.nds')
RESEARCH=Path('work/analysis/hodram_opening_relocation_v2023/hodram_opening_V2013_derived_RESEARCH_ONLY.nds')

if __name__=='__main__':
    output=ROOT/'registered_release_verification.json';assert not output.exists()
    manifest,prior=[read(p.with_suffix('.manifest.json'))for p in(ROM,PARENT)]
    digest=sha(ROM.read_bytes());assert manifest['profile']==PROFILE
    assert manifest['candidate_sha256']==digest==sha(RESEARCH.read_bytes())and ROM.read_bytes()==RESEARCH.read_bytes()
    assert sha(PARENT.read_bytes())=='29d9de4bdd46231b865cbe39a0592dd65a0c55378dfdbb7d8c10aa6104ca7d55'
    assert manifest['base_sha256']=='3cb827e4c52ab2086fb5a626835d72192085a958581279d3c79b0200bbf405fe'
    registry=read('translations/release_stack.json');assert manifest['release_stack_sha256']==sha(Path('translations/release_stack.json').read_bytes())
    restored=deepcopy(registry);profile=restored['profiles'].pop(PROFILE);assert restored==read(ROOT/'registry_before_raw.json')
    old_profile=deepcopy(registry['profiles']['all-routes-unified-v2013'])
    for key in('description','note'):profile.pop(key,None);old_profile.pop(key,None)
    assert profile.pop('hodram_opening_editorial')==CONFIG and profile==old_profile
    config=read(CONFIG);normal=lambda s:str(s).replace('\\','/')
    assert [normal(p)for p in manifest['batches']]==[normal(p)for p in prior['batches']]+[normal(config['manuscript'])]
    assert len(manifest['batches'])==488 and len(registry['accepted_layers'])==114
    assert all(manifest['checks'].values())and registry['latest_promoted_build']['profile']=='all-routes-unified-v1492'
    old,new=map(NdsImage.open,(PARENT,ROM))
    assert [p for _,p,value in old.iter_files()if new.read_file(p)!=value]==['/data/SC1.DK4']
    assert all(new.read_file(p)==value for p,value in old.iter_components())
    a,b=[IlnkContainer.parse(im.read_file('/data/SC1.DK4')).blocks for im in(old,new)]
    assert len(a)==len(b)==325 and[n for n,(x,y)in enumerate(zip(a,b,strict=True))if x!=y]==[42,43,44]
    stage=read(ROOT/'native_source_release_plan.json');assert len(stage['changed_records'])==65
    assert(stage['compiled_progressive_records'],stage['separate_FE_records'],stage['typed_commands'],stage['relative_sites'])==(67,6,171,24)
    final=manifest['relocations']['/data/SC1.DK4']['hodram_opening_editorial']
    assert final['proof']==stage and final['release_config_sha256']==sha(Path(CONFIG).read_bytes())
    arm=new.read_file('/__arm9__.bin');assert sha(arm)=='500b7d6cea559d7252ae4e67f94540e67739428823a17cf26842b6827712a41e'
    assert len(MainCodeFile(arm,0x02000000).sections[3].data)-48==123040
    hashes={p:sha(new.read_file(p))for p in('/data/SC0.DK4','/data/SC1.DK4','/data/SC2.DK4','/data/SC3.DK4','/COMMON/MESFILE.DK4')}
    assert hashes['/data/SC0.DK4']=='e7bfe2b21c7f9ebad0ac1087f48a9e5a86dd5b909cc47ba8128b9b98f385b42d'
    assert hashes['/COMMON/MESFILE.DK4']=='dc26a3260c611fe4686f64deb3d81c4aa50724aa304a7ba399c9ca859b7605ad'
    assert hashes['/data/SC2.DK4']=='c92e8c319b291cd34e1cf940ba1c7452bc36ccd86bd7d9871732f655bef16386'
    builder=Path('scripts/build_integrated_release.py').read_bytes();addition=(ROOT/'builder_added_optional_stage.bin').read_bytes()
    assert builder.count(addition)==1 and builder.replace(addition,b'',1)==(ROOT/'builder_before.py').read_bytes()
    clean=Path('work/clean.nds');clean_sha=sha(clean.read_bytes());assert clean_sha=='f4f07c975cc293f5b2ba469747693d3dd37f2e6dfc408cf5910adf5e83d9177d'
    patch=ROM.with_suffix('.xdelta');reconstruction=ROOT/'patch_reconstruction_RESEARCH_ONLY.nds'
    assert not patch.exists()and not reconstruction.exists();make_xdelta(clean,ROM,patch);apply_xdelta(clean,patch,reconstruction)
    assert reconstruction.read_bytes()==ROM.read_bytes()and sha(clean.read_bytes())==clean_sha
    save(output,dict(candidate=str(ROM),candidate_sha256=digest,profile=PROFILE,canonical_base=manifest['base_rom'],canonical_sha256=manifest['base_sha256'],
        manifest_sha256=sha(ROM.with_suffix('.manifest.json').read_bytes()),release_stack_sha256=manifest['release_stack_sha256'],
        all488_batches114_accepted_layers_and_prior_profiles_preserved=True,only_SC1_B42_B43_B44_change_from_V2013=True,
        all322_other_blocks_every_other_file_and_native_component_exact=True,ARM9_sha256=sha(arm),COMMON_sha256=hashes['/COMMON/MESFILE.DK4'],
        SC0_sha256=hashes['/data/SC0.DK4'],SC1_sha256=hashes['/data/SC1.DK4'],SC2_sha256=hashes['/data/SC2.DK4'],all_route_hashes=hashes,stage=stage,
        registered_ROM_whole_file_exact_to_actual_tested_research=True,actual_scene_research_ROM=str(RESEARCH),
        patch=str(patch),patch_sha256=sha(patch.read_bytes()),clean_input_sha256=clean_sha,reconstruction=str(reconstruction),complete_reconstruction_byte_exact=True,
        startup_controls_and_editorial_completion_pending=True,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    print(dict(candidate_SHA256=digest,patch_SHA256=sha(patch.read_bytes()),batches=488,changed_SC1_blocks=[42,43,44]))
