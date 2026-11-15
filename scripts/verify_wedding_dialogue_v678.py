"""Exact final-stage preservation and clean-source patch reconstruction."""

from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.wedding_dialogue_cleanup import apply_release
from dk4tool.patch.xdelta import apply_xdelta, make_xdelta
from dk4tool.rom.nds import NdsImage
from scripts.prepare_wedding_dialogue_v678 import ROOT
from scripts.verify_village_wrap_v608 import read, save

ROM = Path('out/all_routes_combined_v678_candidate.nds')


def main():
    pre = read(ROOT / 'preflight.json')
    old, new = NdsImage.open(pre['source_candidate']), NdsImage.open(ROM)
    before = {p: d for _, p, d in old.iter_files()} | dict(old.iter_components())
    after = {p: d for _, p, d in new.iter_files()} | dict(new.iter_components())
    assert before.keys() == after.keys()
    assert [p for p in before if before[p] != after[p]] == ['/data/SC2.DK4']
    canonical = NdsImage.open(pre['canonical_baseline']['path'])
    target, changes = apply_release(before['/data/SC2.DK4'], canonical.read_file('/data/SC2.DK4'),
                                    'translations/wedding_dialogue_cleanup_v1.json')
    assert target == after['/data/SC2.DK4']
    stack, manifest = read('translations/release_stack.json'), read(ROM.with_suffix('.manifest.json'))
    parent = read(Path(pre['source_candidate']).with_suffix('.manifest.json'))
    prior = read('translations/release_stack.json')
    del prior['profiles']['all-routes-unified-v678']
    assert prior == pre['source_registry']
    profile = stack['profiles']['all-routes-unified-v678']
    original = stack['profiles']['all-routes-unified-v666']
    assert {k: v for k, v in profile.items() if k not in ('description', 'wedding_dialogue_cleanup')} == {
        k: v for k, v in original.items() if k != 'description'}
    assert manifest['profile'] == 'all-routes-unified-v678'
    assert manifest['candidate_sha256'] == sha(ROM.read_bytes())
    assert manifest['release_stack_sha256'] == sha(Path('translations/release_stack.json').read_bytes())
    assert manifest['base_sha256'] == parent['base_sha256'] == sha(Path(manifest['base_rom']).read_bytes())
    assert manifest['batches'] == parent['batches'] and len(manifest['batches']) == 470
    assert manifest['required_batches'] == parent['required_batches']
    assert len(stack['accepted_layers']) == 114 and stack['accepted_layers'] == pre['accepted_layers']
    assert all(manifest['checks'].values()) and manifest['changed_paths'] == parent['changed_paths']
    stage = manifest['relocations']['/data/SC2.DK4']['wedding_dialogue_cleanup']
    assert stage['proof'] == changes
    assert stage['release_config_sha256'] == sha(Path(stage['release_config']).read_bytes())
    inherited = read('work/analysis/region_boundaries_v640/preservation_proof.json')
    graphics = {p for p in before if p.lower().endswith(('.pxl', '.fls'))}
    assert len(graphics) == 675 and {e['path'] for e in inherited['entries']} == graphics
    assert len(inherited['entries']) == 921 and inherited['all57_embedded_block_extents_exact']
    assert all(before[p] == after[p] for p in graphics)
    clean = Path('work/clean.nds')
    assert sha(clean.read_bytes()) == 'f4f07c975cc293f5b2ba469747693d3dd37f2e6dfc408cf5910adf5e83d9177d'
    patch, rebuilt = ROM.with_suffix('.xdelta'), ROOT / 'all_routes_combined_v678_PATCH_RECONSTRUCTION.nds'
    make_xdelta(clean, ROM, patch)
    apply_xdelta(clean, patch, rebuilt)
    assert rebuilt.read_bytes() == ROM.read_bytes()
    save(ROOT / 'static_release_proof.json', {
        'candidate': str(ROM), 'candidate_sha256': sha(ROM.read_bytes()),
        'manifest_sha256': sha(ROM.with_suffix('.manifest.json').read_bytes()),
        'ARM9_sha256': sha(after['/__arm9__.bin']), 'patch_sha256': sha(patch.read_bytes()),
        'base': manifest['base_rom'], 'base_sha256': manifest['base_sha256'],
        'registry_sha256': manifest['release_stack_sha256'], 'stage': stage,
        'only_two_SC2_spans_changed_all_other_files_components_and_675_graphics_files_exact_V666': True,
        'all921_views57_embedded_extents_preserved': True,
        'all470_batches114_accepted_layers_and_prior_profiles_unchanged': True,
        'exact_clean_patch_reconstruction': True, 'reconstructed_ROM': str(rebuilt),
        'canonical_promoted': False, 'cold_boot_verification_pending': True, 'full_goal_complete': False})
    print('V678 exact two-record integration, complete preservation and patch reconstruction pass.', flush=True)


if __name__ == '__main__':
    main()
