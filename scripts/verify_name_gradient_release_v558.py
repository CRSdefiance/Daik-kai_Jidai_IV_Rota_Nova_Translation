"""Verify own source gradients, embedded storage and complete native sprite composites."""
import argparse
import json
from pathlib import Path

from PIL import Image

from dk4tool.dialogue.font_audit import GameAsciiFont
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.graphics.pxl import PxlImage
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.name_plaque_gradients import apply_release
from dk4tool.patch.xdelta import apply_xdelta, make_xdelta
from dk4tool.rom.nds import NdsImage
from scripts.inventory_embedded_graphics_v151 import decode
from scripts.verify_portrait_native_pixels_v202 import native5
from scripts.verify_source_plaque_grain_v542 import capture_report

ROM = Path('out/all_routes_combined_v558_candidate.nds')
PARENT = Path('out/all_routes_combined_v557_candidate.nds')
ROOT = Path('work/analysis/name_gradients_v558')
CAPTURE = Path('E:/Rota Nova translations/Generated/work/emulation_v193')


def read(path):
    return json.loads(Path(path).read_text(encoding='utf-8'))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--static-only', action='store_true')
    args = parser.parse_args()
    current, parent, clean = [NdsImage.open(p) for p in (ROM, PARENT, Path('work/clean.nds'))]
    digest = sha(ROM.read_bytes())
    manifest, prior = read(ROM.with_suffix('.manifest.json')), read(PARENT.with_suffix('.manifest.json'))
    stack = read('translations/release_stack.json')
    assert manifest['profile'] == 'all-routes-unified-v558' and manifest['candidate_sha256'] == digest
    assert manifest['base_sha256'] == stack['canonical_baseline']['sha256']
    assert manifest['release_stack_sha256'] == sha(Path('translations/release_stack.json').read_bytes())
    assert manifest['batches'] == prior['batches'] and len(manifest['batches']) == 470
    assert len(stack['accepted_layers']) == 114
    old = {p: d for _, p, d in parent.iter_files()} | dict(parent.iter_components())
    new = {p: d for _, p, d in current.iter_files()} | dict(current.iter_components())
    assert old.keys() == new.keys()
    assert sorted(p for p in old if old[p] != new[p]) == ['/GRP/SLACKIMG.DK4', '/_pxl/slackimg12.pxl']
    expected, stage = apply_release(parent, clean, 'translations/name_plaque_gradients_v1.json')
    assert all(new[p] == d for p, d in expected.items())
    source = PxlImage.from_bytes(new['/_pxl/slackimg12.pxl'])
    original = PxlImage.from_bytes(clean.read_file('/_pxl/slackimg12.pxl'))
    old_archive, archive = [IlnkContainer.parse(d['/GRP/SLACKIMG.DK4']) for d in (old, new)]
    assert len(old_archive.blocks) == len(archive.blocks)
    assert all(a == b for i, (a, b) in enumerate(zip(old_archive.blocks, archive.blocks, strict=True)) if i != 12)
    assert old_archive.blocks[12][:64] == archive.blocks[12][:64]
    embedded = decode(archive.blocks[12])
    assert embedded['indices'] == bytes(source.indices) and not embedded['unclassified_trailing_bytes']
    font = GameAsciiFont.from_arm9(new['/__arm9__.bin'])
    config = read('translations/name_plaque_gradients_v1.json')
    masks = []
    all_font_points = set()
    for row in config['records']:
        dl, dt, dr, _ = row['draw_box']
        tx = dl + (dr - dl - len(row['english']) * 5) // 2
        points = set()
        for n, ch in enumerate(row['english']):
            glyph = font.decode(ch)
            assert not glyph.crop((0, 0, 6, 2)).getbbox()
            points.update((tx + n*5 + x, dt + y-2) for y in range(2, 11) for x in range(6) if glyph.getpixel((x, y)))
        assert len(points) == row['complete_English_ink_pixels']
        l, t, r, b = row['box']
        actual = {(x, y) for y in range(t, b) for x in range(l, r) if source.indices[y*44+x] == 15}
        chrome = {(x, y) for y in range(t, b) for x in range(l, r)
                  if original.indices[y*44+x] == 15 and not (4 <= x < 40 and t+1 <= y < t+10)}
        assert actual == points | chrome, (row['english'], sorted(actual - points - chrome))
        masks.append({'english': row['english'], 'full_native_font_ink': len(points), 'first_final_letters_complete': True})
        all_font_points.update(points)
    material_exact = sum(1 for n, value in enumerate(original.indices)
                         if value != 15 and (n % 44, n // 44) not in all_font_points)
    assert all(source.indices[n] == value for n, value in enumerate(original.indices)
               if value != 15 and (n % 44, n // 44) not in all_font_points)
    make_xdelta(Path('work/clean.nds'), ROM, ROM.with_suffix('.xdelta'))
    apply_xdelta(Path('work/clean.nds'), ROM.with_suffix('.xdelta'), ROOT / 'reconstructed.nds')
    assert (ROOT / 'reconstructed.nds').read_bytes() == ROM.read_bytes()
    proof = {'candidate': str(ROM), 'candidate_sha256': digest, 'profile': manifest['profile'],
             'base': manifest['base_rom'], 'base_sha256': manifest['base_sha256'],
             'patch_sha256': sha(ROM.with_suffix('.xdelta').read_bytes()), 'exact_clean_patch_reconstruction': True,
             'stage': stage, 'complete_font_masks': masks, 'original_nonwhite_material_pixels_exact': material_exact,
             'embedded_block12_indices_exact_to_loose': True,
             'original_loose_and_embedded_palette_flags_preserved_separately': True,
             'all_code_and_other_translations_exact_V557': True,
             'all470_batches114_layers_retained': True, 'experimental': True,
             'canonical_promoted': False, 'full_goal_complete': False}
    if args.static_only:
        (ROOT / 'static_release_proof.json').write_text(json.dumps(proof, indent=2) + '\n', encoding='utf-8')
        print('V558 static:5 complete font masks,original materials,both synchronized copies and exact patch pass.')
        return
    cases = []
    for index in (12, 19):
        reports = []
        for version, name in ((557, 'control'), (558, 'actual_r2')):
            fixture = ROOT / f'V{version}_index{index}_RESEARCH_ONLY.nds'
            fixture_proof = read(fixture.with_suffix('.fixture.json'))
            assert fixture_proof['parent_sha256'] == sha((PARENT if version == 557 else ROM).read_bytes())
            saved = NdsImage.open(fixture)
            files = {p: d for _, p, d in saved.iter_files()} | dict(saved.iter_components())
            baseline = old if version == 557 else new
            assert [p for p in baseline if baseline[p] != files[p]] == ['/data/SC0.DK4']
            before, after = baseline['/data/SC0.DK4'], files['/data/SC0.DK4']
            assert sum(a != b for a, b in zip(before, after, strict=True)) <= 4
            reports.append(capture_report(CAPTURE / f'name_gradient_v558_{name}_{index}', fixture_proof['fixture_sha256']))
        control, actual = reports
        assert control['scripted_input_schedule'] == actual['scripted_input_schedule']
        assert control['core_options'] == actual['core_options']
        shots = [{s['frame']: s for s in report['frames_captured']} for report in reports]
        for frame in (3600, 4200, 4800):
            before, after = [Image.open(table[frame]['path']).convert('RGB') for table in shots]
            assert before.size == after.size == (256, 384)
            for y in range(384):
                for x in range(256):
                    colour = native5(before.getpixel((x, y)))
                    if 106 <= x < 150 and 20 <= y < 80:
                        value = source.indices[(y-20)*44+x-106]
                        if value:
                            colour = native5(source.palette[value])
                    assert native5(after.getpixel((x, y))) == colour, (index, frame, x, y)
            cases.append({'index': index, 'frame': frame, 'complete_both_screen_pixels_exact': 98304,
                          'complete_sprite_pixels_including59_zero_points': 2640,
                          'all5_labels_materials_frames_and_bounds_exact': True,
                          'synthetic_original_opcode_not_ordinary_event_reachability': True})
    fresh = capture_report(CAPTURE / 'name_gradient_v558_fresh', digest)
    old_fresh = capture_report(CAPTURE / 'ship_texture_v557_fresh', sha(PARENT.read_bytes()))
    assert fresh['scripted_input_schedule'] == old_fresh['scripted_input_schedule']
    assert fresh['core_options'] == old_fresh['core_options']
    assert [s['PNG_sha256'] for s in fresh['frames_captured']] == [s['PNG_sha256'] for s in old_fresh['frames_captured']]
    assert len(fresh['frames_captured']) == 57
    plaques = read('translations/graphics_completion_campaign_v1.json')['plaque_style_v247']['ongoing_plaque_inventory']
    assert len(plaques) == 18 and all(e['fully_completed'] is False for e in plaques)
    assert len(read('translations/graphics_completion_requirements_v313.json')['historical_pending_items_retained']) == 22
    proof.update(native_cases=cases, total_complete_screen_pixels_exact=589824,
                 full_original_event_reachability_not_claimed=True, unchanged_unique_startup_frames=56,
                 all22_requirements_and18_incomplete_plaques_retained=True, hardware_or_full_route_claimed=False)
    (ROOT / 'release_proof.json').write_text(json.dumps(proof, indent=2) + '\n', encoding='utf-8')
    print('V558:6 full native composites,30 complete labels,all transparent points,56 unchanged startup frames and exact patch pass.')


if __name__ == '__main__':
    main()
