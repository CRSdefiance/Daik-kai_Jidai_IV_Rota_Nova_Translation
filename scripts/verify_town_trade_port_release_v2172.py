"""Registered cumulative ancestry, exact internal payload and clean-input patch."""
from pathlib import Path
from copy import deepcopy
from ndspy.code import MainCodeFile
from dk4tool.patch import town_trade_port_contextual_editorial as owned
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.xdelta import make_xdelta,apply_xdelta
from dk4tool.rom.nds import NdsImage
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/town_trade_port_release_v2172')
ROM=Path('out/all_routes_combined_v2171_candidate.nds')
OLD=Path('out/all_routes_combined_v2143_candidate.nds')
REG=Path('work/analysis/town_trade_port_registration_v2170')
if __name__=='__main__':
 assert not ROOT.exists();ROOT.mkdir(parents=True)
 manifest,prior=[read(p.with_suffix('.manifest.json'))for p in(ROM,OLD)];digest=sha(ROM.read_bytes());registry=read('translations/release_stack.json');conf=read(owned.CONFIG)
 assert manifest['profile']=='all-routes-unified-v2171'and manifest['candidate_sha256']==digest and manifest['base_sha256']=='3cb827e4c52ab2086fb5a626835d72192085a958581279d3c79b0200bbf405fe'
 assert manifest['release_stack_sha256']==sha(Path('translations/release_stack.json').read_bytes())and all(manifest['checks'].values())
 restored=deepcopy(registry);profile=restored['profiles'].pop(manifest['profile']);assert restored==read(REG/'registry_before_raw.json')and profile['town_trade_port_contextual_editorial']==owned.CONFIG
 parent_profile=deepcopy(registry['profiles']['all-routes-unified-v2143']);new_profile=deepcopy(profile)
 for p in(parent_profile,new_profile):p.pop('description',None);p.pop('note',None)
 new_profile.pop('town_trade_port_contextual_editorial');assert parent_profile==new_profile
 normal=lambda p:str(p).replace('\\','/')
 assert [normal(p)for p in manifest['batches']]==[normal(p)for p in prior['batches']]+[normal(conf['manuscript'])]and len(manifest['batches'])==492 and len(registry['accepted_layers'])==114
 assert registry['latest_promoted_build']['profile']=='all-routes-unified-v1492'
 before,after=NdsImage.open(OLD),NdsImage.open(ROM);arm=after.read_file('/__arm9__.bin');common=after.read_file(owned.PATH)
 file_changes=[p for _,p,data in before.iter_files()if after.read_file(p)!=data];component_changes=[p for p,data in before.iter_components()if after.read_file(p)!=data]
 assert file_changes==[owned.PATH]and component_changes==['/__arm9__.bin'],(file_changes,component_changes)
 baseline=NdsImage.open(manifest['base_rom']);stage=owned.apply_release(before,baseline)
 assert before.read_file(owned.PATH)==common and before.read_file('/__arm9__.bin')==arm
 final=manifest['relocations'][owned.PATH]['town_trade_port_contextual_editorial'];assert final['proof']==stage and final['release_config_sha256']==sha(Path(owned.CONFIG).read_bytes())
 assert sha(arm)==conf['target_ARM9_sha256']and sha(common)==conf['target_COMMON_sha256']
 assert len(MainCodeFile(arm,0x02000000).sections[3].data)-48==123040
 source_shape=lambda a:[(s.ramAddress,len(s.data),s.bssSize)for s in MainCodeFile(a,0x02000000).sections]
 assert source_shape(arm)==source_shape(NdsImage.open(OLD).read_file('/__arm9__.bin'))
 clean=Path('work/clean.nds');clean_sha=sha(clean.read_bytes());patch=ROM.with_suffix('.xdelta');result=ROOT/'patch_reconstruction_RESEARCH_ONLY.nds';assert not patch.exists()and not result.exists()
 make_xdelta(clean,ROM,patch);apply_xdelta(clean,patch,result);assert result.read_bytes()==ROM.read_bytes()and sha(clean.read_bytes())==clean_sha
 builder=Path('scripts/build_integrated_release.py').read_bytes();added=(REG/'builder_added_optional_stage.bin').read_bytes();assert builder.count(added)==1 and builder.replace(added,b'',1)==(REG/'builder_before.py').read_bytes()
 save(ROOT/'registered_release_verification.json',dict(candidate=str(ROM),candidate_sha256=digest,manifest=str(ROM.with_suffix('.manifest.json')),manifest_sha256=sha(ROM.with_suffix('.manifest.json').read_bytes()),profile=manifest['profile'],canonical_base=manifest['base_rom'],canonical_base_sha256=manifest['base_sha256'],all492_manifest_batches_and114_accepted_layers_present=True,all_earlier_profiles_and_V1492_promotion_unchanged=True,file_changes=file_changes,component_changes=component_changes,every_other_file_font_graphic_route_ARM7_and_component_exact_to_V2143=True,stage=stage,ARM9_sha256=sha(arm),COMMON_sha256=sha(common),story_hashes={f'SC{i}':sha(after.read_file(f'/data/SC{i}.DK4'))for i in range(4)},all_native_payload_proofs_bound_by_exact_target_hash=True,all_source_shapes_BSS_and123040_staged_bytes_preserved=True,patch=str(patch),patch_sha256=sha(patch.read_bytes()),clean_input_sha256=clean_sha,exact_patch_reconstruction=str(result),whole_ROM_reconstruction_byte_exact=True,revised_startup_and_representative_town_actual_pending=True,completion_credit_added=0,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
 print(dict(candidate_sha256=digest,patch_sha256=sha(patch.read_bytes()),manifest_batches=492,accepted_layers=114,whole_clean_input_reconstruction_exact=True),flush=True)
