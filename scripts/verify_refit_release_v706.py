"""Verify the complete integrated release and reconstruct its clean-ROM patch."""

from copy import deepcopy
from pathlib import Path

from dk4tool.graphics.plaque_contract import verify_final_plaque_material
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.refit_help_release import apply_release
from dk4tool.patch.xdelta import apply_xdelta, make_xdelta
from dk4tool.rom.nds import NdsImage
from scripts.run_refit_display_v706 import ROM
from scripts.run_room_gender_v694 import ROM as OLD_ROM
from scripts.trace_refit_text_v706 import ROOT
from scripts.verify_village_wrap_v608 import read, save


def files(rom):
    return {p: d for _, p, d in rom.iter_files()} | dict(rom.iter_components())


def main():
    pre = read(ROOT / 'preflight.json')
    assert sha(OLD_ROM.read_bytes()) == pre['candidate_sha256']
    old, current, clean = map(NdsImage.open, (OLD_ROM, ROM, 'work/clean.nds'))
    before, after = files(old), files(current)
    assert before.keys() == after.keys()
    assert [p for p in before if before[p] != after[p]] == ['/__arm9__.bin']
    expected, proof = apply_release(before['/__arm9__.bin'], 'translations/refit_help_release_v1.json')
    assert expected == after['/__arm9__.bin']
    graphics = [p for p in before if p.lower().endswith(('.pxl', '.fls'))]
    assert len(graphics) == 675 and all(before[p] == after[p] for p in graphics)
    registry = read('translations/release_stack.json')
    old_registry = read(ROOT / 'registry_before_v706.json')
    reduced = deepcopy(registry)
    profile = reduced['profiles'].pop('all-routes-unified-v706')
    assert reduced == old_registry
    inherited = deepcopy(profile)
    inherited.pop('refit_help_release')
    for key in ('description', 'note'):
        inherited[key] = old_registry['profiles']['all-routes-unified-v692'][key]
    assert inherited == old_registry['profiles']['all-routes-unified-v692']
    assert len(registry['accepted_layers']) == 114
    manifest, prior = read(ROM.with_suffix('.manifest.json')), read(OLD_ROM.with_suffix('.manifest.json'))
    assert manifest['candidate_sha256'] == sha(ROM.read_bytes())
    assert manifest['profile'] == 'all-routes-unified-v706'
    assert manifest['release_stack_sha256'] == sha(Path('translations/release_stack.json').read_bytes())
    assert manifest['base_sha256'] == registry['canonical_baseline']['sha256'] == sha(Path(manifest['base_rom']).read_bytes())
    assert manifest['batches'] == prior['batches'] and len(manifest['batches']) == 470
    assert manifest['required_batches'] == prior['required_batches'] and all(manifest['checks'].values())
    assert manifest['story_percent_contract'] == prior['story_percent_contract']
    assert manifest['final_plaque_contract'] == verify_final_plaque_material(old, clean, old_registry['profiles']['all-routes-unified-v692'])
    stage = manifest['relocations']['/__arm9__.bin']['refit_help_release']
    config = read('translations/refit_help_release_v1.json')
    assert stage['proof'] == config['proof'] and stage['release_config_sha256'] == sha(Path('translations/refit_help_release_v1.json').read_bytes())
    for path, records in prior['changed_records'].items():
        assert all(r in manifest['changed_records'][path] for r in records)
    assert all(f'REFIT_HELP_{r["message_id"]}' in manifest['changed_records']['/__arm9__.bin'] for r in proof['records'])
    assert all(t in after['/__arm9__.bin'] for t in (b'Continue', b'New Game', b'Options', b'Grand Race', b'Extras', b'Gallery'))
    patch = ROM.with_suffix('.xdelta')
    make_xdelta(Path('work/clean.nds'), ROM, patch)
    rebuilt = ROOT / 'V706_exact_patch_reconstruction.nds'
    apply_xdelta(Path('work/clean.nds'), patch, rebuilt)
    assert rebuilt.read_bytes() == ROM.read_bytes()
    save(ROOT / 'release_proof.json', {'candidate': str(ROM), 'candidate_sha256': sha(ROM.read_bytes()),
        'manifest_sha256': sha(ROM.with_suffix('.manifest.json').read_bytes()), 'patch_sha256': sha(patch.read_bytes()),
        'registry_sha256': sha(Path('translations/release_stack.json').read_bytes()),
        'only_ARM9_changed_all675_graphics_COMMON_HELP_story_ARM7_overlays_and_other_files_exact': True,
        'complete_prior470_batches114_accepted_layers_profiles_and_changed_records_preserved': True,
        'final_plaque_raw_art_and_story_percent_contracts_pass': True,
        'exact_clean_ROM_patch_reconstruction': str(rebuilt),
        'dedicated_help_selector_and_generated30_paragraph_proof': config['proof'],
        'source_candidate_preserved_canonical_not_promoted': True,
        'verifier_sha256': sha(Path(__file__).read_bytes()), 'full_goal_complete': False})
    print('V706 full integrated470-batch release and exact clean-ROM patch verified; all675 graphics/source files preserved.', flush=True)


if __name__ == '__main__':
    main()
