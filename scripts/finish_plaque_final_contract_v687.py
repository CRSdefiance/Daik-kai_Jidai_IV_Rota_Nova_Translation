"""Verify the complete rebuild is unchanged and its final contract is recorded."""

from pathlib import Path

from dk4tool.graphics.plaque_contract import verify_final_plaque_material
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.verify_plaque_final_contract_v687 import ROM, ROOT
from scripts.verify_village_wrap_v608 import read, save

REBUILT = Path('out/all_routes_combined_v685_plaque_contract_rebuild.nds')


def main():
    pre = read(ROOT / 'preflight.json')
    proof = read(ROOT / 'contract_proof.json')
    for path, digest in pre['release_hashes'].items():
        assert sha(Path(path).read_bytes()) == digest
    assert proof['gate_sha256'] == sha(Path('dk4tool/graphics/plaque_contract.py').read_bytes())
    assert proof['builder_sha256'] == sha(Path('scripts/build_integrated_release.py').read_bytes())
    assert proof['verifier_sha256'] == sha(Path('scripts/verify_plaque_final_contract_v687.py').read_bytes())
    original, rebuilt = ROM.read_bytes(), REBUILT.read_bytes()
    assert rebuilt == original
    manifest = read(REBUILT.with_suffix('.manifest.json'))
    old = read(ROM.with_suffix('.manifest.json'))
    assert manifest['candidate_sha256'] == sha(original)
    assert manifest['profile'] == old['profile'] == 'all-routes-unified-v685'
    assert manifest['base_sha256'] == old['base_sha256']
    assert manifest['release_stack_sha256'] == old['release_stack_sha256']
    assert manifest['batches'] == old['batches'] and len(manifest['batches']) == 470
    assert manifest['required_batches'] == old['required_batches']
    assert len(read('translations/release_stack.json')['accepted_layers']) == 114
    assert manifest['changed_paths'] == old['changed_paths']
    assert manifest['changed_records'] == old['changed_records']
    assert manifest['relocations'] == old['relocations']
    assert manifest['checks']['final_reviewed_plaque_material_contract_enforced']
    actual = verify_final_plaque_material(NdsImage.open(REBUILT), NdsImage.open('work/clean.nds'),
        read('translations/release_stack.json')['profiles'][manifest['profile']])
    assert actual == manifest['final_plaque_contract'] == proof['final_contract']
    for key, value in old['checks'].items():
        assert manifest['checks'][key] == value
    assert manifest['story_percent_contract'] == old['story_percent_contract']
    save(ROOT / 'rebuild_proof.json', {
        'rebuild': str(REBUILT), 'rebuild_sha256': sha(rebuilt),
        'manifest': str(REBUILT.with_suffix('.manifest.json')),
        'manifest_sha256': sha(REBUILT.with_suffix('.manifest.json').read_bytes()),
        'complete_ROM_bytes_exact_V685_no_graphics_code_or_translation_changed': True,
        'all470_batches114_accepted_layers_and_every_prior_manifest_check_retained': True,
        'changed_paths_records_relocations_and_story_format_contract_exact_V685': True,
        'new_manifest_records_final17_plaque_and_whole_hint_material_contract': True,
        'original_V685_patch_still_applies_to_identical_bytes_no_new_patch_needed': True,
        'existing_V671_runtime_evidence_inherited_no_new_emulator_run_claim': True,
        'new_guard_does_not_close_visual_approval_or_any_of18_open_entries': True,
        'verifier_sha256': sha(Path(__file__).read_bytes()), 'full_goal_complete': False})
    print('V687 complete registered rebuild exact V685; all prior content/checks retained; final plaque contract in new manifest.', flush=True)


if __name__ == '__main__':
    main()
