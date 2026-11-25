"""Freeze330 completed reviews over the exact715-entry registered predecessor."""
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.maria330_release_v1 import plan_release
from scripts.meaning_maria330_clean_v1 import ROOT
from scripts.audit_story_glyph_consistency import load,save
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest

OUT=ROOT/'registered_preparation_v2'
FINAL=Path('translations/maria_B96_B124_final_review_v1.json')
CONFIG=Path('translations/maria330_editorial_release_v1.json')
QUALIFICATION=OUT/'qualification.json'
PARENT=Path('work/maria328_release_v1/registered_release_verification.json')
REGISTRY=Path('translations/release_stack.json'); CLEAN=Path('work/clean.nds')
ARM,ARCHIVE='/__arm9__.bin','/data/SC3.DK4'

def main():
    assert not OUT.exists() and not CONFIG.exists()
    parent=load(PARENT); ready_path=ROOT/'research_completion_v1/research_completion.json'; ready=load(ready_path)
    rebuilt_path=ROOT/'reconstruction_v2/reconstruction.json'; rebuilt=load(rebuilt_path)
    assert (parent['registered_manifest_entries'],parent['accepted_layers'],parent['passing_release_checks'])==(715,114,50)
    assert parent['clean_input_patch_byte_exact'] and not parent['own_registered_startup_pending'] and parent['all_predecessor_stage_dependencies_preserved']
    assert parent['registered_market_format_andboth_data_pointers_preserved']
    assert digest(REGISTRY)==parent['registry_sha256'] and digest(parent['candidate'])==parent['candidate_sha256']==rebuilt['parent_sha256']
    assert digest(parent['manifest'])==parent['manifest_sha256'] and digest(parent['canonical_base'])==parent['canonical_sha256']
    assert digest(CLEAN)==parent['clean_input_sha256'] and digest(FINAL)==ready['manuscript_sha256']
    for p,h in ready['evidence'].items():assert digest(p)==h
    evidence=dict(manuscript=str(FINAL),plan=ready['source_release_plans'],reconstruction=str(rebuilt_path),compiled_native=rebuilt['native'],
        stored_native=str(ROOT/'stored_v1/stored_native_verification.json'),stored_lookup=str(ROOT/'stored_catalogue_all_v1/all330_stored_effective_body_bindings.json'),
        loaders=str(ROOT/'loaders_v1/verification.json'),visual_review=str(ROOT/'offline_display_approval_v1.json'),
        actual=str(ROOT/'gameplay_review_v1.json'),scoped_names=ready['names'],typed_menu=rebuilt['menu'],native_styles=rebuilt['styles'])
    OUT.mkdir(); sealed=OUT/'sealed_research_inputs.json'
    save(sealed,dict(research_completion=str(ready_path),research_completion_sha256=digest(ready_path),inputs={k:dict(path=v,sha256=digest(v)) for k,v in evidence.items()},new_credit=0))
    profile=load(REGISTRY)['profiles'][parent['profile']]; extra=dict(research_completion=str(ready_path),sealed_inputs=str(sealed))
    dependencies=[*evidence.values(),*extra.values(),PARENT,parent['manifest'],ROOT/'display_run_menu0_v1/run_plan.json',ROOT/'display_run_menu1_v1/run_plan.json',
        Path('dk4tool/patch/maria330_release_v1.py'),Path('dk4tool/patch/maria328_release_v1.py'),Path('dk4tool/patch/rafael_story_b81_b84_release_v1.py'),
        Path('dk4tool/patch/reviewed_scene_batch_v5.py'),Path('dk4tool/patch/maria301_release_v2.py'),Path('dk4tool/script/reviewed_FE_pagination_v1.py'),Path('dk4tool/script/reviewed_scene_rebuild_v3.py'),Path(__file__)]
    conf=dict(format='dk4-reviewed-maria330-release-v1',record_count=330,speech_count=328,ordinary_count=293,style_count=35,typed_choice_count=2,menu_count=1,
        scoped_name_count=26,native_pages=338,relative_cases=380,FE_count=8,FE_owner_IDs=['DK4_MES_B116_R0041','DK4_MES_B116_R0051'],captain=3,actual_frames=34402,**evidence,**extra,
        clean_ROM=str(CLEAN),clean_ROM_sha256=digest(CLEAN),canonical_ROM_sha256=parent['canonical_sha256'],parent_ROM=parent['candidate'],parent_ROM_sha256=parent['candidate_sha256'],
        pre_runtime_ARM9_sha256=parent['target_ARM9_sha256'],target_ROM_sha256=rebuilt['research_ROM_sha256'],reviewed_blocks=rebuilt['reviewed_blocks'],blocks=rebuilt['changed_blocks'],
        right_bound_configuration=profile['ascii_glyph_right_bounds'],source25_multiarchive_guard=profile['source25_multiarchive_guard'],dependencies={str(p):digest(p) for p in dependencies})
    draft=OUT/'candidate_config.json'; save(draft,conf)
    result,proof=plan_release(NdsImage.open(parent['candidate']),NdsImage.open(parent['canonical_base']),draft)
    assert bytes(result.save())==Path(rebuilt['research_ROM']).read_bytes() and len(proof['changed_records'])==330
    save(CONFIG,conf)
    save(QUALIFICATION,dict(config=str(CONFIG),config_sha256=digest(CONFIG),predecessor_release=str(PARENT),predecessor_release_sha256=digest(PARENT),registry_sha256=digest(REGISTRY),
        predecessor_profile=parent['profile'],predecessor_manifest_sha256=parent['manifest_sha256'],target_ROM_sha256=rebuilt['research_ROM_sha256'],
        target_ARM9_sha256=parent['target_ARM9_sha256'],changed_blocks=rebuilt['changed_blocks'],source_records=330,physical_body_candidates=330,native_pages=338,
        exact_source_FE_continuations=2,only_SC3_changes=True,complete_parent_inverse_exact=True,all_predecessor_stage_dependencies_preserved=True,
        registration_and_candidate_own_startup_pending=True,new_credit=0))
    print('Qualified330 reviews over715-entry Maria328; mixed/FE transaction andwhole inverse pass.')

if __name__=='__main__':main()
