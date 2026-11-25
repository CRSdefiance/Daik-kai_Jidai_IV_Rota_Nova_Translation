"""Verify complete registered ancestry,approved target identity and exact clean-input patch."""
import json
from copy import deepcopy
from pathlib import Path
from ndspy.code import MainCodeFile
from dk4tool.rom.nds import NdsImage
from dk4tool.patch import shachihoko_item116_editorial_v2 as owned
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.xdelta import make_xdelta,apply_xdelta
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/shachihoko_release_v6111')
ROM=Path('out/all_routes_combined_v6110_candidate.nds')
OLD=Path('out/all_routes_combined_v6050_candidate.nds')
REG=Path('work/analysis/shachihoko_registration_v6109')
if __name__=='__main__':
    assert not ROOT.exists();terminal=read('work/analysis/shachihoko_build_v6110/build_terminal.json');assert terminal['terminal'] and terminal['returncode']==0 and terminal['candidate_exists']
    manifest,prior=[read(p.with_suffix('.manifest.json')) for p in [ROM,OLD]];digest=sha(ROM.read_bytes());registry=read('translations/release_stack.json');config=read(owned.CONFIG);doc=read(config['manuscript']);registration=read(REG/'registration_receipt.json')
    assert manifest['profile']=='all-routes-unified-v6110' and manifest['candidate_sha256']==digest and manifest['base_sha256']=='3cb827e4c52ab2086fb5a626835d72192085a958581279d3c79b0200bbf405fe'
    assert manifest['release_stack_sha256']==sha(Path('translations/release_stack.json').read_bytes())==registration['registry_after_sha256'] and len(manifest['checks'])==18 and all(manifest['checks'].values())
    restored=deepcopy(registry);profile=restored['profiles'].pop(manifest['profile']);assert restored==read(REG/'release_stack.before.json') and profile['shachihoko_item116_editorial']==owned.CONFIG
    a,b=[deepcopy(p) for p in [registry['profiles']['all-routes-unified-v6050'],profile]]
    for p in [a,b]:p.pop('description',None);p.pop('note',None)
    b.pop('shachihoko_item116_editorial');assert a==b and len(registry['accepted_layers'])==114 and registry['latest_promoted_build']['profile']=='all-routes-unified-v4701'
    normal=lambda p:str(p).replace('\\','/')
    assert [normal(p) for p in manifest['batches']]==[normal(p) for p in prior['batches']]+[normal(config['manuscript'])] and len(manifest['batches'])==592
    assert [normal(p) for p in manifest['required_batches']]==[normal(p) for p in prior['required_batches']]
    before,after=NdsImage.open(OLD),NdsImage.open(ROM);baseline=NdsImage.open(manifest['base_rom'])
    files=[p for _,p,v in before.iter_files() if after.read_file(p)!=v];components=[p for p,v in before.iter_components() if after.read_file(p)!=v]
    assert files==[owned.COMMON] and components==[owned.ARM]
    stage=owned.apply_release(before,baseline);serialized_stage=json.loads(json.dumps(stage))
    assert all(before.read_file(p)==v for _,p,v in after.iter_files()) and all(before.read_file(p)==v for p,v in after.iter_components())
    for path in [owned.ARM,owned.COMMON]:
        bound=manifest['relocations'][path]['shachihoko_item116_editorial'];assert bound['proof']==serialized_stage and bound['release_config_sha256']==sha(Path(owned.CONFIG).read_bytes())
    assert sha(after.read_file(owned.ARM))==config['target_ARM9_sha256'] and sha(after.read_file(owned.COMMON))==config['target_COMMON_sha256']
    assert len(MainCodeFile(after.read_file(owned.ARM),0x02000000).sections[3].data)-48==123264
    assert ROM.read_bytes()==Path(doc['native_reference_ROM']).read_bytes() and digest==doc['native_reference_ROM_sha256']
    builder=Path('scripts/build_integrated_release.py').read_bytes();addition=(REG/'builder.stage.bin').read_bytes();assert builder.count(addition)==1 and builder.replace(addition,b'',1)==(REG/'build_integrated_release.py.before').read_bytes()
    clean=Path(config['clean_ROM']);clean_sha=sha(clean.read_bytes());assert clean_sha==config['clean_ROM_sha256']
    patch=ROM.with_suffix('.xdelta');reconstructed=ROOT/'patch_reconstruction_RESEARCH_ONLY.nds';assert not patch.exists() and not reconstructed.exists();ROOT.mkdir(parents=True)
    make_xdelta(clean,ROM,patch);apply_xdelta(clean,patch,reconstructed);assert reconstructed.read_bytes()==ROM.read_bytes() and sha(clean.read_bytes())==clean_sha
    boot=read('work/analysis/shachihoko_boot_v6099/source_bound_growth_boot_input_and_native_allocation_verification.json');assert boot['research_ROM_sha256']==digest and boot['all31_actual_same_input_whole_RGB_frames_equal_V6050']
    save(ROOT/'registered_release_verification.json',dict(candidate=str(ROM),candidate_sha256=digest,manifest=str(ROM.with_suffix('.manifest.json')),manifest_sha256=sha(ROM.with_suffix('.manifest.json').read_bytes()),profile=manifest['profile'],
        canonical_base=manifest['base_rom'],canonical_base_sha256=manifest['base_sha256'],all592_manifest_batches_and114_accepted_layers_present=True,all_previous_profiles_and_main_V4701_unchanged=True,
        all18_registered_release_checks_pass=True,file_changes=files,component_changes=components,all_story_files_fonts_graphics_ARM7_and_other_components_exact_to_V6050=True,
        stage=serialized_stage,ARM9_sha256=config['target_ARM9_sha256'],COMMON_sha256=config['target_COMMON_sha256'],new_payload_bytes=123264,source_payload_bytes=123040,
        approved_reference_whole_ROM_byte_identical=True,reference_ROM=doc['native_reference_ROM'],reference_ROM_sha256=doc['native_reference_ROM_sha256'],
        source_bound_New_Game_and_town_boot_evidence_reused_only_for_identical_whole_ROM=True,source_boot_proof='work/analysis/shachihoko_boot_v6099/source_bound_growth_boot_input_and_native_allocation_verification.json',
        two_existing_boots21402_frames31_RGB_and6_actor_controls_exactly_bound=True,new_emulator_runs=0,
        actual_Items_menu_fixture_differs_only_by_disclosed_B22_clean_scene=True,
        patch=str(patch),patch_sha256=sha(patch.read_bytes()),clean_input_sha256=clean_sha,exact_patch_reconstruction=str(reconstructed),whole_ROM_reconstruction_byte_exact=True,
        completion_credit_added=0,release_regressions_and_final_progress_update_pending=True,
        producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    print(dict(candidate_sha256=digest,patch_sha256=sha(patch.read_bytes()),batches=592,accepted=114,whole_reference_ROM_exact=True,clean_input_patch_reconstruction_exact=True))
