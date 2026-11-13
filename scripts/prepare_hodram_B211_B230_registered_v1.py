"""Qualify the sealed Hodram transaction over the verified cumulative release."""
from pathlib import Path
from dk4tool.patch.hodram_b211_b230_release_v1 import plan_release
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.audit_story_glyph_consistency import load,save
from scripts.build_registered_rafael5186_v1 import RELEASE as PARENT,REGISTRY,CLEAN
from scripts.finalize_hodram_B211_B230_research_v1 import REBUILT,STORED,LOOKUP,LOADERS,NATIVE,FINAL,FINAL_NAMES
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest
from scripts.review_hodram_B221_B230_contextual_v1 import ROOT

ARCHIVE='/data/SC1.DK4';ARM='/__arm9__.bin'
READY=ROOT/'research_final_v3/research_completion.json'
OUT=ROOT/'registered_preparation_v1'
CONFIG=Path('translations/hodram_B211_B230_editorial_release_v1.json')
QUALIFICATION=OUT/'qualification.json'

def main():
    assert not OUT.exists() and not CONFIG.exists()
    parent,ready,rebuilt,registry=map(load,(PARENT,READY,REBUILT,REGISTRY))
    assert digest(REGISTRY)==parent['registry_sha256']
    assert parent['clean_input_patch_byte_exact'] and not parent['own_registered_startup_pending']
    assert parent['all_predecessor_stage_dependencies_preserved'] and parent['owned_Rafael_residual_middle_fields_verified']
    assert (parent['registered_manifest_entries'],parent['accepted_layers'],parent['passing_release_checks'])==(700,114,35)
    profile=registry['profiles'][parent['profile']]
    assert profile['ascii_glyph_right_bounds']=='translations\\ascii_bounds_Rafael3514_dialogue_v1.json'
    baseline,candidate=Path(parent['canonical_base']),Path(parent['candidate'])
    assert digest(candidate)==parent['candidate_sha256']==rebuilt['parent_sha256']
    assert digest(baseline)==parent['canonical_sha256'] and digest(CLEAN)==parent['clean_input_sha256']
    assert digest(parent['manifest'])==parent['manifest_sha256']
    assert ready['all_individual_five_gates_pass'] and ready['registered_integration_pending']
    for p,h in ready['evidence'].items():assert digest(p)==h
    scope=dict(record_count=277,speech_count=270,typed_choice_count=7,menu_count=3,style_count=29,
        scoped_name_count=23,native_pages=284,relative_cases=150,FE_count=4,actual_frames=23441,
        actual_runs=1,actual_speeches=65,actual_body_pages=74,offline_speeches=205)
    evidence=dict(manuscript=str(FINAL),plan=ready['plan'],reconstruction=str(REBUILT),compiled_native=str(NATIVE),
        stored_native=str(STORED),stored_lookup=str(LOOKUP),loaders=str(LOADERS),
        visual_review=str(ROOT/'research_final_v3/complete_visual_approval.json'),actual=str(ROOT/'research_final_v3/actual_review.json'),
        scoped_names=str(FINAL_NAMES),typed_menu=rebuilt['menu'],native_styles=rebuilt['styles'],research_completion=str(READY))
    image=NdsImage.open(candidate);arm_hash=sha(image.read_file(ARM))
    dependencies={str(p):digest(p) for p in (*evidence.values(),PARENT,parent['manifest'],
        Path('dk4tool/patch/hodram_b211_b230_release_v1.py'),Path(__file__))}
    config=dict(format='dk4-reviewed-hodram-b211-b230-release-v1',**scope,**evidence,
        clean_ROM=str(CLEAN),clean_ROM_sha256=digest(CLEAN),canonical_ROM_sha256=digest(baseline),
        parent_ROM=str(candidate),parent_ROM_sha256=digest(candidate),pre_runtime_ARM9_sha256=arm_hash,
        target_ROM_sha256=rebuilt['research_ROM_sha256'],final_dependency_ROM=str(candidate),
        final_dependency_ROM_sha256=digest(candidate),final_runtime_ARM9_sha256=arm_hash,
        reviewed_blocks=rebuilt['reviewed_blocks'],blocks=rebuilt['changed_blocks'],
        right_bound_configuration=profile['ascii_glyph_right_bounds'],dependencies=dependencies)
    OUT.mkdir();draft=OUT/'dialogue_candidate_config.json';save(draft,config)
    proposed,proof=plan_release(image,NdsImage.open(baseline),draft)
    assembled=NdsImage.open(rebuilt['research_ROM'])
    assert proposed.save()==assembled.rom.save() and len(proof['changed_records'])==277
    assert [p for _,p,v in image.iter_files() if assembled.read_file(p)!=v]==[ARCHIVE]
    assert all(assembled.read_file(p)==v for p,v in image.iter_components())
    assembled.replace_file(ARCHIVE,image.read_file(ARCHIVE));assert bytes(assembled.rom.save())==candidate.read_bytes()
    save(CONFIG,config)
    save(QUALIFICATION,dict(config=str(CONFIG),config_sha256=digest(CONFIG),predecessor_release=str(PARENT),
        predecessor_release_sha256=digest(PARENT),registry_sha256=digest(REGISTRY),predecessor_profile=parent['profile'],
        predecessor_manifest_sha256=parent['manifest_sha256'],target_ROM_sha256=rebuilt['research_ROM_sha256'],target_ARM9_sha256=arm_hash,
        exact_277_stored_bindings_verified=True,changed_blocks=rebuilt['changed_blocks'],complete_parent_inverse_exact=True,
        only_SC1_changes=True,all_predecessor_stage_dependencies_preserved=True,registration_and_candidate_own_startup_pending=True,new_credit=0))
    print('Qualified 277 Hodram records over Rafael5186. Whole parent inverse, retained runtime and registered bounds pass.')

if __name__=='__main__':main()
