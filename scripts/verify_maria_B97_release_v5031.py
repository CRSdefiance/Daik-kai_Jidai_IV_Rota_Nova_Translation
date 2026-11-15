"""Verify the registered cumulative ancestry and byte-exact patch from clean input."""
from copy import deepcopy
from pathlib import Path
from ndspy.code import MainCodeFile
from dk4tool.rom.nds import NdsImage
from dk4tool.patch import maria_B97_editorial_v2 as owned
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.xdelta import make_xdelta,apply_xdelta
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/maria_B97_release_v5031')
ROM=Path('out/all_routes_combined_v5030_candidate.nds')
OLD=Path('out/all_routes_combined_v4987_candidate.nds')
REG=Path('work/analysis/maria_B97_registration_v5029b')
if __name__=='__main__':
    assert not ROOT.exists();terminal=read('work/analysis/maria_B97_build_v5030/build_terminal.json');assert terminal['terminal'] and terminal['returncode']==0 and terminal['candidate_exists']
    manifest,prior=[read(p.with_suffix('.manifest.json')) for p in [ROM,OLD]];digest=sha(ROM.read_bytes());registry=read('translations/release_stack.json');conf=read(owned.CONFIG)
    assert manifest['profile']=='all-routes-unified-v5030' and manifest['candidate_sha256']==digest and manifest['base_sha256']=='3cb827e4c52ab2086fb5a626835d72192085a958581279d3c79b0200bbf405fe'
    assert manifest['release_stack_sha256']==sha(Path('translations/release_stack.json').read_bytes()) and len(manifest['checks'])==18 and all(manifest['checks'].values())
    restored=deepcopy(registry);profile=restored['profiles'].pop(manifest['profile']);assert restored==read(REG/'release_stack.before.json') and profile['maria_B97_editorial']==owned.CONFIG
    previous=deepcopy(registry['profiles']['all-routes-unified-v4987']);new=deepcopy(profile)
    for item in [previous,new]:item.pop('description',None);item.pop('note',None)
    new.pop('maria_B97_editorial');assert previous==new
    norm=lambda p:str(p).replace('\\','/');assert [norm(p) for p in manifest['batches']]==[norm(p) for p in prior['batches']]+[norm(conf['manuscript'])]
    assert len(manifest['batches'])==567 and len(registry['accepted_layers'])==114 and registry['latest_promoted_build']['profile']=='all-routes-unified-v4701'
    before,after=NdsImage.open(OLD),NdsImage.open(ROM);baseline=NdsImage.open(manifest['base_rom']);files=[p for _,p,v in before.iter_files() if after.read_file(p)!=v];components=[p for p,v in before.iter_components() if after.read_file(p)!=v]
    assert files==[owned.PATH] and not components;stage=owned.apply_release(before,baseline);assert before.read_file(owned.PATH)==after.read_file(owned.PATH)
    bound=manifest['relocations'][owned.PATH]['maria_B97_editorial'];assert bound['proof']==stage and bound['release_config_sha256']==sha(Path(owned.CONFIG).read_bytes())
    assert sha(after.read_file(owned.PATH))==conf['target_SC3_sha256'];arm=after.read_file('/__arm9__.bin');assert sha(arm)==conf['required_runtime_arm9_sha256'] and len(MainCodeFile(arm,0x02000000).sections[3].data)-48==123040
    added=(REG/'builder_added_stage.bin').read_bytes();builder=Path('scripts/build_integrated_release.py').read_bytes();assert builder.count(added)==1 and builder.replace(added,b'',1)==(REG/'build_integrated_release.py.before').read_bytes()
    clean=Path('work/clean.nds');clean_sha=sha(clean.read_bytes());assert clean_sha==conf['clean_ROM_sha256'];patch=ROM.with_suffix('.xdelta');reconstruction=ROOT/'patch_reconstruction_RESEARCH_ONLY.nds';assert not patch.exists()
    ROOT.mkdir(parents=True);make_xdelta(clean,ROM,patch);apply_xdelta(clean,patch,reconstruction)
    assert reconstruction.read_bytes()==ROM.read_bytes()==Path('out/maria_B97_reference_v5021_RESEARCH_ONLY.nds').read_bytes() and sha(clean.read_bytes())==clean_sha
    save(ROOT/'registered_release_verification.json',dict(candidate=str(ROM),candidate_sha256=digest,manifest=str(ROM.with_suffix('.manifest.json')),manifest_sha256=sha(ROM.with_suffix('.manifest.json').read_bytes()),profile=manifest['profile'],canonical_base=manifest['base_rom'],canonical_base_sha256=manifest['base_sha256'],all567_manifest_batches_and114_accepted_layers_present=True,all18_release_checks_pass=True,all_earlier_profiles_and_V4701_promotion_preserved=True,file_changes=files,component_changes=components,every_other_file_font_graphic_story_ARM9_ARM7_component_and123040_pool_exact_to_V4987=True,stage=stage,ARM9_sha256=sha(arm),COMMON_sha256=sha(after.read_file('/COMMON/MESFILE.DK4')),story_hashes={f'SC{i}':sha(after.read_file(f'/data/SC{i}.DK4')) for i in range(4)},patch=str(patch),patch_sha256=sha(patch.read_bytes()),clean_input_sha256=clean_sha,exact_patch_reconstruction=str(reconstruction),whole_ROM_reconstruction_byte_exact=True,reference_ROM_byte_exact=True,revised_current_startup_pending=True,new_review_credit=0,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    print(dict(candidate_sha256=digest,patch_sha256=sha(patch.read_bytes()),manifest_batches=567,accepted=114,checks=18,clean_reconstruction_exact=True))
