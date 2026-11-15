"""Verify actual minimum/full stat display, plaques, hints and complete restoration."""

from pathlib import Path

from ndspy.code import MainCodeFile
from PIL import Image, ImageDraw

from dk4tool.dialogue.font_audit import GameAsciiFont
from dk4tool.graphics.pxl import PxlImage
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.main_pool_cache_visibility import POOL
from dk4tool.rom.nds import NdsImage
from scripts.inspect_committed_gpu_v646 import CORE_SHA
from scripts.run_stat_plaques_v728 import CAP, FRAMES, ROM, ROOT, actor_stats
from scripts.verify_confirmed_name_widget_pixels_v198 import complete_mask
from scripts.verify_portrait_native_pixels_v202 import native5
from scripts.verify_short_equipment_release_v252 import numeric_field
from scripts.verify_source_plaque_bevels_v546 import hint
from scripts.verify_source_plaque_grain_v542 import masks
from scripts.verify_village_wrap_v608 import read, save

COLOR = (230, 230, 230)
SKILLS = [('Command', 16, 272), ('Sailing', 96, 272), ('Survey', 176, 272),
          ('Finance', 16, 296), ('Observe', 96, 296), ('Vigor', 176, 296),
          ('Aim', 16, 320), ('Swords', 96, 320), ('Speech', 176, 320), ('Guile', 16, 344)]


def main():
    assert not (ROOT / 'proof.json').exists()
    pre = read(ROOT / 'preflight.json')
    assert pre['runner_sha256'] == sha(Path('scripts/run_stat_plaques_v728.py').read_bytes())
    assert pre['shared_harness_sha256'] == sha(Path('scripts/headless_desmume_v193.py').read_bytes())
    for path, digest in pre['release_hashes'].items():
        assert sha(Path(path).read_bytes()) == digest
    for path, digest in ((pre['donor'], pre['donor_sha256']), (pre['original_donor'], pre['original_donor_sha256'])):
        assert sha(Path(path).read_bytes()) == digest
    current = NdsImage.open(ROM)
    arm = current.read_file('/__arm9__.bin')
    assert sha(arm) == pre['ARM9_sha256']
    font = GameAsciiFont.from_arm9(arm)
    previous_path = Path('work/analysis/plaque_review_v714/current_plaque_review_proof.json')
    previous = read(previous_path)
    assert previous['candidate_sha256'] == pre['candidate_sha256']
    definitions, font_masks = {}, []
    for group in read('translations/source_plaque_grain_v1.json')['files']:
        asset = PxlImage.from_bytes(current.read_file(group['file_path']))
        font_masks.extend(masks(asset, group['records'], font))
        for row in group['records']:
            definitions[row['id']] = (asset, row)
    assert len(font_masks) == 17
    plan = read('work/analysis/direct_equipment_v270/runtime_plan.json')
    pool = bytes(MainCodeFile(arm, 0x02000000).sections[3].data)
    at = plan['tile_pointer'] - POOL
    tile = pool[at:at + 1408]
    assert len(tile) == 1408
    reports, pictures, memories = {}, {}, {}
    fixture_rows, plaque_rows, hint_rows, stats, skill_rows = [], [], [], [], []
    for mode in ('disabled', 'zero', 'hundred'):
        folder = CAP / ('stat_plaques_v728_' + mode)
        report_path = folder / 'capture_report.json'
        report = read(report_path)
        assert report['frames'] == 9500 and report['cold_boot'] and not report['savestate_loaded']
        assert report['ROM_sha256'] == pre['candidate_sha256'] and report['core_DLL_sha256'] == CORE_SHA
        assert not report['callback_errors'] and report['scripted_input_schedule'] == read(pre['inputs'])
        assert report['stat_plaque_fixture_control_mode'] == mode
        assert report['battery_save_preloaded']['source_sha256'] == pre['donor_sha256']
        assert bool(report.get('synthetic_sailor_stat_display_fixture')) == (mode != 'disabled')
        receipts = read(folder / 'fixture_receipts.json')
        assert len(receipts) == 2
        for row in receipts:
            before, after = [Path(row[k]).read_bytes() for k in ('before_RAM_path', 'after_RAM_path')]
            assert len(before) == len(after) == 0x400000
            assert sha(before) == row['before_RAM_sha256'] and sha(after) == row['after_RAM_sha256']
            actor, values = actor_stats(arm, before)
            assert actor == row['actor_address'] and values == row['before_values']
            target = row['original_values'] if row['before_original_retro_run_frame'] == 7201 or mode == 'disabled' else [0 if mode == 'zero' else 100] * 6
            expected = bytearray(before)
            offset = actor + 8 - 0x02000000
            expected[offset:offset + 6] = bytes(target)
            assert after == bytes(expected) and row['after_values'] == target
            assert row['write_performed'] == (mode != 'disabled')
            native_before, native_after = row['native_before'], row['native_after']
            for native in (native_before, native_after):
                assert sha(Path(native['path']).read_bytes()) == native['sha256']
                assert native['read_only_export'] and not native['state_loaded']
                for region in native['regions'].values():
                    assert sha(Path(region['path']).read_bytes()) == region['sha256']
            assert native_before['ARM9_registers'] == native_after['ARM9_registers']
            assert native_before['ARM9_instruction_address'] == native_after['ARM9_instruction_address']
            for key in ('DTCM', 'ITCM'):
                assert native_before['regions'][key]['sha256'] == native_after['regions'][key]['sha256']
            fixture_rows.append({'mode': mode, 'before_frame': row['before_original_retro_run_frame'],
                'actor': actor, 'before_values': values, 'after_values': target,
                'whole_main_RAM_change_scope_and_exported_GPR_PC_TCM_checks_pass': True})
        shots = {r['frame']: r for r in report['frames_captured']}
        pictures[mode], memories[mode] = {}, {}
        for frame in FRAMES:
            assert sha(Path(shots[frame]['path']).read_bytes()) == shots[frame]['PNG_sha256']
            pictures[mode][frame] = Image.open(shots[frame]['path']).convert('RGB')
        for row in report['read_only_capture_RAM_snapshots']:
            raw = Path(row['path']).read_bytes()
            assert sha(raw) == row['sha256']
            memories[mode][row['frame']] = raw
        for old in previous['all18_current_native_review_entries'][:17]:
            asset, definition = definitions[old['id']]
            assert definition['english'] == old['English']
            left, top, right, bottom = old['bounds']
            frames = (4300,) if old['number'] <= 7 else (6300, 6700, 7100)
            for frame in frames:
                im = pictures[mode][frame]
                assert all(native5(im.getpixel((x, y))) == native5(asset.palette[asset.indices[y * asset.width + x]])
                           for y in range(top, bottom) for x in range(left, right))
                plaque_rows.append({'mode': mode, 'frame': frame, 'id': old['id'], 'text': old['English'],
                    'whole_native_letter_frame_material_pixels_exact': (right - left) * (bottom - top)})
        for frame, text, slot in ((6300, 'Equipped Items', 208), (6700, 'Weapon', 16), (7100, 'Blue Oak Shield', 64)):
            im = pictures[mode][frame]
            hint_rows.append({'mode': mode, 'frame': frame, **hint(font, tile, im, text, slot)})
            _, values = actor_stats(arm, memories[mode][frame])
            if mode != 'disabled':
                assert values == [0 if mode == 'zero' else 100] * 6
            for n, value in enumerate(values):
                # Fixed native baseline field: 3 cells at227,101+15*n. The2px
                # text inset is observed in the control, not a full-painter model.
                ink, bounds = complete_mask(font, f'{value:3d}', im, 227, 101 + n * 15, COLOR)
                assert bounds[2] <= 256 and bounds[3] <= 192
                stats.append({'mode': mode, 'frame': frame, 'attribute': n, 'value': value,
                    'complete_ink_pixels': ink, 'native_baseline_field_bounds': bounds,
                    'all_three_font_cells_including_blanks_and_first_final_digits_exact': True})
            for label, x, y in SKILLS:
                value = numeric_field(font, im, x + 42, y)
                ink, bounds = complete_mask(font, f'{label:>7}{value:3d}', im, x, y, COLOR)
                skill_rows.append({'mode': mode, 'frame': frame, 'English': label, 'observed_numeric_value': value,
                    'complete_ink_pixels': ink, 'bounds': bounds,
                    'whole_label_and_three_observed_digit_cells_exact_mechanics_not_inferred': True})
        restored_actor, restored_values = actor_stats(arm, memories[mode][7900])
        assert restored_actor == receipts[0]['actor_address'] and restored_values == receipts[0]['before_values']
        reports[mode] = {'path': str(report_path), 'sha256': sha(report_path.read_bytes()),
            'fixture_receipts': str(folder / 'fixture_receipts.json'),
            'fixture_receipts_sha256': sha((folder / 'fixture_receipts.json').read_bytes())}
    matched = []
    for mode in ('zero', 'hundred'):
        for frame in (4300, 5500, 5799, 7900, 8300, 8700, 9100, 9500):
            a, b = pictures['disabled'][frame], pictures[mode][frame]
            assert a.tobytes() == b.tobytes(), (mode, frame)
            matched.append({'mode': mode, 'frame': frame, 'whole_RGB256x384_exact': True})
    assert len(plaque_rows) == 111 and len(hint_rows) == 9 and len(stats) == 54 and len(skill_rows) == 90
    sheet = Image.new('RGB', (1536, 816), '#263238')
    draw = ImageDraw.Draw(sheet)
    for i, (mode, label) in enumerate((('disabled', 'Original stats / control'), ('zero', '0 / isolated display fixture'),
                                      ('hundred', '100 / isolated display fixture'))):
        draw.text((i * 512 + 12, 12), label, fill='white')
        sheet.paste(pictures[mode][6300].resize((512, 768), Image.Resampling.NEAREST), (i * 512, 40))
    sheet_path = ROOT / 'control_zero_hundred_review.png'
    sheet.save(sheet_path)
    proof = {'candidate': str(ROM), 'candidate_sha256': pre['candidate_sha256'],
        'three_terminal9500_frame_runs': reports, 'six_bounded_interventions_and_restores': fixture_rows,
        'all17_static_source_font_masks': font_masks, 'all111_native_static_plaque_crops': plaque_rows,
        'all_nine_complete_native_hints': hint_rows, 'all54_complete_stat_numeric_fields': stats,
        'all90_complete_skill_labels_and_observed_numeric_fields': skill_rows,
        'all16_whole_pre_fixture_and_restored_scene_RGB_pairs': matched,
        'observed_numeric_field_origin_not_claimed_as_full_parent_geometry_reconstruction': True,
        'saved_profile_Hodram_retained_localization_choice_Joakim_unchanged': True,
        'natural_growth_combat_skill_mechanics_or_all_attribute_values_not_verified': True,
        'review_sheet': str(sheet_path), 'review_sheet_sha256': sha(sheet_path.read_bytes()),
        'source_plaque_proof': str(previous_path), 'source_plaque_proof_sha256': sha(previous_path.read_bytes()),
        'runner_sha256': pre['runner_sha256'], 'verifier_sha256': sha(Path(__file__).read_bytes()),
        'release_hashes_unchanged': pre['release_hashes'],
        'all18_overall_audit_objects_remain_incomplete': True, 'full_goal_complete': False}
    for path, digest in pre['release_hashes'].items():
        assert sha(Path(path).read_bytes()) == digest
    save(ROOT / 'proof.json', proof)
    print('V728:111 complete plaque crops,9 hints,54 numeric fields,90 skills and16 whole restoration/control pairs pass; original stats restored.')


if __name__ == '__main__':
    main()
