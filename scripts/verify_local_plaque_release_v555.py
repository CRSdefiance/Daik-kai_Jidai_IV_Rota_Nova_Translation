"""Verify source margins, whole native plaque crops, retained stack and exact patch."""
import argparse
import json
from pathlib import Path

from PIL import Image

from dk4tool.dialogue.font_audit import GameAsciiFont
from dk4tool.graphics.pxl import PxlImage
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.local_plaque_texture import apply_release
from dk4tool.patch.xdelta import apply_xdelta, make_xdelta
from dk4tool.rom.nds import NdsImage
from scripts.verify_portrait_native_pixels_v202 import native5
from scripts.verify_source_plaque_grain_v542 import capture_report, masks

ROM = Path('out/all_routes_combined_v555_candidate.nds')
ROOT = Path('work/analysis/local_plaque_release_v555')
CAPTURES = Path('E:/Rota Nova translations/Generated/work/emulation_v193')


def read(path):
    return json.loads(Path(path).read_text(encoding='utf-8'))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--static-only', action='store_true')
    args = parser.parse_args()
    current = NdsImage.open(ROM)
    parent = NdsImage.open('out/all_routes_combined_v546_candidate.nds')
    clean = NdsImage.open('work/clean.nds')
    digest = sha(ROM.read_bytes())
    manifest = read(ROM.with_suffix('.manifest.json'))
    prior = read('out/all_routes_combined_v546_candidate.manifest.json')
    stack = read('translations/release_stack.json')
    assert manifest['candidate_sha256'] == digest and manifest['profile'] == 'all-routes-unified-v555'
    assert manifest['release_stack_sha256'] == sha(Path('translations/release_stack.json').read_bytes())
    assert manifest['base_sha256'] == stack['canonical_baseline']['sha256']
    assert manifest['batches'] == prior['batches'] and len(manifest['batches']) == 470
    assert len(stack['accepted_layers']) == 114
    old = {p: d for _, p, d in parent.iter_files()} | dict(parent.iter_components())
    new = {p: d for _, p, d in current.iter_files()} | dict(current.iter_components())
    assert old.keys() == new.keys()
    assert sorted(p for p in old if old[p] != new[p]) == ['/_pxl/dividecrewinfo.pxl', '/_pxl/personinfo.pxl']
    expected, stage = apply_release(parent, clean, 'translations/local_plaque_texture_v1.json')
    assert all(new[p] == d for p, d in expected.items())
    assert sum(r['original_material_pixels_restored'] for r in stage) == 424
    config = read('translations/source_plaque_grain_v1.json')
    font = GameAsciiFont.from_arm9(new['/__arm9__.bin'])
    mask_cases = []
    for group in config['files']:
        path = group['file_path']
        asset = PxlImage.from_bytes(new[path])
        before = PxlImage.from_bytes(old[path])
        assert new[path][:asset.pixels_offset] == old[path][:before.pixels_offset]
        mask_cases.extend(masks(asset, group['records'], font))
    preservation = read('work/analysis/plaque_borders_v546/preservation_proof.json')
    assert len(preservation['entries']) == 921
    assert preservation['candidate_sha256'] == sha(parent.source.read_bytes())
    assert all(old[r['path']] == new[r['path']] for r in preservation['entries']
               if r['path'] not in expected)
    patch = ROM.with_suffix('.xdelta')
    make_xdelta(Path('work/clean.nds'), ROM, patch)
    apply_xdelta(Path('work/clean.nds'), patch, ROOT / 'reconstructed.nds')
    assert (ROOT / 'reconstructed.nds').read_bytes() == ROM.read_bytes()
    result = {'candidate': str(ROM), 'candidate_sha256': digest, 'profile': manifest['profile'],
              'base': manifest['base_rom'], 'base_sha256': manifest['base_sha256'],
              'patch_sha256': sha(patch.read_bytes()), 'exact_clean_patch_reconstruction': True,
              'stage': stage, 'all17_complete_font_masks': mask_cases,
              'all_code_and_other_translations_exact_V546': True,
              'all470_batches114_layers921_preservation_entries_retained': True,
              'experimental': True, 'canonical_promoted': False, 'full_goal_complete': False}
    if args.static_only:
        (ROOT / 'static_release_proof.json').write_text(json.dumps(result, indent=2) + '\n', encoding='utf-8')
        print('V555 static:424 exact source pixels,17 full masks, retained stack and exact patch pass.')
        return
    native = []
    for name, group, frames in zip(('crew', 'person'), config['files'],
                                    ((10000, 10300, 10600), (10500, 12600, 13500, 14400)), strict=True):
        report = capture_report(CAPTURES / f'local_plaque_v555_{name}', digest)
        assert not report.get('battery_save_preloaded')
        shots = {s['frame']: s for s in report['frames_captured']}
        atlas = PxlImage.from_bytes(new[group['file_path']])
        for frame in frames:
            image = Image.open(shots[frame]['path']).convert('RGB')
            for row in group['records']:
                l, t, r, b = row['plaque_box']
                assert all(native5(image.getpixel((x, y))) == native5(atlas.palette[atlas.indices[y * atlas.width + x]])
                           for y in range(t, b) for x in range(l, r)), (name, frame, row['id'])
                native.append({'frame': frame, 'id': row['id'], 'complete_native_plaque_pixels': (r - l) * (b - t),
                               'whole_English_texture_and_border_exact': True, 'fully_completed': False})
    assert len(native) == 61
    fresh = capture_report(CAPTURES / 'local_plaque_v555_fresh', digest)
    previous = capture_report(CAPTURES / 'plaque_borders_v546_fresh', sha(parent.source.read_bytes()))
    assert fresh['scripted_input_schedule'] == previous['scripted_input_schedule']
    assert fresh['core_options'] == previous['core_options']
    assert [s['PNG_sha256'] for s in fresh['frames_captured']] == [s['PNG_sha256'] for s in previous['frames_captured']]
    assert len(fresh['frames_captured']) == 57
    inventory = read('translations/graphics_completion_campaign_v1.json')['plaque_style_v247']['ongoing_plaque_inventory']
    assert len(inventory) == 18 and all(e['fully_completed'] is False for e in inventory)
    assert len(read('translations/graphics_completion_requirements_v313.json')['historical_pending_items_retained']) == 22
    result.update(native_plaque_cases=native, unchanged_regression_captures=57,
                  unchanged_unique_regression_frames=56, all18_plaques_remain_incomplete=True,
                  all22_historical_requirements_retained=True, actual_hardware_or_full_route_claimed=False)
    (ROOT / 'release_proof.json').write_text(json.dumps(result, indent=2) + '\n', encoding='utf-8')
    print('V555:61 whole native plaques,17 full masks,56 unchanged regression frames and exact patch pass.')


if __name__ == '__main__':
    main()
