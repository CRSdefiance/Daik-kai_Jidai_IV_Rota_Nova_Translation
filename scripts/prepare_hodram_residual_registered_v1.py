"""Freeze394 reviewed records and qualify their exact cumulative SC1 transaction."""
from copy import deepcopy
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.hodram_residual_release_v1 import plan_release
from scripts.audit_story_glyph_consistency import load,save
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest
from dk4tool.patch.grand_race_menu_release import sha

ROOT=Path('work/Hodram_B0_B41_clean_20261107')
OUT=ROOT/'registered_preparation_v1'
CONFIG=Path('translations/hodram_residual_editorial_release_v1.json')
QUALIFICATION=OUT/'qualification.json'
FINAL=Path('translations/hodram_B0_B41_registered_review_v1.json')
PARENT=Path('work/hodram_B311_B324_release_v1/registered_release_verification.json')
READY=ROOT/'research_final_v2/research_completion.json'
REBUILT=ROOT/'stored_reconstruction_v3/reconstruction.json'
REGISTRY=Path('translations/release_stack.json');CLEAN=Path('work/clean.nds')
ARCHIVE='/data/SC1.DK4';ARM='/__arm9__.bin'

def main():
    assert not OUT.exists() and not CONFIG.exists() and not FINAL.exists()
    parent,ready,rebuilt,registry=map(load,(PARENT,READY,REBUILT,REGISTRY))
    assert digest(REGISTRY)==parent['registry_sha256']
    assert (parent['registered_manifest_entries'],parent['accepted_layers'],parent['passing_release_checks'])==(706,114,41)
    assert parent['clean_input_patch_byte_exact'] and not parent['own_registered_startup_pending'] and parent['all_predecessor_stage_dependencies_preserved']
    assert digest(parent['candidate'])==parent['candidate_sha256']==rebuilt['parent_sha256']
    assert digest(parent['canonical_base'])==parent['canonical_sha256'] and digest(CLEAN)==parent['clean_input_sha256']
    assert digest(parent['manifest'])==parent['manifest_sha256']
    for p,h in ready['evidence'].items():assert digest(p)==h
    doc=deepcopy(load(ready['manuscript']));assert digest(ready['manuscript'])==ready['manuscript_sha256']
    for row in doc['records']:row['finding']=row['editorial_finding']
    doc.update(registered_schema_aliases_only=True,source_review=ready['manuscript'],source_review_sha256=ready['manuscript_sha256'])
    OUT.mkdir();save(FINAL,doc)
    plan=load(ROOT/'research_final_v2/release_plans.json');plan.update(manuscript=str(FINAL),manuscript_sha256=digest(FINAL))
    plans=OUT/'release_plans.json';save(plans,plan)
    evidence=dict(manuscript=str(FINAL),plan=str(plans),reconstruction=str(REBUILT),
        compiled_native=rebuilt['native'],stored_native=str(ROOT/'stored_v2/stored_native_verification.json'),
        stored_lookup=str(ROOT/'stored_catalogue_all_v2/all388_stored_effective_body_bindings.json'),loaders=str(ROOT/'loaders_v2/verification.json'),
        visual_review=str(ROOT/'offline_visual_approval_v2.json'),actual=str(ROOT/'gameplay_review_v1.json'),
        scoped_names='translations/hodram_B0_B41_scoped_names_final_v1.json',typed_menu=rebuilt['menu'],native_styles=rebuilt['styles'])
    sealed=OUT/'sealed_research_inputs.json';save(sealed,dict(research_completion=str(READY),research_completion_sha256=digest(READY),
        inputs={key:dict(path=value,sha256=digest(value)) for key,value in evidence.items()},new_credit=0))
    extra=dict(research_completion=str(READY),sealed_inputs=str(sealed),opaque_pixel_model=str(ROOT/'opaque_pixel_model_qualification_v1.json'),
        capacity_proof='work/Hodram_B301_B310_clean_20261107/native_QA_capacity_v1.json')
    profile=registry['profiles'][parent['profile']];image=NdsImage.open(parent['candidate']);arm_hash=sha(image.read_file(ARM))
    config=dict(format='dk4-reviewed-hodram-residual-release-v1',record_count=394,speech_count=388,typed_choice_count=6,menu_count=3,style_count=47,
        scoped_name_count=42,native_pages=389,relative_cases=685,FE_count=16,actual_frames=57363,actual_runs=3,actual_speeches=169,actual_body_pages=170,offline_speeches=219,
        **evidence,**extra,clean_ROM=str(CLEAN),clean_ROM_sha256=digest(CLEAN),canonical_ROM_sha256=parent['canonical_sha256'],
        parent_ROM=parent['candidate'],parent_ROM_sha256=parent['candidate_sha256'],pre_runtime_ARM9_sha256=arm_hash,
        target_ROM_sha256=rebuilt['research_ROM_sha256'],final_dependency_ROM=parent['candidate'],final_dependency_ROM_sha256=parent['candidate_sha256'],
        final_runtime_ARM9_sha256=arm_hash,reviewed_blocks=rebuilt['reviewed_blocks'],blocks=rebuilt['changed_blocks'],right_bound_configuration=profile['ascii_glyph_right_bounds'],
        dependencies={str(p):digest(p) for p in [*evidence.values(),*extra.values(),PARENT,parent['manifest'],Path(__file__),Path('dk4tool/patch/hodram_residual_release_v1.py')]})
    draft=OUT/'dialogue_candidate_config.json';save(draft,config)
    proposed,proof=plan_release(image,NdsImage.open(parent['canonical_base']),draft)
    assert proposed.save()==NdsImage.open(rebuilt['research_ROM']).rom.save() and len(proof['changed_records'])==394
    save(CONFIG,config)
    save(QUALIFICATION,dict(config=str(CONFIG),config_sha256=digest(CONFIG),predecessor_release=str(PARENT),predecessor_release_sha256=digest(PARENT),
        registry_sha256=digest(REGISTRY),predecessor_profile=parent['profile'],predecessor_manifest_sha256=parent['manifest_sha256'],
        target_ROM_sha256=rebuilt['research_ROM_sha256'],target_ARM9_sha256=arm_hash,exact_394_stored_bindings_verified=True,
        changed_blocks=rebuilt['changed_blocks'],complete_parent_inverse_exact=True,only_SC1_changes=True,
        all_predecessor_stage_dependencies_preserved=True,registration_and_candidate_own_startup_pending=True,new_credit=0))
    print('Qualified394 residual records over the706-entry cumulative parent; complete original SC1 transaction/inverse passes.')

if __name__=='__main__':main()
