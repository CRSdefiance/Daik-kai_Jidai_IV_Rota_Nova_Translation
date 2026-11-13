"""Verify the complete registered five-row Refit build and clean-ROM patch."""

from copy import deepcopy
from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.main_pool_cache_visibility import cache_plan
from dk4tool.patch.refit_help_layout import apply_release
from dk4tool.patch.xdelta import apply_xdelta, make_xdelta
from dk4tool.rom.nds import NdsImage
from scripts.verify_refit_release_v708 import files
from scripts.verify_village_wrap_v608 import read, save

ROOT = Path('work/analysis/refit_help_v710')
ROM = Path('out/all_routes_combined_v710_candidate.nds')
OLD = Path('out/all_routes_combined_v708_candidate.nds')


def main():
    old, current = map(NdsImage.open, (OLD, ROM))
    before, after = files(old), files(current)
    assert before.keys() == after.keys()
    assert {p for p in before if before[p] != after[p]} == {'/__arm9__.bin'}
    arm, proof = apply_release(before['/__arm9__.bin'], 'translations/refit_help_layout_v1.json')
    assert arm == after['/__arm9__.bin'] == (ROOT / 'target_ARM9.bin').read_bytes()
    assert cache_plan(before['/__arm9__.bin']) == cache_plan(arm)
    graphics = [p for p in before if p.lower().endswith(('.pxl', '.fls'))]
    assert len(graphics) == 675 and all(before[p] == after[p] for p in graphics)
    registry_path = Path('translations/release_stack.json')
    registry, original = read(registry_path), read(ROOT / 'registry_before.json')
    reduced = deepcopy(registry)
    profile = reduced['profiles'].pop('all-routes-unified-v710')
    assert reduced == original
    inherited = deepcopy(profile)
    inherited.pop('refit_help_layout')
    for key in ('description', 'status'):
        if key in original['profiles']['all-routes-unified-v708']:
            inherited[key] = original['profiles']['all-routes-unified-v708'][key]
        else:
            inherited.pop(key, None)
    assert inherited == original['profiles']['all-routes-unified-v708']
    assert len(registry['accepted_layers']) == 114
    assert registry['profiles']['all-routes-unified-v706']['status'] == 'revoked'
    manifest, prior = read(ROM.with_suffix('.manifest.json')), read(OLD.with_suffix('.manifest.json'))
    assert manifest['profile'] == 'all-routes-unified-v710'
    assert manifest['candidate_sha256'] == sha(ROM.read_bytes())
    assert manifest['release_stack_sha256'] == sha(registry_path.read_bytes())
    assert manifest['base_sha256'] == registry['canonical_baseline']['sha256']
    assert manifest['base_sha256'] == sha(Path(manifest['base_rom']).read_bytes())
    assert manifest['batches'] == prior['batches'] and len(manifest['batches']) == 470
    assert manifest['required_batches'] == prior['required_batches'] and all(manifest['checks'].values())
    for path, records in prior['changed_records'].items():
        assert set(records) <= set(manifest['changed_records'][path])
    clean = Path('work/clean.nds')
    patch, restored = ROM.with_suffix('.xdelta'), ROOT / 'V710_exact_patch_reconstruction.nds'
    make_xdelta(clean, ROM, patch)
    apply_xdelta(clean, patch, restored)
    assert restored.read_bytes() == ROM.read_bytes()
    save(ROOT / 'release_proof.json', {'candidate': str(ROM), 'candidate_sha256': sha(ROM.read_bytes()),
        'manifest_sha256': sha(ROM.with_suffix('.manifest.json').read_bytes()),
        'patch_sha256': sha(patch.read_bytes()), 'registry_sha256': sha(registry_path.read_bytes()),
        'only_owned_Refit_ARM9_spans_differ_from_V708': proof,
        'all3668_COMMON_texts675_graphics_story_HELP_ARM7_overlays_other_files_exact_to_V708': True,
        'all470_batches114_accepted_layers_prior_profiles_and_final_contracts_retained': True,
        'autoload_pool_cache_and_allocator_bounds_exact_to_V692_V708': True,
        'exact_clean_ROM_patch_reconstruction': str(restored),
        'actual_changed_screen_and_native_heap_lifetime_pending': True,
        'canonical_baseline_not_promoted': True, 'full_goal_complete': False,
        'verifier_sha256': sha(Path(__file__).read_bytes())})
    print('V710 complete470/114 release,675 graphics and all text retained; scoped layout only; exact clean patch passes.', flush=True)


if __name__ == '__main__':
    main()
