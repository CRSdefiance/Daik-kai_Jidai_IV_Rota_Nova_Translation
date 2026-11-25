"""Audit complete-stack registration and exactly reconstructable clean patch."""
from copy import deepcopy
from pathlib import Path
from ndspy.code import MainCodeFile
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch import lil_trade_routes_editorial as owned
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.xdelta import make_xdelta,apply_xdelta
from dk4tool.rom.nds import NdsImage
from scripts.prepare_lil_B24_research_v1829 import ROM as RESEARCH
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/lil_B24_release_v1840')
ROM=Path('out/all_routes_combined_v1841_candidate.nds')
OLD=Path('out/all_routes_combined_v1807_candidate.nds')

if __name__=='__main__':
    output=ROOT/'registered_release_verification.json';assert not output.exists()
    manifest,prior=(read(p.with_suffix('.manifest.json'))for p in(ROM,OLD));digest=sha(ROM.read_bytes())
    assert manifest['profile']=='all-routes-unified-v1841'
    assert manifest['candidate_sha256']==digest==sha(RESEARCH.read_bytes())and ROM.read_bytes()==RESEARCH.read_bytes()
    assert sha(OLD.read_bytes())=='4851f3c54fba3d4b745a8990002687b943b842e836044ab54285a13ec7648fdc'
    assert manifest['base_sha256']=='3cb827e4c52ab2086fb5a626835d72192085a958581279d3c79b0200bbf405fe'
    registry=read('translations/release_stack.json')
    assert manifest['release_stack_sha256']==sha(Path('translations/release_stack.json').read_bytes())
    restored=deepcopy(registry);new_profile=restored['profiles'].pop(manifest['profile'])
    assert restored==read(ROOT/'registry_before_raw.json')
    old_profile=deepcopy(registry['profiles']['all-routes-unified-v1807'])
    for key in('description','note'):new_profile.pop(key,None);old_profile.pop(key,None)
    assert new_profile.pop('lil_trade_routes_editorial')==owned.CONFIG and new_profile==old_profile
    config=read(owned.CONFIG);normal=lambda s:str(s).replace('\\','/')
    assert [normal(v)for v in manifest['batches']]==[normal(v)for v in prior['batches']]+[normal(config['manuscript'])]
    assert len(manifest['batches'])==478 and len(registry['accepted_layers'])==114 and all(manifest['checks'].values())
    assert registry['latest_promoted_build']['profile']=='all-routes-unified-v1492'
    old,new=map(NdsImage.open,(OLD,ROM))
    assert[p for _,p,data in old.iter_files()if new.read_file(p)!=data]==[owned.PATH]
    for path,data in old.iter_components():assert new.read_file(path)==data,path
    before,after=(IlnkContainer.parse(v.read_file(owned.PATH)).blocks for v in(old,new))
    assert len(before)==len(after)==336
    assert[n for n,(a,b)in enumerate(zip(before,after,strict=True))if a!=b]==[24]
    base=NdsImage.open(manifest['base_rom']);stage=owned.apply_release(old,base)
    assert old.read_file(owned.PATH)==new.read_file(owned.PATH)
    assert len(stage['changed_records'])==13 and stage['block_growth_bytes']==136
    final=manifest['relocations'][owned.PATH]['lil_trade_routes_editorial']
    assert final['proof']==stage and final['release_config_sha256']==sha(Path(owned.CONFIG).read_bytes())
    arm=new.read_file('/__arm9__.bin')
    assert sha(arm)=='500b7d6cea559d7252ae4e67f94540e67739428823a17cf26842b6827712a41e'
    assert len(MainCodeFile(arm,0x02000000).sections[3].data)-48==123040
    builder=Path('scripts/build_integrated_release.py').read_bytes();addition=(ROOT/'builder_added_optional_stage.bin').read_bytes()
    assert builder.count(addition)==1 and builder.replace(addition,b'',1)==(ROOT/'builder_before.py').read_bytes()
    clean=Path('work/clean.nds');clean_sha=sha(clean.read_bytes())
    assert clean_sha=='f4f07c975cc293f5b2ba469747693d3dd37f2e6dfc408cf5910adf5e83d9177d'
    patch,reconstruction=ROM.with_suffix('.xdelta'),ROOT/'patch_reconstruction_RESEARCH_ONLY.nds'
    assert not patch.exists()and not reconstruction.exists()
    make_xdelta(clean,ROM,patch);apply_xdelta(clean,patch,reconstruction)
    assert reconstruction.read_bytes()==ROM.read_bytes()and sha(clean.read_bytes())==clean_sha
    save(output,{'candidate':str(ROM),'candidate_sha256':digest,'profile':manifest['profile'],
        'canonical_base':manifest['base_rom'],'canonical_sha256':manifest['base_sha256'],
        'manifest_sha256':sha(ROM.with_suffix('.manifest.json').read_bytes()),'release_stack_sha256':manifest['release_stack_sha256'],
        'all478_batches114_accepted_layers_and_prior_profiles_preserved':True,
        'only_SC2_block24_changed_relative_to_V1807':True,
        'all335_other_blocks_every_other_file_and_native_component_exact':True,
        'ARM9_sha256':sha(arm),'COMMON_sha256':sha(new.read_file('/COMMON/MESFILE.DK4')),
        'SC2_sha256':sha(new.read_file(owned.PATH)),'stage':stage,
        'registered_ROM_whole_file_byte_exact_to_actual_scene_research_ROM':True,'actual_scene_research_ROM':str(RESEARCH),
        'patch':str(patch),'patch_sha256':sha(patch.read_bytes()),'clean_input_sha256':clean_sha,
        'reconstruction':str(reconstruction),'complete_reconstruction_byte_exact':True,
        'startup_controls_and_editorial_completion_pending':True,
        'producer_sha256':sha(Path(__file__).read_bytes()),'full_goal_complete':False})
    print({'candidate_SHA256':digest,'patch_SHA256':sha(patch.read_bytes()),'batches':478,'changed_SC2_blocks':[24]},flush=True)
