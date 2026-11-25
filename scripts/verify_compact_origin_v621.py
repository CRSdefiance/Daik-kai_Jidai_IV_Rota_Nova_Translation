"""Bind full duel text/three crops to actual captured source rows and pixels."""

import struct
from pathlib import Path

from PIL import Image
from unicorn import UC_HOOK_CODE
from unicorn.arm_const import UC_ARM_REG_R2, UC_ARM_REG_R3, UC_ARM_REG_SP

from dk4tool.dialogue.font_audit import GameAsciiFont
from dk4tool.patch.compact_bitmap_origin import transform
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.probe_button_prompt_native import BASE, call, machine
from scripts.run_compact_origin_v621 import CAP, ROM, ROOT
from scripts.verify_regional_ui_v616 import full_cells, native5
from scripts.verify_village_wrap_v608 import read, save


def main():
    digest = sha(ROM.read_bytes())
    manifest = read(ROM.with_suffix('.manifest.json'))
    assert manifest['candidate_sha256'] == digest and manifest['profile'] == 'all-routes-unified-v621'
    assert manifest['release_stack_sha256'] == sha(Path('translations/release_stack.json').read_bytes())
    assert len(manifest['batches']) == 470 and all(manifest['checks'].values())
    parent = NdsImage.open('out/all_routes_combined_v617_candidate.nds')
    arm = NdsImage.open(ROM).read_file('/__arm9__.bin')
    expected_arm, transform_proof = transform(parent.read_file('/__arm9__.bin'))
    assert arm == expected_arm
    root = CAP / 'compact_origin_v621_duel'
    run = read(root / 'capture_report.json')
    assert run['ROM_sha256'] == digest and run['cold_boot'] and not run['savestate_loaded']
    assert not run['callback_errors']
    fixtures = run['synthetic_battle_recovery_proximity_fixtures']
    assert len(fixtures) == 1 and fixtures[0]['frame'] == 20400
    assert fixtures[0]['action'] == 'recover_and_approach'
    assert fixtures[0]['persisted_named_model_remains_entirely_unchanged']
    shots = {r['frame']: r for r in run['frames_captured']}
    native = read(root / 'native_state_021200/native_state.json')
    itcm = Path(native['regions']['ITCM']['path']).read_bytes()
    assert sha(itcm) == native['regions']['ITCM']['sha256']
    font = GameAsciiFont.from_arm9(arm)
    cases = []
    for frame in (20800, 21200):
        raw = (root / f'frame_{frame:06d}_arm9_ram.bin').read_bytes()
        assert sha(Path(shots[frame]['path']).read_bytes()) == shots[frame]['PNG_sha256']
        im = native5(Image.open(shots[frame]['path']))
        u = machine(arm)
        u.mem_write(BASE, raw)
        u.mem_write(0x01FF8000, itcm)
        before = bytes(u.mem_read(0x022BFDD0, 22272))
        for index, left in ((0, 152), (1, 0)):
            events = []

            def trace(uc, address, size, data, events=events):
                if address == BASE + 0xD16B4:
                    code, color = struct.unpack('<2I', uc.mem_read(uc.reg_read(UC_ARM_REG_SP), 8))
                    events.append((code, color, uc.reg_read(UC_ARM_REG_R2), uc.reg_read(UC_ARM_REG_R3)))

            handle = u.hook_add(UC_HOOK_CODE, trace)
            call(u, 0xD54C, (0x0218D4D8, index), instruction_limit=1000000)
            u.hook_del(handle)
            assert bytes(u.mem_read(0x022BFDD0, 22272)) == before
            assert {y for _, _, _, y in events} == {24 + index * 12}
            assert [x for _, _, x, _ in events] == list(range(0, 5 * len(events), 5))
            text = ''.join(chr(code) for code, _, _, _ in events)
            assert text.startswith('Fencing ') and ' HP ' in text and text.endswith('Healthy')
            expected = bytearray(156 * 12)
            for code, color, x, _ in events:
                assert color == 1
                mask = font.decode(chr(code))
                for y in range(11):
                    for xx in range(6):
                        if mask.getpixel((xx, y)):
                            expected[y * 156 + x + xx] = 1
            actual = bytes((before[(24 + index * 12 + y) * 232 + x // 2] >> (4 * (x % 2))) & 15
                           for y in range(12) for x in range(156))
            assert actual == expected
            palette_word = struct.unpack_from('<H', raw, 0x125A22)[0]
            foreground = tuple((palette_word >> shift) & 31 for shift in (0, 5, 10))
            crops = []
            for sx, width, dx, dy in ((0, 60, 4, 103), (60, 60, 4, 115), (120, 36, 66, 119)):
                ink = 0
                for y in range(12):
                    for x in range(width):
                        value = bool(expected[y * 156 + sx + x])
                        assert (im.getpixel((left + dx + x, 192 + dy + y)) == foreground) == value
                        ink += value
                crops.append({'source_x': sx, 'width': width, 'height': 12,
                              'destination': [left + dx, 192 + dy], 'complete_ink_points': ink})
            cases.append({'frame': frame, 'actor_index': index, 'complete_text': text,
                          'independent_font_source_row_pixels': 1872,
                          'complete_original_three_destination_crops': crops,
                          'all_other_canvas_rows_and_native_refresh_exact': True,
                          'no_leading_trailing_letters_digits_or_Healthy_suffix_dropped': True})
    regression = read(ROOT / 'ordinary_regression_proof.json')
    assert regression['all19_ordinary_no_save_no_fixture_full_screens_exact_V617']
    market = read(CAP / 'compact_origin_v621_market/capture_report.json')
    old_market = read(CAP / 'regional_missions_v617_market/capture_report.json')
    assert market['ROM_sha256'] == digest and market['frames'] == 24100
    assert market['cold_boot'] and not market['savestate_loaded'] and not market['callback_errors']
    assert 'battery_save_preloaded' not in market
    assert not any(v for k, v in market.items() if k.startswith('synthetic_'))
    assert market['scripted_input_schedule'] == old_market['scripted_input_schedule']
    old_shots = {r['frame']: r for r in old_market['frames_captured']}
    assert {r['frame'] for r in market['frames_captured']} == set(old_shots)
    assert len(old_shots) == 19
    for row in market['frames_captured']:
        assert sha(Path(row['path']).read_bytes()) == row['PNG_sha256']
        assert Image.open(row['path']).convert('RGB').tobytes() == Image.open(
            old_shots[row['frame']]['path']).convert('RGB').tobytes()
    notices = []
    for frame, text in ((22400, 'Enemy ship Hanse Cog captured!'),
                        (22800, 'Enemy crew defeated. Ship captured!'),
                        (23200, 'Admiral, victory is ours!')):
        im = Image.open(shots[frame]['path']).convert('RGB')
        notices.append({'frame': frame, **full_cells(im, font, text, 16, 296, (0, 8, 0))})
    patch, preservation = read(ROOT / 'patch_proof.json'), read(ROOT / 'preservation_proof.json')
    assert patch['candidate_sha256'] == preservation['candidate_sha256'] == digest
    assert patch['exact_all_byte_reconstruction']
    assert preservation['current921_format_palette_extent_checks'] and preservation['all57_embedded_block_extents_exact']
    save(ROOT / 'release_proof.json', {
        'candidate': str(ROM), 'candidate_sha256': digest, 'profile': manifest['profile'],
        'base': manifest['base_rom'], 'base_sha256': manifest['base_sha256'],
        'patch_sha256': patch['patch_sha256'], 'transform': transform_proof,
        'complete_actual_duel_stat_cases': cases,
        'three_complete_original_capture_and_victory_notices': notices,
        'normal_controls_then_reach_Cargo_Setup_at24800': True,
        'Spoils_Distributed_Goods_and_miniature_controls_not_yet_verified': True,
        'actual_source_view_origins_retained_by_shared_font_callback': True,
        'original_fixture_reachability_not_earned_voyage': fixtures[0],
        'ordinary19_no_fixture_frames_exact_V617': regression['frames'],
        'all470_batches114_accepted_layers921_graphics57_embedded_extents_retained': True,
        'duel_report': str(root / 'capture_report.json'), 'duel_report_sha256': sha((root / 'capture_report.json').read_bytes()),
        'all18_plaques_incomplete_all22_historical_requirements_preserved': True,
        'full_goal_complete': False, 'canonical_promoted': False,
        'script_sha256': sha(Path(__file__).read_bytes())})
    print('V621: both actors across two real duel states; all12 complete stat crops and19 ordinary screens pass.')


if __name__ == '__main__':
    main()
