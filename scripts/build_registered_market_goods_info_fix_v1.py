"""Stage/register the exact cumulative data-only market-format ownership correction."""
from copy import deepcopy
from pathlib import Path
import os
import sys
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.market_goods_info_terminator_v1 import transform,FIELDS,NEW_FORMAT,PAYLOAD
from dk4tool.patch.xdelta import make_xdelta,apply_xdelta
from dk4tool.script.format_safety_relocated_v1 import bind_registered_story_percent_guard
from scripts.audit_story_glyph_consistency import load,save

ROOT=Path('work/market_goods_info_terminator_20261109_v1')
OUT=Path('work/market_goods_info_terminator_release_v1')
PARENT=Path('work/maria301_release_v1/registered_release_verification.json')
REGISTRY=Path('translations/release_stack.json');CLEAN=Path('work/clean.nds')
PROFILE='all-routes-market-goods-info-terminator-v1-20261109'
CANDIDATE=OUT/'all_routes_market_goods_info_fix_candidate.nds'
MANIFEST=CANDIDATE.with_suffix('.manifest.json');PATCH=CANDIDATE.with_suffix('.xdelta')
RECONSTRUCTED=OUT/'clean_input_reconstruction_RESEARCH_ONLY.nds'
CONFIG=OUT/'market_goods_info_terminator_release.json'
PARENT_REGISTRY=OUT/'release_stack_before_market_fix.json'
STAGED=OUT/'staged_successor.json';RELEASE=OUT/'registered_release_verification.json'
STARTUP=OUT/'own_registered_startup_verification.json';GAMEPLAY=OUT/'market_gameplay_verification.json'
GETTERS=OUT/'own_registered_name_getters_v1.json'
CHECK='registered_market_goods_info_terminated_format_and_complete_parent_inverse'

def digest(p):return sha(Path(p).read_bytes())

def stage():
    assert not OUT.exists()
    parent=load(PARENT);registry=load(REGISTRY);old=load(parent['manifest'])
    prep_path=ROOT/'prepared_v1/preparation.json';native_path=ROOT/'native_verification_v1.json'
    prep,native=map(load,[prep_path,native_path])
    assert digest(REGISTRY)==parent['registry_sha256'] and digest(parent['manifest'])==parent['manifest_sha256']
    assert digest(parent['candidate'])==parent['candidate_sha256']==prep['parent_ROM_sha256']
    assert digest(parent['canonical_base'])==parent['canonical_sha256'] and digest(CLEAN)==parent['clean_input_sha256']
    assert not parent['own_registered_startup_pending'] and parent['clean_input_patch_byte_exact']
    assert len(old['batches'])==709 and len(old['checks'])==44 and all(old['checks'].values())
    assert len(registry['accepted_layers'])==114 and PROFILE not in registry['profiles']
    prior_profile=registry['profiles'][parent['profile']]
    assert prior_profile['ascii_glyph_right_bounds'] and old['checks']['registered_runtime_bounds_and_complete_parent_target_inverse']
    assert native['source_cases']==native['corrected_cases']==12 and native['target_ARM9_sha256']==prep['target_ARM9_sha256']
    assert native['all_corrected_outputs_complete_ASCII_with_one_literal_percent_andone_NUL']
    proposed=NdsImage.open(parent['candidate']);original=proposed.read_file('/__arm9__.bin')
    arm,proof=transform(original)
    assert arm==(ROOT/'prepared_v1/target_arm9.bin').read_bytes()
    proposed.replace_file('/__arm9__.bin',arm)
    parent_image=NdsImage.open(parent['candidate'])
    assert [p for _,p,data in parent_image.iter_files() if proposed.read_file(p)!=data]==['/__arm9__.bin']
    assert all(proposed.read_file(p)==data for p,data in parent_image.iter_components())
    archives=[f'/data/SC{n}.DK4' for n in range(4)];clean=NdsImage.open(CLEAN)
    percent=bind_registered_story_percent_guard(old['story_percent_contract']['exact_relocation_receipt'])(
        {p:clean.read_file(p) for p in archives},{p:proposed.read_file(p) for p in archives})
    assert percent==old['story_percent_contract']
    output=bytes(proposed.rom.save());proposed.replace_file('/__arm9__.bin',original)
    assert bytes(proposed.rom.save())==Path(parent['candidate']).read_bytes()
    OUT.mkdir();PARENT_REGISTRY.write_bytes(REGISTRY.read_bytes());CANDIDATE.write_bytes(output)
    reopened=NdsImage.open(CANDIDATE);assert reopened.read_file('/__arm9__.bin')==arm
    assert bytes(reopened.rom.save())==output
    make_xdelta(CLEAN,CANDIDATE,PATCH);apply_xdelta(CLEAN,PATCH,RECONSTRUCTED)
    assert RECONSTRUCTED.read_bytes()==output
    save(CONFIG,dict(format='dk4-market-goods-info-terminator-release-v1',target_locale='en-US',
        parent_ROM=parent['candidate'],parent_ROM_sha256=parent['candidate_sha256'],
        parent_release=str(PARENT),parent_release_sha256=digest(PARENT),
        source_ARM9_sha256=sha(original),target_ARM9_sha256=sha(arm),
        pointer_fields=list(FIELDS),new_declared_literal_address=NEW_FORMAT,new_declared_literal_hex=PAYLOAD.hex(),
        original_code_andall_existing_autoload_payloads_preserved=True,whole_parent_inverse_exact=True,
        native_verification=str(native_path),native_verification_sha256=digest(native_path),
        preparation=str(prep_path),preparation_sha256=digest(prep_path),
        required_driver=__file__,required_driver_sha256=digest(__file__),
        right_bound_configuration=prior_profile['ascii_glyph_right_bounds'],new_editorial_records=0,new_credit=0,
        dependencies={str(p):digest(p) for p in [Path('dk4tool/patch/market_goods_info_terminator_v1.py'),prep_path,native_path]}))
    save(STAGED,dict(profile=PROFILE,candidate=str(CANDIDATE),candidate_sha256=digest(CANDIDATE),
        patch=str(PATCH),patch_sha256=digest(PATCH),clean_input_sha256=digest(CLEAN),
        exact_clean_reconstruction=str(RECONSTRUCTED),reconstructed_sha256=digest(RECONSTRUCTED),clean_input_patch_byte_exact=True,
        parent=parent['candidate'],parent_sha256=parent['candidate_sha256'],canonical_base=parent['canonical_base'],canonical_sha256=parent['canonical_sha256'],
        predecessor_profile=parent['profile'],predecessor_release_sha256=digest(PARENT),predecessor_manifest_sha256=parent['manifest_sha256'],
        predecessor_registry_sha256=digest(PARENT_REGISTRY),release_config=str(CONFIG),release_config_sha256=digest(CONFIG),
        target_ARM9_sha256=sha(arm),only_ARM9_changed=True,whole_parent_inverse_exact=True,
        all_predecessor_stage_dependencies_preserved=True,all_709_entries_114_accepted_layers_andASCII_right_bound_preserved=True,
        all_other_files_components_graphics_names_scripts_andtrade_logic_preserved=True,
        final_story_percent_contract=percent,all_four_story_archives_rechecked=True,format_pointer_proof=proof,
        own_registered_startup_pending=True,market_gameplay_pending=True,experimental_not_promoted=True,new_credit=0))
    assert digest(REGISTRY)==parent['registry_sha256']
    print('Stagedcurrent cumulative market fix;exact clean-input patch andwhole inverse pass. Startup/market checks pending.')

def register():
    assert not RELEASE.exists() and not MANIFEST.exists()
    parent,staged,startup,gameplay,getters=map(load,[PARENT,STAGED,STARTUP,GAMEPLAY,GETTERS])
    assert digest(PARENT)==staged['predecessor_release_sha256']
    assert digest(CONFIG)==staged['release_config_sha256']
    assert digest(CANDIDATE)==staged['candidate_sha256']==startup['candidate_sha256']==gameplay['candidate_sha256']
    assert not staged['own_registered_startup_pending'] and not staged['market_gameplay_pending']
    assert startup['cold_boot'] and not startup['savestate'] and startup['actual_captain_getter']==0
    assert startup['new_declared_format_bytes_andpointer_fields_loaded_exact']
    assert gameplay['actual_Local_andCargo_market_screens_verified'] and gameplay['no_machine_code_suffix_oruntranslated_garbage']
    assert getters['both_name_getters_exact_for_all12_protected_actors']
    assert digest(REGISTRY)==digest(PARENT_REGISTRY)==staged['predecessor_registry_sha256']
    assert digest(PATCH)==staged['patch_sha256'] and RECONSTRUCTED.read_bytes()==CANDIDATE.read_bytes()
    before=REGISTRY.read_bytes();registry=load(REGISTRY);old=load(parent['manifest'])
    assert digest(parent['manifest'])==staged['predecessor_manifest_sha256']
    assert PROFILE not in registry['profiles'] and len(registry['accepted_layers'])==114
    prior=registry['profiles'][parent['profile']];profile=deepcopy(prior)
    predecessor=dict(profile=parent['profile'],candidate=parent['candidate'],candidate_sha256=parent['candidate_sha256'],
        manifest=parent['manifest'],manifest_sha256=parent['manifest_sha256'],registry=str(PARENT_REGISTRY),registry_sha256=digest(PARENT_REGISTRY),
        verified_Maria301_complete_registered_output_reused=True)
    profile.update(verified_maria301_predecessor=predecessor,market_goods_info_terminator=str(CONFIG),
        note='Experimental cumulative correction for Goods Info printf NUL overwritten by the town-stock capture routine; existing code andall dialogue retained.')
    assert profile['ascii_glyph_right_bounds']==prior['ascii_glyph_right_bounds']
    registry['profiles'][PROFILE]=profile
    pending=REGISTRY.with_name('release_stack.market_goods_info.pending.json');assert not pending.exists();save(pending,registry)
    manifest=deepcopy(old);manifest.update(profile=PROFILE,candidate_rom=str(CANDIDATE),candidate_sha256=staged['candidate_sha256'],release_stack_sha256=digest(pending))
    manifest['batches'].append(str(CONFIG))
    manifest['changed_records'].setdefault('/__arm9__.bin',[]).extend(['MARKET_GOODS_INFO_LOCAL_PRINTF_TERMINATOR','MARKET_GOODS_INFO_CARGO_PRINTF_TERMINATOR'])
    manifest['checks'][CHECK]=True
    manifest.setdefault('relocations',{}).setdefault('/__arm9__.bin',{})['market-goods-info-terminated-format']=staged['format_pointer_proof']
    manifest['market_goods_info_terminated_format_pipeline']=dict(driver=__file__,driver_sha256=digest(__file__),
        predecessor=predecessor,config=str(CONFIG),config_sha256=digest(CONFIG),
        original_canonical_prefix_verified_andreused=True,all_prior_stage_contracts_preserved=True,
        startup=str(STARTUP),startup_sha256=digest(STARTUP),gameplay=str(GAMEPLAY),gameplay_sha256=digest(GAMEPLAY))
    assert manifest['batches'][:709]==old['batches'] and len(manifest['batches'])==710
    assert len(manifest['checks'])==45 and all(manifest['checks'].values())
    assert REGISTRY.read_bytes()==before;save(MANIFEST,manifest);os.replace(pending,REGISTRY)
    registered=load(REGISTRY);old_registry=load(PARENT_REGISTRY)
    assert set(registered['profiles'])==set(old_registry['profiles'])|{PROFILE}
    assert all(registered['profiles'][k]==v for k,v in old_registry['profiles'].items())
    assert all(registered[k]==v for k,v in old_registry.items() if k!='profiles')
    assert digest(REGISTRY)==manifest['release_stack_sha256']
    save(RELEASE,{**staged,'manifest':str(MANIFEST),'manifest_sha256':digest(MANIFEST),registry_sha256=digest(REGISTRY),
        predecessor=predecessor,complete_stack_entries=710,registered_manifest_entries=710,passing_release_checks=45,accepted_layers=114,
        own_registered_startup=str(STARTUP),own_registered_startup_sha256=digest(STARTUP),
        own_registered_name_getters=str(GETTERS),own_registered_name_getters_sha256=digest(GETTERS),
        market_gameplay=str(GAMEPLAY),market_gameplay_sha256=digest(GAMEPLAY),
        changed_internal_files=['/__arm9__.bin'],changed_components=[],new_contextual_records=0,prose_revisions=0,justified_retentions=0,
        all_nine_registered_final_stages_preserved=True,owned_Francisca_name_field_verified=True,
        owned_Plett_Jacob_surnames_verified=True,owned_Zaganos_surname_verified=True,
        owned_Hodram_residual_surnames_verified=True,owned_Rafael_residual_middle_fields_verified=True,
        full_goal_complete=False})
    print('Registered710-entry/45-check market fix;main andall prior profiles unchanged.')

if __name__=='__main__':
    if sys.argv[1:]==['--register']:register()
    else:assert not sys.argv[1:];stage()
