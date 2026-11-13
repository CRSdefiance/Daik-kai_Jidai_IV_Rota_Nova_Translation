"""Verify the full registered build, original allocation and exact clean patch."""

import copy
from pathlib import Path

from dk4tool.graphics.plaque_contract import verify_final_plaque_material
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.navigator_captain_filter import AFTER, BEFORE, FIELD, OFFSET, apply_release
from dk4tool.patch.xdelta import apply_xdelta, make_xdelta
from dk4tool.rom.nds import NdsImage
from scripts.run_navigator_filter_v692 import ROM, ROOT
from scripts.verify_village_wrap_v608 import read, save


def files(rom):
    return {p: d for _, p, d in rom.iter_files()} | dict(rom.iter_components())


def main():
    pre, registered = read(ROOT / 'build_preflight.json'), read(ROOT / 'registration.json')
    old_path = Path(pre['source_candidate'])
    assert sha(old_path.read_bytes()) == pre['source_candidate_sha256']
    old, current, clean = map(NdsImage.open, (old_path, ROM, 'work/clean.nds'))
    before, after = files(old), files(current)
    assert before.keys() == after.keys()
    assert [p for p in before if before[p] != after[p]] == ['/__arm9__.bin']
    path = '/__arm9__.bin'
    expected, proof = apply_release(before[path], clean.read_file(path), pre['config'])
    assert expected == after[path] and proof == pre['repair_plan']
    assert before[path][OFFSET:OFFSET + 8] == BEFORE and after[path][OFFSET:OFFSET + 8] == AFTER
    assert before[path][:OFFSET] == after[path][:OFFSET] and before[path][OFFSET + 8:] == after[path][OFFSET + 8:]
    assert after[path][FIELD:FIELD + 8] == before[path][FIELD:FIELD + 8]
    registry_path = Path('translations/release_stack.json')
    registry = read(registry_path)
    old_registry_path = Path(pre['source_registry'])
    assert sha(old_registry_path.read_bytes()) == pre['source_registry_sha256']
    reduced = copy.deepcopy(registry)
    profile = reduced['profiles'].pop(pre['profile'])
    assert reduced == read(old_registry_path)
    assert profile['navigator_captain_filter'] == pre['config']
    inherited = copy.deepcopy(profile)
    inherited.pop('navigator_captain_filter')
    inherited['description'] = reduced['profiles'][pre['source_profile']]['description']
    assert inherited == reduced['profiles'][pre['source_profile']]
    assert len(registry['accepted_layers']) == 114
    manifest = read(ROM.with_suffix('.manifest.json'))
    prior = read(old_path.with_suffix('.manifest.json'))
    assert manifest['profile'] == pre['profile'] and manifest['candidate_sha256'] == sha(ROM.read_bytes())
    assert manifest['release_stack_sha256'] == registered['registry_sha256'] == sha(registry_path.read_bytes())
    assert manifest['batches'] == prior['batches'] and len(manifest['batches']) == 470
    assert manifest['required_batches'] == prior['required_batches'] and all(manifest['checks'].values())
    assert manifest['base_sha256'] == pre['canonical_sha256'] == sha(Path(manifest['base_rom']).read_bytes())
    assert manifest['story_percent_contract'] == prior['story_percent_contract']
    # V685's original manifest predates the V687 final guard. Recheck the actual
    # original ROM rather than inventing a historical manifest field.
    assert manifest['final_plaque_contract'] == verify_final_plaque_material(
        old, clean, reduced['profiles'][pre['source_profile']])
    new_stage = manifest['relocations'][path]['navigator_captain_filter']
    assert new_stage['proof'] == proof and new_stage['release_config_sha256'] == pre['config_sha256']
    for file, records in prior['changed_records'].items():
        assert all(row in manifest['changed_records'][file] for row in records)
    graphics = [p for p in before if p.lower().endswith(('.pxl', '.fls'))]
    assert len(graphics) == 675 and all(before[p] == after[p] for p in graphics)
    assert all(t in after[path] for t in (b'Continue', b'New Game', b'Options', b'Grand Race', b'Extras', b'Gallery'))
    patch = ROM.with_suffix('.xdelta')
    make_xdelta(Path('work/clean.nds'), ROM, patch)
    reconstruction = ROOT / 'V692_exact_patch_reconstruction.nds'
    apply_xdelta(Path('work/clean.nds'), patch, reconstruction)
    assert reconstruction.read_bytes() == ROM.read_bytes()
    save(ROOT / 'static_release_proof.json', {'candidate': str(ROM), 'candidate_sha256': sha(ROM.read_bytes()),
        'manifest_sha256': sha(ROM.with_suffix('.manifest.json').read_bytes()),
        'patch_sha256': sha(patch.read_bytes()), 'registry_sha256': sha(registry_path.read_bytes()),
        'only_original_eight_byte_caption_slot_differs_from_complete_V685': True,
        'all675_whole_graphics_files_all_story_COMMON_HELP_ARM7_overlays_and_other_ARM9_bytes_exact': True,
        'all470_batches114_accepted_layers_prior_profiles_records_and_final_contracts_preserved': True,
        'exact_clean_ROM_patch_reconstruction': True, 'caption_proof': proof,
        'verifier_sha256': sha(Path(__file__).read_bytes()), 'full_goal_complete': False})
    print('V692 static: only8 caption bytes; all graphics/layers retained; exact clean patch reconstructed.', flush=True)


if __name__ == '__main__':
    main()
