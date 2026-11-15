"""Verify full registered ancestry, precisely bounded changes and a clean-input reconstruction."""
from copy import deepcopy
from pathlib import Path
from ndspy.code import MainCodeFile
from dk4tool.patch import lil_B210_editorial_v1 as story,Al_Ferid_name_release_v1 as name
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.xdelta import make_xdelta,apply_xdelta
from dk4tool.rom.nds import NdsImage
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/B210_Ferid_release_v6542');ROM=Path('out/all_routes_combined_v6541_candidate.nds');OLD=Path('out/all_routes_combined_v6488_candidate.nds');REG=Path('work/analysis/B210_Ferid_registration_v6540')
if __name__=='__main__':
    terminal=read('work/analysis/B210_Ferid_build_v6541/build_terminal.json');assert terminal['terminal'] and terminal['returncode']==0 and terminal['candidate_exists'];assert not ROOT.exists()
    manifest,prior=[read(p.with_suffix('.manifest.json')) for p in [ROM,OLD]];digest=sha(ROM.read_bytes());registry=read('translations/release_stack.json');configs=[read(m.CONFIG) for m in [story,name]]
    assert manifest['profile']=='all-routes-unified-v6541' and manifest['candidate_sha256']==digest and manifest['base_sha256']=='3cb827e4c52ab2086fb5a626835d72192085a958581279d3c79b0200bbf405fe'
    assert manifest['release_stack_sha256']==sha(Path('translations/release_stack.json').read_bytes()) and len(manifest['checks'])==18 and all(manifest['checks'].values())
    restored=deepcopy(registry);profile=restored['profiles'].pop(manifest['profile']);assert restored==read(REG/'release_stack.before.json');previous=deepcopy(registry['profiles']['all-routes-unified-v6488']);new=deepcopy(profile)
    for item in [previous,new]:item.pop('description',None);item.pop('note',None)
    assert new.pop('lil_B210_editorial')==story.CONFIG and new.pop('Al_Ferid_name')==name.CONFIG and previous==new
    normal=lambda p:str(p).replace('\\','/');assert [normal(p) for p in manifest['batches']]==[normal(p) for p in prior['batches']]+[normal(c['manuscript']) for c in configs]
    assert len(manifest['batches'])==602 and len(registry['accepted_layers'])==114 and registry['latest_promoted_build']['profile']=='all-routes-unified-v4701'
    before,after=NdsImage.open(OLD),NdsImage.open(ROM);baseline=NdsImage.open(manifest['base_rom']);file_changes=[p for _,p,v in before.iter_files() if after.read_file(p)!=v];component_changes=[p for p,v in before.iter_components() if after.read_file(p)!=v];assert file_changes==[story.PATH] and component_changes==[name.PATH]
    proofs=[]
    for module,key in [(story,'lil_B210_editorial'),(name,'Al_Ferid_name')]:
        proof=module.apply_release(before,baseline);bound=manifest['relocations'][module.PATH][key];assert bound['proof']==proof and bound['release_config_sha256']==sha(Path(module.CONFIG).read_bytes());proofs.append(proof)
    assert all(before.read_file(p)==v for _,p,v in after.iter_files()) and all(before.read_file(p)==v for p,v in after.iter_components())
    arm=after.read_file(name.PATH);assert sha(arm)==name.TARGET and len(MainCodeFile(arm,0x02000000).sections[3].data)-48==123264 and len(proofs[1]['data_plan']['changed_byte_offsets'])==5
    builder=Path('scripts/build_integrated_release.py').read_bytes();added=(REG/'builder.stage.bin').read_bytes();assert builder.count(added)==1 and builder.replace(added,b'',1)==(REG/'build_integrated_release.py.before').read_bytes() and builder.index(b"profile_config.get('lil_B209_editorial')")<builder.index(added)<builder.index(b'    # Lexically valid')
    ref=read('work/analysis/B210_Ferid_reference_v6539/combined_reference_receipt.json');assert ROM.read_bytes()==Path(ref['research_ROM']).read_bytes() and digest==ref['research_ROM_sha256']
    clean=Path('work/clean.nds');clean_sha=sha(clean.read_bytes());assert clean_sha==configs[0]['clean_ROM_sha256'];patch=ROM.with_suffix('.xdelta');result=ROOT/'patch_reconstruction_RESEARCH_ONLY.nds';assert not patch.exists() and not result.exists();ROOT.mkdir(parents=True);make_xdelta(clean,ROM,patch);apply_xdelta(clean,patch,result);assert result.read_bytes()==ROM.read_bytes() and sha(clean.read_bytes())==clean_sha
    save(ROOT/'registered_release_verification.json',dict(candidate=str(ROM),candidate_sha256=digest,manifest=str(ROM.with_suffix('.manifest.json')),manifest_sha256=sha(ROM.with_suffix('.manifest.json').read_bytes()),profile=manifest['profile'],canonical_base=manifest['base_rom'],canonical_base_sha256=manifest['base_sha256'],manifest_batches=602,accepted_layers=114,all602_manifest_batches_and114_accepted_layers_present=True,all18_registered_release_checks_pass=True,all_earlier_profiles_and_V4701_promotion_unchanged=True,file_changes=file_changes,component_changes=component_changes,every_other_file_component_graphic_route_font_and_code_exact_to_V6488=True,stage_proofs=proofs,ARM9_sha256=sha(arm),COMMON_sha256=sha(after.read_file('/COMMON/MESFILE.DK4')),story_hashes={f'SC{i}':sha(after.read_file(f'/data/SC{i}.DK4')) for i in range(4)},all621_name_fields_sections_BSS_cache_copy_and123264_extent_preserved=True,only_five_owned_name_data_bytes_changed=True,patch=str(patch),patch_sha256=sha(patch.read_bytes()),clean_input_sha256=clean_sha,exact_patch_reconstruction=str(result),whole_ROM_reconstruction_byte_exact=True,exact_combined_approved_reference=True,revised_current_startup_pending=True,completion_credit_added=0,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False));print(dict(candidate_sha256=digest,patch_sha256=sha(patch.read_bytes()),manifest_batches=602,accepted_layers=114,whole_clean_input_reconstruction_exact=True),flush=True)
