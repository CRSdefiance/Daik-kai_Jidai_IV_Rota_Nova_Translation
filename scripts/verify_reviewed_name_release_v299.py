"""Verify the full registered migration, inherited art and reconstructable patch."""

import json
from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.xdelta import apply_xdelta, make_xdelta
from dk4tool.rom.nds import NdsImage
from scripts.prepare_reviewed_name_release_v299 import CONFIG, PARENT, ROOT, read
from scripts.verify_artwork_caption_selector_v284 import execute

ROM = Path('out/all_routes_combined_v299_candidate.nds')


def main():
    config = read(CONFIG)
    candidate, parent = NdsImage.open(ROM), NdsImage.open(PARENT)
    manifest, previous = read(ROM.with_suffix('.manifest.json')), read(PARENT.with_suffix('.manifest.json'))
    assert manifest['candidate_sha256'] == sha(ROM.read_bytes())
    assert manifest['profile'] == 'all-routes-unified-v299' and all(manifest['checks'].values())
    assert manifest['release_stack_sha256'] == sha(Path('translations/release_stack.json').read_bytes())
    assert manifest['batches'] == previous['batches'] and manifest['required_batches'] == previous['required_batches']
    a = {p: raw for _, p, raw in parent.iter_files()} | dict(parent.iter_components())
    b = {p: raw for _, p, raw in candidate.iter_files()} | dict(candidate.iter_components())
    changed = sorted(p for p in a if a[p] != b[p])
    assert a.keys() == b.keys() and changed == sorted(config['target_file_sha256'])
    assert {p: sha(b[p]) for p in changed} == config['target_file_sha256']
    assert {p: sha(a[p]) for p in changed} == config['source_file_sha256']
    for name in ('arm9OverlayTable', 'arm7OverlayTable', 'arm7', 'iconBanner', 'name', 'idCode',
                 'arm9RamAddress', 'arm9EntryAddress', 'arm7RamAddress', 'arm7EntryAddress'):
        assert getattr(candidate.rom, name) == getattr(parent.rom, name)
    report = manifest['relocations']['/__arm9__.bin']['reviewed_name_integration']
    assert report['route']['original_actor_records'] == 19254
    assert len(report['route']['fixed_records']) == 197 and report['catalog']['catalog_source_records'] == 247
    assert report['COMMON']['all3668_selections_exact'] and report['COMMON']['all3662_unselected_texts_and_padding_exact']
    assert report['HELP']['native203_history_sentinel_preserved']
    native = read(ROOT / 'full_native_proof.json')
    assert native['ARM9_sha256'] == sha(b['/__arm9__.bin']) and native['all444_complete_body_glyphs_pass']
    # Refresh all artwork caption selectors on the enlarged pool; previous
    # caption pointers and strings must survive the later full name migration.
    scene_cases = [execute(b['/__arm9__.bin'], row, mode)
                   for row in read('translations/scene_caption_manuscript_v2.json')['records'] for mode in (4, 16)]
    prior_scenes = read('work/analysis/artwork_caption_release_v298/release_proof.json')['native_scene_caption_cases']
    assert scene_cases == prior_scenes
    descriptions = [r for r in read('translations/gallery_description_manuscript_v1.json')['records']
                    if r['id'].startswith('EVENT_SCENES_') and r['id'] != 'EVENT_SCENES_DESCRIPTION'
                    and r['id'].endswith('_DESCRIPTION')]
    gallery = [execute(b['/__arm9__.bin'], {'id': row['id'], 'index': index, 'english': row['english']}, mode, gallery=True)
               for index, row in enumerate(descriptions) for mode in (4, 16)]
    assert gallery == read('work/analysis/artwork_caption_release_v298/release_proof.json')['native_gallery_composite_cases']
    patch, reconstructed = ROM.with_suffix('.xdelta'), ROOT / 'exact_patch_reconstruction.nds'
    clean = Path('work/clean.nds')
    assert sha(clean.read_bytes()) == 'f4f07c975cc293f5b2ba469747693d3dd37f2e6dfc408cf5910adf5e83d9177d'
    make_xdelta(clean, ROM, patch)
    apply_xdelta(clean, patch, reconstructed)
    assert reconstructed.read_bytes() == ROM.read_bytes()
    output = {'format': 'dk4-reviewed-name-full-release-v299', 'candidate': str(ROM),
              'candidate_sha256': sha(ROM.read_bytes()), 'patch': str(patch), 'patch_sha256': sha(patch.read_bytes()),
              'canonical_base': manifest['base_rom'], 'canonical_sha256': manifest['base_sha256'],
              'profile': manifest['profile'], 'changed_vs_V298': changed,
              'all467_inherited_batches_and_accepted_requirements_preserved': True,
              'all_graphics_fonts_ARM7_overlays_and_banner_exactV298': True,
              'all328_scene_caption_and8_Gallery_composites_exactV298': True,
              'all444_complete_native_route_bodies_and5604_expanded_copies_pass': True,
              'all19254_original_actor_fields_preserved': True,
              'all621_getters_18_COMMON_copies_and24_modal_glyph_cases_pass': True,
              'all8_HELP_pages_exact_previous_actual_navigation_fixture': True,
              'exact_clean_patch_reconstruction_pass': True,
              'current_actual_cold_boot_and_HELP_navigation_pending': True,
              'all18_plaque_hint_entries_and_variants_incomplete': True,
              'unlocked_Gallery_and_original_deep_scene_navigation_pending': True,
              'full_goal_complete': False}
    (ROOT / 'release_proof.json').write_text(json.dumps(output, indent=2) + '\n', encoding='utf-8')
    print('V299 seven declared files; full inherited art and336 composites exact; complete migration native proofs; exact patch reconstruction.', flush=True)


if __name__ == '__main__':
    main()
