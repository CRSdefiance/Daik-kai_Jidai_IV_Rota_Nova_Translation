"""Freeze the completed Maria research and qualify its cumulative SC3 append."""
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.maria301_release_v1 import plan_release
from dk4tool.patch.grand_race_menu_release import sha
from scripts.audit_story_glyph_consistency import load,save
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest

ROOT = Path('work/Maria_B0_B32_clean_20261109')
OUT = ROOT/'registered_preparation_v1'
FINAL = Path('translations/maria_B0_B32_final_review_v1.json')
CONFIG = Path('translations/maria301_editorial_release_v1.json')
QUALIFICATION = OUT/'qualification.json'
PARENT = Path('work/hodram_residual_release_v1/registered_release_verification.json')
REGISTRY = Path('translations/release_stack.json')
CLEAN = Path('work/clean.nds')
ARM,ARCHIVE = '/__arm9__.bin','/data/SC3.DK4'


def main():
    assert not OUT.exists() and not CONFIG.exists()
    parent = load(PARENT);ready_path = ROOT/'research_final_v1/research_completion.json';ready = load(ready_path)
    rebuilt_path = ROOT/'stored_reconstruction_v1/reconstruction.json';rebuilt = load(rebuilt_path)
    assert digest(REGISTRY) == parent['registry_sha256']
    assert (parent['registered_manifest_entries'],parent['accepted_layers'],parent['passing_release_checks']) == (708,114,43)
    assert parent['clean_input_patch_byte_exact'] and not parent['own_registered_startup_pending'] and parent['all_predecessor_stage_dependencies_preserved']
    assert digest(parent['candidate']) == parent['candidate_sha256'] == rebuilt['parent_sha256']
    assert digest(parent['manifest']) == parent['manifest_sha256']
    assert digest(parent['canonical_base']) == parent['canonical_sha256'] and digest(CLEAN) == parent['clean_input_sha256']
    for p,h in ready['evidence'].items():assert digest(p) == h
    assert digest(FINAL) == ready['manuscript_sha256'] and ready['manuscript'] == str(FINAL)
    evidence = dict(manuscript=str(FINAL),plan=str(ROOT/'research_final_v1/release_plans.json'),reconstruction=str(rebuilt_path),
        compiled_native=rebuilt['native'],stored_native=str(ROOT/'stored_v1/stored_native_verification.json'),
        stored_lookup=str(ROOT/'stored_catalogue_all_v1/all299_stored_effective_body_bindings.json'),
        loaders=str(ROOT/'loaders_v1/verification.json'),visual_review=str(ROOT/'offline_display_approval_v1.json'),
        actual=str(ROOT/'gameplay_review_v1.json'),scoped_names='translations/maria_B0_B32_scoped_names_final_v1.json',
        typed_menu=rebuilt['menu'],native_styles=rebuilt['styles'])
    OUT.mkdir();sealed = OUT/'sealed_research_inputs.json'
    save(sealed,dict(research_completion=str(ready_path),research_completion_sha256=digest(ready_path),
        inputs={k:dict(path=v,sha256=digest(v)) for k,v in evidence.items()},new_credit=0))
    image = NdsImage.open(parent['candidate']);arm_hash = sha(image.read_file(ARM))
    profile = load(REGISTRY)['profiles'][parent['profile']]
    extra = dict(research_completion=str(ready_path),sealed_inputs=str(sealed))
    dependencies = [*evidence.values(),*extra.values(),PARENT,parent['manifest'],Path(__file__),Path('dk4tool/patch/maria301_release_v1.py')]
    dependencies += [r['run_plan'] for r in load(evidence['actual'])['runs']]
    config = dict(format='dk4-reviewed-maria301-release-v1',record_count=301,speech_count=299,typed_choice_count=2,menu_count=1,
        style_count=7,scoped_name_count=36,native_pages=303,relative_cases=635,FE_count=0,captain=3,actual_frames=42683,
        **evidence,**extra,clean_ROM=str(CLEAN),clean_ROM_sha256=digest(CLEAN),canonical_ROM_sha256=parent['canonical_sha256'],
        parent_ROM=parent['candidate'],parent_ROM_sha256=parent['candidate_sha256'],pre_runtime_ARM9_sha256=arm_hash,
        target_ROM_sha256=rebuilt['research_ROM_sha256'],final_dependency_ROM=parent['candidate'],final_dependency_ROM_sha256=parent['candidate_sha256'],
        final_runtime_ARM9_sha256=arm_hash,reviewed_blocks=rebuilt['reviewed_blocks'],blocks=rebuilt['changed_blocks'],
        right_bound_configuration=profile['ascii_glyph_right_bounds'],dependencies={str(p):digest(p) for p in dependencies})
    draft = OUT/'candidate_config.json';save(draft,config)
    proposed,proof = plan_release(image,NdsImage.open(parent['canonical_base']),draft)
    assert bytes(proposed.save()) == Path(rebuilt['research_ROM']).read_bytes() and len(proof['changed_records']) == 301
    save(CONFIG,config)
    save(QUALIFICATION,dict(config=str(CONFIG),config_sha256=digest(CONFIG),predecessor_release=str(PARENT),
        predecessor_release_sha256=digest(PARENT),registry_sha256=digest(REGISTRY),predecessor_profile=parent['profile'],
        predecessor_manifest_sha256=parent['manifest_sha256'],target_ROM_sha256=rebuilt['research_ROM_sha256'],target_ARM9_sha256=arm_hash,
        changed_blocks=rebuilt['changed_blocks'],only_SC3_changes=True,complete_parent_inverse_exact=True,
        all_predecessor_stage_dependencies_preserved=True,registration_and_candidate_own_startup_pending=True,new_credit=0))
    print('Qualified301 reviewed records over the708-entry cumulative parent; complete SC3 transaction andinverse pass.')


if __name__ == '__main__':main()
