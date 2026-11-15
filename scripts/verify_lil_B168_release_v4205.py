"""Full registered ancestry and exactly reconstructable clean-input patch."""
from copy import deepcopy
from pathlib import Path
from ndspy.code import MainCodeFile
from dk4tool.patch import lil_B168_editorial_v1 as owned
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.xdelta import make_xdelta,apply_xdelta
from dk4tool.rom.nds import NdsImage
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/lil_B168_release_v4205')
ROM=Path('out/all_routes_combined_v4204_candidate.nds')
OLD=Path('out/all_routes_combined_v4160_candidate.nds')
REG=Path('work/analysis/lil_B168_registration_v4203')
if __name__=='__main__':
    assert not ROOT.exists();manifest,prior=[read(p.with_suffix('.manifest.json')) for p in [ROM,OLD]]
    digest=sha(ROM.read_bytes());registry=read('translations/release_stack.json');conf=read(owned.CONFIG)
    assert manifest['profile']=='all-routes-unified-v4204' and manifest['candidate_sha256']==digest
    assert manifest['base_sha256']=='3cb827e4c52ab2086fb5a626835d72192085a958581279d3c79b0200bbf405fe'
    assert manifest['release_stack_sha256']==sha(Path('translations/release_stack.json').read_bytes()) and all(manifest['checks'].values())
    restored=deepcopy(registry);profile=restored['profiles'].pop(manifest['profile'])
    assert restored==read(REG/'release_stack.before.json') and profile['lil_B168_editorial']==owned.CONFIG
    previous=deepcopy(registry['profiles']['all-routes-unified-v4160']);new=deepcopy(profile)
    for item in [previous,new]:item.pop('description',None);item.pop('note',None)
    new.pop('lil_B168_editorial');assert previous==new
    normal=lambda p:str(p).replace('\\','/')
    assert [normal(p) for p in manifest['batches']]==[normal(p) for p in prior['batches']]+[normal(conf['manuscript'])]
    assert len(manifest['batches'])==544 and len(registry['accepted_layers'])==114
    assert registry['latest_promoted_build']['profile']=='all-routes-unified-v4160'
    before,after=NdsImage.open(OLD),NdsImage.open(ROM);baseline=NdsImage.open(manifest['base_rom'])
    file_changes=[p for _,p,data in before.iter_files() if after.read_file(p)!=data]
    component_changes=[p for p,data in before.iter_components() if after.read_file(p)!=data]
    assert file_changes==[owned.PATH] and component_changes==[],(file_changes,component_changes)
    stage=owned.apply_release(before,baseline);assert before.read_file(owned.PATH)==after.read_file(owned.PATH)
    bound=manifest['relocations'][owned.PATH]['lil_B168_editorial']
    assert bound['proof']==stage and bound['release_config_sha256']==sha(Path(owned.CONFIG).read_bytes())
    assert sha(after.read_file(owned.PATH))==conf['target_SC2_sha256']
    arm=after.read_file('/__arm9__.bin');assert sha(arm)==conf['required_runtime_arm9_sha256']
    assert len(MainCodeFile(arm,0x02000000).sections[3].data)-48==123040
    builder=Path('scripts/build_integrated_release.py').read_bytes();start=builder.index(b"    lil_mikhail = profile_config.get('lil_B168_editorial')");finish=builder.index(b'    # Lexically valid',start);added=builder[start:finish]
    assert sha(added)==read(REG/'builder_hook_AST_review.json')['stage_sha256'] and builder.count(added)==1 and builder.replace(added,b'',1)==(REG/'build_integrated_release.py.before').read_bytes()
    clean=Path('work/clean.nds');clean_sha=sha(clean.read_bytes());assert clean_sha==conf['clean_ROM_sha256']
    patch=ROM.with_suffix('.xdelta');result=ROOT/'patch_reconstruction_RESEARCH_ONLY.nds'
    assert not patch.exists() and not result.exists();ROOT.mkdir(parents=True)
    make_xdelta(clean,ROM,patch);apply_xdelta(clean,patch,result)
    assert result.read_bytes()==ROM.read_bytes() and sha(clean.read_bytes())==clean_sha
    save(ROOT/'registered_release_verification.json',dict(candidate=str(ROM),candidate_sha256=digest,
        manifest=str(ROM.with_suffix('.manifest.json')),manifest_sha256=sha(ROM.with_suffix('.manifest.json').read_bytes()),
        profile=manifest['profile'],canonical_base=manifest['base_rom'],canonical_base_sha256=manifest['base_sha256'],
        all544_manifest_batches_and114_accepted_layers_present=True,all_earlier_profiles_and_V4160_promotion_unchanged=True,
        file_changes=file_changes,component_changes=component_changes,
        every_other_file_font_graphic_route_ARM9_ARM7_and_component_exact_to_V4160=True,stage=stage,
        ARM9_sha256=sha(arm),COMMON_sha256=sha(after.read_file('/COMMON/MESFILE.DK4')),
        story_hashes={f'SC{i}':sha(after.read_file(f'/data/SC{i}.DK4')) for i in range(4)},
        all_native_payload_proofs_bound_by_exact_target_hash=True,
        all_source_shapes_BSS_and123040_staged_bytes_preserved=True,
        patch=str(patch),patch_sha256=sha(patch.read_bytes()),clean_input_sha256=clean_sha,
        exact_patch_reconstruction=str(result),whole_ROM_reconstruction_byte_exact=True,
        revised_current_startup_pending=True,completion_credit_added=0,
        producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    print(dict(candidate_sha256=digest,patch_sha256=sha(patch.read_bytes()),manifest_batches=544,accepted_layers=114,whole_clean_input_reconstruction_exact=True),flush=True)
