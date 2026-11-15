"""Qualify the dialogue-only successor before creating the registered test candidate."""
from pathlib import Path

from dk4tool.patch.rafael_story_b301_b320_release_v1 import plan_release
from dk4tool.rom.nds import NdsImage
from scripts import finalize_rafael_B301_B320_research_v1 as reviewed
from scripts.audit_story_glyph_consistency import load, save
from scripts.build_registered_rafael3894_v1 import ARCHIVE, ARM, CLEAN, REGISTRY, RELEASE as PARENT
from scripts.refine_rafael_B301_B320_plan_v1 import ROOT, digest, sha


OUT = ROOT / 'registered_preparation_v1'
CONFIG = Path('translations/rafael_B301_B320_editorial_release_v1.json')
QUALIFICATION = OUT / 'qualification.json'


def main():
    assert not OUT.exists() and not CONFIG.exists()
    parent, ready, rebuilt, registry = map(load, (PARENT, reviewed.READY, reviewed.REBUILT, REGISTRY))
    assert digest(REGISTRY) == parent['registry_sha256']
    assert parent['owned_Zaganos_surname_verified'] and parent['all_predecessor_stage_dependencies_preserved']
    assert parent['clean_input_patch_byte_exact'] and not parent['own_registered_startup_pending']
    assert (parent['registered_manifest_entries'], parent['accepted_layers'], parent['passing_release_checks']) == (696, 114, 31)
    profile = registry['profiles'][parent['profile']]
    assert {'owned_Zaganos_surname', 'owned_Plett_Jacob_surnames', 'ascii_glyph_right_bounds'} <= profile.keys()
    baseline, candidate = Path(parent['canonical_base']), Path(parent['candidate'])
    assert digest(candidate) == parent['candidate_sha256'] == rebuilt['parent_sha256']
    assert digest(baseline) == parent['canonical_sha256'] and digest(CLEAN) == parent['clean_input_sha256']
    assert digest(parent['manifest']) == parent['manifest_sha256']
    assert ready['all_individual_five_gates_pass'] and ready['registered_integration_pending']
    assert all(digest(path) == checksum for path, checksum in ready['evidence'].items())
    scope = dict(record_count=453, speech_count=442, typed_choice_count=11, menu_count=5, style_count=145,
        scoped_name_count=19, native_pages=444, relative_cases=630, FE_count=16, actual_frames=17441,
        actual_runs=1, actual_speeches=45, actual_body_pages=47, actual_choice_labels=11, offline_speeches=397)
    evidence = dict(manuscript=ready['manuscript'], plan=ready['plan'], reconstruction=str(reviewed.REBUILT),
        compiled_native=rebuilt['native'], stored_native=str(reviewed.STORED), stored_lookup=str(reviewed.LOOKUP),
        loaders=str(reviewed.LOADERS), visual_review=str(reviewed.RESEARCH/'complete_visual_approval.json'),
        actual=str(reviewed.RESEARCH/'actual_review.json'), scoped_names=str(reviewed.FINAL_NAMES),
        typed_menu=rebuilt['menu'], native_styles=rebuilt['styles'], research_completion=str(reviewed.READY))
    image = NdsImage.open(candidate)
    arm_hash = sha(image.read_file(ARM))
    dependencies = {str(path): digest(path) for path in (
        *evidence.values(), PARENT, parent['manifest'],
        Path('dk4tool/patch/rafael_story_b301_b320_release_v1.py'), Path(__file__))}
    config = dict(format='dk4-reviewed-rafael-compound-fu-scene-release-v1', **scope, **evidence,
        clean_ROM=str(CLEAN), clean_ROM_sha256=digest(CLEAN), canonical_ROM_sha256=digest(baseline),
        parent_ROM=str(candidate), parent_ROM_sha256=digest(candidate), pre_runtime_ARM9_sha256=arm_hash,
        target_ROM_sha256=rebuilt['research_ROM_sha256'], final_dependency_ROM=str(candidate),
        final_dependency_ROM_sha256=digest(candidate), final_runtime_ARM9_sha256=arm_hash,
        reviewed_blocks=rebuilt['reviewed_blocks'], blocks=rebuilt['changed_blocks'],
        right_bound_configuration=profile['ascii_glyph_right_bounds'], dependencies=dependencies)
    OUT.mkdir()
    draft = OUT/'dialogue_candidate_config.json'
    save(draft, config)
    proposed, proof = plan_release(image, NdsImage.open(baseline), draft)
    assembled = NdsImage.open(rebuilt['research_ROM'])
    assert proposed.save() == assembled.rom.save() and len(proof['changed_records']) == 453
    assert [path for _, path, value in image.iter_files() if assembled.read_file(path) != value] == [ARCHIVE]
    assert all(assembled.read_file(path) == value for path, value in image.iter_components())
    assembled.replace_file(ARCHIVE, image.read_file(ARCHIVE))
    assert bytes(assembled.rom.save()) == candidate.read_bytes()
    save(CONFIG, config)
    save(QUALIFICATION, dict(config=str(CONFIG), config_sha256=digest(CONFIG), predecessor_release=str(PARENT),
        predecessor_release_sha256=digest(PARENT), registry_sha256=digest(REGISTRY),
        predecessor_profile=parent['profile'], predecessor_manifest_sha256=parent['manifest_sha256'],
        target_ROM_sha256=rebuilt['research_ROM_sha256'], target_ARM9_sha256=arm_hash,
        dialogue_rebuilt_and_exact_453_stored_bindings_verified=True, changed_blocks=rebuilt['changed_blocks'],
        complete_parent_inverse_exact=True, only_SC0_changes=True, all_predecessor_stage_dependencies_preserved=True,
        registration_and_candidate_own_startup_pending=True, new_credit=0))
    print('Qualified all 453 dialogue records. Exact predecessor inverse and unchanged ARM9 passed.')


if __name__ == '__main__':
    main()
