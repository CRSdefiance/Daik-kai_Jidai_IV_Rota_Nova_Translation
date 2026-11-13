"""Qualify the two independent changes over the exact nine-stage cumulative ROM."""
from pathlib import Path

from dk4tool.patch.rafael_story_b261_b280_release_v1 import plan_release
from dk4tool.rom.nds import NdsImage
from scripts import finalize_rafael_B261_B280_research_v1 as reviewed
from scripts.audit_story_glyph_consistency import load, save
from scripts.finish_rafael_B261_B280_native_pages_v1 import ROOT, digest
from scripts.qualify_rafael_plett_relocation_v1 import CLEAN, REFERENCE, REGISTRY, plan_surnames
from scripts.verify_rafael3514_registered_release_v1 import RELEASE


OUT = ROOT / 'registered_preparation_v1'
CONFIG = Path('translations/rafael_B261_B280_editorial_release_v1.json')
ARCHIVE = '/data/SC0.DK4'
ARM = '/__arm9__.bin'


def main():
    assert not OUT.exists() and not CONFIG.exists()
    release, ready, rebuilt = map(load, (RELEASE, reviewed.READY, reviewed.REBUILT))
    registry = load(REGISTRY)
    assert digest(REGISTRY) == release['registry_sha256']
    assert release['all_preceding_eight_stages_and_exclusive_field_preserved'] and not release['own_registered_startup_pending']
    assert release['clean_input_patch_byte_exact'] and (release['registered_manifest_entries'], release['passing_release_checks']) == (692, 27)
    profile = registry['profiles'][release['profile']]
    assert 'owned_Francisca_name_field' in profile and 'ascii_glyph_right_bounds' in profile
    parent = Path(release['candidate'])
    baseline = Path(release['canonical_base'])
    assert digest(parent) == release['candidate_sha256'] == rebuilt['parent_sha256']
    assert digest(baseline) == release['canonical_sha256']
    assert digest(release['manifest']) == release['manifest_sha256']
    assert digest(CLEAN) == release['clean_input_sha256']
    assert ready['all_individual_five_gates_pass'] and ready['registered_integration_pending']
    assert all(digest(path) == checksum for path, checksum in ready['evidence'].items())
    scope = dict(record_count=135, speech_count=130, typed_choice_count=5, menu_count=2, style_count=16,
        scoped_name_count=18, native_pages=131, relative_cases=390, FE_count=17, actual_frames=15761,
        actual_runs=1, actual_speeches=42, actual_body_pages=43, actual_choice_labels=5, offline_speeches=88)
    evidence = dict(manuscript=ready['manuscript'], plan=ready['plan'], reconstruction=str(reviewed.REBUILT),
        compiled_native=rebuilt['native'], stored_native=str(reviewed.STORED), stored_lookup=str(reviewed.LOOKUP),
        loaders=str(reviewed.LOADERS), visual_review=str(reviewed.RESEARCH/'complete_visual_approval.json'),
        actual=str(reviewed.RESEARCH/'actual_review.json'), scoped_names=str(reviewed.FINAL_NAMES),
        typed_menu=rebuilt['menu'], native_styles=rebuilt['styles'], research_completion=str(reviewed.READY))
    image = NdsImage.open(parent)
    arm = image.read_file(ARM)
    archive = image.read_file(ARCHIVE)
    name_path = REFERENCE/'proposal.json'
    name_proof_path = REFERENCE/'proof.json'
    name_proof = load(name_proof_path)
    assert name_proof['all_other_raw_ROM_file_and_component_reserve_pointer_censuses_empty']
    names, name_plan = plan_surnames(arm, load(name_path), NdsImage.open(CLEAN).read_file(ARM))
    assert name_plan['target_ARM9_sha256'] == name_proof['target_ARM9_sha256']
    assert names == (REFERENCE/'corrected_ARM9_RESEARCH_ONLY.bin').read_bytes()
    dependencies = {str(path): digest(path) for path in (
        *evidence.values(), RELEASE, release['manifest'], name_path, name_proof_path, reviewed.NAME_PROOF,
        Path('dk4tool/patch/rafael_story_b261_b280_release_v1.py'),
        Path('scripts/qualify_rafael_plett_relocation_v1.py'), Path(__file__))}
    config = dict(format='dk4-reviewed-rafael-compound-fu-scene-release-v1', **scope, **evidence,
        clean_ROM=str(CLEAN), clean_ROM_sha256=digest(CLEAN), canonical_ROM_sha256=digest(baseline),
        parent_ROM=str(parent), parent_ROM_sha256=digest(parent), pre_runtime_ARM9_sha256=digest_arm(arm),
        target_ROM_sha256=rebuilt['research_ROM_sha256'], final_dependency_ROM=str(parent),
        final_dependency_ROM_sha256=digest(parent), final_runtime_ARM9_sha256=digest_arm(arm),
        reviewed_blocks=rebuilt['reviewed_blocks'], blocks=rebuilt['changed_blocks'],
        right_bound_configuration=profile['ascii_glyph_right_bounds'], dependencies=dependencies)
    OUT.mkdir()
    draft = OUT/'dialogue_candidate_config.json'
    save(draft, config)
    proposed, proof = plan_release(image, NdsImage.open(baseline), draft)
    assembled = NdsImage.open(rebuilt['research_ROM'])
    assert proposed.save() == assembled.rom.save() and len(proof['changed_records']) == 135
    assembled.replace_file(ARM, names)
    target = bytes(assembled.rom.save())
    assert [path for _, path, value in image.iter_files() if assembled.read_file(path) != value] == [ARCHIVE]
    assert [path for path, value in image.iter_components() if assembled.read_file(path) != value] == [ARM]
    assembled.replace_file(ARM, arm)
    assembled.replace_file(ARCHIVE, archive)
    assert bytes(assembled.rom.save()) == parent.read_bytes()
    save(CONFIG, config)
    save(OUT/'qualification.json', dict(
        config=str(CONFIG), config_sha256=digest(CONFIG), predecessor_release=str(RELEASE),
        predecessor_release_sha256=digest(RELEASE), registry_sha256=digest(REGISTRY),
        predecessor_profile=release['profile'], predecessor_manifest_sha256=release['manifest_sha256'],
        name_proposal=str(name_path), name_proposal_sha256=digest(name_path),
        name_ownership_proof=str(name_proof_path), name_ownership_proof_sha256=digest(name_proof_path),
        target_ROM_sha256=digest_arm(target), target_ARM9_sha256=digest_arm(names),
        dialogue_rebuilt_and_exact_135_stored_bindings_verified=True, changed_blocks=rebuilt['changed_blocks'],
        both_components_whole_parent_inverse_exact=True, only_SC0_and_ARM9_change=True,
        all_nine_prior_stage_dependencies_preserved=True, registration_and_candidate_own_startup_pending=True,
        new_credit=0))
    print('Qualified the exact 135-record and two-surname cumulative successor. Registry unchanged.')


from dk4tool.patch.grand_race_menu_release import sha as digest_arm

if __name__ == '__main__':
    main()
