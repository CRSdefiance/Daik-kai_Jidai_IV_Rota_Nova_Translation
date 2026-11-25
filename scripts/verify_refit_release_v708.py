"""Verify integrated31-help repack, full preservation and exact clean-ROM patch."""

from copy import deepcopy
from pathlib import Path

from dk4tool.graphics.plaque_contract import verify_final_plaque_material
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.main_pool_cache_visibility import cache_plan
from dk4tool.patch.refit_help_repack import apply_release
from dk4tool.patch.xdelta import apply_xdelta, make_xdelta
from dk4tool.rom.nds import NdsImage
from dk4tool.script.common_message_table import common_message_entries
from scripts.run_room_gender_v694 import ROM as OLD_ROM
from scripts.verify_refit_repack_v708 import ROOT
from scripts.verify_village_wrap_v608 import read, save

ROM = Path('out/all_routes_combined_v708_candidate.nds')


def files(rom):
    return {p: d for _, p, d in rom.iter_files()} | dict(rom.iter_components())


def main():
    pre = read(ROOT / 'preflight.json')
    assert sha(OLD_ROM.read_bytes()) == pre['candidate_sha256']
    old, current, clean = map(NdsImage.open, (OLD_ROM, ROM, 'work/clean.nds'))
    before, after = files(old), files(current)
    assert before.keys() == after.keys()
    assert {p for p in before if before[p] != after[p]} == {'/__arm9__.bin', '/COMMON/MESFILE.DK4'}
    common, arm, proof = apply_release(before['/COMMON/MESFILE.DK4'], before['/__arm9__.bin'],
        'translations/refit_help_repack_v2.json')
    assert common == after['/COMMON/MESFILE.DK4'] and arm == after['/__arm9__.bin']
    assert cache_plan(before['/__arm9__.bin']) == cache_plan(arm)
    graphics = [p for p in before if p.lower().endswith(('.pxl', '.fls'))]
    assert len(graphics) == 675 and all(before[p] == after[p] for p in graphics)
    source_entries = common_message_entries(before['/COMMON/MESFILE.DK4'], before['/__arm9__.bin'], clean=False)
    actual_entries = common_message_entries(common, arm, clean=False)
    replacements = {r['message_id']: bytes.fromhex(r['compiled_hex'])[:-1] for r in proof['records']}
    assert len(replacements) == 31
    assert all(e.text == replacements.get(s.message_id, s.text) for s, e in zip(source_entries, actual_entries, strict=True))
    registry_path = Path('translations/release_stack.json')
    registry = read(registry_path)
    original = read(ROOT / 'registry_before_v708.json')
    reduced = deepcopy(registry)
    profile = reduced['profiles'].pop('all-routes-unified-v708')
    assert reduced == original
    inherited = deepcopy(profile)
    inherited.pop('refit_help_repack')
    for key in ('description', 'note'):
        inherited[key] = original['profiles']['all-routes-unified-v692'][key]
    assert inherited == original['profiles']['all-routes-unified-v692']
    assert len(registry['accepted_layers']) == 114 and registry['profiles']['all-routes-unified-v706']['status'] == 'revoked'
    manifest, prior = read(ROM.with_suffix('.manifest.json')), read(OLD_ROM.with_suffix('.manifest.json'))
    assert manifest['profile'] == 'all-routes-unified-v708' and manifest['candidate_sha256'] == sha(ROM.read_bytes())
    assert manifest['release_stack_sha256'] == sha(registry_path.read_bytes())
    assert manifest['base_sha256'] == registry['canonical_baseline']['sha256'] == sha(Path(manifest['base_rom']).read_bytes())
    assert manifest['batches'] == prior['batches'] and len(manifest['batches']) == 470
    assert manifest['required_batches'] == prior['required_batches'] and all(manifest['checks'].values())
    assert manifest['story_percent_contract'] == prior['story_percent_contract']
    assert manifest['final_plaque_contract'] == verify_final_plaque_material(old, clean, original['profiles']['all-routes-unified-v692'])
    for path, rows in prior['changed_records'].items():
        assert all(r in manifest['changed_records'][path] for r in rows)
    assert manifest['relocations']['/__arm9__.bin']['refit_help_repack']['proof'] == read('translations/refit_help_repack_v2.json')['proof']
    assert all(t in arm for t in (b'Continue', b'New Game', b'Options', b'Grand Race', b'Extras', b'Gallery'))
    patch, restored = ROM.with_suffix('.xdelta'), ROOT / 'V708_exact_patch_reconstruction.nds'
    make_xdelta(Path('work/clean.nds'), ROM, patch)
    apply_xdelta(Path('work/clean.nds'), patch, restored)
    assert restored.read_bytes() == ROM.read_bytes()
    save(ROOT / 'release_proof.json', {'candidate': str(ROM), 'candidate_sha256': sha(ROM.read_bytes()),
        'manifest_sha256': sha(ROM.with_suffix('.manifest.json').read_bytes()), 'patch_sha256': sha(patch.read_bytes()),
        'registry_sha256': sha(registry_path.read_bytes()),
        'only_COMMON31_help_texts_and_three_block_directory_offsets_changed': True,
        'all3637_other_native_message_texts675_graphics_story_HELP_ARM7_overlays_and_other_files_exact': True,
        'all_executable_code_startup_allocator_pool_cache_and_section_extents_exact': True,
        'complete_prior470_batches114_accepted_layers_profiles_records_and_final_contracts_preserved': True,
        'V706_runtime_failure_revoked_and_not_used_as_parent': True,
        'exact_clean_ROM_patch_reconstruction': str(restored),
        'canonical_baseline_not_promoted': True,
        'verifier_sha256': sha(Path(__file__).read_bytes()), 'full_goal_complete': False})
    print('V708 complete31-help release:3637 other texts,675 graphics, startup/allocator and all470 batches preserved; clean patch exact.', flush=True)


if __name__ == '__main__':
    main()
