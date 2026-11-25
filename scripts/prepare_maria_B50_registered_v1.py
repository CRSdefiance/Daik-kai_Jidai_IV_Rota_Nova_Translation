"""Freeze the source-owned B50 FE transaction over the exact registered Maria270 prefix."""
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.maria_B50_release_v1 import plan_release
from scripts.audit_story_glyph_consistency import load,save
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest

ROOT=Path('work/Maria_B50_FE_resolution_20261109_v3')
OUT=ROOT/'registered_preparation_v1'
FINAL=Path('translations/maria_B50_final_review_v1.json')
CONFIG=Path('translations/maria_B50_editorial_release_v1.json')
QUALIFICATION=OUT/'qualification.json'
PARENT=Path('work/maria270_release_v1/registered_release_verification.json')
REGISTRY=Path('translations/release_stack.json');CLEAN=Path('work/clean.nds')
ARM,ARCHIVE='/__arm9__.bin','/data/SC3.DK4'

def main():
    assert not OUT.exists() and not CONFIG.exists()
    parent=load(PARENT);ready_path=ROOT/'research_completion_v1.json';ready=load(ready_path)
    rebuilt_path=ROOT/'reconstruction_v1/reconstruction.json';rebuilt=load(rebuilt_path)
    assert (parent['registered_manifest_entries'],parent['accepted_layers'],parent['passing_release_checks'])==(711,114,46)
    assert not parent['own_registered_startup_pending'] and parent['clean_input_patch_byte_exact']
    assert parent['all_predecessor_stage_dependencies_preserved'] and parent['registered_market_format_andboth_data_pointers_preserved']
    assert digest(REGISTRY)==parent['registry_sha256'] and digest(parent['candidate'])==parent['candidate_sha256']==rebuilt['parent_sha256']
    assert digest(parent['manifest'])==parent['manifest_sha256'] and digest(parent['canonical_base'])==parent['canonical_sha256']
    assert digest(CLEAN)==parent['clean_input_sha256'] and digest(FINAL)==ready['manuscript_sha256'] and ready['manuscript']==str(FINAL)
    for p,h in ready['evidence'].items():assert digest(p)==h
    evidence=dict(manuscript=str(FINAL),plan=str(ROOT/'source16_release_plans.json'),reconstruction=str(rebuilt_path),
        compiled_native=str(ROOT/'final_native_v1.json'),stored_native=str(ROOT/'stored_v1/stored_native_verification.json'),
        stored_lookup=str(ROOT/'catalogue_v1/all17_stored_effective_body_bindings.json'),loaders=str(ROOT/'loaders_v1/verification.json'),
        visual_review=str(ROOT/'offline_approval_v1.json'),actual=str(ROOT/'gameplay_review_v1.json'),
        scoped_names='translations/maria_B37_B49_scoped_names_final_v1.json')
    OUT.mkdir();sealed=OUT/'sealed_research_inputs.json'
    save(sealed,dict(research_completion=str(ready_path),research_completion_sha256=digest(ready_path),
        inputs={k:dict(path=v,sha256=digest(v)) for k,v in evidence.items()},new_credit=0))
    profile=load(REGISTRY)['profiles'][parent['profile']]
    extra=dict(research_completion=str(ready_path),sealed_inputs=str(sealed))
    dependencies=[*evidence.values(),*extra.values(),PARENT,parent['manifest'],ROOT/'display_run_v1/run_plan.json',
        Path('dk4tool/patch/maria_B50_release_v1.py'),Path('dk4tool/script/reviewed_FE_pagination_v1.py'),
        Path('dk4tool/script/reviewed_scene_rebuild_v3.py'),Path(__file__)]
    conf=dict(format='dk4-reviewed-maria-B50-FE-release-v1',record_count=16,speech_count=16,native_commands=17,native_pages=17,
        FE_count=12,FE_owner_ID='DK4_MES_B50_R0043',typed_choice_count=0,style_count=0,scoped_name_IDs=[3,10,28,74],
        captain=3,actual_frames=13001,**evidence,**extra,
        clean_ROM=str(CLEAN),clean_ROM_sha256=digest(CLEAN),canonical_ROM_sha256=parent['canonical_sha256'],
        parent_ROM=parent['candidate'],parent_ROM_sha256=parent['candidate_sha256'],pre_runtime_ARM9_sha256=parent['target_ARM9_sha256'],
        target_ROM_sha256=rebuilt['research_ROM_sha256'],reviewed_blocks=[50],blocks=[50],
        right_bound_configuration=profile['ascii_glyph_right_bounds'],
        source25_multiarchive_guard=profile['source25_multiarchive_guard'],dependencies={str(p):digest(p) for p in dependencies})
    draft=OUT/'candidate_config.json';save(draft,conf)
    result,proof=plan_release(NdsImage.open(parent['candidate']),NdsImage.open(parent['canonical_base']),draft)
    assert bytes(result.save())==Path(rebuilt['research_ROM']).read_bytes() and len(proof['changed_records'])==16
    save(CONFIG,conf)
    save(QUALIFICATION,dict(config=str(CONFIG),config_sha256=digest(CONFIG),predecessor_release=str(PARENT),
        predecessor_release_sha256=digest(PARENT),registry_sha256=digest(REGISTRY),predecessor_profile=parent['profile'],
        predecessor_manifest_sha256=parent['manifest_sha256'],target_ROM_sha256=rebuilt['research_ROM_sha256'],
        target_ARM9_sha256=parent['target_ARM9_sha256'],changed_blocks=[50],only_SC3_changes=True,
        source_records=16,native_panels=17,exact_source_FE_continuations=1,complete_parent_inverse_exact=True,
        all_predecessor_stage_dependencies_preserved=True,registration_and_candidate_own_startup_pending=True,new_credit=0))
    print('Qualified16 source reviews/17 panels over711-entry Maria270;full source-owned FE transaction andwhole inverse pass.')
if __name__=='__main__':main()
