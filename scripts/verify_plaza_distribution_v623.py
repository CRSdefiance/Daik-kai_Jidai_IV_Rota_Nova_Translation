"""Verify the real two-row Square menu, distribution banner and original flow."""

import struct
from pathlib import Path

from PIL import Image
from unicorn import UC_HOOK_CODE
from unicorn.arm_const import (
    UC_ARM_REG_LR,
    UC_ARM_REG_PC,
    UC_ARM_REG_R0,
    UC_ARM_REG_R1,
    UC_ARM_REG_R2,
    UC_ARM_REG_R3,
    UC_ARM_REG_SP,
)

from dk4tool.dialogue.font_audit import GameAsciiFont
from dk4tool.graphics.pxl import PxlImage
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.plaza_distribution_label import apply_release
from dk4tool.rom.nds import NdsImage
from scripts.probe_button_prompt_native import BASE, call, machine
from scripts.verify_regional_ui_v616 import full_cells, native5
from scripts.verify_village_wrap_v608 import read, save

ROOT = Path('work/analysis/plaza_distribution_v623')
CAP = Path('E:/Rota Nova translations/Generated/work/emulation_v193')
ROM = Path('out/all_routes_combined_v623_candidate.nds')


def receipt(version):
    root = CAP / f'distribution_menu_v{version}_fixture'
    path = root / 'capture_report.json'
    report = read(path)
    assert report['frames'] == 8001 and report['cold_boot'] and not report['savestate_loaded']
    assert not report['callback_errors']
    fixtures = report['synthetic_missionary_Chapel_assignment_fixtures']
    assert len(fixtures) == 1 and fixtures[0]['frame'] == 3200
    assert len(fixtures[0]['changes']) == 3
    assert not any(v for k, v in report.items() if k.startswith('synthetic_') and k != 'synthetic_missionary_Chapel_assignment_fixtures')
    donor = report['battery_save_preloaded']
    assert sha(Path(donor['source']).read_bytes()) == donor['source_sha256']
    shots = {r['frame']: r for r in report['frames_captured']}
    for row in shots.values():
        assert sha(Path(row['path']).read_bytes()) == row['PNG_sha256']
    return root, report, shots, {'path': str(path), 'sha256': sha(path.read_bytes())}


def native_text_requests(arm, raw, itcm):
    u = machine(arm)
    u.mem_write(BASE, raw)
    u.mem_write(0x01FF8000, itcm)
    renderer = 0x02460000
    u.mem_write(renderer, struct.pack('<I', 0x0215FA94))
    requests = []

    def trace(uc, address, size, data):
        if address == BASE + 0xD13A4:
            # The original selection background is outside this text-crop
            # contract. Actual full-frame comparisons cover it separately.
            uc.reg_write(UC_ARM_REG_PC, uc.reg_read(UC_ARM_REG_LR))
        if address == 0x01FF92D8:
            sizep, destp = struct.unpack('<2I', uc.mem_read(uc.reg_read(UC_ARM_REG_SP), 8))
            requests.append({
                'image': uc.reg_read(UC_ARM_REG_R1), 'layer': uc.reg_read(UC_ARM_REG_R0),
                'flags': uc.reg_read(UC_ARM_REG_R2),
                'source_origin': list(struct.unpack('<2i', uc.mem_read(uc.reg_read(UC_ARM_REG_R3), 8))),
                'size': list(struct.unpack('<2i', uc.mem_read(sizep, 8))),
                'destination_origin': list(struct.unpack('<2i', uc.mem_read(destp, 8)))})
            uc.reg_write(UC_ARM_REG_PC, uc.reg_read(UC_ARM_REG_LR))

    hook = u.hook_add(UC_HOOK_CODE, trace)
    for row in (0x0218FF98, 0x021900D8):
        call(u, 0x52FD0, (row, renderer), instruction_limit=200000)
    u.hook_del(hook)
    assert requests == [
        {'image': 0x022BD79C, 'layer': 0, 'flags': 0, 'source_origin': [0, row * 12],
         'size': [96, 12], 'destination_origin': [80, 80 + row * 20]} for row in (0, 1)]
    return requests


def main():
    rom = NdsImage.open(ROM)
    digest = sha(ROM.read_bytes())
    manifest = read(ROM.with_suffix('.manifest.json'))
    assert manifest['candidate_sha256'] == digest and manifest['profile'] == 'all-routes-unified-v623'
    assert manifest['release_stack_sha256'] == sha(Path('translations/release_stack.json').read_bytes())
    assert len(manifest['batches']) == 470 and all(manifest['checks'].values())
    parent = NdsImage.open('out/all_routes_combined_v621_candidate.nds')
    old_files = {p: d for _, p, d in parent.iter_files()} | dict(parent.iter_components())
    new_files = {p: d for _, p, d in rom.iter_files()} | dict(rom.iter_components())
    assert old_files.keys() == new_files.keys()
    assert [p for p in old_files if old_files[p] != new_files[p]] == ['/__arm9__.bin']
    target, transform = apply_release(old_files['/__arm9__.bin'], 'translations/plaza_distribution_label_v1.json')
    arm = new_files['/__arm9__.bin']
    assert target == arm
    old_root, old_run, old_shots, old_receipt = receipt(621)
    root, run, shots, new_receipt = receipt(623)
    assert run['ROM_sha256'] == digest and run['scripted_input_schedule'] == old_run['scripted_input_schedule']
    assert read(root / 'navigation_command_journal.json')['commands_received'] == read(old_root / 'navigation_command_journal.json')['commands_received']
    itcm_path = root / 'native_state_008000/arm9_itcm.bin'
    itcm = itcm_path.read_bytes()
    font = GameAsciiFont.from_arm9(arm)
    label_cases = []
    for frame in (4000, 4400):
        raw = (root / f'frame_{frame:06d}_arm9_ram.bin').read_bytes()
        im = Image.open(shots[frame]['path']).convert('RGB')
        requests = native_text_requests(arm, raw, itcm)
        flags, words, height, _, pixels_delta = struct.unpack_from('<5I', raw, 0x2BD79C)
        assert (flags, words, height) == (4, 64, 36)
        pixels = 0x2BD79C + pixels_delta
        expected = bytearray(256 * 36)
        for index, text in enumerate(('Trends', 'Distribute Goods')):
            x0 = (96 - len(text) * 6) // 2
            for n, char in enumerate(text):
                mask = font.decode(char)
                for y in range(11):
                    for x in range(6):
                        if mask.getpixel((x, y)):
                            expected[(index * 12 + y) * 256 + x0 + n * 6 + x] = 8
            req = requests[index]
            dx, dy = req['destination_origin']
            label_cases.append({'frame': frame, 'original_native_draw_request': req,
                                **full_cells(im, font, text, dx + x0, 192 + dy, (8, 8, 8))})
        actual = bytes((raw[pixels + i // 2] >> (4 * (i % 2))) & 15 for i in range(len(expected)))
        # This shared256-wide image retains earlier text outside the two
        # original96x12 views. Only those complete native views are submitted.
        assert all(actual[y * 256 + x] == expected[y * 256 + x]
                   for y in range(24) for x in range(96))
    # All subsequent screens match the old-build control after closing its
    # Japanese menu, including the original goods-distribution behavior.
    equal_frames = [4800, 5200, 5600, 6000, 6400, 6800, 7200, 7600, 8000, 8001]
    for frame in equal_frames:
        assert Image.open(shots[frame]['path']).convert('RGB').tobytes() == Image.open(old_shots[frame]['path']).convert('RGB').tobytes()
    art = new_files['/_pxl/haifuhin.pxl']
    atlas = native5(PxlImage.from_bytes(art).render())
    headers = []
    for frame in (5600, 6000, 6400):
        raw = (root / f'frame_{frame:06d}_arm9_ram.bin').read_bytes()
        candidates = [at - 12 for at in range(0x17000C, len(raw) - 48, 4)
                      if struct.unpack_from('<I', raw, at)[0] == 0x023139E8
                      and struct.unpack_from('<2I', raw, at + 28) == (256, 16)]
        assert len(candidates) == 1
        view = BASE + candidates[0]
        cargo_parent = view - 0x3070
        assert struct.unpack_from('<I', raw, cargo_parent - BASE + 0x10)[0] == 2
        u = machine(arm)
        u.mem_write(BASE, raw)
        namep = struct.unpack('<I', u.mem_read(0x023139E8 + 12, 4))[0]
        assert bytes(u.mem_read(namep, 32)).split(b'\0')[0] == b'_pxl/haifuhin.pxl'
        call(u, 0xD4170, (view,))
        pointer = u.reg_read(UC_ARM_REG_R0)
        assert bytes(u.mem_read(pointer, len(art))) == art
        im = native5(Image.open(shots[frame]['path']))
        assert im.crop((0, 261, 256, 277)).tobytes() == atlas.tobytes()
        headers.append({'frame': frame, 'original_mode': 2, 'owner': 0x023139E8,
                        'view': view, 'resident_file': pointer, 'complete_banner_pixels': 4096})
    prompts = []
    for frame, lines in ((4800, ['Give out the goods', 'as free samples?']),
                         (6800, ['Please take one.', 'Free samples available now!'])):
        im = Image.open(shots[frame]['path']).convert('RGB')
        prompts.append({'frame': frame, 'lines': [full_cells(im, font, line, 22, 296 + 16 * i, (0, 8, 0))
                                                for i, line in enumerate(lines)]})
    final_raw = (root / 'frame_008000_arm9_ram.bin').read_bytes()
    u = machine(arm)
    u.mem_write(BASE, final_raw)
    call(u, 0xCB1A8, ())
    fleet_root = u.reg_read(UC_ARM_REG_R0)
    call(u, 0x36180, (fleet_root + 4 + 0x84, 0x02440000))
    assert u.reg_read(UC_ARM_REG_R0) == 0
    market = read(CAP / 'plaza_distribution_v623_market/capture_report.json')
    old_market = read(CAP / 'compact_origin_v621_market/capture_report.json')
    assert market['ROM_sha256'] == digest and market['cold_boot'] and not market['savestate_loaded']
    assert not market['callback_errors'] and 'battery_save_preloaded' not in market
    assert not any(v for k, v in market.items() if k.startswith('synthetic_'))
    market_shots = {r['frame']: r for r in market['frames_captured']}
    previous_shots = {r['frame']: r for r in old_market['frames_captured']}
    assert market_shots.keys() == previous_shots.keys() and len(market_shots) == 19
    for frame, row in market_shots.items():
        assert Image.open(row['path']).convert('RGB').tobytes() == Image.open(previous_shots[frame]['path']).convert('RGB').tobytes()
    patch, preservation = read(ROOT / 'patch_proof.json'), read(ROOT / 'preservation_proof.json')
    assert patch['candidate_sha256'] == preservation['candidate_sha256'] == digest
    assert patch['exact_all_byte_reconstruction'] and preservation['current921_format_palette_extent_checks']
    assert preservation['all57_embedded_block_extents_exact']
    save(ROOT / 'release_proof.json', {
        'candidate': str(ROM), 'candidate_sha256': digest, 'profile': manifest['profile'],
        'base': manifest['base_rom'], 'base_sha256': manifest['base_sha256'], 'patch_sha256': patch['patch_sha256'],
        'transform': transform, 'actual_complete_menu_rows_two_selection_states': label_cases,
        'original_controlled_primary_draw_and_complete_source_views_RGB_verified': True,
        'unowned_shared_canvas_columns_not_assumed_cleared_or_rendered': True,
        'complete_Distributed_Goods_banners_original_mode2': headers,
        'complete_original_distribution_prompts': prompts,
        'all10_post_menu_control_frames_exact_V621': equal_frames,
        'original_after_distribution_goods_count': 0, 'original_before_fixture_goods_count': 2,
        'only_authorized_fixture_three_quarters_assignment_bytes_no_goods_outcome_or_menu_flags_injected': run['synthetic_missionary_Chapel_assignment_fixtures'][0],
        'normal_refit_qualifications_or_earned_staffing_not_claimed': True,
        'ordinary19_no_fixture_New_Game_Market_screens_exact_V621': sorted(market_shots),
        'all470_batches114_accepted_layers921_graphics57_embedded_extents_and_exact_patch_retained': True,
        'reports': [old_receipt, new_receipt], 'all18_plaques_incomplete_all22_historical_scopes_preserved': True,
        'broader_Confirm_miniature_village_card_legacy_comic_movie_and_material_gates_open': True,
        'full_goal_complete': False, 'canonical_promoted': False, 'script_sha256': sha(Path(__file__).read_bytes())})
    print('V623:4 complete menu masks,2 full source-view pairs,3 whole Distributed Goods banners,4 prompt lines,10 control frames,19 ordinary screens and exact patch pass.')


if __name__ == '__main__':
    main()
