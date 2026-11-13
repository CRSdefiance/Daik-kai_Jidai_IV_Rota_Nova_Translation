"""Verify integrated Complete roster role crop, inherited release, and actual First Mate pixels."""

import argparse
import json
from pathlib import Path

from PIL import Image

from dk4tool.dialogue.font_audit import GameAsciiFont
from dk4tool.graphics.pxl import PxlImage
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.roster_role_crop import apply_release
from dk4tool.patch.xdelta import apply_xdelta, make_xdelta
from dk4tool.rom.nds import NdsImage
from scripts.build_integrated_release import rom_files
from scripts.verify_confirmed_name_widget_pixels_v198 import complete_mask

ROOT = Path('work/analysis/roster_role_crop_v341')
ROM = Path('out/all_routes_combined_v341_candidate.nds')
PARENT = Path('out/all_routes_combined_v340_candidate.nds')
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
    assert (ROOT / 'reproduced_v340.nds').read_bytes() == PARENT.read_bytes()
    target, _plan = apply_release(parent.read_file('/__arm9__.bin'), clean.read_file('/__arm9__.bin'),
                                 NdsImage.open('out/raphael_natural_v2_accepted_base.nds').read_file('/__arm9__.bin'),
                                 'translations/roster_role_crop_release_v1.json')
    assert saved.read_file('/__arm9__.bin') == target
    before, after = rom_files(parent), rom_files(saved)
    assert before.keys() == after.keys()
    assert [p for p in before if before[p] != after[p]] == ['/__arm9__.bin']
    manifest, old = read(ROM.with_suffix('.manifest.json')), read(PARENT.with_suffix('.manifest.json'))
    assert manifest['candidate_sha256'] == sha(ROM.read_bytes())
    assert manifest['release_stack_sha256'] == sha(Path('translations/release_stack.json').read_bytes())
    assert manifest['profile'] == 'all-routes-unified-v341'
    assert manifest['batches'] == old['batches'] and len(manifest['batches']) == 470
    assert manifest['required_batches'] == old['required_batches'] and all(manifest['checks'].values())
    for path, stages in old['relocations'].items():
        for name, value in stages.items():
            assert manifest['relocations'][path][name] == value
    for path, records in old['changed_records'].items():
        extra = ['DK4_ROSTER_ROLE_COMPLETE_CROP'] if path == '/__arm9__.bin' else []
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
             'only_ARM9_changed_vs_V340': True, 'exact_V340_reproduction': True,
             'exact_clean_patch_reconstruction': True,
             'native_proof': str(ROOT / 'native_proof.json'), 'startup_proof': str(ROOT / 'startup_proof.json'),
             'actual_old_save_display_verified': False, 'full_goal_complete': False}
    if args.live:
        report, frames = captures(Path('work/emulation_v193/roster_role_crop_v341'))
        previous, older = captures(Path('work/emulation_v193/conditional_guild_v341'))
        assert report['ROM_sha256'] == proof['candidate_sha256'] and report['frames'] == 19800
        assert report['scripted_input_schedule'] == previous['scripted_input_schedule']
        assert report['battery_save_preloaded']['source_sha256'] == sha(DONOR.read_bytes()) == '28ff98d46e3b2ce1b1d9525059988f18a4ddf0d5bedac9140a183285493fdc2e'
        font = GameAsciiFont.from_arm9(target)
        image = Image.open(frames[17800]).convert('RGB')
        ink, bounds = complete_mask(font, 'First Mate', image, 12, 316, (230, 230, 230))
        old_image = Image.open(older[17800]).convert('RGB')
        old_ink, old_bounds = complete_mask(font, 'First Ma', old_image, 12, 316, (230, 230, 230))
        stable, changed = [], []
        for number in sorted(set(frames) & set(older)):
            a, b = [Image.open(p).convert('RGB') for p in (older[number], frames[number])]
            differences = [(x, y) for y in range(384) for x in range(256) if a.getpixel((x, y)) != b.getpixel((x, y))]
            if differences:
                assert all(12 <= x < 216 and 316 <= y < 328 for x, y in differences), number
                changed.append({'frame': number, 'changed_role_pixels': len(differences)})
            else:
                stable.append(number)
        batch = read('translations/person_info_graphics_v3.json')
        asset = PxlImage.from_bytes(saved.read_file(batch['file_path']))
        plaques = []
        for number in (17600, 18200, 19600):
            shot = Image.open(frames[number]).convert('RGB')
            for row in batch['records']:
                left, top, right, bottom = row['plaque_box']
                for y in range(top, bottom):
                    for x in range(left, right):
                        actual = tuple(value >> 3 for value in shot.getpixel((x, y)))
                        expected = tuple(value >> 3 for value in asset.palette[asset.indices[y * asset.width + x]][:3])
                        assert actual == expected, (number, row['text'], x, y)
                plaques.append({'frame': number, 'label': row['text'], 'all_pixels_exact': True,
                                'fully_completed': False})
        fresh, fresh_frames = captures(Path('work/emulation_v193/roster_role_crop_v341_new_game'))
        parent_fresh, parent_frames = captures(Path('work/emulation_v193/guild_diplomacy_v340_new_game'))
        assert fresh['ROM_sha256'] == proof['candidate_sha256'] and fresh['frames'] == 31200
        assert fresh['scripted_input_schedule'] == parent_fresh['scripted_input_schedule']
        comparable = sorted(set(fresh_frames) & set(parent_frames))
        for number in comparable:
            assert Image.open(fresh_frames[number]).tobytes() == Image.open(parent_frames[number]).tobytes(), number
        proof.update(actual_old_save_display_verified=True,
                     actual_First_Mate={'bounds': bounds, 'complete_ink_pixels': ink,
                                       'all_first_internal_final_letters_and_blank_cells_exact': True},
                     old_truncated_role={'text': 'First Ma', 'bounds': old_bounds, 'ink_pixels': old_ink},
                     changed_pixels_confined_to_role_row=changed,
                     other_ordinary_saved_game_frames_exact=stable, fresh_New_Game_frames_exact=comparable,
                     actual_30_plaque_instances=plaques,
                     all18_plaques_and_variants_still_incomplete=True,
                     source_save_unchanged=True, source_save_history_unknown=True,
                     capture_report='work/emulation_v193/roster_role_crop_v341/capture_report.json')
    (ROOT / 'release_proof.json').write_text(json.dumps(proof, indent=2) + '\n', encoding='utf-8')
    print(json.dumps({'candidate_sha256': proof['candidate_sha256'], 'patch_sha256': proof['patch_sha256'],
                      'live_display_verified': proof['actual_old_save_display_verified']}))


if __name__ == '__main__':
    main()
