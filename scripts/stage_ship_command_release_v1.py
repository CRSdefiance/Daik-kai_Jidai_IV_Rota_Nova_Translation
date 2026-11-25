"""Stage the qualified raw ship label over the exact registered Lil261 stack."""

from pathlib import Path

from dk4tool.patch.ship_command_label_v1 import transform
from dk4tool.patch.xdelta import apply_xdelta, make_xdelta
from dk4tool.rom.nds import NdsImage
from scripts.audit_story_glyph_consistency import load, save
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest
from scripts.prepare_ship_command_research_v1 import PROOF, RELEASE as PARENT, ROM as RESEARCH, WORK


OUT = Path('work/ship_command_label_release_v1')
PROFILE = 'all-routes-ship-command-label-v1-20261110'
CANDIDATE = OUT / 'all_routes_ship_command_label_candidate.nds'
PATCH = CANDIDATE.with_suffix('.xdelta')
MANIFEST = CANDIDATE.with_suffix('.manifest.json')
INVERSE_PATCH = OUT / 'clean_input_reconstruction_RESEARCH_ONLY.nds'
PARENT_REGISTRY = OUT / 'release_stack_before_ship_command.json'
STARTUP = OUT / 'own_registered_startup_verification.json'
GETTERS = OUT / 'own_registered_name_getters_v1.json'
STAGED = OUT / 'staged_successor.json'
RELEASE = OUT / 'registered_release_verification.json'
REGISTRY = Path('translations/release_stack.json')
CLEAN = Path('work/clean.nds')
ARM = '/__arm9__.bin'


def main():
    assert not OUT.exists()
    parent, research = map(load, (PARENT, PROOF))
    assert digest(REGISTRY) == parent['registry_sha256']
    assert digest(parent['manifest']) == parent['manifest_sha256']
    assert digest(parent['canonical_base']) == parent['canonical_sha256']
    assert digest(parent['candidate']) == parent['candidate_sha256'] == research['parent_sha256']
    assert digest(CLEAN) == parent['clean_input_sha256']
    assert parent['all_predecessor_stage_dependencies_preserved'] and parent['clean_input_patch_byte_exact']
    assert parent['registered_market_format_andboth_data_pointers_preserved']
    assert not parent['own_registered_startup_pending']
    manifest, registry = load(parent['manifest']), load(REGISTRY)
    assert PROFILE not in registry['profiles'] and len(registry['accepted_layers']) == 114
    assert len(manifest['batches']) == 731 and len(manifest['checks']) == 66 and all(manifest['checks'].values())
    profile = registry['profiles'][parent['profile']]
    assert profile['ascii_glyph_right_bounds'] and manifest['checks']['registered_runtime_bounds_and_complete_parent_target_inverse']
    menu = WORK / 'native_menu/native_ship_menu.json'
    native = load(menu)
    assert native['complete_english_planes_centering_leading_trailing_glyphs_bounds_andguards_pass']
    image = NdsImage.open(parent['candidate'])
    source = image.read_file(ARM)
    arm, proof = transform(source)
    assert digest(RESEARCH) == research['ROM_sha256']
    image.replace_file(ARM, arm)
    output = bytes(image.rom.save())
    assert output == RESEARCH.read_bytes()
    reference = NdsImage.open(parent['candidate'])
    assert list(image.iter_files()) == list(reference.iter_files())
    assert [p for p, data in reference.iter_components() if image.read_file(p) != data] == [ARM]
    image.replace_file(ARM, source)
    assert bytes(image.rom.save()) == Path(parent['candidate']).read_bytes()

    OUT.mkdir()
    PARENT_REGISTRY.write_bytes(REGISTRY.read_bytes())
    CANDIDATE.write_bytes(output)
    make_xdelta(CLEAN, CANDIDATE, PATCH)
    apply_xdelta(CLEAN, PATCH, INVERSE_PATCH)
    assert INVERSE_PATCH.read_bytes() == output
    assert digest(REGISTRY) == digest(PARENT_REGISTRY) == parent['registry_sha256']
    save(STAGED, dict(profile=PROFILE, candidate=str(CANDIDATE), candidate_sha256=digest(CANDIDATE),
        patch=str(PATCH), patch_sha256=digest(PATCH), exact_clean_reconstruction=str(INVERSE_PATCH),
        reconstructed_sha256=digest(INVERSE_PATCH), clean_input_sha256=digest(CLEAN),
        clean_input_patch_byte_exact=True, parent=parent['candidate'], parent_sha256=parent['candidate_sha256'],
        predecessor_profile=parent['profile'], predecessor_release_sha256=digest(PARENT),
        predecessor_manifest_sha256=parent['manifest_sha256'], predecessor_registry_sha256=digest(PARENT_REGISTRY),
        canonical_base=parent['canonical_base'], canonical_sha256=parent['canonical_sha256'],
        target_ARM9_sha256=proof['target_ARM9_sha256'], original_data_only_transform=proof,
        whole_parent_inverse_exact=True, all_predecessor_stage_dependencies_preserved=True,
        unchanged_files_and_other_components_prove_story_and_market_dependencies_preserved=True,
        right_bound_configuration=profile['ascii_glyph_right_bounds'],
        original_final_story_percent_contract=manifest['story_percent_contract'],
        own_registered_startup_pending=True, actual_menu_approval_pending=True,
        registration_pending=True, experimental_not_promoted=True, new_credit=0,
        evidence={str(p):digest(p) for p in [PARENT, PROOF, menu, Path(__file__)]}))
    print('Staged the ship-label successor. Clean-input patch and complete parent inverse match exactly.')


if __name__ == '__main__':
    main()
