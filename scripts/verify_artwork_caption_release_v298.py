"""Verify registered caption integration, inherited files and exact clean patch."""

import json
from pathlib import Path

from dk4tool.patch.artwork_name_captions import apply_release
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.message_actor_integrity import verify_original_actors
from dk4tool.patch.xdelta import apply_xdelta, make_xdelta
from dk4tool.rom.nds import NdsImage
from scripts.prepare_artwork_caption_release_v298 import CONFIG, ROOT, read
from scripts.verify_artwork_caption_selector_v284 import execute
from scripts.verify_ordinary_name_fidelity_research import initialized

ROM = Path('out/all_routes_combined_v298_candidate.nds')


def main():
    parent_path = Path('out/all_routes_combined_v296_candidate.nds')
    parent, candidate, clean = [NdsImage.open(p) for p in (parent_path, ROM, 'work/clean.nds')]
    assert sha(parent_path.read_bytes()) == '6096fb457d460c53964f1fe3c7aac33e152ac7eef28fefe6309e202760497833'
    manifest, previous = read(ROM.with_suffix('.manifest.json')), read(parent_path.with_suffix('.manifest.json'))
    stack = read('translations/release_stack.json')
    assert manifest['candidate_sha256'] == sha(ROM.read_bytes())
    assert manifest['base_sha256'] == stack['canonical_baseline']['sha256']
    assert manifest['release_stack_sha256'] == sha(Path('translations/release_stack.json').read_bytes())
    assert manifest['profile'] == 'all-routes-unified-v298' and all(manifest['checks'].values())
    assert manifest['batches'] == previous['batches'] and manifest['required_batches'] == previous['required_batches']
    before = {p: raw for _, p, raw in parent.iter_files()} | dict(parent.iter_components())
    after = {p: raw for _, p, raw in candidate.iter_files()} | dict(candidate.iter_components())
    changed = [p for p in before if before[p] != after[p]]
    assert before.keys() == after.keys() and changed == ['/__arm9__.bin']
    # Verify every header/table component not exposed as a ROM file as well.
    for name in ('arm9OverlayTable', 'arm7OverlayTable', 'arm7', 'iconBanner', 'name', 'idCode',
                 'arm9RamAddress', 'arm9EntryAddress', 'arm7RamAddress', 'arm7EntryAddress'):
        assert getattr(candidate.rom, name) == getattr(parent.rom, name)
    expected, transform = apply_release(before['/__arm9__.bin'], clean.read_file('/__arm9__.bin'), CONFIG)
    arm = after['/__arm9__.bin']
    assert arm == expected
    initialized(arm)
    paths = [f'/data/SC{i}.DK4' for i in range(4)]
    ordinal_source = NdsImage.open('out/all_routes_combined_v275_candidate.nds')
    actors = verify_original_actors({p: ordinal_source.read_file(p) for p in paths},
                                   {p: candidate.read_file(p) for p in paths},
                                   {p: clean.read_file(p) for p in paths})
    scenes = read('translations/scene_caption_manuscript_v2.json')['records']
    cases = [execute(arm, row, mode) for row in scenes for mode in (4, 16)]
    descriptions = [r for r in read('translations/gallery_description_manuscript_v1.json')['records']
                    if r['id'].startswith('EVENT_SCENES_') and r['id'] != 'EVENT_SCENES_DESCRIPTION'
                    and r['id'].endswith('_DESCRIPTION')]
    assert len(scenes) == 164 and len(descriptions) == 4
    gallery = [execute(arm, {'id': row['id'], 'index': index, 'english': row['english']}, mode, gallery=True)
               for index, row in enumerate(descriptions) for mode in (4, 16)]
    clean_path, patch, reconstruction = Path('work/clean.nds'), ROM.with_suffix('.xdelta'), ROOT / 'exact_patch_reconstruction.nds'
    assert sha(clean_path.read_bytes()) == 'f4f07c975cc293f5b2ba469747693d3dd37f2e6dfc408cf5910adf5e83d9177d'
    make_xdelta(clean_path, ROM, patch)
    apply_xdelta(clean_path, patch, reconstruction)
    assert reconstruction.read_bytes() == ROM.read_bytes()
    proof = {'format': 'dk4-artwork-caption-release-v298', 'candidate': str(ROM), 'candidate_sha256': sha(ROM.read_bytes()),
             'patch': str(patch), 'patch_sha256': sha(patch.read_bytes()), 'profile': manifest['profile'],
             'canonical_base': stack['canonical_baseline'], 'all_inherited_batches': len(manifest['batches']),
             'changed_vs_V296': changed, 'transform': transform, 'native_scene_caption_cases': cases,
             'native_gallery_composite_cases': gallery, 'all_original_native_actor_fields_preserved': actors,
             'all_native_selector_centering_font_clear_overlay_bounds_and_guards_pass': True,
             'exact_clean_patch_reconstruction_pass': True,
             'all_graphics_fonts_route_files_ARM7_and_overlays_exactV296': True,
             'actual_targeted_cold_boot_pending': True, 'unlocked_Gallery_and_original_deep_scene_navigation_pending': True,
             'V297_full_route_naming_integration_pending': True,
             'all18_plaque_hint_entries_and_variants_incomplete': True,
             'experimental_user_acceptance_pending': True, 'full_goal_complete': False}
    (ROOT / 'release_proof.json').write_text(json.dumps(proof, indent=2) + '\n', encoding='utf-8')
    print(f'{len(cases)} native scene cases; {len(gallery)} Gallery composites; all467 inherited batches; exact patch reconstruction.', flush=True)


if __name__ == '__main__':
    main()
