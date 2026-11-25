"""Verify isolated banner changes, exact patch and ordinary complete frame replay."""

import json
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

from dk4tool.graphics.pxl import PxlImage
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.xdelta import apply_xdelta, make_xdelta
from dk4tool.rom.nds import NdsImage
from scripts.build_integrated_release import rom_files
from scripts.verify_portrait_native_pixels_v202 import native5
from scripts.verify_source_plaque_grain_v542 import capture_report

ROOT = Path('work/analysis/action_consumers_v563')
ROM = Path('out/all_routes_combined_v564_candidate.nds')
PARENT = Path('out/all_routes_combined_v558_candidate.nds')
CAPTURE = Path('E:/Rota Nova translations/Generated/work/emulation_v193')
FILE = '/_pxl/tempcargo.pxl'


def read(path):
    return json.loads(Path(path).read_text(encoding='utf-8'))


def main():
    digest = sha(ROM.read_bytes())
    current, old, clean = (NdsImage.open(p) for p in (ROM, PARENT, Path('work/clean.nds')))
    before, after = rom_files(old), rom_files(current)
    assert before.keys() == after.keys() and [p for p in before if before[p] != after[p]] == [FILE]
    image, original = PxlImage.from_bytes(after[FILE]), PxlImage.from_bytes(clean.read_file(FILE))
    inherited = PxlImage.from_bytes(before[FILE])
    assert image.source[:image.pixels_offset] == original.source[:original.pixels_offset]
    assert image.source == (ROOT/'tempcargo_RESEARCH_ONLY.pxl').read_bytes()
    prototype = read(ROOT/'temporary_storage_prototype.json')
    english = {n for n, value in enumerate(image.indices) if value == 15}
    assert english == {n for n, value in enumerate(inherited.indices) if value == 15}
    # Independently lay out the complete original authored English font, including
    # first/final glyphs and blank cells; do not infer text from an output mask.
    font = ImageFont.load_default(size=11)
    bounds = font.getbbox('Temporary Storage')
    mask = Image.new('L', (128, 16))
    ImageDraw.Draw(mask).text(((128-bounds[2]+bounds[0])//2-bounds[0],
                              (16-bounds[3]+bounds[1])//2-bounds[1]),
                             'Temporary Storage', font=font, fill=255)
    expected = {y*256+x+1 for y in range(16) for x in range(128) if mask.getpixel((x, y)) >= 128}
    assert english == expected and len(english) == 241
    assert sum(a != b for a, b in zip(inherited.indices, image.indices, strict=True)) == 275
    manifest = read(ROM.with_suffix('.manifest.json'))
    stack = read('translations/release_stack.json')
    prior_manifest = read(PARENT.with_suffix('.manifest.json'))
    assert manifest['profile'] == 'all-routes-unified-v564'
    assert manifest['release_stack_sha256'] == sha(Path('translations/release_stack.json').read_bytes())
    assert manifest['candidate_sha256'] == digest and manifest['base_sha256'] == prior_manifest['base_sha256']
    assert manifest['batches'] == prior_manifest['batches'] and len(manifest['batches']) == 470
    assert manifest['required_batches'] == prior_manifest['required_batches'] and len(stack['accepted_layers']) == 114
    stage = manifest['relocations'][FILE]['cargo_banner_texture']
    assert stage['target_sha256'] == sha(after[FILE]) and stage['changed_pixels'] == 275
    patch = ROM.with_suffix('.xdelta')
    make_xdelta(Path('work/clean.nds'), ROM, patch)
    reconstructed = ROOT/'v564_reconstructed.nds'
    apply_xdelta(Path('work/clean.nds'), patch, reconstructed)
    assert reconstructed.read_bytes() == ROM.read_bytes()
    control = capture_report(CAPTURE/'action_consumers_v563_navigation', sha(PARENT.read_bytes()))
    actual = capture_report(CAPTURE/'cargo_banner_v564_actual', digest)
    assert actual['frames'] == control['frames'] == 4600
    assert actual['scripted_input_schedule'] == control['scripted_input_schedule']
    assert actual['core_options'] == control['core_options']
    assert actual['battery_save_preloaded']['source_sha256'] == control['battery_save_preloaded']['source_sha256']
    assert not any(actual.get(k) for k in ('synthetic_location_fixtures', 'synthetic_inventory_fixtures',
                                         'synthetic_condition_fixtures', 'synthetic_gallery_fixtures'))
    source_save = Path(actual['battery_save_preloaded']['source'])
    assert sha(source_save.read_bytes()) == actual['battery_save_preloaded']['source_sha256']
    tables = [{r['frame']: r for r in report['frames_captured']} for report in (control, actual)]
    cases = []
    for frame in (4300, 4600):
        shots = [Image.open(table[frame]['path']).convert('RGB') for table in tables]
        assert all(im.size == (256, 384) for im in shots)
        changed = 0
        for y in range(384):
            for x in range(256):
                expected_pixel = native5(shots[0].getpixel((x, y)))
                if 261 <= y < 277:
                    n = (y-261)*256+x
                    assert expected_pixel == native5(inherited.palette[inherited.indices[n]])
                    expected_pixel = native5(image.palette[image.indices[n]])
                assert native5(shots[1].getpixel((x, y))) == expected_pixel, (frame, x, y)
                changed += shots[0].getpixel((x, y)) != shots[1].getpixel((x, y))
        assert changed == 275
        cases.append({'frame': frame, 'complete_both_screen_pixels_exact': 98304,
                      'complete_banner_pixels_exact': 4096, 'changed_pixels_only_in_reviewed_banner': changed,
                      'all241_complete_English_ink_points_visible': True})
    fresh = capture_report(CAPTURE/'cargo_banner_v564_fresh', digest)
    prior_fresh = capture_report(CAPTURE/'name_gradient_v558_fresh', sha(PARENT.read_bytes()))
    assert fresh['frames'] == prior_fresh['frames'] == 21200
    assert fresh['scripted_input_schedule'] == prior_fresh['scripted_input_schedule']
    assert fresh['core_options'] == prior_fresh['core_options']
    assert [r['PNG_sha256'] for r in fresh['frames_captured']] == [r['PNG_sha256'] for r in prior_fresh['frames_captured']]
    assert len({r['frame'] for r in fresh['frames_captured']}) == 56
    for name in ('graphics_completion_campaign_v1.json', 'graphics_visual_audit_v150.json'):
        plaques = read(Path('translations')/name)['plaque_style_v247']['ongoing_plaque_inventory']
        assert len(plaques) == 18 and all(row['fully_completed'] is False for row in plaques)
    assert len(read('translations/graphics_completion_requirements_v313.json')['historical_pending_items_retained']) == 22
    proof = {'candidate': str(ROM), 'candidate_sha256': digest, 'base': manifest['base_rom'],
             'base_sha256': manifest['base_sha256'], 'profile': manifest['profile'],
             'patch_sha256': sha(patch.read_bytes()), 'clean_patch_source_sha256': sha(Path('work/clean.nds').read_bytes()),
             'exact_clean_patch_reconstruction': True, 'only_internal_file_changed_from_V558': FILE,
             'all_code_and_other_translations_exact_V558': True, 'all470_batches114_layers_retained': True,
             'reviewed_reconstruction_audit': {k: v for k, v in prototype.items()
                                               if k not in ('research_only', 'production_ROM_changed')}, 'actual_cases': cases,
             'complete_native_banner_pixels_verified': 8192, 'complete_native_screen_pixels_verified': 196608,
             'unchanged_unique_startup_frames': 56, 'source_save_unchanged': True,
             'ordinary_copied_save_without_fixtures': True, 'experimental': True, 'canonical_promoted': False,
             'production_ROM_changed': True,
             'other5_miniature_caption_native_consumers_remain_open': True,
             'all18_plaques_remain_incomplete': True, 'hardware_or_full_route_verified': False,
             'full_goal_complete': False}
    (ROOT/'v564_release_proof.json').write_text(json.dumps(proof, indent=2)+'\n', encoding='utf-8')
    print('V564:275 banner pixels corrected;2 full native screens,8192 banner pixels,241 complete ink points,56 unchanged startup frames and exact patch pass.')


if __name__ == '__main__':
    main()
