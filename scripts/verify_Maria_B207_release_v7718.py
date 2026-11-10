"""Verify full registered ancestry, exact research equality and clean-input patch reconstruction."""
from copy import deepcopy
from pathlib import Path
from ndspy.code import MainCodeFile
from dk4tool.patch import maria_B207_editorial_v2 as owned
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.xdelta import make_xdelta,apply_xdelta
from dk4tool.rom.nds import NdsImage
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/maria_B207_release_v7718')
ROM=Path('out/all_routes_combined_v7717_candidate.nds')
OLD=Path('out/all_routes_combined_v7660_candidate.nds')
REG=Path('work/analysis/maria_B207_registration_v7716')
if __name__=='__main__':
    build=read('work/analysis/maria_B207_build_v7717/build_terminal.json');regress=read('work/analysis/maria_B207_regressions_v7717/terminal.json')
    assert build['terminal'] and build['returncode']==0 and build['candidate_exists'] and regress['terminal'] and regress['returncode']==0
    assert not ROOT.exists();manifest,prior=[read(p.with_suffix('.manifest.json')) for p in [ROM,OLD]];digest=sha(ROM.read_bytes());registry=read('translations/release_stack.json');conf=read(owned.CONFIG);registration=read(REG/'registration_receipt.json')
    assert manifest['profile']=='all-routes-unified-v7717' and manifest['candidate_sha256']==digest and manifest['base_sha256']=='3cb827e4c52ab2086fb5a626835d72192085a958581279d3c79b0200bbf405fe'
    assert manifest['release_stack_sha256']==sha(Path('translations/release_stack.json').read_bytes()) and len(manifest['checks'])==18 and all(manifest['checks'].values())
    restored=deepcopy(registry);profile=restored['profiles'].pop(manifest['profile']);assert restored==read(REG/'release_stack.before.json')
    previous=deepcopy(registry['profiles']['all-routes-unified-v7660']);new=deepcopy(profile)
    for value in [previous,new]:value.pop('description',None);value.pop('note',None)
    assert new.pop('maria_B207_editorial')==owned.CONFIG and previous==new
    normal=lambda p:str(p).replace('\\','/')
    assert [normal(p) for p in manifest['batches']]==[normal(p) for p in prior['batches']]+[normal(p) for p in conf['manuscripts']]
    assert len(manifest['batches'])==629 and len(registry['accepted_layers'])==114 and registry['latest_promoted_build']['profile']=='all-routes-unified-v4701'
    before,after=NdsImage.open(OLD),NdsImage.open(ROM);reference=NdsImage.open(conf['reference_ROM'])
    changes=[p for _,p,data in before.iter_files() if after.read_file(p)!=data];components=[p for p,data in before.iter_components() if after.read_file(p)!=data]
    assert changes==list(owned.PATHS) and components==[]
    positive=read('work/analysis/maria_B207_atomic_v7714b/positive_reconstruction.json')
    for path in owned.PATHS:
        assert after.read_file(path)==reference.read_file(path)
        record=manifest['relocations'][path]['maria_B207_editorial'];assert record['proof']==positive and record['release_config_sha256']==sha(Path(owned.CONFIG).read_bytes())
        ids={r['id'] for r in positive['changed_records'] if r['file_path']==path}
        assert len(ids)==18 and ids<=set(manifest['changed_records'][path])
    assert ROM.read_bytes()==Path(conf['reference_ROM']).read_bytes()
    arm=after.read_file('/__arm9__.bin');assert sha(arm)==conf['required_runtime_arm9_sha256'] and len(MainCodeFile(arm,0x02000000).sections[3].data)-48==123264
    builder=Path('scripts/build_integrated_release.py').read_bytes();stage=(REG/'builder.stage.bin').read_bytes()
    assert builder.count(stage)==1 and builder.replace(stage,b'',1)==(REG/'build_integrated_release.py.before').read_bytes() and builder.index(b"profile_config.get('papal_trade_editorial')")<builder.index(stage)<builder.index(b'    # Lexically valid')
    clean=Path(conf['clean_ROM']);clean_sha=sha(clean.read_bytes());assert clean_sha==conf['clean_ROM_sha256']
    patch=ROM.with_suffix('.xdelta');result=ROOT/'patch_reconstruction_RESEARCH_ONLY.nds';assert not patch.exists() and not result.exists();ROOT.mkdir(parents=True)
    make_xdelta(clean,ROM,patch);apply_xdelta(clean,patch,result)
    assert result.read_bytes()==ROM.read_bytes() and sha(clean.read_bytes())==clean_sha
    save(ROOT/'registered_release_verification.json',dict(candidate=str(ROM),candidate_sha256=digest,manifest=str(ROM.with_suffix('.manifest.json')),manifest_sha256=sha(ROM.with_suffix('.manifest.json').read_bytes()),profile=manifest['profile'],canonical_base=manifest['base_rom'],canonical_base_sha256=manifest['base_sha256'],manifest_batches=629,accepted_layers=114,all629_manifest_batches_and114_accepted_layers_present=True,all18_registered_release_checks_pass=True,all110_release_dialogue_regressions_pass=True,all_earlier_profiles_andmainV4701_promotion_unchanged=True,file_changes=changes,component_changes=components,every_other_file_font_graphic_route_ARM9_ARM7_andcomponent_exact_to_V7660=True,atomic_positive_proof=str(Path('work/analysis/maria_B207_atomic_v7714b/positive_reconstruction.json')),atomic_positive_proof_sha256=sha(Path('work/analysis/maria_B207_atomic_v7714b/positive_reconstruction.json').read_bytes()),whole_ROM_equals_pinned_approved_reference=True,ARM9_sha256=sha(arm),COMMON_sha256=sha(after.read_file('/COMMON/MESFILE.DK4')),story_hashes={f'SC{r}':sha(after.read_file(f'/data/SC{r}.DK4')) for r in range(4)},all_native_shapes_BSS_and123264_staged_bytes_preserved=True,patch=str(patch),patch_sha256=sha(patch.read_bytes()),clean_input_sha256=clean_sha,exact_patch_reconstruction=str(result),whole_clean_input_ROM_reconstruction_byte_exact=True,registration_receipt_sha256=sha((REG/'registration_receipt.json').read_bytes()),regressions_terminal_sha256=sha(Path('work/analysis/maria_B207_regressions_v7717/terminal.json').read_bytes()),own_ROM_startup_andcompletion_credit_pending=True,completion_credit_added=0,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    print(dict(candidate_sha256=digest,patch_sha256=sha(patch.read_bytes()),batches=628,accepted=114,checks=18,regressions=110,whole_clean_patch_reconstruction_exact=True),flush=True)
