"""Verify integrated legacy saved-name repair, patch, and actual GPU lettering."""

import argparse
import json
from pathlib import Path

from PIL import Image

from dk4tool.dialogue.font_audit import GameAsciiFont
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.legacy_saved_item_names import apply_release
from dk4tool.patch.xdelta import apply_xdelta, make_xdelta
from dk4tool.rom.nds import NdsImage
from scripts.build_integrated_release import rom_files

ROOT = Path('work/analysis/legacy_names_v338')
ROM = Path('out/all_routes_combined_v338_candidate.nds')
PARENT = Path('out/all_routes_combined_v326_candidate.nds')
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
    assert (ROOT / 'reproduced_v326.nds').read_bytes() == PARENT.read_bytes()
    target, _plan = apply_release(parent.read_file('/__arm9__.bin'), clean.read_file('/__arm9__.bin'),
                                 'translations/legacy_saved_item_names_release_v1.json')
    assert saved.read_file('/__arm9__.bin') == target
    before, after = rom_files(parent), rom_files(saved)
    assert before.keys() == after.keys()
    assert [p for p in before if before[p] != after[p]] == ['/__arm9__.bin']
    manifest, old = read(ROM.with_suffix('.manifest.json')), read(PARENT.with_suffix('.manifest.json'))
    assert manifest['candidate_sha256'] == sha(ROM.read_bytes())
    assert manifest['release_stack_sha256'] == sha(Path('translations/release_stack.json').read_bytes())
    assert manifest['profile'] == 'all-routes-unified-v338'
    assert manifest['batches'] == old['batches'] and len(manifest['batches']) == 470
    assert manifest['required_batches'] == old['required_batches'] and all(manifest['checks'].values())
    for path, stages in old['relocations'].items():
        for name, value in stages.items():
            assert manifest['relocations'][path][name] == value
    for path, records in old['changed_records'].items():
        extra = ['DK4_LEGACY_SAVED_PROMOTIONAL_NAMES'] if path == '/__arm9__.bin' else []
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
             'only_ARM9_changed_vs_V326': True, 'exact_V326_reproduction': True,
             'exact_clean_patch_reconstruction': True,
             'native_proof': str(ROOT / 'native_proof.json'), 'startup_proof': str(ROOT / 'startup_proof.json'),
             'actual_old_save_display_verified': False, 'full_goal_complete': False}
    if args.live:
        report, frames = captures(Path('work/emulation_v193/legacy_names_v338'))
        previous, older = captures(Path('work/emulation_v193/ordinary_map_v338'))
        assert report['ROM_sha256'] == proof['candidate_sha256']
        assert report['scripted_input_schedule'] == previous['scripted_input_schedule']
        assert report['battery_save_preloaded']['source_sha256'] == sha(DONOR.read_bytes()) == '28ff98d46e3b2ce1b1d9525059988f18a4ddf0d5bedac9140a183285493fdc2e'
        image = Image.open(frames[7800]).convert('RGB')
        font = GameAsciiFont.from_arm9(target)
        labels = []
        for text, x, y, right in [('Gem-Eating Gem Map 1', 56, 24, 232), ('Ancient Map', 8, 64, 88),
                                   ('Map fragment. Collect all four.', 8, 112, 232)]:
            expected = {(x + n * 5 + gx, y + gy) for n, ch in enumerate(text)
                        for gy in range(11) for gx in range(6) if font.decode(ch).getpixel((gx, gy))}
            actual = {(xx, yy) for yy in range(y, y + 11) for xx in range(x, right)
                      if min(image.getpixel((xx, yy))) > 200
                      and max(image.getpixel((xx, yy))) - min(image.getpixel((xx, yy))) < 5}
            assert actual == expected, (text, len(actual), len(expected))
            labels.append({'text': text, 'complete_ink_pixels': len(expected), 'advance': 5,
                           'all_leading_internal_trailing_pixels_and_blank_cells_exact': True})
        old_image = Image.open(older[7800]).convert('RGB')
        differences = [(x, y) for y in range(384) for x in range(256) if image.getpixel((x, y)) != old_image.getpixel((x, y))]
        assert differences and all(56 <= x < 232 and 24 <= y < 36 for x, y in differences)
        compared = []
        for number in sorted(set(frames) & set(older)):
            if number <= 7600:
                assert Image.open(frames[number]).tobytes() == Image.open(older[number]).tobytes(), number
                compared.append(number)
        fresh, fresh_frames = captures(Path('work/emulation_v193/legacy_names_v338_new_game'))
        parent_fresh, parent_frames = captures(Path('work/emulation_v193/crew_roles_v326_new_game'))
        assert fresh['ROM_sha256'] == proof['candidate_sha256'] and fresh['frames'] == 31200
        assert fresh['scripted_input_schedule'] == parent_fresh['scripted_input_schedule']
        comparable = sorted(set(fresh_frames) & set(parent_frames))
        for number in comparable:
            assert Image.open(fresh_frames[number]).tobytes() == Image.open(parent_frames[number]).tobytes(), number
        proof.update(actual_old_save_display_verified=True, actual_labels=labels,
                     changed_title_pixels=len(differences), all_other_map_screen_pixels_exact=True,
                     prior_saved_game_frames_exact=compared, fresh_New_Game_frames_exact=comparable,
                     source_save_unchanged=True, source_save_history_unknown=True,
                     capture_report='work/emulation_v193/legacy_names_v338/capture_report.json')
    (ROOT / 'release_proof.json').write_text(json.dumps(proof, indent=2) + '\n', encoding='utf-8')
    print(json.dumps({'candidate_sha256': proof['candidate_sha256'], 'patch_sha256': proof['patch_sha256'],
                      'live_display_verified': proof['actual_old_save_display_verified']}))


if __name__ == '__main__':
    main()
