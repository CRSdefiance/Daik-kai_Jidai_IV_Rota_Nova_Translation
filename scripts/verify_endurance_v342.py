"""Verify integrated Faithful Endurance approximation, inherited release, and actual crew panels."""

import argparse
import json
from pathlib import Path

from PIL import Image

from dk4tool.dialogue.font_audit import GameAsciiFont
from dk4tool.graphics.pxl import PxlImage
from dk4tool.patch.endurance_approximation import apply_release
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.xdelta import apply_xdelta, make_xdelta
from dk4tool.rom.nds import NdsImage
from scripts.build_integrated_release import rom_files

ROOT = Path('work/analysis/plaque_review_v342')
ROM = Path('out/all_routes_combined_v342_candidate.nds')
PARENT = Path('out/all_routes_combined_v341_candidate.nds')


def read(path):
    return json.loads(Path(path).read_text(encoding='utf-8'))


def captures(folder):
    report_path = folder / 'capture_report.json'
    report = read(report_path)
    assert report['cold_boot'] and not report['savestate_loaded'] and not report['callback_errors']
    frames = {}
    for row in report['frames_captured']:
        path = Path(row['path'])
        assert sha(path.read_bytes()) == row['PNG_sha256']
        frames[row['frame']] = path
    return report, frames


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--live', action='store_true')
    args = parser.parse_args()
    parent, saved, clean = [NdsImage.open(p) for p in (PARENT, ROM, Path('work/clean.nds'))]
    assert (ROOT / 'reproduced_v341.nds').read_bytes() == PARENT.read_bytes()
    target, _plan = apply_release(parent.read_file('/__arm9__.bin'), clean.read_file('/__arm9__.bin'),
                                 NdsImage.open('out/raphael_natural_v2_accepted_base.nds').read_file('/__arm9__.bin'),
                                 'translations/endurance_approximation_release_v1.json')
    assert saved.read_file('/__arm9__.bin') == target
    before, after = rom_files(parent), rom_files(saved)
    assert before.keys() == after.keys()
    assert [p for p in before if before[p] != after[p]] == ['/__arm9__.bin']
    manifest, old = read(ROM.with_suffix('.manifest.json')), read(PARENT.with_suffix('.manifest.json'))
    assert manifest['candidate_sha256'] == sha(ROM.read_bytes())
    assert manifest['release_stack_sha256'] == sha(Path('translations/release_stack.json').read_bytes())
    assert manifest['profile'] == 'all-routes-unified-v342'
    assert manifest['batches'] == old['batches'] and len(manifest['batches']) == 470
    assert manifest['required_batches'] == old['required_batches'] and all(manifest['checks'].values())
    for path, stages in old['relocations'].items():
        for name, value in stages.items():
            assert manifest['relocations'][path][name] == value
    for path, records in old['changed_records'].items():
        extra = ['DK4_ENDURANCE_APPROXIMATION_MARKER'] if path == '/__arm9__.bin' else []
        assert manifest['changed_records'][path] == records + extra
    patch = ROM.with_suffix('.xdelta')
    if not patch.exists():
        make_xdelta(Path('work/clean.nds'), ROM, patch)
    reconstruction = ROOT / 'patch_reconstruction.nds'
    apply_xdelta(Path('work/clean.nds'), patch, reconstruction)
    assert reconstruction.read_bytes() == ROM.read_bytes()
    proof = {'candidate': str(ROM), 'candidate_sha256': sha(ROM.read_bytes()),
             'patch': str(patch), 'patch_sha256': sha(patch.read_bytes()),
             'profile': manifest['profile'], 'base': manifest['base_rom'], 'base_sha256': manifest['base_sha256'],
             'all470_batches_required_layers_prior_stages_records_preserved': True,
             'only_ARM9_changed_vs_V341': True, 'exact_V341_reproduction': True,
             'exact_clean_patch_reconstruction': True,
             'native_proof': str(ROOT / 'native_proof.json'), 'startup_proof': str(ROOT / 'startup_proof.json'),
             'actual_duration_display_verified': False, 'full_goal_complete': False}
    if args.live:
        report, frames = captures(Path('work/emulation_v193/endurance_v342'))
        previous, older = captures(Path('work/emulation_v193/endurance_v342_parent'))
        assert report['ROM_sha256'] == proof['candidate_sha256'] and report['frames'] == 11200
        assert previous['ROM_sha256'] == sha(PARENT.read_bytes())
        assert report['scripted_input_schedule'] == previous['scripted_input_schedule']
        font = GameAsciiFont.from_arm9(target)
        batch = read('translations/assign_sailors_graphics_v5.json')
        asset = PxlImage.from_bytes(saved.read_file(batch['file_path']))
        plaques, captions = [], []
        for number in (9900, 10200, 10500):
            shot = Image.open(frames[number]).convert('RGB')
            # This is ordinary game output; the duration's numeric value is not forced.
            from scripts.verify_plaque_release_v247 import find_mask

            caption = find_mask(font, '~0 days', shot, (85, 37, 230, 61))
            captions.append({'frame': number, **caption})
            for row in batch['records']:
                left, top, right, bottom = row['plaque_box']
                for y in range(top, bottom):
                    for x in range(left, right):
                        actual = tuple(value >> 3 for value in shot.getpixel((x, y)))
                        expected = tuple(value >> 3 for value in asset.palette[asset.indices[y * asset.width + x]][:3])
                        assert actual == expected
                plaques.append({'frame': number, 'label': row['text'], 'fully_completed': False,
                                'all_pixels_source_exact': True})
        stable, changed = [], []
        for number in sorted(set(frames) & set(older)):
            a, b = [Image.open(p).convert('RGB') for p in (older[number], frames[number])]
            differences = [(x, y) for y in range(384) for x in range(256) if a.getpixel((x, y)) != b.getpixel((x, y))]
            if differences:
                assert all(85 <= x < 230 and 37 <= y < 61 for x, y in differences), number
                changed.append({'frame': number, 'changed_duration_pixels': len(differences)})
            else:
                stable.append(number)
        proof.update(actual_duration_display_verified=True, actual_duration_captions=captions,
                     actual21_plaque_instances=plaques, unchanged_fresh_game_frames=stable,
                     differences_only_in_duration_row=changed,
                     ordinary_new_game_title_character_opening_town_and_crew_navigation=True,
                     all18_plaques_and_variants_still_incomplete=True,
                     actual_saved_game_or_nonzero_duration_not_claimed=True)
    (ROOT / 'release_proof.json').write_text(json.dumps(proof, indent=2) + '\n', encoding='utf-8')
    print(json.dumps({'candidate_sha256': proof['candidate_sha256'], 'patch_sha256': proof['patch_sha256'],
                      'live_display_verified': proof['actual_duration_display_verified']}))


if __name__ == '__main__':
    main()
