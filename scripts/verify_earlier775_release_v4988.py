"""Whole registered ancestry,one-message ownership and exact clean-input reconstruction."""
from pathlib import Path
from copy import deepcopy
from ndspy.code import MainCodeFile
from dk4tool.patch import earlier775_reflow_v1 as owned
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.xdelta import make_xdelta,apply_xdelta
from dk4tool.rom.nds import NdsImage
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/earlier775_release_v4988')
ROM=Path('out/all_routes_combined_v4987_candidate.nds')
OLD=Path('out/all_routes_combined_v4966_candidate.nds')
REG=Path('work/analysis/earlier775_registration_v4986')
if __name__=='__main__':
    assert not ROOT.exists();terminal=read('work/analysis/earlier775_build_v4987/build_terminal.json')
    assert terminal['terminal'] and terminal['returncode']==0 and terminal['candidate_exists']
    manifest,prior=map(lambda p:read(p.with_suffix('.manifest.json')),[ROM,OLD]);registry=read('translations/release_stack.json');conf=read(owned.CONFIG)
    digest=sha(ROM.read_bytes());assert digest==manifest['candidate_sha256'] and manifest['profile']=='all-routes-unified-v4987'
    assert manifest['base_sha256']=='3cb827e4c52ab2086fb5a626835d72192085a958581279d3c79b0200bbf405fe'
    assert manifest['release_stack_sha256']==sha(Path('translations/release_stack.json').read_bytes())
    assert len(manifest['checks'])==18 and all(manifest['checks'].values()) and len(manifest['batches'])==566 and len(registry['accepted_layers'])==114
    restored=deepcopy(registry);profile=restored['profiles'].pop(manifest['profile']);assert restored==read(REG/'release_stack.before.json')
    oldprofile=deepcopy(registry['profiles']['all-routes-unified-v4966']);newprofile=deepcopy(profile)
    for item in [oldprofile,newprofile]:item.pop('description',None);item.pop('note',None)
    newprofile.pop('earlier775_reflow');assert oldprofile==newprofile
    normalize=lambda p:str(p).replace('\\','/')
    assert list(map(normalize,manifest['batches']))==list(map(normalize,prior['batches']))+[normalize(conf['manuscript'])]
    assert registry['latest_promoted_build']['profile']=='all-routes-unified-v4701'
    parent,new=NdsImage.open(OLD),NdsImage.open(ROM);baseline=NdsImage.open(manifest['base_rom'])
    file_changes=[p for _,p,data in parent.iter_files() if new.read_file(p)!=data];component_changes=[p for p,data in parent.iter_components() if new.read_file(p)!=data]
    assert file_changes==[owned.PATH] and not component_changes
    stage=owned.apply_release(parent,baseline);assert parent.read_file(owned.PATH)==new.read_file(owned.PATH)
    bound=manifest['relocations'][owned.PATH]['earlier775_reflow'];assert bound['proof']==stage and bound['release_config_sha256']==sha(Path(owned.CONFIG).read_bytes())
    arm=new.read_file('/__arm9__.bin');assert sha(arm)==conf['source_ARM9_sha256'] and len(MainCodeFile(arm,0x02000000).sections[3].data)-48==123040
    builder=Path('scripts/build_integrated_release.py').read_bytes();start=builder.index(b"    earlier775 = profile_config.get('earlier775_reflow')");end=builder.index(b'    # Lexically valid',start);added=builder[start:end]
    assert builder.replace(added,b'',1)==(REG/'build_integrated_release.py.before').read_bytes()
    clean=Path('work/clean.nds');clean_sha=sha(clean.read_bytes());assert clean_sha==conf['clean_ROM_sha256']
    patch=ROM.with_suffix('.xdelta');reconstruction=ROOT/'patch_reconstruction_RESEARCH_ONLY.nds';assert not patch.exists()
    ROOT.mkdir(parents=True);make_xdelta(clean,ROM,patch);apply_xdelta(clean,patch,reconstruction)
    assert ROM.read_bytes()==reconstruction.read_bytes()==Path('out/recommendation775_reference_v4983_RESEARCH_ONLY.nds').read_bytes()
    assert sha(clean.read_bytes())==clean_sha
    save(ROOT/'registered_release_verification.json',dict(candidate=str(ROM),candidate_sha256=digest,profile=manifest['profile'],
        manifest=str(ROM.with_suffix('.manifest.json')),manifest_sha256=sha(ROM.with_suffix('.manifest.json').read_bytes()),
        canonical_base=manifest['base_rom'],canonical_base_sha256=manifest['base_sha256'],all566_manifest_batches_and114_accepted_layers_present=True,
        all18_cumulative_release_checks_pass=True,all_earlier_profiles_and_main_V4701_unchanged=True,
        file_changes=file_changes,component_changes=component_changes,only_COMMON775_bytes_change=True,stage=stage,
        every_other_message_story_font_graphic_ARM9_ARM7_and_component_exact_to_V4966=True,
        ARM9_sha256=sha(arm),COMMON_sha256=sha(new.read_file(owned.PATH)),story_hashes={f'SC{i}':sha(new.read_file(f'/data/SC{i}.DK4')) for i in range(4)},
        patch=str(patch),patch_sha256=sha(patch.read_bytes()),clean_input_sha256=clean_sha,exact_patch_reconstruction=str(reconstruction),
        whole_ROM_reconstruction_byte_exact=True,current_startup_pending=True,new_editorial_credit=0,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    print(dict(candidate_sha256=digest,patch_sha256=sha(patch.read_bytes()),batches=566,accepted=114,exact_clean_input_reconstruction=True))
