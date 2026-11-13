"""Verify integrated Guild diplomacy release, inherited patch, and actual complete menu glyphs."""

import argparse
import json
from collections import Counter
from pathlib import Path

from PIL import Image

from dk4tool.dialogue.font_audit import GameAsciiFont
from dk4tool.graphics.pxl import PxlImage
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.guild_diplomacy_labels import apply_release
from dk4tool.patch.xdelta import apply_xdelta, make_xdelta
from dk4tool.rom.nds import NdsImage
from scripts.build_integrated_release import rom_files
from scripts.verify_confirmed_name_widget_pixels_v198 import complete_mask

ROOT = Path('work/analysis/guild_diplomacy_v340')
ROM = Path('out/all_routes_combined_v340_candidate.nds')
PARENT = Path('out/all_routes_combined_v338_candidate.nds')
DONOR = Path('../desmume-0.9.13-win64/Battery/extras_options_sound_common_v6_candidate.dsv')


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
    assert Path('work/analysis/guild_diplomacy_v339/reproduced_v338.nds').read_bytes() == PARENT.read_bytes()
    target, _plan = apply_release(parent.read_file('/__arm9__.bin'), clean.read_file('/__arm9__.bin'),
                                 NdsImage.open('out/raphael_natural_v2_accepted_base.nds').read_file('/__arm9__.bin'),
                                 'translations/guild_diplomacy_labels_release_v2.json')
    assert saved.read_file('/__arm9__.bin') == target
    before, after = rom_files(parent), rom_files(saved)
    assert before.keys() == after.keys()
    assert [p for p in before if before[p] != after[p]] == ['/__arm9__.bin']
    manifest, old = read(ROM.with_suffix('.manifest.json')), read(PARENT.with_suffix('.manifest.json'))
    assert manifest['candidate_sha256'] == sha(ROM.read_bytes())
    assert manifest['release_stack_sha256'] == sha(Path('translations/release_stack.json').read_bytes())
    assert manifest['profile'] == 'all-routes-unified-v340'
    assert manifest['batches'] == old['batches'] and len(manifest['batches']) == 470
    assert manifest['required_batches'] == old['required_batches'] and all(manifest['checks'].values())
    for path, stages in old['relocations'].items():
        for name, value in stages.items():
            assert manifest['relocations'][path][name] == value
    for path, records in old['changed_records'].items():
        extra = ['DK4_GUILD_DIPLOMACY_' + str(i) for i in range(7)] if path == '/__arm9__.bin' else []
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
             'only_ARM9_changed_vs_V338': True, 'exact_V338_reproduction': True,
             'exact_clean_patch_reconstruction': True,
             'native_proof': str(ROOT / 'native_proof.json'), 'startup_proof': str(ROOT / 'startup_proof.json'),
             'actual_old_save_display_verified': False, 'full_goal_complete': False}
    if args.live:
        report, frames = captures(Path('work/emulation_v193/guild_diplomacy_v340'))
        previous, older = captures(Path('work/emulation_v193/regional_maps_v339'))
        assert report['ROM_sha256'] == proof['candidate_sha256'] and report['frames'] == 15800
        assert report['scripted_input_schedule'] == previous['scripted_input_schedule']
        assert report['battery_save_preloaded']['source_sha256'] == sha(DONOR.read_bytes()) == '28ff98d46e3b2ce1b1d9525059988f18a4ddf0d5bedac9140a183285493fdc2e'
        font = GameAsciiFont.from_arm9(target)
        labels = []
        for number, texts in [(7200, ['Send Documents']), (12400, ['Send Documents']),
                              (13400, ['Goodwill', 'Declare War']), (14000, ['Goodwill', 'Declare War'])]:
            shot = Image.open(frames[number]).convert('RGB')
            region = (75, 250, 181, 326)
            colors = [c for c, count in Counter(shot.crop(region).get_flattened_data()).most_common()
                      if max(c) < 80 and max(c) - min(c) < 5]
            for text in texts:
                match = None
                for color in colors:
                    if match:
                        break
                    for y in range(region[1], region[3] - 10):
                        if match:
                            break
                        for x in range(region[0], region[2] - len(text) * 6 + 1):
                            try:
                                ink, bounds = complete_mask(font, text, shot, x, y, color)
                            except ValueError:
                                continue
                            match = {'frame': number, 'English': text, 'ink_pixels': ink,
                                     'bounds': bounds, 'color': color, 'all_letters_and_blank_cells_exact': True}
                            break
                assert match, text
                labels.append(match)
        stable, scoped = [], []
        for number in sorted(set(frames) & set(older)):
            a, b = [Image.open(p).convert('RGB') for p in (older[number], frames[number])]
            differences = [(x, y) for y in range(384) for x in range(256) if a.getpixel((x, y)) != b.getpixel((x, y))]
            if differences:
                assert all(75 <= x < 181 and 250 <= y < 326 for x, y in differences), number
                scoped.append({'frame': number, 'changed_menu_pixels': len(differences)})
            else:
                stable.append(number)
        mystery_path = '/_pxl/mysterymap/10_1.pxl'
        painting = PxlImage.from_bytes(saved.read_file(mystery_path))
        assert saved.read_file(mystery_path) == parent.read_file(mystery_path) == clean.read_file(mystery_path)
        shot = Image.open(frames[15600]).convert('RGB')
        painted = 0
        for i, value in enumerate(painting.indices):
            if value:
                actual = tuple(c >> 3 for c in shot.getpixel((8 + i % painting.width, 18 + i // painting.width)))
                expected = tuple(c >> 3 for c in painting.palette[value][:3])
                assert actual == expected
                painted += 1
        assert painted == 11880
        fresh, fresh_frames = captures(Path('work/emulation_v193/guild_diplomacy_v340_new_game'))
        parent_fresh, parent_frames = captures(Path('work/emulation_v193/legacy_names_v338_new_game'))
        assert fresh['ROM_sha256'] == proof['candidate_sha256'] and fresh['frames'] == 31200
        assert fresh['scripted_input_schedule'] == parent_fresh['scripted_input_schedule']
        comparable = sorted(set(fresh_frames) & set(parent_frames))
        for number in comparable:
            assert Image.open(fresh_frames[number]).tobytes() == Image.open(parent_frames[number]).tobytes(), number
        proof.update(actual_old_save_display_verified=True, actual_menu_labels=labels,
                     changed_pixels_confined_to_actual_popup_menu=scoped,
                     other_ordinary_saved_game_frames_exact=stable, fresh_New_Game_frames_exact=comparable,
                     actual_mystery_map={'path': mystery_path, 'origin': [8, 18], 'exact_nonzero_pixels': painted,
                                        'no_source_Japanese_caption_in_this_painting': True,
                                        'other_maps_and_transparency_composition_not_proven': True},
                     all_seven_caption_native_rasters=14,
                     four_unavailable_diplomacy_commands_actual_display_still_open=True,
                     source_save_unchanged=True, source_save_history_unknown=True,
                     capture_report='work/emulation_v193/guild_diplomacy_v340/capture_report.json')
    (ROOT / 'release_proof.json').write_text(json.dumps(proof, indent=2) + '\n', encoding='utf-8')
    print(json.dumps({'candidate_sha256': proof['candidate_sha256'], 'patch_sha256': proof['patch_sha256'],
                      'live_display_verified': proof['actual_old_save_display_verified']}))


if __name__ == '__main__':
    main()
